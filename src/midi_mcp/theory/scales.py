"""Scale generation and analysis functionality."""

from typing import Dict, List, Optional, Tuple
from ..models.theory_models import Scale, Note
from .constants import SCALE_PATTERNS, NOTE_NAMES, FLAT_NOTE_NAMES, ENHARMONIC_EQUIVALENTS


class ScaleManager:
    """Manages scale generation, analysis, and transformations."""

    def __init__(self):
        self.patterns = SCALE_PATTERNS

    def generate_scale(self, root_note: str, scale_type: str, octave: int = 4) -> Scale:
        """
        Generate a scale with specified parameters.

        Args:
            root_note: Root note (C, C#, Db, D, etc.)
            scale_type: Scale type from SCALE_PATTERNS
            octave: Starting octave (0-9)

        Returns:
            Scale object with notes and pattern
        """
        if scale_type not in self.patterns:
            raise ValueError(f"Unknown scale type: {scale_type}. Available: {list(self.patterns.keys())}")

        # Normalize root note
        root_note = self._normalize_note_name(root_note)

        # Calculate root MIDI note
        root_midi = self._note_to_midi(root_note, octave)
        root = Note.from_midi(root_midi, prefer_sharps="#" in root_note)

        # Generate scale pattern
        pattern = self.patterns[scale_type]
        notes = [root]
        current_midi = root_midi

        # Build scale notes
        for interval in pattern[:-1]:  # Don't include the octave return
            current_midi += interval
            note = Note.from_midi(current_midi, prefer_sharps="#" in root_note)
            notes.append(note)

        return Scale(root=root, name=scale_type, pattern=pattern, notes=notes)

    def identify_intervals(self, notes: List[int]) -> List[Dict[str, any]]:
        """
        Identify intervals between consecutive notes.

        Args:
            notes: List of MIDI note numbers

        Returns:
            List of interval information dictionaries
        """
        if len(notes) < 2:
            return []

        intervals = []
        for i in range(len(notes) - 1):
            semitones = notes[i + 1] - notes[i]
            interval_info = {
                "semitones": abs(semitones),
                "direction": "ascending" if semitones > 0 else "descending",
                "from_note": notes[i],
                "to_note": notes[i + 1],
                "name": self._get_interval_name(abs(semitones)),
            }
            intervals.append(interval_info)

        return intervals

    def transpose_to_key(self, notes: List[int], from_key: str, to_key: str) -> List[int]:
        """
        Transpose a sequence of notes from one key to another.

        Args:
            notes: Original MIDI note numbers
            from_key: Original key (C, G, F#, etc.)
            to_key: Target key

        Returns:
            Transposed MIDI note numbers
        """
        from_key = self._normalize_note_name(from_key.replace("m", ""))  # Remove minor indication
        to_key = self._normalize_note_name(to_key.replace("m", ""))

        # Calculate transposition interval
        from_midi = self._note_to_midi(from_key, 4) % 12
        to_midi = self._note_to_midi(to_key, 4) % 12
        transposition = to_midi - from_midi

        return [note + transposition for note in notes]

    def get_scale_degrees(self, scale: Scale, note_names: bool = True) -> Dict[int, any]:
        """
        Get scale degree information for a scale.

        Args:
            scale: Scale object
            note_names: Include note names in output

        Returns:
            Dictionary mapping degree numbers to note info
        """
        degrees = {}
        for i, note in enumerate(scale.notes, 1):
            degree_info = {"degree": i, "midi_note": note.midi_note, "degree_name": self._get_degree_name(i)}
            if note_names:
                degree_info["note_name"] = note.name
            degrees[i] = degree_info

        return degrees

    def find_relative_scales(self, scale: Scale) -> Dict[str, Scale]:
        """
        Find scales related to the given scale.

        Args:
            scale: Reference scale

        Returns:
            Dictionary of related scales
        """
        relatives = {}

        # Generate modes
        for degree in range(1, len(scale.notes) + 1):
            try:
                mode = scale.get_mode(degree)
                mode_name = f"{mode.name}_of_{scale.root.name}"
                relatives[mode_name] = mode
            except ValueError:
                continue

        # Find relative minor/major if applicable
        if scale.name == "major":
            # Relative minor is the 6th degree
            if len(scale.notes) >= 6:
                minor_root = scale.notes[5]  # 6th degree (0-indexed)
                relatives["relative_minor"] = self.generate_scale(minor_root.name, "natural_minor", minor_root.octave)
        elif scale.name in ["natural_minor", "aeolian"]:
            # Relative major is a minor third up
            major_root_midi = scale.root.midi_note + 3
            major_root = Note.from_midi(major_root_midi)
            relatives["relative_major"] = self.generate_scale(major_root.name, "major", major_root.octave)

        # Parallel minor/major
        if scale.name == "major":
            relatives["parallel_minor"] = self.generate_scale(scale.root.name, "natural_minor", scale.root.octave)
        elif scale.name in ["natural_minor", "aeolian"]:
            relatives["parallel_major"] = self.generate_scale(scale.root.name, "major", scale.root.octave)

        return relatives

    def compare_scales(self, scale1: Scale, scale2: Scale) -> Dict[str, any]:
        """
        Compare two scales and find similarities.

        Args:
            scale1: First scale
            scale2: Second scale

        Returns:
            Comparison information
        """
        # Convert to pitch classes for comparison
        pc1 = {note.midi_note % 12 for note in scale1.notes}
        pc2 = {note.midi_note % 12 for note in scale2.notes}

        common_notes = pc1 & pc2
        unique_to_1 = pc1 - pc2
        unique_to_2 = pc2 - pc1

        similarity = len(common_notes) / max(len(pc1), len(pc2))

        return {
            "similarity_ratio": similarity,
            "common_pitch_classes": sorted(list(common_notes)),
            "unique_to_first": sorted(list(unique_to_1)),
            "unique_to_second": sorted(list(unique_to_2)),
            "is_mode_relationship": len(pc1) == len(pc2) and pc1 == pc2,
            "common_note_count": len(common_notes),
        }

    def get_available_scales(self) -> List[str]:
        """Get list of all available scale types."""
        return list(self.patterns.keys())

    def _normalize_note_name(self, note: str) -> str:
        """Normalize note name to standard format."""
        note = note.strip().capitalize()

        # Handle flat notation
        if "b" in note.lower():
            note = note.replace("b", "b").replace("B", "b")

        # Handle enharmonic equivalents
        if note in ENHARMONIC_EQUIVALENTS:
            # Keep the original for now, but we could implement preference logic
            pass

        return note

    def _note_to_midi(self, note_name: str, octave: int) -> int:
        """Convert note name and octave to MIDI number."""
        note_name = self._normalize_note_name(note_name)

        # Find note in chromatic scale
        if note_name in NOTE_NAMES:
            note_index = NOTE_NAMES.index(note_name)
        elif note_name in FLAT_NOTE_NAMES:
            note_index = FLAT_NOTE_NAMES.index(note_name)
        else:
            raise ValueError(f"Unknown note name: {note_name}")

        return (octave + 1) * 12 + note_index

    def _get_interval_name(self, semitones: int) -> str:
        """Get interval name from semitones."""
        from .constants import INTERVAL_NAMES

        return INTERVAL_NAMES.get(semitones % 12, f"{semitones}_semitones")

    def _get_degree_name(self, degree: int) -> str:
        """Get scale degree name."""
        from .constants import SCALE_DEGREE_NAMES

        return SCALE_DEGREE_NAMES.get(degree, f"degree_{degree}")

    def analyze_scale_from_notes(self, notes: List[int]) -> List[Dict[str, any]]:
        """
        Analyze a sequence of notes to identify possible scales.

        Args:
            notes: List of MIDI note numbers

        Returns:
            List of possible scale matches with confidence scores
        """
        # Extract unique pitch classes
        pitch_classes = sorted(list(set(note % 12 for note in notes)))

        if len(pitch_classes) < 5:  # Need sufficient notes for analysis
            return []

        matches = []

        # Test each possible root and scale type
        for root_pc in pitch_classes:
            for scale_name, pattern in self.patterns.items():
                # Generate expected pitch classes for this scale
                expected_pcs = {root_pc}
                current_pc = root_pc

                for interval in pattern[:-1]:  # Skip octave return
                    current_pc = (current_pc + interval) % 12
                    expected_pcs.add(current_pc)

                # Calculate match quality
                common = len(set(pitch_classes) & expected_pcs)
                missing = len(expected_pcs - set(pitch_classes))
                extra = len(set(pitch_classes) - expected_pcs)

                # Scoring: favor high common notes, penalize missing/extra
                if common >= 4:  # Require at least 4 matching notes
                    score = (common * 2) - missing - (extra * 0.5)
                    confidence = max(0, min(1, score / (len(expected_pcs) * 2)))

                    if confidence > 0.6:  # Only include high-confidence matches
                        root_note = NOTE_NAMES[root_pc]
                        matches.append(
                            {
                                "scale_name": scale_name,
                                "root": root_note,
                                "confidence": confidence,
                                "matching_notes": common,
                                "missing_notes": missing,
                                "extra_notes": extra,
                            }
                        )

        # Sort by confidence and return top matches
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches[:5]  # Return top 5 matches
