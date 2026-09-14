"""Third Wheel Assembly Model for Caliber ETA 6497/6498.

Specs:
- Third Wheel: z = 75 teeth, m = 0.12 mm
- Third Pinion: z = 10 leaves, m = 0.15 mm (meshes with Center Wheel)
- Mating Datum: THIRD_PIVOT (4.77, 4.77)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import BuildPart, Location
from cadgen import step

from lib.gears import make_pinion, make_watch_wheel
from lib.parameters import GEAR_DATA


@step(out="../../STEP/third_wheel.step")
def third_wheel():
    cfg = GEAR_DATA["third"]
    wheel_teeth = cfg["wheel_teeth"]      # 75
    wheel_module = cfg["module"]          # 0.12
    pinion_leaves = cfg["pinion_leaves"]  # 10
    pinion_module = 0.15

    with BuildPart() as tw:
        # Toothed Third Wheel disc (elevated above center wheel disc)
        wh = make_watch_wheel(
            teeth=wheel_teeth,
            module=wheel_module,
            rim_thickness=0.18,
            hub_diameter=1.60,
            arbor_hole=0.60,
            spoke_count=4,
            spoke_width=0.35,
        )
        # Position wheel disc at Z = 0.85
        tw.part = wh.moved(Location((0, 0, 0.85)))

        # Pinion (10 leaves) meshing with Center Wheel disc at Z = 0.58
        pin = make_pinion(
            leaves=pinion_leaves,
            module=pinion_module,
            length=0.40,
            arbor_diameter=0.60,
            pivot_diameter=0.20,
            pivot_length=0.40,
        )
        tw.part = tw.part + pin.moved(Location((0, 0, 0.55)))

    return tw.part


if __name__ == "__main__":
    third_wheel()
