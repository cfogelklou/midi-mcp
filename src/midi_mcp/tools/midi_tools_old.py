# -*- coding: utf-8 -*-
"""
MCP tools for MIDI operations.

Implements MCP tools for device discovery, connection management,
note playing, and basic musical operations.
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
import logging
from typing import List, Dict, Any, Optional
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import FastMCP

from ..midi.manager import MidiManager
from ..midi.interfaces import note_name_to_number
from ..midi.exceptions import MidiError
from ..config.settings import MidiConfig


def register_midi_tools(app: FastMCP, midi_manager: MidiManager) -> None:
    """
    Register all MIDI-related MCP tools.

    Args:
        app: FastMCP application instance
        midi_manager: MIDI manager instance
    """
    logger = logging.getLogger(__name__)

    @app.tool(name="discover_midi_devices")
    async def discover_midi_devices() -> List[TextContent]:
        """Discover MIDI devices and return device information."""
        try:
            devices = await midi_manager.discover_devices()

            if not devices:
                return [TextContent(type="text", text="No MIDI devices found on this system.")]

            device_list = []
            for device in devices:
                device_list.append(f"- {device} (ID: {device.device_id})")

            result = f"Found {len(devices)} MIDI devices:\n" + "\n".join(device_list)

            return [TextContent(type="text", text=result)]

        except Exception as e:
            logger.error(f"Device discovery failed: {e}")
            return [TextContent(type="text", text=f"Error discovering MIDI devices: {str(e)}")]

    # Device connection tool
    connect_tool = Tool(
        name="connect_midi_device",
        description="Connect to a MIDI device for sending messages",
        inputSchema={
            "type": "object",
            "properties": {"device_id": {"type": "string", "description": "ID of the device to connect to"}},
            "required": ["device_id"],
        },
    )

    @app.tool(name="connect_midi_device")
    async def connect_midi_device(device_id: str) -> List[TextContent]:
        """Connect to a MIDI device."""
        try:
            # First try to connect with the provided device_id
            try:
                device = await midi_manager.connect_device(device_id)
                return [
                    TextContent(type="text", text=f"Successfully connected to MIDI device: {device.device_info.name}")
                ]
            except Exception:
                # If that fails, try to find device by name
                devices = await midi_manager.discover_devices()
                matching_device = None

                for dev in devices:
                    if dev.name == device_id:
                        matching_device = dev
                        break

                if matching_device:
                    device = await midi_manager.connect_device(matching_device.device_id)
                    return [
                        TextContent(
                            type="text",
                            text=f"Successfully connected to MIDI device: {device.device_info.name} (using name lookup)",
                        )
                    ]
                else:
                    raise Exception(f"MIDI device not found: {device_id}")

        except MidiError as e:
            logger.error(f"MIDI connection error: {e}")
            return [TextContent(type="text", text=f"MIDI Error: {str(e)}")]
        except Exception as e:
            logger.error(f"Unexpected error connecting to device: {e}")
            return [TextContent(type="text", text=f"Error connecting to device: {str(e)}")]

    registry.register("connect_midi_device", connect_tool, connect_midi_device)

    # Play note tool
    play_note_tool = Tool(
        name="play_midi_note",
        description="Play a single MIDI note with specified duration and velocity",
        inputSchema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "ID of the device to play the note on"},
                "note": {
                    "type": ["integer", "string"],
                    "description": "MIDI note number (0-127) or note name (e.g., 'C4', 'A#3')",
                },
                "duration": {
                    "type": "number",
                    "description": "Duration to play the note in seconds",
                    "minimum": 0.1,
                    "maximum": 10.0,
                },
                "velocity": {
                    "type": "integer",
                    "description": "Note velocity (volume) from 1-127",
                    "minimum": 1,
                    "maximum": 127,
                    "default": 100,
                },
                "channel": {
                    "type": "integer",
                    "description": "MIDI channel (0-15)",
                    "minimum": 0,
                    "maximum": 15,
                    "default": 0,
                },
            },
            "required": ["device_id", "note", "duration"],
        },
    )

    @app.tool(name="play_midi_note")
    async def play_midi_note(
        device_id: str, note: Any, duration: float, velocity: int = 100, channel: int = 0
    ) -> List[TextContent]:
        """Play a MIDI note for the specified duration."""
        try:
            # Convert note name to number if needed
            if isinstance(note, str):
                note_number = note_name_to_number(note)
            else:
                note_number = int(note)

            # Validate parameters
            if not 0 <= note_number <= 127:
                return [TextContent(type="text", text=f"Invalid note number: {note_number}. Must be 0-127.")]

            if not 0.1 <= duration <= 10.0:
                return [TextContent(type="text", text=f"Invalid duration: {duration}. Must be 0.1-10.0 seconds.")]

            # Get connected device
            device = await midi_manager.get_device(device_id)
            if not device:
                return [TextContent(type="text", text=f"Device not found or not connected: {device_id}")]

            # Play the note
            await device.send_note_on(note_number, velocity, channel)
            await asyncio.sleep(duration)
            await device.send_note_off(note_number, 64, channel)

            note_name = f"note {note_number}"
            if isinstance(note, str):
                note_name = f"{note} (note {note_number})"

            return [
                TextContent(type="text", text=f"Played {note_name} for {duration} seconds on {device.device_info.name}")
            ]

        except MidiError as e:
            logger.error(f"MIDI error playing note: {e}")
            return [TextContent(type="text", text=f"MIDI Error: {str(e)}")]
        except Exception as e:
            logger.error(f"Unexpected error playing note: {e}")
            return [TextContent(type="text", text=f"Error playing note: {str(e)}")]

    registry.register("play_midi_note", play_note_tool, play_midi_note)

    # List connected devices tool
    list_connected_tool = Tool(
        name="list_connected_devices",
        description="List all currently connected MIDI devices",
        inputSchema={"type": "object", "properties": {}, "required": []},
    )

    @app.tool(name="list_connected_devices")
    async def list_connected_devices() -> List[TextContent]:
        """List all connected MIDI devices."""
        try:
            connected_devices = midi_manager.get_connected_devices()

            if not connected_devices:
                return [TextContent(type="text", text="No MIDI devices are currently connected.")]

            device_list = []
            for device in connected_devices:
                device_list.append(f"- {device.device_info}")

            result = f"Connected MIDI devices ({len(connected_devices)}):\n" + "\n".join(device_list)

            return [TextContent(type="text", text=result)]

        except Exception as e:
            logger.error(f"Error listing connected devices: {e}")
            return [TextContent(type="text", text=f"Error listing connected devices: {str(e)}")]

    registry.register("list_connected_devices", list_connected_tool, list_connected_devices)

    # Disconnect device tool
    disconnect_tool = Tool(
        name="disconnect_midi_device",
        description="Disconnect from a MIDI device",
        inputSchema={
            "type": "object",
            "properties": {"device_id": {"type": "string", "description": "ID of the device to disconnect from"}},
            "required": ["device_id"],
        },
    )

    @app.tool(name="disconnect_midi_device")
    async def disconnect_midi_device(device_id: str) -> List[TextContent]:
        """Disconnect from a MIDI device."""
        try:
            await midi_manager.disconnect_device(device_id)
            return [TextContent(type="text", text=f"Disconnected from MIDI device: {device_id}")]

        except Exception as e:
            logger.error(f"Error disconnecting from device: {e}")
            return [TextContent(type="text", text=f"Error disconnecting from device: {str(e)}")]

    registry.register("disconnect_midi_device", disconnect_tool, disconnect_midi_device)

    logger.info(f"Registered {len(registry.get_tool_names())} MIDI tools")
