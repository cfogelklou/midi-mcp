# -*- coding: utf-8 -*-
"""
MIDI operations package.

Provides interfaces and implementations for MIDI device management,
note operations, file I/O, playback, and cross-platform compatibility.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

from .interfaces import (
    MidiManagerInterface,
    MidiDeviceInterface,
    DeviceInfo,
    MidiMessage,
    NoteOnMessage,
    NoteOffMessage,
    ControlChangeMessage,
    note_name_to_number,
    note_number_to_name
)

from .manager import MidiManager
from .file_ops import MidiFileManager, MidiFileSession
from .player import MidiFilePlayer, PlaybackState, PlaybackProgressTracker
from .analyzer import MidiAnalyzer
from .exceptions import (
    MidiError,
    DeviceNotFoundError,
    DeviceConnectionError,
    BackendNotAvailableError,
    MessageSendError
)

__all__ = [
    'MidiManagerInterface',
    'MidiDeviceInterface',
    'DeviceInfo',
    'MidiMessage',
    'NoteOnMessage',
    'NoteOffMessage',
    'ControlChangeMessage',
    'MidiManager',
    'MidiFileManager',
    'MidiFileSession',
    'MidiFilePlayer',
    'PlaybackState',
    'PlaybackProgressTracker',
    'MidiAnalyzer',
    'MidiError',
    'DeviceNotFoundError',
    'DeviceConnectionError',
    'BackendNotAvailableError',
    'MessageSendError',
    'note_name_to_number',
    'note_number_to_name'
]