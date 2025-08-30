# -*- coding: utf-8 -*-
"""
MCP tools package.

Provides tool registration framework and implements all MCP tools
for MIDI operations, file management, and musical analysis.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

from .registry import ToolRegistry
from .midi_tools import register_midi_tools
from .file_tools import register_midi_file_tools

__all__ = [
    'ToolRegistry',
    'register_midi_tools',
    'register_midi_file_tools'
]