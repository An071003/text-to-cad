# Watch Caliber CAD Model Catalog

This directory contains the parameterized source models and subsystem packages for the mechanical watch caliber (ETA 6497 / Unitas 6498 base reference).

## Subsystems Layout

- `lib/`: Shared kinematic parameters, gear tooth profile generators, tolerance standards, and mating datums.
- `mainplate_and_bridges/`: Mainplate, train bridge, balance bridge, barrel bridge, and pallet bridge.
- `gear_train/`: Center wheel, third wheel, fourth wheel (seconds), and respective arbors/pinions.
- `escapement/`: Swiss lever escapement wheel, pallet fork, entry/exit pallet stones, and guard pin.
- `balance/`: Balance wheel, hairspring (spiral), collet, roller table, impulse jewel, and regulator index.
- `winding_and_barrel/`: Mainspring barrel, barrel cover, arbor, ratchet wheel, crown wheel, click, click spring, stem, winding pinion, clutch wheel, setting lever, and motion work (cannon pinion, minute wheel, hour wheel).
- `fasteners/`: Screws (bridge, ratchet, dial, casing), jewels (friction fit & chatons), steady pins.
- `assembly.py`: Top-level assembly integrating all subsystems via `AssemblyHelper` and named mating datums.
