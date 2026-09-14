"""Fourth Wheel (Seconds Wheel) Assembly Model for Caliber ETA 6497/6498.

Specs:
- Fourth Wheel: z = 80 teeth, m = 0.10 mm
- Fourth Pinion: z = 10 leaves, m = 0.12 mm (meshes with Third Wheel)
- Long lower pivot extends through mainplate to carry the small seconds hand.
- Rotation: 1 revolution per 60 seconds (1 rpm).
- Mating Datum: FOURTH_PIVOT (-9.50, 4.50)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import BuildPart, Cylinder, Location
from cadgen import step

from lib.gears import make_pinion, make_watch_wheel
from lib.parameters import GEAR_DATA


@step(out="../../STEP/fourth_wheel.step")
def fourth_wheel():
    cfg = GEAR_DATA["fourth"]
    wheel_teeth = cfg["wheel_teeth"]      # 80
    wheel_module = cfg["module"]          # 0.10
    pinion_leaves = cfg["pinion_leaves"]  # 10
    pinion_module = 0.12

    with BuildPart() as fw:
        # Toothed Fourth Wheel disc
        wh = make_watch_wheel(
            teeth=wheel_teeth,
            module=wheel_module,
            rim_thickness=0.18,
            hub_diameter=1.40,
            arbor_hole=0.50,
            spoke_count=4,
            spoke_width=0.30,
        )
        # Position wheel at Z = 0.45
        fw.part = wh.moved(Location((0, 0, 0.45)))

        # Pinion (10 leaves) on arbor
        pin = make_pinion(
            leaves=pinion_leaves,
            module=pinion_module,
            length=1.10,
            arbor_diameter=0.50,
            pivot_diameter=0.18,
            pivot_length=0.35,
        )
        fw.part = fw.part + pin.moved(Location((0, 0, -0.20)))

        # Long seconds arbor extending down through mainplate (-Z)
        long_pivot = Cylinder(radius=0.10, height=2.80)
        long_pivot = long_pivot.moved(Location((0, 0, -1.80)))
        fw.part = fw.part + long_pivot

    return fw.part


if __name__ == "__main__":
    fourth_wheel()
