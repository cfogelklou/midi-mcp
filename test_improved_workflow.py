#!/usr/bin/env python3
"""
Test script for the improved MIDI composition workflow.
This demonstrates how to create a complete composition with actual note data.
"""

import asyncio
import json
from src.midi_mcp.composition.complete_composer import CompleteComposer
from src.midi_mcp.midi.file_ops import MidiFileManager
from src.midi_mcp.tools.composition_tools import *

async def test_complete_workflow():
    """Test the complete composition to MIDI workflow."""
    print("🎵 Testing Complete MIDI Composition Workflow")
    print("=" * 50)
    
    # Step 1: Create a MIDI file
    print("1. Creating MIDI file...")
    file_manager = MidiFileManager()
    midi_file_id = file_manager.create_midi_file(
        title="Test Sad Ballad",
        tempo=72,
        key_signature="Am"
    )
    print(f"   Created MIDI file: {midi_file_id}")
    
    # Step 2: Add tracks
    print("2. Adding tracks...")
    track1 = file_manager.add_track(midi_file_id, "Piano", channel=0, program=0)
    track2 = file_manager.add_track(midi_file_id, "Strings", channel=1, program=48) 
    track3 = file_manager.add_track(midi_file_id, "Bass", channel=2, program=32)
    print(f"   Added tracks: Piano({track1}), Strings({track2}), Bass({track3})")
    
    # Step 3: Create composition structure
    print("3. Creating composition...")
    composer = CompleteComposer()
    composition = composer.compose_complete_song(
        description="a melancholic ballad about lost love",
        genre="ballad",
        key="Am",
        tempo=72,
        target_duration=240,
        ensemble_type="string_quartet"  # Use supported ensemble type
    )
    print(f"   Composition: '{composition.title}' in {composition.key}")
    print(f"   Structure: {len(composition.structure.sections)} sections")
    
    # Step 4: Extract composition data for MIDI population
    print("4. Extracting composition data...")
    composition_data = {
        "tempo": composition.tempo,
        "key": composition.key,
        "main_melody": composition.melody,
        "harmonic_progression": composition.harmony,
        "song_structure": {
            "sections": [
                {
                    "type": section.type.value,
                    "duration": section.duration
                } for section in composition.structure.sections
            ]
        }
    }
    
    # Step 5: Add sample note data for testing
    print("5. Adding note data to tracks...")
    
    # Simple melody notes for piano track
    melody_notes = [
        {"note": 69, "start": 0, "duration": 1, "velocity": 80, "channel": 0},    # A
        {"note": 72, "start": 1, "duration": 1, "velocity": 75, "channel": 0},    # C
        {"note": 76, "start": 2, "duration": 2, "velocity": 85, "channel": 0},    # E
        {"note": 74, "start": 4, "duration": 1, "velocity": 70, "channel": 0},    # D
        {"note": 72, "start": 5, "duration": 1, "velocity": 75, "channel": 0},    # C
        {"note": 69, "start": 6, "duration": 2, "velocity": 80, "channel": 0},    # A
    ]
    
    # Chord progression for piano
    chord_notes = [
        # Am chord (A-C-E)
        {"note": 57, "start": 0, "duration": 4, "velocity": 60, "channel": 0},    # A2
        {"note": 60, "start": 0, "duration": 4, "velocity": 60, "channel": 0},    # C3
        {"note": 64, "start": 0, "duration": 4, "velocity": 60, "channel": 0},    # E3
        
        # F chord (F-A-C)  
        {"note": 53, "start": 4, "duration": 4, "velocity": 60, "channel": 0},    # F2
        {"note": 57, "start": 4, "duration": 4, "velocity": 60, "channel": 0},    # A2
        {"note": 60, "start": 4, "duration": 4, "velocity": 60, "channel": 0},    # C3
    ]
    
    # Bass line
    bass_notes = [
        {"note": 45, "start": 0, "duration": 4, "velocity": 70, "channel": 2},    # A1
        {"note": 41, "start": 4, "duration": 4, "velocity": 70, "channel": 2},    # F1
    ]
    
    # Add notes to tracks
    piano_melody_count = file_manager.add_notes_to_track(midi_file_id, 1, melody_notes, 72)
    piano_chord_count = file_manager.add_notes_to_track(midi_file_id, 1, chord_notes, 72)
    bass_count = file_manager.add_notes_to_track(midi_file_id, 3, bass_notes, 72)
    
    print(f"   Piano melody: {piano_melody_count} notes")
    print(f"   Piano chords: {piano_chord_count} notes") 
    print(f"   Bass line: {bass_count} notes")
    
    # Step 6: Save the file
    print("6. Saving MIDI file...")
    filename = file_manager.save_midi_file(midi_file_id, "test_sad_ballad_populated.mid")
    print(f"   Saved: {filename}")
    
    # Step 7: Analyze the file
    print("7. Analyzing populated file...")
    from src.midi_mcp.midi.analyzer import MidiAnalyzer
    analyzer = MidiAnalyzer()
    
    # Get the session to access the midi_file object
    session = file_manager._get_session(midi_file_id)
    analysis = analyzer.analyze_comprehensive(session.midi_file)
    
    # Debug: print the structure
    print(f"   Analysis keys: {list(analysis.keys())}")
    
    duration = analysis.get('timing', {}).get('total_duration', 0)
    total_notes = analysis.get('notes', {}).get('total_notes', 0)
    note_density = total_notes / max(duration, 1)
    
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Total notes: {total_notes}")
    print(f"   Note density: {note_density:.2f} notes/second")
    
    print("\n✅ Complete workflow test successful!")
    print(f"🎵 Your sad ballad is now a real MIDI file with {total_notes} notes!")
    
    return filename

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())
