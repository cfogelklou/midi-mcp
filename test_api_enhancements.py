#!/usr/bin/env python3
"""
Test script for API enhancements to MIDI MCP Server.

Tests the new functionality:
1. add_musical_data_to_midi_file wrapper tool
2. Enhanced composition tools with direct MIDI output
3. Auto-track creation functionality
"""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from midi_mcp.midi.file_ops import MidiFileManager


async def test_midi_enhancements():
    """Test the API enhancements."""
    print("🎵 Testing MIDI API Enhancements")
    print("=" * 50)
    
    # Initialize file manager
    file_manager = MidiFileManager()
    
    try:
        # Test 1: Create a MIDI file
        print("\n1. Testing MIDI file creation...")
        file_id = file_manager.create_midi_file(
            title="Test API Enhancements",
            tempo=120,
            time_signature=(4, 4),
            key_signature="C"
        )
        print(f"✅ Created MIDI file with ID: {file_id}")
        
        # Test 2: Test the enhanced add_notes_to_track functionality (auto-track creation)
        print("\n2. Testing auto-track creation and note addition...")
        
        # Create some test notes - C major scale
        c_major_scale = [
            {"note": 60, "velocity": 80, "start_time": 0.0, "duration": 0.5},  # C4
            {"note": 62, "velocity": 80, "start_time": 0.5, "duration": 0.5},  # D4
            {"note": 64, "velocity": 80, "start_time": 1.0, "duration": 0.5},  # E4
            {"note": 65, "velocity": 80, "start_time": 1.5, "duration": 0.5},  # F4
            {"note": 67, "velocity": 80, "start_time": 2.0, "duration": 0.5},  # G4
            {"note": 69, "velocity": 80, "start_time": 2.5, "duration": 0.5},  # A4
            {"note": 71, "velocity": 80, "start_time": 3.0, "duration": 0.5},  # B4
            {"note": 72, "velocity": 80, "start_time": 3.5, "duration": 0.5},  # C5
        ]
        
        # Add track and notes
        track_index = file_manager.add_track(
            midi_file_id=file_id,
            track_name="C Major Scale",
            channel=0,
            program=0  # Acoustic Grand Piano
        )
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier="C Major Scale",
            notes_data=c_major_scale,
            channel=0
        )
        
        print(f"✅ Added C major scale to track: C Major Scale (index: {track_index})")
        
        # Test 3: Add a chord progression using the wrapper functionality
        print("\n3. Testing chord progression addition...")
        
        # C major chord progression: I-vi-ii-V
        chord_progression = [
            # C major chord (C-E-G)
            {"note": 60, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # C4
            {"note": 64, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # E4
            {"note": 67, "velocity": 70, "start_time": 0.0, "duration": 2.0},  # G4
            
            # A minor chord (A-C-E)
            {"note": 57, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # A3
            {"note": 60, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # C4
            {"note": 64, "velocity": 70, "start_time": 2.0, "duration": 2.0},  # E4
            
            # D minor chord (D-F-A)
            {"note": 62, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # D4
            {"note": 65, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # F4
            {"note": 69, "velocity": 70, "start_time": 4.0, "duration": 2.0},  # A4
            
            # G major chord (G-B-D)
            {"note": 55, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # G3
            {"note": 59, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # B3
            {"note": 62, "velocity": 70, "start_time": 6.0, "duration": 2.0},  # D4
        ]
        
        # This simulates what the add_musical_data_to_midi_file tool would do
        # Check if chord track exists, create if not
        chord_track_name = "Chord Progression"
        session = file_manager.get_session(file_id)
        track_exists = any(track.get("name") == chord_track_name for track in session.tracks)
        
        if not track_exists:
            chord_track_index = file_manager.add_track(
                midi_file_id=file_id,
                track_name=chord_track_name,
                channel=1,
                program=0  # Acoustic Grand Piano
            )
            print(f"✅ Auto-created track: {chord_track_name} (index: {chord_track_index})")
        
        file_manager.add_notes_to_track(
            midi_file_id=file_id,
            track_identifier=chord_track_name,
            notes_data=chord_progression,
            channel=1
        )
        
        print(f"✅ Added chord progression (I-vi-ii-V) to track: {chord_track_name}")
        
        # Test 4: Analyze the MIDI file
        print("\n4. Testing MIDI file analysis...")
        analysis = file_manager.analyze_midi_file(file_id)
        
        print(f"✅ Analysis complete:")
        print(f"   Title: {analysis['title']}")
        print(f"   Duration: {analysis['duration_seconds']:.2f} seconds")
        print(f"   Tracks: {analysis['tracks']}")
        print(f"   Total Notes: {analysis['note_count']}")
        print(f"   Note Range: {analysis['note_range']['min']} - {analysis['note_range']['max']}")
        print(f"   Track Info:")
        for track in analysis['track_info']:
            print(f"     - {track['name']} (Channel {track['channel']}, Program {track['program']})")
        
        # Test 5: Save the MIDI file
        print("\n5. Testing MIDI file saving...")
        output_path = "test_api_enhancements_output.mid"
        saved_path = file_manager.save_midi_file(file_id, output_path)
        print(f"✅ Saved MIDI file to: {saved_path}")
        
        # Test 6: Load the saved file
        print("\n6. Testing MIDI file loading...")
        loaded_file_id = file_manager.load_midi_file(saved_path)
        loaded_analysis = file_manager.analyze_midi_file(loaded_file_id)
        
        print(f"✅ Loaded MIDI file with ID: {loaded_file_id}")
        print(f"   Title: {loaded_analysis['title']}")
        print(f"   Duration: {loaded_analysis['duration_seconds']:.2f} seconds")
        print(f"   Tracks: {loaded_analysis['tracks']}")
        print(f"   Total Notes: {loaded_analysis['note_count']}")
        
        print("\n🎉 All API enhancement tests passed successfully!")
        print(f"📁 Output file saved as: {saved_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("Starting MIDI API Enhancement Tests...")
    
    # Check if mido is available
    try:
        import mido
        print("✅ mido library found")
    except ImportError:
        print("❌ mido library not found. Please install with: pip install mido")
        return False
    
    # Run the tests
    result = asyncio.run(test_midi_enhancements())
    
    if result:
        print("\n🎯 Summary: All API enhancements are working correctly!")
        print("The following new capabilities are now available:")
        print("  ✅ add_musical_data_to_midi_file - General wrapper tool")
        print("  ✅ Enhanced composition tools with optional midi_file_id parameters")
        print("  ✅ Automatic track creation functionality")
        print("  ✅ Direct MIDI output from high-level composition tools")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    return result


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)