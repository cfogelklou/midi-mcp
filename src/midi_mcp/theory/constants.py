"""Music theory constants and data structures."""

from typing import Dict, List, Tuple

# Note names and MIDI mapping
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT_NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
ENHARMONIC_EQUIVALENTS = {
    "C#": "Db",
    "Db": "C#",
    "D#": "Eb",
    "Eb": "D#",
    "F#": "Gb",
    "Gb": "F#",
    "G#": "Ab",
    "Ab": "G#",
    "A#": "Bb",
    "Bb": "A#",
}

# Scale intervals (in semitones)
SCALE_PATTERNS = {
    # Major scales and modes
    "major": [2, 2, 1, 2, 2, 2, 1],
    "ionian": [2, 2, 1, 2, 2, 2, 1],  # Same as major
    "dorian": [2, 1, 2, 2, 2, 1, 2],
    "phrygian": [1, 2, 2, 2, 1, 2, 2],
    "lydian": [2, 2, 2, 1, 2, 2, 1],
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],
    "aeolian": [2, 1, 2, 2, 1, 2, 2],  # Same as natural minor
    "locrian": [1, 2, 2, 1, 2, 2, 2],
    # Minor scales
    "natural_minor": [2, 1, 2, 2, 1, 2, 2],
    "harmonic_minor": [2, 1, 2, 2, 1, 3, 1],
    "melodic_minor": [2, 1, 2, 2, 2, 2, 1],
    # Pentatonic scales
    "major_pentatonic": [2, 2, 3, 2, 3],
    "minor_pentatonic": [3, 2, 2, 3, 2],
    # Blues scales
    "major_blues": [2, 1, 1, 3, 2, 3],
    "minor_blues": [3, 2, 1, 1, 3, 2],
    # Jazz scales
    "altered": [1, 2, 1, 2, 2, 2, 2],  # Super locrian
    "whole_tone": [2, 2, 2, 2, 2, 2],
    "diminished": [2, 1, 2, 1, 2, 1, 2, 1],  # Octatonic
    "half_diminished": [2, 1, 2, 2, 1, 2, 2],  # Locrian #2
    # World music scales
    "harmonic_major": [2, 2, 1, 2, 1, 3, 1],
    "hungarian_minor": [2, 1, 3, 1, 1, 3, 1],
    "neapolitan_minor": [1, 2, 2, 2, 1, 3, 1],
    "neapolitan_major": [1, 2, 2, 2, 2, 2, 1],
}

# Chord intervals (from root)
CHORD_PATTERNS = {
    # Basic triads
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    # Suspended chords
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "sus2sus4": [0, 2, 5, 7],
    # Seventh chords
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "7": [0, 4, 7, 10],  # Dominant 7
    "dim7": [0, 3, 6, 9],
    "half_dim7": [0, 3, 6, 10],  # m7b5
    "aug7": [0, 4, 8, 10],
    "minmaj7": [0, 3, 7, 11],
    # Extended chords - 9ths
    "maj9": [0, 4, 7, 11, 14],
    "min9": [0, 3, 7, 10, 14],
    "9": [0, 4, 7, 10, 14],
    "7b9": [0, 4, 7, 10, 13],
    "7#9": [0, 4, 7, 10, 15],
    "add9": [0, 4, 7, 14],
    "madd9": [0, 3, 7, 14],
    # Extended chords - 11ths
    "maj11": [0, 4, 7, 11, 14, 17],
    "min11": [0, 3, 7, 10, 14, 17],
    "11": [0, 4, 7, 10, 14, 17],
    "add11": [0, 4, 7, 17],
    "madd11": [0, 3, 7, 17],
    # Extended chords - 13ths
    "maj13": [0, 4, 7, 11, 14, 17, 21],
    "min13": [0, 3, 7, 10, 14, 17, 21],
    "13": [0, 4, 7, 10, 14, 17, 21],
    "7b13": [0, 4, 7, 10, 20],
    "add13": [0, 4, 7, 21],
    "madd13": [0, 3, 7, 21],
}

# Roman numeral mappings for major keys
MAJOR_KEY_FUNCTIONS = {
    1: "I",  # Tonic
    2: "ii",  # Supertonic
    3: "iii",  # Mediant
    4: "IV",  # Subdominant
    5: "V",  # Dominant
    6: "vi",  # Submediant
    7: "vii°",  # Leading tone
}

# Roman numeral mappings for minor keys
MINOR_KEY_FUNCTIONS = {
    1: "i",  # Tonic
    2: "ii°",  # Supertonic
    3: "III",  # Mediant
    4: "iv",  # Subdominant
    5: "v",  # Dominant (natural minor)
    6: "VI",  # Submediant
    7: "VII",  # Subtonic
}

# Harmonic minor functions (different V and vii)
HARMONIC_MINOR_FUNCTIONS = {
    **MINOR_KEY_FUNCTIONS,
    5: "V",  # Dominant (major in harmonic minor)
    7: "vii°",  # Leading tone diminished
}

# Circle of fifths
CIRCLE_OF_FIFTHS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "Ab", "Eb", "Bb", "F"]

# Key signatures (number of sharps/flats)
KEY_SIGNATURES = {
    "C": 0,
    "G": 1,
    "D": 2,
    "A": 3,
    "E": 4,
    "B": 5,
    "F#": 6,
    "C#": 7,
    "F": -1,
    "Bb": -2,
    "Eb": -3,
    "Ab": -4,
    "Db": -5,
    "Gb": -6,
    "Cb": -7,
}

# Common chord progressions
COMMON_PROGRESSIONS = {
    "classical": {
        "authentic_cadence": ["V", "I"],
        "plagal_cadence": ["IV", "I"],
        "deceptive_cadence": ["V", "vi"],
        "circle_of_fifths": ["vi", "ii", "V", "I"],
        "pachelbel": ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
    },
    "jazz": {
        "ii_V_I": ["ii", "V", "I"],
        "ii_V_I_vi": ["ii", "V", "I", "vi"],
        "iii_vi_ii_V": ["iii", "vi", "ii", "V"],
        "rhythm_changes_A": ["I", "vi", "ii", "V"],
        "turnaround": ["I", "vi", "ii", "V"],
    },
    "pop": {
        "vi_IV_I_V": ["vi", "IV", "I", "V"],  # Very common in pop
        "I_V_vi_IV": ["I", "V", "vi", "IV"],  # Also very popular
        "I_vi_IV_V": ["I", "vi", "IV", "V"],  # 50s progression
        "vi_V_IV_V": ["vi", "V", "IV", "V"],
    },
    "blues": {
        "twelve_bar_blues": ["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"],
        "quick_change": ["I", "IV", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"],
        "minor_blues": ["i", "i", "i", "i", "iv", "iv", "i", "i", "V", "iv", "i", "V"],
    },
}

# Interval names and semitones
INTERVAL_NAMES = {
    0: "unison",
    1: "minor2nd",
    2: "major2nd",
    3: "minor3rd",
    4: "major3rd",
    5: "perfect4th",
    6: "tritone",
    7: "perfect5th",
    8: "minor6th",
    9: "major6th",
    10: "minor7th",
    11: "major7th",
    12: "octave",
}

# Voice leading preferences (penalty scores)
VOICE_LEADING_RULES = {
    "max_voice_range": 12,  # Maximum semitones a voice should move
    "parallel_fifths_penalty": 100,
    "parallel_octaves_penalty": 100,
    "hidden_fifths_penalty": 50,
    "hidden_octaves_penalty": 50,
    "large_leap_penalty": 10,  # Per semitone over preferred range
    "voice_crossing_penalty": 75,
    "doubled_leading_tone_penalty": 80,
}

# Scale degrees names
SCALE_DEGREE_NAMES = {
    1: "tonic",
    2: "supertonic",
    3: "mediant",
    4: "subdominant",
    5: "dominant",
    6: "submediant",
    7: "leading_tone",  # Or 'subtonic' in natural minor
}

# Non-chord tones
NON_CHORD_TONE_TYPES = [
    "passing_tone",
    "neighbor_tone",
    "suspension",
    "retardation",
    "anticipation",
    "escape_tone",
    "appoggiatura",
    "cambiata",
]
