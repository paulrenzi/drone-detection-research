"""Shared dimensions (mm, g). Each figure names its source or says ESTIMATE.

Change a number here and every model rebuilds from it. Anything marked
MEASURE must be checked with calipers on the real part before printing.
"""

# Printer: Anycubic Vyper, 245 x 245 x 260 build volume (3dsourced review quoting spec)
BED = (245, 245, 260)

# Heltec WiFi LoRa 32 V3: 50.2 x 25.5 x 10.2 (Heltec wiki)
HELTEC = (50.2, 25.5, 10.2)
# INMP441 breakout: ~14 x 14 x 3 (one reseller listing; MEASURE)
MIC = (14.0, 14.0, 3.0)
# 18650 cell: 18.6 dia x 65.2 (common spec; ESTIMATE, MEASURE the cell you buy)
CELL_D, CELL_L = 18.6, 65.2
# Steel spike insert: 6 mm rod or M6 threaded rod (hardware store), length ESTIMATE
ROD_D, ROD_L = 6.0, 110.0
# Mast: one shock-corded tent-pole section, 8.5 mm fibreglass (common size; MEASURE)
POLE_D, POLE_SEG = 8.5, 160.0
POLE_SEGS = 4  # 4 x 160 = 0.64 m; an even count leaves the head beside the hinge when folded

# SG90 micro servo body 22.2 x 11.8 x 31 (TowerPro datasheet), tab span 32.2 (ESTIMATE, MEASURE)
SERVO = (22.2, 11.8, 31.0)
SERVO_TAB_SPAN, SERVO_TAB_T, SERVO_TAB_Z = 32.2, 2.5, 15.9

# Holybro X500 V2 (holybro.com product + docs pages)
X500_RAIL_D = 10.0           # dual 10 mm rods, 250 mm long
X500_RAIL_L = 250.0
X500_RAIL_SPACING = 60.0     # NOT FOUND in any source: MEASURE, clamps are slotted 40-90
X500_WHEELBASE = 500.0
X500_GEAR_H = 215.0
X500_ARM_D = 16.0

# Densities g/cm3 (typical datasheet values; ESTIMATE)
PETG = 1.27
STEEL = 7.85
FIBREGLASS = 1.9

# Masses (g)
M_HELTEC = 9.0    # one search snippet; ESTIMATE
M_CELL = 46.0     # typical 18650; ESTIMATE
M_MIC_FUR = 8.0   # breakout + fur cover; ESTIMATE
M_SERVO = 9.0     # SG90 datasheet
