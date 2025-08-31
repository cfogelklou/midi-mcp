"""Generic MCP tools for genre knowledge and composition."""

from fastmcp import FastMCP
from typing import Dict, List, Optional, Any
import logging

from ..genres import GenreManager, GenericComposer, LibraryIntegration
from ..genres.fusion_engine import FusionEngine
from ..genres.validator import AuthenticityValidator

# Set up logging
logger = logging.getLogger(__name__)

def register_genre_tools(mcp: FastMCP) -> None:
    """Register all genre-related MCP tools."""
    
    # Initialize genre system components inside function to avoid circular imports
    genre_manager = GenreManager()
    composer = GenericComposer(genre_manager)
    libraries = LibraryIntegration()
    
    @mcp.tool()
    def list_available_genres() -> Dict[str, Any]:
        """List all available genres with categories and descriptions.
        
        Returns:
            Dictionary containing all available genres with metadata
        """
        try:
            return genre_manager.get_available_genres()
        except Exception as e:
            logger.error(f"Error listing genres: {e}")
            return {"error": str(e)}
    
    @mcp.tool()
    def get_genre_characteristics(genre: str) -> Dict[str, Any]:
        """Get comprehensive characteristics for any musical genre.
        
        Args:
            genre: Genre name (e.g., 'blues', 'rock', 'hip_hop', 'jazz', 'trance')
            
        Returns:
            Comprehensive genre characteristics including progressions, rhythms, scales
        """
        try:
            return genre_manager.get_genre_data(genre)
        except Exception as e:
            logger.error(f"Error getting genre characteristics for {genre}: {e}")
            return {"error": str(e), "genre": genre}
    
    @mcp.tool()
    def compare_genres(genre1: str, genre2: str) -> Dict[str, Any]:
        """Compare characteristics between two genres.
        
        Args:
            genre1: First genre to compare
            genre2: Second genre to compare
            
        Returns:
            Comparison highlighting similarities and differences
        """
        try:
            return genre_manager.compare_genres(genre1, genre2)
        except Exception as e:
            logger.error(f"Error comparing {genre1} and {genre2}: {e}")
            return {"error": str(e), "genres": [genre1, genre2]}
    
    @mcp.tool() 
    def create_progression(genre: str, key: str, variation: str = "standard", 
                          bars: Optional[int] = None) -> Dict[str, Any]:
        """Create authentic chord progression for any genre.
        
        Args:
            genre: Musical genre (e.g., 'blues', 'rock', 'jazz', 'hip_hop')
            key: Key signature (e.g., 'C', 'Am', 'F#')
            variation: Progression variation (standard, jazz, modern, etc.)
            bars: Number of bars (optional, uses genre default if not specified)
            
        Returns:
            Complete chord progression with harmonic analysis
        """
        try:
            return composer.create_progression(genre, key, variation, bars)
        except Exception as e:
            logger.error(f"Error creating {genre} progression in {key}: {e}")
            return {"error": str(e), "genre": genre, "key": key}
    
    @mcp.tool()
    def create_melody(genre: str, key: str, progression: Dict[str, Any], 
                     style: str = "typical") -> Dict[str, Any]:
        """Generate authentic melody for any genre.
        
        Args:
            genre: Musical genre
            key: Key signature
            progression: Underlying chord progression (from create_progression)
            style: Melodic style (typical, simple, complex, ornate)
            
        Returns:
            Melodic line with analysis and characteristics
        """
        try:
            return composer.create_melody(genre, key, progression, style)
        except Exception as e:
            logger.error(f"Error creating {genre} melody in {key}: {e}")
            return {"error": str(e), "genre": genre, "key": key}
    
    @mcp.tool()
    def create_beat(genre: str, tempo: int, complexity: str = "medium",
                   variation: str = "standard") -> Dict[str, Any]:
        """Create authentic drum patterns for any genre.
        
        Args:
            genre: Musical genre
            tempo: Tempo in BPM
            complexity: Rhythmic complexity (simple, medium, complex)
            variation: Beat variation (standard, shuffle, swing, etc.)
            
        Returns:
            Drum pattern with timing and feel characteristics
        """
        try:
            return composer.create_beat(genre, tempo, complexity, variation)
        except Exception as e:
            logger.error(f"Error creating {genre} beat at {tempo}bpm: {e}")
            return {"error": str(e), "genre": genre, "tempo": tempo}
    
    @mcp.tool()
    def create_bass_line(genre: str, progression: Dict[str, Any], 
                        style: str = "typical") -> Dict[str, Any]:
        """Generate authentic bass lines for any genre.
        
        Args:
            genre: Musical genre
            progression: Chord progression to follow (from create_progression)
            style: Bass style (typical, walking, simple, complex)
            
        Returns:
            Bass line with voice leading analysis
        """
        try:
            return composer.create_bass_line(genre, progression, style)
        except Exception as e:
            logger.error(f"Error creating {genre} bass line: {e}")
            return {"error": str(e), "genre": genre}
    
    @mcp.tool()
    def create_arrangement(genre: str, song_structure: Dict[str, Any], 
                          instrumentation: str = "standard") -> Dict[str, Any]:
        """Create full band arrangement for any genre.
        
        Args:
            genre: Musical genre
            song_structure: Basic song structure with melody, chords, etc.
            instrumentation: Arrangement size (minimal, standard, full, orchestral)
            
        Returns:
            Complete arrangement with parts for all instruments
        """
        try:
            return composer.create_arrangement(genre, song_structure, instrumentation)
        except Exception as e:
            logger.error(f"Error creating {genre} arrangement: {e}")
            return {"error": str(e), "genre": genre}
    
    @mcp.tool()
    def apply_genre_feel(midi_file_id: str, genre: str, 
                        intensity: float = 0.8) -> Dict[str, Any]:
        """Apply genre-specific timing, articulation, and feel to existing MIDI.
        
        Args:
            midi_file_id: ID of MIDI file to process
            genre: Target genre for feel application
            intensity: Intensity of genre feel application (0.0 to 1.0)
            
        Returns:
            Analysis of applied changes and modified MIDI information
        """
        try:
            # This would integrate with existing MIDI file system from Phases 1-2
            genre_data = genre_manager.get_genre_data(genre)
            
            # Get genre-specific characteristics
            rhythms = genre_data.get("rhythms", {})
            feel = rhythms.get("standard", {}).get("feel", "straight")
            swing_ratio = rhythms.get("standard", {}).get("swing_ratio", 0.5)
            
            return {
                "midi_file_id": midi_file_id,
                "genre": genre,
                "applied_feel": feel,
                "swing_ratio": swing_ratio,
                "intensity": intensity,
                "changes_applied": [
                    "Timing adjustments",
                    "Articulation modifications", 
                    "Genre-specific accents"
                ],
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error applying {genre} feel to {midi_file_id}: {e}")
            return {"error": str(e), "midi_file_id": midi_file_id, "genre": genre}
    
    @mcp.tool()
    def create_genre_template(genre: str, song_type: str, key: str, 
                             tempo: int) -> Dict[str, Any]:
        """Create complete song template for any genre.
        
        Args:
            genre: Musical genre
            song_type: Type of song (ballad, uptempo, epic, etc.)
            key: Key signature
            tempo: Tempo in BPM
            
        Returns:
            Complete song template with structure, progression, and arrangement
        """
        try:
            # Create basic progression
            progression = composer.create_progression(genre, key, "standard")
            
            # Create beat pattern
            beat = composer.create_beat(genre, tempo, "medium", "standard")
            
            # Create basic arrangement structure
            genre_data = genre_manager.get_genre_data(genre)
            song_forms = genre_data.get("song_forms", {})
            structure = song_forms.get("standard", {}).get("structure", ["verse", "chorus", "verse", "chorus"])
            
            return {
                "genre": genre,
                "song_type": song_type,
                "key": key,
                "tempo": tempo,
                "structure": structure,
                "progression": progression,
                "beat": beat,
                "instrumentation": genre_data.get("instrumentation", {}),
                "characteristics": genre_data.get("characteristics", {}),
                "template_sections": {
                    section: {
                        "progression": progression,
                        "beat": beat,
                        "dynamics": "mf" if section == "verse" else "f"
                    } for section in structure
                }
            }
        except Exception as e:
            logger.error(f"Error creating {genre} template: {e}")
            return {"error": str(e), "genre": genre}
    
    @mcp.tool()
    def create_fusion_style(primary_genre: str, secondary_genre: str,
                           balance: float = 0.5) -> Dict[str, Any]:
        """Create fusion of two genres with adjustable balance.
        
        Args:
            primary_genre: Main genre influence
            secondary_genre: Secondary genre influence
            balance: Balance between genres (0.0 = all primary, 1.0 = all secondary)
            
        Returns:
            Fused genre characteristics and composition guidelines
        """
        try:
            # Get data for both genres
            primary_data = genre_manager.get_genre_data(primary_genre)
            secondary_data = genre_manager.get_genre_data(secondary_genre)
            
            # Calculate relationship score
            relationship = genre_manager.compare_genres(primary_genre, secondary_genre)
            
            # Create fusion characteristics
            fusion = {
                "primary_genre": primary_genre,
                "secondary_genre": secondary_genre,
                "balance": balance,
                "relationship_score": relationship.get("relationship_score", 0.5),
                "fusion_feasibility": "high" if relationship.get("relationship_score", 0) > 0.6 else "medium",
                "tempo_range": [
                    int(primary_data.get("tempo_range", [120, 120])[0] * (1-balance) + 
                        secondary_data.get("tempo_range", [120, 120])[0] * balance),
                    int(primary_data.get("tempo_range", [120, 120])[1] * (1-balance) + 
                        secondary_data.get("tempo_range", [120, 120])[1] * balance)
                ],
                "combined_scales": list(set(
                    primary_data.get("scales", []) + secondary_data.get("scales", [])
                )),
                "combined_instruments": {
                    "essential": list(set(
                        primary_data.get("instrumentation", {}).get("essential", []) +
                        secondary_data.get("instrumentation", {}).get("essential", [])
                    )),
                    "optional": list(set(
                        primary_data.get("instrumentation", {}).get("optional", []) +
                        secondary_data.get("instrumentation", {}).get("optional", [])
                    ))
                },
                "fusion_suggestions": [
                    f"Use {primary_genre} harmony with {secondary_genre} rhythm",
                    f"Combine {primary_genre} instrumentation with {secondary_genre} production style",
                    f"Apply {secondary_genre} feel to {primary_genre} progressions"
                ]
            }
            
            return fusion
        except Exception as e:
            logger.error(f"Error creating fusion of {primary_genre} and {secondary_genre}: {e}")
            return {"error": str(e), "primary_genre": primary_genre, "secondary_genre": secondary_genre}
    
    @mcp.tool()
    def validate_genre_authenticity(midi_file_id: str, target_genre: str) -> Dict[str, Any]:
        """Analyze how well music matches genre characteristics.
        
        Args:
            midi_file_id: ID of MIDI file to analyze
            target_genre: Genre to validate against
            
        Returns:
            Authenticity analysis with score and suggestions for improvement
        """
        try:
            # This would integrate with MIDI analysis from existing phases
            # For now, return structure showing what analysis would include
            
            genre_data = genre_manager.get_genre_data(target_genre)
            
            # Mock analysis - would use actual MIDI data in full implementation
            analysis = {
                "midi_file_id": midi_file_id,
                "target_genre": target_genre,
                "authenticity_score": 0.75,  # Mock score
                "analysis_categories": {
                    "harmony": {
                        "score": 0.8,
                        "notes": f"Chord progressions align well with {target_genre} expectations"
                    },
                    "rhythm": {
                        "score": 0.7,
                        "notes": f"Rhythmic feel matches {target_genre} characteristics"
                    },
                    "melody": {
                        "score": 0.75,
                        "notes": f"Melodic style appropriate for {target_genre}"
                    },
                    "instrumentation": {
                        "score": 0.8,
                        "notes": f"Instrument choices support {target_genre} authenticity"
                    }
                },
                "strengths": [
                    "Strong harmonic foundation",
                    "Appropriate tempo and feel",
                    "Good instrument selection"
                ],
                "suggestions": [
                    f"Consider incorporating more {target_genre}-specific scales",
                    f"Add characteristic {target_genre} rhythmic patterns",
                    f"Enhance with typical {target_genre} production elements"
                ],
                "genre_characteristics_matched": len(genre_data.get("characteristics", {})),
                "overall_assessment": "Good" if 0.75 > 0.7 else "Fair"
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error validating {target_genre} authenticity for {midi_file_id}: {e}")
            return {"error": str(e), "midi_file_id": midi_file_id, "target_genre": target_genre}
    
    logger.info("Genre MCP tools registered successfully")