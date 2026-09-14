"""Synthetic Ruby Jewels & Shock Springs (Chân kính & Lò xo Incabloc) Model for Caliber ETA 6497/6498.

Components:
- Olive Hole Jewels (chân kính lỗ có vòm chứa dầu bôi trơn)
- Endstone Jewels (chân kính nắp phẳng nén ma sát dọc trục)
- Incabloc Springs (lò xo chống sốc đàn hồi dạng đàn lia)
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
    Mode,
    Polygon,
    extrude,
)
from cadgen import step


@step(out="../../STEP/jewels.step")
def jewels():
    # 1. Olive Hole Jewel (ruby ring with olive oil sink)
    with BuildPart() as hj:
        with BuildSketch():
            Circle(radius=0.60)  # Outer Ø 1.20 mm
            Circle(radius=0.15, mode=Mode.SUBTRACT)  # Pivot hole Ø 0.30 mm
        extrude(amount=0.35)

        with BuildSketch(hj.faces().sort_by().last):
            Circle(radius=0.42)
        extrude(amount=-0.12, mode=Mode.SUBTRACT)

    # 2. Endstone Jewel (flat cap ruby Ø 1.40 x 0.25 mm)
    endstone = Cylinder(radius=0.70, height=0.25).moved(Location((2.20, 0, 0)))

    # 3. Incabloc Shock Spring (Lyre-shaped spring clip)
    with BuildPart() as sp:
        with BuildSketch():
            lyre_pts = [
                (0.0, -0.65),
                (0.75, -0.60),
                (0.95, -0.10),
                (0.60, 0.45),
                (0.80, 0.85),
                (0.40, 0.95),
                (0.20, 0.60),
                (0.0, 0.70),
                (-0.20, 0.60),
                (-0.40, 0.95),
                (-0.80, 0.85),
                (-0.60, 0.45),
                (-0.95, -0.10),
                (-0.75, -0.60),
            ]
            Polygon(lyre_pts)
        extrude(amount=0.10)

    spring_part = sp.part.moved(Location((-2.20, 0, 0)))

    return hj.part + endstone + spring_part


if __name__ == "__main__":
    jewels()
