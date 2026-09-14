"""Ratchet & Crown Wheels with Click Mechanism Model for Caliber ETA 6497/6498.

Specs:
- Ratchet Wheel: z = 42 teeth, m = 0.22 mm (Ø ~9.60 mm), square arbor bore.
- Crown Wheel (Internal): z = 30 teeth, m = 0.20 mm (Ø ~6.40 mm), center bushing.
- Click & Click Spring: One-way winding pawl assembly.
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cadgen import build123d as bd
from cadgen import srgb, step

from lib.datums import BARREL_PIVOT, CROWN_WHEEL_PIVOT, RATCHET_CLICK_PIVOT
from lib.gears import make_watch_wheel


def ratchet_wheel():
    """Ratchet wheel (z=42 teeth, m=0.22 mm) mounted on barrel arbor square seat."""
    with bd.BuildPart() as bp:
        rw = make_watch_wheel(
            teeth=42,
            module=0.22,
            rim_thickness=0.50,
            hub_diameter=3.00,
            arbor_hole=0.0,
            spoke_count=0,
        )
        with bd.BuildSketch(rw.faces().sort_by().last):
            bd.Rectangle(1.10, 1.10)
        hole = bd.extrude(amount=0.50)
        rw_part = rw - hole
        rw_part = rw_part.moved(bd.Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 1.40)))
        rw_part.color = srgb("#B0B8C4")
        rw_part.cad_material = {"roughness": 0.18, "metalness": 0.92}
        return rw_part


def crown_wheel_internal():
    """Internal crown transmission wheel (z=30 teeth, m=0.20 mm) driven by winding pinion."""
    cw = make_watch_wheel(
        teeth=30,
        module=0.20,
        rim_thickness=0.45,
        hub_diameter=2.40,
        arbor_hole=1.20,
        spoke_count=0,
    )
    cw_part = cw.moved(bd.Location((CROWN_WHEEL_PIVOT[0], CROWN_WHEEL_PIVOT[1], 1.40)))
    cw_part.color = srgb("#B0B8C4")
    cw_part.cad_material = {"roughness": 0.18, "metalness": 0.92}
    return cw_part


def ratchet_click():
    """Ratchet click (one-way pawl) oscillating 3-8 degrees to lock ratchet wheel."""
    with bd.BuildPart() as cp:
        with bd.BuildSketch():
            click_pts = [
                (0.0, 0.0),
                (1.80, 0.60),
                (2.20, 1.40),
                (1.40, 1.20),
                (0.0, 0.80),
                (-0.40, 0.40),
            ]
            bd.Polygon(click_pts)
        bd.extrude(amount=0.40)
        # Screw pivot hole for click
        with bd.BuildSketch(cp.faces().sort_by().last):
            bd.Circle(radius=0.40)
        bd.extrude(amount=-0.40, mode=bd.Mode.SUBTRACT)

    click_part = cp.part.moved(bd.Location((RATCHET_CLICK_PIVOT[0], RATCHET_CLICK_PIVOT[1], 1.40)))
    click_part.color = srgb("#B0B8C4")
    click_part.cad_material = {"roughness": 0.18, "metalness": 0.92}
    return click_part


def click_spring():
    """Click spring (curved wire spring) biasing ratchet click against ratchet teeth."""
    with bd.BuildPart() as sp:
        with bd.BuildSketch():
            bd.Circle(radius=1.80)
            bd.Circle(radius=1.55, mode=bd.Mode.SUBTRACT)
            with bd.Locations([(-1.0, 0)]):
                bd.Rectangle(2.5, 3.0)  # cut half of ring to make a curved wire
        bd.extrude(amount=0.30)

    cspring_part = sp.part.moved(bd.Location((RATCHET_CLICK_PIVOT[0] - 1.2, RATCHET_CLICK_PIVOT[1] - 0.5, 1.40)))
    cspring_part.color = srgb("#8FBCBB")
    cspring_part.cad_material = {"roughness": 0.25, "metalness": 0.95}
    return cspring_part


@step(out="../../STEP/ratchet_and_crown.step")
def ratchet_and_crown():
    """Compound model preserving STEP/ratchet_and_crown.step for independent validation."""
    rw_part = ratchet_wheel()
    cw_part = crown_wheel_internal()
    click_part = ratchet_click()
    cspring_part = click_spring()
    combined = rw_part + cw_part + click_part + cspring_part
    combined.color = srgb("#B0B8C4")
    combined.cad_material = {"roughness": 0.18, "metalness": 0.92}
    return combined


if __name__ == "__main__":
    ratchet_and_crown()
