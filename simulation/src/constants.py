"""
Physical Constants and System Parameters for BGKPJR Simulations

This module defines all fundamental physical constants and system-specific
parameters used throughout the simulation framework.

Author: Shane Brazelton
Date: 2025
"""

import math
from dataclasses import dataclass
from typing import Final


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

    # Maglev Track Parameters
    TRACK_LENGTH: float = 28700.0  # m (28.7 km)
    TRACK_ANGLE_MIN: float = 15.0  # degrees
    TRACK_ANGLE_MAX: float = 45.0  # degrees
    TRACK_ANGLE_DEFAULT: float = 30.0  # degrees
    TUBE_PRESSURE_RATIO: float = 0.1  # Fraction of atmospheric (0.1 atm)
    MAX_ACCELERATION_G: float = 4.0  # Maximum allowed g-force

    # Exit Conditions
    EXIT_MACH_MIN: float = 3.5
    EXIT_MACH_MAX: float = 5.0
    EXIT_MACH_DEFAULT: float = 3.5

    # Gryphon Spacecraft
    GRYPHON_MASS_DRY: float = 15000.0  # kg
    GRYPHON_MASS_PAYLOAD: float = 5000.0  # kg
    GRYPHON_MASS_PROPELLANT: float = 30000.0  # kg (initial estimate)
    GRYPHON_WING_AREA: float = 120.0  # m² (deployed)
    GRYPHON_WING_AREA_RETRACTED: float = 40.0  # m² (during tube transit)
    GRYPHON_LENGTH: float = 25.0  # m (characteristic length)
    GRYPHON_CD0: float = 0.015  # Zero-lift drag coefficient (hypersonic)
    GRYPHON_CL_ALPHA: float = 0.05  # Lift curve slope (per degree)
    GRYPHON_LD_HYPERSONIC: float = 4.5  # L/D at hypersonic speeds
    GRYPHON_LD_SUBSONIC: float = 8.0  # L/D for glide return

    # Kepler Solar Sail
    KEPLER_AREA: float = 1200.0  # m²
    KEPLER_MASS: float = 50.0  # kg (sail + deployment mechanism)
    KEPLER_THICKNESS: float = 2.5e-6  # m (2.5 microns)
    KEPLER_REFLECTIVITY: float = 0.9  # Reflectivity coefficient
    SOLAR_CONSTANT: float = 1361.0  # W/m² at 1 AU

    # Propulsion
    ISP_VACUUM: float = 350.0  # s (typical LOX/RP-1)
    ISP_SEA_LEVEL: float = 310.0  # s
    THRUST_MAX: float = 500000.0  # N (500 kN)

    # Mission Targets
    LEO_ALTITUDE: float = 400000.0  # m (400 km)
    ORBITAL_VELOCITY_LEO: float = 7670.0  # m/s at 400 km
    DELTA_V_TO_LEO: float = 9400.0  # m/s (from surface, traditional)

    @property
    def gryphon_mass_initial(self) -> float:
        """Total initial mass of Gryphon (dry + payload + propellant)."""
        return self.GRYPHON_MASS_DRY + self.GRYPHON_MASS_PAYLOAD + self.GRYPHON_MASS_PROPELLANT

    @property
    def exit_velocity_default(self) -> float:
        """Default exit velocity in m/s (Mach 3.5 at sea level)."""
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
