"""Genre knowledge system for the MIDI MCP Server.

This module provides comprehensive genre-specific musical knowledge through
generic, parameterized tools that work with any musical genre.
"""

from .genre_manager import GenreManager
from .composition_engine import GenericComposer
from .pattern_library import PatternLibrary
from .fusion_engine import FusionEngine
from .validator import AuthenticityValidator

__all__ = [
    'GenreManager',
    'GenericComposer',
    'PatternLibrary',
    'FusionEngine',
    'AuthenticityValidator',
]