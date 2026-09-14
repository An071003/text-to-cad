"""Pallet Cock (Cầu neo ngựa) Model for Caliber ETA 6497/6498.

Supports the pallet fork upper jewel.
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
    PALLET_COCK_PINS,
    PALLET_COCK_SCREW,
    PALLET_PIVOT,
)


@step(out="../../STEP/pallet_cock.step")
def pallet_cock():
    cock_thickness = 0.80

    with BuildPart() as pc:
        # Small bridge covering pallet pivot and mounting screw
        with BuildSketch():
            contour_pts = [
                (-7.00, 9.50),
                (-9.00, 9.50),
                (-12.50, 11.00),
                (-12.50, 14.80),
                (-8.50, 15.00),
                (-7.00, 11.50),
            ]
            Polygon(contour_pts)
        extrude(amount=cock_thickness)

        top_face = pc.faces().sort_by().last

        # Pallet jewel hole (through hole Ø 1.00 mm)
        with BuildSketch(top_face):
            with Locations([PALLET_PIVOT]):
                Circle(radius=0.50)
        extrude(amount=-cock_thickness, mode=Mode.SUBTRACT)

        # Jewel counterbore
        with BuildSketch(top_face):
            with Locations([PALLET_PIVOT]):
                Circle(radius=0.75)
        extrude(amount=-0.30, mode=Mode.SUBTRACT)

        # Mounting screw hole (M1.0 through hole Ø 1.10 mm + counterbore Ø 1.80 mm)
        with BuildSketch(top_face):
            with Locations([PALLET_COCK_SCREW]):
                Circle(radius=0.55)
        extrude(amount=-cock_thickness, mode=Mode.SUBTRACT)

        with BuildSketch(top_face):
            with Locations([PALLET_COCK_SCREW]):
                Circle(radius=0.90)
        extrude(amount=-0.35, mode=Mode.SUBTRACT)

        # Steady pin holes (Ø 0.60 mm)
        with BuildSketch(top_face):
            with Locations(PALLET_COCK_PINS):
                Circle(radius=0.30)
        extrude(amount=-cock_thickness, mode=Mode.SUBTRACT)

    return pc.part


if __name__ == "__main__":
    pallet_cock()
