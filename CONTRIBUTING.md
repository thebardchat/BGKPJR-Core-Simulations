# Contributing to BGKPJR Core Simulations

Thank you for your interest in contributing to the BGKPJR project! This document provides guidelines for contributing to the simulation codebase.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Priority Areas](#priority-areas)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors are expected to:

- Be respectful and constructive in discussions
- Focus on technical merit and project goals
- Welcome newcomers and help them contribute
- Accept constructive criticism gracefully

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- Familiarity with aerospace engineering concepts (helpful but not required)

### Setup
```bash
# Clone the repository
git clone https://github.com/your-org/BGKPJR-Core-Simulations.git
cd BGKPJR-Core-Simulations

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # if available

# Run tests to verify setup
pytest simulation/tests/
```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes
- Write code following our standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run unit tests
pytest simulation/tests/

# Run specific module tests
pytest simulation/tests/test_aerodynamics.py

# Check code style
flake8 simulation/src/
black --check simulation/src/
```

### 4. Commit and Push
```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 5. Open a Pull Request
- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Request review from maintainers

## Code Standards

### Python Style
We follow PEP 8 with the following specifics:
- Line length: 100 characters maximum
- Use type hints for function signatures
- Docstrings for all public functions (Google style)

### Example
```python
def calculate_lift(
    velocity: float,
    altitude: float,
    angle_of_attack: float
) -> float:
    """
    Calculate aerodynamic lift force.

    Args:
        velocity: True airspeed in m/s
        altitude: Geometric altitude in meters
        angle_of_attack: Angle of attack in degrees

    Returns:
        Lift force in Newtons

    Raises:
        ValueError: If velocity is negative
    """
    if velocity < 0:
        raise ValueError("Velocity must be non-negative")

    # Implementation...
    return lift_force
```

### Naming Conventions
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### File Organization
```
simulation/src/
├── __init__.py          # Package initialization
├── constants.py         # Physical constants
├── atmosphere.py        # Atmosphere model
├── aerodynamics.py      # Aero force calculations
├── vehicle.py           # Spacecraft model
├── maglev.py            # Track physics
├── trajectory_sim.py    # Trajectory integration
├── thermal.py           # Heat transfer
└── monte_carlo.py       # Statistical analysis
```

## Testing Requirements

### Test Coverage
- All new functions must have unit tests
- Target: 80% code coverage minimum
- Integration tests for module interactions

### Test Structure
```python
# simulation/tests/test_aerodynamics.py

import pytest
from simulation.src.aerodynamics import AeroForces

class TestAeroForces:
    def test_subsonic_lift(self):
        """Test lift calculation in subsonic regime."""
        aero = AeroForces(reference_area=120, reference_length=25)
        result = aero.calculate_forces(velocity=200, altitude=5000, alpha_deg=5)

        assert result.coefficients.CL > 0
        assert result.flight_regime == "subsonic"

    def test_mach_zero_handling(self):
        """Test behavior at zero velocity."""
        aero = AeroForces(reference_area=120, reference_length=25)
        result = aero.calculate_forces(velocity=0.1, altitude=0, alpha_deg=0)

        assert result.mach < 0.01
```

## Documentation

### Code Documentation
- All public functions need docstrings
- Complex algorithms should have inline comments
- Reference equations with sources

### Markdown Documentation
- Update relevant docs in `docs/` when adding features
- Keep README.md current with major changes
- Add examples for new functionality

## Priority Areas

We especially welcome contributions in these areas:

### High Priority
1. **CFD Validation:** Comparing analytical models against CFD results
2. **Control Systems:** Implementing advanced GNC algorithms
3. **Thermal Analysis:** Improving heat transfer models

### Medium Priority
4. **Visualization:** Matplotlib/Plotly trajectory plotting
5. **Optimization:** Trajectory optimization algorithms
6. **Materials Database:** TPS material property data

### Good First Issues
- Improving unit test coverage
- Documentation improvements
- Code style fixes
- Adding input validation

## Questions?

- Open an issue for technical questions
- Tag maintainers for guidance
- Check existing issues/PRs for similar discussions

---

Thank you for contributing to the future of space access!
