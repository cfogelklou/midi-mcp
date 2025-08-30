"""Tests for music theory progressions module."""

import pytest
from src.midi_mcp.theory.progressions import ProgressionManager
from src.midi_mcp.theory.chords import ChordManager
from src.midi_mcp.models.theory_models import ChordProgression

class TestProgressionManager:
    """Test cases for ProgressionManager functionality."""
    
    @pytest.fixture
    def progression_manager(self):
        return ProgressionManager()
    
    @pytest.fixture
    def chord_manager(self):
        return ChordManager()
    
    def test_create_chord_progression_major(self, progression_manager):
        """Test creating a chord progression in C major."""
        progression = progression_manager.create_chord_progression(
            key="C",
            progression=["I", "vi", "ii", "V"],
            duration_per_chord=1.0
        )
        
        assert progression.key == "C"
        assert progression.roman_numerals == ["I", "vi", "ii", "V"]
        assert len(progression.chords) == 4
        assert progression.get_total_duration() == 4.0
        
        # Check chord roots (approximately)
        chord_roots = [chord.root.name for chord in progression.chords]
        # Should be approximately C, A, D, G for I vi ii V in C major
        expected_roots = ["C", "A", "D", "G"]
        assert chord_roots == expected_roots
    
    def test_create_chord_progression_minor(self, progression_manager):
        """Test creating a chord progression in A minor."""
        progression = progression_manager.create_chord_progression(
            key="Am",
            progression=["i", "iv", "V", "i"],
            duration_per_chord=2.0
        )
        
        assert progression.key == "Am"
        assert progression.roman_numerals == ["i", "iv", "V", "i"]
        assert progression.get_total_duration() == 8.0
        
        # Check that we get minor chords where expected
        chord_roots = [chord.root.name for chord in progression.chords]
        expected_roots = ["A", "D", "E", "A"]
        assert chord_roots == expected_roots
    
    def test_analyze_progression(self, progression_manager):
        """Test analyzing a chord progression."""
        chord_symbols = ["C", "Am", "F", "G"]
        
        analysis = progression_manager.analyze_progression(chord_symbols)
        
        assert 'detected_key' in analysis
        assert 'roman_numerals' in analysis
        assert 'harmonic_functions' in analysis
        assert 'cadences' in analysis
        
        # Should detect C major or related key
        assert analysis['detected_key'] in ['C', 'Am', 'F', 'G']
        
        # Should have roman numerals for each chord
        assert len(analysis['roman_numerals']) == 4
    
    def test_analyze_progression_with_key(self, progression_manager):
        """Test analyzing progression with specified key."""
        chord_symbols = ["Dm", "G7", "C", "Am"]
        
        analysis = progression_manager.analyze_progression(chord_symbols, key="C")
        
        assert analysis['detected_key'] == "C"
        
        # In C major: Dm=ii, G7=V7, C=I, Am=vi
        romans = analysis['roman_numerals']
        assert 'ii' in romans or 'II' in romans
        assert 'V' in romans or 'v' in romans
        assert 'I' in romans or 'i' in romans
        assert 'vi' in romans or 'VI' in romans
    
    def test_suggest_next_chord(self, progression_manager):
        """Test chord suggestion functionality."""
        suggestions = progression_manager.suggest_next_chord(
            current_progression=["I", "vi"],
            key="C",
            style="pop"
        )
        
        assert 'suggestions' in suggestions
        assert len(suggestions['suggestions']) > 0
        
        # Each suggestion should have required fields
        for suggestion in suggestions['suggestions']:
            assert 'chord' in suggestion
            assert 'probability' in suggestion
            assert 'reason' in suggestion
            assert 0 <= suggestion['probability'] <= 1
    
    def test_suggest_next_chord_jazz(self, progression_manager):
        """Test jazz-style chord suggestions."""
        suggestions = progression_manager.suggest_next_chord(
            current_progression=["ii", "V"],
            key="C",
            style="jazz"
        )
        
        assert 'suggestions' in suggestions
        
        # After ii-V, should strongly suggest I
        chord_suggestions = [s['chord'] for s in suggestions['suggestions']]
        assert 'I' in chord_suggestions
        
        # I should have high probability after ii-V
        i_suggestion = next(s for s in suggestions['suggestions'] if s['chord'] == 'I')
        assert i_suggestion['probability'] > 0.4
    
    def test_get_common_progressions(self, progression_manager):
        """Test getting common progressions."""
        all_progressions = progression_manager.get_common_progressions()
        
        assert 'classical' in all_progressions
        assert 'jazz' in all_progressions
        assert 'pop' in all_progressions
        assert 'blues' in all_progressions
        
        # Check specific progressions exist
        assert 'ii_V_I' in all_progressions['jazz']
        assert 'vi_IV_I_V' in all_progressions['pop']
        assert 'twelve_bar_blues' in all_progressions['blues']
    
    def test_get_common_progressions_filtered(self, progression_manager):
        """Test getting progressions filtered by style."""
        jazz_progressions = progression_manager.get_common_progressions("jazz")
        
        assert 'jazz' in jazz_progressions
        assert len(jazz_progressions) == 1  # Only jazz
        assert 'ii_V_I' in jazz_progressions['jazz']
    
    def test_transpose_progression(self, progression_manager):
        """Test transposing a chord progression."""
        # Create progression in C major
        original = progression_manager.create_chord_progression(
            key="C",
            progression=["I", "V", "vi", "IV"],
            duration_per_chord=1.0
        )
        
        # Transpose to G major
        transposed = progression_manager.transpose_progression(original, "G")
        
        assert transposed.key == "G"
        assert transposed.roman_numerals == original.roman_numerals
        assert len(transposed.chords) == len(original.chords)
        
        # Check that chord roots are transposed correctly
        # C major I-V-vi-IV = C-G-Am-F
        # G major I-V-vi-IV = G-D-Em-C
        original_roots = [chord.root.name for chord in original.chords]
        transposed_roots = [chord.root.name for chord in transposed.chords]
        
        # Roots should be different (transposed)
        assert original_roots != transposed_roots
        
        # But intervals between roots should be preserved
        def get_intervals(roots):
            from src.midi_mcp.theory.constants import NOTE_NAMES
            indices = [NOTE_NAMES.index(root) for root in roots]
            intervals = []
            for i in range(len(indices) - 1):
                intervals.append((indices[i+1] - indices[i]) % 12)
            return intervals
        
        original_intervals = get_intervals(original_roots)
        transposed_intervals = get_intervals(transposed_roots)
        assert original_intervals == transposed_intervals
    
    def test_validate_progression(self, progression_manager):
        """Test progression validation."""
        # Test a good progression
        good_progression = ["I", "vi", "ii", "V", "I"]
        validation = progression_manager.validate_progression(good_progression, "C")
        
        assert 'score' in validation
        assert 'issues' in validation
        assert 'is_valid' in validation
        assert 'suggestions' in validation
        
        assert validation['is_valid'] == True
        assert validation['score'] > 80  # Should score well
    
    def test_validate_problematic_progression(self, progression_manager):
        """Test validation of problematic progression."""
        # Test a progression with potential issues
        problematic = ["I", "ii", "iii", "vi", "vii"]  # Weak progressions
        validation = progression_manager.validate_progression(problematic, "C")
        
        # May have lower score due to weak progressions
        assert validation['score'] >= 0
        assert isinstance(validation['issues'], list)
        assert isinstance(validation['suggestions'], list)
    
    def test_ii_V_I_progression(self, progression_manager):
        """Test the classic ii-V-I progression."""
        progression = progression_manager.create_chord_progression(
            key="C",
            progression=["ii", "V", "I"],
            duration_per_chord=1.0
        )
        
        # Should create Dm - G - C in C major
        chord_roots = [chord.root.name for chord in progression.chords]
        assert chord_roots == ["D", "G", "C"]
        
        # Validate this should score well
        validation = progression_manager.validate_progression(["ii", "V", "I"], "C")
        assert validation['score'] > 85
    
    def test_blues_progression(self, progression_manager):
        """Test blues progression creation."""
        blues = progression_manager.create_chord_progression(
            key="C",
            progression=["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"],
            duration_per_chord=1.0
        )
        
        assert len(blues.chords) == 12  # 12-bar blues
        assert blues.get_total_duration() == 12.0
        
        # Should have C, F, G chords (I, IV, V in C)
        chord_roots = set(chord.root.name for chord in blues.chords)
        assert chord_roots == {"C", "F", "G"}
    
    def test_analyze_cadences(self, progression_manager):
        """Test cadence identification in analysis."""
        # Progression with clear cadences
        chord_symbols = ["F", "G", "C", "Am", "F", "G", "C"]
        
        analysis = progression_manager.analyze_progression(chord_symbols, key="C")
        
        # Should identify cadences
        cadences = analysis.get('cadences', [])
        assert len(cadences) > 0
        
        # Should find authentic cadences (V-I)
        cadence_types = [cadence['type'] for cadence in cadences]
        assert 'authentic' in cadence_types or 'half' in cadence_types