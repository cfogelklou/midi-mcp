"""Analyzes musical elements."""

from typing import Dict, List, Any

class AnalysisEngine:
    """Analyzes musical elements."""

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
            "genre_appropriateness": "high" if chord_tone_ratio > 0.6 else "medium"
        }

    def analyze_bass_voice_leading(self, bass_line: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bass voice leading quality."""
        if len(bass_line) < 2:
            return {"quality": "insufficient_data"}
        
        # Check for large leaps (simplified)
        large_leaps = 0
        for i in range(1, len(bass_line)):
            # This would need proper interval calculation with music21
            large_leaps += 0  # Placeholder
        
        return {
            "quality": "smooth" if large_leaps == 0 else "moderate",
            "large_leaps": large_leaps,
            "recommendations": ["Consider adding passing tones"] if large_leaps > 2 else []
        }
