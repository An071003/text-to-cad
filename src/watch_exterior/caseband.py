"""Case Middle (Caseband) & Lugs Model for Classical 42 mm Dress Wristwatch.

Design Specifications:
- Outer Diameter: 42.00 mm (Radius 21.00 mm)
- Inner Movement Chamber: Ø 37.40 mm (Radius 18.70 mm, clear for Ø 36.60 mm movement)
- Movement Support Ledge: Ø 36.20 mm step at Z = -2.20 mm
- Height: 8.00 mm (Z = -4.80 mm to Z = +3.20 mm)
- Lugs: 4 ergonomic curved lugs, 20.00 mm strap width, 49.80 mm lug-to-lug span
- Spring-Bar Holes: Ø 1.20 mm at Y = +-23.50 mm
- Crown Tube Bore: Coaxial with Winding Stem (Y = -2.50 mm, Z = -0.80 mm)
- Material Presentation: Polished Stainless Steel (silver-gray satin/polished)
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
    Locations,
    Mode,
    Plane,
    extrude,
)
from cadgen import srgb, step

from lib.datums import STEM_Y, STEM_Z


@step(out="../../STEP/caseband.step")
def caseband():
    r_outer = 21.00       # Ø 42.00 mm
    r_chamber = 18.70     # Ø 37.40 mm movement cavity
    r_dial_seat = 17.50   # Ø 35.00 mm front dial aperture
    z_bottom = -4.80
    z_top = 3.20
    height = z_top - z_bottom  # 8.00 mm

    with BuildPart() as cb:
        # 1. Main cylindrical caseband body
        with BuildSketch(Plane.XY.offset(z_bottom)):
            Circle(radius=r_outer)
        extrude(amount=height)

        # 2. Internal cavities
        # 2a. Movement cavity (Ø 37.40 mm) from Z = -2.20 to Z = +3.20
        with BuildSketch(Plane.XY.offset(-2.20)):
            Circle(radius=r_chamber)
        extrude(amount=z_top - (-2.20), mode=Mode.SUBTRACT)

        # 2b. Lower movement dial cavity from Z = -3.80 to Z = -2.20 (Ø 36.80 mm)
        with BuildSketch(Plane.XY.offset(-3.80)):
            Circle(radius=18.40)
        extrude(amount=1.60, mode=Mode.SUBTRACT)

        # 2c. Dial aperture from Z = -4.80 to Z = -3.80 (Ø 35.20 mm)
        with BuildSketch(Plane.XY.offset(z_bottom)):
            Circle(radius=r_dial_seat)
        extrude(amount=1.00, mode=Mode.SUBTRACT)

        # 3. Four sculpted lugs (Lug-to-Lug ~ 49.8 mm, 20.0 mm strap opening)
        lug_w = 2.80
        lug_len = 11.00
        lug_h = 4.80
        lug_z = -3.80

        # Center Y = +-19.40 mm, so outer tip reaches +- (19.40 + 5.50) = +- 24.90 mm -> Lug-to-Lug = 49.80 mm
        lug_centers = [
            (-11.40, 19.40, lug_z + lug_h / 2.0),
            (11.40, 19.40, lug_z + lug_h / 2.0),
            (-11.40, -19.40, lug_z + lug_h / 2.0),
            (11.40, -19.40, lug_z + lug_h / 2.0),
        ]

        for cx, cy, cz in lug_centers:
            with Locations(Location((cx, cy, cz))):
                Box(length=lug_w, width=lug_len, height=lug_h, mode=Mode.ADD)

        # Re-clear internal movement cavity to eliminate any lug corner intrusions
        with BuildSketch(Plane.XY.offset(-2.20)):
            Circle(radius=r_chamber)
        extrude(amount=z_top - (-2.20) + 0.50, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(-3.80)):
            Circle(radius=18.40)
        extrude(amount=1.60, mode=Mode.SUBTRACT)

        # 4. Spring-bar holes (blind holes of Ø 1.20 mm for 20 mm strap attachment)
        sb_radius = 0.60
        sb_depth = 1.50
        sb_y = 23.50
        sb_z = -1.60

        # Top lugs spring-bar holes
        with Locations(Location((-10.00 - sb_depth / 2.0, sb_y, sb_z), (0, 90, 0))):
            Cylinder(radius=sb_radius, height=sb_depth, mode=Mode.SUBTRACT)
        with Locations(Location((10.00 + sb_depth / 2.0, sb_y, sb_z), (0, 90, 0))):
            Cylinder(radius=sb_radius, height=sb_depth, mode=Mode.SUBTRACT)

        # Bottom lugs spring-bar holes
        with Locations(Location((-10.00 - sb_depth / 2.0, -sb_y, sb_z), (0, 90, 0))):
            Cylinder(radius=sb_radius, height=sb_depth, mode=Mode.SUBTRACT)
        with Locations(Location((10.00 + sb_depth / 2.0, -sb_y, sb_z), (0, 90, 0))):
            Cylinder(radius=sb_radius, height=sb_depth, mode=Mode.SUBTRACT)

        # 5. Crown Tube Bore & External Collar
        # Coaxial with winding stem at Y = -2.50, Z = -0.80
        with Locations(Location((19.00, STEM_Y, STEM_Z), (0, 90, 0))):
            Cylinder(radius=1.30, height=8.00, mode=Mode.SUBTRACT)

        # External crown tube collar extending to X = 21.60 mm (Ø 3.40 mm)
        with Locations(Location((20.60, STEM_Y, STEM_Z), (0, 90, 0))):
            Cylinder(radius=1.70, height=2.00, mode=Mode.ADD)

        # Re-bore through collar
        with Locations(Location((20.60, STEM_Y, STEM_Z), (0, 90, 0))):
            Cylinder(radius=1.30, height=4.00, mode=Mode.SUBTRACT)

        # 6. Smooth bevels on case outer edges
        with BuildSketch(Plane.XY.offset(z_top - 0.50)):
            Circle(radius=r_outer + 5.0)
            Circle(radius=r_outer - 0.40, mode=Mode.SUBTRACT)
        extrude(amount=0.60, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(z_bottom - 0.10)):
            Circle(radius=r_outer + 5.0)
            Circle(radius=r_outer - 0.40, mode=Mode.SUBTRACT)
        extrude(amount=0.60, mode=Mode.SUBTRACT)

    # Apply polished stainless steel presentation color
    cb.part.color = srgb("#D8DEE9")
    return cb.part


if __name__ == "__main__":
    caseband()
