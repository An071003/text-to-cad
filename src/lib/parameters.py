"""Caliber ETA 6497-1 / Unitas 6498-1 Reference Parameters & Kinematic Specs.

Reference Base:
- Type: Manual-wind, time-only, small seconds at 9 (6497) or 6 (6498)
- Size: 16.5''' (ligne) = 36.60 mm diameter, ~4.50 mm height
- Frequency: 18,000 A/h (2.5 Hz, 5 beats/second)
- Jewels: 17 jewels
- Power reserve: ~46-50 hours
"""

# Dimensional constants (mm)
MAINPLATE_DIAMETER = 36.60
MAINPLATE_THICKNESS = 2.20
CALIBER_TOTAL_HEIGHT = 4.50

# Datum & Coordinate Origin Convention
# Origin (0, 0, 0): Center of mainplate, top surface (movement/bridge side) is Z = 0.
# Dial side is negative Z. Bridges stack on positive Z.

# Frequency & Gear train ratio:
# Balance frequency: 2.5 Hz = 5 vibrations/sec = 18,000 vph
# Escapement wheel: 15 teeth -> 30 beats per turn -> 1 turn per 6 seconds (10 rpm)
# Fourth wheel (small seconds): 1 turn per 60 seconds (1 rpm)
# Ratio fourth wheel to escape pinion: 10:1 (e.g., 60 teeth : 6 leaf pinion)
# Center wheel: 1 turn per hour (1/60 rpm)
# Ratio center wheel to third pinion * third wheel to fourth pinion = 60:1
# Typical teeth counts:
# - Great wheel / Barrel: 77 teeth
# - Center pinion: 12 leaves, Center wheel: 80 teeth
# - Third pinion: 10 leaves, Third wheel: 75 teeth
# - Fourth pinion: 10 leaves, Fourth wheel: 80 teeth (or 60:6)
# - Escape pinion: 10 leaves, Escape wheel: 15 teeth

GEAR_DATA = {
    "barrel": {"teeth": 77, "module": 0.18},
    "center": {"pinion_leaves": 12, "wheel_teeth": 80, "module": 0.15, "pinion_module": 0.18},
    "third": {"pinion_leaves": 10, "wheel_teeth": 75, "module": 0.12, "pinion_module": 0.15},
    "fourth": {"pinion_leaves": 10, "wheel_teeth": 80, "module": 0.10, "pinion_module": 0.12},
    "escape": {"pinion_leaves": 8, "wheel_teeth": 15, "module": 0.10, "pinion_module": 0.10},
}

# Calculated pitch radii (mm)
PITCH_RADII = {
    "barrel_wheel": 77 * 0.18 / 2.0,       # 6.93 mm
    "center_pinion": 12 * 0.18 / 2.0,      # 1.08 mm
    "center_wheel": 80 * 0.15 / 2.0,       # 6.00 mm
    "third_pinion": 10 * 0.15 / 2.0,       # 0.75 mm
    "third_wheel": 75 * 0.12 / 2.0,        # 4.50 mm
    "fourth_pinion": 10 * 0.12 / 2.0,      # 0.60 mm
    "fourth_wheel": 80 * 0.10 / 2.0,       # 4.00 mm
    "escape_pinion": 8 * 0.10 / 2.0,       # 0.40 mm
    "escape_wheel": 15 * 0.10 / 2.0,       # 0.75 mm (pitch cylinder reference)
}

# Mathematically exact kinematic center distances (mm)
CENTER_DISTANCES = {
    "barrel_center": PITCH_RADII["barrel_wheel"] + PITCH_RADII["center_pinion"],  # 8.0100 mm
    "center_third":  PITCH_RADII["center_wheel"] + PITCH_RADII["third_pinion"],   # 6.7500 mm
    "third_fourth":  PITCH_RADII["third_wheel"] + PITCH_RADII["fourth_pinion"],   # 5.1000 mm
    "fourth_escape": PITCH_RADII["fourth_wheel"] + PITCH_RADII["escape_pinion"],  # 4.4000 mm
    "escape_pallet": 4.1000,
    "pallet_balance": 4.0000,
}

