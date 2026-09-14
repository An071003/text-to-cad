// STEP/watch_caliber_assembly.step.js
// High-Horology Demonstration Animation Module for ETA 6497 Watch Caliber (18,000 vph / 2.5 Hz).

export const clips = {
  running_2_5hz: {
    label: "Running (2.5 Hz Real-Time)",
    duration: 10,
    loop: true,
    update(t, m) {
      // 1. Balance Wheel & Staff: 2.5 Hz harmonic oscillation, amplitude +-270 deg
      const balAngle = 270.0 * Math.sin(2.0 * Math.PI * 2.5 * t);
      m.get("balance_wheel").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      m.get("hairspring_spiral").rotate([0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      m.get("double_roller_table").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // 2. Pallet Fork: swings between banking pins (+-4.5 deg), locking and unlocking escape teeth
      const palletPhase = Math.sin(2.0 * Math.PI * 2.5 * t);
      const palletAngle = 4.5 * Math.tanh(palletPhase * 8.0);
      m.get("pallet_fork").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      m.get("pallet_jewels").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // 3. Escape Wheel: 15 teeth -> 30 beats per rev -> advances 12 deg per beat (5 beats/sec, period 0.2s)
      const beats = Math.floor(t * 5.0);
      const beatProgress = (t * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0); // crisp rapid impulse during drop
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      m.get("escape_wheel_assembly").rotate([0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // 4. Fourth Wheel (Small Seconds): 1 rev / 60 sec = 6 deg/sec
      // Gear ratio fourth to escape pinion = 80:8 = 10:1 (opposite rotation)
      const fourthAngle = escapeAngle / -10.0;
      m.get("fourth_wheel_assembly").rotate([0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);

      // 5. Third Wheel: gear ratio third to fourth pinion = 75:10 = 7.5:1
      const thirdAngle = fourthAngle / -7.5;
      m.get("third_wheel_assembly").rotate([0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // 6. Center Wheel: gear ratio center to third pinion = 80:10 = 8.0:1 (1 rev / hour)
      const centerAngle = thirdAngle / -8.0;
      m.get("center_wheel_assembly").rotate([0, 0, 1], centerAngle, [0, 0, 0]);
    },
  },

  running_x60: {
    label: "Running (60x Presentation Speed)",
    duration: 10,
    loop: true,
    update(t, m) {
      const simT = t * 60.0;

      // Balance wheel oscillation
      const balAngle = 270.0 * Math.sin(2.0 * Math.PI * 2.5 * simT);
      m.get("balance_wheel").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      m.get("hairspring_spiral").rotate([0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      m.get("double_roller_table").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // Pallet fork
      const palletAngle = 4.5 * Math.tanh(Math.sin(2.0 * Math.PI * 2.5 * simT) * 8.0);
      m.get("pallet_fork").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      m.get("pallet_jewels").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // Escape wheel (10 rpm * 60 = 600 rpm presentation)
      const beats = Math.floor(simT * 5.0);
      const beatProgress = (simT * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0);
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      m.get("escape_wheel_assembly").rotate([0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // Fourth wheel (1 rpm * 60 = 60 rpm = 1 rev/sec presentation)
      const fourthAngle = escapeAngle / -10.0;
      m.get("fourth_wheel_assembly").rotate([0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);

      // Third wheel
      const thirdAngle = fourthAngle / -7.5;
      m.get("third_wheel_assembly").rotate([0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // Center wheel (1 rph * 60 = 1 rpm presentation)
      const centerAngle = thirdAngle / -8.0;
      m.get("center_wheel_assembly").rotate([0, 0, 1], centerAngle, [0, 0, 0]);
    },
  },

  wind_crown: {
    label: "Winding Crown & Ratchet Work",
    duration: 4,
    loop: true,
    update(t, m) {
      // Crown turns clockwise (X-axis)
      const crownDeg = t * 360.0;
      m.get("keyless_winding_mechanism").rotate([1, 0, 0], crownDeg, [18.3, -2.5, -0.8]);

      // Ratchet wheel advances through crown wheel gearing (30:42)
      const ratchetDeg = crownDeg * (30.0 / 42.0);
      m.get("ratchet_and_crown_work").rotate([0, 0, 1], -ratchetDeg, [-3.5019, -7.2039, 0]);
      m.get("mainspring_barrel").rotate([0, 0, 1], -ratchetDeg * 0.08, [-3.5019, -7.2039, 0]);
    },
  },
};
