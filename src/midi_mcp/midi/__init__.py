# -*- coding: utf-8 -*-
"""
MIDI operations and device management.

Provides MIDI device discovery, connection management, message sending,
and musical operations with cross-platform compatibility.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from .interfaces import (
    MidiDeviceInterface,
    MidiManagerInterface,
    MidiMessage,
    NoteOnMessage,
    NoteOffMessage,
    ControlChangeMessage
)
from .manager import MidiManager
from .exceptions import (
    MidiError,
    DeviceNotFoundError,
    DeviceConnectionError,
    MessageSendError
)

__all__ = [
    'MidiDeviceInterface',
    'MidiManagerInterface', 
    'MidiMessage',
    'NoteOnMessage',
    'NoteOffMessage',
    'ControlChangeMessage',
    'MidiManager',
    'MidiError',
    'DeviceNotFoundError',
    'DeviceConnectionError',
    'MessageSendError'
]