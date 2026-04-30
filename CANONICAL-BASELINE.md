# BGKPJR Canonical Baseline — Decision Record
**Effective:** 2026-04-30
**Status:** Active. Supersedes all prior baselines. Pending Lukens validation.

---

## What this is

A single decision record locking in the canonical operating point for the BGKPJR launch architecture. Both `BGKPJR-Launch-Vis` (public site) and `BGKPJR-Core-Simulations` (analysis stack) trace every dimensional value back to this document and to `simulation/src/bgkpjr_dimensions.py`.

## Why this exists now

A pre-Lukens audit (see `expert-reviews/PRE-LUKENS-AUDIT-2026-04-30.md`) found three internally inconsistent BGKPJR baselines living simultaneously across the repos:

- `launch.ts` (public site): 28.7 km / Mach 3.5 / 3.9 G / thermite membrane — internally inconsistent (the four constants did not close kinematically)
- `constants.py` (sims): 28.7 km / Mach 3.5 / ≤4 G — math closed but did not match the public site narrative
- `BGKPJR-VacuumGate Feasibility Report v1.0` (April 18, 2026, authored by Shane Brazelton): 37 km / Mach 5 / 4 G / **liquid-hydrogen cryogenic membrane** — physics-honest revision that explicitly supersedes prior docs

The VG report was written but had not propagated to either repo. This document and the corresponding code changes propagate it.

## The canonical baseline

| Parameter | Canonical Value | Provenance |
|---|---|---|
| Tube length | 37 km | VacuumGate v1.0 §3 |
| Tube diameter (bore) | 10 m | VacuumGate v1.0 §2.2 |
| Tube inclination | 15° | Patent BGKPJR-001 envelope (15-45°) |
| Tube pressure | 0.05 atm | Patent envelope minimum |
| Exit Mach | 5.0 | Patent envelope max; VG canonical |
| Exit velocity | 1,700 m/s | Mach 5 × 340.29 m/s SOS (closes within 0.07 %) |
| Peak G-load | 4.0 G | VG sustained; closes via a = v²/(2L) within 1 % |
| Run time in tube | 43.5 s | Derived: t = v/(a·g₀) |
| Drive architecture | Linear Synchronous Motor (LSM) coilgun | TR-V2, McNab review |
| Drive coil material | Copper (C10100, OFHC) | TR-V2 |
| Vehicle armature | REBCO superconducting (vehicle-mounted) | TR-V2 |
| Armature temperature | 20 K | TR-V2 (LH₂ cryogenic) |
| Coil count | 7,400 (at 5 m spacing) | Derived |
| Peak field | 8 T | TR-V2 |
| Energy storage (SMES) | 580 GJ | Provisional (½·m·v² @ 60 % eff) |
| Peak power | 39 GW | Carry-forward |
| Charge rate | 650 MW | Provisional |
| Charge time | 15 min | Derived (580 GJ / 650 MW) |
| **Muzzle seal** | **Liquid Hydrogen (LH₂) cryogenic membrane** | VacuumGate v1.0 §1, §3 |
| Muzzle LH₂ temperature | 20 K (-253 °C) | VacuumGate |
| Muzzle stagnation pressure | 1.77 MPa | VacuumGate §2.3 (Mach 5 at SL) |
| Wing deploy time | 3 s | Patent envelope ≤5 s |
| Cost (infrastructure) | $85-120 B | VacuumGate §2.7 |
| Cost (per kg LEO) | $1,025/kg | TR-V2 (vs. $2,720 Falcon 9) |
| Development timeline | 13 years | TR-V2 Shotwell integration |

All values within Patent BGKPJR-001 claim envelope (Mach 3-5, 15-45°, 0.05-0.20 atm, ≤5 G, wing deploy ≤5 s).

## What changed from prior baselines

| Parameter | Pre-VG (launch.ts) | VG canonical | Why |
|---|---|---|---|
| Tube length | 28.7 km | **37 km** | 28.7 km did not close kinematically with claimed velocity & G |
| Exit Mach | 3.5 | **5.0** | More energetic, still within patent; reduces propellant fraction further |
| Exit velocity | 1,190 m/s | **1,700 m/s** | Mach 5 at SL |
| Peak G | 3.9 G (unclosed) | **4.0 G** | Closes within 1% via a = v²/(2L) |
| Run time | 23 s (impossible) | **43.5 s** | Derived from v/a |
| Tube pressure | 0.1 atm | **0.05 atm** | At patent envelope minimum |
| Drive architecture | "NbTi superconducting coils" | **LSM coilgun, copper drive + REBCO armature** | McNab review (railgun→coilgun); HTS armature |
| Operating temp | 4.2 K (NbTi rail) | **20 K (REBCO armature on vehicle)** | Coilgun puts cryogenics on vehicle, not rail |
| Muzzle seal | Thermite membrane | **LH₂ cryogenic membrane** | VG novel IP — controlled detonation as thrust impulse |
| Energy stored | 900 MJ | **580 GJ** | Was off by ~600× (probably typo); 580 GJ matches kinetic energy of full-mass vehicle |
| Cost target | $200/kg | **$1,025/kg LEO** | TR-V2 integrated cost |
| Propellant reduction | 40% (claimed) | **18%** (1,700 / 9,400 m/s rail Δv) | Honest accounting |

## What's still PROVISIONAL

These values are best estimates pending Scott Lukens (Sr. Systems Engineer, Victory Solutions Inc., NASA Marshall contractor) validation:

- **Gryphon dry mass: 50,000 kg.** Three values exist across docs (8.2 t / 15 t / 241 t). 50 t is the VG-implicit baseline; Shotwell integration analysis suggested 93.8 t dry / 241 t gross liftoff. Lukens to validate.
- **Manna cargo pod variants (H, I, B):** internalG values reconciled to 4 G rail baseline, but the cargo class definitions and recovery modes need engineering review.
- **Peak power 39 GW / charge rate 650 MW:** carried forward from prior baseline; not yet validated against the larger 580 GJ storage requirement.
- **VacuumGate's 0.001 atm vacuum target:** sits *outside* the 0.05-0.20 atm patent envelope. Canonical sits at 0.05 atm (within patent). Achieving 0.001 atm would require a patent continuation-in-part filing.
- **Solar sail dynamics:** module not yet implemented in `BGKPJR-Core-Simulations`. Constants are correct; trajectory model is a gap.
- **Pod stress models:** not implemented; cargo pod g-loading claims need structural analysis.

## What's frozen and what's open

**Frozen** (changes require an architectural review):
- Three-stage hybrid architecture (rail + Gryphon wing + Kepler sail)
- LSM coilgun, NOT railgun (per McNab review)
- LH₂ cryogenic muzzle membrane (the novel patent-worthy IP)
- Patent BGKPJR-001 claim envelope as legal boundary

**Open** (subject to optimization):
- Specific operating point within patent envelope (currently chosen: max Mach, max efficiency)
- Vehicle mass breakdown
- Power/storage architecture details
- Cargo pod taxonomy
- Phasing (Phase 0 demonstrator → Phase 1 cargo → Phase 2 crew)

## How to keep both repos in lock-step

The Python source-of-truth lives at:
```
BGKPJR-Core-Simulations/simulation/src/bgkpjr_dimensions.py
```

To verify all cross-checks close:
```bash
cd BGKPJR-Core-Simulations
python -m simulation.src.bgkpjr_dimensions
```

Expected output: `✓ All cross-checks pass within 1.0% tolerance.`

The TypeScript mirror at `BGKPJR-Launch-Vis/src/data/launch.ts` carries the same values. To export a JSON dump suitable for round-trip mirror:
```bash
python -m simulation.src.bgkpjr_dimensions --json
```

Whenever a canonical value changes, both files must be updated together. CI should call `derive_check()` on every commit.

## Forward path

1. **Send to Lukens.** Send him this document, the audit, and the pre-VG → VG diff. Ask him: "Which provisional values would you like us to nail down first? Where do you push back on the architecture?"
2. **Receive Lukens's edits.** Update bgkpjr_dimensions.py with whatever he validates. Re-run derive_check.
3. **Build engineering drawings.** Orthographic projections (top, side, end, cross-section) of the tube + breech + LH₂ muzzle interface, dimensioned, scale-bar called out, derived from canonical numbers.
4. **Send drawings to Lukens (visual-only pass).** His working style is visual-first. Let him reverse-engineer the math from the diagrams.
5. **Iterate on his catches.** Whatever he flags, fix in the source of truth and regenerate everything.
6. **Then write the concept paper** (NIAC Phase I format).

---

*— Reconciliation completed 2026-04-30 by Claude Opus 4.7 (1M context), invoked by Shane Brazelton (thebardchat). Forward-facing materials updated to reflect VG canonical baseline. Pending Lukens validation before any submission to NASA Marshall.*
