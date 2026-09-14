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
from cadgen import srgb, step


from lib.datums import (
    BALANCE_PIVOT,
    CENTER_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    PALLET_PIVOT,
    THIRD_PIVOT,
)


def make_olive_jewel(outer_r: float = 0.55, inner_r: float = 0.18, height: float = 0.30):
    """Synthetic ruby olive hole jewel ring."""
    with BuildPart() as oj:
        with BuildSketch():
            Circle(radius=outer_r)
            Circle(radius=inner_r, mode=Mode.SUBTRACT)
        extrude(amount=height)
        with BuildSketch(oj.faces().sort_by().last):
            Circle(radius=outer_r * 0.70)
        extrude(amount=-0.08, mode=Mode.SUBTRACT)
    return oj.part


@step(out="../../STEP/jewels.step")
def jewels():
    all_jewels = []

    # 1. Upper train bridge ruby jewels (seated at Z = 1.30)
    for p in [CENTER_PIVOT, THIRD_PIVOT, FOURTH_PIVOT, ESCAPE_PIVOT]:
        j = make_olive_jewel(0.55, 0.18, 0.28).moved(Location((p[0], p[1], 1.32)))
        all_jewels.append(j)

    # 2. Pallet cock jewel (seated at Z = 0.50)
    j_pallet = make_olive_jewel(0.45, 0.12, 0.25).moved(Location((PALLET_PIVOT[0], PALLET_PIVOT[1], 0.52)))
    all_jewels.append(j_pallet)

    # 3. Balance upper shock jewel & Incabloc spring
    j_bal = Cylinder(radius=0.65, height=0.25).moved(Location((BALANCE_PIVOT[0], BALANCE_PIVOT[1], 1.75)))
    all_jewels.append(j_bal)

    # Incabloc Lyre spring on balance cock
    with BuildPart() as sp:
        with BuildSketch():
            lyre_pts = [
                (0.0, -0.55),
                (0.60, -0.50),
                (0.75, -0.10),
                (0.50, 0.35),
                (0.65, 0.70),
                (0.30, 0.78),
                (0.15, 0.50),
                (0.0, 0.58),
                (-0.15, 0.50),
                (-0.30, 0.78),
                (-0.65, 0.70),
                (-0.50, 0.35),
                (-0.75, -0.10),
                (-0.60, -0.50),
            ]
            Polygon(lyre_pts)
        extrude(amount=0.08)
    spring_part = sp.part.moved(Location((BALANCE_PIVOT[0], BALANCE_PIVOT[1], 1.90)))
    all_jewels.append(spring_part)

    combined = all_jewels[0]
    for j in all_jewels[1:]:
        combined = combined + j

    combined.color = srgb("#C01C46")  # Synthetic pigeon-blood ruby
    combined.cad_material = {"roughness": 0.10, "opacity": 0.75, "clearcoat": 1.0}
    return combined


if __name__ == "__main__":
    jewels()
