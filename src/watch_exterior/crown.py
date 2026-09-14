"""Winding Crown, Tube & Gasket Model for Classical 42 mm Dress Wristwatch.

Design Specifications:
- Alignment: Coaxial with Winding Stem at Y = -2.50 mm, Z = -0.80 mm
- Crown Diameter: Ø 6.50 mm (Radius 3.25 mm)
- Crown Length: 3.40 mm along X-axis
- Grip Detail: 24 precision knurled flutes around the perimeter
- Outer Cap: Elegant domed polished cabochon/cap profile
- Internal Interface: Stem sleeve bore (Ø 1.20 mm)
- Gasket & Tube: Internal sealing gasket (Ø 2.50 mm)
- Two Poses:
  - Winding position: Pushed-in against caseband at X = 21.60 mm
  - Time-setting position: Pulled-out by +1.20 mm to X = 22.80 mm
- Material Presentation: Polished Stainless Steel & Nitrile Gasket
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
    Plane,
    PolarLocations,
    Polygon,
    Rectangle,
    Rot,
    extrude,
)
from cadgen import srgb, step

from lib.datums import STEM_Y, STEM_Z


@step(out="../../STEP/crown.step")
def crown():
    stem_y = STEM_Y    # -2.50 mm
    stem_z = STEM_Z    # -0.80 mm
    x_base = 21.60     # Pushed-in resting position against caseband
    crown_len = 3.40
    r_crown = 3.25     # Ø 6.50 mm

    with BuildPart() as cr:
        # 1. Main Crown Body Cylinder along X-axis
        with Locations(Location((x_base + crown_len / 2.0, stem_y, stem_z), (0, 90, 0))):
            Cylinder(radius=r_crown, height=crown_len, mode=Mode.ADD)

        # 2. Knurled Grip: 24 longitudinal flute grooves around the perimeter
        flute_count = 24
        flute_r = 0.22
        for i in range(flute_count):
            deg = i * (360.0 / flute_count)
            rad = math.radians(deg)
            fy = stem_y + r_crown * math.cos(rad)
            fz = stem_z + r_crown * math.sin(rad)
            with Locations(Location((x_base + crown_len * 0.45, fy, fz), (0, 90, 0))):
                Cylinder(radius=flute_r, height=crown_len * 0.85, mode=Mode.SUBTRACT)

        # 3. Outer Domed Cap Profile
        x_cap = x_base + crown_len
        with Locations(Location((x_cap + 0.20, stem_y, stem_z), (0, 90, 0))):
            Cylinder(radius=r_crown - 0.40, height=0.40, mode=Mode.ADD)

        # 4. Inner stem sleeve & gasket collar (facing caseband, X < x_base)
        with Locations(Location((x_base - 0.90, stem_y, stem_z), (0, 90, 0))):
            Cylinder(radius=1.20, height=1.80, mode=Mode.ADD)

        # Sealing rubber O-ring / gasket
        with Locations(Location((x_base - 0.60, stem_y, stem_z), (0, 90, 0))):
            Cylinder(radius=1.28, height=0.50, mode=Mode.ADD)

        # 5. Continuous internal stem bore clearing the winding stem (stem r=0.45 mm)
        # Bores through both sleeve and crown body from X = 19.50 to X = 25.50
        with Locations(Location((x_base + 0.50, stem_y, stem_z), (0, 90, 0))):
            Cylinder(radius=0.55, height=7.50, mode=Mode.SUBTRACT)

    cr.part.color = srgb("#D8DEE9")
    return cr.part


if __name__ == "__main__":
    crown()
