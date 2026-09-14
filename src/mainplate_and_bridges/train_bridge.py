"""Train Bridge (Cầu bánh răng truyền động) Model for Caliber ETA 6497/6498.

Supports center wheel, third wheel, fourth wheel, and escape wheel arbors.
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
    Location,
    Locations,
    Mode,
    Polygon,
    extrude,
)
from cadgen import step

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
    bridge_thickness = 1.30

    with BuildPart() as tb:
        # Contoured polygon spanning center to the gear pivots
        with BuildSketch():
            contour_pts = [
                (-1.50, -1.50),
                (3.00, -2.00),
                (9.00, 0.00),
                (16.50, 2.00),
                (16.50, 7.50),
                (10.00, 15.50),
                (4.00, 16.50),
                (-3.00, 14.50),
                (-8.50, 13.00),
                (-14.50, 9.50),
                (-14.50, 5.00),
                (-8.00, 1.50),
            ]
            Polygon(contour_pts)
        extrude(amount=bridge_thickness)

        top_face = tb.faces().sort_by().last

        # Jewel holes (through holes Ø 1.20 mm, r = 0.60 mm)
        jewel_positions = [CENTER_PIVOT, THIRD_PIVOT, FOURTH_PIVOT, ESCAPE_PIVOT]
        with BuildSketch(top_face):
            with Locations(jewel_positions):
                Circle(radius=0.60)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

        # Chaton / jewel recess counterbore (Ø 1.80 mm, depth 0.40 mm)
        with BuildSketch(top_face):
            with Locations(jewel_positions):
                Circle(radius=0.90)
        extrude(amount=-0.40, mode=Mode.SUBTRACT)

        # Mounting screw holes (M1.2 through hole Ø 1.30 mm + counterbore Ø 2.20 mm)
        for s_pos in TRAIN_BRIDGE_SCREWS:
            with BuildSketch(top_face):
                with Locations([s_pos]):
                    Circle(radius=0.65)
            extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

            with BuildSketch(top_face):
                with Locations([s_pos]):
                    Circle(radius=1.10)
            extrude(amount=-0.50, mode=Mode.SUBTRACT)

        # Steady pin holes (Ø 0.80 mm)
        with BuildSketch(top_face):
            with Locations(TRAIN_BRIDGE_PINS):
                Circle(radius=0.40)
        extrude(amount=-bridge_thickness, mode=Mode.SUBTRACT)

    return tb.part


if __name__ == "__main__":
    train_bridge()
