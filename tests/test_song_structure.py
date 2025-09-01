# -*- coding: utf-8 -*-
"""
Unit tests for song structure and form generation.
"""

import pytest
from typing import Dict, List, Any

from midi_mcp.composition.song_structure import SongStructureGenerator, SectionGenerator, TransitionCreator
from midi_mcp.models.composition_models import SongStructure, Section, Transition


class TestSongStructureGenerator:
    """Test song structure generation."""

    def test_create_pop_structure(self):
        """Test creating a pop song structure."""
        generator = SongStructureGenerator()
        structure = generator.create_structure(genre="pop", song_type="standard", duration=180)

        assert isinstance(structure, SongStructure)
        assert structure.genre == "pop"
        assert len(structure.sections) >= 5

        # Check for essential pop sections
        section_types = [s.type.value for s in structure.sections]
        assert "verse" in section_types
        assert "chorus" in section_types

    def test_create_blues_structure(self):
        """Test creating a blues song structure."""
        generator = SongStructureGenerator()
        structure = generator.create_structure(genre="blues", song_type="12_bar", duration=240)

        assert structure.genre == "blues"
        # Blues should have specific structural elements
        assert len(structure.sections) >= 4  # Should have multiple sections


class TestSectionGenerator:
    """Test individual section generation."""

    @pytest.mark.skip(reason="Verse section melody generation not fully implemented")
    def test_generate_verse_section(self):
        """Test verse section generation."""
        generator = SectionGenerator()
        section = generator.generate_section(section_type="verse", genre="pop", key="C major")

        assert isinstance(section, Section)
        assert section.type.value == "verse"
        assert section.key == "C major"
        assert section.melody is not None
        assert section.harmony is not None

    def test_generate_chorus_section(self):
        """Test chorus section generation."""
        generator = SectionGenerator()
        section = generator.generate_section(section_type="chorus", genre="rock", key="E major")

        assert section.type.value == "chorus"
        # Chorus should typically be more energetic
        assert section.energy_level > 0.6


class TestTransitionCreator:
    """Test section transition creation."""

    def test_create_smooth_transition(self):
        """Test smooth transition creation."""
        generator = SectionGenerator()
        verse = generator.generate_section("verse", "pop", "C major")
        chorus = generator.generate_section("chorus", "pop", "C major")

        creator = TransitionCreator()
        transition = creator.create_transition(from_section=verse, to_section=chorus, transition_type="smooth")

        assert isinstance(transition, Transition)
        assert transition.type == "smooth"
        assert transition.duration > 0
