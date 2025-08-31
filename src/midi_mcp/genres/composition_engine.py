"""Generic composition engine that works with any genre."""

from typing import Dict, List, Optional, Any, Tuple
import random
from .library_integration import LibraryIntegration
from .genre_manager import GenreManager

class GenericComposer:
    """Generic composition engine using music theory libraries and genre knowledge."""
    
    def __init__(self, genre_manager: Optional[GenreManager] = None):
        """Initialize the generic composer.
        
        Args:
            genre_manager: Optional genre manager instance
        """
        self.genre_manager = genre_manager or GenreManager()
        self.libraries = self.genre_manager.libraries
    
    def create_progression(self, genre: str, key: str, variation: str = "standard", 
                          bars: Optional[int] = None) -> Dict[str, Any]:
        """Create authentic chord progression for any genre.
        
        Args:
            genre: Musical genre
            key: Key signature 
            variation: Progression variation (standard, jazz, modern, etc.)
            bars: Number of bars (optional)
            
        Returns:
            Complete chord progression with analysis
        """
        # Get genre-specific progression using libraries
        progression = self.genre_manager.create_progression_from_library(genre, key, variation)
        
        # Add timing and structure information
        if bars:
            progression["bars"] = bars
            # Extend or truncate pattern to fit bars
            progression = self._adjust_progression_length(progression, bars)
        
        # Add genre-specific characteristics
        genre_data = self.genre_manager.get_genre_data(genre)
        progression["tempo_range"] = genre_data.get("tempo_range", [120, 120])
        progression["typical_feel"] = genre_data.get("rhythms", {}).get("standard", {}).get("feel", "straight")
        
        return progression
    
    def create_melody(self, genre: str, key: str, progression: Dict[str, Any], 
                     style: str = "typical") -> Dict[str, Any]:
        """Generate authentic melody for any genre.
        
        Args:
            genre: Musical genre
            key: Key signature
            progression: Underlying chord progression
            style: Melodic style (typical, simple, complex, ornate)
            
        Returns:
            Melodic line with analysis
        """
        # Get genre characteristics
        genre_data = self.genre_manager.get_genre_data(genre)
        scale_names = genre_data.get("scales", ["major"])
        
        # Get scale notes using music21
        scale_notes = []
        if self.libraries.music21.is_available():
            for scale_name in scale_names:
                notes = self.libraries.music21.get_scale_notes(scale_name, key)
                if notes:
                    scale_notes = notes
                    break
        
        if not scale_notes:
            # Fallback to basic major scale
            scale_notes = ["C", "D", "E", "F", "G", "A", "B"]
        
        # Generate melody based on chord progression
        melody = self._generate_melody_from_progression(progression, scale_notes, style, genre)
        
        return {
            "genre": genre,
            "key": key,
            "style": style,
            "scale_used": scale_names[0] if scale_names else "major",
            "scale_notes": scale_notes,
            "melody": melody,
            "characteristics": self._analyze_melody_characteristics(melody, genre)
        }
    
    def create_beat(self, genre: str, tempo: int, complexity: str = "medium",
                   variation: str = "standard") -> Dict[str, Any]:
        """Create authentic drum patterns for any genre.
        
        Args:
            genre: Musical genre
            tempo: Tempo in BPM
            complexity: Rhythmic complexity (simple, medium, complex)
            variation: Beat variation (standard, shuffle, swing, etc.)
            
        Returns:
            Drum pattern with timing and characteristics
        """
        # Get genre rhythm characteristics
        genre_data = self.genre_manager.get_genre_data(genre)
        rhythms = genre_data.get("rhythms", {})
        
        # Select appropriate rhythm pattern
        if variation in rhythms:
            rhythm_pattern = rhythms[variation]
        else:
            rhythm_pattern = rhythms.get("standard", {
                "feel": "straight",
                "emphasis": [1, 3],
                "subdivision": "quarter"
            })
        
        # Generate beat pattern based on genre and complexity
        beat_pattern = self._generate_beat_pattern(rhythm_pattern, tempo, complexity, genre)
        
        return {
            "genre": genre,
            "tempo": tempo,
            "complexity": complexity,
            "variation": variation,
            "feel": rhythm_pattern.get("feel", "straight"),
            "emphasis": rhythm_pattern.get("emphasis", [1, 3]),
            "subdivision": rhythm_pattern.get("subdivision", "quarter"),
            "pattern": beat_pattern,
            "measures": 4,  # Standard 4-measure pattern
            "time_signature": "4/4"  # Default time signature
        }
    
    def create_bass_line(self, genre: str, progression: Dict[str, Any], 
                        style: str = "typical") -> Dict[str, Any]:
        """Generate authentic bass lines for any genre.
        
        Args:
            genre: Musical genre
            progression: Chord progression to follow
            style: Bass style (typical, walking, simple, complex)
            
        Returns:
            Bass line with voice leading analysis
        """
        if "chords" not in progression:
            return {"error": "Progression must contain chord information"}
        
        # Generate bass line based on chord roots and genre style
        bass_line = self._generate_bass_line_from_chords(progression["chords"], style, genre)
        
        # Get genre-specific bass characteristics
        genre_data = self.genre_manager.get_genre_data(genre)
        instrumentation = genre_data.get("instrumentation", {})
        
        return {
            "genre": genre,
            "style": style,
            "key": progression.get("key"),
            "bass_line": bass_line,
            "voice_leading": self._analyze_bass_voice_leading(bass_line),
            "typical_instruments": instrumentation.get("typical", ["bass"]),
            "pattern_length": len(bass_line)
        }
    
    def create_arrangement(self, genre: str, song_structure: Dict[str, Any], 
                          instrumentation: str = "standard") -> Dict[str, Any]:
        """Create full band arrangement for any genre.
        
        Args:
            genre: Musical genre
            song_structure: Basic song structure (melody, chords, etc.)
            instrumentation: Arrangement size (minimal, standard, full, orchestral)
            
        Returns:
            Complete arrangement with all parts
        """
        # Get genre-appropriate instruments
        genre_data = self.genre_manager.get_genre_data(genre)
        instruments = self._select_instruments_for_arrangement(genre_data, instrumentation)
        
        # Create arrangement for each instrument
        arrangement = {
            "genre": genre,
            "instrumentation_level": instrumentation,
            "selected_instruments": instruments,
            "parts": {},
            "texture": self._determine_texture(genre, instrumentation),
            "dynamics": self._create_dynamic_plan(song_structure, genre)
        }
        
        # Generate part for each instrument
        for instrument in instruments:
            part = self._generate_instrument_part(instrument, song_structure, genre)
            arrangement["parts"][instrument] = part
        
        return arrangement
    
    def _adjust_progression_length(self, progression: Dict[str, Any], target_bars: int) -> Dict[str, Any]:
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
    
    def _generate_melody_from_progression(self, progression: Dict[str, Any], 
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
    
    def _analyze_melody_characteristics(self, melody: List[Dict[str, Any]], genre: str) -> Dict[str, Any]:
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
    
    def _generate_beat_pattern(self, rhythm_pattern: Dict[str, Any], tempo: int, 
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
    
    def _generate_bass_line_from_chords(self, chords: List[Dict[str, Any]], 
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
    
    def _get_passing_tone(self, note: str) -> str:
        """Get a passing tone between notes (simplified)."""
        # This is a simplified approach - could be enhanced with music21
        note_names = ["C", "D", "E", "F", "G", "A", "B"]
        if note in note_names:
            idx = note_names.index(note)
            return note_names[(idx + 1) % len(note_names)]
        return note
    
    def _analyze_bass_voice_leading(self, bass_line: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    
    def _select_instruments_for_arrangement(self, genre_data: Dict[str, Any], 
                                          instrumentation: str) -> List[str]:
        """Select instruments based on genre and arrangement level."""
        inst_data = genre_data.get("instrumentation", {})
        
        instruments = []
        
        # Always include essential instruments
        instruments.extend(inst_data.get("essential", ["piano"]))
        
        if instrumentation in ["standard", "full", "orchestral"]:
            instruments.extend(inst_data.get("typical", ["bass", "drums"]))
        
        if instrumentation in ["full", "orchestral"]:
            instruments.extend(inst_data.get("optional", ["guitar"]))
        
        return list(set(instruments))  # Remove duplicates
    
    def _determine_texture(self, genre: str, instrumentation: str) -> str:
        """Determine arrangement texture based on genre and instrumentation."""
        texture_map = {
            ("blues", "minimal"): "sparse",
            ("blues", "standard"): "medium", 
            ("rock", "standard"): "dense",
            ("jazz", "standard"): "complex",
            ("ambient", "standard"): "layered"
        }
        
        return texture_map.get((genre, instrumentation), "medium")
    
    def _create_dynamic_plan(self, song_structure: Dict[str, Any], genre: str) -> List[str]:
        """Create dynamic plan for the arrangement."""
        # Simplified dynamic planning
        sections = song_structure.get("sections", ["verse", "chorus", "verse", "chorus"])
        dynamics = []
        
        for section in sections:
            if section == "verse":
                dynamics.append("mp")  # mezzo-piano
            elif section == "chorus":
                dynamics.append("f")   # forte
            elif section == "bridge":
                dynamics.append("mf")  # mezzo-forte
            else:
                dynamics.append("mp")
        
        return dynamics
    
    def _generate_instrument_part(self, instrument: str, song_structure: Dict[str, Any], 
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
    
    def _determine_instrument_role(self, instrument: str, genre: str) -> str:
        """Determine the role of an instrument in a genre."""
        role_map = {
            "piano": "harmonic_support",
            "guitar": "harmonic_lead",
            "bass": "harmonic_foundation", 
            "drums": "rhythmic_foundation",
            "vocals": "melodic_lead"
        }
        return role_map.get(instrument, "supporting")
    
    def _determine_pattern_type(self, instrument: str, genre: str) -> str:
        """Determine playing pattern for instrument in genre."""
        if instrument == "piano":
            if genre in ["jazz", "blues"]:
                return "comping"
            elif genre in ["rock", "pop"]:
                return "chordal"
        elif instrument == "bass":
            if genre == "jazz":
                return "walking"
            else:
                return "root_based"
        
        return "standard"
    
    def _get_instrument_articulation(self, instrument: str, genre: str) -> str:
        """Get appropriate articulation for instrument in genre."""
        if genre == "jazz":
            return "swing"
        elif genre == "rock":
            return "staccato"
        elif genre == "blues":
            return "legato"
        else:
            return "normal"