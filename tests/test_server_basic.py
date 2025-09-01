# -*- coding: utf-8 -*-
"""
Basic server functionality tests.

Tests basic server initialization, configuration, and tool registration
to validate the foundation architecture.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import pytest
import asyncio
from unittest.mock import patch

from midi_mcp.core.server import MCPServer, create_server
from midi_mcp.config.settings import ServerConfig, MidiConfig


class TestServerBasic:
    """Test basic server functionality."""

    def test_server_initialization(self):
        """Test server can be initialized with default config."""
        config = ServerConfig()
        server = MCPServer(config)

        assert server is not None
        assert server.config == config
        assert not server.is_running
        assert server.app is not None
        assert server.tool_registry is not None
        assert server.midi_manager is not None

    def test_server_initialization_no_config(self):
        """Test server can be initialized without config."""
        server = MCPServer()

        assert server is not None
        assert server.config is not None
        assert isinstance(server.config, ServerConfig)
        assert not server.is_running

    def test_tool_registry_has_default_tools(self):
        """Test that default tools are registered."""
        server = MCPServer()

        # Should have at least the server_status tool
        tools = server.get_registered_tools()
        tool_names = [tool.name for tool in tools]

        assert "server_status" in tool_names

        # Should also have MIDI tools if enabled
        if server.config.enable_midi:
            assert "discover_midi_devices" in tool_names
            assert "connect_midi_device" in tool_names
            assert "play_midi_note" in tool_names

    @pytest.mark.asyncio
    async def test_create_server_factory(self):
        """Test server factory function."""
        config = ServerConfig()
        server = await create_server(config)

        assert isinstance(server, MCPServer)
        assert server.config == config

    def test_config_validation(self):
        """Test configuration validation."""
        config = ServerConfig()

        # Should not raise exception
        config.validate()

        # Test invalid config
        config.port = -1
        with pytest.raises(ValueError):
            config.validate()

    def test_midi_config_validation(self):
        """Test MIDI configuration validation."""
        midi_config = MidiConfig()

        # Should not raise exception
        midi_config.validate()

        # Test invalid config
        midi_config.max_latency_ms = -1
        with pytest.raises(ValueError):
            midi_config.validate()


if __name__ == "__main__":
    pytest.main([__file__])
