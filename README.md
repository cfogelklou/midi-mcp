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

## �️ MIDI Setup for Quality Playback

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

## �🎼 What You Can Create

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

## 🙏 Acknowledgments

- **MCP Team**: For creating the Model Context Protocol that makes AI-system integration seamless
- **Music Theory Experts**: Who validated our harmonic and theoretical implementations
- **Genre Specialists**: Musicians who ensured authentic representation of musical styles  
- **Open Source Community**: Contributors of MIDI libraries, soundfonts, and musical resources

## 🔗 Links

- **Documentation**: [Full Documentation Site](https://your-org.github.io/midi-mcp/)
- **Examples**: [Community Examples Repository](https://github.com/your-org/midi-mcp-examples)
- **Discord**: [Community Discussion](https://discord.gg/midi-mcp)
- **YouTube**: [Video Tutorials and Demos](https://youtube.com/@midi-mcp)

---

**Transform your AI into a musical collaborator. Start creating today! 🎵**