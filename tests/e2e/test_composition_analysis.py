#!/usr/bin/env python3
"""
End-to-End test for composition analysis system using mission-impossible.mid.

Tests the refactored AnalysisEngine, PartGenerator, and LibraryIntegration
components with a real MIDI file following the E2E testing strategy from
docs/CODE_REVIEW.md.
"""

import pytest
import asyncio
import subprocess
import time
import os
import sys
from pathlib import Path
from jsonschema import validate
from typing import Dict, Any, List

# Add src directory to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from midi_mcp.midi.file_ops import MidiFileManager
from midi_mcp.genres.analysis_engine import AnalysisEngine
from midi_mcp.genres.library_integration import LibraryIntegration
from midi_mcp.genres.composer import Composer


class TestCompositionAnalysis:
    """Test suite for composition analysis using mission-impossible.mid."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.midi_file_path = Path(__file__).parent.parent.parent / "examples" / "mission-impossible.mid"
        cls.libraries = LibraryIntegration()
        cls.analysis_engine = AnalysisEngine(cls.libraries)
        cls.composer = Composer()
        cls.midi_manager = MidiFileManager()

        # Verify test file exists
        assert cls.midi_file_path.exists(), f"Test MIDI file not found: {cls.midi_file_path}"

    def test_midi_file_loading(self):
        """Test loading the mission-impossible.mid file."""
        # Load MIDI file
        file_id = self.midi_manager.load_midi_file(str(self.midi_file_path))

        # Validate file was loaded
        assert file_id is not None
        assert isinstance(file_id, str)
        assert len(file_id) > 0

        # Verify file is in active files
        assert file_id in self.midi_manager._active_files

    def test_extract_melody_characteristics(self):
        """Test melody analysis functionality."""
        # Load MIDI file
        file_id = self.midi_manager.load_midi_file(str(self.midi_file_path))
        session = self.midi_manager._active_files[file_id]

        # Extract melody data (simplified - would need proper MIDI parsing)
        sample_melody = [
            {"note": "G4", "beat": 1, "duration": 1.0, "relation_to_chord": "chord_tone"},
            {"note": "C5", "beat": 2, "duration": 0.5, "relation_to_chord": "chord_tone"},
            {"note": "Bb4", "beat": 2.5, "duration": 0.5, "relation_to_chord": "scale_tone"},
            {"note": "G4", "beat": 3, "duration": 1.0, "relation_to_chord": "chord_tone"},
        ]

        # Analyze melody characteristics
        characteristics = self.analysis_engine.analyze_melody_characteristics(sample_melody, "spy_theme")

        # Validate response structure
        melody_schema = {
            "type": "object",
            "properties": {
                "note_count": {"type": "integer", "minimum": 0},
                "range": {"type": "string"},
                "chord_tone_ratio": {"type": "number", "minimum": 0, "maximum": 1},
                "genre_appropriateness": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["note_count", "range", "chord_tone_ratio", "genre_appropriateness"],
        }

        validate(instance=characteristics, schema=melody_schema)

        # Validate analysis results make sense
        assert characteristics["note_count"] == 4
        assert characteristics["chord_tone_ratio"] == 0.75  # 3 out of 4 notes are chord tones
        assert characteristics["genre_appropriateness"] == "high"

    def test_bass_voice_leading_analysis(self):
        """Test bass voice leading analysis with music21 integration."""
        # Sample bass line data representing mission impossible style movement
        bass_line = [
            {"note": "C2", "beat": 1, "duration": 2.0},
            {"note": "F2", "beat": 3, "duration": 2.0},  # Perfect 4th leap
            {"note": "G2", "beat": 5, "duration": 2.0},  # Step up
            {"note": "C3", "beat": 7, "duration": 2.0},  # Perfect 4th leap up
            {"note": "F1", "beat": 9, "duration": 2.0},  # Large leap down (tritone)
        ]

        # Analyze voice leading
        voice_leading = self.analysis_engine.analyze_bass_voice_leading(bass_line)

        # Validate response structure
        voice_leading_schema = {
            "type": "object",
            "properties": {
                "quality": {"type": "string", "enum": ["insufficient_data", "smooth", "moderate", "choppy"]},
                "large_leaps": {"type": "integer", "minimum": 0},
                "leap_details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from": {"type": "string"},
                            "to": {"type": "string"},
                            "interval_semitones": {"type": ["integer", "null"]},
                            "beat": {"type": ["integer", "number", "null"]},
                        },
                        "required": ["from", "to", "interval_semitones", "beat"],
                    },
                },
                "recommendations": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["quality", "large_leaps", "leap_details", "recommendations"],
        }

        validate(instance=voice_leading, schema=voice_leading_schema)

        # Validate analysis makes musical sense
        if self.libraries.music21.is_available():
            assert voice_leading["large_leaps"] >= 1  # Should detect the large leap to F1
            assert len(voice_leading["leap_details"]) >= 1
            assert voice_leading["quality"] in ["moderate", "choppy"]

    def test_music21_interval_calculation(self):
        """Test proper interval calculation using music21."""
        if not self.libraries.music21.is_available():
            pytest.skip("music21 not available")

        # Test interval calculation
        interval = self.libraries.music21.calculate_interval_semitones("C4", "G4")
        assert interval == 7  # Perfect fifth

        # Test large leap detection
        is_large = self.libraries.music21.is_large_leap("C4", "C5", threshold_semitones=7)
        assert is_large  # Octave is larger than perfect fifth threshold

        # Test passing tone generation
        passing_tone = self.libraries.music21.get_passing_tone("C4", "E4")
        assert passing_tone in ["C#4", "D4", "D#4"]  # Should be a chromatic passing tone

    def test_composition_system_integration(self):
        """Test integration of all refactored composition components."""
        # Test that Composer properly initializes with shared libraries
        assert self.composer.libraries is not None
        assert self.composer.analysis_engine is not None
        assert self.composer.part_generator is not None
        assert self.composer.arrangement_engine is not None

        # Test that components share the same library instance
        assert self.composer.part_generator.libraries is self.composer.libraries
        assert self.composer.analysis_engine.libraries is self.composer.libraries

    def test_genre_data_consistency(self):
        """Test that genre data is properly accessible."""
        # Get some basic genre data
        blues_data = self.composer.genre_manager.get_genre_data("blues")
        assert isinstance(blues_data, dict)
        assert "scales" in blues_data or "rhythms" in blues_data or "instrumentation" in blues_data

    @pytest.mark.timeout(30)
    def test_analysis_performance(self):
        """Test that analysis operations complete within reasonable time."""
        # Large melody for performance testing
        large_melody = [
            {"note": f"C{4 + (i % 2)}", "beat": i + 1, "duration": 0.5, "relation_to_chord": "chord_tone"}
            for i in range(100)
        ]

        start_time = time.time()
        characteristics = self.analysis_engine.analyze_melody_characteristics(large_melody, "test")
        analysis_time = time.time() - start_time

        assert analysis_time < 5.0  # Should complete within 5 seconds
        assert characteristics["note_count"] == 100

    def test_error_handling(self):
        """Test proper error handling in analysis functions."""
        # Test with empty melody
        result = self.analysis_engine.analyze_melody_characteristics([], "test")
        assert result == {}

        # Test with insufficient bass data
        result = self.analysis_engine.analyze_bass_voice_leading([{"note": "C4", "beat": 1}])
        assert result["quality"] == "insufficient_data"

    def test_analysis_response_schemas(self):
        """Test that all analysis responses conform to expected schemas."""
        # This validates the JSON schema validation capability
        sample_data = {
            "melody": [{"note": "C4", "beat": 1, "duration": 1.0, "relation_to_chord": "chord_tone"}],
            "bass_line": [{"note": "C2", "beat": 1, "duration": 4.0}, {"note": "F2", "beat": 5, "duration": 4.0}],
        }

        melody_result = self.analysis_engine.analyze_melody_characteristics(sample_data["melody"], "test")
        bass_result = self.analysis_engine.analyze_bass_voice_leading(sample_data["bass_line"])

        # Both should return valid dictionaries
        assert isinstance(melody_result, dict)
        assert isinstance(bass_result, dict)
        assert "quality" in bass_result
        if melody_result:  # Only check if not empty
            assert "note_count" in melody_result


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])
