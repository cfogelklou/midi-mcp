# -*- coding: utf-8 -*-
"""
Main entry point for MIDI MCP Server.

Allows the package to be run with `python -m midi_mcp`.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import sys

from .core.server import MCPServer
from .config.settings import ServerConfig

if __name__ == "__main__":
    # FastMCP servers run via stdio for MCP protocol communication
    config = ServerConfig()
    server = MCPServer(config)

    # Run the FastMCP server (handles stdio communication)
    server.app.run()
