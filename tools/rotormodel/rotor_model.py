"""Rotor model: a turning barbed wire that winds up and breaks a fibre FPV's line, no sound needed.

Ukraine fields this: a 150 m barbed wire turned by a battery motor, 1 min on and 1 min off. No
specs are public, so this models one built from farm and hobby parts. Barbed wire is strung about
3 ft up, riding in the loops of step-in posts. Each 1,320 ft roll is one piece, turned at its middle
by one small worm gearmotor clamped to the wire, so the motor turns 660 ft each way. Rolls are
joined end to end by ball-bearing swivels, so the line's tension runs straight through and only
its two ends need bracing. A line that drapes across the wire catches on a barb and is wound round
it until it breaks or bends too tight to carry light.

The key point: every turn costs the same energy (friction torque x one turn). So energy a day
depends only on turns a day. Turning slowly and all the time gives the shortest wait for a given
energy; a 1 min on, 1 min off timer just adds waiting.

Prints: torque and twist along the wire, how long a draped line waits for its turns, power and
solar per motor, and parts per mile.

    py rotor_model.py [--wire 15.5] [--drive 1320] [--span 132] [--rpm 3] [--turns 3] [--sup-nm X]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement. The torque per
support is the number the whole design turns on, and it is a guess until test R1.
"""
import argparse, math

MILE = 5280.0
FT = 0.3048
LBF = 4.448
DRONE_MPH = 43.0           # a fibre FPV's top speed (threat-profile)
ROLL_FT = 1320

# ---- the wire: (lb a ft, strand dia m, shear yield Pa ASSUME, $ a 1,320 ft roll) ----------------
WIRES = {
    "12.5": (80 / 1320, 2.5e-3, 300e6, 140),   # 12.5 ga 4-point, mild steel, $125-150 a roll
    "15.5": (42 / 1320, 1.73e-3, 600e6, 80),   # 15.5 ga 4-point high-tensile, $72-90 a roll
}
G_STEEL = 80e9             # Pa
TENSION_LB = 150           # ASSUME, set with a ratchet strainer and a spring at each end
MISALIGN_DEG = 1.0         # posts off a straight line, so the wire presses on each loop ASSUME
BARB_MM = 8                # how far a barb lifts the wire to pass the loop ASSUME
BARBS_PER_REV = 1.5        # barbs passing each loop per turn ASSUME
MU = 0.3                   # galvanized wire in a steel loop ASSUME

# ---- motor and power --------------------------------------------------------------------------
MOTOR_NM = 2.45            # JGY-370 12 V 6 rpm (1:1000): rated 25 kg cm, 0.5 A full load (listings)
SWIVEL_NM = 0.02           # a ball-bearing swivel under 150 lb ASSUME
MOTOR_EFF = 0.30           # small worm gearmotor, motor x gearbox ASSUME
IDLE_W = 0.05              # charge controller's own draw ASSUME
WINTER_SUN_H = 1.5         # full-sun hours a day in a Ukrainian December ASSUME
SOLAR_EFF = 0.7            # panel to battery, PWM controller, dirt ASSUME
AUTONOMY_DAYS = 3          # overcast days the battery must cover ASSUME

# ---- parts, $ each, small batch (retail listings 2026-10 unless est.) --------------------------
P_LINE_POST = 4.0          # steel pigtail step-in post, the wire rides in the loop (est.)
P_TPOST = 10               # 6 ft T-post: one per motor, and 6 for the two end braces
P_SWIVEL = 8               # ball-bearing swivel, 400-500 lb (est.)
P_MOTOR = 31               # JGY-370 12 V 6 rpm, $25-35
P_MOUNT = 8                # bracket on the T-post, drive fork, wire clamp (est.)
P_CONTROLLER = 10          # PWM solar controller with low-voltage cutoff (est.)
P_BOX = 10                 # box, fuse, wiring (est.)
P_STRAIN_MILE = 60         # 2 strainers, 2 springs, clamps
PANEL_PER_W = 1.0          # $ a watt, small 12 V panels (est.)
LFP_PER_WH = 0.35          # $ a Wh, small 12 V LiFePO4 (est.)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wire", choices=WIRES, default="15.5", help="barbed wire gauge")
    ap.add_argument("--drive", type=float, default=1320.0, help="ft of wire one motor turns, from its middle")
    ap.add_argument("--span", type=float, default=132.0, help="ft between line posts")
    ap.add_argument("--rpm", type=float, default=3.0, help="turns a minute, all the time")
    ap.add_argument("--turns", type=float, default=3.0, help="turns to break a draped line ASSUME")
    ap.add_argument("--sup-nm", type=float, default=None, help="override the torque per support, N m")
    a = ap.parse_args()
    lb_ft, d, yield_pa, roll_price = WIRES[a.wire]

    sag_ft = lb_ft * a.span ** 2 / (8 * TENSION_LB)
    weight = lb_ft * a.span * LBF
    side = 2 * TENSION_LB * LBF * math.sin(math.radians(MISALIGN_DEG))
    n = math.hypot(weight, side)
    sup = a.sup_nm if a.sup_nm is not None else MU * n * d + n * BARB_MM / 1000 * BARBS_PER_REV / (2 * math.pi)
    arm_ft = a.drive / 2                              # the motor sits mid-way, turning each arm
    arm_torque = arm_ft / a.span * sup + SWIVEL_NM
    torque = 2 * arm_torque
    gj = 2 * G_STEEL * math.pi * d ** 4 / 32
    twist = arm_torque * arm_ft * FT / (2 * gj) / (2 * math.pi)
    stress = arm_torque / 2 * 16 / (math.pi * d ** 3)

    print(f"{a.wire} ga barbed wire on {a.span:.0f} ft spans: sag {sag_ft * 12:.1f} in at {TENSION_LB} lb.")
    print(f"  One motor turns {a.drive:.0f} ft from its middle: {sup:.3f} N m a support, "
          f"{torque:.2f} N m at the motor (rated {MOTOR_NM} N m).")
    print(f"  Twist held from the motor to each end while turning: {twist:.0f} turns. "
          f"Shear in the strands {stress / 1e6:.0f} MPa of about {yield_pa / 1e6:.0f}.")

    wait_s = a.turns / a.rpm * 60
    fps = DRONE_MPH * 5280 / 3600
    print(f"\nA draped line gets {a.turns:.0f} turns in {wait_s:.0f} s at {a.rpm:g} rpm. "
          f"A drone at {DRONE_MPH:.0f} mph flies {wait_s * fps:,.0f} ft meanwhile,")
    print(f"  so the wire has to sit at least {wait_s * fps / MILE:.2f} mi in front of what it protects.")

    def wh_day(rpm):
        return (torque * rpm * 2 * math.pi / 60 / MOTOR_EFF + IDLE_W) * 24

    e = wh_day(a.rpm)
    panel_w = e / (WINTER_SUN_H * SOLAR_EFF)
    batt_wh = e * AUTONOMY_DAYS
    print(f"\nPower: {e / 24:.2f} W a motor, {e:.0f} Wh a day: a {panel_w:.0f} W panel in December, "
          f"{batt_wh:.0f} Wh of battery for {AUTONOMY_DAYS} grey days.")
    print("  Energy goes with turns a day, so rpm sets it:")
    for r in (2, 3, 6, 10, 30):
        print(f"    {r:>3} rpm: {wh_day(r):5.0f} Wh/day a motor, line waits {a.turns / r * 60:4.0f} s")

    motors = math.ceil(MILE / a.drive)
    rolls = math.ceil(MILE / ROLL_FT)
    swivels = rolls + 1
    line_posts = max(0, math.ceil(MILE / a.span) + 1 - motors)
    power = math.ceil(panel_w / 5) * 5 * PANEL_PER_W + batt_wh * LFP_PER_WH + P_CONTROLLER + P_BOX
    parts = [
        (f"{a.wire} ga barbed wire, {rolls} rolls", rolls * roll_price),
        (f"Line posts, {line_posts} pigtail step-ins", line_posts * P_LINE_POST),
        (f"T-posts: {motors} motor posts, 6 for end braces", (motors + 6) * P_TPOST),
        (f"Swivels, {swivels}: between rolls and at the ends", swivels * P_SWIVEL),
        (f"Gearmotors and mounts, {motors}", motors * (P_MOTOR + P_MOUNT)),
        (f"Power x {motors}: panel, LiFePO4, controller, box", motors * power),
        ("Strainers, springs, clamps", P_STRAIN_MILE),
    ]
    total = sum(c for _, c in parts)
    print(f"\nA mile: {motors} motors, small-batch parts (est.):")
    for name, c in parts:
        print(f"  {name:52s} ${c:6,.0f}")
    print(f"  {'Total':52s} ${total:6,.0f}")


if __name__ == "__main__":
    main()
