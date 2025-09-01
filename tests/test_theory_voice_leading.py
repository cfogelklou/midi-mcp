"""Tests for music theory voice leading module."""

import pytest
from midi_mcp.theory.voice_leading import VoiceLeadingManager
from midi_mcp.theory.chords import ChordManager
from midi_mcp.models.theory_models import Note


class TestVoiceLeadingManager:
    """Test cases for VoiceLeadingManager functionality."""

    @pytest.fixture
    def voice_leading_manager(self):
        return VoiceLeadingManager()

    @pytest.fixture
    def chord_manager(self):
        return ChordManager()

    def create_test_progression(self, chord_manager):
        """Create a test chord progression for voice leading analysis."""
        chords = [
            chord_manager.build_chord("C", "major", 0, "close", 4),
            chord_manager.build_chord("F", "major", 0, "close", 4),
            chord_manager.build_chord("G", "major", 0, "close", 4),
            chord_manager.build_chord("C", "major", 0, "close", 4),
        ]
        return chords

    def test_validate_voice_leading_good_progression(self, voice_leading_manager, chord_manager):
        """Test voice leading validation on a good progression."""
        chords = self.create_test_progression(chord_manager)

        analysis = voice_leading_manager.validate_voice_leading(chords)

        assert analysis.smooth_score >= 0
        assert analysis.smooth_score <= 100
        assert isinstance(analysis.problems, list)
        assert isinstance(analysis.suggestions, list)
        assert isinstance(analysis.parallel_motion, list)

    def test_validate_voice_leading_single_chord(self, voice_leading_manager, chord_manager):
        """Test voice leading validation with single chord."""
        chords = [chord_manager.build_chord("C", "major", 0, "close", 4)]

        analysis = voice_leading_manager.validate_voice_leading(chords)

        # Single chord should have perfect score
        assert analysis.smooth_score == 100.0
        assert len(analysis.problems) == 0
        assert len(analysis.parallel_motion) == 0

    def test_validate_voice_leading_empty_progression(self, voice_leading_manager):
        """Test voice leading validation with empty progression."""
        analysis = voice_leading_manager.validate_voice_leading([])

        assert analysis.smooth_score == 100.0
        assert len(analysis.problems) == 0

    def test_check_parallel_motion(self, voice_leading_manager, chord_manager):
        """Test parallel motion detection."""
        chord1 = chord_manager.build_chord("C", "major", 0, "close", 4)
        chord2 = chord_manager.build_chord("D", "major", 0, "close", 4)

        violations = voice_leading_manager.check_parallel_motion(chord1, chord2)

        # May or may not have parallel motion depending on voicing
        assert isinstance(violations, list)

        # Check structure of violations if any exist
        for violation in violations:
            assert "type" in violation
            assert "voice1" in violation
            assert "voice2" in violation
            assert "severity" in violation

    def test_analyze_voice_motion(self, voice_leading_manager, chord_manager):
        """Test voice motion analysis."""
        chord1 = chord_manager.build_chord("C", "major", 0, "close", 4)
        chord2 = chord_manager.build_chord("G", "major", 0, "close", 4)

        analysis = voice_leading_manager.analyze_voice_motion(chord1, chord2)

        assert "voice_motions" in analysis
        assert "motion_summary" in analysis
        assert "total_motion" in analysis
        assert "largest_leap" in analysis

        # Motion summary should have all motion types
        motion_summary = analysis["motion_summary"]
        assert "parallel" in motion_summary
        assert "similar" in motion_summary
        assert "contrary" in motion_summary
        assert "oblique" in motion_summary

    def test_create_four_part_harmony(self, voice_leading_manager, chord_manager):
        """Test four-part harmony creation."""
        # Create melody and chord progression
        melody_notes = [
            Note.from_midi(72),  # C5
            Note.from_midi(71),  # B4
            Note.from_midi(69),  # A4
            Note.from_midi(67),  # G4
        ]

        chord_progression = [
            chord_manager.build_chord("C", "major", 0, "close", 4),
            chord_manager.build_chord("G", "major", 0, "close", 4),
            chord_manager.build_chord("A", "minor", 0, "close", 4),
            chord_manager.build_chord("F", "major", 0, "close", 4),
        ]

        harmony = voice_leading_manager.create_four_part_harmony(melody_notes, chord_progression)

        # Should have four parts
        assert "soprano" in harmony
        assert "alto" in harmony
        assert "tenor" in harmony
        assert "bass" in harmony

        # Each part should have same length as melody
        for part in harmony.values():
            assert len(part) == len(melody_notes)

        # Soprano should match original melody
        assert harmony["soprano"] == melody_notes

        # Test voice ranges (approximately)
        for note in harmony["bass"]:
            assert note.midi_note <= 60  # Bass shouldn't go too high

        for note in harmony["soprano"]:
            assert note.midi_note >= 60  # Soprano shouldn't go too low

    def test_optimize_voice_leading(self, voice_leading_manager, chord_manager):
        """Test voice leading optimization."""
        # Create progression with potentially poor voice leading
        chords = [
            chord_manager.build_chord("C", "major", 0, "close", 4),
            chord_manager.build_chord("F", "major", 0, "close", 5),  # Jump to higher octave
            chord_manager.build_chord("G", "major", 0, "close", 3),  # Jump to lower octave
            chord_manager.build_chord("C", "major", 0, "close", 4),
        ]

        optimized = voice_leading_manager.optimize_voice_leading(chords)

        # Should return same number of chords
        assert len(optimized) == len(chords)

        # First chord should be unchanged
        assert optimized[0] == chords[0]

        # Optimized version should exist
        assert optimized is not None

    def test_voice_leading_with_different_chord_sizes(self, voice_leading_manager, chord_manager):
        """Test voice leading analysis with different chord sizes."""
        # Mix triads and seventh chords
        chords = [
            chord_manager.build_chord("C", "major", 0, "close", 4),  # Triad
            chord_manager.build_chord("F", "maj7", 0, "close", 4),  # Seventh
            chord_manager.build_chord("G", "7", 0, "close", 4),  # Seventh
            chord_manager.build_chord("C", "major", 0, "close", 4),  # Triad
        ]

        analysis = voice_leading_manager.validate_voice_leading(chords)

        # Should handle different chord sizes gracefully
        assert isinstance(analysis.smooth_score, float)
        assert isinstance(analysis.problems, list)

    def test_large_leap_detection(self, voice_leading_manager):
        """Test detection of large leaps in voice leading."""
        # Create chords with large leaps
        chord1_notes = [Note.from_midi(48), Note.from_midi(52), Note.from_midi(55)]  # C3 E3 G3
        chord2_notes = [Note.from_midi(60), Note.from_midi(64), Note.from_midi(79)]  # C4 E4 G5 (large leap)

        from midi_mcp.models.theory_models import Chord, Quality, ChordType

        chord1 = Chord(
            root=Note.from_midi(48), quality=Quality.MAJOR, chord_type=ChordType.TRIAD, notes=chord1_notes, symbol="C"
        )

        chord2 = Chord(
            root=Note.from_midi(60), quality=Quality.MAJOR, chord_type=ChordType.TRIAD, notes=chord2_notes, symbol="C"
        )

        analysis = voice_leading_manager.validate_voice_leading([chord1, chord2])

        # Should detect large leap problems
        large_leap_problems = [p for p in analysis.problems if p.get("type") == "large_leap"]
        assert len(large_leap_problems) > 0

    def test_voice_range_constraints(self, voice_leading_manager, chord_manager):
        """Test voice leading within specific ranges."""
        chord = chord_manager.build_chord("G", "maj7", 0, "close", 4)

        # Generate voicing within piano range
        piano_range = (21, 108)  # A0 to C8
        voicing = voice_leading_manager.optimize_voice_leading([chord], piano_range)

        assert len(voicing) == 1

        # All notes should be within range
        for note in voicing[0].notes:
            assert piano_range[0] <= note.midi_note <= piano_range[1]

    def test_voice_crossing_detection(self, voice_leading_manager, chord_manager):
        """Test detection of voice crossing."""
        # Create chord with voice crossing (bass higher than tenor)
        crossing_notes = [
            Note.from_midi(67),  # G4 (should be bass but too high)
            Note.from_midi(60),  # C4 (should be tenor but lower than "bass")
            Note.from_midi(64),  # E4 (alto)
            Note.from_midi(72),  # C5 (soprano)
        ]

        from midi_mcp.models.theory_models import Chord, Quality, ChordType

        crossing_chord = Chord(
            root=Note.from_midi(60), quality=Quality.MAJOR, chord_type=ChordType.TRIAD, notes=crossing_notes, symbol="C"
        )

        normal_chord = chord_manager.build_chord("F", "major", 0, "close", 4)

        analysis = voice_leading_manager.validate_voice_leading([crossing_chord, normal_chord])

        # Should detect voice crossing
        crossing_problems = [p for p in analysis.problems if p.get("type") == "voice_crossing"]
        assert len(crossing_problems) > 0

    def test_motion_classification(self, voice_leading_manager):
        """Test classification of voice motion types."""
        # Test different motion types
        note1a = Note.from_midi(60)  # C4
        note1b = Note.from_midi(64)  # E4
        note2a = Note.from_midi(62)  # D4 (up by step)
        note2b = Note.from_midi(66)  # F#4 (up by step)

        # This should be similar motion (both up, different intervals)
        motion_type = voice_leading_manager._classify_motion(note1a, note1b, note2a, note2b)
        assert motion_type in ["parallel", "similar"]

        # Test contrary motion
        note2a_contrary = Note.from_midi(58)  # Bb3 (down)
        note2b_contrary = Note.from_midi(67)  # G4 (up)

        motion_type_contrary = voice_leading_manager._classify_motion(note1a, note1b, note2a_contrary, note2b_contrary)
        assert motion_type_contrary == "contrary"

        # Test oblique motion
        note2a_oblique = Note.from_midi(60)  # C4 (stays same)
        note2b_oblique = Note.from_midi(67)  # G4 (moves)

        motion_type_oblique = voice_leading_manager._classify_motion(note1a, note1b, note2a_oblique, note2b_oblique)
        assert motion_type_oblique == "oblique"
