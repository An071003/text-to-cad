"""Roller Table & Impulse Jewel (Mâm quay kép & Chốt ngọc xung động) Model for Caliber ETA 6497/6498.

Specs:
- Double roller: Large roller holding the ruby pin, small safety roller with passing crescent.
- Ruby impulse pin (D-shaped jewel pin) interacting with the pallet fork notch.
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
    Locations,
    Mode,
    Polygon,
    extrude,
)
from cadgen import step


@step(out="../../STEP/roller_table.step")
def roller_table():
    with BuildPart() as rt:
        # 1. Large impulse roller disc
        with BuildSketch():
            Circle(radius=1.10)
            Circle(radius=0.35, mode=Mode.SUBTRACT)  # Staff hole
        extrude(amount=0.20)

        # 2. Small safety roller disc below
        with BuildSketch():
            Circle(radius=0.65)
            Circle(radius=0.35, mode=Mode.SUBTRACT)
        extrude(amount=-0.25)

        # Crescent passing hollow for guard pin
        with BuildSketch():
            with Locations([(0.55, 0.0)]):
                Circle(radius=0.25)
        extrude(amount=-0.25, mode=Mode.SUBTRACT)

        # 3. Ruby Impulse Pin (D-shaped pin)
        with BuildSketch():
            with Locations([(0.80, 0.0)]):
                # D-shape ruby profile
                pin_pts = [
                    (-0.08, -0.15),
                    (0.08, -0.15),
                    (0.12, 0.0),
                    (0.08, 0.15),
                    (-0.08, 0.15),
                ]
                Polygon(pin_pts)
        extrude(amount=0.65)

        # Position below the balance wheel at Z = 0.40
        rt.part = rt.part.moved(Location((0, 0, 0.40)))

    return rt.part


if __name__ == "__main__":
    roller_table()
