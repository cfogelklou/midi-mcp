"""Comprehensive music analysis functionality combining all theory components."""

from typing import Dict, List, Optional, Tuple, Union
from ..models.theory_models import HarmonicAnalysis, KeyAnalysis, VoiceLeadingAnalysis, ChordProgression, Note, Chord
from .scales import ScaleManager
from .chords import ChordManager
from .progressions import ProgressionManager
from .keys import KeyManager
from .voice_leading import VoiceLeadingManager
from .constants import NON_CHORD_TONE_TYPES


class MusicAnalyzer:
    """Comprehensive music analysis combining all theory components."""

    def __init__(self):
        self.scale_manager = ScaleManager()
        self.chord_manager = ChordManager()
        self.progression_manager = ProgressionManager()
        self.key_manager = KeyManager()
        self.voice_leading_manager = VoiceLeadingManager()

    def analyze_midi_file(
        self, midi_notes: List[int], timestamps: Optional[List[float]] = None, track_info: Optional[Dict] = None
    ) -> HarmonicAnalysis:
        """
        Create complete harmonic analysis of MIDI data.

        Args:
            midi_notes: List of MIDI note numbers
            timestamps: Optional timestamps for each note
            track_info: Optional metadata about tracks

        Returns:
            Comprehensive harmonic analysis
        """
        # Step 1: Key Analysis
        key_analysis = self.key_manager.detect_key(midi_notes, timestamps)

        # Step 2: Chord Analysis
        chord_progression = self._analyze_harmonic_progression(midi_notes, timestamps, key_analysis.most_likely_key)

        # Step 3: Voice Leading Analysis
        voice_leading = self.voice_leading_manager.validate_voice_leading(chord_progression.chords)

        # Step 4: Identify Cadences
        cadences = self._identify_cadences(chord_progression)

        # Step 5: Analyze Modulations
        modulations = []
        if timestamps:
            modulations = self.key_manager.analyze_modulations(midi_notes, timestamps)

        # Step 6: Non-chord Tone Analysis
        non_chord_tones = self._analyze_non_chord_tones(midi_notes, timestamps, chord_progression)

        # Step 7: Harmonic Rhythm Analysis
        harmonic_rhythm = self._analyze_harmonic_rhythm(chord_progression, timestamps)

        return HarmonicAnalysis(
            key_analysis=key_analysis,
            chord_progression=chord_progression,
            voice_leading=voice_leading,
            cadences=cadences,
            modulations=modulations,
            non_chord_tones=non_chord_tones,
            harmonic_rhythm=harmonic_rhythm,
        )

    def analyze_chord_sequence(self, chord_symbols: List[str], key: Optional[str] = None) -> Dict[str, any]:
        """
        Analyze a sequence of chord symbols.

        Args:
            chord_symbols: List of chord symbols (["C", "Am", "F", "G"])
            key: Optional key context

        Returns:
            Analysis of the chord sequence
        """
        # Analyze progression
        progression_analysis = self.progression_manager.analyze_progression(chord_symbols, key)

        # Build chord objects for voice leading analysis
        chords = []
        for symbol in chord_symbols:
            try:
                # Parse symbol to build chord
                parsed = self._parse_chord_symbol_for_analysis(symbol)
                if parsed:
                    chord = self.chord_manager.build_chord(
                        root_note=parsed["root"], chord_type=parsed["type"], octave=4
                    )
                    chords.append(chord)
            except Exception:
                continue  # Skip problematic chords

        # Voice leading analysis
        voice_leading = None
        if len(chords) > 1:
            voice_leading = self.voice_leading_manager.validate_voice_leading(chords)

        return {
            "progression_analysis": progression_analysis,
            "voice_leading": voice_leading.smooth_score if voice_leading else None,
            "voice_leading_problems": voice_leading.problems if voice_leading else [],
            "chord_functions": progression_analysis.get("harmonic_functions", []),
            "cadences": progression_analysis.get("cadences", []),
            "modulations": progression_analysis.get("modulations", []),
        }

    def suggest_harmonic_improvements(self, chord_progression: ChordProgression) -> List[str]:
        """
        Suggest improvements for a chord progression.

        Args:
            chord_progression: Chord progression to analyze

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Voice leading suggestions
        vl_analysis = self.voice_leading_manager.validate_voice_leading(chord_progression.chords)
        suggestions.extend(vl_analysis.suggestions)

        # Progression suggestions
        progression_validation = self.progression_manager.validate_progression(
            chord_progression.roman_numerals, chord_progression.key
        )
        suggestions.extend(progression_validation.get("suggestions", []))

        # Add theory-specific suggestions
        if len(chord_progression.chords) > 2:
            # Check for strong tonal centers
            has_dominant_resolution = any(
                chord_progression.roman_numerals[i : i + 2] in [["V", "I"], ["V7", "I"]]
                for i in range(len(chord_progression.roman_numerals) - 1)
            )

            if not has_dominant_resolution:
                suggestions.append("Consider adding V-I resolution for stronger tonal center")

        # Check for melodic interest in bass line
        bass_notes = [chord.get_bass_note().midi_note for chord in chord_progression.chords]
        bass_movement = sum(abs(bass_notes[i + 1] - bass_notes[i]) for i in range(len(bass_notes) - 1))

        if bass_movement < len(bass_notes) * 2:  # Very static bass
            suggestions.append("Consider adding more movement in bass line")

        return suggestions

    def identify_musical_form(
        self, chord_progression: ChordProgression, section_markers: Optional[List[float]] = None
    ) -> Dict[str, any]:
        """
        Identify musical form and structure.

        Args:
            chord_progression: Chord progression to analyze
            section_markers: Optional time markers for sections

        Returns:
            Form analysis
        """
        # This is a simplified form analysis - could be much more sophisticated
        total_chords = len(chord_progression.chords)

        # Look for repeated patterns
        patterns = self._find_repeated_patterns(chord_progression.roman_numerals)

        # Identify phrase lengths
        phrase_lengths = self._analyze_phrase_structure(chord_progression)

        # Guess at form based on patterns and length
        form_guess = self._guess_musical_form(total_chords, patterns, phrase_lengths)

        return {
            "total_length": total_chords,
            "repeated_patterns": patterns,
            "phrase_lengths": phrase_lengths,
            "suggested_form": form_guess,
            "key_centers": self._identify_key_centers(chord_progression),
            "structural_points": self._identify_structural_points(chord_progression),
        }

    def _analyze_harmonic_progression(
        self, midi_notes: List[int], timestamps: Optional[List[float]], key: str
    ) -> ChordProgression:
        """Analyze MIDI notes to extract chord progression."""
        if not timestamps:
            # Simple case: analyze all notes as one chord
            chord_notes = self.chord_manager.analyze_chord(midi_notes)
            if chord_notes:
                # Build chord from analysis
                best_match = chord_notes[0]
                chord = self.chord_manager.build_chord(
                    root_note=best_match["root"], chord_type=best_match["chord_type"]
                )
                return ChordProgression(chords=[chord], key=key, roman_numerals=["I"], durations=[1.0])  # Simplified

        # More sophisticated analysis with timestamps
        # Group notes into time windows to identify chords
        chord_windows = self._group_notes_by_time(midi_notes, timestamps)

        chords = []
        roman_numerals = []
        durations = []

        for window_notes, duration in chord_windows:
            if len(window_notes) >= 3:  # Need minimum notes for chord
                chord_analysis = self.chord_manager.analyze_chord(window_notes)
                if chord_analysis:
                    best_match = chord_analysis[0]
                    chord = self.chord_manager.build_chord(
                        root_note=best_match["root"], chord_type=best_match["chord_type"]
                    )
                    chords.append(chord)

                    # Convert to roman numeral
                    roman = self._convert_to_roman_numeral(best_match["root"], key)
                    roman_numerals.append(roman)
                    durations.append(duration)

        return ChordProgression(chords=chords, key=key, roman_numerals=roman_numerals, durations=durations)

    def _identify_cadences(self, chord_progression: ChordProgression) -> List[Dict[str, any]]:
        """Identify cadences in the progression."""
        cadences = []
        romans = chord_progression.roman_numerals

        for i in range(len(romans) - 1):
            current = romans[i]
            next_chord = romans[i + 1]

            cadence_type = None
            if current == "V" and next_chord == "I":
                cadence_type = "authentic"
            elif current == "V7" and next_chord == "I":
                cadence_type = "authentic"
            elif current == "IV" and next_chord == "I":
                cadence_type = "plagal"
            elif current == "V" and next_chord == "vi":
                cadence_type = "deceptive"
            elif next_chord == "V":
                cadence_type = "half"

            if cadence_type:
                cadences.append(
                    {
                        "type": cadence_type,
                        "position": i,
                        "chords": [current, next_chord],
                        "strength": self._assess_cadence_strength(cadence_type),
                    }
                )

        return cadences

    def _analyze_non_chord_tones(
        self, midi_notes: List[int], timestamps: Optional[List[float]], chord_progression: ChordProgression
    ) -> List[Dict[str, any]]:
        """Analyze non-chord tones in the melody."""
        if not timestamps or not chord_progression.chords:
            return []

        non_chord_tones = []

        # This is a simplified analysis - real implementation would be more complex
        for i, (note, time) in enumerate(zip(midi_notes, timestamps)):
            # Find which chord this note belongs to
            chord_at_time = self._find_chord_at_time(time, chord_progression)

            if chord_at_time:
                note_pc = note % 12
                chord_pcs = {n.midi_note % 12 for n in chord_at_time.notes}

                if note_pc not in chord_pcs:
                    # This is a non-chord tone
                    nct_type = self._classify_non_chord_tone(note, i, midi_notes, timestamps, chord_at_time)

                    non_chord_tones.append(
                        {"note": note, "time": time, "type": nct_type, "chord_context": chord_at_time.symbol}
                    )

        return non_chord_tones

    def _analyze_harmonic_rhythm(
        self, chord_progression: ChordProgression, timestamps: Optional[List[float]]
    ) -> List[float]:
        """Analyze the rate of harmonic change."""
        if not chord_progression.durations:
            return [1.0] * len(chord_progression.chords)

        # Calculate harmonic rhythm as rate of chord changes
        rhythm = []
        for duration in chord_progression.durations:
            # Convert duration to harmonic rhythm rate
            rhythm_rate = 1.0 / max(duration, 0.1)  # Avoid division by zero
            rhythm.append(rhythm_rate)

        return rhythm

    def _group_notes_by_time(self, midi_notes: List[int], timestamps: List[float]) -> List[Tuple[List[int], float]]:
        """Group notes into time windows for chord analysis."""
        if len(midi_notes) != len(timestamps):
            return []

        # Simple grouping by time windows (e.g., every 2 seconds)
        window_size = 2.0  # seconds
        windows = []

        current_window_notes = []
        window_start = timestamps[0]

        for note, time in zip(midi_notes, timestamps):
            if time - window_start < window_size:
                current_window_notes.append(note)
            else:
                # Start new window
                if current_window_notes:
                    windows.append((current_window_notes, window_size))
                current_window_notes = [note]
                window_start = time

        # Add final window
        if current_window_notes:
            final_duration = timestamps[-1] - window_start
            windows.append((current_window_notes, final_duration))

        return windows

    def _convert_to_roman_numeral(self, chord_root: str, key: str) -> str:
        """Convert chord root to roman numeral in given key."""
        # Simplified conversion
        key_root = key.replace("m", "")
        is_minor = "m" in key

        # Calculate scale degree
        from .constants import NOTE_NAMES

        key_pc = NOTE_NAMES.index(key_root)
        chord_pc = NOTE_NAMES.index(chord_root)
        degree = ((chord_pc - key_pc) % 12) // 2 + 1  # Simplified

        # Map to roman numerals (simplified)
        romans = ["I", "ii", "iii", "IV", "V", "vi", "vii"]
        if 1 <= degree <= 7:
            return romans[degree - 1]

        return "I"  # Fallback

    def _assess_cadence_strength(self, cadence_type: str) -> float:
        """Assess the strength of a cadence type."""
        strengths = {"authentic": 1.0, "plagal": 0.7, "deceptive": 0.8, "half": 0.5}
        return strengths.get(cadence_type, 0.3)

    def _find_chord_at_time(self, time: float, chord_progression: ChordProgression) -> Optional[Chord]:
        """Find which chord is active at a given time."""
        # Simplified - assumes chords are evenly spaced
        if not chord_progression.durations:
            return None

        cumulative_time = 0
        for i, duration in enumerate(chord_progression.durations):
            if time <= cumulative_time + duration:
                return chord_progression.chords[i]
            cumulative_time += duration

        # Return last chord if time is beyond progression
        return chord_progression.chords[-1] if chord_progression.chords else None

    def _classify_non_chord_tone(
        self, note: int, position: int, melody: List[int], timestamps: List[float], chord: Chord
    ) -> str:
        """Classify the type of non-chord tone."""
        # Simplified classification - real implementation would be more sophisticated

        # Check surrounding notes for context
        prev_note = melody[position - 1] if position > 0 else None
        next_note = melody[position + 1] if position < len(melody) - 1 else None

        if prev_note and next_note:
            # Check for passing tone (stepwise motion through)
            if abs(note - prev_note) <= 2 and abs(next_note - note) <= 2:
                return "passing_tone"

            # Check for neighbor tone (returns to same note)
            if prev_note == next_note:
                return "neighbor_tone"

        # Default classification
        return "other"

    def _find_repeated_patterns(self, roman_numerals: List[str]) -> List[Dict[str, any]]:
        """Find repeated patterns in roman numeral progression."""
        patterns = []

        # Look for patterns of different lengths
        for length in range(2, min(8, len(roman_numerals) // 2)):
            for start in range(len(roman_numerals) - length + 1):
                pattern = roman_numerals[start : start + length]

                # Look for repetitions of this pattern
                occurrences = [start]
                for i in range(start + length, len(roman_numerals) - length + 1):
                    if roman_numerals[i : i + length] == pattern:
                        occurrences.append(i)

                if len(occurrences) > 1:
                    patterns.append(
                        {
                            "pattern": pattern,
                            "length": length,
                            "occurrences": occurrences,
                            "repetitions": len(occurrences),
                        }
                    )

        # Sort by number of repetitions and length
        patterns.sort(key=lambda x: (x["repetitions"], x["length"]), reverse=True)
        return patterns[:5]  # Return top 5 patterns

    def _analyze_phrase_structure(self, chord_progression: ChordProgression) -> List[int]:
        """Analyze phrase lengths in the progression."""
        # Simplified - look for cadential points
        phrase_lengths = []
        current_phrase_length = 0

        for i, roman in enumerate(chord_progression.roman_numerals):
            current_phrase_length += 1

            # Look for cadential endings
            if (
                i < len(chord_progression.roman_numerals) - 1
                and roman == "V"
                and chord_progression.roman_numerals[i + 1] == "I"
            ):
                phrase_lengths.append(current_phrase_length + 1)  # Include the I chord
                current_phrase_length = -1  # Will be incremented next iteration

        # Add remaining length as final phrase
        if current_phrase_length > 0:
            phrase_lengths.append(current_phrase_length)

        return phrase_lengths

    def _guess_musical_form(self, total_length: int, patterns: List[Dict], phrase_lengths: List[int]) -> str:
        """Guess the musical form based on analysis."""
        if total_length <= 8:
            return "phrase"
        elif total_length <= 16:
            return "period"
        elif total_length <= 32:
            if patterns and patterns[0]["repetitions"] >= 2:
                return "binary_form"
            else:
                return "song_form"
        else:
            return "extended_form"

    def _identify_key_centers(self, chord_progression: ChordProgression) -> List[str]:
        """Identify different tonal centers in the progression."""
        # Simplified - just return main key and any obvious modulations
        key_centers = [chord_progression.key]

        # Look for secondary dominants or modulations
        for i, roman in enumerate(chord_progression.roman_numerals):
            if "/" in roman:  # Secondary dominant notation
                target_key = roman.split("/")[-1]
                if target_key not in key_centers:
                    key_centers.append(target_key)

        return key_centers

    def _identify_structural_points(self, chord_progression: ChordProgression) -> List[Dict[str, any]]:
        """Identify important structural points in the progression."""
        structural_points = []

        # Find strong cadences
        for i in range(len(chord_progression.roman_numerals) - 1):
            current = chord_progression.roman_numerals[i]
            next_chord = chord_progression.roman_numerals[i + 1]

            if current in ["V", "V7"] and next_chord == "I":
                structural_points.append({"type": "authentic_cadence", "position": i, "importance": "high"})

        return structural_points

    def _parse_chord_symbol_for_analysis(self, symbol: str) -> Optional[Dict[str, str]]:
        """Parse chord symbol for analysis purposes."""
        # Simplified parser
        import re

        pattern = r"^([A-G][#b]?)(.*)$"
        match = re.match(pattern, symbol)

        if not match:
            return None

        root = match.group(1)
        extensions = match.group(2).lower()

        # Map extensions to internal chord types
        if "m7" in extensions:
            chord_type = "min7"
        elif "maj7" in extensions:
            chord_type = "maj7"
        elif "7" in extensions:
            chord_type = "7"
        elif "m" in extensions and "maj" not in extensions:
            chord_type = "minor"
        elif "dim" in extensions:
            chord_type = "diminished"
        elif "aug" in extensions:
            chord_type = "augmented"
        else:
            chord_type = "major"

        return {"root": root, "type": chord_type}
