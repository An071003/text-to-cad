"""Regression Tests for Horological Gear Train Kinematics & Center Distances.

Verifies that all pitch radii, center distances, and gear ratios match
horological design theory for the ETA 6497 caliber reference.
"""

import math
import pytest
from src.lib.datums import (
    BALANCE_PIVOT,
    BARREL_PIVOT,
    CENTER_PIVOT,
    ESCAPE_PIVOT,
    FOURTH_PIVOT,
    PALLET_PIVOT,
    THIRD_PIVOT,
)
from src.lib.parameters import CENTER_DISTANCES, GEAR_DATA, MAINPLATE_DIAMETER, PITCH_RADII


def test_pitch_radii_calculations():
    """Verify individual gear pitch radii match teeth and module."""
    assert PITCH_RADII["barrel_wheel"] == pytest.approx(77 * 0.18 / 2.0, abs=1e-4)
    assert PITCH_RADII["center_pinion"] == pytest.approx(12 * 0.18 / 2.0, abs=1e-4)
    assert PITCH_RADII["center_wheel"] == pytest.approx(80 * 0.15 / 2.0, abs=1e-4)
    assert PITCH_RADII["third_pinion"] == pytest.approx(10 * 0.15 / 2.0, abs=1e-4)
    assert PITCH_RADII["third_wheel"] == pytest.approx(75 * 0.12 / 2.0, abs=1e-4)
    assert PITCH_RADII["fourth_pinion"] == pytest.approx(10 * 0.12 / 2.0, abs=1e-4)
    assert PITCH_RADII["fourth_wheel"] == pytest.approx(80 * 0.10 / 2.0, abs=1e-4)
    assert PITCH_RADII["escape_pinion"] == pytest.approx(8 * 0.10 / 2.0, abs=1e-4)


def test_gear_train_center_distances():
    """Verify physical center-to-center distances between pivots match theoretical pitch distance."""
    # 1. Center to Barrel (8.0100 mm)
    d_barrel_center = math.hypot(BARREL_PIVOT[0] - CENTER_PIVOT[0], BARREL_PIVOT[1] - CENTER_PIVOT[1])
    assert d_barrel_center == pytest.approx(CENTER_DISTANCES["barrel_center"], abs=1e-3)

    # 2. Center to Third (6.7500 mm)
    d_center_third = math.hypot(THIRD_PIVOT[0] - CENTER_PIVOT[0], THIRD_PIVOT[1] - CENTER_PIVOT[1])
    assert d_center_third == pytest.approx(CENTER_DISTANCES["center_third"], abs=1e-3)

    # 3. Third to Fourth (5.1000 mm) - CRITICAL FIX (previously 14.27 mm)
    d_third_fourth = math.hypot(FOURTH_PIVOT[0] - THIRD_PIVOT[0], FOURTH_PIVOT[1] - THIRD_PIVOT[1])
    assert d_third_fourth == pytest.approx(CENTER_DISTANCES["third_fourth"], abs=1e-3)
    assert d_third_fourth < 6.0, "Third to Fourth distance must be close to pitch distance 5.10 mm"

    # 4. Fourth to Escape (4.4000 mm)
    d_fourth_escape = math.hypot(ESCAPE_PIVOT[0] - FOURTH_PIVOT[0], ESCAPE_PIVOT[1] - FOURTH_PIVOT[1])
    assert d_fourth_escape == pytest.approx(CENTER_DISTANCES["fourth_escape"], abs=1e-3)

    # 5. Escape to Pallet (4.1000 mm)
    d_escape_pallet = math.hypot(PALLET_PIVOT[0] - ESCAPE_PIVOT[0], PALLET_PIVOT[1] - ESCAPE_PIVOT[1])
    assert d_escape_pallet == pytest.approx(CENTER_DISTANCES["escape_pallet"], abs=1e-3)

    # 6. Pallet to Balance (4.0000 mm)
    d_pallet_balance = math.hypot(BALANCE_PIVOT[0] - PALLET_PIVOT[0], BALANCE_PIVOT[1] - PALLET_PIVOT[1])
    assert d_pallet_balance == pytest.approx(CENTER_DISTANCES["pallet_balance"], abs=1e-3)


def test_small_seconds_position():
    """Verify fourth wheel is placed at canonical 9 o'clock position (X = -9.0, Y = 0.0)."""
    assert FOURTH_PIVOT[0] == pytest.approx(-9.0, abs=0.5)
    assert FOURTH_PIVOT[1] == pytest.approx(0.0, abs=0.5)


def test_balance_envelope_clearance():
    """Verify 11.5mm balance wheel stays within the mainplate boundary."""
    mainplate_radius = MAINPLATE_DIAMETER / 2.0  # 18.30 mm
    balance_radius = 11.5 / 2.0  # 5.75 mm
    dist_center_to_balance = math.hypot(BALANCE_PIVOT[0], BALANCE_PIVOT[1])
    outer_edge = dist_center_to_balance + balance_radius
    assert outer_edge < mainplate_radius, f"Balance outer edge {outer_edge:.2f} exceeds {mainplate_radius:.2f}"


def test_kinematic_frequency():
    """Verify gear ratios produce exact 18,000 vph (2.5 Hz) frequency."""
    c_to_3 = GEAR_DATA["center"]["wheel_teeth"] / GEAR_DATA["third"]["pinion_leaves"]
    t_to_4 = GEAR_DATA["third"]["wheel_teeth"] / GEAR_DATA["fourth"]["pinion_leaves"]
    f_to_e = GEAR_DATA["fourth"]["wheel_teeth"] / GEAR_DATA["escape"]["pinion_leaves"]
    escape_teeth = GEAR_DATA["escape"]["wheel_teeth"]

    total_ratio = c_to_3 * t_to_4 * f_to_e
    assert total_ratio == pytest.approx(600.0)

    vph = total_ratio * (2 * escape_teeth)
    assert vph == pytest.approx(18000.0)
    hz = vph / 7200.0
    assert hz == pytest.approx(2.5)
