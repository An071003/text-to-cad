"""Top-Level Assembly Model for Mechanical Watch Caliber (ETA 6497/6498 Reference).

Integrates all 7 subsystems into a fully functional, validated kinematic 3D CAD assembly:
1. Mainplate & Bridges (Mainplate, Barrel Bridge, Train Bridge, Pallet Cock, Balance Cock)
2. Gear Train (Center, Third, Fourth Wheel & Pinion Assemblies)
3. Escapement (Escape Wheel, Pallet Fork, Pallet Jewels)
4. Balance Assembly (Balance Wheel, Hairspring, Double Roller Table)
5. Power & Winding (Mainspring Barrel, Ratchet & Crown Wheels, Keyless Winding Mechanism, Motion Work)
6. Fasteners & Jewels (Bridge Screws, Ruby Jewels, Steady Pins)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build123d import Compound, Location
from cadgen import step
from cadgen.assembly import AssemblyHelper

from balance.balance_wheel import balance_wheel
from balance.hairspring import hairspring
from balance.roller_table import roller_table
from escapement.escape_wheel import escape_wheel
from escapement.pallet_fork import pallet_fork
from escapement.pallet_jewels import pallet_jewels
from fasteners.jewels import jewels
from fasteners.screws import screws
from fasteners.steady_pins import steady_pins
from gear_train.center_wheel import center_wheel
from gear_train.fourth_wheel import fourth_wheel
from gear_train.third_wheel import third_wheel
from lib.datums import (
    BALANCE_PIVOT,
    BARREL_PIVOT,
    CENTER_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    PALLET_PIVOT,
    THIRD_PIVOT,
)
from mainplate_and_bridges.balance_cock import balance_cock
from mainplate_and_bridges.barrel_bridge import barrel_bridge
from mainplate_and_bridges.mainplate import mainplate
from mainplate_and_bridges.pallet_cock import pallet_cock
from mainplate_and_bridges.train_bridge import train_bridge
from winding_and_barrel.mainspring_barrel import mainspring_barrel
from winding_and_barrel.motion_work import motion_work
from winding_and_barrel.ratchet_and_crown import ratchet_and_crown
from winding_and_barrel.winding_mechanism import winding_mechanism


@step(out="../STEP/watch_caliber_assembly.step")
def watch_caliber_assembly():
    asm = AssemblyHelper("ETA_6497_Caliber_Assembly")

    # 1. Base Mainplate
    p_mainplate = mainplate()
    asm.add(p_mainplate, "mainplate")

    # 2. Structural Bridges
    p_barrel_bridge = barrel_bridge()
    p_train_bridge = train_bridge()
    p_pallet_cock = pallet_cock()
    p_balance_cock = balance_cock()

    asm.add(p_barrel_bridge, "barrel_bridge")
    asm.add(p_train_bridge, "train_bridge")
    asm.add(p_pallet_cock, "pallet_cock")
    asm.add(p_balance_cock, "balance_cock")

    # 3. Gear Train Components
    p_center = center_wheel().moved(Location((CENTER_PIVOT[0], CENTER_PIVOT[1], 0)))
    p_third = third_wheel().moved(Location((THIRD_PIVOT[0], THIRD_PIVOT[1], 0)))
    p_fourth = fourth_wheel().moved(Location((FOURTH_PIVOT[0], FOURTH_PIVOT[1], 0)))

    asm.add(p_center, "center_wheel_assembly")
    asm.add(p_third, "third_wheel_assembly")
    asm.add(p_fourth, "fourth_wheel_assembly")

    # 4. Escapement Subsystem
    p_escape = escape_wheel().moved(Location((ESCAPE_PIVOT[0], ESCAPE_PIVOT[1], 0)))
    p_pallet = pallet_fork().moved(Location((PALLET_PIVOT[0], PALLET_PIVOT[1], 0)))
    p_pallet_j = pallet_jewels().moved(Location((PALLET_PIVOT[0], PALLET_PIVOT[1], 0)))

    asm.add(p_escape, "escape_wheel_assembly")
    asm.add(p_pallet, "pallet_fork")
    asm.add(p_pallet_j, "pallet_jewels")

    # 5. Balance Assembly
    p_balance = balance_wheel().moved(Location((BALANCE_PIVOT[0], BALANCE_PIVOT[1], 0)))
    p_hairspring = hairspring().moved(Location((BALANCE_PIVOT[0], BALANCE_PIVOT[1], 0)))
    p_roller = roller_table().moved(Location((BALANCE_PIVOT[0], BALANCE_PIVOT[1], 0)))

    asm.add(p_balance, "balance_wheel")
    asm.add(p_hairspring, "hairspring_spiral")
    asm.add(p_roller, "double_roller_table")

    # 6. Power & Winding Mechanism
    p_barrel = mainspring_barrel().moved(Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 0)))
    p_ratchet_crown = ratchet_and_crown()
    p_winding = winding_mechanism()
    p_motion = motion_work()

    asm.add(p_barrel, "mainspring_barrel")
    asm.add(p_ratchet_crown, "ratchet_and_crown_work")
    asm.add(p_winding, "keyless_winding_mechanism")
    asm.add(p_motion, "motion_work_train")

    # 7. Fasteners, Jewels & Pins
    p_screws = screws()
    p_jewels = jewels()
    p_pins = steady_pins()

    asm.add(p_screws, "bridge_fasteners")
    asm.add(p_jewels, "synthetic_ruby_jewels")
    asm.add(p_pins, "alignment_steady_pins")

    return asm.build()


if __name__ == "__main__":
    watch_caliber_assembly()
