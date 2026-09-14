"""Balance Cock (Cầu bánh xe cân bằng) Model for Caliber ETA 6497/6498.

Supports upper shock jewel (Incabloc) for balance staff, regulator, and hairspring stud.
Mating Datum: Mounts onto Mainplate at Z = 0.
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
    Polygon,
    extrude,
)
from cadgen import step

from lib.datums import (
    BALANCE_COCK_PINS,
    BALANCE_COCK_SCREW,
    BALANCE_PIVOT,
)


@step(out="../../STEP/balance_cock.step")
def balance_cock():
    cock_height = 1.80

    with BuildPart() as bc:
        # Elegant cantilever arm reaching to balance pivot
        with BuildSketch():
            contour_pts = [
                (2.00, 14.50),
                (2.00, 17.50),
                (-3.50, 17.50),
                (-5.50, 14.50),
                (-5.50, 11.00),
                (-3.00, 10.50),
                (-2.50, 13.00),
                (0.50, 13.50),
            ]
            Polygon(contour_pts)
        extrude(amount=cock_height)

        top_face = bc.faces().sort_by().last

        # Incabloc shock absorber setting hole (through hole Ø 1.50 mm)
        with BuildSketch(top_face):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=0.75)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

        # Shock spring recess counterbore (Ø 2.20 mm, depth 0.60 mm)
        with BuildSketch(top_face):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=1.10)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Mounting screw hole (M1.2 through hole Ø 1.30 mm + counterbore Ø 2.20 mm)
        with BuildSketch(top_face):
            with Locations([BALANCE_COCK_SCREW]):
                Circle(radius=0.65)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

        with BuildSketch(top_face):
            with Locations([BALANCE_COCK_SCREW]):
                Circle(radius=1.10)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Steady pin holes (Ø 0.80 mm)
        with BuildSketch(top_face):
            with Locations(BALANCE_COCK_PINS):
                Circle(radius=0.40)
        extrude(amount=-cock_height, mode=Mode.SUBTRACT)

    return bc.part


if __name__ == "__main__":
    balance_cock()
