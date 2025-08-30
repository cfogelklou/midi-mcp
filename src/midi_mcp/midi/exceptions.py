# -*- coding: utf-8 -*-
"""
MIDI-specific exceptions for error handling.

Defines custom exception classes for MIDI operations, device management,
and musical operations with clear error categories and messages.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#


class MidiError(Exception):
    """Base exception for all MIDI-related errors."""
    
    def __init__(self, message: str, error_code: str = None) -> None:
        """
        Initialize MIDI error.
        
        Args:
            message: Human-readable error message
            error_code: Optional machine-readable error code
        """
        super().__init__(message)
        self.error_code = error_code


class DeviceNotFoundError(MidiError):
    """Raised when a MIDI device cannot be found."""
    
    def __init__(self, device_id: str) -> None:
        message = f"MIDI device not found: {device_id}"
        super().__init__(message, "DEVICE_NOT_FOUND")
        self.device_id = device_id


class DeviceConnectionError(MidiError):
    """Raised when a MIDI device connection fails."""
    
    def __init__(self, device_id: str, reason: str = None) -> None:
        message = f"Failed to connect to MIDI device: {device_id}"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "DEVICE_CONNECTION_ERROR")
        self.device_id = device_id
        self.reason = reason


class DeviceDisconnectionError(MidiError):
    """Raised when a MIDI device disconnection fails."""
    
    def __init__(self, device_id: str, reason: str = None) -> None:
        message = f"Failed to disconnect from MIDI device: {device_id}"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "DEVICE_DISCONNECTION_ERROR")
        self.device_id = device_id
        self.reason = reason


class MessageSendError(MidiError):
    """Raised when sending a MIDI message fails."""
    
    def __init__(self, device_id: str, message_type: str = None, reason: str = None) -> None:
        message = f"Failed to send MIDI message to device: {device_id}"
        if message_type:
            message += f" (message type: {message_type})"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "MESSAGE_SEND_ERROR")
        self.device_id = device_id
        self.message_type = message_type
        self.reason = reason


class InvalidMessageError(MidiError):
    """Raised when a MIDI message is invalid."""
    
    def __init__(self, message_info: str, reason: str = None) -> None:
        message = f"Invalid MIDI message: {message_info}"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "INVALID_MESSAGE")
        self.message_info = message_info
        self.reason = reason


class TimingError(MidiError):
    """Raised when MIDI timing requirements are not met."""
    
    def __init__(self, operation: str, actual_latency_ms: float, max_latency_ms: float) -> None:
        message = (f"MIDI timing requirement not met for {operation}: "
                  f"{actual_latency_ms:.2f}ms > {max_latency_ms:.2f}ms")
        super().__init__(message, "TIMING_ERROR")
        self.operation = operation
        self.actual_latency_ms = actual_latency_ms
        self.max_latency_ms = max_latency_ms


class SequencePlaybackError(MidiError):
    """Raised when MIDI sequence playback fails."""
    
    def __init__(self, reason: str = None) -> None:
        message = "MIDI sequence playback failed"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "SEQUENCE_PLAYBACK_ERROR")
        self.reason = reason


class BackendNotAvailableError(MidiError):
    """Raised when the requested MIDI backend is not available."""
    
    def __init__(self, backend_name: str, available_backends: list = None) -> None:
        message = f"MIDI backend not available: {backend_name}"
        if available_backends:
            message += f" (available: {', '.join(available_backends)})"
        super().__init__(message, "BACKEND_NOT_AVAILABLE")
        self.backend_name = backend_name
        self.available_backends = available_backends or []


class ConfigurationError(MidiError):
    """Raised when MIDI configuration is invalid."""
    
    def __init__(self, config_parameter: str, reason: str = None) -> None:
        message = f"Invalid MIDI configuration: {config_parameter}"
        if reason:
            message += f" - {reason}"
        super().__init__(message, "CONFIGURATION_ERROR")
        self.config_parameter = config_parameter
        self.reason = reason