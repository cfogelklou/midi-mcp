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
from mcp.types import TextContent
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
                return [TextContent(
                    type="text",
                    text="No MIDI devices found on this system."
                )]
            
            device_list = []
            for device in devices:
                device_list.append(f"- {device} (ID: {device.device_id})")
            
            result = f"Found {len(devices)} MIDI devices:\n" + "\n".join(device_list)
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Device discovery failed: {e}")
            return [TextContent(
                type="text", 
                text=f"Error discovering MIDI devices: {str(e)}"
            )]

    @app.tool(name="connect_midi_device")
    async def connect_midi_device(device_id: str) -> List[TextContent]:
        """Connect to a specific MIDI device."""
        try:
            await midi_manager.connect_device(device_id)
            return [TextContent(
                type="text",
                text=f"Successfully connected to MIDI device: {device_id}"
            )]
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return [TextContent(
                type="text",
                text=f"Error connecting to device: {str(e)}"
            )]

    @app.tool(name="play_midi_note") 
    async def play_midi_note(
        note: str, 
        velocity: int = 64, 
        duration: float = 1.0,
        device_id: Optional[str] = None
    ) -> List[TextContent]:
        """
        Play a MIDI note on connected device.
        
        Args:
            note: Note name (C4, D#5, etc.) or MIDI number (60, 61, etc.)
            velocity: Note velocity (0-127)
            duration: Note duration in seconds
            device_id: Target device ID (optional, uses default if not specified)
        """
        try:
            # Convert note name to MIDI number if needed
            if isinstance(note, str) and not note.isdigit():
                midi_note = note_name_to_number(note)
            else:
                midi_note = int(note)
            
            # Validate inputs
            if not (0 <= midi_note <= 127):
                return [TextContent(
                    type="text",
                    text=f"Invalid MIDI note number: {midi_note}. Must be 0-127."
                )]
            
            if not (0 <= velocity <= 127):
                return [TextContent(
                    type="text", 
                    text=f"Invalid velocity: {velocity}. Must be 0-127."
                )]
            
            # Play the note
            await midi_manager.play_note(midi_note, velocity, duration, device_id)
            
            return [TextContent(
                type="text",
                text=f"Played note {note} (MIDI {midi_note}) with velocity {velocity} for {duration}s"
            )]
            
        except Exception as e:
            logger.error(f"Note playback failed: {e}")
            return [TextContent(
                type="text",
                text=f"Error playing note: {str(e)}"
            )]

    @app.tool(name="list_connected_devices")
    async def list_connected_devices() -> List[TextContent]:
        """List all currently connected MIDI devices."""
        try:
            connected = midi_manager.get_connected_devices()
            
            if not connected:
                return [TextContent(
                    type="text",
                    text="No MIDI devices currently connected."
                )]
            
            device_list = [f"- {device}" for device in connected]
            result = f"Connected MIDI devices ({len(connected)}):\n" + "\n".join(device_list)
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Error listing connected devices: {e}")
            return [TextContent(
                type="text",
                text=f"Error listing connected devices: {str(e)}"
            )]

    @app.tool(name="disconnect_midi_device")
    async def disconnect_midi_device(device_id: str) -> List[TextContent]:
        """Disconnect from a MIDI device."""
        try:
            await midi_manager.disconnect_device(device_id)
            return [TextContent(
                type="text",
                text=f"Disconnected from MIDI device: {device_id}"
            )]
            
        except Exception as e:
            logger.error(f"Error disconnecting from device: {e}")
            return [TextContent(
                type="text",
                text=f"Error disconnecting from device: {str(e)}"
            )]
    
    logger.info("Registered 6 MIDI tools")
