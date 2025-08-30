# Phase 2: Core MIDI Operations Implementation

## Overview
Build comprehensive MIDI file creation, manipulation, and management capabilities. This phase transforms the basic note-playing system into a full MIDI production environment.

## Goals
- Implement complete MIDI file I/O operations
- Add multi-track MIDI composition tools
- Create MIDI editing and manipulation functions
- Establish file-based workflow for AI agents

## Duration: Week 2 (5 days)

## Prerequisites
- Phase 1 completed and tested
- Working MCP server with basic MIDI functionality
- Understanding of MIDI file format and structure

## Day-by-Day Implementation

### Day 1: MIDI File Creation and Basic I/O
**Morning (3-4 hours):**
- Implement MIDI file creation from scratch
- Add track management (create, add, remove tracks)
- Create basic MIDI file saving functionality
- Add metadata handling (tempo, time signature, key signature)

**Code Framework**:
```python
@mcp.tool()
def create_midi_file(title: str = "Untitled", tempo: int = 120, 
                    time_signature: Tuple[int, int] = (4, 4), 
                    key_signature: str = "C") -> dict:
    """
    Create a new MIDI file with basic metadata.
    
    Args:
        title: Song title for metadata
        tempo: Tempo in BPM (default 120)
        time_signature: Time signature as (numerator, denominator)  
        key_signature: Key signature (C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F)
    
    Returns:
        MIDI file ID and basic information
    """

@mcp.tool()
def add_track(midi_file_id: str, track_name: str, channel: int = 0, 
              program: int = 0) -> dict:
    """
    Add a new track to an existing MIDI file.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_name: Name for the track
        channel: MIDI channel (0-15)
        program: MIDI program number (instrument, 0-127)
    """

@mcp.tool()
def save_midi_file(midi_file_id: str, filename: str) -> dict:
    """
    Save MIDI file to disk.
    
    Args:
        midi_file_id: ID of the MIDI file to save
        filename: Output filename (should end in .mid or .midi)
    """
```

**Afternoon (2-3 hours):**
- Test MIDI file creation with multiple tracks
- Verify file format compatibility with DAWs
- Add basic validation and error checking
- Create simple multi-track example

**HIL Test**: "Ask AI to create a new MIDI file with piano and drum tracks, then save it"

### Day 2: MIDI File Loading and Analysis
**Morning (3-4 hours):**
- Implement MIDI file loading from disk
- Create MIDI file analysis tools (track info, note count, duration)
- Add MIDI file structure inspection
- Implement track extraction and isolation

**Code Framework**:
```python
@mcp.tool()
def load_midi_file(filename: str) -> dict:
    """
    Load a MIDI file from disk.
    
    Args:
        filename: Path to MIDI file
        
    Returns:
        MIDI file ID and basic analysis
    """

@mcp.tool()
def analyze_midi_file(midi_file_id: str) -> dict:
    """
    Analyze a loaded MIDI file.
    
    Returns:
        Comprehensive analysis including:
        - Number of tracks
        - Duration in seconds and beats
        - Tempo changes
        - Key signatures
        - Note range and density
        - Instrument list
    """

@mcp.tool()
def get_track_info(midi_file_id: str, track_number: int) -> dict:
    """
    Get detailed information about a specific track.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Track number to analyze
        
    Returns:
        Track details including notes, timing, program changes
    """
```

**Afternoon (2-3 hours):**
- Test with various MIDI file formats
- Add support for different MIDI file types (Type 0, 1, 2)
- Create track comparison and similarity tools
- Test analysis accuracy with known files

**HIL Test**: "Ask AI to load a MIDI file and analyze its structure"

### Day 3: MIDI Editing and Manipulation
**Morning (3-4 hours):**
- Implement note editing (add, remove, modify notes)
- Add timing manipulation (quantization, swing, tempo changes)
- Create velocity and dynamics editing
- Add track merging and splitting

**Code Framework**:
```python
@mcp.tool()
def add_note_to_track(midi_file_id: str, track_number: int, note: int,
                     start_time: float, duration: float, velocity: int = 64) -> dict:
    """
    Add a note to a specific track.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Target track number
        note: MIDI note number (0-127)
        start_time: Start time in beats
        duration: Note duration in beats
        velocity: Note velocity (0-127)
    """

@mcp.tool()
def quantize_track(midi_file_id: str, track_number: int, 
                  grid_size: float = 0.25) -> dict:
    """
    Quantize timing of notes in a track.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Track to quantize
        grid_size: Quantization grid in beats (0.25 = 16th notes)
    """

@mcp.tool()
def transpose_track(midi_file_id: str, track_number: int, 
                   semitones: int) -> dict:
    """
    Transpose all notes in a track by semitones.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Track to transpose
        semitones: Number of semitones to transpose (positive = up)
    """
```

**Afternoon (2-3 hours):**
- Add batch editing operations
- Implement undo/redo functionality for edits
- Create track copying and pasting
- Test editing operations thoroughly

**HIL Test**: "Ask AI to load a MIDI file, transpose the melody up an octave, and quantize the drums"

### Day 4: Advanced MIDI Operations
**Morning (3-4 hours):**
- Implement MIDI file merging and combining
- Add tempo and time signature modification
- Create advanced timing operations (groove templates, humanization)
- Add MIDI effect application (echo, delay, arpeggiation)

**Code Framework**:
```python
@mcp.tool()
def merge_midi_files(file_ids: List[str], output_filename: str) -> dict:
    """
    Merge multiple MIDI files into one.
    
    Args:
        file_ids: List of MIDI file IDs to merge
        output_filename: Name for the merged file
    """

@mcp.tool()
def apply_groove_template(midi_file_id: str, track_number: int,
                         groove_type: str = "swing", intensity: float = 0.5) -> dict:
    """
    Apply a groove template to a track.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Track to apply groove to
        groove_type: Type of groove (swing, shuffle, latin, etc.)
        intensity: Groove intensity (0.0-1.0)
    """

@mcp.tool()
def humanize_track(midi_file_id: str, track_number: int,
                  timing_variation: float = 0.05, 
                  velocity_variation: float = 0.1) -> dict:
    """
    Add human-like variations to perfect MIDI timing and velocity.
    
    Args:
        midi_file_id: ID of the MIDI file
        track_number: Track to humanize
        timing_variation: Amount of timing variation (0.0-1.0)
        velocity_variation: Amount of velocity variation (0.0-1.0)
    """
```

**Afternoon (2-3 hours):**
- Test advanced operations with complex MIDI files
- Add batch processing capabilities
- Create preset management for common operations
- Optimize performance for large MIDI files

**HIL Test**: "Ask AI to merge two MIDI files, apply swing groove to drums, and humanize the piano track"

### Day 5: Integration and File Management
**Morning (3-4 hours):**
- Implement MIDI file session management
- Add automatic backup and versioning
- Create file organization and tagging system
- Add batch file operations

**Code Framework**:
```python
@mcp.tool()
def list_midi_files() -> dict:
    """
    List all MIDI files in the current session.
    
    Returns:
        List of file IDs, names, and basic metadata
    """

@mcp.tool()
def create_file_backup(midi_file_id: str, backup_name: str = None) -> dict:
    """
    Create a backup copy of a MIDI file.
    
    Args:
        midi_file_id: ID of file to backup
        backup_name: Optional name for backup (auto-generated if None)
    """

@mcp.tool()
def batch_process_files(file_ids: List[str], operations: List[dict]) -> dict:
    """
    Apply a series of operations to multiple files.
    
    Args:
        file_ids: List of MIDI file IDs to process
        operations: List of operations to apply in order
    """
```

**Afternoon (2-3 hours):**
- Complete testing of all MIDI file operations
- Create comprehensive examples and documentation
- Prepare integration tests with Phase 1 functionality
- Set up for Phase 3 development

**HIL Test**: "Ask AI to create a workflow that loads multiple MIDI files, processes them differently, and saves organized results"

## File Structure After Phase 2
```
midi-mcp/
├── src/
│   ├── server.py
│   ├── midi/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── player.py
│   │   ├── file_ops.py         # MIDI file operations
│   │   ├── editor.py           # MIDI editing functions
│   │   ├── analyzer.py         # MIDI analysis tools
│   │   └── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── midi_models.py
│   │   └── file_models.py      # File-specific models
│   └── storage/
│       ├── __init__.py
│       └── session_manager.py  # File session management
├── tests/
│   ├── test_file_ops.py
│   ├── test_editor.py
│   ├── test_analyzer.py
│   └── test_sessions.py
├── sample_files/                # Test MIDI files
│   ├── basic_song.mid
│   ├── complex_arrangement.mid
│   └── various_formats/
└── [existing files]
```

## HIL Testing Scenarios

### Scenario 1: File Creation Workflow
```
Human: "Create a new MIDI file with piano, bass, and drum tracks"
Expected: AI creates file, adds three tracks with appropriate programs
Result: Playable MIDI file with proper track structure
```

### Scenario 2: File Analysis and Modification
```  
Human: "Load this MIDI file, analyze it, then transpose the melody up 5 semitones"
Expected: AI loads, analyzes, identifies melody track, transposes correctly
Result: Modified file plays with transposed melody
```

### Scenario 3: Complex File Operations
```
Human: "Merge these three MIDI files, quantize all tracks, and apply swing to drums"
Expected: AI performs all operations in logical order
Result: Merged file with quantized timing and swung drums
```

### Scenario 4: Batch Processing
```
Human: "Process all MIDI files in the folder: humanize timing and normalize velocities"
Expected: AI identifies files, applies operations consistently
Result: All files processed with subtle humanization
```

## Success Criteria
- [ ] Complete MIDI file I/O functionality works reliably
- [ ] All editing operations produce musically correct results
- [ ] File management handles complex workflows smoothly
- [ ] Performance is acceptable for typical file sizes (< 2MB)
- [ ] AI agents can chain operations logically
- [ ] All HIL test scenarios pass consistently
- [ ] Files are compatible with major DAWs (Logic, Pro Tools, Ableton)

## Performance Considerations
- Load times under 1 second for files up to 1MB
- Editing operations complete in real-time
- Memory usage scales linearly with file size
- Concurrent file operations supported

## Integration Notes
- All Phase 1 functionality remains available
- Real-time playback works with loaded MIDI files
- File operations can be combined with live performance
- Session state persists across server restarts

## Next Phase Preparation
- Verify all file operations work correctly
- Test integration with Phase 1 real-time capabilities  
- Confirm compatibility with various MIDI file sources
- Review music theory requirements for Phase 3

Phase 2 establishes professional-grade MIDI file handling capabilities. The focus shifts from basic playback to comprehensive composition and editing tools that enable sophisticated musical workflows.