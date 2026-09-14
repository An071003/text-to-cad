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
from cadgen import step


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
        # M1.2 Bridge screw (head Ø 2.0, shank M1.2 x 2.2)
        s_m12 = make_watch_screw(1.20, 2.20, 2.00, 0.60, 0.28)

        # M1.6 Ratchet screw (wide head Ø 3.4, shank M1.6 x 1.8)
        s_m16 = make_watch_screw(1.60, 1.80, 3.40, 0.50, 0.35).moved(Location((3.5, 0, 0)))

        # M1.4 Crown screw (head Ø 2.6, shank M1.4 x 1.6)
        s_m14 = make_watch_screw(1.40, 1.60, 2.60, 0.45, 0.30).moved(Location((-3.5, 0, 0)))

        # M1.0 Setting screw (head Ø 1.6, shank M1.0 x 1.5)
        s_m10 = make_watch_screw(1.00, 1.50, 1.60, 0.40, 0.22).moved(Location((0, 3.0, 0)))

        bp.part = s_m12 + s_m16 + s_m14 + s_m10

    return bp.part


if __name__ == "__main__":
    screws()
