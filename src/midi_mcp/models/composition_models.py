# -*- coding: utf-8 -*-
"""Data models for advanced composition features."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum

from .theory_models import Note, Scale, Chord


class SectionType(Enum):
    """Types of song sections."""
    INTRO = "intro"
    VERSE = "verse"
    CHORUS = "chorus"
    BRIDGE = "bridge"
    SOLO = "solo"
    OUTRO = "outro"
    INSTRUMENTAL = "instrumental"
    BREAKDOWN = "breakdown"
    BUILD_UP = "buildup"


class DynamicLevel(Enum):
    """Dynamic levels for orchestration."""
    PP = "pp"
    P = "p"
    MP = "mp"
    MF = "mf"
    F = "f"
    FF = "ff"


class TextureLevel(Enum):
    """Texture density levels for orchestration."""
    THIN = "thin"
    MEDIUM = "medium"
    THICK = "thick"
    VERY_THICK = "very_thick"


@dataclass
class Melody:
    """Represents a melodic line."""
    notes: List[int]  # MIDI note numbers
    rhythm: List[float] = field(default_factory=list)  # Note durations
    phrase_structure: Optional[Dict[str, Any]] = None
    contour: Optional[str] = None  # "ascending", "descending", "arch", etc.
    register: str = "mid"  # "low", "mid", "high"
    
    def __post_init__(self):
        if not self.rhythm:
            # Default to quarter notes if no rhythm specified
            self.rhythm = [1.0] * len(self.notes)


@dataclass
class Motif:
    """Represents a short melodic motif."""
    notes: List[int]  # MIDI note numbers
    rhythm: Optional[List[float]] = None
    intervallic_pattern: Optional[List[int]] = None
    
    def __post_init__(self):
        if self.intervallic_pattern is None and len(self.notes) > 1:
            self.intervallic_pattern = [
                self.notes[i+1] - self.notes[i] 
                for i in range(len(self.notes) - 1)
            ]


@dataclass
class DevelopmentTechnique:
    """Represents a melodic development technique."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MelodicDevelopment:
    """Result of melodic development process."""
    original_motif: Motif
    developed_melody: Melody
    techniques_applied: List[DevelopmentTechnique]
    analysis: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phrase:
    """Represents a musical phrase."""
    melody: Melody
    harmony: List[Dict[str, Any]]  # Chord progression
    structure_type: str  # "period", "sentence", "phrase_group"
    structure_analysis: Dict[str, Any] = field(default_factory=dict)
    cadences: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MelodyVariation:
    """Result of melody variation process."""
    original_melody: List[int]
    varied_melody: Melody
    variation_type: str
    similarity_score: float
    variation_techniques: List[str] = field(default_factory=list)


@dataclass
class VoiceLeadingAnalysis:
    """Analysis of voice leading quality."""
    total_motion: int  # Total semitone movement across all voices
    parallel_motion_count: int
    contrary_motion_count: int
    oblique_motion_count: int
    smoothness_score: float  # 0-1, higher is smoother
    voice_independence: float  # 0-1, higher is more independent


@dataclass
class Section:
    """Represents a song section."""
    type: SectionType
    key: str
    duration: float  # In seconds
    measures: int
    melody: Optional[Melody] = None
    harmony: List[Dict[str, Any]] = field(default_factory=list)
    rhythm: Dict[str, Any] = field(default_factory=dict)
    arrangement: Dict[str, Any] = field(default_factory=dict)
    energy_level: float = 0.5  # 0-1 scale
    characteristics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Transition:
    """Represents a transition between sections."""
    from_section: str
    to_section: str
    type: str  # "smooth", "dramatic", "surprise", "buildup"
    duration: float
    material: Dict[str, Any] = field(default_factory=dict)
    

@dataclass
class SongStructure:
    """Represents complete song structure."""
    genre: str
    sections: List[Section]
    key_plan: Dict[str, Any]
    tempo: int
    time_signature: tuple = (4, 4)
    total_duration: float = 0.0
    
    def __post_init__(self):
        if self.total_duration == 0.0:
            self.total_duration = sum(section.duration for section in self.sections)


@dataclass
class InstrumentPart:
    """Represents a part for a specific instrument."""
    instrument: str
    notes: List[int]
    rhythm: List[float]
    register: str = "mid"
    dynamics: List[DynamicLevel] = field(default_factory=list)
    articulation: List[str] = field(default_factory=list)
    style_characteristics: List[str] = field(default_factory=list)


@dataclass
class CounterMelody:
    """Represents a counter-melody."""
    notes: List[int]
    rhythm: List[float] = field(default_factory=list)
    independence_score: float = 0.0  # How independent from main melody
    complementarity_score: float = 0.0  # How well it complements main melody
    rhythmic_independence_score: float = 0.0


@dataclass
class TexturePoint:
    """Represents texture at a specific point in time."""
    timestamp: float  # Time in seconds
    density: float  # 0-1, how many voices/instruments active
    register_spread: float  # Range of registers used
    target_dynamic: str  # Target dynamic level
    ensemble_balance: Dict[str, float] = field(default_factory=dict)
    active_instruments: List[str] = field(default_factory=list)


@dataclass
class TexturePlan:
    """Represents orchestrated texture changes over time."""
    texture_points: List[TexturePoint]
    overall_arc: str = "static"  # "static", "building", "receding", "wave"


@dataclass
class Arrangement:
    """Represents a complete arrangement."""
    parts: Dict[str, InstrumentPart]  # instrument_name -> part
    ensemble_type: str
    style: str
    texture_plan: Optional[TexturePlan] = None
    mix_balance: Dict[str, float] = field(default_factory=dict)  # instrument -> volume
    arrangement_analysis: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Composition:
    """Base composition data."""
    melody: Dict[str, Any]
    harmony: List[Dict[str, Any]]
    key: str
    tempo: Optional[int] = None
    structure: Optional[Dict[str, Any]] = None


@dataclass 
class CompleteComposition:
    """Represents a complete musical composition."""
    title: str = "Untitled"
    genre: str = ""
    key: str = "C major"
    tempo: int = 120
    time_signature: tuple = (4, 4)
    description: str = ""
    
    # Musical content
    structure: Optional[SongStructure] = None
    melody: Dict[str, Any] = field(default_factory=dict)
    harmony: List[Dict[str, Any]] = field(default_factory=list)
    arrangement: Optional[Arrangement] = None
    
    # Analysis metrics
    overall_energy: float = 0.5  # 0-1 scale
    harmonic_complexity_score: float = 0.5  # 0-1 scale  
    style_characteristics: List[str] = field(default_factory=list)
    
    # Metadata
    duration: float = 0.0
    created_timestamp: Optional[str] = None


@dataclass
class CategoryAnalysis:
    """Analysis of a specific category (melody, harmony, etc.)."""
    score: float  # 0-10 scale
    analysis_details: Dict[str, Any] = field(default_factory=dict)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


@dataclass
class ImprovementSuggestion:
    """Represents a suggested improvement."""
    category: str  # "melody", "harmony", "rhythm", "form", "arrangement"
    priority: str  # "high", "medium", "low"
    suggestion: str  # Description of the improvement
    specific_measures: Optional[List[int]] = None  # Which measures to change
    

@dataclass
class CompositionAnalysis:
    """Complete analysis of a composition."""
    category_scores: Dict[str, CategoryAnalysis]  # category -> analysis
    improvement_suggestions: List[ImprovementSuggestion]
    overall_assessment: str = ""
    analysis_timestamp: Optional[str] = None


@dataclass
class RefinementChange:
    """Represents a change made during refinement."""
    category: str
    description: str
    before: Any
    after: Any
    measures_affected: Optional[List[int]] = None


@dataclass
class RefinementResult:
    """Result of composition refinement process."""
    refined_composition: CompleteComposition
    changes_made: List[RefinementChange]
    improvement_metrics: Dict[str, float] = field(default_factory=dict)
    coherence_maintained: bool = True
    style_consistency_score: float = 0.0