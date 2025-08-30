# -*- coding: utf-8 -*-
"""
Utility modules for MIDI MCP Server.

Provides common utilities for logging, error handling, timing,
and other cross-cutting concerns.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from .logger import setup_logging
from .timing import Timer, measure_latency

__all__ = ['setup_logging', 'Timer', 'measure_latency']