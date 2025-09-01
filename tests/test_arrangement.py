# -*- coding: utf-8 -*-
"""
Unit tests for arrangement and orchestration.
"""

import pytest
from typing import Dict, List

from midi_mcp.composition.arrangement import (
    EnsembleArranger,
    CounterMelodyGenerator,
    TextureOrchestrator
)
from midi_mcp.models.composition_models import (
    Composition,
    Arrangement,
    CounterMelody,
    TexturePlan
)


class TestEnsembleArranger:
    """Test ensemble arrangement capabilities."""
    
    def test_string_quartet_arrangement(self):
        """Test arrangement for string quartet."""
        arranger = EnsembleArranger()
        
        composition = Composition(
            melody={"notes": [60, 62, 64, 67, 65, 64, 62, 60]},
            harmony=[{"chord": "C", "duration": 4}, {"chord": "G", "duration": 4}],
            key="C major"
        )
        
        arrangement = arranger.arrange_for_ensemble(
            composition=composition,
            ensemble_type="string_quartet",
            arrangement_style="balanced"
        )
        
        assert isinstance(arrangement, Arrangement)
        
        # Should have all string quartet instruments
        expected_parts = ["violin_1", "violin_2", "viola", "cello"]
        assert all(part in arrangement.parts for part in expected_parts)
        
        # Each part should have content
        for part_name in expected_parts:
            part = arrangement.parts[part_name]
            assert len(part.notes) > 0
            assert part.instrument == part_name
            
    def test_jazz_combo_arrangement(self):
        """Test arrangement for jazz combo."""
        arranger = EnsembleArranger()
        
        composition = Composition(
            melody={"notes": [60, 63, 65, 67, 70, 67, 65, 63]},
            harmony=[
                {"chord": "Cmaj7", "duration": 4},
                {"chord": "Am7", "duration": 4},
                {"chord": "Dm7", "duration": 4},
                {"chord": "G7", "duration": 4}
            ],
            key="C major"
        )
        
        arrangement = arranger.arrange_for_ensemble(
            composition=composition,
            ensemble_type="jazz_combo",
            arrangement_style="full"
        )
        
        # Should have jazz combo instruments
        expected_parts = ["piano", "bass", "drums", "saxophone"]
        assert all(part in arrangement.parts for part in expected_parts)
        
        # Jazz-specific elements
        bass_part = arrangement.parts["bass"]
        assert "walking" in bass_part.style_characteristics or \
               "quarter_note" in bass_part.style_characteristics
               
    def test_rock_band_arrangement(self):
        """Test arrangement for rock band."""
        arranger = EnsembleArranger()
        
        composition = Composition(
            melody={"notes": [55, 57, 60, 62, 60, 57, 55]},
            harmony=[
                {"chord": "G5", "duration": 2},
                {"chord": "C5", "duration": 2}, 
                {"chord": "D5", "duration": 2},
                {"chord": "G5", "duration": 2}
            ],
            key="G major"
        )
        
        arrangement = arranger.arrange_for_ensemble(
            composition=composition,
            ensemble_type="rock_band",
            arrangement_style="dense"
        )
        
        # Should have rock band instruments
        expected_parts = ["lead_guitar", "rhythm_guitar", "bass", "drums", "vocals"]
        assert all(part in arrangement.parts for part in expected_parts)
        
        # Rock-specific characteristics
        lead_guitar = arrangement.parts["lead_guitar"]
        assert lead_guitar.register >= 60  # Lead guitar should be in higher register


class TestCounterMelodyCreator:
    """Test counter-melody creation."""
    
    def test_create_counter_melody(self):
        """Test basic counter-melody creation."""
        creator = CounterMelodyCreator()
        
        main_melody = [60, 62, 64, 67, 65, 64, 62, 60]
        harmony = [
            {"chord": "C", "duration": 4},
            {"chord": "G", "duration": 4}
        ]
        
        counter = creator.create_counter_melody(
            main_melody=main_melody,
            harmony=harmony,
            instrument="violin"
        )
        
        assert isinstance(counter, CounterMelody)
        assert len(counter.notes) > 0
        
        # Should be independent from main melody
        assert counter.independence_score >= 0.5
        
        # Should be complementary
        assert counter.complementarity_score >= 0.5
        
    def test_counter_melody_register_separation(self):
        """Test that counter-melody uses appropriate register."""
        creator = CounterMelodyCreator()
        
        # High main melody
        main_melody = [72, 74, 76, 79, 77, 76, 74, 72]
        harmony = [{"chord": "C", "duration": 8}]
        
        counter = creator.create_counter_melody(
            main_melody=main_melody,
            harmony=harmony,
            instrument="cello"
        )
        
        # Counter melody should be in lower register for cello
        avg_counter_pitch = sum(counter.notes) / len(counter.notes)
        avg_main_pitch = sum(main_melody) / len(main_melody)
        
        assert avg_counter_pitch < avg_main_pitch
        
    def test_rhythmic_independence(self):
        """Test rhythmic independence in counter-melody."""
        creator = CounterMelodyCreator()
        
        main_melody = [60, 60, 62, 62, 64, 64, 65, 65]  # Repeated notes
        harmony = [{"chord": "C", "duration": 8}]
        
        counter = creator.create_counter_melody(
            main_melody=main_melody,
            harmony=harmony,
            instrument="flute"
        )
        
        # Counter melody should have different rhythm
        # (This would need rhythm information in the model)
        assert counter.rhythmic_independence_score >= 0.6


class TestTextureOrchestrator:
    """Test texture orchestration capabilities."""
    
    def test_dynamic_texture_changes(self):
        """Test orchestrating texture changes for dynamics."""
        orchestrator = TextureOrchestrator()
        
        composition = Composition(
            melody={"notes": [60, 62, 64, 67] * 4},
            harmony=[{"chord": "C", "duration": 4}] * 4
        )
        
        dynamic_plan = ["p", "mp", "mf", "f"]
        
        texture_plan = orchestrator.orchestrate_texture_changes(
            composition=composition,
            dynamic_plan=dynamic_plan
        )
        
        assert isinstance(texture_plan, TexturePlan)
        assert len(texture_plan.texture_points) == len(dynamic_plan)
        
        # Verify texture density increases with dynamics
        textures = texture_plan.texture_points
        p_texture = next(t for t in textures if t.target_dynamic == "p")
        f_texture = next(t for t in textures if t.target_dynamic == "f")
        
        assert f_texture.density > p_texture.density
        
    def test_register_distribution(self):
        """Test register distribution in texture orchestration."""
        orchestrator = TextureOrchestrator()
        
        composition = Composition(
            melody={"notes": [60, 62, 64, 65]},
            harmony=[{"chord": "C", "duration": 4}]
        )
        
        texture_plan = orchestrator.orchestrate_texture_changes(
            composition=composition,
            dynamic_plan=["mf"]
        )
        
        texture = texture_plan.texture_points[0]
        
        # Should specify register distribution
        assert hasattr(texture, "register_spread")
        assert texture.register_spread > 0
        
    def test_ensemble_balance(self):
        """Test ensemble balance in texture orchestration."""
        orchestrator = TextureOrchestrator()
        
        composition = Composition(
            melody={"notes": [67, 69, 71, 72]},  # High melody
            harmony=[{"chord": "C", "duration": 4}]
        )
        
        # Should balance high melody with lower accompaniment
        texture_plan = orchestrator.orchestrate_texture_changes(
            composition=composition,
            dynamic_plan=["mf"],
            ensemble_type="orchestra"
        )
        
        texture = texture_plan.texture_points[0]
        
        # Should have balance information
        assert hasattr(texture, "ensemble_balance")
        assert "bass_presence" in texture.ensemble_balance
        assert texture.ensemble_balance["bass_presence"] > 0.3