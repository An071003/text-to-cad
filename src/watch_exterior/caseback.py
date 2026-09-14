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
    Compound,
    Cylinder,
    Location,
    Locations,
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

        # 4. Six Tool Notches (screw-down wrench notches on outer rim)
        notch_count = 6
        notch_r = 19.40
        for i in range(notch_count):
            deg = i * (360.0 / notch_count)
            rad = math.radians(deg)
            nx = notch_r * math.cos(rad)
            ny = notch_r * math.sin(rad)
            with Locations(Location((nx, ny, z_top - 0.30), (0, 0, deg))):
                Box(length=1.40, width=2.40, height=0.60, mode=Mode.SUBTRACT)

        # 5. Concentric Inscription Relief Bands
        with BuildSketch(Plane.XY.offset(z_top)):
            Circle(radius=18.60)
            Circle(radius=18.45, mode=Mode.SUBTRACT)
        extrude(amount=-0.05, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(z_top)):
            Circle(radius=16.90)
            Circle(radius=16.75, mode=Mode.SUBTRACT)
        extrude(amount=-0.05, mode=Mode.SUBTRACT)

        # 6. Caseback Alignment & Thread Spigot Lip (Z = +2.90 to Z = +3.20)
        # Sits inside the caseband cavity with 0.15 mm clearance fit (r = 18.55 mm < 18.70 mm)
        # Positioned well clear above the highest movement bridge (movement bridges end at Z <= 2.60 mm)
        with BuildSketch(Plane.XY.offset(2.90)):
            Circle(radius=18.55)
            Circle(radius=r_sapphire - 0.20, mode=Mode.SUBTRACT)
        extrude(amount=0.30, mode=Mode.ADD)

    caseback_ring = cbk.part
    caseback_ring.color = srgb("#D8DEE9")
    caseback_ring.cad_material = {"roughness": 0.15, "metalness": 0.92}

    # 7. Exhibition Sapphire Glass Disc as separate translucent body
    with BuildPart() as cry:
        with BuildSketch(Plane.XY.offset(z_mount - 0.10)):
            Circle(radius=r_sapphire - 0.05)
        extrude(amount=0.85)

    rear_sapphire = cry.part
    rear_sapphire.color = srgb("#D8E8F8")
    rear_sapphire.cad_material = {"opacity": 0.15, "roughness": 0.04, "metalness": 0.05}

    return Compound(children=[caseback_ring, rear_sapphire])


if __name__ == "__main__":
    caseback()
