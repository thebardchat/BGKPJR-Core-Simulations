"""
Physical Constants and System Parameters for BGKPJR Simulations

This module defines fundamental physical constants and system-specific
parameters used throughout the simulation framework.

⚠️  CANONICAL DIMENSIONS NOTICE (2026-04-30)
   The dimensional constants in this file have been reconciled with the
   canonical source-of-truth at:
       simulation/src/bgkpjr_dimensions.py
   which aligns with the BGKPJR-VacuumGate Feasibility Report v1.0
   (April 18, 2026). Key changes from prior baseline:
       TRACK_LENGTH: 28,700 m → 37,000 m
       EXIT_MACH_DEFAULT: 3.5 → 5.0
       MAX_ACCELERATION_G: 4.0 (unchanged, now matches kinematics)
   Run `python -m simulation.src.bgkpjr_dimensions` to verify.
   See expert-reviews/PRE-LUKENS-AUDIT-2026-04-30.md for full rationale.

Author: Shane Brazelton
Date: 2025 (reconciled 2026-04-30)
"""

import math
from dataclasses import dataclass
from typing import Final

# Import canonical SoT (single source of truth)
from . import bgkpjr_dimensions as _SoT


@dataclass(frozen=True)
class PhysicalConstants:
    """Immutable physical constants."""

    # Gravitational
    G0: Final[float] = 9.80665  # Standard gravity (m/s²)
    G_UNIVERSAL: Final[float] = 6.67430e-11  # Universal gravitational constant (N·m²/kg²)

    # Earth Parameters
    EARTH_MASS: Final[float] = 5.972e24  # kg
    EARTH_RADIUS: Final[float] = 6.371e6  # m (mean radius)
    EARTH_MU: Final[float] = 3.986e14  # Standard gravitational parameter (m³/s²)

    # Atmospheric (Sea Level Standard)
    P0: Final[float] = 101325.0  # Standard pressure (Pa)
    T0: Final[float] = 288.15  # Standard temperature (K)
    RHO0: Final[float] = 1.225  # Standard density (kg/m³)

    # Gas Properties (Dry Air)
    R_AIR: Final[float] = 287.05  # Specific gas constant (J/(kg·K))
    GAMMA_AIR: Final[float] = 1.4  # Heat capacity ratio
    CP_AIR: Final[float] = 1005.0  # Specific heat at constant pressure (J/(kg·K))

    # Speed of Sound at Sea Level
    A0: Final[float] = 340.29  # m/s

    # Stefan-Boltzmann Constant
    STEFAN_BOLTZMANN: Final[float] = 5.67e-8  # W/(m²·K⁴)


# Global constants instance
Constants = PhysicalConstants()


@dataclass
class SystemParams:
    """
    BGKPJR System-specific parameters.
    These can be modified for parametric studies.
    """

    # ── Maglev Track Parameters ──────────────────────────────────────
    # All values mirror bgkpjr_dimensions.py (the canonical source of truth).
    TRACK_LENGTH: float = _SoT.RAIL.LENGTH_M
    TRACK_ANGLE_MIN: float = _SoT.PATENT.INCLINATION_DEG_MIN
    TRACK_ANGLE_MAX: float = _SoT.PATENT.INCLINATION_DEG_MAX
    TRACK_ANGLE_DEFAULT: float = _SoT.RAIL.INCLINATION_DEG
    TUBE_PRESSURE_RATIO: float = _SoT.RAIL.TUBE_PRESSURE_ATM
    MAX_ACCELERATION_G: float = _SoT.RAIL.PEAK_G

    # ── Exit Conditions ──────────────────────────────────────────────
    EXIT_MACH_MIN: float = _SoT.PATENT.EXIT_MACH_MIN
    EXIT_MACH_MAX: float = _SoT.PATENT.EXIT_MACH_MAX
    EXIT_MACH_DEFAULT: float = _SoT.RAIL.EXIT_MACH

    # ── Gryphon Spacecraft (DEFERRED — Phase 2 future project) ─────
    # Gryphon is deferred per 2026-04-30 architectural decision. Current
    # critical path is the unmanned cargo pod pipeline (Manna pods + Tug).
    # Gryphon constants retained for forward-compatibility with the LSM
    # accelerator (same rail accommodates both vehicles).
    GRYPHON_MASS_DRY: float = _SoT.GRYPHON.DRY_MASS_KG
    GRYPHON_MASS_PAYLOAD: float = _SoT.GRYPHON.PAYLOAD_MASS_KG
    GRYPHON_MASS_PROPELLANT: float = _SoT.GRYPHON.PROPELLANT_MASS_KG
    GRYPHON_WING_AREA: float = 120.0  # m² (deployed) — retained from original
    GRYPHON_WING_AREA_RETRACTED: float = 40.0  # m² — retained from original
    GRYPHON_LENGTH: float = _SoT.GRYPHON.LENGTH_M
    GRYPHON_CD0: float = _SoT.GRYPHON.CD0_HYPERSONIC
    GRYPHON_CL_ALPHA: float = _SoT.GRYPHON.CL_ALPHA_PER_DEG
    GRYPHON_LD_HYPERSONIC: float = _SoT.GRYPHON.LD_HYPERSONIC
    GRYPHON_LD_SUBSONIC: float = _SoT.GRYPHON.LD_SUBSONIC

    # ── Kepler Solar Sail ──────────────────────────────────────────
    KEPLER_AREA: float = _SoT.KEPLER.SAIL_AREA_M2
    KEPLER_MASS: float = _SoT.KEPLER.SAIL_MASS_KG
    KEPLER_THICKNESS: float = _SoT.KEPLER.SAIL_THICKNESS_M
    KEPLER_REFLECTIVITY: float = _SoT.KEPLER.REFLECTIVITY
    SOLAR_CONSTANT: float = _SoT.SOLAR_CONSTANT_1AU

    # ── Propulsion ─────────────────────────────────────────────────
    ISP_VACUUM: float = _SoT.GRYPHON.ISP_VACUUM_S
    ISP_SEA_LEVEL: float = _SoT.GRYPHON.ISP_SEA_LEVEL_S
    THRUST_MAX: float = _SoT.GRYPHON.THRUST_MAX_N

    # ── Mission Targets ────────────────────────────────────────────
    LEO_ALTITUDE: float = _SoT.MISSION.LEO_ALTITUDE_KM * 1000
    ORBITAL_VELOCITY_LEO: float = _SoT.MISSION.LEO_VELOCITY_MS
    DELTA_V_TO_LEO: float = _SoT.MISSION.DELTA_V_TO_LEO_TOTAL_MS

    @property
    def gryphon_mass_initial(self) -> float:
        """Total initial mass of Gryphon (dry + payload + propellant)."""
        return self.GRYPHON_MASS_DRY + self.GRYPHON_MASS_PAYLOAD + self.GRYPHON_MASS_PROPELLANT

    @property
    def exit_velocity_default(self) -> float:
        """Default exit velocity in m/s (Mach 5 at sea level, VG canonical)."""
        return self.EXIT_MACH_DEFAULT * Constants.A0

    @property
    def track_angle_rad(self) -> float:
        """Default track angle in radians."""
        return math.radians(self.TRACK_ANGLE_DEFAULT)


# Default system parameters instance
DEFAULT_PARAMS = SystemParams()


def calculate_track_length(exit_velocity: float, max_g: float = 4.0) -> float:
    """
    Calculate minimum track length for given exit velocity and g-limit.

    Uses: L = v² / (2 * a)

    Args:
        exit_velocity: Target exit velocity in m/s
        max_g: Maximum allowed acceleration in g's

    Returns:
        Minimum track length in meters
    """
    max_accel = max_g * Constants.G0
    return (exit_velocity ** 2) / (2 * max_accel)


def calculate_exit_velocity(track_length: float, max_g: float = 4.0) -> float:
    """
    Calculate maximum exit velocity for given track length and g-limit.

    Uses: v = sqrt(2 * a * L)

    Args:
        track_length: Track length in meters
        max_g: Maximum allowed acceleration in g's

    Returns:
        Maximum exit velocity in m/s
    """
    max_accel = max_g * Constants.G0
    return math.sqrt(2 * max_accel * track_length)


def tsiolkovsky_delta_v(isp: float, mass_initial: float, mass_final: float) -> float:
    """
    Calculate delta-v using the Tsiolkovsky rocket equation.

    Δv = Isp * g0 * ln(m_initial / m_final)

    Args:
        isp: Specific impulse in seconds
        mass_initial: Initial mass (wet) in kg
        mass_final: Final mass (dry) in kg

    Returns:
        Delta-v in m/s
    """
    if mass_final <= 0 or mass_initial <= mass_final:
        raise ValueError("Invalid mass values for Tsiolkovsky equation")

    return isp * Constants.G0 * math.log(mass_initial / mass_final)


def required_mass_ratio(delta_v: float, isp: float) -> float:
    """
    Calculate required mass ratio for given delta-v.

    m_initial / m_final = exp(Δv / (Isp * g0))

    Args:
        delta_v: Required delta-v in m/s
        isp: Specific impulse in seconds

    Returns:
        Required mass ratio (dimensionless)
    """
    return math.exp(delta_v / (isp * Constants.G0))


if __name__ == "__main__":
    # Quick validation
    print("=== BGKPJR System Parameters Validation ===\n")

    params = DEFAULT_PARAMS

    # Track calculations
    min_length = calculate_track_length(params.exit_velocity_default)
    print(f"Exit velocity (Mach {params.EXIT_MACH_DEFAULT}): {params.exit_velocity_default:.1f} m/s")
    print(f"Minimum track length @ 4g: {min_length/1000:.1f} km")
    print(f"Actual track length: {params.TRACK_LENGTH/1000:.1f} km")
    print(f"Safety margin: {(params.TRACK_LENGTH - min_length)/min_length * 100:.1f}%\n")

    # Rocket equation comparison
    print("=== Tsiolkovsky Analysis ===")
    print(f"Initial mass: {params.gryphon_mass_initial:.0f} kg")

    # Traditional launch
    traditional_ratio = required_mass_ratio(params.DELTA_V_TO_LEO, params.ISP_VACUUM)
    print(f"\nTraditional launch (Δv = {params.DELTA_V_TO_LEO} m/s):")
    print(f"  Required mass ratio: {traditional_ratio:.1f}:1")
    print(f"  Propellant fraction: {(1 - 1/traditional_ratio)*100:.1f}%")

    # BGKPJR launch (reduced delta-v needed)
    bgkpjr_delta_v = params.DELTA_V_TO_LEO - params.exit_velocity_default - 800  # 800 m/s from aero assist
    bgkpjr_ratio = required_mass_ratio(bgkpjr_delta_v, params.ISP_VACUUM)
    print(f"\nBGKPJR launch (Δv = {bgkpjr_delta_v:.0f} m/s):")
    print(f"  Required mass ratio: {bgkpjr_ratio:.1f}:1")
    print(f"  Propellant fraction: {(1 - 1/bgkpjr_ratio)*100:.1f}%")
    print(f"  Mass savings: {(1 - bgkpjr_ratio/traditional_ratio)*100:.1f}%")
