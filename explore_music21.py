#!/usr/bin/env python3
"""Explore music21's genre and style capabilities."""

def explore_music21_genre_knowledge():
    """Explore what music21 offers for genre and style analysis."""
    print("=== Exploring music21 Genre Knowledge ===")
    
    try:
        from music21 import corpus, scale, chord, roman, key, stream, analysis
        
        # Check what scales are available
        print("\n1. Available Scales:")
        from music21.scale import Scale
        
        # Test some common scales
        scales_to_test = ['major', 'minor', 'blues', 'pentatonic', 'dorian']
        for scale_name in scales_to_test:
            try:
                if scale_name == 'blues':
                    s = scale.BluesScale('C')
                elif scale_name == 'pentatonic':
                    s = scale.MajorPentatonicScale('C')
                elif scale_name == 'dorian':
                    s = scale.DorianScale('C')
                else:
                    s = scale.MajorScale('C') if scale_name == 'major' else scale.MinorScale('C')
                print(f"  {scale_name}: {[str(p) for p in s.pitches]}")
            except Exception as e:
                print(f"  {scale_name}: Error - {e}")
        
        # Check chord analysis capabilities
        print("\n2. Chord Analysis:")
        test_chords = [
            ['C', 'E', 'G'],      # C major
            ['C', 'E-', 'G'],     # C minor  
            ['C', 'E', 'G', 'B-'],  # C7
            ['C', 'E', 'G', 'B'],   # Cmaj7
        ]
        
        for chord_notes in test_chords:
            try:
                c = chord.Chord(chord_notes)
                print(f"  {chord_notes} -> {c.commonName} ({c.root().name}{c.quality})")
            except Exception as e:
                print(f"  {chord_notes} -> Error: {e}")
        
        # Check Roman numeral analysis
        print("\n3. Roman Numeral Analysis:")
        try:
            # Test progression analysis
            key_c = key.Key('C')
            numerals = ['I', 'vi', 'IV', 'V']
            for numeral in numerals:
                rn = roman.RomanNumeral(numeral, key_c)
                print(f"  {numeral} in C major = {rn.pitches}")
        except Exception as e:
            print(f"  Roman numeral error: {e}")
        
        # Check corpus for genre examples  
        print("\n4. Corpus Genre Examples:")
        try:
            # Search for different styles
            searches = ['folk', 'bach', 'jazz', 'blues']
            for search_term in searches:
                results = corpus.search(search_term)
                print(f"  {search_term}: {len(results)} pieces found")
                if results and len(results) > 0:
                    # Try to get first result
                    first_result = results[0]
                    print(f"    Example: {first_result}")
        except Exception as e:
            print(f"  Corpus search error: {e}")
        
        # Check analysis capabilities
        print("\n5. Analysis Capabilities:")
        try:
            # Create a simple progression
            s = stream.Stream()
            s.append(chord.Chord(['C', 'E', 'G']))
            s.append(chord.Chord(['F', 'A', 'C']))  
            s.append(chord.Chord(['G', 'B', 'D']))
            s.append(chord.Chord(['C', 'E', 'G']))
            
            # Analyze key
            analyzed_key = s.analyze('key')
            print(f"  Key analysis: {analyzed_key}")
            
            # Try other analyses
            for analysis_type in ['ambitus']:
                try:
                    result = s.analyze(analysis_type)
                    print(f"  {analysis_type}: {result}")
                except:
                    print(f"  {analysis_type}: Not available")
                    
        except Exception as e:
            print(f"  Analysis error: {e}")
            
        print("\n✅ music21 exploration complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error exploring music21: {e}")
        return False

def explore_chord_progressions():
    """Explore chord progression capabilities."""
    print("\n=== Exploring Chord Progressions ===")
    
    try:
        from music21 import roman, key, progression
        
        # Common progressions by genre
        progressions = {
            'pop': ['vi', 'IV', 'I', 'V'],  # vi-IV-I-V
            'jazz': ['ii', 'V', 'I'],        # ii-V-I
            'blues': ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'V'],  # 12-bar blues
            'classical': ['I', 'V', 'vi', 'iii', 'IV', 'I', 'IV', 'V']  # Common practice
        }
        
        key_c = key.Key('C')
        
        for genre, prog in progressions.items():
            print(f"\n{genre.title()} progression: {' - '.join(prog)}")
            chords = []
            for numeral in prog:
                try:
                    rn = roman.RomanNumeral(numeral, key_c)
                    chord_symbol = f"{rn.root().name}{rn.quality}"
                    chords.append(chord_symbol)
                except Exception as e:
                    chords.append(f"Error({numeral})")
            print(f"  In C major: {' - '.join(chords)}")
        
        return True
    except Exception as e:
        print(f"❌ Error with progressions: {e}")
        return False

if __name__ == "__main__":
    success1 = explore_music21_genre_knowledge()
    success2 = explore_chord_progressions()
    
    if success1 and success2:
        print("\n🎉 Ready to build Phase 4 with music21 knowledge base!")
    else:
        print("\n⚠️  Some capabilities need investigation.")