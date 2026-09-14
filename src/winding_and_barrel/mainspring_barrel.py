"""Mainspring Barrel Assembly (Hộp cót chính) Model for Caliber ETA 6497/6498.

Specs:
- Barrel drum with outer toothed rim: z = 77 teeth, m = 0.18 mm (Ø ~15.50 mm)
- Barrel arbor with lower/upper journals and square drive for ratchet wheel
- Barrel cover (snapped on)
- Internal coiled mainspring strip
- Mating Datum: BARREL_PIVOT (-3.50, -7.20)
"""

import math
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

from lib.gears import make_watch_wheel


@step(out="../../STEP/mainspring_barrel.step")
def mainspring_barrel():
    teeth = 77
    module = 0.18
    barrel_h = 1.60
    wall_t = 0.45
    outer_r = (teeth * module) / 2.0 + 0.95 * module  # ~7.10 mm

    with BuildPart() as msb:
        # 1. Outer toothed rim of the barrel
        wh = make_watch_wheel(
            teeth=teeth,
            module=module,
            rim_thickness=0.50,
            hub_diameter=3.20,
            arbor_hole=1.80,
            spoke_count=0,  # solid base plate
        )
        msb.part = wh

        # 2. Cylindrical drum wall
        with BuildSketch():
            Circle(radius=outer_r - 0.20)
            Circle(radius=outer_r - 0.20 - wall_t, mode=Mode.SUBTRACT)
        extrude(amount=barrel_h)

        # 3. Barrel Arbor in the center
        arbor = Cylinder(radius=0.90, height=barrel_h + 0.80)
        # Upper pivot and square seat for ratchet wheel
        top_pivot = Cylinder(radius=0.60, height=0.60).moved(Location((0, 0, barrel_h / 2.0 + 0.60)))
        square_seat = Cylinder(radius=0.70, height=0.50).moved(Location((0, 0, barrel_h / 2.0 + 0.30)))
        bot_pivot = Cylinder(radius=0.60, height=0.60).moved(Location((0, 0, -barrel_h / 2.0 - 0.50)))
        msb.part = msb.part + arbor + top_pivot + square_seat + bot_pivot

        # 4. Internal coiled mainspring (spiral layers inside the drum)
        for i in range(4):
            r_c = 1.60 + i * 0.95
            with BuildSketch():
                Circle(radius=r_c + 0.08)
                Circle(radius=r_c - 0.08, mode=Mode.SUBTRACT)
            extrude(amount=barrel_h - 0.20)

        # 5. Barrel Cover (top closing disc)
        with BuildSketch():
            Circle(radius=outer_r - 0.22)
            Circle(radius=1.10, mode=Mode.SUBTRACT)
        extrude(amount=0.25)
        cover = msb.part.faces().sort_by().last

        # Position assembly at barrel plane Z = -0.50
        msb.part = msb.part.moved(Location((0, 0, -0.50)))

    return msb.part


if __name__ == "__main__":
    mainspring_barrel()
