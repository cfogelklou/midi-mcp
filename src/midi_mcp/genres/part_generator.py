"""Generates musical parts for different instruments."""

from typing import Dict, List, Any
import random

class PartGenerator:
    """Generates musical parts."""

    def generate_melody_from_progression(self, progression: Dict[str, Any], 
                                        scale_notes: List[str], style: str, genre: str) -> List[Dict[str, Any]]:
        """Generate melody notes from chord progression."""
        melody = []
        chords = progression.get("chords", [])
        
        for i, chord_info in enumerate(chords):
            if isinstance(chord_info, dict) and "notes" in chord_info:
                # Select melody note from chord tones or scale
                chord_notes = chord_info["notes"]
                
                if style == "simple":
                    # Use chord root
                    melody_note = chord_notes[0] if chord_notes else scale_notes[0]
                elif style == "complex":
                    # Use chord extensions or scale passages
                    melody_note = random.choice(chord_notes + scale_notes[:4])
                else:
                    # Typical - balance chord tones and passing notes
                    available_notes = chord_notes + scale_notes[:3]
                    melody_note = random.choice(available_notes)
                
                melody.append({
                    "note": melody_note,
                    "beat": i + 1,
                    "duration": 1.0,
                    "relation_to_chord": "chord_tone" if melody_note in chord_notes else "scale_tone"
                })
        
        return melody

    def generate_beat_pattern(self, rhythm_pattern: Dict[str, Any], tempo: int, 
                             complexity: str, genre: str) -> List[Dict[str, Any]]:
        """Generate drum beat pattern."""
        feel = rhythm_pattern.get("feel", "straight")
        emphasis = rhythm_pattern.get("emphasis", [1, 3])
        
        # Basic 4/4 pattern
        pattern = []
        for beat in range(1, 5):
            kick = beat in emphasis
            snare = beat in [2, 4] if complexity != "simple" else beat == 2
            hihat = True if complexity in ["medium", "complex"] else beat in [1, 3]
            
            pattern.append({
                "beat": beat,
                "kick": kick,
                "snare": snare,
                "hihat": hihat,
                "feel_modifier": "swing" if feel == "swing" else "straight"
            })
        
        return pattern

    def generate_bass_line_from_chords(self, chords: List[Dict[str, Any]], 
                                      style: str, genre: str) -> List[Dict[str, Any]]:
        """Generate bass line from chord progression."""
        bass_line = []
        
        for i, chord_info in enumerate(chords):
            if isinstance(chord_info, dict) and "root" in chord_info:
                root_note = chord_info["root"]
                
                if style == "walking" and i < len(chords) - 1:
                    # Add passing tones for walking bass
                    bass_line.append({
                        "note": root_note,
                        "beat": i * 4 + 1,
                        "duration": 2.0
                    })
                    # Add passing tone
                    bass_line.append({
                        "note": self._get_passing_tone(root_note),
                        "beat": i * 4 + 3,
                        "duration": 2.0
                    })
                else:
                    # Simple root note bass
                    bass_line.append({
                        "note": root_note,
                        "beat": i * 4 + 1,
                        "duration": 4.0
                    })
        
        return bass_line

    def generate_instrument_part(self, instrument: str, song_structure: Dict[str, Any], 
                                genre: str) -> Dict[str, Any]:
        """Generate a part for a specific instrument."""
        return {
            "instrument": instrument,
            "role": self._determine_instrument_role(instrument, genre),
            "pattern_type": self._determine_pattern_type(instrument, genre),
            "notes": [],  # Would be filled with actual notes
            "articulation": self._get_instrument_articulation(instrument, genre),
            "dynamics": "mf"  # Default
        }

    def _get_passing_tone(self, note: str) -> str:
        """Get a passing tone between notes (simplified)."""
        # This is a simplified approach - could be enhanced with music21
        note_names = ["C", "D", "E", "F", "G", "A", "B"]
        if note in note_names:
            idx = note_names.index(note)
            return note_names[(idx + 1) % len(note_names)]
        return note

    def adjust_progression_length(self, progression: Dict[str, Any], target_bars: int) -> Dict[str, Any]:
        """Adjust progression length to match target bars."""
        current_length = len(progression["pattern"])
        
        if current_length == target_bars:
            return progression
        elif current_length < target_bars:
            # Repeat pattern to fill bars
            repeats = target_bars // current_length
            remainder = target_bars % current_length
            new_pattern = progression["pattern"] * repeats + progression["pattern"][:remainder]
            progression["pattern"] = new_pattern
            progression["chords"] = progression["chords"] * repeats + progression["chords"][:remainder]
        else:
            # Truncate pattern
            progression["pattern"] = progression["pattern"][:target_bars]
            progression["chords"] = progression["chords"][:target_bars]
        
        return progression
