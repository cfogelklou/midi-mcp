"""Creates full arrangements from musical parts."""

from typing import Dict, List, Any

class ArrangementEngine:
    """Creates full arrangements."""

    def select_instruments_for_arrangement(self, genre_data: Dict[str, Any], 
                                          instrumentation: str) -> List[str]:
        """Select instruments based on genre and arrangement level."""
        inst_data = genre_data.get("instrumentation", {})
        
        instruments = []
        
        # Always include essential instruments
        instruments.extend(inst_data.get("essential", ["piano"]))
        
        if instrumentation in ["standard", "full", "orchestral"]:
            instruments.extend(inst_data.get("typical", ["bass", "drums"]))
        
        if instrumentation in ["full", "orchestral"]:
            instruments.extend(inst_data.get("optional", ["guitar"]))
        
        return list(set(instruments))  # Remove duplicates

    def determine_texture(self, genre: str, instrumentation: str) -> str:
        """Determine arrangement texture based on genre and instrumentation."""
        texture_map = {
            ("blues", "minimal"): "sparse",
            ("blues", "standard"): "medium", 
            ("rock", "standard"): "dense",
            ("jazz", "standard"): "complex",
            ("ambient", "standard"): "layered"
        }
        
        return texture_map.get((genre, instrumentation), "medium")

    def create_dynamic_plan(self, song_structure: Dict[str, Any], genre: str) -> List[str]:
        """Create dynamic plan for the arrangement."""
        # Simplified dynamic planning
        sections = song_structure.get("sections", ["verse", "chorus", "verse", "chorus"])
        dynamics = []
        
        for section in sections:
            if section == "verse":
                dynamics.append("mp")  # mezzo-piano
            elif section == "chorus":
                dynamics.append("f")   # forte
            elif section == "bridge":
                dynamics.append("mf")  # mezzo-forte
            else:
                dynamics.append("mp")
        
        return dynamics

    def determine_instrument_role(self, instrument: str, genre: str) -> str:
        """Determine the role of an instrument in a genre."""
        role_map = {
            "piano": "harmonic_support",
            "guitar": "harmonic_lead",
            "bass": "harmonic_foundation", 
            "drums": "rhythmic_foundation",
            "vocals": "melodic_lead"
        }
        return role_map.get(instrument, "supporting")

    def determine_pattern_type(self, instrument: str, genre: str) -> str:
        """Determine playing pattern for instrument in genre."""
        if instrument == "piano":
            if genre in ["jazz", "blues"]:
                return "comping"
            elif genre in ["rock", "pop"]:
                return "chordal"
        elif instrument == "bass":
            if genre == "jazz":
                return "walking"
            else:
                return "root_based"
        
        return "standard"

    def get_instrument_articulation(self, instrument: str, genre: str) -> str:
        """Get appropriate articulation for instrument in genre."""
        if genre == "jazz":
            return "swing"
        elif genre == "rock":
            return "staccato"
        elif genre == "blues":
            return "legato"
        else:
            return "normal"
