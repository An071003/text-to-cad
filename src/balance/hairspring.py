"""Hairspring & Collet (Lò xo dây tóc xoắn ốc & Cổ áo kẹp) Model for Caliber ETA 6497/6498.

Specs:
- Flat Archimedean spiral spring with 10 active coils.
- Slotted brass collet (hairspring collet) for friction fit on balance staff.
- Breguet overcoil / terminal stud block.
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
    Locations,
    Mode,
    Rectangle,
    extrude,
)
from cadgen import step


@step(out="../../STEP/hairspring.step")
def hairspring():
    coil_count = 8
    pitch = 0.22  # distance between coils
    r_start = 0.65
    strip_w = 0.04
    height = 0.12

    with BuildPart() as hs:
        # Collet (central brass ring with slot)
        with BuildSketch():
            Circle(radius=0.55)
            Circle(radius=0.35, mode=Mode.SUBTRACT)
        extrude(amount=0.35)
        # Split slot on collet
        with BuildSketch(hs.faces().sort_by().last):
            with Locations([(0.40, 0)]):
                Rectangle(0.50, 0.10)
        extrude(amount=-0.35, mode=Mode.SUBTRACT)

        # Approximate concentric ring layers for the flat spiral spring
        for i in range(coil_count):
            r = r_start + i * pitch
            with BuildSketch():
                Circle(radius=r + strip_w / 2.0)
                Circle(radius=r - strip_w / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=height)

        # Stud block at the outer terminal end
        stud_pos = (r_start + (coil_count - 1) * pitch, 0.40)
        stud = Cylinder(radius=0.20, height=0.60).moved(Location((stud_pos[0], stud_pos[1], 0.20)))
        hs.part = hs.part + stud

        # Position hairspring above the balance wheel at Z = 1.45
        hs.part = hs.part.moved(Location((0, 0, 1.45)))

    return hs.part


if __name__ == "__main__":
    hairspring()
