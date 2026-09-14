"""Keyless Winding & Hand-Setting Mechanism Model for Caliber ETA 6497/6498.

Components:
- Winding Stem (ty núm) with square shank
- Winding Pinion (bánh răng lên cót)
- Sliding Pinion / Clutch Wheel (bánh trượt ly hợp)
- Setting Lever (đòn khóa ty núm) & Yoke (đòn bẩy càng cua ly hợp)
- Setting Lever Jumper / Spring (cầu lò xo đòn chuyển)
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
    Polygon,
    Rectangle,
    extrude,
)
from cadgen import step

from lib.datums import STEM_Y, STEM_Z
from lib.parameters import MAINPLATE_DIAMETER


@step(out="../../STEP/winding_mechanism.step")
def winding_mechanism():
    stem_x = MAINPLATE_DIAMETER / 2.0  # 18.30 mm

    with BuildPart() as wm:
        # 1. Winding Stem
        # Pilot tip (inside mainplate)
        pilot = Cylinder(radius=0.35, height=2.20).moved(Location((10.0, STEM_Y, STEM_Z), (0, 90, 0)))
        # Square section for sliding clutch
        square_shank = Box(3.0, 0.85, 0.85).moved(Location((12.50, STEM_Y, STEM_Z)))
        # Cylindrical bearing journal
        journal = Cylinder(radius=0.60, height=3.50).moved(Location((15.75, STEM_Y, STEM_Z), (0, 90, 0)))
        # Outer threaded stem section for winding crown
        outer_stem = Cylinder(radius=0.45, height=6.0).moved(Location((20.50, STEM_Y, STEM_Z), (0, 90, 0)))
        stem_solid = pilot + square_shank + journal + outer_stem

        # 2. Winding Pinion (cylindrical body with face teeth)
        w_pinion = Cylinder(radius=1.30, height=1.40).moved(Location((11.20, STEM_Y, STEM_Z), (0, 90, 0)))

        # 3. Sliding Clutch Wheel (with central square hole and circumferential yoke groove)
        clutch = Cylinder(radius=1.35, height=1.60).moved(Location((13.20, STEM_Y, STEM_Z), (0, 90, 0)))

        # 4. Setting Lever (lock for stem detent groove)
        with BuildSketch():
            sl_pts = [
                (0.0, 0.0),
                (3.20, 0.50),
                (3.80, 1.40),
                (1.50, 2.20),
                (0.0, 1.60),
            ]
            Polygon(sl_pts)
        extrude(amount=0.50)
        setting_lever = wm.part.moved(Location((12.0, STEM_Y + 1.2, -0.60)))

        # 5. Yoke (fork lever engaging the clutch wheel groove)
        with BuildSketch():
            yoke_pts = [
                (0.0, 0.0),
                (2.80, -0.40),
                (3.20, 0.80),
                (1.80, 1.80),
                (0.20, 1.20),
            ]
            Polygon(yoke_pts)
        extrude(amount=0.45)
        yoke = wm.part.moved(Location((11.50, STEM_Y - 2.2, -0.60)))

        wm.part = stem_solid + w_pinion + clutch + setting_lever + yoke

    return wm.part


if __name__ == "__main__":
    winding_mechanism()
