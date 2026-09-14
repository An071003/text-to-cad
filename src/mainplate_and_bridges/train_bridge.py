"""Train Bridge (Cầu bánh răng truyền động) Model for Caliber ETA 6497/6498.

Supports center wheel, third wheel, fourth wheel, and escape wheel arbors.
Updated to exactly match the corrected horological layout:
- CENTER_PIVOT = (0.0, 0.0)
- THIRD_PIVOT  = (-5.5863, 3.7890)
- FOURTH_PIVOT = (-9.0000, 0.0000)
- ESCAPE_PIVOT = (-7.6403, 4.1846)
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
    Plane,
    Polygon,
    extrude,
)
from cadgen import srgb, step

from lib.datums import (
    CENTER_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    THIRD_PIVOT,
    TRAIN_BRIDGE_PINS,
    TRAIN_BRIDGE_SCREWS,
)


@step(out="../../STEP/train_bridge.step")
def train_bridge():
    bridge_thickness = 1.65

    with BuildPart() as tb:
        # Contoured polygon spanning center to the gear pivots (avoiding pallet cock & balance)
        with BuildSketch():
            contour_pts = [
                (-2.50, -2.00),
                (4.00, -2.00),
                (6.50, 2.50),
                (4.50, 4.80),
                (0.00, 5.00),
                (-4.00, 5.20),
                (-8.50, 5.20),
                (-10.50, 4.60),
                (-11.50, 2.50),
                (-11.50, -1.50),
                (-8.00, -2.00),
            ]
            Polygon(contour_pts)
        extrude(amount=bridge_thickness)

        # Underside clearance pockets for rotating wheels (depth 1.12 mm up along +Z from Plane.XY)
        with BuildSketch(Plane.XY):
            with Locations([CENTER_PIVOT]):
                Circle(radius=6.40)
            with Locations([THIRD_PIVOT]):
                Circle(radius=4.80)
            with Locations([FOURTH_PIVOT]):
                Circle(radius=4.30)
            with Locations([ESCAPE_PIVOT]):
                Circle(radius=3.50)
        extrude(amount=1.12, mode=Mode.SUBTRACT)

        top_plane = Plane.XY.offset(bridge_thickness)

        # Jewel holes (through holes Ø 1.20 mm, r = 0.60 mm)
        jewel_positions = [CENTER_PIVOT, THIRD_PIVOT, FOURTH_PIVOT, ESCAPE_PIVOT]
        with BuildSketch(top_plane):
            with Locations(jewel_positions):
                Circle(radius=0.60)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

        # Chaton / jewel recess counterbore (Ø 1.80 mm, depth 0.35 mm)
        with BuildSketch(top_plane):
            with Locations(jewel_positions):
                Circle(radius=0.90)
        extrude(amount=-0.35, mode=Mode.SUBTRACT)

        # Mounting screw holes (M1.2 through hole Ø 1.30 mm + counterbore Ø 2.20 mm)
        for s_pos in TRAIN_BRIDGE_SCREWS:
            with BuildSketch(top_plane):
                with Locations([s_pos]):
                    Circle(radius=0.65)
            extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

            with BuildSketch(top_plane):
                with Locations([s_pos]):
                    Circle(radius=1.10)
            extrude(amount=-0.50, mode=Mode.SUBTRACT)

        # Steady pin holes (Ø 0.80 mm)
        with BuildSketch(top_plane):
            with Locations(TRAIN_BRIDGE_PINS):
                Circle(radius=0.40)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

    part = tb.part
    part.color = srgb("#D8DEE9")  # Satin rhodium
    part.cad_material = {"roughness": 0.30, "metalness": 0.88}
    return part


if __name__ == "__main__":
    train_bridge()
