"""Mainplate (Tấm đế chính) Model for Caliber ETA 6497/6498.

Reference specs:
- Caliber: 16.5''' (Ø 36.60 mm, thickness 2.20 mm)
- Datum: Origin (0, 0, 0) at center of mainplate, top surface (movement/bridges side) is Z = 0.
- Dial side is Z < 0.
"""

import os
import sys
from pathlib import Path

# Add src to sys.path for lib imports
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
    Rectangle,
    Rot,
    extrude,
    fillet,
)
from cadgen import step

from lib.datums import (
    BALANCE_COCK_PINS,
    BALANCE_COCK_SCREW,
    BALANCE_PIVOT,
    BARREL_BRIDGE_PINS,
    BARREL_BRIDGE_SCREWS,
    BARREL_PIVOT,
    CENTER_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    PALLET_COCK_PINS,
    PALLET_COCK_SCREW,
    PALLET_PIVOT,
    STEM_Y,
    STEM_Z,
    THIRD_PIVOT,
    TRAIN_BRIDGE_PINS,
    TRAIN_BRIDGE_SCREWS,
)
from lib.parameters import MAINPLATE_DIAMETER, MAINPLATE_THICKNESS

OUT_STEP = str(Path(__file__).resolve().parents[2] / "STEP" / "mainplate.step")


@step(out="../../STEP/mainplate.step")
def mainplate():
    radius = MAINPLATE_DIAMETER / 2.0  # 18.30 mm
    thickness = MAINPLATE_THICKNESS  # 2.20 mm

    with BuildPart() as mp:
        # Base circular plate, extruding from Z = -thickness up to Z = 0
        with BuildSketch():
            Circle(radius=radius)
        extrude(amount=thickness)
        # Shift down so top face is precisely Z = 0
        mp.part = mp.part.moved(Location((0, 0, -thickness)))

        top_face = mp.faces().sort_by().last

        # --- Recesses (Pockets for gear train & moving parts) ---
        # 1. Barrel recess
        with BuildSketch(top_face):
            with Locations([BARREL_PIVOT]):
                Circle(radius=7.60)
        extrude(amount=-1.40, mode=Mode.SUBTRACT)

        # 2. Center wheel recess
        with BuildSketch(top_face):
            with Locations([CENTER_PIVOT]):
                Circle(radius=4.80)
        extrude(amount=-0.80, mode=Mode.SUBTRACT)

        # 3. Third wheel recess
        with BuildSketch(top_face):
            with Locations([THIRD_PIVOT]):
                Circle(radius=4.00)
        extrude(amount=-0.80, mode=Mode.SUBTRACT)

        # 4. Fourth wheel recess
        with BuildSketch(top_face):
            with Locations([FOURTH_PIVOT]):
                Circle(radius=3.80)
        extrude(amount=-0.80, mode=Mode.SUBTRACT)

        # 5. Escapement & Pallet recess
        with BuildSketch(top_face):
            with Locations([ESCAPE_PIVOT, PALLET_PIVOT]):
                Circle(radius=3.20)
        extrude(amount=-1.10, mode=Mode.SUBTRACT)

        # 6. Balance wheel well (recess)
        with BuildSketch(top_face):
            with Locations([BALANCE_PIVOT]):
                Circle(radius=6.40)
        extrude(amount=-1.50, mode=Mode.SUBTRACT)

        # --- Through Holes & Jewel Settings ---
        jewel_holes = [
            (CENTER_PIVOT, 0.60),       # Center tube hole (radius)
            (THIRD_PIVOT, 0.60),        # Third jewel hole
            (FOURTH_PIVOT, 0.60),       # Fourth long pivot jewel hole
            (ESCAPE_PIVOT, 0.60),       # Escape jewel hole
            (PALLET_PIVOT, 0.50),       # Pallet jewel hole
            (BALANCE_PIVOT, 0.85),      # Balance shock setting hole
        ]
        for pos, r in jewel_holes:
            with BuildSketch(top_face):
                with Locations([pos]):
                    Circle(radius=r)
            extrude(amount=-thickness, mode=Mode.SUBTRACT)

        # --- Screw Holes for Bridges (M1.2 tap holes, r = 0.50 mm) ---
        screw_holes = (
            BARREL_BRIDGE_SCREWS
            + TRAIN_BRIDGE_SCREWS
            + [BALANCE_COCK_SCREW, PALLET_COCK_SCREW]
        )
        with BuildSketch(top_face):
            with Locations(screw_holes):
                Circle(radius=0.50)
        extrude(amount=-1.50, mode=Mode.SUBTRACT)

        # --- Steady Pin Holes (Dowel holes, r = 0.40 mm) ---
        pin_holes = (
            BARREL_BRIDGE_PINS
            + TRAIN_BRIDGE_PINS
            + BALANCE_COCK_PINS
            + PALLET_COCK_PINS
        )
        with BuildSketch(top_face):
            with Locations(pin_holes):
                Circle(radius=0.40)
        extrude(amount=-1.20, mode=Mode.SUBTRACT)

        # --- Stem clearance bore at 3 o'clock ---
        with BuildSketch():
            with Locations([(radius - 1.50, STEM_Y, STEM_Z)]):
                Circle(radius=0.75)
        # Cut along X-axis
        stem_bore = Cylinder(radius=0.75, height=6.0)
        stem_bore = stem_bore.moved(Location((radius - 1.50, STEM_Y, STEM_Z), (0, 90, 0)))
        mp.part = mp.part - stem_bore

    return mp.part


if __name__ == "__main__":
    mainplate()
