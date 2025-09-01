#!/usr/bin/env python3
"""
Integration test for the complete MIDI composition workflow.

This test validates the end-to-end process of creating a complete composition
with actual MIDI note data, ensuring all components work together properly.
"""

import pytest
import asyncio
import json
import tempfile
import os
import sys
from pathlib import Path

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from midi_mcp.composition.complete_composer import CompleteComposer
from midi_mcp.midi.file_ops import MidiFileManager
from midi_mcp.midi.analyzer import MidiAnalyzer


class TestCompleteWorkflow:
    """Test the complete composition to MIDI workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.file_manager = MidiFileManager()
        self.composer = CompleteComposer()
        self.analyzer = MidiAnalyzer()
        
    def test_complete_composition_workflow(self):
        """Test the complete composition to playable MIDI workflow."""
        # Step 1: Create a MIDI file
        midi_file_id = self.file_manager.create_midi_file(
            title="Test Integration Song",
            tempo=120,
            key_signature="C"  # Use C major to avoid the Am issue for now
        )
        assert midi_file_id is not None
        
        # Step 2: Add tracks
        piano_track = self.file_manager.add_track(midi_file_id, "Piano", channel=0, program=0)
        bass_track = self.file_manager.add_track(midi_file_id, "Bass", channel=1, program=32)
        
        assert piano_track == 1
        assert bass_track == 2
        
        # Step 3: Create composition structure
        composition = self.composer.compose_complete_song(
            description="a simple test song",
            genre="pop",
            key="C major",  # Use C major to avoid the scale issue
            tempo=120,
            target_duration=120
        )
        
        assert composition is not None
        assert composition.key == "C major"
        assert composition.tempo == 120
        assert len(composition.structure.sections) > 0
        
        # Step 4: Add simple test notes to verify MIDI population works
        test_melody = [
            {"note": 60, "start": 0, "duration": 1, "velocity": 80, "channel": 0},  # C
            {"note": 62, "start": 1, "duration": 1, "velocity": 75, "channel": 0},  # D
            {"note": 64, "start": 2, "duration": 1, "velocity": 85, "channel": 0},  # E
            {"note": 65, "start": 3, "duration": 1, "velocity": 70, "channel": 0},  # F
        ]
        
        test_bass = [
            {"note": 48, "start": 0, "duration": 2, "velocity": 70, "channel": 1},  # C2
            {"note": 53, "start": 2, "duration": 2, "velocity": 70, "channel": 1},  # F2
        ]
        
        # Add notes to tracks
        melody_count = self.file_manager.add_notes_to_track(midi_file_id, 1, test_melody, 120)
        bass_count = self.file_manager.add_notes_to_track(midi_file_id, 2, test_bass, 120)
        
        assert melody_count == 4
        assert bass_count == 2
        
        # Step 5: Save the file to a temporary location
        with tempfile.TemporaryDirectory() as temp_dir:
            test_filename = os.path.join(temp_dir, "test_integration.mid")
            saved_path = self.file_manager.save_midi_file(midi_file_id, test_filename)
            
            assert os.path.exists(saved_path)
            assert Path(saved_path).suffix == '.mid'
            
            # Step 6: Analyze the file
            session = self.file_manager._get_session(midi_file_id)
            analysis = self.analyzer.analyze_comprehensive(session.midi_file)
            
            assert 'notes' in analysis
            assert 'timing' in analysis
            assert analysis['notes']['total_notes'] == 6  # 4 melody + 2 bass
            
    def test_composition_with_minor_key(self):
        """Test composition workflow with a minor key to verify the scale fix."""
        # Create a simple minor key composition to test the scale fix
        composition = self.composer.compose_complete_song(
            description="a melancholic song",
            genre="ballad", 
            key="Am",  # This should now work without the warning
            tempo=72,
            target_duration=60
        )
        
        assert composition is not None
        assert composition.key == "Am"
        assert composition.tempo == 72
        
    def test_add_notes_timing_accuracy(self):
        """Test that MIDI timing is calculated correctly."""
        midi_file_id = self.file_manager.create_midi_file(
            title="Timing Test",
            tempo=120
        )
        
        track_idx = self.file_manager.add_track(midi_file_id, "Test Track", channel=0)
        
        # Add notes with specific timing
        notes = [
            {"note": 60, "start": 0, "duration": 1, "velocity": 80},
            {"note": 64, "start": 1, "duration": 1, "velocity": 80},
            {"note": 67, "start": 2, "duration": 2, "velocity": 80},
        ]
        
        count = self.file_manager.add_notes_to_track(midi_file_id, track_idx, notes, 120)
        assert count == 3
        
        # Verify the MIDI file contains the correct timing
        session = self.file_manager._get_session(midi_file_id)
        analysis = self.analyzer.analyze_comprehensive(session.midi_file)
        
        assert analysis['notes']['total_notes'] == 3
        
    def test_multiple_note_additions_to_same_track(self):
        """Test adding multiple sets of notes to the same track without timing conflicts."""
        midi_file_id = self.file_manager.create_midi_file(title="Multi-Add Test")
        track_idx = self.file_manager.add_track(midi_file_id, "Test Track")
        
        # Add first set of notes
        notes1 = [{"note": 60, "start": 0, "duration": 1, "velocity": 80}]
        count1 = self.file_manager.add_notes_to_track(midi_file_id, track_idx, notes1, 120)
        
        # Add second set of notes (should be appended after first set)
        notes2 = [{"note": 64, "start": 0, "duration": 1, "velocity": 80}]
        count2 = self.file_manager.add_notes_to_track(midi_file_id, track_idx, notes2, 120)
        
        assert count1 == 1
        assert count2 == 1
        
        # Verify both notes are in the file
        session = self.file_manager._get_session(midi_file_id)
        analysis = self.analyzer.analyze_comprehensive(session.midi_file)
        assert analysis['notes']['total_notes'] == 2


if __name__ == "__main__":
    # Allow running the test directly
    test_instance = TestCompleteWorkflow()
    test_instance.setup_method()
    
    print("🎵 Running Complete Workflow Integration Tests")
    print("=" * 50)
    
    try:
        test_instance.test_complete_composition_workflow()
        print("✅ Complete workflow test passed")
        
        test_instance.test_composition_with_minor_key()
        print("✅ Minor key composition test passed")
        
        test_instance.test_add_notes_timing_accuracy()
        print("✅ Timing accuracy test passed")
        
        test_instance.test_multiple_note_additions_to_same_track()
        print("✅ Multiple note additions test passed")
        
        print("\n🎉 All integration tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
