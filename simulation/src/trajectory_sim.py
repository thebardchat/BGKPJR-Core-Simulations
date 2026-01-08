"""
Trajectory Simulation for BGKPJR Launch System

Integrates equations of motion for complete mission profile:
    1. Maglev tube acceleration (handled by MaglevTrack)
    2. Atmospheric ascent with aerodynamic forces
    3. Exoatmospheric coast and burn phases
    4. Orbital insertion

Uses 3-DOF (point mass) model with:
    - Gravity (altitude-dependent)
    - Aerodynamic lift and drag
    - Thrust (variable with altitude)

Author: Shane Brazelton
Date: 2025
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable
from .constants import Constants, SystemParams, DEFAULT_PARAMS
from .atmosphere import Atmosphere
from .aerodynamics import AeroForces, calculate_stagnation_temperature
from .vehicle import GryphonVehicle, VehicleState, FlightPhase
from .maglev import MaglevTrack, LaunchResult


@dataclass
class TrajectoryPoint:
    """Single point along trajectory."""
    time: float  # s
    x: float  # m (downrange)
    z: float  # m (altitude)
    vx: float  # m/s
    vz: float  # m/s
    mass: float  # kg
    mach: float
    dynamic_pressure: float  # Pa
    g_load: float  # g
    temperature_stagnation: float  # K
    flight_phase: str


@dataclass
class MissionResult:
    """Complete mission simulation result."""
    trajectory: List[TrajectoryPoint]
    final_altitude: float
    final_velocity: float
    final_orbital_velocity: float
    max_q: float  # Maximum dynamic pressure
    max_q_altitude: float
    max_g: float
    max_temperature: float
    propellant_used: float
    time_to_orbit: float
    success: bool
    failure_reason: str = ""

    def to_arrays(self) -> dict:
        """Convert trajectory to numpy arrays for plotting."""
        return {
            'time': np.array([p.time for p in self.trajectory]),
            'altitude': np.array([p.z for p in self.trajectory]) / 1000,  # km
            'downrange': np.array([p.x for p in self.trajectory]) / 1000,  # km
            'velocity': np.array([math.sqrt(p.vx**2 + p.vz**2) for p in self.trajectory]),
            'mach': np.array([p.mach for p in self.trajectory]),
            'dynamic_pressure': np.array([p.dynamic_pressure for p in self.trajectory]) / 1000,  # kPa
            'g_load': np.array([p.g_load for p in self.trajectory]),
            'temperature': np.array([p.temperature_stagnation for p in self.trajectory]),
        }


class TrajectorySimulator:
    """
    3-DOF trajectory simulator for BGKPJR launch system.

    Simulates planar (2D) trajectory with:
    - Downrange (x) and altitude (z) position
    - Gravity varying with altitude
    - Aerodynamic forces from AeroForces module
    - Propulsion from GryphonVehicle module
    """

    def __init__(
        self,
        vehicle: Optional[GryphonVehicle] = None,
        track: Optional[MaglevTrack] = None,
        params: Optional[SystemParams] = None
    ):
        """
        Initialize trajectory simulator.

        Args:
            vehicle: Gryphon spacecraft model
            track: Maglev launch track model
            params: System parameters
        """
        self.params = params or DEFAULT_PARAMS
        self.vehicle = vehicle or GryphonVehicle(self.params)
        self.track = track or MaglevTrack(params=self.params)

        # Aerodynamics model
        self.aero = AeroForces(
            reference_area=self.vehicle.wing_area_deployed,
            reference_length=self.vehicle.length,
            CD0=self.vehicle.CD0,
            CL_alpha=self.vehicle.CL_alpha
        )

        # Simulation settings
        self.dt = 0.1  # Time step (s)
        self.max_time = 600.0  # Maximum simulation time (s)

        # Guidance parameters
        self.target_altitude = self.params.LEO_ALTITUDE
        self.target_velocity = self.params.ORBITAL_VELOCITY_LEO

    def gravity(self, altitude: float) -> float:
        """
        Calculate gravitational acceleration at altitude.

        g(h) = g0 * (R_E / (R_E + h))²

        Args:
            altitude: Altitude above sea level in meters

        Returns:
            Gravitational acceleration in m/s²
        """
        R = Constants.EARTH_RADIUS
        return Constants.G0 * (R / (R + altitude)) ** 2

    def equations_of_motion(
        self,
        state: np.ndarray,
        alpha_deg: float,
        throttle: float
    ) -> np.ndarray:
        """
        Compute state derivatives (equations of motion).

        State vector: [x, z, vx, vz, mass]

        Args:
            state: Current state vector
            alpha_deg: Angle of attack (degrees)
            throttle: Engine throttle (0-1)

        Returns:
            State derivatives [dx, dz, dvx, dvz, dmass]
        """
        x, z, vx, vz, mass = state

        # Velocity magnitude and flight path angle
        v = math.sqrt(vx**2 + vz**2)
        if v < 1e-6:
            gamma = math.radians(self.track.geometry.incline_angle)
        else:
            gamma = math.atan2(vz, vx)

        # Atmospheric conditions
        atm = Atmosphere.get_conditions(max(0, z))
        rho = atm.density
        a_sound = atm.speed_of_sound

        # Mach number
        mach = v / a_sound if a_sound > 0 else 0

        # Gravity
        g = self.gravity(z)

        # Aerodynamic forces (only if in atmosphere with significant density)
        if rho > 1e-10 and v > 1:
            # Update aero reference area based on wing configuration
            self.aero.S = self.vehicle.wing_area

            result = self.aero.calculate_forces(v, z, alpha_deg, atm)
            lift = result.lift
            drag = result.drag
        else:
            lift = 0
            drag = 0

        # Thrust
        self.vehicle.set_throttle(throttle)
        thrust = self.vehicle.get_thrust(z)

        # Thrust direction (along velocity vector + pitch adjustment)
        thrust_angle = gamma + math.radians(alpha_deg)

        # Mass flow rate
        mdot = self.vehicle.get_mass_flow_rate(z)

        # Forces in x and z directions
        # Drag opposes velocity, lift perpendicular to velocity
        Fx = thrust * math.cos(thrust_angle) - drag * math.cos(gamma) - lift * math.sin(gamma)
        Fz = thrust * math.sin(thrust_angle) - drag * math.sin(gamma) + lift * math.cos(gamma) - mass * g

        # Accelerations
        ax = Fx / mass
        az = Fz / mass

        # State derivatives
        return np.array([vx, vz, ax, az, -mdot])

    def simple_guidance(
        self,
        state: np.ndarray,
        phase: FlightPhase,
        time: float
    ) -> Tuple[float, float]:
        """
        Simple open-loop guidance for initial testing.

        Returns angle of attack and throttle based on flight phase.

        Args:
            state: Current state vector [x, z, vx, vz, mass]
            phase: Current flight phase
            time: Mission elapsed time

        Returns:
            (alpha_deg, throttle)
        """
        x, z, vx, vz, mass = state
        v = math.sqrt(vx**2 + vz**2)
        gamma = math.degrees(math.atan2(vz, vx)) if v > 1 else 30

        if phase == FlightPhase.ATMOSPHERIC_ASCENT:
            # Gravity turn with slight pitch up
            # Start at track exit angle, gradually reduce
            alpha = max(5, 15 - time * 0.1)
            throttle = 1.0

        elif phase == FlightPhase.EXOATMOSPHERIC:
            # Coast or burn to circularize
            if z < self.target_altitude * 0.9:
                alpha = 0  # Nose on velocity vector
                throttle = 1.0
            else:
                # Circularization burn (horizontal)
                alpha = -gamma  # Point horizontal
                v_horizontal = vx
                if v_horizontal < self.target_velocity * 0.95:
                    throttle = 1.0
                else:
                    throttle = 0.0
                alpha = 0

        else:
            alpha = 0
            throttle = 0

        return alpha, throttle

    def determine_phase(self, z: float, vz: float, mach: float, rho: float) -> FlightPhase:
        """
        Determine current flight phase based on state.

        Args:
            z: Altitude (m)
            vz: Vertical velocity (m/s)
            mach: Mach number
            rho: Air density (kg/m³)

        Returns:
            Current FlightPhase
        """
        KARMAN_LINE = 100000  # m

        if z < KARMAN_LINE and rho > 1e-8:
            return FlightPhase.ATMOSPHERIC_ASCENT
        elif z >= KARMAN_LINE or rho <= 1e-8:
            return FlightPhase.EXOATMOSPHERIC
        else:
            return FlightPhase.ATMOSPHERIC_ASCENT

    def run_simulation(
        self,
        guidance: Optional[Callable] = None,
        record_interval: float = 1.0
    ) -> MissionResult:
        """
        Run complete mission simulation.

        Args:
            guidance: Custom guidance function (uses simple_guidance if None)
            record_interval: Time interval between trajectory records (s)

        Returns:
            MissionResult with complete trajectory data
        """
        if guidance is None:
            guidance = self.simple_guidance

        # Phase 1: Maglev Launch
        launch_result = self.track.simulate_launch(self.vehicle.total_mass)

        if not launch_result.success:
            return MissionResult(
                trajectory=[],
                final_altitude=0,
                final_velocity=0,
                final_orbital_velocity=0,
                max_q=0, max_q_altitude=0,
                max_g=launch_result.peak_g_force,
                max_temperature=0,
                propellant_used=0,
                time_to_orbit=0,
                success=False,
                failure_reason=f"Launch failed: {launch_result.notes}"
            )

        # Initialize state from track exit
        track_angle_rad = math.radians(self.track.geometry.incline_angle)
        x0 = self.track.geometry.horizontal_distance
        z0 = launch_result.exit_altitude
        vx0 = launch_result.exit_velocity * math.cos(track_angle_rad)
        vz0 = launch_result.exit_velocity * math.sin(track_angle_rad)
        mass0 = self.vehicle.total_mass

        state = np.array([x0, z0, vx0, vz0, mass0])

        # Deploy wings for atmospheric flight
        self.vehicle.deploy_wings()
        self.vehicle.set_flight_phase(FlightPhase.ATMOSPHERIC_ASCENT)

        # Trajectory storage
        trajectory = []
        time = launch_result.time_in_tube
        last_record = 0

        # Tracking variables
        max_q = 0
        max_q_alt = 0
        max_g = launch_result.peak_g_force
        max_temp = 0
        initial_propellant = self.vehicle.mass_propellant

        # Phase 2 & 3: Atmospheric and Exoatmospheric Flight
        while time < self.max_time:
            x, z, vx, vz, mass = state
            v = math.sqrt(vx**2 + vz**2)

            # Check termination conditions
            if z < 0:
                return MissionResult(
                    trajectory=trajectory,
                    final_altitude=z,
                    final_velocity=v,
                    final_orbital_velocity=vx,
                    max_q=max_q, max_q_altitude=max_q_alt,
                    max_g=max_g,
                    max_temperature=max_temp,
                    propellant_used=initial_propellant - self.vehicle.mass_propellant,
                    time_to_orbit=time,
                    success=False,
                    failure_reason="Vehicle impacted surface"
                )

            if z > self.target_altitude and vx > self.target_velocity * 0.95:
                # Success! Reached target orbit
                return MissionResult(
                    trajectory=trajectory,
                    final_altitude=z,
                    final_velocity=v,
                    final_orbital_velocity=vx,
                    max_q=max_q, max_q_altitude=max_q_alt,
                    max_g=max_g,
                    max_temperature=max_temp,
                    propellant_used=initial_propellant - self.vehicle.mass_propellant,
                    time_to_orbit=time,
                    success=True
                )

            # Atmospheric conditions
            atm = Atmosphere.get_conditions(max(0, z))
            mach = v / atm.speed_of_sound if atm.speed_of_sound > 0 else 0
            q = 0.5 * atm.density * v**2
            T_stag = calculate_stagnation_temperature(atm.temperature, mach)

            # Update tracking
            if q > max_q:
                max_q = q
                max_q_alt = z

            max_temp = max(max_temp, T_stag)

            # Determine flight phase
            phase = self.determine_phase(z, vz, mach, atm.density)
            self.vehicle.set_flight_phase(phase)

            # Get guidance commands
            alpha, throttle = guidance(state, phase, time)

            # Record trajectory point
            if time - last_record >= record_interval:
                # Calculate g-load
                derivs = self.equations_of_motion(state, alpha, throttle)
                g_load = math.sqrt(derivs[2]**2 + (derivs[3] + self.gravity(z))**2) / Constants.G0
                max_g = max(max_g, g_load)

                trajectory.append(TrajectoryPoint(
                    time=time,
                    x=x, z=z,
                    vx=vx, vz=vz,
                    mass=mass,
                    mach=mach,
                    dynamic_pressure=q,
                    g_load=g_load,
                    temperature_stagnation=T_stag,
                    flight_phase=phase.value
                ))
                last_record = time

            # Integration (RK4)
            k1 = self.equations_of_motion(state, alpha, throttle)
            k2 = self.equations_of_motion(state + 0.5*self.dt*k1, alpha, throttle)
            k3 = self.equations_of_motion(state + 0.5*self.dt*k2, alpha, throttle)
            k4 = self.equations_of_motion(state + self.dt*k3, alpha, throttle)

            state = state + (self.dt/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Update vehicle mass
            self.vehicle.mass_propellant = max(0, state[4] - self.vehicle.mass_empty)
            self.vehicle.state.mass = state[4]

            time += self.dt

        # Timeout
        return MissionResult(
            trajectory=trajectory,
            final_altitude=state[1],
            final_velocity=math.sqrt(state[2]**2 + state[3]**2),
            final_orbital_velocity=state[2],
            max_q=max_q, max_q_altitude=max_q_alt,
            max_g=max_g,
            max_temperature=max_temp,
            propellant_used=initial_propellant - self.vehicle.mass_propellant,
            time_to_orbit=time,
            success=False,
            failure_reason="Simulation timeout"
        )


def print_mission_summary(result: MissionResult):
    """Print formatted mission summary."""
    print("=" * 60)
    print("MISSION SIMULATION RESULTS")
    print("=" * 60)
    print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
    if not result.success:
        print(f"Failure Reason: {result.failure_reason}")
    print()
    print("FINAL STATE:")
    print(f"  Altitude: {result.final_altitude/1000:.1f} km")
    print(f"  Total Velocity: {result.final_velocity:.0f} m/s")
    print(f"  Orbital Velocity: {result.final_orbital_velocity:.0f} m/s")
    print(f"  Time to Orbit: {result.time_to_orbit:.1f} s ({result.time_to_orbit/60:.1f} min)")
    print()
    print("PEAK VALUES:")
    print(f"  Max Q: {result.max_q/1000:.1f} kPa at {result.max_q_altitude/1000:.1f} km")
    print(f"  Max G-Load: {result.max_g:.1f} g")
    print(f"  Max Stagnation Temp: {result.max_temperature:.0f} K ({result.max_temperature-273:.0f}°C)")
    print()
    print("PROPULSION:")
    print(f"  Propellant Used: {result.propellant_used:.0f} kg")
    print("=" * 60)


if __name__ == "__main__":
    print("=== BGKPJR Trajectory Simulation ===\n")

    # Create simulator
    sim = TrajectorySimulator()

    # Print initial configuration
    sim.track.print_track_summary()
    print()
    print(sim.vehicle.status_report())

    # Run simulation
    print("\n--- Running Mission Simulation ---\n")
    result = sim.run_simulation()

    # Print results
    print_mission_summary(result)

    # Save trajectory data
    if result.trajectory:
        print(f"\nTrajectory recorded: {len(result.trajectory)} points")
        print("Sample points:")
        for i in [0, len(result.trajectory)//4, len(result.trajectory)//2,
                  3*len(result.trajectory)//4, -1]:
            p = result.trajectory[i]
            print(f"  t={p.time:6.1f}s: alt={p.z/1000:7.1f}km, "
                  f"v={math.sqrt(p.vx**2+p.vz**2):7.0f}m/s, M={p.mach:.2f}, "
                  f"q={p.dynamic_pressure/1000:.1f}kPa")
