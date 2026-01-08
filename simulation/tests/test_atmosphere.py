"""
Unit tests for atmosphere module.

Validates the ISA atmosphere model against standard values.
"""

import pytest
import math
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from atmosphere import Atmosphere, TubeAtmosphere


class TestAtmosphere:
    """Tests for standard atmosphere model."""

    def test_sea_level_temperature(self):
        """Sea level temperature should be 288.15 K."""
        T = Atmosphere.temperature(0)
        assert abs(T - 288.15) < 0.01

    def test_sea_level_pressure(self):
        """Sea level pressure should be 101325 Pa."""
        P = Atmosphere.pressure(0)
        assert abs(P - 101325) < 1

    def test_sea_level_density(self):
        """Sea level density should be 1.225 kg/m³."""
        rho = Atmosphere.density(0)
        assert abs(rho - 1.225) < 0.001

    def test_tropopause_temperature(self):
        """Temperature at 11 km should be ~216.65 K."""
        T = Atmosphere.temperature(11000)
        assert abs(T - 216.65) < 1

    def test_temperature_decreases_in_troposphere(self):
        """Temperature should decrease with altitude in troposphere."""
        T_low = Atmosphere.temperature(0)
        T_high = Atmosphere.temperature(10000)
        assert T_high < T_low

    def test_pressure_decreases_with_altitude(self):
        """Pressure should always decrease with altitude."""
        for h in [0, 10000, 30000, 50000, 80000]:
            P1 = Atmosphere.pressure(h)
            P2 = Atmosphere.pressure(h + 1000)
            assert P2 < P1

    def test_speed_of_sound_sea_level(self):
        """Speed of sound at sea level should be ~340 m/s."""
        a = Atmosphere.speed_of_sound(0)
        assert abs(a - 340.29) < 1

    def test_viscosity_positive(self):
        """Viscosity should always be positive."""
        for h in [0, 10000, 50000, 100000]:
            mu = Atmosphere.viscosity(h)
            assert mu > 0

    def test_get_conditions_returns_all_properties(self):
        """get_conditions should return complete state."""
        cond = Atmosphere.get_conditions(10000)

        assert hasattr(cond, 'temperature')
        assert hasattr(cond, 'pressure')
        assert hasattr(cond, 'density')
        assert hasattr(cond, 'speed_of_sound')
        assert hasattr(cond, 'viscosity')
        assert hasattr(cond, 'mean_free_path')

    def test_high_altitude_extrapolation(self):
        """Model should handle altitudes > 85 km without error."""
        cond = Atmosphere.get_conditions(150000)

        assert cond.temperature > 0
        assert cond.pressure > 0
        assert cond.density > 0


class TestTubeAtmosphere:
    """Tests for evacuated tube atmosphere."""

    def test_pressure_ratio(self):
        """Tube pressure should be reduced by pressure ratio."""
        tube = TubeAtmosphere(0.1)
        std = Atmosphere.get_conditions(0)
        tube_cond = tube.get_conditions(0)

        assert abs(tube_cond.pressure - std.pressure * 0.1) < 1

    def test_density_ratio(self):
        """Tube density should be reduced proportionally."""
        tube = TubeAtmosphere(0.1)
        std = Atmosphere.get_conditions(0)
        tube_cond = tube.get_conditions(0)

        assert abs(tube_cond.density - std.density * 0.1) < 0.001

    def test_temperature_unchanged(self):
        """Tube temperature should match standard atmosphere."""
        tube = TubeAtmosphere(0.1)
        std = Atmosphere.get_conditions(0)
        tube_cond = tube.get_conditions(0)

        assert abs(tube_cond.temperature - std.temperature) < 0.01

    def test_invalid_pressure_ratio(self):
        """Should raise error for invalid pressure ratio."""
        with pytest.raises(ValueError):
            TubeAtmosphere(1.5)

        with pytest.raises(ValueError):
            TubeAtmosphere(-0.1)


class TestKnudsenNumber:
    """Tests for flow regime determination."""

    def test_continuum_at_sea_level(self):
        """Flow should be continuum at sea level for typical vehicles."""
        Kn = Atmosphere.knudsen_number(0, 25)  # 25 m vehicle
        assert Kn < 0.01  # Continuum regime

    def test_rarefied_at_high_altitude(self):
        """Flow becomes rarefied at very high altitudes."""
        Kn = Atmosphere.knudsen_number(200000, 25)  # 200 km
        assert Kn > 0.01  # Not continuum


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
