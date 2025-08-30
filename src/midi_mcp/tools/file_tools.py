# -*- coding: utf-8 -*-
"""
MCP tools for MIDI file operations.

Implements MCP tools for creating, loading, saving, and playing MIDI files.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import logging
from typing import List, Dict, Any, Optional
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import FastMCP

from ..midi.file_ops import MidiFileManager
from ..midi.player import MidiFilePlayer
from ..midi.analyzer import MidiAnalyzer
from ..midi.manager import MidiManager
from ..midi.exceptions import MidiError
from .registry import ToolRegistry


def register_midi_file_tools(
    app: FastMCP, 
    registry: ToolRegistry, 
    midi_manager: MidiManager,
    file_manager: MidiFileManager,
    player: MidiFilePlayer,
    analyzer: MidiAnalyzer
) -> None:
    """
    Register all MIDI file-related MCP tools.
    
    Args:
        app: FastMCP application instance
        registry: Tool registry
        midi_manager: MIDI manager instance
        file_manager: MIDI file manager instance
        player: MIDI file player instance
        analyzer: MIDI analyzer instance
    """
    logger = logging.getLogger(__name__)
    
    # Create MIDI file tool
    create_file_tool = Tool(
        name="create_midi_file",
        description="Create a new MIDI file with basic metadata",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Song title for metadata",
                    "default": "Untitled"
                },
                "tempo": {
                    "type": "integer",
                    "description": "Tempo in BPM",
                    "minimum": 60,
                    "maximum": 200,
                    "default": 120
                },
                "time_signature": {
                    "type": "array",
                    "description": "Time signature as [numerator, denominator]",
                    "items": {"type": "integer"},
                    "minItems": 2,
                    "maxItems": 2,
                    "default": [4, 4]
                },
                "key_signature": {
                    "type": "string",
                    "description": "Key signature (C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F)",
                    "enum": ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"],
                    "default": "C"
                }
            },
            "required": []
        }
    )
    
    @app.tool(name="create_midi_file")
    async def create_midi_file(
        title: str = "Untitled",
        tempo: int = 120,
        time_signature: List[int] = [4, 4],
        key_signature: str = "C"
    ) -> List[TextContent]:
        """Create a new MIDI file with basic metadata."""
        try:
            file_id = file_manager.create_midi_file(
                title=title,
                tempo=tempo,
                time_signature=tuple(time_signature),
                key_signature=key_signature
            )
            
            return [TextContent(
                type="text",
                text=f"Created MIDI file '{title}' with ID: {file_id}\n"
                     f"Settings: {tempo} BPM, {time_signature[0]}/{time_signature[1]} time, Key of {key_signature}"
            )]
            
        except MidiError as e:
            logger.error(f"MIDI file creation error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error creating MIDI file: {e}")
            return [TextContent(
                type="text",
                text=f"Error creating MIDI file: {str(e)}"
            )]
    
    registry.register("create_midi_file", create_file_tool, create_midi_file)
    
    # Add track tool
    add_track_tool = Tool(
        name="add_track",
        description="Add a new track to an existing MIDI file",
        inputSchema={
            "type": "object",
            "properties": {
                "midi_file_id": {
                    "type": "string",
                    "description": "ID of the MIDI file"
                },
                "track_name": {
                    "type": "string",
                    "description": "Name for the track"
                },
                "channel": {
                    "type": "integer",
                    "description": "MIDI channel (0-15)",
                    "minimum": 0,
                    "maximum": 15,
                    "default": 0
                },
                "program": {
                    "type": "integer",
                    "description": "MIDI program number (instrument, 0-127)",
                    "minimum": 0,
                    "maximum": 127,
                    "default": 0
                }
            },
            "required": ["midi_file_id", "track_name"]
        }
    )
    
    @app.tool(name="add_track")
    async def add_track(
        midi_file_id: str,
        track_name: str,
        channel: int = 0,
        program: int = 0
    ) -> List[TextContent]:
        """Add a new track to an existing MIDI file."""
        try:
            track_index = file_manager.add_track(
                midi_file_id=midi_file_id,
                track_name=track_name,
                channel=channel,
                program=program
            )
            
            return [TextContent(
                type="text",
                text=f"Added track '{track_name}' to MIDI file {midi_file_id}\n"
                     f"Track index: {track_index}, Channel: {channel}, Program: {program}"
            )]
            
        except MidiError as e:
            logger.error(f"Track addition error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error adding track: {e}")
            return [TextContent(
                type="text",
                text=f"Error adding track: {str(e)}"
            )]
    
    registry.register("add_track", add_track_tool, add_track)
    
    # Save MIDI file tool
    save_file_tool = Tool(
        name="save_midi_file",
        description="Save MIDI file to disk",
        inputSchema={
            "type": "object",
            "properties": {
                "midi_file_id": {
                    "type": "string",
                    "description": "ID of the MIDI file to save"
                },
                "filename": {
                    "type": "string",
                    "description": "Output filename (should end in .mid or .midi)"
                }
            },
            "required": ["midi_file_id", "filename"]
        }
    )
    
    @app.tool(name="save_midi_file")
    async def save_midi_file(midi_file_id: str, filename: str) -> List[TextContent]:
        """Save MIDI file to disk."""
        try:
            saved_path = file_manager.save_midi_file(midi_file_id, filename)
            
            return [TextContent(
                type="text",
                text=f"MIDI file saved successfully to: {saved_path}"
            )]
            
        except MidiError as e:
            logger.error(f"File save error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error saving file: {e}")
            return [TextContent(
                type="text",
                text=f"Error saving file: {str(e)}"
            )]
    
    registry.register("save_midi_file", save_file_tool, save_midi_file)
    
    # Load MIDI file tool
    load_file_tool = Tool(
        name="load_midi_file",
        description="Load a MIDI file from disk",
        inputSchema={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Path to MIDI file"
                }
            },
            "required": ["filename"]
        }
    )
    
    @app.tool(name="load_midi_file")
    async def load_midi_file(filename: str) -> List[TextContent]:
        """Load a MIDI file from disk."""
        try:
            file_id = file_manager.load_midi_file(filename)
            
            # Get basic analysis
            analysis = file_manager.analyze_midi_file(file_id)
            
            return [TextContent(
                type="text",
                text=f"Loaded MIDI file '{filename}' with ID: {file_id}\n"
                     f"Title: {analysis['title']}\n"
                     f"Duration: {analysis['duration_seconds']:.2f} seconds\n"
                     f"Tracks: {analysis['tracks']}\n"
                     f"Tempo: {analysis['tempo']} BPM\n"
                     f"Notes: {analysis['note_count']}"
            )]
            
        except MidiError as e:
            logger.error(f"File load error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error loading file: {e}")
            return [TextContent(
                type="text",
                text=f"Error loading file: {str(e)}"
            )]
    
    registry.register("load_midi_file", load_file_tool, load_midi_file)
    
    # Play MIDI file tool
    play_file_tool = Tool(
        name="play_midi_file",
        description="Play a loaded MIDI file in real-time through a specified MIDI device",
        inputSchema={
            "type": "object",
            "properties": {
                "midi_file_id": {
                    "type": "string",
                    "description": "ID of the MIDI file to play"
                },
                "device_id": {
                    "type": "string",
                    "description": "ID of the connected MIDI output device"
                }
            },
            "required": ["midi_file_id", "device_id"]
        }
    )
    
    @app.tool(name="play_midi_file")
    async def play_midi_file(midi_file_id: str, device_id: str) -> List[TextContent]:
        """Play a loaded MIDI file in real-time through a specified MIDI device."""
        try:
            # Get the file session
            session = file_manager.get_session(midi_file_id)
            
            # Get the device
            device = await midi_manager.get_device(device_id)
            if not device:
                return [TextContent(
                    type="text",
                    text=f"Device not found or not connected: {device_id}"
                )]
            
            # Start playback
            playback_id = await player.play_midi_file(
                session.midi_file,
                device,
                playback_id=f"{midi_file_id}_playback"
            )
            
            return [TextContent(
                type="text",
                text=f"Started playing MIDI file '{session.title}' on device {device.device_info.name}\n"
                     f"Playback ID: {playback_id}\n"
                     f"Duration: {session.midi_file.length:.2f} seconds"
            )]
            
        except MidiError as e:
            logger.error(f"File playback error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error playing file: {e}")
            return [TextContent(
                type="text",
                text=f"Error playing file: {str(e)}"
            )]
    
    registry.register("play_midi_file", play_file_tool, play_midi_file)
    
    # Analyze MIDI file tool
    analyze_file_tool = Tool(
        name="analyze_midi_file",
        description="Analyze a loaded MIDI file for detailed information",
        inputSchema={
            "type": "object",
            "properties": {
                "midi_file_id": {
                    "type": "string",
                    "description": "ID of the MIDI file to analyze"
                }
            },
            "required": ["midi_file_id"]
        }
    )
    
    @app.tool(name="analyze_midi_file")
    async def analyze_midi_file(midi_file_id: str) -> List[TextContent]:
        """Analyze a loaded MIDI file for detailed information."""
        try:
            # Get basic analysis from file manager
            basic_analysis = file_manager.analyze_midi_file(midi_file_id)
            
            # Get comprehensive analysis from analyzer
            session = file_manager.get_session(midi_file_id)
            comprehensive_analysis = analyzer.analyze_comprehensive(session.midi_file)
            
            # Format the analysis results
            result = f"MIDI File Analysis for '{basic_analysis['title']}'\n"
            result += "=" * 50 + "\n\n"
            
            # Basic information
            result += f"File ID: {midi_file_id}\n"
            result += f"Duration: {basic_analysis['duration_seconds']:.2f} seconds\n"
            result += f"Tracks: {basic_analysis['tracks']}\n"
            result += f"Tempo: {basic_analysis['tempo']} BPM\n"
            result += f"Time Signature: {basic_analysis['time_signature'][0]}/{basic_analysis['time_signature'][1]}\n"
            result += f"Key Signature: {basic_analysis['key_signature']}\n"
            result += f"Total Notes: {basic_analysis['note_count']}\n"
            result += f"Note Density: {basic_analysis.get('note_density', 0):.2f} notes/second\n\n"
            
            # Track information
            result += "Track Information:\n"
            for track_info in basic_analysis['track_info']:
                result += f"  Track {track_info['index']}: {track_info['name']} "
                result += f"(Channel {track_info['channel']}, Program {track_info['program']})\n"
            
            result += "\n"
            
            # Instruments
            if basic_analysis['instruments']:
                result += f"Instruments Used: {', '.join(map(str, basic_analysis['instruments']))}\n"
            
            # Note range
            if basic_analysis['note_count'] > 0:
                note_range = basic_analysis['note_range']
                result += f"Note Range: {note_range['min']} - {note_range['max']}\n"
            
            # Additional comprehensive analysis summary
            dynamics = comprehensive_analysis.get('dynamics', {})
            if dynamics:
                result += f"Dynamic Range: {dynamics.get('dynamic_range', 'Unknown')}\n"
                result += f"Average Velocity: {dynamics.get('average_velocity', 0)}\n"
            
            return [TextContent(type="text", text=result)]
            
        except MidiError as e:
            logger.error(f"File analysis error: {e}")
            return [TextContent(
                type="text",
                text=f"MIDI Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error analyzing file: {e}")
            return [TextContent(
                type="text",
                text=f"Error analyzing file: {str(e)}"
            )]
    
    registry.register("analyze_midi_file", analyze_file_tool, analyze_midi_file)
    
    # List MIDI files tool
    list_files_tool = Tool(
        name="list_midi_files",
        description="List all MIDI files in the current session",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )
    
    @app.tool(name="list_midi_files")
    async def list_midi_files() -> List[TextContent]:
        """List all MIDI files in the current session."""
        try:
            files = file_manager.list_midi_files()
            
            if not files:
                return [TextContent(
                    type="text",
                    text="No MIDI files are currently loaded in the session."
                )]
            
            result = f"MIDI Files in Session ({len(files)}):\n"
            result += "=" * 40 + "\n\n"
            
            for file_info in files:
                result += f"ID: {file_info['file_id']}\n"
                result += f"Title: {file_info['title']}\n"
                result += f"Filename: {file_info['filename'] or 'Not saved'}\n"
                result += f"Tracks: {file_info['tracks']}\n"
                result += f"Tempo: {file_info['tempo']} BPM\n"
                result += f"Time Signature: {file_info['time_signature'][0]}/{file_info['time_signature'][1]}\n"
                result += f"Saved: {'Yes' if file_info['saved'] else 'No'}\n"
                result += "\n"
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Error listing MIDI files: {e}")
            return [TextContent(
                type="text",
                text=f"Error listing MIDI files: {str(e)}"
            )]
    
    registry.register("list_midi_files", list_files_tool, list_midi_files)
    
    # Stop playback tool
    stop_playback_tool = Tool(
        name="stop_midi_playback",
        description="Stop MIDI file playback",
        inputSchema={
            "type": "object",
            "properties": {
                "playback_id": {
                    "type": "string",
                    "description": "ID of the playback to stop (optional - stops all if not provided)"
                }
            },
            "required": []
        }
    )
    
    @app.tool(name="stop_midi_playback")
    async def stop_midi_playback(playback_id: Optional[str] = None) -> List[TextContent]:
        """Stop MIDI file playback."""
        try:
            if playback_id:
                success = await player.stop_playback(playback_id)
                if success:
                    return [TextContent(
                        type="text",
                        text=f"Stopped playback: {playback_id}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Playback not found: {playback_id}"
                    )]
            else:
                stopped_count = await player.stop_all_playback()
                return [TextContent(
                    type="text",
                    text=f"Stopped {stopped_count} active playback session(s)"
                )]
                
        except Exception as e:
            logger.error(f"Error stopping playback: {e}")
            return [TextContent(
                type="text",
                text=f"Error stopping playback: {str(e)}"
            )]
    
    registry.register("stop_midi_playback", stop_playback_tool, stop_midi_playback)
    
    logger.info(f"Registered {8} MIDI file tools")
