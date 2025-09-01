#!/usr/bin/env python3
"""Test to see how many tools are actually registered with FastMCP."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig


async def test_tool_count():
    """Test to see how many tools are actually registered."""
    print("Testing tool count...")

    config = ServerConfig()
    config.log_level = "INFO"  # Reduce noise

    server = MCPServer(config)

    # The tool_registry only tracks tools registered through it
    registry_count = len(server.tool_registry.tools)
    print(f"Tools in tool_registry: {registry_count}")

    # FastMCP tools are registered directly with the app
    # Let's see if we can get the total from the app
    if hasattr(server.app, "_tools"):
        fastmcp_count = len(server.app._tools)
        print(f"Tools registered with FastMCP: {fastmcp_count}")

    # List the tools from both
    print(f"\nTools in registry: {list(server.tool_registry.tools.keys())}")

    if hasattr(server.app, "_tools"):
        print(f"\nTools in FastMCP: {list(server.app._tools.keys())}")

    print("\n✅ Tool count analysis complete!")


if __name__ == "__main__":
    asyncio.run(test_tool_count())
