"""Band model: long nylon loops on cheap rods that carry a fibre FPV's line into fixed blades.

The line is hand-laid. The band is 80 lb nylon monofilament, a closed loop out and back. Every
1,320 ft of line has one drive post in its middle: a 12 V car power-window motor turning a printed
pulley for the loop on each side. Each loop runs 660 ft to an idler post, a T-post with a printed
pulley, shared with the next section's loop. Between them the line rides in printed guide heads
on 3/8 in fibreglass fence rods, one every 50 ft, top run about 32 in up and the return run under
it. Small printed catchers with three soft forward-leaning spurs are crimped to the line every 3 ft.
A fibre that falls across the top run is caught by the next catcher and carried to the next rod,
where two snapped-off utility blade segments stand either side of the line. The catcher pulls the
fibre between them and its two sides, hanging over the line, are drawn onto the edges and cut.

It runs only when the tripwire's radio trigger says a drone is near, plus one clearing stroke an
hour (one rod spacing) for a drone that lands and waits. A box that stops hearing the trigger's
heartbeat runs clearing strokes more often, so jamming the link slows the line but never stops it.

Prints: sag, line speed, the longest wait from a fibre landing to its cut and how far out the line
must sit, drag, torque and power at a drive post, the daily energy budget, and parts per mile.

    py band_model.py [--rod 50] [--loop 660] [--rpm 90] [--pulley 8] [--catch 3] [--cut-lb 0.5]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement. The drag per
guide and the cut force set the motor and the power, and both are guesses until tested.
"""
import argparse, math

MILE = 5280.0
LBF = 4.448
DRONE_MPH = 43.0           # a fibre FPV's top speed (threat-profile)

# ---- the band ---------------------------------------------------------------------------------
LINE = "80 lb nylon monofilament, about 0.04 in"
LINE_LB_FT = 0.0006        # 0.79 mm2 of nylon at 1.14 g/cm3
LINE_BREAK_LB = 80
LINE_PER_FT = 0.012        # bulk spools (est.)
TENSION_LB = 10.0          # set at the idler ASSUME
MISALIGN_DEG = 1.0         # rods off a straight line, so the line presses on each guide ASSUME
MU = 0.15                  # nylon on a smooth printed guide ASSUME
CATCH_LB = 0.01            # a catcher pushing through a guide or the blades ASSUME
CUT_LB = 0.5               # extra pull while a fibre is drawn onto the blades ASSUME (R4)

# ---- the drive --------------------------------------------------------------------------------
MOTOR = "12 V car power-window motor (worm, sealed)"
MOTOR_EFF = 0.4            # ASSUME
EVENT_MIN = 3              # minutes of running per trigger: the drone crosses in seconds

# ---- power, one drive post ---------------------------------------------------------------------
PANEL_W = 20               # 12 V 20 W panel
BATT_WH = 84               # 12 V 7 Ah sealed lead-acid: charges in frost, unlike lithium
BATT_USABLE = 0.5          # lead-acid lasts if held above half charge
STANDBY_W = 0.072          # 6 mA at 12 V: controller, MCU asleep, LoRa listening in bursts ASSUME
WINTER_SUN_H = 1.5         # full-sun hours a day in a Ukrainian December ASSUME
SOLAR_EFF = 0.7            # panel to battery, PWM controller, dirt ASSUME

# ---- parts, $ each, small batch (retail listings 2026-10 unless est.) --------------------------
P_ROD = 2.0                # 3/8 x 48 in fibreglass fence rod, $1.99-2.49
P_GUIDE = 0.4              # printed guide head: two eyes and a blade holder (est.)
P_BLADES = 0.1             # two segments snapped off an 18 mm utility blade (est.)
P_CATCH = 0.03             # printed TPU catcher and a fishing crimp sleeve (est.)
P_TPOST = 7.0              # 5.5 ft studded steel T-post
P_IDLER = 2.0              # printed pulley head, two 608 bearings (est.)
P_END = 16                 # each end of the line: spiral earth anchor and guy (est.)
DRIVE = [                  # one drive post
    ("T-post", P_TPOST),
    (MOTOR + ", aftermarket", 15),
    ("12 V 20 W panel", 20),
    ("12 V 7 Ah sealed lead-acid", 18),
    ("PWM solar controller, low-voltage cutoff", 5),
    ("ESP32-C3 SuperMini and Ra-01H LoRa (868 MHz)", 9),
    ("relay or MOSFET driver, fuse, wire, glands", 4),
    ("IP65 junction box", 3),
    ("printed head, two 8 in pulleys, bearings (est.)", 4),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rod", type=float, default=50.0, help="ft between guide rods (each has blades)")
    ap.add_argument("--loop", type=float, default=660.0, help="ft of line one loop covers, drive to idler")
    ap.add_argument("--rpm", type=float, default=90.0, help="drive pulley rpm under load ASSUME")
    ap.add_argument("--pulley", type=float, default=8.0, help="in, drive pulley diameter")
    ap.add_argument("--catch", type=float, default=3.0, help="ft between catchers on the line")
    ap.add_argument("--cut-lb", type=float, default=CUT_LB, help="lbf to draw a fibre through the blades ASSUME")
    a = ap.parse_args()

    sag_in = LINE_LB_FT * a.rod ** 2 / (8 * TENSION_LB) * 12
    print(f"{LINE} on rods every {a.rod:.0f} ft: sag {sag_in:.1f} in at {TENSION_LB:.0f} lb "
          f"({TENSION_LB / LINE_BREAK_LB:.0%} of break).")

    fps = a.rpm * math.pi * a.pulley / 12 / 60
    wait_s = (a.catch + a.rod) / fps
    drone_fps = DRONE_MPH * 5280 / 3600
    print(f"\nLine speed {fps:.1f} ft/s ({a.rpm:.0f} rpm on an {a.pulley:.0f} in pulley).")
    print(f"  Longest wait from a fibre landing to its cut: a catcher {a.catch:.0f} ft away, then one rod "
          f"spacing: {wait_s:.0f} s.")
    print(f"  A drone at {DRONE_MPH:.0f} mph flies {wait_s * drone_fps:,.0f} ft meanwhile, so that is how far "
          f"out the line must sit.")

    # drag of one loop: both runs press on every guide, and every catcher pushes through guides and blades
    n = math.hypot(LINE_LB_FT * a.rod, 2 * TENSION_LB * math.sin(math.radians(MISALIGN_DEG)))
    guides = a.loop / a.rod
    drag = 2 * guides * MU * n + 2 * a.loop / a.catch * CATCH_LB * a.catch / a.rod
    loop_lb = drag + a.cut_lb
    post_lb = 2 * drag + a.cut_lb
    kgcm = post_lb * a.pulley / 2 * LBF * 2.54 / 9.81
    w_run = 2 * drag * LBF * fps * 0.3048 / MOTOR_EFF
    w_cut = post_lb * LBF * fps * 0.3048 / MOTOR_EFF
    print(f"\nOne {a.loop:.0f} ft loop drags {drag:.1f} lbf empty, {loop_lb:.1f} lbf cutting "
          f"(tension {TENSION_LB:.0f} lb holds it).")
    print(f"  Drive post, two loops: {post_lb:.1f} lbf, {kgcm:.0f} kg cm at the shaft; {w_run:.0f} W running, "
          f"{w_cut:.0f} W cutting. A window motor is rated about 30 kg cm.")

    event_wh = w_cut * EVENT_MIN / 60
    clear_wh = w_run * (a.rod + a.catch) / fps / 3600 * 24
    standby_wh = STANDBY_W * 24
    panel_wh = PANEL_W * WINTER_SUN_H * SOLAR_EFF
    spare = panel_wh - standby_wh - clear_wh
    print(f"\nEnergy a day, one drive post: standby {standby_wh:.1f} Wh, hourly clearing strokes {clear_wh:.1f} Wh.")
    print(f"  A {PANEL_W} W panel makes about {panel_wh:.0f} Wh on a December day, leaving {spare:.0f} Wh: "
          f"{spare / event_wh:.0f} triggers a day at {event_wh:.1f} Wh ({EVENT_MIN} min each).")
    print(f"  The battery holds {BATT_WH * BATT_USABLE:.0f} Wh above half charge: "
          f"{BATT_WH * BATT_USABLE / (standby_wh + clear_wh):.0f} sunless days, or "
          f"{BATT_WH * BATT_USABLE / event_wh:.0f} triggers.")

    drives = math.ceil(MILE / (2 * a.loop))
    loops = 2 * drives
    idlers = drives + 1
    rods = math.ceil(MILE / a.rod) - drives - idlers + 1
    line_ft = loops * (2 * a.loop + 10)
    catches = math.ceil(line_ft / a.catch)
    drive_each = sum(c for _, c in DRIVE)
    parts = [
        (f"{LINE}, {line_ft:,.0f} ft", line_ft * LINE_PER_FT),
        (f"Catchers and crimps, {catches:,}", catches * P_CATCH),
        (f"Fibreglass rods with guide heads and blades, {rods}", rods * (P_ROD + P_GUIDE + P_BLADES)),
        (f"Idler posts, {idlers}: T-post and pulley head", idlers * (P_TPOST + P_IDLER)),
        (f"Drive posts, {drives} at ${drive_each:.0f}", drives * drive_each),
        ("End anchors and guys, 2", 2 * P_END),
    ]
    total = sum(c for _, c in parts)
    print(f"\nA mile: {loops} loops, {drives} drive posts, small-batch parts (est.):")
    for name, c in parts:
        print(f"  {name:58s} ${c:5,.0f}")
    print(f"  {'Total':58s} ${total:5,.0f}")
    print("\nOne drive post:")
    for name, c in DRIVE:
        print(f"  {name:58s} ${c:3.0f}")


if __name__ == "__main__":
    main()
