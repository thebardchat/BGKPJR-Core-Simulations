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

    # ── Muzzle interface — VacuumGate's novel IP: LH₂ membrane ────────
    MUZZLE_SEAL_TYPE = "Liquid Hydrogen (LH₂) cryogenic membrane"  # VG
    MUZZLE_LH2_TEMP_K = 20.0                # VG
    MUZZLE_STAGNATION_PRESSURE_MPA = 1.77   # VG    at Mach 5 sea-level
    MUZZLE_CONTROLLED_DETONATION = True     # VG    intended thrust-boost

# ═══════════════════════════════════════════════════════════════════════
#  STAGE 2 — GRYPHON: Hypersonic waverider with variable-geometry wings
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
