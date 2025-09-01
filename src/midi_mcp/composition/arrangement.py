# -*- coding: utf-8 -*-
"""
Advanced arrangement and orchestration system for Phase 5 composition features.

Provides intelligent instrument assignment, counter-melody generation,
and dynamic texture orchestration for complete musical arrangements.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import random
import logging

from ..models.composition_models import (
    Melody,
    Arrangement,
    Section,
    CounterMelody,
    TextureLevel,
    DynamicLevel,
    InstrumentPart,
    Composition,
)
from ..genres.arrangement_engine import ArrangementEngine

logger = logging.getLogger(__name__)


@dataclass
class EnsembleDefinition:
    """Defines characteristics of a musical ensemble."""

    name: str
    instruments: List[str]
    typical_ranges: Dict[str, Tuple[int, int]]  # MIDI note ranges
    texture_capabilities: List[str]
    style_characteristics: Dict[str, Any]


class EnsembleArranger:
    """Creates intelligent arrangements for specific ensembles."""

    def __init__(self):
        self.arrangement_engine = ArrangementEngine()
        self.ensembles = self._initialize_ensembles()

    def _initialize_ensembles(self) -> Dict[str, EnsembleDefinition]:
        """Initialize standard ensemble definitions."""
        return {
            "string_quartet": EnsembleDefinition(
                name="String Quartet",
                instruments=["violin_1", "violin_2", "viola", "cello"],
                typical_ranges={
                    "violin_1": (55, 103),  # G3-G7
                    "violin_2": (55, 98),  # G3-D7
                    "viola": (48, 91),  # C3-G6
                    "cello": (36, 84),  # C2-C6
                },
                texture_capabilities=["homophonic", "polyphonic", "contrapuntal"],
                style_characteristics={"voice_leading": "strict", "texture_density": "medium", "dynamic_range": "wide"},
            ),
            "jazz_combo": EnsembleDefinition(
                name="Jazz Combo",
                instruments=["piano", "bass", "drums", "trumpet", "saxophone"],
                typical_ranges={
                    "piano": (21, 108),  # A0-C8
                    "bass": (28, 67),  # E1-G4
                    "drums": (35, 81),  # Kick to cymbal
                    "trumpet": (58, 94),  # Bb3-Bb6
                    "saxophone": (49, 94),  # Db3-Bb6
                },
                texture_capabilities=["swing", "walking_bass", "comping", "solo_sections"],
                style_characteristics={
                    "voice_leading": "flexible",
                    "texture_density": "variable",
                    "dynamic_range": "moderate",
                },
            ),
            "rock_band": EnsembleDefinition(
                name="Rock Band",
                instruments=["electric_guitar", "bass_guitar", "drums", "vocals"],
                typical_ranges={
                    "electric_guitar": (40, 84),  # E2-C6
                    "bass_guitar": (28, 67),  # E1-G4
                    "drums": (35, 81),  # Kick to cymbal
                    "vocals": (60, 84),  # C4-C6
                },
                texture_capabilities=["power_chords", "riffs", "rhythmic"],
                style_characteristics={
                    "voice_leading": "loose",
                    "texture_density": "dense",
                    "dynamic_range": "high_energy",
                },
            ),
            "symphony_orchestra": EnsembleDefinition(
                name="Symphony Orchestra",
                instruments=["strings", "woodwinds", "brass", "percussion"],
                typical_ranges={
                    "strings": (28, 103),  # Full string range
                    "woodwinds": (47, 98),  # Bassoon to piccolo
                    "brass": (34, 94),  # Tuba to trumpet
                    "percussion": (28, 108),  # Full range
                },
                texture_capabilities=["orchestral", "symphonic", "massive"],
                style_characteristics={
                    "voice_leading": "sophisticated",
                    "texture_density": "very_dense",
                    "dynamic_range": "extreme",
                },
            ),
        }

    def arrange_for_ensemble(
        self, composition: Union[Dict[str, Any], Composition], ensemble_type: str, arrangement_style: str = "balanced"
    ) -> Arrangement:
        """
        Create a full arrangement for a specific ensemble.

        Args:
            composition: Base composition with melody, chords, structure
            ensemble_type: Target ensemble type
            arrangement_style: Arrangement approach

        Returns:
            Complete arrangement with parts for each instrument
        """
        try:
            if ensemble_type not in self.ensembles:
                raise ValueError(f"Unknown ensemble type: {ensemble_type}")

            ensemble = self.ensembles[ensemble_type]

            # Extract composition elements - handle both Dict and Composition types
            if isinstance(composition, dict):
                melody = composition.get("melody", {})
                harmony = composition.get("harmony", [])
                structure = composition.get("structure", {})
            else:  # Composition object
                melody = composition.melody if hasattr(composition, "melody") else {}
                harmony = composition.harmony if hasattr(composition, "harmony") else []
                structure = composition.structure if hasattr(composition, "structure") else {}

            # Create instrument parts
            instrument_parts = []

            for instrument in ensemble.instruments:
                part = self._create_instrument_part(instrument, melody, harmony, ensemble, arrangement_style)
                instrument_parts.append(part)

            # Determine overall texture and dynamics
            texture_level = self._determine_texture_level(arrangement_style, ensemble)
            dynamic_plan = self._create_dynamic_plan(structure, ensemble)

            # Convert instrument parts to dict format
            parts_dict = {}
            for part in instrument_parts:
                parts_dict[part.instrument] = part

            arrangement = Arrangement(
                parts=parts_dict,
                ensemble_type=ensemble_type,
                style=arrangement_style,
                arrangement_analysis={
                    "ensemble_name": ensemble.name,
                    "texture_level": texture_level.value,
                    "dynamic_plan": [d.value for d in dynamic_plan],
                    "performance_notes": self._generate_performance_notes(ensemble, arrangement_style),
                },
            )

            logger.info(f"Created {arrangement_style} arrangement for {ensemble.name}")
            return arrangement

        except Exception as e:
            logger.error(f"Error creating arrangement: {e}")
            raise

    def _create_instrument_part(
        self,
        instrument: str,
        melody: Dict[str, Any],
        harmony: List[Dict[str, Any]],
        ensemble: EnsembleDefinition,
        style: str,
    ) -> InstrumentPart:
        """Create a specific instrument part."""

        # Get instrument range
        note_range = ensemble.typical_ranges.get(instrument, (36, 84))

        # Determine role for this instrument
        role = self._determine_instrument_role(instrument, ensemble, style)

        # Create appropriate musical content based on role
        if role == "melody":
            notes = melody.get("notes", [60, 62, 64, 65])
            rhythm = melody.get("rhythm", [0.25] * len(notes))
        elif role == "harmony":
            notes = self._create_harmonic_part(harmony, note_range)
            rhythm = [0.5] * len(notes)
        elif role == "bass":
            notes = self._create_bass_part(harmony, note_range)
            rhythm = [0.25] * len(notes)
        elif role == "accompaniment":
            notes = self._create_accompaniment_part(harmony, note_range)
            rhythm = [0.125] * len(notes)
        else:
            # Default simple part
            notes = [note_range[0] + 12]  # Root + octave
            rhythm = [1.0]

        # Ensure notes are in range
        notes = [max(note_range[0], min(note_range[1], note)) for note in notes]

        return InstrumentPart(
            instrument=instrument,
            notes=notes,
            rhythm=rhythm,
            register="mid",
            dynamics=[DynamicLevel.MF],
            articulation=["normal"],
            style_characteristics=[f"role: {role}"],
        )

    def _determine_instrument_role(self, instrument: str, ensemble: EnsembleDefinition, style: str) -> str:
        """Determine the primary role for an instrument in the arrangement."""

        # Define typical roles by instrument
        role_map = {
            "violin_1": "melody",
            "violin_2": "harmony",
            "viola": "harmony",
            "cello": "bass",
            "piano": "harmony",
            "bass": "bass",
            "bass_guitar": "bass",
            "drums": "rhythm",
            "electric_guitar": "melody" if style == "solo" else "harmony",
            "trumpet": "melody",
            "saxophone": "melody",
            "vocals": "melody",
        }

        return role_map.get(instrument, "accompaniment")

    def _create_harmonic_part(self, harmony: List[Dict[str, Any]], note_range: Tuple[int, int]) -> List[int]:
        """Create a harmonic accompaniment part."""
        notes = []
        for chord in harmony[:4]:  # Take first 4 chords
            # Handle different chord formats
            if "root" in chord:
                root = chord.get("root", 60)
            elif "chord" in chord:
                # Convert chord symbol to MIDI note
                chord_symbol = chord.get("chord", "C")
                root = self._chord_symbol_to_root(chord_symbol)
            else:
                root = 60  # Default to middle C

            # Adjust to range and add thirds
            root = max(note_range[0], min(note_range[1] - 4, root))
            notes.extend([root, root + 4, root + 7])  # Basic triad
        return notes[:8]  # Limit length

    def _chord_symbol_to_root(self, chord_symbol: str) -> int:
        """Convert chord symbol to MIDI root note."""
        chord_roots = {
            "C": 60,
            "C#": 61,
            "Db": 61,
            "D": 62,
            "D#": 63,
            "Eb": 63,
            "E": 64,
            "F": 65,
            "F#": 66,
            "Gb": 66,
            "G": 67,
            "G#": 68,
            "Ab": 68,
            "A": 69,
            "A#": 70,
            "Bb": 70,
            "B": 71,
        }
        # Extract just the root note (ignore chord quality)
        root_note = chord_symbol[0].upper()
        if len(chord_symbol) > 1 and chord_symbol[1] in ["#", "b"]:
            root_note += chord_symbol[1]
        return chord_roots.get(root_note, 60)

    def _create_bass_part(self, harmony: List[Dict[str, Any]], note_range: Tuple[int, int]) -> List[int]:
        """Create a bass line."""
        notes = []
        for chord in harmony[:8]:  # Take more chords for bass movement
            # Handle different chord formats
            if "root" in chord:
                root = chord.get("root", 48)
            elif "chord" in chord:
                chord_symbol = chord.get("chord", "C")
                root = self._chord_symbol_to_root(chord_symbol)
            else:
                root = 48  # Default to bass C

            # Keep in bass range
            while root > note_range[1]:
                root -= 12
            while root < note_range[0]:
                root += 12
            notes.append(root)
        return notes

    def _create_accompaniment_part(self, harmony: List[Dict[str, Any]], note_range: Tuple[int, int]) -> List[int]:
        """Create an accompaniment part with arpeggiation."""
        notes = []
        for chord in harmony[:4]:
            # Handle different chord formats
            if "root" in chord:
                root = chord.get("root", 60)
            elif "chord" in chord:
                chord_symbol = chord.get("chord", "C")
                root = self._chord_symbol_to_root(chord_symbol)
            else:
                root = 60  # Default to middle C

            # Adjust to range
            root = max(note_range[0], min(note_range[1] - 8, root))
            # Create simple arpeggio
            notes.extend([root, root + 4, root + 7, root + 4])
        return notes

    def _determine_texture_level(self, style: str, ensemble: EnsembleDefinition) -> TextureLevel:
        """Determine appropriate texture density."""
        style_map = {
            "minimal": TextureLevel.THIN,
            "balanced": TextureLevel.MEDIUM,
            "full": TextureLevel.THICK,
            "dense": TextureLevel.VERY_THICK,
        }
        return style_map.get(style, TextureLevel.MEDIUM)

    def _create_dynamic_plan(self, structure: Dict[str, Any], ensemble: EnsembleDefinition) -> List[DynamicLevel]:
        """Create a dynamic plan for the arrangement."""
        if structure is None:
            sections = ["verse", "chorus"]
        else:
            sections = structure.get("sections", ["verse", "chorus"])
        dynamics = []

        for section in sections:
            if section == "verse":
                dynamics.append(DynamicLevel.MP)
            elif section == "chorus":
                dynamics.append(DynamicLevel.F)
            elif section == "bridge":
                dynamics.append(DynamicLevel.MF)
            elif section == "intro":
                dynamics.append(DynamicLevel.P)
            elif section == "outro":
                dynamics.append(DynamicLevel.PP)
            else:
                dynamics.append(DynamicLevel.MF)

        return dynamics

    def _generate_performance_notes(self, ensemble: EnsembleDefinition, style: str) -> List[str]:
        """Generate performance notes for the arrangement."""
        notes = [
            f"Arranged for {ensemble.name}",
            f"Style: {style}",
            f"Texture capabilities: {', '.join(ensemble.texture_capabilities)}",
        ]

        if ensemble.style_characteristics.get("voice_leading") == "strict":
            notes.append("Pay attention to voice leading between parts")

        return notes


class CounterMelodyGenerator:
    """Generates counter-melodies that complement main melodies."""

    def __init__(self):
        pass

    def create_counter_melodies(
        self, main_melody: List[int], harmony: List[Dict[str, Any]], instrument: str = "violin"
    ) -> CounterMelody:
        """
        Create counter-melodies that complement the main melody.

        Args:
            main_melody: Primary melodic line
            harmony: Underlying chord progression
            instrument: Target instrument

        Returns:
            Counter-melodies with proper independence and complementarity
        """
        try:
            # Analyze main melody characteristics
            melody_range = (min(main_melody), max(main_melody))
            melody_contour = self._analyze_contour(main_melody)

            # Create complementary counter-melody
            counter_notes = self._generate_counter_melody_notes(main_melody, harmony, melody_range, melody_contour)

            # Create appropriate rhythm that complements main melody
            counter_rhythm = self._generate_counter_rhythm(len(counter_notes))

            # Analyze the relationship
            independence_score = self._calculate_independence(main_melody, counter_notes)
            complementarity_score = self._calculate_complementarity(main_melody, counter_notes)

            counter_melody = CounterMelody(
                main_melody=main_melody,
                counter_notes=counter_notes,
                counter_rhythm=counter_rhythm,
                instrument=instrument,
                relationship_type="complementary",
                independence_score=independence_score,
                complementarity_score=complementarity_score,
                voice_leading_quality="good",
            )

            logger.info(f"Generated counter-melody for {instrument} with independence: {independence_score:.2f}")
            return counter_melody

        except Exception as e:
            logger.error(f"Error generating counter-melody: {e}")
            raise

    def _analyze_contour(self, melody: List[int]) -> str:
        """Analyze the melodic contour."""
        if len(melody) < 2:
            return "static"

        ups = sum(1 for i in range(1, len(melody)) if melody[i] > melody[i - 1])
        downs = sum(1 for i in range(1, len(melody)) if melody[i] < melody[i - 1])

        if ups > downs * 1.5:
            return "ascending"
        elif downs > ups * 1.5:
            return "descending"
        else:
            return "undulating"

    def _generate_counter_melody_notes(
        self, main_melody: List[int], harmony: List[Dict[str, Any]], melody_range: Tuple[int, int], contour: str
    ) -> List[int]:
        """Generate counter-melody notes."""
        counter_notes = []

        # Use contrary motion principle
        for i, main_note in enumerate(main_melody):
            # Get current chord context if available
            chord = harmony[min(i, len(harmony) - 1)] if harmony else {"root": 60}
            chord_root = chord.get("root", 60)

            # Create contrary motion
            if i > 0:
                main_interval = main_note - main_melody[i - 1]
                # Move in opposite direction
                if main_interval > 0:  # Main melody goes up
                    counter_note = counter_notes[-1] - random.randint(1, 4)
                elif main_interval < 0:  # Main melody goes down
                    counter_note = counter_notes[-1] + random.randint(1, 4)
                else:  # Main melody static
                    counter_note = counter_notes[-1] + random.choice([-2, -1, 1, 2])
            else:
                # Start in different register from main melody
                if main_note > melody_range[0] + (melody_range[1] - melody_range[0]) / 2:
                    counter_note = chord_root - 12  # Start lower
                else:
                    counter_note = chord_root + 12  # Start higher

            # Ensure it's a chord tone or passing tone
            counter_note = self._adjust_to_harmony(counter_note, chord)
            counter_notes.append(counter_note)

        return counter_notes

    def _adjust_to_harmony(self, note: int, chord: Dict[str, Any]) -> int:
        """Adjust note to fit harmony."""
        root = chord.get("root", 60)
        quality = chord.get("quality", "major")

        # Define chord tones
        if quality == "major":
            chord_tones = [0, 4, 7]  # 1, 3, 5
        elif quality == "minor":
            chord_tones = [0, 3, 7]  # 1, b3, 5
        else:
            chord_tones = [0, 4, 7]  # Default to major

        # Find closest chord tone
        note_class = note % 12
        root_class = root % 12
        interval = (note_class - root_class) % 12

        # If not a chord tone, adjust to nearest one
        if interval not in chord_tones:
            closest_tone = min(chord_tones, key=lambda x: abs(x - interval))
            adjustment = closest_tone - interval
            note += adjustment

        return note

    def _generate_counter_rhythm(self, note_count: int) -> List[float]:
        """Generate complementary rhythm for counter-melody."""
        # Create syncopated or offset rhythm
        rhythms = [0.5, 0.25, 0.25, 0.5, 0.25, 0.75]
        return (rhythms * (note_count // len(rhythms) + 1))[:note_count]

    def _calculate_independence(self, melody1: List[int], melody2: List[int]) -> float:
        """Calculate rhythmic and melodic independence between parts."""
        if len(melody1) != len(melody2):
            return 0.5

        # Check for parallel motion (reduces independence)
        parallel_motions = 0
        for i in range(1, len(melody1)):
            interval1 = melody1[i] - melody1[i - 1]
            interval2 = melody2[i] - melody2[i - 1]
            if interval1 * interval2 > 0 and abs(interval1) == abs(interval2):
                parallel_motions += 1

        independence = 1.0 - (parallel_motions / (len(melody1) - 1))
        return max(0.0, min(1.0, independence))

    def _calculate_complementarity(self, melody1: List[int], melody2: List[int]) -> float:
        """Calculate how well the melodies complement each other."""
        if len(melody1) != len(melody2):
            return 0.5

        # Check for good voice leading and harmonic intervals
        good_intervals = 0
        for note1, note2 in zip(melody1, melody2):
            interval = abs(note1 - note2) % 12
            # Good harmonic intervals: 3rd, 4th, 5th, 6th
            if interval in [3, 4, 5, 7, 8, 9]:
                good_intervals += 1

        complementarity = good_intervals / len(melody1)
        return max(0.0, min(1.0, complementarity))


class TextureOrchestrator:
    """Creates dynamic texture changes throughout compositions."""

    def orchestrate_texture_changes(self, composition: Dict[str, Any], dynamic_plan: List[str]) -> Dict[str, Any]:
        """
        Create texture changes throughout a composition for dynamic interest.

        Args:
            composition: Base composition
            dynamic_plan: Planned dynamic levels (pp, p, mp, mf, f, ff)

        Returns:
            Composition with varied textures supporting dynamic plan
        """
        try:
            # Convert dynamic plan to structured format
            dynamics = [self._parse_dynamic(d) for d in dynamic_plan]

            # Analyze composition structure
            sections = composition.get("structure", {}).get("sections", [])

            # Create texture plan
            texture_plan = self._create_texture_plan(dynamics, sections)

            # Apply textures to composition
            orchestrated_composition = self._apply_texture_changes(composition, texture_plan)

            # Add orchestration metadata
            orchestrated_composition["orchestration"] = {
                "texture_plan": texture_plan,
                "dynamic_plan": dynamic_plan,
                "texture_changes": len(texture_plan),
                "orchestration_notes": self._generate_orchestration_notes(texture_plan),
            }

            logger.info(f"Applied {len(texture_plan)} texture changes to composition")
            return orchestrated_composition

        except Exception as e:
            logger.error(f"Error orchestrating texture changes: {e}")
            raise

    def _parse_dynamic(self, dynamic_str: str) -> DynamicLevel:
        """Parse dynamic string to enum."""
        dynamic_map = {
            "pp": DynamicLevel.PP,
            "p": DynamicLevel.P,
            "mp": DynamicLevel.MP,
            "mf": DynamicLevel.MF,
            "f": DynamicLevel.F,
            "ff": DynamicLevel.FF,
        }
        return dynamic_map.get(dynamic_str.lower(), DynamicLevel.MF)

    def _create_texture_plan(
        self, dynamics: List[DynamicLevel], sections: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create a plan for texture changes."""
        texture_plan = []

        for i, (dynamic, section) in enumerate(zip(dynamics, sections)):
            texture = self._determine_texture_for_dynamic(dynamic)
            density = self._determine_density_for_section(section, dynamic)

            texture_plan.append(
                {
                    "section_index": i,
                    "section_type": section.get("type", "unknown"),
                    "dynamic_level": dynamic,
                    "texture_type": texture,
                    "density": density,
                    "orchestration_technique": self._select_orchestration_technique(texture, dynamic),
                }
            )

        return texture_plan

    def _determine_texture_for_dynamic(self, dynamic: DynamicLevel) -> TextureLevel:
        """Map dynamic level to appropriate texture."""
        texture_map = {
            DynamicLevel.PP: TextureLevel.THIN,
            DynamicLevel.P: TextureLevel.THIN,
            DynamicLevel.MP: TextureLevel.MEDIUM,
            DynamicLevel.MF: TextureLevel.MEDIUM,
            DynamicLevel.F: TextureLevel.THICK,
            DynamicLevel.FF: TextureLevel.VERY_THICK,
        }
        return texture_map.get(dynamic, TextureLevel.MEDIUM)

    def _determine_density_for_section(self, section: Dict[str, Any], dynamic: DynamicLevel) -> str:
        """Determine note density for section."""
        section_type = section.get("type", "verse")

        if dynamic in [DynamicLevel.PP, DynamicLevel.P]:
            return "sparse"
        elif section_type == "verse":
            return "moderate"
        elif section_type == "chorus":
            return "dense"
        elif section_type == "bridge":
            return "varied"
        else:
            return "moderate"

    def _select_orchestration_technique(self, texture: TextureLevel, dynamic: DynamicLevel) -> str:
        """Select appropriate orchestration technique."""
        techniques = {
            TextureLevel.THIN: ["unison", "octaves", "sparse_harmony"],
            TextureLevel.MEDIUM: ["basic_harmony", "doubling", "counterpoint"],
            TextureLevel.THICK: ["full_harmony", "multiple_doublings", "dense_counterpoint"],
            TextureLevel.VERY_THICK: ["tutti", "massive_doublings", "complex_polyphony"],
        }

        available = techniques.get(texture, ["basic_harmony"])
        return random.choice(available)

    def _apply_texture_changes(self, composition: Dict[str, Any], texture_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply the texture plan to the composition."""
        # Create a copy to avoid modifying original
        result = composition.copy()

        # Apply texture changes to each section
        sections = result.get("structure", {}).get("sections", [])

        for plan_item in texture_plan:
            section_index = plan_item["section_index"]
            if section_index < len(sections):
                sections[section_index]["texture"] = {
                    "type": plan_item["texture_type"].value,
                    "density": plan_item["density"],
                    "technique": plan_item["orchestration_technique"],
                    "dynamic_level": plan_item["dynamic_level"].value,
                }

        return result

    def _generate_orchestration_notes(self, texture_plan: List[Dict[str, Any]]) -> List[str]:
        """Generate performance notes for the orchestration."""
        notes = ["Orchestrated with dynamic texture changes:"]

        for i, plan in enumerate(texture_plan):
            note = (
                f"Section {i+1}: {plan['texture_type'].value} texture, "
                f"{plan['density']} density, {plan['orchestration_technique']}"
            )
            notes.append(note)

        return notes
