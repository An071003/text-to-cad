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
    "center": {"pinion_leaves": 12, "wheel_teeth": 80, "module": 0.15},
    "third": {"pinion_leaves": 10, "wheel_teeth": 75, "module": 0.12},
    "fourth": {"pinion_leaves": 10, "wheel_teeth": 80, "module": 0.10},
    "escape": {"pinion_leaves": 8, "wheel_teeth": 15, "module": 0.08},
}
