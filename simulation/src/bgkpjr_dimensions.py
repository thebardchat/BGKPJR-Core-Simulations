"""
BGKPJR Canonical Dimensions Module — SINGLE SOURCE OF TRUTH
============================================================

This module is the canonical source of dimensional truth for the BGKPJR
program. Both `BGKPJR-Launch-Vis` (TypeScript public site) and
`BGKPJR-Core-Simulations` (Python sim/analysis stack) trace every
dimensional constant back here.

Reconciliation
--------------
Reconciled 2026-04-30 to align with the BGKPJR-VacuumGate Feasibility
Report v1.0 (April 18, 2026), which supersedes:
- Original BGKPJR Lead Architect Report v1 (April 2025)
- BGKPJR Technical Report v2 (April 2025)
- BGKPJR Technical Documentation v3.0 (April 2025)

The VacuumGate revision changes the rail baseline from 28.7 km / Mach 3.5 /
thermite membrane to 37 km / Mach 5 / liquid-hydrogen cryogenic membrane,
based on physics-honest analysis of:
- Track-length / G-force paradox (orbital from ground = 1,035 km, impossible)
- Atmospheric exit dynamic pressure (1.77 MPa at Mach 5 SL)
- Realistic infrastructure cost ($85-120B vs prior optimistic estimates)

All values within the BGKPJR-001 patent claim envelope (Mach 3-5, 15-45°,
≤5G, 0.05-0.2 atm).

Provenance Tags
---------------
Every constant carries one of these provenance labels in its comment:
  VG       — Direct from VacuumGate Feasibility Report v1.0
  PATENT   — From BGKPJR-001 patent claim envelope
  TR-V2    — Technical Report v2 (post-expert-review)
  DERIVED  — Computed from other canonical constants
  PROVISIONAL — Best estimate, awaiting Lukens validation

Validation
----------
Run `python -m simulation.src.bgkpjr_dimensions` to execute all
internal cross-checks. Returns 0 if all close within 1 % tolerance.
"""

import math

# ═══════════════════════════════════════════════════════════════════════
#  PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

G_EARTH = 9.80665              # m/s² standard gravity
EARTH_RADIUS_M = 6.371e6       # m mean equatorial radius
EARTH_MU = 3.986e14            # m³/s² gravitational parameter
MACH_1_SL = 340.29             # m/s, ICAO sea-level speed of sound
SOLAR_PRESSURE_1AU = 4.56e-6   # Pa solar radiation pressure at 1 AU
SOLAR_CONSTANT_1AU = 1361.0    # W/m²
ISA_P0 = 101325.0              # Pa standard atmosphere sea-level pressure
ISA_T0 = 288.15                # K standard atmosphere sea-level temperature
ISA_RHO0 = 1.225               # kg/m³ standard sea-level density

# ═══════════════════════════════════════════════════════════════════════
#  PATENT CLAIM ENVELOPE — BGKPJR-001 (filed April 18, 2025)
#  All canonical operating points MUST sit inside this envelope.
# ═══════════════════════════════════════════════════════════════════════

class PATENT:
    INCLINATION_DEG_MIN = 15.0   # PATENT
    INCLINATION_DEG_MAX = 45.0   # PATENT
    TUBE_PRESSURE_ATM_MIN = 0.05 # PATENT
    TUBE_PRESSURE_ATM_MAX = 0.20 # PATENT
    EXIT_MACH_MIN = 3.0          # PATENT
    EXIT_MACH_MAX = 5.0          # PATENT
    PEAK_G_MAX = 5.0             # PATENT (sustained, human-rated)
    WING_DEPLOY_SEC_MAX = 5.0    # PATENT

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 1 — RAIL: Vacuum-Sealed Maglev Tunnel (VacuumGate baseline)
# ═══════════════════════════════════════════════════════════════════════

class RAIL:
    # ── Geometry ──────────────────────────────────────────────────────
    LENGTH_KM = 37.0             # VG    (revised from 28.7 km)
    LENGTH_M = 37000.0           # DERIVED
    DIAMETER_M = 10.0            # VG    internal bore (vehicle clearance)
    INCLINATION_DEG = 15.0       # PATENT envelope; choose 15° for trajectory loft

    # ── Vacuum ────────────────────────────────────────────────────────
    # Canonical sits at patent envelope minimum (0.05 atm). VacuumGate Report
    # envisions 0.001 atm (10⁻³) as the engineering aspirational target; this
    # tighter vacuum sits OUTSIDE the BGKPJR-001 patent claim envelope and
    # would require a patent continuation-in-part to defend legally.
    TUBE_PRESSURE_ATM = 0.05         # PATENT envelope minimum
    TUBE_PRESSURE_PA = 5066.25       # DERIVED (0.05 × ISA_P0)
    TUBE_PRESSURE_ATM_VG_TARGET = 0.001  # VG aspirational (requires patent CIP)
    VACUUM_MAINTENANCE_MW_LOW = 50.0    # VG  pumping power range
    VACUUM_MAINTENANCE_MW_HIGH = 150.0  # VG

    # ── Kinematics (Mach 5 baseline; physics closes) ──────────────────
    EXIT_MACH = 5.0              # VG    revised from Mach 3.5
    EXIT_VELOCITY_MS = 1700.0    # VG    matches Mach 5 × MACH_1_SL within 0.07 %
    PEAK_G = 4.0                 # VG    sustained, within patent ≤5

    # ── Coilgun architecture (NOT railgun — corrected by McNab review) ─
    DRIVE_TYPE = "Linear Synchronous Motor (LSM) coilgun"  # TR-V2
    DRIVE_COIL_MATERIAL = "Copper (C10100, OFHC, actively cooled)"  # TR-V2
    ARMATURE_MATERIAL = "REBCO superconducting (vehicle-mounted)"   # TR-V2
    ARMATURE_TEMP_K = 20.0       # VG    cryogenic operating temperature
    COIL_INNER_DIAMETER_M = 16.0 # TR-V2
    COIL_OUTER_DIAMETER_M = 20.0 # TR-V2
    COIL_AXIAL_LENGTH_M = 2.0    # TR-V2
    COIL_TURNS = 50              # TR-V2
    COIL_SPACING_M = 5.0         # TR-V2 (λ/2 synchronization)
    COIL_PEAK_FIELD_T = 8.0      # TR-V2

    # ── Power (provisional pending Shotwell-style integration update) ─
    PEAK_POWER_GW = 39.0         # PROVISIONAL (carry-forward from prior baseline)
    SMES_CAPACITY_GJ = 580.0     # PROVISIONAL (½·m·v² @ 60 % eff for ~241t vehicle)
    CHARGE_RATE_MW = 650.0       # PROVISIONAL
    CHARGE_TIME_MIN = 15.0       # PROVISIONAL (revised from 4 min for 580 GJ)

    # ── Muzzle interface — TWO ALTERNATIVE ARCHITECTURES ─────────────
    # Per 2026-04-30 architectural decision: thermite and LH₂ membranes
    # are documented as two parallel alternatives, not one superseding the
    # other. Trade study to be performed (Phase 0).
    MUZZLE_STAGNATION_PRESSURE_MPA = 1.77   # VG  at Mach 5 sea-level
    MUZZLE_ALTERNATIVES = {
        "lh2": {
            "name": "Liquid Hydrogen (LH₂) Cryogenic Membrane",
            "membrane_temp_k": 20.0,        # VG  -253 °C
            "novel_ip": True,               # VG  controlled detonation = thrust boost
            "thrust_boost_dv_ms": 50.0,     # VG  estimated Δv from controlled detonation
            "reset_time_min": 30.0,         # LH₂ refill cycle
            "advantages": [
                "Novel patent-worthy IP (controlled detonation as thrust impulse)",
                "Acts as cryogenic heat sink during transit",
                "Aligns with VG vehicle LH₂ propellant supply",
            ],
            "disadvantages": [
                "Requires cryogenic infrastructure at muzzle (per launch)",
                "Detonation control is the central engineering risk",
                "Hindenburg-mode failure if detonation goes uncontrolled",
            ],
        },
        "thermite": {
            "name": "Thermite (Al/Fe₂O₃) Three-Layer Membrane",
            "ignition_velocity_ms": 1700.0,  # WC tip contact ignition
            "ignition_time_us": 50.0,        # microsecond combustion
            "peak_temperature_c": 2000.0,    # Al/Fe₂O₃ flame temp
            "novel_ip": False,               # known reaction, novel application
            "reset_time_min": 8.0,           # membrane swap cycle
            "advantages": [
                "Self-consuming: zero solid debris field after vehicle passes",
                "Faster reset between launches (~8 min vs 30 min for LH₂)",
                "No cryogenic infrastructure required at muzzle",
            ],
            "disadvantages": [
                "No thrust-impulse benefit (detonation contained, not directed)",
                "Pyrotechnic consumable cost per launch (~$2,400/seal)",
                "Plasma aperture flash exposes vehicle nose to 2,000 °C for 50 μs",
            ],
        },
    }
    # Canonical default (used by visualizations and primary mission profile)
    MUZZLE_DEFAULT = "lh2"
    MUZZLE_SEAL_TYPE = MUZZLE_ALTERNATIVES[MUZZLE_DEFAULT]["name"]
    MUZZLE_LH2_TEMP_K = MUZZLE_ALTERNATIVES["lh2"]["membrane_temp_k"]
    MUZZLE_CONTROLLED_DETONATION = True

# ═══════════════════════════════════════════════════════════════════════
#  PROGRAM PHASING — 2026-04-30 architectural decision
# ═══════════════════════════════════════════════════════════════════════
#
#  Two parallel programs share the same 37 km LSM rail infrastructure:
#
#    Phase 1 (CURRENT, 2026-2033)   : MANNA cargo pods + Space Tug
#                                      Unmanned resupply pipeline to Moon.
#                                      "Manhattan timeline" — operational
#                                      cargo by 2033-2035.
#    Phase 2 (DEFERRED)             : GRYPHON crewed vehicle
#                                      Hypersonic waverider, 4 crew + 10 t.
#                                      Same rail; deferred until pod
#                                      pipeline is proven and Artemis crew
#                                      missions establish lunar presence.
#
#  In the Space Pipeline architecture:
#    Earth surface → [BGKPJR rail] → LEO (cargo pods)
#                                      ↓
#                                   [Space Tug]
#                                      ↓
#                                  Lunar orbit
#                                      ↓
#                                [Blue Moon Mk2 lander or SpaceX HLS]
#                                      ↓
#                                Lunar surface
#                                      ↓
#                       [Empty pods → regolith-filled "Space LEGO"
#                        radiation-proof base structures]
#
# ═══════════════════════════════════════════════════════════════════════

class PROGRAM_PHASE:
    CURRENT = "Phase 1 — Manna Cargo Pipeline"
    PHASES = {
        "phase_0": {"name": "Concept Maturation & Subscale Demonstrator",
                    "years": "2026-2028",
                    "status": "ACTIVE — concept paper, NIAC submission, dimensional reconciliation"},
        "phase_1": {"name": "Manna Cargo Pipeline (unmanned)",
                    "years": "2029-2033",
                    "status": "PRIMARY OBJECTIVE",
                    "description": "37 km rail operational; cargo pods to LEO; Tug to lunar orbit; lander handoff"},
        "phase_2": {"name": "Gryphon Crewed (deferred)",
                    "years": "2034+",
                    "status": "DEFERRED",
                    "description": "Same rail; hypersonic crewed vehicle; pending pod pipeline maturity"},
    }

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 2A — MANNA POD: Unmanned cargo pod (CURRENT PRIMARY VEHICLE)
# ═══════════════════════════════════════════════════════════════════════

class MANNA_POD:
    """
    Canonical Manna pod: passive ballistic cargo unit launched on the 37 km
    rail to LEO, captured by a Space Tug for translunar transfer.

    Pod variants (H/I/B/F/M/X/T) all share these chassis dimensions and
    the canonical 4 G rail acceleration; they differ in cargo class,
    internal cushioning (effective internal G), and recovery mode.
    """
    # Chassis (common to all variants)
    DIAMETER_M = 1.8                # bore-clearance (tube ID = 10 m)
    LENGTH_M_NOMINAL = 4.5          # mean of variants
    DRY_MASS_KG_NOMINAL = 800.0     # PROVISIONAL  pending Lukens
    PAYLOAD_FRACTION_NOMINAL = 0.65 # PROVISIONAL  variant-dependent

    # Mass class (canonical at canonical rail v=1700 m/s, 4G internal)
    GROSS_MASS_KG_NOMINAL = 4000.0  # PROVISIONAL
    PAYLOAD_KG_NOMINAL = 2600.0     # PROVISIONAL  cargo

    # Mission profile
    EXIT_VELOCITY_MS = 1700.0       # = RAIL.EXIT_VELOCITY_MS (canonical)
    EXIT_MACH = 5.0
    INTERNAL_G_DEFAULT = 4.0        # rail G; can be cushioned to lower
    SECOND_STAGE_DV_MS = 7700.0     # rocket boost from Mach 5 to LEO

    # End-of-life — pods become regolith-filled "Space LEGO" structures
    REPURPOSE_AS_REGOLITH_FILL = True  # NASA / lunar base structural use

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 2B — SPACE TUG: Reusable LEO-to-Moon transfer vehicle
# ═══════════════════════════════════════════════════════════════════════

class SPACE_TUG:
    """
    Permanent in-space cargo tug. Captures Manna pods in LEO, performs
    trans-lunar injection, releases pods in lunar orbit for capture by
    a lander (Blue Moon Mk2, SpaceX HLS, or equivalent). Refuels in LEO
    or lunar orbit (eventually from Manna-F propellant pods carrying
    LH₂/LOX or ISRU water from lunar surface).

    Size class: "size of a delivery van — never lands, never fights
    Earth's gravity. Engine + hitch. Fuel is the limit, not size."
    """
    # Size class (PROVISIONAL pending Phase 0 design study)
    DRY_MASS_KG = 5000.0            # PROVISIONAL  ~delivery-van scale
    PROPELLANT_CAPACITY_KG = 25000.0
    LENGTH_M_NOMINAL = 6.0
    DIAMETER_M_NOMINAL = 3.0

    # Performance
    DELTA_V_PER_REFUEL_MS = 4500.0  # full-tank Δv budget
    LEO_TO_LUNAR_DV_REQUIRED = 4100.0  # m/s LEO → low-lunar orbit
    ROUNDTRIP_DV_REQUIRED = 4500.0  # one-way + return-empty + station-keep

    # Architecture
    PROPELLANT_TYPE = "LH₂ / LOX (ISRU compatible)"
    REFUELING_INTERFACE = "Manna-F propellant pod compatible"
    LIFETIME_CYCLES = 50            # PROVISIONAL  refurbish cadence

# ═══════════════════════════════════════════════════════════════════════
#  THE MANHATTAN TIMELINE — 7-9 year operational cargo pipeline
# ═══════════════════════════════════════════════════════════════════════

class TIMELINE:
    """
    The 'Manhattan Project' timeline (Shane's framing): assuming 2026 start,
    operational cargo pipeline in 7-9 years (i.e., 2033-2035).

    Parallel to Artemis crew launches at 10-month cadence using SpaceX HLS
    or Blue Moon Mk2 landers. BGKPJR pods feed those landers with cargo,
    propellant (Manna-F), and ISRU feedstock.

    Current push: lunar base operational in 3 years (~2029).
    """
    PROGRAM_START_YEAR = 2026
    OPERATIONAL_CARGO_YEAR_LOW = 2033      # 7-year aggressive
    OPERATIONAL_CARGO_YEAR_HIGH = 2035     # 9-year nominal
    LUNAR_BASE_TARGET_YEAR = 2029          # 3-year aggressive (NASA-led)
    ARTEMIS_CADENCE_MONTHS = 10            # crew launches every 10 mo
    BGKPJR_CARGO_CADENCE_TARGET_YEAR = 21  # pod launches per year initial
    BGKPJR_CARGO_CADENCE_TARGET_MATURE = 50  # pod launches per year mature

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 3 — GRYPHON: Hypersonic waverider with variable-geometry wings
#  STATUS: DEFERRED (Phase 2). Constants retained for forward-compatibility.
# ═══════════════════════════════════════════════════════════════════════

class GRYPHON:
    # ── Mass (PROVISIONAL — three values exist across docs) ───────────
    DRY_MASS_KG = 50000.0        # PROVISIONAL  pending Lukens validation
    PAYLOAD_MASS_KG = 5000.0     # PROVISIONAL  10 t cargo or 4 crew
    PROPELLANT_MASS_KG = 30000.0 # PROVISIONAL  initial estimate

    # ── Aero geometry (Boyd waverider) ────────────────────────────────
    LENGTH_M = 25.0              # TR-V2
    SPAN_RETRACTED_M = 12.0      # TR-V2  tube clearance
    SPAN_DEPLOYED_M = 18.0       # TR-V2
    PLANFORM_AREA_M2 = 180.0     # TR-V2
    LEADING_EDGE_SWEEP_DEG = 75.0  # TR-V2
    LEADING_EDGE_RADIUS_MM = 3.0   # TR-V2

    # ── Aero performance ──────────────────────────────────────────────
    LD_HYPERSONIC = 4.5          # TR-V2  L/D at Mach 8-10
    LD_SUBSONIC = 8.0            # TR-V2
    CD0_HYPERSONIC = 0.015       # TR-V2  zero-lift drag
    CL_ALPHA_PER_DEG = 0.05      # TR-V2

    # ── Mission profile ───────────────────────────────────────────────
    MAX_MACH_ATMOSPHERE = 8.0    # PROVISIONAL  scramjet upper bound
    WING_DEPLOY_TIME_SEC = 3.0   # PATENT envelope (≤5)
    GLIDE_RATIO = 6.5            # PROVISIONAL

    # ── Propulsion (rocket phase) ─────────────────────────────────────
    ISP_VACUUM_S = 350.0         # TR-V2  LOX/RP-1
    ISP_SEA_LEVEL_S = 310.0      # TR-V2
    THRUST_MAX_N = 500000.0      # TR-V2  per engine, 3 engines

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 3 — KEPLER: Orbital solar sail (Phase 4 deep-space, post-LEO)
# ═══════════════════════════════════════════════════════════════════════

class KEPLER:
    SAIL_AREA_M2 = 1200.0          # Both repos agreed
    SAIL_MASS_KG = 50.0            # Sims; sail + boom + deploy mech
    SAIL_THICKNESS_M = 2.5e-6      # Sims
    SAIL_MATERIAL = "CP1 Polyimide"
    REFLECTIVITY = 0.9             # Sims canonical η
    DEPLOY_ALTITUDE_KM = 400.0     # Standard LEO baseline
    BOOM_LENGTH_M = 35.0           # PROVISIONAL

# ═══════════════════════════════════════════════════════════════════════
#  MISSION ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════

class MISSION:
    DELTA_V_TO_LEO_TOTAL_MS = 9400.0   # standard from-surface
    LEO_VELOCITY_MS = 7670.0
    LEO_ALTITUDE_KM = 400.0

    # Rail provides this much
    RAIL_DELTA_V_FRACTION = RAIL.EXIT_VELOCITY_MS / DELTA_V_TO_LEO_TOTAL_MS  # ~18 %

    LAUNCH_CADENCE_INITIAL_PER_YEAR = 21    # TR-V2 Shotwell integration
    LAUNCH_CADENCE_TARGET_PER_YEAR = 50

# ═══════════════════════════════════════════════════════════════════════
#  COSTS (programmatic estimates — all PROVISIONAL)
# ═══════════════════════════════════════════════════════════════════════

class COSTS:
    INFRASTRUCTURE_USD_LOW = 85e9     # VG
    INFRASTRUCTURE_USD_HIGH = 120e9   # VG
    PER_LAUNCH_USD = 10e6             # TR-V2
    PER_KG_LEO_USD = 1025             # TR-V2 vs $2,720 Falcon 9
    DEVELOPMENT_TIMELINE_YEARS = 13   # TR-V2 to crewed operations

# ═══════════════════════════════════════════════════════════════════════
#  DERIVE-CHECK: assert all internal cross-validations close
# ═══════════════════════════════════════════════════════════════════════

def derive_check(tolerance: float = 0.01, verbose: bool = True) -> dict:
    """Run internal cross-checks. Returns dict of check results.
    Raises AssertionError on any failure outside tolerance."""

    results = {}

    # ── Rail kinematics: a = v² / (2L) ────────────────────────────────
    a_required = RAIL.EXIT_VELOCITY_MS**2 / (2 * RAIL.LENGTH_M)
    g_required = a_required / G_EARTH
    err = abs(g_required - RAIL.PEAK_G) / RAIL.PEAK_G
    results["rail_kinematics_g"] = {
        "claimed": RAIL.PEAK_G,
        "computed": g_required,
        "error_pct": err * 100,
        "pass": err < tolerance,
    }
    assert err < tolerance, (
        f"Rail kinematics fail: a = v²/(2L) = {a_required:.2f} m/s² = "
        f"{g_required:.3f} G; claim is {RAIL.PEAK_G} G ({err*100:.1f} % error)"
    )

    # ── Run time: t = v / a ───────────────────────────────────────────
    t_computed = RAIL.EXIT_VELOCITY_MS / a_required
    results["rail_run_time_sec"] = round(t_computed, 2)

    # ── Mach to velocity (sea level) ──────────────────────────────────
    v_from_mach = RAIL.EXIT_MACH * MACH_1_SL
    err = abs(v_from_mach - RAIL.EXIT_VELOCITY_MS) / RAIL.EXIT_VELOCITY_MS
    results["mach_velocity_consistency"] = {
        "claimed": RAIL.EXIT_VELOCITY_MS,
        "computed": v_from_mach,
        "error_pct": err * 100,
        "pass": err < tolerance,
    }
    assert err < tolerance, f"Mach conversion fail: M{RAIL.EXIT_MACH} = {v_from_mach:.0f} m/s ≠ {RAIL.EXIT_VELOCITY_MS}"

    # ── Patent envelope ───────────────────────────────────────────────
    assert PATENT.EXIT_MACH_MIN <= RAIL.EXIT_MACH <= PATENT.EXIT_MACH_MAX, \
        f"Mach {RAIL.EXIT_MACH} outside patent envelope [{PATENT.EXIT_MACH_MIN}, {PATENT.EXIT_MACH_MAX}]"
    assert RAIL.PEAK_G <= PATENT.PEAK_G_MAX, \
        f"G-load {RAIL.PEAK_G} exceeds patent claim ≤{PATENT.PEAK_G_MAX}"
    assert PATENT.INCLINATION_DEG_MIN <= RAIL.INCLINATION_DEG <= PATENT.INCLINATION_DEG_MAX, \
        f"Inclination outside patent envelope"
    assert PATENT.TUBE_PRESSURE_ATM_MIN <= RAIL.TUBE_PRESSURE_ATM <= PATENT.TUBE_PRESSURE_ATM_MAX, \
        f"Tube pressure outside patent envelope"
    assert GRYPHON.WING_DEPLOY_TIME_SEC <= PATENT.WING_DEPLOY_SEC_MAX, \
        f"Wing deploy time exceeds patent claim"
    results["patent_envelope"] = {"pass": True}

    # ── Coil count ────────────────────────────────────────────────────
    coil_count = int(RAIL.LENGTH_M / RAIL.COIL_SPACING_M)
    results["coil_count_total"] = coil_count

    # ── Solar sail acceleration (derived, not asserted) ───────────────
    a_sail_si = (2 * SOLAR_PRESSURE_1AU * KEPLER.SAIL_AREA_M2 * KEPLER.REFLECTIVITY) / KEPLER.SAIL_MASS_KG
    results["kepler_acceleration_mmps2"] = round(a_sail_si * 1000, 4)

    # ── Rail Δv as fraction of total to LEO ───────────────────────────
    results["rail_delta_v_fraction_pct"] = round(MISSION.RAIL_DELTA_V_FRACTION * 100, 1)

    # ── Energy required (kinetic, vehicle dependent) ──────────────────
    # Lower bound: Gryphon dry only
    e_dry_gj = 0.5 * GRYPHON.DRY_MASS_KG * RAIL.EXIT_VELOCITY_MS**2 / 1e9
    # Upper bound: Gryphon dry + payload + propellant
    m_full = GRYPHON.DRY_MASS_KG + GRYPHON.PAYLOAD_MASS_KG + GRYPHON.PROPELLANT_MASS_KG
    e_full_gj = 0.5 * m_full * RAIL.EXIT_VELOCITY_MS**2 / 1e9
    results["kinetic_energy_min_gj"] = round(e_dry_gj, 1)
    results["kinetic_energy_max_gj"] = round(e_full_gj, 1)

    if verbose:
        print("=" * 72)
        print("BGKPJR Canonical Dimensions — Cross-Check")
        print("=" * 72)
        print(f"  RAIL          : L={RAIL.LENGTH_KM} km, D={RAIL.DIAMETER_M} m, "
              f"θ={RAIL.INCLINATION_DEG}°, P={RAIL.TUBE_PRESSURE_ATM} atm")
        print(f"  KINEMATICS    : v={RAIL.EXIT_VELOCITY_MS} m/s (Mach {RAIL.EXIT_MACH}), "
              f"{RAIL.PEAK_G} G, t≈{t_computed:.1f} s")
        print(f"  COILS         : {coil_count} total at {RAIL.COIL_SPACING_M} m spacing, "
              f"{RAIL.COIL_PEAK_FIELD_T} T peak field")
        print(f"  MUZZLE        : {RAIL.MUZZLE_SEAL_TYPE}")
        print(f"                  stagnation P = {RAIL.MUZZLE_STAGNATION_PRESSURE_MPA} MPa @ Mach 5 SL")
        print(f"  GRYPHON       : {GRYPHON.DRY_MASS_KG/1000:.0f} t dry, "
              f"{GRYPHON.PAYLOAD_MASS_KG/1000:.0f} t payload, L={GRYPHON.LENGTH_M} m")
        print(f"  KEPLER        : {KEPLER.SAIL_AREA_M2} m², {KEPLER.SAIL_MASS_KG} kg, "
              f"a = {a_sail_si*1000:.2f} mm/s² (derived)")
        print(f"  ENERGY        : {e_dry_gj:.0f}–{e_full_gj:.0f} GJ kinetic; "
              f"{RAIL.SMES_CAPACITY_GJ} GJ stored ({RAIL.PEAK_POWER_GW} GW peak)")
        print(f"  MISSION       : rail Δv = {MISSION.RAIL_DELTA_V_FRACTION*100:.1f} % of {MISSION.DELTA_V_TO_LEO_TOTAL_MS} m/s to LEO")
        print(f"  COSTS         : ${COSTS.INFRASTRUCTURE_USD_LOW/1e9:.0f}–"
              f"${COSTS.INFRASTRUCTURE_USD_HIGH/1e9:.0f} B infra; "
              f"${COSTS.PER_KG_LEO_USD}/kg LEO (provisional)")
        print(f"  PATENT        : envelope respected (Mach 3-5, 15-45°, ≤5G, 0.05-0.2 atm)")
        print()
        print(f"  ✓ All cross-checks pass within {tolerance*100:.1f}% tolerance.")
        print("=" * 72)

    return results


def export_for_typescript() -> dict:
    """Return a flat dict suitable for JSON dump and TypeScript mirror.
    Used to keep BGKPJR-Launch-Vis/src/data/launch.ts in lock-step."""
    return {
        "_provenance": {
            "source": "BGKPJR-Core-Simulations/simulation/src/bgkpjr_dimensions.py",
            "reconciliation_date": "2026-04-30",
            "supersedes": "Pre-VacuumGate baselines (28.7 km / Mach 3.5)",
        },
        "RAIL": {
            "lengthKm": RAIL.LENGTH_KM,
            "diameterM": RAIL.DIAMETER_M,
            "inclinationDeg": RAIL.INCLINATION_DEG,
            "tubePressureAtm": RAIL.TUBE_PRESSURE_ATM,
            "exitMach": RAIL.EXIT_MACH,
            "exitVelocityMs": RAIL.EXIT_VELOCITY_MS,
            "peakG": RAIL.PEAK_G,
            "runTimeSec": round(RAIL.EXIT_VELOCITY_MS / (RAIL.PEAK_G * G_EARTH), 1),
            "armatureMaterial": RAIL.ARMATURE_MATERIAL,
            "armatureTempK": RAIL.ARMATURE_TEMP_K,
            "magFieldT": RAIL.COIL_PEAK_FIELD_T,
            "coilCount": int(RAIL.LENGTH_M / RAIL.COIL_SPACING_M),
            "coilSpacingM": RAIL.COIL_SPACING_M,
            "energyGJ": RAIL.SMES_CAPACITY_GJ,
            "peakPowerGW": RAIL.PEAK_POWER_GW,
            "muzzleSealType": RAIL.MUZZLE_SEAL_TYPE,
            "muzzleLh2TempK": RAIL.MUZZLE_LH2_TEMP_K,
            "muzzleStagnationPressureMPa": RAIL.MUZZLE_STAGNATION_PRESSURE_MPA,
        },
        "GRYPHON": {
            "dryMassKg": GRYPHON.DRY_MASS_KG,
            "payloadKg": GRYPHON.PAYLOAD_MASS_KG,
            "propellantKg": GRYPHON.PROPELLANT_MASS_KG,
            "lengthM": GRYPHON.LENGTH_M,
            "spanDeployedM": GRYPHON.SPAN_DEPLOYED_M,
            "spanRetractedM": GRYPHON.SPAN_RETRACTED_M,
            "planformAreaM2": GRYPHON.PLANFORM_AREA_M2,
            "ldHypersonic": GRYPHON.LD_HYPERSONIC,
            "ldSubsonic": GRYPHON.LD_SUBSONIC,
            "maxMach": GRYPHON.MAX_MACH_ATMOSPHERE,
            "wingDeploySec": GRYPHON.WING_DEPLOY_TIME_SEC,
            "glideRatio": GRYPHON.GLIDE_RATIO,
        },
        "KEPLER": {
            "sailAreaM2": KEPLER.SAIL_AREA_M2,
            "sailMassKg": KEPLER.SAIL_MASS_KG,
            "sailThicknessM": KEPLER.SAIL_THICKNESS_M,
            "materialCP1": KEPLER.SAIL_MATERIAL,
            "reflectivity": KEPLER.REFLECTIVITY,
            "deployAltKm": KEPLER.DEPLOY_ALTITUDE_KM,
            "solarPressurePa": SOLAR_PRESSURE_1AU,
            "nominalDvMmps": round(
                (2 * SOLAR_PRESSURE_1AU * KEPLER.SAIL_AREA_M2 * KEPLER.REFLECTIVITY)
                / KEPLER.SAIL_MASS_KG * 1000, 3),
        },
        "MISSION": {
            "deltaVToLeoMs": MISSION.DELTA_V_TO_LEO_TOTAL_MS,
            "leoVelocityMs": MISSION.LEO_VELOCITY_MS,
            "leoAltitudeKm": MISSION.LEO_ALTITUDE_KM,
            "railDvFraction": round(MISSION.RAIL_DELTA_V_FRACTION, 3),
            "cadenceInitialPerYr": MISSION.LAUNCH_CADENCE_INITIAL_PER_YEAR,
            "cadenceTargetPerYr": MISSION.LAUNCH_CADENCE_TARGET_PER_YEAR,
        },
        "COSTS": {
            "infrastructureUsdLow": COSTS.INFRASTRUCTURE_USD_LOW,
            "infrastructureUsdHigh": COSTS.INFRASTRUCTURE_USD_HIGH,
            "perLaunchUsd": COSTS.PER_LAUNCH_USD,
            "perKgLeoUsd": COSTS.PER_KG_LEO_USD,
            "developmentYears": COSTS.DEVELOPMENT_TIMELINE_YEARS,
        },
    }


if __name__ == "__main__":
    import json
    import sys

    results = derive_check(verbose=True)

    if "--json" in sys.argv:
        print()
        print(json.dumps(export_for_typescript(), indent=2))
