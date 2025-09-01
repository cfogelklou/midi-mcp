# -*- coding: utf-8 -*-
"""
MIDI file operations.

Handles creation, loading, saving, and manipulation of MIDI files.
Supports multi-track composition and metadata management.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import logging
import os
import uuid
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

try:
    import mido

    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    mido = None

from .exceptions import MidiError


class MidiFileManager:
    """
    Manages MIDI file operations including creation, loading, saving,
    and session management.
    """

    def __init__(self):
        """Initialize the MIDI file manager."""
        self.logger = logging.getLogger(__name__)
        self._active_files: Dict[str, "MidiFileSession"] = {}

        if not MIDO_AVAILABLE:
            self.logger.warning("mido library not available - MIDI file operations will be limited")

    def create_midi_file(
        self,
        title: str = "Untitled",
        tempo: int = 120,
        time_signature: Tuple[int, int] = (4, 4),
        key_signature: str = "C",
    ) -> str:
        """
        Create a new MIDI file with basic metadata.

        Args:
            title: Song title for metadata
            tempo: Tempo in BPM (default 120)
            time_signature: Time signature as (numerator, denominator)
            key_signature: Key signature (C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F)

        Returns:
            MIDI file ID for future operations
        """
        if not MIDO_AVAILABLE:
            raise MidiError("MIDI file operations require the 'mido' library")

        file_id = str(uuid.uuid4())

        try:
            # Create new MIDI file with type 1 (multi-track)
            midi_file = mido.MidiFile(type=1)

            # Create metadata track (track 0)
            meta_track = mido.MidiTrack()
            midi_file.tracks.append(meta_track)

            # Add tempo
            meta_track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

            # Add time signature
            meta_track.append(
                mido.MetaMessage("time_signature", numerator=time_signature[0], denominator=time_signature[1])
            )

            # Add key signature
            meta_track.append(mido.MetaMessage("key_signature", key=key_signature))

            # Add track name
            meta_track.append(mido.MetaMessage("track_name", name=title))

            # Create session
            session = MidiFileSession(
                file_id=file_id,
                title=title,
                midi_file=midi_file,
                tempo=tempo,
                time_signature=time_signature,
                key_signature=key_signature,
            )

            self._active_files[file_id] = session

            self.logger.info(f"Created MIDI file '{title}' with ID: {file_id}")
            return file_id

        except Exception as e:
            self.logger.error(f"Failed to create MIDI file: {e}")
            raise MidiError(f"Failed to create MIDI file: {str(e)}")

    def add_track(self, midi_file_id: str, track_name: str, channel: int = 0, program: int = 0) -> int:
        """
        Add a new track to an existing MIDI file.

        Args:
            midi_file_id: ID of the MIDI file
            track_name: Name for the track
            channel: MIDI channel (0-15)
            program: MIDI program number (instrument, 0-127)

        Returns:
            Track index number
        """
        session = self._get_session(midi_file_id)

        try:
            # Create new track
            track = mido.MidiTrack()
            session.midi_file.tracks.append(track)

            # Add track name
            track.append(mido.MetaMessage("track_name", name=track_name))

            # Add program change for instrument
            track.append(mido.Message("program_change", channel=channel, program=program))

            track_index = len(session.midi_file.tracks) - 1

            # Update session metadata
            session.tracks.append({"index": track_index, "name": track_name, "channel": channel, "program": program})

            self.logger.info(f"Added track '{track_name}' to MIDI file {midi_file_id}")
            return track_index

        except Exception as e:
            self.logger.error(f"Failed to add track: {e}")
            raise MidiError(f"Failed to add track: {str(e)}")

    def save_midi_file(self, midi_file_id: str, filename: str) -> str:
        """
        Save MIDI file to disk.

        Args:
            midi_file_id: ID of the MIDI file to save
            filename: Output filename (should end in .mid or .midi)

        Returns:
            Full path to saved file
        """
        session = self._get_session(midi_file_id)

        try:
            # Ensure filename has proper extension
            path = Path(filename)
            if path.suffix.lower() not in [".mid", ".midi"]:
                path = path.with_suffix(".mid")

            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Save the file
            session.midi_file.save(str(path))

            # Update session
            session.filename = str(path)
            session.saved = True

            self.logger.info(f"Saved MIDI file {midi_file_id} to {path}")
            return str(path)

        except Exception as e:
            self.logger.error(f"Failed to save MIDI file: {e}")
            raise MidiError(f"Failed to save MIDI file: {str(e)}")

    def load_midi_file(self, filename: str) -> str:
        """
        Load a MIDI file from disk.

        Args:
            filename: Path to MIDI file

        Returns:
            MIDI file ID for future operations
        """
        if not MIDO_AVAILABLE:
            raise MidiError("MIDI file operations require the 'mido' library")

        try:
            path = Path(filename)
            if not path.exists():
                raise MidiError(f"MIDI file not found: {filename}")

            # Load the MIDI file
            midi_file = mido.MidiFile(str(path))

            # Generate file ID
            file_id = str(uuid.uuid4())

            # Analyze the file for metadata
            title = path.stem
            tempo = 120  # Default
            time_signature = (4, 4)  # Default
            key_signature = "C"  # Default
            tracks = []

            # Extract metadata from tracks
            for i, track in enumerate(midi_file.tracks):
                track_info = {"index": i, "name": f"Track {i}", "channel": 0, "program": 0}

                for msg in track:
                    if hasattr(msg, "type"):
                        if msg.type == "track_name":
                            if i == 0:
                                title = msg.name
                            else:
                                track_info["name"] = msg.name
                        elif msg.type == "set_tempo":
                            tempo = round(mido.tempo2bpm(msg.tempo))
                        elif msg.type == "time_signature":
                            time_signature = (msg.numerator, msg.denominator)
                        elif msg.type == "program_change":
                            track_info["channel"] = msg.channel
                            track_info["program"] = msg.program

                tracks.append(track_info)

            # Create session
            session = MidiFileSession(
                file_id=file_id,
                title=title,
                midi_file=midi_file,
                tempo=tempo,
                time_signature=time_signature,
                key_signature=key_signature,
                filename=str(path),
                saved=True,
            )
            session.tracks = tracks

            self._active_files[file_id] = session

            self.logger.info(f"Loaded MIDI file '{filename}' with ID: {file_id}")
            return file_id

        except Exception as e:
            self.logger.error(f"Failed to load MIDI file: {e}")
            raise MidiError(f"Failed to load MIDI file: {str(e)}")

    def analyze_midi_file(self, midi_file_id: str) -> Dict[str, Any]:
        """
        Analyze a loaded MIDI file.

        Returns:
            Comprehensive analysis including:
            - Number of tracks
            - Duration in seconds and beats
            - Tempo changes
            - Key signatures
            - Note range and density
            - Instrument list
        """
        session = self._get_session(midi_file_id)

        try:
            analysis = {
                "file_id": midi_file_id,
                "title": session.title,
                "filename": session.filename,
                "tracks": len(session.midi_file.tracks),
                "tempo": session.tempo,
                "time_signature": session.time_signature,
                "key_signature": session.key_signature,
                "duration_seconds": session.midi_file.length,
                "total_messages": sum(len(track) for track in session.midi_file.tracks),
                "track_info": session.tracks.copy(),
                "note_range": {"min": 127, "max": 0},
                "note_count": 0,
                "instruments": set(),
                "tempo_changes": [],
                "key_changes": [],
            }

            # Analyze each track for detailed information
            for track_idx, track in enumerate(session.midi_file.tracks):
                note_count = 0
                min_note = 127
                max_note = 0

                for msg in track:
                    if hasattr(msg, "type"):
                        if msg.type == "note_on" and msg.velocity > 0:
                            note_count += 1
                            min_note = min(min_note, msg.note)
                            max_note = max(max_note, msg.note)
                        elif msg.type == "program_change":
                            analysis["instruments"].add(msg.program)
                        elif msg.type == "set_tempo":
                            analysis["tempo_changes"].append(
                                {"tempo": round(mido.tempo2bpm(msg.tempo)), "track": track_idx}
                            )
                        elif msg.type == "key_signature":
                            analysis["key_changes"].append({"key": msg.key, "track": track_idx})

                if note_count > 0:
                    analysis["note_range"]["min"] = min(analysis["note_range"]["min"], min_note)
                    analysis["note_range"]["max"] = max(analysis["note_range"]["max"], max_note)
                    analysis["note_count"] += note_count

            # Convert instruments set to list
            analysis["instruments"] = list(analysis["instruments"])

            # Calculate note density (notes per second)
            if analysis["duration_seconds"] > 0:
                analysis["note_density"] = analysis["note_count"] / analysis["duration_seconds"]
            else:
                analysis["note_density"] = 0

            self.logger.info(f"Analyzed MIDI file {midi_file_id}")
            return analysis

        except Exception as e:
            self.logger.error(f"Failed to analyze MIDI file: {e}")
            raise MidiError(f"Failed to analyze MIDI file: {str(e)}")

    def list_midi_files(self) -> List[Dict[str, Any]]:
        """
        List all MIDI files in the current session.

        Returns:
            List of file IDs, names, and basic metadata
        """
        files = []
        for file_id, session in self._active_files.items():
            files.append(
                {
                    "file_id": file_id,
                    "title": session.title,
                    "filename": session.filename,
                    "saved": session.saved,
                    "tracks": len(session.tracks),
                    "tempo": session.tempo,
                    "time_signature": session.time_signature,
                    "key_signature": session.key_signature,
                }
            )

        return files

    def get_session(self, midi_file_id: str) -> "MidiFileSession":
        """Get a MIDI file session by ID."""
        return self._get_session(midi_file_id)

    def close_midi_file(self, midi_file_id: str) -> bool:
        """
        Close a MIDI file session.

        Args:
            midi_file_id: ID of the file to close

        Returns:
            True if closed successfully
        """
        if midi_file_id in self._active_files:
            del self._active_files[midi_file_id]
            self.logger.info(f"Closed MIDI file session {midi_file_id}")
            return True
        return False

    def _get_session(self, midi_file_id: str) -> "MidiFileSession":
        """Get session or raise error if not found."""
        if midi_file_id not in self._active_files:
            raise MidiError(f"MIDI file not found: {midi_file_id}")
        return self._active_files[midi_file_id]


class MidiFileSession:
    """
    Represents an active MIDI file session with metadata and state.
    """

    def __init__(
        self,
        file_id: str,
        title: str,
        midi_file,
        tempo: int = 120,
        time_signature: Tuple[int, int] = (4, 4),
        key_signature: str = "C",
        filename: Optional[str] = None,
        saved: bool = False,
    ):
        """Initialize a MIDI file session."""
        self.file_id = file_id
        self.title = title
        self.midi_file = midi_file
        self.tempo = tempo
        self.time_signature = time_signature
        self.key_signature = key_signature
        self.filename = filename
        self.saved = saved
        self.tracks: List[Dict[str, Any]] = []
        self.created_at = asyncio.get_event_loop().time()

    def __str__(self) -> str:
        """String representation of the session."""
        return f"MidiFileSession(id={self.file_id[:8]}, title='{self.title}', tracks={len(self.tracks)})"
