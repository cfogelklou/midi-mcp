"""Core genre management system."""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

class GenreManager:
    """Manages genre hierarchies, relationships, and characteristics."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize the genre manager.
        
        Args:
            data_dir: Directory containing genre data files
        """
        if data_dir is None:
            # Default to project data directory
            current_dir = Path(__file__).parent.parent.parent.parent
            data_dir = current_dir / "data" / "genres"
        
        self.data_dir = Path(data_dir)
        self._genre_hierarchy = None
        self._genre_data_cache = {}
        
        # Load genre hierarchy
        self._load_genre_hierarchy()
    
    def _load_genre_hierarchy(self) -> None:
        """Load the genre hierarchy from JSON file."""
        hierarchy_file = self.data_dir / "genre_hierarchy.json"
        
        if hierarchy_file.exists():
            with open(hierarchy_file, 'r') as f:
                self._genre_hierarchy = json.load(f)
        else:
            # Create default hierarchy if file doesn't exist
            self._genre_hierarchy = self._create_default_hierarchy()
            self._save_genre_hierarchy()
    
    def _create_default_hierarchy(self) -> Dict[str, Any]:
        """Create the default genre hierarchy."""
        return {
            "genres": {
                "blues": {
                    "parent": None,
                    "subgenres": ["chicago_blues", "delta_blues", "electric_blues"],
                    "related": ["rock", "jazz", "r_and_b"]
                },
                "rock": {
                    "parent": None,
                    "subgenres": ["classic_rock", "hard_rock", "punk", "metal"],
                    "related": ["blues", "pop", "country"]
                },
                "hip_hop": {
                    "parent": None,
                    "subgenres": ["boom_bap", "trap", "lo_fi", "drill", "old_school"],
                    "related": ["r_and_b", "funk", "jazz"]
                },
                "jazz": {
                    "parent": None,
                    "subgenres": ["bebop", "cool_jazz", "fusion", "swing"],
                    "related": ["blues", "r_and_b", "latin"]
                },
                "country": {
                    "parent": None,
                    "subgenres": ["bluegrass", "honky_tonk", "outlaw_country"],
                    "related": ["rock", "blues", "folk"]
                },
                "electronic": {
                    "parent": None,
                    "subgenres": ["house", "techno", "trance", "ambient"],
                    "related": ["pop", "hip_hop"]
                },
                "trance": {
                    "parent": "electronic",
                    "subgenres": ["progressive_trance", "uplifting_trance", "psytrance", "tech_trance"],
                    "related": ["house", "techno", "ambient"]
                },
                "pop": {
                    "parent": None,
                    "subgenres": ["dance_pop", "indie_pop", "electropop", "synth_pop"],
                    "related": ["rock", "r_and_b", "electronic"]
                },
                "ambient": {
                    "parent": "electronic",
                    "subgenres": ["dark_ambient", "drone", "new_age", "space_ambient"],
                    "related": ["trance", "downtempo", "experimental"]
                },
                "k_pop": {
                    "parent": "pop",
                    "subgenres": ["k_pop_ballad", "k_pop_dance", "k_pop_rap", "k_pop_r&b"],
                    "related": ["pop", "hip_hop", "r_and_b", "electronic"]
                }
            }
        }
    
    def _save_genre_hierarchy(self) -> None:
        """Save the genre hierarchy to JSON file."""
        hierarchy_file = self.data_dir / "genre_hierarchy.json"
        hierarchy_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(hierarchy_file, 'w') as f:
            json.dump(self._genre_hierarchy, f, indent=2)
    
    def get_available_genres(self) -> Dict[str, Any]:
        """Get all available genres with categories and descriptions.
        
        Returns:
            Dictionary of genres with metadata
        """
        genres = {}
        
        for genre_name, genre_info in self._genre_hierarchy["genres"].items():
            genres[genre_name] = {
                "parent": genre_info.get("parent"),
                "subgenres": genre_info.get("subgenres", []),
                "related": genre_info.get("related", []),
                "description": self._get_genre_description(genre_name)
            }
        
        return {
            "genres": genres,
            "total_count": len(genres),
            "main_genres": [g for g, info in genres.items() if info["parent"] is None],
            "subgenres": [g for g, info in genres.items() if info["parent"] is not None]
        }
    
    def get_genre_data(self, genre: str) -> Dict[str, Any]:
        """Get comprehensive data for a specific genre.
        
        Args:
            genre: Genre name
            
        Returns:
            Genre data including characteristics, patterns, and relationships
        """
        if genre in self._genre_data_cache:
            return self._genre_data_cache[genre]
        
        # Load genre data from file
        genre_file = self.data_dir / f"{genre}.json"
        
        if genre_file.exists():
            with open(genre_file, 'r') as f:
                genre_data = json.load(f)
        else:
            # Create default genre data
            genre_data = self._create_default_genre_data(genre)
            self._save_genre_data(genre, genre_data)
        
        # Add hierarchy information
        if genre in self._genre_hierarchy["genres"]:
            genre_data.update(self._genre_hierarchy["genres"][genre])
        
        self._genre_data_cache[genre] = genre_data
        return genre_data
    
    def _create_default_genre_data(self, genre: str) -> Dict[str, Any]:
        """Create default data structure for a genre."""
        return {
            "name": genre,
            "tempo_range": [60, 180],
            "key_preferences": ["major", "minor"],
            "progressions": {
                "standard": {
                    "pattern": ["I", "V", "vi", "IV"],
                    "bars": 4,
                    "variations": []
                }
            },
            "rhythms": {
                "standard": {
                    "feel": "straight",
                    "emphasis": [1, 3],
                    "subdivision": "quarter"
                }
            },
            "scales": ["major", "minor"],
            "instrumentation": {
                "essential": ["piano"],
                "typical": ["bass", "drums"],
                "optional": ["guitar", "vocals"]
            },
            "characteristics": {
                "energy": "medium",
                "complexity": "medium",
                "mood": "neutral"
            }
        }
    
    def _save_genre_data(self, genre: str, data: Dict[str, Any]) -> None:
        """Save genre data to file."""
        genre_file = self.data_dir / f"{genre}.json"
        genre_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(genre_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_genre_description(self, genre: str) -> str:
        """Get a description for a genre."""
        descriptions = {
            "blues": "Traditional American blues with 12-bar progressions and blues scales",
            "rock": "Rock music with electric guitars, strong rhythms, and power chords",
            "hip_hop": "Urban music with rhythmic speech over strong beats",
            "jazz": "Sophisticated harmony with improvisation and swing rhythms",
            "country": "American folk music with storytelling and acoustic instruments",
            "electronic": "Synthesized music with electronic production techniques",
            "trance": "Electronic dance music with hypnotic rhythms and build-ups",
            "pop": "Popular music designed for mass appeal and radio play",
            "ambient": "Atmospheric music focused on texture and mood",
            "k_pop": "Korean pop music with polished production and catchy hooks"
        }
        return descriptions.get(genre, f"{genre.replace('_', ' ').title()} music")
    
    def get_progression_patterns(self, genre: str) -> Dict[str, Any]:
        """Get chord progression patterns for a genre."""
        genre_data = self.get_genre_data(genre)
        return genre_data.get("progressions", {})
    
    def get_rhythm_patterns(self, genre: str) -> Dict[str, Any]:
        """Get rhythm patterns for a genre."""
        genre_data = self.get_genre_data(genre)
        return genre_data.get("rhythms", {})
    
    def get_instrumentation(self, genre: str) -> Dict[str, List[str]]:
        """Get typical instrumentation for a genre."""
        genre_data = self.get_genre_data(genre)
        return genre_data.get("instrumentation", {})
    
    def compare_genres(self, genre1: str, genre2: str) -> Dict[str, Any]:
        """Compare characteristics between two genres.
        
        Args:
            genre1: First genre to compare
            genre2: Second genre to compare
            
        Returns:
            Comparison data highlighting similarities and differences
        """
        data1 = self.get_genre_data(genre1)
        data2 = self.get_genre_data(genre2)
        
        comparison = {
            "genres": [genre1, genre2],
            "similarities": [],
            "differences": [],
            "tempo_comparison": {
                genre1: data1.get("tempo_range", [120, 120]),
                genre2: data2.get("tempo_range", [120, 120])
            },
            "common_progressions": self._find_common_progressions(data1, data2),
            "instrumentation_overlap": self._find_instrumentation_overlap(data1, data2),
            "relationship_score": self._calculate_relationship_score(genre1, genre2)
        }
        
        return comparison
    
    def _find_common_progressions(self, data1: Dict, data2: Dict) -> List[str]:
        """Find common chord progressions between two genres."""
        progs1 = set(data1.get("progressions", {}).keys())
        progs2 = set(data2.get("progressions", {}).keys())
        return list(progs1.intersection(progs2))
    
    def _find_instrumentation_overlap(self, data1: Dict, data2: Dict) -> List[str]:
        """Find common instruments between two genres."""
        inst1 = data1.get("instrumentation", {})
        inst2 = data2.get("instrumentation", {})
        
        all_inst1 = set()
        all_inst2 = set()
        
        for category in ["essential", "typical", "optional"]:
            all_inst1.update(inst1.get(category, []))
            all_inst2.update(inst2.get(category, []))
        
        return list(all_inst1.intersection(all_inst2))
    
    def _calculate_relationship_score(self, genre1: str, genre2: str) -> float:
        """Calculate how related two genres are (0.0 to 1.0)."""
        if genre1 == genre2:
            return 1.0
        
        # Check direct relationships
        genre1_info = self._genre_hierarchy["genres"].get(genre1, {})
        genre2_info = self._genre_hierarchy["genres"].get(genre2, {})
        
        if genre2 in genre1_info.get("related", []):
            return 0.8
        if genre1 in genre2_info.get("related", []):
            return 0.8
        
        # Check parent-child relationships
        if genre1_info.get("parent") == genre2 or genre2_info.get("parent") == genre1:
            return 0.9
        
        # Check sibling relationships (same parent)
        if (genre1_info.get("parent") and 
            genre1_info.get("parent") == genre2_info.get("parent")):
            return 0.7
        
        return 0.1  # Distant relationship