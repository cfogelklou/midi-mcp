# -*- coding: utf-8 -*-
"""
Abstract interfaces for MIDI operations.

Defines abstract base classes for MIDI devices, managers, and message types
to enable cross-platform compatibility and testability.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import time


class MidiMessageType(Enum):
    """MIDI message types."""
    NOTE_ON = "note_on"
    NOTE_OFF = "note_off"
    CONTROL_CHANGE = "control_change"
    PROGRAM_CHANGE = "program_change"
    PITCH_BEND = "pitch_bend"
    SYSTEM_EXCLUSIVE = "system_exclusive"


@dataclass
class MidiMessage:
    """Base class for MIDI messages."""
    
    message_type: MidiMessageType
    channel: int
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.perf_counter()
        
        # Validate channel (0-15 for MIDI channels)
        if not 0 <= self.channel <= 15:
            raise ValueError("MIDI channel must be between 0 and 15")
    
    def to_bytes(self) -> bytes:
        """Convert message to raw MIDI bytes."""
        raise NotImplementedError("Subclasses must implement to_bytes()")


@dataclass
class NoteOnMessage:
    """MIDI Note On message."""
    
    note: int
    velocity: int
    channel: int = 0
    timestamp: Optional[float] = field(default=None)
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.perf_counter()
            
        # Validate channel (0-15 for MIDI channels)
        if not 0 <= self.channel <= 15:
            raise ValueError("MIDI channel must be between 0 and 15")
        
        # Validate note (0-127)
        if not 0 <= self.note <= 127:
            raise ValueError("MIDI note must be between 0 and 127")
        
        # Validate velocity (0-127)
        if not 0 <= self.velocity <= 127:
            raise ValueError("MIDI velocity must be between 0 and 127")
    
    @property
    def message_type(self) -> MidiMessageType:
        return MidiMessageType.NOTE_ON
    
    def to_bytes(self) -> bytes:
        """Convert to MIDI bytes (status byte + note + velocity)."""
        status_byte = 0x90 | self.channel  # Note On + channel
        return bytes([status_byte, self.note, self.velocity])


@dataclass
class NoteOffMessage:
    """MIDI Note Off message."""
    
    note: int
    velocity: int = 64  # Default release velocity
    channel: int = 0
    timestamp: Optional[float] = field(default=None)
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.perf_counter()
            
        # Validate channel (0-15 for MIDI channels)
        if not 0 <= self.channel <= 15:
            raise ValueError("MIDI channel must be between 0 and 15")
        
        # Validate note (0-127)
        if not 0 <= self.note <= 127:
            raise ValueError("MIDI note must be between 0 and 127")
        
        # Validate velocity (0-127)
        if not 0 <= self.velocity <= 127:
            raise ValueError("MIDI velocity must be between 0 and 127")
    
    @property
    def message_type(self) -> MidiMessageType:
        return MidiMessageType.NOTE_OFF
    
    def to_bytes(self) -> bytes:
        """Convert to MIDI bytes (status byte + note + velocity)."""
        status_byte = 0x80 | self.channel  # Note Off + channel
        return bytes([status_byte, self.note, self.velocity])


@dataclass
class ControlChangeMessage:
    """MIDI Control Change message."""
    
    controller: int
    value: int
    channel: int = 0
    timestamp: Optional[float] = field(default=None)
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.perf_counter()
            
        # Validate channel (0-15 for MIDI channels)
        if not 0 <= self.channel <= 15:
            raise ValueError("MIDI channel must be between 0 and 15")
        
        # Validate controller (0-127)
        if not 0 <= self.controller <= 127:
            raise ValueError("MIDI controller must be between 0 and 127")
        
        # Validate value (0-127)
        if not 0 <= self.value <= 127:
            raise ValueError("MIDI controller value must be between 0 and 127")
    
    @property
    def message_type(self) -> MidiMessageType:
        return MidiMessageType.CONTROL_CHANGE
    
    def to_bytes(self) -> bytes:
        """Convert to MIDI bytes (status byte + controller + value)."""
        status_byte = 0xB0 | self.channel  # Control Change + channel
        return bytes([status_byte, self.controller, self.value])


@dataclass
class DeviceInfo:
    """Information about a MIDI device."""
    
    name: str
    device_id: str
    is_input: bool
    is_output: bool
    is_connected: bool = False
    port_number: Optional[int] = None
    manufacturer: Optional[str] = None
    product: Optional[str] = None
    
    def __str__(self) -> str:
        direction = []
        if self.is_input:
            direction.append("INPUT")
        if self.is_output:
            direction.append("OUTPUT")
        direction_str = "/".join(direction) if direction else "UNKNOWN"
        
        status = "CONNECTED" if self.is_connected else "DISCONNECTED"
        return f"{self.name} [{direction_str}] ({status})"


class MidiDeviceInterface(ABC):
    """Abstract interface for MIDI device operations."""
    
    @property
    @abstractmethod
    def device_info(self) -> DeviceInfo:
        """Get device information."""
        pass
    
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if device is connected."""
        pass
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to the MIDI device."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the MIDI device."""
        pass
    
    @abstractmethod
    async def send_message(self, message: Union[NoteOnMessage, NoteOffMessage, ControlChangeMessage]) -> None:
        """Send a MIDI message to the device."""
        pass
    
    @abstractmethod
    async def send_note_on(self, note: int, velocity: int = 127, channel: int = 0) -> None:
        """Send a Note On message."""
        pass
    
    @abstractmethod
    async def send_note_off(self, note: int, velocity: int = 64, channel: int = 0) -> None:
        """Send a Note Off message."""
        pass
    
    @abstractmethod
    async def send_control_change(self, controller: int, value: int, channel: int = 0) -> None:
        """Send a Control Change message."""
        pass


class MidiManagerInterface(ABC):
    """Abstract interface for MIDI device management."""
    
    @abstractmethod
    async def discover_devices(self) -> List[DeviceInfo]:
        """Discover available MIDI devices."""
        pass
    
    @abstractmethod
    async def get_device(self, device_id: str) -> Optional[MidiDeviceInterface]:
        """Get a MIDI device by ID."""
        pass
    
    @abstractmethod
    async def connect_device(self, device_id: str) -> MidiDeviceInterface:
        """Connect to a MIDI device."""
        pass
    
    @abstractmethod
    async def disconnect_device(self, device_id: str) -> None:
        """Disconnect from a MIDI device."""
        pass
    
    @abstractmethod
    async def disconnect_all(self) -> None:
        """Disconnect from all MIDI devices."""
        pass
    
    @abstractmethod
    def get_connected_devices(self) -> List[MidiDeviceInterface]:
        """Get all currently connected devices."""
        pass


class SequencePlayerInterface(ABC):
    """Abstract interface for playing MIDI sequences."""
    
    @abstractmethod
    async def play_note(self, note: int, duration: float, velocity: int = 127, channel: int = 0) -> None:
        """Play a single note for a specified duration."""
        pass
    
    @abstractmethod
    async def play_chord(self, notes: List[int], duration: float, velocity: int = 127, channel: int = 0) -> None:
        """Play multiple notes simultaneously."""
        pass
    
    @abstractmethod
    async def play_sequence(self, sequence: List[Dict[str, Any]], tempo: float = 120.0) -> None:
        """Play a sequence of notes with timing."""
        pass
    
    @abstractmethod
    async def stop_all_notes(self, channel: int = 0) -> None:
        """Stop all currently playing notes."""
        pass


# Helper functions for common operations
def note_name_to_number(note_name: str) -> int:
    """
    Convert note name to MIDI note number.
    
    Args:
        note_name: Note name like 'C4', 'A#3', 'Bb5'
        
    Returns:
        MIDI note number (0-127)
    """
    # Basic implementation - can be enhanced later
    note_map = {
        'C': 0, 'C#': 1, 'DB': 1,
        'D': 2, 'D#': 3, 'EB': 3,
        'E': 4,
        'F': 5, 'F#': 6, 'GB': 6,
        'G': 7, 'G#': 8, 'AB': 8,
        'A': 9, 'A#': 10, 'BB': 10,
        'B': 11
    }
    
    # Parse note name
    note_name = note_name.upper()
    if len(note_name) < 2:
        raise ValueError("Invalid note name format")
    
    # Extract note and octave
    if note_name[1] in ['#', 'B']:
        note = note_name[:2]
        octave = int(note_name[2:])
    else:
        note = note_name[0]
        octave = int(note_name[1:])
    
    if note not in note_map:
        raise ValueError(f"Unknown note: {note}")
    
    # Calculate MIDI note number
    midi_number = (octave + 1) * 12 + note_map[note]
    
    if not 0 <= midi_number <= 127:
        raise ValueError(f"MIDI note number {midi_number} out of range (0-127)")
    
    return midi_number


def note_number_to_name(note_number: int) -> str:
    """
    Convert MIDI note number to note name.
    
    Args:
        note_number: MIDI note number (0-127)
        
    Returns:
        Note name like 'C4', 'A#3'
    """
    if not 0 <= note_number <= 127:
        raise ValueError(f"MIDI note number {note_number} out of range (0-127)")
    
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_number // 12) - 1
    note = note_names[note_number % 12]
    
    return f"{note}{octave}"