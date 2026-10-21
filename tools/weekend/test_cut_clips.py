"""Checks cut_clips.py on a synthetic recording. Run: python -m unittest test_cut_clips"""

import array
import csv
import io
import math
import os
import random
import tempfile
import unittest
import wave
from contextlib import redirect_stdout

import cut_clips

RATE = 16000
T0 = 1_761_400_000_000.0  # logger clock at the start of the recording, epoch ms
CLAP_S = 3.25


def write_wav(path, seconds):
    rnd = random.Random(1)
    samples = array.array("h", (int(rnd.gauss(0, 200)) for _ in range(int(seconds * RATE))))
    for i in range(400):  # a clap: a sharp decaying burst
        samples[int(CLAP_S * RATE) + i] = int(20000 * math.exp(-i / 80) * (1 if i % 2 else -1))
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(samples.tobytes())


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


class CutClips(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.wav = os.path.join(d, "rec.wav")
        write_wav(self.wav, 60)
        sync = T0 + CLAP_S * 1000
        run = lambda rid, kind, a, b, dist: {
            "session": "S1", "run_id": rid, "type": kind, "distance_m": dist, "mic_height_m": "0.5",
            "start_ms": sync + a * 1000, "end_ms": sync + b * 1000, "gw_alarms": "1", "det_alarms": "0"}
        self.runs = os.path.join(d, "runs.csv")
        write_csv(self.runs, ["session", "run_id", "type", "distance_m", "mic_height_m", "start_ms", "end_ms", "gw_alarms", "det_alarms"], [
            run("R01", "hover", 5, 25, "100"),
            run("R02", "nodrone", 30, 50, ""),
            run("R03", "radio", 50, 55, "300"),
            run("R04", "speaker", 52, 58, "200"),
        ])
        self.events = os.path.join(d, "events.csv")
        ev = lambda t, src, kind, rid="": {"session": "S1", "run_id": rid, "t_ms": t, "source": src, "kind": kind}
        write_csv(self.events, ["session", "run_id", "t_ms", "source", "kind"], [
            ev(sync, "mark", "sync"),
            ev(sync + 10_000, "gateway", "alarm", "R01"),
            ev(sync + 15_000, "gateway", "clear", "R01"),
        ])
        self.out = os.path.join(d, "clips")

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *extra):
        with redirect_stdout(io.StringIO()):
            return cut_clips.main(["--runs", self.runs, "--events", self.events, "--recording", self.wav, "--out", self.out, *extra])

    def manifest(self):
        with open(os.path.join(self.out, "manifest.csv"), newline="") as f:
            return list(csv.DictReader(f))

    def test_clap_is_found(self):
        self.assertAlmostEqual(cut_clips.find_clap(self.wav, 20), CLAP_S, delta=0.002)

    def test_sync_cuts_labels_and_alarms(self):
        self.assertEqual(self.run_tool("--sync"), 0)
        rows = self.manifest()
        by = {}
        for r in rows:
            by.setdefault(r["label"], []).append(r)
        self.assertEqual(set(by), {"drone_100m", "background", "speaker_200m"})  # the radio walk is skipped
        self.assertEqual(len(by["speaker_200m"]), 2)  # 6 s run, 2 s trimmed each end
        self.assertEqual(len(by["drone_100m"]), 16)  # 20 s run, 2 s trimmed each end
        self.assertEqual(len(by["background"]), 16)
        alarmed = [r for r in by["drone_100m"] if r["batear_alarm"] == "1"]
        self.assertEqual(len(alarmed), 5)  # alarm from 10 s to 15 s into the hover
        first = by["drone_100m"][0]
        self.assertAlmostEqual(float(first["offset_s"]), CLAP_S + 7, delta=0.01)
        self.assertTrue(os.path.exists(os.path.join(self.out, first["clip"])))
        with wave.open(os.path.join(self.out, first["clip"])) as w:
            self.assertEqual(w.getnframes(), RATE)

    def test_start_time_matches_sync(self):
        start = cut_clips.iso(T0)
        self.assertEqual(self.run_tool("--start", start), 0)
        self.assertAlmostEqual(float(self.manifest()[0]["offset_s"]), CLAP_S + 7, delta=0.01)

    def test_same_run_same_fold(self):
        self.run_tool("--sync")
        folds = {(r["run_id"], r["fold"]) for r in self.manifest()}
        self.assertEqual(len(folds), 3)


if __name__ == "__main__":
    unittest.main()
