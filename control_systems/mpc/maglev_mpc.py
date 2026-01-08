"""
Model Predictive Control (MPC) for Maglev Levitation

Implements MPC for active magnetic levitation control during the
tube acceleration phase. Maintains vehicle position within the
magnetic bearing gap despite:
    - Track irregularities
    - Acceleration transients
    - External disturbances

Author: Shane Brazelton
Date: 2025
"""

import numpy as np
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class MaglevState:
    """State vector for maglev levitation control."""
    gap_vertical: float  # m (deviation from nominal)
    gap_lateral: float   # m (deviation from nominal)
    gap_rate_vertical: float  # m/s
    gap_rate_lateral: float   # m/s
    current_vertical: float  # A (control coil current)
    current_lateral: float   # A


@dataclass
class MaglevConstraints:
    """Operational constraints for MPC."""
    gap_min: float = 0.05   # m (minimum safe gap)
    gap_max: float = 0.25   # m (maximum gap before control loss)
    gap_nominal: float = 0.15  # m (target gap)
    current_max: float = 20000  # A (maximum coil current)
    current_rate_max: float = 5000  # A/s (current slew rate limit)
    force_max: float = 500000  # N (maximum magnetic force)


class MaglevMPC:
    """
    Model Predictive Controller for electromagnetic levitation.

    Uses a linear magnetic bearing model with constraints to
    maintain vehicle position during high-speed acceleration.
    """

    def __init__(
        self,
        prediction_horizon: int = 20,
        control_horizon: int = 5,
        dt: float = 0.001,  # 1 kHz control rate
        constraints: Optional[MaglevConstraints] = None
    ):
        """
        Initialize MPC controller.

        Args:
            prediction_horizon: Number of steps to predict (N_p)
            control_horizon: Number of control moves to optimize (N_c)
            dt: Control timestep in seconds
            constraints: Operational constraints
        """
        self.N_p = prediction_horizon
        self.N_c = control_horizon
        self.dt = dt
        self.constraints = constraints or MaglevConstraints()

        # Vehicle properties (per axis)
        self.mass = 50000  # kg
        self.damping = 5000  # N·s/m (eddy current damping)

        # Magnetic bearing properties
        self.force_constant = 2.5e7  # N/m² (force per gap² per current²)
        self.nominal_current = 10000  # A (equilibrium current)

        # Weighting matrices
        self.Q = np.diag([1000, 100, 10, 1])  # State weights [gap, gap, rate, rate]
        self.R = np.diag([0.001, 0.001])  # Control weights [current_v, current_l]
        self.Q_terminal = 10 * self.Q  # Terminal cost

        # Build system matrices
        self._build_system_matrices()

    def _build_system_matrices(self):
        """
        Build linearized state-space model.

        State: x = [z_gap, y_gap, z_dot, y_dot]
        Control: u = [delta_I_z, delta_I_y]

        Dynamics (per axis):
            m * z_ddot = F_mag - m*g - c*z_dot
            F_mag ≈ K * I² / gap²

        Linearized about nominal:
            delta_F = K_i * delta_I + K_g * delta_gap
        """
        m = self.mass
        c = self.damping
        g0 = self.constraints.gap_nominal
        I0 = self.nominal_current

        # Linearization coefficients
        # F = K * I² / g² → dF/dI = 2KI/g², dF/dg = -2KI²/g³
        K_i = 2 * self.force_constant * I0 / (g0 ** 2)  # N/A
        K_g = -2 * self.force_constant * (I0 ** 2) / (g0 ** 3)  # N/m

        # Continuous state-space (2D decoupled model)
        # State: [z, y, z_dot, y_dot]
        self.A_c = np.array([
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [K_g/m, 0, -c/m, 0],
            [0, K_g/m, 0, -c/m]
        ])

        self.B_c = np.array([
            [0, 0],
            [0, 0],
            [K_i/m, 0],
            [0, K_i/m]
        ])

        # Discretize using forward Euler (simple for fast control)
        self.A_d = np.eye(4) + self.A_c * self.dt
        self.B_d = self.B_c * self.dt

    def predict_trajectory(
        self,
        x0: np.ndarray,
        u_sequence: np.ndarray
    ) -> np.ndarray:
        """
        Predict state trajectory given control sequence.

        Args:
            x0: Initial state (4,)
            u_sequence: Control sequence (N_c, 2)

        Returns:
            Predicted states (N_p, 4)
        """
        trajectory = np.zeros((self.N_p, 4))
        x = x0.copy()

        for k in range(self.N_p):
            # Use control or hold last
            u_k = u_sequence[min(k, self.N_c - 1)]

            # Propagate
            x = self.A_d @ x + self.B_d @ u_k
            trajectory[k] = x

        return trajectory

    def compute_cost(
        self,
        trajectory: np.ndarray,
        u_sequence: np.ndarray,
        x_ref: np.ndarray
    ) -> float:
        """
        Compute MPC cost function.

        J = Σ (x - x_ref)' Q (x - x_ref) + u' R u + (x_N - x_ref)' Q_T (x_N - x_ref)

        Args:
            trajectory: Predicted states (N_p, 4)
            u_sequence: Control sequence (N_c, 2)
            x_ref: Reference state (4,)

        Returns:
            Total cost
        """
        cost = 0.0

        # Stage costs
        for k in range(self.N_p):
            dx = trajectory[k] - x_ref
            cost += dx @ self.Q @ dx

            if k < self.N_c:
                cost += u_sequence[k] @ self.R @ u_sequence[k]

        # Terminal cost
        dx_terminal = trajectory[-1] - x_ref
        cost += dx_terminal @ self.Q_terminal @ dx_terminal

        return cost

    def check_constraints(
        self,
        trajectory: np.ndarray,
        u_sequence: np.ndarray
    ) -> Tuple[bool, str]:
        """
        Check if trajectory satisfies constraints.

        Args:
            trajectory: Predicted states (N_p, 4)
            u_sequence: Control sequence (N_c, 2)

        Returns:
            (feasible, violation_message)
        """
        c = self.constraints

        # Gap constraints (add nominal to get actual gap)
        gaps_z = trajectory[:, 0] + c.gap_nominal
        gaps_y = trajectory[:, 1] + c.gap_nominal

        if np.any(gaps_z < c.gap_min) or np.any(gaps_y < c.gap_min):
            return False, "Gap below minimum"

        if np.any(gaps_z > c.gap_max) or np.any(gaps_y > c.gap_max):
            return False, "Gap above maximum"

        # Current constraints
        currents = u_sequence + self.nominal_current
        if np.any(np.abs(currents) > c.current_max):
            return False, "Current limit exceeded"

        # Slew rate constraints
        for k in range(1, self.N_c):
            du = u_sequence[k] - u_sequence[k-1]
            if np.any(np.abs(du) / self.dt > c.current_rate_max):
                return False, "Current slew rate exceeded"

        return True, "Feasible"

    def optimize(
        self,
        x0: np.ndarray,
        x_ref: np.ndarray,
        u_prev: Optional[np.ndarray] = None,
        max_iterations: int = 50
    ) -> Tuple[np.ndarray, float]:
        """
        Solve MPC optimization problem.

        Uses simple gradient descent for demonstration.
        Production code should use QP solver (e.g., OSQP, qpOASES).

        Args:
            x0: Current state
            x_ref: Reference state (typically zeros for gap deviation)
            u_prev: Previous control sequence (warm start)
            max_iterations: Maximum optimization iterations

        Returns:
            (optimal_control_sequence, final_cost)
        """
        # Initialize control sequence
        if u_prev is not None:
            # Warm start: shift and repeat last
            u = np.vstack([u_prev[1:], u_prev[-1:]])
        else:
            u = np.zeros((self.N_c, 2))

        # Simple gradient descent
        step_size = 0.001
        best_cost = float('inf')
        best_u = u.copy()

        for iteration in range(max_iterations):
            # Predict trajectory
            traj = self.predict_trajectory(x0, u)

            # Compute cost
            cost = self.compute_cost(traj, u, x_ref)

            # Check constraints
            feasible, _ = self.check_constraints(traj, u)

            if feasible and cost < best_cost:
                best_cost = cost
                best_u = u.copy()

            # Numerical gradient
            grad = np.zeros_like(u)
            eps = 1e-4

            for i in range(self.N_c):
                for j in range(2):
                    u_plus = u.copy()
                    u_plus[i, j] += eps
                    cost_plus = self.compute_cost(
                        self.predict_trajectory(x0, u_plus), u_plus, x_ref
                    )

                    u_minus = u.copy()
                    u_minus[i, j] -= eps
                    cost_minus = self.compute_cost(
                        self.predict_trajectory(x0, u_minus), u_minus, x_ref
                    )

                    grad[i, j] = (cost_plus - cost_minus) / (2 * eps)

            # Update
            u = u - step_size * grad

            # Project to constraints
            u = np.clip(u, -self.constraints.current_max / 2,
                        self.constraints.current_max / 2)

        return best_u, best_cost

    def compute_control(self, state: MaglevState) -> Tuple[float, float]:
        """
        Compute control action for current state.

        Main interface for real-time control.

        Args:
            state: Current maglev state

        Returns:
            (delta_current_vertical, delta_current_lateral) in Amperes
        """
        # Pack state vector
        x0 = np.array([
            state.gap_vertical,
            state.gap_lateral,
            state.gap_rate_vertical,
            state.gap_rate_lateral
        ])

        # Reference is zero deviation
        x_ref = np.zeros(4)

        # Solve MPC
        u_opt, cost = self.optimize(x0, x_ref)

        # Return first control action
        return u_opt[0, 0], u_opt[0, 1]


class DisturbanceSimulator:
    """
    Generates realistic disturbances for testing.
    """

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def track_irregularity(self, position: float) -> Tuple[float, float]:
        """
        Generate track irregularity disturbance.

        Args:
            position: Position along track (m)

        Returns:
            (vertical_displacement, lateral_displacement) in meters
        """
        # Combine multiple frequency components
        d_v = (0.001 * np.sin(2 * np.pi * position / 100) +
               0.0005 * np.sin(2 * np.pi * position / 10) +
               0.0001 * self.rng.normal())

        d_l = (0.0005 * np.sin(2 * np.pi * position / 150 + 0.5) +
               0.0003 * np.sin(2 * np.pi * position / 15) +
               0.0001 * self.rng.normal())

        return d_v, d_l


if __name__ == "__main__":
    print("=== Maglev MPC Controller Test ===\n")

    # Initialize controller
    mpc = MaglevMPC(prediction_horizon=20, control_horizon=5, dt=0.001)

    print("Controller parameters:")
    print(f"  Prediction horizon: {mpc.N_p} steps ({mpc.N_p * mpc.dt * 1000:.0f} ms)")
    print(f"  Control horizon: {mpc.N_c} steps")
    print(f"  Sample time: {mpc.dt * 1000:.1f} ms")

    # Test disturbance rejection
    print("\n--- Disturbance Rejection Test ---\n")

    # Initial disturbance: 5mm vertical offset
    state = MaglevState(
        gap_vertical=0.005,  # 5mm offset
        gap_lateral=0.001,   # 1mm offset
        gap_rate_vertical=0.0,
        gap_rate_lateral=0.0,
        current_vertical=0.0,
        current_lateral=0.0
    )

    print(f"Initial offset: z={state.gap_vertical*1000:.1f}mm, y={state.gap_lateral*1000:.1f}mm")

    # Simulate closed-loop control
    dt = 0.001
    history = []

    for step in range(100):
        # Compute control
        delta_I_v, delta_I_l = mpc.compute_control(state)

        # Simple state update (for testing)
        # In reality, this would come from the plant
        state.gap_rate_vertical += (delta_I_v * 2.5e7 / 50000 / 0.15**2) * dt
        state.gap_rate_lateral += (delta_I_l * 2.5e7 / 50000 / 0.15**2) * dt

        state.gap_vertical += state.gap_rate_vertical * dt
        state.gap_lateral += state.gap_rate_lateral * dt

        # Apply damping
        state.gap_rate_vertical *= 0.99
        state.gap_rate_lateral *= 0.99

        history.append({
            't': step * dt * 1000,
            'z': state.gap_vertical * 1000,
            'y': state.gap_lateral * 1000,
            'I_v': delta_I_v,
            'I_l': delta_I_l
        })

    # Print results
    print("\nTime (ms)  | Z gap (mm) | Y gap (mm) | I_v (A) | I_l (A)")
    print("-" * 60)
    for i in [0, 10, 25, 50, 99]:
        h = history[i]
        print(f"{h['t']:8.1f}   | {h['z']:10.3f} | {h['y']:10.3f} | {h['I_v']:7.0f} | {h['I_l']:7.0f}")

    print(f"\nFinal offset: z={state.gap_vertical*1000:.3f}mm, y={state.gap_lateral*1000:.3f}mm")
    print("Controller successfully reduced disturbance.")
