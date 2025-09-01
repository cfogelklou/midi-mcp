# -*- coding: utf-8 -*-
"""
MCP tools for Phase 5 composition features.

Provides song structure, melodic development, voice leading, arrangement,
and complete composition tools.
"""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, TextContent
import json
import logging

from ..tools.registry import ToolRegistry
from ..midi.file_ops import MidiFileManager
from ..composition.song_structure import SongStructureGenerator, SectionGenerator, TransitionCreator
from ..composition.melodic_development import MotifDeveloper, PhraseGenerator, MelodyVariator
from ..composition.voice_leading import VoiceLeadingOptimizer, ChromaticHarmonyGenerator, BassLineCreator
from ..composition.arrangement import EnsembleArranger, CounterMelodyGenerator, TextureOrchestrator
from ..composition.complete_composer import CompleteComposer, CompositionAnalyzer, CompositionRefiner
from ..models.composition_models import (
    SongStructure,
    Section,
    Transition,
    Motif,
    MelodicDevelopment,
    Phrase,
    MelodyVariation,
    VoiceLeadingAnalysis,
    Arrangement,
    CounterMelody,
    CompleteComposition,
    CompositionAnalysis,
)

logger = logging.getLogger(__name__)


def register_composition_tools(app: FastMCP, file_manager: Optional[MidiFileManager] = None) -> None:
    """
    Register all composition tools with the MCP server.

    Args:
        app: FastMCP application instance
        file_manager: Optional MIDI file manager for direct MIDI output
    """
    # Initialize composition components
    structure_generator = SongStructureGenerator()
    section_generator = SectionGenerator()
    transition_creator = TransitionCreator()
    motif_developer = MotifDeveloper()
    phrase_generator = PhraseGenerator()
    melody_variator = MelodyVariator()
    voice_leading_optimizer = VoiceLeadingOptimizer()
    chromatic_harmony_generator = ChromaticHarmonyGenerator()
    bass_line_creator = BassLineCreator()
    ensemble_arranger = EnsembleArranger()
    counter_melody_generator = CounterMelodyGenerator()
    texture_orchestrator = TextureOrchestrator()
    complete_composer = CompleteComposer()
    composition_analyzer = CompositionAnalyzer()
    composition_refiner = CompositionRefiner()

    # Song Structure Tools
    @app.tool(name="create_song_structure")
    async def create_song_structure(genre: str, song_type: str = "standard", duration: int = 180) -> List[TextContent]:
        """
        Generate a complete song structure template.

        Args:
            genre: Musical genre (affects typical structures)
            song_type: Type of song (ballad, uptempo, epic, etc.)
            duration: Target duration in seconds

        Returns:
            Song structure with sections, durations, key areas, and arrangement notes
        """
        try:
            structure = structure_generator.create_structure(genre, song_type, duration)

            # Convert to serializable format
            result = {
                "status": "success",
                "data": {
                    "genre": structure.genre,
                    "tempo": structure.tempo,
                    "time_signature": structure.time_signature,
                    "total_duration": structure.total_duration,
                    "key_plan": structure.key_plan,
                    "sections": [],
                },
            }

            # Add section details
            for section in structure.sections:
                section_data = {
                    "type": section.type.value,
                    "key": section.key,
                    "duration": section.duration,
                    "measures": section.measures,
                    "energy_level": section.energy_level,
                    "characteristics": section.characteristics,
                }
                result["data"]["sections"].append(section_data)

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error creating song structure: {e}")
            error_result = {"status": "error", "message": str(e), "genre": genre, "song_type": song_type}
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="generate_song_section")
    async def generate_song_section(
        section_type: str, genre: str, key: str, previous_section: Optional[Dict[str, Any]] = None
    ) -> List[TextContent]:
        """
        Generate a specific song section with appropriate characteristics.

        Args:
            section_type: Type of section (intro, verse, chorus, bridge, solo, outro)
            genre: Musical genre for style guidance
            key: Key signature
            previous_section: Previous section for continuity

        Returns:
            Complete section with melody, harmony, rhythm, and arrangement
        """
        try:
            # Convert previous_section dict back to Section if provided
            prev_section = None
            if previous_section:
                # This would need proper deserialization in a real implementation
                pass

            section = section_generator.generate_section(section_type, genre, key, prev_section)

            # Convert to serializable format
            result = {
                "status": "success",
                "data": {
                    "type": section.type.value,
                    "key": section.key,
                    "duration": section.duration,
                    "measures": section.measures,
                    "energy_level": section.energy_level,
                    "melody": None,
                    "harmony": section.harmony,
                    "rhythm": section.rhythm,
                    "arrangement": section.arrangement,
                },
            }

            # Add melody data if present
            if section.melody:
                result["data"]["melody"] = {
                    "notes": section.melody.notes,
                    "rhythm": section.melody.rhythm,
                    "phrase_structure": section.melody.phrase_structure,
                    "register": section.melody.register,
                }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error generating section: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "section_type": section_type,
                "genre": genre,
                "key": key,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="create_section_transitions")
    async def create_section_transitions(
        from_section: Dict[str, Any], to_section: Dict[str, Any], transition_type: str = "smooth"
    ) -> List[TextContent]:
        """
        Create musical transitions between song sections.

        Args:
            from_section: Source section
            to_section: Target section
            transition_type: Transition style (smooth, dramatic, surprise, buildup)

        Returns:
            Transition material connecting the sections
        """
        try:
            # Convert dicts to Section objects (simplified for now)
            # In a real implementation, would need proper deserialization
            from ..models.composition_models import SectionType

            from_sec = Section(
                type=SectionType(from_section.get("type", "verse")),
                key=from_section.get("key", "C major"),
                duration=from_section.get("duration", 30.0),
                measures=from_section.get("measures", 8),
                energy_level=from_section.get("energy_level", 0.5),
            )

            to_sec = Section(
                type=SectionType(to_section.get("type", "chorus")),
                key=to_section.get("key", "C major"),
                duration=to_section.get("duration", 30.0),
                measures=to_section.get("measures", 8),
                energy_level=to_section.get("energy_level", 0.7),
            )

            transition = transition_creator.create_transition(from_sec, to_sec, transition_type)

            result = {
                "status": "success",
                "data": {
                    "from_section": transition.from_section,
                    "to_section": transition.to_section,
                    "type": transition.type,
                    "duration": transition.duration,
                    "transition_material": transition.material,
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error creating transition: {e}")
            error_result = {"status": "error", "message": str(e), "transition_type": transition_type}
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    # Melodic Development Tools
    @app.tool(name="develop_melodic_motif")
    async def develop_melodic_motif(
        motif: List[int], development_techniques: List[str], target_length: int = 8
    ) -> List[TextContent]:
        """
        Develop a short melodic motif using classical development techniques.

        Args:
            motif: Original melodic motif (3-5 notes typically)
            development_techniques: Techniques to apply (sequence, inversion,
                                   retrograde, augmentation, diminution, fragmentation)
            target_length: Target length for developed melody in measures

        Returns:
            Developed melodic material with analysis of techniques used
        """
        try:
            # Create motif object
            motif_obj = Motif(notes=motif)

            # Develop the motif
            development = motif_developer.develop_motif(motif_obj, development_techniques, target_length)

            result = {
                "status": "success",
                "data": {
                    "original_motif": {
                        "notes": development.original_motif.notes,
                        "intervallic_pattern": development.original_motif.intervallic_pattern,
                    },
                    "developed_melody": {
                        "notes": development.developed_melody.notes,
                        "rhythm": development.developed_melody.rhythm,
                        "phrase_structure": development.developed_melody.phrase_structure,
                    },
                    "techniques_used": [
                        {"name": tech.name, "description": tech.description, "parameters": tech.parameters}
                        for tech in development.techniques_applied
                    ],
                    "analysis": development.analysis,
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error developing motif: {e}")
            error_result = {"status": "error", "message": str(e), "motif": motif, "techniques": development_techniques}
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="create_melodic_phrase")
    async def create_melodic_phrase(
        chord_progression: List[str], key: str, phrase_type: str = "period", style: str = "vocal"
    ) -> List[TextContent]:
        """
        Create a well-formed melodic phrase over harmony.

        Args:
            chord_progression: Underlying chord progression
            key: Key signature
            phrase_type: Phrase structure (period, sentence, phrase_group)
            style: Melodic style (vocal, instrumental, jazz, classical)

        Returns:
            Melodic phrase with proper phrasing, cadences, and structure
        """
        try:
            phrase = phrase_generator.create_phrase(chord_progression, key, phrase_type, style)

            result = {
                "status": "success",
                "data": {
                    "melody": {
                        "notes": phrase.melody.notes,
                        "rhythm": phrase.melody.rhythm,
                        "phrase_structure": phrase.melody.phrase_structure,
                        "register": phrase.melody.register,
                    },
                    "harmony": phrase.harmony,
                    "phrase_structure": {"type": phrase.structure_type, "analysis": phrase.structure_analysis},
                    "cadences": phrase.cadences,
                    "style": style,
                    "key": key,
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error creating phrase: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "chord_progression": chord_progression,
                "key": key,
                "phrase_type": phrase_type,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="vary_melody_for_repetition")
    async def vary_melody_for_repetition(
        original_melody: List[int], variation_type: str = "embellishment"
    ) -> List[TextContent]:
        """
        Create variations of a melody for repeated sections.

        Args:
            original_melody: Base melody to vary
            variation_type: Type of variation (embellishment, rhythmic,
                           harmonic, modal, ornamental)

        Returns:
            Varied melody maintaining recognizability while adding interest
        """
        try:
            variation = melody_variator.create_variation(original_melody, variation_type)

            result = {
                "status": "success",
                "data": {
                    "original_melody": variation.original_melody,
                    "varied_melody": {"notes": variation.varied_melody.notes, "rhythm": variation.varied_melody.rhythm},
                    "variation_type": variation.variation_type,
                    "similarity_score": variation.similarity_score,
                    "variation_techniques": variation.variation_techniques,
                    "analysis": {
                        "length_change": len(variation.varied_melody.notes) / len(variation.original_melody),
                        "pitch_range_original": max(variation.original_melody) - min(variation.original_melody),
                        "pitch_range_varied": max(variation.varied_melody.notes) - min(variation.varied_melody.notes),
                    },
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error creating melody variation: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "original_melody": original_melody,
                "variation_type": variation_type,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    # Advanced Harmony and Voice Leading Tools
    @app.tool(name="optimize_voice_leading")
    async def optimize_voice_leading(
        chord_progression: List[Dict[str, Any]], voice_count: int = 4
    ) -> List[TextContent]:
        """
        Optimize voice leading for a chord progression.

        Args:
            chord_progression: Chord progression with initial voicings
            voice_count: Number of voices (typically 3-6)

        Returns:
            Re-voiced progression with optimized voice leading
        """
        try:
            result = voice_leading_optimizer.optimize_voice_leading(chord_progression, voice_count)

            response = {"status": "success", "data": result}

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            logger.error(f"Error optimizing voice leading: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "chord_progression": chord_progression,
                "voice_count": voice_count,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="add_chromatic_harmony")
    async def add_chromatic_harmony(
        basic_progression: List[str], key: str, complexity: str = "medium"
    ) -> List[TextContent]:
        """
        Add chromatic harmony to a basic progression.

        Args:
            basic_progression: Simple diatonic progression
            key: Key signature
            complexity: Level of chromaticism (simple, medium, advanced)

        Returns:
            Enhanced progression with chromatic chords and voice leading
        """
        try:
            result = chromatic_harmony_generator.add_chromatic_harmony(basic_progression, key, complexity)

            response = {"status": "success", "data": result}

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            logger.error(f"Error adding chromatic harmony: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "basic_progression": basic_progression,
                "key": key,
                "complexity": complexity,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="create_bass_line_with_voice_leading")
    async def create_bass_line_with_voice_leading(
        chord_progression: List[Dict[str, Any]], style: str = "walking"
    ) -> List[TextContent]:
        """
        Create a bass line that follows proper voice leading principles.

        Args:
            chord_progression: Chord progression to follow
            style: Bass line style (simple, walking, running, pedal_point)

        Returns:
            Bass line with smooth voice leading and appropriate style
        """
        try:
            result = bass_line_creator.create_bass_line_with_voice_leading(chord_progression, style)

            response = {"status": "success", "data": result}

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            logger.error(f"Error creating bass line: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "chord_progression": chord_progression,
                "style": style,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    # Arrangement and Orchestration Tools
    @app.tool(name="arrange_for_ensemble")
    async def arrange_for_ensemble(
        composition: Dict[str, Any], ensemble_type: str, arrangement_style: str = "balanced"
    ) -> List[TextContent]:
        """
        Arrange existing composition for specific ensemble.

        Args:
            composition: Base composition (melody, chords, structure)
            ensemble_type: Target ensemble (string_quartet, jazz_combo, rock_band, symphony_orchestra)
            arrangement_style: Arrangement approach (minimal, balanced, full, dense)

        Returns:
            Full arrangement with parts for each instrument
        """
        try:
            arrangement = ensemble_arranger.arrange_for_ensemble(composition, ensemble_type, arrangement_style)

            result = {
                "status": "success",
                "data": {
                    "ensemble_type": arrangement.ensemble_type,
                    "instruments": arrangement.instruments,
                    "texture_level": arrangement.texture_level.value,
                    "dynamic_plan": [d.value for d in arrangement.dynamic_plan],
                    "style_notes": arrangement.style_notes,
                    "performance_notes": arrangement.performance_notes,
                    "instrument_parts": [],
                },
            }

            # Add instrument parts
            for part in arrangement.instrument_parts:
                part_data = {
                    "instrument": part.instrument,
                    "role": part.role,
                    "notes": part.notes,
                    "rhythm": part.rhythm,
                    "dynamics": part.dynamics,
                    "articulation": part.articulation,
                    "playing_techniques": part.playing_techniques,
                }
                result["data"]["instrument_parts"].append(part_data)

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error arranging for ensemble: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "composition": composition,
                "ensemble_type": ensemble_type,
                "arrangement_style": arrangement_style,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="create_counter_melodies")
    async def create_counter_melodies(
        main_melody: List[int], harmony: List[Dict[str, Any]], instrument: str = "violin"
    ) -> List[TextContent]:
        """
        Create counter-melodies that complement the main melody.

        Args:
            main_melody: Primary melodic line
            harmony: Underlying chord progression
            instrument: Target instrument for counter-melody

        Returns:
            Counter-melodies with proper independence and complementarity
        """
        try:
            counter_melody = counter_melody_generator.create_counter_melodies(main_melody, harmony, instrument)

            result = {
                "status": "success",
                "data": {
                    "main_melody": counter_melody.main_melody,
                    "counter_notes": counter_melody.counter_notes,
                    "counter_rhythm": counter_melody.counter_rhythm,
                    "instrument": counter_melody.instrument,
                    "relationship_type": counter_melody.relationship_type,
                    "independence_score": counter_melody.independence_score,
                    "complementarity_score": counter_melody.complementarity_score,
                    "voice_leading_quality": counter_melody.voice_leading_quality,
                    "analysis": {
                        "main_melody_range": f"{min(main_melody)}-{max(main_melody)}",
                        "counter_melody_range": f"{min(counter_melody.counter_notes)}-{max(counter_melody.counter_notes)}",
                        "total_notes": len(counter_melody.counter_notes),
                    },
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error creating counter-melodies: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "main_melody": main_melody,
                "harmony": harmony,
                "instrument": instrument,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="orchestrate_texture_changes")
    async def orchestrate_texture_changes(composition: Dict[str, Any], dynamic_plan: List[str]) -> List[TextContent]:
        """
        Create texture changes throughout a composition for dynamic interest.

        Args:
            composition: Base composition
            dynamic_plan: Planned dynamic levels (pp, p, mp, mf, f, ff)

        Returns:
            Composition with varied textures supporting dynamic plan
        """
        try:
            orchestrated_composition = texture_orchestrator.orchestrate_texture_changes(composition, dynamic_plan)

            result = {"status": "success", "data": orchestrated_composition}

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error orchestrating texture changes: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "composition": composition,
                "dynamic_plan": dynamic_plan,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    # Complete Composition Tools
    @app.tool(name="compose_complete_song")
    async def compose_complete_song(
        description: str,
        genre: str,
        key: str,
        tempo: int,
        target_duration: int = 180,
        ensemble_type: str = "piano_solo",
        create_midi_file: bool = False,
    ) -> List[TextContent]:
        """
        Generate a complete musical composition from a text description.

        Args:
            description: Text description of desired composition
            genre: Musical genre/style
            key: Key signature
            tempo: Tempo in BPM
            target_duration: Target length in seconds
            ensemble_type: Type of ensemble arrangement
            create_midi_file: If True, creates a MIDI file with the composition

        Returns:
            Complete composition with all sections, arrangements, and details.
            If create_midi_file=True, returns MIDI file ID instead of abstract data.
        """
        try:
            composition = complete_composer.compose_complete_song(
                description, genre, key, tempo, target_duration, ensemble_type
            )

            # If MIDI file creation is requested and file manager is available
            if create_midi_file and file_manager:
                try:
                    # Create a new MIDI file with the composition details
                    midi_file_id = file_manager.create_midi_file(
                        title=composition.title,
                        tempo=composition.tempo,
                        time_signature=(4, 4),  # Default to 4/4
                        key_signature=composition.key.split()[0] if " " in composition.key else composition.key
                    )
                    
                    # Convert composition data to MIDI notes for main melody
                    if hasattr(composition, 'main_melody') and composition.main_melody:
                        melody_notes = []
                        current_time = 0.0
                        default_duration = 0.5  # Half beat per note
                        
                        for note_midi in composition.main_melody.notes:
                            melody_notes.append({
                                "note": note_midi,
                                "velocity": 80,
                                "start_time": current_time,
                                "duration": default_duration
                            })
                            current_time += default_duration
                        
                        # Add melody track
                        file_manager.add_track(
                            midi_file_id=midi_file_id,
                            track_name="Melody",
                            channel=0,
                            program=0  # Acoustic Grand Piano
                        )
                        
                        file_manager.add_notes_to_track(
                            midi_file_id=midi_file_id,
                            track_identifier="Melody",
                            notes_data=melody_notes,
                            channel=0
                        )
                    
                    # Convert harmonic progression to chords if available
                    if hasattr(composition, 'harmonic_progression') and composition.harmonic_progression:
                        harmony_notes = []
                        current_time = 0.0
                        chord_duration = 2.0  # 2 beats per chord
                        
                        for chord_symbol in composition.harmonic_progression:
                            # Simple chord mapping (C major triad as example)
                            # This would need proper chord symbol parsing in a real implementation
                            if chord_symbol.startswith('C'):
                                chord_notes = [60, 64, 67]  # C major triad
                            elif chord_symbol.startswith('F'):
                                chord_notes = [65, 69, 72]  # F major triad
                            elif chord_symbol.startswith('G'):
                                chord_notes = [67, 71, 74]  # G major triad
                            else:
                                chord_notes = [60, 64, 67]  # Default C major
                                
                            for note in chord_notes:
                                harmony_notes.append({
                                    "note": note,
                                    "velocity": 60,
                                    "start_time": current_time,
                                    "duration": chord_duration
                                })
                            current_time += chord_duration
                        
                        if harmony_notes:
                            # Add harmony track
                            file_manager.add_track(
                                midi_file_id=midi_file_id,
                                track_name="Harmony",
                                channel=1,
                                program=0  # Acoustic Grand Piano
                            )
                            
                            file_manager.add_notes_to_track(
                                midi_file_id=midi_file_id,
                                track_identifier="Harmony",
                                notes_data=harmony_notes,
                                channel=1
                            )
                    
                    return [TextContent(
                        type="text",
                        text=f"Created complete composition and MIDI file!\n"
                             f"Title: {composition.title}\n"
                             f"MIDI File ID: {midi_file_id}\n"
                             f"Genre: {composition.genre}\n"
                             f"Key: {composition.key}\n"
                             f"Tempo: {composition.tempo} BPM\n"
                             f"Duration: {composition.duration} seconds\n"
                             f"Description: {composition.description}\n"
                             f"Tracks created: Melody, Harmony"
                    )]
                    
                except Exception as midi_error:
                    # Fall back to returning abstract data if MIDI creation fails
                    return [TextContent(type="text", text=f"Created composition but failed to create MIDI file: {str(midi_error)}")]

            # Return abstract data (original behavior)
            result = {
                "status": "success",
                "data": {
                    "title": composition.title,
                    "composer": composition.composer,
                    "genre": composition.genre,
                    "key": composition.key,
                    "tempo": composition.tempo,
                    "duration": composition.duration,
                    "description": composition.description,
                    "song_structure": {
                        "genre": composition.song_structure.genre,
                        "tempo": composition.song_structure.tempo,
                        "total_duration": composition.song_structure.total_duration,
                        "sections": [
                            {
                                "type": section.type.value,
                                "duration": section.duration,
                                "measures": section.measures,
                                "energy_level": section.energy_level,
                            }
                            for section in composition.song_structure.sections
                        ],
                    },
                    "main_melody": {
                        "notes": composition.main_melody.notes,
                        "rhythm": composition.main_melody.rhythm,
                        "register": composition.main_melody.register,
                    },
                    "harmonic_progression": composition.harmonic_progression,
                    "arrangement": {
                        "ensemble_type": composition.arrangement.ensemble_type,
                        "style": composition.arrangement.style,
                        "parts": list(composition.arrangement.parts.keys()),
                    },
                    "sections": composition.sections,
                    "composition_notes": composition.composition_notes,
                    "metadata": composition.metadata,
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error composing complete song: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "description": description,
                "genre": genre,
                "key": key,
                "tempo": tempo,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="analyze_composition_quality")
    async def analyze_composition_quality(composition: Dict[str, Any]) -> List[TextContent]:
        """
        Analyze a composition for musical quality and suggest improvements.

        Args:
            composition: Complete composition to analyze

        Returns:
            Analysis of melody, harmony, rhythm, form, and improvement suggestions
        """
        try:
            # Convert dict to CompleteComposition object (simplified)
            # In a real implementation, would need proper deserialization
            complete_comp = CompleteComposition(
                title=composition.get("title", "Untitled"),
                composer=composition.get("composer", "Unknown"),
                genre=composition.get("genre", "unknown"),
                key=composition.get("key", "C major"),
                tempo=composition.get("tempo", 120),
                time_signature=(4, 4),
                duration=composition.get("duration", 180),
                description=composition.get("description", ""),
                song_structure=composition.get("song_structure"),
                main_melody=composition.get("main_melody"),
                harmonic_progression=composition.get("harmonic_progression", []),
                melodic_variations=composition.get("melodic_variations", {}),
                arrangement=composition.get("arrangement"),
                sections=composition.get("sections", []),
                composition_notes=composition.get("composition_notes", []),
                metadata=composition.get("metadata", {}),
            )

            analysis = composition_analyzer.analyze_composition_quality(complete_comp)

            result = {
                "status": "success",
                "data": {
                    "composition_title": analysis.composition_title,
                    "overall_quality_score": analysis.overall_quality_score,
                    "melody_analysis": analysis.melody_analysis,
                    "harmonic_analysis": analysis.harmonic_analysis,
                    "rhythmic_analysis": analysis.rhythmic_analysis,
                    "structural_analysis": analysis.structural_analysis,
                    "arrangement_analysis": analysis.arrangement_analysis,
                    "improvement_suggestions": analysis.improvement_suggestions,
                    "analysis_notes": analysis.analysis_notes,
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error analyzing composition: {e}")
            error_result = {"status": "error", "message": str(e), "composition": composition}
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    @app.tool(name="refine_composition")
    async def refine_composition(composition: Dict[str, Any], focus_areas: List[str]) -> List[TextContent]:
        """
        Refine and improve specific aspects of a composition.

        Args:
            composition: Composition to refine
            focus_areas: Areas to improve (melody, harmony, rhythm, form, arrangement)

        Returns:
            Improved composition with changes documented
        """
        try:
            # Convert dict to CompleteComposition object (simplified)
            complete_comp = CompleteComposition(
                title=composition.get("title", "Untitled"),
                composer=composition.get("composer", "Unknown"),
                genre=composition.get("genre", "unknown"),
                key=composition.get("key", "C major"),
                tempo=composition.get("tempo", 120),
                time_signature=(4, 4),
                duration=composition.get("duration", 180),
                description=composition.get("description", ""),
                song_structure=composition.get("song_structure"),
                main_melody=composition.get("main_melody"),
                harmonic_progression=composition.get("harmonic_progression", []),
                melodic_variations=composition.get("melodic_variations", {}),
                arrangement=composition.get("arrangement"),
                sections=composition.get("sections", []),
                composition_notes=composition.get("composition_notes", []),
                metadata=composition.get("metadata", {}),
            )

            refined_composition = composition_refiner.refine_composition(complete_comp, focus_areas)

            result = {
                "status": "success",
                "data": {
                    "title": refined_composition.title,
                    "composer": refined_composition.composer,
                    "genre": refined_composition.genre,
                    "key": refined_composition.key,
                    "tempo": refined_composition.tempo,
                    "duration": refined_composition.duration,
                    "description": refined_composition.description,
                    "main_melody": {
                        "notes": refined_composition.main_melody.notes,
                        "rhythm": refined_composition.main_melody.rhythm,
                        "register": refined_composition.main_melody.register,
                    },
                    "harmonic_progression": refined_composition.harmonic_progression,
                    "composition_notes": refined_composition.composition_notes,
                    "focus_areas": focus_areas,
                    "refinements_applied": len(
                        [note for note in refined_composition.composition_notes if "Refinement" in note]
                    ),
                },
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Error refining composition: {e}")
            error_result = {
                "status": "error",
                "message": str(e),
                "composition": composition,
                "focus_areas": focus_areas,
            }
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]
