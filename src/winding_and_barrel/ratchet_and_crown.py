"""Ratchet & Crown Wheels with Click Mechanism Model for Caliber ETA 6497/6498.

Specs:
- Ratchet Wheel: z = 42 teeth, m = 0.22 mm (Ø ~9.60 mm), square arbor bore.
- Crown Wheel: z = 30 teeth, m = 0.20 mm (Ø ~6.40 mm), center bushing.
- Click & Click Spring: One-way winding pawl assembly.
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
    Location,
    Locations,
    Mode,
    PolarLocations,
    Polygon,
    Rectangle,
    extrude,
)
from cadgen import step

from lib.datums import BARREL_PIVOT
from lib.gears import make_watch_wheel


@step(out="../../STEP/ratchet_and_crown.step")
def ratchet_and_crown():
    crown_pos = (3.50, -6.00)
    click_pos = (-8.50, -13.00)

    with BuildPart() as rc:
        # 1. Ratchet Wheel (z = 42)
        rw = make_watch_wheel(
            teeth=42,
            module=0.22,
            rim_thickness=0.50,
            hub_diameter=3.00,
            arbor_hole=0.0,
            spoke_count=0,
        )
        # Square drive hole for barrel arbor
        with BuildSketch(rw.faces().sort_by().last):
            Rectangle(1.10, 1.10)
        rw_part = rw - extrude(amount=0.50)
        rw_part = rw_part.moved(Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 1.40)))

        # 2. Crown Wheel (z = 30)
        cw = make_watch_wheel(
            teeth=30,
            module=0.20,
            rim_thickness=0.45,
            hub_diameter=2.40,
            arbor_hole=1.20,
            spoke_count=0,
        )
        cw_part = cw.moved(Location((crown_pos[0], crown_pos[1], 1.40)))

        # 3. Click (steel pawl)
        with BuildSketch():
            click_pts = [
                (0.0, 0.0),
                (1.80, 0.60),
                (2.20, 1.40),
                (1.40, 1.20),
                (0.0, 0.80),
                (-0.40, 0.40),
            ]
            Polygon(click_pts)
        extrude(amount=0.40)
        # Screw pivot hole for click
        with BuildSketch(rc.faces().sort_by().last):
            Circle(radius=0.40)
        extrude(amount=-0.40, mode=Mode.SUBTRACT)
        click_part = rc.part.moved(Location((click_pos[0], click_pos[1], 1.40)))

        # 4. Click spring (curved wire spring)
        with BuildSketch():
            Circle(radius=1.80)
            Circle(radius=1.55, mode=Mode.SUBTRACT)
            with Locations([(-1.0, 0)]):
                Rectangle(2.5, 3.0)  # cut half of ring to make a curved wire
        extrude(amount=0.30)
        cspring = rc.part.faces().sort_by().last
        cspring_part = rc.part.moved(Location((click_pos[0] - 1.2, click_pos[1] - 0.5, 1.40)))

        rc.part = rw_part + cw_part + click_part + cspring_part

    return rc.part


if __name__ == "__main__":
    ratchet_and_crown()
