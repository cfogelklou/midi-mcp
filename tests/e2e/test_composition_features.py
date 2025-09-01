# -*- coding: utf-8 -*-
"""
End-to-end tests for Phase 5 composition features.

Tests all composition functionality including song structure, melodic development,
voice leading, arrangement, and complete composition generation.
"""

import pytest
import asyncio
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock

from midi_mcp.core.server import MCPServer
from midi_mcp.config.settings import ServerConfig


class TestCompositionFeatures:
    """End-to-end tests for all composition features."""

    @pytest.fixture
    async def server(self):
        """Create test server instance."""
        config = ServerConfig()
        server = MCPServer(config)
        await server.start()
        yield server
        await server.stop()

    # Song Structure Tests (Day 1)

    @pytest.mark.asyncio
    async def test_create_song_structure_pop(self, server):
        """Test creating a pop song structure."""
        result = await server.call_tool(
            "create_song_structure", {"genre": "pop", "song_type": "standard", "duration": 180}
        )

        assert result["status"] == "success"
        structure = result["data"]

        # Verify essential sections present
        section_types = [section["type"] for section in structure["sections"]]
        expected_sections = ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"]
        assert all(section in section_types for section in ["intro", "verse", "chorus", "outro"])

        # Verify timing constraints
        total_duration = sum(section["duration"] for section in structure["sections"])
        assert 170 <= total_duration <= 190  # Allow 10 second variance

        # Verify key relationships
        assert "key_plan" in structure
        assert structure["key_plan"]["main_key"] is not None

    @pytest.mark.asyncio
    async def test_generate_song_section_verse(self, server):
        """Test generating a verse section."""
        result = await server.call_tool(
            "generate_song_section", {"section_type": "verse", "genre": "pop", "key": "C major"}
        )

        assert result["status"] == "success"
        section = result["data"]

        # Verify section structure
        assert section["type"] == "verse"
        assert section["key"] == "C major"
        assert "melody" in section
        assert "harmony" in section
        assert "rhythm" in section
        assert "arrangement" in section

        # Verify melodic content
        melody = section["melody"]
        assert len(melody["notes"]) > 0
        assert "phrase_structure" in melody

        # Verify harmonic content
        harmony = section["harmony"]
        assert len(harmony["progression"]) >= 4  # At least 4 chords
        assert all("chord" in chord_info for chord_info in harmony["progression"])

    @pytest.mark.asyncio
    async def test_create_section_transitions(self, server):
        """Test creating transitions between sections."""
        # First create two sections
        verse_result = await server.call_tool(
            "generate_song_section", {"section_type": "verse", "genre": "rock", "key": "G major"}
        )

        chorus_result = await server.call_tool(
            "generate_song_section", {"section_type": "chorus", "genre": "rock", "key": "G major"}
        )

        # Create transition
        transition_result = await server.call_tool(
            "create_section_transitions",
            {"from_section": verse_result["data"], "to_section": chorus_result["data"], "transition_type": "buildup"},
        )

        assert transition_result["status"] == "success"
        transition = transition_result["data"]

        assert "transition_material" in transition
        assert transition["type"] == "buildup"
        assert "duration" in transition
        assert transition["duration"] > 0

    # Melodic Development Tests (Day 2)

    @pytest.mark.asyncio
    async def test_develop_melodic_motif(self, server):
        """Test melodic motif development."""
        motif = [60, 62, 64, 65]  # C-D-E-F

        result = await server.call_tool(
            "develop_melodic_motif",
            {"motif": motif, "development_techniques": ["sequence", "inversion", "retrograde"], "target_length": 8},
        )

        assert result["status"] == "success"
        developed = result["data"]

        # Verify development occurred
        assert "developed_melody" in developed
        assert len(developed["developed_melody"]) >= 8

        # Verify techniques were applied
        assert "techniques_used" in developed
        techniques = developed["techniques_used"]
        assert any("sequence" in tech["name"].lower() for tech in techniques)

        # Verify analysis
        assert "analysis" in developed
        assert "original_motif" in developed["analysis"]

    @pytest.mark.asyncio
    async def test_create_melodic_phrase(self, server):
        """Test melodic phrase creation."""
        progression = ["C", "Am", "F", "G"]

        result = await server.call_tool(
            "create_melodic_phrase",
            {"chord_progression": progression, "key": "C major", "phrase_type": "period", "style": "vocal"},
        )

        assert result["status"] == "success"
        phrase = result["data"]

        # Verify phrase structure
        assert "melody" in phrase
        assert "phrase_structure" in phrase
        assert phrase["phrase_structure"]["type"] == "period"

        # Verify cadences
        assert "cadences" in phrase["phrase_structure"]
        cadences = phrase["phrase_structure"]["cadences"]
        assert len(cadences) >= 1

        # Verify vocal style characteristics
        melody_notes = phrase["melody"]["notes"]
        intervals = [melody_notes[i + 1] - melody_notes[i] for i in range(len(melody_notes) - 1)]
        large_leaps = [abs(interval) for interval in intervals if abs(interval) > 4]
        assert len(large_leaps) / len(intervals) < 0.3  # Less than 30% large leaps for vocal style

    @pytest.mark.asyncio
    async def test_vary_melody_for_repetition(self, server):
        """Test melody variation."""
        original_melody = [60, 62, 64, 67, 65, 64, 62, 60]

        result = await server.call_tool(
            "vary_melody_for_repetition", {"original_melody": original_melody, "variation_type": "embellishment"}
        )

        assert result["status"] == "success"
        variation = result["data"]

        # Verify variation occurred
        assert "varied_melody" in variation
        varied_melody = variation["varied_melody"]["notes"]
        assert len(varied_melody) >= len(original_melody)  # Embellishment should add notes

        # Verify recognizability maintained
        assert "similarity_score" in variation
        assert variation["similarity_score"] >= 0.6  # At least 60% similar

        # Verify variation techniques
        assert "variation_techniques" in variation

    # Advanced Harmony Tests (Day 3)

    @pytest.mark.asyncio
    async def test_optimize_voice_leading(self, server):
        """Test voice leading optimization."""
        progression = [
            {"chord": "C", "voicing": [48, 60, 64, 67]},  # C major
            {"chord": "F", "voicing": [53, 57, 60, 65]},  # F major
            {"chord": "G", "voicing": [55, 59, 62, 67]},  # G major
            {"chord": "C", "voicing": [48, 60, 64, 67]},  # C major
        ]

        result = await server.call_tool("optimize_voice_leading", {"chord_progression": progression, "voice_count": 4})

        assert result["status"] == "success"
        optimized = result["data"]

        # Verify optimization occurred
        assert "optimized_progression" in optimized
        opt_prog = optimized["optimized_progression"]
        assert len(opt_prog) == len(progression)

        # Verify voice leading quality
        assert "voice_leading_analysis" in optimized
        analysis = optimized["voice_leading_analysis"]
        assert "total_motion" in analysis
        assert analysis["total_motion"] < 50  # Should be reasonably smooth

    @pytest.mark.asyncio
    async def test_add_chromatic_harmony(self, server):
        """Test chromatic harmony addition."""
        basic_progression = ["C", "F", "G", "C"]

        result = await server.call_tool(
            "add_chromatic_harmony", {"basic_progression": basic_progression, "key": "C major", "complexity": "medium"}
        )

        assert result["status"] == "success"
        enhanced = result["data"]

        # Verify enhancement occurred
        assert "enhanced_progression" in enhanced
        enh_prog = enhanced["enhanced_progression"]
        assert len(enh_prog) >= len(basic_progression)  # Should add chords

        # Verify chromatic elements
        assert "chromatic_elements" in enhanced
        chromatic = enhanced["chromatic_elements"]
        assert len(chromatic) > 0

    @pytest.mark.asyncio
    async def test_create_bass_line_with_voice_leading(self, server):
        """Test bass line creation with voice leading."""
        progression = [
            {"chord": "C", "duration": 4},
            {"chord": "Am", "duration": 4},
            {"chord": "F", "duration": 4},
            {"chord": "G", "duration": 4},
        ]

        result = await server.call_tool(
            "create_bass_line_with_voice_leading", {"chord_progression": progression, "style": "walking"}
        )

        assert result["status"] == "success"
        bass_line = result["data"]

        # Verify bass line structure
        assert "bass_notes" in bass_line
        assert "rhythm" in bass_line
        assert "voice_leading_quality" in bass_line

        # Verify walking bass characteristics
        notes = bass_line["bass_notes"]
        assert len(notes) >= 16  # Walking bass should have many notes

        # Verify voice leading quality
        vl_quality = bass_line["voice_leading_quality"]
        assert "smoothness_score" in vl_quality
        assert vl_quality["smoothness_score"] >= 0.7

    # Arrangement Tests (Day 4)

    @pytest.mark.asyncio
    async def test_arrange_for_ensemble(self, server):
        """Test arrangement for specific ensemble."""
        composition = {
            "melody": {"notes": [60, 62, 64, 67, 65, 64, 62, 60]},
            "chords": [{"chord": "C", "duration": 4}, {"chord": "G", "duration": 4}],
            "structure": {"sections": [{"type": "A", "measures": 8}]},
        }

        result = await server.call_tool(
            "arrange_for_ensemble",
            {"composition": composition, "ensemble_type": "string_quartet", "arrangement_style": "balanced"},
        )

        assert result["status"] == "success"
        arrangement = result["data"]

        # Verify ensemble parts
        assert "parts" in arrangement
        parts = arrangement["parts"]
        expected_instruments = ["violin1", "violin2", "viola", "cello"]
        assert all(instr in parts for instr in expected_instruments)

        # Verify each part has content
        for instrument in expected_instruments:
            part = parts[instrument]
            assert "notes" in part
            assert "rhythm" in part
            assert len(part["notes"]) > 0

        # Verify arrangement quality
        assert "arrangement_analysis" in arrangement

    @pytest.mark.asyncio
    async def test_create_counter_melodies(self, server):
        """Test counter-melody creation."""
        main_melody = [60, 62, 64, 67, 65, 64, 62, 60]
        harmony = [{"chord": "C", "duration": 4}, {"chord": "G", "duration": 4}]

        result = await server.call_tool(
            "create_counter_melodies", {"main_melody": main_melody, "harmony": harmony, "instrument": "violin"}
        )

        assert result["status"] == "success"
        counter = result["data"]

        # Verify counter-melody structure
        assert "counter_melodies" in counter
        counter_melodies = counter["counter_melodies"]
        assert len(counter_melodies) >= 1

        # Verify independence and complementarity
        assert "analysis" in counter
        analysis = counter["analysis"]
        assert "independence_score" in analysis
        assert "complementarity_score" in analysis
        assert analysis["independence_score"] >= 0.6
        assert analysis["complementarity_score"] >= 0.6

    @pytest.mark.asyncio
    async def test_orchestrate_texture_changes(self, server):
        """Test texture orchestration."""
        composition = {
            "melody": {"notes": [60, 62, 64, 67] * 8},
            "harmony": [{"chord": "C", "duration": 4}] * 8,
            "structure": {"sections": [{"type": "A", "measures": 16}]},
        }

        dynamic_plan = ["p", "mp", "mf", "f", "mf", "p"]

        result = await server.call_tool(
            "orchestrate_texture_changes", {"composition": composition, "dynamic_plan": dynamic_plan}
        )

        assert result["status"] == "success"
        orchestrated = result["data"]

        # Verify texture variations
        assert "texture_plan" in orchestrated
        texture_plan = orchestrated["texture_plan"]
        assert len(texture_plan) == len(dynamic_plan)

        # Verify texture supports dynamics
        for i, texture in enumerate(texture_plan):
            expected_dynamic = dynamic_plan[i]
            assert "density" in texture
            assert "register_spread" in texture

            # Louder dynamics should have denser textures
            if expected_dynamic in ["f", "ff"]:
                assert texture["density"] >= 0.7
            elif expected_dynamic in ["p", "pp"]:
                assert texture["density"] <= 0.4

    # Complete Composition Tests (Day 5)

    @pytest.mark.asyncio
    async def test_compose_complete_song(self, server):
        """Test complete song composition."""
        result = await server.call_tool(
            "compose_complete_song",
            {
                "description": "a driving song about freedom with a memorable chorus",
                "genre": "blues_rock",
                "key": "E major",
                "tempo": 120,
                "target_duration": 180,
            },
        )

        assert result["status"] == "success"
        composition = result["data"]

        # Verify complete structure
        assert "structure" in composition
        assert "sections" in composition["structure"]
        sections = composition["structure"]["sections"]

        # Should have multiple sections
        assert len(sections) >= 5
        section_types = [s["type"] for s in sections]
        assert "chorus" in section_types  # Must have memorable chorus

        # Verify musical content
        assert "melody" in composition
        assert "harmony" in composition
        assert "arrangement" in composition

        # Verify timing
        total_duration = sum(s["duration"] for s in sections)
        assert 170 <= total_duration <= 190

        # Verify genre characteristics
        assert composition["genre"] == "blues_rock"
        assert composition["key"] == "E major"
        assert composition["tempo"] == 120

    @pytest.mark.asyncio
    async def test_analyze_composition_quality(self, server):
        """Test composition analysis."""
        composition = {
            "melody": {"notes": [60, 62, 64, 67, 65, 64, 62, 60], "rhythm": [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0]},
            "harmony": [
                {"chord": "C", "duration": 2},
                {"chord": "Am", "duration": 2},
                {"chord": "F", "duration": 2},
                {"chord": "G", "duration": 2},
            ],
            "structure": {"sections": [{"type": "verse", "measures": 8}, {"type": "chorus", "measures": 8}]},
        }

        result = await server.call_tool("analyze_composition_quality", {"composition": composition})

        assert result["status"] == "success"
        analysis = result["data"]

        # Verify analysis categories
        required_categories = ["melody", "harmony", "rhythm", "form", "overall"]
        assert all(category in analysis for category in required_categories)

        # Verify scoring
        for category in required_categories:
            category_analysis = analysis[category]
            assert "score" in category_analysis
            assert 0 <= category_analysis["score"] <= 10

        # Verify improvement suggestions
        assert "improvement_suggestions" in analysis
        suggestions = analysis["improvement_suggestions"]
        assert len(suggestions) >= 1
        assert all("category" in suggestion for suggestion in suggestions)
        assert all("suggestion" in suggestion for suggestion in suggestions)

    @pytest.mark.asyncio
    async def test_refine_composition(self, server):
        """Test composition refinement."""
        composition = {
            "melody": {"notes": [60, 60, 60, 60, 60, 60, 60, 60]},  # Boring melody
            "harmony": [{"chord": "C", "duration": 8}],  # Static harmony
            "structure": {"sections": [{"type": "verse", "measures": 8}]},
        }

        result = await server.call_tool(
            "refine_composition", {"composition": composition, "focus_areas": ["melody", "harmony"]}
        )

        assert result["status"] == "success"
        refined = result["data"]

        # Verify refinement occurred
        assert "refined_composition" in refined
        refined_comp = refined["refined_composition"]

        # Melody should be more varied
        original_notes = composition["melody"]["notes"]
        refined_notes = refined_comp["melody"]["notes"]
        original_variety = len(set(original_notes)) / len(original_notes)
        refined_variety = len(set(refined_notes)) / len(refined_notes)
        assert refined_variety > original_variety

        # Harmony should be more varied
        assert len(refined_comp["harmony"]) > len(composition["harmony"])

        # Verify change documentation
        assert "changes_made" in refined
        changes = refined["changes_made"]
        assert len(changes) > 0

    # Integration Tests

    @pytest.mark.asyncio
    async def test_full_composition_workflow(self, server):
        """Test complete composition workflow integration."""
        # Step 1: Create song structure
        structure_result = await server.call_tool(
            "create_song_structure", {"genre": "pop", "song_type": "standard", "duration": 120}
        )

        # Step 2: Generate sections
        sections = []
        for section_info in structure_result["data"]["sections"][:3]:  # First 3 sections
            section_result = await server.call_tool(
                "generate_song_section", {"section_type": section_info["type"], "genre": "pop", "key": "C major"}
            )
            sections.append(section_result["data"])

        # Step 3: Create arrangement
        composition = {"sections": sections, "key": "C major", "tempo": 120}

        arrangement_result = await server.call_tool(
            "arrange_for_ensemble",
            {"composition": composition, "ensemble_type": "rock_band", "arrangement_style": "full"},
        )

        # Step 4: Analyze and refine
        analysis_result = await server.call_tool(
            "analyze_composition_quality", {"composition": arrangement_result["data"]}
        )

        # Verify workflow completion
        assert all(result["status"] == "success" for result in [structure_result, arrangement_result, analysis_result])

        # Verify final composition has all elements
        final_composition = arrangement_result["data"]
        assert "parts" in final_composition
        assert len(final_composition["parts"]) >= 3  # Should have multiple instruments

        # Verify analysis provides useful feedback
        analysis = analysis_result["data"]
        assert "overall" in analysis
        assert analysis["overall"]["score"] > 0
