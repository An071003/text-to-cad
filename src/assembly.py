"""Top-Level Assembly Model for Complete 42 mm Mechanical Dress Wristwatch.

Reference: ETA 6497/6498 Caliber (Ø 36.60 mm, 18,000 vph / 2.5 Hz) housed in a
classic 42.00 mm stainless-steel wristwatch with exhibition caseback, front and
rear sapphire crystals, classical sector dial, and blued-steel hands.

Integrates all 8 subsystems into a fully functional, validated kinematic 3D CAD assembly:
1. Mainplate & Bridges (Mainplate, Barrel Bridge, Train Bridge, Pallet Cock, Balance Cock)
2. Gear Train (Center, Third, Fourth Wheel & Pinion Assemblies)
3. Escapement (Escape Wheel, Pallet Fork, Pallet Jewels)
4. Balance Assembly (Balance Wheel, Hairspring, Double Roller Table)
5. Power & Winding (Mainspring Barrel Drum, Barrel Arbor, Ratchet Wheel, Crown Wheel Internal, Click, Click Spring, Winding Stem, Winding Pinion, Sliding Pinion, Setting Work, Motion Work)
6. Fasteners & Jewels (Bridge Screws, Synthetic Ruby Jewels, Steady Pins)
7. Dial & Hands (Sector Dial, Leaf Hour & Minute Hands, Small Seconds Needle at 9 o'clock)
8. Watch Exterior (Caseband with 4 Lugs, Bezel & Front Sapphire, Knurled Crown, Exhibition Caseback & Spacer)

Kinematics:
- Verified physical gear ratios: 1 : -8 : +60 : -600 (Center -> Third -> Fourth -> Escape)
- Revolute joints defined at exact horological pivot coordinates
- Coaxial hand drives: 1:1 minute hand, 1/12 hour hand, 60:1 small-seconds hand
- Winding and ratchet work kinematics with dedicated DOFs
- Named poses: rest, winding, wound, time_setting, running_preview
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import cadgen
from cadgen.build123d import Location
from cadgen import glb, step
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
    CROWN_WHEEL_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    PALLET_PIVOT,
    RATCHET_CLICK_PIVOT,
    STEM_Y,
    STEM_Z,
    THIRD_PIVOT,
)
from mainplate_and_bridges.balance_cock import balance_cock
from mainplate_and_bridges.barrel_bridge import barrel_bridge
from mainplate_and_bridges.mainplate import mainplate
from mainplate_and_bridges.pallet_cock import pallet_cock
from mainplate_and_bridges.train_bridge import train_bridge
from watch_exterior.bezel import bezel
from watch_exterior.caseback import caseback
from watch_exterior.caseband import caseband
from watch_exterior.crown import crown
from watch_exterior.dial import dial
from watch_exterior.hands import hour_hand, minute_hand, seconds_hand
from winding_and_barrel.mainspring_barrel import barrel_arbor, mainspring_barrel_drum
from winding_and_barrel.motion_work import motion_work
from winding_and_barrel.ratchet_and_crown import (
    click_spring,
    crown_wheel_internal,
    ratchet_click,
    ratchet_wheel,
)
from winding_and_barrel.winding_mechanism import (
    keyless_setting_work,
    sliding_pinion,
    winding_pinion,
    winding_stem,
)

# Kinematic articulation & gear coupling definitions
KINEMATICS = {
    "mates": [
        cadgen.revolute(
            "barrel_rot",
            parent="#mainplate",
            child="#mainspring_barrel_drum",
            origin=(BARREL_PIVOT[0], BARREL_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "barrel_arbor_rot",
            parent="#mainplate",
            child="#barrel_arbor",
            origin=(BARREL_PIVOT[0], BARREL_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "ratchet_wheel_rot",
            parent="#mainplate",
            child="#ratchet_wheel",
            origin=(BARREL_PIVOT[0], BARREL_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "crown_wheel_rot",
            parent="#mainplate",
            child="#crown_wheel_internal",
            origin=(CROWN_WHEEL_PIVOT[0], CROWN_WHEEL_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "ratchet_click_rot",
            parent="#mainplate",
            child="#ratchet_click",
            origin=(RATCHET_CLICK_PIVOT[0], RATCHET_CLICK_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(0.0, 8.0),
        ),
        cadgen.revolute(
            "center_wheel_rot",
            parent="#mainplate",
            child="#center_wheel_assembly",
            origin=(CENTER_PIVOT[0], CENTER_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "third_wheel_rot",
            parent="#mainplate",
            child="#third_wheel_assembly",
            origin=(THIRD_PIVOT[0], THIRD_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "fourth_wheel_rot",
            parent="#mainplate",
            child="#fourth_wheel_assembly",
            origin=(FOURTH_PIVOT[0], FOURTH_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "escape_wheel_rot",
            parent="#mainplate",
            child="#escape_wheel_assembly",
            origin=(ESCAPE_PIVOT[0], ESCAPE_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "pallet_rot",
            parent="#mainplate",
            child="#pallet_fork",
            origin=(PALLET_PIVOT[0], PALLET_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-4.5, 4.5),
        ),
        cadgen.revolute(
            "balance_rot",
            parent="#mainplate",
            child="#balance_wheel",
            origin=(BALANCE_PIVOT[0], BALANCE_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-270.0, 270.0),
        ),
        cadgen.revolute(
            "minute_hand_rot",
            parent="#mainplate",
            child="#minute_hand",
            origin=(CENTER_PIVOT[0], CENTER_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "hour_hand_rot",
            parent="#mainplate",
            child="#hour_hand",
            origin=(CENTER_PIVOT[0], CENTER_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.revolute(
            "seconds_hand_rot",
            parent="#mainplate",
            child="#seconds_hand",
            origin=(FOURTH_PIVOT[0], FOURTH_PIVOT[1], 0.0),
            direction=(0, 0, 1),
            limits=(-360.0, 360.0),
        ),
        cadgen.cylindrical(
            "crown_joint",
            parent="#mainplate",
            child="#winding_crown",
            origin=(21.60, STEM_Y, STEM_Z),
            direction=(1, 0, 0),
            limits={"turn": (-360.0, 360.0), "travel": (0.0, 1.20)},
        ),
        cadgen.fastened(
            "stem_to_crown",
            parent="#winding_crown",
            child="#winding_stem",
        ),
        cadgen.revolute(
            "winding_pinion_rot",
            parent="#mainplate",
            child="#winding_pinion",
            origin=(11.20, STEM_Y, STEM_Z),
            direction=(1, 0, 0),
            limits=(-360.0, 360.0),
        ),
        cadgen.cylindrical(
            "sliding_pinion_joint",
            parent="#mainplate",
            child="#sliding_pinion",
            origin=(13.20, STEM_Y, STEM_Z),
            direction=(1, 0, 0),
            limits={"turn": (-360.0, 360.0), "travel": (0.0, 1.20)},
        ),
        # 3 Inspection / Exploded View Sliders for Native CAD Viewer Controls
        cadgen.slider(
            "front_cover_open",
            parent="#mainplate",
            child="#bezel_and_crystal",
            origin=(0.0, 0.0, -4.80),
            direction=(0.0, 0.0, -1.0),
            limits=(0.0, 8.0),
        ),
        cadgen.slider(
            "rear_cover_open",
            parent="#mainplate",
            child="#exhibition_caseback",
            origin=(0.0, 0.0, 3.20),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 8.0),
        ),
        cadgen.slider(
            "caseband_inspection_shift",
            parent="#mainplate",
            child="#caseband",
            origin=(0.0, 0.0, 0.0),
            direction=(1.0, 0.0, 0.0),
            limits=(0.0, 10.0),
        ),
    ],
    "couplings": [
        cadgen.couple(
            "gear_train",
            {
                "barrel_rot": 12.0 / 77.0,
                "center_wheel_rot": 1.0,
                "third_wheel_rot": -8.0,
                "fourth_wheel_rot": 60.0,
                "escape_wheel_rot": -600.0,
                "minute_hand_rot": 1.0,
                "hour_hand_rot": 1.0 / 12.0,
                "seconds_hand_rot": 60.0,
            },
            limits=(-360.0, 360.0),
        ),
    ],
    "poses": {
        "rest": {
            "barrel_rot": 0.0,
            "barrel_arbor_rot": 0.0,
            "ratchet_wheel_rot": 0.0,
            "crown_wheel_rot": 0.0,
            "ratchet_click_rot": 0.0,
            "center_wheel_rot": 0.0,
            "third_wheel_rot": 0.0,
            "fourth_wheel_rot": 0.0,
            "escape_wheel_rot": 0.0,
            "pallet_rot": 0.0,
            "balance_rot": 0.0,
            "minute_hand_rot": 0.0,
            "hour_hand_rot": 0.0,
            "seconds_hand_rot": 0.0,
            "crown_joint.turn": 0.0,
            "crown_joint.travel": 0.0,
            "front_cover_open": 0.0,
            "rear_cover_open": 0.0,
            "caseband_inspection_shift": 0.0,
        },
        "inspection_open": {
            "front_cover_open": 8.0,
            "rear_cover_open": 8.0,
            "caseband_inspection_shift": 10.0,
            "minute_hand_rot": 0.0,
            "hour_hand_rot": 0.0,
            "seconds_hand_rot": 0.0,
            "crown_joint.turn": 0.0,
            "crown_joint.travel": 0.0,
        },
        "winding": {
            "crown_joint.travel": 0.0,
            "crown_joint.turn": 360.0,
            "crown_wheel_rot": -168.0,
            "ratchet_wheel_rot": 120.0,
            "barrel_arbor_rot": 120.0,
            "ratchet_click_rot": 5.0,
            "barrel_rot": 0.0,
            "front_cover_open": 0.0,
            "rear_cover_open": 0.0,
            "caseband_inspection_shift": 0.0,
        },
        "wound": {
            "barrel_rot": 90.0,
            "barrel_arbor_rot": 240.0,
            "ratchet_wheel_rot": 240.0,
            "crown_wheel_rot": -336.0,
            "ratchet_click_rot": 0.0,
            "balance_rot": 200.0,
            "pallet_rot": 4.5,
            "crown_joint.turn": 720.0,
            "crown_joint.travel": 0.0,
            "front_cover_open": 0.0,
            "rear_cover_open": 0.0,
            "caseband_inspection_shift": 0.0,
        },
        "time_setting": {
            "crown_joint.travel": 1.20,
            "crown_joint.turn": 180.0,
            "crown_wheel_rot": 0.0,
            "ratchet_wheel_rot": 0.0,
            "barrel_arbor_rot": 0.0,
            "barrel_rot": 0.0,
            "minute_hand_rot": 360.0,
            "hour_hand_rot": 30.0,
            "seconds_hand_rot": 0.0,
            "front_cover_open": 0.0,
            "rear_cover_open": 0.0,
            "caseband_inspection_shift": 0.0,
        },
        "running_preview": {
            "barrel_rot": 0.004,
            "ratchet_wheel_rot": 0.0,
            "barrel_arbor_rot": 0.0,
            "crown_wheel_rot": 0.0,
            "balance_rot": 180.0,
            "pallet_rot": -4.5,
            "escape_wheel_rot": 12.0,
            "fourth_wheel_rot": 1.2,
            "seconds_hand_rot": 1.2,
            "minute_hand_rot": 0.02,
            "hour_hand_rot": 0.0016,
            "crown_joint.travel": 0.0,
            "crown_joint.turn": 0.0,
            "front_cover_open": 0.0,
            "rear_cover_open": 0.0,
            "caseband_inspection_shift": 0.0,
        },
    },
}


@step(out="../STEP/watch_caliber_assembly.step", kinematics=KINEMATICS)
@glb(out="../STEP/watch_caliber_assembly.glb")
def watch_caliber_assembly():
    asm = AssemblyHelper("ETA_6497_Watch_Assembly")

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

    # 3. Gear Train Components (placed at exact kinematic pivots)
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

    # 6. Power & Winding Mechanism (Individual Horological Occurrences)
    p_barrel_drum = mainspring_barrel_drum().moved(Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 0)))
    p_barrel_arbor = barrel_arbor().moved(Location((BARREL_PIVOT[0], BARREL_PIVOT[1], 0)))
    p_ratchet_wheel = ratchet_wheel()
    p_crown_wheel = crown_wheel_internal()
    p_click = ratchet_click()
    p_click_spring = click_spring()

    p_stem = winding_stem()
    p_w_pinion = winding_pinion()
    p_sliding_pinion = sliding_pinion()
    p_setting_work = keyless_setting_work()
    p_motion = motion_work()

    asm.add(p_barrel_drum, "mainspring_barrel_drum")
    asm.add(p_barrel_arbor, "barrel_arbor")
    asm.add(p_ratchet_wheel, "ratchet_wheel")
    asm.add(p_crown_wheel, "crown_wheel_internal")
    asm.add(p_click, "ratchet_click")
    asm.add(p_click_spring, "click_spring")

    asm.add(p_stem, "winding_stem")
    asm.add(p_w_pinion, "winding_pinion")
    asm.add(p_sliding_pinion, "sliding_pinion")
    asm.add(p_setting_work, "keyless_setting_work")
    asm.add(p_motion, "motion_work_train")

    # 7. Fasteners, Jewels & Pins
    p_screws = screws()
    p_jewels = jewels()
    p_pins = steady_pins()

    asm.add(p_screws, "bridge_fasteners")
    asm.add(p_jewels, "synthetic_ruby_jewels")
    asm.add(p_pins, "alignment_steady_pins")

    # 8. Dial & Hands (Dial Side Z < 0)
    p_dial = dial()
    p_h_hand = hour_hand()
    p_m_hand = minute_hand()
    p_s_hand = seconds_hand()

    asm.add(p_dial, "dial_plate")
    asm.add(p_h_hand, "hour_hand")
    asm.add(p_m_hand, "minute_hand")
    asm.add(p_s_hand, "seconds_hand")

    # 9. Watch Exterior (Caseband, Bezel & Crystals, Crown, Exhibition Caseback)
    p_caseband = caseband()
    p_bezel = bezel()
    p_crown = crown()
    p_caseback = caseback()

    asm.add(p_caseband, "caseband")
    asm.add(p_bezel, "bezel_and_crystal")
    asm.add(p_crown, "winding_crown")
    asm.add(p_caseback, "exhibition_caseback")

    return asm.build()


if __name__ == "__main__":
    watch_caliber_assembly()
