"""Chord progression generation, analysis, and manipulation functionality."""

from typing import Dict, List, Optional, Tuple, Union
from ..models.theory_models import Chord, ChordProgression, Note
from .constants import (
    COMMON_PROGRESSIONS, MAJOR_KEY_FUNCTIONS, MINOR_KEY_FUNCTIONS, 
    HARMONIC_MINOR_FUNCTIONS, NOTE_NAMES, CIRCLE_OF_FIFTHS
)
from .chords import ChordManager

class ProgressionManager:
    """Manages chord progression creation, analysis, and transformations."""
    
    def __init__(self):
        self.chord_manager = ChordManager()
        self.common_progressions = COMMON_PROGRESSIONS
        
    def create_chord_progression(self, key: str, progression: List[str], 
                               duration_per_chord: float = 1.0,
                               voicing: str = "close") -> ChordProgression:
        """
        Create a chord progression in a specific key.
        
        Args:
            key: Key signature (C, Am, F#, Bbm, etc.)
            progression: Roman numeral progression (["I", "vi", "ii", "V"])
            duration_per_chord: Duration of each chord in beats
            voicing: Voicing style for all chords
            
        Returns:
            ChordProgression object with MIDI data
        """
        is_minor = 'm' in key.lower()
        root_key = key.replace('m', '').replace('M', '')
        
        # Get appropriate function map
        if is_minor:
            if self._uses_harmonic_minor(progression):
                functions = HARMONIC_MINOR_FUNCTIONS
            else:
                functions = MINOR_KEY_FUNCTIONS
        else:
            functions = MAJOR_KEY_FUNCTIONS
        
        chords = []
        durations = []
        
        for roman_numeral in progression:
            # Parse roman numeral to get degree and quality
            degree, chord_quality = self._parse_roman_numeral(roman_numeral)
            
            # Calculate root note of chord
            chord_root = self._get_chord_root(root_key, degree, is_minor)
            
            # Determine chord type from roman numeral
            chord_type = self._determine_chord_type_from_roman(roman_numeral, is_minor)
            
            # Build the chord
            try:
                chord = self.chord_manager.build_chord(
                    root_note=chord_root,
                    chord_type=chord_type,
                    voicing=voicing,
                    octave=4
                )
                chords.append(chord)
                durations.append(duration_per_chord)
            except ValueError as e:
                # Fallback to major triad if chord type not recognized
                chord = self.chord_manager.build_chord(
                    root_note=chord_root,
                    chord_type='major',
                    voicing=voicing,
                    octave=4
                )
                chords.append(chord)
                durations.append(duration_per_chord)
        
        return ChordProgression(
            chords=chords,
            key=key,
            roman_numerals=progression,
            durations=durations
        )
    
    def analyze_progression(self, chord_symbols: List[str], key: str = None) -> Dict[str, any]:
        """
        Analyze the harmonic function of a chord progression.
        
        Args:
            chord_symbols: List of chord symbols (["C", "Am", "F", "G"])
            key: Key context (auto-detected if None)
            
        Returns:
            Analysis including roman numerals, key relationships, voice leading quality
        """
        if key is None:
            key = self._detect_key_from_progression(chord_symbols)
        
        is_minor = 'm' in key.lower()
        root_key = key.replace('m', '').replace('M', '')
        
        analysis = {
            'detected_key': key,
            'roman_numerals': [],
            'harmonic_functions': [],
            'cadences': [],
            'secondary_dominants': [],
            'modulations': []
        }
        
        # Analyze each chord
        for i, symbol in enumerate(chord_symbols):
            # Parse chord symbol to get root and quality
            chord_info = self._parse_chord_symbol(symbol)
            if not chord_info:
                continue
            
            chord_root = chord_info['root']
            chord_quality = chord_info['quality']
            
            # Calculate scale degree
            degree = self._calculate_degree(root_key, chord_root)
            
            # Determine roman numeral
            roman = self._generate_roman_numeral(degree, chord_quality, is_minor)
            analysis['roman_numerals'].append(roman)
            
            # Identify harmonic function
            function = self._identify_harmonic_function(degree, chord_quality, is_minor)
            analysis['harmonic_functions'].append(function)
            
            # Look for cadences
            if i > 0:
                cadence = self._identify_cadence(
                    analysis['roman_numerals'][i-1], 
                    roman,
                    is_minor
                )
                if cadence:
                    analysis['cadences'].append({
                        'position': i,
                        'type': cadence,
                        'chords': [chord_symbols[i-1], symbol]
                    })
            
            # Check for secondary dominants
            if self._is_secondary_dominant(roman, is_minor):
                analysis['secondary_dominants'].append({
                    'position': i,
                    'chord': symbol,
                    'roman': roman,
                    'target': self._get_secondary_target(roman)
                })
        
        return analysis
    
    def suggest_next_chord(self, current_progression: List[str], key: str,
                          style: str = "common_practice") -> Dict[str, any]:
        """
        Suggest logical next chords for a progression.
        
        Args:
            current_progression: Existing chord progression (roman numerals)
            key: Key signature
            style: Harmonic style (common_practice, jazz, pop, modal)
            
        Returns:
            List of suggested chords with probability scores
        """
        if not current_progression:
            # If no progression yet, suggest common starting chords
            if style == "pop":
                suggestions = [
                    {'chord': 'vi', 'probability': 0.3, 'reason': 'Popular starting chord'},
                    {'chord': 'I', 'probability': 0.25, 'reason': 'Tonic start'},
                    {'chord': 'IV', 'probability': 0.2, 'reason': 'Subdominant start'}
                ]
            else:
                suggestions = [
                    {'chord': 'I', 'probability': 0.4, 'reason': 'Tonic start'},
                    {'chord': 'vi', 'probability': 0.2, 'reason': 'Relative minor'},
                    {'chord': 'ii', 'probability': 0.15, 'reason': 'Pre-dominant'}
                ]
            return {'suggestions': suggestions}
        
        last_chord = current_progression[-1]
        is_minor = 'm' in key.lower()
        
        # Get style-specific progression tendencies
        tendencies = self._get_progression_tendencies(style, is_minor)
        
        suggestions = []
        
        # Look up common continuations for the last chord
        if last_chord in tendencies:
            for next_chord, probability in tendencies[last_chord].items():
                reason = self._get_progression_reason(last_chord, next_chord, style)
                suggestions.append({
                    'chord': next_chord,
                    'probability': probability,
                    'reason': reason
                })
        
        # Add context-aware suggestions
        if len(current_progression) >= 2:
            # Look for common patterns
            last_two = current_progression[-2:]
            pattern_suggestions = self._suggest_from_pattern(last_two, style, is_minor)
            suggestions.extend(pattern_suggestions)
        
        # Sort by probability and return top suggestions
        suggestions.sort(key=lambda x: x['probability'], reverse=True)
        return {'suggestions': suggestions[:5]}
    
    def get_common_progressions(self, style: str = None) -> Dict[str, List[str]]:
        """
        Get library of common chord progressions.
        
        Args:
            style: Filter by style (classical, jazz, pop, blues)
            
        Returns:
            Dictionary of progression names and their chord sequences
        """
        if style and style in self.common_progressions:
            return {style: self.common_progressions[style]}
        
        return self.common_progressions
    
    def transpose_progression(self, progression: ChordProgression, 
                            target_key: str) -> ChordProgression:
        """
        Transpose a chord progression to a new key.
        
        Args:
            progression: Original progression
            target_key: Target key
            
        Returns:
            Transposed progression
        """
        # Calculate transposition interval
        original_key_root = progression.key.replace('m', '').replace('M', '')
        target_key_root = target_key.replace('m', '').replace('M', '')
        
        original_midi = NOTE_NAMES.index(original_key_root) 
        target_midi = NOTE_NAMES.index(target_key_root)
        semitones = target_midi - original_midi
        
        return progression.transpose(semitones)
    
    def validate_progression(self, progression: List[str], key: str) -> Dict[str, any]:
        """
        Validate a chord progression for voice leading and harmonic logic.
        
        Args:
            progression: Roman numeral progression
            key: Key signature
            
        Returns:
            Validation results with problems and suggestions
        """
        issues = []
        score = 100
        
        # Check for basic harmonic logic
        for i in range(len(progression) - 1):
            current = progression[i]
            next_chord = progression[i + 1]
            
            # Check for problematic progressions
            if self._is_problematic_progression(current, next_chord):
                issues.append({
                    'position': i,
                    'type': 'weak_progression',
                    'description': f'{current} to {next_chord} is uncommon',
                    'severity': 'minor'
                })
                score -= 5
            
            # Check for parallel motion issues (simplified)
            if self._has_parallel_motion_risk(current, next_chord):
                issues.append({
                    'position': i,
                    'type': 'parallel_motion_risk',
                    'description': f'{current} to {next_chord} may have parallel fifths/octaves',
                    'severity': 'moderate'
                })
                score -= 10
        
        # Check for strong cadences
        has_authentic_cadence = any(
            progression[i:i+2] == ['V', 'I'] or progression[i:i+2] == ['V7', 'I']
            for i in range(len(progression) - 1)
        )
        
        if not has_authentic_cadence and len(progression) > 3:
            issues.append({
                'type': 'missing_cadence',
                'description': 'Progression lacks strong authentic cadence',
                'severity': 'minor'
            })
            score -= 5
        
        return {
            'score': max(0, score),
            'issues': issues,
            'is_valid': score > 60,
            'suggestions': self._generate_improvement_suggestions(progression, issues)
        }
    
    def _parse_roman_numeral(self, roman: str) -> Tuple[int, str]:
        """Parse roman numeral to get degree and quality."""
        # Remove extensions and alterations for now
        base_roman = roman.split('/')[0]  # Remove slash chords
        
        # Quality determination
        if base_roman.isupper():
            quality = 'major'
        elif base_roman.islower():
            quality = 'minor'
        elif '°' in base_roman or 'dim' in base_roman:
            quality = 'diminished'
        elif '+' in base_roman or 'aug' in base_roman:
            quality = 'augmented'
        else:
            quality = 'major'
        
        # Degree calculation
        roman_map = {
            'I': 1, 'i': 1, 'II': 2, 'ii': 2, 'III': 3, 'iii': 3,
            'IV': 4, 'iv': 4, 'V': 5, 'v': 5, 'VI': 6, 'vi': 6,
            'VII': 7, 'vii': 7
        }
        
        base = base_roman.replace('°', '').replace('+', '').replace('7', '')
        degree = roman_map.get(base, 1)
        
        return degree, quality
    
    def _get_chord_root(self, key_root: str, degree: int, is_minor: bool) -> str:
        """Calculate the root note for a chord at a given degree."""
        # Start from key root
        key_index = NOTE_NAMES.index(key_root)
        
        # Use major scale intervals to find the degree
        # Major scale: W W H W W W H (2 2 1 2 2 2 1 semitones)
        scale_intervals = [0, 2, 4, 5, 7, 9, 11]  # Cumulative semitones
        
        if is_minor:
            # Adjust for natural minor (lower 3rd, 6th, 7th)
            scale_intervals = [0, 2, 3, 5, 7, 8, 10]
        
        # Get the note for this degree
        if 1 <= degree <= 7:
            note_index = (key_index + scale_intervals[degree - 1]) % 12
            return NOTE_NAMES[note_index]
        
        return key_root  # Fallback
    
    def _determine_chord_type_from_roman(self, roman: str, is_minor: bool) -> str:
        """Determine chord type string from roman numeral."""
        if '7' in roman:
            if roman.isupper() and '7' in roman and 'maj' not in roman.lower():
                return '7'  # Dominant 7th
            elif roman.isupper() and 'maj7' in roman.lower():
                return 'maj7'
            elif roman.islower():
                return 'min7'
            else:
                return '7'
        elif '°' in roman or 'dim' in roman:
            return 'diminished'
        elif '+' in roman or 'aug' in roman:
            return 'augmented'
        elif roman.islower():
            return 'minor'
        else:
            return 'major'
    
    def _uses_harmonic_minor(self, progression: List[str]) -> bool:
        """Check if progression uses harmonic minor (has major V)."""
        return any('V' in chord and chord.isupper() for chord in progression)
    
    def _detect_key_from_progression(self, chord_symbols: List[str]) -> str:
        """Attempt to detect key from chord symbols."""
        # Simplified key detection - could be much more sophisticated
        # Look for strong tonal indicators like V-I motion
        
        for i in range(len(chord_symbols) - 1):
            current = chord_symbols[i]
            next_chord = chord_symbols[i + 1]
            
            # Look for V-I patterns
            if self._is_dominant_to_tonic(current, next_chord):
                return next_chord  # Assume next chord is tonic
        
        # Fallback: use first chord as key center
        return chord_symbols[0] if chord_symbols else 'C'
    
    def _parse_chord_symbol(self, symbol: str) -> Optional[Dict[str, str]]:
        """Parse chord symbol into components."""
        # Simplified parsing
        import re
        
        pattern = r'^([A-G][#b]?)(.*)$'
        match = re.match(pattern, symbol)
        
        if not match:
            return None
        
        root = match.group(1)
        extensions = match.group(2).lower()
        
        if 'm' in extensions and 'maj' not in extensions:
            quality = 'minor'
        elif 'dim' in extensions:
            quality = 'diminished'
        elif 'aug' in extensions:
            quality = 'augmented'
        else:
            quality = 'major'
        
        return {'root': root, 'quality': quality, 'extensions': extensions}
    
    def _calculate_degree(self, key_root: str, chord_root: str) -> int:
        """Calculate scale degree of chord root relative to key."""
        key_index = NOTE_NAMES.index(key_root)
        chord_index = NOTE_NAMES.index(chord_root)
        
        # Calculate semitone distance
        distance = (chord_index - key_index) % 12
        
        # Map to scale degrees (simplified for major scale)
        degree_map = {0: 1, 2: 2, 4: 3, 5: 4, 7: 5, 9: 6, 11: 7}
        return degree_map.get(distance, 1)
    
    def _generate_roman_numeral(self, degree: int, quality: str, is_minor: bool) -> str:
        """Generate roman numeral from degree and quality."""
        if is_minor:
            functions = MINOR_KEY_FUNCTIONS
        else:
            functions = MAJOR_KEY_FUNCTIONS
        
        base_roman = functions.get(degree, 'I')
        
        # Adjust for actual chord quality vs. expected
        if quality == 'major' and base_roman.islower():
            base_roman = base_roman.upper()
        elif quality == 'minor' and base_roman.isupper():
            base_roman = base_roman.lower()
        
        return base_roman
    
    def _identify_harmonic_function(self, degree: int, quality: str, is_minor: bool) -> str:
        """Identify the harmonic function of a chord."""
        function_map = {
            1: 'tonic',
            2: 'supertonic',
            3: 'mediant', 
            4: 'subdominant',
            5: 'dominant',
            6: 'submediant',
            7: 'leading_tone'
        }
        
        base_function = function_map.get(degree, 'unknown')
        
        # Add functional context
        if degree in [2, 4]:
            return f'{base_function} (predominant)'
        elif degree == 5:
            return f'{base_function} (dominant)'
        elif degree in [1, 3, 6]:
            return f'{base_function} (tonic)'
        
        return base_function
    
    def _identify_cadence(self, chord1: str, chord2: str, is_minor: bool) -> Optional[str]:
        """Identify cadence type between two chords."""
        if chord1 == 'V' and chord2 == 'I':
            return 'authentic'
        elif chord1 == 'V7' and chord2 == 'I':
            return 'authentic'
        elif chord1 == 'IV' and chord2 == 'I':
            return 'plagal'
        elif chord1 == 'V' and chord2 == 'vi':
            return 'deceptive'
        elif chord1 == 'ii' and chord2 == 'V':
            return 'half_cadence_approach'
        
        return None
    
    def _is_secondary_dominant(self, roman: str, is_minor: bool) -> bool:
        """Check if chord is a secondary dominant."""
        return '/' in roman and ('V' in roman or '7' in roman)
    
    def _get_secondary_target(self, roman: str) -> str:
        """Get the target of a secondary dominant."""
        if '/' in roman:
            return roman.split('/')[1]
        return ''
    
    def _get_progression_tendencies(self, style: str, is_minor: bool) -> Dict[str, Dict[str, float]]:
        """Get chord progression tendencies for a style."""
        if style == "pop":
            return {
                'I': {'V': 0.3, 'vi': 0.25, 'IV': 0.2, 'ii': 0.15},
                'vi': {'IV': 0.4, 'V': 0.25, 'I': 0.2, 'ii': 0.1},
                'IV': {'I': 0.35, 'V': 0.3, 'vi': 0.2, 'ii': 0.1},
                'V': {'I': 0.5, 'vi': 0.25, 'IV': 0.15, 'ii': 0.1}
            }
        elif style == "jazz":
            return {
                'I': {'vi': 0.3, 'II7': 0.25, 'V7': 0.2, 'iii': 0.15},
                'ii': {'V7': 0.6, 'V': 0.2, 'I': 0.1, 'vi': 0.05},
                'V7': {'I': 0.5, 'vi': 0.2, 'ii': 0.15, 'IV': 0.1},
                'vi': {'ii': 0.4, 'V7': 0.25, 'IV': 0.2, 'I': 0.1}
            }
        else:  # common_practice
            return {
                'I': {'V': 0.25, 'vi': 0.2, 'IV': 0.2, 'ii': 0.15, 'iii': 0.1},
                'ii': {'V': 0.5, 'V7': 0.3, 'I': 0.1, 'vi': 0.05},
                'V': {'I': 0.6, 'vi': 0.25, 'IV': 0.1, 'ii': 0.03},
                'vi': {'IV': 0.3, 'ii': 0.25, 'V': 0.2, 'I': 0.15}
            }
    
    def _get_progression_reason(self, from_chord: str, to_chord: str, style: str) -> str:
        """Get explanation for chord progression."""
        reasons = {
            ('V', 'I'): 'Strong authentic resolution',
            ('ii', 'V'): 'Predominant to dominant motion',
            ('vi', 'IV'): 'Popular descending motion',
            ('IV', 'I'): 'Plagal resolution',
            ('V', 'vi'): 'Deceptive resolution'
        }
        
        return reasons.get((from_chord, to_chord), 'Common progression')
    
    def _suggest_from_pattern(self, last_two: List[str], style: str, is_minor: bool) -> List[Dict]:
        """Suggest chords based on recent pattern."""
        pattern = tuple(last_two)
        
        pattern_suggestions = {
            ('ii', 'V'): [{'chord': 'I', 'probability': 0.8, 'reason': 'Completes ii-V-I'}],
            ('I', 'vi'): [{'chord': 'ii', 'probability': 0.4, 'reason': 'Continues circle progression'}],
            ('vi', 'ii'): [{'chord': 'V', 'probability': 0.6, 'reason': 'Sets up resolution'}]
        }
        
        return pattern_suggestions.get(pattern, [])
    
    def _is_problematic_progression(self, from_chord: str, to_chord: str) -> bool:
        """Check if progression is problematic."""
        # Some progressions to avoid in common practice
        problematic = [
            ('I', 'ii'),  # Weak progression
            ('iii', 'IV'),  # Uncommon
            ('vi', 'vii')  # Weak
        ]
        
        return (from_chord, to_chord) in problematic
    
    def _has_parallel_motion_risk(self, from_chord: str, to_chord: str) -> bool:
        """Check if progression risks parallel motion."""
        # Simplified - actual voice leading analysis needed
        risk_progressions = [
            ('I', 'V'),  # Risk if not voice-led properly
            ('IV', 'V')   # Common risk area
        ]
        
        return (from_chord, to_chord) in risk_progressions
    
    def _generate_improvement_suggestions(self, progression: List[str], issues: List[Dict]) -> List[str]:
        """Generate suggestions for improving progression."""
        suggestions = []
        
        if not any(issue['type'] == 'missing_cadence' for issue in issues):
            suggestions.append("Consider adding a strong V-I cadence")
        
        if any(issue['type'] == 'weak_progression' for issue in issues):
            suggestions.append("Try using ii-V-I or vi-IV-I-V patterns")
        
        if any(issue['type'] == 'parallel_motion_risk' for issue in issues):
            suggestions.append("Check voice leading for parallel fifths and octaves")
        
        return suggestions
    
    def _is_dominant_to_tonic(self, chord1: str, chord2: str) -> bool:
        """Check if chord1 is dominant of chord2."""
        # Simplified - would need full harmonic analysis
        dominant_patterns = [
            ('G7', 'C'), ('G', 'C'), ('D7', 'G'), ('D', 'G'),
            ('A7', 'D'), ('A', 'D'), ('E7', 'A'), ('E', 'A'),
            ('B7', 'E'), ('B', 'E'), ('F#7', 'B'), ('F#', 'B'),
            ('C#7', 'F#'), ('C#', 'F#')
        ]
        
        return (chord1, chord2) in dominant_patterns