"""
Aerodynamic Force Calculations for BGKPJR Simulations

Implements comprehensive aerodynamic models covering:
    - Subsonic (M < 0.8): Standard incompressible with compressibility corrections
    - Transonic (0.8 < M < 1.2): Wave drag modeling
    - Supersonic (1.2 < M < 5): Ackeret/Linear theory
    - Hypersonic (M > 5): Newtonian impact theory

Includes:
    - Prandtl-Glauert compressibility correction
    - Ackeret linear supersonic theory
    - Modified Newtonian theory for hypersonic regime
    - Induced drag (drag due to lift) calculations
    - Reynolds number effects

Author: Shane Brazelton
Date: 2025

Mathematical Foundation:
    Lift:  L = 0.5 * ρ * V² * S * C_L
    Drag:  D = 0.5 * ρ * V² * S * C_D

    Where C_L and C_D are modified based on Mach number regime.
"""

import math
from dataclasses import dataclass
from typing import Tuple, Optional
from .constants import Constants
from .atmosphere import Atmosphere, AtmosphericConditions


@dataclass
class AeroCoefficients:
    """Aerodynamic coefficient container."""
    CL: float  # Lift coefficient
    CD: float  # Drag coefficient
    CM: float  # Pitching moment coefficient (about c/4)

    @property
    def L_D(self) -> float:
        """Lift-to-drag ratio."""
        if self.CD < 1e-10:
            return float('inf')
        return self.CL / self.CD


@dataclass
class AeroForceResult:
    """Complete aerodynamic force calculation result."""
    lift: float  # N
    drag: float  # N
    moment: float  # N·m (pitching moment)
    coefficients: AeroCoefficients
    mach: float
    reynolds: float
    dynamic_pressure: float  # Pa
    flight_regime: str


class AeroForces:
    """
    Comprehensive aerodynamic force calculator for the Gryphon spacecraft.

    Handles all flight regimes from subsonic tube exit to hypersonic
    atmospheric ascent.
    """

    # Regime boundaries
    MACH_SUBSONIC_LIMIT = 0.8
    MACH_TRANSONIC_LOW = 0.8
    MACH_TRANSONIC_HIGH = 1.2
    MACH_SUPERSONIC_LIMIT = 5.0

    def __init__(
        self,
        reference_area: float,
        reference_length: float,
        CD0: float = 0.015,
        CL_alpha: float = 0.05,  # per degree
        aspect_ratio: float = 2.5,
        oswald_efficiency: float = 0.8
    ):
        """
        Initialize aerodynamic model.

        Args:
            reference_area: Wing reference area (m²)
            reference_length: Characteristic length for Reynolds number (m)
            CD0: Zero-lift drag coefficient (parasitic drag)
            CL_alpha: Lift curve slope (per degree)
            aspect_ratio: Wing aspect ratio (b²/S)
            oswald_efficiency: Oswald span efficiency factor
        """
        self.S = reference_area
        self.L_ref = reference_length
        self.CD0 = CD0
        self.CL_alpha = CL_alpha  # per degree
        self.AR = aspect_ratio
        self.e = oswald_efficiency

        # Induced drag factor: k = 1 / (π * AR * e)
        self.k = 1.0 / (math.pi * self.AR * self.e)

    def determine_regime(self, mach: float) -> str:
        """Determine flight regime based on Mach number."""
        if mach < self.MACH_SUBSONIC_LIMIT:
            return "subsonic"
        elif mach < self.MACH_TRANSONIC_HIGH:
            return "transonic"
        elif mach < self.MACH_SUPERSONIC_LIMIT:
            return "supersonic"
        else:
            return "hypersonic"

    def prandtl_glauert_correction(self, mach: float) -> float:
        """
        Prandtl-Glauert compressibility correction factor.

        Valid for subsonic flow (M < ~0.8).
        C_L,comp = C_L,0 / sqrt(1 - M²)

        Args:
            mach: Mach number

        Returns:
            Correction factor (>1 for subsonic)
        """
        if mach >= 1.0:
            return 1.0

        beta_squared = 1.0 - mach ** 2
        if beta_squared <= 0.01:  # Avoid singularity near M=1
            beta_squared = 0.01

        return 1.0 / math.sqrt(beta_squared)

    def ackeret_CL(self, alpha_deg: float, mach: float) -> float:
        """
        Ackeret linear supersonic lift coefficient.

        C_L = 4α / sqrt(M² - 1)

        Valid for thin wings at moderate angles in supersonic flow.

        Args:
            alpha_deg: Angle of attack in degrees
            mach: Mach number (must be > 1)

        Returns:
            Lift coefficient
        """
        if mach <= 1.0:
            return 0.0

        alpha_rad = math.radians(alpha_deg)
        return 4.0 * alpha_rad / math.sqrt(mach ** 2 - 1.0)

    def ackeret_CD_wave(self, alpha_deg: float, mach: float, thickness_ratio: float = 0.05) -> float:
        """
        Ackeret wave drag coefficient for supersonic flow.

        C_D,wave = 4α² / sqrt(M² - 1) + (4/sqrt(M²-1)) * (t/c)²

        Args:
            alpha_deg: Angle of attack in degrees
            mach: Mach number (must be > 1)
            thickness_ratio: Thickness to chord ratio

        Returns:
            Wave drag coefficient
        """
        if mach <= 1.0:
            return 0.0

        alpha_rad = math.radians(alpha_deg)
        sqrt_term = math.sqrt(mach ** 2 - 1.0)

        # Wave drag due to angle of attack
        CD_alpha = 4.0 * (alpha_rad ** 2) / sqrt_term

        # Wave drag due to thickness
        CD_thickness = 4.0 * (thickness_ratio ** 2) / sqrt_term

        return CD_alpha + CD_thickness

    def newtonian_CL(self, alpha_deg: float) -> float:
        """
        Modified Newtonian lift coefficient for hypersonic flow.

        For a flat plate: C_L = 2 * sin²(α) * cos(α)
        Modified for lifting body: C_L ≈ C_p,max * sin(2α)

        Where C_p,max ≈ 1.84 for γ = 1.4 (stagnation pressure coefficient)

        Args:
            alpha_deg: Angle of attack in degrees

        Returns:
            Lift coefficient
        """
        alpha_rad = math.radians(alpha_deg)
        Cp_max = 1.84  # Modified Newtonian stagnation coefficient

        return Cp_max * (math.sin(alpha_rad) ** 2) * math.cos(alpha_rad)

    def newtonian_CD(self, alpha_deg: float) -> float:
        """
        Modified Newtonian drag coefficient for hypersonic flow.

        C_D = C_p,max * sin³(α) + C_D0

        Args:
            alpha_deg: Angle of attack in degrees

        Returns:
            Drag coefficient
        """
        alpha_rad = math.radians(alpha_deg)
        Cp_max = 1.84

        return Cp_max * (math.sin(alpha_rad) ** 3) + self.CD0

    def calculate_coefficients(
        self,
        alpha_deg: float,
        mach: float,
        reynolds: Optional[float] = None
    ) -> AeroCoefficients:
        """
        Calculate aerodynamic coefficients for given flight conditions.

        Automatically selects appropriate theory based on Mach number.

        Args:
            alpha_deg: Angle of attack in degrees
            mach: Mach number
            reynolds: Reynolds number (optional, for skin friction corrections)

        Returns:
            AeroCoefficients dataclass
        """
        regime = self.determine_regime(mach)

        if regime == "subsonic":
            # Standard lift curve with Prandtl-Glauert correction
            correction = self.prandtl_glauert_correction(mach)
            CL = self.CL_alpha * alpha_deg * correction

            # Induced drag
            CD_induced = self.k * (CL ** 2)
            CD = self.CD0 + CD_induced

        elif regime == "transonic":
            # Interpolate between subsonic and supersonic
            # Add wave drag rise
            fraction = (mach - self.MACH_TRANSONIC_LOW) / (self.MACH_TRANSONIC_HIGH - self.MACH_TRANSONIC_LOW)

            # Subsonic component
            CL_sub = self.CL_alpha * alpha_deg * self.prandtl_glauert_correction(0.8)
            CD_sub = self.CD0 + self.k * (CL_sub ** 2)

            # Supersonic component (at M = 1.2)
            CL_sup = self.ackeret_CL(alpha_deg, 1.2)
            CD_sup = self.CD0 + self.ackeret_CD_wave(alpha_deg, 1.2)

            # Wave drag rise (peaks near M = 1)
            wave_drag_rise = 0.15 * math.sin(math.pi * fraction)  # Empirical transonic drag rise

            CL = CL_sub * (1 - fraction) + CL_sup * fraction
            CD = CD_sub * (1 - fraction) + CD_sup * fraction + wave_drag_rise

        elif regime == "supersonic":
            # Ackeret linear theory
            CL = self.ackeret_CL(alpha_deg, mach)
            CD = self.CD0 + self.ackeret_CD_wave(alpha_deg, mach)

        else:  # hypersonic
            # Modified Newtonian theory
            CL = self.newtonian_CL(alpha_deg)
            CD = self.newtonian_CD(alpha_deg)

        # Simple pitching moment estimate (nose-down tendency increases with alpha)
        CM = -0.01 * alpha_deg

        return AeroCoefficients(CL=CL, CD=CD, CM=CM)

    def calculate_forces(
        self,
        velocity: float,
        altitude: float,
        alpha_deg: float,
        atmosphere: Optional[AtmosphericConditions] = None
    ) -> AeroForceResult:
        """
        Calculate complete aerodynamic forces.

        Args:
            velocity: True airspeed in m/s
            altitude: Geometric altitude in meters
            alpha_deg: Angle of attack in degrees
            atmosphere: Pre-computed atmospheric conditions (optional)

        Returns:
            AeroForceResult with all force and coefficient data
        """
        # Get atmospheric conditions
        if atmosphere is None:
            atm = Atmosphere.get_conditions(altitude)
        else:
            atm = atmosphere

        # Mach and Reynolds numbers
        mach = velocity / atm.speed_of_sound
        reynolds = (atm.density * velocity * self.L_ref) / atm.viscosity

        # Dynamic pressure
        q = 0.5 * atm.density * (velocity ** 2)

        # Get coefficients
        coeffs = self.calculate_coefficients(alpha_deg, mach, reynolds)

        # Calculate forces
        lift = q * self.S * coeffs.CL
        drag = q * self.S * coeffs.CD
        moment = q * self.S * self.L_ref * coeffs.CM

        return AeroForceResult(
            lift=lift,
            drag=drag,
            moment=moment,
            coefficients=coeffs,
            mach=mach,
            reynolds=reynolds,
            dynamic_pressure=q,
            flight_regime=self.determine_regime(mach)
        )


def calculate_stagnation_temperature(freestream_temp: float, mach: float) -> float:
    """
    Calculate stagnation (total) temperature.

    T_0 = T_∞ * (1 + (γ-1)/2 * M²)

    Critical for thermal protection system design.

    Args:
        freestream_temp: Freestream static temperature (K)
        mach: Mach number

    Returns:
        Stagnation temperature (K)
    """
    gamma = Constants.GAMMA_AIR
    return freestream_temp * (1.0 + ((gamma - 1.0) / 2.0) * (mach ** 2))


def calculate_stagnation_pressure(freestream_pressure: float, mach: float) -> float:
    """
    Calculate stagnation (total) pressure.

    Uses isentropic relation for subsonic, normal shock relations for supersonic.

    Args:
        freestream_pressure: Freestream static pressure (Pa)
        mach: Mach number

    Returns:
        Stagnation pressure (Pa)
    """
    gamma = Constants.GAMMA_AIR

    if mach < 1.0:
        # Isentropic: P_0/P_∞ = (1 + (γ-1)/2 * M²)^(γ/(γ-1))
        ratio = (1.0 + ((gamma - 1.0) / 2.0) * (mach ** 2)) ** (gamma / (gamma - 1.0))
    else:
        # Behind normal shock (Rayleigh pitot formula)
        term1 = ((gamma + 1.0) ** 2 * mach ** 2) / (4.0 * gamma * mach ** 2 - 2.0 * (gamma - 1.0))
        term2 = (1.0 - gamma + 2.0 * gamma * mach ** 2) / (gamma + 1.0)
        ratio = (term1 ** (gamma / (gamma - 1.0))) * (term2 ** (1.0 / (gamma - 1.0)))

    return freestream_pressure * ratio


if __name__ == "__main__":
    # Validation tests
    print("=== BGKPJR Aerodynamics Model Validation ===\n")

    # Create Gryphon aerodynamics model
    gryphon = AeroForces(
        reference_area=120.0,  # m²
        reference_length=25.0,  # m
        CD0=0.015,
        CL_alpha=0.05,
        aspect_ratio=2.5,
        oswald_efficiency=0.8
    )

    # Test at various Mach numbers
    alpha = 10.0  # degrees
    altitude = 30000  # m

    print(f"Test conditions: α = {alpha}°, altitude = {altitude/1000:.0f} km")
    print("-" * 90)
    print(f"{'Mach':<8} {'Regime':<12} {'CL':<10} {'CD':<10} {'L/D':<10} {'Lift (kN)':<12} {'Drag (kN)':<12}")
    print("-" * 90)

    for mach in [0.3, 0.7, 0.95, 1.5, 2.5, 3.5, 5.0, 7.0]:
        atm = Atmosphere.get_conditions(altitude)
        velocity = mach * atm.speed_of_sound

        result = gryphon.calculate_forces(velocity, altitude, alpha)

        print(f"{mach:<8.1f} {result.flight_regime:<12} {result.coefficients.CL:<10.4f} "
              f"{result.coefficients.CD:<10.4f} {result.coefficients.L_D:<10.2f} "
              f"{result.lift/1000:<12.1f} {result.drag/1000:<12.1f}")

    # Stagnation temperature analysis
    print("\n" + "=" * 60)
    print("\nStagnation Temperature Analysis (Sea Level Exit):")
    print("-" * 60)

    T_inf = 288.15  # K
    for mach in [3.5, 4.0, 5.0, 6.0]:
        T_stag = calculate_stagnation_temperature(T_inf, mach)
        print(f"Mach {mach:.1f}: T_stagnation = {T_stag:.0f} K ({T_stag - 273.15:.0f}°C)")
