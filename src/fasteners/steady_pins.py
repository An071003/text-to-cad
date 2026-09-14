"""Steady Pins (Chốt định vị dẫn hướng cầu máy) Model for Caliber ETA 6497/6498.

Precision hardened steel dowel pins:
- Ø 0.80 mm x 2.20 mm (for barrel & train bridges, balance cock)
- Ø 0.60 mm x 1.40 mm (for pallet cock)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import BuildPart, Cylinder, Location
from cadgen import step


from lib.datums import BARREL_BRIDGE_PINS, TRAIN_BRIDGE_PINS


@step(out="../../STEP/steady_pins.step")
def steady_pins():
    all_pins = []
    # Ø 0.70 mm dowel pins (fits clearance hole Ø 0.90 mm)
    for p in BARREL_BRIDGE_PINS + TRAIN_BRIDGE_PINS:
        pin = Cylinder(radius=0.35, height=1.60).moved(Location((p[0], p[1], 0.50)))
        all_pins.append(pin)

    combined = all_pins[0]
    for p in all_pins[1:]:
        combined = combined + p

    return combined


if __name__ == "__main__":
    steady_pins()
