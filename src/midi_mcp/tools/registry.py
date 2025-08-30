# -*- coding: utf-8 -*-
"""
Tool registry for MCP server tools.

Provides centralized registration and management of MCP tools
with validation and conflict detection.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import logging
from typing import Dict, Callable, Optional, List, Any
from mcp.types import Tool


class ToolRegistry:
    """Registry for managing MCP server tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Tool] = {}
        self.handlers: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, name: str, tool: Tool, handler: Callable) -> None:
        """
        Register a tool with its handler.
        
        Args:
            name: Tool name (must match tool.name)
            tool: MCP tool definition
            handler: Async function to handle tool calls
            
        Raises:
            ValueError: If tool name mismatch or already registered
        """
        # Validate tool name matches
        if tool.name != name:
            raise ValueError(f"Tool name mismatch: {name} != {tool.name}")
        
        # Check for existing registration
        if name in self.tools:
            self.logger.warning(f"Overwriting existing tool: {name}")
        
        # Register tool and handler
        self.tools[name] = tool
        self.handlers[name] = handler
        
        self.logger.debug(f"Registered tool: {name}")
    
    def unregister(self, name: str) -> None:
        """
        Unregister a tool.
        
        Args:
            name: Tool name to unregister
        """
        if name in self.tools:
            del self.tools[name]
            del self.handlers[name]
            self.logger.debug(f"Unregistered tool: {name}")
        else:
            self.logger.warning(f"Attempted to unregister unknown tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool definition by name."""
        return self.tools.get(name)
    
    def get_handler(self, name: str) -> Optional[Callable]:
        """Get tool handler by name."""
        return self.handlers.get(name)
    
    def get_tool_names(self) -> List[str]:
        """Get list of all registered tool names."""
        return list(self.tools.keys())
    
    def validate_tool(self, tool: Tool) -> List[str]:
        """
        Validate a tool definition.
        
        Args:
            tool: Tool to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        if not tool.name:
            errors.append("Tool name is required")
        
        if not tool.description:
            errors.append("Tool description is required")
        
        # Check name format
        if tool.name and not tool.name.replace('_', '').replace('-', '').isalnum():
            errors.append("Tool name must contain only alphanumeric characters, hyphens, and underscores")
        
        # Check schema if present
        if hasattr(tool, 'inputSchema') and tool.inputSchema:
            if not isinstance(tool.inputSchema, dict):
                errors.append("inputSchema must be a dictionary")
            elif 'type' not in tool.inputSchema:
                errors.append("inputSchema must have a 'type' field")
        
        return errors
    
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Get summary information about all registered tools.
        
        Returns:
            Dictionary with tool information
        """
        return {
            name: {
                'name': tool.name,
                'description': tool.description,
                'has_handler': name in self.handlers,
                'schema': getattr(tool, 'inputSchema', None)
            }
            for name, tool in self.tools.items()
        }
    
    def clear(self) -> None:
        """Clear all registered tools."""
        count = len(self.tools)
        self.tools.clear()
        self.handlers.clear()
        self.logger.info(f"Cleared {count} registered tools")