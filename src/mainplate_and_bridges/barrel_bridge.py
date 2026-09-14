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
    Plane,
    PolarLocations,
    Polygon,
    Rectangle,
    extrude,
)
from cadgen import srgb, step

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

        # Trim outer perimeter to strictly conform to caliber circular boundary (radius 18.30 mm)
        with BuildSketch(Plane.XY):
            Circle(radius=outer_r + 6.0)
            Circle(radius=outer_r, mode=Mode.SUBTRACT)
        extrude(amount=bridge_thickness + 0.10, mode=Mode.SUBTRACT)

        # Underside barrel clearance pocket (depth 0.90 mm from Z=0)
        with BuildSketch(Plane.XY):
            with Locations([BARREL_PIVOT]):
                Circle(radius=7.80)
        extrude(amount=0.90, mode=Mode.SUBTRACT)

        top_plane = Plane.XY.offset(bridge_thickness)

        # Barrel arbor upper pivot bushing hole (Ø 2.50 mm)
        with BuildSketch(top_plane):
            with Locations([BARREL_PIVOT]):
                Circle(radius=1.25)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

        # Crown wheel screw recess (X = 4.50, Y = -6.50)
        with BuildSketch(top_plane):
            with Locations([(4.50, -6.50)]):
                Circle(radius=3.50)
        extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Ratchet wheel core recess around barrel arbor
        with BuildSketch(top_plane):
            with Locations([BARREL_PIVOT]):
                Circle(radius=4.20)
        extrude(amount=-0.50, mode=Mode.SUBTRACT)

        # Mounting screw holes (3 holes, M1.2 through hole Ø 1.30 mm + counterbore Ø 2.20 mm)
        for s_pos in BARREL_BRIDGE_SCREWS:
            with BuildSketch(top_plane):
                with Locations([s_pos]):
                    Circle(radius=0.65)
            extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

            with BuildSketch(top_plane):
                with Locations([s_pos]):
                    Circle(radius=1.10)
            extrude(amount=-0.60, mode=Mode.SUBTRACT)

        # Steady pin holes (2 holes, Ø 0.80 mm)
        with BuildSketch(top_plane):
            with Locations(BARREL_BRIDGE_PINS):
                Circle(radius=0.40)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

    part = bb.part
    part.color = srgb("#D8DEE9")
    part.cad_material = {"roughness": 0.30, "metalness": 0.88}
    return part


if __name__ == "__main__":
    barrel_bridge()
