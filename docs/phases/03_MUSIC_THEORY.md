# Phase 3: Music Theory Implementation

## Overview
Integrate comprehensive music theory knowledge into the MCP server, enabling AI agents to create musically intelligent compositions using scales, chords, progressions, and harmonic relationships.

## Goals
- Implement comprehensive scale and chord libraries
- Add chord progression generation and validation
- Create key detection and modulation tools
- Establish music theory rule engine for harmonic validation

## Duration: Week 3 (5 days)

## Prerequisites
- Phases 1 and 2 completed and tested
- Working MIDI file creation and playback system
- Basic understanding of music theory concepts

## Day-by-Day Implementation

### Day 1: Scales and Intervals Foundation
**Morning (3-4 hours):**
- Implement comprehensive scale library
- Add interval calculation and validation
- Create scale degree identification
- Add mode generation and rotation

**Code Framework**:
```python
@mcp.tool()
def get_scale_notes(root_note: str, scale_type: str, octave: int = 4) -> dict:
    """
    Generate notes for a specific scale.
    
    Args:
        root_note: Root note (C, C#, Db, D, etc.)
        scale_type: Scale type (major, minor, dorian, mixolydian, 
                   pentatonic_major, pentatonic_minor, blues, etc.)
        octave: Starting octave (0-9)
    
    Returns:
        List of MIDI note numbers and note names in the scale
    """

@mcp.tool()
def identify_intervals(notes: List[int]) -> dict:
    """
    Identify intervals between consecutive notes.
    
    Args:
        notes: List of MIDI note numbers
        
    Returns:
        List of interval types (unison, minor2nd, major2nd, etc.)
    """

@mcp.tool()
def transpose_to_key(notes: List[int], from_key: str, to_key: str) -> dict:
    """
    Transpose a sequence of notes from one key to another.
    
    Args:
        notes: Original MIDI note numbers
        from_key: Original key (C, G, F#, etc.)
        to_key: Target key
    """
```

**Afternoon (2-3 hours):**
- Build scale relationship matrix (relative, parallel, modes)
- Add scale degree naming (tonic, supertonic, etc.)
- Create scale comparison and similarity tools
- Test scale generation accuracy

**HIL Test**: "Ask AI to generate an E minor scale, then transpose it to F# major"

### Day 2: Chord Construction and Analysis
**Morning (3-4 hours):**
- Implement comprehensive chord library
- Add chord construction from intervals
- Create chord inversion and voicing tools
- Add chord symbol parsing and generation

**Code Framework**:
```python
@mcp.tool()
def build_chord(root_note: str, chord_type: str, inversion: int = 0, 
                voicing: str = "close") -> dict:
    """
    Build a chord with specified parameters.
    
    Args:
        root_note: Root note of chord (C, F#, Bb, etc.)
        chord_type: Chord quality (major, minor, dom7, maj7, min7, 
                   dim, aug, sus2, sus4, add9, etc.)
        inversion: Chord inversion (0=root position, 1=first, 2=second, etc.)
        voicing: Voicing style (close, open, drop2, drop3)
    
    Returns:
        MIDI note numbers and chord analysis
    """

@mcp.tool()
def analyze_chord(notes: List[int]) -> dict:
    """
    Analyze a set of notes to identify chord(s).
    
    Args:
        notes: MIDI note numbers to analyze
        
    Returns:
        Possible chord interpretations with confidence scores
    """

@mcp.tool()
def get_chord_tones_and_extensions(chord_symbol: str) -> dict:
    """
    Break down a chord symbol into component tones.
    
    Args:
        chord_symbol: Chord symbol (Cmaj7, F#dim, Bb7sus4, etc.)
        
    Returns:
        Root, chord tones, available tensions, avoid notes
    """
```

**Afternoon (2-3 hours):**
- Add chord quality detection (major, minor, diminished, augmented)
- Implement chord extension handling (7ths, 9ths, 11ths, 13ths)
- Create chord substitution suggestions
- Test chord analysis accuracy

**HIL Test**: "Ask AI to build a Cmaj9 chord, then analyze what makes it different from a C7 chord"

### Day 3: Chord Progressions and Harmonic Function
**Morning (3-4 hours):**
- Implement functional harmony analysis (I, ii, V7, etc.)
- Add common chord progression library
- Create progression validation and smoothness scoring
- Add voice leading analysis and optimization

**Code Framework**:
```python
@mcp.tool()
def create_chord_progression(key: str, progression: List[str], 
                           duration_per_chord: float = 1.0) -> dict:
    """
    Create a chord progression in a specific key.
    
    Args:
        key: Key signature (C, Am, F#, Bbm, etc.)
        progression: Roman numeral progression (["I", "vi", "ii", "V"])
        duration_per_chord: Duration of each chord in beats
        
    Returns:
        MIDI data for the chord progression
    """

@mcp.tool()
def analyze_progression(chord_symbols: List[str], key: str = None) -> dict:
    """
    Analyze the harmonic function of a chord progression.
    
    Args:
        chord_symbols: List of chord symbols (["C", "Am", "F", "G"])
        key: Key context (auto-detected if None)
        
    Returns:
        Roman numeral analysis, key relationships, voice leading quality
    """

@mcp.tool()
def suggest_next_chord(current_progression: List[str], key: str,
                      style: str = "common_practice") -> dict:
    """
    Suggest logical next chords for a progression.
    
    Args:
        current_progression: Existing chord progression
        key: Key signature
        style: Harmonic style (common_practice, jazz, pop, modal)
        
    Returns:
        List of suggested chords with probability scores
    """
```

**Afternoon (2-3 hours):**
- Build common progression templates (ii-V-I, vi-IV-I-V, etc.)
- Add modulation detection and pivot chord analysis
- Create circle of fifths navigation
- Test progression generation and analysis

**HIL Test**: "Ask AI to create a ii-V-I progression in G major, then suggest what chord could come next"

### Day 4: Key Analysis and Modulation
**Morning (3-4 hours):**
- Implement key detection from MIDI data
- Add modulation identification and analysis
- Create key relationship tools (relative, parallel, closely related)
- Add tonicization and temporary key area detection

**Code Framework**:
```python
@mcp.tool()
def detect_key(midi_file_id: str, track_number: int = None) -> dict:
    """
    Detect the key(s) of a MIDI file or track.
    
    Args:
        midi_file_id: ID of MIDI file to analyze
        track_number: Specific track to analyze (all tracks if None)
        
    Returns:
        Most likely key(s) with confidence scores, key changes
    """

@mcp.tool()
def analyze_modulations(midi_file_id: str) -> dict:
    """
    Identify key changes and modulations in a MIDI file.
    
    Returns:
        Timeline of key changes, modulation types, pivot analysis
    """

@mcp.tool()
def suggest_modulation(from_key: str, to_key: str) -> dict:
    """
    Suggest ways to modulate between two keys.
    
    Args:
        from_key: Starting key
        to_key: Target key
        
    Returns:
        Pivot chords, common tones, modulation strategies
    """
```

**Afternoon (2-3 hours):**
- Add key signature and accidental management
- Create enharmonic equivalence handling
- Implement chromatic harmony analysis
- Test key detection accuracy with various musical styles

**HIL Test**: "Ask AI to analyze the key of a loaded MIDI file and suggest a modulation to the relative minor"

### Day 5: Advanced Theory Integration and Validation
**Morning (3-4 hours):**
- Implement harmonic rhythm analysis
- Add non-chord tone identification (passing tones, neighbors, etc.)
- Create voice leading validation and improvement
- Add parallel motion detection and correction

**Code Framework**:
```python
@mcp.tool()
def validate_voice_leading(chord_progression: List[dict]) -> dict:
    """
    Validate and score voice leading in a chord progression.
    
    Args:
        chord_progression: List of chord dictionaries with voicings
        
    Returns:
        Voice leading analysis, problem identification, improvement suggestions
    """

@mcp.tool()
def add_non_chord_tones(melody: List[int], chord_progression: List[dict],
                       style: str = "common_practice") -> dict:
    """
    Add appropriate non-chord tones to a melody.
    
    Args:
        melody: Original melody notes
        chord_progression: Underlying harmony
        style: Style context for non-chord tone usage
        
    Returns:
        Enhanced melody with non-chord tones
    """

@mcp.tool()
def create_harmonic_analysis(midi_file_id: str) -> dict:
    """
    Create complete harmonic analysis of a MIDI file.
    
    Returns:
        Comprehensive analysis including key areas, chord progressions,
        voice leading, form analysis, cadence identification
    """
```

**Afternoon (2-3 hours):**
- Complete integration testing with MIDI file operations
- Create music theory rule validation system
- Add theory-guided composition suggestions
- Prepare comprehensive examples and documentation

**HIL Test**: "Ask AI to create a Bach-style chord progression with proper voice leading, then analyze the harmonic function of each chord"

## File Structure After Phase 3
```
midi-mcp/
├── src/
│   ├── server.py
│   ├── midi/
│   │   └── [existing files]
│   ├── theory/
│   │   ├── __init__.py
│   │   ├── scales.py           # Scale definitions and operations
│   │   ├── chords.py           # Chord construction and analysis
│   │   ├── progressions.py     # Chord progression tools
│   │   ├── keys.py             # Key analysis and modulation
│   │   ├── voice_leading.py    # Voice leading rules and validation
│   │   ├── analysis.py         # Comprehensive music analysis
│   │   └── constants.py        # Music theory constants and data
│   ├── models/
│   │   ├── theory_models.py    # Music theory data models
│   │   └── [existing files]
│   └── [existing directories]
├── data/
│   ├── scales.json             # Scale definitions
│   ├── chords.json             # Chord library
│   ├── progressions.json       # Common progressions
│   └── theory_rules.json       # Harmonic rules and constraints
├── tests/
│   ├── test_scales.py
│   ├── test_chords.py
│   ├── test_progressions.py
│   ├── test_key_analysis.py
│   └── [existing test files]
└── [existing files and directories]
```

## Music Theory Knowledge Base

### Scale Library Includes:
- **Major scales**: All 12 keys
- **Minor scales**: Natural, harmonic, melodic
- **Modes**: Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian
- **Pentatonic scales**: Major and minor pentatonic
- **Blues scales**: Major and minor blues
- **Jazz scales**: Altered, half-diminished, whole tone
- **World music scales**: Harmonic major, Hungarian minor, etc.

### Chord Library Includes:
- **Triads**: Major, minor, diminished, augmented
- **Seventh chords**: Major 7, minor 7, dominant 7, half-diminished, diminished
- **Extended chords**: 9ths, 11ths, 13ths with all alterations
- **Suspended chords**: sus2, sus4, sus2sus4
- **Added tone chords**: add9, add11, add13, maj7add13, etc.

### Progression Library Includes:
- **Classical**: I-vi-ii-V, I-IV-vi-V, vi-ii-V-I
- **Jazz**: ii-V-I, I-vi-ii-V, iii-vi-ii-V-I
- **Pop/Rock**: vi-IV-I-V, I-V-vi-IV, I-VII-IV-I
- **Blues**: I-I-I-I-IV-IV-I-I-V-IV-I-V
- **Modal**: Various modal progression patterns

## HIL Testing Scenarios

### Scenario 1: Scale-Based Melody Creation
```
Human: "Create a melody in D dorian mode"
Expected: AI generates scale, creates melodic phrase using scale tones
Result: Melody that clearly demonstrates dorian characteristics
```

### Scenario 2: Chord Progression Analysis
```
Human: "Analyze this chord progression: Dm - G7 - Cmaj7 - Am"
Expected: AI identifies ii-V-I-vi in C major, explains function
Result: Complete harmonic analysis with Roman numerals
```

### Scenario 3: Voice Leading Optimization
```
Human: "Create a four-part harmony for this chord progression with smooth voice leading"
Expected: AI applies voice leading rules, minimizes large leaps
Result: Well-voiced progression playable by human ensemble
```

### Scenario 4: Key Modulation
```
Human: "Start in C major, then modulate to E minor using a pivot chord"
Expected: AI identifies common chords, creates smooth transition
Result: Musical modulation that sounds natural and logical
```

## Success Criteria
- [ ] All scales generate correct note sequences
- [ ] Chord construction produces accurate harmonies
- [ ] Progression analysis identifies correct harmonic functions
- [ ] Key detection accuracy > 90% on test files
- [ ] Voice leading follows established rules
- [ ] Integration with MIDI operations works seamlessly
- [ ] AI agents can create theory-informed compositions
- [ ] All HIL test scenarios pass consistently

## Integration with Previous Phases
- Scales can be played using Phase 1 real-time tools
- Chord progressions can be saved as MIDI files (Phase 2)
- Theory analysis can be applied to loaded MIDI files
- All theory tools work with existing MIDI manipulation

## Performance Requirements
- Scale generation: < 10ms
- Chord analysis: < 50ms per chord
- Key detection: < 500ms for typical song
- Progression analysis: < 200ms for 8-chord sequence

## Next Phase Preparation
- Verify theory accuracy with music theory expert review
- Test integration with complex musical examples
- Prepare genre-specific theory applications
- Review genre knowledge base requirements for Phase 4

Phase 3 establishes the musical intelligence that enables AI agents to create harmonically sophisticated compositions. The focus is on accuracy, completeness, and seamless integration with practical music creation tools.