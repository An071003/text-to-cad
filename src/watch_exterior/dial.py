"""Sector Dial Model for Classical 42 mm Dress Wristwatch (ETA 6497 Reference).

Design Specifications:
- Dial Diameter: Ø 35.00 mm (Radius 17.50 mm)
- Dial Thickness: 0.40 mm (Z = -3.65 mm to Z = -4.05 mm)
- Center Hole: Ø 1.80 mm at (0.0, 0.0) for Cannon Pinion & Hour Wheel Tube
- Small-Seconds Hole: Ø 0.70 mm at (-9.0000, 0.0000) for Fourth Wheel Arbor
- Small-Seconds Subdial: Sunken circular recess (R = 4.60 mm) with radial markers at 9 o'clock
- Applied Indices: Classical 3D faceted baton markers (double baton at 12 o'clock)
- Outer Sector Track: Concentric engraved railroad minute track
- Dial Feet: 2 locating pins on back face extending into mainplate dial recesses
- Typography: Raised horological signatures "MECHANICAL" and "18,000 VPH"
- Material Presentation: Warm ivory/champagne dial with dark rhodium / charcoal markers
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
    Locations,
    Mode,
    Plane,
    PolarLocations,
    Rectangle,
    Rot,
    extrude,
)
from cadgen import srgb, step

from lib.datums import FOURTH_PIVOT


@step(out="../../STEP/dial.step")
def dial():
    r_dial = 17.50        # Ø 35.00 mm
    thickness = 0.40      # Base plate thickness
    z_back = -3.65        # Facing movement motion work
    z_front = -4.05       # Facing hands and front crystal
    sec_pos = FOURTH_PIVOT  # (-9.0000, 0.0000)

    with BuildPart() as d:
        # 1. Main Circular Dial Plate (extruding from Z = -3.65 to Z = -4.05)
        with BuildSketch(Plane.XY.offset(z_back)):
            Circle(radius=r_dial)
        extrude(amount=z_front - z_back)  # amount = -0.40 mm

        # 2. Center arbor clearance hole (Ø 1.80 mm)
        with Locations(Location((0, 0, (z_back + z_front) / 2.0))):
            Cylinder(radius=0.90, height=1.00, mode=Mode.SUBTRACT)

        # 3. Small-seconds arbor clearance hole (Ø 0.70 mm at fourth pivot)
        with Locations(Location((sec_pos[0], sec_pos[1], (z_back + z_front) / 2.0))):
            Cylinder(radius=0.35, height=1.00, mode=Mode.SUBTRACT)

        # 4. Sunken Small-Seconds Subdial at (-9.0000, 0.0000)
        with Locations(Location((sec_pos[0], sec_pos[1], z_front + 0.05))):
            Cylinder(radius=4.60, height=0.10, mode=Mode.SUBTRACT)

        # Subdial concentric ring track
        with BuildSketch(Plane.XY.offset(z_front + 0.10)):
            with Locations([sec_pos]):
                Circle(radius=4.30)
                Circle(radius=4.15, mode=Mode.SUBTRACT)
        extrude(amount=-0.04, mode=Mode.SUBTRACT)

        # 5. Outer Railroad Sector Minute Track
        with BuildSketch(Plane.XY.offset(z_front)):
            Circle(radius=16.50)
            Circle(radius=16.30, mode=Mode.SUBTRACT)
        extrude(amount=0.04, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(z_front)):
            Circle(radius=15.00)
            Circle(radius=14.80, mode=Mode.SUBTRACT)
        extrude(amount=0.04, mode=Mode.SUBTRACT)

        # 6. Applied Baton Hour Markers (Faceted 3D batons raised by 0.15 mm on front face)
        baton_r = 13.20
        baton_w = 0.55
        baton_len = 2.00
        baton_h = 0.15

        # 12 hours positions (omit 9 o'clock to clear small-seconds subdial at (-9.0, 0))
        for hour in range(1, 13):
            if hour == 9:
                continue  # Omit 9h marker; small-seconds subdial occupies this sector

            angle_deg = 90.0 - hour * 30.0
            angle_rad = math.radians(angle_deg)
            x = baton_r * math.cos(angle_rad)
            y = baton_r * math.sin(angle_rad)

            if hour == 12:
                # Double baton at 12 o'clock for classic high-horology identity
                for offset_x in [-0.55, 0.55]:
                    with Locations(Location((x + offset_x, y, z_front - baton_h / 2.0))):
                        Box(length=baton_w, width=baton_len, height=baton_h, mode=Mode.ADD)
            else:
                with Locations(Location((x, y, z_front - baton_h / 2.0), (0, 0, angle_deg - 90.0))):
                    Box(length=baton_w, width=baton_len, height=baton_h, mode=Mode.ADD)

        # 7. Subtle typographic brand plaques / markings
        # "MECHANICAL" bar below 12 o'clock (Y = +8.20)
        with Locations(Location((0, 8.20, z_front - 0.02))):
            Box(length=4.20, width=0.40, height=0.04, mode=Mode.ADD)

        # "18,000 VPH" bar above 6 o'clock (Y = -8.50)
        with Locations(Location((0, -8.50, z_front - 0.02))):
            Box(length=3.60, width=0.35, height=0.04, mode=Mode.ADD)

        # 8. Dial Feet on reverse face (locating pins for mainplate)
        with Locations(Location((12.00, 8.00, z_back + 0.45))):
            Cylinder(radius=0.40, height=0.90, mode=Mode.ADD)
        with Locations(Location((-12.00, -8.00, z_back + 0.45))):
            Cylinder(radius=0.40, height=0.90, mode=Mode.ADD)

    d.part.color = srgb("#F0EFEA")
    return d.part


if __name__ == "__main__":
    dial()
