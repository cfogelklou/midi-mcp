"""Main composition class that orchestrates the composition process."""

from typing import Dict, Optional, Any

from .genre_manager import GenreManager
from .part_generator import PartGenerator
from .arrangement_engine import ArrangementEngine
from .analysis_engine import AnalysisEngine


class Composer:
    """High-level composition facade."""

    def __init__(self, genre_manager: Optional[GenreManager] = None):
        """Initialize the composer.

        Args:
            genre_manager: Optional genre manager instance
        """
        self.genre_manager = genre_manager or GenreManager()
        self.libraries = self.genre_manager.libraries
        self.part_generator = PartGenerator(self.libraries)
        self.arrangement_engine = ArrangementEngine()
        self.analysis_engine = AnalysisEngine(self.libraries)

    def create_progression(
        self, genre: str, key: str, variation: str = "standard", bars: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create authentic chord progression for any genre."""
        progression = self.genre_manager.create_progression_from_library(genre, key, variation)

        if bars:
            progression["bars"] = bars
            progression = self.part_generator.adjust_progression_length(progression, bars)

        genre_data = self.genre_manager.get_genre_data(genre)
        progression["tempo_range"] = genre_data.get("tempo_range", [120, 120])
        progression["typical_feel"] = genre_data.get("rhythms", {}).get("standard", {}).get("feel", "straight")

        return progression

    def create_melody(
        self, genre: str, key: str, progression: Dict[str, Any], style: str = "typical"
    ) -> Dict[str, Any]:
        """Generate authentic melody for any genre."""
        genre_data = self.genre_manager.get_genre_data(genre)
        scale_names = genre_data.get("scales", ["major"])

        scale_notes = []
        if self.libraries.music21.is_available():
            for scale_name in scale_names:
                notes = self.libraries.music21.get_scale_notes(scale_name, key)
                if notes:
                    scale_notes = notes
                    break

        if not scale_notes:
            scale_notes = ["C", "D", "E", "F", "G", "A", "B"]

        melody = self.part_generator.generate_melody_from_progression(progression, scale_notes, style, genre)

        return {
            "genre": genre,
            "key": key,
            "style": style,
            "scale_used": scale_names[0] if scale_names else "major",
            "scale_notes": scale_notes,
            "melody": melody,
            "characteristics": self.analysis_engine.analyze_melody_characteristics(melody, genre),
        }

    def create_beat(
        self, genre: str, tempo: int, complexity: str = "medium", variation: str = "standard"
    ) -> Dict[str, Any]:
        """Create authentic drum patterns for any genre."""
        genre_data = self.genre_manager.get_genre_data(genre)
        rhythms = genre_data.get("rhythms", {})

        if variation in rhythms:
            rhythm_pattern = rhythms[variation]
        else:
            rhythm_pattern = rhythms.get("standard", {"feel": "straight", "emphasis": [1, 3], "subdivision": "quarter"})

        beat_pattern = self.part_generator.generate_beat_pattern(rhythm_pattern, tempo, complexity, genre)

        return {
            "genre": genre,
            "tempo": tempo,
            "complexity": complexity,
            "variation": variation,
            "feel": rhythm_pattern.get("feel", "straight"),
            "emphasis": rhythm_pattern.get("emphasis", [1, 3]),
            "subdivision": rhythm_pattern.get("subdivision", "quarter"),
            "pattern": beat_pattern,
            "measures": 4,
            "time_signature": "4/4",
        }

    def create_bass_line(self, genre: str, progression: Dict[str, Any], style: str = "typical") -> Dict[str, Any]:
        """Generate authentic bass lines for any genre."""
        if "chords" not in progression:
            return {"error": "Progression must contain chord information"}

        bass_line = self.part_generator.generate_bass_line_from_chords(progression["chords"], style, genre)

        genre_data = self.genre_manager.get_genre_data(genre)
        instrumentation = genre_data.get("instrumentation", {})

        return {
            "genre": genre,
            "style": style,
            "key": progression.get("key"),
            "bass_line": bass_line,
            "voice_leading": self.analysis_engine.analyze_bass_voice_leading(bass_line),
            "typical_instruments": instrumentation.get("typical", ["bass"]),
            "pattern_length": len(bass_line),
        }

    def create_arrangement(
        self, genre: str, song_structure: Dict[str, Any], instrumentation: str = "standard"
    ) -> Dict[str, Any]:
        """Create full band arrangement for any genre."""
        genre_data = self.genre_manager.get_genre_data(genre)
        instruments = self.arrangement_engine.select_instruments_for_arrangement(genre_data, instrumentation)

        arrangement = {
            "genre": genre,
            "instrumentation_level": instrumentation,
            "selected_instruments": instruments,
            "parts": {},
            "texture": self.arrangement_engine.determine_texture(genre, instrumentation),
            "dynamics": self.arrangement_engine.create_dynamic_plan(song_structure, genre),
        }

        for instrument in instruments:
            part = self.part_generator.generate_instrument_part(instrument, song_structure, genre)
            arrangement["parts"][instrument] = part

        return arrangement
