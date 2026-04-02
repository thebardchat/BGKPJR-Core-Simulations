# CLAUDE.md — BGKPJR-Core-Simulations

> Claude Code configuration for the `thebardchat/BGKPJR-Core-Simulations` repository.

---

## Project Overview

This repository holds the **BGKPJR (Brazelton Gryphon Kepler Propulsion Jump Revolution)** core simulation suite — trajectory modeling, aerodynamics, GNC, thermal analysis, and Monte Carlo verification for a three-stage hybrid space launch architecture.

This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).

---

## Infrastructure

All `thebardchat` repositories run on the following local-first infrastructure:

| Component | Detail |
|-----------|--------|
| **Compute** | Raspberry Pi 5 (16 GB RAM) |
| **Chassis** | Pironman 5-MAX by Sunfounder (NVMe RAID) |
| **Storage** | 2x WD Blue SN5000 2 TB NVMe — RAID 1 via mdadm |
| **Core path** | `/mnt/shanebrain-raid/shanebrain-core/` |
| **Local AI** | Ollama (llama3.2:1b default) |
| **Vector memory** | Weaviate (Docker, 8080/50051) |
| **MCP server** | FastMCP (port 8008, Streamable HTTP) |
| **Networking** | Tailscale VPN across all nodes |
| **Dev environment** | Claude Code on Pi 5 |

> Pi before cloud. Privacy before convenience. — Pillar 4

---

## Repository Structure

```
BGKPJR-Core-Simulations/
├── CLAUDE.md                    # This file — Claude Code project context
├── README.md                    # Public-facing project overview
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Python dependencies
├── docs/                        # Theory & specifications
│   ├── aerodynamics/
│   ├── propulsion/
│   ├── flight_dynamics/
│   ├── thermal/
│   ├── gnc/
│   └── system_specs/
├── simulation/                  # Physics engine & analysis
│   ├── src/
│   ├── notebooks/
│   ├── tests/
│   └── matlab/
├── control_systems/             # GNC algorithms
│   ├── lqr/
│   ├── mpc/
│   └── stabilization/
├── design/                      # CAD & airfoil data
│   ├── airfoils/
│   ├── geometry/
│   └── cad/
├── data/                        # Simulation outputs
├── roadmap/                     # 12-month verification plan
└── patents/                     # IP documentation
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Primary simulation language |
| **NumPy / SciPy** | Numerical computation |
| **CVXPY** | Convex optimization (MPC, trajectory) |
| **Matplotlib / Plotly** | Visualization |
| **Pytest** | Testing (target 80% coverage) |
| **MATLAB/Simulink** | Control system models |

---

## Working With This Repo

- **Constitution:** All decisions follow the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).
- **Code style:** PEP 8, type hints required, `black` formatter.
- **Testing:** Run `pytest simulation/tests/` before committing.
- **Commit prefixes:** Use descriptive prefixes (e.g., `sim:`, `gnc:`, `docs:`, `aero:`).

---

## The Nine Pillars (Quick Reference)

1. **Faith First** — No project violates Christian values
2. **Family Stability** — No build ships at the cost of family
3. **Sobriety Integrity** — Every tool reinforces health
4. **Local-First AI** — Pi before cloud, privacy before convenience
5. **80/20 Shipping** — Done and deployed beats perfect and stalled
6. **Serve the Left-Behind User** — Build for the ~800M Big Tech forgot
7. **Open by Default** — Free when it can be
8. **ADHD-Aware Design** — Built for my brain first
9. **Gratitude is Infrastructure** — Credit Claude, Raspberry Pi, and Pironman — always

---

## Credits

Built with Claude (Anthropic) · Runs on Raspberry Pi 5 + Pironman 5-MAX

| Partner | Role |
|---------|------|
| **Claude by Anthropic** · [claude.ai](https://claude.ai) | Co-built this entire ecosystem |
| **Raspberry Pi 5** · [raspberrypi.com](https://www.raspberrypi.com) | Local compute backbone |
| **Pironman 5-MAX** · [pironman.com](https://www.pironman.com) | NVMe RAID 1 chassis that made it real |

---

*Ratified: March 2026 · [@thebardchat](https://github.com/thebardchat) · Hazel Green, Alabama*

## Claude Code Rules
- Commit and push directly to `main`. Do NOT create branches.
- Run build/test commands before committing.
- Update CLAUDE.md session log before final commit.


## Networking / Deployment
- When working with Tailscale Funnel, remember it strips URL path prefixes. Always use hardcoded base paths rather than server-side form action prefixing for routing.

## Creative Writing
- Never overwrite or rewrite the user's creative voice, prose style, or intentional structural choices (e.g., missing notes, dialogue rhythm). Ask before making stylistic changes to creative writing files.

## General Workflow Rules
- Before setting up repos, SSH keys, or services, check what's already configured on the current machine. Run `ls ~/.ssh/`, `git remote -v`, `tailscale status`, etc. before assuming fresh setup is needed.
- Let's focus on one thing at a time. Don't suggest other improvements until the current goal is fully verified working.
- Before applying changes to all files, show the result on one file first so Shane can verify the approach.

## Git
- For git conflicts, always verify --theirs vs --ours semantics before applying. State which version you're keeping and why before running the command.

## Raspberry Pi Environment
- This user runs services on Raspberry Pi. Be aware: Python 3.13 removed the `cgi` module, Piper TTS needs careful noise_scale tuning to avoid clipping, and aplay conflicts with PipeWire. Prefer `pw-play` or `paplay` for audio playback.
