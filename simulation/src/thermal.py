"""
Thermal Analysis Module for BGKPJR Simulations

Models heat transfer to the Gryphon spacecraft during:
    - Tube exit (Mach 3.5+ into partial vacuum)
    - Atmospheric ascent (peak heating at Max Q)
    - Potential reentry scenario

Includes:
    - Stagnation point heating (Fay-Riddell correlation)
    - Convective heat transfer
    - Radiative equilibrium temperature
    - Transpiration cooling effectiveness

Author: Shane Brazelton
Date: 2025

Critical Design Points:
    - Nose cone stagnation: ~1000K at Mach 3.5
    - Max Q heating: Requires active cooling
    - Leading edges: Highest heat flux regions
"""

import math
from dataclasses import dataclass
from typing import Tuple, Optional
from .constants import Constants
from .atmosphere import Atmosphere


@dataclass
class ThermalState:
    """Thermal state at a point on the vehicle."""
    heat_flux: float  # W/m² (convective)
    heat_flux_radiative: float  # W/m² (to space)
    temperature_wall: float  # K
    temperature_stagnation: float  # K
    temperature_recovery: float  # K
    cooling_required: float  # W/m² (net heat to manage)


@dataclass
class MaterialProperties:
    """Thermal protection material properties."""
    name: str
    max_temperature: float  # K
    thermal_conductivity: float  # W/(m·K)
    specific_heat: float  # J/(kg·K)
    density: float  # kg/m³
    emissivity: float  # dimensionless


# Standard TPS Materials
TITANIUM_6AL4V = MaterialProperties(
    name="Ti-6Al-4V",
    max_temperature=870 + 273,  # ~870°C
    thermal_conductivity=6.7,
    specific_heat=526,
    density=4430,
    emissivity=0.6
)

INCONEL_718 = MaterialProperties(
    name="Inconel 718",
    max_temperature=980 + 273,  # ~980°C
    thermal_conductivity=11.4,
    specific_heat=435,
    density=8190,
    emissivity=0.7
)

CARBON_CARBON = MaterialProperties(
    name="Carbon-Carbon Composite",
    max_temperature=1650 + 273,  # ~1650°C
    thermal_conductivity=50,
    specific_heat=710,
    density=1750,
    emissivity=0.85
)

UHTC_HAFNIUM = MaterialProperties(
    name="HfC-SiC UHTC",
    max_temperature=2200 + 273,  # ~2200°C
    thermal_conductivity=20,
    specific_heat=400,
    density=12200,
    emissivity=0.9
)


class ThermalAnalyzer:
    """
    Aerothermal heating calculator for hypersonic flight.

    Implements engineering correlations for convective heating
    and thermal management system sizing.
    """

    def __init__(
        self,
        nose_radius: float = 0.5,  # m
        material: MaterialProperties = TITANIUM_6AL4V
    ):
        """
        Initialize thermal analyzer.

        Args:
            nose_radius: Effective nose radius for stagnation heating (m)
            material: TPS material properties
        """
        self.R_nose = nose_radius
        self.material = material

    def stagnation_temperature(self, T_inf: float, mach: float) -> float:
        """
        Calculate stagnation (total) temperature.

        T_0 = T_∞ × (1 + (γ-1)/2 × M²)

        Args:
            T_inf: Freestream static temperature (K)
            mach: Mach number

        Returns:
            Stagnation temperature (K)
        """
        gamma = Constants.GAMMA_AIR
        return T_inf * (1.0 + ((gamma - 1.0) / 2.0) * (mach ** 2))

    def recovery_temperature(self, T_inf: float, mach: float, r: float = 0.9) -> float:
        """
        Calculate recovery (adiabatic wall) temperature.

        T_r = T_∞ × (1 + r × (γ-1)/2 × M²)

        Args:
            T_inf: Freestream static temperature (K)
            mach: Mach number
            r: Recovery factor (0.85-0.9 for turbulent, 0.9-0.95 for laminar)

        Returns:
            Recovery temperature (K)
        """
        gamma = Constants.GAMMA_AIR
        return T_inf * (1.0 + r * ((gamma - 1.0) / 2.0) * (mach ** 2))

    def sutton_graves_heating(
        self,
        velocity: float,
        density: float,
        nose_radius: Optional[float] = None
    ) -> float:
        """
        Sutton-Graves stagnation point heating correlation.

        q = C × sqrt(ρ/R_n) × V³

        where C ≈ 1.83e-4 for air (SI units)

        This is an engineering approximation for rapid analysis.

        Args:
            velocity: Freestream velocity (m/s)
            density: Freestream density (kg/m³)
            nose_radius: Nose radius (m), uses default if None

        Returns:
            Stagnation point heat flux (W/m²)
        """
        R_n = nose_radius or self.R_nose
        C = 1.83e-4  # Sutton-Graves constant for air

        return C * math.sqrt(density / R_n) * (velocity ** 3)

    def fay_riddell_heating(
        self,
        velocity: float,
        altitude: float,
        wall_temperature: float,
        nose_radius: Optional[float] = None
    ) -> float:
        """
        Fay-Riddell stagnation point heating (more accurate).

        Accounts for:
        - Chemical equilibrium at stagnation point
        - Wall temperature effects
        - Dissociation at high temperatures

        Args:
            velocity: Freestream velocity (m/s)
            altitude: Altitude (m)
            wall_temperature: Wall temperature (K)
            nose_radius: Nose radius (m)

        Returns:
            Stagnation point heat flux (W/m²)
        """
        R_n = nose_radius or self.R_nose

        # Get atmospheric conditions
        atm = Atmosphere.get_conditions(altitude)
        rho = atm.density
        T_inf = atm.temperature
        mu = atm.viscosity

        # Stagnation conditions
        T_s = self.stagnation_temperature(T_inf, velocity / atm.speed_of_sound)

        # Fay-Riddell correlation (simplified form)
        # Full form requires chemical equilibrium calculations
        rho_s = rho * (T_inf / T_s) ** 0.5  # Approximate stagnation density

        # Heat transfer coefficient approximation
        # Based on Fay-Riddell for equilibrium air
        Pr = 0.71  # Prandtl number for air
        Le = 1.4   # Lewis number

        # Velocity gradient at stagnation point
        du_dx = velocity / R_n  # Newtonian approximation

        # Reference enthalpy
        h_0 = Constants.CP_AIR * T_s  # Total enthalpy approximation
        h_w = Constants.CP_AIR * wall_temperature  # Wall enthalpy

        # Heat flux (simplified Fay-Riddell)
        q = 0.763 * (Pr ** -0.6) * (rho_s * mu) ** 0.5 * (du_dx ** 0.5) * (h_0 - h_w)

        return max(0, q)

    def radiative_equilibrium_temperature(self, heat_flux: float) -> float:
        """
        Calculate radiative equilibrium temperature.

        At equilibrium: q_in = ε × σ × T⁴
        Therefore: T = (q / (ε × σ))^(1/4)

        Args:
            heat_flux: Incident heat flux (W/m²)

        Returns:
            Equilibrium temperature (K)
        """
        if heat_flux <= 0:
            return 200  # Minimum (space background)

        epsilon = self.material.emissivity
        sigma = Constants.STEFAN_BOLTZMANN

        return (heat_flux / (epsilon * sigma)) ** 0.25

    def net_heat_flux(
        self,
        incident_flux: float,
        wall_temperature: float
    ) -> float:
        """
        Calculate net heat flux (incident - radiated).

        q_net = q_incident - ε × σ × T_w⁴

        Args:
            incident_flux: Convective heat flux (W/m²)
            wall_temperature: Current wall temperature (K)

        Returns:
            Net heat flux into wall (W/m²)
        """
        q_radiated = (self.material.emissivity * Constants.STEFAN_BOLTZMANN *
                      (wall_temperature ** 4))
        return incident_flux - q_radiated

    def transpiration_cooling_effectiveness(
        self,
        mass_flow_rate: float,
        specific_heat_coolant: float,
        heat_flux_uncooled: float,
        area: float = 1.0
    ) -> float:
        """
        Estimate transpiration cooling effectiveness.

        Transpiration cooling injects coolant through a porous surface,
        creating a protective film and absorbing heat.

        η = 1 - exp(-m_dot × c_p / (h × A))

        Simplified model for preliminary design.

        Args:
            mass_flow_rate: Coolant mass flow rate (kg/s)
            specific_heat_coolant: Coolant specific heat (J/(kg·K))
            heat_flux_uncooled: Heat flux without cooling (W/m²)
            area: Cooled surface area (m²)

        Returns:
            Cooling effectiveness (0-1, where 1 = complete cooling)
        """
        if heat_flux_uncooled <= 0:
            return 1.0

        # Estimate heat transfer coefficient from heat flux
        # Assuming ΔT ~ 1000 K
        h = heat_flux_uncooled / 1000

        # Effectiveness
        exponent = mass_flow_rate * specific_heat_coolant / (h * area)
        return 1.0 - math.exp(-exponent)

    def analyze_trajectory_point(
        self,
        velocity: float,
        altitude: float,
        time: float,
        wall_temp_history: Optional[float] = None
    ) -> ThermalState:
        """
        Perform thermal analysis at a single trajectory point.

        Args:
            velocity: Current velocity (m/s)
            altitude: Current altitude (m)
            time: Mission elapsed time (s)
            wall_temp_history: Previous wall temperature for transient analysis

        Returns:
            ThermalState with complete thermal data
        """
        atm = Atmosphere.get_conditions(max(0, altitude))
        mach = velocity / atm.speed_of_sound if atm.speed_of_sound > 0 else 0

        # Temperature calculations
        T_stag = self.stagnation_temperature(atm.temperature, mach)
        T_rec = self.recovery_temperature(atm.temperature, mach)

        # Heat flux (Sutton-Graves for speed)
        q_conv = self.sutton_graves_heating(velocity, atm.density)

        # Wall temperature (equilibrium or transient)
        if wall_temp_history is None:
            T_wall = self.radiative_equilibrium_temperature(q_conv)
        else:
            # Simple transient model
            T_eq = self.radiative_equilibrium_temperature(q_conv)
            tau = 10.0  # Thermal time constant (s)
            T_wall = wall_temp_history + (T_eq - wall_temp_history) * (1 - math.exp(-1/tau))

        # Radiative heat loss
        q_rad = (self.material.emissivity * Constants.STEFAN_BOLTZMANN *
                 (T_wall ** 4))

        # Net cooling required
        q_net = max(0, q_conv - q_rad)

        return ThermalState(
            heat_flux=q_conv,
            heat_flux_radiative=q_rad,
            temperature_wall=T_wall,
            temperature_stagnation=T_stag,
            temperature_recovery=T_rec,
            cooling_required=q_net
        )


def analyze_tube_exit_heating():
    """
    Analyze thermal conditions at tube exit (critical design point).

    This is the "Jump" moment - exiting the evacuated tube at Mach 3.5
    into a partial vacuum environment.
    """
    print("=" * 60)
    print("TUBE EXIT THERMAL ANALYSIS")
    print("=" * 60)

    analyzer = ThermalAnalyzer(nose_radius=0.3)

    # Tube exit conditions
    exit_mach_values = [3.5, 4.0, 4.5, 5.0]
    tube_pressure_ratio = 0.1  # 0.1 atm inside tube

    print(f"\nTube pressure: {tube_pressure_ratio * 100}% atmosphere")
    print(f"Nose radius: {analyzer.R_nose} m")
    print()

    # Sea level conditions (tube at ground level)
    T_inf = 288.15  # K
    rho_std = 1.225  # kg/m³

    print(f"{'Mach':<8} {'V (m/s)':<10} {'T_stag (K)':<12} {'T_stag (°C)':<12} {'q (MW/m²)':<12}")
    print("-" * 54)

    for mach in exit_mach_values:
        a = 340.29  # Speed of sound at sea level
        velocity = mach * a

        # Density in tube
        rho = rho_std * tube_pressure_ratio

        # Stagnation temperature
        T_stag = analyzer.stagnation_temperature(T_inf, mach)

        # Heat flux (using tube density)
        q = analyzer.sutton_graves_heating(velocity, rho)

        print(f"{mach:<8.1f} {velocity:<10.0f} {T_stag:<12.0f} {T_stag-273:<12.0f} {q/1e6:<12.2f}")

    print()
    print("MATERIAL LIMITS:")
    for mat in [TITANIUM_6AL4V, INCONEL_718, CARBON_CARBON, UHTC_HAFNIUM]:
        print(f"  {mat.name}: {mat.max_temperature - 273:.0f}°C max")

    # Recommendation
    print()
    print("RECOMMENDATION:")
    print("  - At Mach 3.5, T_stag ≈ 721°C - Titanium edges feasible")
    print("  - Active transpiration cooling recommended for nose cone")
    print("  - Consider Inconel or C-C for Mach 4.5+ operations")


if __name__ == "__main__":
    analyze_tube_exit_heating()

    print("\n")

    # Trajectory analysis example
    print("=" * 60)
    print("SAMPLE TRAJECTORY THERMAL PROFILE")
    print("=" * 60)

    analyzer = ThermalAnalyzer(nose_radius=0.3, material=TITANIUM_6AL4V)

    # Sample trajectory points
    trajectory = [
        (1190, 8000),   # Tube exit
        (1500, 20000),  # Accelerating climb
        (2000, 35000),  # Near Max Q
        (2500, 50000),  # High altitude
        (3000, 70000),  # Exiting atmosphere
    ]

    print(f"\n{'Alt (km)':<10} {'V (m/s)':<10} {'Mach':<8} {'q (kW/m²)':<12} {'T_eq (°C)':<12}")
    print("-" * 52)

    for v, alt in trajectory:
        state = analyzer.analyze_trajectory_point(v, alt, 0)
        mach = v / Atmosphere.get_conditions(alt).speed_of_sound
        print(f"{alt/1000:<10.0f} {v:<10.0f} {mach:<8.1f} "
              f"{state.heat_flux/1000:<12.1f} {state.temperature_wall-273:<12.0f}")
