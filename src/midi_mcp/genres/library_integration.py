"""Integration layer for external music libraries."""

from typing import Dict, List, Optional, Any, Tuple
import logging
from pathlib import Path
import threading

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Music21Integration:
    """Integration wrapper for music21 library."""
    
    def __init__(self):
        """Initialize music21 integration."""
        try:
            from music21 import corpus, chord, roman, key, scale, stream, analysis
            self.corpus = corpus
            self.chord = chord
            self.roman = roman
            self.key = key
            self.scale = scale
            self.stream = stream
            self.analysis = analysis
            self._available = True
            logger.debug("music21 integration initialized")
        except ImportError as e:
            logger.warning(f"music21 not available: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        """Check if music21 is available."""
        return self._available
    
    def get_chord_from_notes(self, notes: List[str]) -> Optional[Dict[str, Any]]:
        """Analyze a chord from note names."""
        if not self._available:
            return None
        
        try:
            c = self.chord.Chord(notes)
            return {
                'name': c.commonName,
                'root': str(c.root()),
                'quality': c.quality,
                'notes': [str(p) for p in c.pitches],
                'bass': str(c.bass()) if c.bass() != c.root() else None
            }
        except Exception as e:
            logger.warning(f"Error analyzing chord {notes}: {e}")
            return None
    
    def get_roman_numeral_chord(self, numeral: str, key_name: str) -> Optional[Dict[str, Any]]:
        """Get chord from Roman numeral in a key."""
        if not self._available:
            return None
        
        try:
            key_obj = self.key.Key(key_name)
            rn = self.roman.RomanNumeral(numeral, key_obj)
            return {
                'numeral': numeral,
                'key': key_name,
                'chord_name': f"{rn.root().name}{rn.quality}",
                'notes': [str(p) for p in rn.pitches],
                'root': str(rn.root()),
                'quality': rn.quality
            }
        except Exception as e:
            logger.warning(f"Error with Roman numeral {numeral} in {key_name}: {e}")
            return None
    
    def analyze_key_from_notes(self, midi_notes: List[int]) -> Optional[Dict[str, Any]]:
        """Analyze key from MIDI note numbers."""
        if not self._available:
            return None
        
        try:
            # Convert MIDI numbers to music21 notes
            s = self.stream.Stream()
            for midi_note in midi_notes:
                note = self.stream.Note(midi=midi_note)
                s.append(note)
            
            analyzed_key = s.analyze('key')
            return {
                'key': str(analyzed_key),
                'tonic': analyzed_key.tonic.name,
                'mode': analyzed_key.mode,
                'confidence': getattr(analyzed_key, 'confidence', None)
            }
        except Exception as e:
            logger.warning(f"Error analyzing key from {midi_notes}: {e}")
            return None
    
    def get_scale_notes(self, scale_name: str, key_name: str) -> Optional[List[str]]:
        """Get notes for a scale in a specific key."""
        if not self._available:
            return None
        
        try:
            # Handle different scale types
            if scale_name.lower() == 'major':
                s = self.scale.MajorScale(key_name)
            elif scale_name.lower() == 'minor':
                s = self.scale.MinorScale(key_name)
            elif scale_name.lower() == 'dorian':
                s = self.scale.DorianScale(key_name)
            elif scale_name.lower() == 'mixolydian':
                s = self.scale.MixolydianScale(key_name)
            else:
                # Default to major if unknown
                s = self.scale.MajorScale(key_name)
            
            return [str(p) for p in s.pitches]
        except Exception as e:
            logger.warning(f"Error getting {scale_name} scale in {key_name}: {e}")
            return None
    
    def search_corpus_by_genre(self, genre: str) -> List[str]:
        """Search music21 corpus for genre examples."""
        if not self._available:
            return []
        
        try:
            results = self.corpus.search(genre)
            return [str(result) for result in results[:10]]  # Limit to 10 results
        except Exception as e:
            logger.warning(f"Error searching corpus for {genre}: {e}")
            return []

    def calculate_interval_semitones(self, note1: str, note2: str) -> Optional[int]:
        """Calculate interval between two notes in semitones."""
        if not self._available:
            return None
        
        try:
            from music21 import pitch
            p1 = pitch.Pitch(note1)
            p2 = pitch.Pitch(note2)
            interval = p2.midi - p1.midi
            return abs(interval)
        except Exception as e:
            logger.warning(f"Error calculating interval between {note1} and {note2}: {e}")
            return None

    def is_large_leap(self, note1: str, note2: str, threshold_semitones: int = 7) -> bool:
        """Check if interval between notes is a large leap (default: larger than perfect fifth)."""
        interval = self.calculate_interval_semitones(note1, note2)
        return interval is not None and interval > threshold_semitones

    def get_passing_tone(self, from_note: str, to_note: str) -> Optional[str]:
        """Get a passing tone between two notes."""
        if not self._available:
            return None
        
        try:
            from music21 import pitch
            p1 = pitch.Pitch(from_note)
            p2 = pitch.Pitch(to_note)
            
            # Simple chromatic passing tone
            interval = p2.midi - p1.midi
            if abs(interval) > 2:  # Only if interval is larger than a whole tone
                passing_midi = p1.midi + (1 if interval > 0 else -1)
                passing_pitch = pitch.Pitch(midi=passing_midi)
                return str(passing_pitch)
            
            return None
        except Exception as e:
            logger.warning(f"Error getting passing tone between {from_note} and {to_note}: {e}")
            return None

class PrettyMidiIntegration:
    """Integration wrapper for pretty_midi library."""
    
    def __init__(self):
        """Initialize pretty_midi integration."""
        try:
            import pretty_midi
            self.pretty_midi = pretty_midi
            self._available = True
            logger.debug("pretty_midi integration initialized")
        except ImportError as e:
            logger.warning(f"pretty_midi not available: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        """Check if pretty_midi is available."""
        return self._available
    
    def analyze_midi_file(self, midi_data: bytes) -> Optional[Dict[str, Any]]:
        """Analyze a MIDI file for rhythm and timing characteristics."""
        if not self._available:
            return None
        
        try:
            # Create PrettyMIDI object from bytes
            import io
            midi = self.pretty_midi.PrettyMIDI(io.BytesIO(midi_data))
            
            analysis = {
                'duration': midi.get_end_time(),
                'tempo_changes': len(midi.tempo_changes),
                'time_signature_changes': len(midi.time_signature_changes),
                'instruments': []
            }
            
            # Analyze each instrument
            for instrument in midi.instruments:
                inst_analysis = {
                    'program': instrument.program,
                    'is_drum': instrument.is_drum,
                    'note_count': len(instrument.notes),
                    'pitch_range': self._get_pitch_range(instrument.notes) if instrument.notes else None
                }
                analysis['instruments'].append(inst_analysis)
            
            # Try to get tempo estimate
            try:
                analysis['estimated_tempo'] = midi.estimate_tempo()
            except:
                analysis['estimated_tempo'] = None
            
            # Get chroma features
            try:
                chroma = midi.get_chroma()
                analysis['chroma_shape'] = chroma.shape
                analysis['key_profile'] = self._estimate_key_from_chroma(chroma)
            except:
                analysis['chroma_shape'] = None
                analysis['key_profile'] = None
            
            return analysis
            
        except Exception as e:
            logger.warning(f"Error analyzing MIDI file: {e}")
            return None
    
    def _get_pitch_range(self, notes: List) -> Tuple[int, int]:
        """Get pitch range from notes."""
        if not notes:
            return (0, 0)
        pitches = [note.pitch for note in notes]
        return (min(pitches), max(pitches))
    
    def _estimate_key_from_chroma(self, chroma) -> Optional[str]:
        """Estimate key from chroma features (simplified)."""
        try:
            import numpy as np
            # Sum chroma across time
            chroma_sum = np.sum(chroma, axis=1)
            # Find most prominent note
            dominant_note = np.argmax(chroma_sum)
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            return note_names[dominant_note]
        except:
            return None

class MuspyIntegration:
    """Integration wrapper for muspy library."""
    
    def __init__(self):
        """Initialize muspy integration."""
        try:
            import muspy
            self.muspy = muspy
            self._available = True
            logger.debug("muspy integration initialized")
        except ImportError as e:
            logger.warning(f"muspy not available: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        """Check if muspy is available."""
        return self._available
    
    def create_music_object(self, resolution: int = 480) -> Optional[Any]:
        """Create a new muspy Music object."""
        if not self._available:
            return None
        
        try:
            return self.muspy.Music(resolution=resolution)
        except Exception as e:
            logger.warning(f"Error creating music object: {e}")
            return None
    
    def add_chord_to_music(self, music, chord_notes: List[int], start_time: int, 
                          duration: int, velocity: int = 80) -> bool:
        """Add a chord to a muspy Music object."""
        if not self._available or music is None:
            return False
        
        try:
            # Create or get first track
            if not music.tracks:
                track = self.muspy.Track(program=1, is_drum=False)
                music.tracks.append(track)
            else:
                track = music.tracks[0]
            
            # Add notes for the chord
            for pitch in chord_notes:
                note = self.muspy.Note(
                    time=start_time,
                    pitch=pitch,
                    duration=duration,
                    velocity=velocity
                )
                track.notes.append(note)
            
            return True
        except Exception as e:
            logger.warning(f"Error adding chord to music: {e}")
            return False

class LibraryIntegration:
    """Main integration class that combines all music libraries (Singleton)."""
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LibraryIntegration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize all library integrations (only once)."""
        if self._initialized:
            return
            
        with self._lock:
            if self._initialized:
                return
                
            self.music21 = Music21Integration()
            self.pretty_midi = PrettyMidiIntegration() 
            self.muspy = MuspyIntegration()
            
            # Log availability
            available = []
            if self.music21.is_available():
                available.append("music21")
            if self.pretty_midi.is_available():
                available.append("pretty_midi")
            if self.muspy.is_available():
                available.append("muspy")
            
            logger.info(f"Library integration initialized. Available: {', '.join(available)}")
            LibraryIntegration._initialized = True
    
    def get_available_libraries(self) -> Dict[str, bool]:
        """Get status of all integrated libraries."""
        return {
            'music21': self.music21.is_available(),
            'pretty_midi': self.pretty_midi.is_available(),
            'muspy': self.muspy.is_available()
        }
    
    def analyze_chord_progression(self, numerals: List[str], key: str) -> List[Dict[str, Any]]:
        """Analyze a chord progression using available libraries."""
        progression = []
        
        for numeral in numerals:
            chord_info = self.music21.get_roman_numeral_chord(numeral, key)
            if chord_info:
                progression.append(chord_info)
        
        return progression
    
    def get_genre_examples_from_corpus(self, genre: str) -> List[str]:
        """Get genre examples from music21 corpus."""
        return self.music21.search_corpus_by_genre(genre)


def get_library_integration() -> LibraryIntegration:
    """
    Get the singleton instance of LibraryIntegration.
    
    Returns:
        LibraryIntegration: The singleton instance
    """
    return LibraryIntegration()