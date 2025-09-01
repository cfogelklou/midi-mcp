#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test server functionality and tool registration.

Validates that the server initializes properly, registers the expected tools,
and that library integration is working correctly.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import pytest
from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig
from midi_mcp.genres.library_integration import LibraryIntegration


class TestServerFunctionality:
    """Test server functionality and tool registration."""

    @pytest.fixture
    def server_config(self):
        """Provide server configuration for testing."""
        config = ServerConfig()
        config.log_level = "INFO"  # Less verbose for tests
        return config

    @pytest.fixture
    def server(self, server_config):
        """Provide configured server instance."""
        return MCPServer(server_config)

    @pytest.fixture
    def library_integration(self):
        """Provide library integration instance."""
        return LibraryIntegration()

    def test_server_initialization(self, server):
        """Test that server initializes properly."""
        assert server is not None
        assert hasattr(server, 'tool_registry')
        assert hasattr(server, 'config')
        assert hasattr(server, 'midi_manager')
        assert hasattr(server, 'file_manager')

    def test_tool_registration_count(self, server):
        """Test that tools are properly registered."""
        tool_count = len(server.tool_registry.tools)
        assert tool_count > 0, f"Expected tools to be registered, got {tool_count}"
        
        # Should have a reasonable number of tools (adjust based on expected count)
        # Based on our previous analysis, we expect around 15+ tools
        assert tool_count >= 10, f"Expected at least 10 tools, got {tool_count}"
        
        # Verify tools are properly structured
        assert hasattr(server.tool_registry, 'tools')
        assert isinstance(server.tool_registry.tools, dict)

    def test_critical_tools_present(self, server):
        """Test that critical tools are registered."""
        tools = list(server.tool_registry.tools.keys())
        
        # Check for essential server tools that are actually registered in tool_registry
        essential_tools = [
            "server_status",           # Basic server functionality
            "create_midi_file",        # Core MIDI file operations
            "discover_midi_devices",   # MIDI device management
            "add_musical_data_to_midi_file", # Enhanced API functionality
            "connect_midi_device",     # MIDI device connection
            "play_midi_note"          # MIDI playback
        ]
        
        for tool in essential_tools:
            assert tool in tools, f"Critical tool '{tool}' not found in registered tools. Available: {sorted(tools)}"

    def test_tool_categories_present(self, server):
        """Test that different categories of tools are present."""
        tools = list(server.tool_registry.tools.keys())
        
        # Check for MIDI file tools
        midi_file_tools = [tool for tool in tools if 'midi_file' in tool or 'midi' in tool]
        assert len(midi_file_tools) > 0, "Expected MIDI file tools to be registered"
        
        # Check for MIDI device tools
        device_tools = [tool for tool in tools if 'midi_device' in tool or 'discover' in tool or 'connect' in tool]
        assert len(device_tools) > 0, "Expected MIDI device tools to be registered"
        
        # Check for enhanced API tools
        enhanced_tools = [tool for tool in tools if 'musical_data' in tool or 'add_track' in tool]
        assert len(enhanced_tools) > 0, "Expected enhanced API tools to be registered"

    def test_server_configuration(self, server):
        """Test that server configuration is properly applied."""
        assert server.config is not None
        assert hasattr(server.config, 'enable_midi')
        assert hasattr(server.config, 'log_level')
        assert hasattr(server.config, 'debug_mode')
        
        # Test configuration values
        assert isinstance(server.config.enable_midi, bool)
        assert server.config.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']

    def test_library_integration_available(self, library_integration):
        """Test that library integration is working."""
        available = library_integration.get_available_libraries()
        
        assert isinstance(available, dict), "Available libraries should be returned as dict"
        assert len(available) > 0, "At least some libraries should be available"
        
        # Test that we can check specific libraries without errors
        for lib_name, is_available in available.items():
            assert isinstance(is_available, bool), f"Library '{lib_name}' availability should be boolean"
            
        # Test that common libraries are checked (based on actual implementation)
        expected_libraries = ['music21', 'pretty_midi', 'muspy']
        for lib in expected_libraries:
            assert lib in available, f"Expected library '{lib}' to be checked for availability"

    def test_library_integration_methods(self, library_integration):
        """Test that library integration methods work properly."""
        # Test individual library checks (based on actual implementation)
        assert hasattr(library_integration, 'music21')
        assert hasattr(library_integration, 'pretty_midi')
        assert hasattr(library_integration, 'muspy')
        
        # Test that library objects have is_available method
        assert hasattr(library_integration.music21, 'is_available')
        assert hasattr(library_integration.pretty_midi, 'is_available')
        assert hasattr(library_integration.muspy, 'is_available')
        
        # Test that is_available returns boolean
        assert isinstance(library_integration.music21.is_available(), bool)
        assert isinstance(library_integration.pretty_midi.is_available(), bool)
        assert isinstance(library_integration.muspy.is_available(), bool)
        
        # Test core library integration methods
        assert hasattr(library_integration, 'get_available_libraries')
        assert callable(library_integration.get_available_libraries)

    def test_server_tool_execution_readiness(self, server):
        """Test that server is ready to execute tools."""
        # Verify key components are initialized
        assert server.midi_manager is not None
        assert server.file_manager is not None
        
        # Verify tool registry is properly populated and accessible
        tools = server.get_registered_tools()
        assert len(tools) > 0, "Server should have registered tools available for execution"
        
        # Verify each registered tool has required attributes
        for tool in tools:
            assert hasattr(tool, 'name'), "Tool should have a name attribute"
            assert hasattr(tool, 'description'), "Tool should have a description attribute"
            assert tool.name is not None, "Tool name should not be None"
            assert len(tool.name) > 0, "Tool name should not be empty"