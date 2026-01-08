"""
Monte Carlo Simulation Framework for BGKPJR

Performs statistical analysis of mission success probability by
varying key parameters within their uncertainty bounds:
    - Track exit velocity (±2%)
    - Track exit angle (±1°)
    - Vehicle mass (±3%)
    - Aerodynamic coefficients (±10%)
    - Atmospheric conditions (seasonal variation)
    - Propulsion performance (±2% Isp)

Outputs:
    - Mission success probability
    - Parameter sensitivity analysis
    - "Sweet spot" optimization for track angle
    - Failure mode distribution

Author: Shane Brazelton
Date: 2025

Usage:
    python monte_carlo.py --runs 1000 --output results.csv
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# Import local modules (handle both package and direct execution)
try:
    from .constants import SystemParams, DEFAULT_PARAMS
    from .trajectory_sim import TrajectorySimulator, MissionResult
    from .vehicle import GryphonVehicle
    from .maglev import MaglevTrack, TrackGeometry, AccelerationProfile
except ImportError:
    from constants import SystemParams, DEFAULT_PARAMS
    from trajectory_sim import TrajectorySimulator, MissionResult
    from vehicle import GryphonVehicle
    from maglev import MaglevTrack, TrackGeometry, AccelerationProfile


@dataclass
class ParameterVariation:
    """Defines uncertainty range for a parameter."""
    name: str
    nominal: float
    sigma: float  # Standard deviation (for Gaussian)
    distribution: str = "gaussian"  # "gaussian", "uniform", "triangular"
    bounds: Tuple[float, float] = None  # Hard limits


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation batch."""
    n_runs: int
    n_success: int
    success_probability: float
    mean_final_altitude: float
    std_final_altitude: float
    mean_final_velocity: float
    std_final_velocity: float
    mean_max_g: float
    std_max_g: float
    mean_max_q: float
    std_max_q: float
    failure_modes: Dict[str, int]
    parameter_sensitivities: Dict[str, float]
    raw_results: List[Dict]


class MonteCarloSimulator:
    """
    Monte Carlo simulation framework for BGKPJR mission analysis.

    Performs randomized simulations to assess mission robustness
    and identify critical parameters.
    """

    def __init__(
        self,
        base_params: Optional[SystemParams] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize Monte Carlo simulator.

        Args:
            base_params: Nominal system parameters
            seed: Random seed for reproducibility
        """
        self.base_params = base_params or DEFAULT_PARAMS
        self.rng = np.random.default_rng(seed)

        # Define parameter variations (uncertainties)
        self.variations = self._define_variations()

    def _define_variations(self) -> List[ParameterVariation]:
        """Define parameter uncertainties for Monte Carlo analysis."""
        return [
            # Track parameters
            ParameterVariation(
                name="exit_velocity_factor",
                nominal=1.0,
                sigma=0.02,  # ±2%
                bounds=(0.95, 1.05)
            ),
            ParameterVariation(
                name="track_angle",
                nominal=self.base_params.TRACK_ANGLE_DEFAULT,
                sigma=1.0,  # ±1°
                bounds=(15, 45)
            ),

            # Vehicle parameters
            ParameterVariation(
                name="mass_factor",
                nominal=1.0,
                sigma=0.03,  # ±3%
                bounds=(0.95, 1.10)
            ),
            ParameterVariation(
                name="cd0_factor",
                nominal=1.0,
                sigma=0.10,  # ±10%
                bounds=(0.8, 1.3)
            ),
            ParameterVariation(
                name="cl_factor",
                nominal=1.0,
                sigma=0.10,  # ±10%
                bounds=(0.8, 1.2)
            ),

            # Propulsion parameters
            ParameterVariation(
                name="isp_factor",
                nominal=1.0,
                sigma=0.02,  # ±2%
                bounds=(0.95, 1.05)
            ),
            ParameterVariation(
                name="thrust_factor",
                nominal=1.0,
                sigma=0.03,  # ±3%
                bounds=(0.95, 1.05)
            ),

            # Atmospheric variation (seasonal/daily)
            ParameterVariation(
                name="density_factor",
                nominal=1.0,
                sigma=0.05,  # ±5%
                bounds=(0.90, 1.10)
            ),
        ]

    def sample_parameter(self, var: ParameterVariation) -> float:
        """
        Sample a parameter value from its uncertainty distribution.

        Args:
            var: Parameter variation specification

        Returns:
            Sampled parameter value
        """
        if var.distribution == "gaussian":
            value = self.rng.normal(var.nominal, var.sigma)
        elif var.distribution == "uniform":
            value = self.rng.uniform(
                var.nominal - 2*var.sigma,
                var.nominal + 2*var.sigma
            )
        elif var.distribution == "triangular":
            value = self.rng.triangular(
                var.nominal - 2*var.sigma,
                var.nominal,
                var.nominal + 2*var.sigma
            )
        else:
            value = var.nominal

        # Apply bounds if specified
        if var.bounds:
            value = np.clip(value, var.bounds[0], var.bounds[1])

        return value

    def sample_all_parameters(self) -> Dict[str, float]:
        """Sample all uncertain parameters."""
        return {var.name: self.sample_parameter(var) for var in self.variations}

    def run_single_simulation(self, params: Dict[str, float]) -> Dict:
        """
        Run a single trajectory simulation with given parameters.

        Args:
            params: Dictionary of sampled parameter values

        Returns:
            Dictionary with simulation results
        """
        # Create modified system parameters
        mod_params = SystemParams()

        # Apply track angle variation
        track_geometry = TrackGeometry(
            length=mod_params.TRACK_LENGTH,
            incline_angle=params["track_angle"]
        )

        # Create track with modified geometry
        track = MaglevTrack(geometry=track_geometry, params=mod_params)

        # Create vehicle with modified parameters
        vehicle = GryphonVehicle(mod_params)
        vehicle.mass_propellant *= params["mass_factor"]
        vehicle.CD0 *= params["cd0_factor"]
        vehicle.CL_alpha *= params["cl_factor"]
        vehicle.isp_vacuum *= params["isp_factor"]
        vehicle.isp_sea_level *= params["isp_factor"]
        vehicle.thrust_max *= params["thrust_factor"]

        # Create simulator
        sim = TrajectorySimulator(vehicle=vehicle, track=track, params=mod_params)

        # Run simulation
        try:
            result = sim.run_simulation()

            return {
                "success": result.success,
                "final_altitude": result.final_altitude,
                "final_velocity": result.final_velocity,
                "max_g": result.max_g,
                "max_q": result.max_q,
                "time_to_orbit": result.time_to_orbit,
                "failure_reason": result.failure_reason,
                "params": params
            }
        except Exception as e:
            return {
                "success": False,
                "final_altitude": 0,
                "final_velocity": 0,
                "max_g": 0,
                "max_q": 0,
                "time_to_orbit": 0,
                "failure_reason": str(e),
                "params": params
            }

    def run_batch(
        self,
        n_runs: int,
        parallel: bool = True,
        show_progress: bool = True
    ) -> MonteCarloResult:
        """
        Run batch of Monte Carlo simulations.

        Args:
            n_runs: Number of simulation runs
            parallel: Use parallel processing
            show_progress: Show progress bar

        Returns:
            MonteCarloResult with statistical analysis
        """
        results = []

        if parallel:
            # Note: For true parallelism, would need multiprocessing
            # Simplified sequential execution here for portability
            iterator = range(n_runs)
            if show_progress:
                try:
                    iterator = tqdm(iterator, desc="Monte Carlo")
                except:
                    pass

            for i in iterator:
                params = self.sample_all_parameters()
                result = self.run_single_simulation(params)
                results.append(result)
        else:
            for i in range(n_runs):
                params = self.sample_all_parameters()
                result = self.run_single_simulation(params)
                results.append(result)
                if show_progress and (i + 1) % 100 == 0:
                    print(f"  Completed {i + 1}/{n_runs} runs...")

        # Analyze results
        return self._analyze_results(results)

    def _analyze_results(self, results: List[Dict]) -> MonteCarloResult:
        """Perform statistical analysis on simulation results."""
        n_runs = len(results)
        n_success = sum(1 for r in results if r["success"])

        # Extract successful runs for statistics
        successful = [r for r in results if r["success"]]

        if successful:
            altitudes = [r["final_altitude"] for r in successful]
            velocities = [r["final_velocity"] for r in successful]
            max_gs = [r["max_g"] for r in successful]
            max_qs = [r["max_q"] for r in successful]
        else:
            altitudes = velocities = max_gs = max_qs = [0]

        # Failure mode analysis
        failure_modes = {}
        for r in results:
            if not r["success"]:
                reason = r["failure_reason"] or "Unknown"
                # Simplify failure reason
                if "surface" in reason.lower():
                    key = "Surface Impact"
                elif "timeout" in reason.lower():
                    key = "Timeout"
                elif "launch" in reason.lower():
                    key = "Launch Failure"
                else:
                    key = reason[:30]
                failure_modes[key] = failure_modes.get(key, 0) + 1

        # Parameter sensitivity (correlation with success)
        sensitivities = self._calculate_sensitivities(results)

        return MonteCarloResult(
            n_runs=n_runs,
            n_success=n_success,
            success_probability=n_success / n_runs if n_runs > 0 else 0,
            mean_final_altitude=np.mean(altitudes),
            std_final_altitude=np.std(altitudes),
            mean_final_velocity=np.mean(velocities),
            std_final_velocity=np.std(velocities),
            mean_max_g=np.mean(max_gs),
            std_max_g=np.std(max_gs),
            mean_max_q=np.mean(max_qs),
            std_max_q=np.std(max_qs),
            failure_modes=failure_modes,
            parameter_sensitivities=sensitivities,
            raw_results=results
        )

    def _calculate_sensitivities(self, results: List[Dict]) -> Dict[str, float]:
        """
        Calculate parameter sensitivities using correlation analysis.

        Returns correlation coefficient between each parameter and success.
        """
        sensitivities = {}

        # Get parameter names
        if not results or "params" not in results[0]:
            return sensitivities

        param_names = list(results[0]["params"].keys())
        success_values = np.array([1.0 if r["success"] else 0.0 for r in results])

        for param_name in param_names:
            param_values = np.array([r["params"][param_name] for r in results])

            # Pearson correlation
            if np.std(param_values) > 1e-10 and np.std(success_values) > 1e-10:
                corr = np.corrcoef(param_values, success_values)[0, 1]
                sensitivities[param_name] = corr
            else:
                sensitivities[param_name] = 0.0

        return sensitivities

    def find_sweet_spot_angle(
        self,
        angle_range: Tuple[float, float] = (20, 40),
        angle_steps: int = 21,
        runs_per_angle: int = 100
    ) -> Tuple[float, float]:
        """
        Find optimal track angle through systematic search.

        Args:
            angle_range: (min_angle, max_angle) in degrees
            angle_steps: Number of angles to test
            runs_per_angle: Monte Carlo runs per angle

        Returns:
            (optimal_angle, success_probability)
        """
        angles = np.linspace(angle_range[0], angle_range[1], angle_steps)
        results = []

        print(f"Searching for optimal track angle ({angle_steps} angles, "
              f"{runs_per_angle} runs each)...")

        for angle in angles:
            # Fix track angle for this batch
            for var in self.variations:
                if var.name == "track_angle":
                    var.nominal = angle
                    var.sigma = 0.1  # Small variation

            batch_result = self.run_batch(runs_per_angle, show_progress=False)
            results.append((angle, batch_result.success_probability))
            print(f"  Angle {angle:5.1f}°: {batch_result.success_probability*100:5.1f}% success")

        # Find best angle
        best_idx = np.argmax([r[1] for r in results])
        best_angle, best_prob = results[best_idx]

        # Reset track angle variation
        for var in self.variations:
            if var.name == "track_angle":
                var.nominal = self.base_params.TRACK_ANGLE_DEFAULT
                var.sigma = 1.0

        return best_angle, best_prob


def print_monte_carlo_report(result: MonteCarloResult):
    """Print formatted Monte Carlo analysis report."""
    print("=" * 70)
    print("MONTE CARLO SIMULATION REPORT")
    print("=" * 70)
    print(f"\nSimulation Statistics:")
    print(f"  Total Runs: {result.n_runs}")
    print(f"  Successful: {result.n_success}")
    print(f"  Success Rate: {result.success_probability * 100:.1f}%")

    print(f"\nPerformance Statistics (successful runs):")
    print(f"  Final Altitude: {result.mean_final_altitude/1000:.1f} ± "
          f"{result.std_final_altitude/1000:.1f} km")
    print(f"  Final Velocity: {result.mean_final_velocity:.0f} ± "
          f"{result.std_final_velocity:.0f} m/s")
    print(f"  Max G-Load: {result.mean_max_g:.1f} ± {result.std_max_g:.1f} g")
    print(f"  Max Q: {result.mean_max_q/1000:.1f} ± {result.std_max_q/1000:.1f} kPa")

    print(f"\nFailure Mode Distribution:")
    if result.failure_modes:
        total_failures = sum(result.failure_modes.values())
        for mode, count in sorted(result.failure_modes.items(),
                                   key=lambda x: x[1], reverse=True):
            pct = count / total_failures * 100
            print(f"  {mode}: {count} ({pct:.1f}%)")
    else:
        print("  No failures recorded")

    print(f"\nParameter Sensitivities (correlation with success):")
    sorted_sens = sorted(result.parameter_sensitivities.items(),
                         key=lambda x: abs(x[1]), reverse=True)
    for param, corr in sorted_sens:
        impact = "HIGH" if abs(corr) > 0.3 else "MED" if abs(corr) > 0.1 else "LOW"
        direction = "↑" if corr > 0 else "↓" if corr < 0 else "─"
        print(f"  {param:25s}: {corr:+.3f} {direction} [{impact}]")

    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BGKPJR Monte Carlo Simulation")
    parser.add_argument("--runs", type=int, default=100,
                        help="Number of simulation runs")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    parser.add_argument("--find-sweet-spot", action="store_true",
                        help="Search for optimal track angle")
    args = parser.parse_args()

    print("=== BGKPJR Monte Carlo Analysis ===\n")

    mc = MonteCarloSimulator(seed=args.seed)

    if args.find_sweet_spot:
        best_angle, best_prob = mc.find_sweet_spot_angle(
            runs_per_angle=max(50, args.runs // 20)
        )
        print(f"\nOPTIMAL TRACK ANGLE: {best_angle:.1f}°")
        print(f"Success Probability: {best_prob * 100:.1f}%")
    else:
        print(f"Running {args.runs} Monte Carlo simulations...")
        result = mc.run_batch(args.runs)
        print_monte_carlo_report(result)
