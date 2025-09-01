#!/usr/bin/env python3
"""Quick test to verify the server functionality after singleton implementation."""

import sys
import os
import asyncio
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig

async def test_server_functionality():
    """Test that the server can start without errors."""
    print("Testing server functionality...")
    
    # Create server with debug logging to see what's happening
    config = ServerConfig()
    config.log_level = "DEBUG"
    
    server = MCPServer(config)
    
    # Check that tools are registered
    tool_count = len(server.tool_registry.tools)
    print(f"Registered tools: {tool_count}")
    
    # List some tools
    tools = list(server.tool_registry.tools.keys())[:10]  # First 10 tools
    print(f"Sample tools: {tools}")
    
    # Test that library integration is working
    from midi_mcp.genres.library_integration import LibraryIntegration
    lib = LibraryIntegration()
    available = lib.get_available_libraries()
    print(f"Available libraries: {available}")
    
    print("✅ Server functionality test passed!")

if __name__ == "__main__":
    asyncio.run(test_server_functionality())
