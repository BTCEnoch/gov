"""Schemas for visual traits and aspects."""
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class FormAspects:
    """Form-related visual aspects."""
    base_form: str
    description: str
    complexity: int
    detail_density: str

@dataclass
class ColorPattern:
    """Color pattern characteristics."""
    type: str
    speed: int

@dataclass
class ColorAspects:
    """Color-related visual aspects."""
    primary_color: List[int]
    energy_type: str
    vibration: str
    pattern: ColorPattern

@dataclass
class GeometryMotion:
    """Geometric motion characteristics."""
    type: str
    speed: int
    complexity: int

@dataclass
class GeometryAspects:
    """Geometry-related visual aspects."""
    base_pattern: str
    dimension: int
    symmetry_points: int
    motion: GeometryMotion

@dataclass
class TemporalCycle:
    """Temporal cycle characteristics."""
    type: str
    duration: int
    phase: float

@dataclass
class TemporalAspects:
    """Time-related visual aspects."""
    primary_cycle: TemporalCycle
    flow_type: str
    stability: float
    variations: List[str]

@dataclass
class EnergyFlow:
    """Energy flow characteristics."""
    direction: str
    intensity: float
    frequency: float

@dataclass
class EnergyAspects:
    """Energy-related visual aspects."""
    signature_type: str
    primary_flow: EnergyFlow
    resonance: List[str]
    harmonics: List[float]

@dataclass
class VisualTraits:
    """Visual traits and aspects of a governor."""
    form: FormAspects
    color: ColorAspects
    geometry: GeometryAspects
    temporal: TemporalAspects
    energy: EnergyAspects 