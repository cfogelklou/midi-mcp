#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 Demo - MIDI File Operations

Demonstrates MIDI file creation, multi-track composition, analysis,
and playback capabilities.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig


async def demo_phase_2_workflow():
    """Demonstrate a complete Phase 2 workflow."""
    print("🎵 MIDI MCP Server - Phase 2 Demo")
    print("==================================")

    # Initialize server
    config = ServerConfig()
    server = MCPServer(config)

    try:
        print(f"\n✓ Server initialized with {len(server.get_registered_tools())} tools")

        print("\n1. Creating a new MIDI file...")
        result = await server.app.call_tool(
            "create_midi_file", {"title": "Demo Song", "tempo": 128, "time_signature": [4, 4], "key_signature": "G"}
        )
        print(f"   Result: {result[0][0].text}")

        # Extract file ID (in real usage, AI agent would parse this)
        file_id = result[0][0].text.split("ID: ")[1].split("\n")[0]

        print("\n2. Adding tracks...")
        tracks = [
            {"track_name": "Piano", "channel": 0, "program": 0},
            {"track_name": "Bass", "channel": 1, "program": 32},
            {"track_name": "Drums", "channel": 9, "program": 0},
        ]

        for track in tracks:
            result = await server.app.call_tool("add_track", {"midi_file_id": file_id, **track})
            print(f"   Added: {track['track_name']}")

        print("\n3. Saving MIDI file...")
        result = await server.app.call_tool("save_midi_file", {"midi_file_id": file_id, "filename": "demo_song.mid"})
        print(f"   Result: {result[0][0].text}")

        print("\n4. Analyzing the file...")
        result = await server.app.call_tool("analyze_midi_file", {"midi_file_id": file_id})
        print("   Analysis:")
        print(result[0][0].text)

        print("\n5. Discovering MIDI devices...")
        result = await server.app.call_tool("discover_midi_devices", {})
        print(f"   {result[0][0].text}")

        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("- Connect a MIDI device to test playback")
        print("- Add actual notes to tracks")
        print("- Explore music theory tools (Phase 3)")

    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(demo_phase_2_workflow())
