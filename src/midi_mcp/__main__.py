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
import uvicorn
from .core.server import create_server
from .config.settings import get_default_config

async def main():
    """Main entry point for running the server."""
    config = get_default_config()
    server = await create_server(config)
    
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