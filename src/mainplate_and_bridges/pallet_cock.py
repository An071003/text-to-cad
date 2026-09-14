"""Pallet Cock (Cầu neo ngựa) Model for Caliber ETA 6497/6498.

Supports the pallet fork upper jewel.
Updated to exactly enclose:
- PALLET_PIVOT = (-5.9076, 7.9005)
- PALLET_COCK_SCREW = (-8.50, 9.50)
- PALLET_COCK_PINS = [(-9.50, 8.00), (-7.50, 10.50)]
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
from cadgen import srgb, step

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
                (-5.00, 7.50),
                (-6.50, 7.00),
                (-10.50, 7.50),
                (-10.50, 10.50),
                (-7.00, 11.50),
                (-5.00, 9.00),
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

        # Mounting screw hole (M1.2 through hole + counterbore)
        with BuildSketch(top_face):
            with Locations([PALLET_COCK_SCREW]):
                Circle(radius=0.65)
        extrude(amount=-cock_thickness, mode=Mode.SUBTRACT)

        with BuildSketch(top_face):
            with Locations([PALLET_COCK_SCREW]):
                Circle(radius=1.05)
        extrude(amount=-0.35, mode=Mode.SUBTRACT)

        # Steady pin holes
        with BuildSketch(top_face):
            with Locations(PALLET_COCK_PINS):
                Circle(radius=0.40)
        extrude(amount=-cock_thickness, mode=Mode.SUBTRACT)

    part = pc.part
    part.color = srgb("#D8DEE9")
    part.cad_material = {"roughness": 0.30, "metalness": 0.88}
    return part


if __name__ == "__main__":
    pallet_cock()
