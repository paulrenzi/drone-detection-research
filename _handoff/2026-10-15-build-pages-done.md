# Handoff: build pages shipped

Written at HEAD c147685 (2026-10-15). Supersedes `2026-10-15-printed-hardware-and-software.md`, which is now done.

## Shipped (render-verified at ?cb=c147685)
- `build-hardware.md`: dart, X500 harness, TL-1 printed quad, flight-time table, parts list (~$145; Amazon listings opened in a browser 10-15).
- `build-software.md`: six components, five interfaces, Batear coverage, Batear nonce defect plus fix.
- `cad/`: CadQuery scripts, STL/STEP in `cad/out/`, renders in `assets/images/build/`. Venv on the PC: `C:\Users\paulm\.venvs\cad` (python 3.14, cadquery 2.8).
- Checker: `%TEMP%\rc_build.py <sha>`. Amazon cart/price checker: `%TEMP%\amz_check.py <ASIN...>` (headed Chromium; plain fetch gets 503).

## Paul's answers
Printer: Anycubic Vyper (PETG, prototype grade). Drone: design both the X500 harness and a fully printed carrier. Pages: two. CAD: Claude's choice; picked CadQuery.

## Open, measure before printing
X500 rail spacing (clamps slotted 40-90 mm), X500 leg tube (extensions ~60-80 mm not modelled), INMP441 size, 18650 actual size, SG90 tab span, the bare Heltec V3's sleep current on battery (decides custom board).

## Next
Print the dart, then T10 drop heights 3/5/10/15 m. Edge receiver mount not designed. Optional: PR the nonce fix to batear-io/batear (ask Paul first, it's outward-facing). XVF3800 line in layer 2 still unasked.
