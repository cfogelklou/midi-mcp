# -*- coding: utf-8 -*-
"""
Advanced harmony and voice leading optimization tools.

Builds on existing voice leading system with sophisticated optimization
and chromatic harmony generation using music21.
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from ..models.composition_models import VoiceLeadingAnalysis
from ..models.theory_models import Chord, Note
from ..theory.voice_leading import VoiceLeadingManager
from ..theory.chords import ChordManager
from ..genres.library_integration import LibraryIntegration


class VoiceLeadingOptimizer:
    """Optimizes voice leading for chord progressions."""

    def __init__(self):
        """Initialize with existing voice leading tools."""
        self.voice_leading_manager = VoiceLeadingManager()
        self.chord_manager = ChordManager()
        self.libraries = LibraryIntegration()

    def optimize_voice_leading(self, chord_progression: List[Dict[str, Any]], voice_count: int = 4) -> Dict[str, Any]:
        """
        Optimize voice leading for a chord progression.

        Args:
            chord_progression: Chord progression with initial voicings
            voice_count: Number of voices (typically 3-6)

        Returns:
            Re-voiced progression with optimized voice leading
        """
        optimized_progression = []
        total_motion = 0
        voice_leading_moves = []

        # If first chord doesn't have voicing, create one
        if not chord_progression[0].get("voicing"):
            first_voicing = self._create_initial_voicing(chord_progression[0]["chord"], voice_count)
            chord_progression[0]["voicing"] = first_voicing

        optimized_progression.append(chord_progression[0])

        # Optimize each subsequent chord
        for i in range(1, len(chord_progression)):
            current_chord = chord_progression[i]
            previous_voicing = optimized_progression[-1]["voicing"]

            # Generate optimal voicing for current chord
            optimal_voicing, motion = self._optimize_single_voicing(
                current_chord["chord"], previous_voicing, voice_count
            )

            # Create optimized chord entry
            optimized_chord = dict(current_chord)
            optimized_chord["voicing"] = optimal_voicing
            optimized_progression.append(optimized_chord)

            # Track voice leading
            total_motion += motion
            voice_leading_moves.append(
                {
                    "from_chord": optimized_progression[-2]["chord"],
                    "to_chord": current_chord["chord"],
                    "motion": motion,
                    "voice_movements": self._calculate_voice_movements(previous_voicing, optimal_voicing),
                }
            )

        # Analyze final result
        analysis = self._analyze_optimized_progression(optimized_progression, total_motion)

        return {
            "optimized_progression": optimized_progression,
            "voice_leading_analysis": analysis,
            "total_motion": total_motion,
            "voice_leading_moves": voice_leading_moves,
            "optimization_score": self._calculate_optimization_score(total_motion, len(chord_progression)),
        }

    def _create_initial_voicing(self, chord_symbol: str, voice_count: int) -> List[int]:
        """Create initial voicing for the first chord."""
        # Get chord tones (simplified - could use chord_manager for more sophistication)
        base_notes = self._get_basic_chord_tones(chord_symbol)

        # Distribute across voices with appropriate spacing
        voicing = []
        octave_offset = 48  # Start around C3

        for i in range(voice_count):
            if i < len(base_notes):
                note = base_notes[i % len(base_notes)]
                # Add octave displacement for upper voices
                octave = i // len(base_notes)
                voicing.append(note + octave_offset + (octave * 12))
            else:
                # Double some notes for additional voices
                note = base_notes[i % len(base_notes)]
                voicing.append(note + octave_offset + 12)  # Up an octave

        return sorted(voicing)

    def _get_basic_chord_tones(self, chord_symbol: str) -> List[int]:
        """Get basic chord tones for a chord symbol."""
        # Simplified chord tone mapping - could be enhanced with chord_manager
        basic_chords = {
            "C": [0, 4, 7],  # C major
            "Cm": [0, 3, 7],  # C minor
            "C7": [0, 4, 7, 10],  # C dominant 7
            "Cmaj7": [0, 4, 7, 11],  # C major 7
            "F": [5, 9, 0],  # F major (using inversions)
            "G": [7, 11, 2],  # G major
            "Am": [9, 0, 4],  # A minor
            "Dm": [2, 5, 9],  # D minor
            "Em": [4, 7, 11],  # E minor
        }

        return basic_chords.get(chord_symbol, [0, 4, 7])  # Default to C major

    def _optimize_single_voicing(
        self, chord_symbol: str, previous_voicing: List[int], voice_count: int
    ) -> Tuple[List[int], int]:
        """Optimize voicing for a single chord given the previous voicing."""
        chord_tones = self._get_basic_chord_tones(chord_symbol)

        # Generate several possible voicings
        candidate_voicings = []

        for _ in range(10):  # Try 10 different voicings
            voicing = self._generate_candidate_voicing(chord_tones, previous_voicing, voice_count)
            motion = self._calculate_total_motion(previous_voicing, voicing)
            candidate_voicings.append((voicing, motion))

        # Choose the voicing with minimal motion
        best_voicing, best_motion = min(candidate_voicings, key=lambda x: x[1])

        return best_voicing, best_motion

    def _generate_candidate_voicing(
        self, chord_tones: List[int], previous_voicing: List[int], voice_count: int
    ) -> List[int]:
        """Generate a candidate voicing for optimization."""
        voicing = []

        for i, prev_note in enumerate(previous_voicing):
            if i >= voice_count:
                break

            # Find closest chord tone to previous note
            best_note = prev_note
            best_distance = float("inf")

            # Try chord tones in multiple octaves
            for octave in [-1, 0, 1]:  # Try octave below, same, above
                for chord_tone in chord_tones:
                    candidate = chord_tone + (prev_note // 12) * 12 + (octave * 12)
                    distance = abs(candidate - prev_note)

                    if distance < best_distance:
                        best_distance = distance
                        best_note = candidate

            voicing.append(best_note)

        # Fill remaining voices if needed
        while len(voicing) < voice_count:
            # Add doubled notes in appropriate octaves
            base_note = random.choice(chord_tones)
            octave = (len(voicing) // len(chord_tones)) + 4
            voicing.append(base_note + octave * 12)

        return sorted(voicing)

    def _calculate_total_motion(self, voicing1: List[int], voicing2: List[int]) -> int:
        """Calculate total semitone motion between voicings."""
        total = 0
        for i in range(min(len(voicing1), len(voicing2))):
            total += abs(voicing2[i] - voicing1[i])
        return total

    def _calculate_voice_movements(self, prev_voicing: List[int], current_voicing: List[int]) -> List[Dict[str, int]]:
        """Calculate individual voice movements."""
        movements = []
        for i in range(min(len(prev_voicing), len(current_voicing))):
            movements.append(
                {
                    "voice": i + 1,
                    "from": prev_voicing[i],
                    "to": current_voicing[i],
                    "interval": current_voicing[i] - prev_voicing[i],
                }
            )
        return movements

    def _analyze_optimized_progression(self, progression: List[Dict[str, Any]], total_motion: int) -> Dict[str, Any]:
        """Analyze the quality of the optimized progression."""
        # Count motion types
        parallel_motion_count = 0
        contrary_motion_count = 0
        oblique_motion_count = 0

        # Analyze consecutive chord pairs
        for i in range(len(progression) - 1):
            voicing1 = progression[i]["voicing"]
            voicing2 = progression[i + 1]["voicing"]

            # Simple motion analysis
            motions = []
            for j in range(min(len(voicing1), len(voicing2))):
                if voicing2[j] > voicing1[j]:
                    motions.append("up")
                elif voicing2[j] < voicing1[j]:
                    motions.append("down")
                else:
                    motions.append("static")

            # Categorize motion type
            if all(m == motions[0] for m in motions):
                parallel_motion_count += 1
            elif any(m1 != m2 for m1, m2 in zip(motions[:-1], motions[1:])):
                contrary_motion_count += 1
            else:
                oblique_motion_count += 1

        # Calculate smoothness score
        chord_count = len(progression) - 1
        smoothness_score = max(0.0, 1.0 - (total_motion / (chord_count * 20)))  # Normalize

        return {
            "total_motion": total_motion,
            "parallel_motion_count": parallel_motion_count,
            "contrary_motion_count": contrary_motion_count,
            "oblique_motion_count": oblique_motion_count,
            "smoothness_score": smoothness_score,
            "average_motion_per_chord": total_motion / chord_count if chord_count > 0 else 0,
        }

    def _calculate_optimization_score(self, total_motion: int, chord_count: int) -> float:
        """Calculate overall optimization score (0-1, higher is better)."""
        if chord_count <= 1:
            return 1.0

        # Lower motion is better
        avg_motion = total_motion / (chord_count - 1)
        # Score decreases as motion increases, with 3 semitones being optimal
        if avg_motion <= 3:
            return 1.0
        else:
            return max(0.0, 1.0 - ((avg_motion - 3) / 10))


class ChromaticHarmonyGenerator:
    """Generates chromatic harmony enhancements."""

    def __init__(self):
        """Initialize chromatic harmony generator."""
        self.libraries = LibraryIntegration()
        self.chord_manager = ChordManager()

    def add_chromatic_harmony(
        self, basic_progression: List[str], key: str, complexity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Add chromatic harmony to a basic progression.

        Args:
            basic_progression: Simple diatonic progression
            key: Key signature
            complexity: Level of chromaticism (simple, medium, advanced)

        Returns:
            Enhanced progression with chromatic chords and voice leading
        """
        enhanced_progression = []
        chromatic_elements = []

        complexity_settings = {
            "simple": {"secondary_dominants": 0.3, "applied_chords": 0.1, "modal_mixture": 0.1},
            "medium": {"secondary_dominants": 0.5, "applied_chords": 0.3, "modal_mixture": 0.2},
            "advanced": {"secondary_dominants": 0.7, "applied_chords": 0.5, "modal_mixture": 0.4},
        }

        settings = complexity_settings.get(complexity, complexity_settings["medium"])

        for i, chord in enumerate(basic_progression):
            # Add the original chord
            enhanced_progression.append({"chord": chord, "function": "diatonic"})

            # Consider adding chromatic harmony before next chord
            if i < len(basic_progression) - 1:
                next_chord = basic_progression[i + 1]

                # Try to add secondary dominant
                if random.random() < settings["secondary_dominants"]:
                    secondary_dom = self._create_secondary_dominant(next_chord, key)
                    if secondary_dom:
                        enhanced_progression.append(
                            {"chord": secondary_dom, "function": "secondary_dominant", "resolves_to": next_chord}
                        )
                        chromatic_elements.append(
                            {
                                "type": "secondary_dominant",
                                "chord": secondary_dom,
                                "position": len(enhanced_progression) - 1,
                            }
                        )

                # Try to add applied chord
                elif random.random() < settings["applied_chords"]:
                    applied = self._create_applied_chord(chord, next_chord, key)
                    if applied:
                        enhanced_progression.append({"chord": applied, "function": "applied_chord"})
                        chromatic_elements.append(
                            {"type": "applied_chord", "chord": applied, "position": len(enhanced_progression) - 1}
                        )

        # Add modal mixture elements
        if random.random() < settings["modal_mixture"]:
            enhanced_progression = self._add_modal_mixture(enhanced_progression, key)

        return {
            "enhanced_progression": enhanced_progression,
            "chromatic_elements": chromatic_elements,
            "complexity_level": complexity,
            "original_progression": basic_progression,
            "harmonic_analysis": self._analyze_harmonic_content(enhanced_progression),
        }

    def _create_secondary_dominant(self, target_chord: str, key: str) -> Optional[str]:
        """Create secondary dominant chord."""
        # Simplified secondary dominant creation
        secondary_dominants = {
            "ii": "V/ii",  # A7 in C major
            "iii": "V/iii",  # B7 in C major
            "vi": "V/vi",  # E7 in C major
            "V": "V/V",  # D7 in C major
        }

        return secondary_dominants.get(target_chord)

    def _create_applied_chord(self, from_chord: str, to_chord: str, key: str) -> Optional[str]:
        """Create applied chord (diminished or other)."""
        # Simplified applied chord creation
        if from_chord == "I" and to_chord == "vi":
            return "#ivo7"  # Diminished chord between I and vi
        elif from_chord == "vi" and to_chord == "IV":
            return "viio7/V"  # Applied diminished
        return None

    def _add_modal_mixture(self, progression: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        """Add modal mixture elements."""
        # Find a good spot to add modal mixture (simplified)
        for i, chord_info in enumerate(progression):
            if chord_info["chord"] == "I" and random.random() < 0.5:
                # Change major I to minor i
                progression[i] = {"chord": "i", "function": "modal_mixture", "borrowed_from": "minor"}
                break

        return progression

    def _analyze_harmonic_content(self, progression: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze harmonic content of enhanced progression."""
        functions = {}
        for chord_info in progression:
            function = chord_info.get("function", "unknown")
            functions[function] = functions.get(function, 0) + 1

        return {
            "chord_count": len(progression),
            "function_distribution": functions,
            "chromaticism_percentage": (
                functions.get("secondary_dominant", 0)
                + functions.get("applied_chord", 0)
                + functions.get("modal_mixture", 0)
            )
            / len(progression),
        }


class BassLineCreator:
    """Creates bass lines with proper voice leading."""

    def __init__(self):
        """Initialize bass line creator."""
        self.voice_leading_optimizer = VoiceLeadingOptimizer()

    def create_bass_line_with_voice_leading(
        self, chord_progression: List[Dict[str, Any]], style: str = "walking"
    ) -> Dict[str, Any]:
        """
        Create bass line that follows proper voice leading principles.

        Args:
            chord_progression: Chord progression to follow
            style: Bass line style (simple, walking, running, pedal_point)

        Returns:
            Bass line with smooth voice leading and appropriate style
        """
        bass_notes = []
        rhythm = []

        if style == "walking":
            bass_notes, rhythm = self._create_walking_bass(chord_progression)
        elif style == "running":
            bass_notes, rhythm = self._create_running_bass(chord_progression)
        elif style == "pedal_point":
            bass_notes, rhythm = self._create_pedal_point_bass(chord_progression)
        else:  # simple
            bass_notes, rhythm = self._create_simple_bass(chord_progression)

        # Analyze voice leading quality
        voice_leading_quality = self._analyze_bass_voice_leading(bass_notes)

        return {
            "bass_notes": bass_notes,
            "rhythm": rhythm,
            "style": style,
            "voice_leading_quality": voice_leading_quality,
            "harmonic_support": self._analyze_harmonic_support(bass_notes, chord_progression),
        }

    def _create_walking_bass(self, progression: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        """Create walking bass line."""
        bass_notes = []
        rhythm = []

        for i, chord_info in enumerate(progression):
            chord = chord_info["chord"]
            duration = chord_info.get("duration", 4)

            # Get root of chord (simplified)
            root_note = self._get_chord_root(chord) + 36  # Bass register (around C2)

            # Walking bass: root on beat 1, then walk to next chord
            bass_notes.append(root_note)
            rhythm.append(1.0)  # Quarter note

            # Add walking notes for remaining beats
            beats_remaining = int(duration - 1)
            if beats_remaining > 0 and i < len(progression) - 1:
                next_root = self._get_chord_root(progression[i + 1]["chord"]) + 36
                walking_notes = self._create_walking_notes(root_note, next_root, beats_remaining)
                bass_notes.extend(walking_notes)
                rhythm.extend([1.0] * len(walking_notes))

        return bass_notes, rhythm

    def _create_simple_bass(self, progression: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        """Create simple bass line (roots only)."""
        bass_notes = []
        rhythm = []

        for chord_info in progression:
            chord = chord_info["chord"]
            duration = chord_info.get("duration", 4)

            root_note = self._get_chord_root(chord) + 36  # Bass register
            bass_notes.append(root_note)
            rhythm.append(duration)

        return bass_notes, rhythm

    def _create_running_bass(self, progression: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        """Create running bass line (eighth notes)."""
        bass_notes = []
        rhythm = []

        for chord_info in progression:
            chord = chord_info["chord"]
            duration = chord_info.get("duration", 4)

            # Get chord tones
            chord_tones = self._get_chord_tones_for_bass(chord)

            # Fill duration with eighth notes
            notes_needed = int(duration * 2)  # Eighth notes
            for j in range(notes_needed):
                note = chord_tones[j % len(chord_tones)] + 36
                bass_notes.append(note)
                rhythm.append(0.5)  # Eighth note

        return bass_notes, rhythm

    def _create_pedal_point_bass(self, progression: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        """Create pedal point bass (sustained note)."""
        if not progression:
            return [], []

        # Use root of first chord as pedal point
        pedal_note = self._get_chord_root(progression[0]["chord"]) + 36

        # Calculate total duration
        total_duration = sum(chord_info.get("duration", 4) for chord_info in progression)

        return [pedal_note], [total_duration]

    def _get_chord_root(self, chord_symbol: str) -> int:
        """Get root note of chord (in semitones from C)."""
        roots = {
            "C": 0,
            "Cm": 0,
            "C7": 0,
            "Cmaj7": 0,
            "F": 5,
            "Fm": 5,
            "F7": 5,
            "Fmaj7": 5,
            "G": 7,
            "Gm": 7,
            "G7": 7,
            "Gmaj7": 7,
            "Am": 9,
            "A": 9,
            "A7": 9,
            "Amaj7": 9,
            "Dm": 2,
            "D": 2,
            "D7": 2,
            "Dmaj7": 2,
            "Em": 4,
            "E": 4,
            "E7": 4,
            "Emaj7": 4,
            "Bm": 11,
            "B": 11,
            "B7": 11,
            "Bmaj7": 11,
        }

        # Extract root from chord symbol
        for chord_name, root in roots.items():
            if chord_symbol.startswith(chord_name):
                return root

        return 0  # Default to C

    def _get_chord_tones_for_bass(self, chord_symbol: str) -> List[int]:
        """Get chord tones for bass line."""
        root = self._get_chord_root(chord_symbol)

        if "m" in chord_symbol and "maj" not in chord_symbol:
            return [root, root + 3, root + 7]  # Minor triad
        else:
            return [root, root + 4, root + 7]  # Major triad

    def _create_walking_notes(self, from_note: int, to_note: int, num_notes: int) -> List[int]:
        """Create walking notes between two bass notes."""
        if num_notes <= 0:
            return []
        if num_notes == 1:
            return [from_note + (1 if to_note > from_note else -1)]

        # Create chromatic or scalar walking line
        notes = []
        interval = to_note - from_note
        step_size = interval // (num_notes + 1)

        for i in range(num_notes):
            note = from_note + step_size * (i + 1)
            notes.append(note)

        return notes

    def _analyze_bass_voice_leading(self, bass_notes: List[int]) -> Dict[str, Any]:
        """Analyze voice leading quality of bass line."""
        if len(bass_notes) < 2:
            return {"smoothness_score": 1.0, "average_interval": 0.0, "large_leaps": 0}

        intervals = []
        large_leaps = 0

        for i in range(len(bass_notes) - 1):
            interval = abs(bass_notes[i + 1] - bass_notes[i])
            intervals.append(interval)
            if interval > 4:  # Larger than major third
                large_leaps += 1

        avg_interval = sum(intervals) / len(intervals)
        smoothness_score = max(0.0, 1.0 - (avg_interval / 12))  # Normalize to 0-1

        return {
            "smoothness_score": smoothness_score,
            "average_interval": avg_interval,
            "large_leaps": large_leaps,
            "total_motion": sum(intervals),
        }

    def _analyze_harmonic_support(
        self, bass_notes: List[int], chord_progression: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze how well bass supports harmony."""
        # Simplified analysis
        root_support = 0
        total_chords = len(chord_progression)

        bass_idx = 0
        for chord_info in chord_progression:
            if bass_idx < len(bass_notes):
                chord_root = self._get_chord_root(chord_info["chord"])
                bass_note = bass_notes[bass_idx] % 12  # Reduce to pitch class

                if bass_note == chord_root:
                    root_support += 1

                bass_idx += 1

        root_support_percentage = root_support / total_chords if total_chords > 0 else 0.0

        return {
            "root_support_percentage": root_support_percentage,
            "harmonic_clarity": (
                "high" if root_support_percentage > 0.7 else "medium" if root_support_percentage > 0.4 else "low"
            ),
        }
