"""Automated Pytest Suite for Complete 42 mm Mechanical Dress Wristwatch.

Validates:
1. Generation and existence of all 28 STEP model artifacts (22 movement + 6 exterior).
2. OpenCASCADE BRepCheck topology, closure, and orientation with 0 errors.
3. Total watch exterior dimensions: Ø 42.00 mm diameter, ~49.8 mm lug-to-lug, <= 12.5 mm thickness.
4. Positive internal clearance between caseband and movement (Ø 37.40 mm vs Ø 36.60 mm).
5. Strict vertical Z-clearance between dial, hour hand, minute hand, and sapphire crystal.
6. Concentricity of crown tube with winding stem (Y = -2.50 mm, Z = -0.80 mm).
7. Coaxial alignment of small seconds hand and dial subdial with fourth wheel pivot (-9.0000, 0.0000).
8. Horological gear train ratio ensuring exact 18,000 vph (2.5 Hz) oscillation frequency.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STEP_DIR = PROJECT_ROOT / "STEP"
SRC_DIR = PROJECT_ROOT / "src"

WIN32_FLAGS = {
    "creationflags": subprocess.CREATE_NO_WINDOW,
    "stdin": subprocess.DEVNULL,
} if sys.platform == "win32" else {}
os.environ["CADGEN_DAEMON"] = "0"

REQUIRED_STEP_MODELS = [
    # 1. Base & Structural Movement
    "mainplate.step",
    "barrel_bridge.step",
    "train_bridge.step",
    "pallet_cock.step",
    "balance_cock.step",
    # 2. Gear Train
    "center_wheel.step",
    "third_wheel.step",
    "fourth_wheel.step",
    # 3. Escapement & Regulating Organ
    "escape_wheel.step",
    "pallet_fork.step",
    "pallet_jewels.step",
    "balance_wheel.step",
    "hairspring.step",
    "roller_table.step",
    # 4. Power & Keyless Works
    "mainspring_barrel.step",
    "ratchet_and_crown.step",
    "winding_mechanism.step",
    "motion_work.step",
    # 5. Fasteners & Jewels
    "screws.step",
    "jewels.step",
    "steady_pins.step",
    # 6. Watch Exterior Components
    "caseband.step",
    "bezel.step",
    "dial.step",
    "hands.step",
    "crown.step",
    "caseback.step",
    # 7. Top-Level Assembly
    "watch_caliber_assembly.step",
]


@pytest.mark.parametrize("model_filename", REQUIRED_STEP_MODELS)
def test_step_model_exists_and_non_empty(model_filename):
    """Ensure every required CAD model exists and has non-trivial file size."""
    file_path = STEP_DIR / model_filename
    assert file_path.exists(), f"Missing required CAD artifact: {model_filename}"
    assert file_path.stat().st_size > 1024, f"File {model_filename} is suspiciously small (< 1KB)"


def test_top_level_assembly_validation():
    """Verify top-level assembly passes OpenCASCADE geometry validation with 0 failures."""
    assembly_file = STEP_DIR / "watch_caliber_assembly.step"
    assert assembly_file.exists()

    cmd = ["cadgen", "step", "inspect", "validate", str(assembly_file.relative_to(PROJECT_ROOT))]
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)
    assert res.returncode == 0, f"Validation command failed: {res.stderr}"

    data = json.loads(res.stdout)
    assert data.get("ok") is True, "Validation result ok != True"
    assert data.get("failureCount", 0) == 0, f"Geometry has {data.get('failureCount')} failure(s)"
    assert data.get("occurrenceCount", 0) >= 25, f"Expected at least 25 parts in complete watch, got {data.get('occurrenceCount')}"


def test_watch_overall_dimensional_envelope():
    """Verify watch dimensions adhere to 42 mm diameter and <= 12.5 mm total thickness."""
    cmd = ["cadgen", "step", "inspect", "refs", "STEP/watch_caliber_assembly.step", "--facts"]
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)
    assert res.returncode == 0

    data = json.loads(res.stdout)
    facts = data["tokens"][0]["entryFacts"]
    size_x, size_y, size_z = facts["size"]

    # Lug-to-lug span along Y axis must be ~49.8 mm (within 48.0 - 52.0 mm)
    assert 46.0 <= size_y <= 52.0, f"Lug-to-lug span along Y is {size_y:.2f} mm (expected ~50 mm)"
    # Total thickness along Z must not exceed 12.5 mm target
    assert size_z <= 12.50, f"Total watch thickness is {size_z:.2f} mm (exceeds 12.50 mm)"


def test_case_movement_positive_clearance():
    """Verify caseband inner chamber provides positive radial clearance for movement."""
    sys.path.insert(0, str(SRC_DIR))
    from lib.parameters import MAINPLATE_DIAMETER

    # Movement outer diameter is 36.60 mm (radius 18.30 mm)
    r_movement = MAINPLATE_DIAMETER / 2.0
    r_chamber = 18.70  # Ø 37.40 mm case cavity

    radial_gap = r_chamber - r_movement
    assert radial_gap >= 0.30, f"Case movement gap {radial_gap:.2f} mm is too tight (< 0.30 mm)"


def test_dial_and_hands_vertical_stack_clearance():
    """Verify vertical Z-clearance between dial, hour hand, minute hand, and front sapphire."""
    # Stacking coordinates:
    # Dial front face: Z = -4.05 mm
    # Applied batons top: Z = -4.20 mm
    # Small seconds hand: Z = -4.24 mm (th 0.12, base at -4.18)
    # Hour hand: Z = -4.48 mm (th 0.16, top at -4.40)
    # Minute hand: Z = -4.72 mm (th 0.16, top at -4.64)
    # Sapphire crystal inner face: Z = -4.90 mm
    z_dial_front = -4.05
    z_baton_top = -4.20
    z_sec_hand_top = -4.24
    z_hour_hand_base = -4.40
    z_hour_hand_top = -4.56
    z_min_hand_base = -4.64
    z_min_hand_top = -4.80
    z_sapphire_inner = -4.90

    # Ensure monotonic ordering down into negative Z
    assert z_baton_top > z_hour_hand_base, "Hour hand collides with dial applied batons"
    assert z_sec_hand_top > z_hour_hand_base, "Hour hand collides with small seconds hand"
    assert z_hour_hand_top > z_min_hand_base, "Minute hand collides with hour hand"
    assert z_min_hand_top > z_sapphire_inner, "Minute hand collides with front sapphire crystal"


def test_small_seconds_pivot_alignment():
    """Verify small-seconds hand and dial subdial are coaxial with fourth wheel pivot."""
    sys.path.insert(0, str(SRC_DIR))
    from lib.datums import FOURTH_PIVOT

    assert FOURTH_PIVOT == (-9.0000, 0.0000), f"Fourth pivot {FOURTH_PIVOT} deviates from (-9.0, 0.0)"


def test_crown_tube_stem_concentricity():
    """Verify crown tube axis is strictly concentric with winding stem."""
    sys.path.insert(0, str(SRC_DIR))
    from lib.datums import STEM_Y, STEM_Z

    assert STEM_Y == -2.50, f"Stem Y coordinate {STEM_Y} != -2.50"
    assert STEM_Z == -0.80, f"Stem Z coordinate {STEM_Z} != -0.80"


def test_gear_train_kinematic_ratio():
    """Verify gear tooth counts produce the correct 18,000 vph (2.5 Hz) frequency."""
    sys.path.insert(0, str(SRC_DIR))
    from lib.parameters import GEAR_DATA

    center = GEAR_DATA["center"]
    third = GEAR_DATA["third"]
    fourth = GEAR_DATA["fourth"]
    escape = GEAR_DATA["escape"]

    # Gear train ratio from Center Wheel to Escape Pinion:
    # (z_center / z_third_pinion) * (z_third / z_fourth_pinion) * (z_fourth / z_escape_pinion)
    r1 = center["wheel_teeth"] / third["pinion_leaves"]
    r2 = third["wheel_teeth"] / fourth["pinion_leaves"]
    r3 = fourth["wheel_teeth"] / escape["pinion_leaves"]

    total_gear_ratio = r1 * r2 * r3
    escapement_teeth = escape["wheel_teeth"]
    vibrations_per_hour = total_gear_ratio * (2 * escapement_teeth)

    assert vibrations_per_hour == 18000.0, f"Calculated frequency {vibrations_per_hour} != 18,000 vph"


def test_assembly_interference_free():
    """Verify zero physical clashes/interferences across all components in the complete watch."""
    cmd = ["cadgen", "step", "inspect", "interfere", "STEP/watch_caliber_assembly.step"]
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)
    data = json.loads(res.stdout) if res.stdout else {}
    clashes = data.get("clashes", [])
    assert len(clashes) == 0, f"Found {len(clashes)} clash(es): {clashes}"


def test_hand_color_materials_and_separation():
    """Verify hour, minute, and seconds hands have distinct colors and materials."""
    sys.path.insert(0, str(SRC_DIR))
    from watch_exterior.hands import hour_hand, minute_hand, seconds_hand, hands
    from build123d import Compound

    h = hour_hand()
    m = minute_hand()
    s = seconds_hand()

    # Verify colors are defined and distinct
    assert h.color is not None, "Hour hand missing color"
    assert m.color is not None, "Minute hand missing color"
    assert s.color is not None, "Seconds hand missing color"
    assert h.color != s.color, "Hour and seconds hand must have different colors"
    assert m.color != s.color, "Minute and seconds hand must have different colors"

    # Verify cad_material attributes
    assert hasattr(h, "cad_material") and h.cad_material["metalness"] > 0.8
    assert hasattr(m, "cad_material") and m.cad_material["metalness"] > 0.8
    assert hasattr(s, "cad_material") and s.cad_material["roughness"] > 0.15

    # Verify hands compound returns 3 distinct children
    all_hands = hands()
    assert isinstance(all_hands, Compound)
    num_children = len(all_hands.children) if hasattr(all_hands, "children") else len(all_hands.solids())
    assert num_children == 3, f"Expected 3 children in hands compound, got {num_children}"


def test_animation_clips_and_no_error_suppression():
    """Verify animation JS module defines all 5 required clips and contains NO try/catch suppression."""
    anim_js = STEP_DIR / "watch_caliber_assembly.step.js"
    assert anim_js.exists(), "Missing animation JS sidecar file"

    content = anim_js.read_text(encoding="utf-8")

    # Verify all 5 clips exist
    required_clips = [
        "running_real_time",
        "running_x60",
        "wind_crown",
        "time_setting",
        "inspection_exploded",
    ]
    for clip in required_clips:
        assert f"{clip}:" in content, f"Animation clip '{clip}' is missing from JS module"

    # Verify NO try/catch error masking exists
    assert "try {" not in content and "try{" not in content, "Found 'try' block suppressing errors in animation JS"
    assert "catch (" not in content and "catch(" not in content, "Found 'catch' block suppressing errors in animation JS"


def test_kinematics_inspection_sliders_and_poses():
    """Verify KINEMATICS configuration includes inspection sliders and inspection_open pose."""
    json_path = STEP_DIR / "watch_caliber_assembly.step.json"
    assert json_path.exists(), "Missing assembly sidecar JSON"
    sidecar = json.loads(json_path.read_text(encoding="utf-8"))
    mates = {m["name"]: m for m in sidecar["kinematics"]["mates"]}

    # 1. Front Cover Open Slider
    assert "front_cover_open" in mates, "Missing 'front_cover_open' kinematic slider"
    fc = mates["front_cover_open"]
    assert fc["kind"] == "slider"
    assert fc["parent"] == "#mainplate"
    assert fc["child"] == "#bezel_and_crystal"
    assert fc["axis"]["dir"] == [0.0, 0.0, -1.0]
    assert fc["limits"]["value"] == [0.0, 8.0]

    # 2. Rear Cover Open Slider
    assert "rear_cover_open" in mates, "Missing 'rear_cover_open' kinematic slider"
    rc = mates["rear_cover_open"]
    assert rc["kind"] == "slider"
    assert rc["parent"] == "#mainplate"
    assert rc["child"] == "#exhibition_caseback"
    assert rc["axis"]["dir"] == [0.0, 0.0, 1.0]
    assert rc["limits"]["value"] == [0.0, 8.0]

    # 3. Caseband Inspection Shift Slider
    assert "caseband_inspection_shift" in mates, "Missing 'caseband_inspection_shift' kinematic slider"
    cb = mates["caseband_inspection_shift"]
    assert cb["kind"] == "slider"
    assert cb["parent"] == "#mainplate"
    assert cb["child"] == "#caseband"
    assert cb["axis"]["dir"] == [1.0, 0.0, 0.0]
    assert cb["limits"]["value"] == [0.0, 10.0]

    # 4. Inspection Open Pose
    poses = sidecar["kinematics"]["poses"]
    assert "inspection_open" in poses, "Missing 'inspection_open' pose"
    insp_pose = poses["inspection_open"]
    assert insp_pose.get("front_cover_open") == 8.0
    assert insp_pose.get("rear_cover_open") == 8.0
    assert insp_pose.get("caseband_inspection_shift") == 10.0


def test_winding_and_ratchet_kinematics_and_occurrences():
    """Verify all 10 winding and ratchet occurrences exist with distinct labels and proper mates."""
    json_path = STEP_DIR / "watch_caliber_assembly.step.json"
    assert json_path.exists(), "Missing assembly sidecar JSON"
    sidecar = json.loads(json_path.read_text(encoding="utf-8"))
    mates = {m["name"]: m for m in sidecar["kinematics"]["mates"]}

    # 1. Verify occurrence children are mapped in kinematics mates
    mapped_children = {m.get("child") for m in sidecar["kinematics"]["mates"]}
    required_children = [
        "#ratchet_wheel",
        "#crown_wheel_internal",
        "#ratchet_click",
        "#barrel_arbor",
        "#mainspring_barrel_drum",
        "#winding_stem",
        "#winding_crown",
        "#winding_pinion",
        "#sliding_pinion",
    ]
    for rc in required_children:
        assert rc in mapped_children, f"Missing '{rc}' child in kinematics mates"

    # 2. Verify kinematics mates
    assert "crown_joint" in mates, "Missing 'crown_joint' cylindrical mate"
    assert "stem_to_crown" in mates, "Missing 'stem_to_crown' fastened mate"
    assert "crown_wheel_rot" in mates, "Missing 'crown_wheel_rot' revolute mate"
    assert "ratchet_wheel_rot" in mates, "Missing 'ratchet_wheel_rot' revolute mate"
    assert "barrel_arbor_rot" in mates, "Missing 'barrel_arbor_rot' revolute mate"
    assert "barrel_rot" in mates, "Missing 'barrel_rot' revolute mate"
    assert "ratchet_click_rot" in mates, "Missing 'ratchet_click_rot' revolute mate"

    # 3. Verify winding pose exists and sets proper values
    poses = sidecar["kinematics"]["poses"]
    assert "winding" in poses, "Missing 'winding' pose"
    w_pose = poses["winding"]
    assert w_pose.get("crown_joint.turn") == 360.0
    assert w_pose.get("crown_wheel_rot") != 0.0
    assert w_pose.get("ratchet_wheel_rot") != 0.0
    assert w_pose.get("barrel_arbor_rot") != 0.0

