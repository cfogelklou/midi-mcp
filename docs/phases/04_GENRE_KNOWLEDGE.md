# Phase 4: Genre Knowledge Base Implementation - REVISED DESIGN

## Overview
Implement comprehensive genre-specific musical knowledge with **generic, parameterized tools** that can work with any genre. This scalable approach enables AI agents to create authentic music in various styles without cluttering the API with genre-specific functions.

## Goals
- Build comprehensive genre knowledge databases
- Implement **generic composition tools** that take genre as a parameter
- Create style-appropriate rhythm and instrumentation tools
- Enable AI agents to create authentic genre-based music
- **Maximize reusability and minimize API surface area**

## Design Philosophy: Generic Tools + Genre Data

### ✅ **APPROACH**: Generic Functions + Genre Parameter
```python
create_progression(genre="blues")
create_progression(genre="rock")
create_beat(genre="hip_hop")
create_arrangement(genre="bluegrass")
```

## Revised Tool Set (12 Generic Tools)

### **Genre Discovery Tools**
```python
@mcp.tool()
def list_available_genres() -> dict:
    """List all available genres with categories and descriptions."""

@mcp.tool()
def get_genre_characteristics(genre: str) -> dict:
    """Get comprehensive characteristics for any musical genre."""

@mcp.tool() 
def compare_genres(genre1: str, genre2: str) -> dict:
    """Compare characteristics between two genres."""
```

### **Generic Composition Tools**
```python
@mcp.tool()
def create_progression(genre: str, key: str, variation: str = "standard", 
                      bars: int = None) -> dict:
    """Create authentic chord progression for any genre."""

@mcp.tool()
def create_melody(genre: str, key: str, progression: dict, 
                 style: str = "typical") -> dict:
    """Generate authentic melody for any genre."""

@mcp.tool()
def create_beat(genre: str, tempo: int, complexity: str = "medium",
               variation: str = "standard") -> dict:
    """Create authentic drum patterns for any genre."""

@mcp.tool()
def create_bass_line(genre: str, progression: dict, style: str = "typical") -> dict:
    """Generate authentic bass lines for any genre."""

@mcp.tool()
def create_arrangement(genre: str, song_structure: dict, 
                      instrumentation: str = "standard") -> dict:
    """Create full band arrangement for any genre."""
```

### **Style Application Tools**
```python
@mcp.tool()
def apply_genre_feel(midi_file_id: str, genre: str, 
                    intensity: float = 0.8) -> dict:
    """Apply genre-specific timing, articulation, and feel to existing MIDI."""

@mcp.tool()
def create_genre_template(genre: str, song_type: str, key: str, 
                         tempo: int) -> dict:
    """Create complete song template for any genre."""

@mcp.tool()
def create_fusion_style(primary_genre: str, secondary_genre: str,
                       balance: float = 0.5) -> dict:
    """Create fusion of two genres with adjustable balance."""

@mcp.tool()
def validate_genre_authenticity(midi_file_id: str, target_genre: str) -> dict:
    """Analyze how well music matches genre characteristics."""
```

## Genre Knowledge Architecture

### **Hierarchical Genre System**
```json
{
  "genres": {
    "blues": {
      "parent": null,
      "subgenres": ["chicago_blues", "delta_blues", "electric_blues"],
      "related": ["rock", "jazz", "r_and_b"]
    },
    "rock": {
      "parent": null, 
      "subgenres": ["classic_rock", "hard_rock", "punk", "metal"],
      "related": ["blues", "pop", "country"]
    },
    "hip_hop": {
      "parent": null,
      "subgenres": ["boom_bap", "trap", "lo_fi", "drill", "old_school"],
      "related": ["r_and_b", "funk", "jazz"]
    },
    "trance": {
      "parent": "electronic",
      "subgenres": ["progressive_trance", "uplifting_trance", "psytrance", "tech_trance"],
      "related": ["house", "techno", "ambient"]
    },
    "pop": {
      "parent": null,
      "subgenres": ["dance_pop", "indie_pop", "electropop", "synth_pop"],
      "related": ["rock", "r_and_b", "electronic"]
    },
    "ambient": {
      "parent": "electronic",
      "subgenres": ["dark_ambient", "drone", "new_age", "space_ambient"],
      "related": ["trance", "downtempo", "experimental"]
    },
    "k_pop": {
      "parent": "pop",
      "subgenres": ["k_pop_ballad", "k_pop_dance", "k_pop_rap", "k_pop_r&b"],
      "related": ["pop", "hip_hop", "r_and_b", "electronic"]
    }
  }
}
```

### **Generic Pattern Structure**
```json
{
  "blues": {
    "progressions": {
      "standard": {
        "pattern": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"],
        "bars": 12,
        "variations": ["quick_change", "minor_blues", "jazz_blues"]
      }
    },
    "rhythms": {
      "standard": {
        "feel": "shuffle",
        "emphasis": [1, 3],
        "subdivision": "triplet"
      }
    },
    "scales": ["blues_scale", "minor_pentatonic", "mixolydian"],
    "instrumentation": {
      "essential": ["guitar", "vocals"],
      "typical": ["harmonica", "bass", "drums"],
      "optional": ["piano", "saxophone"]
    }
  }
}
```

## Implementation Plan

### **Day 1: Generic Architecture + Genre Data System**
```python
# Core genre manager
class GenreManager:
    def get_genre_data(self, genre: str) -> dict
    def get_progression_patterns(self, genre: str) -> dict
    def get_rhythm_patterns(self, genre: str) -> dict
    def get_instrumentation(self, genre: str) -> dict

# Generic composition engine
class GenericComposer:
    def create_progression(self, genre: str, **kwargs) -> dict
    def create_melody(self, genre: str, **kwargs) -> dict
    def create_arrangement(self, genre: str, **kwargs) -> dict
```

### **Day 2-4: Genre Data Implementation**
- **Load comprehensive genre databases** (blues, rock, hip_hop, bluegrass, jazz, country, trance, pop, ambient, k_pop)
- **Pattern libraries**: Progressions, rhythms, melodies for each genre
- **Instrumentation templates**: Standard lineups for each style
- **Style characteristics**: Tempo, feel, harmony, structure

### **Day 5: Integration + Advanced Features**
- **Genre fusion engine**: Blend characteristics from multiple genres
- **Authenticity validation**: Score how well music matches genre
- **Style evolution**: Modern vs traditional variations

## Revised File Structure
```
midi-mcp/
├── src/midi_mcp/
│   ├── genres/
│   │   ├── __init__.py
│   │   ├── genre_manager.py      # Generic genre management
│   │   ├── composition_engine.py # Generic composition tools
│   │   ├── pattern_library.py    # Pattern storage and retrieval
│   │   ├── fusion_engine.py      # Genre fusion capabilities
│   │   └── validator.py          # Authenticity validation
│   └── tools/
│       └── genre_tools.py        # Generic MCP tools
├── data/
│   ├── genres/
│   │   ├── genre_hierarchy.json  # Genre relationships
│   │   ├── blues.json           # Blues patterns and characteristics
│   │   ├── rock.json            # Rock patterns and characteristics
│   │   ├── hip_hop.json         # Hip hop patterns and characteristics
│   │   ├── bluegrass.json       # Bluegrass patterns and characteristics
│   │   ├── trance.json          # Trance patterns and characteristics
│   │   ├── pop.json             # Pop patterns and characteristics
│   │   ├── ambient.json         # Ambient patterns and characteristics
│   │   ├── k_pop.json           # K-pop patterns and characteristics
│   │   └── fusion_rules.json    # Genre fusion compatibility
│   └── patterns/
│       ├── progressions/        # Chord progression libraries
│       ├── rhythms/            # Rhythm pattern libraries
│       ├── melodies/           # Melodic phrase libraries
│       └── arrangements/       # Instrumentation templates
```

## Example Usage

### **Example Usage:**
```python
# Generic functions handle all genres with clean parameters
create_progression(genre="blues", key="E", variation="quick_change")
create_progression(genre="rock", key="A", variation="classic_rock")  
create_beat(genre="hip_hop", tempo=90, variation="boom_bap")
create_beat(genre="trance", tempo=130, variation="progressive")
create_melody(genre="pop", key="C", style="catchy")
create_melody(genre="ambient", key="Am", style="ethereal")
create_arrangement(genre="bluegrass", song_structure=data)
create_arrangement(genre="k_pop", song_structure=data, instrumentation="full")
```

## Benefits of This Approach

### ✅ **Scalability**
- Adding new genres requires only **data**, not new functions
- API remains clean and consistent
- Easy to add subgenres and variations

### ✅ **Maintainability**  
- Single codebase handles all genres
- Consistent parameter patterns
- Centralized genre logic

### ✅ **Flexibility**
- Easy to add new genre characteristics
- Simple to implement genre fusion
- Parameter validation in one place

### ✅ **User Experience**
- Consistent interface across all genres
- Easy to discover available genres
- Natural parameter progression

## HIL Testing Scenarios (Revised)

### Scenario 1: Genre Discovery
```
Human: "What genres are available?"
AI: Uses list_available_genres() → Returns blues, rock, hip_hop, bluegrass, jazz, trance, pop, ambient, k_pop, etc.
```

### Scenario 2: Generic Blues Creation
```
Human: "Create a 12-bar blues in E"
AI: Uses create_progression(genre="blues", key="E", bars=12)
Result: Authentic E7-A7-B7 blues progression
```

### Scenario 3: Rock Arrangement
```
Human: "Create a rock arrangement for this melody"
AI: Uses create_arrangement(genre="rock", song_structure=melody_data)
Result: Full band arrangement with guitar, bass, drums
```

### Scenario 4: Genre Fusion
```
Human: "Combine blues and hip hop"
AI: Uses create_fusion_style(primary_genre="blues", secondary_genre="hip_hop")
Result: Blues harmony with hip hop beats and production
```

### Scenario 5: Style Application
```
Human: "Make this MIDI file sound more like jazz"
AI: Uses apply_genre_feel(midi_file_id="123", genre="jazz")
Result: Swing timing, jazz chord voicings, appropriate articulation
```

## Success Criteria
- [ ] Single generic function handles multiple genres correctly
- [ ] New genres can be added via data files only
- [ ] Genre characteristics are accurately represented
- [ ] Fusion between genres produces musical results
- [ ] API remains clean with 12 total tools instead of 40+
- [ ] All original Phase 4 functionality preserved
- [ ] Performance scales well with new genres

## Next Phase Preparation
This generic architecture sets up perfectly for Phase 5 (Advanced Composition) by providing:
- **Scalable pattern library** for advanced composition
- **Generic tools** that can be enhanced with AI generation
- **Clean architecture** for adding specialized agents
- **Rich genre knowledge** for style-appropriate composition

## Migration Strategy
The revised approach reduces complexity while increasing capability:
- **From 40+ genre-specific tools** → **12 generic tools**
- **From hardcoded genre logic** → **Data-driven genre system**
- **From scattered implementations** → **Unified composition engine**
- **From difficult maintenance** → **Easy extensibility**

This approach transforms Phase 4 from a maintenance nightmare into an elegant, scalable system that can grow with new genres and styles while maintaining a clean, intuitive API.