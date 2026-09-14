"""Continuous Archimedean Spiral Hairspring & Collet for Caliber ETA 6497/6498.

High-horology hairspring specification:
- Continuous flat Archimedean spiral spring with 8 active coils.
- Slotted brass collet for friction fit on balance staff.
- Terminal stud block and regulator pins for timing adjustment.
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
    Locations,
    Mode,
    Polygon,
    Rectangle,
    extrude,
)
from cadgen import srgb, step


@step(out="../../STEP/hairspring.step")
def hairspring():
    coil_count = 8
    pitch = 0.22  # distance between coils (mm)
    r_start = 0.65
    strip_w = 0.04
    height = 0.12

    theta_max = 2.0 * math.pi * coil_count
    steps = 36 * coil_count  # 10 degrees per step for smooth curve
    outer_pts = []
    inner_pts = []

    for i in range(steps + 1):
        theta = (i / steps) * theta_max
        r = r_start + (pitch / (2.0 * math.pi)) * theta
        r_out = r + strip_w / 2.0
        r_in = r - strip_w / 2.0

        outer_pts.append((r_out * math.cos(theta), r_out * math.sin(theta)))
        inner_pts.append((r_in * math.cos(theta), r_in * math.sin(theta)))

    polygon_pts = outer_pts + list(reversed(inner_pts))

    with BuildPart() as hs:
        # 1. Continuous Archimedean Spiral Ribbon and Collet Ring
        with BuildSketch():
            Polygon(polygon_pts)
            Circle(radius=0.55)
            Circle(radius=0.35, mode=Mode.SUBTRACT)
        extrude(amount=height)

        # 2. Split slot on collet
        with BuildSketch(Location((0, 0, 0))):
            with Locations([(0.42, 0)]):
                Rectangle(0.35, 0.08)
        extrude(amount=height + 0.15, mode=Mode.SUBTRACT)

        # 3. Outer Terminal Stud Block (Hairspring Stud)
        end_theta = theta_max
        end_r = r_start + (pitch / (2.0 * math.pi)) * end_theta
        stud_x = end_r * math.cos(end_theta)
        stud_y = end_r * math.sin(end_theta)

        with BuildSketch(Location((stud_x + 0.2, stud_y, 0))):
            Rectangle(0.50, 0.40)
            Circle(radius=0.10, mode=Mode.SUBTRACT)  # Pin hole
        extrude(amount=0.35)

        # 4. Regulator Index Pins (Gắp vi chỉnh nhanh/chậm)
        reg_r = end_r - 0.25
        with BuildSketch(Location((reg_r * 0.95, -0.30, 0))):
            Circle(radius=0.08)
            with Locations([(0.20, 0)]):
                Circle(radius=0.08)
        extrude(amount=0.45)

    part = hs.part
    part.color = srgb("#8892B0")  # Blued/tempered hairspring steel
    part.cad_material = {"roughness": 0.25, "metalness": 0.90}
    return part


if __name__ == "__main__":
    p = hairspring()
    print(f"Hairspring created: {len(p.faces())} faces, {len(p.edges())} edges")
