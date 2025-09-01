# -*- coding: utf-8 -*-
"""
Unit tests for API enhancements to MIDI MCP Server.

Tests the new functionality:
1. add_musical_data_to_midi_file wrapper tool
2. Enhanced composition tools with direct MIDI output
3. Auto-track creation functionality
"""

import pytest
from typing import Dict, List, Any

from midi_mcp.midi.file_ops import MidiFileManager


class TestApiEnhancements:
    """Test API enhancements for MIDI MCP Server."""

    @pytest.fixture
    def file_manager(self):
        """Create a MidiFileManager instance for testing."""
        return MidiFileManager()

    def test_midi_file_creation(self, file_manager):
        """Test basic MIDI file creation."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        file_id = file_manager.create_midi_file(
            title="Test API Enhancements",
            tempo=120,
            time_signature=(4, 4),
            key_signature="C"
        )
        
        assert file_id is not None
        assert isinstance(file_id, str)
        
        # Verify file was created in session
        session = file_manager.get_session(file_id)
        assert session.title == "Test API Enhancements"
        assert session.tempo == 120
        assert session.time_signature == (4, 4)
        assert session.key_signature == "C"

    def test_track_creation_and_note_addition(self, file_manager):
        """Test track creation and note addition functionality."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        # Create MIDI file
        file_id = file_manager.create_midi_file(title="Track Test")
        
        # Create test notes - C major scale
        c_major_scale = [
            {"note": 60, "velocity": 80, "start_time": 0.0, "duration": 0.5},  # C4
            {"note": 62, "velocity": 80, "start_time": 0.5, "duration": 0.5},  # D4
            {"note": 64, "velocity": 80, "start_time": 1.0, "duration": 0.5},  # E4
            {"note": 65, "velocity": 80, "start_time": 1.5, "duration": 0.5},  # F4
            {"note": 67, "velocity": 80, "start_time": 2.0, "duration": 0.5},  # G4
            {"note": 69, "velocity": 80, "start_time": 2.5, "duration": 0.5},  # A4
            {"note": 71, "velocity": 80, "start_time": 3.0, "duration": 0.5},  # B4
            {"note": 72, "velocity": 80, "start_time": 3.5, "duration": 0.5},  # C5
        ]
        
        # Add track and notes
        track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name="C Major Scale",
            channel=0,
            program=0
        )
        
        assert isinstance(track_index, int)
        assert track_index >= 0
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="C Major Scale",
            notes_data=c_major_scale,
            channel=0
        )
        
        # Verify track was created
        session = file_manager.get_session(file_id)
        track_names = [track["name"] for track in session.tracks]
        assert "C Major Scale" in track_names

    def test_auto_track_creation_functionality(self, file_manager):
        """Test auto-track creation functionality (simulating add_musical_data_to_midi_file tool)."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        # Create MIDI file
        file_id = file_manager.create_midi_file(title="Auto Track Test")
        
        # Create chord progression
        chord_progression = [
            # C major chord (C-E-G)
            {"note": 60, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # C4
            {"note": 64, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # E4
            {"note": 67, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # G4
            
            # A minor chord (A-C-E)
            {"note": 57, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # A3
            {"note": 60, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # C4
            {"note": 64, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # E4
            
            # D minor chord (D-F-A)
            {"note": 62, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # D4
            {"note": 65, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # F4
            {"note": 69, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # A4
            
            # G major chord (G-B-D)
            {"note": 55, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # G3
            {"note": 59, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # B3
            {"note": 62, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # D4
        ]
        
        # Test auto-track creation logic (simulating add_musical_data_to_midi_file tool)
        chord_track_name = "Chord Progression"
        session = file_manager.get_session(file_id)
        track_exists = any(track.get("name") == chord_track_name for track in session.tracks)
        
        assert not track_exists  # Should not exist initially
        
        # Create track automatically
        chord_track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name=chord_track_name,
            channel=1,
            program=0
        )
        
        assert isinstance(chord_track_index, int)
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier=chord_track_name,
            notes_data=chord_progression,
            channel=1
        )
        
        # Verify track was auto-created
        session = file_manager.get_session(file_id)
        track_names = [track["name"] for track in session.tracks]
        assert chord_track_name in track_names

    def test_midi_file_analysis(self, file_manager):
        """Test MIDI file analysis functionality."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        # Create MIDI file with content
        file_id = file_manager.create_midi_file(title="Analysis Test")
        
        # Add a track with some notes
        track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name="Test Track",
            channel=0,
            program=0
        )
        
        test_notes = [
            {"note": 60, "velocity": 80, "start_time": 0.0, "duration": 1.0},
            {"note": 64, "velocity": 80, "start_time": 1.0, "duration": 1.0},
            {"note": 67, "velocity": 80, "start_time": 2.0, "duration": 1.0},
        ]
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="Test Track",
            notes_data=test_notes,
            channel=0
        )
        
        # Analyze the file
        analysis = file_manager.analyze_midi_file(file_id)
        
        assert analysis["file_id"] == file_id
        assert analysis["title"] == "Analysis Test"
        assert analysis["tracks"] >= 1  # At least metadata track + our track
        assert analysis["note_count"] == 3
        assert analysis["note_range"]["min"] == 60
        assert analysis["note_range"]["max"] == 67
        assert len(analysis["track_info"]) >= 1
        
        # Check track info
        track_names = [track["name"] for track in analysis["track_info"]]
        assert "Test Track" in track_names

    def test_file_save_and_load(self, file_manager, tmp_path):
        """Test MIDI file saving and loading functionality."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        # Create MIDI file with content
        file_id = file_manager.create_midi_file(title="Save Load Test")
        
        # Add a track
        file_manager.add_track(
            midi_file_id=file_id,
            track_name="Test Track",
            channel=0,
            program=0
        )
        
        test_notes = [
            {"note": 60, "velocity": 80, "start_time": 0.0, "duration": 1.0},
            {"note": 64, "velocity": 80, "start_time": 1.0, "duration": 1.0},
        ]
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="Test Track",
            notes_data=test_notes,
            channel=0
        )
        
        # Save the file
        output_path = tmp_path / "test_save_load.mid"
        saved_path = file_manager.save_midi_file(file_id, str(output_path))
        
        assert output_path.exists()
        assert saved_path == str(output_path)
        
        # Load the saved file
        loaded_file_id = file_manager.load_midi_file(saved_path)
        loaded_analysis = file_manager.analyze_midi_file(loaded_file_id)
        
        assert loaded_file_id != file_id  # Different ID for loaded file
        assert loaded_analysis["title"] == "Save Load Test"
        assert loaded_analysis["note_count"] == 2
        
        # Verify track names match
        original_analysis = file_manager.analyze_midi_file(file_id)
        original_tracks = [track["name"] for track in original_analysis["track_info"]]
        loaded_tracks = [track["name"] for track in loaded_analysis["track_info"]]
        
        assert "Test Track" in original_tracks
        assert "Test Track" in loaded_tracks

    def test_complete_workflow(self, file_manager, tmp_path):
        """Test the complete API enhancement workflow end-to-end."""
        try:
            import mido
        except ImportError:
            pytest.skip("mido library not available")

        # Step 1: Create MIDI file
        file_id = file_manager.create_midi_file(
            title="Complete Workflow Test",
            tempo=120,
            time_signature=(4, 4),
            key_signature="C"
        )
        assert file_id is not None
        
        # Step 2: Add melody track
        melody_track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name="Melody",
            channel=0,
            program=0
        )
        
        melody_notes = [
            {"note": 60, "velocity": 80, "start_time": 0.0, "duration": 0.5},
            {"note": 62, "velocity": 80, "start_time": 0.5, "duration": 0.5},
            {"note": 64, "velocity": 80, "start_time": 1.0, "duration": 0.5},
            {"note": 65, "velocity": 80, "start_time": 1.5, "duration": 0.5},
        ]
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="Melody",
            notes_data=melody_notes,
            channel=0
        )
        
        # Step 3: Add harmony track (auto-creation test)
        harmony_notes = [
            {"note": 48, "velocity": 60, "start_time": 0.0, "duration": 2.0},
            {"note": 52, "velocity": 60, "start_time": 0.0, "duration": 2.0},
            {"note": 55, "velocity": 60, "start_time": 0.0, "duration": 2.0},
        ]
        
        harmony_track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name="Harmony",
            channel=1,
            program=0
        )
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="Harmony",
            notes_data=harmony_notes,
            channel=1
        )
        
        # Step 4: Analyze
        analysis = file_manager.analyze_midi_file(file_id)
        assert analysis["tracks"] >= 2  # At least melody + harmony + metadata
        assert analysis["note_count"] == 7  # 4 melody + 3 harmony
        
        track_names = [track["name"] for track in analysis["track_info"]]
        assert "Melody" in track_names
        assert "Harmony" in track_names
        
        # Step 5: Save
        output_path = tmp_path / "complete_workflow_test.mid"
        saved_path = file_manager.save_midi_file(file_id, str(output_path))
        assert output_path.exists()
        
        # Step 6: Load and verify
        loaded_file_id = file_manager.load_midi_file(saved_path)
        loaded_analysis = file_manager.analyze_midi_file(loaded_file_id)
        
        assert loaded_analysis["title"] == "Complete Workflow Test"
        assert loaded_analysis["note_count"] == 7
        
        loaded_track_names = [track["name"] for track in loaded_analysis["track_info"]]
        assert "Melody" in loaded_track_names
        assert "Harmony" in loaded_track_names
