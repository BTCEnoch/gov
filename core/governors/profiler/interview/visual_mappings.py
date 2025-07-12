"""Visual aspect mappings and transformations."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class ColorMapping:
    """Color mapping with RGB values and associations."""
    rgb: Tuple[int, int, int]
    energy: str
    vibration: str
    associations: List[str]

@dataclass
class FormMapping:
    """Form mapping with descriptions and characteristics."""
    base_form: str
    description: str
    characteristics: List[str]
    interactions: List[str]

@dataclass
class GeometryMapping:
    """Sacred geometry mapping with properties."""
    base_pattern: str
    dimension: int
    symmetry_points: int
    properties: List[str]
    energy_multiplier: float

@dataclass
class TemporalMapping:
    """Temporal pattern mapping with characteristics."""
    cycle_type: str
    base_duration: int
    stability_factor: float
    variations: List[str]
    effects: List[str]

@dataclass
class EnergyMapping:
    """Energy signature mapping with characteristics."""
    signature_type: str
    base_frequency: float
    resonance_patterns: List[str]
    harmonic_series: List[float]
    effects: List[str]

class VisualMappings:
    """Manages mappings for visual aspects."""
    
    # Color mappings
    COLORS = {
        "golden": ColorMapping(
            rgb=(255, 215, 0),
            energy="solar",
            vibration="high",
            associations=["divine light", "enlightenment", "wisdom"]
        ),
        "silver": ColorMapping(
            rgb=(192, 192, 192),
            energy="lunar",
            vibration="medium",
            associations=["reflection", "purification", "clarity"]
        ),
        "azure": ColorMapping(
            rgb=(0, 127, 255),
            energy="celestial",
            vibration="high",
            associations=["truth", "clarity", "expansion"]
        ),
        "emerald": ColorMapping(
            rgb=(0, 168, 107),
            energy="natural",
            vibration="medium",
            associations=["growth", "healing", "abundance"]
        ),
        "crimson": ColorMapping(
            rgb=(220, 20, 60),
            energy="vital",
            vibration="intense",
            associations=["power", "transformation", "vitality"]
        ),
        "violet": ColorMapping(
            rgb=(138, 43, 226),
            energy="spiritual",
            vibration="very_high",
            associations=["mystery", "transmutation", "higher wisdom"]
        ),
        "obsidian": ColorMapping(
            rgb=(0, 0, 0),
            energy="void",
            vibration="deep",
            associations=["protection", "absorption", "grounding"]
        )
    }
    
    # Form mappings
    FORMS = {
        "geometric": FormMapping(
            base_form="geometric",
            description="Pure geometric forms with precise mathematical proportions",
            characteristics=["precise", "structured", "mathematical"],
            interactions=["pattern_matching", "geometric_alignment"]
        ),
        "organic": FormMapping(
            base_form="organic",
            description="Flowing, natural forms reminiscent of living structures",
            characteristics=["flowing", "adaptive", "growing"],
            interactions=["natural_harmony", "life_force"]
        ),
        "abstract": FormMapping(
            base_form="abstract",
            description="Non-representational forms that defy conventional categorization",
            characteristics=["unconventional", "transcendent", "fluid"],
            interactions=["reality_bending", "perception_shift"]
        ),
        "crystalline": FormMapping(
            base_form="crystalline",
            description="Faceted, crystal-like structures with regular patterns",
            characteristics=["faceted", "refractive", "structured"],
            interactions=["light_refraction", "energy_amplification"]
        ),
        "fluid": FormMapping(
            base_form="fluid",
            description="Liquid-like forms in constant smooth motion",
            characteristics=["flowing", "adaptable", "dynamic"],
            interactions=["flow_states", "transmutation"]
        ),
        "composite": FormMapping(
            base_form="composite",
            description="Complex forms combining multiple form types",
            characteristics=["complex", "integrated", "multifaceted"],
            interactions=["form_synthesis", "pattern_integration"]
        )
    }
    
    # Geometry mappings
    GEOMETRIES = {
        "flower_of_life": GeometryMapping(
            base_pattern="flower_of_life",
            dimension=2,
            symmetry_points=6,
            properties=["creation", "unity", "interconnection"],
            energy_multiplier=1.5
        ),
        "merkaba": GeometryMapping(
            base_pattern="merkaba",
            dimension=3,
            symmetry_points=8,
            properties=["ascension", "protection", "transformation"],
            energy_multiplier=2.0
        ),
        "metatron_cube": GeometryMapping(
            base_pattern="metatron_cube",
            dimension=3,
            symmetry_points=13,
            properties=["creation", "balance", "sacred geometry"],
            energy_multiplier=2.5
        ),
        "sri_yantra": GeometryMapping(
            base_pattern="sri_yantra",
            dimension=2,
            symmetry_points=9,
            properties=["manifestation", "cosmic unity", "divine feminine"],
            energy_multiplier=2.0
        ),
        "torus": GeometryMapping(
            base_pattern="torus",
            dimension=3,
            symmetry_points=-1,  # Infinite symmetry
            properties=["flow", "self-sustaining", "infinite"],
            energy_multiplier=1.8
        ),
        "vesica_piscis": GeometryMapping(
            base_pattern="vesica_piscis",
            dimension=2,
            symmetry_points=2,
            properties=["creation", "duality", "birth"],
            energy_multiplier=1.2
        )
    }
    
    # Temporal mappings
    TEMPORAL = {
        "solar": TemporalMapping(
            cycle_type="solar",
            base_duration=24,
            stability_factor=0.9,
            variations=["dawn", "noon", "dusk", "midnight"],
            effects=["illumination", "vitality", "clarity"]
        ),
        "lunar": TemporalMapping(
            cycle_type="lunar",
            base_duration=28,
            stability_factor=0.8,
            variations=["new", "waxing", "full", "waning"],
            effects=["intuition", "transformation", "mystery"]
        ),
        "celestial": TemporalMapping(
            cycle_type="celestial",
            base_duration=365,
            stability_factor=0.95,
            variations=["spring", "summer", "autumn", "winter"],
            effects=["cosmic alignment", "seasonal power", "celestial harmony"]
        ),
        "quantum": TemporalMapping(
            cycle_type="quantum",
            base_duration=1,
            stability_factor=0.5,
            variations=["superposition", "entanglement", "collapse"],
            effects=["reality manipulation", "probability shift", "quantum resonance"]
        ),
        "eternal": TemporalMapping(
            cycle_type="eternal",
            base_duration=-1,  # Infinite duration
            stability_factor=1.0,
            variations=["timeless", "infinite", "absolute"],
            effects=["time transcendence", "eternal presence", "infinite wisdom"]
        ),
        "spiral": TemporalMapping(
            cycle_type="spiral",
            base_duration=144,
            stability_factor=0.7,
            variations=["ascending", "descending", "expanding", "contracting"],
            effects=["evolution", "transformation", "cyclic progression"]
        )
    }
    
    # Energy mappings
    ENERGY = {
        "elemental": EnergyMapping(
            signature_type="elemental",
            base_frequency=432.0,
            resonance_patterns=["earth", "water", "fire", "air", "spirit"],
            harmonic_series=[1.0, 1.5, 2.0, 2.5, 3.0],
            effects=["elemental attunement", "natural harmony", "primal force"]
        ),
        "celestial": EnergyMapping(
            signature_type="celestial",
            base_frequency=528.0,
            resonance_patterns=["solar", "lunar", "stellar", "planetary", "cosmic"],
            harmonic_series=[1.0, 1.618, 2.236, 2.718, 3.141],
            effects=["cosmic alignment", "celestial power", "astral resonance"]
        ),
        "ethereal": EnergyMapping(
            signature_type="ethereal",
            base_frequency=396.0,
            resonance_patterns=["light", "shadow", "void", "presence", "absence"],
            harmonic_series=[1.0, 1.414, 1.732, 2.0, 2.236],
            effects=["ethereal manifestation", "spiritual presence", "divine connection"]
        ),
        "quantum": EnergyMapping(
            signature_type="quantum",
            base_frequency=417.0,
            resonance_patterns=["wave", "particle", "field", "force", "potential"],
            harmonic_series=[1.0, 1.259, 1.587, 2.0, 2.520],
            effects=["quantum entanglement", "probability manipulation", "reality shift"]
        ),
        "primordial": EnergyMapping(
            signature_type="primordial",
            base_frequency=369.0,
            resonance_patterns=["chaos", "order", "creation", "destruction", "balance"],
            harmonic_series=[1.0, 1.333, 1.777, 2.369, 3.157],
            effects=["primal force", "fundamental power", "cosmic balance"]
        ),
        "transcendent": EnergyMapping(
            signature_type="transcendent",
            base_frequency=639.0,
            resonance_patterns=["unity", "duality", "trinity", "infinity", "eternity"],
            harmonic_series=[1.0, 1.618, 2.618, 4.236, 6.854],
            effects=["transcendence", "enlightenment", "ultimate reality"]
        )
    }
    
    @classmethod
    def get_color_mapping(cls, color: str) -> Optional[ColorMapping]:
        """Get color mapping by name."""
        return cls.COLORS.get(color.lower())
        
    @classmethod
    def get_form_mapping(cls, form: str) -> Optional[FormMapping]:
        """Get form mapping by name."""
        return cls.FORMS.get(form.lower())
        
    @classmethod
    def get_geometry_mapping(cls, geometry: str) -> Optional[GeometryMapping]:
        """Get geometry mapping by name."""
        return cls.GEOMETRIES.get(geometry.lower())
        
    @classmethod
    def get_color_rgb(cls, color: str) -> Tuple[int, int, int]:
        """Get RGB values for a color."""
        mapping = cls.get_color_mapping(color)
        return mapping.rgb if mapping else (0, 0, 0)
        
    @classmethod
    def get_form_description(cls, form: str) -> str:
        """Get description for a form type."""
        mapping = cls.get_form_mapping(form)
        return mapping.description if mapping else ""
        
    @classmethod
    def get_geometry_properties(cls, geometry: str) -> List[str]:
        """Get properties for a geometric pattern."""
        mapping = cls.get_geometry_mapping(geometry)
        return mapping.properties if mapping else [] 
        
    @classmethod
    def get_temporal_mapping(cls, cycle: str) -> Optional[TemporalMapping]:
        """Get temporal mapping by cycle type."""
        return cls.TEMPORAL.get(cycle.lower())
        
    @classmethod
    def get_energy_mapping(cls, signature: str) -> Optional[EnergyMapping]:
        """Get energy mapping by signature type."""
        return cls.ENERGY.get(signature.lower())
        
    @classmethod
    def get_temporal_effects(cls, cycle: str) -> List[str]:
        """Get effects for a temporal cycle."""
        mapping = cls.get_temporal_mapping(cycle)
        return mapping.effects if mapping else []
        
    @classmethod
    def get_energy_resonance(cls, signature: str) -> List[str]:
        """Get resonance patterns for an energy signature."""
        mapping = cls.get_energy_mapping(signature)
        return mapping.resonance_patterns if mapping else []
        
    @classmethod
    def get_energy_harmonics(cls, signature: str) -> List[float]:
        """Get harmonic series for an energy signature."""
        mapping = cls.get_energy_mapping(signature)
        return mapping.harmonic_series if mapping else [] 