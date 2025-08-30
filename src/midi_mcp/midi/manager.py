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
import platform
from typing import List, Optional, Dict, Any, Union
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

# Optional MIDI backend imports
try:
    import mido
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    mido = None

try:
    import rtmidi
    RTMIDI_AVAILABLE = True
except ImportError:
    RTMIDI_AVAILABLE = False
    rtmidi = None


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


class MidoMidiDevice(MidiDeviceInterface):
    """Mido-based MIDI device implementation for cross-platform support."""
    
    def __init__(self, device_info: DeviceInfo):
        self._device_info = device_info
        self._connected = False
        self._port = None
        self.logger = logging.getLogger(__name__)
    
    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info
    
    @property
    def is_connected(self) -> bool:
        return self._connected and self._port is not None
    
    async def connect(self) -> None:
        """Connect to MIDI device using mido."""
        if not MIDO_AVAILABLE:
            raise BackendNotAvailableError("mido", "Mido library not available")
        
        try:
            if self._device_info.is_output:
                self._port = mido.open_output(self._device_info.name)
            else:
                self._port = mido.open_input(self._device_info.name)
            
            self._connected = True
            self._device_info.is_connected = True
            self.logger.info(f"Connected to MIDI device via mido: {self._device_info.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to device {self._device_info.name} via mido: {e}")
            raise DeviceConnectionError(self._device_info.device_id, str(e))
    
    async def disconnect(self) -> None:
        """Disconnect from MIDI device."""
        try:
            if self._port:
                self._port.close()
                self._port = None
            
            self._connected = False
            self._device_info.is_connected = False
            self.logger.info(f"Disconnected from MIDI device: {self._device_info.name}")
            
        except Exception as e:
            self.logger.error(f"Error disconnecting from device {self._device_info.name}: {e}")
            self._connected = False
            self._port = None
    
    async def send_message(self, message: Union[NoteOnMessage, NoteOffMessage, ControlChangeMessage]) -> None:
        """Send MIDI message using mido."""
        if not self._connected or not self._port:
            raise MessageSendError(
                self._device_info.device_id,
                message.message_type.value,
                "Device not connected"
            )
        
        try:
            # Convert our message to mido message
            if isinstance(message, NoteOnMessage):
                mido_msg = mido.Message('note_on', 
                                      channel=message.channel,
                                      note=message.note, 
                                      velocity=message.velocity)
            elif isinstance(message, NoteOffMessage):
                mido_msg = mido.Message('note_off',
                                      channel=message.channel,
                                      note=message.note,
                                      velocity=message.velocity)
            elif isinstance(message, ControlChangeMessage):
                mido_msg = mido.Message('control_change',
                                      channel=message.channel,
                                      control=message.controller,
                                      value=message.value)
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
            
            # Send message asynchronously
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._port.send, mido_msg)
            
            self.logger.debug(f"Sent MIDI message via mido: {mido_msg}")
            
        except Exception as e:
            self.logger.error(f"Failed to send MIDI message: {e}")
            raise MessageSendError(self._device_info.device_id, 
                                 message.message_type.value, 
                                 str(e))
    
    async def send_note_on(self, note: int, velocity: int = 127, channel: int = 0) -> None:
        """Send Note On message."""
        message = NoteOnMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_note_off(self, note: int, velocity: int = 64, channel: int = 0) -> None:
        """Send Note Off message."""
        message = NoteOffMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_control_change(self, controller: int, value: int, channel: int = 0) -> None:
        """Send Control Change message."""
        message = ControlChangeMessage(controller=controller, value=value, channel=channel)
        await self.send_message(message)


class RtMidiDevice(MidiDeviceInterface):
    """Python-rtmidi based MIDI device implementation for low-latency support."""
    
    def __init__(self, device_info: DeviceInfo):
        self._device_info = device_info
        self._connected = False
        self._midi_out = None
        self._midi_in = None
        self.logger = logging.getLogger(__name__)
    
    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info
    
    @property
    def is_connected(self) -> bool:
        return self._connected and (self._midi_out is not None or self._midi_in is not None)
    
    async def connect(self) -> None:
        """Connect to MIDI device using python-rtmidi."""
        if not RTMIDI_AVAILABLE:
            raise BackendNotAvailableError("rtmidi", "python-rtmidi library not available")
        
        try:
            if self._device_info.is_output:
                self._midi_out = rtmidi.MidiOut()
                port_number = self._device_info.port_number
                if port_number is not None:
                    self._midi_out.open_port(port_number)
                else:
                    # Find port by name
                    for i, port_name in enumerate(self._midi_out.get_ports()):
                        if port_name == self._device_info.name:
                            self._midi_out.open_port(i)
                            break
                    else:
                        raise DeviceNotFoundError(self._device_info.device_id)
            
            if self._device_info.is_input:
                self._midi_in = rtmidi.MidiIn()
                port_number = self._device_info.port_number
                if port_number is not None:
                    self._midi_in.open_port(port_number)
                else:
                    # Find port by name
                    for i, port_name in enumerate(self._midi_in.get_ports()):
                        if port_name == self._device_info.name:
                            self._midi_in.open_port(i)
                            break
                    else:
                        raise DeviceNotFoundError(self._device_info.device_id)
            
            self._connected = True
            self._device_info.is_connected = True
            self.logger.info(f"Connected to MIDI device via rtmidi: {self._device_info.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to device {self._device_info.name} via rtmidi: {e}")
            raise DeviceConnectionError(self._device_info.device_id, str(e))
    
    async def disconnect(self) -> None:
        """Disconnect from MIDI device."""
        try:
            if self._midi_out:
                self._midi_out.close_port()
                self._midi_out = None
            
            if self._midi_in:
                self._midi_in.close_port()
                self._midi_in = None
            
            self._connected = False
            self._device_info.is_connected = False
            self.logger.info(f"Disconnected from MIDI device: {self._device_info.name}")
            
        except Exception as e:
            self.logger.error(f"Error disconnecting from device {self._device_info.name}: {e}")
            self._connected = False
            self._midi_out = None
            self._midi_in = None
    
    async def send_message(self, message: Union[NoteOnMessage, NoteOffMessage, ControlChangeMessage]) -> None:
        """Send MIDI message using python-rtmidi."""
        if not self._connected or not self._midi_out:
            raise MessageSendError(
                self._device_info.device_id,
                message.message_type.value,
                "Device not connected or not an output device"
            )
        
        try:
            # Convert message to raw MIDI bytes
            midi_bytes = message.to_bytes()
            
            # Send message asynchronously
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._midi_out.send_message, list(midi_bytes))
            
            self.logger.debug(f"Sent MIDI message via rtmidi: {list(midi_bytes)}")
            
        except Exception as e:
            self.logger.error(f"Failed to send MIDI message: {e}")
            raise MessageSendError(self._device_info.device_id,
                                 message.message_type.value,
                                 str(e))
    
    async def send_note_on(self, note: int, velocity: int = 127, channel: int = 0) -> None:
        """Send Note On message."""
        message = NoteOnMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_note_off(self, note: int, velocity: int = 64, channel: int = 0) -> None:
        """Send Note Off message."""
        message = NoteOffMessage(note=note, velocity=velocity, channel=channel)
        await self.send_message(message)
    
    async def send_control_change(self, controller: int, value: int, channel: int = 0) -> None:
        """Send Control Change message."""
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
        Discover available MIDI devices across all available backends.
        
        Returns:
            List of available MIDI device information
        """
        async with measure_async_latency("device_discovery"):
            try:
                devices = []
                
                # Try mido backend first (more stable)
                if MIDO_AVAILABLE:
                    devices.extend(await self._discover_mido_devices())
                
                # Try rtmidi backend for additional devices
                if RTMIDI_AVAILABLE:
                    rtmidi_devices = await self._discover_rtmidi_devices()
                    # Filter out duplicates by name
                    existing_names = {d.name for d in devices}
                    for device in rtmidi_devices:
                        if device.name not in existing_names:
                            devices.append(device)
                
                # If no real devices found, add mock devices for development
                if not devices:
                    self.logger.warning("No real MIDI devices found, using mock devices")
                    devices = await self._create_mock_devices()
                
                # Update internal device registry
                self._devices.clear()
                for device in devices:
                    self._devices[device.device_id] = device
                
                self.logger.info(f"Discovered {len(devices)} MIDI devices")
                return devices
                
            except Exception as e:
                self.logger.error(f"Device discovery failed: {e}")
                # Fall back to mock devices
                mock_devices = await self._create_mock_devices()
                self._devices.clear()
                for device in mock_devices:
                    self._devices[device.device_id] = device
                return mock_devices
    
    async def _discover_mido_devices(self) -> List[DeviceInfo]:
        """Discover MIDI devices using mido backend."""
        devices = []
        
        try:
            # Get output devices
            output_names = mido.get_output_names()
            for i, name in enumerate(output_names):
                device_id = f"mido_output_{i}_{name.replace(' ', '_').replace('/', '_')}"
                devices.append(DeviceInfo(
                    name=name,
                    device_id=device_id,
                    is_input=False,
                    is_output=True,
                    port_number=i,
                    manufacturer="Unknown",
                    product=name
                ))
            
            # Get input devices
            input_names = mido.get_input_names()
            for i, name in enumerate(input_names):
                device_id = f"mido_input_{i}_{name.replace(' ', '_').replace('/', '_')}"
                devices.append(DeviceInfo(
                    name=name,
                    device_id=device_id,
                    is_input=True,
                    is_output=False,
                    port_number=i,
                    manufacturer="Unknown",
                    product=name
                ))
            
            self.logger.debug(f"Mido discovered {len(devices)} devices")
            
        except Exception as e:
            self.logger.error(f"Mido device discovery failed: {e}")
        
        return devices
    
    async def _discover_rtmidi_devices(self) -> List[DeviceInfo]:
        """Discover MIDI devices using python-rtmidi backend."""
        devices = []
        
        try:
            # Get output devices
            midi_out = rtmidi.MidiOut()
            output_ports = midi_out.get_ports()
            for i, name in enumerate(output_ports):
                device_id = f"rtmidi_output_{i}_{name.replace(' ', '_').replace('/', '_')}"
                devices.append(DeviceInfo(
                    name=name,
                    device_id=device_id,
                    is_input=False,
                    is_output=True,
                    port_number=i,
                    manufacturer="Unknown",
                    product=name
                ))
            
            # Get input devices  
            midi_in = rtmidi.MidiIn()
            input_ports = midi_in.get_ports()
            for i, name in enumerate(input_ports):
                device_id = f"rtmidi_input_{i}_{name.replace(' ', '_').replace('/', '_')}"
                devices.append(DeviceInfo(
                    name=name,
                    device_id=device_id,
                    is_input=True,
                    is_output=False,
                    port_number=i,
                    manufacturer="Unknown",
                    product=name
                ))
            
            self.logger.debug(f"RtMidi discovered {len(devices)} devices")
            
        except Exception as e:
            self.logger.error(f"RtMidi device discovery failed: {e}")
        
        return devices
    
    async def _create_mock_devices(self) -> List[DeviceInfo]:
        """Create mock devices for development/testing."""
        return [
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
            return self._create_device_instance(device_info)
        
        return None
    
    def _create_device_instance(self, device_info: DeviceInfo) -> MidiDeviceInterface:
        """Create appropriate device instance based on device ID."""
        if device_info.device_id.startswith("mido_"):
            return MidoMidiDevice(device_info)
        elif device_info.device_id.startswith("rtmidi_"):
            return RtMidiDevice(device_info)
        else:
            # Default to mock device
            return MockMidiDevice(device_info)
    
    async def connect_device(self, device_id: str) -> MidiDeviceInterface:
        """
        Connect to a MIDI device using the appropriate backend.
        
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
                # Create and connect device using appropriate backend
                device_info = self._devices[device_id]
                device = self._create_device_instance(device_info)
                
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
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get status of available MIDI backends."""
        return {
            "mido_available": MIDO_AVAILABLE,
            "rtmidi_available": RTMIDI_AVAILABLE,
            "platform": platform.system(),
            "preferred_backend": "mido" if MIDO_AVAILABLE else "rtmidi" if RTMIDI_AVAILABLE else "mock"
        }
    
    async def cleanup(self) -> None:
        """Clean up manager resources."""
        await self.disconnect_all()
        self._executor.shutdown(wait=True)
        self.logger.info("MIDI Manager cleanup completed")