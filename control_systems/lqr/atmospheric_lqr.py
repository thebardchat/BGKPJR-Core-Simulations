"""
Linear Quadratic Regulator (LQR) for Atmospheric Ascent Phase

Implements state-feedback optimal control for the Gryphon spacecraft
during atmospheric flight (post-tube exit to exoatmospheric).

Control Objectives:
    - Track optimal trajectory (altitude, velocity)
    - Minimize structural loads (g-force, dynamic pressure)
    - Maintain attitude stability

State Vector: x = [altitude_error, velocity_error, flight_path_error, pitch_rate]
Control Input: u = [elevator_deflection, throttle_adjustment]

Author: Shane Brazelton
Date: 2025
"""

import numpy as np
from typing import Tuple, Optional
import math


class AtmosphericLQR:
    """
    LQR controller for atmospheric ascent phase.

    Uses linearized equations of motion about a reference trajectory
    to compute optimal feedback gains.
    """

    def __init__(
        self,
        Q: Optional[np.ndarray] = None,
        R: Optional[np.ndarray] = None
    ):
        """
        Initialize LQR controller.

        Args:
            Q: State weighting matrix (4x4)
            R: Control weighting matrix (2x2)
        """
        # Default state weights (penalize errors)
        if Q is None:
            self.Q = np.diag([
                1.0,    # Altitude error weight
                10.0,   # Velocity error weight (most important)
                5.0,    # Flight path angle error weight
                0.1     # Pitch rate weight (stability)
            ])
        else:
            self.Q = Q

        # Default control weights (penalize control effort)
        if R is None:
            self.R = np.diag([
                1.0,    # Elevator deflection cost
                0.5     # Throttle adjustment cost
            ])
        else:
            self.R = R

        # Controller gains (computed by solve_riccati)
        self.K = None

        # Reference trajectory (to be set)
        self.reference_altitude = None
        self.reference_velocity = None
        self.reference_gamma = None

    def linearize_dynamics(
        self,
        velocity: float,
        altitude: float,
        flight_path_angle: float,
        mass: float = 50000,
        wing_area: float = 120
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Linearize equations of motion about current state.

        Returns A (state) and B (control) matrices for:
            dx/dt = A*x + B*u

        Args:
            velocity: Current velocity (m/s)
            altitude: Current altitude (m)
            flight_path_angle: Current flight path angle (rad)
            mass: Vehicle mass (kg)
            wing_area: Reference wing area (m²)

        Returns:
            (A, B) state-space matrices
        """
        # Physical constants
        g = 9.81 * (6.371e6 / (6.371e6 + altitude))**2
        gamma = flight_path_angle

        # Simplified atmospheric model
        rho0 = 1.225
        H = 8500  # Scale height
        rho = rho0 * np.exp(-altitude / H)

        # Dynamic pressure
        q = 0.5 * rho * velocity**2

        # Aerodynamic derivatives (linearized)
        CL_alpha = 0.05  # per degree
        CD0 = 0.015
        S = wing_area

        # Partial derivatives for A matrix
        # State: [h, V, gamma, q_pitch]

        # dh/dt = V * sin(gamma)
        dhdot_dV = np.sin(gamma)
        dhdot_dgamma = velocity * np.cos(gamma)

        # dV/dt = (T - D)/m - g*sin(gamma)
        # Linearized around trim
        dVdot_dV = -rho * velocity * CD0 * S / mass
        dVdot_dgamma = -g * np.cos(gamma)

        # dgamma/dt = (L - W*cos(gamma))/(m*V)
        dgammadot_dV = -q * CL_alpha * S / (mass * velocity**2)
        dgammadot_dgamma = g * np.sin(gamma) / velocity

        # A matrix (4x4)
        A = np.array([
            [0, dhdot_dV, dhdot_dgamma, 0],
            [0, dVdot_dV, dVdot_dgamma, 0],
            [0, dgammadot_dV, dgammadot_dgamma, 1],
            [0, 0, 0, -2.0]  # Pitch rate dynamics (damped)
        ])

        # B matrix (4x2) - control effectiveness
        # Control: [elevator (affects pitch), throttle (affects velocity)]
        elevator_effectiveness = q * S * 0.1 / (mass * velocity)  # rad/s² per deg
        throttle_effectiveness = 500000 / mass  # m/s² per unit throttle

        B = np.array([
            [0, 0],
            [0, throttle_effectiveness],
            [elevator_effectiveness, 0],
            [10.0, 0]  # Elevator directly affects pitch rate
        ])

        return A, B

    def solve_riccati(
        self,
        A: np.ndarray,
        B: np.ndarray,
        max_iterations: int = 1000,
        tolerance: float = 1e-9
    ) -> np.ndarray:
        """
        Solve the continuous-time algebraic Riccati equation (CARE).

        A'P + PA - PBR⁻¹B'P + Q = 0

        Uses iterative method for numerical stability.

        Args:
            A: State matrix
            B: Control matrix
            max_iterations: Maximum solver iterations
            tolerance: Convergence tolerance

        Returns:
            Optimal feedback gain matrix K
        """
        n = A.shape[0]
        P = np.eye(n)  # Initial guess

        R_inv = np.linalg.inv(self.R)
        BRinvBT = B @ R_inv @ B.T

        for i in range(max_iterations):
            P_new = self.Q + A.T @ P + P @ A - P @ BRinvBT @ P

            # Check convergence
            if np.max(np.abs(P_new - P)) < tolerance:
                break

            # Damped update for stability
            P = 0.5 * P + 0.5 * P_new

        # Compute optimal gain
        K = R_inv @ B.T @ P

        self.K = K
        return K

    def compute_control(
        self,
        state_error: np.ndarray,
        velocity: float,
        altitude: float,
        flight_path_angle: float
    ) -> Tuple[float, float]:
        """
        Compute optimal control inputs.

        Args:
            state_error: [altitude_error, velocity_error, gamma_error, pitch_rate]
            velocity: Current velocity for linearization
            altitude: Current altitude for linearization
            flight_path_angle: Current flight path angle

        Returns:
            (elevator_deflection_deg, throttle_adjustment)
        """
        # Update linearization if needed
        A, B = self.linearize_dynamics(velocity, altitude, flight_path_angle)

        # Solve for gains
        K = self.solve_riccati(A, B)

        # Compute control
        u = -K @ state_error

        # Apply saturation limits
        elevator = np.clip(u[0], -25, 25)  # degrees
        throttle = np.clip(u[1], -0.5, 0.5)  # throttle adjustment

        return elevator, throttle

    def set_reference_trajectory(
        self,
        altitude: float,
        velocity: float,
        flight_path_angle: float
    ):
        """
        Set reference trajectory for tracking.

        Args:
            altitude: Target altitude (m)
            velocity: Target velocity (m/s)
            flight_path_angle: Target flight path angle (rad)
        """
        self.reference_altitude = altitude
        self.reference_velocity = velocity
        self.reference_gamma = flight_path_angle

    def get_state_error(
        self,
        altitude: float,
        velocity: float,
        flight_path_angle: float,
        pitch_rate: float
    ) -> np.ndarray:
        """
        Calculate state error from reference.

        Args:
            altitude: Current altitude (m)
            velocity: Current velocity (m/s)
            flight_path_angle: Current flight path angle (rad)
            pitch_rate: Current pitch rate (rad/s)

        Returns:
            State error vector
        """
        if self.reference_altitude is None:
            return np.zeros(4)

        return np.array([
            altitude - self.reference_altitude,
            velocity - self.reference_velocity,
            flight_path_angle - self.reference_gamma,
            pitch_rate  # Reference pitch rate assumed zero
        ])


class GravityTurnGuidance:
    """
    Gravity turn guidance for atmospheric ascent.

    Implements the classic gravity turn trajectory where pitch
    follows the velocity vector, allowing gravity to naturally
    curve the trajectory toward horizontal.
    """

    def __init__(
        self,
        initial_pitch: float = 80.0,  # degrees from horizontal
        pitch_over_altitude: float = 5000.0,  # m
        pitch_over_rate: float = 0.5  # deg/s
    ):
        """
        Initialize gravity turn guidance.

        Args:
            initial_pitch: Initial pitch angle after tube exit (deg)
            pitch_over_altitude: Altitude to begin pitch-over maneuver (m)
            pitch_over_rate: Rate of pitch-over (deg/s)
        """
        self.initial_pitch = initial_pitch
        self.pitch_over_altitude = pitch_over_altitude
        self.pitch_over_rate = pitch_over_rate
        self.pitch_over_started = False
        self.pitch_over_start_time = None

    def get_commanded_pitch(
        self,
        time: float,
        altitude: float,
        velocity: float,
        flight_path_angle: float  # rad
    ) -> float:
        """
        Get commanded pitch angle.

        Args:
            time: Mission elapsed time (s)
            altitude: Current altitude (m)
            velocity: Current velocity (m/s)
            flight_path_angle: Current flight path angle (rad)

        Returns:
            Commanded pitch angle (degrees from horizontal)
        """
        # Initial vertical ascent
        if altitude < self.pitch_over_altitude and not self.pitch_over_started:
            return self.initial_pitch

        # Begin pitch-over
        if not self.pitch_over_started:
            self.pitch_over_started = True
            self.pitch_over_start_time = time

        # During pitch-over, follow velocity vector (gravity turn)
        # Commanded pitch = flight path angle
        gamma_deg = np.degrees(flight_path_angle)

        # Small pitch offset to maintain positive angle of attack
        pitch_offset = 2.0  # degrees

        return max(0, gamma_deg + pitch_offset)

    def get_commanded_throttle(
        self,
        altitude: float,
        velocity: float,
        dynamic_pressure: float,
        max_q_limit: float = 50000  # Pa
    ) -> float:
        """
        Get commanded throttle setting.

        Throttles down during Max Q to limit structural loads.

        Args:
            altitude: Current altitude (m)
            velocity: Current velocity (m/s)
            dynamic_pressure: Current dynamic pressure (Pa)
            max_q_limit: Maximum allowed dynamic pressure (Pa)

        Returns:
            Throttle setting (0-1)
        """
        # Full throttle except during Max Q
        if dynamic_pressure > max_q_limit * 0.9:
            # Reduce throttle to limit Q
            throttle = 0.7 * (max_q_limit / dynamic_pressure)
            return max(0.5, min(1.0, throttle))

        # Otherwise full throttle
        return 1.0


if __name__ == "__main__":
    print("=== Atmospheric LQR Controller Test ===\n")

    # Initialize controller
    lqr = AtmosphericLQR()

    # Test linearization at different flight conditions
    print("Linearization test at various conditions:")
    print("-" * 60)

    conditions = [
        (1200, 10000, 0.5),   # Post-tube exit
        (2000, 30000, 0.3),   # Mid-atmosphere
        (3000, 60000, 0.1),   # Near space
    ]

    for v, h, gamma in conditions:
        A, B = lqr.linearize_dynamics(v, h, gamma)
        K = lqr.solve_riccati(A, B)

        print(f"\nV={v} m/s, h={h/1000:.0f} km, γ={np.degrees(gamma):.0f}°:")
        print(f"  Gain K shape: {K.shape}")
        print(f"  K[0,:] (elevator gains): {K[0,:]}")
        print(f"  K[1,:] (throttle gains): {K[1,:]}")

    # Test gravity turn guidance
    print("\n" + "=" * 60)
    print("Gravity Turn Guidance Test")
    print("-" * 60)

    guidance = GravityTurnGuidance()

    for t, h, v, gamma in [(0, 5000, 1200, 0.8), (30, 15000, 1800, 0.5),
                            (60, 40000, 2500, 0.2), (120, 100000, 4000, 0.05)]:
        pitch = guidance.get_commanded_pitch(t, h, v, gamma)
        q = 0.5 * 1.225 * np.exp(-h/8500) * v**2
        throttle = guidance.get_commanded_throttle(h, v, q)

        print(f"t={t:3d}s, h={h/1000:5.1f}km: pitch={pitch:5.1f}°, "
              f"throttle={throttle:.2f}, q={q/1000:.1f}kPa")
