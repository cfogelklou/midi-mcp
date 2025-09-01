# MIDI MCP Server

**AI-Powered Music Creation and Production System**

Transform AI agents into professional musicians and producers with comprehensive MIDI composition, music theory, genre knowledge, and audio production capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

## ✨ Key Features

### 🎵 **Complete Music Creation Suite**
- **Real-time MIDI Playback**: Direct connection to synthesizers and DAWs
- **Professional MIDI File Operations**: Create, edit, and manipulate multi-track compositions
- **Advanced Music Theory Engine**: Scales, chords, progressions, and harmonic analysis
- **Genre Intelligence**: Authentic music creation in Blues, Rock, Hip Hop, Bluegrass, and more

### 🤖 **AI Agent Specialization**
- **Composer Agent**: Creative vision and song structure expertise
- **Arranger Agent**: Orchestration and instrumental arrangement mastery  
- **Theory Assistant**: Music education and analytical guidance
- **Jam Session Agent**: Real-time improvisation and interactive music-making
- **Audio Engineer**: Professional mixing, mastering, and production

### 🎚️ **Professional Production** *(Phase 2 Complete)*
- **✅ MIDI File Operations**: Create, save, load, and analyze MIDI files
- **✅ Multi-track Composition**: Add tracks with instruments and channel assignments
- **✅ Real-time Playback**: Accurate timing and device synchronization
- **✅ Comprehensive Analysis**: Musical structure and content analysis
- **🔄 MIDI Humanization**: Transform mechanical sequences (Phase 3+)
- **🔄 Mixing & Mastering**: Professional audio processing (Future phases)
- **🔄 High-Quality Rendering**: Export studio-quality audio (Future phases)

## 🚀 Quick Start

### TL;DR - Install & Run
```bash
# 1. Setup
git clone https://github.com/your-org/midi-mcp.git
cd midi-mcp
python -m venv venv

# ⚠️ IMPORTANT: Always activate virtual environment before running commands
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# 2. Test MIDI device discovery
python test_device_discovery.py

# 3. Test Phase 2 features
python test_phase_2.py

# 4. Demo all MCP tools  
python demo_phase_2_mcp.py

# 5. Start server
python -m midi_mcp

# 6. Connect AI agent (Claude Desktop config):
# Add to ~/.config/claude-desktop/config.json:
{
  "mcpServers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/midi-mcp/venv/bin/python", "-m", "midi_mcp"]
    }
  }
}

# 7. Test with AI agent:
"Create a MIDI file with piano and bass tracks"
"List MIDI devices and play middle C"
```

### Full Setup
1. **Install Dependencies**: 
   ```bash
   cd midi-mcp
   python -m venv venv
   source venv/bin/activate  # Always activate first!
   pip install -r requirements.txt
   ```
2. **Test MIDI Setup**: `python test_device_discovery.py`
3. **Configure MIDI Output**: 
   - **macOS**: Enable IAC Driver in Audio MIDI Setup → "Create Multi-Output Device"
   - **Windows**: Install loopMIDI virtual MIDI driver
   - **Linux**: `sudo modprobe snd-virmidi`
4. **Connect AI Agent**: Add server path to your AI agent configuration (use full path to venv python)
5. **Verify**: Ask your AI agent to "discover MIDI devices and show backend status"

### Your First Composition
```python
# In your AI agent (GitHub Copilot, Claude Desktop, etc.):
"Create a MIDI file called 'My Song' with 120 BPM in the key of C"
"Add a piano track and a bass track to it"
"Save the file as 'my_first_song.mid'"
"Now analyze the file and show me the details"
```

## ️ MIDI Setup for Quality Playback

### **macOS Setup for Multi-Channel MIDI**

The MIDI MCP server sends different instruments on different MIDI channels, which requires proper setup for quality playback.

#### **FluidSynth Setup (Recommended)**
FluidSynth provides professional-grade multi-channel MIDI synthesis with excellent sound quality:

**Quick Setup**: Run the automated setup script:
```bash
./setup_fluidsynth.sh
```

**Manual Setup**:

1. **Install FluidSynth and SoundFont**:
   ```bash
   # Install FluidSynth via Homebrew
   brew install fluidsynth
   
   # Create soundfonts directory
   mkdir -p ~/soundfonts
   
   # Download GeneralUser GS SoundFont (high quality, 30MB)
   curl -L -o ~/soundfonts/GeneralUser_GS.sf2 \
     "https://musical-artifacts.com/artifacts/1176/GeneralUser_GS_v1.471.sf2"
   ```

2. **Launch FluidSynth**:
   ```bash
   # Basic launch with CoreAudio
   fluidsynth -a coreaudio -g 0.5 ~/soundfonts/GeneralUser_GS.sf2
   
   # Advanced multi-channel setup
   fluidsynth -a coreaudio -o audio.output-channels=32 \
     -o synth.audio-groups=16 -g 0.5 ~/soundfonts/GeneralUser_GS.sf2
   ```

3. **Test Setup**: With FluidSynth running, test the MIDI MCP server:
   ```bash
   # In another terminal
   python demo_phase_2_mcp.py
   # Then play: examples/mission-impossible.mid
   ```

#### **Audio MIDI Setup Configuration**

1. **Open Audio MIDI Setup**: Applications → Utilities → Audio MIDI Setup
2. **Enable IAC Driver**:
   - Double-click "IAC Driver"
   - Check "Device is online"
   - Set "Ports: 1" (or more if needed)
3. **Create Multi-Output Device** (if using multiple outputs):
   - Click "+" → "Create Multi-Output Device"
   - Check the boxes for your desired outputs

#### **⚠️ GarageBand Limitations**

**Important**: GarageBand has significant limitations for multi-channel MIDI playback:

- **Problem**: GarageBand listens to all MIDI channels simultaneously but only plays the instrument assigned to each track
- **Result**: All channels sound like the same instrument (usually piano)
- **Workaround Options**:
  1. **Use FluidSynth instead** (recommended - provides professional multi-timbral synthesis)
  2. **Manual GarageBand Setup**:
     - Create separate tracks for each MIDI channel (1-16)
     - Assign different instruments to each track
     - Set each track to listen to a specific MIDI channel
     - Note: This is time-consuming and not ideal for automatic playback

#### **Testing Your Setup**

1. **Run the test file**:
   ```bash
   python test_device_discovery.py
   ```

2. **Test with Mission Impossible**:
   ```bash
   python demo_phase_2_mcp.py
   # Then use: play examples/mission-impossible.mid
   ```

3. **Expected Results**:
   - **With FluidSynth**: Different instruments playing on different channels with rich, realistic sound
   - **With GarageBand**: All instruments sound the same (limitation - not recommended)

### **Windows Setup**

1. **Install loopMIDI**: https://www.tobias-erichsen.de/software/loopmidi.html
2. **Create Virtual MIDI Port**: Launch loopMIDI and create "MIDI MCP Port"
3. **Install Virtual Synthesizer**:
   - **VirtualMIDISynth**: https://coolsoft.altervista.org/en/virtualmidisynth
   - **FluidSynth Windows**: https://github.com/FluidSynth/fluidsynth/releases

### **Linux Setup**

1. **Install FluidSynth**:
   ```bash
   sudo apt install fluidsynth  # Ubuntu/Debian
   sudo pacman -S fluidsynth    # Arch Linux
   ```

2. **Enable Virtual MIDI**:
   ```bash
   sudo modprobe snd-virmidi
   ```

3. **Launch with ALSA**:
   ```bash
   fluidsynth -a alsa -g 0.5 path/to/soundfont.sf2
   ```

## 🎼 What You Can Create

### **For Musicians & Composers**
- Generate chord progressions in any genre
- Create complete song structures with verses, choruses, and bridges
- Develop melodies and harmonize them with sophisticated voice leading
- Transpose and arrange music for different instruments and ensembles

### **For Producers & Beatmakers**
- Generate authentic drum patterns for any genre
- Create harmonic foundations for sampling and production
- Apply professional mixing and mastering to MIDI compositions
- Export high-quality stems and final masters

### **For Educators & Students**
- Demonstrate music theory concepts with interactive examples
- Analyze existing compositions for harmonic and structural insights
- Generate practice exercises and ear training materials
- Explore different musical genres and their characteristics

### **For Developers & Researchers**
- Integrate AI music generation into applications
- Experiment with computational creativity and music AI
- Build educational music software with intelligent assistance
- Research human-AI collaboration in creative domains

## 🎯 Example Use Cases

### Composition Assistant
```
"I need a sad ballad in A minor. Create the basic structure with piano and strings."
→ AI generates complete song form with appropriate harmonies and arrangement
```

### Genre Explorer
```
"Show me what makes blues different from jazz harmonically."
→ AI creates examples demonstrating characteristic progressions of each genre
```

### Production Helper
```
"Take this MIDI piano track and make it sound like a real performance."
→ AI applies humanization, timing variations, and expressive dynamics
```

### Theory Tutor
```
"Explain secondary dominants and create an example in the key of F major."
→ AI provides educational explanation with practical musical demonstration
```
## Available Tools

The MIDI MCP Server provides a comprehensive suite of tools for AI agents to create, manipulate, and analyze music. The tools are organized by their implementation phase.

### Phase 1: Foundation

These tools provide the basic building blocks for MIDI interaction.

*   **`play_note(note: int, velocity: int = 64, duration: float = 1.0, channel: int = 0)`**
    *   **Description**: Plays a single MIDI note.
    *   **AI Agent Prompt**: "Play middle C for 2 seconds." (Note: 60, Velocity: 64, Duration: 2.0, Channel: 0)

*   **`play_sequence(notes: List[int], durations: List[float], velocities: List[int] = None, tempo: float = 120.0, channel: int = 0)`**
    *   **Description**: Plays a sequence of MIDI notes with specified timing.
    *   **AI Agent Prompt**: "Play the first few notes of 'Twinkle Twinkle Little Star'." (Notes: [60, 60, 67, 67, 69, 69, 67], Durations: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0], Tempo: 120.0, Channel: 0)

*   **`play_chord(notes: List[int], velocity: int = 64, duration: float = 1.0, channel: int = 0)`**
    *   **Description**: Plays multiple notes simultaneously as a chord.
    *   **AI Agent Prompt**: "Play a C major chord." (Notes: [60, 64, 67], Velocity: 64, Duration: 1.0, Channel: 0)

*   **`list_midi_devices()`**
    *   **Description**: Lists available MIDI output devices.
    *   **AI Agent Prompt**: "Show me the available MIDI devices."

*   **`set_midi_device(device_id: int)`**
    *   **Description**: Sets the active MIDI output device.
    *   **AI Agent Prompt**: "Set the MIDI output to device 0." (Device ID: 0)

*   **`get_server_status()`**
    *   **Description**: Gets the current server status and configuration.
    *   **AI Agent Prompt**: "What is the current status of the MIDI server?"

### Phase 2: Core MIDI I/O and Playback

These tools enable working with MIDI files.

*   **`create_midi_file(title: str = "Untitled", tempo: int = 120, time_signature: Tuple[int, int] = (4, 4), key_signature: str = "C")`**
    *   **Description**: Creates a new MIDI file with basic metadata.
    *   **AI Agent Prompt**: "Create a new MIDI file titled 'My Song' in the key of G major with a tempo of 130 BPM." (Title: "My Song", Tempo: 130, Time Signature: (4, 4), Key Signature: "G")

*   **`add_track(midi_file_id: str, track_name: str, channel: int = 0, program: int = 0)`**
    *   **Description**: Adds a new track to an existing MIDI file.
    *   **AI Agent Prompt**: "Add a piano track to the MIDI file." (MIDI File ID: [current_midi_file_id], Track Name: "Piano", Channel: 0, Program: 0)

*   **`save_midi_file(midi_file_id: str, filename: str)`**
    *   **Description**: Saves a MIDI file to disk.
    *   **AI Agent Prompt**: "Save the current MIDI file as 'my_song.mid'." (MIDI File ID: [current_midi_file_id], Filename: "my_song.mid")

*   **`load_midi_file(filename: str)`**
    *   **Description**: Loads a MIDI file from disk.
    *   **AI Agent Prompt**: "Load the MIDI file 'my_song.mid'." (Filename: "my_song.mid")

*   **`play_midi_file(midi_file_id: str, device_id: str)`**
    *   **Description**: Plays a loaded MIDI file in real-time through a specified MIDI device.
    *   **AI Agent Prompt**: "Play the loaded MIDI file." (MIDI File ID: [current_midi_file_id], Device ID: [current_device_id])

*   **`analyze_midi_file(midi_file_id: str)`**
    *   **Description**: Analyzes a loaded MIDI file.
    *   **AI Agent Prompt**: "Analyze the structure of the loaded MIDI file." (MIDI File ID: [current_midi_file_id])

*   **`list_midi_files()`**
    *   **Description**: Lists all MIDI files in the current session.
    *   **AI Agent Prompt**: "Show me all the MIDI files in the current session."

### Phase 3: Music Theory

These tools provide music theory intelligence.

*   **`get_scale_notes(root_note: str, scale_type: str, octave: int = 4)`**
    *   **Description**: Generates the notes for a specific scale.
    *   **AI Agent Prompt**: "What are the notes in a C minor scale?" (Root Note: "C", Scale Type: "minor", Octave: 4)

*   **`build_chord(root_note: str, chord_type: str, inversion: int = 0, voicing: str = "close")`**
    *   **Description**: Builds a chord with specified parameters.
    *   **AI Agent Prompt**: "Build a G dominant 7th chord in first inversion." (Root Note: "G", Chord Type: "dom7", Inversion: 1, Voicing: "close")

*   **`create_chord_progression(key: str, progression: List[str], duration_per_chord: float = 1.0)`**
    *   **Description**: Creates a chord progression in a specific key.
    *   **AI Agent Prompt**: "Create a I-V-vi-IV chord progression in the key of C major." (Key: "C major", Progression: ["I", "V", "vi", "IV"], Duration per Chord: 1.0)

*   **`detect_key(midi_file_id: str, track_number: int = None)`**
    *   **Description**: Detects the key(s) of a MIDI file or track.
    *   **AI Agent Prompt**: "What is the key of the loaded MIDI file?" (MIDI File ID: [current_midi_file_id])

### Phase 4: Genre Knowledge

These tools enable the creation of music in specific genres.

*   **`list_available_genres()`**
    *   **Description**: Lists all available genres with categories and descriptions.
    *   **AI Agent Prompt**: "What music genres do you know?"

*   **`get_genre_characteristics(genre: str)`**
    *   **Description**: Gets comprehensive characteristics for any musical genre.
    *   **AI Agent Prompt**: "Tell me about the characteristics of blues music." (Genre: "blues")

*   **`create_progression(genre: str, key: str, variation: str = "standard", bars: int = None)`**
    *   **Description**: Creates an authentic chord progression for any genre.
    *   **AI Agent Prompt**: "Create a 12-bar blues progression in the key of E." (Genre: "blues", Key: "E", Bars: 12)

*   **`create_beat(genre: str, tempo: int, complexity: str = "medium", variation: str = "standard")`**
    *   **Description**: Creates authentic drum patterns for any genre.
    *   **AI Agent Prompt**: "Create a hip-hop beat at 90 BPM." (Genre: "hip_hop", Tempo: 90)

### Phase 5: Advanced Composition

These tools enable the creation of complete musical works.

*   **`create_song_structure(genre: str, song_type: str = "standard", duration: int = 180)`**
    *   **Description**: Generates a complete song structure template.
    *   **AI Agent Prompt**: "Create a standard pop song structure." (Genre: "pop", Song Type: "standard")

*   **`develop_melodic_motif(motif: List[int], development_techniques: List[str], target_length: int = 8)`**
    *   **Description**: Develops a short melodic motif using classical development techniques.
    *   **AI Agent Prompt**: "Develop this 3-note motif [60, 62, 64] into an 8-bar melody using sequencing and inversion." (Motif: [60, 62, 64], Development Techniques: ["sequencing", "inversion"], Target Length: 8)

*   **`arrange_for_ensemble(composition: dict, ensemble_type: str, arrangement_style: str = "balanced")`**
    *   **Description**: Arranges an existing composition for a specific ensemble.
    *   **AI Agent Prompt**: "Arrange this melody for a string quartet." (Composition: [current_composition_data], Ensemble Type: "string_quartet")

*   **`compose_complete_song(description: str, genre: str, key: str, tempo: int, target_duration: int = 180)`**
    *   **Description**: Generates a complete musical composition from a text description.
    *   **AI Agent Prompt**: "Compose a sad ballad in A minor about lost love." (Description: "sad ballad about lost love", Genre: "ballad", Key: "A minor")

## 🏗️ System Architecture

### **Phase-Based Development**
The system is built in 8 comprehensive phases:

1. **Foundation**: Basic MIDI playback and MCP server framework
2. **Core MIDI**: Complete file operations and editing capabilities  
3. **Music Theory**: Scales, chords, progressions, and analysis
4. **Genre Knowledge**: Style-specific creation and authenticity
5. **Advanced Composition**: Complete song creation and development
6. **Specialized Agents**: Domain-expert AI personas
7. **Production**: Professional audio processing and rendering
8. **Integration**: Complete system polish and optimization

### **Knowledge-Driven Architecture**
- **Music Theory Engine**: Expert-validated harmonic rules and relationships
- **Genre Databases**: Comprehensive style profiles with authentic patterns
- **Pattern Libraries**: Rhythmic, melodic, and harmonic templates
- **Quality Validation**: Automatic musical correctness checking

## 📖 Documentation

### **Getting Started**
- [Installation Guide](docs/usage/GETTING_STARTED.md) - Complete setup instructions
- [Quick Start Tutorial](docs/usage/GETTING_STARTED.md#first-steps) - Create your first composition
- [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md) - Technical overview

### **Implementation**
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) - Complete development roadmap
- [Phase Documentation](docs/phases/) - Detailed phase-by-phase guides
- [HIL Testing Guide](docs/testing/HIL_TESTING_GUIDE.md) - Human-in-the-loop validation

### **API Reference**
- [Tool Documentation](docs/api/) - Complete MCP tool reference
- [Agent Guide](docs/usage/AGENT_EXAMPLES.md) - Specialized agent usage
- [Genre Profiles](docs/architecture/KNOWLEDGE_BASE_DESIGN.md) - Musical style definitions

## 🎵 Musical Examples

### Blues in E
```python
# Create authentic 12-bar blues with shuffle feel
create_blues_progression(key="E", variation="standard", bars=12)
add_blues_feel(shuffle_intensity=0.67)
create_blues_melody(style="chicago")
```

### Jazz Ballad
```python
# Sophisticated jazz harmony with professional voice leading
create_chord_progression(key="Bb", progression=["ii", "V", "I", "vi"])
optimize_voice_leading(voice_count=4)
add_jazz_extensions(complexity="professional")
```

### Hip Hop Production
```python
# Modern trap-influenced beat with dark harmonies
create_hip_hop_beat(style="trap", tempo=140)
create_hip_hop_chord_loop(key="F#m", mood="dark", duration=4)
apply_production_effects(style="modern")
```

## 🧪 Testing & Quality

### **Human-in-the-Loop Validation**
Every feature is validated through comprehensive HIL testing:
- **Musical Accuracy**: Expert musician validation of theory and harmony
- **Genre Authenticity**: Style specialists verify authentic characteristics
- **Production Quality**: Audio engineers validate professional standards
- **User Experience**: Real users test creative workflows

### **Automated Testing**
- **Unit Tests**: Individual component validation
- **Integration Tests**: Cross-system compatibility
- **Performance Tests**: Speed and resource usage optimization
- **Regression Tests**: Ensure updates don't break existing functionality

## 🤝 Contributing

We welcome contributions from musicians, developers, and music enthusiasts!

### **Ways to Contribute**
- **Musical Knowledge**: Add genre profiles, patterns, and examples
- **Code Contributions**: Improve algorithms, add features, fix bugs
- **Documentation**: Help others learn and use the system
- **Testing**: Validate musical quality and report issues

### **Development Setup**
```bash
git clone https://github.com/your-org/midi-mcp.git
cd midi-mcp
python -m venv dev-env
source dev-env/bin/activate
pip install -r requirements-dev.txt
pytest  # Run test suite
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Transform your AI into a musical collaborator. Start creating today! 🎵**
