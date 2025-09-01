# -*- coding: utf-8 -*-
"""
Unit tests for complete composition generation and analysis.
"""

import pytest
from typing import Dict, List, Any

from midi_mcp.composition.composer import CompleteComposer
from midi_mcp.composition.analyzer import CompositionAnalyzer
from midi_mcp.composition.refinement import CompositionRefiner
from midi_mcp.models.composition_models import CompleteComposition, CompositionAnalysis, RefinementResult


class TestCompleteComposer:
    """Test complete composition generation."""

    def test_compose_pop_ballad(self):
        """Test complete pop ballad composition."""
        composer = CompleteComposer()

        composition = composer.compose_complete_song(
            description="a heartfelt ballad about lost love",
            genre="pop_ballad",
            key="F major",
            tempo=72,
            target_duration=240,
        )

        assert isinstance(composition, CompleteComposition)
        assert composition.genre == "pop_ballad"
        assert composition.key == "F major"
        assert composition.tempo == 72

        # Should have ballad characteristics
        assert composition.overall_energy < 0.5  # Ballads are typically low energy
        assert "emotional" in composition.style_characteristics

        # Should have complete structure
        assert len(composition.structure.sections) >= 5
        section_types = [s.type for s in composition.structure.sections]
        assert "verse" in section_types
        assert "chorus" in section_types

        # Duration should be close to target
        total_duration = sum(s.duration for s in composition.structure.sections)
        assert 230 <= total_duration <= 250

    def test_compose_blues_rock(self):
        """Test complete blues-rock composition."""
        composer = CompleteComposer()

        composition = composer.compose_complete_song(
            description="a driving song about freedom with a memorable chorus",
            genre="blues_rock",
            key="E major",
            tempo=120,
            target_duration=180,
        )

        assert composition.genre == "blues_rock"
        assert composition.key == "E major"
        assert composition.tempo == 120

        # Should have blues-rock characteristics
        assert composition.overall_energy > 0.6  # Should be driving
        assert any("blues" in char for char in composition.style_characteristics)
        assert any("rock" in char for char in composition.style_characteristics)

        # Should have memorable chorus
        choruses = [s for s in composition.structure.sections if s.type == "chorus"]
        assert len(choruses) >= 2  # Multiple choruses for memorability

        # Chorus should be more energetic than verses
        verses = [s for s in composition.structure.sections if s.type == "verse"]
        if verses and choruses:
            assert choruses[0].energy_level > verses[0].energy_level

    def test_compose_jazz_standard(self):
        """Test complete jazz standard composition."""
        composer = CompleteComposer()

        composition = composer.compose_complete_song(
            description="a sophisticated jazz standard with complex harmony",
            genre="jazz",
            key="Bb major",
            tempo=100,
            target_duration=200,
        )

        assert composition.genre == "jazz"

        # Should have jazz characteristics
        assert "sophisticated" in composition.description.lower()
        assert any("jazz" in char for char in composition.style_characteristics)

        # Should have complex harmony
        harmony_complexity = composition.harmonic_complexity_score
        assert harmony_complexity >= 0.7  # Jazz should be harmonically complex

        # Should follow jazz standard form (AABA typical)
        section_pattern = [s.type for s in composition.structure.sections]
        # Check for repeated A sections
        a_sections = [s for s in section_pattern if s == "A"]
        assert len(a_sections) >= 2


class TestCompositionAnalyzer:
    """Test composition quality analysis."""

    def test_analyze_melodic_quality(self):
        """Test melodic quality analysis."""
        analyzer = CompositionAnalyzer()

        composition = CompleteComposition(
            melody={
                "notes": [60, 62, 64, 67, 65, 64, 62, 60],  # Well-shaped melody
                "rhythm": [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0],
            },
            harmony=[
                {"chord": "C", "duration": 2},
                {"chord": "Am", "duration": 2},
                {"chord": "F", "duration": 2},
                {"chord": "G", "duration": 2},
            ],
            key="C major",
        )

        analysis = analyzer.analyze_composition_quality(composition)

        assert isinstance(analysis, CompositionAnalysis)

        # Should analyze melody
        assert "melody" in analysis.category_scores
        melody_analysis = analysis.category_scores["melody"]
        assert 0 <= melody_analysis.score <= 10

        # Should identify melodic strengths/weaknesses
        assert "contour" in melody_analysis.analysis_details
        assert "phrase_structure" in melody_analysis.analysis_details

    def test_analyze_harmonic_quality(self):
        """Test harmonic quality analysis."""
        analyzer = CompositionAnalyzer()

        # Create composition with poor voice leading
        composition = CompleteComposition(
            melody={"notes": [60, 62, 64, 65]},
            harmony=[
                {"chord": "C", "voicing": [48, 60, 64, 67], "duration": 2},
                {"chord": "F", "voicing": [41, 65, 69, 72], "duration": 2},  # Big jumps
            ],
            key="C major",
        )

        analysis = analyzer.analyze_composition_quality(composition)

        # Should identify voice leading issues
        harmony_analysis = analysis.category_scores["harmony"]
        assert "voice_leading" in harmony_analysis.analysis_details

        # Should suggest improvements
        vl_suggestions = [s for s in analysis.improvement_suggestions if "voice leading" in s.suggestion.lower()]
        assert len(vl_suggestions) > 0

    def test_analyze_structural_quality(self):
        """Test structural quality analysis."""
        analyzer = CompositionAnalyzer()

        # Create composition with poor structure
        composition = CompleteComposition(
            structure={
                "sections": [
                    {"type": "verse", "duration": 120},  # Way too long verse
                    {"type": "outro", "duration": 10},  # Abrupt ending
                ]
            }
        )

        analysis = analyzer.analyze_composition_quality(composition)

        # Should identify structural issues
        form_analysis = analysis.category_scores["form"]
        assert "proportions" in form_analysis.analysis_details

        # Should suggest structural improvements
        structure_suggestions = [
            s
            for s in analysis.improvement_suggestions
            if "structure" in s.suggestion.lower() or "section" in s.suggestion.lower()
        ]
        assert len(structure_suggestions) > 0

    def test_overall_quality_scoring(self):
        """Test overall quality scoring."""
        analyzer = CompositionAnalyzer()

        # Create well-balanced composition
        composition = CompleteComposition(
            melody={"notes": [60, 62, 64, 67, 65, 64, 62, 60]},
            harmony=[{"chord": "C", "duration": 4}, {"chord": "G", "duration": 4}],
            structure={
                "sections": [
                    {"type": "verse", "duration": 30},
                    {"type": "chorus", "duration": 30},
                    {"type": "verse", "duration": 30},
                    {"type": "chorus", "duration": 30},
                ]
            },
            key="C major",
            tempo=120,
        )

        analysis = analyzer.analyze_composition_quality(composition)

        # Should have overall score
        assert "overall" in analysis.category_scores
        overall_score = analysis.category_scores["overall"].score
        assert 0 <= overall_score <= 10

        # Overall score should relate to category scores
        category_avg = (
            sum(cat.score for cat in analysis.category_scores.values() if cat != analysis.category_scores["overall"])
            / 4
        )
        assert abs(overall_score - category_avg) < 2.0


class TestCompositionRefiner:
    """Test composition refinement capabilities."""

    def test_refine_melody(self):
        """Test melody refinement."""
        refiner = CompositionRefiner()

        # Create composition with boring melody
        composition = CompleteComposition(
            melody={"notes": [60, 60, 60, 60, 60, 60, 60, 60]},  # All same note
            harmony=[{"chord": "C", "duration": 8}],
            key="C major",
        )

        refined = refiner.refine_composition(composition=composition, focus_areas=["melody"])

        assert isinstance(refined, RefinementResult)

        # Melody should be more varied
        original_variety = len(set(composition.melody["notes"]))
        refined_variety = len(set(refined.refined_composition.melody["notes"]))
        assert refined_variety > original_variety

        # Should document changes
        melody_changes = [c for c in refined.changes_made if c.category == "melody"]
        assert len(melody_changes) > 0

    def test_refine_harmony(self):
        """Test harmony refinement."""
        refiner = CompositionRefiner()

        # Create composition with static harmony
        composition = CompleteComposition(
            melody={"notes": [60, 62, 64, 65, 67, 69, 71, 72]},
            harmony=[{"chord": "C", "duration": 16}],  # One chord for everything
            key="C major",
        )

        refined = refiner.refine_composition(composition=composition, focus_areas=["harmony"])

        # Should add more chords
        original_chord_count = len(composition.harmony)
        refined_chord_count = len(refined.refined_composition.harmony)
        assert refined_chord_count > original_chord_count

        # Should document harmony changes
        harmony_changes = [c for c in refined.changes_made if c.category == "harmony"]
        assert len(harmony_changes) > 0

    def test_refine_form(self):
        """Test form refinement."""
        refiner = CompositionRefiner()

        # Create composition with poor form
        composition = CompleteComposition(
            structure={"sections": [{"type": "verse", "duration": 200}]}  # One giant section
        )

        refined = refiner.refine_composition(composition=composition, focus_areas=["form"])

        # Should break into multiple sections
        original_section_count = len(composition.structure["sections"])
        refined_section_count = len(refined.refined_composition.structure["sections"])
        assert refined_section_count > original_section_count

        # Should document structural changes
        form_changes = [c for c in refined.changes_made if c.category == "form"]
        assert len(form_changes) > 0

    def test_comprehensive_refinement(self):
        """Test comprehensive refinement of multiple areas."""
        refiner = CompositionRefiner()

        # Create composition needing work in multiple areas
        composition = CompleteComposition(
            melody={"notes": [60, 60, 60, 60]},  # Boring melody
            harmony=[{"chord": "C", "duration": 8}],  # Static harmony
            structure={"sections": [{"type": "verse", "duration": 120}]},  # Poor form
            key="C major",
        )

        refined = refiner.refine_composition(composition=composition, focus_areas=["melody", "harmony", "form"])

        # Should improve all areas
        changes_by_category = {}
        for change in refined.changes_made:
            if change.category not in changes_by_category:
                changes_by_category[change.category] = 0
            changes_by_category[change.category] += 1

        # Should have changes in all requested areas
        assert "melody" in changes_by_category
        assert "harmony" in changes_by_category
        assert "form" in changes_by_category

        # Should maintain overall coherence
        assert refined.coherence_maintained == True
        assert refined.style_consistency_score >= 0.7
