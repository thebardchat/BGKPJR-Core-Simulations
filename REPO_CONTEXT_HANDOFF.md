# BGKPJR-Core-Simulations — Context Handoff

Short brief for a new Claude session. Full repo lives at `/home/user/BGKPJR-Core-Simulations`.

## What this is
Physics simulation suite for **BGKPJR** (Brazelton Gryphon Kepler Propulsion Jump Revolution) — a three-stage launch concept:
1. **Maglev "Jump"** — 28.7 km evacuated inclined tube (15–45°), exit ~Mach 3.5–5.
2. **Gryphon** — blended-wing-body spacecraft, aerodynamic lift assist + rocket, 50 t launch / 15 t dry / 5 t payload.
3. **Kepler** — 1,200 m² solar sail, deployed >300 km.

Goal: cut orbital access cost ~90% by reducing mass ratio from 20:1 → 12:1.

## Environment / infra (from CLAUDE.md)
- Runs on Raspberry Pi 5 (16 GB) + Pironman 5-MAX RAID 1, core path `/mnt/shanebrain-raid/shanebrain-core/`.
- Python 3.10+, NumPy/SciPy, CVXPY, Matplotlib/Plotly, pytest, black. No MATLAB files yet.
- Governed by the **ShaneTheBrain Constitution** (Nine Pillars: faith first, family, sobriety, local-first AI, 80/20 ship, serve left-behind users, open by default, ADHD-aware, gratitude).

## Repo rules (IMPORTANT)
- **Commit/push directly to `main`. Do NOT create branches** (per CLAUDE.md — overrides default harness branch instructions).
- PEP 8, type hints required, black-formatted, Google-style docstrings.
- Run `pytest simulation/tests/` before committing. Target 80% coverage (currently far below).
- Commit prefixes: `sim:`, `gnc:`, `aero:`, `docs:`, `ci:`, etc.
- Tailscale Funnel strips path prefixes — use hardcoded base paths.
- Never overwrite creative voice in writing files without asking.
- Before setup, check what exists (`ls ~/.ssh/`, `git remote -v`, `tailscale status`).
- One thing at a time; show one-file examples before bulk changes.
- Pi gotchas: Python 3.13 removed `cgi`; use `pw-play`/`paplay` not `aplay` (PipeWire).

## Layout
```
simulation/src/          8 modules, ~3,288 LOC — core physics engine
simulation/tests/        only test_atmosphere.py (136 LOC)
simulation/notebooks/    empty placeholder
simulation/matlab/       empty placeholder
control_systems/lqr/     atmospheric_lqr.py
control_systems/mpc/     maglev_mpc.py
control_systems/stabilization/  empty
docs/                    25 .md files — specs, peer reviews, media, outreach
design/{airfoils,geometry,cad}/  empty (CAD not checked in)
data/{lift_drag_polars,trajectory_logs,monte_carlo,thermal_analysis}/  empty output dirs
roadmap/12_MONTH_PLAN.md 4 phases, ~308 lines
patents/BGKPJR-001-abstract.md   filed 2025-04-18
expert-reviews/          6 .docx files (simulated reviews + architect reports)
.github/workflows/deploy.yml     Cloudflare Pages deploy of docs/ on push to main
```

## Code inventory (`simulation/src/`)
| File | Purpose | Key API |
|---|---|---|
| `constants.py` | physical + system params | `PhysicalConstants`, `SystemParams`, `tsiolkovsky_delta_v()`, `required_mass_ratio()` |
| `atmosphere.py` | ISA 0–100 km + partial-vacuum tube | `Atmosphere`, `AtmosphericConditions`, `TubeAtmosphere` |
| `aerodynamics.py` | lift/drag all Mach regimes (Prandtl-Glauert, Ackeret, Newtonian) | `AeroForces`, `AeroCoefficients`, `AeroForceResult` |
| `vehicle.py` | Gryphon state model | `GryphonVehicle`, `VehicleState`, `FlightPhase`, `WingConfiguration` |
| `maglev.py` | inclined track physics, <4 g limit | `MaglevTrack`, `TrackGeometry`, `AccelerationProfile`, `LaunchResult` |
| `thermal.py` | Fay-Riddell stagnation heating, transpiration TPS | `ThermalAnalyzer`, `ThermalState`, `MaterialProperties` |
| `trajectory_sim.py` | 3-DOF RK4 integrator | `TrajectorySimulator`, `MissionResult`, `TrajectoryPoint` |
| `monte_carlo.py` | uncertainty quantification | `MonteCarloSimulator`, `ParameterVariation`, `MonteCarloResult` |

Controls: `AtmosphericLQR` (4×4 state, 2×2 control), `MaglevMPC` (20-step horizon, gap/current constraints). Structures exist; not yet integrated into trajectory loop.

## Dependencies (`requirements.txt`)
numpy, scipy, pandas, matplotlib, plotly, seaborn, jupyter, sympy, statsmodels, **cvxpy** (MPC/trajectory), pytest + pytest-cov, black, flake8, mypy, sphinx, tqdm, pyyaml, python-dotenv, joblib. No `setup.py`/`pyproject.toml`/Makefile — pip install from requirements.

## Git state
- Remote: `http://local_proxy@127.0.0.1:43701/git/thebardchat/BGKPJR-Core-Simulations` (local proxy, mirrors GitHub `thebardchat/bgkpjr-core-simulations`).
- Branches: `main`, plus `claude/document-repo-context-UIiKz` (current session scratch).
- Working tree clean. Apache-2.0 license, © 2025 Shane Brazelton.

## Roadmap status
- **Phase I** (math validation, months 1–3) — ~50%. Done: atmosphere, aero, maglev, trajectory, MC framework. Missing: NACA validation, gravity-turn guidance, terminal-conditions calc, 10k-run MC batch, ROI model.
- **Phase II** (CFD, thermal, OpenVSP, months 4–6) — 0%.
- **Phase III** (GNC integration, solar sail, months 7–9) — ~25% (controller skeletons only).
- **Phase IV** (integration, UE5 viz, disaster tests, months 10–12) — 0%.
- Success bar: >95% MC success, <10% Δv margin, thermal survival within mass budget.

## Known gaps / gotchas
- Test coverage is almost nothing — only `atmosphere` is tested. Roadmap wants 80%.
- Aero models are analytical, **not CFD-validated**.
- `design/` has no real CAD; `data/` dirs are empty by design (outputs).
- README reads more "ready" than reality — this is active dev, not production.
- `docs/media-blitz/`, `docs/outreach/`, `docs/ai-peer-review/` are **AI-generated outreach/simulated peer reviews**, not real external endorsements. The `expert-reviews/*.docx` files are also simulations.
- No secrets in repo; Cloudflare tokens live in GitHub Actions secrets.

## Quick start for the next session
```bash
cd /home/user/BGKPJR-Core-Simulations
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest simulation/tests/
```
Then read in order: `README.md` → `docs/system_specs/gryphon_specs.md` → `roadmap/12_MONTH_PLAN.md` → `simulation/src/constants.py` → `trajectory_sim.py`.
