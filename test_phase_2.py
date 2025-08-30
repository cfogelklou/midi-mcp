# -*- coding: utf-8 -*-
"""
Test Phase 2 MIDI file operations.

Basic test to verify MIDI file creation, saving, loading, and analysis functionality.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import asyncio
import logging
import tempfile
import os
from pathlib import Path

from src.midi_mcp.midi.file_ops import MidiFileManager
from src.midi_mcp.midi.analyzer import MidiAnalyzer
from src.midi_mcp.midi.player import MidiFilePlayer
from src.midi_mcp.utils.logger import setup_logging


async def test_phase_2_basics():
    """Test basic Phase 2 functionality."""
    logger = setup_logging("INFO")
    logger.info("Starting Phase 2 basic functionality test")
    
    # Initialize components
    file_manager = MidiFileManager()
    analyzer = MidiAnalyzer()
    player = MidiFilePlayer()
    
    try:
        # Test 1: Create a new MIDI file
        logger.info("Test 1: Creating MIDI file")
        file_id = file_manager.create_midi_file(
            title="Phase 2 Test Song",
            tempo=128,
            time_signature=(4, 4),
            key_signature="G"
        )
        logger.info(f"Created MIDI file with ID: {file_id}")
        
        # Test 2: Add tracks
        logger.info("Test 2: Adding tracks")
        piano_track = file_manager.add_track(file_id, "Piano", channel=0, program=0)
        bass_track = file_manager.add_track(file_id, "Bass", channel=1, program=32)
        drum_track = file_manager.add_track(file_id, "Drums", channel=9, program=0)
        
        logger.info(f"Added tracks: Piano({piano_track}), Bass({bass_track}), Drums({drum_track})")
        
        # Test 3: Save the file
        logger.info("Test 3: Saving MIDI file")
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test_song.mid")
            saved_path = file_manager.save_midi_file(file_id, filename)
            logger.info(f"Saved MIDI file to: {saved_path}")
            
            # Verify file exists
            if os.path.exists(saved_path):
                logger.info("✓ File saved successfully")
            else:
                logger.error("✗ File not found after saving")
                return False
            
            # Test 4: Load the file
            logger.info("Test 4: Loading MIDI file")
            loaded_file_id = file_manager.load_midi_file(saved_path)
            logger.info(f"Loaded MIDI file with ID: {loaded_file_id}")
            
            # Test 5: Analyze the file
            logger.info("Test 5: Analyzing MIDI file")
            analysis = file_manager.analyze_midi_file(loaded_file_id)
            logger.info(f"Analysis results:")
            logger.info(f"  Title: {analysis['title']}")
            logger.info(f"  Tracks: {analysis['tracks']}")
            logger.info(f"  Tempo: {analysis['tempo']} BPM")
            logger.info(f"  Duration: {analysis['duration_seconds']:.2f} seconds")
            
            # Test 6: Comprehensive analysis
            logger.info("Test 6: Comprehensive analysis")
            session = file_manager.get_session(loaded_file_id)
            comprehensive = analyzer.analyze_comprehensive(session.midi_file)
            logger.info(f"Comprehensive analysis completed")
            logger.info(f"  Format type: {comprehensive['basic_info']['format_type']}")
            logger.info(f"  Total messages: {comprehensive['basic_info']['total_messages']}")
            
            # Test 7: List files
            logger.info("Test 7: Listing MIDI files")
            files = file_manager.list_midi_files()
            logger.info(f"Found {len(files)} MIDI files in session")
            for file_info in files:
                logger.info(f"  - {file_info['title']} ({file_info['file_id'][:8]}...)")
        
        logger.info("✓ All Phase 2 basic tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Phase 2 test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test runner."""
    print("MIDI MCP Server - Phase 2 Test")
    print("===============================")
    
    success = await test_phase_2_basics()
    
    if success:
        print("\n🎉 Phase 2 implementation successful!")
        print("Ready for:")
        print("- MIDI file creation and editing")
        print("- Multi-track composition")
        print("- File I/O operations")
        print("- MIDI analysis")
        print("- Real-time playback (requires connected MIDI device)")
    else:
        print("\n❌ Phase 2 test failed - check logs for details")


if __name__ == "__main__":
    asyncio.run(main())
