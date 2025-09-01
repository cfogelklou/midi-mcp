"""Genre knowledge system for the MIDI MCP Server.

This module provides comprehensive genre-specific musical knowledge through
generic, parameterized tools that work with any musical genre.
"""

from .genre_manager import GenreManager
from .composer import Composer
from .library_integration import LibraryIntegration, get_library_integration
from .pattern_library import PatternLibrary
from .fusion_engine import FusionEngine
from .validator import AuthenticityValidator

__all__ = [
    'GenreManager',
    'Composer', 
    'LibraryIntegration',
    'get_library_integration',
    'PatternLibrary',
    'FusionEngine',
    'AuthenticityValidator',
]