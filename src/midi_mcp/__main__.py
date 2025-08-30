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

import asyncio
import argparse
import uvicorn
from .core.server import create_server
from .config.settings import get_default_config

async def main():
    """Main entry point for running the server."""
    parser = argparse.ArgumentParser(description="MIDI MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Run in stdio mode for MCP communication")
    args = parser.parse_args()

    config = get_default_config()
    server = create_server(config)

    if args.stdio:
        # Run the FastMCP server (handles stdio communication)
        await server.app.run_stdio_async()
    else:
        # Run the uvicorn server for port-based communication
        uvicorn_config = uvicorn.Config(
            server.app,
            host=config.host,
            port=config.port,
            log_level=config.log_level.lower(),
        )
        uvicorn_server = uvicorn.Server(uvicorn_config)
        await uvicorn_server.serve()

if __name__ == "__main__":
    asyncio.run(main())