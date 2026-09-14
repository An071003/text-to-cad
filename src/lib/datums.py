"""Shared Coordinate Datums and Pivot Locations for ETA 6497/6498 Caliber.

All coordinates are referenced to the Mainplate Center at (0.0, 0.0, 0.0).
- Z = 0: Top face of mainplate (bridges side)
- Z < 0: Dial side (negative Z)
- Z > 0: Movement bridges and balance cock (positive Z)
"""

# Center of Mainplate (0, 0)
CENTER_PIVOT = (0.0, 0.0)

# Mainspring Barrel: meshes with Center Pinion
# Center distance = 8.01 mm
BARREL_PIVOT = (-3.50, -7.20)

# Third Wheel: meshes with Center Wheel
# Center distance = 6.75 mm
THIRD_PIVOT = (4.77, 4.77)

# Fourth Wheel (Small Seconds at 9 o'clock position):
# Center distance from center ~ 10.50 mm
FOURTH_PIVOT = (-9.50, 4.50)

# Escape Wheel: meshes with Fourth Wheel
ESCAPE_PIVOT = (-11.80, 8.20)

# Pallet Fork (Lever):
PALLET_PIVOT = (-8.20, 10.50)

# Balance Wheel & Staff:
BALANCE_PIVOT = (-4.20, 11.80)

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

# Train Bridge mounting holes
TRAIN_BRIDGE_SCREWS = [
    (13.50, 3.50),
    (7.50, 13.00),
    (1.50, 5.50),
]
TRAIN_BRIDGE_PINS = [
    (14.50, 1.00),
    (5.00, 14.50),
]

# Balance Cock mounting holes
BALANCE_COCK_SCREW = (-1.00, 15.50)
BALANCE_COCK_PINS = [(-2.50, 14.20), (0.50, 14.80)]

# Pallet Cock mounting holes
PALLET_COCK_SCREW = (-10.50, 13.20)
PALLET_COCK_PINS = [(-11.50, 11.50), (-9.20, 14.20)]
