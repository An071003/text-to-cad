"""Exhibition Caseback & Movement Spacer Ring for Classical 42 mm Dress Wristwatch.

Design Specifications:
- Caseback Outer Diameter: 42.00 mm (matching caseband)
- Exhibition Window Aperture: Ø 32.00 mm (wide panoramic view of bridges, jewels & balance)
- Sapphire Caseback Disc: Ø 33.60 mm, thickness 0.90 mm (Z = +3.10 mm to Z = +4.00 mm)
- Bridge Clearance: >= 0.30 mm above highest bridge points (Z = +2.80 mm)
- Caseback Ring Thickness: Z = +3.20 mm to Z = +4.20 mm
- Tool Key Notches: 6 perimeter wrench notches for classic screw-down appearance
- Inscription: Concentric horological engraving "MECHANICAL WATCH · 18,000 VPH · SAPPHIRE BACK"
- Movement Casing Spacer Ring: Precision collar (Ø 37.40 mm OD, Ø 36.60 mm ID) with clamp tabs
- Material Presentation: Polished Stainless Steel & Optical Exhibition Sapphire
"""

import math
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
    Plane,
    PolarLocations,
    Rectangle,
    Rot,
    extrude,
)
from cadgen import srgb, step


@step(out="../../STEP/caseback.step")
def caseback():
    r_outer = 21.00          # Ø 42.00 mm
    r_window = 16.00         # Ø 32.00 mm exhibition aperture
    r_sapphire = 16.80       # Ø 33.60 mm rear sapphire disc
    z_mount = 3.20           # Mating face with caseband
    z_top = 4.20             # Rear apex of watch
    r_spacer_od = 18.70      # Ø 37.40 mm matching case chamber
    r_spacer_id = 18.30      # Ø 36.60 mm matching movement perimeter

    with BuildPart() as cbk:
        # 1. Main Steel Caseback Ring (Z = +3.20 to Z = +4.20, height 1.00 mm)
        with BuildSketch(Plane.XY.offset(z_mount)):
            Circle(radius=r_outer)
            Circle(radius=r_window, mode=Mode.SUBTRACT)
        extrude(amount=z_top - z_mount)

        # 2. Outer Chamfer / Beveled Profile on Caseback
        with BuildSketch(Plane.XY.offset(z_top - 0.40)):
            Circle(radius=r_outer + 1.0)
            Circle(radius=20.20, mode=Mode.SUBTRACT)
        extrude(amount=0.45, mode=Mode.SUBTRACT)

        # 3. Inner Sapphire Seating Groove (Z = +3.10 to Z = +4.00, radius 16.80 mm)
        with BuildSketch(Plane.XY.offset(z_mount - 0.10)):
            Circle(radius=r_sapphire)
        extrude(amount=0.90, mode=Mode.SUBTRACT)

        # 4. Exhibition Sapphire Glass Disc
        with BuildSketch(Plane.XY.offset(z_mount - 0.10)):
            Circle(radius=r_sapphire - 0.05)
        extrude(amount=0.85, mode=Mode.ADD)

        # 5. Six Tool Notches (screw-down wrench notches on outer rim)
        notch_count = 6
        notch_r = 19.40
        for i in range(notch_count):
            deg = i * (360.0 / notch_count)
            rad = math.radians(deg)
            nx = notch_r * math.cos(rad)
            ny = notch_r * math.sin(rad)
            Box(length=1.40, width=2.40, height=0.60, mode=Mode.SUBTRACT).moved(
                Location((nx, ny, z_top - 0.30), (0, 0, deg))
            )

        # 6. Concentric Inscription Relief Bands
        # "MECHANICAL WATCH · 18,000 VPH · SAPPHIRE BACK"
        with BuildSketch(Plane.XY.offset(z_top)):
            Circle(radius=18.60)
            Circle(radius=18.45, mode=Mode.SUBTRACT)
        extrude(amount=-0.05, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(z_top)):
            Circle(radius=16.90)
            Circle(radius=16.75, mode=Mode.SUBTRACT)
        extrude(amount=-0.05, mode=Mode.SUBTRACT)

        # 7. Internal Movement Casing Spacer Ring (Holder)
        # Sits in caseband cavity between movement OD (18.30) and case ID (18.70)
        # from Z = 0.00 to Z = +2.40 mm
        with BuildSketch(Plane.XY.offset(0.00)):
            Circle(radius=r_spacer_od)
            Circle(radius=r_spacer_id, mode=Mode.SUBTRACT)
        extrude(amount=2.40, mode=Mode.ADD)

        # Three movement clamp dog tabs securing mainplate flange (at 120 deg intervals)
        for i in range(3):
            deg = i * 120.0 + 30.0
            rad = math.radians(deg)
            tx = (r_spacer_id - 0.30) * math.cos(rad)
            ty = (r_spacer_id - 0.30) * math.sin(rad)
            Box(length=1.20, width=1.60, height=0.50, mode=Mode.ADD).moved(
                Location((tx, ty, 0.25), (0, 0, deg))
            )

    cbk.part.color = srgb("#D8DEE9")
    return cbk.part


if __name__ == "__main__":
    caseback()
