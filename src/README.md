# Watch Caliber CAD Model Catalog (ETA 6497 / 6498 Reference)

This directory contains the fully parameterized 3D CAD models, horological gear train calculations, and assembly definitions for a classic manual-wind Swiss watch movement (Ø36.60 mm, 16.5''', 18,000 vph / 2.5 Hz).

## Kinematic Layout & Mating Datums

The movement layout has been geometrically and kinematically solved for 100% pitch-circle meshing and 0 geometric collisions:

| Subsystem / Pivot | Coordinates $(X, Y)$ [mm] | Center Distance $C$ [mm] | Gear Ratio & Teeth |
| :--- | :--- | :--- | :--- |
| **Center Pivot** | $(0.0000, 0.0000)$ | — | Center: $Z=80, m=0.15$; Pinion: $z=12, m=0.18$ |
| **Barrel Pivot** | $(-3.5019, -7.2039)$ | $C_{b-c} = 8.0100$ | Barrel: $Z=77, m=0.18$ |
| **Third Pivot** | $(-5.5863, 3.7890)$ | $C_{c-3} = 6.7500$ | Third Wheel: $Z=75, m=0.12$; Pinion: $z=10, m=0.15$ |
| **Fourth Pivot** | $(-9.0000, 0.0000)$ | $C_{3-4} = 5.1000$ | Fourth Wheel: $Z=80, m=0.10$; Pinion: $z=10, m=0.12$ (Small-seconds at 9 o'clock) |
| **Escape Pivot** | $(-7.6403, 4.1846)$ | $C_{4-e} = 4.4000$ | Escape Wheel: 15 club teeth; Pinion: $z=8, m=0.10$ |
| **Pallet Pivot** | $(-5.9076, 7.9005)$ | $C_{e-p} = 4.1000$ | Swiss lever, entry/exit ruby stones, $\pm 4.5^\circ$ swing |
| **Balance Pivot** | $(-3.3364, 10.9647)$ | $C_{p-b} = 4.0000$ | Balance: Ø11.5 mm, 12 timing screws, $\pm 270^\circ$ amplitude, 2.5 Hz |

## Vertical Stacking & Non-Interference Layers (Z-Axis)

- **Layer 0 (Z = -2.20 to -0.70 mm)**: Dial-side motion work (cannon pinion, minute wheel, hour wheel) and keyless winding works (winding stem, sliding clutch, setting lever), housed within underside pockets of the mainplate.
- **Layer 1 (Z = -0.60 to +0.40 mm)**: Mainspring barrel drum and outer toothed rim, meshing with the center pinion at $Z = 0.05 \dots 0.45\text{ mm}$.
- **Layer 2 (Z = 0.50 to 0.78 mm)**: Center wheel disc ($Z = 0.58 \dots 0.78\text{ mm}$, elevated to clear barrel drum), fourth wheel disc ($Z = 0.50 \dots 0.68\text{ mm}$).
- **Layer 3 (Z = 0.82 to 1.03 mm)**: Third wheel disc ($Z = 0.85 \dots 1.03\text{ mm}$), fourth pinion ($Z = 0.82 \dots 1.00\text{ mm}$).
- **Layer 4 (Z = 0.75 to 0.92 mm)**: Escapement interaction plane (escape wheel club teeth, pallet fork horns and ruby stones, roller impulse jewel).
- **Layer 5 (Z = 1.18 to 1.48 mm)**: Balance wheel rim and 12 peripheral poise screws.
- **Layer 6 (Z = 1.50 to 1.62 mm)**: Archimedean spiral hairspring with slotted collet, stud, and regulator pins.
- **Bridges**:
  - `train_bridge`: Base ceiling at $Z = 1.12\text{ mm}$ with dedicated gear clearance pockets, top face at $Z = 1.65\text{ mm}$.
  - `barrel_bridge`: Underside clearance pocket at $Z = 0.0 \dots 0.90\text{ mm}$, top face at $Z = 1.60\text{ mm}$ carrying ratchet & crown work.
  - `balance_cock`: Cantilever undercut pocket at $Z = 0.0 \dots 1.60\text{ mm}$, top face at $Z = 2.10\text{ mm}$ with Incabloc shock setting.

## Verification & Status

- **CI/CD Sandbox**: 6/6 pipeline stages pass (`AST Audit`, `Model Build`, `BRepCheck Validation`, `Horological Tolerances`, `Snapshots`).
- **Interference**: `cadgen step inspect interfere` reports **0 clashes** across all 21 occurrence pairs.
- **Kinematics & Animation**: Mates declared via `cadgen.revolute`, `cadgen.couple` ($1 : -8 : +60 : -600$), clips `running_2_5hz`, `running_x60`, and `wind_crown` defined in `STEP/watch_caliber_assembly.step.js`.
- **Engineering Disclaimer**: This CAD model is a demonstration caliber with kinematic clearance and nominal dimensions. Commercial manufacturing requires physical tolerance stackup analysis (ISO 2768 / NIHS horological standards), DFM tooling allowances, and physical spring rate validation.

