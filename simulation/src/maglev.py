"""
Maglev Launch Track Physics for BGKPJR Simulations

Models the superconducting magnetic levitation accelerator including:
    - Track geometry (length, incline, curvature)
    - Electromagnetic acceleration profile
    - G-force constraints and optimization
    - Evacuated tube aerodynamics
    - Energy requirements

Author: Shane Brazelton
Date: 2025

Key Equations:
    Track Length: L = v²/(2a) for constant acceleration
    Exit Velocity: v = sqrt(2aL)
    Time in tube: t = v/a = sqrt(2L/a)
    Energy: E = 0.5 * m * v²
"""

import math
from dataclasses import dataclass
from typing import Tuple, List, Optional
from .constants import Constants, SystemParams, DEFAULT_PARAMS
from .atmosphere import TubeAtmosphere


@dataclass
class TrackGeometry:
    """Maglev track geometric parameters."""
    length: float  # m
    incline_angle: float  # degrees
    tube_diameter: float = 8.0  # m (must accommodate Gryphon + clearance)
    entry_radius: float = 5000.0  # m (curve radius at entry)
    exit_radius: float = 10000.0  # m (curve radius at exit)

    @property
    def incline_rad(self) -> float:
        """Incline angle in radians."""
        return math.radians(self.incline_angle)

    @property
    def vertical_rise(self) -> float:
        """Total vertical rise from entry to exit."""
        return self.length * math.sin(self.incline_rad)

    @property
    def horizontal_distance(self) -> float:
        """Horizontal distance covered."""
        return self.length * math.cos(self.incline_rad)


@dataclass
class AccelerationProfile:
    """Acceleration profile along the track."""
    max_g: float  # Maximum g-force
    ramp_up_distance: float  # Distance to reach max acceleration
    ramp_down_distance: float  # Distance to reduce acceleration before exit
    profile_type: str = "trapezoidal"  # "constant", "trapezoidal", "sinusoidal"


@dataclass
class LaunchResult:
    """Results from a simulated launch sequence."""
    exit_velocity: float  # m/s
    exit_mach: float
    exit_altitude: float  # m
    time_in_tube: float  # s
    peak_g_force: float  # g
    average_g_force: float  # g
    energy_delivered: float  # J
    exit_angle: float  # degrees (flight path angle)
    success: bool
    notes: str = ""


class MaglevTrack:
    """
    Superconducting Maglev Launch Track model.

    Simulates electromagnetic acceleration through an evacuated tube
    to achieve hypersonic exit velocities while maintaining safe g-forces.
    """

    def __init__(
        self,
        geometry: Optional[TrackGeometry] = None,
        accel_profile: Optional[AccelerationProfile] = None,
        tube_pressure_ratio: float = 0.1,
        params: Optional[SystemParams] = None
    ):
        """
        Initialize maglev track.

        Args:
            geometry: Track geometry parameters
            accel_profile: Acceleration profile
            tube_pressure_ratio: Fraction of atmospheric pressure in tube
            params: System parameters
        """
        self.params = params or DEFAULT_PARAMS

        # Default geometry
        if geometry is None:
            self.geometry = TrackGeometry(
                length=self.params.TRACK_LENGTH,
                incline_angle=self.params.TRACK_ANGLE_DEFAULT
            )
        else:
            self.geometry = geometry

        # Default acceleration profile
        if accel_profile is None:
            self.accel_profile = AccelerationProfile(
                max_g=self.params.MAX_ACCELERATION_G,
                ramp_up_distance=1000.0,  # 1 km ramp up
                ramp_down_distance=500.0  # 0.5 km ramp down
            )
        else:
            self.accel_profile = accel_profile

        # Tube atmosphere
        self.tube_atmo = TubeAtmosphere(tube_pressure_ratio)

    def calculate_minimum_track_length(self, target_velocity: float, max_g: float) -> float:
        """
        Calculate minimum track length for target velocity.

        L = v² / (2 * a)

        Args:
            target_velocity: Target exit velocity in m/s
            max_g: Maximum allowed g-force

        Returns:
            Minimum track length in meters
        """
        max_accel = max_g * Constants.G0
        return (target_velocity ** 2) / (2 * max_accel)

    def calculate_exit_velocity(self, track_length: float, max_g: float) -> float:
        """
        Calculate achievable exit velocity for given track.

        v = sqrt(2 * a * L)

        Args:
            track_length: Track length in meters
            max_g: Maximum allowed g-force

        Returns:
            Exit velocity in m/s
        """
        max_accel = max_g * Constants.G0
        return math.sqrt(2 * max_accel * track_length)

    def calculate_time_in_tube(self, exit_velocity: float, avg_g: float) -> float:
        """
        Calculate time spent in launch tube.

        t = v / a

        Args:
            exit_velocity: Exit velocity in m/s
            avg_g: Average g-force during acceleration

        Returns:
            Time in seconds
        """
        avg_accel = avg_g * Constants.G0
        return exit_velocity / avg_accel

    def get_acceleration_at_position(self, position: float) -> float:
        """
        Get acceleration at given position along track.

        Implements the configured acceleration profile.

        Args:
            position: Distance from track entry in meters

        Returns:
            Acceleration in m/s²
        """
        L = self.geometry.length
        a_max = self.accel_profile.max_g * Constants.G0
        ramp_up = self.accel_profile.ramp_up_distance
        ramp_down = self.accel_profile.ramp_down_distance

        if self.accel_profile.profile_type == "constant":
            return a_max

        elif self.accel_profile.profile_type == "trapezoidal":
            if position < ramp_up:
                # Linear ramp up
                return a_max * (position / ramp_up)
            elif position > (L - ramp_down):
                # Linear ramp down
                return a_max * ((L - position) / ramp_down)
            else:
                # Constant maximum
                return a_max

        elif self.accel_profile.profile_type == "sinusoidal":
            # Smooth sine wave profile
            return a_max * math.sin(math.pi * position / L)

        return a_max

    def calculate_tube_drag(self, velocity: float, vehicle_area: float) -> float:
        """
        Calculate aerodynamic drag inside evacuated tube.

        Even at 0.1 atm, significant drag at hypersonic speeds.

        Args:
            velocity: Current velocity in m/s
            vehicle_area: Vehicle frontal area in m²

        Returns:
            Drag force in Newtons
        """
        cond = self.tube_atmo.get_conditions(0)
        CD = 0.3  # Estimated drag coefficient for streamlined body in tube

        q = 0.5 * cond.density * (velocity ** 2)
        return q * vehicle_area * CD

    def calculate_energy_requirement(self, vehicle_mass: float, exit_velocity: float) -> float:
        """
        Calculate total energy needed to accelerate vehicle.

        E = 0.5 * m * v² + m * g * h (kinetic + potential)

        Args:
            vehicle_mass: Vehicle mass in kg
            exit_velocity: Target exit velocity in m/s

        Returns:
            Energy in Joules
        """
        # Kinetic energy
        E_kinetic = 0.5 * vehicle_mass * (exit_velocity ** 2)

        # Potential energy (climbing the incline)
        E_potential = vehicle_mass * Constants.G0 * self.geometry.vertical_rise

        # Losses (estimated 10% for EM system inefficiency)
        efficiency = 0.90
        E_total = (E_kinetic + E_potential) / efficiency

        return E_total

    def simulate_launch(
        self,
        vehicle_mass: float,
        vehicle_area: float = 40.0,  # Frontal area in m² (retracted wings)
        dt: float = 0.01
    ) -> LaunchResult:
        """
        Simulate complete launch sequence through the tube.

        Args:
            vehicle_mass: Vehicle mass in kg
            vehicle_area: Vehicle frontal area in m²
            dt: Time step in seconds

        Returns:
            LaunchResult with complete launch data
        """
        # Initial conditions
        position = 0.0
        velocity = 0.0
        time = 0.0
        max_g_experienced = 0.0
        total_accel = 0.0
        steps = 0

        # Simulation loop
        while position < self.geometry.length:
            # Get acceleration from maglev
            a_maglev = self.get_acceleration_at_position(position)

            # Calculate drag
            drag = self.calculate_tube_drag(velocity, vehicle_area) if velocity > 0 else 0
            a_drag = drag / vehicle_mass

            # Gravity component along incline
            a_gravity = Constants.G0 * math.sin(self.geometry.incline_rad)

            # Net acceleration
            a_net = a_maglev - a_drag - a_gravity

            # Update state
            velocity += a_net * dt
            position += velocity * dt
            time += dt

            # Track g-force
            g_force = a_net / Constants.G0
            max_g_experienced = max(max_g_experienced, abs(g_force))
            total_accel += abs(g_force)
            steps += 1

            # Safety check
            if velocity < 0:
                return LaunchResult(
                    exit_velocity=0, exit_mach=0, exit_altitude=0,
                    time_in_tube=time, peak_g_force=max_g_experienced,
                    average_g_force=total_accel/steps if steps > 0 else 0,
                    energy_delivered=0, exit_angle=self.geometry.incline_angle,
                    success=False, notes="Launch failed: Vehicle decelerated"
                )

        # Calculate final state
        exit_altitude = self.geometry.vertical_rise
        atm = self.tube_atmo.get_conditions(exit_altitude)
        exit_mach = velocity / atm.speed_of_sound

        energy = self.calculate_energy_requirement(vehicle_mass, velocity)
        avg_g = total_accel / steps if steps > 0 else 0

        # Determine success
        success = (
            exit_mach >= self.params.EXIT_MACH_MIN and
            max_g_experienced <= self.accel_profile.max_g * 1.1  # 10% tolerance
        )

        notes = []
        if exit_mach < self.params.EXIT_MACH_MIN:
            notes.append(f"Exit Mach {exit_mach:.2f} below minimum {self.params.EXIT_MACH_MIN}")
        if max_g_experienced > self.accel_profile.max_g * 1.1:
            notes.append(f"Peak g-force {max_g_experienced:.2f} exceeded limit")

        return LaunchResult(
            exit_velocity=velocity,
            exit_mach=exit_mach,
            exit_altitude=exit_altitude,
            time_in_tube=time,
            peak_g_force=max_g_experienced,
            average_g_force=avg_g,
            energy_delivered=energy,
            exit_angle=self.geometry.incline_angle,
            success=success,
            notes="; ".join(notes) if notes else "Nominal launch"
        )

    def optimize_incline_angle(
        self,
        vehicle_mass: float,
        target_velocity: float,
        angle_range: Tuple[float, float] = (15, 45),
        steps: int = 31
    ) -> Tuple[float, LaunchResult]:
        """
        Find optimal incline angle for given target velocity.

        Balances:
        - Higher angle = more altitude gain, less horizontal distance
        - Lower angle = gentler g-forces, more track length needed

        Args:
            vehicle_mass: Vehicle mass in kg
            target_velocity: Target exit velocity in m/s
            angle_range: (min_angle, max_angle) in degrees
            steps: Number of angles to test

        Returns:
            (optimal_angle, best_result)
        """
        best_angle = angle_range[0]
        best_result = None
        best_score = float('-inf')

        for angle in [angle_range[0] + i * (angle_range[1] - angle_range[0]) / (steps - 1)
                      for i in range(steps)]:
            # Update geometry
            self.geometry.incline_angle = angle

            # Simulate
            result = self.simulate_launch(vehicle_mass)

            if not result.success:
                continue

            # Score: maximize exit velocity, minimize g-force, maximize altitude
            score = (
                result.exit_velocity / target_velocity +
                result.exit_altitude / 10000 -
                result.peak_g_force / self.accel_profile.max_g
            )

            if score > best_score:
                best_score = score
                best_angle = angle
                best_result = result

        return best_angle, best_result

    def print_track_summary(self):
        """Print track configuration summary."""
        print("=" * 60)
        print("MAGLEV LAUNCH TRACK CONFIGURATION")
        print("=" * 60)
        print(f"Track Length: {self.geometry.length/1000:.1f} km")
        print(f"Incline Angle: {self.geometry.incline_angle:.1f}°")
        print(f"Vertical Rise: {self.geometry.vertical_rise/1000:.2f} km")
        print(f"Horizontal Distance: {self.geometry.horizontal_distance/1000:.1f} km")
        print(f"Tube Diameter: {self.geometry.tube_diameter:.1f} m")
        print(f"Tube Pressure: {self.tube_atmo.pressure_ratio * 100:.1f}% atm")
        print(f"Max Acceleration: {self.accel_profile.max_g:.1f} g")
        print(f"Profile Type: {self.accel_profile.profile_type}")

        # Theoretical values
        v_max = self.calculate_exit_velocity(
            self.geometry.length, self.accel_profile.max_g
        )
        t_min = self.calculate_time_in_tube(v_max, self.accel_profile.max_g)

        print("\nTheoretical Performance (no losses):")
        print(f"  Max Exit Velocity: {v_max:.0f} m/s (Mach {v_max/340:.1f})")
        print(f"  Min Time in Tube: {t_min:.1f} s")
        print("=" * 60)


if __name__ == "__main__":
    # Test maglev track model
    print("=== BGKPJR Maglev Track Simulation ===\n")

    track = MaglevTrack()
    track.print_track_summary()

    # Simulate launch
    print("\n--- Simulating Launch (50,000 kg vehicle) ---\n")
    result = track.simulate_launch(vehicle_mass=50000)

    print("LAUNCH RESULTS:")
    print(f"  Exit Velocity: {result.exit_velocity:.0f} m/s (Mach {result.exit_mach:.2f})")
    print(f"  Exit Altitude: {result.exit_altitude/1000:.2f} km")
    print(f"  Time in Tube: {result.time_in_tube:.2f} s")
    print(f"  Peak G-Force: {result.peak_g_force:.2f} g")
    print(f"  Average G-Force: {result.average_g_force:.2f} g")
    print(f"  Energy Delivered: {result.energy_delivered/1e9:.2f} GJ")
    print(f"  Status: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"  Notes: {result.notes}")

    # Optimization
    print("\n--- Optimizing Incline Angle ---\n")
    optimal_angle, optimal_result = track.optimize_incline_angle(
        vehicle_mass=50000,
        target_velocity=1190  # Mach 3.5
    )
    print(f"Optimal Incline Angle: {optimal_angle:.1f}°")
    if optimal_result:
        print(f"Exit Velocity at Optimal: {optimal_result.exit_velocity:.0f} m/s")
        print(f"Exit Altitude at Optimal: {optimal_result.exit_altitude/1000:.2f} km")
