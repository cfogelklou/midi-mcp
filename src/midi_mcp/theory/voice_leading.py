"""Voice leading analysis, validation, and optimization functionality."""

from typing import Dict, List, Optional, Tuple, Union
from ..models.theory_models import Chord, VoiceLeadingAnalysis, Note
from .constants import VOICE_LEADING_RULES, INTERVAL_NAMES


class VoiceLeadingManager:
    """Manages voice leading analysis and optimization."""

    def __init__(self):
        self.rules = VOICE_LEADING_RULES

    def validate_voice_leading(self, chord_progression: List[Chord]) -> VoiceLeadingAnalysis:
        """
        Validate and score voice leading in a chord progression.

        Args:
            chord_progression: List of chord objects with voicings

        Returns:
            VoiceLeadingAnalysis with problems and suggestions
        """
        if len(chord_progression) < 2:
            return VoiceLeadingAnalysis(smooth_score=100.0, problems=[], suggestions=[], parallel_motion=[])

        problems = []
        parallel_motion = []
        total_score = 100.0

        # Analyze each chord transition
        for i in range(len(chord_progression) - 1):
            current_chord = chord_progression[i]
            next_chord = chord_progression[i + 1]

            # Analyze this transition
            transition_analysis = self._analyze_transition(current_chord, next_chord, i)

            problems.extend(transition_analysis["problems"])
            parallel_motion.extend(transition_analysis["parallel_motion"])
            total_score -= transition_analysis["penalty"]

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(problems)

        return VoiceLeadingAnalysis(
            smooth_score=max(0.0, total_score),
            problems=problems,
            suggestions=suggestions,
            parallel_motion=parallel_motion,
        )

    def optimize_voice_leading(
        self, chord_progression: List[Chord], voice_range: Tuple[int, int] = (48, 84)
    ) -> List[Chord]:
        """
        Optimize voice leading for a chord progression.

        Args:
            chord_progression: Original progression
            voice_range: (min_midi, max_midi) range for voices

        Returns:
            Optimized chord progression with improved voice leading
        """
        if len(chord_progression) < 2:
            return chord_progression

        optimized = [chord_progression[0]]  # Keep first chord as-is

        # Optimize each subsequent chord
        for i in range(1, len(chord_progression)):
            current_voicing = optimized[-1]
            target_chord = chord_progression[i]

            # Find best voicing for target chord
            best_voicing = self._find_optimal_voicing(current_voicing, target_chord, voice_range)

            optimized.append(best_voicing)

        return optimized

    def analyze_voice_motion(self, chord1: Chord, chord2: Chord) -> Dict[str, any]:
        """
        Analyze motion between two chords.

        Args:
            chord1: First chord
            chord2: Second chord

        Returns:
            Dictionary with motion analysis
        """
        if len(chord1.notes) != len(chord2.notes):
            # Handle different voice counts - simplified approach
            min_voices = min(len(chord1.notes), len(chord2.notes))
            notes1 = chord1.notes[:min_voices]
            notes2 = chord2.notes[:min_voices]
        else:
            notes1 = chord1.notes
            notes2 = chord2.notes

        voice_motions = []
        motion_types = {"parallel": 0, "similar": 0, "contrary": 0, "oblique": 0}

        # Analyze each voice pair
        for i in range(len(notes1)):
            for j in range(i + 1, len(notes1)):
                motion_type = self._classify_motion(notes1[i], notes1[j], notes2[i], notes2[j])
                motion_types[motion_type] += 1

                voice_motions.append(
                    {
                        "voice1": i,
                        "voice2": j,
                        "motion_type": motion_type,
                        "interval1": self._calculate_interval(notes1[i], notes1[j]),
                        "interval2": self._calculate_interval(notes2[i], notes2[j]),
                    }
                )

        return {
            "voice_motions": voice_motions,
            "motion_summary": motion_types,
            "total_motion": sum(abs(n2.midi_note - n1.midi_note) for n1, n2 in zip(notes1, notes2)),
            "largest_leap": max(abs(n2.midi_note - n1.midi_note) for n1, n2 in zip(notes1, notes2)),
        }

    def check_parallel_motion(self, chord1: Chord, chord2: Chord) -> List[Dict[str, any]]:
        """
        Check for parallel fifths and octaves between two chords.

        Args:
            chord1: First chord
            chord2: Second chord

        Returns:
            List of parallel motion violations
        """
        violations = []

        if len(chord1.notes) != len(chord2.notes):
            return violations  # Can't analyze different voice counts easily

        notes1 = chord1.notes
        notes2 = chord2.notes

        # Check all voice pairs
        for i in range(len(notes1)):
            for j in range(i + 1, len(notes1)):
                interval1 = self._calculate_interval(notes1[i], notes1[j])
                interval2 = self._calculate_interval(notes2[i], notes2[j])

                # Check if both intervals are the same and both voices move
                if (
                    interval1["semitones"] == interval2["semitones"]
                    and notes1[i].midi_note != notes2[i].midi_note
                    and notes1[j].midi_note != notes2[j].midi_note
                ):

                    # Check for problematic intervals
                    if interval1["semitones"] % 12 == 7:  # Perfect fifth
                        violations.append(
                            {
                                "type": "parallel_fifths",
                                "voice1": i,
                                "voice2": j,
                                "severity": "severe",
                                "interval": "perfect_fifth",
                            }
                        )
                    elif interval1["semitones"] % 12 == 0:  # Octave/unison
                        violations.append(
                            {
                                "type": "parallel_octaves",
                                "voice1": i,
                                "voice2": j,
                                "severity": "severe",
                                "interval": "octave",
                            }
                        )

        return violations

    def suggest_voice_leading_improvements(self, chord_progression: List[Chord]) -> List[str]:
        """
        Suggest improvements for voice leading in a progression.

        Args:
            chord_progression: Chord progression to analyze

        Returns:
            List of specific improvement suggestions
        """
        analysis = self.validate_voice_leading(chord_progression)
        return analysis.suggestions

    def _analyze_transition(self, chord1: Chord, chord2: Chord, position: int) -> Dict[str, any]:
        """Analyze a single chord transition."""
        problems = []
        parallel_motion = []
        total_penalty = 0

        # Check for parallel motion
        parallel_violations = self.check_parallel_motion(chord1, chord2)
        for violation in parallel_violations:
            parallel_motion.append(violation)
            if violation["type"] == "parallel_fifths":
                total_penalty += self.rules["parallel_fifths_penalty"]
                problems.append(
                    {
                        "position": position,
                        "type": "parallel_fifths",
                        "description": f"Parallel fifths between voices {violation['voice1']} and {violation['voice2']}",
                        "severity": "severe",
                    }
                )
            elif violation["type"] == "parallel_octaves":
                total_penalty += self.rules["parallel_octaves_penalty"]
                problems.append(
                    {
                        "position": position,
                        "type": "parallel_octaves",
                        "description": f"Parallel octaves between voices {violation['voice1']} and {violation['voice2']}",
                        "severity": "severe",
                    }
                )

        # Check for large leaps
        if len(chord1.notes) == len(chord2.notes):
            for i, (note1, note2) in enumerate(zip(chord1.notes, chord2.notes)):
                leap_size = abs(note2.midi_note - note1.midi_note)
                if leap_size > self.rules["max_voice_range"]:
                    excess = leap_size - self.rules["max_voice_range"]
                    penalty = excess * self.rules["large_leap_penalty"]
                    total_penalty += penalty
                    problems.append(
                        {
                            "position": position,
                            "type": "large_leap",
                            "description": f"Large leap of {leap_size} semitones in voice {i}",
                            "severity": "moderate" if leap_size < 18 else "severe",
                        }
                    )

        # Check for voice crossing in each chord
        for chord in [chord1, chord2]:
            if self._has_voice_crossing(chord):
                total_penalty += self.rules["voice_crossing_penalty"]
                problems.append(
                    {
                        "position": position,
                        "type": "voice_crossing",
                        "description": "Voice crossing detected",
                        "severity": "moderate",
                    }
                )
                break  # Don't double-penalize

        return {"problems": problems, "parallel_motion": parallel_motion, "penalty": total_penalty}

    def _generate_suggestions(self, problems: List[Dict]) -> List[str]:
        """Generate improvement suggestions based on problems."""
        suggestions = []

        problem_types = set(problem["type"] for problem in problems)

        if "parallel_fifths" in problem_types:
            suggestions.append("Avoid parallel fifths by moving inner voices in contrary or oblique motion")

        if "parallel_octaves" in problem_types:
            suggestions.append("Eliminate parallel octaves by changing the motion of one voice")

        if "large_leap" in problem_types:
            suggestions.append("Reduce large leaps by using stepwise motion or smaller intervals")

        if "voice_crossing" in problem_types:
            suggestions.append("Maintain proper voice order (soprano highest, bass lowest)")

        # Add general suggestions
        suggestions.append("Prefer stepwise motion in individual voices")
        suggestions.append("Keep common tones between chords when possible")
        suggestions.append("Use contrary motion when voices must move in large intervals")

        return suggestions

    def _find_optimal_voicing(self, current_chord: Chord, target_chord: Chord, voice_range: Tuple[int, int]) -> Chord:
        """Find optimal voicing for target chord based on current voicing."""
        min_midi, max_midi = voice_range

        # Generate possible voicings for target chord
        possible_voicings = self._generate_voicings(target_chord, voice_range)

        if not possible_voicings:
            return target_chord  # Return original if no alternatives

        # Score each voicing based on voice leading quality
        best_voicing = None
        best_score = float("inf")

        for voicing in possible_voicings:
            score = self._score_voicing_transition(current_chord, voicing)
            if score < best_score:
                best_score = score
                best_voicing = voicing

        return best_voicing or target_chord

    def _generate_voicings(self, chord: Chord, voice_range: Tuple[int, int], voice_count: int = 4) -> List[Chord]:
        """Generate different voicings for a chord within range."""
        min_midi, max_midi = voice_range
        voicings = []

        # Get chord tones
        chord_tones = [note.midi_note % 12 for note in chord.notes]

        # Generate voicings by distributing chord tones across range
        # This is a simplified approach - could be much more sophisticated

        # Try different bass notes
        for bass_pc in chord_tones:
            # Find bass note in appropriate register
            bass_midi = bass_pc
            while bass_midi < min_midi:
                bass_midi += 12

            if bass_midi > max_midi:
                continue

            # Generate upper voices
            upper_voices = []
            for pc in chord_tones:
                if pc != bass_pc or len([t for t in chord_tones if t == pc]) > 1:
                    # Find appropriate register for this voice
                    voice_midi = pc + 12 * 4  # Start in middle register
                    while voice_midi < bass_midi + 12:
                        voice_midi += 12

                    if voice_midi <= max_midi:
                        upper_voices.append(voice_midi)

            # Limit to voice_count total voices
            all_voices = [bass_midi] + sorted(upper_voices)[: voice_count - 1]

            if len(all_voices) >= 3:  # Minimum for a chord
                notes = [Note.from_midi(midi) for midi in all_voices]
                voicing = Chord(
                    root=chord.root,
                    quality=chord.quality,
                    chord_type=chord.chord_type,
                    notes=notes,
                    symbol=chord.symbol,
                    inversion=0 if bass_pc == chord.root.midi_note % 12 else 1,
                )
                voicings.append(voicing)

        return voicings[:5]  # Return top 5 voicings

    def _score_voicing_transition(self, chord1: Chord, chord2: Chord) -> float:
        """Score a voicing transition (lower is better)."""
        if len(chord1.notes) != len(chord2.notes):
            return 1000  # High penalty for mismatched voice counts

        score = 0

        # Penalty for total voice motion
        total_motion = sum(abs(n2.midi_note - n1.midi_note) for n1, n2 in zip(chord1.notes, chord2.notes))
        score += total_motion * 0.5

        # Penalty for large leaps
        for n1, n2 in zip(chord1.notes, chord2.notes):
            leap = abs(n2.midi_note - n1.midi_note)
            if leap > 12:  # Octave
                score += (leap - 12) * 2

        # Penalty for parallel motion
        parallel_violations = self.check_parallel_motion(chord1, chord2)
        score += len(parallel_violations) * 50

        # Bonus for voice independence (contrary motion)
        motion_analysis = self.analyze_voice_motion(chord1, chord2)
        score -= motion_analysis["motion_summary"]["contrary"] * 5

        return score

    def _classify_motion(self, note1_a: Note, note1_b: Note, note2_a: Note, note2_b: Note) -> str:
        """Classify motion type between two voice pairs."""
        motion_a = note2_a.midi_note - note1_a.midi_note
        motion_b = note2_b.midi_note - note1_b.midi_note

        if motion_a == 0 and motion_b == 0:
            return "oblique"  # Both voices stay
        elif motion_a == 0 or motion_b == 0:
            return "oblique"  # One voice stays
        elif (motion_a > 0) == (motion_b > 0):
            # Same direction
            if abs(motion_a) == abs(motion_b):
                return "parallel"
            else:
                return "similar"
        else:
            # Opposite directions
            return "contrary"

    def _calculate_interval(self, note1: Note, note2: Note) -> Dict[str, any]:
        """Calculate interval between two notes."""
        semitones = abs(note2.midi_note - note1.midi_note)

        return {
            "semitones": semitones,
            "name": INTERVAL_NAMES.get(semitones % 12, f"{semitones}_semitones"),
            "compound": semitones > 12,
        }

    def _has_voice_crossing(self, chord: Chord) -> bool:
        """Check if chord has voice crossing."""
        if len(chord.notes) < 2:
            return False

        # Check if voices are in order from low to high
        midi_notes = [note.midi_note for note in chord.notes]
        return midi_notes != sorted(midi_notes)

    def create_four_part_harmony(
        self, melody_notes: List[Note], chord_progression: List[Chord]
    ) -> Dict[str, List[Note]]:
        """
        Create four-part harmony (SATB) from melody and chord progression.

        Args:
            melody_notes: Soprano melody line
            chord_progression: Underlying harmonic progression

        Returns:
            Dictionary with parts: soprano, alto, tenor, bass
        """
        if len(melody_notes) != len(chord_progression):
            raise ValueError("Melody and chord progression must have same length")

        # Voice ranges (MIDI numbers)
        ranges = {
            "soprano": (60, 81),  # C4 to A5
            "alto": (55, 74),  # G3 to D5
            "tenor": (48, 67),  # C3 to G4
            "bass": (36, 60),  # C2 to C4
        }

        parts = {"soprano": melody_notes, "alto": [], "tenor": [], "bass": []}

        # Generate other voices
        for i, (melody_note, chord) in enumerate(zip(melody_notes, chord_progression)):
            # Determine which chord tone the melody represents
            melody_pc = melody_note.midi_note % 12
            chord_pcs = [note.midi_note % 12 for note in chord.notes]

            # Generate bass line (usually root or fifth)
            bass_pc = chord.root.midi_note % 12
            bass_midi = bass_pc + 12 * 2  # Start in bass range
            while bass_midi > ranges["bass"][1]:
                bass_midi -= 12
            parts["bass"].append(Note.from_midi(bass_midi))

            # Generate inner voices to complete harmony
            remaining_pcs = [pc for pc in chord_pcs if pc != melody_pc and pc != bass_pc]

            # Alto voice
            if remaining_pcs:
                alto_pc = remaining_pcs[0]
                alto_midi = alto_pc + 12 * 4  # Start in alto range
                while alto_midi < ranges["alto"][0] or alto_midi > ranges["alto"][1]:
                    if alto_midi < ranges["alto"][0]:
                        alto_midi += 12
                    else:
                        alto_midi -= 12
                parts["alto"].append(Note.from_midi(alto_midi))
            else:
                # Double another voice if no remaining chord tones
                parts["alto"].append(Note.from_midi(bass_midi + 12))

            # Tenor voice
            if len(remaining_pcs) > 1:
                tenor_pc = remaining_pcs[1]
            else:
                tenor_pc = bass_pc  # Double bass

            tenor_midi = tenor_pc + 12 * 3  # Start in tenor range
            while tenor_midi < ranges["tenor"][0] or tenor_midi > ranges["tenor"][1]:
                if tenor_midi < ranges["tenor"][0]:
                    tenor_midi += 12
                else:
                    tenor_midi -= 12
            parts["tenor"].append(Note.from_midi(tenor_midi))

        return parts
