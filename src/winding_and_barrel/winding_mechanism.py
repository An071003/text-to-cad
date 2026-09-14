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

from cadgen import build123d as bd
from cadgen import srgb, step

from lib.datums import STEM_Y, STEM_Z


def winding_stem():
    """Winding stem (ty núm) with pilot, square shank, journal, and outer section."""
    with bd.BuildPart() as sp:
        # Pilot tip (inside mainplate)
        pilot = bd.Cylinder(radius=0.35, height=2.20).moved(bd.Location((10.0, STEM_Y, STEM_Z), (0, 90, 0)))
        # Square section for sliding clutch (0.85 x 0.85 mm)
        square_shank = bd.Box(3.0, 0.85, 0.85).moved(bd.Location((12.50, STEM_Y, STEM_Z)))
        # Cylindrical bearing journal
        journal = bd.Cylinder(radius=0.60, height=3.50).moved(bd.Location((15.75, STEM_Y, STEM_Z), (0, 90, 0)))
        # Outer threaded stem section for winding crown
        outer_stem = bd.Cylinder(radius=0.45, height=6.0).moved(bd.Location((20.50, STEM_Y, STEM_Z), (0, 90, 0)))
        sp.part = pilot + square_shank + journal + outer_stem
        sp.part.color = srgb("#E5E9F0")
        sp.part.cad_material = {"roughness": 0.20, "metalness": 0.92}

    return sp.part


def winding_pinion():
    """Winding pinion (bánh răng lên cót) with contrate/face teeth driven by sliding pinion."""
    with bd.BuildPart() as wp:
        pinion = bd.Cylinder(radius=1.30, height=1.40).moved(bd.Location((11.20, STEM_Y, STEM_Z), (0, 90, 0)))
        bore = bd.Cylinder(radius=0.40, height=1.60).moved(bd.Location((11.20, STEM_Y, STEM_Z), (0, 90, 0)))
        wp.part = pinion - bore
        wp.part.color = srgb("#D8DEE9")
        wp.part.cad_material = {"roughness": 0.22, "metalness": 0.90}

    return wp.part


def sliding_pinion():
    """Sliding pinion / clutch wheel with central square hole and yoke groove."""
    with bd.BuildPart() as clp:
        body = bd.Cylinder(radius=1.35, height=1.60).moved(bd.Location((13.20, STEM_Y, STEM_Z), (0, 90, 0)))
        # Central square sliding bore (0.90 x 0.90 mm) clearing 0.85 x 0.85 mm stem shank
        square_bore = bd.Box(1.70, 0.90, 0.90).moved(bd.Location((13.20, STEM_Y, STEM_Z)))
        clp.part = body - square_bore
        clp.part.color = srgb("#D8DEE9")
        clp.part.cad_material = {"roughness": 0.22, "metalness": 0.90}

    return clp.part


def keyless_setting_work():
    """Setting lever and yoke mechanism for position detent and clutch shifting."""
    with bd.BuildPart() as kp:
        # Setting Lever (lock for stem detent groove)
        with bd.BuildSketch():
            sl_pts = [
                (0.0, 0.0),
                (3.20, 0.50),
                (3.80, 1.40),
                (1.50, 2.20),
                (0.0, 1.60),
            ]
            bd.Polygon(sl_pts)
        bd.extrude(amount=0.50)
        setting_lever = kp.part.moved(bd.Location((12.0, STEM_Y + 1.2, -0.60)))

        # Yoke (fork lever engaging the clutch wheel groove)
        with bd.BuildSketch():
            yoke_pts = [
                (0.0, 0.0),
                (2.80, -0.40),
                (3.20, 0.80),
                (1.80, 1.80),
                (0.20, 1.20),
            ]
            bd.Polygon(yoke_pts)
        bd.extrude(amount=0.45)
        yoke = kp.part.moved(bd.Location((11.50, STEM_Y - 2.2, -0.60)))

        kp.part = setting_lever + yoke
        kp.part.color = srgb("#B0B8C4")
        kp.part.cad_material = {"roughness": 0.25, "metalness": 0.90}

    return kp.part


@step(out="../../STEP/winding_mechanism.step")
def winding_mechanism():
    """Compound model preserving STEP/winding_mechanism.step for independent validation."""
    stem = winding_stem()
    w_pin = winding_pinion()
    s_pin = sliding_pinion()
    setting = keyless_setting_work()
    combined = stem + w_pin + s_pin + setting
    combined.color = srgb("#D8DEE9")
    combined.cad_material = {"roughness": 0.20, "metalness": 0.92}
    return combined


if __name__ == "__main__":
    winding_mechanism()
