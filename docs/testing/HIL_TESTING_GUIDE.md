# Human-in-the-Loop (HIL) Testing Guide

## Overview
This guide establishes comprehensive testing procedures for validating the MIDI MCP server with AI agents at every development phase. HIL testing ensures that AI agents can effectively use the MCP tools to create musical content.

## Testing Philosophy
- **Real-World Validation**: Test with actual AI agents, not just unit tests
- **Musical Quality**: Evaluate both technical functionality and musical merit
- **User Experience**: Ensure AI interactions are intuitive and productive
- **Incremental Validation**: Test each capability as it's developed
- **Cross-Platform Testing**: Verify compatibility across different systems

## Testing Environment Setup

### Hardware Requirements
```
Minimum Setup:
- Computer with MIDI output capability
- Software synthesizer or DAW
- Audio interface (built-in audio acceptable)

Recommended Setup:
- Dedicated audio interface
- External MIDI synthesizer or high-quality software synths
- Studio monitors or quality headphones
- MIDI controller for additional testing
```

### Software Requirements
```
Core Requirements:
- Python 3.10+ with MCP SDK
- MIDI routing software:
  - macOS: Built-in IAC Driver
  - Windows: loopMIDI or MIDI-OX
  - Linux: ALSA MIDI or JACK
- AI Agent Platform:
  - GitHub Copilot with VS Code
  - Claude Desktop
  - Custom MCP client

Music Software (choose one or more):
- Free: GarageBand, Reaper (60-day trial), LMMS
- Paid: Logic Pro, Ableton Live, FL Studio, Pro Tools
```

### MIDI Routing Configuration

#### macOS Setup
```bash
# Enable IAC Driver
1. Open Audio MIDI Setup
2. Go to Window → Show MIDI Studio
3. Double-click "IAC Driver"
4. Check "Device is online"
5. Add ports as needed (typically 1 port sufficient)
```

#### Windows Setup
```
1. Download and install loopMIDI
2. Create a virtual MIDI port named "MCP-MIDI"
3. Configure DAW to receive from "MCP-MIDI" port
4. Test connection with MIDI monitor
```

#### Linux Setup
```bash
# Install ALSA utils
sudo apt-get install alsa-utils

# Create virtual MIDI port
sudo modprobe snd-virmidi

# List available MIDI ports
aplaymidi -l
```

## AI Agent Configuration

### GitHub Copilot + VS Code Setup
```json
// In VS Code settings.json
{
  "mcp.servers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/midi-mcp/src/server.py"],
      "env": {
        "MIDI_OUTPUT_PORT": "0",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Claude Desktop Setup
```json
// In claude_desktop_config.json
{
  "mcpServers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/Users/username/dev/midi-mcp/src/server.py"],
      "env": {
        "MIDI_OUTPUT_PORT": "0"
      }
    }
  }
}
```

## Phase-Specific Testing Protocols

### Phase 1: Foundation Testing
**Test Duration**: 30 minutes per test cycle
**Frequency**: After each major change

#### Test 1.1: Basic Connectivity
```
Setup: Start MCP server, connect AI agent
Prompt: "List available MIDI tools"
Expected: AI lists all implemented MIDI tools
Validation: All tools appear in response
```

#### Test 1.2: Single Note Playback
```
Setup: Connect to MIDI synthesizer
Prompt: "Play middle C for 2 seconds"
Expected: AI uses play_note(60, 64, 2.0)
Validation: Hear middle C note for correct duration
```

#### Test 1.3: Scale Playback
```
Setup: Same as above
Prompt: "Play a C major scale ascending"
Expected: AI plays notes C-D-E-F-G-A-B-C in sequence
Validation: Hear correct scale with proper timing
```

#### Test 1.4: Device Management
```
Setup: Multiple MIDI devices available
Prompt: "List MIDI devices and play a test note on device 1"
Expected: AI lists devices, switches, plays note
Validation: Note plays on specified device
```

### Phase 2: Core MIDI Testing
**Test Duration**: 45 minutes per test cycle
**Frequency**: Daily during development

#### Test 2.1: File Creation
```
Setup: Clean workspace
Prompt: "Create a new MIDI file called 'test_song' with piano and drums"
Expected: AI creates file with 2 tracks, proper programs
Validation: File loads in DAW with correct track setup
```

#### Test 2.2: File Loading and Analysis
```
Setup: Known MIDI file available
Prompt: "Load 'example.mid' and tell me about its structure"
Expected: AI loads file, provides detailed analysis
Validation: Analysis matches known file properties
```

#### Test 2.3: Complex Editing
```
Setup: MIDI file with melody
Prompt: "Transpose the melody track up 5 semitones and quantize to 16th notes"
Expected: AI identifies melody, applies transformations
Validation: Resulting file has correct changes
```

### Phase 3: Music Theory Testing
**Test Duration**: 60 minutes per test cycle
**Frequency**: After each theory module completion

#### Test 3.1: Scale Generation
```
Setup: Music theory reference available
Prompt: "Generate an F# harmonic minor scale and explain its characteristics"
Expected: AI creates correct scale, explains intervals
Validation: Scale matches theoretical expectations
```

#### Test 3.2: Chord Progression Creation
```
Setup: Music theory knowledge for validation
Prompt: "Create a ii-V-I progression in Bb major with jazz voicings"
Expected: AI creates Cm7-F7-BbMaj7 with proper voicings
Validation: Progression sounds harmonically correct
```

#### Test 3.3: Harmonic Analysis
```
Setup: Known chord progression in MIDI file
Prompt: "Analyze the harmony in this chord progression"
Expected: AI identifies chords, key, harmonic function
Validation: Analysis matches music theory expectations
```

## HIL Testing Scenarios by Musical Context

### Scenario Category 1: Basic Music Creation
**Target**: Non-musician users with AI assistance

#### Scenario 1A: Simple Melody
```
Human: "I want to create a happy melody in C major"
AI Expected Actions:
1. Generate C major scale
2. Create melodic phrase using scale tones
3. Apply appropriate rhythm and timing
4. Play result for human feedback

Success Criteria:
- Melody uses only C major scale tones
- Rhythm is musically logical
- Overall feel matches "happy" descriptor
- Human finds result acceptable
```

#### Scenario 1B: Basic Chord Progression
```
Human: "Create a simple chord progression that sounds like a pop song"
AI Expected Actions:
1. Select appropriate pop progression (vi-IV-I-V or similar)
2. Choose suitable key and voicing
3. Apply typical pop rhythm
4. Generate MIDI file

Success Criteria:
- Progression follows pop conventions
- Chord voicings are appropriate
- Rhythm matches genre expectations
- Result is recognizable as pop style
```

### Scenario Category 2: Music Theory Application
**Target**: Musicians seeking theory assistance

#### Scenario 2A: Advanced Harmony
```
Human: "Create a jazz progression using secondary dominants"
AI Expected Actions:
1. Select base progression (ii-V-I)
2. Add appropriate secondary dominants
3. Voice chords with jazz conventions
4. Explain harmonic analysis

Success Criteria:
- Secondary dominants are correctly applied
- Voice leading follows jazz practices
- Analysis correctly identifies harmonic functions
- Musician finds progression sophisticated but playable
```

#### Scenario 2B: Modulation
```
Human: "Start in G major and modulate to E minor using a pivot chord"
AI Expected Actions:
1. Create progression in G major
2. Identify suitable pivot chord (Em or Am)
3. Create smooth modulation
4. Establish E minor key clearly

Success Criteria:
- Modulation sounds smooth and logical
- Pivot chord functions properly in both keys
- New key is clearly established
- No awkward voice leading
```

### Scenario Category 3: Genre-Specific Creation
**Target**: Users wanting specific musical styles

#### Scenario 3A: Blues Composition
```
Human: "Create a 12-bar blues in E with a traditional feel"
AI Expected Actions:
1. Use 12-bar blues form (I-I-I-I-IV-IV-I-I-V-IV-I-V)
2. Apply E7-A7-B7 chords with blues voicings
3. Add shuffle rhythm feel
4. Create appropriate bass line

Success Criteria:
- Form follows 12-bar blues exactly
- Chords are blues-appropriate (dominant 7ths)
- Rhythm has authentic shuffle feel
- Overall sound is recognizably blues
```

## Testing Data Collection

### Quantitative Metrics
```python
# Example metrics to track
test_metrics = {
    "response_time": "Time from prompt to first MIDI output",
    "accuracy": "Percentage of correct musical theory applications",
    "completeness": "Percentage of requested features implemented",
    "stability": "Crashes or errors per hour of testing",
    "compatibility": "Percentage of successful DAW imports"
}
```

### Qualitative Assessment
```
Musical Quality Rubric (1-5 scale):
- Harmonic Correctness: Are chord progressions theoretically sound?
- Rhythmic Quality: Do rhythms feel natural and musical?
- Melodic Flow: Do melodies have logical phrasing and direction?
- Genre Authenticity: Does output match genre expectations?
- Overall Musicality: Would a musician find this acceptable?
```

### User Experience Metrics
```
UX Assessment:
- Prompt Understanding: Does AI interpret requests correctly?
- Response Clarity: Are explanations clear and helpful?
- Error Handling: Does AI handle mistakes gracefully?
- Learning Curve: How quickly can users become productive?
- Workflow Integration: Does AI fit into natural creative process?
```

## Testing Documentation

### Test Session Report Template
```markdown
# HIL Test Session Report

## Session Info
- Date: [YYYY-MM-DD]
- Phase: [1-8]
- Tester: [Name]
- Duration: [X hours]
- AI Agent: [GitHub Copilot/Claude Desktop/Other]

## Environment
- OS: [macOS/Windows/Linux version]
- MIDI Software: [DAW/Synthesizer used]
- MIDI Routing: [Configuration]

## Tests Performed
### Test [Number]: [Name]
- **Prompt**: [Exact prompt given to AI]
- **Expected**: [Expected behavior]
- **Actual**: [What actually happened]
- **Result**: [Pass/Fail/Partial]
- **Notes**: [Additional observations]
- **Audio Recording**: [Link to recording if applicable]

## Summary
- **Total Tests**: [Number]
- **Passed**: [Number]
- **Failed**: [Number]
- **Overall Assessment**: [Success level]
- **Key Issues**: [Major problems found]
- **Recommendations**: [Suggested improvements]
```

## Automated Testing Integration

### Continuous Testing Framework
```python
# Example automated test that can run alongside HIL testing
def test_mcp_server_availability():
    """Verify MCP server responds to basic queries"""
    client = MCPClient()
    response = client.call_tool("list_midi_devices")
    assert response.status == "success"
    
def test_midi_output_timing():
    """Verify MIDI output timing accuracy"""
    start_time = time.time()
    client.call_tool("play_note", {"note": 60, "duration": 1.0})
    elapsed = time.time() - start_time
    assert 0.9 <= elapsed <= 1.1  # Allow 10% timing variance
```

## Troubleshooting Common Issues

### MIDI Connection Problems
```
Problem: No MIDI output
Diagnosis:
1. Check MIDI routing configuration
2. Verify synthesizer is receiving on correct channel
3. Test with known-good MIDI file
4. Check MCP server logs

Problem: Timing issues
Diagnosis:
1. Check system audio buffer settings
2. Verify MIDI clock synchronization
3. Test with different software synthesizers
4. Monitor CPU usage during playback
```

### AI Agent Issues
```
Problem: AI doesn't understand MIDI tools
Diagnosis:
1. Verify MCP server is running and accessible
2. Check tool definitions are properly exposed
3. Test tool discovery with direct MCP client
4. Review AI agent configuration

Problem: AI makes music theory errors
Diagnosis:
1. Check theory validation functions
2. Review knowledge base accuracy
3. Test with known correct examples
4. Verify rule engine logic
```

This HIL testing guide ensures that every component is validated with real AI agents in realistic musical scenarios. The comprehensive approach catches both technical issues and musical quality problems early in development.