"""Music theory module for MIDI MCP server.

This module provides comprehensive music theory functionality including:
- Scale generation and analysis
- Chord construction and identification  
- Chord progression analysis
- Key detection and modulation
- Voice leading validation
- Comprehensive harmonic analysis
"""

from .constants import *
from .scales import ScaleManager
from .chords import ChordManager  
from .progressions import ProgressionManager
from .keys import KeyManager
from .voice_leading import VoiceLeadingManager
from .analysis import MusicAnalyzer

__all__ = [
    'ScaleManager',
    'ChordManager', 
    'ProgressionManager',
    'KeyManager',
    'VoiceLeadingManager',
    'MusicAnalyzer',
]