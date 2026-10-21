"""Checks make_playback.py on a synthetic clip. Run: python -m unittest test_make_playback"""

import array
import csv
import io
import math
import os
import tempfile
import unittest
import wave
from contextlib import redirect_stderr, redirect_stdout

import make_playback

RATE = 8000


def write_tone(path, seconds=2.0, amp=0.3):
    s = array.array("h", (int(amp * 32767 * math.sin(2 * math.pi * 220 * i / RATE)) for i in range(int(seconds * RATE))))
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(s.tobytes())


def rms_db(path, skip_s=1.0):
    with wave.open(path) as w:
        a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
        n0 = int(skip_s * w.getframerate())
    mid = a[n0:len(a) - n0]
    return 10 * math.log10(sum(v * v for v in mid) / len(mid))


class MakePlayback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clip = os.path.join(self.tmp.name, "clip.wav")
        write_tone(self.clip)
        self.out = os.path.join(self.tmp.name, "out")

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *extra):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return make_playback.main(["--clip", self.clip, "--out", self.out, "--seconds", "5", *extra])

    def playlist(self):
        with open(os.path.join(self.out, "playlist.csv"), newline="") as f:
            return {r["file"]: r for r in csv.DictReader(f)}

    def test_cal_only_is_normalised_and_looped(self):
        self.assertEqual(self.run_tool("--cal-only"), 0)
        with wave.open(os.path.join(self.out, "cal.wav")) as w:
            self.assertEqual(w.getnframes(), 5 * RATE)
            a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
        peak = max(abs(v) for v in a) / 32767
        self.assertAlmostEqual(20 * math.log10(peak), -1.0, delta=0.1)

    def test_gains_follow_spreading(self):
        self.assertEqual(self.run_tool("--cal-spl", "66", "--source-lwa", "81", "--distances", "25,100,200"), 0)
        rows = self.playlist()
        self.assertEqual(len(rows), 3)
        cal = rms_db(os.path.join(self.out, "cal.wav"))
        for name, r in rows.items():
            x = float(r["distance_m"])
            want = 81 - 11 - 20 * math.log10(x)
            self.assertAlmostEqual(float(r["level_dba"]), want, places=1)
            self.assertAlmostEqual(rms_db(os.path.join(self.out, name)) - cal, want - 66, delta=0.15)
        # 100 m is 6 dB above 200 m
        g = {float(r["distance_m"]): float(r["gain_db"]) for r in rows.values()}
        self.assertAlmostEqual(g[100] - g[200], 20 * math.log10(2), delta=0.05)

    def test_levels_give_distances(self):
        self.run_tool("--cal-spl", "66", "--source-lwa", "81", "--levels", "30")
        (r,) = self.playlist().values()
        self.assertAlmostEqual(float(r["distance_m"]), 100.0, delta=0.2)

    def test_measured_source_level(self):
        self.run_tool("--cal-spl", "66", "--source-spl", "60", "--source-distance", "5", "--distances", "50")
        (r,) = self.playlist().values()
        self.assertAlmostEqual(float(r["level_dba"]), 40.0, places=1)

    def test_background_is_removed(self):
        self.run_tool("--cal-spl", "60", "--cal-background", "57", "--source-lwa", "81", "--distances", "100")
        (r,) = self.playlist().values()
        cal = 10 * math.log10(10 ** 6 - 10 ** 5.7)
        self.assertAlmostEqual(float(r["gain_db"]), 30 - cal, places=1)

    def test_too_loud_is_refused(self):
        with self.assertRaises(SystemExit):
            self.run_tool("--cal-spl", "40", "--source-lwa", "81", "--distances", "10")


if __name__ == "__main__":
    unittest.main()
