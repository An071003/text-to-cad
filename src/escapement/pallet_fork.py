"""Pallet Fork (Cần neo ngựa) Assembly Model for Caliber ETA 6497/6498.

Specs:
- Swiss Lever Escapement fork with entry/exit jewel slots and safety dart (guard pin).
- Pallet Arbor with top and bottom fine pivots.
- Mating Datum: PALLET_PIVOT (-8.20, 10.50)
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
    Rectangle,
    extrude,
)
from cadgen import step


@step(out="../../STEP/pallet_fork.step")
def pallet_fork():
    body_thickness = 0.25

    with BuildPart() as pf:
        # Pallet fork body: T-shaped / anchor-shaped structure
        with BuildSketch():
            # Outline connecting arbor hub, entry arm, exit arm, and lever notch
            body_pts = [
                (0.0, -0.60),      # Bottom near arbor
                (1.80, -0.20),     # Exit stone arm
                (2.20, 0.40),
                (1.40, 0.50),
                (0.40, 0.20),
                (0.20, 2.20),      # Fork stem reaching towards balance
                (0.60, 2.60),      # Horn 1
                (0.30, 2.80),
                (0.0, 2.40),       # Fork notch
                (-0.30, 2.80),
                (-0.60, 2.60),     # Horn 2
                (-0.20, 2.20),
                (-0.40, 0.20),
                (-1.40, 0.50),     # Entry stone arm
                (-2.20, 0.40),
                (-1.80, -0.20),
            ]
            Polygon(body_pts)
        extrude(amount=body_thickness)

        top_face = pf.faces().sort_by().last

        # Arbor hole in center of fork hub
        with BuildSketch(top_face):
            Circle(radius=0.25)
        extrude(amount=-body_thickness, mode=Mode.SUBTRACT)

        # Slot for Entry jewel
        with BuildSketch(top_face):
            with Locations([(-1.75, 0.20)]):
                Rectangle(0.50, 0.30)
        extrude(amount=-body_thickness, mode=Mode.SUBTRACT)

        # Slot for Exit jewel
        with BuildSketch(top_face):
            with Locations([(1.75, 0.20)]):
                Rectangle(0.50, 0.30)
        extrude(amount=-body_thickness, mode=Mode.SUBTRACT)

        # Guard pin (dart / chốt an toàn) under the notch
        dart = Cylinder(radius=0.08, height=0.70)
        dart = dart.moved(Location((0.0, 2.35, -0.20)))
        pf.part = pf.part + dart

        # Pallet Arbor shaft with fine pivots
        arbor = Cylinder(radius=0.25, height=1.60)
        # Pivots top and bottom
        pivot_top = Cylinder(radius=0.08, height=0.35).moved(Location((0, 0, 0.95)))
        pivot_bot = Cylinder(radius=0.08, height=0.35).moved(Location((0, 0, -0.95)))
        full_arbor = arbor + pivot_top + pivot_bot
        pf.part = pf.part + full_arbor

    return pf.part


if __name__ == "__main__":
    pallet_fork()
