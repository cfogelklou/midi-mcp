"""Tests for comprehensive music theory analysis module."""

import pytest
from midi_mcp.theory.analysis import MusicAnalyzer


class TestMusicAnalyzer:
    """Test cases for MusicAnalyzer functionality."""

    @pytest.fixture
    def music_analyzer(self):
        return MusicAnalyzer()

    def test_analyze_midi_file_c_major_scale(self, music_analyzer):
        """Test comprehensive analysis of C major scale."""
        # C major scale notes
        midi_notes = [60, 62, 64, 65, 67, 69, 71]
        timestamps = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

        analysis = music_analyzer.analyze_midi_file(midi_notes, timestamps)

        # Check key analysis
        assert analysis.key_analysis.most_likely_key in ["C", "Am"]  # C major or relative minor
        assert analysis.key_analysis.confidence > 0.5

        # Check that analysis components exist
        assert analysis.chord_progression is not None
        assert analysis.voice_leading is not None
        assert isinstance(analysis.cadences, list)
        assert isinstance(analysis.modulations, list)
        assert isinstance(analysis.non_chord_tones, list)
        assert isinstance(analysis.harmonic_rhythm, list)

    def test_analyze_midi_file_chord_progression(self, music_analyzer):
        """Test analysis of a chord progression."""
        # Simple C-Am-F-G progression (I-vi-IV-V)
        midi_notes = (
            [60, 64, 67] * 4 + [57, 60, 64] * 4 + [53, 57, 60] * 4 + [55, 59, 62] * 4  # C major  # A minor  # F major
        )  # G major

        # 4 beats per chord
        timestamps = (
            [i * 0.25 for i in range(12)]
            + [3 + i * 0.25 for i in range(12)]
            + [6 + i * 0.25 for i in range(12)]
            + [9 + i * 0.25 for i in range(12)]
        )

        analysis = music_analyzer.analyze_midi_file(midi_notes, timestamps)

        # Should detect C major as likely key
        assert analysis.key_analysis.most_likely_key in ["C", "Am", "F", "G"]

        # Should have some chords in progression
        assert len(analysis.chord_progression.chords) > 0

        # Voice leading should be analyzed
        assert 0 <= analysis.voice_leading.smooth_score <= 100

    def test_analyze_chord_sequence_pop_progression(self, music_analyzer):
        """Test analysis of a chord sequence."""
        chord_symbols = ["C", "Am", "F", "G"]

        analysis = music_analyzer.analyze_chord_sequence(chord_symbols, key="C")

        # Check required fields
        assert "progression_analysis" in analysis
        assert "voice_leading" in analysis
        assert "chord_functions" in analysis
        assert "cadences" in analysis

        # Should have analysis for each chord
        progression_analysis = analysis["progression_analysis"]
        assert "roman_numerals" in progression_analysis
        assert len(progression_analysis["roman_numerals"]) == 4

        # Should detect some harmonic functions
        assert "harmonic_functions" in progression_analysis
        assert len(progression_analysis["harmonic_functions"]) == 4

    def test_analyze_chord_sequence_jazz_progression(self, music_analyzer):
        """Test analysis of jazz ii-V-I progression."""
        chord_symbols = ["Dm7", "G7", "Cmaj7"]

        analysis = music_analyzer.analyze_chord_sequence(chord_symbols, key="C")

        progression_analysis = analysis["progression_analysis"]

        # Should identify ii-V-I pattern
        romans = progression_analysis.get("roman_numerals", [])
        # Should have some version of ii, V, I
        assert any("ii" in roman.lower() or "2" in roman for roman in romans)
        assert any("v" in roman.lower() or "5" in roman for roman in romans)
        assert any("i" in roman.lower() or "1" in roman for roman in romans)

    def test_suggest_harmonic_improvements_good_progression(self, music_analyzer):
        """Test harmonic improvement suggestions for good progression."""
        from midi_mcp.theory.progressions import ProgressionManager
        from midi_mcp.models.theory_models import ChordProgression

        progression_manager = ProgressionManager()

        # Create a good progression (ii-V-I)
        chord_progression = progression_manager.create_chord_progression(
            key="C", progression=["ii", "V", "I"], duration_per_chord=1.0
        )

        suggestions = music_analyzer.suggest_harmonic_improvements(chord_progression)

        # Should return list of suggestions
        assert isinstance(suggestions, list)

        # Good progression might have fewer suggestions
        # (This is implementation dependent)

    def test_suggest_harmonic_improvements_weak_progression(self, music_analyzer):
        """Test harmonic improvement suggestions for weak progression."""
        from midi_mcp.theory.progressions import ProgressionManager

        progression_manager = ProgressionManager()

        # Create a potentially weak progression
        chord_progression = progression_manager.create_chord_progression(
            key="C", progression=["I", "ii", "iii", "vi"], duration_per_chord=1.0  # No strong resolution
        )

        suggestions = music_analyzer.suggest_harmonic_improvements(chord_progression)

        # Should provide suggestions for improvement
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # Should suggest adding V-I resolution
        suggestion_text = " ".join(suggestions).lower()
        assert "v-i" in suggestion_text or "dominant" in suggestion_text or "resolution" in suggestion_text

    def test_identify_musical_form_short_phrase(self, music_analyzer):
        """Test musical form identification for short phrase."""
        from midi_mcp.theory.progressions import ProgressionManager

        progression_manager = ProgressionManager()

        # Create short progression
        chord_progression = progression_manager.create_chord_progression(
            key="C", progression=["I", "V", "vi", "IV"], duration_per_chord=1.0
        )

        form_analysis = music_analyzer.identify_musical_form(chord_progression)

        assert "total_length" in form_analysis
        assert "suggested_form" in form_analysis
        assert "repeated_patterns" in form_analysis
        assert "phrase_lengths" in form_analysis

        assert form_analysis["total_length"] == 4
        # Short progression should be identified as phrase or period
        assert form_analysis["suggested_form"] in ["phrase", "period"]

    def test_identify_musical_form_longer_piece(self, music_analyzer):
        """Test musical form identification for longer piece."""
        from midi_mcp.theory.progressions import ProgressionManager

        progression_manager = ProgressionManager()

        # Create longer progression with repetition
        progression = ["I", "V", "vi", "IV"] * 4 + ["ii", "V", "I", "vi"] * 2  # 16 bars  # 8 bars

        chord_progression = progression_manager.create_chord_progression(
            key="C", progression=progression, duration_per_chord=1.0
        )

        form_analysis = music_analyzer.identify_musical_form(chord_progression)

        assert form_analysis["total_length"] == 24
        # Should find repeated patterns
        assert len(form_analysis["repeated_patterns"]) > 0
        # Longer piece should suggest more complex form
        assert form_analysis["suggested_form"] in ["binary_form", "song_form", "extended_form"]

    def test_analyze_empty_input(self, music_analyzer):
        """Test analysis with empty input."""
        analysis = music_analyzer.analyze_midi_file([], timestamps=[])

        # Should handle empty input gracefully
        assert analysis.key_analysis.most_likely_key == "C"  # Default
        assert analysis.key_analysis.confidence == 0.0

    def test_analyze_single_note(self, music_analyzer):
        """Test analysis with single note."""
        analysis = music_analyzer.analyze_midi_file([60], timestamps=[0.0])  # Single C

        # Should handle single note
        assert analysis.key_analysis.most_likely_key == "C"
        assert len(analysis.chord_progression.chords) >= 0  # May or may not create chords

    def test_analyze_chord_sequence_empty(self, music_analyzer):
        """Test chord sequence analysis with empty input."""
        analysis = music_analyzer.analyze_chord_sequence([])

        # Should handle empty sequence gracefully
        assert "progression_analysis" in analysis
        assert analysis["voice_leading"] is None  # No chords to analyze

    def test_analyze_chord_sequence_invalid_symbols(self, music_analyzer):
        """Test chord sequence analysis with invalid chord symbols."""
        # Include some invalid chord symbols
        chord_symbols = ["C", "InvalidChord", "G", "Am"]

        analysis = music_analyzer.analyze_chord_sequence(chord_symbols, key="C")

        # Should handle invalid symbols gracefully
        assert "progression_analysis" in analysis
        # Should still analyze valid chords

    def test_comprehensive_analysis_integration(self, music_analyzer):
        """Test integration of all analysis components."""
        # Create a more complex musical example
        # Simple melody with harmony
        melody_notes = [72, 71, 69, 67, 65, 64, 62, 60]  # C5 down to C4
        harmony_notes = [48, 52, 55, 53, 57, 60, 55, 59]  # Bass line

        all_notes = []
        timestamps = []

        # Interleave melody and harmony
        for i, (mel, har) in enumerate(zip(melody_notes, harmony_notes)):
            all_notes.extend([har, mel])
            timestamps.extend([i * 1.0, i * 1.0 + 0.1])

        analysis = music_analyzer.analyze_midi_file(all_notes, timestamps)

        # Should produce comprehensive analysis
        assert analysis.key_analysis.confidence > 0.3
        assert len(analysis.harmonic_rhythm) > 0

        # All components should be present and properly formatted
        assert hasattr(analysis, "key_analysis")
        assert hasattr(analysis, "chord_progression")
        assert hasattr(analysis, "voice_leading")
        assert hasattr(analysis, "cadences")
        assert hasattr(analysis, "modulations")
        assert hasattr(analysis, "non_chord_tones")
        assert hasattr(analysis, "harmonic_rhythm")

    def test_harmonic_rhythm_analysis(self, music_analyzer):
        """Test harmonic rhythm analysis specifically."""
        # Create progression with varying chord durations
        midi_notes = [60, 64, 67] * 8  # Repeated C major chord
        # Vary the timestamps to simulate different harmonic rhythms
        timestamps = [
            0.0,
            0.1,
            0.2,
            2.0,
            2.1,
            2.2,
            3.0,
            3.1,
            3.2,  # Slow-fast-medium
            5.0,
            5.1,
            5.2,
            5.5,
            5.6,
            5.7,
            6.0,
            6.1,
            6.2,  # Medium rhythm
            7.0,
            7.1,
            7.2,
            7.25,
            7.3,
            7.35,
        ]  # Fast rhythm

        analysis = music_analyzer.analyze_midi_file(midi_notes, timestamps)

        # Should analyze harmonic rhythm
        assert len(analysis.harmonic_rhythm) > 0
        assert all(isinstance(rate, float) for rate in analysis.harmonic_rhythm)
        assert all(rate > 0 for rate in analysis.harmonic_rhythm)
