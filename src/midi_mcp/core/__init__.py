# -*- coding: utf-8 -*-
"""
Core MCP server components.

Contains the fundamental MCP server implementation, protocol handling,
and base abstractions for the MIDI MCP server.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from .server import MCPServer
from .version import __version__

__all__ = ['MCPServer', '__version__']