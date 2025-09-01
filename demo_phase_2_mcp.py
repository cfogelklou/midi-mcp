# -*- coding: utf-8 -*-
"""
Demonstration of Phase 2 MCP tools.

Shows how to use the new MIDI file tools through the MCP interface.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import logging
import json
from typing import Any, Dict

from src.midi_mcp.core.server import MCPServer
from src.midi_mcp.config.settings import ServerConfig
from src.midi_mcp.utils.logger import setup_logging


async def demonstrate_mcp_tools():
    """Demonstrate Phase 2 MCP tools functionality."""
    logger = setup_logging("INFO")
    logger.info("Starting Phase 2 MCP tools demonstration")

    # Create server with configuration
    config = ServerConfig()
    server = MCPServer(config)

    # Get the tools and simulate MCP calls
    try:
        logger.info("=== Phase 2 MCP Tools Demonstration ===")

        # 1. List available tools
        tools = server.get_registered_tools()
        logger.info(f"Available tools: {len(tools)}")
        phase2_tools = [tool.name for tool in tools if "midi" in tool.name.lower()]
        logger.info(f"MIDI tools: {', '.join(phase2_tools)}")

        # 2. Create MIDI file
        logger.info("\n--- Creating MIDI File ---")
        create_result = await server.app.call_tool(
            "create_midi_file", {"title": "MCP Demo Song", "tempo": 140, "time_signature": [3, 4], "key_signature": "D"}
        )
        logger.info(f"Create result: {create_result}")

        # Extract file ID from the result (this is a simplification - in real MCP the AI would parse this)
        file_id = None
        if create_result and len(create_result) > 0:
            # create_result is a tuple: (list_of_content, metadata)
            content_list = create_result[0]
            if content_list and len(content_list) > 0:
                content = content_list[0].text
                if "ID:" in content:
                    file_id = content.split("ID:")[1].split()[0]
                    logger.info(f"Extracted file ID: {file_id}")

        if not file_id:
            logger.error("Could not extract file ID")
            return False

        # 3. Add tracks
        logger.info("\n--- Adding Tracks ---")
        tracks_to_add = [
            {"track_name": "Lead Guitar", "channel": 0, "program": 30},
            {"track_name": "Bass", "channel": 1, "program": 34},
            {"track_name": "Strings", "channel": 2, "program": 48},
            {"track_name": "Drums", "channel": 9, "program": 0},
        ]

        for track_info in tracks_to_add:
            track_result = await server.app.call_tool("add_track", {"midi_file_id": file_id, **track_info})
            logger.info(f"Added track '{track_info['track_name']}': {track_result[0][0].text}")

        # 4. Save the file
        logger.info("\n--- Saving MIDI File ---")
        save_result = await server.app.call_tool(
            "save_midi_file", {"midi_file_id": file_id, "filename": "mcp_demo_song.mid"}
        )
        logger.info(f"Save result: {save_result[0][0].text}")

        # 5. Analyze the file
        logger.info("\n--- Analyzing MIDI File ---")
        analyze_result = await server.app.call_tool("analyze_midi_file", {"midi_file_id": file_id})
        logger.info("Analysis result:")
        logger.info(analyze_result[0][0].text)

        # 6. List all files
        logger.info("\n--- Listing MIDI Files ---")
        list_result = await server.app.call_tool("list_midi_files", {})
        logger.info("Files in session:")
        logger.info(list_result[0][0].text)

        # 7. Test server status
        logger.info("\n--- Server Status ---")
        status_result = await server.app.call_tool("server_status", {})
        logger.info("Server status:")
        logger.info(status_result[0][0].text)

        # 8. Discover MIDI devices (from Phase 1)
        logger.info("\n--- MIDI Device Discovery ---")
        discover_result = await server.app.call_tool("discover_midi_devices", {})
        logger.info("MIDI devices:")
        logger.info(discover_result[0][0].text)

        logger.info("\n✓ All MCP tools demonstrated successfully!")
        return True

    except Exception as e:
        logger.error(f"✗ MCP tools demonstration failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Clean up
        await server.stop()


async def main():
    """Main demonstration runner."""
    print("MIDI MCP Server - Phase 2 MCP Tools Demo")
    print("========================================")

    success = await demonstrate_mcp_tools()

    if success:
        print("\n🎉 Phase 2 MCP tools working perfectly!")
        print("Available functionality:")
        print("✓ create_midi_file - Create new MIDI files with metadata")
        print("✓ add_track - Add tracks with instruments to MIDI files")
        print("✓ save_midi_file - Save files to disk")
        print("✓ load_midi_file - Load existing MIDI files")
        print("✓ play_midi_file - Real-time playback (needs connected device)")
        print("✓ analyze_midi_file - Comprehensive MIDI analysis")
        print("✓ list_midi_files - List session files")
        print("✓ stop_midi_playback - Control playback")
        print("\nPhase 1 tools still available:")
        print("✓ discover_midi_devices")
        print("✓ connect_midi_device")
        print("✓ play_midi_note")
        print("✓ list_connected_devices")
        print("✓ disconnect_midi_device")
        print("✓ server_status")
    else:
        print("\n❌ MCP tools demonstration failed - check logs for details")


if __name__ == "__main__":
    asyncio.run(main())
