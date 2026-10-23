"""Laser model: how long a laser has to stay on a fibre FPV's line to cut it.

The line is 0.25 mm of acrylate coating over 0.125 mm of glass. To cut it, a beam has to burn off
the coating and soften the glass through; it lies slack, so nothing snaps it. A beam wider than
the line wastes most of its power, so the dwell depends on the spot size, and the spot depends on
the range and the optics.

The road case: a drone parked by the road is visible, and its line runs from it to its pilot. So
any loop drawn around the drone must cross the line. The beam traces a loop around the drone; aim
errors only bend the loop.

Prints: energy per mm, dwell and sweep speed for a set of lasers, the spot at range, how long a
loop around a parked drone takes, and the light a camera's lens would focus onto its sensor.

    py laser_model.py [--power 100] [--absorb 0.3] [--range 300] [--loop 24]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement. Heat lost from
the line while the beam is on it is ignored, so every dwell here is a lower bound.
"""
import argparse, math

# ---- the line --------------------------------------------------------------------------------
LINE_MM = 0.25          # coated diameter (vendor listings: 0.25-0.28 mm)
GLASS_MM = 0.125        # bare glass
COAT_DENSITY = 1.1      # g/cm3, acrylate
GLASS_DENSITY = 2.2     # g/cm3, silica
COAT_CP = 1.5           # J/g/K ASSUME
COAT_RISE_K = 250       # to about 270 F above ambient, where acrylate breaks down (~500 F)
COAT_DECOMP_J_G = 1000  # to break it down and burn it off ASSUME
GLASS_CP = 1.0          # J/g/K, silica at high temperature, about
GLASS_RISE_K = 1600     # to soften it, about 2,900 F

# ---- the beam ---------------------------------------------------------------------------------
LASERS = [              # (name, watts, spot mm)
    ("10 W blue engraving diode, close up", 10, 2.0),
    ("10 W blue engraving diode, wide spot", 10, 10.0),
    ("100 W fibre laser, tight spot", 100, 2.0),
    ("100 W fibre laser, 5 mm spot", 100, 5.0),
]
APERTURE_MM = 50        # a 2 in output lens ASSUME
WAVE_UM = {"1 um fibre laser": 1.07, "CO2": 10.6}
FT = 0.3048


def energy_per_mm():
    """Joules to clear 1 mm of the line: burn off its coating, then soften its glass."""
    coat_cm3 = math.pi / 4 * (LINE_MM ** 2 - GLASS_MM ** 2) * 1 / 1000
    glass_cm3 = math.pi / 4 * GLASS_MM ** 2 * 1 / 1000
    coat = coat_cm3 * COAT_DENSITY * (COAT_CP * COAT_RISE_K + COAT_DECOMP_J_G)
    glass = glass_cm3 * GLASS_DENSITY * GLASS_CP * GLASS_RISE_K
    return coat, glass


def dwell(watts, spot_mm, absorb):
    """Seconds the beam must stay on the line, and the fastest it can sweep across it (mm/s)."""
    caught = 4 * LINE_MM / (math.pi * spot_mm)        # share of a round flat-top beam the line crosses
    w_per_mm = watts * caught * absorb / spot_mm
    coat, glass = energy_per_mm()
    t = (coat + glass) / w_per_mm
    return caught, t, spot_mm / t


def spot_at(range_ft, wave_um):
    """Smallest spot, in mm, a perfect beam from the aperture can make at that range."""
    return 2.44 * wave_um * 1e-6 * range_ft * FT / (APERTURE_MM / 1000) * 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--power", type=float, default=100.0, help="watts, for the loop and the camera")
    ap.add_argument("--absorb", type=float, default=0.3, help="share of the light the line absorbs ASSUME")
    ap.add_argument("--range", type=float, default=300.0, help="ft from the laser to the drone")
    ap.add_argument("--loop", type=float, default=24.0, help="in, width of the loop around the drone (a 7-10 in FPV and its arms)")
    a = ap.parse_args()

    coat, glass = energy_per_mm()
    print(f"To clear 1 mm of line: coating {coat * 1000:.0f} mJ + glass {glass * 1000:.0f} mJ "
          f"= {(coat + glass) * 1000:.0f} mJ (heat loss ignored, so more in practice).\n")

    print(f"Laser                                    spot      line catches  dwell    fastest sweep  ({a.absorb:.0%} absorbed)")
    for name, w, s in LASERS:
        caught, t, v = dwell(w, s, a.absorb)
        print(f"  {name:38s} {s / 25.4:.2f} in   {caught:5.1%}        {t:6.2f} s  {v / 25.4:5.2f} in/s")

    print("\nSmallest spot from a 2 in lens (a perfect beam; real lasers are wider):")
    for label, wl in WAVE_UM.items():
        cells = "   ".join(f"{r:.0f} ft: {spot_at(r, wl) / 25.4:.2f} in" for r in (100, 300))
        print(f"  {label:18s} {cells}")

    spot = max(spot_at(a.range, WAVE_UM["1 um fibre laser"]), 2.0)
    caught, t, v = dwell(a.power, spot, a.absorb)
    loop_mm = math.pi * a.loop * 25.4
    print(f"\nLoop around a parked drone: {a.power:.0f} W at {a.range:.0f} ft, spot {spot / 25.4:.2f} in, "
          f"a {a.loop:.0f} in loop ({loop_mm / 25.4:.0f} in around) at {v / 25.4:.2f} in/s "
          f"takes {loop_mm / v:.0f} s to be sure of crossing the line.")

    # a camera's lens focuses what enters it onto a spot a few pixels wide
    beam_mm, lens_mm, focus_um = 20.0, 3.0, 10.0      # a cheap diode's beam at 100 ft, an FPV lens, the focused spot ASSUME
    for w in (1, 5):
        into = w * (lens_mm / beam_mm) ** 2
        irr = into / (math.pi / 4 * (focus_um * 1e-4) ** 2)
        print(f"Camera: {w} W in a {beam_mm / 25.4:.1f} in beam puts {into * 1000:.0f} mW through a "
              f"{lens_mm:.0f} mm lens, about {irr:,.0f} W/cm2 on the sensor "
              f"(reported damage to colour CMOS: 40,000-60,000 W/cm2 in 0.25 s).")


if __name__ == "__main__":
    main()
