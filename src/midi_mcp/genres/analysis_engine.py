"""Analyzes musical elements."""

from typing import Dict, List, Any, Optional
from .library_integration import LibraryIntegration


class AnalysisEngine:
    """Analyzes musical elements."""

    def __init__(self, libraries: Optional[LibraryIntegration] = None):
        """Initialize analysis engine.

        Args:
            libraries: Optional library integration instance
        """
        self.libraries = libraries or LibraryIntegration()

    def analyze_melody_characteristics(self, melody: List[Dict[str, Any]], genre: str) -> Dict[str, Any]:
        """Analyze melodic characteristics."""
        if not melody:
            return {}

        # Basic analysis
        notes = [note["note"] for note in melody]
        chord_tone_ratio = len([n for n in melody if n.get("relation_to_chord") == "chord_tone"]) / len(melody)

        return {
            "note_count": len(notes),
            "range": f"{notes[0]} to {notes[-1]}",
            "chord_tone_ratio": round(chord_tone_ratio, 2),
            "genre_appropriateness": "high" if chord_tone_ratio > 0.6 else "medium",
        }

    def analyze_bass_voice_leading(self, bass_line: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bass voice leading quality."""
        if len(bass_line) < 2:
            return {"quality": "insufficient_data"}

        # Check for large leaps using music21
        large_leaps = 0
        leap_details = []

        for i in range(1, len(bass_line)):
            current_note = bass_line[i].get("note")
            previous_note = bass_line[i - 1].get("note")

            if current_note and previous_note:
                if self.libraries.music21.is_available():
                    is_leap = self.libraries.music21.is_large_leap(previous_note, current_note, threshold_semitones=7)
                    if is_leap:
                        large_leaps += 1
                        interval = self.libraries.music21.calculate_interval_semitones(previous_note, current_note)
                        leap_details.append(
                            {
                                "from": previous_note,
                                "to": current_note,
                                "interval_semitones": interval,
                                "beat": bass_line[i].get("beat"),
                            }
                        )

        quality = "smooth" if large_leaps == 0 else "moderate" if large_leaps <= 2 else "choppy"
        recommendations = []

        if large_leaps > 2:
            recommendations.append("Consider adding passing tones to smooth large leaps")
        if large_leaps > 4:
            recommendations.append("Voice leading could be significantly improved with stepwise motion")

        return {
            "quality": quality,
            "large_leaps": large_leaps,
            "leap_details": leap_details,
            "recommendations": recommendations,
        }
