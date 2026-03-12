"""Plakoto game package - A traditional backgammon variant."""

__version__ = "5.0.0"
__author__ = "S4_L2N1 Team"
__description__ = "Plakoto game implementation with text and graphical interfaces"

# Core game components
from .core.board import *
from .core.moves import *

# Interfaces
from .interfaces.text_interface import TextInterface
from .interfaces.graphical_interface import GraphicalInterface

# Utility functions
from .utils.save_load import sauvegarder_partie, charger_partie

# Convenience imports for common functionality
__all__ = [
    'TextInterface', 
    'GraphicalInterface',
    'init_plateau',
    'afficher_plateau',
    'sauvegarder_partie',
    'charger_partie',
]
