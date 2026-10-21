#!/usr/bin/env python3
"""Cut a weekend-test recording into labelled 1 s clips, using the logger's CSVs.

The weekend logger (logger.html) writes runs.csv (one row per run, with type,
distance, mic height, wind, start and stop times) and events.csv (every
reading, plus the Sync clap and Mark presses). This script lines a recording
up with the logger's clock, cuts each run into clips, files them by label, and
writes a manifest you can split by run for training.

Line the audio up one of two ways:

  --sync         Clap next to the recorder while pressing Sync clap. The script
                 finds the loudest transient near the start of the recording and
                 pins it to that press. Needs --events.
  --start ISO    The wall-clock time the recording started, e.g.
                 2026-10-25T10:03:12.5-04:00 (no offset = this machine's local time).

Labels: hover runs become drone_<distance>m, passes drone_pass, no-drone runs
background. Radio walks and bench checks are skipped.

Phone apps record .m4a; with ffmpeg on the PATH the script converts any input
(and --rate resamples). Without ffmpeg, give it a PCM .wav.

Standard library only. Example:

  python cut_clips.py --runs S20261025-1003_runs.csv --events S20261025-1003_events.csv \\
      --recording phone-0.5m.m4a --sync --tag mic05 --rate 16000 --out clips
"""

import argparse
import array
import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from datetime import datetime

LABELS = {"hover": None, "pass": "drone_pass", "nodrone": "background"}
MANIFEST_COLS = [
    "clip", "label", "session", "run_id", "fold", "tag", "recording", "offset_s", "clip_iso",
    "type", "distance_m", "altitude_m", "mic_height_m", "wind", "drone", "batear_alarm",
    "run_gw_alarms", "run_det_alarms",
]


def parse_time(text):
    """ISO time to epoch milliseconds. A time with no offset is local time."""
    dt = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.timestamp() * 1000.0


def iso(ms):
    return datetime.fromtimestamp(ms / 1000.0).astimezone().isoformat(timespec="milliseconds")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_wav(src, rate, workdir):
    """Return a PCM wav path for src, converting with ffmpeg when needed."""
    is_wav = src.lower().endswith(".wav")
    if is_wav and not rate:
        return src
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        if not is_wav:
            sys.exit(f"{src} is not a .wav and ffmpeg is not on the PATH. Install ffmpeg, "
                     "or convert it to a PCM .wav first.")
        print("ffmpeg not found: keeping the recording's own sample rate", file=sys.stderr)
        return src
    out = os.path.join(workdir, "converted.wav")
    cmd = [ffmpeg, "-v", "error", "-y", "-i", src, "-ac", "1"]
    if rate:
        cmd += ["-ar", str(rate)]
    cmd += ["-c:a", "pcm_s16le", out]
    subprocess.run(cmd, check=True)
    return out


def channel0(raw, width, channels):
    """Absolute sample values of the first channel, as a list of ints."""
    if width == 2:
        a = array.array("h"); a.frombytes(raw)
    elif width == 4:
        a = array.array("i"); a.frombytes(raw)
    elif width == 1:
        a = [b - 128 for b in raw]
    elif width == 3:
        a = [int.from_bytes(raw[i:i + 3], "little", signed=True) for i in range(0, len(raw) - 2, 3)]
    else:
        sys.exit(f"unsupported sample width {width}")
    if sys.byteorder == "big" and width in (2, 4):
        a.byteswap()
    return [abs(v) for v in a[::channels]]


def find_clap(path, window_s):
    """Seconds into the recording of the loudest transient in the first window_s."""
    with wave.open(path, "rb") as w:
        rate, width, ch = w.getframerate(), w.getsampwidth(), w.getnchannels()
        samples = channel0(w.readframes(int(window_s * rate)), width, ch)
    if not samples:
        sys.exit("the recording is empty")
    block = max(1, rate // 100)
    peaks = [max(samples[i:i + block]) for i in range(0, len(samples), block)]
    best = max(range(len(peaks)), key=peaks.__getitem__)
    floor = sorted(peaks)[len(peaks) // 2] or 1
    if peaks[best] < 8 * floor:
        print(f"warning: the loudest sound in the first {window_s:.0f} s is only "
              f"{peaks[best] / floor:.1f}x the median level; the clap may not be in the window",
              file=sys.stderr)
    # The clap's onset: first sample in that block, or the one before, above half its peak.
    start = max(0, (best - 1) * block)
    half = peaks[best] / 2
    for i in range(start, min(len(samples), (best + 1) * block)):
        if samples[i] >= half:
            return i / rate
    return best * block / rate


def alarm_intervals(events, session, run_id, end_ms):
    """[start, end) times when Batear was in alarm during a run, gateway or detector."""
    spans, on = [], {}
    for e in events:
        if e.get("session") != session or e.get("run_id") != run_id:
            continue
        src, kind = e.get("source"), e.get("kind")
        if src not in ("gateway", "detector"):
            continue
        t = float(e["t_ms"])
        if kind == "alarm" and src not in on:
            on[src] = t
        elif kind == "clear" and src in on:
            spans.append((on.pop(src), t))
    spans += [(t, end_ms) for t in on.values()]
    return spans


def fold_of(session, run_id, folds):
    return int(hashlib.sha1(f"{session}/{run_id}".encode()).hexdigest(), 16) % folds


def label_for(run):
    kind = run.get("type", "")
    if kind not in LABELS:
        return None
    if kind == "hover":
        d = run.get("distance_m", "")
        return f"drone_{float(d):g}m" if d else "drone_unknown"
    return LABELS[kind]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", required=True, help="runs.csv from the logger")
    ap.add_argument("--events", help="events.csv from the logger (needed for --sync and the batear_alarm column)")
    ap.add_argument("--recording", required=True, help="the audio file")
    when = ap.add_mutually_exclusive_group(required=True)
    when.add_argument("--start", help="wall-clock time the recording started (ISO 8601)")
    when.add_argument("--sync", action="store_true", help="align on a Sync clap")
    ap.add_argument("--sync-mark", type=int, default=1, help="which Sync clap press, counting from 1 (default 1)")
    ap.add_argument("--sync-window", type=float, default=120.0, help="seconds at the start to search for the clap")
    ap.add_argument("--out", default="clips", help="output folder (default clips)")
    ap.add_argument("--tag", default="", help="names this recorder, e.g. mic05; goes in file names and the manifest")
    ap.add_argument("--clip", type=float, default=1.0, help="clip length in seconds (default 1)")
    ap.add_argument("--hop", type=float, default=None, help="seconds between clip starts (default = --clip)")
    ap.add_argument("--trim", type=float, default=2.0, help="seconds dropped at each end of a run (default 2)")
    ap.add_argument("--rate", type=int, default=None, help="resample to this rate, e.g. 16000 (needs ffmpeg)")
    ap.add_argument("--folds", type=int, default=5, help="number of run-level folds (default 5)")
    args = ap.parse_args(argv)
    hop = args.hop or args.clip

    runs = read_csv(args.runs)
    events = read_csv(args.events) if args.events else []

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = to_wav(args.recording, args.rate, tmp)

        if args.sync:
            syncs = sorted(float(e["t_ms"]) for e in events if e.get("kind") == "sync")
            if not syncs:
                sys.exit("--sync needs --events with at least one Sync clap press")
            if not 1 <= args.sync_mark <= len(syncs):
                sys.exit(f"--sync-mark {args.sync_mark}: events.csv has {len(syncs)} Sync clap press(es): "
                         + ", ".join(iso(s) for s in syncs))
            clap_s = find_clap(wav_path, args.sync_window)
            rec_start = syncs[args.sync_mark - 1] - clap_s * 1000.0
            print(f"clap found {clap_s:.3f} s into the recording; recording started {iso(rec_start)}")
        else:
            rec_start = parse_time(args.start)

        with wave.open(wav_path, "rb") as w:
            rate, width, ch, nframes = w.getframerate(), w.getsampwidth(), w.getnchannels(), w.getnframes()
            rec_end = rec_start + nframes / rate * 1000.0
            clip_frames = int(round(args.clip * rate))

            os.makedirs(args.out, exist_ok=True)
            manifest = os.path.join(args.out, "manifest.csv")
            new_file = not os.path.exists(manifest)
            counts = {}
            with open(manifest, "a", newline="", encoding="utf-8") as mf:
                mw = csv.DictWriter(mf, fieldnames=MANIFEST_COLS)
                if new_file:
                    mw.writeheader()
                for run in runs:
                    label = label_for(run)
                    if not label or not run.get("end_ms"):
                        continue
                    r0, r1 = float(run["start_ms"]), float(run["end_ms"])
                    a, b = max(r0 + args.trim * 1000, rec_start), min(r1 - args.trim * 1000, rec_end)
                    if b - a < args.clip * 1000:
                        if r1 > rec_start and r0 < rec_end:
                            print(f"{run['run_id']}: too short after trimming, skipped", file=sys.stderr)
                        continue
                    if r0 + args.trim * 1000 < rec_start or r1 - args.trim * 1000 > rec_end:
                        print(f"{run['run_id']}: only partly inside the recording", file=sys.stderr)
                    spans = alarm_intervals(events, run.get("session"), run.get("run_id"), r1)
                    folder = os.path.join(args.out, label)
                    os.makedirs(folder, exist_ok=True)
                    t, n = a, 0
                    while t + args.clip * 1000 <= b + 1e-6:
                        offset = (t - rec_start) / 1000.0
                        w.setpos(int(round(offset * rate)))
                        frames = w.readframes(clip_frames)
                        if len(frames) < clip_frames * width * ch:
                            break
                        name = "_".join(x for x in (run.get("session", ""), run["run_id"], args.tag, f"{n:03d}") if x) + ".wav"
                        path = os.path.join(folder, name)
                        with wave.open(path, "wb") as o:
                            o.setnchannels(ch); o.setsampwidth(width); o.setframerate(rate)
                            o.writeframes(frames)
                        mid = t + args.clip * 500
                        mw.writerow({
                            "clip": os.path.relpath(path, args.out).replace(os.sep, "/"), "label": label,
                            "session": run.get("session", ""), "run_id": run["run_id"],
                            "fold": fold_of(run.get("session", ""), run["run_id"], args.folds),
                            "tag": args.tag, "recording": os.path.basename(args.recording),
                            "offset_s": f"{offset:.3f}", "clip_iso": iso(t), "type": run.get("type", ""),
                            "distance_m": run.get("distance_m", ""), "altitude_m": run.get("altitude_m", ""),
                            "mic_height_m": run.get("mic_height_m", ""), "wind": run.get("wind", ""),
                            "drone": run.get("drone", ""),
                            "batear_alarm": int(any(s <= mid < e for s, e in spans)),
                            "run_gw_alarms": run.get("gw_alarms", ""), "run_det_alarms": run.get("det_alarms", ""),
                        })
                        n += 1
                        t += hop * 1000
                    counts[label] = counts.get(label, 0) + n
    total = sum(counts.values())
    for k in sorted(counts):
        print(f"{k:>16}: {counts[k]} clips")
    print(f"{total} clips written to {args.out}; manifest {manifest}")
    if total == 0:
        print("No run overlapped the recording. Check the start time or the Sync clap.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
