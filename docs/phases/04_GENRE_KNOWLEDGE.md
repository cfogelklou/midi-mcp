# Phase 4: Genre Knowledge Base Implementation

## Overview
Implement comprehensive genre-specific musical knowledge, enabling AI agents to create authentic music in various styles including Blues, Rock, Hip Hop, and Bluegrass. This phase transforms generic music theory into style-specific creation tools.

## Goals
- Build comprehensive genre knowledge databases
- Implement genre-specific composition rules and patterns
- Create style-appropriate rhythm and instrumentation tools
- Enable AI agents to create authentic genre-based music

## Duration: Week 4 (5 days)

## Prerequisites
- Phases 1-3 completed and tested
- Working music theory system with scales, chords, and progressions
- MIDI file creation and editing capabilities

## Day-by-Day Implementation

### Day 1: Genre Knowledge Base Architecture
**Morning (3-4 hours):**
- Design genre knowledge data structures
- Implement genre profile loading system
- Create genre characteristic validation
- Build genre inheritance and fusion capabilities

**Code Framework**:
```python
@mcp.tool()
def get_genre_characteristics(genre: str) -> dict:
    """
    Get comprehensive characteristics for a musical genre.
    
    Args:
        genre: Genre name (blues, rock, jazz, hip_hop, bluegrass, country, etc.)
        
    Returns:
        Genre profile including tempo ranges, typical progressions,
        instrumentation, rhythmic patterns, and style characteristics
    """

@mcp.tool()
def list_available_genres() -> dict:
    """
    List all available genres in the knowledge base.
    
    Returns:
        Categorized list of genres with brief descriptions
    """

@mcp.tool()
def compare_genres(genre1: str, genre2: str) -> dict:
    """
    Compare characteristics between two genres.
    
    Args:
        genre1: First genre to compare
        genre2: Second genre to compare
        
    Returns:
        Similarities, differences, and fusion possibilities
    """
```

**Afternoon (2-3 hours):**
- Load initial genre data (Blues, Rock, Hip Hop, Bluegrass)
- Test genre profile retrieval and validation
- Create genre hierarchy and relationships
- Add genre tagging and categorization system

**HIL Test**: "Ask AI to describe the characteristics of blues music and compare it to rock"

### Day 2: Blues Knowledge Implementation
**Morning (3-4 hours):**
- Implement comprehensive blues knowledge base
- Add 12-bar blues progression variations
- Create blues scale and harmonic patterns
- Add blues-specific rhythmic feel (shuffle, swing)

**Code Framework**:
```python
@mcp.tool()
def create_blues_progression(key: str, variation: str = "standard", 
                           bars: int = 12) -> dict:
    """
    Create an authentic blues chord progression.
    
    Args:
        key: Key signature (works best with E, A, G, D, B)
        variation: Blues variation (standard, quick_change, minor_blues)
        bars: Number of bars (12, 8, or 16)
        
    Returns:
        Blues progression with appropriate chord voicings and timing
    """

@mcp.tool()
def add_blues_feel(midi_file_id: str, shuffle_intensity: float = 0.67) -> dict:
    """
    Apply authentic blues feel to existing MIDI data.
    
    Args:
        midi_file_id: MIDI file to modify
        shuffle_intensity: Swing ratio (0.5=straight, 0.67=medium shuffle, 0.75=heavy shuffle)
        
    Returns:
        Modified MIDI with blues timing feel
    """

@mcp.tool()
def create_blues_melody(key: str, progression: dict, style: str = "traditional") -> dict:
    """
    Generate an authentic blues melody.
    
    Args:
        key: Key of the blues
        progression: Chord progression to follow
        style: Blues style (traditional, chicago, delta, electric)
        
    Returns:
        Blues melody with appropriate scales, bends, and phrasing
    """
```

**Afternoon (2-3 hours):**
- Add blues turnaround patterns
- Implement call-and-response structures
- Create blues-specific instrumentation templates
- Add blue note handling and microtonal bends

**HIL Test**: "Ask AI to create a 12-bar blues in E with authentic shuffle feel and a simple melody"

### Day 3: Rock Knowledge Implementation
**Morning (3-4 hours):**
- Build comprehensive rock music knowledge base
- Implement power chord progressions and voicings
- Add rock-specific song structures (verse-chorus-bridge)
- Create rock rhythmic patterns and drum beats

**Code Framework**:
```python
@mcp.tool()
def create_rock_progression(key: str, style: str = "classic_rock", 
                          complexity: str = "medium") -> dict:
    """
    Create an authentic rock chord progression.
    
    Args:
        key: Key signature (E, A, D, G work well for rock)
        style: Rock style (classic_rock, hard_rock, pop_rock, punk, metal)
        complexity: Harmonic complexity (simple, medium, complex)
        
    Returns:
        Rock progression with power chords and full chord options
    """

@mcp.tool()
def add_rock_arrangement(midi_file_id: str, lineup: str = "standard") -> dict:
    """
    Arrange existing music for a rock band.
    
    Args:
        midi_file_id: Base musical material
        lineup: Band configuration (standard, power_trio, extended)
        
    Returns:
        Full rock arrangement with appropriate parts for each instrument
    """

@mcp.tool()
def create_rock_drum_pattern(style: str = "basic_rock", tempo: int = 120,
                           complexity: str = "medium") -> dict:
    """
    Create authentic rock drum patterns.
    
    Args:
        style: Drum style (basic_rock, shuffle_rock, punk, metal)
        tempo: Tempo in BPM
        complexity: Pattern complexity (simple, medium, complex)
        
    Returns:
        Complete drum pattern with kick, snare, hi-hat, and fills
    """
```

**Afternoon (2-3 hours):**
- Add rock guitar techniques (power chords, palm muting, etc.)
- Implement rock song form templates
- Create rock bass line patterns
- Add distortion and dynamics simulation

**HIL Test**: "Ask AI to create a classic rock song structure with power chord progression and driving drum beat"

### Day 4: Hip Hop and Bluegrass Implementation
**Morning (3-4 hours) - Hip Hop:**
- Build hip hop production knowledge base
- Implement trap and boom-bap rhythm patterns
- Add hip hop chord progression tendencies
- Create sampling and loop-based composition tools

**Code Framework**:
```python
@mcp.tool()
def create_hip_hop_beat(style: str = "boom_bap", tempo: int = 90,
                       complexity: str = "medium") -> dict:
    """
    Create authentic hip hop drum patterns.
    
    Args:
        style: Hip hop style (boom_bap, trap, lo_fi, drill, old_school)
        tempo: Tempo in BPM (typically 70-140)
        complexity: Beat complexity (simple, medium, complex)
        
    Returns:
        Hip hop drum pattern with appropriate samples and programming
    """

@mcp.tool()
def create_hip_hop_chord_loop(key: str, mood: str = "dark", 
                            duration: int = 4) -> dict:
    """
    Create chord progression suitable for hip hop production.
    
    Args:
        key: Key signature
        mood: Overall mood (dark, uplifting, mysterious, aggressive)
        duration: Loop length in bars
        
    Returns:
        Hip hop chord progression with appropriate voicings and rhythm
    """
```

**Afternoon (2-3 hours) - Bluegrass:**
- Build bluegrass tradition knowledge base
- Implement bluegrass picking patterns and techniques
- Add bluegrass song forms and structures
- Create authentic bluegrass instrumentation

**Code Framework**:
```python
@mcp.tool()
def create_bluegrass_arrangement(song_structure: dict, key: str = "G") -> dict:
    """
    Create full bluegrass band arrangement.
    
    Args:
        song_structure: Basic melody and chord progression
        key: Key signature (G, D, A, C, F work well)
        
    Returns:
        Full arrangement with banjo, fiddle, guitar, mandolin, bass parts
    """

@mcp.tool()
def add_bluegrass_picking_pattern(instrument: str, chord_progression: dict) -> dict:
    """
    Add authentic picking patterns for bluegrass instruments.
    
    Args:
        instrument: Target instrument (banjo, guitar, mandolin)
        chord_progression: Chord progression to follow
        
    Returns:
        Picking pattern appropriate to instrument and style
    """
```

**HIL Test**: "Ask AI to create a lo-fi hip hop beat and a bluegrass fiddle tune"

### Day 5: Integration and Style Fusion
**Morning (3-4 hours):**
- Create genre fusion and crossover capabilities
- Implement style intensity controls (how strictly to follow genre rules)
- Add genre evolution and modern variations
- Build genre-appropriate song structure templates

**Code Framework**:
```python
@mcp.tool()
def create_fusion_style(primary_genre: str, secondary_genre: str, 
                       balance: float = 0.5) -> dict:
    """
    Create a fusion of two musical genres.
    
    Args:
        primary_genre: Dominant genre (provides main structure)
        secondary_genre: Secondary genre (provides flavor elements)
        balance: Balance between genres (0.0=all primary, 1.0=all secondary)
        
    Returns:
        Fusion style profile with blended characteristics
    """

@mcp.tool()
def apply_genre_style(midi_file_id: str, target_genre: str,
                     intensity: float = 0.8) -> dict:
    """
    Apply genre-specific styling to existing musical material.
    
    Args:
        midi_file_id: Source musical material
        target_genre: Genre style to apply
        intensity: How strongly to apply genre characteristics (0.0-1.0)
        
    Returns:
        Restyled musical material with genre characteristics
    """

@mcp.tool()
def create_song_from_genre_template(genre: str, song_type: str,
                                  key: str, tempo: int) -> dict:
    """
    Create complete song from genre-specific template.
    
    Args:
        genre: Target musical genre
        song_type: Type of song (ballad, uptempo, dance, etc.)
        key: Key signature
        tempo: Tempo in BPM
        
    Returns:
        Complete song structure with all sections and arrangements
    """
```

**Afternoon (2-3 hours):**
- Complete comprehensive testing of all genre tools
- Create genre-specific validation and quality assessment
- Add genre recommendation system
- Prepare documentation and examples

**HIL Test**: "Ask AI to create a blues-rock fusion song, then apply hip hop production techniques to a bluegrass melody"

## File Structure After Phase 4
```
midi-mcp/
├── src/
│   ├── server.py
│   ├── midi/ [existing files]
│   ├── theory/ [existing files]
│   ├── genres/
│   │   ├── __init__.py
│   │   ├── genre_manager.py      # Genre loading and management
│   │   ├── blues.py              # Blues-specific implementations
│   │   ├── rock.py               # Rock-specific implementations  
│   │   ├── hip_hop.py            # Hip hop-specific implementations
│   │   ├── bluegrass.py          # Bluegrass-specific implementations
│   │   ├── fusion.py             # Genre fusion capabilities
│   │   └── validator.py          # Genre authenticity validation
│   ├── models/
│   │   ├── genre_models.py       # Genre-specific data models
│   │   └── [existing files]
│   └── [existing directories]
├── data/
│   ├── genres/
│   │   ├── blues.json            # Blues knowledge base
│   │   ├── rock.json             # Rock knowledge base
│   │   ├── hip_hop.json          # Hip hop knowledge base
│   │   ├── bluegrass.json        # Bluegrass knowledge base
│   │   └── genre_relationships.json # Inter-genre relationships
│   ├── patterns/
│   │   ├── drum_patterns/        # Genre-specific drum patterns
│   │   ├── bass_patterns/        # Genre-specific bass patterns
│   │   └── chord_voicings/       # Genre-specific chord voicings
│   └── [existing files]
├── tests/
│   ├── test_genres.py
│   ├── test_blues.py
│   ├── test_rock.py
│   ├── test_hip_hop.py
│   ├── test_bluegrass.py
│   └── [existing test files]
└── [existing directories]
```

## Genre Knowledge Database Structure

### Blues Knowledge Base
```json
{
  "blues": {
    "characteristics": {
      "tempo_range": [60, 120],
      "time_signatures": ["4/4", "12/8"],
      "typical_keys": ["E", "A", "G", "D", "B"],
      "mood_descriptors": ["melancholy", "soulful", "gritty", "emotional"]
    },
    "harmonic_patterns": {
      "progressions": {
        "standard_12_bar": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"],
        "quick_change": ["I7", "IV7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"]
      },
      "turnarounds": ["I-VI-ii-V", "I-#idim-ii-V"]
    },
    "scales": {
      "primary": ["blues_scale", "minor_pentatonic"],
      "secondary": ["mixolydian", "dorian"]
    },
    "instrumentation": {
      "essential": ["guitar", "vocals", "harmonica"],
      "common": ["bass", "drums", "piano"]
    }
  }
}
```

## HIL Testing Scenarios

### Scenario 1: Blues Authenticity
```
Human: "Create an authentic 12-bar blues in A with shuffle feel"
Expected: AI creates proper 12-bar form (A7-A7-A7-A7-D7-D7-A7-A7-E7-D7-A7-E7) with shuffle timing
Result: Blues that would be recognizable to blues musicians
```

### Scenario 2: Rock Power and Drive
```
Human: "Create a driving rock song with power chords and a strong backbeat"
Expected: AI uses power chord voicings, emphasizes beats 2 and 4, creates energy
Result: Rock song that sounds powerful and energetic
```

### Scenario 3: Hip Hop Production Feel
```
Human: "Create a lo-fi hip hop beat with a dark, moody chord progression"
Expected: AI creates appropriate drum programming with vinyl crackle feel, minor chord progressions
Result: Beat that sounds like contemporary hip hop production
```

### Scenario 4: Bluegrass Tradition
```
Human: "Create a bluegrass tune with banjo rolls and fiddle melody"
Expected: AI creates appropriate picking patterns, fast tempo, traditional harmony
Result: Tune that sounds authentically bluegrass
```

### Scenario 5: Genre Fusion
```
Human: "Combine blues and hip hop to create something unique"
Expected: AI blends blues harmony/melody with hip hop rhythms and production
Result: Creative fusion that maintains elements of both genres
```

## Success Criteria
- [ ] All genre knowledge bases contain accurate information
- [ ] AI agents create recognizable genre-specific music
- [ ] Musical output passes authenticity tests by genre experts
- [ ] Genre fusion produces creative and musical results
- [ ] System handles genre requests consistently
- [ ] Performance remains acceptable with expanded knowledge base
- [ ] All HIL test scenarios demonstrate genre accuracy

## Musical Authenticity Validation
Each genre implementation includes validation criteria:
- **Harmonic Authenticity**: Chord progressions match genre conventions
- **Rhythmic Accuracy**: Time feel and rhythmic patterns are genre-appropriate
- **Structural Correctness**: Song forms follow genre traditions
- **Instrumental Appropriateness**: Instrumentation matches genre expectations
- **Style Consistency**: Overall feel aligns with genre characteristics

## Integration with Previous Phases
- Genre knowledge enhances music theory applications (Phase 3)
- Genre-specific MIDI files can be created and edited (Phase 2)
- Real-time performance uses genre-appropriate patterns (Phase 1)
- All existing functionality works within genre contexts

## Next Phase Preparation
- Verify genre authenticity with musical experts
- Test genre knowledge with complex composition scenarios
- Prepare advanced composition tools for Phase 5
- Review specialized agent requirements

Phase 4 transforms the MIDI MCP server from a general music tool into a genre-aware composition system that can create authentic music in specific styles. This cultural and stylistic knowledge enables AI agents to create music that resonates with listeners familiar with these genres.