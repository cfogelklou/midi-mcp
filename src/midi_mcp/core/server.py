# -*- coding: utf-8 -*-
"""
Core MCP server implementation for MIDI operations.

Provides the main MCP server class with protocol handling, tool registration,
and async event loop management for MIDI operations.
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
import sys
from typing import Any, Dict, List, Optional, Callable, Awaitable
from abc import ABC, abstractmethod

from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

from ..config.settings import ServerConfig
from ..tools.registry import ToolRegistry
from ..tools.midi_tools import register_midi_tools
from ..tools.file_tools import register_midi_file_tools
from ..tools.theory_tools import register_theory_tools
from ..tools.genre_tools import register_genre_tools
from ..tools.composition_tools import register_composition_tools
from ..midi.manager import MidiManager
from ..midi.file_ops import MidiFileManager
from ..midi.player import MidiFilePlayer
from ..midi.analyzer import MidiAnalyzer
from ..utils.logger import setup_logging


class MCPServerInterface(ABC):
    """Abstract interface for MCP server implementations."""
    
    @abstractmethod
    async def start(self) -> None:
        """Start the MCP server."""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the MCP server."""
        pass
    
    @abstractmethod
    def register_tool(self, tool: Tool, handler: Callable) -> None:
        """Register a tool with its handler."""
        pass


class MCPServer(MCPServerInterface):
    """
    Main MCP server implementation for MIDI operations.
    
    Handles MCP protocol communication, tool registration, and provides
    the foundation for MIDI device management and musical operations.
    """
    
    def __init__(self, config: Optional[ServerConfig] = None) -> None:
        """
        Initialize the MCP server.
        
        Args:
            config: Server configuration. If None, uses default configuration.
        """
        self.config = config or ServerConfig()
        self.logger = setup_logging(self.config.log_level, self.config.log_file)
        
        # Initialize FastMCP server
        self.app = FastMCP("MIDI MCP Server")
        self.tool_registry = ToolRegistry()
        self._running = False
        
        # Initialize MIDI manager
        self.midi_manager = MidiManager(self.config.midi_config)
        
        # Initialize Phase 2 components (file operations, playback, analysis)
        self.file_manager = MidiFileManager()
        self.player = MidiFilePlayer()
        self.analyzer = MidiAnalyzer()
        
        self.logger.info("MIDI MCP Server initialized with Phase 1-5 capabilities (MIDI + Music Theory + Genre Knowledge + Composition)")
        
        # Register core server info handlers
        self._setup_server_info()
        self._register_default_tools()
        self._register_midi_tools()
        self._register_theory_tools()
        self._register_genre_tools()
        self._register_composition_tools()
    
    def _setup_server_info(self) -> None:
        """Set up server information and capabilities."""
        # FastMCP handles server info automatically, so we just need to ensure
        # our app is properly configured with name and description
        self.logger.debug("Server info configured via FastMCP initialization")
    
    def _register_default_tools(self) -> None:
        """Register default tools for basic server functionality."""
        
        # Server status tool
        status_tool = Tool(
            name="server_status",
            description="Get the current status of the MIDI MCP server",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        
        @self.app.tool(name="server_status")
        async def server_status() -> List[TextContent]:
            """Get server status information."""
            status = {
                "running": self._running,
                "tools_registered": len(self.tool_registry.tools),
                "config": {
                    "log_level": self.config.log_level,
                    "debug_mode": self.config.debug_mode
                }
            }
            
            # Add MIDI backend information if MIDI is enabled
            if self.config.enable_midi and self.midi_manager:
                backend_status = self.midi_manager.get_backend_status()
                status["midi_backends"] = backend_status
                
                # Add connected devices count
                connected_devices = self.midi_manager.get_connected_devices()
                status["connected_devices"] = len(connected_devices)
                
                # Add file manager status
                midi_files = self.file_manager.list_midi_files()
                status["loaded_midi_files"] = len(midi_files)
                
                # Add player status
                active_playbacks = self.player.list_active_playbacks()
                status["active_playbacks"] = len(active_playbacks)
            
            return [TextContent(
                type="text",
                text=f"MIDI MCP Server Status:\n{status}"
            )]
        
        self.tool_registry.register("server_status", status_tool, server_status)
        self.logger.debug("Registered default tools")
    
    def _register_midi_tools(self) -> None:
        """Register MIDI-specific tools."""
        if self.config.enable_midi:
            # Register Phase 1 tools (basic MIDI operations)
            register_midi_tools(self.app, self.midi_manager)
            
            # Register Phase 2 tools (file operations, playback, analysis)
            register_midi_file_tools(
                self.app, 
                self.tool_registry, 
                self.midi_manager,
                self.file_manager,
                self.player,
                self.analyzer
            )
            
            self.logger.debug("Registered MIDI tools (Phase 1 & Phase 2)")
        else:
            self.logger.info("MIDI tools disabled in configuration")
    
    def _register_theory_tools(self) -> None:
        """Register music theory tools (Phase 3)."""
        try:
            # Register Phase 3 tools (music theory)
            register_theory_tools(self.app)
            self.logger.debug("Registered music theory tools (Phase 3)")
        except Exception as e:
            self.logger.error(f"Error registering theory tools: {e}")
    
    def _register_genre_tools(self) -> None:
        """Register genre knowledge tools (Phase 4)."""
        try:
            # Register Phase 4 tools (genre knowledge and composition)
            register_genre_tools(self.app)
            self.logger.debug("Registered genre knowledge tools (Phase 4)")
        except Exception as e:
            self.logger.error(f"Error registering genre tools: {e}")
    
    def _register_composition_tools(self) -> None:
        """Register advanced composition tools (Phase 5)."""
        try:
            # Register Phase 5 tools (song structure, melodic development, etc.)
            register_composition_tools(self.app)
            self.logger.debug("Registered composition tools (Phase 5)")
        except Exception as e:
            self.logger.error(f"Error registering composition tools: {e}")
    
    def register_tool(self, tool: Tool, handler: Callable) -> None:
        """
        Register a tool with the server.
        
        Args:
            tool: The MCP tool definition
            handler: Async function to handle the tool call
        """
        self.tool_registry.register(tool.name, tool, handler)
        
        # Register with FastMCP
        self.app.tool(name=tool.name)(handler)
        
        self.logger.info(f"Registered tool: {tool.name}")
    
    async def start(self) -> None:
        """Start the MCP server."""
        try:
            self._running = True
            self.logger.info("Starting MIDI MCP Server")
            
            # FastMCP servers run via stdin/stdout, not as async servers
            # For standalone testing, we just mark as running and wait
            self.logger.info("Server ready for MCP connections via stdio")
            self.logger.info(f"Registered {len(self.tool_registry.tools)} tools")
            
            # In a real MCP environment, the host will connect via stdio
            # For testing, we can just keep the server alive
            try:
                while self._running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Server shutdown requested")
                self._running = False
            
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            self._running = False
            raise
    
    async def stop(self) -> None:
        """Stop the MCP server."""
        self.logger.info("Stopping MIDI MCP Server")
        self._running = False
        
        # Clean up any resources
        await self._cleanup()
    
    async def _cleanup(self) -> None:
        """Clean up server resources."""
        try:
            # Stop all MIDI playback
            if hasattr(self, 'player'):
                await self.player.stop_all_playback()
            
            # Clean up MIDI manager
            if hasattr(self, 'midi_manager'):
                await self.midi_manager.cleanup()
            
            self.logger.debug("Server cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def get_registered_tools(self) -> List[Tool]:
        """Get list of all registered tools."""
        return list(self.tool_registry.tools.values())
    
    @property
    def is_running(self) -> bool:
        """Check if the server is currently running."""
        return self._running


async def create_server(config: Optional[ServerConfig] = None) -> MCPServer:
    """
    Factory function to create and initialize an MCP server.
    
    Args:
        config: Server configuration
        
    Returns:
        Initialized MCP server instance
    """
    server = MCPServer(config)
    return server


async def main() -> None:
    """Main entry point for running the server directly."""
    try:
        config = ServerConfig()
        server = await create_server(config)
        await server.start()
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Server shutdown requested")
    except Exception as e:
        logging.getLogger(__name__).error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())