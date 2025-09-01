# Music Composition Architecture

This document outlines the architecture of the music composition system within the MIDI MCP server. The system is designed to be modular, with clear separation of concerns between different musical tasks.

## Core Modules

The composition system is built around a set of core modules, each responsible for a specific aspect of music creation.

### 1. `composition` Module

This is the central module for high-level composition tasks. It orchestrates the other modules to generate complete musical pieces.

-   **`complete_composer.py`**: Contains the `CompleteComposer` class, which is the main entry point for generating a full composition from a high-level description. It handles the entire workflow, from creating the song structure to arranging the final piece.
-   **`song_structure.py`**: Defines the structure of a song, including sections (verse, chorus, etc.), transitions, and the overall key plan. The `SongStructureGenerator` class creates these structures based on genre conventions.
-   **`melodic_development.py`**: Provides tools for creating and manipulating melodies. This includes `MotifDeveloper` for evolving short musical ideas, `PhraseGenerator` for creating well-formed musical phrases, and `MelodyVariator` for adding interest to repeated melodies.
-   **`arrangement.py`**: Handles the orchestration of the composition. The `EnsembleArranger` assigns instruments to different parts, the `CounterMelodyGenerator` creates complementary melodic lines, and the `TextureOrchestrator` manages the overall sonic density.
-   **`voice_leading.py`**: (Part of the `theory` module, but crucial for composition) Ensures that the transitions between chords are smooth and musically pleasing. The `VoiceLeadingOptimizer` can be used to improve the voice leading of a given chord progression.

### 2. `theory` Module

This module provides the fundamental music theory knowledge required for composition.

-   **`chords.py`**: `ChordManager` handles everything related to chords, from building them from a root note and quality to analyzing their function within a progression.
-   **`scales.py`**: `ScaleManager` provides functionality for generating scales, identifying intervals, and understanding the relationships between different scales.
-   **`keys.py`**: `KeyManager` is used to detect the key of a piece of music, suggest modulations, and provide information about key signatures.
-   **`progressions.py`**: `ProgressionManager` creates, analyzes, and validates chord progressions based on common harmonic practices.

### 3. `genres` Module

This module encapsulates the knowledge of different musical genres.

-   **`genre_manager.py`**: The `GenreManager` is the central repository for genre-specific information, such as typical tempos, chord progressions, and instrumentation.
-   **`composer.py`**: The `Composer` class in this module is a high-level facade that uses the `GenreManager` to create genre-authentic musical components like chord progressions and melodies.

### 4. `models` Module

This module contains the data classes that represent the various musical concepts used throughout the system.

-   **`composition_models.py`**: Defines the data structures for compositions, sections, melodies, arrangements, and other high-level musical constructs.
-   **`theory_models.py`**: Defines the fundamental data structures for notes, chords, and scales.

## Composition Workflow

A typical composition workflow involves the following steps:

1.  **Request**: A high-level request is made to the `CompleteComposer` with a description of the desired music.
2.  **Structure Generation**: The `SongStructureGenerator` creates a song structure based on the requested genre and duration.
3.  **Harmonic Foundation**: The `ProgressionManager` or the genre-specific `Composer` generates a foundational chord progression.
4.  **Melody Creation**: The `PhraseGenerator` and `MotifDeveloper` create the main melodic themes.
5.  **Melodic Development**: The `MelodyVariator` creates variations of the melodies for different sections of the song.
6.  **Arrangement**: The `EnsembleArranger` assigns instruments to the different musical parts. The `CounterMelodyGenerator` may be used to create additional melodic lines.
7.  **Orchestration**: The `TextureOrchestrator` adjusts the texture and dynamics of the arrangement to create a more engaging listening experience.
8.  **Voice Leading Optimization**: The `VoiceLeadingOptimizer` refines the connections between chords to ensure smooth transitions.
9.  **Analysis and Refinement**: The `CompositionAnalyzer` can be used to assess the quality of the generated composition, and the `CompositionRefiner` can be used to make improvements based on the analysis.

## Key Interactions

-   The `CompleteComposer` acts as the main orchestrator, calling upon the other modules in a logical sequence to build the final composition.
-   The `composition` modules rely heavily on the `theory` modules for fundamental music theory knowledge. For example, the `PhraseGenerator` uses the `ChordManager` to understand the underlying harmony.
-   The `genres` module provides the stylistic context for the composition. The `CompleteComposer` uses the `GenreManager` to inform its decisions about structure, harmony, and instrumentation.
-   The `models` provide a common language for the different modules to communicate. For example, the `SongStructureGenerator` produces a `SongStructure` object that is then used by the `EnsembleArranger`.
