#!/usr/bin/env python3
"""Write level-matched WAVs that make a speaker sound like a drone at a chosen distance.

The idea: a drone at distance x reaches the mic at a predictable level. Play the
same drone sound through a speaker near the mic, turned down to exactly that
level, and the detector hears what it would hear at x (minus everything the path
does to the sound: ground, wind, trees). See the weekend test page, "Could a
speaker stand in for the drone?".

Steps:

1. Make the calibration file and play it through the speaker, volume set once
   and then left alone:
       python make_playback.py --clip mini-hover.wav --out playback --cal-only
2. Measure it at the mic with a sound level meter: A-weighting, slow, averaged
   over about 10 s. Note the background level with the speaker off, too.
3. Write the distance files from that reading:
       python make_playback.py --clip mini-hover.wav --out playback \\
           --cal-spl 66 --cal-background 38 --source-lwa 81 \\
           --distances 25,50,75,100,150,200,300
4. Play each file without touching the volume, and log each one in the logger as
   a Speaker run at that distance.

Level at the mic for a drone at x metres, free field (the drone is in the air):
    L(x) = LWA - 11 - 20*log10(x)        from a sound power level, e.g. EASA's label
    L(x) = SPL_ref - 20*log10(x / r_ref)  from your own measurement at r_ref
Each file's digital gain is L(x) minus the calibration reading. Air absorption is
left out: under about 1 dB at 300 m below 1 kHz, where rotor tones sit.

--levels writes files by level at the mic instead (a threshold sweep), with the
distance each level stands for.

Standard library only; ffmpeg converts any input that isn't a PCM .wav.
"""

import argparse
import array
import csv
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import wave

CAL_PEAK_DBFS = -1.0


def to_wav(src, workdir):
    if src.lower().endswith(".wav"):
        return src
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit(f"{src} is not a .wav and ffmpeg is not on the PATH. Install ffmpeg or convert it first.")
    out = os.path.join(workdir, "clip.wav")
    subprocess.run([ffmpeg, "-v", "error", "-y", "-i", src, "-c:a", "pcm_s16le", out], check=True)
    return out


def read_wav(path):
    """Return (rate, channels, samples as floats in [-1, 1], interleaved)."""
    with wave.open(path, "rb") as w:
        rate, width, ch, n = w.getframerate(), w.getsampwidth(), w.getnchannels(), w.getnframes()
        raw = w.readframes(n)
    if width == 2:
        a = array.array("h"); a.frombytes(raw); scale = 32768.0
    elif width == 4:
        a = array.array("i"); a.frombytes(raw); scale = 2147483648.0
    elif width == 3:
        a = [int.from_bytes(raw[i:i + 3], "little", signed=True) for i in range(0, len(raw) - 2, 3)]; scale = 8388608.0
    elif width == 1:
        a = [b - 128 for b in raw]; scale = 128.0
    else:
        sys.exit(f"unsupported sample width {width}")
    if sys.byteorder == "big" and width in (2, 4):
        a.byteswap()
    return rate, ch, [v / scale for v in a]


def write_wav(path, rate, ch, samples, rng):
    """16-bit with TPDF dither, so the quiet far-distance files keep their detail."""
    out = array.array("h", bytes(2 * len(samples)))
    for i, v in enumerate(samples):
        s = v * 32767.0 + rng.random() - rng.random()
        out[i] = 32767 if s > 32767 else -32768 if s < -32768 else int(round(s))
    if sys.byteorder == "big":
        out.byteswap()
    with wave.open(path, "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(out.tobytes())


def loop_to(samples, ch, rate, seconds, fade_s=0.05):
    """Repeat the clip to `seconds`, crossfading each join so it doesn't click."""
    frames = len(samples) // ch
    want = int(seconds * rate)
    if want <= frames:
        return samples[:want * ch]
    fade = min(int(fade_s * rate), frames // 4)
    out = list(samples)
    while len(out) // ch < want:
        start = len(out) // ch - fade
        for f in range(fade):
            g = f / fade
            for c in range(ch):
                i = (start + f) * ch + c
                out[i] = out[i] * (1 - g) + samples[f * ch + c] * g
        out.extend(samples[fade * ch:])
    return out[:want * ch]


def ramp(samples, ch, rate, ramp_s=0.5):
    """Fade in and out, so starting and stopping a file doesn't make a click."""
    n = len(samples) // ch
    r = min(int(ramp_s * rate), n // 2)
    for f in range(r):
        g = f / r
        for c in range(ch):
            samples[f * ch + c] *= g
            samples[(n - 1 - f) * ch + c] *= g
    return samples


def energy_minus(total_db, background_db):
    """Remove the background's contribution from a meter reading."""
    diff = total_db - background_db
    if diff < 3:
        sys.exit(f"the calibration reading is only {diff:.1f} dB above the background; turn the speaker up "
                 "or move it closer, and measure again (it needs to be at least 10 dB above)")
    if diff < 10:
        print(f"warning: calibration only {diff:.1f} dB above background; corrected, but less certain", file=sys.stderr)
    return 10 * math.log10(10 ** (total_db / 10) - 10 ** (background_db / 10))


def source_at(x, args):
    if args.source_lwa is not None:
        return args.source_lwa - 11 - 20 * math.log10(x)
    return args.source_spl - 20 * math.log10(x / args.source_distance)


def distance_for(level, args):
    if args.source_lwa is not None:
        return 10 ** ((args.source_lwa - 11 - level) / 20)
    return args.source_distance * 10 ** ((args.source_spl - level) / 20)


def parse_list(text):
    return [float(v) for v in text.replace(" ", "").split(",") if v]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clip", required=True, help="a recording of the drone hovering, steady")
    ap.add_argument("--out", default="playback", help="output folder (default playback)")
    ap.add_argument("--cal-only", action="store_true", help="only write cal.wav, to play and measure")
    ap.add_argument("--cal-spl", type=float, help="meter reading at the mic while cal.wav plays, dB(A)")
    ap.add_argument("--cal-background", type=float, help="meter reading at the mic with the speaker off, dB(A)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--source-lwa", type=float, help="the drone's sound power, dB(A); DJI Mini 4 Pro: 81 (EASA)")
    src.add_argument("--source-spl", type=float, help="the drone's level you measured at --source-distance, dB(A)")
    ap.add_argument("--source-distance", type=float, default=1.0, help="distance of --source-spl, m (default 1)")
    ap.add_argument("--distances", help="comma list of distances to emulate, m, e.g. 25,50,100,200")
    ap.add_argument("--levels", help="comma list of levels at the mic, dB(A), for a threshold sweep, e.g. 40,36,32,28,24")
    ap.add_argument("--seconds", type=float, default=60.0, help="length of each file, s (default 60)")
    ap.add_argument("--seed", type=int, default=1, help="dither seed")
    args = ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        rate, ch, clip = read_wav(to_wav(args.clip, tmp))
    if not clip:
        sys.exit("the clip is empty")
    peak = max(abs(v) for v in clip)
    if peak == 0:
        sys.exit("the clip is silent")
    norm = 10 ** (CAL_PEAK_DBFS / 20) / peak
    base = ramp(loop_to([v * norm for v in clip], ch, rate, args.seconds), ch, rate)
    rng = random.Random(args.seed)
    os.makedirs(args.out, exist_ok=True)

    cal_path = os.path.join(args.out, "cal.wav")
    write_wav(cal_path, rate, ch, base, rng)
    print(f"wrote {cal_path}: play it, measure at the mic, then rerun with --cal-spl")
    if args.cal_only:
        return 0

    if args.cal_spl is None:
        sys.exit("--cal-spl is required (or use --cal-only first)")
    if args.source_lwa is None and args.source_spl is None:
        sys.exit("give the drone's level: --source-lwa (sound power) or --source-spl with --source-distance")
    if not args.distances and not args.levels:
        sys.exit("give --distances, --levels, or both")
    cal = args.cal_spl if args.cal_background is None else energy_minus(args.cal_spl, args.cal_background)

    targets = [(x, source_at(x, args)) for x in parse_list(args.distances or "")]
    targets += [(distance_for(lv, args), lv) for lv in parse_list(args.levels or "")]
    if any(x <= 0 for x, _ in targets):
        sys.exit("distances must be above zero")

    rows = []
    for x, level in sorted(targets):
        gain = level - cal
        if gain > 0:
            sys.exit(f"{x:.0f} m needs {level:.1f} dB(A) at the mic, {gain:.1f} dB louder than the calibration. "
                     "Turn the speaker up or move it closer, then measure cal.wav again.")
        name = f"speaker_{x:04.0f}m_{level:.0f}dBA.wav"
        g = 10 ** (gain / 20)
        write_wav(os.path.join(args.out, name), rate, ch, [v * g for v in base], rng)
        rows.append({"file": name, "distance_m": f"{x:.1f}", "level_dba": f"{level:.1f}", "gain_db": f"{gain:.1f}"})
        quiet = args.cal_background is not None and level < args.cal_background
        print(f"{name}: {x:7.1f} m  {level:5.1f} dB(A) at the mic  gain {gain:6.1f} dB"
              + ("  (quieter than the background: expected at range)" if quiet else ""))

    with open(os.path.join(args.out, "playlist.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "distance_m", "level_dba", "gain_db"])
        w.writeheader()
        w.writerows(rows)
    print(f"calibration {cal:.1f} dB(A) at the mic; {len(rows)} files and playlist.csv in {args.out}")
    print("Leave the speaker's volume exactly where it was when you measured cal.wav.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
