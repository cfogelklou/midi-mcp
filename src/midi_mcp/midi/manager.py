# -*- coding: utf-8 -*-
"""
MIDI device manager implementation.

Provides concrete implementation of MIDI device discovery, connection management,
and cross-platform compatibility using multiple MIDI backends.
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
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from .interfaces import (
    MidiManagerInterface,
    MidiDeviceInterface,
    DeviceInfo,
    NoteOnMessage,
    NoteOffMessage,
    ControlChangeMessage
)
from .exceptions import (
    DeviceNotFoundError,
    DeviceConnectionError,
    BackendNotAvailableError,
    MessageSendError
)
from ..config.settings import MidiConfig
from ..utils.timing import measure_async_latency, LatencyTracker


class MockMidiDevice(MidiDeviceInterface):
    """Mock MIDI device for testing and development."""
    
    def __init__(self, device_info: DeviceInfo):
        self._device_info = device_info
        self._connected = False
        self.logger = logging.getLogger(__name__)
    
    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info
    
    @property
    def is_connected(self) -> bool:
        return self._connected
    
    async def connect(self) -> None:
        """Mock connection - always succeeds."""
        self._connected = True
        self._device_info.is_connected = True
        self.logger.info(f"Connected to mock device: {self._device_info.name}")
    
    async def disconnect(self) -> None:
        """Mock disconnection."""
        self._connected = False
        self._device_info.is_connected = False
        self.logger.info(f"Disconnected from mock device: {self._device_info.name}")
    
    async def send_message(self, message) -> None:
        """Mock message sending - logs the message."""
        if not self._connected:
            raise MessageSendError(
                self._device_info.device_id, 
                message.message_type.value, 
                "Device not connected"
            )
        
        self.logger.debug(f"Mock device {self._device_info.name} received: {message}")
    
    async def send_note_on(self, note: int, velocity: int = 127, channel: int = 0) -> None:
        """Send mock Note On message."""
        message = NoteOnMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_note_off(self, note: int, velocity: int = 64, channel: int = 0) -> None:
        """Send mock Note Off message."""
        message = NoteOffMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_control_change(self, controller: int, value: int, channel: int = 0) -> None:
        """Send mock Control Change message."""
        message = ControlChangeMessage(controller=controller, value=value, channel=channel)
        await self.send_message(message)


class MidiManager(MidiManagerInterface):
    """
    Concrete implementation of MIDI device management.
    
    Manages MIDI device discovery, connection, and message routing
    with support for multiple backends and error recovery.
    """
    
    def __init__(self, config: MidiConfig):
        """
        Initialize MIDI manager.
        
        Args:
            config: MIDI configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Device management
        self._devices: Dict[str, DeviceInfo] = {}
        self._connected_devices: Dict[str, MidiDeviceInterface] = {}
        
        # Performance tracking
        self.latency_tracker = LatencyTracker()
        
        # Thread pool for blocking operations
        self._executor = ThreadPoolExecutor(max_workers=4)
        
        self.logger.info("MIDI Manager initialized")
    
    async def discover_devices(self) -> List[DeviceInfo]:
        """
        Discover available MIDI devices.
        
        Returns:
            List of available MIDI device information
        """
        async with measure_async_latency("device_discovery"):
            try:
                # For Phase 1, return mock devices
                # TODO: Implement real device discovery in Phase 2
                mock_devices = [
                    DeviceInfo(
                        name="Mock MIDI Output",
                        device_id="mock_output_1",
                        is_input=False,
                        is_output=True,
                        port_number=0,
                        manufacturer="Mock Inc.",
                        product="Virtual MIDI Device"
                    ),
                    DeviceInfo(
                        name="Mock MIDI Input",
                        device_id="mock_input_1", 
                        is_input=True,
                        is_output=False,
                        port_number=1,
                        manufacturer="Mock Inc.",
                        product="Virtual MIDI Device"
                    )
                ]
                
                # Update internal device registry
                self._devices.clear()
                for device in mock_devices:
                    self._devices[device.device_id] = device
                
                self.logger.info(f"Discovered {len(mock_devices)} MIDI devices")
                return mock_devices
                
            except Exception as e:
                self.logger.error(f"Device discovery failed: {e}")
                raise DeviceConnectionError("discovery", str(e))
    
    async def get_device(self, device_id: str) -> Optional[MidiDeviceInterface]:
        """
        Get a MIDI device by ID.
        
        Args:
            device_id: Device identifier
            
        Returns:
            MIDI device interface or None if not found
        """
        if device_id in self._connected_devices:
            return self._connected_devices[device_id]
        
        if device_id in self._devices:
            # Create device instance but don't connect yet
            device_info = self._devices[device_id]
            return MockMidiDevice(device_info)
        
        return None
    
    async def connect_device(self, device_id: str) -> MidiDeviceInterface:
        """
        Connect to a MIDI device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            Connected MIDI device interface
            
        Raises:
            DeviceNotFoundError: If device is not found
            DeviceConnectionError: If connection fails
        """
        async with measure_async_latency(f"device_connection_{device_id}"):
            # Check if already connected
            if device_id in self._connected_devices:
                return self._connected_devices[device_id]
            
            # Check if device exists
            if device_id not in self._devices:
                # Try to discover devices first
                await self.discover_devices()
                
                if device_id not in self._devices:
                    raise DeviceNotFoundError(device_id)
            
            try:
                # Create and connect device
                device_info = self._devices[device_id]
                device = MockMidiDevice(device_info)
                
                await device.connect()
                
                # Store connected device
                self._connected_devices[device_id] = device
                
                self.logger.info(f"Connected to MIDI device: {device_info.name}")
                return device
                
            except Exception as e:
                self.logger.error(f"Failed to connect to device {device_id}: {e}")
                raise DeviceConnectionError(device_id, str(e))
    
    async def disconnect_device(self, device_id: str) -> None:
        """
        Disconnect from a MIDI device.
        
        Args:
            device_id: Device identifier
        """
        if device_id in self._connected_devices:
            device = self._connected_devices[device_id]
            
            try:
                await device.disconnect()
                del self._connected_devices[device_id]
                self.logger.info(f"Disconnected from MIDI device: {device_id}")
                
            except Exception as e:
                self.logger.error(f"Error disconnecting from device {device_id}: {e}")
                # Remove from connected devices even if disconnect failed
                del self._connected_devices[device_id]
    
    async def disconnect_all(self) -> None:
        """Disconnect from all MIDI devices."""
        disconnect_tasks = []
        
        for device_id in list(self._connected_devices.keys()):
            disconnect_tasks.append(self.disconnect_device(device_id))
        
        if disconnect_tasks:
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            self.logger.info("Disconnected from all MIDI devices")
    
    def get_connected_devices(self) -> List[MidiDeviceInterface]:
        """Get all currently connected devices."""
        return list(self._connected_devices.values())
    
    def get_device_info(self, device_id: str) -> Optional[DeviceInfo]:
        """Get device information by ID."""
        return self._devices.get(device_id)
    
    def get_latency_stats(self) -> Dict[str, float]:
        """Get latency statistics for MIDI operations."""
        return self.latency_tracker.get_stats()
    
    async def cleanup(self) -> None:
        """Clean up manager resources."""
        await self.disconnect_all()
        self._executor.shutdown(wait=True)
        self.logger.info("MIDI Manager cleanup completed")