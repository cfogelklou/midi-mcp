"""Chord construction, analysis, and manipulation functionality."""

import re
from typing import Dict, List, Optional, Tuple, Union
from ..models.theory_models import Chord, Note, Quality, ChordType
from .constants import (
    CHORD_PATTERNS, NOTE_NAMES, FLAT_NOTE_NAMES, 
    ENHARMONIC_EQUIVALENTS, INTERVAL_NAMES
)

class ChordManager:
    """Manages chord construction, analysis, and transformations."""
    
    def __init__(self):
        self.patterns = CHORD_PATTERNS
        self._voicing_strategies = {
            'close': self._close_voicing,
            'open': self._open_voicing,
            'drop2': self._drop2_voicing,
            'drop3': self._drop3_voicing
        }
    
    def build_chord(self, root_note: str, chord_type: str, inversion: int = 0, 
                   voicing: str = "close", octave: int = 4) -> Chord:
        """
        Build a chord with specified parameters.
        
        Args:
            root_note: Root note of chord (C, F#, Bb, etc.)
            chord_type: Chord quality from CHORD_PATTERNS
            inversion: Chord inversion (0=root position, 1=first, 2=second, etc.)
            voicing: Voicing style (close, open, drop2, drop3)
            octave: Starting octave for root note
            
        Returns:
            Chord object with all notes and metadata
        """
        if chord_type not in self.patterns:
            raise ValueError(f"Unknown chord type: {chord_type}. Available: {list(self.patterns.keys())}")
        
        # Normalize root note
        root_note = self._normalize_note_name(root_note)
        root_midi = self._note_to_midi(root_note, octave)
        root = Note.from_midi(root_midi, prefer_sharps='#' in root_note)
        
        # Get chord pattern (intervals from root)
        intervals = self.patterns[chord_type].copy()
        
        # Build basic chord notes
        chord_notes = []
        for interval in intervals:
            note_midi = root_midi + interval
            note = Note.from_midi(note_midi, prefer_sharps='#' in root_note)
            chord_notes.append(note)
        
        # Apply inversion
        if inversion > 0:
            for _ in range(min(inversion, len(chord_notes) - 1)):
                # Move bass note up an octave
                bass_note = chord_notes.pop(0)
                new_bass = Note.from_midi(bass_note.midi_note + 12)
                chord_notes.append(new_bass)
        
        # Apply voicing strategy
        if voicing in self._voicing_strategies:
            chord_notes = self._voicing_strategies[voicing](chord_notes, root_midi)
        
        # Determine chord quality and type
        quality = self._determine_chord_quality(chord_type)
        c_type = self._determine_chord_type(chord_type)
        
        # Generate chord symbol
        symbol = self._generate_chord_symbol(root_note, chord_type, inversion)
        
        return Chord(
            root=root,
            quality=quality,
            chord_type=c_type,
            notes=chord_notes,
            symbol=symbol,
            inversion=inversion,
            voicing=voicing
        )
    
    def analyze_chord(self, notes: List[int]) -> List[Dict[str, any]]:
        """
        Analyze a set of notes to identify possible chords.
        
        Args:
            notes: MIDI note numbers to analyze
            
        Returns:
            List of possible chord interpretations with confidence scores
        """
        if len(notes) < 3:
            return []  # Need at least 3 notes for a chord
        
        # Normalize to pitch classes and sort
        pitch_classes = sorted(list(set(note % 12 for note in notes)))
        
        chord_matches = []
        
        # Try each pitch class as a potential root
        for root_pc in pitch_classes:
            # Calculate intervals from this root
            intervals = []
            for pc in pitch_classes:
                interval = (pc - root_pc) % 12
                intervals.append(interval)
            intervals.sort()
            
            # Compare against known chord patterns
            for chord_name, pattern in self.patterns.items():
                # Normalize pattern to pitch classes
                pattern_pcs = sorted([i % 12 for i in pattern])
                
                # Calculate match quality
                common = len(set(intervals) & set(pattern_pcs))
                missing = len(set(pattern_pcs) - set(intervals))
                extra = len(set(intervals) - set(pattern_pcs))
                
                if common >= 3:  # Require at least 3 matching intervals
                    confidence = common / max(len(intervals), len(pattern_pcs))
                    confidence -= (missing + extra) * 0.1  # Penalty for missing/extra notes
                    confidence = max(0, min(1, confidence))
                    
                    if confidence > 0.5:
                        root_note = NOTE_NAMES[root_pc]
                        symbol = self._generate_chord_symbol(root_note, chord_name)
                        
                        chord_matches.append({
                            'root': root_note,
                            'chord_type': chord_name,
                            'symbol': symbol,
                            'confidence': confidence,
                            'intervals': intervals,
                            'matching_intervals': common,
                            'missing_intervals': missing,
                            'extra_intervals': extra
                        })
        
        # Sort by confidence and return best matches
        chord_matches.sort(key=lambda x: x['confidence'], reverse=True)
        return chord_matches[:3]  # Return top 3 matches
    
    def get_chord_tones_and_extensions(self, chord_symbol: str) -> Dict[str, any]:
        """
        Break down a chord symbol into component tones.
        
        Args:
            chord_symbol: Chord symbol (Cmaj7, F#dim, Bb7sus4, etc.)
            
        Returns:
            Dictionary with root, chord tones, extensions, and avoid notes
        """
        parsed = self._parse_chord_symbol(chord_symbol)
        if not parsed:
            return {}
        
        root, chord_type = parsed['root'], parsed['chord_type']
        
        if chord_type not in self.patterns:
            return {}
        
        # Get base intervals
        intervals = self.patterns[chord_type]
        root_midi = self._note_to_midi(root, 4)
        
        # Separate chord tones from extensions
        chord_tones = []
        extensions = []
        
        for i, interval in enumerate(intervals):
            note_midi = root_midi + interval
            note = Note.from_midi(note_midi)
            
            # Determine if it's a chord tone or extension
            if interval <= 12:  # Within an octave = chord tone
                chord_tones.append(note)
            else:  # Extension
                extensions.append(note)
        
        # Identify avoid notes (context-dependent)
        avoid_notes = self._get_avoid_notes(chord_type, root_midi)
        
        return {
            'root': Note.from_midi(root_midi),
            'chord_tones': chord_tones,
            'extensions': extensions,
            'available_tensions': self._get_available_tensions(chord_type),
            'avoid_notes': avoid_notes,
            'chord_type': chord_type
        }
    
    def generate_chord_voicing(self, chord: Chord, target_range: Tuple[int, int],
                             voice_count: int = 4) -> List[Note]:
        """
        Generate a specific voicing for a chord within a range.
        
        Args:
            chord: Base chord to voice
            target_range: (min_midi, max_midi) range for voicing
            voice_count: Number of voices to use
            
        Returns:
            List of notes representing the voicing
        """
        min_midi, max_midi = target_range
        
        # Get available chord tones and extensions
        available_notes = []
        
        # Add chord tones in various octaves
        for note in chord.notes:
            current_midi = note.midi_note
            # Add notes in range
            while current_midi >= min_midi:
                if current_midi <= max_midi:
                    available_notes.append(Note.from_midi(current_midi))
                current_midi -= 12
            
            current_midi = note.midi_note + 12
            while current_midi <= max_midi:
                if current_midi >= min_midi:
                    available_notes.append(Note.from_midi(current_midi))
                current_midi += 12
        
        # Sort by MIDI number
        available_notes.sort(key=lambda n: n.midi_note)
        
        # Select best voicing (this is simplified - could be more sophisticated)
        if len(available_notes) <= voice_count:
            return available_notes
        
        # Try to include essential tones (root, 3rd, 7th if present)
        essential_intervals = [0, 3, 4, 10, 11]  # Root, m3, M3, m7, M7
        voicing = []
        
        for note in available_notes:
            interval = (note.midi_note - chord.root.midi_note) % 12
            if interval in essential_intervals and len(voicing) < voice_count:
                voicing.append(note)
        
        # Fill remaining voices
        for note in available_notes:
            if note not in voicing and len(voicing) < voice_count:
                voicing.append(note)
        
        return sorted(voicing[:voice_count], key=lambda n: n.midi_note)
    
    def suggest_chord_substitutions(self, chord: Chord, context: str = "jazz") -> List[Dict[str, any]]:
        """
        Suggest chord substitutions for the given chord.
        
        Args:
            chord: Original chord
            context: Musical context (jazz, classical, pop)
            
        Returns:
            List of substitution suggestions with explanations
        """
        substitutions = []
        root_pc = chord.root.midi_note % 12
        
        if context == "jazz":
            # Common jazz substitutions
            if chord.chord_type == ChordType.SEVENTH:
                # Tritone substitution (for dominant chords)
                if chord.symbol.endswith('7') and not 'maj' in chord.symbol.lower():
                    sub_root_pc = (root_pc + 6) % 12
                    sub_root = NOTE_NAMES[sub_root_pc]
                    substitutions.append({
                        'original': chord.symbol,
                        'substitution': f"{sub_root}7",
                        'type': 'tritone_substitution',
                        'explanation': 'Dominant chord a tritone away shares important guide tones'
                    })
                
                # Relative ii-V substitution
                if 'maj7' in chord.symbol:
                    # Major 7 can be replaced by ii-V of relative
                    ii_root_pc = (root_pc + 2) % 12
                    v_root_pc = (root_pc + 9) % 12
                    substitutions.append({
                        'original': chord.symbol,
                        'substitution': f"{NOTE_NAMES[ii_root_pc]}m7 - {NOTE_NAMES[v_root_pc]}7",
                        'type': 'ii_V_substitution',
                        'explanation': 'Replace static chord with ii-V motion to create more movement'
                    })
        
        elif context == "pop":
            # Pop substitutions tend to be simpler
            if 'maj7' in chord.symbol:
                # maj7 can be replaced with add9
                substitutions.append({
                    'original': chord.symbol,
                    'substitution': chord.symbol.replace('maj7', 'add9'),
                    'type': 'color_substitution',
                    'explanation': 'Add9 chord has similar color but less tension'
                })
        
        return substitutions
    
    def _close_voicing(self, notes: List[Note], root_midi: int) -> List[Note]:
        """Apply close voicing (notes as close together as possible)."""
        return notes  # Already in close position from basic construction
    
    def _open_voicing(self, notes: List[Note], root_midi: int) -> List[Note]:
        """Apply open voicing (spread notes over wider range)."""
        if len(notes) < 4:
            return notes
        
        # Move middle voices up an octave
        result = [notes[0]]  # Keep bass
        for i in range(1, len(notes) - 1):
            new_note = Note.from_midi(notes[i].midi_note + 12)
            result.append(new_note)
        result.append(notes[-1])  # Keep top voice
        
        return result
    
    def _drop2_voicing(self, notes: List[Note], root_midi: int) -> List[Note]:
        """Apply drop-2 voicing (drop second-highest voice an octave)."""
        if len(notes) < 4:
            return notes
        
        result = notes.copy()
        # Drop second-from-top voice down an octave
        drop_note = result[-2]
        result[-2] = Note.from_midi(drop_note.midi_note - 12)
        
        # Re-sort to maintain bass-to-treble order
        return sorted(result, key=lambda n: n.midi_note)
    
    def _drop3_voicing(self, notes: List[Note], root_midi: int) -> List[Note]:
        """Apply drop-3 voicing (drop third-highest voice an octave)."""
        if len(notes) < 4:
            return notes
        
        result = notes.copy()
        # Drop third-from-top voice down an octave
        if len(result) >= 3:
            drop_note = result[-3]
            result[-3] = Note.from_midi(drop_note.midi_note - 12)
        
        # Re-sort to maintain bass-to-treble order
        return sorted(result, key=lambda n: n.midi_note)
    
    def _normalize_note_name(self, note: str) -> str:
        """Normalize note name to standard format."""
        return note.strip().capitalize().replace('B', 'b')
    
    def _note_to_midi(self, note_name: str, octave: int) -> int:
        """Convert note name and octave to MIDI number."""
        note_name = self._normalize_note_name(note_name)
        
        if note_name in NOTE_NAMES:
            note_index = NOTE_NAMES.index(note_name)
        elif note_name in FLAT_NOTE_NAMES:
            note_index = FLAT_NOTE_NAMES.index(note_name)
        else:
            raise ValueError(f"Unknown note name: {note_name}")
        
        return (octave + 1) * 12 + note_index
    
    def _determine_chord_quality(self, chord_type: str) -> Quality:
        """Determine chord quality from chord type string."""
        chord_type_lower = chord_type.lower()
        
        if 'maj' in chord_type_lower or chord_type == 'major':
            return Quality.MAJOR
        elif 'min' in chord_type_lower or chord_type == 'minor':
            return Quality.MINOR
        elif 'dim' in chord_type_lower:
            return Quality.DIMINISHED
        elif 'aug' in chord_type_lower:
            return Quality.AUGMENTED
        elif '7' in chord_type and 'maj' not in chord_type_lower:
            return Quality.DOMINANT
        else:
            return Quality.MAJOR  # Default
    
    def _determine_chord_type(self, chord_type: str) -> ChordType:
        """Determine chord type from chord type string."""
        if any(ext in chord_type for ext in ['13']):
            return ChordType.THIRTEENTH
        elif any(ext in chord_type for ext in ['11']):
            return ChordType.ELEVENTH
        elif any(ext in chord_type for ext in ['9', 'add9']):
            return ChordType.NINTH
        elif any(ext in chord_type for ext in ['7']):
            return ChordType.SEVENTH
        else:
            return ChordType.TRIAD
    
    def _generate_chord_symbol(self, root: str, chord_type: str, inversion: int = 0) -> str:
        """Generate standard chord symbol."""
        symbol = root
        
        # Add quality/extension indicators
        if chord_type == 'minor':
            symbol += 'm'
        elif chord_type == 'diminished':
            symbol += 'dim'
        elif chord_type == 'augmented':
            symbol += 'aug'
        elif chord_type == 'maj7':
            symbol += 'maj7'
        elif chord_type == '7':
            symbol += '7'
        elif chord_type == 'min7':
            symbol += 'm7'
        elif chord_type == 'sus2':
            symbol += 'sus2'
        elif chord_type == 'sus4':
            symbol += 'sus4'
        # Add more mappings as needed
        
        # Add inversion notation if not root position
        if inversion > 0:
            inversion_names = ['', '/3', '/5', '/7', '/9']  # Simplified
            if inversion < len(inversion_names):
                symbol += inversion_names[inversion]
        
        return symbol
    
    def _parse_chord_symbol(self, symbol: str) -> Optional[Dict[str, str]]:
        """Parse chord symbol into components."""
        # This is a simplified parser - could be much more sophisticated
        pattern = r'^([A-G][#b]?)(.*)$'
        match = re.match(pattern, symbol)
        
        if not match:
            return None
        
        root = match.group(1)
        extensions = match.group(2)
        
        # Map extensions to chord types (simplified)
        if extensions == 'm':
            chord_type = 'minor'
        elif extensions == 'maj7':
            chord_type = 'maj7'
        elif extensions == '7':
            chord_type = '7'
        elif extensions == 'm7':
            chord_type = 'min7'
        else:
            chord_type = 'major'  # Default
        
        return {'root': root, 'chord_type': chord_type, 'extensions': extensions}
    
    def _get_available_tensions(self, chord_type: str) -> List[str]:
        """Get available tension notes for chord type."""
        tensions = {
            'maj7': ['9', '11', '13'],
            'min7': ['9', '11'],
            '7': ['9', '11', '13', 'b9', '#9', '#11', 'b13'],
            'dim7': ['9', '11'],
            'half_dim7': ['9', '11', 'b13']
        }
        return tensions.get(chord_type, [])
    
    def _get_avoid_notes(self, chord_type: str, root_midi: int) -> List[Note]:
        """Get avoid notes for the chord type."""
        # Simplified - in practice this is context-dependent
        avoid_intervals = {
            'maj7': [11],  # Avoid 11 in major chords (unless #11)
            'min7': [],    # Minor chords have fewer avoid notes
            '7': [11],     # Avoid natural 11 in dominant
        }
        
        intervals = avoid_intervals.get(chord_type, [])
        avoid_notes = []
        
        for interval in intervals:
            note_midi = root_midi + interval
            avoid_notes.append(Note.from_midi(note_midi))
        
        return avoid_notes