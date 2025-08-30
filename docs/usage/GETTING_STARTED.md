# Getting Started with MIDI MCP Server

## Overview
The MIDI MCP Server is a comprehensive music creation and production system that enables AI agents to compose, arrange, and produce professional-quality music. This guide will help you get up and running quickly.

## What You'll Create
By the end of this guide, you'll have:
- A working MIDI MCP server
- An AI agent that can create music
- Your first AI-generated musical composition
- Understanding of the system's core capabilities

## Prerequisites

### System Requirements
**Minimum Requirements:**
- Python 3.10 or higher
- 4GB RAM
- 2GB free disk space
- Audio output capability (built-in audio is fine)

**Recommended Setup:**
- Python 3.11+
- 8GB+ RAM
- 5GB+ free disk space
- Dedicated audio interface
- MIDI synthesizer or high-quality software synth

### Software Dependencies
**Required:**
- Python 3.10+ with pip
- MCP-compatible AI agent (GitHub Copilot with VS Code or Claude Desktop)

**Optional but Recommended:**
- Digital Audio Workstation (DAW) like GarageBand, Logic Pro, Ableton Live, or FL Studio
- MIDI routing software (IAC Driver on Mac, loopMIDI on Windows)

## Installation

### Step 1: Install the MIDI MCP Server
```bash
# Clone the repository
git clone https://github.com/your-org/midi-mcp.git
cd midi-mcp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Step 2: Configure MIDI Output
#### macOS Setup
1. Open **Audio MIDI Setup** (Applications > Utilities)
2. Go to **Window > Show MIDI Studio**
3. Double-click **IAC Driver**
4. Check **"Device is online"**
5. Note the port name for configuration

#### Windows Setup
1. Download and install [loopMIDI](http://www.tobias-erichsen.de/software/loopmidi.html)
2. Create a virtual MIDI port named "MCP-MIDI"
3. Keep loopMIDI running

#### Linux Setup
```bash
# Install ALSA MIDI
sudo apt-get install alsa-utils

# Load virtual MIDI module
sudo modprobe snd-virmidi

# List available MIDI ports
aplaymidi -l
```

### Step 3: Set Up Your DAW or Synthesizer
**Option A: Using a DAW**
1. Open your preferred DAW
2. Create a new project
3. Set up a MIDI track
4. Set the MIDI input to your virtual MIDI port (IAC Driver or MCP-MIDI)
5. Load a software instrument (piano, strings, etc.)

**Option B: Using Built-in Software Synth**
1. The server includes basic software synthesis
2. No additional setup required
3. Audio will play through your default audio device

### Step 4: Configure Your AI Agent

#### GitHub Copilot with VS Code
1. Install the MCP extension for VS Code (if available)
2. Add to your VS Code `settings.json`:
```json
{
  "mcp.servers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/midi-mcp/src/server.py"],
      "env": {
        "MIDI_OUTPUT_PORT": "0"
      }
    }
  }
}
```

#### Claude Desktop
1. Locate your `claude_desktop_config.json` file
2. Add the server configuration:
```json
{
  "mcpServers": {
    "midi-mcp": {
      "command": "python",
      "args": ["/Users/yourusername/path/to/midi-mcp/src/server.py"],
      "env": {
        "MIDI_OUTPUT_PORT": "0"
      }
    }
  }
}
```

## First Steps

### Step 1: Start the Server
```bash
# Activate your virtual environment if not already active
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the server
python src/server.py
```

You should see output indicating the server is running and listening for connections.

### Step 2: Connect Your AI Agent
1. Start your AI agent (VS Code with Copilot or Claude Desktop)
2. The agent should automatically discover the MIDI MCP server
3. Test the connection by asking: "What MIDI tools are available?"

### Step 3: Create Your First Music

#### Test 1: Play a Simple Note
Ask your AI agent:
```
"Play middle C for 2 seconds"
```

**Expected Result**: You should hear a middle C note play for 2 seconds through your audio setup.

#### Test 2: Create a Scale
Ask your AI agent:
```
"Play a C major scale ascending"
```

**Expected Result**: You should hear the 8 notes of a C major scale played in sequence.

#### Test 3: Create a Chord Progression
Ask your AI agent:
```
"Create and play a simple chord progression in C major"
```

**Expected Result**: You should hear a series of chords that sound musical and harmonious.

### Step 4: Create Your First Composition
Ask your AI agent:
```
"Create a simple pop song structure with verse and chorus in the key of G major"
```

**Expected Result**: The AI will create a more complex musical structure with multiple sections.

## Understanding the System

### Core Concepts

#### Tools vs. Agents
- **Tools**: Individual functions like `play_note()`, `create_chord()`, `analyze_key()`
- **Agents**: Specialized personas like Composer Agent, Arranger Agent, Theory Assistant

#### MIDI Files vs. Real-time Playback
- **Real-time**: Immediate playback through MIDI devices
- **MIDI Files**: Saved compositions that can be opened in DAWs

#### Phases and Capabilities
The system is organized into phases of increasing sophistication:
1. **Basic MIDI**: Play notes and sequences
2. **File Operations**: Create and edit MIDI files
3. **Music Theory**: Scales, chords, progressions
4. **Genre Knowledge**: Style-specific creation
5. **Advanced Composition**: Complete song creation
6. **Specialized Agents**: Expert-level assistance
7. **Production**: Professional audio processing

### Key Features

#### Intelligent Music Creation
The AI understands music theory and can create harmonically correct, stylistically appropriate music.

#### Genre Awareness
The system knows the characteristics of different musical genres and can create authentic-sounding music in various styles.

#### Professional Quality
All output is suitable for professional use, from MIDI files to rendered audio.

#### Educational Value
The system can explain music theory concepts and analyze musical examples.

## Common Use Cases

### For Musicians
- **Composition Assistance**: Get help with chord progressions, melodies, arrangements
- **Theory Learning**: Understand complex musical concepts with examples
- **Arrangement Ideas**: Transform simple melodies into full arrangements

### For Producers
- **Beat Creation**: Generate rhythmic patterns for various genres
- **Harmonic Foundation**: Create chord progressions for sampling or live recording
- **Production Templates**: Get starting points for different musical styles

### For Educators
- **Theory Examples**: Generate musical examples for teaching
- **Student Exercises**: Create practice materials and exercises
- **Analysis Tools**: Analyze musical examples for educational purposes

### For Developers
- **Music Generation**: Add music generation to applications
- **Educational Tools**: Build music learning applications
- **Creative AI**: Explore AI-assisted creativity

## Troubleshooting

### Common Issues

#### No Sound Output
**Problem**: Commands execute but no sound plays
**Solutions**:
1. Check MIDI routing configuration
2. Verify DAW or synthesizer is receiving MIDI
3. Check audio device settings
4. Try built-in software synthesis

#### Agent Can't Connect
**Problem**: AI agent doesn't see MIDI tools
**Solutions**:
1. Verify server is running (`python src/server.py`)
2. Check configuration file paths are correct
3. Restart AI agent application
4. Check server logs for error messages

#### Musical Quality Issues
**Problem**: Generated music doesn't sound good
**Solutions**:
1. Try different genres or styles
2. Use more specific prompts
3. Ask for music theory explanations
4. Experiment with different agents (Composer vs. Arranger)

#### Performance Issues
**Problem**: System responds slowly
**Solutions**:
1. Close unnecessary applications
2. Use simpler prompts initially
3. Check system resources (CPU, memory)
4. Try smaller musical examples first

### Getting Help

#### Documentation
- **User Guide**: Comprehensive feature documentation
- **API Reference**: Detailed tool descriptions
- **Examples**: Sample projects and use cases

#### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community questions and sharing
- **Examples Repository**: Community-contributed examples

#### Support Channels
- **Documentation**: Most questions answered in docs
- **Community Forum**: Peer support and discussions
- **GitHub Issues**: Bug reports and feature requests

## Next Steps

### Learn More
1. **Read the User Guide**: Comprehensive documentation of all features
2. **Try Different Genres**: Explore blues, rock, jazz, classical
3. **Experiment with Agents**: Try the specialized agent personas
4. **Create Complete Songs**: Use advanced composition features

### Advanced Features
1. **Production Tools**: Learn mixing and mastering capabilities
2. **Custom Genres**: Create your own genre profiles
3. **Batch Processing**: Work with multiple files
4. **Audio Rendering**: Generate high-quality audio files

### Contribute
1. **Share Examples**: Contribute interesting musical examples
2. **Report Issues**: Help improve the system
3. **Suggest Features**: Ideas for new capabilities
4. **Documentation**: Help improve guides and examples

## Quick Reference

### Essential Commands
```
# Basic playback
"Play middle C"
"Play a C major scale"
"Play a C major chord"

# Music theory
"What notes are in E minor?"
"Create a ii-V-I progression in F major"
"Analyze this chord progression"

# Composition
"Create a blues progression in A"
"Write a simple melody over these chords"
"Create a song structure for a ballad"

# File operations
"Save this as a MIDI file called 'my_song'"
"Load the MIDI file 'example.mid'"
"Create a new MIDI file with piano and drums"

# Agent activation
"Activate the composer agent"
"Switch to the theory assistant"
"Use the arranger agent to orchestrate this"
```

### Keyboard Shortcuts (if applicable)
- **Ctrl+C**: Stop current playback
- **Ctrl+S**: Quick save current project
- **Ctrl+O**: Open MIDI file browser

Welcome to the world of AI-assisted music creation! The MIDI MCP Server opens up new possibilities for musical creativity and learning. Start with simple examples and gradually explore the more advanced features as you become comfortable with the system.