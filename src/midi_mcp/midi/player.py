# -*- coding: utf-8 -*-
"""
MIDI file player for real-time playback.

Handles playback of MIDI files through connected MIDI devices
with accurate timing and synchronization.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import logging
import time
from typing import Optional, Dict, Any, Callable
from enum import Enum

try:
    import mido

    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    mido = None

from .exceptions import MidiError
from .interfaces import MidiDeviceInterface


class PlaybackState(Enum):
    """Playback state enumeration."""

    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    FINISHED = "finished"


class MidiFilePlayer:
    """
    Real-time MIDI file player with timing synchronization.
    """

    def __init__(self):
        """Initialize the MIDI file player."""
        self.logger = logging.getLogger(__name__)
        self._playback_tasks: Dict[str, asyncio.Task] = {}
        self._playback_states: Dict[str, PlaybackState] = {}

        if not MIDO_AVAILABLE:
            self.logger.warning("mido library not available - MIDI playback will be limited")

    async def play_midi_file(
        self,
        midi_file,
        device: MidiDeviceInterface,
        playback_id: Optional[str] = None,
        start_time: float = 0.0,
        progress_callback: Optional[Callable[[float, float], None]] = None,
    ) -> str:
        """
        Play a MIDI file through a connected device.

        Args:
            midi_file: mido.MidiFile object to play
            device: Connected MIDI device interface
            playback_id: Optional ID for this playback session
            start_time: Start time in seconds (for seeking)
            progress_callback: Optional callback for playback progress

        Returns:
            Playback ID for controlling playback
        """
        if not MIDO_AVAILABLE:
            raise MidiError("MIDI file playback requires the 'mido' library")

        if playback_id is None:
            playback_id = f"playback_{int(time.time() * 1000)}"

        # Stop any existing playback with this ID
        await self.stop_playback(playback_id)

        # Create and start playback task
        task = asyncio.create_task(self._playback_loop(midi_file, device, playback_id, start_time, progress_callback))

        self._playback_tasks[playback_id] = task
        self._playback_states[playback_id] = PlaybackState.PLAYING

        self.logger.info(f"Started MIDI playback with ID: {playback_id}")
        return playback_id

    async def stop_playback(self, playback_id: str) -> bool:
        """
        Stop playback for the given ID.

        Args:
            playback_id: ID of the playback to stop

        Returns:
            True if playback was stopped, False if not found
        """
        if playback_id in self._playback_tasks:
            task = self._playback_tasks[playback_id]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            del self._playback_tasks[playback_id]
            self._playback_states[playback_id] = PlaybackState.STOPPED

            self.logger.info(f"Stopped MIDI playback: {playback_id}")
            return True

        return False

    async def pause_playback(self, playback_id: str) -> bool:
        """
        Pause playback (not implemented in this version).

        Args:
            playback_id: ID of the playback to pause

        Returns:
            True if paused successfully
        """
        # For Phase 2, we'll implement basic stop/start only
        # Pause/resume functionality would require more complex state management
        self.logger.warning("Pause functionality not implemented - use stop instead")
        return False

    def get_playback_state(self, playback_id: str) -> PlaybackState:
        """
        Get the current playback state.

        Args:
            playback_id: ID of the playback to check

        Returns:
            Current playback state
        """
        return self._playback_states.get(playback_id, PlaybackState.STOPPED)

    def list_active_playbacks(self) -> Dict[str, PlaybackState]:
        """
        List all active playback sessions.

        Returns:
            Dictionary of playback IDs and their states
        """
        # Clean up finished tasks
        finished_ids = []
        for playback_id, task in self._playback_tasks.items():
            if task.done():
                finished_ids.append(playback_id)
                self._playback_states[playback_id] = PlaybackState.FINISHED

        for playback_id in finished_ids:
            del self._playback_tasks[playback_id]

        return self._playback_states.copy()

    async def stop_all_playback(self) -> int:
        """
        Stop all active playback sessions.

        Returns:
            Number of playback sessions stopped
        """
        stopped_count = 0
        playback_ids = list(self._playback_tasks.keys())

        for playback_id in playback_ids:
            if await self.stop_playback(playback_id):
                stopped_count += 1

        return stopped_count

    async def _playback_loop(
        self,
        midi_file,
        device: MidiDeviceInterface,
        playback_id: str,
        start_time: float,
        progress_callback: Optional[Callable[[float, float], None]],
    ) -> None:
        """
        Main playback loop with timing synchronization.

        Args:
            midi_file: MIDI file to play
            device: MIDI device to send messages to
            playback_id: ID for this playback session
            start_time: Start time offset in seconds
            progress_callback: Optional progress callback
        """
        try:
            self.logger.info(f"Starting playback loop for {playback_id}")

            # Send initial setup messages (program changes, etc.)
            await self._send_initial_setup(device, midi_file)

            # Get total file duration
            total_duration = midi_file.length

            # Convert MIDI file to absolute time messages
            messages = []
            current_time = 0.0

            for msg in midi_file:
                current_time += msg.time
                if current_time >= start_time:  # Skip messages before start time
                    messages.append((current_time - start_time, msg))

            if not messages:
                self.logger.warning(f"No MIDI messages to play in {playback_id}")
                return

            # Start playback timing
            playback_start = time.time()
            message_index = 0

            while message_index < len(messages):
                # Check if playback was cancelled
                if playback_id not in self._playback_tasks:
                    break

                msg_time, msg = messages[message_index]
                current_playback_time = time.time() - playback_start

                # Wait until it's time to send this message
                if msg_time > current_playback_time:
                    sleep_time = msg_time - current_playback_time
                    if sleep_time > 0.001:  # Only sleep if significant time
                        await asyncio.sleep(sleep_time)

                # Send the MIDI message
                try:
                    await self._send_midi_message(device, msg)
                except Exception as e:
                    self.logger.error(f"Error sending MIDI message: {e}")

                # Update progress
                if progress_callback:
                    progress = (msg_time + start_time) / total_duration if total_duration > 0 else 1.0
                    try:
                        progress_callback(msg_time + start_time, progress)
                    except Exception as e:
                        self.logger.error(f"Error in progress callback: {e}")

                message_index += 1

            # Playback finished
            self._playback_states[playback_id] = PlaybackState.FINISHED
            self.logger.info(f"Playback finished: {playback_id}")

        except asyncio.CancelledError:
            self.logger.info(f"Playback cancelled: {playback_id}")
            # Send all notes off to prevent hanging notes
            await self._send_all_notes_off(device)
            raise
        except Exception as e:
            self.logger.error(f"Playback error in {playback_id}: {e}")
            self._playback_states[playback_id] = PlaybackState.STOPPED
            await self._send_all_notes_off(device)
            raise

    async def _send_midi_message(self, device: MidiDeviceInterface, msg) -> None:
        """
        Send a MIDI message through the device interface.

        Args:
            device: MIDI device interface
            msg: mido MIDI message
        """
        try:
            # Handle different message types
            if hasattr(msg, "type"):
                if msg.type == "note_on":
                    await device.send_note_on(msg.note, msg.velocity, msg.channel)
                elif msg.type == "note_off":
                    await device.send_note_off(msg.note, msg.velocity, msg.channel)
                elif msg.type == "control_change":
                    await device.send_control_change(msg.control, msg.value, msg.channel)
                elif msg.type == "program_change":
                    await device.send_program_change(msg.program, msg.channel)
                elif msg.type == "pitchwheel":
                    await device.send_pitch_bend(msg.pitch, msg.channel)
                # Skip meta messages (tempo, time signature, etc.) as they don't send MIDI data
                # Skip system exclusive and other non-standard messages for now

        except Exception as e:
            self.logger.error(f"Failed to send MIDI message {msg}: {e}")
            # Don't re-raise to avoid stopping playback for single message errors

    async def _send_all_notes_off(self, device: MidiDeviceInterface) -> None:
        """
        Send all notes off messages to prevent hanging notes.

        Args:
            device: MIDI device interface
        """
        try:
            # Send control change 123 (all notes off) on all channels
            for channel in range(16):
                await device.send_control_change(123, 0, channel)

            self.logger.debug("Sent all notes off messages")

        except Exception as e:
            self.logger.error(f"Failed to send all notes off: {e}")

    async def _send_initial_setup(self, device: MidiDeviceInterface, midi_file) -> None:
        """
        Send initial setup messages (program changes, controllers, etc.) to prepare for playback.

        Args:
            device: MIDI device interface
            midi_file: MIDI file to extract setup from
        """
        try:
            # Extract the first program change for each channel
            channel_programs = {}
            channel_volumes = {}
            channel_pans = {}

            for track in midi_file.tracks:
                for msg in track:
                    if hasattr(msg, "type") and hasattr(msg, "channel"):
                        if msg.type == "program_change":
                            if msg.channel not in channel_programs:
                                channel_programs[msg.channel] = msg.program
                        elif msg.type == "control_change":
                            if msg.control == 7 and msg.channel not in channel_volumes:  # Volume
                                channel_volumes[msg.channel] = msg.value
                            elif msg.control == 10 and msg.channel not in channel_pans:  # Pan
                                channel_pans[msg.channel] = msg.value

            # Send program changes
            for channel, program in channel_programs.items():
                await device.send_program_change(program, channel)

            # Send volume settings
            for channel, volume in channel_volumes.items():
                await device.send_control_change(7, volume, channel)

            # Send pan settings
            for channel, pan in channel_pans.items():
                await device.send_control_change(10, pan, channel)

            setup_count = len(channel_programs) + len(channel_volumes) + len(channel_pans)
            if setup_count > 0:
                self.logger.info(
                    f"Sent initial setup: {len(channel_programs)} programs, {len(channel_volumes)} volumes, {len(channel_pans)} pans"
                )

        except Exception as e:
            self.logger.error(f"Failed to send initial setup: {e}")


class PlaybackProgressTracker:
    """
    Tracks playback progress and provides callbacks for UI updates.
    """

    def __init__(self, playback_id: str, total_duration: float):
        """
        Initialize progress tracker.

        Args:
            playback_id: ID of the playback session
            total_duration: Total duration in seconds
        """
        self.playback_id = playback_id
        self.total_duration = total_duration
        self.current_time = 0.0
        self.progress = 0.0
        self.callbacks = []

    def add_callback(self, callback: Callable[[str, float, float], None]) -> None:
        """
        Add a progress callback.

        Args:
            callback: Function to call with (playback_id, current_time, progress)
        """
        self.callbacks.append(callback)

    def update_progress(self, current_time: float, progress: float) -> None:
        """
        Update progress and notify callbacks.

        Args:
            current_time: Current playback time in seconds
            progress: Progress as a float 0.0-1.0
        """
        self.current_time = current_time
        self.progress = progress

        for callback in self.callbacks:
            try:
                callback(self.playback_id, current_time, progress)
            except Exception as e:
                logging.getLogger(__name__).error(f"Progress callback error: {e}")
