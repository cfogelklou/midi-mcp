# Phase 1: Foundation Implementation

## Overview
Establish the basic MCP server framework with minimal MIDI functionality. This phase creates the foundation that all subsequent phases will build upon.

## Goals
- Set up working MCP server with Python SDK
- Implement basic MIDI note playing
- Establish HIL testing workflow
- Create project structure and development environment

## Duration: Week 1 (5 days)

## Prerequisites
- Python 3.10+ installed
- Basic understanding of MIDI concepts
- MIDI synthesizer or DAW available for testing
- GitHub Copilot or Claude Desktop access

## Day-by-Day Implementation

### Day 1: Environment Setup
**Morning (2-3 hours):**
```bash
# Project initialization
mkdir midi-mcp
cd midi-mcp
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install core dependencies
pip install mcp[cli] mido python-rtmidi pydantic
```

**Afternoon (3-4 hours):**
- Set up project structure
- Create basic MCP server skeleton
- Implement server initialization
- Test MCP server connectivity

**Deliverable**: Working MCP server that can be discovered by clients

**HIL Test**: 
```json
// In claude_desktop_config.json
{
  "mcpServers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/path/to/midi-mcp/src/server.py"]
    }
  }
}
```

### Day 2: Basic MIDI Infrastructure
**Morning (3-4 hours):**
- Implement MIDI port discovery and connection
- Create basic MIDI message sending
- Add error handling and logging
- Test MIDI output to synthesizer

**Afternoon (2-3 hours):**
- Implement simple note-on/note-off functionality
- Add velocity and timing control
- Create basic MIDI utilities
- Test with physical MIDI device or software synth

**Deliverable**: MCP tools that can send MIDI notes to external devices

**Code Example**:
```python
@mcp.tool()
def play_note(note: int, velocity: int = 64, duration: float = 1.0, channel: int = 0) -> dict:
    """
    Play a single MIDI note.
    
    Args:
        note: MIDI note number (0-127, middle C = 60)
        velocity: Note velocity (0-127, 64 = medium)
        duration: Note duration in seconds
        channel: MIDI channel (0-15)
    
    Returns:
        Status dictionary with success/failure information
    """
```

**HIL Test**: Ask GitHub Copilot to "Play middle C for 2 seconds"

### Day 3: Note Sequences and Basic Timing
**Morning (3-4 hours):**
- Implement note sequence playing
- Add timing and tempo control
- Create chord playing functionality
- Add real-time MIDI monitoring

**Afternoon (2-3 hours):**
- Implement basic scale playing
- Add arpeggiation functionality
- Create simple melody playback
- Test timing accuracy and synchronization

**Deliverable**: Tools for playing sequences of notes with accurate timing

**Code Example**:
```python
@mcp.tool()
def play_sequence(notes: List[int], durations: List[float], velocities: List[int] = None, 
                 tempo: float = 120.0, channel: int = 0) -> dict:
    """
    Play a sequence of MIDI notes with specified timing.
    
    Args:
        notes: List of MIDI note numbers
        durations: List of note durations in beats
        velocities: List of velocities (defaults to 64 for all notes)
        tempo: Tempo in BPM
        channel: MIDI channel
    """

@mcp.tool()  
def play_chord(notes: List[int], velocity: int = 64, duration: float = 1.0, 
               channel: int = 0) -> dict:
    """
    Play multiple notes simultaneously as a chord.
    """
```

**HIL Test**: Ask GitHub Copilot to "Play a C major scale followed by a C major chord"

### Day 4: MCP Integration and Error Handling  
**Morning (3-4 hours):**
- Improve MCP tool definitions and documentation
- Add comprehensive error handling
- Implement proper resource cleanup
- Add logging and debugging tools

**Afternoon (2-3 hours):**
- Create tool discovery and help system
- Add MIDI device management
- Implement graceful shutdown procedures
- Test edge cases and error conditions

**Deliverable**: Robust MCP server with proper error handling and resource management

**Code Example**:
```python
@mcp.tool()
def list_midi_devices() -> dict:
    """
    List available MIDI output devices.
    
    Returns:
        Dictionary containing available MIDI devices and their IDs
    """

@mcp.tool()
def set_midi_device(device_id: int) -> dict:
    """
    Set the active MIDI output device.
    
    Args:
        device_id: ID of the MIDI device to use
    """

@mcp.tool()
def get_server_status() -> dict:
    """
    Get current server status and configuration.
    
    Returns:
        Server status including active device, connections, etc.
    """
```

**HIL Test**: Ask GitHub Copilot to "List available MIDI devices and play a test note on device 0"

### Day 5: Testing and Documentation
**Morning (2-3 hours):**
- Create comprehensive test suite
- Write unit tests for all tools
- Add integration tests
- Test with multiple MIDI devices

**Afternoon (3-4 hours):**
- Write complete documentation
- Create usage examples
- Record demonstration videos
- Prepare for Phase 2

**Deliverable**: Fully tested and documented Phase 1 system

## File Structure After Phase 1
```
midi-mcp/
├── src/
│   ├── server.py              # Main MCP server
│   ├── midi/
│   │   ├── __init__.py
│   │   ├── connection.py      # MIDI device connection
│   │   ├── player.py          # MIDI playback functionality
│   │   └── utils.py           # MIDI utility functions
│   └── models/
│       ├── __init__.py
│       └── midi_models.py     # Pydantic models
├── tests/
│   ├── test_server.py
│   ├── test_midi.py
│   └── test_integration.py
├── docs/
│   └── [documentation files]
├── examples/
│   ├── basic_usage.py
│   └── copilot_examples.md
├── requirements.txt
└── pyproject.toml
```

## HIL Testing Scenarios

### Scenario 1: Basic Note Playing
```
Human: "Ask the AI to play middle C"
Expected: AI uses play_note tool with note=60
Result: Single note plays through MIDI synth
```

### Scenario 2: Scale Playing  
```
Human: "Ask the AI to play a C major scale"
Expected: AI uses play_sequence with appropriate notes
Result: Eight-note scale plays in sequence
```

### Scenario 3: Chord Playing
```
Human: "Ask the AI to play a C major chord"  
Expected: AI uses play_chord with notes=[60,64,67]
Result: Three notes play simultaneously
```

### Scenario 4: Device Management
```
Human: "Ask the AI to list MIDI devices and switch to a different one"
Expected: AI lists devices, then switches using set_midi_device
Result: Different synthesizer receives subsequent MIDI data
```

## Success Criteria
- [ ] MCP server starts and accepts connections
- [ ] AI agents can discover and use all MIDI tools
- [ ] Notes play correctly through MIDI synthesizers
- [ ] Timing is accurate (no noticeable delay or jitter)
- [ ] Error handling works properly (device disconnection, etc.)
- [ ] All HIL test scenarios pass
- [ ] Code is well-documented and tested

## Common Issues and Solutions

### MIDI Device Not Found
- **Problem**: MCP server can't find MIDI devices
- **Solution**: Check MIDI routing software, verify device permissions
- **Code**: Add device discovery debugging in `list_midi_devices()`

### Timing Issues
- **Problem**: Notes don't play with accurate timing
- **Solution**: Use proper threading and timing mechanisms
- **Code**: Implement precise timing with `threading.Timer` or `asyncio`

### MCP Connection Issues
- **Problem**: GitHub Copilot can't connect to server
- **Solution**: Check config file path, server startup logs
- **Code**: Add connection status logging

## Next Phase Preparation
- Verify all Phase 1 functionality works reliably
- Ensure development environment is stable  
- Confirm HIL testing workflow is established
- Review Phase 2 requirements (`02_CORE_MIDI.md`)

Phase 1 establishes the foundation for all subsequent development. The emphasis is on creating a solid, testable base rather than complex functionality. Success in this phase is measured by reliable basic MIDI playback and smooth AI agent interaction.