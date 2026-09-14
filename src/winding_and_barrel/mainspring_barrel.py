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
from cadgen import srgb, step

from lib.gears import make_watch_wheel


@step(out="../../STEP/mainspring_barrel.step")
def mainspring_barrel():
    teeth = 77
    module = 0.18
    barrel_h = 1.00
    wall_t = 0.45
    outer_r = (teeth * module) / 2.0 + 0.95 * module  # ~7.10 mm

    with BuildPart() as msb:
        # 1. Outer toothed rim of the barrel (at Z = 0.05 to mesh with center pinion)
        wh = make_watch_wheel(
            teeth=teeth,
            module=module,
            rim_thickness=0.35,
            hub_diameter=3.20,
            arbor_hole=1.80,
            spoke_count=0,  # solid base plate
        )
        msb.part = wh.moved(Location((0, 0, 0.05)))

        # 2. Cylindrical drum wall (from Z = -0.60 to 0.40)
        drum_solid = Cylinder(radius=outer_r - 0.20, height=barrel_h) - Cylinder(radius=outer_r - 0.20 - wall_t, height=barrel_h + 0.1)
        drum_solid = drum_solid.moved(Location((0, 0, -0.10)))
        msb.part = msb.part + drum_solid

        # 3. Barrel Arbor in the center
        arbor = Cylinder(radius=0.90, height=1.60).moved(Location((0, 0, 0.20)))
        # Upper pivot and square seat for ratchet wheel on top of barrel bridge
        top_pivot = Cylinder(radius=0.55, height=0.80).moved(Location((0, 0, 1.40)))
        square_seat = Cylinder(radius=0.70, height=0.45).moved(Location((0, 0, 1.00)))
        bot_pivot = Cylinder(radius=0.55, height=0.70).moved(Location((0, 0, -0.95)))
        msb.part = msb.part + arbor + top_pivot + square_seat + bot_pivot

        # 4. Internal coiled mainspring (spiral layers inside the drum)
        for i in range(3):
            r_c = 1.80 + i * 1.10
            coil = Cylinder(radius=r_c + 0.08, height=0.70) - Cylinder(radius=r_c - 0.08, height=0.80)
            msb.part = msb.part + coil.moved(Location((0, 0, -0.10)))

        msb.part.color = srgb("#E5C07B")  # Warm golden brass
        msb.part.cad_material = {"roughness": 0.22, "metalness": 0.90}

    return msb.part


if __name__ == "__main__":
    mainspring_barrel()
