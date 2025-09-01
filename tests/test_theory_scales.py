"""Tests for music theory scales module."""

import pytest
from src.midi_mcp.theory.scales import ScaleManager
from src.midi_mcp.models.theory_models import Scale, Note


class TestScaleManager:
    """Test cases for ScaleManager functionality."""

    @pytest.fixture
    def scale_manager(self):
        return ScaleManager()

    def test_generate_major_scale(self, scale_manager):
        """Test generating a C major scale."""
        scale = scale_manager.generate_scale("C", "major", 4)

        assert scale.root.name == "C"
        assert scale.name == "major"
        assert len(scale.notes) == 7

        # Check note names
        expected_notes = ["C", "D", "E", "F", "G", "A", "B"]
        actual_notes = [note.name for note in scale.notes]
        assert actual_notes == expected_notes

        # Check MIDI numbers for C4 major scale
        expected_midi = [60, 62, 64, 65, 67, 69, 71]
        actual_midi = [note.midi_note for note in scale.notes]
        assert actual_midi == expected_midi

    def test_generate_minor_scale(self, scale_manager):
        """Test generating an A natural minor scale."""
        scale = scale_manager.generate_scale("A", "natural_minor", 4)

        assert scale.root.name == "A"
        assert scale.name == "natural_minor"

        # A natural minor: A B C D E F G
        expected_notes = ["A", "B", "C", "D", "E", "F", "G"]
        actual_notes = [note.name for note in scale.notes]
        assert actual_notes == expected_notes

    def test_generate_dorian_mode(self, scale_manager):
        """Test generating a D dorian scale."""
        scale = scale_manager.generate_scale("D", "dorian", 4)

        assert scale.root.name == "D"
        assert scale.name == "dorian"

        # D dorian: D E F G A B C
        expected_notes = ["D", "E", "F", "G", "A", "B", "C"]
        actual_notes = [note.name for note in scale.notes]
        assert actual_notes == expected_notes

    def test_generate_pentatonic_scale(self, scale_manager):
        """Test generating a major pentatonic scale."""
        scale = scale_manager.generate_scale("G", "major_pentatonic", 4)

        assert scale.root.name == "G"
        assert scale.name == "major_pentatonic"
        assert len(scale.notes) == 5

        # G major pentatonic: G A B D E
        expected_notes = ["G", "A", "B", "D", "E"]
        actual_notes = [note.name for note in scale.notes]
        assert actual_notes == expected_notes

    def test_invalid_scale_type(self, scale_manager):
        """Test error handling for invalid scale type."""
        with pytest.raises(ValueError, match="Unknown scale type"):
            scale_manager.generate_scale("C", "invalid_scale", 4)

    def test_identify_intervals(self, scale_manager):
        """Test interval identification."""
        notes = [60, 62, 64, 67]  # C D E G
        intervals = scale_manager.identify_intervals(notes)

        assert len(intervals) == 3
        assert intervals[0]["semitones"] == 2  # C to D (major second)
        assert intervals[1]["semitones"] == 2  # D to E (major second)
        assert intervals[2]["semitones"] == 3  # E to G (minor third)

        # Check interval names
        assert intervals[0]["name"] == "major2nd"
        assert intervals[2]["name"] == "minor3rd"

    def test_transpose_to_key(self, scale_manager):
        """Test transposing notes between keys."""
        # C major notes
        c_major_notes = [60, 62, 64, 65, 67, 69, 71]

        # Transpose from C to G (up 7 semitones)
        g_major_notes = scale_manager.transpose_to_key(c_major_notes, "C", "G")
        expected_g_major = [67, 69, 71, 72, 74, 76, 78]

        assert g_major_notes == expected_g_major

    def test_get_scale_degrees(self, scale_manager):
        """Test scale degree identification."""
        scale = scale_manager.generate_scale("F", "major", 4)
        degrees = scale_manager.get_scale_degrees(scale)

        assert len(degrees) == 7
        assert degrees[1]["degree"] == 1
        assert degrees[1]["degree_name"] == "tonic"
        assert degrees[5]["degree_name"] == "dominant"
        assert degrees[1]["note_name"] == "F"  # Root

    def test_find_relative_scales(self, scale_manager):
        """Test finding relative scales."""
        c_major = scale_manager.generate_scale("C", "major", 4)
        relatives = scale_manager.find_relative_scales(c_major)

        # Should include relative minor
        assert "relative_minor" in relatives
        relative_minor = relatives["relative_minor"]
        assert relative_minor.root.name == "A"  # Am is relative minor of C major

        # Should include parallel minor
        assert "parallel_minor" in relatives
        parallel_minor = relatives["parallel_minor"]
        assert parallel_minor.root.name == "C"  # Cm is parallel minor of C major

    def test_compare_scales(self, scale_manager):
        """Test scale comparison functionality."""
        c_major = scale_manager.generate_scale("C", "major", 4)
        a_minor = scale_manager.generate_scale("A", "natural_minor", 4)

        comparison = scale_manager.compare_scales(c_major, a_minor)

        # C major and A minor are relative - should share all pitch classes
        assert comparison["similarity_ratio"] == 1.0
        assert comparison["is_mode_relationship"] == True
        assert len(comparison["common_pitch_classes"]) == 7
        assert len(comparison["unique_to_first"]) == 0
        assert len(comparison["unique_to_second"]) == 0

    def test_analyze_scale_from_notes(self, scale_manager):
        """Test scale analysis from MIDI notes."""
        # C major scale notes
        c_major_notes = [60, 62, 64, 65, 67, 69, 71]

        matches = scale_manager.analyze_scale_from_notes(c_major_notes)

        assert len(matches) > 0

        # First match should be C major
        best_match = matches[0]
        assert best_match["root"] == "C"
        assert best_match["scale_name"] == "major"
        assert best_match["confidence"] > 0.9

    def test_get_available_scales(self, scale_manager):
        """Test getting list of available scales."""
        scales = scale_manager.get_available_scales()

        assert isinstance(scales, list)
        assert len(scales) > 0
        assert "major" in scales
        assert "minor" in scales
        assert "dorian" in scales
        assert "pentatonic_major" in scales
