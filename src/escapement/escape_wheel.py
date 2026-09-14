"""Escape Wheel Assembly Model for Caliber ETA 6497/6498.

Specs:
- 15 Club teeth (Swiss Lever Escapement standard)
- Module: m = 0.08 - 0.10 mm (outer diameter ~ 6.50 mm)
- Escape Pinion: 10 leaves, m = 0.10 mm (meshes with Fourth Wheel)
- Frequency: 18,000 vph -> 15 teeth = 30 vibrations per turn -> 1 turn per 6 seconds.
- Mating Datum: ESCAPE_PIVOT (-11.80, 8.20)
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
    PolarLocations,
    Polygon,
    extrude,
)
from cadgen import step

from lib.gears import make_pinion


@step(out="../../STEP/escape_wheel.step")
def escape_wheel():
    teeth_count = 15
    outer_r = 3.25
    thickness = 0.14

    with BuildPart() as ew:
        # Base hub and rim
        with BuildSketch():
            Circle(radius=outer_r)
        extrude(amount=thickness)

        # Cut club tooth profiles (15 angled teeth with locking and impulse faces)
        with BuildSketch(ew.faces().sort_by().last):
            with PolarLocations(radius=2.60, count=teeth_count):
                tooth_cut = [
                    (0.0, -0.20),
                    (1.10, 0.50),
                    (0.90, 0.90),
                    (-0.30, 0.40),
                ]
                Polygon(tooth_cut)
        extrude(amount=-thickness, mode=Mode.SUBTRACT)

        # 3 Spoke cutouts
        with BuildSketch(ew.faces().sort_by().last):
            with PolarLocations(radius=1.35, count=3):
                spoke_cut = [
                    (-0.60, -0.40),
                    (0.60, -0.40),
                    (0.80, 0.40),
                    (-0.80, 0.40),
                ]
                Polygon(spoke_cut)
        extrude(amount=-thickness, mode=Mode.SUBTRACT)

        # Escape Pinion (10 leaves) on arbor
        pin = make_pinion(
            leaves=10,
            module=0.10,
            length=1.00,
            arbor_diameter=0.45,
            pivot_diameter=0.15,
            pivot_length=0.35,
        )
        # Position wheel at Z = 0.50
        ew.part = ew.part.moved(Location((0, 0, 0.50)))
        ew.part = ew.part + pin.moved(Location((0, 0, -0.10)))

    return ew.part


if __name__ == "__main__":
    escape_wheel()
