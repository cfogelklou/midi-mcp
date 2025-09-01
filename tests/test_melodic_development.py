# -*- coding: utf-8 -*-
"""
Unit tests for melodic development and variation.
"""

import pytest
from typing import List

from midi_mcp.composition.melodic_development import MotifDeveloper, PhraseGenerator, MelodyVariator
from midi_mcp.models.composition_models import Motif, Phrase, MelodyVariation


class TestMotifDeveloper:
    """Test melodic motif development."""

    def test_sequence_development(self):
        """Test sequence development technique."""
        developer = MotifDeveloper()
        motif = Motif(notes=[60, 62, 64, 65])

        developed = developer.develop_motif(motif=motif, techniques=["sequence"], target_length=8)

        assert len(developed.melody.notes) >= 8
        assert "sequence" in [t.name for t in developed.techniques_applied]

    def test_inversion_development(self):
        """Test inversion development technique."""
        developer = MotifDeveloper()
        motif = Motif(notes=[60, 64, 62, 65])  # C-E-D-F

        developed = developer.develop_motif(motif=motif, techniques=["inversion"], target_length=4)

        # Check that inversion was applied
        original_intervals = [64 - 60, 62 - 64, 65 - 62]  # [4, -2, 3]
        assert any("inversion" in t.name for t in developed.techniques_applied)

    def test_retrograde_development(self):
        """Test retrograde development technique."""
        developer = MotifDeveloper()
        motif = Motif(notes=[60, 62, 64, 67])

        developed = developer.develop_motif(motif=motif, techniques=["retrograde"], target_length=8)

        # Should contain both original and retrograde
        notes = developed.melody.notes
        assert 67 in notes and 60 in notes
        assert any("retrograde" in t.name for t in developed.techniques_applied)


class TestPhraseGenerator:
    """Test melodic phrase generation."""

    def test_period_phrase(self):
        """Test period phrase structure generation."""
        generator = PhraseGenerator()
        phrase = generator.create_phrase(
            chord_progression=["C", "Am", "F", "G"], key="C major", phrase_type="period", style="vocal"
        )

        assert isinstance(phrase, Phrase)
        assert phrase.structure_type == "period"
        assert len(phrase.melody.notes) > 0

        # Period should have clear antecedent/consequent
        assert "antecedent" in phrase.structure_analysis
        assert "consequent" in phrase.structure_analysis

    def test_sentence_phrase(self):
        """Test sentence phrase structure generation."""
        generator = PhraseGenerator()
        phrase = generator.create_phrase(
            chord_progression=["C", "F", "G", "C"], key="C major", phrase_type="sentence", style="instrumental"
        )

        assert phrase.structure_type == "sentence"
        # Sentence should have presentation/continuation
        assert "presentation" in phrase.structure_analysis
        assert "continuation" in phrase.structure_analysis

    def test_vocal_style_constraints(self):
        """Test vocal style melodic constraints."""
        generator = PhraseGenerator()
        phrase = generator.create_phrase(
            chord_progression=["C", "G", "Am", "F"], key="C major", phrase_type="period", style="vocal"
        )

        # Check for vocal-friendly intervals
        notes = phrase.melody.notes
        intervals = [notes[i + 1] - notes[i] for i in range(len(notes) - 1)]
        large_leaps = [abs(i) for i in intervals if abs(i) > 4]

        # Vocal melodies should have few large leaps
        assert len(large_leaps) / len(intervals) < 0.3


class TestMelodyVariator:
    """Test melody variation techniques."""

    def test_embellishment_variation(self):
        """Test embellishment variation."""
        variator = MelodyVariator()
        original = [60, 62, 64, 67, 65, 64, 62, 60]

        variation = variator.create_variation(original_melody=original, variation_type="embellishment")

        assert isinstance(variation, MelodyVariation)
        assert len(variation.varied_melody.notes) >= len(original)
        assert variation.similarity_score >= 0.6

    def test_rhythmic_variation(self):
        """Test rhythmic variation."""
        variator = MelodyVariator()
        original = [60, 62, 64, 67]

        variation = variator.create_variation(original_melody=original, variation_type="rhythmic")

        # Should maintain pitch content but vary rhythm
        original_pitches = set(original)
        varied_pitches = set(variation.varied_melody.notes)
        assert len(original_pitches.intersection(varied_pitches)) > 0

    def test_modal_variation(self):
        """Test modal variation."""
        variator = MelodyVariator()
        original = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale

        variation = variator.create_variation(original_melody=original, variation_type="modal")

        # Should change some pitches to create modal flavor
        assert variation.varied_melody.notes != original
        assert variation.similarity_score >= 0.5
