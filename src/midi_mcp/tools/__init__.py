# -*- coding: utf-8 -*-
"""
MCP tools for MIDI operations.

Provides MCP tool implementations for MIDI device management,
note playing, and musical operations.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from .registry import ToolRegistry
from .midi_tools import register_midi_tools

__all__ = ['ToolRegistry', 'register_midi_tools']