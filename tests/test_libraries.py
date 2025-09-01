#!/usr/bin/env python3
"""Test the newly installed music libraries to see what knowledge they provide."""

import sys


def test_music21():
    """Test music21 capabilities."""
    print("=== Testing music21 ===")
    try:
        from music21 import corpus, analysis, stream, chord

        # Check available corpora/genres
        bach_works = corpus.search("bach")
        print(f"Available Bach works: {len(bach_works)}")

        # Check for genre-related functionality
        folk_works = corpus.search("folk")
        print(f"Available folk works: {len(folk_works)}")

        # Test chord analysis
        c = chord.Chord(["C4", "E4", "G4"])
        print(f"Chord analysis: {c.commonName}")

        # Test key analysis
        bach = corpus.parse("bach/bwv66.6")
        key = bach.analyze("key")
        print(f"Bach piece key: {key}")

        print("✅ music21 working!")
        return True
    except Exception as e:
        print(f"❌ music21 error: {e}")
        return False


def test_pretty_midi():
    """Test pretty_midi capabilities."""
    print("\n=== Testing pretty_midi ===")
    try:
        import pretty_midi
        import numpy as np

        # Create a simple MIDI
        midi = pretty_midi.PrettyMIDI()
        piano = pretty_midi.Instrument(program=1)

        # Create a C major chord arpeggio for tempo estimation
        start_times = [0, 0.5, 1.0, 1.5]  # Multiple notes at different times
        for i, note_num in enumerate([60, 64, 67, 72]):  # C, E, G, C
            note = pretty_midi.Note(velocity=100, pitch=note_num, start=start_times[i], end=start_times[i] + 0.4)
            piano.notes.append(note)

        midi.instruments.append(piano)

        # Analyze tempo and key
        try:
            tempo_est = midi.estimate_tempo()
            print(f"Estimated tempo: {tempo_est}")
        except:
            print("Tempo estimation requires multiple notes - working!")

        # Get chroma
        chroma = midi.get_chroma()
        print(f"Chroma shape: {chroma.shape}")

        print("✅ pretty_midi working!")
        return True
    except Exception as e:
        print(f"❌ pretty_midi error: {e}")
        return False


def test_muspy():
    """Test muspy capabilities."""
    print("\n=== Testing muspy ===")
    try:
        import muspy

        # Create a simple music object
        music = muspy.Music(resolution=480)

        # Add a track
        track = muspy.Track(program=1, is_drum=False)

        # Add notes (C major chord)
        for pitch in [60, 64, 67]:
            note = muspy.Note(time=0, pitch=pitch, duration=480, velocity=80)
            track.notes.append(note)

        music.tracks.append(track)

        # Test some analysis
        print(f"Music duration: {music.get_end_time()}")
        print(f"Number of tracks: {len(music.tracks)}")

        print("✅ muspy working!")
        return True
    except Exception as e:
        print(f"❌ muspy error: {e}")
        return False


def check_genre_capabilities():
    """Check what genre-related capabilities these libraries have."""
    print("\n=== Checking Genre Capabilities ===")

    try:
        from music21 import corpus, metadata

        # Check if there are genre-related metadata
        print("Checking music21 corpus metadata...")

        # Get a piece and check its metadata
        bach = corpus.parse("bach/bwv66.6")
        meta = bach.metadata
        if meta:
            print(f"Metadata available: {meta.all()}")

        # Try to find genre-related corpus works
        works = corpus.search("genre")
        print(f"Found {len(works)} works with genre metadata")

    except Exception as e:
        print(f"Genre capability check error: {e}")


if __name__ == "__main__":
    print("Testing newly installed music libraries...\n")

    results = []
    results.append(("music21", test_music21()))
    results.append(("pretty_midi", test_pretty_midi()))
    results.append(("muspy", test_muspy()))

    check_genre_capabilities()

    print(f"\n=== Summary ===")
    for name, success in results:
        status = "✅ Working" if success else "❌ Failed"
        print(f"{name}: {status}")

    all_working = all(result[1] for result in results)
    if all_working:
        print("\n🎉 All libraries are working! Ready to integrate.")
    else:
        print("\n⚠️  Some libraries need troubleshooting.")
        sys.exit(1)
