"""Center Wheel Assembly Model for Caliber ETA 6497/6498.

Specs:
- Center Wheel: z = 80 teeth, m = 0.15 mm
- Center Pinion: z = 12 leaves, m = 0.18 mm (meshes with barrel)
- Rotation: 1 revolution per hour (drives cannon pinion / minute hand)
- Mating Datum: CENTER_PIVOT (0.0, 0.0)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import (
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Location,
    Mode,
    PolarLocations,
    Rectangle,
    extrude,
)
from cadgen import step

from lib.gears import make_pinion, make_watch_wheel
from lib.parameters import GEAR_DATA


@step(out="../../STEP/center_wheel.step")
def center_wheel():
    cfg = GEAR_DATA["center"]
    wheel_teeth = cfg["wheel_teeth"]      # 80
    wheel_module = cfg["module"]          # 0.15
    pinion_leaves = cfg["pinion_leaves"]  # 12
    pinion_module = 0.18

    with BuildPart() as cw:
        # 1. Toothed Center Wheel disc (elevated above barrel top)
        wh = make_watch_wheel(
            teeth=wheel_teeth,
            module=wheel_module,
            rim_thickness=0.20,
            hub_diameter=2.00,
            arbor_hole=0.80,
            spoke_count=4,
            spoke_width=0.45,
        )
        # Position wheel disc at Z = 0.58
        cw.part = wh.moved(Location((0, 0, 0.58)))

        # 2. Center Pinion (12 leaves) meshing with mainspring barrel
        pin = make_pinion(
            leaves=pinion_leaves,
            module=pinion_module,
            length=0.45,
            arbor_diameter=0.80,
            pivot_diameter=0.35,
            pivot_length=0.50,
        )
        cw.part = cw.part + pin.moved(Location((0, 0, 0.05)))

        # 3. Central cannon arbor extending to dial side and upper bridge jewel
        tube = Cylinder(radius=0.38, height=2.80)
        tube = tube.moved(Location((0, 0, -0.20)))
        cw.part = cw.part + tube

        # Central bore through the tube for seconds arbor
        bore = Cylinder(radius=0.18, height=3.5)
        bore = bore.moved(Location((0, 0, -0.50)))
        cw.part = cw.part - bore

    return cw.part


if __name__ == "__main__":
    center_wheel()
