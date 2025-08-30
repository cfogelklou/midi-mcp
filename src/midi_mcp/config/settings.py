# -*- coding: utf-8 -*-
"""
Configuration settings for MIDI MCP Server.

Defines configuration classes for server settings, MIDI configuration,
and environment-specific parameters with validation and defaults.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import os
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MidiConfig:
    """Configuration for MIDI operations and device management."""
    
    # Device settings
    default_device: Optional[str] = None
    device_timeout: float = 5.0  # seconds
    auto_reconnect: bool = True
    
    # Timing settings
    max_latency_ms: float = 10.0  # Maximum acceptable latency
    buffer_size: int = 1024
    sample_rate: int = 44100
    
    # Performance settings
    enable_threading: bool = True
    max_concurrent_notes: int = 128
    
    # Platform-specific settings
    use_virtual_devices: bool = False
    preferred_backend: Optional[str] = None  # 'rtmidi', 'pygame', etc.
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.max_latency_ms <= 0:
            raise ValueError("max_latency_ms must be positive")
        
        if self.device_timeout <= 0:
            raise ValueError("device_timeout must be positive")
        
        if self.buffer_size <= 0:
            raise ValueError("buffer_size must be positive")
        
        if self.max_concurrent_notes <= 0:
            raise ValueError("max_concurrent_notes must be positive")


@dataclass
class ServerConfig:
    """Configuration for the MCP server."""
    
    # Server settings
    host: str = "localhost"
    port: int = 8080
    debug_mode: bool = False
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance settings
    max_connections: int = 100
    connection_timeout: float = 30.0
    
    # Feature flags
    enable_midi: bool = True
    enable_file_operations: bool = False  # For future phases
    enable_composition: bool = False  # For future phases
    
    # MIDI configuration
    midi_config: MidiConfig = field(default_factory=MidiConfig)
    
    # Environment-specific settings
    environment: str = field(default_factory=lambda: os.getenv('ENVIRONMENT', 'development'))
    
    @classmethod
    def from_env(cls) -> 'ServerConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Server settings from environment
        config.host = os.getenv('MCP_HOST', config.host)
        config.port = int(os.getenv('MCP_PORT', str(config.port)))
        config.debug_mode = os.getenv('MCP_DEBUG', '').lower() in ('true', '1', 'yes')
        
        # Logging settings
        config.log_level = os.getenv('MCP_LOG_LEVEL', config.log_level).upper()
        config.log_file = os.getenv('MCP_LOG_FILE', config.log_file)
        
        # Performance settings
        config.max_connections = int(os.getenv('MCP_MAX_CONNECTIONS', str(config.max_connections)))
        config.connection_timeout = float(os.getenv('MCP_CONNECTION_TIMEOUT', str(config.connection_timeout)))
        
        # Feature flags
        config.enable_midi = os.getenv('MCP_ENABLE_MIDI', 'true').lower() in ('true', '1', 'yes')
        
        # MIDI configuration from environment
        midi_config = MidiConfig()
        midi_config.default_device = os.getenv('MIDI_DEFAULT_DEVICE')
        midi_config.device_timeout = float(os.getenv('MIDI_DEVICE_TIMEOUT', str(midi_config.device_timeout)))
        midi_config.max_latency_ms = float(os.getenv('MIDI_MAX_LATENCY_MS', str(midi_config.max_latency_ms)))
        midi_config.auto_reconnect = os.getenv('MIDI_AUTO_RECONNECT', 'true').lower() in ('true', '1', 'yes')
        midi_config.preferred_backend = os.getenv('MIDI_PREFERRED_BACKEND')
        
        config.midi_config = midi_config
        
        return config
    
    @classmethod
    def from_file(cls, file_path: str) -> 'ServerConfig':
        """Create configuration from a configuration file."""
        # For now, return default config
        # TODO: Implement config file parsing (YAML/JSON) in future phases
        return cls.from_env()
    
    def validate(self) -> None:
        """Validate all configuration parameters."""
        # Validate server settings
        if self.port <= 0 or self.port > 65535:
            raise ValueError("port must be between 1 and 65535")
        
        if self.max_connections <= 0:
            raise ValueError("max_connections must be positive")
        
        if self.connection_timeout <= 0:
            raise ValueError("connection_timeout must be positive")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"log_level must be one of {valid_log_levels}")
        
        # Validate MIDI configuration
        self.midi_config.validate()
        
        # Environment-specific validation
        if self.environment not in ['development', 'testing', 'production']:
            raise ValueError("environment must be 'development', 'testing', or 'production'")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'server': {
                'host': self.host,
                'port': self.port,
                'debug_mode': self.debug_mode,
                'max_connections': self.max_connections,
                'connection_timeout': self.connection_timeout,
                'environment': self.environment,
            },
            'logging': {
                'log_level': self.log_level,
                'log_file': self.log_file,
                'log_format': self.log_format,
            },
            'features': {
                'enable_midi': self.enable_midi,
                'enable_file_operations': self.enable_file_operations,
                'enable_composition': self.enable_composition,
            },
            'midi': {
                'default_device': self.midi_config.default_device,
                'device_timeout': self.midi_config.device_timeout,
                'auto_reconnect': self.midi_config.auto_reconnect,
                'max_latency_ms': self.midi_config.max_latency_ms,
                'buffer_size': self.midi_config.buffer_size,
                'sample_rate': self.midi_config.sample_rate,
                'enable_threading': self.midi_config.enable_threading,
                'max_concurrent_notes': self.midi_config.max_concurrent_notes,
                'use_virtual_devices': self.midi_config.use_virtual_devices,
                'preferred_backend': self.midi_config.preferred_backend,
            }
        }


def get_default_config() -> ServerConfig:
    """Get the default server configuration."""
    return ServerConfig.from_env()


def validate_config(config: ServerConfig) -> None:
    """Validate a server configuration and raise exceptions for invalid settings."""
    config.validate()