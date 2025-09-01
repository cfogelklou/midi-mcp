#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing MIDI MCP Server usage.

Demonstrates basic server functionality, device discovery, and note playing
capabilities of the Phase 1 implementation.
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
import sys
import logging
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig


async def demo_basic_functionality():
    """Demonstrate basic MIDI MCP Server functionality."""
    print("🎵 MIDI MCP Server Demo - Phase 1 Foundation")
    print("=" * 50)

    # Initialize server with default configuration
    config = ServerConfig()
    config.log_level = "DEBUG"  # Show debug output

    server = MCPServer(config)
    print(f"✓ Server initialized with {len(server.get_registered_tools())} tools")

    # Show available tools
    print("\n📋 Available MCP Tools:")
    for tool in server.get_registered_tools():
        print(f"   • {tool.name}: {tool.description}")

    # Demonstrate device discovery
    print("\n🔍 Discovering MIDI devices...")
    devices = await server.midi_manager.discover_devices()
    print(f"Found {len(devices)} MIDI devices:")
    for device in devices:
        print(f"   • {device}")

    if devices:
        # Demonstrate device connection and note playing
        device_id = devices[0].device_id
        print(f"\n🔗 Connecting to: {device_id}")

        try:
            device = await server.midi_manager.connect_device(device_id)
            print(f"✓ Connected to: {device.device_info.name}")

            # Play a simple melody
            print("\n🎼 Playing test melody...")
            notes = [60, 62, 64, 65, 67]  # C, D, E, F, G
            for i, note in enumerate(notes):
                print(f"   Playing note {note} ({i+1}/{len(notes)})")
                await device.send_note_on(note, 100)
                await asyncio.sleep(0.3)  # Hold note
                await device.send_note_off(note)
                await asyncio.sleep(0.1)  # Brief pause

            print("✓ Melody completed!")

            # Cleanup
            await server.midi_manager.disconnect_device(device_id)
            print("✓ Disconnected from device")

        except Exception as e:
            print(f"❌ Error during MIDI operations: {e}")

    print("\n🏁 Demo completed successfully!")
    print("\nNext Steps:")
    print("• MIDI Expert Agent will add real device support")
    print("• Testing Orchestrator will add HIL validation")
    print("• Real-time latency optimization (<10ms target)")
    print("• Cross-platform device compatibility")


async def demo_configuration_options():
    """Demonstrate configuration options."""
    print("\n⚙️  Configuration Options Demo")
    print("-" * 30)

    # Show default configuration
    config = ServerConfig.from_env()
    print("Default configuration:")
    config_dict = config.to_dict()

    for section, settings in config_dict.items():
        print(f"\n[{section.upper()}]")
        for key, value in settings.items():
            print(f"  {key}: {value}")


async def main():
    """Main demo function."""
    try:
        await demo_basic_functionality()
        await demo_configuration_options()

    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Set up logging for demo
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    print("Starting MIDI MCP Server demo...")
    asyncio.run(main())
