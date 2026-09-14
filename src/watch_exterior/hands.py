"""Hands Model for Classical 42 mm Dress Wristwatch (ETA 6497 Reference).

Design Specifications:
- Hour Hand: Classical faceted feuille/dauphine leaf shape, length 10.20 mm, blued steel
  Mounted coaxially at (0.0, 0.0) at Z = -4.48 mm (thickness 0.16 mm)
- Minute Hand: Slender feuille/dauphine leaf shape, length 14.80 mm (reaches minute rail), blued steel
  Mounted coaxially at (0.0, 0.0) at Z = -4.72 mm (thickness 0.16 mm)
- Small Seconds Hand: Fine needle with teardrop counterweight, length 3.60 mm, crimson red accent
  Mounted at Fourth Wheel Pivot (-9.0000, 0.0000) at Z = -4.24 mm (thickness 0.12 mm)
- Clearance:
  Dial applied markers to Seconds hand: >= 0.08 mm
  Seconds hand to Hour hand: >= 0.10 mm
  Hour hand to Minute hand: >= 0.10 mm
  Minute hand to Front Sapphire: >= 0.15 mm
- Material Presentation: Polished Blued Steel & Vivid Crimson Red
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
    Plane,
    Polygon,
    Rectangle,
    Rot,
    extrude,
)
from cadgen import srgb, step

from lib.datums import FOURTH_PIVOT


def make_leaf_blade(length: float, max_width: float, mid_pos: float, thickness: float):
    """Generate a classical feuille (leaf-shaped) watch hand blade."""
    pts = [
        (0.0, 0.0),
        (mid_pos * 0.4, max_width * 0.4),
        (mid_pos, max_width * 0.5),
        (length * 0.8, max_width * 0.35),
        (length, 0.0),
        (length * 0.8, -max_width * 0.35),
        (mid_pos, -max_width * 0.5),
        (mid_pos * 0.4, -max_width * 0.4),
    ]
    with BuildSketch(Plane.XY):
        Polygon(pts)
    return extrude(amount=-thickness)


def hour_hand():
    """Parametric Feuille Hour Hand (blued steel, length 10.20 mm)."""
    z_mount = -4.48
    th = 0.16
    with BuildPart() as hh:
        # Hub collar at center (0, 0)
        Cylinder(radius=1.10, height=th, mode=Mode.ADD).moved(Location((0, 0, z_mount - th / 2.0)))
        Cylinder(radius=0.60, height=th + 0.10, mode=Mode.SUBTRACT).moved(
            Location((0, 0, z_mount - th / 2.0))
        )

        # Leaf blade extending along +Y (default 12 o'clock orientation)
        blade = make_leaf_blade(length=10.20, max_width=1.35, mid_pos=5.50, thickness=th)
        # Rotate blade 90 deg so length aligns with +Y axis
        blade = blade.moved(Location((0, 0, z_mount), (0, 0, 90.0)))
        hh.part = hh.part + blade

    hh.part.color = srgb("#204080")
    return hh.part


def minute_hand():
    """Parametric Feuille Minute Hand (blued steel, length 14.80 mm)."""
    z_mount = -4.72
    th = 0.16
    with BuildPart() as mh:
        # Hub collar at center (0, 0)
        Cylinder(radius=0.90, height=th, mode=Mode.ADD).moved(Location((0, 0, z_mount - th / 2.0)))
        Cylinder(radius=0.45, height=th + 0.10, mode=Mode.SUBTRACT).moved(
            Location((0, 0, z_mount - th / 2.0))
        )

        # Slender blade reaching minute track along +Y
        blade = make_leaf_blade(length=14.80, max_width=1.15, mid_pos=7.50, thickness=th)
        blade = blade.moved(Location((0, 0, z_mount), (0, 0, 90.0)))
        mh.part = mh.part + blade

    mh.part.color = srgb("#204080")
    return mh.part


def seconds_hand():
    """Parametric Small Seconds Needle Hand (crimson red accent, length 3.60 mm)."""
    z_mount = -4.24
    th = 0.12
    sec_x, sec_y = FOURTH_PIVOT

    with BuildPart() as sh:
        # Center boss at Fourth Wheel Pivot (-9.0000, 0.0000)
        Cylinder(radius=0.50, height=th, mode=Mode.ADD).moved(Location((sec_x, sec_y, z_mount - th / 2.0)))
        Cylinder(radius=0.20, height=th + 0.10, mode=Mode.SUBTRACT).moved(
            Location((sec_x, sec_y, z_mount - th / 2.0))
        )

        # Needle pointer along +Y (3.60 mm length, 0.22 mm width)
        pointer_pts = [
            (sec_x - 0.10, sec_y),
            (sec_x - 0.05, sec_y + 3.60),
            (sec_x + 0.05, sec_y + 3.60),
            (sec_x + 0.10, sec_y),
        ]
        with BuildSketch(Plane.XY.offset(z_mount)):
            Polygon(pointer_pts)
        extrude(amount=-th)

        # Teardrop counterweight tail along -Y (1.10 mm length)
        tail_pts = [
            (sec_x - 0.10, sec_y),
            (sec_x - 0.22, sec_y - 0.70),
            (sec_x, sec_y - 1.10),
            (sec_x + 0.22, sec_y - 0.70),
            (sec_x + 0.10, sec_y),
        ]
        with BuildSketch(Plane.XY.offset(z_mount)):
            Polygon(tail_pts)
        extrude(amount=-th)

    sh.part.color = srgb("#D02020")
    return sh.part


@step(out="../../STEP/hands.step")
def hands():
    """Combined hands artifact in classical presentation display pose."""
    # Hour hand oriented towards 10 o'clock (-60 deg)
    h = hour_hand().moved(Location((0, 0, 0), (0, 0, 60.0)))
    # Minute hand oriented towards 2 o'clock (+60 deg) -> classic 10:10 pose
    m = minute_hand().moved(Location((0, 0, 0), (0, 0, -60.0)))
    # Seconds hand oriented towards 30 seconds (+180 deg)
    s = seconds_hand()

    return h + m + s


if __name__ == "__main__":
    hands()
