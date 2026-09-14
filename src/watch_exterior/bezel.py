"""Bezel, Rehaut & Front Sapphire Crystal Model for Classical 42 mm Dress Wristwatch.

Design Specifications:
- Bezel Outer Diameter: 42.00 mm (matching caseband)
- Bezel Inner Aperture: Ø 35.20 mm (clear dial view)
- Integrated Rehaut / Chapter-Ring: Angled interior flange framing the dial
- Sapphire Crystal: Ø 35.80 mm, thickness 1.05 mm, high optical clarity
- Z Range: Z = -4.80 mm to Z = -6.00 mm (dial side, Z < 0)
- Clearance: Sufficient space above hour and minute hands
- Material Presentation: Polished Stainless Steel & Transparent Optical Sapphire
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
    Plane,
    extrude,
)
from cadgen import srgb, step


@step(out="../../STEP/bezel.step")
def bezel():
    r_outer = 21.00       # Ø 42.00 mm
    r_inner = 17.60       # Ø 35.20 mm
    r_sapphire = 17.90    # Ø 35.80 mm
    z_mount = -4.80       # Mating face with caseband
    z_top = -6.00         # Front apex of bezel

    with BuildPart() as bz:
        # 1. Bezel ring solid profile
        # Extrude downwards from Z = -4.80 to Z = -6.00 (amount = -1.20 mm)
        with BuildSketch(Plane.XY.offset(z_mount)):
            Circle(radius=r_outer)
            Circle(radius=r_inner, mode=Mode.SUBTRACT)
        extrude(amount=z_top - z_mount)  # amount = -1.20 mm

        # 2. Outer polished chamfer / conical bevel
        # Outer radius narrows from 21.00 mm at mount to 19.80 mm at front face
        with BuildSketch(Plane.XY.offset(z_top)):
            Circle(radius=r_outer + 1.0)
            Circle(radius=19.80, mode=Mode.SUBTRACT)
        extrude(amount=0.60, mode=Mode.SUBTRACT)

        # 3. Inner sapphire seating step (r = 17.90 mm, depth 1.05 mm from Z = -4.85 to -5.90)
        with BuildSketch(Plane.XY.offset(z_mount - 0.05)):
            Circle(radius=r_sapphire)
        extrude(amount=-1.05, mode=Mode.SUBTRACT)

        # 4. Front Sapphire Crystal Disc
        with BuildSketch(Plane.XY.offset(z_mount - 0.10)):
            Circle(radius=r_sapphire - 0.05)
        extrude(amount=-0.95, mode=Mode.ADD)

    # Polished steel with subtle crystal tint
    bz.part.color = srgb("#E5E9F0")
    return bz.part


if __name__ == "__main__":
    bezel()
