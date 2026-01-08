"""
BGKPJR Core Simulations
=======================

Physics simulation engine for the Brazelton Gryphon Kepler Propulsion Jump Revolution
launch architecture.

Modules:
    - constants: Physical constants and system parameters
    - atmosphere: Standard atmosphere model (ISA + extensions to 100km)
    - aerodynamics: Lift, drag, compressibility corrections
    - vehicle: Gryphon spacecraft model
    - maglev: Launch track physics
    - trajectory: Flight path integration
    - thermal: Heat transfer analysis
"""

__version__ = "0.1.0"
__author__ = "Shane Brazelton"

from .constants import Constants, SystemParams
from .atmosphere import Atmosphere
from .aerodynamics import AeroForces
from .vehicle import GryphonVehicle
from .maglev import MaglevTrack
