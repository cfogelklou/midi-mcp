# -*- coding: utf-8 -*-
"""
Song structure and form generation tools.

Builds on existing genre knowledge and music theory to create complete song structures.
"""

import random
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from ..models.composition_models import (
    SongStructure, Section, SectionType, Transition, Melody
)
from ..genres.genre_manager import GenreManager
from ..genres.composer import Composer
from ..genres.library_integration import LibraryIntegration
from ..theory.keys import KeyManager


class SongStructureGenerator:
    """Generates complete song structures using genre knowledge."""
    
    def __init__(self, genre_manager: Optional[GenreManager] = None):
        """Initialize with genre manager."""
        self.genre_manager = genre_manager or GenreManager()
        self.composer = Composer(self.genre_manager)
        self.libraries = LibraryIntegration()
        self.key_manager = KeyManager()
        
    def create_structure(
        self, 
        genre: str, 
        song_type: str = "standard",
        duration: int = 180
    ) -> SongStructure:
        """
        Create a complete song structure.
        
        Args:
            genre: Musical genre
            song_type: Type of song (standard, ballad, epic, etc.)
            duration: Target duration in seconds
            
        Returns:
            Complete song structure
        """
        genre_data = self.genre_manager.get_genre_data(genre)
        
        # Get typical song structures for this genre
        structure_templates = genre_data.get("song_structures", {})
        template = structure_templates.get(song_type, self._get_default_structure(genre))
        
        # Calculate section durations based on target duration
        sections = self._calculate_section_durations(template, duration, genre_data)
        
        # Create key plan
        key_plan = self._create_key_plan(genre, sections)
        
        # Set tempo based on genre
        tempo_range = genre_data.get("tempo_range", [120, 120])
        tempo = random.randint(tempo_range[0], tempo_range[1])
        
        return SongStructure(
            genre=genre,
            sections=sections,
            key_plan=key_plan,
            tempo=tempo,
            time_signature=(4, 4),  # Default, can be genre-specific later
            total_duration=duration
        )
    
    def _get_default_structure(self, genre: str) -> List[Dict[str, Any]]:
        """Get default structure based on genre."""
        if genre in ["blues", "blues_rock"]:
            return [
                {"type": "intro", "relative_duration": 0.1},
                {"type": "verse", "relative_duration": 0.2},
                {"type": "chorus", "relative_duration": 0.15},
                {"type": "verse", "relative_duration": 0.2},
                {"type": "chorus", "relative_duration": 0.15},
                {"type": "solo", "relative_duration": 0.15},
                {"type": "outro", "relative_duration": 0.05}
            ]
        elif genre in ["pop", "rock"]:
            return [
                {"type": "intro", "relative_duration": 0.08},
                {"type": "verse", "relative_duration": 0.18},
                {"type": "chorus", "relative_duration": 0.18},
                {"type": "verse", "relative_duration": 0.18},
                {"type": "chorus", "relative_duration": 0.18},
                {"type": "bridge", "relative_duration": 0.12},
                {"type": "chorus", "relative_duration": 0.18},
                {"type": "outro", "relative_duration": 0.04}
            ]
        elif genre == "jazz":
            return [
                {"type": "intro", "relative_duration": 0.1},
                {"type": "verse", "relative_duration": 0.25},  # Theme
                {"type": "verse", "relative_duration": 0.25},  # Theme repeat
                {"type": "solo", "relative_duration": 0.3},    # Improvisation
                {"type": "verse", "relative_duration": 0.25},  # Theme return
                {"type": "outro", "relative_duration": 0.05}
            ]
        else:
            # Generic pop structure
            return [
                {"type": "intro", "relative_duration": 0.1},
                {"type": "verse", "relative_duration": 0.2},
                {"type": "chorus", "relative_duration": 0.2},
                {"type": "verse", "relative_duration": 0.2},
                {"type": "chorus", "relative_duration": 0.2},
                {"type": "outro", "relative_duration": 0.1}
            ]
    
    def _calculate_section_durations(
        self, 
        template: List[Dict[str, Any]], 
        total_duration: int,
        genre_data: Dict[str, Any]
    ) -> List[Section]:
        """Calculate actual durations for each section."""
        sections = []
        
        for section_info in template:
            section_type = SectionType(section_info["type"])
            relative_duration = section_info["relative_duration"]
            actual_duration = total_duration * relative_duration
            
            # Calculate measures based on tempo and time signature
            tempo = genre_data.get("tempo_range", [120, 120])[0]
            measures = max(1, int(actual_duration / (240 / tempo)))  # Rough estimate
            
            # Set energy level based on section type
            energy_level = self._get_section_energy_level(section_type, genre_data)
            
            section = Section(
                type=section_type,
                key="C major",  # Will be updated by key plan
                duration=actual_duration,
                measures=measures,
                energy_level=energy_level
            )
            
            sections.append(section)
            
        return sections
    
    def _get_section_energy_level(self, section_type: SectionType, genre_data: Dict[str, Any]) -> float:
        """Determine energy level for section type."""
        base_energy = genre_data.get("energy_level", 0.5)
        
        energy_modifiers = {
            SectionType.INTRO: -0.2,
            SectionType.VERSE: -0.1,
            SectionType.CHORUS: +0.2,
            SectionType.BRIDGE: +0.1,
            SectionType.SOLO: +0.3,
            SectionType.BREAKDOWN: -0.3,
            SectionType.BUILD_UP: +0.4,
            SectionType.OUTRO: -0.2,
        }
        
        modifier = energy_modifiers.get(section_type, 0.0)
        return max(0.0, min(1.0, base_energy + modifier))
    
    def _create_key_plan(self, genre: str, sections: List[Section]) -> Dict[str, Any]:
        """Create key relationships throughout the song."""
        # For now, keep it simple - can be enhanced later
        main_key = "C major"
        
        key_plan = {
            "main_key": main_key,
            "modulations": [],
            "section_keys": {}
        }
        
        # Assign keys to sections
        for section in sections:
            section.key = main_key
            key_plan["section_keys"][section.type.value] = main_key
        
        return key_plan


class SectionGenerator:
    """Generates individual song sections."""
    
    def __init__(self, genre_manager: Optional[GenreManager] = None):
        """Initialize with genre manager."""
        self.genre_manager = genre_manager or GenreManager()
        self.composer = Composer(self.genre_manager)
        self.libraries = LibraryIntegration()
        
    def generate_section(
        self,
        section_type: str,
        genre: str,
        key: str,
        previous_section: Optional[Section] = None
    ) -> Section:
        """
        Generate a specific song section.
        
        Args:
            section_type: Type of section
            genre: Musical genre
            key: Key signature  
            previous_section: Previous section for continuity
            
        Returns:
            Complete section with musical content
        """
        section_enum = SectionType(section_type)
        genre_data = self.genre_manager.get_genre_data(genre)
        
        # Generate harmony using existing tools
        harmony = self._generate_section_harmony(section_enum, genre, key, genre_data)
        
        # Generate melody using existing tools  
        melody = self._generate_section_melody(section_enum, genre, key, harmony, genre_data)
        
        # Generate rhythm pattern
        rhythm = self._generate_section_rhythm(section_enum, genre, genre_data)
        
        # Create arrangement notes
        arrangement = self._generate_section_arrangement(section_enum, genre, genre_data)
        
        # Calculate duration (rough estimate)
        duration = self._estimate_section_duration(section_enum, genre_data)
        measures = max(4, int(duration / 2))  # Rough 2 seconds per measure
        
        return Section(
            type=section_enum,
            key=key,
            duration=duration,
            measures=measures,
            melody=melody,
            harmony=harmony,
            rhythm=rhythm,
            arrangement=arrangement,
            energy_level=self._get_section_energy_level(section_enum, genre_data)
        )
    
    def _generate_section_harmony(
        self, 
        section_type: SectionType, 
        genre: str, 
        key: str,
        genre_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate harmony for the section."""
        # Use existing progression creation
        variation = "standard"
        if section_type == SectionType.CHORUS:
            variation = "strong"  # More powerful progression for chorus
        elif section_type == SectionType.BRIDGE:
            variation = "contrasting"
            
        try:
            progression_result = self.composer.create_progression(genre, key, variation)
            return progression_result.get("progression", [])
        except Exception:
            # Fallback to simple progression
            return [
                {"chord": "I", "duration": 2},
                {"chord": "vi", "duration": 2}, 
                {"chord": "IV", "duration": 2},
                {"chord": "V", "duration": 2}
            ]
    
    def _generate_section_melody(
        self,
        section_type: SectionType,
        genre: str,
        key: str,
        harmony: List[Dict[str, Any]],
        genre_data: Dict[str, Any]
    ) -> Optional[Melody]:
        """Generate melody for the section."""
        try:
            melody_result = self.composer.create_melody(genre, key, {"progression": harmony})
            notes = melody_result.get("notes", [])
            rhythm = melody_result.get("rhythm", [])
            
            if not notes:
                return None
                
            # Create phrase structure based on section type
            phrase_structure = self._create_phrase_structure(section_type)
            
            # Determine register based on section type
            register = "mid"
            if section_type == SectionType.CHORUS:
                register = "high"  # Choruses typically higher
            elif section_type == SectionType.VERSE:
                register = "mid"
                
            return Melody(
                notes=notes,
                rhythm=rhythm,
                phrase_structure=phrase_structure,
                register=register
            )
        except Exception:
            return None
    
    def _create_phrase_structure(self, section_type: SectionType) -> Dict[str, Any]:
        """Create appropriate phrase structure for section type."""
        if section_type == SectionType.VERSE:
            return {
                "type": "period",
                "antecedent": {"measures": [1, 2, 3, 4]},
                "consequent": {"measures": [5, 6, 7, 8]}
            }
        elif section_type == SectionType.CHORUS:
            return {
                "type": "sentence", 
                "presentation": {"measures": [1, 2]},
                "repetition": {"measures": [3, 4]},
                "continuation": {"measures": [5, 6, 7, 8]}
            }
        else:
            return {"type": "phrase_group"}
    
    def _generate_section_rhythm(
        self, 
        section_type: SectionType, 
        genre: str,
        genre_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate rhythm pattern for section."""
        rhythms = genre_data.get("rhythms", {})
        standard_rhythm = rhythms.get("standard", {})
        
        # Modify rhythm based on section type
        if section_type == SectionType.CHORUS:
            feel = standard_rhythm.get("feel", "straight")
            return {
                "feel": feel,
                "intensity": "high",
                "pattern": "driving"
            }
        elif section_type == SectionType.VERSE:
            return {
                "feel": standard_rhythm.get("feel", "straight"),
                "intensity": "medium",
                "pattern": "steady"
            }
        else:
            return standard_rhythm or {"feel": "straight", "intensity": "medium"}
    
    def _generate_section_arrangement(
        self,
        section_type: SectionType,
        genre: str, 
        genre_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate arrangement notes for section."""
        instruments = genre_data.get("instruments", {})
        
        arrangement = {
            "texture": "medium",
            "instrumentation": instruments.get("core", ["piano", "bass", "drums"]),
            "dynamics": "mf"  # Default medium forte
        }
        
        # Adjust based on section type
        if section_type == SectionType.INTRO:
            arrangement.update({
                "texture": "thin",
                "dynamics": "mp",
                "notes": "Gradual build-up, establish key and tempo"
            })
        elif section_type == SectionType.CHORUS:
            arrangement.update({
                "texture": "full",
                "dynamics": "f",
                "notes": "Full arrangement, all instruments active"
            })
        elif section_type == SectionType.VERSE:
            arrangement.update({
                "texture": "medium",
                "dynamics": "mf",
                "notes": "Accompaniment supports vocal melody"
            })
        elif section_type == SectionType.BRIDGE:
            arrangement.update({
                "texture": "contrasting",
                "dynamics": "mp",
                "notes": "Textural contrast with previous sections"
            })
            
        return arrangement
    
    def _estimate_section_duration(self, section_type: SectionType, genre_data: Dict[str, Any]) -> float:
        """Estimate duration for section type."""
        base_duration = 30.0  # 30 seconds default
        
        duration_modifiers = {
            SectionType.INTRO: 0.5,    # 15 seconds
            SectionType.VERSE: 1.0,    # 30 seconds  
            SectionType.CHORUS: 1.0,   # 30 seconds
            SectionType.BRIDGE: 0.8,   # 24 seconds
            SectionType.SOLO: 1.2,     # 36 seconds
            SectionType.OUTRO: 0.4,    # 12 seconds
        }
        
        modifier = duration_modifiers.get(section_type, 1.0)
        return base_duration * modifier
    
    def _get_section_energy_level(self, section_type: SectionType, genre_data: Dict[str, Any]) -> float:
        """Get energy level for section type."""
        base_energy = genre_data.get("energy_level", 0.5)
        
        energy_modifiers = {
            SectionType.INTRO: -0.2,
            SectionType.VERSE: -0.1,
            SectionType.CHORUS: +0.2,
            SectionType.BRIDGE: +0.1,
            SectionType.SOLO: +0.3,
            SectionType.OUTRO: -0.2,
        }
        
        modifier = energy_modifiers.get(section_type, 0.0)
        return max(0.0, min(1.0, base_energy + modifier))


class TransitionCreator:
    """Creates transitions between song sections."""
    
    def __init__(self):
        """Initialize transition creator."""
        pass
        
    def create_transition(
        self,
        from_section: Section,
        to_section: Section,
        transition_type: str = "smooth"
    ) -> Transition:
        """
        Create transition between sections.
        
        Args:
            from_section: Source section
            to_section: Target section  
            transition_type: Type of transition
            
        Returns:
            Transition material
        """
        # Calculate transition duration
        duration = self._calculate_transition_duration(transition_type, from_section, to_section)
        
        # Create transition material based on type
        material = self._create_transition_material(
            transition_type, from_section, to_section
        )
        
        return Transition(
            from_section=from_section.type.value,
            to_section=to_section.type.value,
            type=transition_type,
            duration=duration,
            material=material
        )
    
    def _calculate_transition_duration(
        self, 
        transition_type: str, 
        from_section: Section, 
        to_section: Section
    ) -> float:
        """Calculate appropriate transition duration."""
        base_durations = {
            "smooth": 2.0,
            "dramatic": 4.0, 
            "surprise": 0.5,
            "buildup": 6.0
        }
        return base_durations.get(transition_type, 2.0)
    
    def _create_transition_material(
        self,
        transition_type: str,
        from_section: Section,
        to_section: Section
    ) -> Dict[str, Any]:
        """Create musical material for the transition."""
        material = {
            "type": transition_type,
            "from_key": from_section.key,
            "to_key": to_section.key,
            "from_energy": from_section.energy_level,
            "to_energy": to_section.energy_level
        }
        
        if transition_type == "smooth":
            material.update({
                "approach": "gradual",
                "techniques": ["voice_leading", "harmonic_preparation"],
                "description": "Smooth harmonic transition maintaining flow"
            })
        elif transition_type == "buildup":
            material.update({
                "approach": "crescendo",
                "techniques": ["rhythmic_intensification", "textural_buildup"],
                "description": "Dynamic buildup creating energy and anticipation"
            })
        elif transition_type == "dramatic":
            material.update({
                "approach": "contrast",
                "techniques": ["dynamic_shift", "textural_break"],
                "description": "Dramatic shift creating strong contrast"
            })
        elif transition_type == "surprise":
            material.update({
                "approach": "sudden",
                "techniques": ["deceptive_resolution", "rhythmic_displacement"], 
                "description": "Unexpected transition creating surprise"
            })
            
        return material