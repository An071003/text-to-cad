// STEP/watch_caliber_assembly.step.js
// High-Horology Demonstration Animation Module for Classical 42 mm Mechanical Dress Wristwatch.
// Reference: Caliber ETA 6497/6498 (18,000 vph / 2.5 Hz).

function rot(m, name, axis, deg, origin) {
  m.get(name).rotate(axis, deg, origin);
}

function trans(m, name, vec) {
  m.get(name).translate(vec);
}

export const clips = {
  running_real_time: {
    label: "Running Real-Time (18,000 vph / 2.5 Hz)",
    duration: 60,
    loop: true,
    update(t, m) {
      // 1. Balance Wheel & Staff: 2.5 Hz harmonic oscillation, amplitude +-220 deg
      const balAngle = 220.0 * Math.sin(2.0 * Math.PI * 2.5 * t);
      rot(m, "balance_wheel", [0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      rot(m, "hairspring_spiral", [0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      rot(m, "double_roller_table", [0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // 2. Pallet Fork: swings between banking pins (+-4.5 deg), locking & unlocking escape teeth
      const palletPhase = Math.sin(2.0 * Math.PI * 2.5 * t);
      const palletAngle = 4.5 * Math.tanh(palletPhase * 8.0);
      rot(m, "pallet_fork", [0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      rot(m, "pallet_jewels", [0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // 3. Escape Wheel: 15 teeth -> 30 beats per rev -> advances 12 deg per beat (5 beats/sec, period 0.2s)
      const beats = Math.floor(t * 5.0);
      const beatProgress = (t * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0); // crisp impulse during drop
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      rot(m, "escape_wheel_assembly", [0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // 4. Fourth Wheel & Small Seconds Hand: 1 rev / 60 sec (6 deg/sec)
      // Gear ratio fourth to escape pinion = 80:8 = 10:1 (opposite rotation)
      const fourthAngle = escapeAngle / -10.0;
      rot(m, "fourth_wheel_assembly", [0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);
      // Small seconds hand rotates clockwise from dial view: -6 deg/s (-360 deg in 60s)
      const secHandAngle = - (t / 60.0) * 360.0;
      rot(m, "seconds_hand", [0, 0, 1], secHandAngle, [-9.0000, 0.0000, 0]);

      // 5. Third Wheel: gear ratio third to fourth pinion = 75:10 = 7.5:1
      const thirdAngle = fourthAngle / -7.5;
      rot(m, "third_wheel_assembly", [0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // 6. Center Wheel, Minute Hand & Hour Hand:
      // Center wheel gear ratio center to third pinion = 80:10 = 8.0:1 (1 rev / hour)
      const centerAngle = thirdAngle / -8.0;
      rot(m, "center_wheel_assembly", [0, 0, 1], centerAngle, [0, 0, 0]);

      // Minute hand: 360 deg / 3600 s = -0.1 deg/s (clockwise from dial face)
      const minHandAngle = - (t / 3600.0) * 360.0;
      rot(m, "minute_hand", [0, 0, 1], minHandAngle, [0, 0, 0]);

      // Hour hand: 360 deg / 43200 s = - (0.1 / 12.0) deg/s
      const hourHandAngle = minHandAngle / 12.0;
      rot(m, "hour_hand", [0, 0, 1], hourHandAngle, [0, 0, 0]);

      // 7. Mainspring Barrel Drum: slowly rotates to power gear train (z=77 meshes with z=12 center pinion)
      const barrelDrumAngle = - centerAngle * (12.0 / 77.0);
      rot(m, "mainspring_barrel_drum", [0, 0, 1], barrelDrumAngle, [-3.5019, -7.2039, 0]);

      // Ratchet wheel and barrel arbor remain fixed after winding
      rot(m, "ratchet_wheel", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "barrel_arbor", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "crown_wheel_internal", [0, 0, 1], 0.0, [3.5000, -6.0000, 0]);
    },
  },

  running_x60: {
    label: "Running 60x Speed Presentation",
    duration: 12,
    loop: true,
    update(t, m) {
      const simT = t * 60.0;

      // Balance wheel oscillation (2.5 Hz * 60)
      const balAngle = 220.0 * Math.sin(2.0 * Math.PI * 2.5 * simT);
      rot(m, "balance_wheel", [0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);
      rot(m, "hairspring_spiral", [0, 0, 1], balAngle * 0.95, [-3.3364, 10.9647, 0]);
      rot(m, "double_roller_table", [0, 0, 1], balAngle, [-3.3364, 10.9647, 0]);

      // Pallet fork
      const palletAngle = 4.5 * Math.tanh(Math.sin(2.0 * Math.PI * 2.5 * simT) * 8.0);
      rot(m, "pallet_fork", [0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);
      rot(m, "pallet_jewels", [0, 0, 1], palletAngle, [-5.9076, 7.9005, 0]);

      // Escape wheel (10 rpm * 60 = 600 rpm presentation)
      const beats = Math.floor(simT * 5.0);
      const beatProgress = (simT * 5.0) - beats;
      const stepImpulse = Math.min(1.0, beatProgress * 4.0);
      const escapeAngle = -(beats + stepImpulse) * 12.0;
      rot(m, "escape_wheel_assembly", [0, 0, 1], escapeAngle, [-7.6403, 4.1846, 0]);

      // Fourth wheel & small seconds (1 rev/sec in presentation: -360 deg/s clockwise)
      const fourthAngle = escapeAngle / -10.0;
      rot(m, "fourth_wheel_assembly", [0, 0, 1], fourthAngle, [-9.0000, 0.0000, 0]);
      const secHandAngle = - (simT / 60.0) * 360.0;
      rot(m, "seconds_hand", [0, 0, 1], secHandAngle, [-9.0000, 0.0000, 0]);

      // Third wheel
      const thirdAngle = fourthAngle / -7.5;
      rot(m, "third_wheel_assembly", [0, 0, 1], thirdAngle, [-5.5863, 3.7890, 0]);

      // Center wheel (1 rpm presentation)
      const centerAngle = thirdAngle / -8.0;
      rot(m, "center_wheel_assembly", [0, 0, 1], centerAngle, [0, 0, 0]);

      // Minute hand: sweeps 72 deg over 12s (6 deg/s clockwise)
      const minHandAngle = - (simT / 3600.0) * 360.0;
      rot(m, "minute_hand", [0, 0, 1], minHandAngle, [0, 0, 0]);

      // Hour hand: sweeps 6 deg over 12s (0.5 deg/s clockwise, 12:1 ratio)
      const hourHandAngle = minHandAngle / 12.0;
      rot(m, "hour_hand", [0, 0, 1], hourHandAngle, [0, 0, 0]);

      // Mainspring barrel drum rotation at 60x
      const barrelDrumAngle = - centerAngle * (12.0 / 77.0);
      rot(m, "mainspring_barrel_drum", [0, 0, 1], barrelDrumAngle, [-3.5019, -7.2039, 0]);
      rot(m, "ratchet_wheel", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "barrel_arbor", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "crown_wheel_internal", [0, 0, 1], 0.0, [3.5000, -6.0000, 0]);
    },
  },

  wind_crown: {
    label: "Winding Crown & Ratchet Mechanism",
    duration: 4,
    loop: true,
    update(t, m) {
      // 1. Crown & Stem rotate about X-axis
      const crownDeg = t * 360.0;
      rot(m, "winding_crown", [1, 0, 0], crownDeg, [21.60, -2.50, -0.80]);
      rot(m, "winding_stem", [1, 0, 0], crownDeg, [18.30, -2.50, -0.80]);
      rot(m, "winding_pinion", [1, 0, 0], crownDeg, [11.20, -2.50, -0.80]);
      rot(m, "sliding_pinion", [1, 0, 0], crownDeg, [13.20, -2.50, -0.80]);

      // 2. Crown wheel internal rotates about its own real pivot [3.50, -6.00, 0]
      // Winding pinion (z=14) drives crown wheel (z=30)
      const crownWheelDeg = - crownDeg * (14.0 / 30.0);
      rot(m, "crown_wheel_internal", [0, 0, 1], crownWheelDeg, [3.5000, -6.0000, 0]);

      // 3. Ratchet wheel rotates about BARREL_PIVOT driven by crown wheel
      // Crown wheel (z=30) drives ratchet wheel (z=42)
      const ratchetDeg = - crownWheelDeg * (30.0 / 42.0);
      rot(m, "ratchet_wheel", [0, 0, 1], ratchetDeg, [-3.5019, -7.2039, 0]);

      // 4. Barrel arbor rotates with ratchet wheel on square seat (winding the mainspring)
      rot(m, "barrel_arbor", [0, 0, 1], ratchetDeg, [-3.5019, -7.2039, 0]);

      // Mainspring barrel drum remains stationary during winding
      rot(m, "mainspring_barrel_drum", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);

      // 5. Ratchet click oscillates 3-8 deg as each ratchet tooth passes
      const toothPitch = 360.0 / 42.0;
      const toothProgress = ((ratchetDeg % toothPitch) + toothPitch) % toothPitch / toothPitch;
      const clickAngle = 3.0 + 5.0 * Math.sin(toothProgress * Math.PI);
      rot(m, "ratchet_click", [0, 0, 1], clickAngle, [-8.5000, -13.0000, 0]);

      // 6. Click spring remains fixed
      rot(m, "click_spring", [0, 0, 1], 0.0, [-9.7000, -13.5000, 0]);
    },
  },

  time_setting: {
    label: "Time Setting (Crown Pulled & Hands Sweeping)",
    duration: 6,
    loop: true,
    update(t, m) {
      // 1. Crown & Stem pull out along +X by 1.20 mm in the first 0.6 seconds
      const pullProgress = Math.min(1.0, t / 0.6);
      const crownX = pullProgress * 1.20;
      trans(m, "winding_crown", [crownX, 0, 0]);
      trans(m, "winding_stem", [crownX, 0, 0]);
      trans(m, "sliding_pinion", [crownX * 0.8, 0, 0]);

      // 2. Once pulled, crown & stem rotate to adjust time
      const activeT = Math.max(0.0, t - 0.6);
      const crownTurn = activeT * 360.0 * 1.5;
      rot(m, "winding_crown", [1, 0, 0], crownTurn, [21.60 + crownX, -2.50, -0.80]);
      rot(m, "winding_stem", [1, 0, 0], crownTurn, [18.30 + crownX, -2.50, -0.80]);
      rot(m, "sliding_pinion", [1, 0, 0], crownTurn, [13.20 + crownX * 0.8, -2.50, -0.80]);

      // Crown wheel internal does NOT rotate when crown is pulled in time setting mode
      rot(m, "crown_wheel_internal", [0, 0, 1], 0.0, [3.5000, -6.0000, 0]);
      rot(m, "ratchet_wheel", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "barrel_arbor", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);
      rot(m, "mainspring_barrel_drum", [0, 0, 1], 0.0, [-3.5019, -7.2039, 0]);

      // 3. Minute hand rotates rapidly (1.5 full turns per second)
      const minHandDeg = - activeT * 360.0 * 1.5;
      rot(m, "minute_hand", [0, 0, 1], minHandDeg, [0, 0, 0]);

      // 4. Hour hand follows with precise 12:1 reduction (-45 deg per 1.5 turns of minute hand)
      const hourHandDeg = minHandDeg / 12.0;
      rot(m, "hour_hand", [0, 0, 1], hourHandDeg, [0, 0, 0]);

      // 5. Small seconds hand remains stationary (hacked / isolated)
      rot(m, "seconds_hand", [0, 0, 1], 0.0, [-9.0000, 0.0000, 0]);
    },
  },

  inspection_exploded: {
    label: "Inspection / Exploded View (5s)",
    duration: 5,
    loop: true,
    update(t, m) {
      // 0 - 1.5s: Bezel & Front Sapphire shift negative Z (towards dial side by 8 mm)
      const p1 = Math.min(1.0, t / 1.5);
      trans(m, "bezel_and_crystal", [0, 0, -8.0 * p1]);

      // 1.5 - 3.0s: Exhibition Caseback shifts positive Z (towards bridge side by 8 mm)
      const p2 = Math.min(1.0, Math.max(0.0, (t - 1.5) / 1.5));
      trans(m, "exhibition_caseback", [0, 0, 8.0 * p2]);

      // 3.0 - 4.0s: Caseband shifts positive X (by 10 mm) to completely reveal movement caliber
      const p3 = Math.min(1.0, Math.max(0.0, (t - 3.0) / 1.0));
      trans(m, "caseband", [10.0 * p3, 0, 0]);

      // 4.0 - 5.0s: Holds open inspection state; all internal caliber parts stay firmly at datum
    },
  },
};
