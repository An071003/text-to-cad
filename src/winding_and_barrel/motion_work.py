"""Motion Work (Bộ phân phối kim Giờ - Phút) Model for Caliber ETA 6497/6498.

Components:
- Cannon Pinion (ống kim phút ma sát): z = 12, m = 0.18 mm
- Minute Wheel & Pinion: Wheel z = 36, Pinion z = 10 (3:1 reduction)
- Hour Wheel: z = 40, m = 0.20 mm (4:1 reduction from minute pinion -> 12:1 total)
- Dial Washer (hour wheel foil)
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
    extrude,
)
from cadgen import step

from lib.gears import make_pinion, make_watch_wheel


@step(out="../../STEP/motion_work.step")
def motion_work():
    minute_wheel_pos = (-4.20, -1.80)

    with BuildPart() as mw:
        # 1. Cannon Pinion (friction fit onto center arbor on dial side Z < 0)
        cp_pinion = make_pinion(
            leaves=12,
            module=0.18,
            length=1.40,
            arbor_diameter=0.85,
            pivot_diameter=0.0,
            pivot_length=0.0,
        )
        cp_tube = Cylinder(radius=0.45, height=2.40).moved(Location((0, 0, 1.20)))
        cp_bore = Cylinder(radius=0.25, height=3.0).moved(Location((0, 0, 1.0)))
        cannon_pinion = (cp_pinion + cp_tube) - cp_bore
        cannon_pinion = cannon_pinion.moved(Location((0, 0, -1.80)))

        # 2. Minute Wheel & Pinion
        min_wheel = make_watch_wheel(
            teeth=36,
            module=0.18,
            rim_thickness=0.25,
            hub_diameter=1.80,
            arbor_hole=0.60,
            spoke_count=3,
        )
        min_pinion = make_pinion(
            leaves=10,
            module=0.20,
            length=1.10,
            arbor_diameter=0.60,
            pivot_diameter=0.25,
            pivot_length=0.30,
        )
        min_assembly = min_wheel + min_pinion.moved(Location((0, 0, 0.30)))
        min_assembly = min_assembly.moved(Location((minute_wheel_pos[0], minute_wheel_pos[1], -1.80)))

        # 3. Hour Wheel (slips over cannon pinion, carries hour hand)
        hw_wheel = make_watch_wheel(
            teeth=40,
            module=0.20,
            rim_thickness=0.25,
            hub_diameter=2.00,
            arbor_hole=0.95,
            spoke_count=4,
        )
        hw_tube = Cylinder(radius=0.65, height=1.60).moved(Location((0, 0, 0.80)))
        hw_bore = Cylinder(radius=0.48, height=2.0).moved(Location((0, 0, 0.80)))
        hour_wheel = (hw_wheel + hw_tube) - hw_bore
        hour_wheel = hour_wheel.moved(Location((0, 0, -1.40)))

        # 4. Dial Washer (curved spring foil)
        with BuildSketch():
            Circle(radius=1.80)
            Circle(radius=0.75, mode=Mode.SUBTRACT)
        extrude(amount=0.08)
        foil = mw.part.faces().sort_by().last
        washer = mw.part.moved(Location((0, 0, -0.90)))

        mw.part = cannon_pinion + min_assembly + hour_wheel + washer

    return mw.part


if __name__ == "__main__":
    motion_work()
