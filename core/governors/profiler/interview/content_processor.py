"""Process interview responses into visual aspects."""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .schemas.interview_schemas import InterviewResponse
from .visual_mappings import VisualMappings
from ...traits.schemas.trait_schemas import (
    VisualTraits,
    FormAspects,
    ColorAspects,
    ColorPattern,
    GeometryAspects,
    GeometryMotion,
    TemporalAspects,
    TemporalCycle,
    EnergyAspects,
    EnergyFlow
)

logger = logging.getLogger(__name__)

class ContentProcessor:
    """Processes interview responses and generates visual aspects."""
    
    def __init__(self, knowledge_base_path: str):
        """Initialize the content processor.
        
        Args:
            knowledge_base_path: Path to the knowledge base directory
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.templates = self._load_visual_templates()
        self.mappings = VisualMappings()
        
    def _load_visual_templates(self) -> Dict:
        """Load visual aspect templates."""
        try:
            template_path = self.knowledge_base_path / "templates" / "visual_templates.json"
            with open(template_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load visual templates: {e}")
            return {}
            
    def process_responses(self, responses: List[InterviewResponse]) -> VisualTraits:
        """Process interview responses into visual aspects.
        
        Args:
            responses: List of interview responses to process
            
        Returns:
            Generated visual traits
        """
        form_aspects = self._process_form_responses(responses)
        color_aspects = self._process_color_responses(responses)
        geometry_aspects = self._process_geometry_responses(responses)
        temporal_aspects = self._process_temporal_responses(responses)
        energy_aspects = self._process_energy_responses(responses)
        
        return VisualTraits(
            form=form_aspects,
            color=color_aspects,
            geometry=geometry_aspects,
            temporal=temporal_aspects,
            energy=energy_aspects
        )
        
    def _process_form_responses(self, responses: List[InterviewResponse]) -> FormAspects:
        """Process form-related responses.
        
        Args:
            responses: List of responses to process
            
        Returns:
            Processed form aspects
        """
        # Process base form type
        base_type_responses = [r for r in responses if r.question_id == "form_base_type"]
        base_type = base_type_responses[0].selected_option if base_type_responses else "undefined"
        form_mapping = self.mappings.get_form_mapping(base_type)
        
        # Process complexity
        complexity_responses = [r for r in responses if r.question_id == "form_complexity"]
        complexity = complexity_responses[0].selected_option if complexity_responses else "simple"
        
        return FormAspects(
            base_form=form_mapping.base_form if form_mapping else base_type,
            description=form_mapping.description if form_mapping else "",
            complexity=self._map_complexity_level(complexity),
            detail_density=self._map_detail_density(complexity)
        )
        
    def _process_color_responses(self, responses: List[InterviewResponse]) -> ColorAspects:
        """Process color-related responses.
        
        Args:
            responses: List of responses to process
            
        Returns:
            Processed color aspects
        """
        # Process primary color
        primary_responses = [r for r in responses if r.question_id == "color_primary"]
        color = primary_responses[0].selected_option if primary_responses else "undefined"
        color_mapping = self.mappings.get_color_mapping(color)
        
        # Process color pattern
        pattern_responses = [r for r in responses if r.question_id == "color_pattern"]
        pattern = pattern_responses[0].selected_option if pattern_responses else "static"
        
        # Convert RGB tuple to list
        rgb = list(color_mapping.rgb) if color_mapping else [0, 0, 0]
        
        return ColorAspects(
            primary_color=rgb,
            energy_type=color_mapping.energy if color_mapping else "undefined",
            vibration=color_mapping.vibration if color_mapping else "low",
            pattern=ColorPattern(
                type=pattern,
                speed=self._map_pattern_speed(pattern)
            )
        )
        
    def _process_geometry_responses(self, responses: List[InterviewResponse]) -> GeometryAspects:
        """Process geometry-related responses.
        
        Args:
            responses: List of responses to process
            
        Returns:
            Processed geometry aspects
        """
        # Process base pattern
        pattern_responses = [r for r in responses if r.question_id == "geometry_pattern"]
        pattern = pattern_responses[0].selected_option if pattern_responses else "undefined"
        geometry_mapping = self.mappings.get_geometry_mapping(pattern)
        
        # Process motion
        motion_responses = [r for r in responses if r.question_id == "geometry_motion"]
        motion = motion_responses[0].selected_option if motion_responses else "static"
        
        return GeometryAspects(
            base_pattern=geometry_mapping.base_pattern if geometry_mapping else pattern,
            dimension=geometry_mapping.dimension if geometry_mapping else 2,
            symmetry_points=geometry_mapping.symmetry_points if geometry_mapping else 0,
            motion=GeometryMotion(
                type=motion,
                speed=self._map_motion_speed(motion),
                complexity=self._map_motion_complexity(motion)
            )
        )
        
    def _process_temporal_responses(self, responses: List[InterviewResponse]) -> TemporalAspects:
        """Process temporal-related responses.
        
        Args:
            responses: List of responses to process
            
        Returns:
            Processed temporal aspects
        """
        # Process temporal cycle
        cycle_responses = [r for r in responses if r.question_id == "temporal_cycle"]
        cycle = cycle_responses[0].selected_option if cycle_responses else "solar"
        temporal_mapping = self.mappings.get_temporal_mapping(cycle)
        
        # Process flow type
        flow_responses = [r for r in responses if r.question_id == "temporal_flow"]
        flow = flow_responses[0].selected_option if flow_responses else "linear"
        
        # Process stability
        stability_responses = [r for r in responses if r.question_id == "temporal_stability"]
        stability = stability_responses[0].selected_option if stability_responses else "stable"
        
        return TemporalAspects(
            primary_cycle=TemporalCycle(
                type=temporal_mapping.cycle_type if temporal_mapping else cycle,
                duration=temporal_mapping.base_duration if temporal_mapping else 24,
                phase=self._map_temporal_phase(cycle)
            ),
            flow_type=flow,
            stability=self._map_stability_factor(stability),
            variations=temporal_mapping.variations if temporal_mapping else []
        )
        
    def _process_energy_responses(self, responses: List[InterviewResponse]) -> EnergyAspects:
        """Process energy-related responses.
        
        Args:
            responses: List of responses to process
            
        Returns:
            Processed energy aspects
        """
        # Process energy type
        type_responses = [r for r in responses if r.question_id == "energy_type"]
        energy_type = type_responses[0].selected_option if type_responses else "elemental"
        energy_mapping = self.mappings.get_energy_mapping(energy_type)
        
        # Process flow
        flow_responses = [r for r in responses if r.question_id == "energy_flow"]
        flow = flow_responses[0].selected_option if flow_responses else "radiating"
        
        # Process intensity
        intensity_responses = [r for r in responses if r.question_id == "energy_intensity"]
        intensity = intensity_responses[0].selected_option if intensity_responses else "moderate"
        
        return EnergyAspects(
            signature_type=energy_mapping.signature_type if energy_mapping else energy_type,
            primary_flow=EnergyFlow(
                direction=flow,
                intensity=self._map_energy_intensity(intensity),
                frequency=energy_mapping.base_frequency if energy_mapping else 432.0
            ),
            resonance=energy_mapping.resonance_patterns if energy_mapping else [],
            harmonics=energy_mapping.harmonic_series if energy_mapping else [1.0]
        )
        
    def _map_complexity_level(self, complexity: str) -> int:
        """Map complexity string to numeric level."""
        levels = {
            "simple": 1,
            "moderate": 2,
            "complex": 3,
            "highly_complex": 4,
            "metamorphic": 5
        }
        return levels.get(complexity, 1)
        
    def _map_detail_density(self, complexity: str) -> str:
        """Map complexity to detail density."""
        densities = {
            "simple": "low",
            "moderate": "medium",
            "complex": "high",
            "highly_complex": "very_high",
            "metamorphic": "dynamic"
        }
        return densities.get(complexity, "low")
        
    def _map_pattern_speed(self, pattern: str) -> int:
        """Map pattern type to speed value."""
        speeds = {
            "static": 0,
            "pulsing": 2,
            "shifting": 3,
            "radiating": 2,
            "prismatic": 4,
            "phase_changing": 5
        }
        return speeds.get(pattern, 0)
        
    def _map_motion_speed(self, motion: str) -> int:
        """Map motion type to speed value."""
        speeds = {
            "static": 0,
            "rotating": 2,
            "pulsing": 3,
            "flowing": 3,
            "phase_shifting": 4,
            "dimension_folding": 5
        }
        return speeds.get(motion, 0)
        
    def _map_motion_complexity(self, motion: str) -> int:
        """Map motion type to complexity value."""
        complexities = {
            "static": 1,
            "rotating": 2,
            "pulsing": 2,
            "flowing": 3,
            "phase_shifting": 4,
            "dimension_folding": 5
        }
        return complexities.get(motion, 1)
        
    def _map_temporal_phase(self, cycle: str) -> float:
        """Map temporal cycle to initial phase."""
        phases = {
            "solar": 0.0,
            "lunar": 0.25,
            "celestial": 0.0,
            "quantum": 0.5,
            "eternal": 1.0,
            "spiral": 0.0
        }
        return phases.get(cycle, 0.0)
        
    def _map_stability_factor(self, stability: str) -> float:
        """Map stability string to factor value."""
        factors = {
            "unstable": 0.2,
            "fluctuating": 0.4,
            "stable": 0.6,
            "crystallized": 0.8,
            "eternal": 0.9,
            "absolute": 1.0
        }
        return factors.get(stability, 0.6)
        
    def _map_energy_intensity(self, intensity: str) -> float:
        """Map intensity string to numeric value."""
        intensities = {
            "subtle": 0.2,
            "moderate": 0.4,
            "strong": 0.6,
            "intense": 0.8,
            "overwhelming": 0.9,
            "transcendent": 1.0
        }
        return intensities.get(intensity, 0.4) 