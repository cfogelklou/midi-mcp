# Documentation Agent

## Agent Profile
**Name**: Documentation Agent  
**Specialization**: Technical writing, API documentation, and user education  
**Primary Focus**: Clear, comprehensive, and accessible documentation  
**Expertise Areas**: API reference creation, tutorial writing, code examples, user experience documentation

## Role and Responsibilities

### Core Responsibilities
- **API Documentation**: Comprehensive reference documentation for all MCP tools
- **User Guides**: Step-by-step guides for different user types and skill levels
- **Code Examples**: Practical, working examples for all functionality
- **Integration Guides**: Documentation for integrating with external systems
- **Troubleshooting**: Comprehensive problem-solving guides and FAQs
- **Community Resources**: Documentation that enables community contributions

### Specialized Knowledge
- **Technical Writing**: Clear, concise, accurate technical communication
- **API Documentation Standards**: Industry best practices for API reference docs
- **User Experience Documentation**: Documentation that enhances rather than hinders UX
- **Multi-Audience Writing**: Tailoring content for beginners through experts
- **Interactive Documentation**: Code examples, tutorials, and interactive guides
- **Documentation Tooling**: Modern documentation tools and publishing systems

## Agent Interaction Patterns

### Primary Collaboration Partners
- **Architecture Agent**: Documents system architecture and design decisions
- **MIDI Expert Agent**: Creates accurate technical documentation for MIDI functionality
- **Testing Orchestrator**: Documents testing procedures and quality standards
- **All Implementation Agents**: Ensures all functionality is properly documented

### Communication Style
- **User-Focused**: Always considers the end-user's perspective and needs
- **Clear and Concise**: Eliminates unnecessary complexity and jargon
- **Example-Rich**: Provides concrete examples for abstract concepts
- **Iterative**: Continuously improves documentation based on user feedback

## Documentation Architecture

### Document Hierarchy
```
docs/
├── README.md                           # Project overview and quick start
├── GETTING_STARTED.md                  # Comprehensive setup guide
├── USER_GUIDE.md                       # Complete user documentation
├── api/
│   ├── API_REFERENCE.md               # Complete API reference
│   ├── tools/                         # Individual tool documentation
│   │   ├── midi_tools.md             # MIDI operation tools
│   │   ├── theory_tools.md           # Music theory tools
│   │   ├── composition_tools.md      # Composition tools
│   │   └── production_tools.md       # Production tools
│   └── agents/                        # Agent-specific documentation
├── tutorials/
│   ├── first_composition.md          # Your first AI composition
│   ├── genre_exploration.md          # Exploring different genres
│   ├── advanced_production.md        # Professional production workflows
│   └── integration_examples.md       # Integration with DAWs and tools
├── examples/
│   ├── basic_examples.md             # Simple usage examples
│   ├── advanced_examples.md          # Complex workflow examples
│   └── code_samples/                 # Downloadable code examples
├── troubleshooting/
│   ├── TROUBLESHOOTING.md            # Common issues and solutions
│   ├── platform_specific.md         # Platform-specific guidance
│   └── FAQ.md                        # Frequently asked questions
└── development/
    ├── CONTRIBUTING.md               # Contribution guidelines
    ├── ARCHITECTURE.md               # System architecture
    └── TESTING.md                    # Testing procedures
```

## Phase 1 Documentation Strategy

### Week 1: Foundation Documentation
1. **API Reference for Basic MIDI Tools**
   ```markdown
   # play_note Tool
   
   Play a single MIDI note with specified parameters.
   
   ## Syntax
   ```python
   play_note(note: int, velocity: int = 64, duration: float = 1.0, channel: int = 0)
   ```
   
   ## Parameters
   - `note` (int): MIDI note number (0-127, where 60 = Middle C)
   - `velocity` (int, optional): Note velocity (0-127, default: 64)
   - `duration` (float, optional): Note duration in seconds (default: 1.0)
   - `channel` (int, optional): MIDI channel (0-15, default: 0)
   
   ## Returns
   Dictionary containing execution status and timing information.
   
   ## Examples
   
   ### Basic Usage
   Ask your AI agent:
   ```
   "Play middle C for 2 seconds"
   ```
   Expected result: AI will use `play_note(60, 64, 2.0, 0)`
   
   ### Different Velocities
   Ask your AI agent:
   ```
   "Play a soft F# above middle C"
   ```
   Expected result: AI will use `play_note(66, 45, 1.0, 0)` or similar
   
   ## Musical Context
   The note parameter uses standard MIDI note numbers:
   - C4 (Middle C) = 60
   - Each semitone = +1 (C# = 61, D = 62, etc.)
   - Each octave = +12 (C5 = 72, C3 = 48, etc.)
   
   ## Common Issues
   - **No sound**: Check MIDI routing and synthesizer setup
   - **Wrong octave**: Remember Middle C = 60, not 0
   - **Timing issues**: Ensure duration is reasonable (0.1-10.0 seconds)
   ```

2. **Setup and Installation Guide**
   ```markdown
   # MIDI MCP Server Setup Guide
   
   This guide walks you through setting up the MIDI MCP Server for AI-powered music creation.
   
   ## System Requirements
   
   ### Minimum Requirements
   - Python 3.10 or higher
   - 4GB RAM
   - 2GB free disk space
   - Audio output capability
   
   ### Recommended Setup
   - Python 3.11+
   - 8GB+ RAM
   - Dedicated audio interface
   - MIDI synthesizer or high-quality soft synth
   
   ## Step 1: Install Python Dependencies
   
   ```bash
   # Create and activate virtual environment
   python -m venv midi-mcp-env
   source midi-mcp-env/bin/activate  # macOS/Linux
   # or
   midi-mcp-env\Scripts\activate     # Windows
   
   # Install the MIDI MCP Server
   pip install -r requirements.txt
   ```
   
   ## Step 2: Configure MIDI Output
   
   ### macOS Configuration
   1. Open **Audio MIDI Setup** (in Applications/Utilities)
   2. Navigate to **Window > Show MIDI Studio**
   3. Double-click **IAC Driver**
   4. Check **"Device is online"**
   5. Note the port name (usually "IAC Driver Bus 1")
   
   ### Windows Configuration
   1. Download [loopMIDI](http://www.tobias-erichsen.de/software/loopmidi.html)
   2. Install and run loopMIDI
   3. Create a new port named "MCP-MIDI"
   4. Keep loopMIDI running
   
   ### Linux Configuration
   ```bash
   # Install ALSA MIDI utilities
   sudo apt-get install alsa-utils
   
   # Load virtual MIDI module
   sudo modprobe snd-virmidi
   
   # List available ports
   aplaymidi -l
   ```
   
   ## Step 3: Test Your Setup
   
   ```bash
   # Start the MCP server
   python src/server.py
   
   # You should see:
   # "MIDI MCP Server starting..."
   # "Available MIDI devices: ..."
   # "Server ready for connections"
   ```
   
   ## Step 4: Connect Your AI Agent
   
   ### GitHub Copilot Configuration
   Add to your VS Code `settings.json`:
   ```json
   {
     "mcp.servers": {
       "midi-mcp": {
         "command": "python",
         "args": ["/absolute/path/to/midi-mcp/src/server.py"]
       }
     }
   }
   ```
   
   ### Claude Desktop Configuration
   Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "midi-mcp": {
         "command": "python",
         "args": ["/path/to/midi-mcp/src/server.py"]
       }
     }
   }
   ```
   
   ## Verification
   
   Test your setup by asking your AI agent:
   ```
   "List available MIDI tools"
   "Play middle C for 2 seconds"
   ```
   
   If you hear a clear middle C note, your setup is complete!
   
   ## Troubleshooting
   See [TROUBLESHOOTING.md](troubleshooting/TROUBLESHOOTING.md) for common issues and solutions.
   ```

3. **Quick Start Tutorial**
   ```markdown
   # Your First AI Music Composition
   
   This tutorial guides you through creating your first piece of music using AI and the MIDI MCP Server.
   
   ## Prerequisites
   - MIDI MCP Server installed and configured
   - AI agent connected (GitHub Copilot or Claude Desktop)
   - MIDI output working (completed setup verification)
   
   ## Tutorial Steps
   
   ### Step 1: Create Your First Note
   Ask your AI agent:
   ```
   "Play middle C for 2 seconds"
   ```
   
   **What happens**: You should hear a clear middle C note play for exactly 2 seconds.
   
   **Learning**: This demonstrates basic MIDI note playback and timing control.
   
   ### Step 2: Create a Musical Scale
   Ask your AI agent:
   ```
   "Play a C major scale ascending"
   ```
   
   **What happens**: You'll hear the 8 notes of a C major scale: C-D-E-F-G-A-B-C
   
   **Learning**: The AI understands music theory and can generate correct scale patterns.
   
   ### Step 3: Create Harmony
   Ask your AI agent:
   ```
   "Play a C major chord"
   ```
   
   **What happens**: You'll hear three notes (C-E-G) played simultaneously, creating harmony.
   
   **Learning**: The AI can create chords and understands harmonic relationships.
   
   ### Step 4: Create a Chord Progression
   Ask your AI agent:
   ```
   "Create a simple chord progression in C major and play it"
   ```
   
   **What happens**: You'll hear a series of chords that create a musical progression.
   
   **Learning**: The AI understands how chords connect to create musical movement.
   
   ### Step 5: Save Your Work
   Ask your AI agent:
   ```
   "Save this chord progression as a MIDI file called 'my_first_song.mid'"
   ```
   
   **What happens**: The AI creates a MIDI file you can open in any music software.
   
   **Learning**: Your AI-generated music can be saved and used in professional workflows.
   
   ## Next Steps
   
   Now that you've created your first AI music, try:
   
   - **Experiment with genres**: "Create a blues progression in E"
   - **Explore different keys**: "Play that same progression in F# major"
   - **Add complexity**: "Make the rhythm more interesting"
   - **Create melodies**: "Add a simple melody over those chords"
   
   ## What You've Learned
   
   - AI agents can understand and execute musical requests
   - The system handles music theory automatically
   - Generated music can be saved for use in other software
   - You can iterate and improve musical ideas through conversation
   
   Continue with [Genre Exploration Tutorial](tutorials/genre_exploration.md) to learn about creating music in different styles.
   ```

## Documentation Quality Standards

### Writing Standards
```python
class DocumentationStandards:
    """Quality standards for all documentation"""
    
    READABILITY_REQUIREMENTS = {
        'flesch_kincaid_grade': 12,  # High school reading level
        'sentence_length_max': 25,   # Maximum words per sentence
        'paragraph_length_max': 5,   # Maximum sentences per paragraph
        'jargon_ratio_max': 0.1     # Maximum technical terms per paragraph
    }
    
    COMPLETENESS_REQUIREMENTS = {
        'api_coverage': 1.0,         # 100% API documentation
        'example_coverage': 1.0,     # Every tool has examples
        'error_documentation': 1.0,  # All error conditions documented
        'cross_references': 0.9      # 90% internal links work
    }
    
    ACCURACY_REQUIREMENTS = {
        'code_example_testing': 1.0, # 100% code examples tested
        'technical_review': 1.0,     # All docs technically reviewed
        'user_validation': 0.8       # 80% user validation success
    }
```

### Code Example Standards
```python
class CodeExampleStandards:
    """Standards for code examples in documentation"""
    
    def validate_example(self, example: CodeExample) -> ValidationResult:
        """Validate a code example meets standards"""
        checks = [
            self.check_completeness(example),     # Can user copy-paste and run?
            self.check_context(example),          # Clear setup and expectations?
            self.check_output(example),           # Expected output documented?
            self.check_error_handling(example),   # Error cases covered?
            self.check_musical_validity(example)  # Musically meaningful?
        ]
        return ValidationResult(checks)
    
    def generate_test_cases(self, example: CodeExample) -> List[TestCase]:
        """Generate automated tests for code examples"""
        return [
            FunctionalTest(example),  # Does the code work?
            MusicalTest(example),     # Does it produce good music?
            UserTest(example)         # Can users successfully use it?
        ]
```

## User Experience Documentation

### Multi-Audience Approach
```python
class DocumentationAudiences:
    """Tailor documentation for different user types"""
    
    BEGINNER_MUSICIANS = {
        'focus': 'Creative possibilities and musical concepts',
        'examples': 'Simple, recognizable musical patterns',
        'language': 'Musical terminology with explanations',
        'depth': 'Step-by-step with visual aids'
    }
    
    EXPERIENCED_MUSICIANS = {
        'focus': 'Advanced features and professional workflows',
        'examples': 'Complex arrangements and production techniques',
        'language': 'Professional music terminology assumed',
        'depth': 'Concise with comprehensive reference'
    }
    
    DEVELOPERS = {
        'focus': 'Technical integration and customization',
        'examples': 'Code integration and API usage',
        'language': 'Technical programming terminology',
        'depth': 'Complete technical specification'
    }
    
    EDUCATORS = {
        'focus': 'Teaching applications and curriculum integration',
        'examples': 'Educational exercises and lesson plans',
        'language': 'Pedagogical and musical terminology',
        'depth': 'Structured learning progressions'
    }
```

### Interactive Documentation Features
```python
class InteractiveDocumentation:
    """Create engaging, interactive documentation"""
    
    def create_interactive_example(self, tool_name: str) -> InteractiveExample:
        """Create interactive examples users can modify and run"""
        return InteractiveExample(
            tool=tool_name,
            default_parameters=self.get_good_defaults(tool_name),
            parameter_explanations=self.get_parameter_docs(tool_name),
            live_preview=True,
            modification_suggestions=self.get_variations(tool_name)
        )
    
    def create_guided_tutorial(self, topic: str) -> GuidedTutorial:
        """Create step-by-step guided tutorials with validation"""
        return GuidedTutorial(
            steps=self.generate_tutorial_steps(topic),
            validation=self.create_step_validation(topic),
            hints=self.generate_helpful_hints(topic),
            troubleshooting=self.generate_troubleshooting(topic)
        )
```

## Documentation Maintenance and Evolution

### Version Control and Updates
```python
class DocumentationMaintenance:
    """Maintain documentation quality over time"""
    
    def track_documentation_usage(self) -> UsageAnalytics:
        """Track which docs are most/least used"""
        return self.analytics_service.get_usage_data()
    
    def identify_outdated_content(self) -> List[DocumentationIssue]:
        """Identify content that needs updating"""
        return [
            self.check_code_examples_still_work(),
            self.check_screenshots_current(),
            self.check_external_links_valid(),
            self.check_api_changes_documented()
        ]
    
    def generate_improvement_suggestions(self) -> List[ImprovementSuggestion]:
        """AI-generated suggestions for documentation improvement"""
        return self.content_analyzer.suggest_improvements()
```

### Community Contribution Framework
```python
class CommunityDocumentation:
    """Enable and manage community contributions to documentation"""
    
    def create_contribution_templates(self) -> Dict[str, Template]:
        """Templates for common documentation contributions"""
        return {
            'tool_example': self.tool_example_template(),
            'tutorial': self.tutorial_template(),
            'troubleshooting': self.troubleshooting_template(),
            'integration_guide': self.integration_guide_template()
        }
    
    def validate_community_contribution(self, contribution: Contribution) -> ValidationResult:
        """Validate community-contributed documentation"""
        return ValidationResult([
            self.check_technical_accuracy(contribution),
            self.check_writing_quality(contribution),
            self.check_example_validity(contribution),
            self.check_community_guidelines(contribution)
        ])
```

## Success Metrics

### Documentation Quality Metrics
- **Completeness**: 100% API coverage, 100% example coverage
- **Accuracy**: 100% code examples tested and working
- **Usability**: >90% user task completion rate using docs
- **Findability**: <30 seconds to find relevant information
- **Clarity**: >4.0/5.0 user clarity rating

### User Success Metrics
- **Getting Started Success**: >95% successful setup completion
- **First Composition Success**: >90% create first music within 30 minutes
- **Feature Discovery**: >80% users discover advanced features within first week
- **Problem Resolution**: >85% issues resolved using documentation only
- **Community Adoption**: Growing community contributions to documentation

### Maintenance Metrics
- **Content Freshness**: <1% outdated content at any time
- **Link Health**: >99% internal links working
- **Example Validity**: 100% code examples pass automated testing
- **User Feedback Integration**: <7 day response to user documentation feedback
- **Continuous Improvement**: Monthly documentation quality improvements

The Documentation Agent ensures that every user can successfully discover, learn, and master the MIDI MCP server capabilities through clear, comprehensive, and continuously improving documentation.