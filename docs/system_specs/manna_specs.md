# MANNA Supply Pod Specifications

> **MANNA** — *Modular Aerospace Necessities & Nutrient Asset*
>
> The supply pod we literally shoot into space.

**Companion repository:** [thebardchat/manna](https://github.com/thebardchat/manna)

---

## Overview

MANNA is the BGKPJR architecture's dedicated resupply payload — a modular,
maglev-launched cargo capsule for delivering necessities (food, water, parts,
experiments) to orbital stations and beyond.

The name draws from Exodus 16: provision delivered from above, on time, in
the measure that's needed. Faith First (Pillar 1) — even the cargo bay tells
the story.

## Naming

| Letter | Word |
|--------|------|
| **M** | Modular |
| **A** | Aerospace |
| **N** | Necessities |
| **N** | & Nutrient |
| **A** | Asset |

## Role in the BGKPJR Stack

| Stage | Vehicle | MANNA Interface |
|-------|---------|-----------------|
| 1 — Maglev Jump | Track | MANNA rides inside Gryphon's payload bay (50 m³) |
| 2 — Atmospheric Ascent | Gryphon | Carried as payload (≤ 5,000 kg to LEO) |
| 3 — Orbital Insertion | Kepler / RCS | MANNA separates and rendezvous-docks with destination |

## Cross-Repository Boundary

Detailed specs (mass budgets, docking interfaces, thermal envelope, life-cycle
analysis) live in **[thebardchat/manna](https://github.com/thebardchat/manna)**.

This file exists in BGKPJR-Core-Simulations only to:

1. Reserve the name and acronym
2. Document the integration point with Gryphon's payload bay
3. Link forward to the canonical MANNA repo

---

*Part of the [ShaneBrain Ecosystem](https://github.com/thebardchat) · Built under the [Constitution](https://github.com/thebardchat/constitution)*
