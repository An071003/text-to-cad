"""Pallet Jewels (Chân kính ngọc neo Ruby) Model for Caliber ETA 6497/6498.

Synthetic ruby pallet stones (Entry & Exit) with precision impulse planes.
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
    Location,
    Mode,
    Polygon,
    extrude,
)
from cadgen import step


@step(out="../../STEP/pallet_jewels.step")
def pallet_jewels():
    # Model both entry and exit stones as a pair compound
    with BuildPart() as pj:
        # Entry jewel (ruby prism with 32° impulse bevel)
        with BuildSketch():
            entry_pts = [
                (0.0, 0.0),
                (0.45, 0.0),
                (0.45, 0.22),
                (0.12, 0.28),
                (0.0, 0.22),
            ]
            Polygon(entry_pts)
        extrude(amount=0.25)
        entry_stone = pj.part.moved(Location((-1.75, 0.20, 0.0)))

        # Exit jewel (ruby prism with 42° impulse bevel)
        with BuildSketch():
            exit_pts = [
                (0.0, 0.0),
                (0.45, 0.0),
                (0.45, 0.22),
                (0.33, 0.28),
                (0.0, 0.22),
            ]
            Polygon(exit_pts)
        extrude(amount=0.25)
        exit_stone = pj.part.moved(Location((1.75, 0.20, 0.0)))

        pj.part = entry_stone + exit_stone

    return pj.part


if __name__ == "__main__":
    pallet_jewels()
