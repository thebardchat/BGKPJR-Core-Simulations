"""
Gryphon Spacecraft Model for BGKPJR Simulations

Defines the Gryphon lifting body spacecraft including:
    - Mass properties and propellant tracking
    - Variable geometry wing configuration
    - Thrust and propulsion modeling
    - State vector management

Author: Shane Brazelton
Date: 2025
"""

import math
from dataclasses import dataclass, field
from typing import Tuple, Optional
from enum import Enum
from .constants import Constants, SystemParams, DEFAULT_PARAMS


class FlightPhase(Enum):
    """Gryphon flight phases."""
    TUBE_ACCELERATION = "tube_acceleration"
    ATMOSPHERIC_ASCENT = "atmospheric_ascent"
    EXOATMOSPHERIC = "exoatmospheric"
    ORBITAL = "orbital"
    REENTRY = "reentry"
    GLIDE_RETURN = "glide_return"


class WingConfiguration(Enum):
    """Wing deployment states."""
    RETRACTED = "retracted"  # During tube transit
    DEPLOYED = "deployed"     # Atmospheric flight
    PARTIAL = "partial"       # Transition state


@dataclass
class VehicleState:
    """Complete vehicle state vector."""
    # Position (Earth-fixed frame)
    x: float = 0.0  # m (downrange)
    y: float = 0.0  # m (crossrange)
    z: float = 0.0  # m (altitude)

    # Velocity (Earth-fixed frame)
    vx: float = 0.0  # m/s
    vy: float = 0.0  # m/s
    vz: float = 0.0  # m/s

    # Attitude (body frame)
    pitch: float = 0.0  # rad
    yaw: float = 0.0    # rad
    roll: float = 0.0   # rad

    # Angular rates
    pitch_rate: float = 0.0  # rad/s
    yaw_rate: float = 0.0    # rad/s
    roll_rate: float = 0.0   # rad/s

    # Mass
    mass: float = 50000.0  # kg (total)

    # Time
    time: float = 0.0  # s

    @property
    def altitude(self) -> float:
        """Alias for z coordinate."""
        return self.z

    @property
    def velocity_magnitude(self) -> float:
        """Total velocity magnitude."""
        return math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)

    @property
    def flight_path_angle(self) -> float:
        """Flight path angle (gamma) in radians."""
        v_horizontal = math.sqrt(self.vx**2 + self.vy**2)
        if v_horizontal < 1e-10:
            return math.pi / 2 if self.vz > 0 else -math.pi / 2
        return math.atan2(self.vz, v_horizontal)

    @property
    def heading(self) -> float:
        """Heading angle in radians (from North)."""
        return math.atan2(self.vx, self.vy)

    def to_tuple(self) -> Tuple[float, ...]:
        """Convert to tuple for ODE integrators."""
        return (self.x, self.y, self.z, self.vx, self.vy, self.vz,
                self.pitch, self.yaw, self.roll,
                self.pitch_rate, self.yaw_rate, self.roll_rate, self.mass)


class GryphonVehicle:
    """
    Gryphon Spacecraft model.

    A stealth-inspired blended wing body designed for hypersonic
    atmospheric flight and orbital insertion.
    """

    def __init__(self, params: Optional[SystemParams] = None):
        """
        Initialize Gryphon vehicle.

        Args:
            params: System parameters (uses defaults if None)
        """
        self.params = params or DEFAULT_PARAMS

        # Mass properties
        self.mass_dry = self.params.GRYPHON_MASS_DRY
        self.mass_payload = self.params.GRYPHON_MASS_PAYLOAD
        self.mass_propellant_initial = self.params.GRYPHON_MASS_PROPELLANT
        self.mass_propellant = self.mass_propellant_initial

        # Geometry
        self.wing_area_deployed = self.params.GRYPHON_WING_AREA
        self.wing_area_retracted = self.params.GRYPHON_WING_AREA_RETRACTED
        self.length = self.params.GRYPHON_LENGTH

        # Aerodynamic coefficients
        self.CD0 = self.params.GRYPHON_CD0
        self.CL_alpha = self.params.GRYPHON_CL_ALPHA

        # Propulsion
        self.isp_vacuum = self.params.ISP_VACUUM
        self.isp_sea_level = self.params.ISP_SEA_LEVEL
        self.thrust_max = self.params.THRUST_MAX

        # Current configuration
        self.wing_config = WingConfiguration.RETRACTED
        self.flight_phase = FlightPhase.TUBE_ACCELERATION
        self.throttle = 0.0  # 0.0 to 1.0

        # Initialize state
        self.state = VehicleState(mass=self.total_mass)

    @property
    def total_mass(self) -> float:
        """Current total mass."""
        return self.mass_dry + self.mass_payload + self.mass_propellant

    @property
    def mass_empty(self) -> float:
        """Mass after all propellant expended."""
        return self.mass_dry + self.mass_payload

    @property
    def propellant_fraction(self) -> float:
        """Current propellant mass fraction."""
        return self.mass_propellant / self.total_mass

    @property
    def wing_area(self) -> float:
        """Current effective wing area based on configuration."""
        if self.wing_config == WingConfiguration.RETRACTED:
            return self.wing_area_retracted
        elif self.wing_config == WingConfiguration.DEPLOYED:
            return self.wing_area_deployed
        else:  # PARTIAL
            return (self.wing_area_retracted + self.wing_area_deployed) / 2

    def deploy_wings(self):
        """Deploy wings for atmospheric flight."""
        self.wing_config = WingConfiguration.DEPLOYED

    def retract_wings(self):
        """Retract wings for tube transit or reentry."""
        self.wing_config = WingConfiguration.RETRACTED

    def get_isp(self, altitude: float) -> float:
        """
        Get specific impulse adjusted for ambient pressure.

        Linear interpolation between sea level and vacuum values.

        Args:
            altitude: Current altitude in meters

        Returns:
            Effective Isp in seconds
        """
        # Approximate scale height for pressure
        scale_height = 8500.0  # m
        pressure_ratio = math.exp(-altitude / scale_height)

        # Interpolate between sea level and vacuum Isp
        return self.isp_vacuum - (self.isp_vacuum - self.isp_sea_level) * pressure_ratio

    def get_thrust(self, altitude: float) -> float:
        """
        Get current thrust output.

        Args:
            altitude: Current altitude in meters

        Returns:
            Thrust in Newtons
        """
        if self.mass_propellant <= 0 or self.throttle <= 0:
            return 0.0

        # Thrust increases slightly with altitude due to nozzle expansion
        # Simplified model: assume constant thrust
        return self.thrust_max * self.throttle

    def get_mass_flow_rate(self, altitude: float) -> float:
        """
        Calculate propellant mass flow rate.

        mdot = Thrust / (Isp * g0)

        Args:
            altitude: Current altitude in meters

        Returns:
            Mass flow rate in kg/s
        """
        thrust = self.get_thrust(altitude)
        if thrust <= 0:
            return 0.0

        isp = self.get_isp(altitude)
        return thrust / (isp * Constants.G0)

    def update_mass(self, dt: float, altitude: float):
        """
        Update vehicle mass based on propellant consumption.

        Args:
            dt: Time step in seconds
            altitude: Current altitude in meters
        """
        mdot = self.get_mass_flow_rate(altitude)
        mass_consumed = mdot * dt

        self.mass_propellant = max(0.0, self.mass_propellant - mass_consumed)
        self.state.mass = self.total_mass

    def set_throttle(self, throttle: float):
        """
        Set engine throttle.

        Args:
            throttle: Throttle setting 0.0 to 1.0
        """
        self.throttle = max(0.0, min(1.0, throttle))

    def set_flight_phase(self, phase: FlightPhase):
        """Update flight phase and adjust configuration."""
        self.flight_phase = phase

        if phase == FlightPhase.TUBE_ACCELERATION:
            self.wing_config = WingConfiguration.RETRACTED
        elif phase in [FlightPhase.ATMOSPHERIC_ASCENT, FlightPhase.GLIDE_RETURN]:
            self.wing_config = WingConfiguration.DEPLOYED
        elif phase == FlightPhase.REENTRY:
            self.wing_config = WingConfiguration.RETRACTED

    def calculate_delta_v_remaining(self) -> float:
        """
        Calculate remaining delta-v capability.

        Returns:
            Remaining delta-v in m/s
        """
        if self.mass_propellant <= 0:
            return 0.0

        mass_final = self.mass_empty
        mass_initial = self.total_mass

        return self.isp_vacuum * Constants.G0 * math.log(mass_initial / mass_final)

    def calculate_delta_v_expended(self) -> float:
        """
        Calculate delta-v already expended.

        Returns:
            Expended delta-v in m/s
        """
        if self.mass_propellant >= self.mass_propellant_initial:
            return 0.0

        mass_initial = self.mass_empty + self.mass_propellant_initial
        mass_current = self.total_mass

        return self.isp_vacuum * Constants.G0 * math.log(mass_initial / mass_current)

    def get_inertia_tensor(self) -> Tuple[float, float, float]:
        """
        Estimate moments of inertia (simplified model).

        Assumes uniform density distribution for lifting body shape.

        Returns:
            (Ixx, Iyy, Izz) in kg·m²
        """
        # Simplified lifting body inertia estimates
        # Based on characteristic dimensions
        m = self.total_mass
        L = self.length
        W = math.sqrt(self.wing_area)  # Approximate wingspan

        # Roll (about x-axis)
        Ixx = m * (W ** 2) / 12

        # Pitch (about y-axis)
        Iyy = m * (L ** 2) / 12

        # Yaw (about z-axis)
        Izz = m * (L ** 2 + W ** 2) / 12

        return (Ixx, Iyy, Izz)

    def status_report(self) -> str:
        """Generate human-readable status report."""
        lines = [
            "=" * 50,
            "GRYPHON VEHICLE STATUS",
            "=" * 50,
            f"Flight Phase: {self.flight_phase.value}",
            f"Wing Configuration: {self.wing_config.value}",
            "",
            "MASS PROPERTIES:",
            f"  Total Mass: {self.total_mass:.0f} kg",
            f"  Propellant: {self.mass_propellant:.0f} kg ({self.propellant_fraction*100:.1f}%)",
            f"  Dry + Payload: {self.mass_empty:.0f} kg",
            "",
            "PROPULSION:",
            f"  Throttle: {self.throttle*100:.0f}%",
            f"  Thrust: {self.get_thrust(0)/1000:.1f} kN",
            f"  Isp (vacuum): {self.isp_vacuum:.0f} s",
            "",
            "PERFORMANCE:",
            f"  Delta-V Remaining: {self.calculate_delta_v_remaining():.0f} m/s",
            f"  Delta-V Expended: {self.calculate_delta_v_expended():.0f} m/s",
            "",
            "STATE:",
            f"  Altitude: {self.state.altitude/1000:.2f} km",
            f"  Velocity: {self.state.velocity_magnitude:.1f} m/s",
            f"  Flight Path Angle: {math.degrees(self.state.flight_path_angle):.1f}°",
            "=" * 50,
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    # Test vehicle model
    print("=== Gryphon Vehicle Model Test ===\n")

    gryphon = GryphonVehicle()
    print(gryphon.status_report())

    # Test propellant burn
    print("\n--- Simulating 60s burn at full throttle ---\n")
    gryphon.set_throttle(1.0)
    gryphon.state.z = 30000  # 30 km altitude

    for t in range(0, 61, 10):
        if t > 0:
            gryphon.update_mass(10.0, gryphon.state.z)
        print(f"t = {t:3d}s: mass = {gryphon.total_mass:.0f} kg, "
              f"prop = {gryphon.mass_propellant:.0f} kg, "
              f"Δv_remaining = {gryphon.calculate_delta_v_remaining():.0f} m/s")
