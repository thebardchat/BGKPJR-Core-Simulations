"""
Kepler Solar Sail Dynamics Module
==================================

Closes the canonical-baseline gap flagged in PRE-LUKENS-AUDIT-2026-04-30:

    "🔴 SHOWSTOPPER: MISSING SOLAR SAIL DYNAMICS MODEL
        Patent claims Kepler sail for 'station-keeping and orbital
        maneuvering' (Claim 4). Reality: no acceleration, thrust, or
        orbital mechanics model exists."

This module provides:
    1. Solar radiation pressure force model (canonical)
    2. Sail attitude / cone-angle effects on thrust vector
    3. Orbit-raising delta-v over time
    4. Distance-from-sun scaling (1/r² law)
    5. Reflectivity sensitivity (canonical η = 0.9 CP1 polyimide)

All values trace to bgkpjr_dimensions.py SoT. Run derive_check() to verify.

Note: Kepler is Phase 4 (deep-space, post-LEO). Phase 1 (Manna cargo
pipeline to Moon) does NOT use the sail. This module exists for
forward-compatibility with future Phase 4 missions and for the patent
claim to be backed by a working analytical model.

Author: Shane Brazelton + Claude (Anthropic)
Date: 2026-04-30
"""

from __future__ import annotations
import math
from dataclasses import dataclass

from . import bgkpjr_dimensions as _SoT


# ═══════════════════════════════════════════════════════════════════════
#  Physical constants
# ═══════════════════════════════════════════════════════════════════════

AU_M = 1.495978707e11        # 1 astronomical unit in meters
LY_PER_AU = 1 / 63241.07     # for very long missions

# Solar pressure at 1 AU is the SoT canonical value
P_SOLAR_1AU_PA = _SoT.SOLAR_PRESSURE_1AU


# ═══════════════════════════════════════════════════════════════════════
#  Sail spec from canonical SoT
# ═══════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class SailSpec:
    """Canonical Kepler sail specification (mirrors SoT.KEPLER)."""
    area_m2: float = _SoT.KEPLER.SAIL_AREA_M2          # 1200 m²
    mass_kg: float = _SoT.KEPLER.SAIL_MASS_KG          # 50 kg sail+boom+deploy
    thickness_m: float = _SoT.KEPLER.SAIL_THICKNESS_M  # 2.5 µm
    reflectivity: float = _SoT.KEPLER.REFLECTIVITY     # 0.9 (CP1 polyimide)
    deploy_alt_km: float = _SoT.KEPLER.DEPLOY_ALTITUDE_KM
    boom_length_m: float = _SoT.KEPLER.BOOM_LENGTH_M

    @property
    def areal_density_g_m2(self) -> float:
        """Sail areal density (sail material + boom averaged), g/m²."""
        return (self.mass_kg / self.area_m2) * 1000

    @property
    def characteristic_acceleration_mmps2(self) -> float:
        """Acceleration at 1 AU with sail face-on to Sun (peak performance)."""
        return _solar_accel(self, distance_au=1.0, cone_angle_deg=0.0) * 1000


# ═══════════════════════════════════════════════════════════════════════
#  Core force / acceleration models
# ═══════════════════════════════════════════════════════════════════════

def solar_pressure_at_distance(distance_au: float) -> float:
    """Solar radiation pressure (Pa) at given heliocentric distance.

    Inverse-square law: P(r) = P_0 / (r_AU)²
    """
    if distance_au <= 0:
        raise ValueError(f"distance_au must be positive, got {distance_au}")
    return P_SOLAR_1AU_PA / (distance_au ** 2)


def _solar_accel(sail: SailSpec, distance_au: float = 1.0, cone_angle_deg: float = 0.0) -> float:
    """Sail acceleration in m/s² for a given heliocentric distance and
    cone angle (angle between sail normal and sun line).

    Derivation:
        F_radial = (1 + ρ) · P · A · cos²(α)        (perfect specular reflector)
        a = F_radial / m

    For canonical reflectivity η = 0.9:
        Effective momentum coupling = (1 + η) ≈ 1.9
        (perfectly absorbing sail = 1.0; perfect reflector = 2.0)

    Args:
        sail: sail specification
        distance_au: heliocentric distance in AU (1 AU = 1.495×10¹¹ m)
        cone_angle_deg: angle between sail normal and sun line (deg).
                        0° = face-on (max thrust), 90° = edge-on (zero).
    """
    if not (0.0 <= cone_angle_deg <= 90.0):
        raise ValueError(f"cone_angle_deg must be in [0, 90], got {cone_angle_deg}")
    pressure = solar_pressure_at_distance(distance_au)
    cos_alpha = math.cos(math.radians(cone_angle_deg))
    momentum_coupling = (1.0 + sail.reflectivity) * (cos_alpha ** 2)
    force_n = momentum_coupling * pressure * sail.area_m2
    return force_n / sail.mass_kg


def thrust_components(sail: SailSpec, distance_au: float = 1.0,
                      cone_angle_deg: float = 0.0) -> tuple[float, float]:
    """Return (radial_accel_m_s2, transverse_accel_m_s2).

    For a flat sail tilted at cone angle α from sun line:
        F_normal = (1 + ρ) P A cos²(α)
        F_radial    = F_normal × cos(α)    [pushed away from sun]
        F_transverse = F_normal × sin(α)    [along sail in-plane]

    For orbit raising / lowering, transverse component is what does work
    against the orbit's velocity vector.
    """
    pressure = solar_pressure_at_distance(distance_au)
    alpha = math.radians(cone_angle_deg)
    cos_a, sin_a = math.cos(alpha), math.sin(alpha)
    f_normal = (1.0 + sail.reflectivity) * pressure * sail.area_m2 * (cos_a ** 2)
    a_radial = f_normal * cos_a / sail.mass_kg
    a_trans = f_normal * sin_a / sail.mass_kg
    return a_radial, a_trans


# ═══════════════════════════════════════════════════════════════════════
#  Mission-class delta-v over time
# ═══════════════════════════════════════════════════════════════════════

def delta_v_over_days(sail: SailSpec, days: float, distance_au: float = 1.0,
                      cone_angle_deg: float = 35.26) -> float:
    """Total Δv accumulated by a sail over a given duration.

    35.26° cone angle is the optimal-thrust geometry for prograde
    orbit-raising (maximizes transverse component while keeping the
    sail in a productive attitude). Derivation in §3.5 of the appendix.

    Args:
        sail: sail spec
        days: mission duration
        distance_au: heliocentric distance (constant — this is a
                     simplified estimate; for orbital sims integrate over r(t))
        cone_angle_deg: 35.26° for max prograde thrust; 0° for radial.

    Returns:
        Δv in m/s, accumulated over duration.
    """
    a_radial, a_trans = thrust_components(sail, distance_au, cone_angle_deg)
    a_total = math.hypot(a_radial, a_trans)
    seconds = days * 86400
    return a_total * seconds


def required_days_for_delta_v(sail: SailSpec, target_delta_v_ms: float,
                              distance_au: float = 1.0,
                              cone_angle_deg: float = 35.26) -> float:
    """Inverse: how many days to accumulate `target_delta_v_ms`?"""
    a_radial, a_trans = thrust_components(sail, distance_au, cone_angle_deg)
    a_total = math.hypot(a_radial, a_trans)
    if a_total <= 0:
        return float('inf')
    return (target_delta_v_ms / a_total) / 86400


# ═══════════════════════════════════════════════════════════════════════
#  Sanity / report
# ═══════════════════════════════════════════════════════════════════════

def report(sail: SailSpec | None = None) -> dict:
    """Print and return a complete characterization of the canonical sail."""
    if sail is None:
        sail = SailSpec()

    char_accel = sail.characteristic_acceleration_mmps2

    # Reference Δv targets
    targets = [
        ("Lunar escape (from ~LEO baseline)", 1100),
        ("Earth-to-Mars Hohmann transfer", 2900),
        ("Earth-to-Jupiter (sail-augmented)", 8800),
    ]

    print("=" * 72)
    print("Kepler Solar Sail — Canonical Performance Report")
    print("=" * 72)
    print(f"  Sail area              : {sail.area_m2:>10.1f} m²")
    print(f"  Sail mass              : {sail.mass_kg:>10.1f} kg")
    print(f"  Sail thickness         : {sail.thickness_m*1e6:>10.2f} µm")
    print(f"  Reflectivity (η)       : {sail.reflectivity:>10.2f}")
    print(f"  Areal density          : {sail.areal_density_g_m2:>10.2f} g/m²")
    print(f"  Boom length            : {sail.boom_length_m:>10.1f} m")
    print(f"  Deploy altitude        : {sail.deploy_alt_km:>10.0f} km")
    print()
    print(f"  P_solar at 1 AU        : {P_SOLAR_1AU_PA:>10.3e} Pa")
    print(f"  Char. acceleration     : {char_accel:>10.3f} mm/s²  (face-on at 1 AU)")
    print()
    print("  Orbit-raising Δv potential (cone 35.26°, 1 AU):")
    a_r, a_t = thrust_components(sail, 1.0, 35.26)
    a_tot_mmps2 = math.hypot(a_r, a_t) * 1000
    print(f"    Total prograde a     : {a_tot_mmps2:>10.4f} mm/s²")
    print(f"    30 days              : {delta_v_over_days(sail, 30):>10.1f} m/s")
    print(f"    180 days             : {delta_v_over_days(sail, 180):>10.1f} m/s")
    print(f"    1 year               : {delta_v_over_days(sail, 365):>10.1f} m/s")
    print()
    print("  Mission-class Δv targets — time required:")
    for name, dv in targets:
        days = required_days_for_delta_v(sail, dv)
        print(f"    {name:<42} : {days:>7.0f} days  ({days/365:.1f} years)")
    print()
    print("  Distance scaling (face-on, days for 1000 m/s Δv):")
    for r in [0.5, 1.0, 1.5, 5.2]:  # Venus, Earth, Mars, Jupiter
        days = 1000.0 / (_solar_accel(sail, r, 0.0) * 86400)
        print(f"    {r:.1f} AU                       : {days:>7.0f} days")
    print("=" * 72)

    return {
        "areal_density_g_m2": round(sail.areal_density_g_m2, 2),
        "characteristic_accel_mmps2": round(char_accel, 4),
        "delta_v_30d_ms": round(delta_v_over_days(sail, 30), 2),
        "delta_v_180d_ms": round(delta_v_over_days(sail, 180), 2),
        "delta_v_1yr_ms": round(delta_v_over_days(sail, 365), 2),
        "days_for_lunar_escape": round(required_days_for_delta_v(sail, 1100), 1),
        "days_for_mars_transfer": round(required_days_for_delta_v(sail, 2900), 1),
    }


# ═══════════════════════════════════════════════════════════════════════
#  Self-test (matches SoT canonical value for cross-check)
# ═══════════════════════════════════════════════════════════════════════

def derive_check(tolerance: float = 0.01) -> None:
    """Verify this module's characteristic acceleration matches the SoT
    derived value in bgkpjr_dimensions.export_for_typescript()."""
    sail = SailSpec()
    a_module = sail.characteristic_acceleration_mmps2

    sot_export = _SoT.export_for_typescript()
    a_sot = sot_export["KEPLER"]["nominalDvMmps"]

    # The SoT computes "face-on at 1 AU" exactly, so they should match
    rel_err = abs(a_module - a_sot) / a_sot
    assert rel_err < tolerance, (
        f"Solar sail derive_check FAILED: module computes "
        f"{a_module:.4f} mm/s², SoT exports {a_sot} mm/s² "
        f"({rel_err*100:.2f}% error)"
    )
    print(f"✓ Solar sail module characteristic acceleration "
          f"({a_module:.4f} mm/s²) matches SoT ({a_sot} mm/s²) within {tolerance*100:.1f}%")


if __name__ == "__main__":
    derive_check()
    print()
    report()
