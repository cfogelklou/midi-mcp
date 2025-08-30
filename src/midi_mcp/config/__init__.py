# -*- coding: utf-8 -*-
"""
Configuration management for MIDI MCP Server.

Provides configuration classes and utilities for server settings,
MIDI device configuration, and runtime parameters.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from .settings import ServerConfig, MidiConfig

__all__ = ['ServerConfig', 'MidiConfig']