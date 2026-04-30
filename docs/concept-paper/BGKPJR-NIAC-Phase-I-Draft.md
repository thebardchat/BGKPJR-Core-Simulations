# BGKPJR — NIAC Phase I Concept Paper (DRAFT)

**Title:** *Brazelton-Gryphon-Kepler Propulsion Jump Revolution (BGKPJR): A Vacuum-Sealed Maglev Tunnel and Liquid-Hydrogen Cryogenic Membrane for Cost-Reduced Cargo-to-Lunar-Surface Delivery*

**Principal Investigator:** Shane Brazelton, Independent Researcher · Hazel Green, AL · `thebardchat@github`
**Technical Advisor (Pending Confirmation):** Scott Lukens, Senior Systems Engineer, Victory Solutions Inc., NASA Marshall Space Flight Center contractor, Huntsville, AL
**Document Version:** Draft v0.1
**Draft Date:** 2026-04-30
**Document Provenance:** Reconciled to canonical source-of-truth `bgkpjr_dimensions.py` (VacuumGate Feasibility Report v1.0, April 18 2026)
**Patent Reference:** BGKPJR-001 (filed April 18, 2025, Inventor: Shane Brazelton)

---

> ⚠️ **DRAFT STATUS.** This document is a Phase I scaffolding draft. Sections marked `[VALIDATED]` close to ±1 % against the canonical SoT. Sections marked `[PROVISIONAL]` are best estimates pending Lukens validation. Sections marked `[GAP]` are known holes the Phase I work plan is designed to close. No section is yet peer-reviewed. The six "expert reviews" in `expert-reviews/` are explicitly AI-generated synthetic critiques, not independent peer review. This paper is for review feedback before formal NIAC submission.

---

## 1. ABSTRACT (250 words)

The BGKPJR concept is a 37 km vacuum-sealed Linear Synchronous Motor (LSM) coilgun that accelerates unmanned cargo pods from sea level to Mach 5 (1,700 m/s) under 4 G sustained acceleration, providing 18 % of the Δv required to reach low Earth orbit. A novel liquid-hydrogen (LH₂) cryogenic membrane seals the tube muzzle and, on vehicle breach, undergoes a controlled detonation in the atmospheric wake to provide an additional ~50 m/s thrust impulse. Pods completing onboard rocket boost reach circular LEO at 7,670 m/s, where they are captured by a permanent in-space tug for trans-lunar transfer to a lander (Blue Moon Mark 2 / SpaceX HLS) for surface delivery. Empty pods become regolith-filled radiation-proof structural units in a permanent lunar base.

The concept positions BGKPJR as the missing link in the Space Pipeline: while NASA Artemis flies crew on a 10-month cadence and Blue Origin / SpaceX deliver landers and ISRU refueling, no architecture currently delivers cargo to LEO at a price compatible with sustained lunar operations. Target: $1,025/kg LEO at 21–50 launches/year, against $2,720/kg Falcon 9. Total infrastructure: $85–120 B over 7–9 years to operational cargo (2026 program start, 2033–2035 first cargo delivery).

This Phase I will: (1) close trajectory analysis for cargo pods through the muzzle interface, (2) perform muzzle-architecture trade study (LH₂ vs. thermite), (3) deliver a subscale demonstration of sequential coil firing on a moving armature, and (4) produce a Phase II preliminary design ready for downselect.

## 2. RELEVANCE TO NASA STRATEGIC PLAN

NASA's Moon to Mars Architecture (2024) identifies sustained lunar surface operations as the foundational stepping stone to Mars. Sustained operations require **continuous, affordable cargo delivery** that current launch vehicles do not provide at scale: Falcon 9 at $2,720/kg LEO is the floor of conventional chemical launch; Starship promises lower per-kg but at low cadence and with significant orbital refueling complexity. The CLPS lunar lander program currently operates at ~$1.2 M/kg to lunar surface — an unsustainable cost-per-kg for sustained base operations.

BGKPJR addresses this gap with a ground-based electromagnetic accelerator that:

1. Eliminates the first-stage propellant fraction for cargo missions (rail provides the first 1,700 m/s)
2. Supports launch cadences (~50/year mature) that conventional chemical launchers cannot match
3. Repurposes empty payload containers into structural elements via NASA's in-situ regolith-filling research, addressing the radiation-shielding mass problem that limits surface habitation

The concept is **distinct from prior art** (StarTram, Sandia maglev studies, Slough plasma armature) by its vacuum-sealed-tube + cryogenic-membrane architecture, which trades a hard atmospheric-exit transition for a cleaner vacuum-to-atmosphere event with simultaneous thrust augmentation.

## 3. TECHNICAL DESCRIPTION

### 3.1 Architecture Overview `[VALIDATED]`

| Subsystem | Spec | SoT field |
|---|---|---|
| Tube length | 37,000 m | `RAIL.LENGTH_M` |
| Tube bore | 10.0 m diameter | `RAIL.DIAMETER_M` |
| Inclination | 15° (within patent envelope 15–45°) | `RAIL.INCLINATION_DEG` |
| Tube pressure | 0.05 atm (within patent 0.05–0.20) | `RAIL.TUBE_PRESSURE_ATM` |
| Exit velocity | 1,700 m/s (Mach 5 at sea level) | `RAIL.EXIT_VELOCITY_MS` |
| Sustained G | 4.0 G (within patent ≤5 G) | `RAIL.PEAK_G` |
| Run time | 43.5 s (derived: t = v / a) | derived |
| Drive | LSM coilgun, copper drive coils, REBCO armature on vehicle | `RAIL.DRIVE_TYPE` |
| Coils | 7,400 at 5 m spacing, 8 T peak field | derived + `RAIL.COIL_*` |
| Stored energy | 580 GJ in SMES at 60% drive efficiency | `RAIL.SMES_CAPACITY_GJ` |
| Peak power | 39 GW | `RAIL.PEAK_POWER_GW` |

All values close internally within 1 % via `derive_check()`. All values within Patent BGKPJR-001 claim envelope.

### 3.2 The Muzzle Interface — Two Alternatives Under Trade Study `[PROVISIONAL]`

The single most-load-bearing engineering decision is the muzzle membrane. The vehicle transitions from 0.05 atm vacuum into ~1 atm atmosphere in milliseconds; dynamic pressure at exit is 1.77 MPa. Two parallel architectures are under study; trade study deliverable in Phase 0:

**Alternative A — Liquid Hydrogen (LH₂) Cryogenic Membrane (current canonical)**
- Thin LH₂ membrane (20 K) sealed behind structural diaphragm + aerogel buffer
- Vehicle breach: LH₂ flashes to gas (~1000× volume expansion), mixes stoichiometrically with O₂ in wake, detonates from plasma-temperature ignition
- Detonation geometry directs impulse forward → ~50 m/s controlled thrust boost
- Reset time per launch: ~30 min (LH₂ refill)
- Novel patent-worthy IP; central engineering risk is detonation control

**Alternative B — Thermite (Al/Fe₂O₃) Three-Layer Membrane**
- L1 thermite + L2 aerogel buffer + L3 structural diaphragm
- Vehicle breach: WC tip contact ignites thermite in <50 μs; self-consuming reaction creates plasma aperture; vehicle passes through
- No thrust gain (detonation contained, not directed)
- Reset time per launch: ~8 min
- Known reaction chemistry; lower IP novelty but lower engineering risk

### 3.3 Mission Profile (Cargo Pipeline) `[VALIDATED — kinematics]`, `[PROVISIONAL — mass/power]`

```
Stage 1: Earth surface → tube exit
         t = 43.5 s · 0 → 1,700 m/s · 4 G sustained · 37 km

Stage 2: Tube exit → LEO
         Pod 2nd-stage rocket: +5,970 m/s
         Final: 7,670 m/s circular at 400 km · ~9 min

Stage 3: LEO catch by Space Tug
         Closing burn ~0.05 km/s · ~8 min rendezvous

Stage 4: TLI burn (Tug)
         ~4.10 km/s from circular LEO · ~8 min
         Lunar transit · ~3.2 days

Stage 5: Pod release in lunar orbit
         Hand-off to Blue Moon Mk2 / SpaceX HLS lander

Stage 6: Lander descent + surface delivery
         Empty pod → regolith-filled structural unit (NASA ISRU concept)
```

### 3.4 Vehicle: Manna Cargo Pod `[PROVISIONAL — mass]`

- Common chassis: 1.8 m diameter, ~4.5 m length, 800 kg dry, ~3,200 kg gross with payload
- Three operational variants: Manna-H (Hardened, no isolation), Manna-I (Isolated, passive shock-mount), Manna-B (Biological, double-cushioned + active TCS)
- Differentiation: internal cushioning, cargo class, recovery mode
- All variants share canonical 4 G external rail acceleration

### 3.5 The Space Tug `[PROVISIONAL]`

- Permanent in-space transfer vehicle: ~5,000 kg dry, ~25,000 kg propellant (LH₂/LOX, ISRU compatible)
- Δv per refuel: 4,500 m/s (covers LEO → lunar orbit + return + station-keep)
- Design lifetime: 50 cycles refurbishable
- Refuel: Manna-F propellant pods from Earth initially; lunar ISRU water long-term

## 4. KEY INNOVATIONS

1. **Vacuum-sealed muzzle with LH₂ cryogenic membrane** — Novel solution to the atmospheric-exit shock problem that has historically constrained electromagnetic launch concepts. By relocating the vacuum/atmosphere transition into a controlled cryogenic phase change, both the structural shock and the propellant-augmentation opportunity are simultaneously addressed. Patent claim envelope under BGKPJR-001.

2. **Hybrid rail + onboard rocket architecture** — Pure ground-based EM launch to orbital velocity is geometrically infeasible (would require ~1,000 km tube at human-rated G). BGKPJR honestly partitions the Δv: 18 % from rail, 82 % from onboard rocket and Tug. This eliminates the StarTram-class atmospheric-exit problem by exiting at survivable Mach 5, not Mach 25.

3. **Pod-to-structure repurposing** — Empty cargo pods are designed for regolith-fill end-of-life, leveraging NASA's published in-situ resource utilization research. Every kilogram delivered becomes a kilogram of radiation-shielding base structure.

4. **Space Pipeline integration** — BGKPJR is designed as the cargo lifeline within an existing ecosystem (Blue Origin landers, SpaceX HLS, NASA Artemis, ISRU), not as a standalone moonshot. This dramatically reduces program risk by depending on infrastructure others are already building.

## 5. WHAT WE WILL PROVE IN PHASE I

Phase I (9 months, target $175 K) deliverables:

### 5.1 Trajectory Closure Analysis `[GAP — PRIMARY DELIVERABLE]`
Currently the simulation stack does not have an end-to-end trajectory simulation that closes from rail exit through LEO insertion. Phase I will deliver a 6-DOF trajectory simulation in Python (extending the existing `BGKPJR-Core-Simulations` framework) that:
- Integrates from rail exit through atmospheric ascent, second-stage burn, and LEO circularization
- Validates payload-to-orbit at the claimed 4 G / Mach 5 rail conditions
- Accounts for atmospheric loads at the Mach 5 exit (the hardest critique to anticipate)

### 5.2 Muzzle Architecture Trade Study `[PROVISIONAL → VALIDATED]`
Quantitative comparison of LH₂ vs. thermite muzzle alternatives:
- Detonation modeling for LH₂ (analytical + literature-based)
- Per-launch cost amortization including infrastructure
- FMEA for both alternatives
- Recommendation with documented rationale

### 5.3 Subscale Coil Firing Demonstration `[GAP — DEMONSTRATION]`
Working with Marshall propulsion test facilities (via Lukens / Victory Solutions), a 1:100 scale subsection demonstration:
- 10 m of representative LSM coilgun
- Sequential coil firing controller
- Moving armature instrumented for force / position
- Goal: TRL-3 graduation for the LSM core architecture

### 5.4 Cost Model `[PROVISIONAL → REFINED]`
Bottom-up cost analysis:
- Capital cost (tube structure, coil array, SMES, vacuum infrastructure)
- Operating cost per launch (energy, consumables, refurbishment)
- Revenue model (cargo at $1,025/kg LEO)
- Break-even cadence analysis

### 5.5 Path to Phase II
Phase II ($600 K, 2 years) will:
- Full preliminary design of the operational system
- Larger (1:10) scale subsection demonstration
- Real-world site selection study (geology, grid interconnect, regulatory)

## 6. RISKS AND CHALLENGES

| # | Risk | Severity | Phase I mitigation |
|---|---|---|---|
| 1 | Atmospheric exit aero loads at Mach 5 destroy vehicle | High | Trajectory simulation + analytical shock loading; pre-empt the hardest critique |
| 2 | LH₂ membrane detonation control fails (Hindenburg mode) | High | Analytical detonation modeling; trade study with thermite as fallback |
| 3 | 580 GJ SMES technology not at TRL for required peak power 39 GW | High | Document trade space; consider distributed flywheel + capacitor hybrid |
| 4 | 37 km tube alignment over LIGO-class precision | Medium | Document civil engineering challenge; defer detailed design to Phase II |
| 5 | Patent claim envelope for VG aspirational 0.001 atm vacuum requires CIP filing | Low | Operate canonical at 0.05 atm (within patent); pursue CIP separately |
| 6 | Pod stress models not yet implemented | Medium | Phase I deliverable (Section 5.1) |
| 7 | Real peer review absent (synthetic only) | High | Lukens engagement during Phase I; AIAA paper submission as further peer review |

## 7. TEAM

**Principal Investigator:** Shane Brazelton (Independent Researcher; Concrete Dispatch Operator + Self-Taught Aerospace Architect; Hazel Green, AL). Patent BGKPJR-001 inventor. Built the existing simulation suite and architecture documentation.

**Technical Advisor:** Scott Lukens (Senior Systems Engineer, Victory Solutions Inc., Huntsville AL). NASA Marshall Space Flight Center contractor with experience in launch vehicle systems, propulsion, mission operations. Has reviewed the BGKPJR concept and assessed it as "high probability rate" of feasibility.

**Tooling:** All simulation, design, and documentation work performed in collaboration with Claude (Anthropic) AI as a force multiplier. The entire BGKPJR concept-development environment is publicly visible in `BGKPJR-Core-Simulations` and `BGKPJR-Launch-Vis` repositories under `thebardchat` on GitHub. This represents a genuine demonstration of solo + AI aerospace concept development at a level that historically required institutional teams.

## 8. RELATIONSHIP TO PRIOR ART

| Concept | Year | Architecture | Distinction from BGKPJR |
|---|---|---|---|
| StarTram (Powell, Maise) | 2001–2012 | Maglev to LEO directly | StarTram targets orbital velocity from rail; BGKPJR honestly partitions Δv |
| Sandia maglev launch studies | 1990s–2000s | Various coilgun configs | Sandia did not address muzzle interface; BGKPJR's LH₂ membrane is novel |
| Slough plasma armature | 2000s | Plasma-current armature | BGKPJR uses solid REBCO armature; different physics regime |
| AFRL railgun studies | 2010s | EM launch for projectiles | Munitions-class G; not human-cargo-rated; BGKPJR sustained 4 G |
| LLNL coilgun (1992) | 1992 | Coilgun feasibility | Established physics base; BGKPJR scales to human-rated and adds cryogenic muzzle IP |

## 9. WHAT THIS PAPER DOES *NOT* CLAIM

In keeping with the dimensional-integrity discipline that drove the 2026-04-30 baseline reconciliation:

- **We do not claim to have a working system.** We have a concept paper, a simulation suite that closes within 1 %, and a public patent filing.
- **We do not claim independent peer review.** The "expert reviews" in our repository are AI-generated synthetic critiques. Lukens (named above) has provided informal favorable feedback but has not yet performed formal review.
- **We do not claim the costs are validated.** $1,025/kg LEO is a target derived from the integrated Shotwell-style mass budget; actual cost will depend on Phase II–III preliminary design.
- **We do not claim the muzzle architecture is selected.** LH₂ is canonical; thermite is alternative; trade study deliverable in Phase 0/I.
- **We do not claim Mach 5 exit aero loads are solved.** Atmospheric exit is the hardest open critique; closing it is a Phase I deliverable.

These honest acknowledgments are deliberate. Pre-Phase A concepts that hide their gaps fail review on first contact. We document our gaps publicly to invite the level of technical scrutiny that ladders the concept up.

## 10. APPENDIX — REFERENCED ARTIFACTS

| Artifact | Location |
|---|---|
| Canonical source-of-truth | `BGKPJR-Core-Simulations/simulation/src/bgkpjr_dimensions.py` |
| Decision record | `BGKPJR-Core-Simulations/CANONICAL-BASELINE.md` |
| Pre-Lukens audit | `BGKPJR-Core-Simulations/expert-reviews/PRE-LUKENS-AUDIT-2026-04-30.md` |
| VacuumGate Feasibility Report v1.0 | `BGKPJR-Core-Simulations/docs/BGKPJR-VacuumGate-Feasibility-Report.md` |
| Orthographic engineering drawing | `BGKPJR-Core-Simulations/design/engineering-drawings/tube-orthographic.svg` |
| Patent BGKPJR-001 abstract | `BGKPJR-Core-Simulations/patents/BGKPJR-001-abstract.md` |
| Public visualization site | `https://thebardchat.github.io/BGKPJR-Launch-Vis` |
| Project ecosystem | `https://github.com/thebardchat` |

---

*Draft prepared by Shane Brazelton with Claude Opus 4.7 (1M context). Prepared for review by Scott Lukens, Victory Solutions Inc., before NASA NIAC Phase I submission. All values traceable to canonical source-of-truth. Honest about gaps. Game time.*
