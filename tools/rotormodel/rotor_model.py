"""Rotor model: a turning barbed wire that winds up and breaks a fibre FPV's line, no sound needed.

Ukraine fields this: a 150 m barbed wire turned by a battery motor, 1 min on and 1 min off. No
specs are public, so this models one built from farm and hobby parts. Barbed wire is strung about
3 ft up on step-in posts and split into segments, each turned at one end by a small worm
gearmotor through a ball-bearing swivel. Segments meet at posts where their tensions cancel, so
only the two ends of the line need bracing. A line that drapes across the wire catches on a barb
and is wound round it until it breaks or bends too tight to carry light.

The key point: every turn costs the same energy (friction torque x one turn). So energy a day
depends only on turns a day. Turning slowly and all the time gives the shortest wait for a given
energy; a 1 min on, 1 min off timer just adds waiting.

Prints: torque and twist along a segment, how long a draped line waits for its turns, power and
solar per station, and parts per mile.

    py rotor_model.py [--seg 330] [--span 66] [--rpm 6] [--turns 3] [--sup-nm 0.1]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement. The torque per
support is the number the whole design turns on, and it is a guess until test R1.
"""
import argparse, math

MILE = 5280.0
FT = 0.3048
LBF = 4.448
DRONE_MPH = 43.0           # a fibre FPV's top speed (threat-profile)

# ---- the wire --------------------------------------------------------------------------------
WIRE_LB_FT = 80 / 1320     # 12.5 ga 4-point barbed wire, about 80 lb a 1,320 ft roll
STRAND_D = 2.5e-3          # m, each of the two 12.5 ga strands
G_STEEL = 80e9             # Pa
SHEAR_YIELD = 500e6        # Pa, galvanized fence wire, about ASSUME
TENSION_LB = 150           # ASSUME, set with a ratchet strainer and a spring at each end

# ---- friction ---------------------------------------------------------------------------------
SWIVEL_NM = 0.02           # a ball-bearing swivel under 150 lb ASSUME
MOTOR_EFF = 0.30           # small worm gearmotor, motor x gearbox ASSUME

# ---- power ------------------------------------------------------------------------------------
IDLE_W = 0.05              # charge controller's own draw ASSUME
WINTER_SUN_H = 1.5         # full-sun hours a day in a Ukrainian December ASSUME
SOLAR_EFF = 0.7            # panel to battery, PWM controller, dirt ASSUME
AUTONOMY_DAYS = 3          # overcast days the battery must cover ASSUME
MOTORS_PER_STATION = 2     # one each way from a station post

# ---- parts, $ each, small batch (retail listings 2026-10 unless est.) --------------------------
P_WIRE_ROLL = 140          # 1,320 ft roll, $125-150
P_LINE_POST = 4.5          # steel pigtail step-in post, the wire rides in the loop (est.)
P_TPOST = 10               # 6 ft T-post, at stations, junctions and braces
P_SWIVEL = 8               # ball-bearing swivel, 400-500 lb (est.)
P_MOTOR = 21               # JGY-370 12 V worm gearmotor, self-locking
P_MOUNT = 10               # motor bracket, drive fork, wire clamp (est.)
P_CONTROLLER = 15          # 10 A PWM solar controller with low-voltage cutoff
P_BOX = 20                 # box, fuse, wiring (est.)
P_STRAIN_MILE = 80         # 2 strainers, 2 springs, clamps, end-stops
PANEL_PER_W = 1.0          # $ a watt, small 12 V panels (est.)
LFP_PER_WH = 0.35          # $ a Wh, small 12 V LiFePO4 (est.)


def support_nm(span_ft, misalign_deg, barb_mm, barbs_per_rev, mu):
    """Torque one support takes: the wire rubs in the loop, and each barb lifts it to pass."""
    weight = WIRE_LB_FT * span_ft * LBF
    side = 2 * TENSION_LB * LBF * math.sin(math.radians(misalign_deg))
    n = math.hypot(weight, side)
    rub = mu * n * STRAND_D
    lift = n * barb_mm / 1000 * barbs_per_rev / (2 * math.pi)
    return rub + lift


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", type=float, default=330.0, help="ft of wire one motor turns")
    ap.add_argument("--span", type=float, default=66.0, help="ft between line posts")
    ap.add_argument("--rpm", type=float, default=6.0, help="turns a minute, all the time")
    ap.add_argument("--turns", type=float, default=3.0, help="turns to break a draped line ASSUME")
    ap.add_argument("--sup-nm", type=float, default=None, help="override the torque per support, N m")
    a = ap.parse_args()

    sag_ft = WIRE_LB_FT * a.span ** 2 / (8 * TENSION_LB)
    sup = a.sup_nm if a.sup_nm is not None else support_nm(a.span, 1.0, 8, 1.5, 0.3)
    n_sup = a.seg / a.span
    torque = n_sup * sup + 2 * SWIVEL_NM
    gj = 2 * G_STEEL * math.pi * STRAND_D ** 4 / 32
    twist_turns = torque * a.seg * FT / (2 * gj) / (2 * math.pi)
    stress = torque / 2 * 16 / (math.pi * STRAND_D ** 3)

    print(f"Segment {a.seg:.0f} ft on {a.span:.0f} ft spans: sag {sag_ft * 12:.1f} in at {TENSION_LB} lb.")
    print(f"  Torque: {sup:.3f} N m a support x {n_sup:.1f} + swivels = {torque:.2f} N m at the motor "
          f"(JGY-370 rated about 0.5 N m at 30 rpm, more at lower rpm).")
    print(f"  Twist held along it while turning: {twist_turns:.1f} turns, end to end. "
          f"Shear in the strands {stress / 1e6:.0f} MPa of about {SHEAR_YIELD / 1e6:.0f}.")

    wait_s = a.turns / a.rpm * 60
    fps = DRONE_MPH * 5280 / 3600
    print(f"\nA draped line gets {a.turns:.0f} turns in {wait_s:.0f} s at {a.rpm:g} rpm. "
          f"A drone at {DRONE_MPH:.0f} mph flies {wait_s * fps:,.0f} ft meanwhile,")
    print(f"  so the wire has to sit at least {wait_s * fps / MILE:.2f} mi in front of what it protects.")

    mech_w = torque * a.rpm * 2 * math.pi / 60
    elec_w = mech_w / MOTOR_EFF
    wh_day = (elec_w * MOTORS_PER_STATION + IDLE_W) * 24
    panel_w = wh_day / (WINTER_SUN_H * SOLAR_EFF)
    batt_wh = wh_day * AUTONOMY_DAYS
    print(f"\nPower: {mech_w:.2f} W at the wire, {elec_w:.2f} W from the battery per motor.")
    print(f"  A station turns {MOTORS_PER_STATION} segments: {wh_day:.0f} Wh a day, "
          f"a {panel_w:.0f} W panel in December, {batt_wh:.0f} Wh of battery for {AUTONOMY_DAYS} grey days.")
    print("  Energy goes with turns a day, so rpm sets it:")
    for r in (2, 4, 6, 10, 30):
        e = (torque * r * 2 * math.pi / 60 / MOTOR_EFF * MOTORS_PER_STATION + IDLE_W) * 24
        print(f"    {r:>3} rpm: {e:5.0f} Wh/day a station, line waits {a.turns / r * 60:4.0f} s")
    timer = (torque * 30 * 2 * math.pi / 60 / MOTOR_EFF * MOTORS_PER_STATION) * 24 * 0.5
    print(f"  The fielded timer (30 rpm, 1 min on, 1 off) would use {timer:.0f} Wh/day and wait up to "
          f"{60 + a.turns / 30 * 60:.0f} s.")

    segs = math.ceil(MILE / a.seg)
    stations = math.ceil(segs / MOTORS_PER_STATION)
    junctions = segs - stations
    line_posts = max(0, math.ceil(MILE / a.span) - segs)
    rolls = math.ceil(MILE * 1.03 / 1320)
    station_power = math.ceil(panel_w / 10) * 10 * PANEL_PER_W + batt_wh * LFP_PER_WH + P_CONTROLLER + P_BOX
    parts = [
        (f"Barbed wire, {rolls} rolls", rolls * P_WIRE_ROLL),
        (f"Line posts, {line_posts} pigtail step-ins", line_posts * P_LINE_POST),
        (f"T-posts: {stations} stations, {junctions} junctions, 6 for end braces", (stations + junctions + 6) * P_TPOST),
        (f"Swivels, {2 * segs}", 2 * segs * P_SWIVEL),
        (f"Gearmotors and mounts, {segs}", segs * (P_MOTOR + P_MOUNT)),
        (f"Station power x {stations}: panel, LiFePO4, controller, box", stations * station_power),
        ("Strainers, springs, clamps", P_STRAIN_MILE),
    ]
    total = sum(c for _, c in parts)
    print(f"\nA mile: {segs} segments, {stations} stations, small-batch parts (est.):")
    for name, c in parts:
        print(f"  {name:58s} ${c:6,.0f}")
    print(f"  {'Total':58s} ${total:6,.0f}")


if __name__ == "__main__":
    main()
