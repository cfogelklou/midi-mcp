# AI Fails and Areas for Improvement

This document lists issues, inconsistencies, and areas for improvement identified during the architectural review of the music composition system. These are primarily aimed at improving the robustness, maintainability, and overall quality of the codebase.

After each step of this document, please do ./run_all_tests and fix any failing tests (or disable them with a comment if they require massive refactoring)

## 0. Create or update the "help" tool to add all of the other tools
- The AI agent should be able to call "help" for any of the other tools
- Help will return the function of the tool, and the expected input parameters, and expected outputs.
- Help will prevent the AI agent spinning its wheels trying to figure out how to use a particular tool, or what it is for.
- Because of the advanced nature of some of the tools, the description of the more advanced functions might be complex. This is ok.
- When adding help, if you find hardcoded constants that are embedded right into a function, move them to the top of the file, or to constants.py, and ensure they are exposed via help.

## 1. API Mismatches and Inconsistencies

Several API mismatches and inconsistencies were found, which can lead to confusion and errors.

-   **Inconsistent Data Structures**: Different modules expect slightly different data structures for the same concepts. For example, a `Composition` object is sometimes represented as a dictionary and sometimes as a dataclass. This is particularly evident in the `EnsembleArranger.arrange_for_ensemble` method, which has to handle both `Dict` and `Composition` types.
-   **`CompleteComposer` Return Type**: The `compose_complete_song` method in `CompleteComposer` returns a `CompleteComposition` object, but the `_apply_texture_orchestration` method it calls returns a `Dict`. This inconsistency should be resolved.
-   **`create_song_structure` in `composition_tools.py`**: The tool `create_song_structure` returns a JSON string, but the underlying `SongStructureGenerator.create_structure` returns a `SongStructure` object. The tool should ideally return a more structured object, or the conversion to JSON should be handled more gracefully.
-   **`generate_song_section` in `composition_tools.py`**: Similar to the above, this tool also returns a JSON string, while the underlying function returns a `Section` object.

## 2. Hardcoded Strings and Magic Numbers

There are numerous instances of hardcoded strings and magic numbers that should be replaced with named constants or configuration values.

-   **Ensemble Definitions**: In `arrangement.py`, the `EnsembleArranger` has hardcoded definitions for different ensembles (e.g., "piano_solo", "string_quartet"). These should be moved to a configuration file or a dedicated constants module.
-   **Instrument Roles**: The `_determine_instrument_role` method in `EnsembleArranger` uses a hardcoded dictionary to map instruments to roles. This should be made more flexible and configurable.
-   **Dynamic Plan Strings**: The `_apply_texture_orchestration` method in `CompleteComposer` uses hardcoded strings for dynamic plans (e.g., "p", "mp", "f"). These should be replaced with the `DynamicLevel` enum.
-   **Fallback Progressions**: The `_create_harmonic_foundation` method in `CompleteComposer` has hardcoded fallback chord progressions for different genres. This logic should be moved into the `genres` module and defined in the genre data files.
-   **Title Generation**: The `_generate_title` method in `CompleteComposer` contains hardcoded stop words. These should be defined in a more appropriate location.

## 3. Lack of Input Validation

Many functions and methods lack proper input validation, which could lead to unexpected errors.

-   **`create_song_structure`**: The `genre` and `song_type` parameters are not validated against the available genres and song types.
-   **`arrange_for_ensemble`**: The `ensemble_type` is validated, but the `composition` input is not thoroughly checked for the required keys.

## 4. Redundant Code and Logic

There are some instances of redundant code that could be refactored for better maintainability.

-   **`_get_section_energy_level`**: This method is duplicated in `song_structure.py` and `section_generator.py`. It should be defined in a single place.
-   **Chord Symbol to Root Conversion**: The `_chord_symbol_to_root` method in `arrangement.py` is a simplified version of what is likely available in the `theory` module. It should be replaced with a call to the `ChordManager`.

## 5. Recommendations for Improvement

-   **Standardize Data Models**: Enforce the consistent use of the data classes defined in `composition_models.py` and `theory_models.py` across all modules. Avoid passing around dictionaries when a dataclass is available.
-   **Create a Constants Module**: Create a dedicated module for constants, such as instrument names, ensemble definitions, and other magic strings.
-   **Improve Configuration**: Move genre-specific data, such as fallback progressions and instrument roles, into the JSON files in the `data/genres` directory.
-   **Add Input Validation**: Add robust input validation to all public-facing functions and methods to ensure that they receive the expected data.
-   **Refactor Redundant Code**: Identify and refactor redundant code to improve maintainability and reduce the risk of inconsistencies.

## 6. Improving AI Agent Accessibility and Workflow

To make the composition tools more accessible and effective for an AI agent, we should encourage a more structured, query-based workflow. Instead of directly calling a high-level composition tool, the agent should first engage in a "discovery" phase to gather relevant musical context.

### Proposed Agent Workflow

When a user asks to create a song (e.g., "make a jazz song"), the AI agent should follow a workflow similar to this:

1.  **Genre Discovery**: The agent should first query the system for information about the requested genre. This can be done using a new tool, `get_genre_characteristics`.

    -   **Example**: `get_genre_characteristics(genre="jazz")`
    -   **Returns**: Information about typical tempos, key signatures, scales, chord progressions, and instrumentation for jazz.

2.  **Theory Exploration**: Based on the genre information, the agent can then explore specific music theory concepts. For example, if the genre information indicates that "ii-V-I" progressions are common, the agent can query for more information about that progression.

    -   **Example**: `analyze_progression(progression=["ii", "V", "I"], key="C")`
    -   **Returns**: A detailed analysis of the ii-V-I progression in the key of C.

3.  **Component-Based Composition**: Armed with this theoretical knowledge, the agent can then start building the song piece by piece, using the individual composition tools.

    -   **Create a progression**: `create_chord_progression(key="C", progression=["Dm7", "G7", "Cmaj7"])`
    -   **Create a melody**: `create_melodic_phrase(chord_progression=["Dm7", "G7", "Cmaj7"], key="C")`
    -   **Create a bass line**: `create_bass_line_with_voice_leading(chord_progression=...)`
    -   **Arrange the parts**: `arrange_for_ensemble(composition=..., ensemble_type="jazz_combo")`

### New Tools for Agent Accessibility

To support this workflow, we should introduce a few new high-level tools specifically designed for AI agents:

-   **`get_genre_characteristics(genre: str)`**: A tool that returns a summary of the musical characteristics of a given genre, as described above.
-   **`suggest_composition_ideas(genre: str, mood: str)`**: A tool that provides a list of suggested starting points for a composition, such as common chord progressions, melodic motifs, or rhythmic patterns for a given genre and mood.

By encouraging this query-based approach, we can help the AI agent make more musically informed decisions, leading to higher-quality compositions and a more interactive and transparent user experience.

## 7. Why are only these tools available via list_tools.py?

Here are the available tools:
   * server_status: Get the current status of the MIDI MCP server
   * discover_midi_devices: Discover MIDI devices and return device
     information
   * connect_midi_device: Connect to a MIDI device
   * play_midi_note: Play a single MIDI note
   * list_connected_devices: List currently connected MIDI devices
   * disconnect_midi_device: Disconnect from a MIDI device
   * create_midi_file: Create a new MIDI file with basic metadata
   * add_track: Add a new track to an existing MIDI file
   * save_midi_file: Save MIDI file to disk
   * load_midi_file: Load a MIDI file from disk
   * play_midi_file: Play a loaded MIDI file in real-time through a specified
     MIDI device
   * analyze_midi_file: Analyze a loaded MIDI file for detailed information
   * list_midi_files: List all MIDI files in the current session
   * stop_midi_playback: Stop MIDI file playback
   * add_musical_data_to_midi_file: Add musical note data to a specified
     track within a MIDI file