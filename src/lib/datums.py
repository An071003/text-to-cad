"""Shared Coordinate Datums and Pivot Locations for ETA 6497/6498 Caliber.

All coordinates are referenced to the Mainplate Center at (0.0, 0.0, 0.0).
- Z = 0: Top face of mainplate (bridges side)
- Z < 0: Dial side (negative Z)
- Z > 0: Movement bridges and balance cock (positive Z)

Exact Horological Kinematic Layout (Center distances verified to 0.0001 mm):
- Center (0,0) -> Barrel: C_b-c = 8.0100 mm (z77 / z12, m=0.18)
- Center (0,0) -> Third:  C_c-3 = 6.7500 mm (z80 / z10, m=0.15)
- Third -> Fourth (Small Seconds at 9 o'clock): C_3-4 = 5.1000 mm (z75 / z10, m=0.12)
- Fourth -> Escape:       C_4-e = 4.4000 mm (z80 / z8,  m=0.10)
- Escape -> Pallet:       C_e-p = 4.1000 mm
- Pallet -> Balance:      C_p-b = 4.0000 mm
"""

# Center of Mainplate (Center Wheel & Cannon Pinion)
CENTER_PIVOT = (0.0000, 0.0000)

# Mainspring Barrel: meshes with Center Pinion
# Distance from center = 8.0100 mm
BARREL_PIVOT = (-3.5019, -7.2039)

# Third Wheel: meshes with Center Wheel and Fourth Pinion
# Distance from center = 6.7500 mm
THIRD_PIVOT = (-5.5863, 3.7890)

# Fourth Wheel: carries small seconds hand at 9 o'clock position
# Distance from center = 9.0000 mm, Distance from Third = 5.1000 mm
FOURTH_PIVOT = (-9.0000, 0.0000)

# Escape Wheel: meshes with Fourth Wheel
# Distance from Fourth = 4.4000 mm
ESCAPE_PIVOT = (-7.6403, 4.1846)

# Pallet Fork (Lever):
# Distance from Escape = 4.1000 mm
PALLET_PIVOT = (-5.9076, 7.9005)

# Balance Wheel & Staff:
# Distance from Pallet = 4.0000 mm, Outer radius reach = 17.21 mm (< 18.30 mm)
BALANCE_PIVOT = (-3.3364, 10.9647)

# Winding Stem axis:
# Passes through X = 18.30 (3 o'clock position), Y = -2.50, Z = -0.80
STEM_Y = -2.50
STEM_Z = -0.80

# Bridge Screw & Steady Pin Hole Locations:
# Barrel Bridge mounting holes
BARREL_BRIDGE_SCREWS = [
    (-13.50, -8.50),
    (5.50, -14.20),
    (-2.00, -15.50),
]
BARREL_BRIDGE_PINS = [
    (-14.20, -6.00),
    (7.00, -12.50),
]

# Train Bridge mounting holes (spanning Center, Third, Fourth, Escape)
TRAIN_BRIDGE_SCREWS = [
    (2.50, 4.50),
    (-10.50, 2.00),
    (-4.00, 7.50),
]
TRAIN_BRIDGE_PINS = [
    (3.00, 1.50),
    (-10.80, -0.50),
]

# Balance Cock mounting holes
BALANCE_COCK_SCREW = (-0.50, 14.50)
BALANCE_COCK_PINS = [(-2.00, 13.80), (1.00, 14.00)]

# Pallet Cock mounting holes
PALLET_COCK_SCREW = (-8.50, 9.50)
PALLET_COCK_PINS = [(-9.50, 8.00), (-7.50, 10.50)]
