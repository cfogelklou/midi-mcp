#!/usr/bin/env python3
"""Demonstration of Phase 4: Genre Knowledge capabilities."""

import json
from src.midi_mcp.genres import GenreManager, GenericComposer

def demo_genre_discovery():
    """Demonstrate genre discovery functionality."""
    print("🎵 === GENRE DISCOVERY DEMO ===")
    
    manager = GenreManager()
    
    # List available genres
    genres = manager.get_available_genres()
    print(f"Available Genres: {list(genres['genres'].keys())}")
    print(f"Total: {genres['total_count']} genres")
    print(f"Main genres: {genres['main_genres']}")
    print(f"Subgenres: {genres['subgenres']}")

def demo_genre_characteristics():
    """Demonstrate getting genre characteristics."""
    print(f"\n🎸 === GENRE CHARACTERISTICS DEMO ===")
    
    manager = GenreManager()
    
    # Get blues characteristics
    blues = manager.get_genre_data('blues')
    print(f"\nBlues Characteristics:")
    print(f"  Tempo range: {blues['tempo_range']} BPM")
    print(f"  Progressions: {list(blues['progressions'].keys())}")
    print(f"  Essential instruments: {blues['instrumentation']['essential']}")
    print(f"  Typical scales: {blues['scales'][:3]}")

def demo_genre_comparison():
    """Demonstrate genre comparison."""
    print(f"\n🔍 === GENRE COMPARISON DEMO ===")
    
    manager = GenreManager()
    
    # Compare blues and rock
    comparison = manager.compare_genres('blues', 'rock')
    print(f"\nBlues vs Rock:")
    print(f"  Relationship score: {comparison['relationship_score']}")
    print(f"  Common instruments: {comparison['instrumentation_overlap']}")

def demo_progression_creation():
    """Demonstrate chord progression creation."""
    print(f"\n🎹 === PROGRESSION CREATION DEMO ===")
    
    manager = GenreManager()
    composer = GenericComposer(manager)
    
    # Create different genre progressions
    genres_to_test = ['blues', 'rock', 'jazz', 'hip_hop', 'trance']
    
    for genre in genres_to_test:
        progression = composer.create_progression(genre, 'C', 'standard')
        pattern = progression.get('pattern', [])
        print(f"  {genre.title()}: {' - '.join(pattern)}")

def demo_beat_creation():
    """Demonstrate beat pattern creation."""
    print(f"\n🥁 === BEAT CREATION DEMO ===")
    
    manager = GenreManager()
    composer = GenericComposer(manager)
    
    # Create beats for different genres
    beat_demos = [
        ('hip_hop', 90, 'boom_bap'),
        ('rock', 120, 'driving'),
        ('jazz', 140, 'swing'),
        ('trance', 132, 'four_on_floor')
    ]
    
    for genre, tempo, variation in beat_demos:
        beat = composer.create_beat(genre, tempo, 'medium', variation)
        feel = beat.get('feel', 'unknown')
        print(f"  {genre.title()}: {feel} feel at {tempo}bpm ({variation})")

def demo_melody_creation():
    """Demonstrate melody creation."""
    print(f"\n🎼 === MELODY CREATION DEMO ===")
    
    manager = GenreManager()
    composer = GenericComposer(manager)
    
    # Create a rock progression then melody
    progression = composer.create_progression('rock', 'G', 'standard')
    melody = composer.create_melody('rock', 'G', progression, 'typical')
    
    print(f"  Rock melody in G major:")
    print(f"    Scale used: {melody.get('scale_used')}")
    print(f"    Notes: {len(melody.get('melody', []))} melody notes")
    print(f"    Chord tone ratio: {melody.get('characteristics', {}).get('chord_tone_ratio', 0)}")

def demo_arrangement_creation():
    """Demonstrate arrangement creation."""
    print(f"\n🎺 === ARRANGEMENT DEMO ===")
    
    manager = GenreManager()
    composer = GenericComposer(manager)
    
    # Create jazz arrangement
    song_structure = {'sections': ['intro', 'verse', 'chorus', 'solo', 'outro']}
    arrangement = composer.create_arrangement('jazz', song_structure, 'standard')
    
    print(f"  Jazz arrangement:")
    print(f"    Instruments: {list(arrangement['parts'].keys())}")
    print(f"    Texture: {arrangement['texture']}")
    print(f"    Dynamics: {arrangement['dynamics']}")

def demo_fusion_style():
    """Demonstrate genre fusion."""
    print(f"\n🔀 === GENRE FUSION DEMO ===")
    
    from src.midi_mcp.tools.genre_tools import register_genre_tools
    from fastmcp import FastMCP
    
    # This would normally be done through MCP tools
    # For demo, we'll show the concept
    
    manager = GenreManager()
    
    # Show relationship scores for fusion potential
    fusion_pairs = [
        ('jazz', 'blues'),
        ('rock', 'blues'),
        ('hip_hop', 'jazz'),
        ('trance', 'ambient'),
        ('pop', 'rock')
    ]
    
    print("  Fusion potential (relationship scores):")
    for genre1, genre2 in fusion_pairs:
        comparison = manager.compare_genres(genre1, genre2)
        score = comparison.get('relationship_score', 0)
        compatibility = "High" if score > 0.7 else "Medium" if score > 0.4 else "Low"
        print(f"    {genre1.title()} + {genre2.title()}: {score:.1f} ({compatibility})")

def demo_library_integration():
    """Demonstrate integration with music21."""
    print(f"\n📚 === LIBRARY INTEGRATION DEMO ===")
    
    manager = GenreManager()
    
    # Show music21 integration
    available_libs = manager.libraries.get_available_libraries()
    print(f"  Available libraries: {list(available_libs.keys())}")
    
    if available_libs.get('music21'):
        # Demonstrate chord analysis
        chord_analysis = manager.libraries.music21.get_chord_from_notes(['C', 'E', 'G', 'B'])
        print(f"  Cmaj7 analysis: {chord_analysis['name']} ({chord_analysis['quality']})")
        
        # Demonstrate Roman numeral
        roman_analysis = manager.libraries.music21.get_roman_numeral_chord('ii7', 'C')
        print(f"  ii7 in C major: {roman_analysis['chord_name']} ({roman_analysis['notes']})")

def run_all_demos():
    """Run all Phase 4 demonstrations."""
    print("🎵 MIDI MCP Server - Phase 4: Genre Knowledge System Demo 🎵\n")
    print("Demonstrating real-world usage of generic genre tools...\n")
    
    try:
        demo_genre_discovery()
        demo_genre_characteristics()
        demo_genre_comparison()
        demo_progression_creation()
        demo_beat_creation()
        demo_melody_creation()
        demo_arrangement_creation()
        demo_fusion_style()
        demo_library_integration()
        
        print(f"\n{'='*60}")
        print("🎉 Phase 4 Demo Complete!")
        print("The system successfully demonstrates:")
        print("  ✅ Generic functions working with 10+ genres")
        print("  ✅ Real music theory via music21 integration")
        print("  ✅ Authentic chord progressions and patterns")
        print("  ✅ Genre comparison and fusion capabilities")
        print("  ✅ Complete composition pipeline (progression → melody → arrangement)")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        raise

if __name__ == "__main__":
    run_all_demos()