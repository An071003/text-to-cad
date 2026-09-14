// STEP/watch_caliber_assembly.step.js
// High-Horology Demonstration Animation Module for Classical 42 mm Mechanical Dress Wristwatch.
// Reference: Caliber ETA 6497/6498 (18,000 vph / 2.5 Hz).

export const clips = {
  running_real_time: {
    label: "Running Real-Time (18,000 vph / 2.5 Hz)",
    duration: 60,
    loop: true,
    update(t, m) {
      // 1. Balance Wheel & Staff: 2.5 Hz harmonic oscillation, amplitude +-220 deg
      const balAngle = 220.0 * Math.sin(2.0 * Math.PI * 2.5 * t);
      if (m.has("balance_wheel")) m.get("balance_wheel").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      if (m.has("hairspring_spiral")) m.get("hairspring_spiral").rotate([0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      if (m.has("double_roller_table")) m.get("double_roller_table").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // 2. Pallet Fork: swings between banking pins (+-4.5 deg), locking & unlocking escape teeth
      const palletPhase = Math.sin(2.0 * Math.PI * 2.5 * t);
      const palletAngle = 4.5 * Math.tanh(palletPhase * 8.0);
      if (m.has("pallet_fork")) m.get("pallet_fork").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      if (m.has("pallet_jewels")) m.get("pallet_jewels").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // 3. Escape Wheel: 15 teeth -> 30 beats per rev -> advances 12 deg per beat (5 beats/sec, period 0.2s)
      const beats = Math.floor(t * 5.0);
      const beatProgress = (t * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0); // crisp impulse during drop
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      if (m.has("escape_wheel_assembly")) m.get("escape_wheel_assembly").rotate([0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // 4. Fourth Wheel & Small Seconds Hand: 1 rev / 60 sec (6 deg/sec)
      // Gear ratio fourth to escape pinion = 80:8 = 10:1 (opposite rotation)
      const fourthAngle = escapeAngle / -10.0;
      if (m.has("fourth_wheel_assembly")) m.get("fourth_wheel_assembly").rotate([0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);
      // Small seconds hand rotates clockwise from dial view: -6 deg/s (-360 deg in 60s)
      const secHandAngle = - (t / 60.0) * 360.0;
      if (m.has("seconds_hand")) m.get("seconds_hand").rotate([0, 0, 1], secHandAngle, [-9.0000, 0.0000, 0]);

      // 5. Third Wheel: gear ratio third to fourth pinion = 75:10 = 7.5:1
      const thirdAngle = fourthAngle / -7.5;
      if (m.has("third_wheel_assembly")) m.get("third_wheel_assembly").rotate([0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // 6. Center Wheel, Minute Hand & Hour Hand:
      // Center wheel gear ratio center to third pinion = 80:10 = 8.0:1 (1 rev / hour)
      const centerAngle = thirdAngle / -8.0;
      if (m.has("center_wheel_assembly")) m.get("center_wheel_assembly").rotate([0, 0, 1], centerAngle, [0, 0, 0]);

      // Minute hand: 360 deg / 3600 s = -0.1 deg/s (clockwise from dial face)
      const minHandAngle = - (t / 3600.0) * 360.0;
      if (m.has("minute_hand")) m.get("minute_hand").rotate([0, 0, 1], minHandAngle, [0, 0, 0]);

      // Hour hand: 360 deg / 43200 s = - (0.1 / 12.0) deg/s
      const hourHandAngle = minHandAngle / 12.0;
      if (m.has("hour_hand")) m.get("hour_hand").rotate([0, 0, 1], hourHandAngle, [0, 0, 0]);
    },
  },

  running_x60: {
    label: "Running 60x Speed Presentation",
    duration: 12,
    loop: true,
    update(t, m) {
      const simT = t * 60.0;

      // Balance wheel oscillation
      const balAngle = 220.0 * Math.sin(2.0 * Math.PI * 2.5 * simT);
      if (m.has("balance_wheel")) m.get("balance_wheel").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      if (m.has("hairspring_spiral")) m.get("hairspring_spiral").rotate([0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      if (m.has("double_roller_table")) m.get("double_roller_table").rotate([0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // Pallet fork
      const palletAngle = 4.5 * Math.tanh(Math.sin(2.0 * Math.PI * 2.5 * simT) * 8.0);
      if (m.has("pallet_fork")) m.get("pallet_fork").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      if (m.has("pallet_jewels")) m.get("pallet_jewels").rotate([0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // Escape wheel (10 rpm * 60 = 600 rpm presentation)
      const beats = Math.floor(simT * 5.0);
      const beatProgress = (simT * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0);
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      if (m.has("escape_wheel_assembly")) m.get("escape_wheel_assembly").rotate([0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // Fourth wheel & small seconds (1 rev/sec in presentation)
      const fourthAngle = escapeAngle / -10.0;
      if (m.has("fourth_wheel_assembly")) m.get("fourth_wheel_assembly").rotate([0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);
      const secHandAngle = - (simT / 60.0) * 360.0;
      if (m.has("seconds_hand")) m.get("seconds_hand").rotate([0, 0, 1], secHandAngle, [-9.0000, 0.0000, 0]);

      // Third wheel
      const thirdAngle = fourthAngle / -7.5;
      if (m.has("third_wheel_assembly")) m.get("third_wheel_assembly").rotate([0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // Center wheel (1 rpm presentation)
      const centerAngle = thirdAngle / -8.0;
      if (m.has("center_wheel_assembly")) m.get("center_wheel_assembly").rotate([0, 0, 1], centerAngle, [0, 0, 0]);

      // Minute hand: sweeps 72 deg over 12s (6 deg/s)
      const minHandAngle = - (simT / 3600.0) * 360.0;
      if (m.has("minute_hand")) m.get("minute_hand").rotate([0, 0, 1], minHandAngle, [0, 0, 0]);

      // Hour hand: sweeps 6 deg over 12s
      const hourHandAngle = minHandAngle / 12.0;
      if (m.has("hour_hand")) m.get("hour_hand").rotate([0, 0, 1], hourHandAngle, [0, 0, 0]);
    },
  },

  wind_crown: {
    label: "Winding Crown & Ratchet Mechanism",
    duration: 4,
    loop: true,
    update(t, m) {
      // Crown turns clockwise about X-axis
      const crownDeg = t * 360.0;
      if (m.has("winding_crown")) m.get("winding_crown").rotate([1, 0, 0], crownDeg, [21.60, -2.50, -0.80]);
      if (m.has("keyless_winding_mechanism")) m.get("keyless_winding_mechanism").rotate([1, 0, 0], crownDeg, [18.30, -2.50, -0.80]);

      // Ratchet wheel advances through crown wheel gearing (30:42)
      const ratchetDeg = crownDeg * (30.0 / 42.0);
      if (m.has("ratchet_and_crown_work")) m.get("ratchet_and_crown_work").rotate([0, 0, 1], -ratchetDeg, [-3.5019, -7.2039, 0]);
      if (m.has("mainspring_barrel")) m.get("mainspring_barrel").rotate([0, 0, 1], -ratchetDeg * 0.08, [-3.5019, -7.2039, 0]);
    },
  },

  time_setting: {
    label: "Time Setting (Crown Pulled & Hands Sweeping)",
    duration: 6,
    loop: true,
    update(t, m) {
      // 1. Crown pulls out along +X by 1.20 mm in the first 0.6 seconds
      const pullProgress = Math.min(1.0, t / 0.6);
      const crownX = pullProgress * 1.20;
      if (m.has("winding_crown")) m.get("winding_crown").translate([crownX, 0, 0]);

      // 2. Once pulled, crown rotates to adjust time
      const activeT = Math.max(0.0, t - 0.6);
      const crownTurn = activeT * 360.0 * 1.5;
      if (m.has("winding_crown")) m.get("winding_crown").rotate([1, 0, 0], crownTurn, [21.60 + crownX, -2.50, -0.80]);

      // 3. Minute hand rotates rapidly (1.5 full turns per second)
      const minHandDeg = - activeT * 360.0 * 1.5;
      if (m.has("minute_hand")) m.get("minute_hand").rotate([0, 0, 1], minHandDeg, [0, 0, 0]);

      // 4. Hour hand follows with precise 12:1 reduction (-45 deg per 1.5 turns of minute hand)
      const hourHandDeg = minHandDeg / 12.0;
      if (m.has("hour_hand")) m.get("hour_hand").rotate([0, 0, 1], hourHandDeg, [0, 0, 0]);

      // 5. Small seconds hand remains stationary (hacked / isolated)
      if (m.has("seconds_hand")) m.get("seconds_hand").rotate([0, 0, 1], 0.0, [-9.0000, 0.0000, 0]);
    },
  },
};
