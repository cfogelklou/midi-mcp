# -*- coding: utf-8 -*-
"""
Constants and tool information for MIDI MCP server.

Contains tool descriptions, parameters, and help information for all available tools.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from typing import Dict, List, Any

# Import all music theory constants
from .theory.constants import (
    NOTE_NAMES,
    FLAT_NOTE_NAMES, 
    ENHARMONIC_EQUIVALENTS,
    SCALE_PATTERNS,
    CHORD_PATTERNS,
    MAJOR_KEY_FUNCTIONS,
    MINOR_KEY_FUNCTIONS,
    HARMONIC_MINOR_FUNCTIONS,
    CIRCLE_OF_FIFTHS,
    KEY_SIGNATURES,
    COMMON_PROGRESSIONS,
    INTERVAL_NAMES,
    VOICE_LEADING_RULES,
    SCALE_DEGREE_NAMES,
    NON_CHORD_TONE_TYPES,
)

# Tool categories
TOOL_CATEGORIES = {
    "server": "Server Status and Management",
    "midi_devices": "MIDI Device Management",
    "midi_files": "MIDI File Operations", 
    "music_theory": "Music Theory and Analysis",
    "genre_tools": "Genre-Specific Tools",
    "composition": "Music Composition Tools",
}

# Comprehensive tool definitions with help information
TOOL_DEFINITIONS = {
    # Server Management Tools
    "server_status": {
        "category": "server",
        "description": "Get the current status of the MIDI MCP server",
        "parameters": {},
        "returns": "Server status including connected devices, loaded files, and active playbacks",
        "examples": ["server_status()"]
    },
    
    # MIDI Device Management Tools
    "discover_midi_devices": {
        "category": "midi_devices", 
        "description": "Discover available MIDI devices and return device information",
        "parameters": {},
        "returns": "List of available MIDI input and output devices with their capabilities",
        "examples": ["discover_midi_devices()"]
    },
    "connect_midi_device": {
        "category": "midi_devices",
        "description": "Connect to a specific MIDI device for input or output",
        "parameters": {
            "device_name": "Name of the MIDI device to connect to",
            "device_type": "Type of connection ('input', 'output', or 'both')"
        },
        "returns": "Connection status and device information",
        "examples": [
            "connect_midi_device('USB MIDI Device', 'output')",
            "connect_midi_device('Built-in Output', 'both')"
        ]
    },
    "play_midi_note": {
        "category": "midi_devices",
        "description": "Play a single MIDI note through a connected device",
        "parameters": {
            "device_name": "Name of the connected MIDI output device", 
            "note": "MIDI note number (0-127) or note name (e.g., 'C4', 'F#5')",
            "velocity": "Note velocity (1-127, optional, default: 64)",
            "duration": "Note duration in seconds (optional, default: 1.0)",
            "channel": "MIDI channel (1-16, optional, default: 1)"
        },
        "returns": "Confirmation of note playback",
        "examples": [
            "play_midi_note('USB MIDI Device', 60, 80, 0.5)",
            "play_midi_note('Built-in Output', 'C4', 100, 2.0, 10)"
        ]
    },
    "list_connected_devices": {
        "category": "midi_devices",
        "description": "List currently connected MIDI devices",
        "parameters": {},
        "returns": "List of connected MIDI devices with connection details",
        "examples": ["list_connected_devices()"]
    },
    "disconnect_midi_device": {
        "category": "midi_devices", 
        "description": "Disconnect from a MIDI device",
        "parameters": {
            "device_name": "Name of the device to disconnect"
        },
        "returns": "Disconnection status",
        "examples": ["disconnect_midi_device('USB MIDI Device')"]
    },
    
    # MIDI File Operations
    "create_midi_file": {
        "category": "midi_files",
        "description": "Create a new MIDI file with basic metadata",
        "parameters": {
            "filename": "Name for the MIDI file",
            "tempo": "Tempo in BPM (optional, default: 120)",
            "time_signature": "Time signature as [numerator, denominator] (optional, default: [4, 4])",
            "key_signature": "Key signature (optional, default: 'C')"
        },
        "returns": "MIDI file creation confirmation and file ID",
        "examples": [
            "create_midi_file('my_song.mid')",
            "create_midi_file('jazz_tune.mid', 140, [4, 4], 'Bb')"
        ]
    },
    "add_track": {
        "category": "midi_files",
        "description": "Add a new track to an existing MIDI file",
        "parameters": {
            "file_id": "ID of the MIDI file",
            "track_name": "Name for the new track",
            "instrument": "MIDI instrument/program number (optional, default: 1)",
            "channel": "MIDI channel (optional, default: 1)"
        },
        "returns": "Track creation confirmation and track ID", 
        "examples": [
            "add_track('file123', 'Piano')",
            "add_track('file123', 'Bass', 33, 2)"
        ]
    },
    "save_midi_file": {
        "category": "midi_files",
        "description": "Save MIDI file to disk",
        "parameters": {
            "file_id": "ID of the MIDI file to save",
            "filepath": "Path where to save the file (optional)"
        },
        "returns": "File save confirmation and path",
        "examples": [
            "save_midi_file('file123')",
            "save_midi_file('file123', '/path/to/output.mid')"
        ]
    },
    "load_midi_file": {
        "category": "midi_files",
        "description": "Load a MIDI file from disk",
        "parameters": {
            "filepath": "Path to the MIDI file to load"
        },
        "returns": "File load confirmation, file ID, and basic file information",
        "examples": ["load_midi_file('/path/to/song.mid')"]
    },
    "play_midi_file": {
        "category": "midi_files",
        "description": "Play a loaded MIDI file in real-time through a specified device",
        "parameters": {
            "file_id": "ID of the loaded MIDI file",
            "device_name": "Name of the MIDI output device",
            "start_time": "Start time in seconds (optional, default: 0)",
            "loop": "Whether to loop playback (optional, default: False)"
        },
        "returns": "Playback start confirmation",
        "examples": [
            "play_midi_file('file123', 'USB MIDI Device')",
            "play_midi_file('file123', 'Built-in Output', 30, True)"
        ]
    },
    "analyze_midi_file": {
        "category": "midi_files",
        "description": "Analyze a loaded MIDI file for detailed musical information",
        "parameters": {
            "file_id": "ID of the loaded MIDI file"
        },
        "returns": "Comprehensive analysis including key signatures, chord progressions, tempo changes, and track information",
        "examples": ["analyze_midi_file('file123')"]
    },
    "list_midi_files": {
        "category": "midi_files",
        "description": "List all MIDI files in the current session",
        "parameters": {},
        "returns": "List of loaded MIDI files with basic information",
        "examples": ["list_midi_files()"]
    },
    "stop_midi_playback": {
        "category": "midi_files",
        "description": "Stop MIDI file playback",
        "parameters": {
            "playback_id": "ID of the playback to stop (optional, stops all if not specified)"
        },
        "returns": "Playback stop confirmation",
        "examples": [
            "stop_midi_playback()",
            "stop_midi_playback('playback456')"
        ]
    },
    "add_musical_data_to_midi_file": {
        "category": "midi_files",
        "description": "Add musical note data to a specified track within a MIDI file",
        "parameters": {
            "file_id": "ID of the MIDI file",
            "track_id": "ID of the track",
            "notes": "List of note data with timing, pitch, velocity, and duration",
            "start_time": "Start time offset in beats (optional, default: 0)"
        },
        "returns": "Confirmation of data addition",
        "examples": [
            "add_musical_data_to_midi_file('file123', 'track1', [{'note': 60, 'velocity': 80, 'start': 0, 'duration': 1}])"
        ]
    },
    
    # Music Theory Tools  
    "get_scale_notes": {
        "category": "music_theory",
        "description": "Get the notes in a specific scale",
        "parameters": {
            "root_note": "Root note of the scale (e.g., 'C', 'F#')",
            "scale_type": "Type of scale (e.g., 'major', 'minor', 'dorian', 'pentatonic')"
        },
        "returns": "List of notes in the scale with MIDI note numbers",
        "examples": [
            "get_scale_notes('C', 'major')",
            "get_scale_notes('A', 'minor')",
            "get_scale_notes('D', 'dorian')"
        ]
    },
    "identify_intervals": {
        "category": "music_theory", 
        "description": "Identify intervals between notes",
        "parameters": {
            "notes": "List of note names or MIDI numbers"
        },
        "returns": "Analysis of intervals between the notes",
        "examples": [
            "identify_intervals(['C', 'E', 'G'])",
            "identify_intervals([60, 64, 67])"
        ]
    },
    "transpose_to_key": {
        "category": "music_theory",
        "description": "Transpose a set of notes or chords to a different key",
        "parameters": {
            "notes_or_chords": "Notes or chord symbols to transpose",
            "from_key": "Original key",
            "to_key": "Target key"
        },
        "returns": "Transposed notes or chord symbols",
        "examples": [
            "transpose_to_key(['C', 'Dm', 'G'], 'C', 'G')",
            "transpose_to_key([60, 62, 64], 'C', 'F')"
        ]
    },
    "build_chord": {
        "category": "music_theory",
        "description": "Build a chord from a root note and chord type",
        "parameters": {
            "root": "Root note of the chord",
            "chord_type": "Type of chord (e.g., 'major', 'minor', 'dom7', 'maj7')"
        },
        "returns": "Chord notes with MIDI numbers and note names",
        "examples": [
            "build_chord('C', 'major')",
            "build_chord('F#', 'dom7')",
            "build_chord('Bb', 'min7')"
        ]
    },
    "analyze_chord": {
        "category": "music_theory",
        "description": "Analyze a chord to determine its type and function",
        "parameters": {
            "notes": "List of notes in the chord (note names or MIDI numbers)"
        },
        "returns": "Chord analysis including possible chord names and functions",
        "examples": [
            "analyze_chord(['C', 'E', 'G'])",
            "analyze_chord([60, 64, 67, 70])"
        ]
    },
    "get_chord_tones_and_extensions": {
        "category": "music_theory",
        "description": "Get chord tones and available extensions for a chord",
        "parameters": {
            "chord_symbol": "Chord symbol (e.g., 'Cmaj7', 'F#m7b5')"
        },
        "returns": "Chord tones, available extensions, and avoid notes",
        "examples": [
            "get_chord_tones_and_extensions('Cmaj7')",
            "get_chord_tones_and_extensions('G7alt')"
        ]
    },
    "create_chord_progression": {
        "category": "music_theory",
        "description": "Create a chord progression in a specific key and style",
        "parameters": {
            "key": "Key signature",
            "progression_type": "Type of progression or Roman numerals",
            "length": "Number of chords (optional)"
        },
        "returns": "Chord progression with chord symbols and Roman numeral analysis",
        "examples": [
            "create_chord_progression('C', 'ii-V-I')",
            "create_chord_progression('Am', 'i-VI-VII-i', 8)"
        ]
    },
    "analyze_progression": {
        "category": "music_theory",
        "description": "Analyze a chord progression for key, function, and voice leading",
        "parameters": {
            "chords": "List of chord symbols"
        },
        "returns": "Analysis including key center, Roman numerals, and voice leading quality",
        "examples": [
            "analyze_progression(['C', 'Am', 'F', 'G'])",
            "analyze_progression(['Dm7', 'G7', 'Cmaj7'])"
        ]
    },
    "suggest_next_chord": {
        "category": "music_theory",
        "description": "Suggest next chord options based on current progression",
        "parameters": {
            "current_progression": "Current chord progression",
            "key": "Key signature (optional)",
            "style": "Musical style preference (optional)"
        },
        "returns": "List of suggested next chords with functional explanations",
        "examples": [
            "suggest_next_chord(['C', 'Am'], 'C')",
            "suggest_next_chord(['Dm7', 'G7'], 'C', 'jazz')"
        ]
    },
    "detect_key": {
        "category": "music_theory",
        "description": "Detect the key signature from a set of notes or chords",
        "parameters": {
            "notes_or_chords": "List of notes or chord symbols to analyze"
        },
        "returns": "Most likely key signatures with confidence scores",
        "examples": [
            "detect_key(['C', 'D', 'E', 'F', 'G', 'A', 'B'])",
            "detect_key(['C', 'Am', 'F', 'G'])"
        ]
    },
    "suggest_modulation": {
        "category": "music_theory",
        "description": "Suggest modulation options from current key",
        "parameters": {
            "from_key": "Current key",
            "modulation_type": "Type of modulation (optional: 'circle_of_fifths', 'relative', 'parallel')"
        },
        "returns": "List of modulation targets with transition chord suggestions",
        "examples": [
            "suggest_modulation('C')",
            "suggest_modulation('Am', 'circle_of_fifths')"
        ]
    },
    "validate_voice_leading": {
        "category": "music_theory",
        "description": "Validate and analyze voice leading between chord progressions",
        "parameters": {
            "progression": "Chord progression with voicings"
        },
        "returns": "Voice leading analysis with rules violations and suggestions",
        "examples": [
            "validate_voice_leading([['C3', 'E3', 'G3'], ['F3', 'A3', 'C4']])"
        ]
    },
    "analyze_music": {
        "category": "music_theory", 
        "description": "Comprehensive musical analysis of notes, chords, or progressions",
        "parameters": {
            "musical_data": "Musical data to analyze (notes, chords, or MIDI data)"
        },
        "returns": "Complete musical analysis including harmony, melody, rhythm, and form",
        "examples": [
            "analyze_music(['C', 'E', 'G', 'Am', 'F', 'G'])"
        ]
    },
    "get_available_scales": {
        "category": "music_theory",
        "description": "Get list of available scale types",
        "parameters": {},
        "returns": "List of all available scale types with descriptions",
        "examples": ["get_available_scales()"]
    },
    "get_common_progressions": {
        "category": "music_theory",
        "description": "Get common chord progressions for different musical styles",
        "parameters": {
            "style": "Musical style (optional: 'jazz', 'classical', 'pop', 'blues')"
        },
        "returns": "List of common progressions for the specified style",
        "examples": [
            "get_common_progressions('jazz')",
            "get_common_progressions()"
        ]
    },
    
    # Composition Tools
    "create_song_structure": {
        "category": "composition",
        "description": "Generate a complete song structure template",
        "parameters": {
            "genre": "Musical genre (affects typical structures)",
            "song_type": "Type of song (optional: 'ballad', 'uptempo', 'epic', default: 'standard')",
            "duration": "Target duration in seconds (optional, default: 180)"
        },
        "returns": "Song structure with sections, durations, key areas, and arrangement notes",
        "examples": [
            "create_song_structure('jazz')",
            "create_song_structure('rock', 'ballad', 240)"
        ]
    },
    "generate_song_section": {
        "category": "composition",
        "description": "Generate a specific song section with appropriate characteristics",
        "parameters": {
            "section_type": "Type of section ('intro', 'verse', 'chorus', 'bridge', 'solo', 'outro')",
            "genre": "Musical genre for style guidance",
            "key": "Key signature",
            "previous_section": "Previous section for continuity (optional)"
        },
        "returns": "Complete section with melody, harmony, rhythm, and arrangement",
        "examples": [
            "generate_song_section('verse', 'jazz', 'C')",
            "generate_song_section('chorus', 'pop', 'G')"
        ]
    },
    "create_section_transitions": {
        "category": "composition",
        "description": "Create smooth transitions between song sections",
        "parameters": {
            "from_section": "Source section information",
            "to_section": "Target section information",
            "transition_type": "Type of transition (optional: 'fill', 'turnaround', 'modulation')"
        },
        "returns": "Transition measures with harmonic and rhythmic elements",
        "examples": [
            "create_section_transitions(verse_data, chorus_data)",
            "create_section_transitions(chorus_data, bridge_data, 'modulation')"
        ]
    },
    "develop_melodic_motif": {
        "category": "composition",
        "description": "Develop a melodic motif through various compositional techniques",
        "parameters": {
            "motif": "Base melodic motif as list of notes",
            "development_techniques": "List of development techniques (optional)",
            "target_length": "Target length for development (optional)"
        },
        "returns": "Developed motif variations with technique annotations",
        "examples": [
            "develop_melodic_motif([60, 62, 64])",
            "develop_melodic_motif([67, 65, 64], ['inversion', 'augmentation'])"
        ]
    },
    "create_melodic_phrase": {
        "category": "composition", 
        "description": "Create a melodic phrase that fits over chord progressions",
        "parameters": {
            "chord_progression": "Chord progression as context",
            "phrase_length": "Length in measures (optional, default: 4)",
            "style": "Melodic style preference (optional)",
            "range": "Note range constraints (optional)"
        },
        "returns": "Melodic phrase with rhythmic and harmonic analysis",
        "examples": [
            "create_melodic_phrase(['C', 'Am', 'F', 'G'])",
            "create_melodic_phrase(['Dm7', 'G7', 'Cmaj7'], 2, 'jazz')"
        ]
    },
    "vary_melody_for_repetition": {
        "category": "composition",
        "description": "Create variations of a melody to avoid exact repetition",
        "parameters": {
            "original_melody": "Original melody to vary",
            "variation_type": "Type of variation (optional: 'rhythmic', 'ornamental', 'harmonic')",
            "intensity": "Variation intensity (optional: 'subtle', 'moderate', 'significant')"
        },
        "returns": "Varied melody with analysis of changes made",
        "examples": [
            "vary_melody_for_repetition(melody_data)",
            "vary_melody_for_repetition(melody_data, 'ornamental', 'subtle')"
        ]
    },
    "optimize_voice_leading": {
        "category": "composition",
        "description": "Optimize voice leading in chord progressions",
        "parameters": {
            "progression": "Chord progression with voicings",
            "voice_count": "Number of voices (optional, default: 4)",
            "style": "Voice leading style (optional: 'classical', 'jazz', 'pop')"
        },
        "returns": "Optimized voicings with voice leading analysis",
        "examples": [
            "optimize_voice_leading(chord_progression)",
            "optimize_voice_leading(progression, 3, 'jazz')"
        ]
    },
    "add_chromatic_harmony": {
        "category": "composition",
        "description": "Add chromatic harmony and passing chords to progressions",
        "parameters": {
            "base_progression": "Base chord progression",
            "density": "Chromatic density (optional: 'light', 'medium', 'heavy')",
            "style": "Harmonic style (optional: 'classical', 'jazz', 'contemporary')"
        },
        "returns": "Enhanced progression with chromatic harmony",
        "examples": [
            "add_chromatic_harmony(['C', 'F', 'G'])",
            "add_chromatic_harmony(progression, 'medium', 'jazz')"
        ]
    },
    "create_bass_line_with_voice_leading": {
        "category": "composition",
        "description": "Create a bass line with good voice leading principles",
        "parameters": {
            "chord_progression": "Chord progression for bass line",
            "style": "Bass line style (optional: 'walking', 'root_position', 'melodic')",
            "rhythm_pattern": "Rhythmic pattern preference (optional)"
        },
        "returns": "Bass line with voice leading analysis",
        "examples": [
            "create_bass_line_with_voice_leading(['Dm7', 'G7', 'Cmaj7'])",
            "create_bass_line_with_voice_leading(progression, 'walking')"
        ]
    },
    "arrange_for_ensemble": {
        "category": "composition",
        "description": "Arrange a composition for a specific ensemble",
        "parameters": {
            "composition": "Composition data to arrange",
            "ensemble_type": "Type of ensemble (e.g., 'string_quartet', 'jazz_combo', 'big_band')",
            "arrangement_style": "Arrangement style preference (optional)"
        },
        "returns": "Arranged composition with part assignments and orchestration",
        "examples": [
            "arrange_for_ensemble(composition_data, 'string_quartet')",
            "arrange_for_ensemble(song_data, 'jazz_combo', 'traditional')"
        ]
    },
    "create_counter_melodies": {
        "category": "composition", 
        "description": "Create counter-melodies that complement the main melody",
        "parameters": {
            "main_melody": "Primary melody to complement",
            "harmony": "Underlying harmony",
            "voices": "Number of counter-melodies (optional, default: 1)",
            "style": "Counterpoint style (optional: 'species', 'free', 'jazz')"
        },
        "returns": "Counter-melodies with counterpoint analysis",
        "examples": [
            "create_counter_melodies(melody_data, harmony_data)",
            "create_counter_melodies(melody, chords, 2, 'species')"
        ]
    },
    "orchestrate_texture_changes": {
        "category": "composition",
        "description": "Orchestrate dynamic texture changes throughout a composition",
        "parameters": {
            "composition": "Base composition data",
            "texture_plan": "Plan for texture changes (optional)",
            "ensemble": "Target ensemble (optional)"
        },
        "returns": "Composition with orchestrated texture variations",
        "examples": [
            "orchestrate_texture_changes(composition_data)",
            "orchestrate_texture_changes(song, texture_plan, 'orchestra')"
        ]
    },
    "compose_complete_song": {
        "category": "composition",
        "description": "Compose a complete song from high-level parameters",
        "parameters": {
            "genre": "Musical genre",
            "mood": "Mood or emotion to convey",
            "duration": "Target duration in seconds (optional, default: 180)",
            "key": "Key signature (optional)",
            "tempo": "Tempo in BPM (optional)",
            "ensemble": "Target ensemble (optional)"
        },
        "returns": "Complete composition with all musical elements",
        "examples": [
            "compose_complete_song('jazz', 'relaxed')",
            "compose_complete_song('rock', 'energetic', 240, 'E', 120, 'rock_band')"
        ]
    },
    "analyze_composition_quality": {
        "category": "composition",
        "description": "Analyze the quality and effectiveness of a composition",
        "parameters": {
            "composition": "Composition to analyze"
        },
        "returns": "Quality analysis with strengths, weaknesses, and suggestions",
        "examples": [
            "analyze_composition_quality(composition_data)"
        ]
    },
    "refine_composition": {
        "category": "composition", 
        "description": "Refine and improve an existing composition",
        "parameters": {
            "composition": "Composition to refine",
            "focus_areas": "Areas to focus on (optional: list of aspects to improve)",
            "style_preferences": "Style preferences for refinement (optional)"
        },
        "returns": "Refined composition with change annotations",
        "examples": [
            "refine_composition(composition_data)",
            "refine_composition(song, ['harmony', 'melody'], 'contemporary')"
        ]
    },
}

# Tool help information organized by category
TOOL_HELP_BY_CATEGORY = {
    category: {
        tool_name: tool_info 
        for tool_name, tool_info in TOOL_DEFINITIONS.items() 
        if tool_info["category"] == category
    }
    for category in TOOL_CATEGORIES.keys()
}

# Quick reference for tool parameter validation
REQUIRED_PARAMETERS = {
    tool_name: [
        param for param, desc in tool_info["parameters"].items()
        if not desc.endswith("(optional)") and "(optional" not in desc
    ]
    for tool_name, tool_info in TOOL_DEFINITIONS.items()
    if "parameters" in tool_info and tool_info["parameters"]
}

# Common parameter values for validation (using imported theory constants)
COMMON_PARAMETER_VALUES = {
    "scale_types": list(SCALE_PATTERNS.keys()),
    "chord_types": list(CHORD_PATTERNS.keys()),
    "device_types": ["input", "output", "both"],
    "progression_types": [
        "ii-V-I", "I-vi-IV-V", "vi-IV-I-V", "circle_of_fifths",
        "twelve_bar_blues", "rhythm_changes", "classical_cadence"
    ],
    "modulation_types": ["circle_of_fifths", "relative", "parallel", "chromatic", "enharmonic"],
    "musical_styles": ["jazz", "classical", "pop", "blues", "rock", "folk", "electronic"],
    "note_names": NOTE_NAMES + FLAT_NOTE_NAMES,
    "keys": list(KEY_SIGNATURES.keys()),
    "intervals": list(INTERVAL_NAMES.values()),
    "section_types": ["intro", "verse", "chorus", "bridge", "solo", "outro"],
    "song_types": ["standard", "ballad", "uptempo", "epic"],
    "ensemble_types": [
        "piano_solo", "string_quartet", "jazz_combo", "big_band", "rock_band", 
        "orchestra", "choir", "electronic"
    ],
    "arrangement_styles": ["traditional", "contemporary", "minimal", "full"],
    "voice_leading_styles": ["classical", "jazz", "pop"],
    "bass_line_styles": ["walking", "root_position", "melodic"],
    "counterpoint_styles": ["species", "free", "jazz"],
    "variation_types": ["rhythmic", "ornamental", "harmonic"],
    "variation_intensities": ["subtle", "moderate", "significant"],
    "chromatic_densities": ["light", "medium", "heavy"],
    "harmonic_styles": ["classical", "jazz", "contemporary"]
}

# Ensemble definitions (moved from arrangement.py)
ENSEMBLE_DEFINITIONS = {
    "piano_solo": {
        "name": "Piano Solo",
        "instruments": ["piano"],
        "typical_ranges": {"piano": (21, 108)},  # A0 to C8
        "texture_capabilities": ["melody", "harmony", "bass", "counter_melody"],
        "style_characteristics": {"versatility": "high", "dynamic_range": "full"}
    },
    "string_quartet": {
        "name": "String Quartet",
        "instruments": ["violin_1", "violin_2", "viola", "cello"],
        "typical_ranges": {
            "violin_1": (55, 103),  # G3 to G7
            "violin_2": (55, 96),   # G3 to C7
            "viola": (48, 84),     # C3 to C6
            "cello": (36, 76)      # C2 to E5
        },
        "texture_capabilities": ["melody", "harmony", "counter_melody", "bass"],
        "style_characteristics": {"blend": "excellent", "articulation": "precise"}
    },
    "jazz_combo": {
        "name": "Jazz Combo",
        "instruments": ["piano", "bass", "drums", "lead"],
        "typical_ranges": {
            "piano": (21, 108),
            "bass": (28, 67),      # E1 to G4
            "drums": (35, 81),     # Kick to crash
            "lead": (60, 96)       # Horn/guitar range
        },
        "texture_capabilities": ["melody", "harmony", "bass", "rhythm", "improvisation"],
        "style_characteristics": {"swing": True, "improvisation": "high"}
    },
    "big_band": {
        "name": "Big Band",
        "instruments": ["lead_trumpet", "trumpet2", "trumpet3", "trombone1", "trombone2", 
                       "alto_sax1", "alto_sax2", "tenor_sax1", "tenor_sax2", "bari_sax",
                       "piano", "bass", "drums"],
        "typical_ranges": {
            "lead_trumpet": (58, 82),    # Bb3 to Bb5
            "trumpet2": (58, 79),        
            "trumpet3": (58, 77),        
            "trombone1": (40, 72),       # E2 to C5
            "trombone2": (40, 69),       
            "alto_sax1": (49, 84),       # Db3 to C6
            "alto_sax2": (49, 81),       
            "tenor_sax1": (44, 77),      # Ab2 to F5
            "tenor_sax2": (44, 74),      
            "bari_sax": (37, 69),        # Db2 to A4
            "piano": (21, 108),
            "bass": (28, 67),
            "drums": (35, 81)
        },
        "texture_capabilities": ["melody", "harmony", "bass", "rhythm", "section_work"],
        "style_characteristics": {"power": "high", "section_blend": "excellent"}
    },
    "rock_band": {
        "name": "Rock Band", 
        "instruments": ["lead_guitar", "rhythm_guitar", "bass", "drums", "vocals"],
        "typical_ranges": {
            "lead_guitar": (40, 84),     # E2 to C6
            "rhythm_guitar": (40, 76),   
            "bass": (28, 55),            # E1 to G3
            "drums": (35, 81),
            "vocals": (55, 84)           # G3 to C6
        },
        "texture_capabilities": ["melody", "harmony", "bass", "rhythm", "power"],
        "style_characteristics": {"drive": "high", "amplification": True}
    },
    "orchestra": {
        "name": "Orchestra",
        "instruments": ["flute", "oboe", "clarinet", "bassoon", "horn", "trumpet", "trombone", 
                       "tuba", "timpani", "violin_1", "violin_2", "viola", "cello", "double_bass"],
        "typical_ranges": {
            "flute": (60, 96),           # C4 to C7
            "oboe": (58, 89),            # Bb3 to F6
            "clarinet": (50, 89),        # D3 to F6
            "bassoon": (34, 72),         # Bb1 to C5
            "horn": (41, 77),            # F2 to F5
            "trumpet": (55, 82),         # G3 to Bb5
            "trombone": (40, 72),        # E2 to C5
            "tuba": (28, 53),            # E1 to F3
            "timpani": (35, 60),         # Bb1 to C4
            "violin_1": (55, 103),        # G3 to G7
            "violin_2": (55, 96),         # G3 to C7
            "viola": (48, 84),           # C3 to C6
            "cello": (36, 76),           # C2 to E5
            "double_bass": (28, 55)      # E1 to G3
        },
        "texture_capabilities": ["melody", "harmony", "bass", "orchestral_color", "dynamics"],
        "style_characteristics": {"range": "full", "color": "maximum", "dynamics": "extreme"}
    }
}

# Dynamic level mappings (replacing hardcoded strings)
DYNAMIC_LEVELS = {
    "ppp": 10,   # Pianississimo
    "pp": 20,    # Pianissimo  
    "p": 35,     # Piano
    "mp": 50,    # Mezzo-piano
    "mf": 65,    # Mezzo-forte
    "f": 80,     # Forte
    "ff": 95,    # Fortissimo
    "fff": 110   # Fortississimo
}

# Section type to dynamic level mapping
SECTION_DYNAMICS = {
    "intro": "p",
    "verse": "mp", 
    "chorus": "f",
    "bridge": "mf",
    "solo": "f",
    "outro": "pp"
}

# Instrument role mappings (moved from arrangement.py)
INSTRUMENT_ROLES = {
    # Keyboard instruments
    "piano": ["melody", "harmony", "bass", "accompaniment"],
    "organ": ["harmony", "bass", "sustained"],
    "harpsichord": ["melody", "accompaniment"],
    
    # String instruments  
    "violin_1": ["melody", "harmony"],
    "violin_2": ["harmony", "counter_melody"],
    "viola": ["harmony", "inner_voice"],
    "cello": ["bass", "melody", "harmony"],
    "double_bass": ["bass"],
    "guitar": ["melody", "harmony", "rhythm"],
    "lead_guitar": ["melody", "solo"],
    "rhythm_guitar": ["harmony", "rhythm"],
    "bass": ["bass", "rhythm"],
    
    # Wind instruments
    "flute": ["melody", "counter_melody"],
    "oboe": ["melody", "color"],
    "clarinet": ["melody", "harmony"],
    "bassoon": ["bass", "color"],
    "horn": ["harmony", "color"],
    "trumpet": ["melody", "fanfare"],
    "trombone": ["harmony", "bass"],
    "tuba": ["bass"],
    
    # Saxophones
    "alto_sax": ["melody", "harmony"],
    "tenor_sax": ["melody", "harmony"],
    "bari_sax": ["bass", "harmony"],
    
    # Percussion
    "drums": ["rhythm", "dynamics"],
    "timpani": ["bass", "accent"],
    
    # Vocals
    "vocals": ["melody", "lyrics"],
    "lead_vocals": ["melody", "lyrics"],
    "backing_vocals": ["harmony", "texture"]
}

# Fallback chord progressions by genre (moved from complete_composer.py)
GENRE_FALLBACK_PROGRESSIONS = {
    "pop": ["I", "vi", "IV", "V"],
    "rock": ["I", "VII", "IV", "I"],
    "jazz": ["ii", "V", "I", "vi"],
    "blues": ["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"],
    "classical": ["I", "V", "vi", "IV"],
    "folk": ["I", "IV", "V", "I"],
    "country": ["I", "V", "vi", "V"]
}

# Title generation stop words (moved from complete_composer.py)
TITLE_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", "were",
    "been", "be", "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "shall"
}

# MIDI and Music Constants
# Standard MIDI note numbers for octave 4
MIDDLE_C_MIDI = 60
OCTAVE_SEMITONES = 12

# Default fallback melodies (C-D-E-F pattern)
DEFAULT_MELODY_NOTES = [60, 62, 64, 65]  # C4-D4-E4-F4
DEFAULT_RHYTHM_PATTERN = [0.25, 0.25, 0.25, 0.25]  # Quarter notes

# Register ranges for different moods/styles
REGISTER_RANGES = {
    "low": (36, 60),      # C2 to C4
    "middle": (48, 72),   # C3 to C5  
    "high": (60, 84),     # C4 to C6
    "very_high": (72, 96), # C5 to C7
}

# Mood-based adjustments
MOOD_ADJUSTMENTS = {
    "happy": {
        "chromatic_adjust": [2 if note % 12 in [1, 3, 6, 8, 10] else 0 for note in range(12)],
        "register_shift": +12,  # Higher register
        "register_threshold": 60
    },
    "sad": {
        "chromatic_adjust": [0] * 12,  # Keep natural
        "register_shift": -12,  # Lower register  
        "register_threshold": 72
    },
    "energetic": {
        "register_shift": +12,
        "register_threshold": 48
    },
    "calm": {
        "register_shift": 0,
        "register_threshold": 60
    }
}

# API Consistency Helper Functions
def normalize_composition_input(composition):
    """
    Normalize composition input to ensure consistent data structure.
    Converts Dict input to standardized format compatible with Composition objects.
    
    Args:
        composition: Either a Dict or Composition object
        
    Returns:
        Dict with standardized keys: melody, harmony, structure, metadata
    """
    if isinstance(composition, dict):
        return {
            "melody": composition.get("melody", {}),
            "harmony": composition.get("harmony", []), 
            "structure": composition.get("structure", {}),
            "metadata": composition.get("metadata", {})
        }
    else:  # Composition object
        return {
            "melody": getattr(composition, "melody", {}),
            "harmony": getattr(composition, "harmony", []),
            "structure": getattr(composition, "structure", {}),
            "metadata": getattr(composition, "metadata", {})
        }

def get_dynamic_level_value(dynamic_string: str) -> int:
    """
    Convert dynamic level string to MIDI velocity value.
    
    Args:
        dynamic_string: Dynamic marking (e.g., "p", "mf", "ff")
        
    Returns:
        MIDI velocity value (0-127)
    """
    return DYNAMIC_LEVELS.get(dynamic_string.lower(), 64)  # Default to mf

def get_section_dynamic(section_type: str) -> str:
    """
    Get appropriate dynamic level for a section type.
    
    Args:
        section_type: Type of musical section
        
    Returns:
        Dynamic level string
    """
    return SECTION_DYNAMICS.get(section_type.lower(), "mf")

def validate_ensemble_type(ensemble_type: str) -> bool:
    """
    Validate if ensemble type is supported.
    
    Args:
        ensemble_type: Ensemble type to validate
        
    Returns:
        True if valid ensemble type
    """
    return ensemble_type in ENSEMBLE_DEFINITIONS

def get_ensemble_info(ensemble_type: str) -> dict:
    """
    Get complete ensemble definition.
    
    Args:
        ensemble_type: Type of ensemble
        
    Returns:
        Ensemble definition dict or empty dict if not found
    """
    return ENSEMBLE_DEFINITIONS.get(ensemble_type, {})

def validate_genre(genre: str) -> bool:
    """
    Validate if genre has fallback progressions defined.
    
    Args:
        genre: Genre to validate
        
    Returns:
        True if genre is supported
    """
    return genre.lower() in GENRE_FALLBACK_PROGRESSIONS

def get_genre_fallback_progression(genre: str) -> list:
    """
    Get fallback chord progression for a genre.
    
    Args:
        genre: Musical genre
        
    Returns:
        List of chord symbols
    """
    return GENRE_FALLBACK_PROGRESSIONS.get(genre.lower(), ["I", "vi", "IV", "V"])

def note_name_to_midi(note_name: str, octave: int = 4) -> int:
    """Convert note name to MIDI number using music21."""
    from music21 import note
    music21_note = note.Note(f"{note_name}{octave}")
    return music21_note.pitch.midi

def chord_symbol_to_midi_root(chord_symbol: str, octave: int = 4) -> int:
    """Extract root note from chord symbol and convert to MIDI using music21."""
    from music21 import harmony
    chord = harmony.ChordSymbol(chord_symbol)
    root_note = chord.root().name
    return note_name_to_midi(root_note, octave)

def apply_mood_adjustments(melody_notes: list, mood: str) -> list:
    """
    Apply mood-based adjustments to melody notes.
    
    Args:
        melody_notes: List of MIDI note numbers
        mood: Mood string ('happy', 'sad', 'energetic', 'calm')
        
    Returns:
        Adjusted list of MIDI note numbers
    """
    if mood not in MOOD_ADJUSTMENTS:
        return melody_notes
    
    adjustments = MOOD_ADJUSTMENTS[mood]
    adjusted_notes = melody_notes.copy()
    
    # Apply chromatic adjustments if specified
    if "chromatic_adjust" in adjustments:
        chromatic_adj = adjustments["chromatic_adjust"]
        adjusted_notes = [
            note + chromatic_adj[note % OCTAVE_SEMITONES] 
            for note in adjusted_notes
        ]
    
    # Apply register shifts
    if "register_shift" in adjustments and "register_threshold" in adjustments:
        shift = adjustments["register_shift"]
        threshold = adjustments["register_threshold"]
        
        if shift > 0:  # Shift higher
            adjusted_notes = [
                note + shift if note < threshold else note 
                for note in adjusted_notes
            ]
        elif shift < 0:  # Shift lower
            adjusted_notes = [
                note + shift if note > threshold else note 
                for note in adjusted_notes
            ]
    
    return adjusted_notes

def get_default_melody_notes() -> list:
    """Get default melody pattern (C-D-E-F)."""
    return DEFAULT_MELODY_NOTES.copy()

def get_default_rhythm_pattern() -> list:
    """Get default rhythm pattern (quarter notes).""" 
    return DEFAULT_RHYTHM_PATTERN.copy()

def get_section_energy_level(section_type, genre_data: dict) -> float:
    """
    Get energy level for section type (consolidated from duplicated methods).
    
    Args:
        section_type: Section type (SectionType enum or string)
        genre_data: Genre data containing base energy level
        
    Returns:
        Energy level between 0.0 and 1.0
    """
    # Handle both enum and string types
    section_str = section_type.value if hasattr(section_type, 'value') else str(section_type).lower()
    
    base_energy = genre_data.get("energy_level", 0.5)
    energy_modifiers = {
        "intro": -0.2,
        "verse": -0.1,
        "chorus": +0.2,
        "bridge": +0.1,
        "solo": +0.3,
        "breakdown": -0.3,
        "build_up": +0.4,
        "outro": -0.2,
    }
    modifier = energy_modifiers.get(section_str, 0.0)
    return max(0.0, min(1.0, base_energy + modifier))

def convert_roman_to_chord_symbol(roman_numeral: str, key: str) -> str:
    """Convert Roman numeral to chord symbol using music21."""
    from music21 import roman, key as music21_key
    
    # Parse the key
    if 'major' in key.lower():
        key_obj = music21_key.Key(key.replace(' major', ''), 'major')
    elif 'minor' in key.lower() or 'm' in key.lower():
        key_name = key.replace(' minor', '').replace('m', '')
        key_obj = music21_key.Key(key_name, 'minor')
    else:
        # Determine if major or minor by common patterns
        minor_keys = ['am', 'em', 'bm', 'f#m', 'c#m', 'g#m', 'd#m', 'dm', 'gm', 'cm', 'fm', 'bbm', 'ebm', 'abm', 'dbm', 'gbm']
        key_obj = music21_key.Key(key.replace('m', ''), 'minor') if key.lower() in minor_keys else music21_key.Key(key, 'major')
    
    # Create Roman numeral object and convert to chord
    roman_obj = roman.RomanNumeral(roman_numeral, key_obj)
    return roman_obj.figure