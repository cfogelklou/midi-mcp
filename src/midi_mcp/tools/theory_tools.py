"""Music theory MCP tools for Phase 3 implementation."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import json

from ..theory import ScaleManager, ChordManager, ProgressionManager, KeyManager, VoiceLeadingManager, MusicAnalyzer
from ..models.theory_models import Note


def register_theory_tools(app: FastMCP) -> None:
    """
    Register all music theory tools with the MCP server.

    Args:
        app: FastMCP application instance
    """
    # Initialize theory managers
    scale_manager = ScaleManager()
    chord_manager = ChordManager()
    progression_manager = ProgressionManager()
    key_manager = KeyManager()
    voice_leading_manager = VoiceLeadingManager()
    music_analyzer = MusicAnalyzer()

    # Scale Tools
    @app.tool(name="get_scale_notes")
    async def get_scale_notes(root_note: str, scale_type: str, octave: int = 4) -> List[TextContent]:
        """
        Generate notes for a specific scale.

        Args:
            root_note: Root note (C, C#, Db, D, etc.)
            scale_type: Scale type (major, minor, dorian, mixolydian, etc.)
            octave: Starting octave (0-9)

        Returns:
            List of MIDI note numbers and note names in the scale
        """
        try:
            scale = scale_manager.generate_scale(root_note, scale_type, octave)

            result = {
                "root": scale.root.name,
                "scale_type": scale.name,
                "notes": [
                    {"name": note.name, "midi_note": note.midi_note, "octave": note.octave} for note in scale.notes
                ],
                "pattern": scale.pattern,
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error generating scale: {str(e)}")]

    @app.tool(name="identify_intervals")
    async def identify_intervals(notes: List[int]) -> List[TextContent]:
        """
        Identify intervals between consecutive notes.

        Args:
            notes: List of MIDI note numbers

        Returns:
            List of interval types and information
        """
        try:
            intervals = scale_manager.identify_intervals(notes)

            return [TextContent(type="text", text=json.dumps(intervals, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error identifying intervals: {str(e)}")]

    @app.tool(name="transpose_to_key")
    async def transpose_to_key(notes: List[int], from_key: str, to_key: str) -> List[TextContent]:
        """
        Transpose a sequence of notes from one key to another.

        Args:
            notes: Original MIDI note numbers
            from_key: Original key (C, G, F#, etc.)
            to_key: Target key

        Returns:
            Transposed MIDI note numbers
        """
        try:
            transposed = scale_manager.transpose_to_key(notes, from_key, to_key)

            result = {"original_notes": notes, "from_key": from_key, "to_key": to_key, "transposed_notes": transposed}

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error transposing: {str(e)}")]

    # Chord Tools
    @app.tool(name="build_chord")
    async def build_chord(
        root_note: str, chord_type: str, inversion: int = 0, voicing: str = "close"
    ) -> List[TextContent]:
        """
        Build a chord with specified parameters.

        Args:
            root_note: Root note of chord (C, F#, Bb, etc.)
            chord_type: Chord quality (major, minor, dom7, maj7, min7, etc.)
            inversion: Chord inversion (0=root position, 1=first, etc.)
            voicing: Voicing style (close, open, drop2, drop3)

        Returns:
            MIDI note numbers and chord analysis
        """
        try:
            chord = chord_manager.build_chord(root_note, chord_type, inversion, voicing)

            result = {
                "root": chord.root.name,
                "symbol": chord.symbol,
                "quality": chord.quality.value,
                "type": chord.chord_type.value,
                "inversion": chord.inversion,
                "voicing": chord.voicing,
                "notes": [
                    {"name": note.name, "midi_note": note.midi_note, "octave": note.octave} for note in chord.notes
                ],
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error building chord: {str(e)}")]

    @app.tool(name="analyze_chord")
    async def analyze_chord(notes: List[int]) -> List[TextContent]:
        """
        Analyze a set of notes to identify chord(s).

        Args:
            notes: MIDI note numbers to analyze

        Returns:
            Possible chord interpretations with confidence scores
        """
        try:
            analysis = chord_manager.analyze_chord(notes)

            return [TextContent(type="text", text=json.dumps(analysis, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing chord: {str(e)}")]

    @app.tool(name="get_chord_tones_and_extensions")
    async def get_chord_tones_and_extensions(chord_symbol: str) -> List[TextContent]:
        """
        Break down a chord symbol into component tones.

        Args:
            chord_symbol: Chord symbol (Cmaj7, F#dim, Bb7sus4, etc.)

        Returns:
            Root, chord tones, available tensions, avoid notes
        """
        try:
            analysis = chord_manager.get_chord_tones_and_extensions(chord_symbol)

            # Convert Note objects to dictionaries for JSON serialization
            def note_to_dict(note):
                return {"name": note.name, "midi_note": note.midi_note, "octave": note.octave}

            result = {
                "chord_symbol": chord_symbol,
                "root": note_to_dict(analysis["root"]) if analysis.get("root") else None,
                "chord_tones": [note_to_dict(note) for note in analysis.get("chord_tones", [])],
                "extensions": [note_to_dict(note) for note in analysis.get("extensions", [])],
                "available_tensions": analysis.get("available_tensions", []),
                "avoid_notes": [note_to_dict(note) for note in analysis.get("avoid_notes", [])],
                "chord_type": analysis.get("chord_type", ""),
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing chord symbol: {str(e)}")]

    # Progression Tools
    @app.tool(name="create_chord_progression")
    async def create_chord_progression(
        key: str, progression: List[str], duration_per_chord: float = 1.0
    ) -> List[TextContent]:
        """
        Create a chord progression in a specific key.

        Args:
            key: Key signature (C, Am, F#, Bbm, etc.)
            progression: Roman numeral progression (["I", "vi", "ii", "V"])
            duration_per_chord: Duration of each chord in beats

        Returns:
            MIDI data for the chord progression
        """
        try:
            chord_progression = progression_manager.create_chord_progression(key, progression, duration_per_chord)

            result = {
                "key": chord_progression.key,
                "roman_numerals": chord_progression.roman_numerals,
                "durations": chord_progression.durations,
                "total_duration": chord_progression.get_total_duration(),
                "chords": [
                    {
                        "symbol": chord.symbol,
                        "root": chord.root.name,
                        "notes": [
                            {"name": note.name, "midi_note": note.midi_note, "octave": note.octave}
                            for note in chord.notes
                        ],
                    }
                    for chord in chord_progression.chords
                ],
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error creating chord progression: {str(e)}")]

    @app.tool(name="analyze_progression")
    async def analyze_progression(chord_symbols: List[str], key: Optional[str] = None) -> List[TextContent]:
        """
        Analyze the harmonic function of a chord progression.

        Args:
            chord_symbols: List of chord symbols (["C", "Am", "F", "G"])
            key: Key context (auto-detected if None)

        Returns:
            Roman numeral analysis, key relationships, voice leading quality
        """
        try:
            analysis = progression_manager.analyze_progression(chord_symbols, key)

            return [TextContent(type="text", text=json.dumps(analysis, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing progression: {str(e)}")]

    @app.tool(name="suggest_next_chord")
    async def suggest_next_chord(
        current_progression: List[str], key: str, style: str = "common_practice"
    ) -> List[TextContent]:
        """
        Suggest logical next chords for a progression.

        Args:
            current_progression: Existing chord progression (roman numerals)
            key: Key signature
            style: Harmonic style (common_practice, jazz, pop, modal)

        Returns:
            List of suggested chords with probability scores
        """
        try:
            suggestions = progression_manager.suggest_next_chord(current_progression, key, style)

            return [TextContent(type="text", text=json.dumps(suggestions, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error suggesting next chord: {str(e)}")]

    # Key Analysis Tools
    @app.tool(name="detect_key")
    async def detect_key(midi_notes: List[int]) -> List[TextContent]:
        """
        Detect the key(s) of a sequence of MIDI notes.

        Args:
            midi_notes: List of MIDI note numbers to analyze

        Returns:
            Most likely key(s) with confidence scores
        """
        try:
            analysis = key_manager.detect_key(midi_notes)

            result = {
                "most_likely_key": analysis.most_likely_key,
                "confidence": analysis.confidence,
                "alternative_keys": analysis.alternative_keys,
                "key_changes": analysis.key_changes,
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error detecting key: {str(e)}")]

    @app.tool(name="suggest_modulation")
    async def suggest_modulation(from_key: str, to_key: str) -> List[TextContent]:
        """
        Suggest ways to modulate between two keys.

        Args:
            from_key: Starting key
            to_key: Target key

        Returns:
            Pivot chords, common tones, modulation strategies
        """
        try:
            suggestions = key_manager.suggest_modulation(from_key, to_key)

            return [TextContent(type="text", text=json.dumps(suggestions, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error suggesting modulation: {str(e)}")]

    # Voice Leading Tools
    @app.tool(name="validate_voice_leading")
    async def validate_voice_leading(chord_symbols: List[str]) -> List[TextContent]:
        """
        Validate voice leading in a chord progression.

        Args:
            chord_symbols: List of chord symbols to analyze

        Returns:
            Voice leading analysis with problems and suggestions
        """
        try:
            # Convert chord symbols to Chord objects
            chords = []
            for symbol in chord_symbols:
                # Simple parsing for common chord symbols
                root = symbol[0] if symbol else "C"
                chord_type = "minor" if "m" in symbol and "maj" not in symbol else "major"
                chord = chord_manager.build_chord(root, chord_type)
                chords.append(chord)

            analysis = voice_leading_manager.validate_voice_leading(chords)

            result = {
                "smooth_score": analysis.smooth_score,
                "problems": analysis.problems,
                "suggestions": analysis.suggestions,
                "parallel_motion": analysis.parallel_motion,
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error validating voice leading: {str(e)}")]

    # Comprehensive Analysis Tool
    @app.tool(name="analyze_music")
    async def analyze_music(midi_notes: List[int], timestamps: Optional[List[float]] = None) -> List[TextContent]:
        """
        Create complete harmonic analysis of MIDI data.

        Args:
            midi_notes: List of MIDI note numbers
            timestamps: Optional timestamps for temporal analysis

        Returns:
            Comprehensive analysis including key, harmony, voice leading
        """
        try:
            analysis = music_analyzer.analyze_midi_file(midi_notes, timestamps)

            # Convert complex objects to serializable format
            result = {
                "key_analysis": {
                    "most_likely_key": analysis.key_analysis.most_likely_key,
                    "confidence": analysis.key_analysis.confidence,
                    "alternative_keys": analysis.key_analysis.alternative_keys,
                },
                "voice_leading_score": analysis.voice_leading.smooth_score,
                "voice_leading_problems": len(analysis.voice_leading.problems),
                "cadences": analysis.cadences,
                "modulations": analysis.modulations,
                "non_chord_tones": len(analysis.non_chord_tones),
                "harmonic_rhythm": analysis.harmonic_rhythm,
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing music: {str(e)}")]

    # Utility Tools
    @app.tool(name="get_available_scales")
    async def get_available_scales() -> List[TextContent]:
        """Get list of all available scale types."""
        try:
            scales = scale_manager.get_available_scales()
            return [TextContent(type="text", text=json.dumps(scales, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting scales: {str(e)}")]

    @app.tool(name="get_common_progressions")
    async def get_common_progressions(style: Optional[str] = None) -> List[TextContent]:
        """
        Get library of common chord progressions.

        Args:
            style: Optional style filter (classical, jazz, pop, blues)

        Returns:
            Dictionary of progression names and chord sequences
        """
        try:
            progressions = progression_manager.get_common_progressions(style)
            return [TextContent(type="text", text=json.dumps(progressions, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting progressions: {str(e)}")]
