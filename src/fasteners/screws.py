"""Horological Screws (Bộ vít chuyên dụng đồng hồ) Model for Caliber ETA 6497/6498.

Generates standard watch screws:
- M1.2 Bridge Screws (flat cheese head with screwdriver slot)
- M1.6 Ratchet Wheel Screw
- M1.4 Crown Wheel Screw
- M1.0 Small Mechanism Screws
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import (
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Location,
    Mode,
    Rectangle,
    extrude,
)
from cadgen import srgb, step


from lib.datums import (
    BALANCE_COCK_SCREW,
    BARREL_BRIDGE_SCREWS,
    BARREL_PIVOT,
    PALLET_COCK_SCREW,
    TRAIN_BRIDGE_SCREWS,
)


def make_watch_screw(thread_diameter: float, length: float, head_diameter: float, head_height: float, slot_w: float = 0.25):
    """Generate a high-finish slotted watch screw."""
    with BuildPart() as sc:
        # Cylindrical threaded shank
        shank = Cylinder(radius=thread_diameter / 2.0, height=length)

        # Cylindrical flat head
        head = Cylinder(radius=head_diameter / 2.0, height=head_height)
        head = head.moved(Location((0, 0, (length + head_height) / 2.0)))

        full_screw = shank + head

        # Screwdriver slot
        slot_box = Box(head_diameter * 1.2, slot_w, head_height * 0.7)
        slot_box = slot_box.moved(Location((0, 0, (length + head_height) / 2.0 + head_height * 0.35)))

        full_screw = full_screw - slot_box
        sc.part = full_screw

    return sc.part


@step(out="../../STEP/screws.step")
def screws():
    with BuildPart() as bp:
        all_screws = []

        # 1. Train bridge screws
        for s_pos in TRAIN_BRIDGE_SCREWS:
            s = make_watch_screw(0.95, 1.00, 1.90, 0.40, 0.25).moved(Location((s_pos[0], s_pos[1], 0.90)))
            all_screws.append(s)

        # 2. Barrel bridge screws
        for s_pos in BARREL_BRIDGE_SCREWS:
            s = make_watch_screw(0.95, 1.00, 1.90, 0.40, 0.25).moved(Location((s_pos[0], s_pos[1], 0.90)))
            all_screws.append(s)

        # 3. Balance cock screw
        s_bc = make_watch_screw(0.95, 1.20, 1.90, 0.40, 0.25).moved(Location((BALANCE_COCK_SCREW[0], BALANCE_COCK_SCREW[1], 1.30)))
        all_screws.append(s_bc)

        # 4. Pallet cock screw
        s_pc = make_watch_screw(0.95, 0.80, 1.90, 0.35, 0.25).moved(Location((PALLET_COCK_SCREW[0], PALLET_COCK_SCREW[1], 0.20)))
        all_screws.append(s_pc)

        # 5. Ratchet and Crown wheel screws
        s_ratchet = make_watch_screw(1.10, 1.00, 2.80, 0.40, 0.30).moved(Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 1.90)))
        s_crown = make_watch_screw(1.00, 0.80, 2.40, 0.35, 0.28).moved(Location((4.50, -6.50, 1.50)))
        all_screws.extend([s_ratchet, s_crown])

        combined = all_screws[0]
        for sc in all_screws[1:]:
            combined = combined + sc

        bp.part = combined
        bp.part.color = srgb("#2B4C7E")  # Classic heat-blued steel
        bp.part.cad_material = {"roughness": 0.10, "metalness": 0.98}

    return bp.part


if __name__ == "__main__":
    screws()
