"""Mainspring Barrel Assembly (Hộp cót chính) Model for Caliber ETA 6497/6498.

Specs:
- Barrel drum with outer toothed rim: z = 77 teeth, m = 0.18 mm (Ø ~15.50 mm)
- Barrel arbor with lower/upper journals and square drive for ratchet wheel
- Barrel cover (snapped on)
- Internal coiled mainspring strip
- Mating Datum: BARREL_PIVOT (-3.50, -7.20)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cadgen import build123d as bd
from cadgen import srgb, step

from lib.gears import make_watch_wheel


def mainspring_barrel_drum():
    """Mainspring barrel drum with outer toothed rim driving the center wheel pinion."""
    teeth = 77
    module = 0.18
    barrel_h = 1.00
    wall_t = 0.45
    outer_r = (teeth * module) / 2.0 + 0.95 * module  # ~7.10 mm

    with bd.BuildPart() as msb:
        # 1. Outer toothed rim of the barrel (at Z = 0.05 to mesh with center pinion)
        wh = make_watch_wheel(
            teeth=teeth,
            module=module,
            rim_thickness=0.35,
            hub_diameter=3.20,
            arbor_hole=1.80,
            spoke_count=0,  # solid base plate
        )
        wh_part = wh.moved(bd.Location((0, 0, 0.05)))

        # 2. Cylindrical drum wall (from Z = -0.60 to 0.40)
        drum_solid = bd.Cylinder(radius=outer_r - 0.20, height=barrel_h) - bd.Cylinder(
            radius=outer_r - 0.20 - wall_t, height=barrel_h + 0.1
        )
        drum_solid = drum_solid.moved(bd.Location((0, 0, -0.10)))

        # 3. Internal coiled mainspring (spiral layers inside the drum)
        spring_solid = None
        for i in range(3):
            r_c = 1.80 + i * 1.10
            coil = bd.Cylinder(radius=r_c + 0.08, height=0.70) - bd.Cylinder(radius=r_c - 0.08, height=0.80)
            coil = coil.moved(bd.Location((0, 0, -0.10)))
            spring_solid = coil if spring_solid is None else (spring_solid + coil)

        msb.part = wh_part + drum_solid + spring_solid
        msb.part.color = srgb("#E5C07B")  # Warm golden brass
        msb.part.cad_material = {"roughness": 0.22, "metalness": 0.90}

    return msb.part


def barrel_arbor():
    """Barrel arbor with lower/upper journals and square drive for ratchet wheel."""
    with bd.BuildPart() as ap:
        # Central shaft body
        arbor = bd.Cylinder(radius=0.90, height=1.60).moved(bd.Location((0, 0, 0.20)))
        # Upper pivot and square seat for ratchet wheel on top of barrel bridge
        top_pivot = bd.Cylinder(radius=0.55, height=0.80).moved(bd.Location((0, 0, 1.40)))
        square_seat = bd.Cylinder(radius=0.70, height=0.45).moved(bd.Location((0, 0, 1.00)))
        bot_pivot = bd.Cylinder(radius=0.55, height=0.70).moved(bd.Location((0, 0, -0.95)))
        ap.part = arbor + top_pivot + square_seat + bot_pivot
        ap.part.color = srgb("#D8DEE9")  # Polished steel
        ap.part.cad_material = {"roughness": 0.15, "metalness": 0.95}

    return ap.part


@step(out="../../STEP/mainspring_barrel.step")
def mainspring_barrel():
    """Compound model preserving STEP/mainspring_barrel.step for independent validation."""
    drum = mainspring_barrel_drum()
    arbor = barrel_arbor()
    combined = drum + arbor
    combined.color = srgb("#E5C07B")
    combined.cad_material = {"roughness": 0.22, "metalness": 0.90}
    return combined


if __name__ == "__main__":
    mainspring_barrel()
