"""Key analysis, detection, and modulation functionality."""

from typing import Dict, List, Optional, Tuple, Union
import statistics
from collections import Counter
from ..models.theory_models import KeyAnalysis, Note
from .constants import (
    KEY_SIGNATURES, CIRCLE_OF_FIFTHS, NOTE_NAMES, FLAT_NOTE_NAMES,
    MAJOR_KEY_FUNCTIONS, MINOR_KEY_FUNCTIONS
)

class KeyManager:
    """Manages key analysis, detection, and modulation tools."""
    
    def __init__(self):
        self.key_signatures = KEY_SIGNATURES
        self.circle_of_fifths = CIRCLE_OF_FIFTHS
        
        # Major and minor scale templates (pitch class sets)
        self.major_template = {0, 2, 4, 5, 7, 9, 11}  # C major
        self.minor_template = {0, 2, 3, 5, 7, 8, 10}  # C minor (natural)
        
        # Key profiles for key detection (Krumhansl-Schmuckler)
        self.major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 
                             5.19, 2.39, 3.66, 2.29, 2.88]
        self.minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54,
                             4.75, 3.98, 2.69, 3.34, 3.17]
    
    def detect_key(self, midi_notes: List[int], 
                   timestamps: Optional[List[float]] = None) -> KeyAnalysis:
        """
        Detect the key(s) of a sequence of MIDI notes.
        
        Args:
            midi_notes: List of MIDI note numbers
            timestamps: Optional timestamps for temporal analysis
            
        Returns:
            KeyAnalysis with most likely key and alternatives
        """
        if not midi_notes:
            return KeyAnalysis(
                most_likely_key='C',
                confidence=0.0,
                alternative_keys=[],
                key_changes=[]
            )
        
        # Convert to pitch classes and count occurrences
        pitch_classes = [note % 12 for note in midi_notes]
        pc_counts = Counter(pitch_classes)
        
        # Create pitch class distribution
        total_notes = len(pitch_classes)
        pc_distribution = [pc_counts.get(i, 0) / total_notes for i in range(12)]
        
        # Calculate key scores using key profiles
        key_scores = []
        
        # Test all major keys
        for i in range(12):
            # Rotate profile to test different keys
            rotated_major = self.major_profile[i:] + self.major_profile[:i]
            score = self._correlation(pc_distribution, rotated_major)
            key_name = NOTE_NAMES[i]
            key_scores.append((key_name, 'major', score))
        
        # Test all minor keys  
        for i in range(12):
            # Rotate profile to test different keys
            rotated_minor = self.minor_profile[i:] + self.minor_profile[:i]
            score = self._correlation(pc_distribution, rotated_minor)
            key_name = NOTE_NAMES[i] + 'm'
            key_scores.append((key_name, 'minor', score))
        
        # Sort by score (highest first)
        key_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Get top result and alternatives
        best_key = key_scores[0][0]
        best_confidence = key_scores[0][2]
        
        # Normalize confidence to 0-1 range
        confidence = max(0, min(1, (best_confidence + 1) / 2))
        
        alternatives = []
        for key_name, mode, score in key_scores[1:6]:  # Top 5 alternatives
            alt_confidence = max(0, min(1, (score + 1) / 2))
            alternatives.append((key_name, alt_confidence))
        
        # Detect key changes if timestamps provided
        key_changes = []
        if timestamps and len(timestamps) == len(midi_notes):
            key_changes = self._detect_key_changes(midi_notes, timestamps)
        
        return KeyAnalysis(
            most_likely_key=best_key,
            confidence=confidence,
            alternative_keys=alternatives,
            key_changes=key_changes
        )
    
    def analyze_modulations(self, midi_notes: List[int], 
                           timestamps: List[float]) -> List[Dict[str, any]]:
        """
        Identify key changes and modulations in a sequence.
        
        Args:
            midi_notes: List of MIDI note numbers
            timestamps: Timestamps for each note
            
        Returns:
            List of modulation points with analysis
        """
        if len(midi_notes) != len(timestamps):
            return []
        
        modulations = []
        window_size = 20  # Analyze in chunks of 20 notes
        overlap = 10      # 50% overlap
        
        current_key = None
        
        for i in range(0, len(midi_notes) - window_size, overlap):
            # Get window of notes
            window_notes = midi_notes[i:i + window_size]
            window_start_time = timestamps[i]
            window_end_time = timestamps[min(i + window_size - 1, len(timestamps) - 1)]
            
            # Detect key in this window
            window_analysis = self.detect_key(window_notes)
            window_key = window_analysis.most_likely_key
            
            # Check if key changed
            if current_key is None:
                current_key = window_key
            elif window_key != current_key and window_analysis.confidence > 0.7:
                # Significant key change detected
                modulation_type = self._classify_modulation(current_key, window_key)
                
                modulations.append({
                    'timestamp': window_start_time,
                    'from_key': current_key,
                    'to_key': window_key,
                    'confidence': window_analysis.confidence,
                    'type': modulation_type,
                    'pivot_analysis': self._analyze_pivot_area(
                        midi_notes[max(0, i-10):i+10], current_key, window_key
                    )
                })
                
                current_key = window_key
        
        return modulations
    
    def suggest_modulation(self, from_key: str, to_key: str) -> Dict[str, any]:
        """
        Suggest ways to modulate between two keys.
        
        Args:
            from_key: Starting key (C, Am, F#, etc.)
            to_key: Target key
            
        Returns:
            Dictionary with modulation strategies and pivot chords
        """
        from_root = from_key.replace('m', '')
        to_root = to_key.replace('m', '')
        from_minor = 'm' in from_key
        to_minor = 'm' in to_key
        
        # Calculate interval between keys
        from_pc = NOTE_NAMES.index(from_root)
        to_pc = NOTE_NAMES.index(to_root)
        interval = (to_pc - from_pc) % 12
        
        # Classify modulation relationship
        relationship = self._classify_key_relationship(from_key, to_key)
        
        suggestions = {
            'relationship': relationship,
            'interval': interval,
            'difficulty': self._assess_modulation_difficulty(from_key, to_key),
            'strategies': [],
            'pivot_chords': [],
            'common_tones': self._find_common_tones(from_key, to_key)
        }
        
        # Generate specific strategies based on relationship
        if relationship == 'closely_related':
            # Use pivot chords
            pivot_chords = self._find_pivot_chords(from_key, to_key)
            suggestions['pivot_chords'] = pivot_chords
            suggestions['strategies'].append({
                'type': 'pivot_chord',
                'description': f"Use pivot chord(s): {', '.join(pivot_chords)}",
                'difficulty': 'easy'
            })
        
        elif relationship == 'distant':
            # Suggest intermediate modulations
            intermediate_keys = self._find_intermediate_keys(from_key, to_key)
            suggestions['strategies'].append({
                'type': 'intermediate_modulation',
                'description': f"Modulate via intermediate key(s): {', '.join(intermediate_keys)}",
                'difficulty': 'moderate'
            })
            
            # Suggest chromatic mediant
            if self._is_chromatic_mediant(from_key, to_key):
                suggestions['strategies'].append({
                    'type': 'chromatic_mediant',
                    'description': "Direct chromatic mediant relationship - use common tone",
                    'difficulty': 'moderate'
                })
        
        # Always suggest secondary dominants
        secondary_dom = self._suggest_secondary_dominant(to_key)
        if secondary_dom:
            suggestions['strategies'].append({
                'type': 'secondary_dominant',
                'description': f"Use secondary dominant {secondary_dom} to establish {to_key}",
                'difficulty': 'easy'
            })
        
        return suggestions
    
    def get_key_signature_info(self, key: str) -> Dict[str, any]:
        """
        Get information about a key signature.
        
        Args:
            key: Key name (C, G, Am, F#m, etc.)
            
        Returns:
            Key signature information
        """
        root = key.replace('m', '')
        is_minor = 'm' in key
        
        if root not in self.key_signatures:
            return {}
        
        accidentals = self.key_signatures[root]
        
        # Generate scale notes
        scale_notes = self._generate_scale_notes(root, is_minor)
        
        # Determine sharp/flat preference
        uses_sharps = accidentals > 0
        uses_flats = accidentals < 0
        
        return {
            'key': key,
            'root': root,
            'is_minor': is_minor,
            'accidentals': abs(accidentals),
            'uses_sharps': uses_sharps,
            'uses_flats': uses_flats,
            'scale_notes': scale_notes,
            'relative_key': self._get_relative_key(key),
            'parallel_key': self._get_parallel_key(key),
            'circle_position': self._get_circle_position(root)
        }
    
    def find_closely_related_keys(self, key: str) -> List[str]:
        """
        Find keys closely related to the given key.
        
        Args:
            key: Reference key
            
        Returns:
            List of closely related keys
        """
        root = key.replace('m', '')
        is_minor = 'm' in key
        
        related = []
        
        # Add relative major/minor
        relative = self._get_relative_key(key)
        related.append(relative)
        
        # Add parallel major/minor
        parallel = self._get_parallel_key(key)
        related.append(parallel)
        
        # Add keys one position away in circle of fifths
        circle_pos = self._get_circle_position(root)
        
        # Key a fifth up
        up_fifth_pos = (circle_pos + 1) % len(self.circle_of_fifths)
        up_fifth_root = self.circle_of_fifths[up_fifth_pos]
        related.extend([up_fifth_root, up_fifth_root + 'm'])
        
        # Key a fifth down  
        down_fifth_pos = (circle_pos - 1) % len(self.circle_of_fifths)
        down_fifth_root = self.circle_of_fifths[down_fifth_pos]
        related.extend([down_fifth_root, down_fifth_root + 'm'])
        
        # Remove duplicates and the original key
        related = list(set(related))
        if key in related:
            related.remove(key)
        
        return related
    
    def _correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y):
            return 0
        
        n = len(x)
        if n < 2:
            return 0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        denominator = (sum_sq_x * sum_sq_y) ** 0.5
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    def _detect_key_changes(self, midi_notes: List[int], 
                           timestamps: List[float]) -> List[Tuple[float, str, float]]:
        """Detect key changes over time."""
        changes = []
        window_size = 15
        step_size = 5
        
        current_key = None
        
        for i in range(0, len(midi_notes) - window_size, step_size):
            window = midi_notes[i:i + window_size]
            window_time = timestamps[i + window_size // 2]  # Middle of window
            
            analysis = self.detect_key(window)
            
            if (current_key is None or 
                (analysis.most_likely_key != current_key and analysis.confidence > 0.75)):
                
                changes.append((
                    window_time,
                    analysis.most_likely_key,
                    analysis.confidence
                ))
                current_key = analysis.most_likely_key
        
        return changes
    
    def _classify_modulation(self, from_key: str, to_key: str) -> str:
        """Classify the type of modulation."""
        relationship = self._classify_key_relationship(from_key, to_key)
        
        if relationship == 'closely_related':
            if self._is_relative_keys(from_key, to_key):
                return 'relative'
            elif self._is_parallel_keys(from_key, to_key):
                return 'parallel'
            else:
                return 'closely_related'
        elif relationship == 'distant':
            if self._is_chromatic_mediant(from_key, to_key):
                return 'chromatic_mediant'
            else:
                return 'distant'
        else:
            return 'enharmonic'
    
    def _analyze_pivot_area(self, notes: List[int], from_key: str, to_key: str) -> Dict[str, any]:
        """Analyze the pivot area between keys."""
        # This is a simplified analysis - could be much more sophisticated
        pivot_chords = self._find_pivot_chords(from_key, to_key)
        
        return {
            'pivot_chords': pivot_chords,
            'pivot_notes': self._find_common_tones(from_key, to_key),
            'transition_length': len(notes)
        }
    
    def _classify_key_relationship(self, key1: str, key2: str) -> str:
        """Classify relationship between two keys."""
        root1 = key1.replace('m', '')
        root2 = key2.replace('m', '')
        
        # Same root = closely related
        if root1 == root2:
            return 'closely_related'
        
        # Check circle of fifths distance
        try:
            pos1 = self.circle_of_fifths.index(root1)
            pos2 = self.circle_of_fifths.index(root2)
            distance = min(abs(pos1 - pos2), 12 - abs(pos1 - pos2))
            
            if distance <= 1:
                return 'closely_related'
            elif distance <= 3:
                return 'moderately_related'
            else:
                return 'distant'
        except ValueError:
            return 'distant'
    
    def _assess_modulation_difficulty(self, from_key: str, to_key: str) -> str:
        """Assess difficulty of modulating between keys."""
        relationship = self._classify_key_relationship(from_key, to_key)
        
        if relationship == 'closely_related':
            return 'easy'
        elif relationship == 'moderately_related':
            return 'moderate'
        else:
            return 'difficult'
    
    def _find_pivot_chords(self, from_key: str, to_key: str) -> List[str]:
        """Find chords that exist in both keys."""
        # Simplified - generate triads for each key and find common ones
        from_chords = self._generate_diatonic_chords(from_key)
        to_chords = self._generate_diatonic_chords(to_key)
        
        # Find common chord symbols
        common = []
        for chord1 in from_chords:
            for chord2 in to_chords:
                if self._chords_equivalent(chord1, chord2):
                    common.append(chord1)
                    break
        
        return list(set(common))  # Remove duplicates
    
    def _find_common_tones(self, key1: str, key2: str) -> List[str]:
        """Find notes common to both keys."""
        notes1 = set(self._generate_scale_notes(key1.replace('m', ''), 'm' in key1))
        notes2 = set(self._generate_scale_notes(key2.replace('m', ''), 'm' in key2))
        
        return sorted(list(notes1 & notes2))
    
    def _find_intermediate_keys(self, from_key: str, to_key: str) -> List[str]:
        """Find intermediate keys for distant modulations."""
        # Find keys on the path in circle of fifths
        from_root = from_key.replace('m', '')
        to_root = to_key.replace('m', '')
        
        try:
            from_pos = self.circle_of_fifths.index(from_root)
            to_pos = self.circle_of_fifths.index(to_root)
            
            # Choose shorter path around circle
            if abs(to_pos - from_pos) <= 6:
                # Go direct direction
                if to_pos > from_pos:
                    positions = list(range(from_pos + 1, to_pos))
                else:
                    positions = list(range(from_pos - 1, to_pos, -1))
            else:
                # Go the other way around
                if to_pos > from_pos:
                    positions = list(range(from_pos - 1, -1, -1)) + list(range(11, to_pos, -1))
                else:
                    positions = list(range(from_pos + 1, 12)) + list(range(0, to_pos))
            
            # Take middle key(s) as intermediate
            if len(positions) > 0:
                mid_pos = positions[len(positions) // 2]
                return [self.circle_of_fifths[mid_pos]]
        except ValueError:
            pass
        
        return []
    
    def _is_chromatic_mediant(self, key1: str, key2: str) -> bool:
        """Check if keys have chromatic mediant relationship."""
        root1 = key1.replace('m', '')
        root2 = key2.replace('m', '')
        
        pc1 = NOTE_NAMES.index(root1)
        pc2 = NOTE_NAMES.index(root2)
        
        interval = abs(pc2 - pc1)
        # Chromatic mediants are at intervals of 3 or 4 semitones
        return interval in [3, 4, 8, 9]
    
    def _suggest_secondary_dominant(self, target_key: str) -> Optional[str]:
        """Suggest secondary dominant for target key."""
        root = target_key.replace('m', '')
        root_pc = NOTE_NAMES.index(root)
        
        # Dominant is a fifth above
        dom_pc = (root_pc + 7) % 12
        dom_root = NOTE_NAMES[dom_pc]
        
        return f"{dom_root}7"
    
    def _generate_scale_notes(self, root: str, is_minor: bool) -> List[str]:
        """Generate scale notes for a key."""
        root_pc = NOTE_NAMES.index(root)
        
        if is_minor:
            intervals = [0, 2, 3, 5, 7, 8, 10]  # Natural minor
        else:
            intervals = [0, 2, 4, 5, 7, 9, 11]  # Major
        
        notes = []
        for interval in intervals:
            note_pc = (root_pc + interval) % 12
            notes.append(NOTE_NAMES[note_pc])
        
        return notes
    
    def _get_relative_key(self, key: str) -> str:
        """Get the relative major/minor key."""
        root = key.replace('m', '')
        is_minor = 'm' in key
        
        if is_minor:
            # Relative major is a minor third up
            root_pc = NOTE_NAMES.index(root)
            major_pc = (root_pc + 3) % 12
            return NOTE_NAMES[major_pc]
        else:
            # Relative minor is a minor third down
            root_pc = NOTE_NAMES.index(root)
            minor_pc = (root_pc - 3) % 12
            return NOTE_NAMES[minor_pc] + 'm'
    
    def _get_parallel_key(self, key: str) -> str:
        """Get the parallel major/minor key."""
        root = key.replace('m', '')
        is_minor = 'm' in key
        
        return root + ('' if is_minor else 'm')
    
    def _get_circle_position(self, root: str) -> int:
        """Get position in circle of fifths."""
        try:
            return self.circle_of_fifths.index(root)
        except ValueError:
            return 0
    
    def _generate_diatonic_chords(self, key: str) -> List[str]:
        """Generate diatonic triads for a key."""
        root = key.replace('m', '')
        is_minor = 'm' in key
        
        scale_notes = self._generate_scale_notes(root, is_minor)
        chords = []
        
        # Build triad on each scale degree
        for i in range(7):
            chord_root = scale_notes[i]
            third = scale_notes[(i + 2) % 7]
            fifth = scale_notes[(i + 4) % 7]
            
            # Determine chord quality from intervals
            root_pc = NOTE_NAMES.index(chord_root)
            third_pc = NOTE_NAMES.index(third)
            
            third_interval = (third_pc - root_pc) % 12
            
            if third_interval == 3:  # Minor third
                chords.append(chord_root + 'm')
            else:  # Major third
                chords.append(chord_root)
        
        return chords
    
    def _chords_equivalent(self, chord1: str, chord2: str) -> bool:
        """Check if two chord symbols represent the same chord."""
        # Simplified comparison
        return chord1 == chord2
    
    def _is_relative_keys(self, key1: str, key2: str) -> bool:
        """Check if keys are relative major/minor."""
        return self._get_relative_key(key1) == key2
    
    def _is_parallel_keys(self, key1: str, key2: str) -> bool:
        """Check if keys are parallel major/minor."""
        return self._get_parallel_key(key1) == key2