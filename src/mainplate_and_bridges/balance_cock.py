"""Balance Cock (Cầu bánh xe cân bằng) Model for Caliber ETA 6497/6498.

Supports upper shock jewel (Incabloc) for balance staff, regulator, and hairspring stud.
Updated to exactly enclose:
- BALANCE_PIVOT = (-3.3364, 10.9647)
- BALANCE_COCK_SCREW = (-0.50, 14.50)
- BALANCE_COCK_PINS = [(-2.00, 13.80), (1.00, 14.00)]
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
    Locations,
    Mode,
    Plane,
    Polygon,
    extrude,
)
from cadgen import srgb, step

from lib.datums import (
    BALANCE_COCK_PINS,
    BALANCE_COCK_SCREW,
    BALANCE_PIVOT,
)


@step(out="../../STEP/balance_cock.step")
def balance_cock():
    cock_height = 2.10

    with BuildPart() as bc:
        # Elegant cantilever arm reaching to balance pivot
        with BuildSketch():
            contour_pts = [
                (2.00, 14.50),
                (2.00, 17.50),
                (-3.50, 17.50),
                (-5.50, 14.50),
                (-5.50, 10.00),
                (-2.00, 10.00),
                (-2.00, 13.00),
                (1.50, 13.50),
            ]
            Polygon(contour_pts)
        extrude(amount=cock_height)

        # Underside clearance pocket for balance wheel and hairspring (depth 1.60 mm from Z=0)
        with BuildSketch(Plane.XY):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=6.40)
        extrude(amount=1.60, mode=Mode.SUBTRACT)

        top_plane = Plane.XY.offset(cock_height)

        # Incabloc shock absorber setting hole (through hole Ø 1.50 mm)
        with BuildSketch(top_plane):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=0.75)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

        # Shock spring recess counterbore (Ø 2.20 mm, depth 0.60 mm)
        with BuildSketch(top_plane):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=1.10)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Mounting screw hole (M1.2 through hole + counterbore)
        with BuildSketch(top_plane):
            with Locations([BALANCE_COCK_SCREW]):
                Circle(radius=0.65)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

        with BuildSketch(top_plane):
            with Locations([BALANCE_COCK_SCREW]):
                Circle(radius=1.10)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Steady pin holes
        with BuildSketch(top_plane):
            with Locations(BALANCE_COCK_PINS):
                Circle(radius=0.40)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

    part = bc.part
    part.color = srgb("#D8DEE9")
    part.cad_material = {"roughness": 0.30, "metalness": 0.88}
    return part


if __name__ == "__main__":
    balance_cock()
