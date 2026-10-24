"""Band model: short strap loops between posts, each driven by its own small solar motor, that carry
a fibre FPV's line into fixed blades.

The line is hand-laid: 5.5 ft steel T-posts driven 2 ft, one every span. Between each pair of posts
runs one closed loop of 1/2 in polyester pallet strapping, on a pulley at each post, in an upright
plane: the top run is about 32 in up and the return run sits under it. Printed hooks are riveted to
the strap's outside face, so on the top run they point up. Every other post is a drive post: one
12 V gearmotor turns a shaft with a pulley for the span on each side. The posts between are idlers.
A fibre that falls across a top run is caught by the next hook and carried to the end of the span,
where two utility blades stand either side of the strap. The hook pulls the fibre through between
them and the fibre's two sides, hanging over the strap, are drawn onto the edges and cut.

It runs only when the tripwire's radio trigger says a drone is near, plus one clearing pass an hour
for a drone that lands and waits. A box that stops hearing the trigger's heartbeat runs clearing
passes more often, so jamming the link slows the line down but never switches it off.

Prints: strap sag, belt speed, the longest wait from a fibre landing to its cut and how far out the
line must sit, the torque and power at each drive post, the daily energy budget, and parts per mile.

    py band_model.py [--span 33] [--rpm 85] [--pulley 6] [--hook 12] [--cut-lb 0.5] [--drag-lb 0.3]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement. The cut force and
the drag per loop set the motor, and both are guesses until tested.
"""
import argparse, math

MILE = 5280.0
LBF = 4.448
DRONE_MPH = 43.0           # a fibre FPV's top speed (threat-profile)

# ---- the strap and hooks ----------------------------------------------------------------------
STRAP_LB_FT = 0.0083       # 1/2 x 0.028 in PET strapping: 9 mm2 at 1.38 g/cm3
STRAP_BREAK_LB = 800       # listings, 1/2 in x 0.027-0.028 in, 6,500 ft coils
STRAP_PER_FT = 0.015       # $65-150 a 6,500 ft coil (listings 2026-10)
TENSION_LB = 5.0           # pretension in each loop, set at the idler ASSUME
SEAL_LOSS_FT = 1.0         # overlap at the crimped seal that closes each loop

# ---- the drive --------------------------------------------------------------------------------
MOTOR = "JGB37-3530 12 V, 107 rpm no load"
MOTOR_RATED_KGCM = 4.0     # rated torque, sellers' figures disagree: MEASURE
DRAG_LB = 0.3              # strap over two pulleys and hooks through the blades, per loop ASSUME (R3)
CUT_LB = 0.5               # extra pull while a fibre is drawn onto the blades ASSUME (R4)
MOTOR_EFF = 0.35           # small spur gearmotor, motor x gearbox ASSUME
EVENT_MIN = 10             # minutes of running per trigger

# ---- power, one drive post ---------------------------------------------------------------------
PANEL_W = 5                # 12 V 5 W panel
BATT_WH = 14.4             # 12 V 1.2 Ah sealed lead-acid: charges in frost, unlike lithium
BATT_USABLE = 0.5          # lead-acid lasts if held above half charge
STANDBY_W = 0.072          # 6 mA at 12 V: charge controller, LDO, MCU asleep, LoRa listening in bursts ASSUME
WINTER_SUN_H = 1.5         # full-sun hours a day in a Ukrainian December ASSUME
SOLAR_EFF = 0.7            # panel to battery, PWM controller, dirt ASSUME

# ---- parts, $ each, small batch (retail listings 2026-10 unless est.) --------------------------
P_TPOST = 7.0              # 5.5 ft studded steel T-post with anchor plate
P_END = 16                 # each end: a spiral earth anchor and a guy line (est.)
P_HOSE_CLAMP = 1.0         # stainless worm-gear clamp that locks a head to its post (est.)
DRIVE = [                  # one drive post's head
    ("gearmotor, " + MOTOR, 10),
    ("12 V 5 W panel", 15),
    ("12 V 1.2 Ah sealed lead-acid", 12),
    ("solar charge controller, lead-acid, low-voltage cutoff", 5),
    ("ESP32-C3 SuperMini", 2),
    ("Ai-Thinker Ra-01H LoRa (SX1276, 868 MHz) and wire antenna", 7),
    ("MOSFET driver, fuse, wire, glands", 3),
    ("IP65 junction box, about 4 x 3 x 2 in", 3),
    ("two 608 bearings, shaft, printed head and two pulleys (est.)", 4),
]
P_IDLER = 4.0              # printed head, two pulleys, two 608 bearings, take-up screw (est.)
P_CUTTER = 0.6             # two trapezoid utility blades and a printed holder (est.)
P_HOOK = 0.03              # printed hook and a 1/8 in aluminium pop rivet (est.)
P_SEAL = 0.05              # 1/2 in steel strap seal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--span", type=float, default=33.0, help="ft between posts, one loop a span")
    ap.add_argument("--rpm", type=float, default=85.0, help="drive pulley rpm under load ASSUME")
    ap.add_argument("--pulley", type=float, default=6.0, help="in, pulley pitch diameter")
    ap.add_argument("--hook", type=float, default=12.0, help="in between hooks on the strap")
    ap.add_argument("--cut-lb", type=float, default=CUT_LB, help="lbf to draw a fibre through the blades ASSUME")
    ap.add_argument("--drag-lb", type=float, default=DRAG_LB, help="lbf to run one loop empty ASSUME")
    a = ap.parse_args()

    sag_in = STRAP_LB_FT * a.span ** 2 / (8 * TENSION_LB) * 12
    loop_ft = 2 * a.span + math.pi * a.pulley / 12 + SEAL_LOSS_FT
    print(f"1/2 in PET strap on {a.span:.0f} ft spans: sag {sag_in:.1f} in at {TENSION_LB:.0f} lb, "
          f"{TENSION_LB / STRAP_BREAK_LB:.1%} of its break strength. Loop {loop_ft:.0f} ft.")

    fps = a.rpm * math.pi * a.pulley / 12 / 60
    wait_s = (a.hook / 12 + a.span) / fps
    drone_fps = DRONE_MPH * 5280 / 3600
    print(f"\nStrap speed {fps:.1f} ft/s ({a.rpm:.0f} rpm on a {a.pulley:.0f} in pulley).")
    print(f"  Longest wait from a fibre landing to its cut: a hook {a.hook:.0f} in away, then the whole span: "
          f"{wait_s:.0f} s.")
    print(f"  A drone at {DRONE_MPH:.0f} mph flies {wait_s * drone_fps:,.0f} ft meanwhile, so that is how far "
          f"out the line must sit.")

    # one drive post turns two loops; a cut adds its pull on one of them
    r_in = a.pulley / 2
    run_lb = 2 * a.drag_lb
    cut_lb = run_lb + a.cut_lb
    kgcm = cut_lb * r_in * LBF * 2.54 / 9.81
    w_run = run_lb * LBF * fps * 0.3048 / MOTOR_EFF
    w_cut = cut_lb * LBF * fps * 0.3048 / MOTOR_EFF
    print(f"\nDrive post, two loops: {run_lb:.1f} lbf running, {cut_lb:.1f} lbf while cutting, "
          f"{kgcm:.1f} kg cm at the shaft (motor rated about {MOTOR_RATED_KGCM:.0f}, MEASURE).")
    print(f"  {w_run:.1f} W running, {w_cut:.1f} W while cutting.")

    event_wh = w_cut * EVENT_MIN / 60
    clear_wh = w_run * loop_ft / fps / 3600 * 24
    standby_wh = STANDBY_W * 24
    panel_wh = PANEL_W * WINTER_SUN_H * SOLAR_EFF
    spare = panel_wh - standby_wh - clear_wh
    print(f"\nEnergy a day, one drive post: standby {standby_wh:.1f} Wh, hourly clearing passes {clear_wh:.1f} Wh.")
    print(f"  A {PANEL_W} W panel makes about {panel_wh:.1f} Wh on a December day, leaving {spare:.1f} Wh: "
          f"{spare / event_wh:.0f} triggers a day at {event_wh:.1f} Wh each ({EVENT_MIN} min of running).")
    print(f"  The battery holds {BATT_WH * BATT_USABLE:.1f} Wh above half charge: "
          f"{BATT_WH * BATT_USABLE / (standby_wh + clear_wh):.1f} sunless days, or "
          f"{BATT_WH * BATT_USABLE / event_wh:.0f} triggers.")

    spans = math.ceil(MILE / a.span)
    posts = spans + 1
    drives = math.ceil(spans / 2)
    idlers = posts - drives
    hooks = math.ceil(spans * loop_ft * 12 / a.hook)
    drive_each = sum(c for _, c in DRIVE)
    parts = [
        (f"T-posts, {posts}", posts * P_TPOST),
        (f"Hose clamps, {posts}", posts * P_HOSE_CLAMP),
        (f"Drive heads, {drives} at ${drive_each:.0f}", drives * drive_each),
        (f"Idler heads, {idlers}", idlers * P_IDLER),
        (f"Blade pairs, {spans}", spans * P_CUTTER),
        (f"Strap, {spans * loop_ft:,.0f} ft, and {spans} seals", spans * (loop_ft * STRAP_PER_FT + P_SEAL)),
        (f"Hooks and rivets, {hooks:,}", hooks * P_HOOK),
        ("End anchors and guys, 2", 2 * P_END),
    ]
    total = sum(c for _, c in parts)
    print(f"\nA mile: {spans} spans, {drives} drive posts, small-batch parts (est.):")
    for name, c in parts:
        print(f"  {name:52s} ${c:6,.0f}")
    print(f"  {'Total':52s} ${total:6,.0f}")
    print("\nOne drive head:")
    for name, c in DRIVE:
        print(f"  {name:64s} ${c:3.0f}")


if __name__ == "__main__":
    main()
