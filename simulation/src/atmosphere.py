"""
Standard Atmosphere Model for BGKPJR Simulations

Implements the International Standard Atmosphere (ISA) model extended to 100 km
altitude for full trajectory simulation including exoatmospheric operations.

Atmospheric Layers:
    - Troposphere: 0 - 11 km (temperature decreases)
    - Tropopause: 11 - 20 km (isothermal)
    - Stratosphere: 20 - 32 km (temperature increases)
    - Stratopause: 32 - 47 km (temperature increases)
    - Mesosphere: 47 - 51 km (isothermal)
    - Upper Mesosphere: 51 - 71 km (temperature decreases)
    - Mesopause: 71 - 85 km (temperature decreases)
    - Thermosphere: 85+ km (temperature increases)

Author: Shane Brazelton
Date: 2025
"""

import math
from dataclasses import dataclass
from typing import Optional
from .constants import Constants


@dataclass
class AtmosphericConditions:
    """Container for atmospheric state at a given altitude."""
    altitude: float  # m
    temperature: float  # K
    pressure: float  # Pa
    density: float  # kg/m³
    speed_of_sound: float  # m/s
    viscosity: float  # Pa·s
    mean_free_path: float  # m

    @property
    def mach_number(self) -> callable:
        """Returns a function to calculate Mach number for given velocity."""
        def calc_mach(velocity: float) -> float:
            return velocity / self.speed_of_sound
        return calc_mach


class Atmosphere:
    """
    International Standard Atmosphere (ISA) model extended to 100 km.

    Provides accurate atmospheric properties for trajectory simulation
    across all flight regimes from sea level to the edge of space.
    """

    # Layer definitions: (base_altitude, base_temp, lapse_rate)
    # Lapse rate in K/m (negative = temperature decreasing with altitude)
    LAYERS = [
        (0, 288.15, -0.0065),      # Troposphere
        (11000, 216.65, 0.0),       # Tropopause (isothermal)
        (20000, 216.65, 0.001),     # Lower Stratosphere
        (32000, 228.65, 0.0028),    # Upper Stratosphere
        (47000, 270.65, 0.0),       # Stratopause (isothermal)
        (51000, 270.65, -0.0028),   # Lower Mesosphere
        (71000, 214.65, -0.002),    # Upper Mesosphere
        (85000, 186.95, 0.0),       # Mesopause (approx isothermal)
    ]

    # Base pressures at layer boundaries (pre-computed for efficiency)
    BASE_PRESSURES = [
        101325.0,    # Sea level
        22632.1,     # 11 km
        5474.89,     # 20 km
        868.019,     # 32 km
        110.906,     # 47 km
        66.9389,     # 51 km
        3.95642,     # 71 km
        0.373384,    # 85 km
    ]

    @classmethod
    def get_layer_index(cls, altitude: float) -> int:
        """Determine which atmospheric layer contains the given altitude."""
        for i in range(len(cls.LAYERS) - 1, -1, -1):
            if altitude >= cls.LAYERS[i][0]:
                return i
        return 0

    @classmethod
    def temperature(cls, altitude: float) -> float:
        """
        Calculate temperature at given altitude.

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Temperature in Kelvin
        """
        if altitude < 0:
            altitude = 0
        if altitude > 100000:
            # Above 100 km, use simplified thermosphere model
            # Temperature increases rapidly but we cap it for numerical stability
            return 186.95 + 0.003 * (altitude - 85000)

        idx = cls.get_layer_index(altitude)
        h_base, T_base, lapse = cls.LAYERS[idx]

        return T_base + lapse * (altitude - h_base)

    @classmethod
    def pressure(cls, altitude: float) -> float:
        """
        Calculate pressure at given altitude using barometric formula.

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Pressure in Pascals
        """
        if altitude < 0:
            altitude = 0
        if altitude > 100000:
            # Exponential decay above 100 km
            P_100 = cls.pressure(100000)
            scale_height = 8500  # Approximate scale height at this altitude
            return P_100 * math.exp(-(altitude - 100000) / scale_height)

        idx = cls.get_layer_index(altitude)
        h_base, T_base, lapse = cls.LAYERS[idx]
        P_base = cls.BASE_PRESSURES[idx]

        h = altitude - h_base
        T = T_base + lapse * h

        if abs(lapse) < 1e-10:  # Isothermal layer
            return P_base * math.exp(-Constants.G0 * h / (Constants.R_AIR * T_base))
        else:
            exponent = Constants.G0 / (Constants.R_AIR * lapse)
            return P_base * (T / T_base) ** (-exponent)

    @classmethod
    def density(cls, altitude: float) -> float:
        """
        Calculate air density using ideal gas law.

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Density in kg/m³
        """
        T = cls.temperature(altitude)
        P = cls.pressure(altitude)
        return P / (Constants.R_AIR * T)

    @classmethod
    def speed_of_sound(cls, altitude: float) -> float:
        """
        Calculate speed of sound.

        a = sqrt(gamma * R * T)

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Speed of sound in m/s
        """
        T = cls.temperature(altitude)
        return math.sqrt(Constants.GAMMA_AIR * Constants.R_AIR * T)

    @classmethod
    def viscosity(cls, altitude: float) -> float:
        """
        Calculate dynamic viscosity using Sutherland's Law.

        μ = μ_ref * (T/T_ref)^(3/2) * (T_ref + S) / (T + S)

        where μ_ref = 1.716e-5 Pa·s at T_ref = 273.15 K, S = 110.4 K

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Dynamic viscosity in Pa·s
        """
        T = cls.temperature(altitude)
        T_ref = 273.15
        mu_ref = 1.716e-5
        S = 110.4  # Sutherland's constant for air

        return mu_ref * ((T / T_ref) ** 1.5) * ((T_ref + S) / (T + S))

    @classmethod
    def mean_free_path(cls, altitude: float) -> float:
        """
        Calculate molecular mean free path.

        Important for determining flow regime (continuum vs. rarefied).

        λ = μ * sqrt(π / (2 * ρ * P))

        Args:
            altitude: Geometric altitude in meters

        Returns:
            Mean free path in meters
        """
        mu = cls.viscosity(altitude)
        rho = cls.density(altitude)
        P = cls.pressure(altitude)

        if rho < 1e-10 or P < 1e-10:
            return float('inf')

        return mu * math.sqrt(math.pi / (2 * rho * P))

    @classmethod
    def get_conditions(cls, altitude: float) -> AtmosphericConditions:
        """
        Get complete atmospheric state at given altitude.

        Args:
            altitude: Geometric altitude in meters

        Returns:
            AtmosphericConditions dataclass with all properties
        """
        return AtmosphericConditions(
            altitude=altitude,
            temperature=cls.temperature(altitude),
            pressure=cls.pressure(altitude),
            density=cls.density(altitude),
            speed_of_sound=cls.speed_of_sound(altitude),
            viscosity=cls.viscosity(altitude),
            mean_free_path=cls.mean_free_path(altitude)
        )

    @classmethod
    def knudsen_number(cls, altitude: float, characteristic_length: float) -> float:
        """
        Calculate Knudsen number for flow regime determination.

        Kn = λ / L

        Flow regimes:
            Kn < 0.01: Continuum (Navier-Stokes valid)
            0.01 < Kn < 0.1: Slip flow
            0.1 < Kn < 10: Transitional
            Kn > 10: Free molecular flow

        Args:
            altitude: Geometric altitude in meters
            characteristic_length: Vehicle characteristic length in meters

        Returns:
            Knudsen number (dimensionless)
        """
        mfp = cls.mean_free_path(altitude)
        return mfp / characteristic_length


class TubeAtmosphere:
    """
    Modified atmosphere model for the evacuated launch tube.

    The tube maintains a partial vacuum (typically 0.1 atm) to reduce
    aerodynamic drag during the maglev acceleration phase.
    """

    def __init__(self, pressure_ratio: float = 0.1):
        """
        Initialize tube atmosphere.

        Args:
            pressure_ratio: Fraction of standard atmospheric pressure (0.0 - 1.0)
        """
        if not 0.0 <= pressure_ratio <= 1.0:
            raise ValueError("Pressure ratio must be between 0 and 1")
        self.pressure_ratio = pressure_ratio

    def get_conditions(self, altitude: float = 0) -> AtmosphericConditions:
        """
        Get tube atmospheric conditions.

        Assumes isothermal tube at ground level temperature.

        Args:
            altitude: Altitude of tube section (for temperature variation along incline)

        Returns:
            AtmosphericConditions for tube environment
        """
        # Get standard conditions at this altitude
        std = Atmosphere.get_conditions(altitude)

        # Modify pressure and density for partial vacuum
        tube_pressure = std.pressure * self.pressure_ratio
        tube_density = std.density * self.pressure_ratio

        # Speed of sound and viscosity depend only on temperature
        return AtmosphericConditions(
            altitude=altitude,
            temperature=std.temperature,
            pressure=tube_pressure,
            density=tube_density,
            speed_of_sound=std.speed_of_sound,
            viscosity=std.viscosity,
            mean_free_path=std.mean_free_path / self.pressure_ratio
        )


if __name__ == "__main__":
    # Validation and visualization
    print("=== BGKPJR Atmosphere Model Validation ===\n")

    # Test standard altitudes
    test_altitudes = [0, 5000, 11000, 20000, 30000, 50000, 80000, 100000]

    print("Standard Atmosphere:")
    print("-" * 80)
    print(f"{'Altitude (km)':<15} {'Temp (K)':<12} {'Pressure (Pa)':<15} {'Density (kg/m³)':<18} {'Mach 1 (m/s)':<12}")
    print("-" * 80)

    for h in test_altitudes:
        cond = Atmosphere.get_conditions(h)
        print(f"{h/1000:<15.1f} {cond.temperature:<12.2f} {cond.pressure:<15.2f} {cond.density:<18.6f} {cond.speed_of_sound:<12.2f}")

    print("\n" + "=" * 80)
    print("\nTube Atmosphere (0.1 atm):")
    tube = TubeAtmosphere(0.1)
    tube_cond = tube.get_conditions(0)
    print(f"Pressure: {tube_cond.pressure:.1f} Pa")
    print(f"Density: {tube_cond.density:.4f} kg/m³")
    print(f"Drag reduction factor: {1/0.1:.0f}x")

    # Flow regime analysis
    print("\n" + "=" * 80)
    print("\nFlow Regime Analysis (L = 25m characteristic length):")
    L = 25  # Gryphon length
    for h in [0, 50000, 80000, 100000, 150000]:
        Kn = Atmosphere.knudsen_number(h, L)
        if Kn < 0.01:
            regime = "Continuum"
        elif Kn < 0.1:
            regime = "Slip Flow"
        elif Kn < 10:
            regime = "Transitional"
        else:
            regime = "Free Molecular"
        print(f"h = {h/1000:6.0f} km: Kn = {Kn:.2e} ({regime})")
