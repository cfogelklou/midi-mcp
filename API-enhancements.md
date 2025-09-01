# API Enhancements for MIDI MCP Server

This document outlines proposed enhancements to the MIDI MCP Server API to improve the AI agent's ability to create complete musical compositions with fewer steps and a more intuitive workflow. The current API design often requires the agent to perform low-level MIDI file manipulation after generating abstract musical data, leading to a cumbersome and error-prone process.

## Core Problem Identified

The primary issue is the disconnect between tools that generate musical *ideas* (e.g., chord progressions, melodies, song structures) and tools that generate actual *MIDI note data* within a MIDI file. High-level composition tools currently return abstract data representations (e.g., lists of notes, chord symbols, dictionaries of musical parameters) but do not directly produce or modify MIDI files with playable content. This forces the AI agent to manually bridge this gap using low-level file management operations.

## Proposed Enhancements

### 1. Enhance High-Level Composition Tools to Directly Output MIDI

Tools that generate significant musical content should have the capability to directly create or append to a MIDI file. This would significantly reduce the number of steps and complexity for the AI agent.

**Affected Tools (Examples):**
*   `create_chord_progression` (from `theory_tools.py`)
*   `create_melody` (from `genre_tools.py`)
*   `create_bass_line` (from `genre_tools.py`)
*   `compose_complete_song` (from `composition_tools.py`)
*   `generate_song_section` (from `composition_tools.py`)
*   `create_progression` (from `genre_tools.py`)
*   `create_beat` (from `genre_tools.py`)
*   `create_arrangement` (from `genre_tools.py`)

**Proposed Change:**
Add optional parameters to these tools, such as `midi_file_id` and `track_name` (or `track_index`), allowing the generated musical data to be directly written to a specified MIDI file and track. If `midi_file_id` is not provided, the tool can return the abstract data as it does now. If provided, it should return the `midi_file_id` and confirmation of notes added.

**Example for `create_chord_progression`:**

```python
@app.tool(name="create_chord_progression")
async def create_chord_progression(
    key: str,
    progression: List[str],
    duration_per_chord: float = 1.0,
    midi_file_id: Optional[str] = None,  # New parameter
    track_name: Optional[str] = None,    # New parameter
    channel: int = 0,                    # New parameter
    program: int = 0                     # New parameter
) -> List[TextContent]:
    """
    Create a chord progression in a specific key, optionally adding it to a MIDI file.

    Args:
        key: Key signature (C, Am, F#, Bbm, etc.)
        progression: Roman numeral progression (["I", "vi", "ii", "V"])
        duration_per_chord: Duration of each chord in beats
        midi_file_id: Optional ID of the MIDI file to add the progression to.
        track_name: Optional name for the new track (if midi_file_id is provided).
        channel: MIDI channel for the notes (if midi_file_id is provided).
        program: MIDI program (instrument) for the notes (if midi_file_id is provided).

    Returns:
        MIDI data for the chord progression, or confirmation of MIDI file update.
    """
    # ... existing logic to create chord_progression object ...

    if midi_file_id and track_name:
        # Logic to create track if it doesn't exist and add notes to it
        # This would involve calling MidiFileManager.add_track and MidiFileManager.add_notes_to_track
        # (or a new helper function that wraps these)
        # Return success message with midi_file_id
        pass
    else:
        # Return abstract data as currently
        pass
```

**Specific consideration for `compose_complete_song`:**
This tool should ideally return a `midi_file_id` directly, representing the fully composed and populated song. It would internally orchestrate the creation of tracks and addition of notes from its generated sections, melodies, and harmonies.

### 2. Introduce a General `add_musical_data_to_midi_file` Tool

While enhancing high-level tools is crucial, a more general tool would also be beneficial for scenarios where the AI agent needs fine-grained control or wants to combine outputs from different tools. This tool would encapsulate the `add_notes_to_track` functionality that the agent had to discover and use manually.

**Proposed New Tool (in `file_tools.py`):**

```python
@app.tool(name="add_musical_data_to_midi_file")
async def add_musical_data_to_midi_file(
    midi_file_id: str,
    track_name: str,
    notes_data: List[Dict[str, Any]], # e.g., [{"note": 60, "velocity": 100, "start_time": 0.0, "duration": 1.0}, ...]
    channel: int = 0,
    program: int = 0,
    create_track_if_not_exists: bool = True
) -> List[TextContent]:
    """
    Adds musical note data to a specified track within a MIDI file.

    Args:
        midi_file_id: ID of the MIDI file to modify.
        track_name: Name of the track to add notes to.
        notes_data: List of dictionaries, each representing a note with 'note' (MIDI number),
                    'velocity', 'start_time' (in beats), and 'duration' (in beats).
        channel: MIDI channel for the notes.
        program: MIDI program (instrument) for the notes.
        create_track_if_not_exists: If True, creates the track if it doesn't already exist.

    Returns:
        Confirmation of notes added and updated MIDI file information.
    """
    # This tool would wrap MidiFileManager.add_notes_to_track and potentially MidiFileManager.add_track
    pass
```

This tool would allow the agent to take the output (e.g., `notes` lists) from any musical generation tool and easily convert it into MIDI file content.

### 3. Streamline Track Management

The current `add_track` tool requires a `midi_file_id`. While necessary, ensuring that high-level tools can implicitly manage tracks (e.g., create a new track if `track_name` is provided but no `track_index` or existing track is found) would further simplify the workflow.

**Proposed Change:**
Ensure that any tool that adds notes to a MIDI file can automatically create a track if the specified `track_name` does not exist within the `midi_file_id`. This would be part of the implementation for the enhanced tools (point 1) and the new `add_musical_data_to_midi_file` tool (point 2).

## Benefits of Proposed Enhancements

*   **Reduced Steps:** AI agent can achieve musical composition goals in fewer tool calls.
*   **Improved Intuition:** High-level tools directly produce tangible MIDI output, aligning better with the agent's goal of "making a song."
*   **Increased Efficiency:** Less manual orchestration of low-level file operations.
*   **Clearer API Contract:** The purpose and output of composition tools become more explicit regarding MIDI generation.
*   **Enhanced Agent Autonomy:** The agent can more easily self-correct and achieve complex musical tasks without human intervention for MIDI conversion.

These enhancements will transform the MCP API from a set of abstract musical concept generators and separate file manipulators into a cohesive system for end-to-end musical composition.