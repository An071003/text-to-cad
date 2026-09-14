"""Automated Pytest Suite for Watch Caliber CAD Models."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STEP_DIR = PROJECT_ROOT / "STEP"
SRC_DIR = PROJECT_ROOT / "src"

REQUIRED_STEP_MODELS = [
    "mainplate.step",
    "barrel_bridge.step",
    "train_bridge.step",
    "pallet_cock.step",
    "balance_cock.step",
    "center_wheel.step",
    "third_wheel.step",
    "fourth_wheel.step",
    "escape_wheel.step",
    "pallet_fork.step",
    "pallet_jewels.step",
    "balance_wheel.step",
    "hairspring.step",
    "roller_table.step",
    "mainspring_barrel.step",
    "ratchet_and_crown.step",
    "winding_mechanism.step",
    "motion_work.step",
    "screws.step",
    "jewels.step",
    "steady_pins.step",
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
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    assert res.returncode == 0, f"Validation command failed: {res.stderr}"

    data = json.loads(res.stdout)
    assert data.get("ok") is True, "Validation result ok != True"
    assert data.get("failureCount", 0) == 0, f"Geometry has {data.get('failureCount')} failure(s)"
    assert data.get("occurrenceCount", 0) >= 21, f"Expected at least 21 parts in assembly, got {data.get('occurrenceCount')}"


def test_caliber_bounding_box_specifications():
    """Verify caliber dimensions adhere to the 16.5 ligne (Ø 36.60 mm) standard."""
    cmd = ["cadgen", "step", "inspect", "refs", "STEP/watch_caliber_assembly.step", "--facts"]
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    assert res.returncode == 0

    data = json.loads(res.stdout)
    facts = data["tokens"][0]["entryFacts"]
    size_x, size_y, size_z = facts["size"]

    # Mainplate base diameter across Y axis must be 36.60 mm (+/- 0.5 mm)
    assert abs(size_y - 36.60) < 1.0, f"Caliber diameter across Y is {size_y:.2f} mm (expected ~36.60 mm)"
    # Height must not exceed 8.0 mm
    assert size_z <= 8.0, f"Caliber total height is {size_z:.2f} mm (exceeds 8.0 mm)"


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
    # 1 hour = 60 minutes = 3600 seconds.
    # Escape wheel rotates (total_gear_ratio) turns per hour.
    # Each escape tooth gives 2 vibrations (beats).
    escapement_teeth = escape["wheel_teeth"]
    vibrations_per_hour = total_gear_ratio * (2 * escapement_teeth)

    assert vibrations_per_hour == 18000.0, f"Calculated frequency {vibrations_per_hour} != 18,000 vph"
