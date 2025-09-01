# -*- coding: utf-8 -*-
"""
Melodic development and variation tools.

Implements classical melodic development techniques using music21 integration.
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from ..models.composition_models import (
    Motif, Melody, MelodicDevelopment, DevelopmentTechnique, 
    Phrase, MelodyVariation
)
from ..genres.library_integration import LibraryIntegration
from ..theory.scales import ScaleManager
from ..theory.chords import ChordManager


class MotifDeveloper:
    """Develops melodic motifs using classical techniques."""
    
    def __init__(self):
        """Initialize with music theory tools."""
        self.libraries = LibraryIntegration()
        self.scale_manager = ScaleManager()
        
    def develop_motif(
        self,
        motif: Motif,
        techniques: List[str],
        target_length: int = 8
    ) -> MelodicDevelopment:
        """
        Develop a melodic motif using specified techniques.
        
        Args:
            motif: Original melodic motif
            techniques: Development techniques to apply
            target_length: Target length in measures
            
        Returns:
            Developed melodic material with analysis
        """
        developed_notes = list(motif.notes)
        applied_techniques = []
        
        for technique in techniques:
            if technique == "sequence":
                developed_notes, tech_info = self._apply_sequence(developed_notes, motif)
                applied_techniques.append(tech_info)
            elif technique == "inversion":
                developed_notes, tech_info = self._apply_inversion(developed_notes, motif)
                applied_techniques.append(tech_info)
            elif technique == "retrograde":
                developed_notes, tech_info = self._apply_retrograde(developed_notes, motif)
                applied_techniques.append(tech_info)
            elif technique == "augmentation":
                motif.rhythm, tech_info = self._apply_augmentation(motif.rhythm)
                applied_techniques.append(tech_info)
            elif technique == "diminution":
                motif.rhythm, tech_info = self._apply_diminution(motif.rhythm)
                applied_techniques.append(tech_info)
            elif technique == "fragmentation":
                developed_notes, tech_info = self._apply_fragmentation(developed_notes, motif)
                applied_techniques.append(tech_info)
                
        # Ensure we reach target length
        while len(developed_notes) < target_length * 4:  # Rough 4 notes per measure
            # Repeat or extend the material
            developed_notes.extend(motif.notes[:2])  # Add first two notes of motif
            
        # Create rhythm if not specified
        rhythm = motif.rhythm or [0.5] * len(developed_notes)
        if len(rhythm) < len(developed_notes):
            rhythm.extend([0.5] * (len(developed_notes) - len(rhythm)))
        elif len(rhythm) > len(developed_notes):
            rhythm = rhythm[:len(developed_notes)]
            
        developed_melody = Melody(
            notes=developed_notes,
            rhythm=rhythm,
            phrase_structure={"type": "developed_motif", "original_length": len(motif.notes)}
        )
        
        analysis = {
            "original_motif": asdict(motif),
            "techniques_count": len(applied_techniques),
            "length_expansion": len(developed_notes) / len(motif.notes),
            "intervallic_preservation": self._analyze_intervallic_preservation(motif, developed_notes)
        }
        
        return MelodicDevelopment(
            original_motif=motif,
            developed_melody=developed_melody,
            techniques_applied=applied_techniques,
            analysis=analysis
        )
    
    def _apply_sequence(self, notes: List[int], motif: Motif) -> Tuple[List[int], DevelopmentTechnique]:
        """Apply sequence technique."""
        # Transpose the motif up by a step (2 semitones) and append
        sequenced_motif = [note + 2 for note in motif.notes]
        new_notes = notes + sequenced_motif
        
        technique = DevelopmentTechnique(
            name="sequence",
            description="Repetition of motif at different pitch level",
            parameters={"transposition": 2, "direction": "ascending"}
        )
        
        return new_notes, technique
    
    def _apply_inversion(self, notes: List[int], motif: Motif) -> Tuple[List[int], DevelopmentTechnique]:
        """Apply inversion technique."""
        if not motif.intervallic_pattern:
            return notes, DevelopmentTechnique("inversion", "No intervals to invert")
            
        # Invert the intervals (make ascending intervals descending and vice versa)
        inverted_intervals = [-interval for interval in motif.intervallic_pattern]
        
        # Build inverted motif starting from original first note
        inverted_motif = [motif.notes[0]]
        current_note = motif.notes[0]
        
        for interval in inverted_intervals:
            current_note += interval
            inverted_motif.append(current_note)
            
        new_notes = notes + inverted_motif
        
        technique = DevelopmentTechnique(
            name="inversion",
            description="Inversion of melodic intervals",
            parameters={"original_intervals": motif.intervallic_pattern, "inverted_intervals": inverted_intervals}
        )
        
        return new_notes, technique
    
    def _apply_retrograde(self, notes: List[int], motif: Motif) -> Tuple[List[int], DevelopmentTechnique]:
        """Apply retrograde technique."""
        retrograde_motif = list(reversed(motif.notes))
        new_notes = notes + retrograde_motif
        
        technique = DevelopmentTechnique(
            name="retrograde", 
            description="Reverse order of motif notes",
            parameters={"original_order": motif.notes, "retrograde_order": retrograde_motif}
        )
        
        return new_notes, technique
    
    def _apply_augmentation(self, rhythm: Optional[List[float]]) -> Tuple[List[float], DevelopmentTechnique]:
        """Apply augmentation (lengthen note values)."""
        if not rhythm:
            rhythm = [1.0, 1.0, 1.0, 1.0]  # Default quarter notes
            
        augmented_rhythm = [duration * 2 for duration in rhythm]
        
        technique = DevelopmentTechnique(
            name="augmentation",
            description="Double the duration of all note values", 
            parameters={"original_rhythm": rhythm, "augmentation_factor": 2}
        )
        
        return augmented_rhythm, technique
    
    def _apply_diminution(self, rhythm: Optional[List[float]]) -> Tuple[List[float], DevelopmentTechnique]:
        """Apply diminution (shorten note values)."""
        if not rhythm:
            rhythm = [1.0, 1.0, 1.0, 1.0]
            
        diminished_rhythm = [duration * 0.5 for duration in rhythm]
        
        technique = DevelopmentTechnique(
            name="diminution", 
            description="Halve the duration of all note values",
            parameters={"original_rhythm": rhythm, "diminution_factor": 0.5}
        )
        
        return diminished_rhythm, technique
    
    def _apply_fragmentation(self, notes: List[int], motif: Motif) -> Tuple[List[int], DevelopmentTechnique]:
        """Apply fragmentation (use only part of motif)."""
        # Take first half of motif and repeat it
        fragment_length = max(1, len(motif.notes) // 2)
        fragment = motif.notes[:fragment_length]
        new_notes = notes + fragment + fragment  # Repeat the fragment
        
        technique = DevelopmentTechnique(
            name="fragmentation",
            description="Use only part of the original motif",
            parameters={"fragment_length": fragment_length, "fragment": fragment}
        )
        
        return new_notes, technique
    
    def _analyze_intervallic_preservation(self, motif: Motif, developed_notes: List[int]) -> float:
        """Analyze how well original intervals are preserved."""
        if not motif.intervallic_pattern or len(developed_notes) < 2:
            return 0.0
            
        # Calculate intervals in developed melody
        developed_intervals = [developed_notes[i+1] - developed_notes[i] 
                             for i in range(len(developed_notes) - 1)]
        
        # Count how many original intervals appear
        preserved_count = 0
        for orig_interval in motif.intervallic_pattern:
            if orig_interval in developed_intervals:
                preserved_count += 1
                
        return preserved_count / len(motif.intervallic_pattern)


class PhraseGenerator:
    """Generates well-formed musical phrases."""
    
    def __init__(self):
        """Initialize with music theory tools.""" 
        self.libraries = LibraryIntegration()
        self.chord_manager = ChordManager()
        
    def create_phrase(
        self,
        chord_progression: List[str],
        key: str,
        phrase_type: str = "period",
        style: str = "vocal"
    ) -> Phrase:
        """
        Create a well-formed melodic phrase.
        
        Args:
            chord_progression: Underlying chords
            key: Key signature
            phrase_type: Phrase structure type
            style: Melodic style
            
        Returns:
            Complete phrase with structure analysis
        """
        # Generate melody that fits the harmonic progression
        melody_notes = self._generate_phrase_melody(chord_progression, key, style)
        
        # Create appropriate rhythm
        rhythm = self._generate_phrase_rhythm(phrase_type, style, len(melody_notes))
        
        melody = Melody(
            notes=melody_notes,
            rhythm=rhythm,
            phrase_structure={"type": phrase_type}
        )
        
        # Analyze phrase structure
        structure_analysis = self._analyze_phrase_structure(phrase_type, len(melody_notes))
        
        # Generate cadences
        cadences = self._generate_cadences(phrase_type, chord_progression)
        
        return Phrase(
            melody=melody,
            harmony=[{"chord": chord, "duration": 4} for chord in chord_progression],
            structure_type=phrase_type,
            structure_analysis=structure_analysis,
            cadences=cadences
        )
    
    def _generate_phrase_melody(self, chord_progression: List[str], key: str, style: str) -> List[int]:
        """Generate melody that fits the harmonic progression."""
        melody_notes = []
        base_octave = 4
        
        # Use music21 if available for scale-based melody generation
        if self.libraries.music21.is_available():
            try:
                key_notes = self.libraries.music21.get_scale_notes("major", key)
                if key_notes:
                    scale_notes = key_notes
                else:
                    scale_notes = self._get_fallback_scale(key)
            except Exception:
                scale_notes = self._get_fallback_scale(key)
        else:
            scale_notes = self._get_fallback_scale(key)
        
        # Generate melody based on chord progression
        for chord in chord_progression:
            # Get chord tones
            chord_tones = self._get_chord_tones(chord, key)
            
            # Add 2-4 notes per chord depending on style
            notes_per_chord = 2 if style == "vocal" else 4
            
            for _ in range(notes_per_chord):
                # Choose between chord tones and scale tones
                if random.random() < 0.6:  # 60% chance of chord tone
                    note = random.choice(chord_tones)
                else:
                    note = random.choice(scale_notes[:7])  # First octave
                    
                melody_notes.append(note + (base_octave * 12))
        
        # Apply style constraints
        if style == "vocal":
            melody_notes = self._apply_vocal_constraints(melody_notes)
            
        return melody_notes
    
    def _get_fallback_scale(self, key: str) -> List[int]:
        """Get a simple major scale as fallback."""
        # Simple C major scale transposed to key
        key_offset = self._get_key_offset(key)
        return [key_offset + offset for offset in [0, 2, 4, 5, 7, 9, 11]]
    
    def _get_key_offset(self, key: str) -> int:
        """Get semitone offset for key."""
        key_offsets = {
            "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
        }
        key_name = key.split()[0]  # Remove "major"/"minor"
        return key_offsets.get(key_name, 0)
    
    def _get_chord_tones(self, chord: str, key: str) -> List[int]:
        """Get the notes that make up a chord."""
        # Simplified chord tone generation
        key_offset = self._get_key_offset(key)
        
        # Roman numeral to interval mapping
        roman_intervals = {
            "I": [0, 4, 7], "ii": [2, 5, 9], "iii": [4, 7, 11],
            "IV": [5, 9, 0], "V": [7, 11, 2], "vi": [9, 0, 4], "vii": [11, 2, 5]
        }
        
        if chord in roman_intervals:
            return [key_offset + interval for interval in roman_intervals[chord]]
        else:
            # Default to tonic triad
            return [key_offset, key_offset + 4, key_offset + 7]
    
    def _apply_vocal_constraints(self, notes: List[int]) -> List[int]:
        """Apply constraints for vocal-friendly melodies."""
        constrained_notes = [notes[0]]  # Keep first note
        
        for i in range(1, len(notes)):
            prev_note = constrained_notes[-1]
            current_note = notes[i]
            interval = abs(current_note - prev_note)
            
            # Limit large leaps for vocal style
            if interval > 7:  # More than a fifth
                # Move by step instead
                direction = 1 if current_note > prev_note else -1
                new_note = prev_note + (direction * 2)  # Move by step
                constrained_notes.append(new_note)
            else:
                constrained_notes.append(current_note)
                
        return constrained_notes
    
    def _generate_phrase_rhythm(self, phrase_type: str, style: str, note_count: int) -> List[float]:
        """Generate appropriate rhythm for phrase."""
        if style == "vocal":
            # Vocal style - longer note values
            base_duration = 1.0  # Quarter notes
        else:
            # Instrumental style - more varied rhythms
            base_duration = 0.5  # Eighth notes
            
        rhythm = []
        for i in range(note_count):
            # Add some rhythmic variation
            if i % 4 == 3:  # End of measure - longer note
                rhythm.append(base_duration * 1.5)
            else:
                rhythm.append(base_duration)
                
        return rhythm
    
    def _analyze_phrase_structure(self, phrase_type: str, length: int) -> Dict[str, Any]:
        """Analyze the phrase structure."""
        if phrase_type == "period":
            return {
                "type": "period",
                "antecedent": {"measures": list(range(1, length//2 + 1))},
                "consequent": {"measures": list(range(length//2 + 1, length + 1))},
                "length": length
            }
        elif phrase_type == "sentence":
            return {
                "type": "sentence",
                "presentation": {"measures": list(range(1, length//4 + 1))},
                "repetition": {"measures": list(range(length//4 + 1, length//2 + 1))},
                "continuation": {"measures": list(range(length//2 + 1, length + 1))},
                "length": length
            }
        else:
            return {"type": "phrase_group", "length": length}
    
    def _generate_cadences(self, phrase_type: str, progression: List[str]) -> List[Dict[str, Any]]:
        """Generate cadences for the phrase."""
        cadences = []
        
        if phrase_type == "period":
            # Half cadence at end of antecedent
            cadences.append({
                "type": "half_cadence",
                "location": "mid_phrase",
                "chords": ["I", "V"]
            })
            # Authentic cadence at end
            cadences.append({
                "type": "authentic_cadence", 
                "location": "phrase_end",
                "chords": ["V", "I"]
            })
        else:
            # Simple authentic cadence
            cadences.append({
                "type": "authentic_cadence",
                "location": "phrase_end", 
                "chords": ["V", "I"]
            })
            
        return cadences


class MelodyVariator:
    """Creates variations of existing melodies."""
    
    def __init__(self):
        """Initialize melody variator."""
        self.libraries = LibraryIntegration()
        
    def create_variation(
        self,
        original_melody: List[int],
        variation_type: str = "embellishment"
    ) -> MelodyVariation:
        """
        Create variation of a melody.
        
        Args:
            original_melody: Original melody notes
            variation_type: Type of variation
            
        Returns:
            Melody variation with analysis
        """
        if variation_type == "embellishment":
            varied_notes, techniques = self._apply_embellishment(original_melody)
        elif variation_type == "rhythmic":
            varied_notes, techniques = self._apply_rhythmic_variation(original_melody)
        elif variation_type == "harmonic":
            varied_notes, techniques = self._apply_harmonic_variation(original_melody)
        elif variation_type == "modal":
            varied_notes, techniques = self._apply_modal_variation(original_melody)
        elif variation_type == "ornamental":
            varied_notes, techniques = self._apply_ornamentation(original_melody)
        else:
            # Default to embellishment
            varied_notes, techniques = self._apply_embellishment(original_melody)
            
        # Calculate similarity score
        similarity_score = self._calculate_similarity(original_melody, varied_notes)
        
        # Create rhythm for varied melody
        rhythm = [0.5] * len(varied_notes)  # Default eighth notes
        
        varied_melody = Melody(notes=varied_notes, rhythm=rhythm)
        
        return MelodyVariation(
            original_melody=original_melody,
            varied_melody=varied_melody,
            variation_type=variation_type,
            similarity_score=similarity_score,
            variation_techniques=techniques
        )
    
    def _apply_embellishment(self, melody: List[int]) -> Tuple[List[int], List[str]]:
        """Add embellishing notes between original notes."""
        embellished = []
        techniques = ["passing_tones", "neighbor_tones"]
        
        for i in range(len(melody)):
            embellished.append(melody[i])
            
            # Add passing tone between notes
            if i < len(melody) - 1:
                current = melody[i]
                next_note = melody[i + 1]
                interval = abs(next_note - current)
                
                # Add passing tone for intervals larger than a whole step
                if interval >= 3:
                    direction = 1 if next_note > current else -1
                    passing_tone = current + direction
                    embellished.append(passing_tone)
                    
        return embellished, techniques
    
    def _apply_rhythmic_variation(self, melody: List[int]) -> Tuple[List[int], List[str]]:
        """Apply rhythmic variation while keeping pitches similar."""
        # For rhythmic variation, we keep the same pitches but could repeat some
        varied = []
        techniques = ["rhythmic_displacement", "syncopation"]
        
        for note in melody:
            varied.append(note)
            # Occasionally repeat a note for rhythmic effect
            if random.random() < 0.3:
                varied.append(note)
                
        return varied, techniques
    
    def _apply_harmonic_variation(self, melody: List[int]) -> Tuple[List[int], List[str]]:
        """Apply harmonic variation by changing some pitches."""
        varied = []
        techniques = ["chord_tone_substitution", "chromatic_alteration"]
        
        for note in melody:
            if random.random() < 0.3:  # 30% chance to alter
                # Move up or down by semitone
                altered_note = note + random.choice([-1, 1])
                varied.append(altered_note)
            else:
                varied.append(note)
                
        return varied, techniques
    
    def _apply_modal_variation(self, melody: List[int]) -> Tuple[List[int], List[str]]:
        """Apply modal variation by altering scale degrees."""
        varied = []
        techniques = ["modal_mixture", "scale_alteration"]
        
        for note in melody:
            # Occasionally lower certain degrees (like 3rd, 6th, 7th for minor feel)
            if random.random() < 0.2:
                altered_note = note - 1  # Lower by semitone
                varied.append(altered_note)
            else:
                varied.append(note)
                
        return varied, techniques
    
    def _apply_ornamentation(self, melody: List[int]) -> Tuple[List[int], List[str]]:
        """Add ornamental figures to the melody."""
        ornamented = []
        techniques = ["trills", "mordents", "appoggiaturas"]
        
        for note in melody:
            # Add appoggiatura (grace note) occasionally
            if random.random() < 0.25:
                grace_note = note + 1  # Upper neighbor
                ornamented.append(grace_note)
                
            ornamented.append(note)
            
        return ornamented, techniques
    
    def _calculate_similarity(self, original: List[int], variation: List[int]) -> float:
        """Calculate similarity score between original and variation."""
        if not original or not variation:
            return 0.0
            
        # Count common notes
        original_set = set(original)
        variation_set = set(variation)
        common_notes = len(original_set.intersection(variation_set))
        total_unique = len(original_set.union(variation_set))
        
        if total_unique == 0:
            return 1.0
            
        similarity = common_notes / total_unique
        
        # Also consider interval preservation
        if len(original) > 1 and len(variation) > 1:
            orig_intervals = set(original[i+1] - original[i] for i in range(len(original)-1))
            var_intervals = set(variation[i+1] - variation[i] for i in range(len(variation)-1))
            
            if orig_intervals:
                interval_similarity = len(orig_intervals.intersection(var_intervals)) / len(orig_intervals)
                similarity = (similarity + interval_similarity) / 2
                
        return similarity