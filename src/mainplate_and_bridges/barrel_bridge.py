"""Barrel Bridge (Cầu hộp cót) Model for Caliber ETA 6497/6498.

Covers the mainspring barrel, crown wheel, and ratchet mechanism.
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
    Cylinder,
    Location,
    Locations,
    Mode,
    PolarLocations,
    Polygon,
    Rectangle,
    extrude,
    fillet,
)
from cadgen import step

from lib.datums import (
    BARREL_BRIDGE_PINS,
    BARREL_BRIDGE_SCREWS,
    BARREL_PIVOT,
    CENTER_PIVOT,
)
from lib.parameters import MAINPLATE_DIAMETER


@step(out="../../STEP/barrel_bridge.step")
def barrel_bridge():
    bridge_thickness = 1.40
    outer_r = MAINPLATE_DIAMETER / 2.0  # 18.30 mm

    with BuildPart() as bb:
        # Base contoured shape of the barrel bridge covering quadrant 3 & 4
        with BuildSketch():
            # Approximate the perimeter enclosing the barrel, screws, and pins
            contour_pts = [
                (-17.50, -3.00),
                (-17.50, -11.50),
                (-8.00, -17.50),
                (3.50, -17.50),
                (9.50, -13.00),
                (4.00, -5.50),
                (0.0, -2.50),
                (-5.50, -2.50),
            ]
            Polygon(contour_pts)
        extrude(amount=bridge_thickness)

        top_face = bb.faces().sort_by().last

        # Recess for Ratchet Wheel on top face
        with BuildSketch(top_face):
            with Locations([BARREL_PIVOT]):
                Circle(radius=8.50)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Recess for Crown Wheel
        crown_center = (3.50, -6.00)
        with BuildSketch(top_face):
            with Locations([crown_center]):
                Circle(radius=5.20)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Barrel Arbor upper pivot hole (through hole)
        with BuildSketch(top_face):
            with Locations([BARREL_PIVOT]):
                Circle(radius=1.00)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

        # Crown Wheel center post / hole
        with BuildSketch(top_face):
            with Locations([crown_center]):
                Circle(radius=1.20)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

        # Screw counterbore holes (M1.2 screws)
        for s_pos in BARREL_BRIDGE_SCREWS:
            # Through hole Ø 1.30 mm
            with BuildSketch(top_face):
                with Locations([s_pos]):
                    Circle(radius=0.65)
            extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

            # Counterbore pocket Ø 2.30 mm, depth 0.60 mm
            with BuildSketch(top_face):
                with Locations([s_pos]):
                    Circle(radius=1.15)
            extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Steady pin holes (Ø 0.80 mm blind/through)
        with BuildSketch(top_face):
            with Locations(BARREL_BRIDGE_PINS):
                Circle(radius=0.40)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

    return bb.part


if __name__ == "__main__":
    barrel_bridge()
