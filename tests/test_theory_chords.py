"""Tests for music theory chords module."""

import pytest
from src.midi_mcp.theory.chords import ChordManager
from src.midi_mcp.models.theory_models import Chord, Note, Quality, ChordType


class TestChordManager:
    """Test cases for ChordManager functionality."""

    @pytest.fixture
    def chord_manager(self):
        return ChordManager()

    def test_build_major_chord(self, chord_manager):
        """Test building a C major chord."""
        chord = chord_manager.build_chord("C", "major", 0, "close", 4)

        assert chord.root.name == "C"
        assert chord.quality == Quality.MAJOR
        assert chord.chord_type == ChordType.TRIAD
        assert chord.inversion == 0
        assert chord.voicing == "close"

        # Check notes: C E G
        expected_midi = [60, 64, 67]
        actual_midi = [note.midi_note for note in chord.notes]
        assert actual_midi == expected_midi

    def test_build_minor_chord(self, chord_manager):
        """Test building an A minor chord."""
        chord = chord_manager.build_chord("A", "minor", 0, "close", 4)

        assert chord.root.name == "A"
        assert chord.quality == Quality.MINOR

        # Check notes: A C E
        expected_midi = [57, 60, 64]
        actual_midi = [note.midi_note for note in chord.notes]
        assert actual_midi == expected_midi

    def test_build_seventh_chord(self, chord_manager):
        """Test building a G7 chord."""
        chord = chord_manager.build_chord("G", "7", 0, "close", 4)

        assert chord.root.name == "G"
        assert chord.quality == Quality.DOMINANT
        assert chord.chord_type == ChordType.SEVENTH

        # Check notes: G B D F
        expected_midi = [67, 71, 74, 77]
        actual_midi = [note.midi_note for note in chord.notes]
        assert actual_midi == expected_midi

    def test_build_maj7_chord(self, chord_manager):
        """Test building a Cmaj7 chord."""
        chord = chord_manager.build_chord("C", "maj7", 0, "close", 4)

        assert chord.root.name == "C"
        assert chord.quality == Quality.MAJOR
        assert chord.chord_type == ChordType.SEVENTH

        # Check notes: C E G B
        expected_midi = [60, 64, 67, 71]
        actual_midi = [note.midi_note for note in chord.notes]
        assert actual_midi == expected_midi

    def test_chord_inversion(self, chord_manager):
        """Test chord inversions."""
        # First inversion C major (E in bass)
        chord = chord_manager.build_chord("C", "major", 1, "close", 4)

        assert chord.inversion == 1

        # First note should be E (moved up an octave)
        bass_note = chord.notes[0]
        assert bass_note.midi_note % 12 == 4  # E

    def test_analyze_chord(self, chord_manager):
        """Test chord analysis from MIDI notes."""
        # C major triad
        c_major_notes = [60, 64, 67]

        analysis = chord_manager.analyze_chord(c_major_notes)

        assert len(analysis) > 0

        best_match = analysis[0]
        assert best_match["root"] == "C"
        assert best_match["chord_type"] == "major"
        assert best_match["confidence"] > 0.8

    def test_analyze_seventh_chord(self, chord_manager):
        """Test analyzing a seventh chord."""
        # Dm7 chord: D F A C
        dm7_notes = [62, 65, 69, 72]

        analysis = chord_manager.analyze_chord(dm7_notes)

        assert len(analysis) > 0

        best_match = analysis[0]
        assert best_match["root"] == "D"
        # Should identify as minor7 or similar
        assert "min" in best_match["chord_type"] or "m7" in best_match.get("symbol", "")

    def test_get_chord_tones_and_extensions(self, chord_manager):
        """Test chord tone analysis."""
        analysis = chord_manager.get_chord_tones_and_extensions("Cmaj7")

        assert analysis["root"].name == "C"
        assert len(analysis["chord_tones"]) >= 3  # At least root, 3rd, 5th

        # Should have available tensions
        assert isinstance(analysis["available_tensions"], list)

    def test_invalid_chord_type(self, chord_manager):
        """Test error handling for invalid chord type."""
        with pytest.raises(ValueError, match="Unknown chord type"):
            chord_manager.build_chord("C", "invalid_chord", 0, "close", 4)

    def test_chord_voicings(self, chord_manager):
        """Test different voicing styles."""
        chord_close = chord_manager.build_chord("C", "major", 0, "close", 4)
        chord_open = chord_manager.build_chord("C", "major", 0, "open", 4)

        # Open voicing should have wider spread
        close_span = chord_close.notes[-1].midi_note - chord_close.notes[0].midi_note
        open_span = chord_open.notes[-1].midi_note - chord_open.notes[0].midi_note

        assert open_span >= close_span

    def test_chord_symbol_generation(self, chord_manager):
        """Test chord symbol generation."""
        c_major = chord_manager.build_chord("C", "major", 0, "close", 4)
        assert c_major.symbol == "C"

        c_minor = chord_manager.build_chord("C", "minor", 0, "close", 4)
        assert c_minor.symbol == "Cm"

        c_dom7 = chord_manager.build_chord("C", "7", 0, "close", 4)
        assert c_dom7.symbol == "C7"

    def test_diminished_chord(self, chord_manager):
        """Test building diminished chords."""
        chord = chord_manager.build_chord("B", "diminished", 0, "close", 4)

        assert chord.root.name == "B"
        assert chord.quality == Quality.DIMINISHED

        # B diminished: B D F
        expected_intervals = [0, 3, 6]  # Root, minor 3rd, diminished 5th
        actual_intervals = [(note.midi_note - chord.root.midi_note) % 12 for note in chord.notes[:3]]
        assert actual_intervals == expected_intervals

    def test_augmented_chord(self, chord_manager):
        """Test building augmented chords."""
        chord = chord_manager.build_chord("C", "augmented", 0, "close", 4)

        assert chord.root.name == "C"
        assert chord.quality == Quality.AUGMENTED

        # C augmented: C E G#
        expected_intervals = [0, 4, 8]  # Root, major 3rd, augmented 5th
        actual_intervals = [(note.midi_note - chord.root.midi_note) % 12 for note in chord.notes[:3]]
        assert actual_intervals == expected_intervals

    def test_suspend_chords(self, chord_manager):
        """Test suspended chords."""
        csus4 = chord_manager.build_chord("C", "sus4", 0, "close", 4)

        # C sus4: C F G (no 3rd)
        expected_intervals = [0, 5, 7]
        actual_intervals = [(note.midi_note - csus4.root.midi_note) % 12 for note in csus4.notes[:3]]
        assert actual_intervals == expected_intervals

    def test_chord_suggestions(self, chord_manager):
        """Test chord substitution suggestions."""
        c_major = chord_manager.build_chord("C", "major", 0, "close", 4)

        suggestions = chord_manager.suggest_chord_substitutions(c_major, "jazz")

        # Should return some suggestions for jazz context
        assert isinstance(suggestions, list)

    def test_generate_chord_voicing(self, chord_manager):
        """Test generating specific voicings."""
        chord = chord_manager.build_chord("F", "maj7", 0, "close", 4)

        # Generate voicing in specific range
        voicing = chord_manager.generate_chord_voicing(
            chord, target_range=(48, 72), voice_count=4  # Bass clef to treble clef
        )

        assert len(voicing) <= 4
        assert all(48 <= note.midi_note <= 72 for note in voicing)
