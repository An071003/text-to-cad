"""Balance Wheel & Staff (Vành bánh xe cân bằng & Trục) Model for Caliber ETA 6497/6498.

Specs:
- Screw balance wheel: Ø 11.50 mm, Glucydur / beryllium bronze alloy
- 3 radial spokes, central hub
- Peripheral timing screws (12 balance screws around the rim)
- Balance staff with conical pivots for Incabloc shock setting
- Mating Datum: BALANCE_PIVOT (-4.20, 11.80)
"""

import math
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
    Mode,
    PolarLocations,
    Polygon,
    extrude,
)
from cadgen import step


@step(out="../../STEP/balance_wheel.step")
def balance_wheel():
    rim_outer_r = 5.75  # Ø 11.50 mm
    rim_inner_r = 5.10
    rim_thickness = 0.45

    with BuildPart() as bw:
        # 1. Main balance rim
        with BuildSketch():
            Circle(radius=rim_outer_r)
            Circle(radius=rim_inner_r, mode=Mode.SUBTRACT)
        extrude(amount=rim_thickness)

        # 2. Central hub and 3 spokes
        with BuildSketch():
            Circle(radius=0.90)  # Hub
        extrude(amount=rim_thickness)

        # 3 Straight arms/spokes connecting hub to rim
        for angle in [0, 120, 240]:
            with BuildSketch():
                arm_pts = [
                    (-0.25, 0.80),
                    (0.25, 0.80),
                    (0.25, rim_inner_r + 0.1),
                    (-0.25, rim_inner_r + 0.1),
                ]
                # Rotate arm
                rad = math.radians(angle)
                rot_pts = [
                    (x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad))
                    for x, y in arm_pts
                ]
                Polygon(rot_pts)
            extrude(amount=rim_thickness)

        # 3. Balance screws on the outer periphery (12 screws for poise and inertia)
        with BuildSketch(bw.faces().sort_by().last):
            with PolarLocations(radius=rim_outer_r + 0.15, count=12):
                Circle(radius=0.25)
        extrude(amount=0.50)

        # 4. Balance Staff (Arbor with precision pivots)
        staff = Cylinder(radius=0.35, height=2.60)
        # Upper conical pivot
        pivot_top = Cylinder(radius=0.07, height=0.35).moved(Location((0, 0, 1.45)))
        # Lower conical pivot
        pivot_bot = Cylinder(radius=0.07, height=0.35).moved(Location((0, 0, -1.45)))
        full_staff = staff + pivot_top + pivot_bot
        bw.part = bw.part + full_staff

        # Position assembly at balance plane Z = 0.85
        bw.part = bw.part.moved(Location((0, 0, 0.85)))

    return bw.part


if __name__ == "__main__":
    balance_wheel()
