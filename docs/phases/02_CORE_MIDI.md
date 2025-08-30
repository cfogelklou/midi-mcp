# Phase 2: Core MIDI I/O and Playback

## Overview
This phase focuses on the core capabilities of creating, saving, loading, and playing MIDI files. The goal is to enable AI agents to work with MIDI data and hear their creations in real-time. This phase transforms the basic note-playing system into a foundational MIDI production environment.

## Goals
- Implement complete MIDI file I/O operations (create, save, load)
- Add multi-track MIDI composition tools
- Dynamically play MIDI files in real-time through an attached MIDI device
- Establish a file-based workflow for AI agents
- **Set up a CI/CD pipeline with GitHub Actions for automated testing.**

## Duration: Week 2 (3 days)

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

### Day 2: MIDI File Loading and Real-time Playback
**Morning (3-4 hours):**
- Implement MIDI file loading from disk
- Create MIDI file analysis tools (track info, note count, duration)
- Implement real-time playback of a loaded MIDI file through a connected device

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
def play_midi_file(midi_file_id: str, device_id: str) -> dict:
    """
    Play a loaded MIDI file in real-time through a specified MIDI device.
    
    Args:
        midi_file_id: ID of the MIDI file to play
        device_id: ID of the connected MIDI output device
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
```

**Afternoon (2-3 hours):**
- Test with various MIDI file formats
- Add support for different MIDI file types (Type 0, 1, 2)
- Test playback synchronization and timing
- Test analysis accuracy with known files

**HIL Test**: "Ask AI to load a MIDI file, analyze its structure, and then play it."

### Day 3: Integration and File Management
**Morning (3-4 hours):**
- Implement MIDI file session management
- Create file organization and tagging system
- Add batch file operations for loading and saving

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
def batch_process_files(file_ids: List[str], operations: List[dict]) -> dict:
    """
    Apply a series of operations to multiple files.
    
    Args:
        file_ids: List of MIDI file IDs to process
        operations: List of operations to apply in order (e.g., save, analyze)
    """
```

**Afternoon (2-3 hours):**
- Complete testing of all MIDI file I/O and playback operations
- Create comprehensive examples and documentation
- Prepare integration tests with Phase 1 functionality
- Set up for Phase 3 development

**HIL Test**: "Ask AI to create a workflow that loads multiple MIDI files, analyzes them, and saves them to an organized directory."

## File Structure After Phase 2
```
midi-mcp/
├── src/
│   ├── server.py
│   ├── midi/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── player.py           # Real-time MIDI playback
│   │   ├── file_ops.py         # MIDI file I/O operations
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
│   ├── test_player.py
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
Expected: AI creates file, adds three tracks with appropriate programs, and saves it.
Result: Playable MIDI file with proper track structure is created on disk.
```

### Scenario 2: File Analysis and Playback
```  
Human: "Load this MIDI file, analyze it, and then play it for me."
Expected: AI loads, analyzes, and plays the file through the connected MIDI device.
Result: The MIDI file is heard playing in real-time.
```

## CI/CD and Automated Testing
To ensure code quality and stability, a Continuous Integration (CI) pipeline will be established using GitHub Actions. This will automate the testing process for every commit and pull request.

### Testing Strategy
The CI pipeline will execute the following tests:

1.  **Unit & Core Logic Tests:** These tests run on every commit and validate the fundamental building blocks of the server without requiring special environments.
    *   **Server Initialization:** Verifies that the MCP server and its configurations start correctly (`tests/test_server_basic.py`).
    *   **MIDI File Operations:** Ensures that creating, saving, loading, and analyzing MIDI files works as expected (`test_phase_2.py`).

2.  **System Tests with Virtual MIDI (Future Step):** A separate job will be configured to handle tests requiring MIDI I/O.
    *   **Virtual MIDI Environment:** The test runner will use `snd-virmidi` (ALSA) or a software synthesizer like FluidSynth to simulate MIDI devices.
    *   **Device Discovery & I/O:** Tests like `test_device_discovery.py` will be run in this environment to validate real-time MIDI messaging.

## Success Criteria
- [ ] Complete MIDI file I/O functionality (create, save, load) works reliably.
- [ ] Real-time playback of MIDI files is accurate and synchronized.
- [ ] File management handles complex workflows smoothly.
- [ ] Performance is acceptable for typical file sizes (< 2MB).
- [ ] AI agents can chain operations logically.
- [ ] All HIL test scenarios pass consistently.
- [ ] Files are compatible with major DAWs (Logic, Pro Tools, Ableton).
- [ ] The CI pipeline passes for all unit and core logic tests.

## Performance Considerations
- Load times under 1 second for files up to 1MB
- Real-time playback should have low latency.
- Memory usage scales linearly with file size.
- Concurrent file operations supported.

## Integration Notes
- All Phase 1 functionality remains available.
- Real-time playback works with loaded MIDI files.
- File operations can be combined with live performance.
- Session state persists across server restarts.

## Next Phase Preparation
- Verify all file operations and playback work correctly.
- Test integration with Phase 1 real-time capabilities.
- Confirm compatibility with various MIDI file sources.
- Review music theory requirements for Phase 3.

This updated Phase 2 focuses on the core of MIDI creation and playback, setting a strong foundation for the more advanced composition and music theory phases to come.