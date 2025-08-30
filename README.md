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

### 🎚️ **Professional Production**
- **MIDI Humanization**: Transform mechanical sequences into expressive performances
- **Mixing & Mastering**: Professional audio processing and loudness optimization
- **High-Quality Rendering**: Export studio-quality audio in multiple formats
- **Workflow Integration**: Seamlessly fits into existing music production workflows

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/your-org/midi-mcp.git
cd midi-mcp
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Basic Setup
1. **Configure MIDI Output**: Set up virtual MIDI routing (IAC Driver on Mac, loopMIDI on Windows)
2. **Connect Your DAW**: Route MIDI to your favorite music software
3. **Configure AI Agent**: Add server to GitHub Copilot or Claude Desktop

### Your First Composition
```python
# In your AI agent (GitHub Copilot, Claude Desktop, etc.):
"Create a blues progression in E major and play it"
"Now add a simple melody over those chords"
"Save this as a MIDI file called 'my_first_blues.mid'"
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