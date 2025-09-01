"""Data models for music theory components."""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union
from enum import Enum


class Quality(Enum):
    """Chord and interval qualities."""

    MAJOR = "major"
    MINOR = "minor"
    PERFECT = "perfect"
    AUGMENTED = "augmented"
    DIMINISHED = "diminished"
    DOMINANT = "dominant"


class ChordType(Enum):
    """Extended chord types."""

    TRIAD = "triad"
    SEVENTH = "seventh"
    NINTH = "ninth"
    ELEVENTH = "eleventh"
    THIRTEENTH = "thirteenth"


@dataclass
class Note:
    """Represents a musical note."""

    midi_note: int
    name: str
    octave: int

    def __post_init__(self):
        if self.octave is None:
            self.octave = self.midi_note // 12 - 1

    @classmethod
    def from_midi(cls, midi_note: int, prefer_sharps: bool = True) -> "Note":
        """Create Note from MIDI number."""
        from ..theory.constants import NOTE_NAMES, FLAT_NOTE_NAMES

        octave = midi_note // 12 - 1
        note_names = NOTE_NAMES if prefer_sharps else FLAT_NOTE_NAMES
        name = note_names[midi_note % 12]
        return cls(midi_note, name, octave)

    def __str__(self) -> str:
        return f"{self.name}{self.octave}"


@dataclass
class Interval:
    """Represents a musical interval."""

    semitones: int
    name: str
    quality: Quality

    @classmethod
    def between_notes(cls, note1: Note, note2: Note) -> "Interval":
        """Calculate interval between two notes."""
        from ..theory.constants import INTERVAL_NAMES

        semitones = abs(note2.midi_note - note1.midi_note) % 12
        name = INTERVAL_NAMES.get(semitones, f"{semitones}_semitones")

        # Determine quality based on semitones
        if semitones in [0, 5, 7, 12]:
            quality = Quality.PERFECT
        elif semitones in [4, 9, 11]:
            quality = Quality.MAJOR
        elif semitones in [3, 8, 10]:
            quality = Quality.MINOR
        elif semitones == 6:
            quality = Quality.AUGMENTED  # or diminished
        else:
            quality = Quality.MAJOR  # default

        return cls(semitones, name, quality)


@dataclass
class Scale:
    """Represents a musical scale."""

    root: Note
    name: str
    pattern: List[int]  # Interval pattern in semitones
    notes: List[Note]

    def get_degree(self, degree: int) -> Optional[Note]:
        """Get the note at a specific scale degree (1-indexed)."""
        if 1 <= degree <= len(self.notes):
            return self.notes[degree - 1]
        return None

    def get_mode(self, degree: int) -> "Scale":
        """Get a mode starting from the specified degree."""
        if not (1 <= degree <= len(self.notes)):
            raise ValueError(f"Invalid degree: {degree}")

        # Rotate pattern and notes
        new_pattern = self.pattern[degree - 1 :] + self.pattern[: degree - 1]
        new_root = self.notes[degree - 1]

        # Calculate new notes based on rotated pattern
        new_notes = [new_root]
        current_midi = new_root.midi_note

        for interval in new_pattern[:-1]:  # Exclude last interval (back to octave)
            current_midi += interval
            new_notes.append(Note.from_midi(current_midi))

        mode_names = {
            1: self.name,
            2: "dorian",
            3: "phrygian",
            4: "lydian",
            5: "mixolydian",
            6: "aeolian",
            7: "locrian",
        }

        mode_name = mode_names.get(degree, f"{self.name}_mode_{degree}")

        return Scale(new_root, mode_name, new_pattern, new_notes)


@dataclass
class Chord:
    """Represents a musical chord."""

    root: Note
    quality: Quality
    chord_type: ChordType
    notes: List[Note]
    symbol: str
    inversion: int = 0
    voicing: str = "close"

    def get_bass_note(self) -> Note:
        """Get the bass (lowest) note."""
        return self.notes[0] if self.notes else self.root

    def get_chord_tones(self) -> List[Note]:
        """Get the essential chord tones (no extensions)."""
        # For most chords, first 3-4 notes are chord tones
        if self.chord_type == ChordType.TRIAD:
            return self.notes[:3]
        elif self.chord_type == ChordType.SEVENTH:
            return self.notes[:4]
        else:
            return self.notes[:4]  # Root, 3rd, 5th, 7th

    def get_extensions(self) -> List[Note]:
        """Get the extension notes (9th, 11th, 13th, etc.)."""
        chord_tones = self.get_chord_tones()
        return [note for note in self.notes if note not in chord_tones]


@dataclass
class ChordProgression:
    """Represents a sequence of chords."""

    chords: List[Chord]
    key: str
    roman_numerals: List[str]
    durations: List[float]  # Duration of each chord in beats

    def get_total_duration(self) -> float:
        """Get total duration of the progression."""
        return sum(self.durations)

    def transpose(self, semitones: int) -> "ChordProgression":
        """Transpose the entire progression."""
        new_chords = []
        for chord in self.chords:
            new_root = Note.from_midi(chord.root.midi_note + semitones)
            new_notes = [Note.from_midi(note.midi_note + semitones) for note in chord.notes]
            new_chord = Chord(
                root=new_root,
                quality=chord.quality,
                chord_type=chord.chord_type,
                notes=new_notes,
                symbol=chord.symbol,  # This should be updated based on new root
                inversion=chord.inversion,
                voicing=chord.voicing,
            )
            new_chords.append(new_chord)

        # Calculate new key
        from ..theory.constants import NOTE_NAMES

        key_root_midi = NOTE_NAMES.index(self.key.split("m")[0]) + semitones
        new_key_root = NOTE_NAMES[key_root_midi % 12]
        new_key = new_key_root + ("m" if "m" in self.key else "")

        return ChordProgression(
            chords=new_chords, key=new_key, roman_numerals=self.roman_numerals.copy(), durations=self.durations.copy()
        )


@dataclass
class KeyAnalysis:
    """Results of key analysis."""

    most_likely_key: str
    confidence: float
    alternative_keys: List[Tuple[str, float]]  # (key, confidence) pairs
    key_changes: List[Tuple[float, str, float]]  # (timestamp, new_key, confidence)


@dataclass
class VoiceLeadingAnalysis:
    """Results of voice leading analysis."""

    smooth_score: float  # 0-100, higher is better
    problems: List[Dict[str, Union[str, int, float]]]  # List of voice leading issues
    suggestions: List[str]  # Improvement suggestions
    parallel_motion: List[Dict[str, Union[int, str]]]  # Parallel fifth/octave locations


@dataclass
class HarmonicAnalysis:
    """Comprehensive harmonic analysis results."""

    key_analysis: KeyAnalysis
    chord_progression: ChordProgression
    voice_leading: VoiceLeadingAnalysis
    cadences: List[Dict[str, Union[str, int, float]]]  # Identified cadences
    modulations: List[Dict[str, Union[str, float]]]  # Modulation points
    non_chord_tones: List[Dict[str, Union[int, str, float]]]  # NCT analysis
    harmonic_rhythm: List[float]  # Rate of harmonic change
