# -*- coding: utf-8 -*-
"""
Complete composition integration system for Phase 5.

Provides end-to-end composition generation from high-level descriptions,
composition analysis, quality assessment, and refinement capabilities.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging
import re
import random

from ..models.composition_models import (
    CompleteComposition,
    CompositionAnalysis,
    SongStructure,
    Section,
    Melody,
    Arrangement,
    TextureLevel,
    DynamicLevel,
)
from .song_structure import SongStructureGenerator, SectionGenerator
from .melodic_development import MotifDeveloper, PhraseGenerator, MelodyVariator
from .voice_leading import VoiceLeadingOptimizer, ChromaticHarmonyGenerator
from .arrangement import EnsembleArranger, TextureOrchestrator
from ..genres.composer import Composer
from ..genres.genre_manager import GenreManager

logger = logging.getLogger(__name__)


@dataclass
class CompositionRequest:
    """Represents a high-level composition request."""

    description: str
    genre: str
    key: str
    tempo: int
    target_duration: int = 180
    ensemble_type: str = "piano_solo"
    mood: Optional[str] = None
    style_preferences: List[str] = field(default_factory=list)
    structural_preferences: List[str] = field(default_factory=list)


class CompleteComposer:
    """Orchestrates complete composition generation from high-level descriptions."""

    def __init__(self):
        self.structure_generator = SongStructureGenerator()
        self.section_generator = SectionGenerator()
        self.motif_developer = MotifDeveloper()
        self.phrase_generator = PhraseGenerator()
        self.melody_variator = MelodyVariator()
        self.voice_leading_optimizer = VoiceLeadingOptimizer()
        self.chromatic_harmony_generator = ChromaticHarmonyGenerator()
        self.ensemble_arranger = EnsembleArranger()
        self.texture_orchestrator = TextureOrchestrator()
        self.composer = Composer()
        self.genre_manager = GenreManager()

    def compose_complete_song(
        self,
        description: str,
        genre: str,
        key: str,
        tempo: int,
        target_duration: int = 180,
        ensemble_type: str = "piano_solo",
    ) -> CompleteComposition:
        """
        Generate a complete musical composition from a text description.

        Args:
            description: Text description of desired composition
            genre: Musical genre/style
            key: Key signature
            tempo: Tempo in BPM
            target_duration: Target length in seconds
            ensemble_type: Type of ensemble arrangement

        Returns:
            Complete composition with all sections, arrangements, and details
        """
        try:
            # Parse the description for musical elements
            request = self._parse_composition_request(description, genre, key, tempo, target_duration, ensemble_type)

            # Step 1: Generate song structure
            logger.info(f"Creating song structure for {genre} composition")
            song_structure = self.structure_generator.create_structure(
                request.genre, "standard", request.target_duration
            )

            # Step 2: Create core harmonic progression
            logger.info("Generating harmonic foundation")
            base_progression = self._create_harmonic_foundation(request, song_structure)

            # Step 3: Generate main melody
            logger.info("Creating main melody")
            main_melody = self._create_main_melody(request, base_progression)

            # Step 4: Develop melodic materials
            logger.info("Developing melodic variations")
            melodic_variations = self._develop_melodic_materials(main_melody, song_structure)

            # Step 5: Create arrangement
            logger.info(f"Arranging for {ensemble_type}")
            arrangement = self._create_full_arrangement(request, song_structure, main_melody, base_progression)

            # Step 6: Apply texture orchestration
            logger.info("Orchestrating texture changes")
            orchestrated_composition = self._apply_texture_orchestration(arrangement, song_structure)

            # Step 7: Assemble complete composition
            complete_composition = CompleteComposition(
                title=self._generate_title(request),
                genre=request.genre,
                key=request.key,
                tempo=request.tempo,
                time_signature=(4, 4),
                description=request.description,
                structure=song_structure,
                melody={"notes": main_melody.notes, "rhythm": main_melody.rhythm, "register": main_melody.register},
                harmony=base_progression,
                arrangement=arrangement,
                duration=float(request.target_duration),  # Set the actual duration
                style_characteristics=[
                    f"mood: {request.mood}" if request.mood else "no specific mood",
                    f"ensemble: {ensemble_type}",
                    f"generation: ai_created",
                ],
            )

            logger.info(f"Successfully generated complete composition: '{complete_composition.title}'")
            return complete_composition

        except Exception as e:
            logger.error(f"Error composing complete song: {e}")
            raise

    def _parse_composition_request(
        self, description: str, genre: str, key: str, tempo: int, target_duration: int, ensemble_type: str
    ) -> CompositionRequest:
        """Parse text description for musical elements and preferences."""

        # Extract mood indicators
        mood_keywords = {
            "happy": ["happy", "joyful", "cheerful", "upbeat", "bright"],
            "sad": ["sad", "melancholy", "somber", "dark", "minor"],
            "energetic": ["driving", "powerful", "intense", "aggressive", "fast"],
            "calm": ["peaceful", "serene", "gentle", "soft", "quiet"],
            "dramatic": ["dramatic", "epic", "cinematic", "grand", "heroic"],
            "romantic": ["romantic", "tender", "loving", "sweet", "intimate"],
        }

        mood = None
        description_lower = description.lower()
        for mood_type, keywords in mood_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                mood = mood_type
                break

        # Extract style preferences
        style_preferences = []
        if "memorable" in description_lower:
            style_preferences.append("catchy_melody")
        if "chorus" in description_lower:
            style_preferences.append("strong_chorus")
        if "verse" in description_lower:
            style_preferences.append("narrative_verse")
        if "solo" in description_lower or "instrumental" in description_lower:
            style_preferences.append("instrumental_focus")

        # Extract structural preferences
        structural_preferences = []
        if "intro" in description_lower:
            structural_preferences.append("extended_intro")
        if "bridge" in description_lower:
            structural_preferences.append("include_bridge")
        if "outro" in description_lower or "ending" in description_lower:
            structural_preferences.append("extended_outro")

        return CompositionRequest(
            description=description,
            genre=genre,
            key=key,
            tempo=tempo,
            target_duration=target_duration,
            ensemble_type=ensemble_type,
            mood=mood,
            style_preferences=style_preferences,
            structural_preferences=structural_preferences,
        )

    def _create_harmonic_foundation(
        self, request: CompositionRequest, song_structure: SongStructure
    ) -> List[Dict[str, Any]]:
        """Create the foundational harmonic progression."""

        # Use existing genre composer to create base progression
        progression_result = self.composer.create_progression(request.genre, request.key, "standard")

        base_chords = progression_result.get("chord_progression", [])

        # If no chords generated from genre composer, create fallback progression based on genre characteristics
        if not base_chords:
            logger.warning(f"No genre-specific progression found for {request.genre}, creating fallback")
            
            # Get genre characteristics to inform the fallback
            genre_data = self.genre_manager.get_genre_data(request.genre)
            
            # Use genre data to create appropriate progression
            if genre_data and "progressions" in genre_data:
                # Use the first available progression from genre data
                genre_progressions = genre_data["progressions"]
                if "standard" in genre_progressions:
                    progression_data = genre_progressions["standard"]
                    if "pattern" in progression_data:
                        progression_pattern = progression_data["pattern"]
                        base_chords = [
                            {"symbol": self._convert_roman_to_chord(chord, request.key), 
                             "root": self._get_chord_root_from_roman(chord, request.key), 
                             "duration": 4}
                            for chord in progression_pattern
                        ]
                elif genre_progressions:
                    # Use first available progression
                    first_key = list(genre_progressions.keys())[0]
                    progression_data = genre_progressions[first_key]
                    if "pattern" in progression_data:
                        progression_pattern = progression_data["pattern"]
                        base_chords = [
                            {"symbol": self._convert_roman_to_chord(chord, request.key), 
                             "root": self._get_chord_root_from_roman(chord, request.key), 
                             "duration": 4}
                            for chord in progression_pattern
                        ]
            
            # If still no chords from genre data, use fallback progressions from constants
            if not base_chords:
                from ..constants import get_genre_fallback_progression
                roman_progression = get_genre_fallback_progression(request.genre)
                base_chords = [
                    {"symbol": self._convert_roman_to_chord(chord, request.key), 
                     "root": self._get_chord_root_from_roman(chord, request.key), 
                     "duration": 4}
                    for chord in roman_progression
                    ]

        # Extend the harmonic progression to fill the target duration
        beats_per_minute = request.tempo
        target_duration_beats = request.target_duration * (beats_per_minute / 60.0)
        
        # Calculate duration of base progression
        base_progression_duration = sum(chord.get("duration", 4) for chord in base_chords)
        repetitions_needed = max(1, int(target_duration_beats / base_progression_duration))
        
        # Extend harmony by repeating the base progression
        extended_harmony = []
        for rep in range(repetitions_needed):
            for chord in base_chords:
                extended_harmony.append(chord.copy())
        
        # If we still need more time, add a few more chords
        current_duration = sum(chord.get("duration", 4) for chord in extended_harmony)
        while current_duration < target_duration_beats:
            # Add the first chord again
            extended_harmony.append(base_chords[0].copy())
            current_duration += base_chords[0].get("duration", 4)

        return extended_harmony

    def _get_chord_root(self, chord_symbol: str, key: str) -> int:
        """Get MIDI note number for chord root based on symbol and key."""
        from ..constants import chord_symbol_to_midi_root
        return chord_symbol_to_midi_root(chord_symbol, octave=4)

    def _convert_roman_to_chord(self, roman_numeral: str, key: str) -> str:
        """Convert Roman numeral to chord symbol using music21."""
        from ..constants import convert_roman_to_chord_symbol
        return convert_roman_to_chord_symbol(roman_numeral, key)

    def _get_chord_root_from_roman(self, roman_numeral: str, key: str) -> int:
        """Get MIDI root note from Roman numeral and key."""
        chord_symbol = self._convert_roman_to_chord(roman_numeral, key)
        return self._get_chord_root(chord_symbol, key)

    def _create_main_melody(self, request: CompositionRequest, harmony: List[Dict[str, Any]]) -> Melody:
        """Create the main melody over the harmonic foundation."""

        # Create initial phrase using phrase generator
        phrase = self.phrase_generator.create_phrase(
            [chord.get("symbol", "C") for chord in harmony[:4]],
            request.key,
            "period",
            "vocal" if request.ensemble_type != "piano_solo" else "instrumental",
        )

        # Extract melody from phrase using constants
        from ..constants import get_default_melody_notes
        base_melody_notes = phrase.melody.notes if hasattr(phrase.melody, "notes") else get_default_melody_notes()
        from ..constants import get_default_rhythm_pattern
        base_melody_rhythm = phrase.melody.rhythm if hasattr(phrase.melody, "rhythm") else get_default_rhythm_pattern()

        # Calculate how many times to repeat/vary the melody to fill the target duration
        beats_per_minute = request.tempo
        target_duration_beats = request.target_duration * (beats_per_minute / 60.0)
        
        # Calculate duration of base melody
        base_melody_duration = sum(base_melody_rhythm)
        repetitions_needed = max(1, int(target_duration_beats / base_melody_duration))
        
        # Extend melody by repeating and varying the base melody
        extended_melody_notes = []
        extended_melody_rhythm = []
        
        for rep in range(repetitions_needed):
            current_notes = base_melody_notes.copy()
            current_rhythm = base_melody_rhythm.copy()
            
            # Apply variations every few repetitions to avoid monotony
            if rep % 4 == 1:  # Transpose up
                current_notes = [note + 2 for note in current_notes]
            elif rep % 4 == 2:  # Transpose down
                current_notes = [note - 2 for note in current_notes]
            elif rep % 4 == 3:  # Rhythmic variation
                current_rhythm = [r * 0.75 if i % 2 == 0 else r * 1.25 for i, r in enumerate(current_rhythm)]
            
            extended_melody_notes.extend(current_notes)
            extended_melody_rhythm.extend(current_rhythm)

        # Apply mood-based adjustments using constants
        if request.mood:
            from ..constants import apply_mood_adjustments
            extended_melody_notes = apply_mood_adjustments(extended_melody_notes, request.mood)
            
            # Special case for energetic mood: increase rhythmic activity
            if request.mood == "energetic":
                extended_melody_rhythm = [r / 2 for r in extended_melody_rhythm]

        return Melody(
            notes=extended_melody_notes,
            rhythm=extended_melody_rhythm,
            phrase_structure={
                "type": "period",
                "phrases": ["a", "a'", "b", "a''"],
                "cadences": ["half", "authentic", "deceptive", "authentic"],
            },
            register="mid",
        )

    def _develop_melodic_materials(self, main_melody: Melody, song_structure: SongStructure) -> Dict[str, Melody]:
        """Develop variations of the main melody for different sections."""

        variations = {}
        base_notes = main_melody.notes[:4]  # Use first 4 notes as motif

        for i, section in enumerate(song_structure.sections):
            section_type = section.type.value

            if section_type == "verse":
                # Create simpler version for verse
                variation = self.melody_variator.create_variation(main_melody.notes, "rhythmic")
                variations[f"verse_{i}"] = Melody(
                    notes=variation.varied_melody.notes, rhythm=variation.varied_melody.rhythm
                )

            elif section_type == "chorus":
                # Create more elaborate version for chorus
                from ..models.composition_models import Motif

                motif_obj = Motif(notes=base_notes)
                development = self.motif_developer.develop_motif(motif_obj, ["sequence", "inversion"], 8)
                variations[f"chorus_{i}"] = Melody(
                    notes=development.developed_melody.notes, rhythm=development.developed_melody.rhythm
                )

            elif section_type == "bridge":
                # Create contrasting variation for bridge
                variation = self.melody_variator.create_variation(main_melody.notes, "modal")
                variations[f"bridge_{i}"] = Melody(
                    notes=variation.varied_melody.notes, rhythm=variation.varied_melody.rhythm
                )

        return variations

    def _create_full_arrangement(
        self,
        request: CompositionRequest,
        song_structure: SongStructure,
        main_melody: Melody,
        harmony: List[Dict[str, Any]],
    ) -> Arrangement:
        """Create full arrangement for the specified ensemble."""

        # Create composition dict for arrangement
        composition = {
            "melody": {"notes": main_melody.notes, "rhythm": main_melody.rhythm},
            "harmony": harmony,
            "structure": {"sections": [{"type": section.type.value} for section in song_structure.sections]},
        }

        # Determine arrangement style based on genre and mood
        if request.mood == "energetic":
            arrangement_style = "dense"
        elif request.mood == "calm":
            arrangement_style = "minimal"
        else:
            arrangement_style = "balanced"

        # Create arrangement
        arrangement = self.ensemble_arranger.arrange_for_ensemble(composition, request.ensemble_type, arrangement_style)

        return arrangement

    def _apply_texture_orchestration(self, arrangement: Arrangement, song_structure: SongStructure) -> Dict[str, Any]:
        """Apply texture orchestration to the arrangement."""

        # Create dynamic plan based on song structure using constants
        from ..constants import get_section_dynamic
        dynamic_plan = []
        for section in song_structure.sections:
            section_type = section.type.value if hasattr(section.type, 'value') else str(section.type)
            dynamic_level = get_section_dynamic(section_type)
            dynamic_plan.append(dynamic_level)

        # Apply orchestration
        composition_dict = {
            "structure": {"sections": [{"type": section.type.value} for section in song_structure.sections]}
        }

        orchestrated = self.texture_orchestrator.orchestrate_texture_changes(composition_dict, dynamic_plan)

        return orchestrated

    def _create_detailed_sections(
        self, song_structure: SongStructure, melodic_variations: Dict[str, Melody]
    ) -> List[Dict[str, Any]]:
        """Create detailed section data."""
        from ..constants import get_default_melody_notes, get_default_rhythm_pattern

        sections = []
        verse_count = 0
        chorus_count = 0

        for section in song_structure.sections:
            section_type = section.type.value

            # Find appropriate melodic variation
            if section_type == "verse":
                variation_key = f"verse_{verse_count}"
                verse_count += 1
            elif section_type == "chorus":
                variation_key = f"chorus_{chorus_count}"
                chorus_count += 1
            else:
                variation_key = list(melodic_variations.keys())[0] if melodic_variations else None

            section_melody = melodic_variations.get(variation_key)

            sections.append(
                {
                    "type": section_type,
                    "duration": section.duration,
                    "measures": section.measures,
                    "key": section.key,
                    "melody": (
                        {
                            "notes": section_melody.notes if section_melody else get_default_melody_notes(),
                            "rhythm": section_melody.rhythm if section_melody else get_default_rhythm_pattern(),
                        }
                        if section_melody
                        else None
                    ),
                    "energy_level": section.energy_level,
                    "characteristics": section.characteristics,
                }
            )

        return sections

    def _generate_title(self, request: CompositionRequest) -> str:
        """Generate a title based on the composition request."""

        # Extract key words from description
        description_words = re.findall(r"\b\w+\b", request.description.lower())

        # Filter out common words using constants
        from ..constants import TITLE_STOP_WORDS
        stop_words = TITLE_STOP_WORDS
        key_words = [word for word in description_words if word not in stop_words and len(word) > 2]

        if key_words:
            # Use first significant word and mood
            main_word = key_words[0].title()
            if request.mood:
                return f"{main_word} {request.mood.title()}"
            else:
                return f"{main_word} Song"
        else:
            # Fallback titles
            mood_titles = {
                "happy": "Joyful Melody",
                "sad": "Melancholy Blues",
                "energetic": "Driving Force",
                "calm": "Peaceful Moment",
                "dramatic": "Epic Journey",
                "romantic": "Sweet Serenade",
            }
            return mood_titles.get(request.mood, f"{request.genre.title()} Composition")

    def _generate_composition_notes(
        self, request: CompositionRequest, orchestrated_composition: Dict[str, Any]
    ) -> List[str]:
        """Generate composition and performance notes."""

        notes = [
            f"Generated from description: '{request.description}'",
            f"Genre: {request.genre}",
            f"Key: {request.key}",
            f"Tempo: {request.tempo} BPM",
            f"Target duration: {request.target_duration} seconds",
        ]

        if request.mood:
            notes.append(f"Mood: {request.mood}")

        if request.style_preferences:
            notes.append(f"Style preferences: {', '.join(request.style_preferences)}")

        # Add orchestration notes
        orchestration = orchestrated_composition.get("orchestration", {})
        if orchestration:
            texture_changes = orchestration.get("texture_changes", 0)
            notes.append(f"Applied {texture_changes} texture changes for dynamic interest")

        return notes


class CompositionAnalyzer:
    """Analyzes compositions for quality and provides improvement suggestions."""

    def __init__(self):
        self.voice_leading_optimizer = VoiceLeadingOptimizer()
        self.motif_developer = MotifDeveloper()

    def analyze_composition_quality(self, composition: CompleteComposition) -> CompositionAnalysis:
        """
        Analyze a composition for musical quality and suggest improvements.

        Args:
            composition: Complete composition to analyze

        Returns:
            Analysis of melody, harmony, rhythm, form, and improvement suggestions
        """
        try:
            # Analyze different aspects of the composition
            melody_analysis = self._analyze_melody_quality(composition.main_melody)
            harmonic_analysis = self._analyze_harmonic_quality(composition.harmonic_progression)
            rhythmic_analysis = self._analyze_rhythmic_quality(composition.main_melody)
            structural_analysis = self._analyze_form_quality(composition.song_structure)
            arrangement_analysis = self._analyze_arrangement_quality(composition.arrangement)

            # Generate overall score
            overall_score = self._calculate_overall_score(
                melody_analysis, harmonic_analysis, rhythmic_analysis, structural_analysis, arrangement_analysis
            )

            # Generate improvement suggestions
            improvement_suggestions = self._generate_improvement_suggestions(
                melody_analysis, harmonic_analysis, rhythmic_analysis, structural_analysis, arrangement_analysis
            )

            return CompositionAnalysis(
                composition_title=composition.title,
                overall_quality_score=overall_score,
                melody_analysis=melody_analysis,
                harmonic_analysis=harmonic_analysis,
                rhythmic_analysis=rhythmic_analysis,
                structural_analysis=structural_analysis,
                arrangement_analysis=arrangement_analysis,
                improvement_suggestions=improvement_suggestions,
                analysis_notes=self._generate_analysis_notes(composition),
            )

        except Exception as e:
            logger.error(f"Error analyzing composition: {e}")
            raise

    def _analyze_melody_quality(self, melody: Melody) -> Dict[str, Any]:
        """Analyze melodic quality."""
        if not melody or not melody.notes:
            return {"score": 0.0, "issues": ["No melody present"]}

        notes = melody.notes
        score_factors = []
        issues = []
        strengths = []

        # Analyze melodic range
        note_range = max(notes) - min(notes)
        if note_range < 5:
            issues.append("Very limited melodic range")
            score_factors.append(0.3)
        elif note_range > 24:
            issues.append("Extremely wide melodic range may be difficult to perform")
            score_factors.append(0.7)
        else:
            strengths.append("Good melodic range")
            score_factors.append(0.9)

        # Analyze melodic contour
        intervals = [notes[i + 1] - notes[i] for i in range(len(notes) - 1)]
        large_leaps = sum(1 for interval in intervals if abs(interval) > 7)
        leap_ratio = large_leaps / len(intervals) if intervals else 0

        if leap_ratio > 0.5:
            issues.append("Too many large melodic leaps")
            score_factors.append(0.5)
        elif leap_ratio < 0.1:
            strengths.append("Smooth melodic contour")
            score_factors.append(0.9)
        else:
            strengths.append("Balanced use of steps and leaps")
            score_factors.append(0.8)

        # Analyze melodic direction
        ascending = sum(1 for interval in intervals if interval > 0)
        descending = sum(1 for interval in intervals if interval < 0)
        direction_balance = (
            min(ascending, descending) / max(ascending, descending) if max(ascending, descending) > 0 else 0
        )

        if direction_balance > 0.6:
            strengths.append("Well-balanced melodic direction")
            score_factors.append(0.9)
        else:
            issues.append("Unbalanced melodic direction")
            score_factors.append(0.6)

        average_score = sum(score_factors) / len(score_factors) if score_factors else 0.5

        return {
            "score": average_score,
            "range": note_range,
            "leap_ratio": leap_ratio,
            "direction_balance": direction_balance,
            "issues": issues,
            "strengths": strengths,
        }

    def _analyze_harmonic_quality(self, harmony: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze harmonic quality."""
        if not harmony:
            return {"score": 0.0, "issues": ["No harmonic progression present"]}

        score_factors = []
        issues = []
        strengths = []

        # Analyze progression length
        if len(harmony) < 3:
            issues.append("Very short harmonic progression")
            score_factors.append(0.4)
        elif len(harmony) > 16:
            issues.append("Progression may be too long and complex")
            score_factors.append(0.7)
        else:
            strengths.append("Good progression length")
            score_factors.append(0.8)

        # Analyze chord variety
        unique_chords = len(set(chord.get("symbol", "C") for chord in harmony))
        variety_ratio = unique_chords / len(harmony)

        if variety_ratio > 0.8:
            strengths.append("Good harmonic variety")
            score_factors.append(0.9)
        elif variety_ratio < 0.3:
            issues.append("Limited harmonic variety")
            score_factors.append(0.5)
        else:
            score_factors.append(0.7)

        average_score = sum(score_factors) / len(score_factors) if score_factors else 0.5

        return {
            "score": average_score,
            "progression_length": len(harmony),
            "unique_chords": unique_chords,
            "variety_ratio": variety_ratio,
            "issues": issues,
            "strengths": strengths,
        }

    def _analyze_rhythmic_quality(self, melody: Melody) -> Dict[str, Any]:
        """Analyze rhythmic quality."""
        if not melody or not melody.rhythm:
            return {"score": 0.5, "issues": ["No rhythmic data available"]}

        rhythm = melody.rhythm
        score_factors = []
        issues = []
        strengths = []

        # Analyze rhythmic variety
        unique_durations = len(set(rhythm))
        variety_ratio = unique_durations / len(rhythm)

        if variety_ratio > 0.5:
            strengths.append("Good rhythmic variety")
            score_factors.append(0.9)
        elif variety_ratio < 0.2:
            issues.append("Limited rhythmic variety")
            score_factors.append(0.4)
        else:
            score_factors.append(0.7)

        # Check for extreme durations
        very_short = sum(1 for d in rhythm if d < 0.125)
        very_long = sum(1 for d in rhythm if d > 2.0)

        if very_short > len(rhythm) * 0.5:
            issues.append("Too many very short notes")
            score_factors.append(0.6)
        elif very_long > len(rhythm) * 0.3:
            issues.append("Too many very long notes")
            score_factors.append(0.6)
        else:
            strengths.append("Balanced note durations")
            score_factors.append(0.8)

        average_score = sum(score_factors) / len(score_factors) if score_factors else 0.5

        return {
            "score": average_score,
            "variety_ratio": variety_ratio,
            "unique_durations": unique_durations,
            "issues": issues,
            "strengths": strengths,
        }

    def _analyze_form_quality(self, song_structure: SongStructure) -> Dict[str, Any]:
        """Analyze song structure and form quality."""
        if not song_structure or not song_structure.sections:
            return {"score": 0.0, "issues": ["No song structure present"]}

        sections = song_structure.sections
        score_factors = []
        issues = []
        strengths = []

        # Check for essential sections
        section_types = [section.type.value for section in sections]

        if "verse" not in section_types:
            issues.append("Missing verse section")
            score_factors.append(0.5)
        else:
            strengths.append("Has verse section")
            score_factors.append(0.8)

        if "chorus" not in section_types and song_structure.genre not in ["blues", "jazz"]:
            issues.append("Missing chorus section for this genre")
            score_factors.append(0.6)
        else:
            strengths.append("Has appropriate main sections")
            score_factors.append(0.9)

        # Analyze section balance
        total_duration = sum(section.duration for section in sections)
        if total_duration < 90:
            issues.append("Song may be too short")
            score_factors.append(0.6)
        elif total_duration > 300:
            issues.append("Song may be too long")
            score_factors.append(0.7)
        else:
            strengths.append("Good overall length")
            score_factors.append(0.9)

        average_score = sum(score_factors) / len(score_factors) if score_factors else 0.5

        return {
            "score": average_score,
            "total_sections": len(sections),
            "section_types": section_types,
            "total_duration": total_duration,
            "issues": issues,
            "strengths": strengths,
        }

    def _analyze_arrangement_quality(self, arrangement: Arrangement) -> Dict[str, Any]:
        """Analyze arrangement quality."""
        if not arrangement or not arrangement.parts:
            return {"score": 0.5, "issues": ["Basic or no arrangement"]}

        score_factors = []
        issues = []
        strengths = []

        # Check instrument count
        instrument_count = len(arrangement.parts)
        if instrument_count == 1:
            issues.append("Solo arrangement - limited textural variety")
            score_factors.append(0.6)
        elif instrument_count > 8:
            issues.append("Very large ensemble - may be complex to perform")
            score_factors.append(0.7)
        else:
            strengths.append("Good ensemble size")
            score_factors.append(0.8)

        # Check for part balance (simplified analysis)
        parts_with_content = sum(1 for part in arrangement.parts.values() if len(part.notes) > 0)
        if parts_with_content == len(arrangement.parts):
            strengths.append("All parts have musical content")
            score_factors.append(0.9)
        else:
            issues.append("Some parts lack musical content")
            score_factors.append(0.6)

        average_score = sum(score_factors) / len(score_factors) if score_factors else 0.5

        return {
            "score": average_score,
            "instrument_count": instrument_count,
            "parts_with_content": parts_with_content,
            "issues": issues,
            "strengths": strengths,
        }

    def _calculate_overall_score(self, *analyses) -> float:
        """Calculate overall composition quality score."""
        scores = [analysis.get("score", 0.5) for analysis in analyses]
        return sum(scores) / len(scores) if scores else 0.5

    def _generate_improvement_suggestions(self, *analyses) -> List[str]:
        """Generate specific improvement suggestions."""
        suggestions = []

        for analysis in analyses:
            if "issues" in analysis:
                for issue in analysis["issues"]:
                    if "melodic range" in issue.lower():
                        suggestions.append("Consider expanding the melodic range to create more interest")
                    elif "harmonic" in issue.lower():
                        suggestions.append("Add more harmonic variety or complexity")
                    elif "rhythmic" in issue.lower():
                        suggestions.append("Introduce more rhythmic variety and syncopation")
                    elif "structure" in issue.lower() or "section" in issue.lower():
                        suggestions.append("Review song structure for better balance and flow")
                    elif "arrangement" in issue.lower():
                        suggestions.append("Enhance arrangement with better part writing and balance")

        # Add generic suggestions if no specific ones found
        if not suggestions:
            suggestions = [
                "Consider adding more melodic ornamentation",
                "Experiment with different harmonic progressions",
                "Try varying the rhythmic patterns",
                "Review the overall song structure and pacing",
            ]

        return list(set(suggestions))  # Remove duplicates

    def _generate_analysis_notes(self, composition: CompleteComposition) -> List[str]:
        """Generate general analysis notes."""
        notes = [
            f"Analysis of '{composition.title}' by {composition.composer}",
            f"Genre: {composition.genre}",
            f"Key: {composition.key}",
            f"Duration: {composition.duration} seconds",
            f"Structure: {len(composition.song_structure.sections)} sections",
        ]

        if composition.metadata:
            creation_method = composition.metadata.get("creation_method")
            if creation_method:
                notes.append(f"Creation method: {creation_method}")

        return notes


class CompositionRefiner:
    """Refines and improves compositions based on analysis feedback."""

    def __init__(self):
        self.melody_variator = MelodyVariator()
        self.voice_leading_optimizer = VoiceLeadingOptimizer()
        self.chromatic_harmony_generator = ChromaticHarmonyGenerator()
        self.analyzer = CompositionAnalyzer()

    def refine_composition(self, composition: CompleteComposition, focus_areas: List[str]) -> CompleteComposition:
        """
        Refine and improve specific aspects of a composition.

        Args:
            composition: Composition to refine
            focus_areas: Areas to improve (melody, harmony, rhythm, form, arrangement)

        Returns:
            Improved composition with changes documented
        """
        try:
            # Create a copy to avoid modifying the original
            refined_composition = self._deep_copy_composition(composition)
            refinement_changes = []

            # Apply refinements based on focus areas
            if "melody" in focus_areas:
                refined_composition, melody_changes = self._refine_melody(refined_composition)
                refinement_changes.extend(melody_changes)

            if "harmony" in focus_areas:
                refined_composition, harmony_changes = self._refine_harmony(refined_composition)
                refinement_changes.extend(harmony_changes)

            if "rhythm" in focus_areas:
                refined_composition, rhythm_changes = self._refine_rhythm(refined_composition)
                refinement_changes.extend(rhythm_changes)

            if "form" in focus_areas:
                refined_composition, form_changes = self._refine_form(refined_composition)
                refinement_changes.extend(form_changes)

            if "arrangement" in focus_areas:
                refined_composition, arrangement_changes = self._refine_arrangement(refined_composition)
                refinement_changes.extend(arrangement_changes)

            # Update composition notes with refinements
            refined_composition.composition_notes.extend(
                [
                    "--- Refinement Applied ---",
                    f"Focus areas: {', '.join(focus_areas)}",
                    f"Changes made: {len(refinement_changes)}",
                ]
                + refinement_changes
            )

            # Update title to indicate refinement
            if not refined_composition.title.endswith(" (Refined)"):
                refined_composition.title += " (Refined)"

            logger.info(f"Refined composition with {len(refinement_changes)} changes")
            return refined_composition

        except Exception as e:
            logger.error(f"Error refining composition: {e}")
            raise

    def _deep_copy_composition(self, composition: CompleteComposition) -> CompleteComposition:
        """Create a deep copy of the composition for refinement."""
        # For now, create a new composition with copied data
        # In a full implementation, would use proper deep copying
        return CompleteComposition(
            title=composition.title,
            composer=composition.composer,
            genre=composition.genre,
            key=composition.key,
            tempo=composition.tempo,
            time_signature=composition.time_signature,
            duration=composition.duration,
            description=composition.description,
            song_structure=composition.song_structure,
            main_melody=composition.main_melody,
            harmonic_progression=composition.harmonic_progression,
            melodic_variations=composition.melodic_variations,
            arrangement=composition.arrangement,
            sections=composition.sections,
            composition_notes=composition.composition_notes.copy(),
            metadata=composition.metadata.copy() if composition.metadata else {},
        )

    def _refine_melody(self, composition: CompleteComposition) -> Tuple[CompleteComposition, List[str]]:
        """Refine the melody."""
        changes = []

        if composition.main_melody and composition.main_melody.notes:
            # Create a variation with embellishments
            variation = self.melody_variator.create_variation(composition.main_melody.notes, "embellishment")

            # Update the main melody
            composition.main_melody.notes = variation.varied_melody.notes
            composition.main_melody.rhythm = variation.varied_melody.rhythm
            changes.append("Added melodic embellishments and variations")

            # Adjust register if needed
            note_range = max(composition.main_melody.notes) - min(composition.main_melody.notes)
            if note_range < 10:
                # Expand range by adding some octave leaps
                expanded_notes = composition.main_melody.notes.copy()
                for i in range(0, len(expanded_notes), 4):
                    if i < len(expanded_notes):
                        expanded_notes[i] += 12  # Add octave leap
                composition.main_melody.notes = expanded_notes
                changes.append("Expanded melodic range with octave variations")

        return composition, changes

    def _refine_harmony(self, composition: CompleteComposition) -> Tuple[CompleteComposition, List[str]]:
        """Refine the harmonic progression."""
        changes = []

        if composition.harmonic_progression:
            # Add chromatic harmony
            chord_symbols = [chord.get("symbol", "C") for chord in composition.harmonic_progression]
            enhanced = self.chromatic_harmony_generator.add_chromatic_harmony(chord_symbols, composition.key, "medium")

            if "enhanced_progression" in enhanced:
                composition.harmonic_progression = enhanced["enhanced_progression"]
                changes.append("Enhanced harmonic progression with chromatic elements")

        return composition, changes

    def _refine_rhythm(self, composition: CompleteComposition) -> Tuple[CompleteComposition, List[str]]:
        """Refine rhythmic elements."""
        changes = []

        if composition.main_melody and composition.main_melody.rhythm:
            # Add rhythmic syncopation
            original_rhythm = composition.main_melody.rhythm.copy()
            syncopated_rhythm = []

            for i, duration in enumerate(original_rhythm):
                if i % 4 == 1:  # Syncopate every second beat
                    syncopated_rhythm.append(duration * 1.5)
                else:
                    syncopated_rhythm.append(duration * 0.75)

            composition.main_melody.rhythm = syncopated_rhythm
            changes.append("Added rhythmic syncopation and variation")

        return composition, changes

    def _refine_form(self, composition: CompleteComposition) -> Tuple[CompleteComposition, List[str]]:
        """Refine song structure and form."""
        changes = []

        # Check if bridge is needed
        section_types = [section.type.value for section in composition.song_structure.sections]
        if "bridge" not in section_types and len(composition.song_structure.sections) > 4:
            # Could add bridge logic here
            changes.append("Analyzed form structure for potential bridge placement")

        return composition, changes

    def _refine_arrangement(self, composition: CompleteComposition) -> Tuple[CompleteComposition, List[str]]:
        """Refine arrangement and orchestration."""
        changes = []

        if composition.arrangement and composition.arrangement.parts:
            # Enhance dynamics in arrangement
            for part in composition.arrangement.parts.values():
                if len(part.dynamics) == 1:
                    # Add dynamic variation
                    part.dynamics.extend([DynamicLevel.P, DynamicLevel.F, DynamicLevel.MF])

            changes.append("Enhanced dynamic markings in arrangement")

        return composition, changes
