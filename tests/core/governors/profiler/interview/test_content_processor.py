"""Tests for the content processor."""
import json
import pytest
from pathlib import Path

from core.governors.profiler.interview.content_processor import ContentProcessor
from core.governors.profiler.interview.schemas.interview_schemas import InterviewResponse
from core.governors.traits.schemas.trait_schemas import (
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

@pytest.fixture
def test_templates():
    """Sample visual templates for testing."""
    return {
        "version": "1.0",
        "form_mappings": {
            "form_base_type": {
                "geometric": {
                    "base_form": "geometric",
                    "description": "Test geometric form"
                }
            },
            "form_complexity": {
                "moderate": {
                    "complexity_level": 2,
                    "detail_density": "medium"
                }
            }
        },
        "color_mappings": {
            "color_primary": {
                "azure": {
                    "rgb": [0, 127, 255],
                    "energy": "celestial",
                    "vibration": "high"
                }
            },
            "color_pattern": {
                "pulsing": {
                    "pattern_type": "rhythmic",
                    "transition_speed": 2
                }
            }
        },
        "geometry_mappings": {
            "geometry_pattern": {
                "merkaba": {
                    "base_pattern": "merkaba",
                    "dimension": 3,
                    "symmetry_points": 8
                }
            },
            "geometry_motion": {
                "rotating": {
                    "motion_type": "rotation",
                    "speed": 2,
                    "complexity": 2
                }
            }
        }
    }

@pytest.fixture
def test_responses():
    """Sample interview responses for testing."""
    return [
        InterviewResponse(
            question_id="form_base_type",
            selected_option="geometric"
        ),
        InterviewResponse(
            question_id="form_complexity",
            selected_option="moderate"
        ),
        InterviewResponse(
            question_id="color_primary",
            selected_option="azure"
        ),
        InterviewResponse(
            question_id="color_pattern",
            selected_option="pulsing"
        ),
        InterviewResponse(
            question_id="geometry_pattern",
            selected_option="merkaba"
        ),
        InterviewResponse(
            question_id="geometry_motion",
            selected_option="rotating"
        ),
        InterviewResponse(
            question_id="temporal_cycle",
            selected_option="solar"
        ),
        InterviewResponse(
            question_id="temporal_flow",
            selected_option="cyclical"
        ),
        InterviewResponse(
            question_id="temporal_stability",
            selected_option="stable"
        ),
        InterviewResponse(
            question_id="energy_type",
            selected_option="celestial"
        ),
        InterviewResponse(
            question_id="energy_flow",
            selected_option="radiating"
        ),
        InterviewResponse(
            question_id="energy_intensity",
            selected_option="intense"
        )
    ]

@pytest.fixture
def processor(tmp_path):
    """Create content processor instance."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    template_file = templates_dir / "visual_templates.json"
    with open(template_file, 'w') as f:
        json.dump(test_templates(), f)
        
    return ContentProcessor(tmp_path)

def test_process_form_responses(processor, test_responses):
    """Test processing form responses."""
    form_aspects = processor._process_form_responses(test_responses)
    
    assert isinstance(form_aspects, FormAspects)
    assert form_aspects.base_form == "geometric"
    assert "geometric" in form_aspects.description.lower()
    assert form_aspects.complexity == 2
    assert form_aspects.detail_density == "medium"

def test_process_color_responses(processor, test_responses):
    """Test processing color responses."""
    color_aspects = processor._process_color_responses(test_responses)
    
    assert isinstance(color_aspects, ColorAspects)
    assert color_aspects.primary_color == [0, 127, 255]
    assert color_aspects.energy_type == "celestial"
    assert color_aspects.vibration == "high"
    assert isinstance(color_aspects.pattern, ColorPattern)
    assert color_aspects.pattern.type == "pulsing"
    assert color_aspects.pattern.speed == 2

def test_process_geometry_responses(processor, test_responses):
    """Test processing geometry responses."""
    geometry_aspects = processor._process_geometry_responses(test_responses)
    
    assert isinstance(geometry_aspects, GeometryAspects)
    assert geometry_aspects.base_pattern == "merkaba"
    assert geometry_aspects.dimension == 3
    assert geometry_aspects.symmetry_points == 8
    assert isinstance(geometry_aspects.motion, GeometryMotion)
    assert geometry_aspects.motion.type == "rotating"
    assert geometry_aspects.motion.speed == 2
    assert geometry_aspects.motion.complexity == 2

def test_process_temporal_responses(processor, test_responses):
    """Test processing temporal responses."""
    temporal_aspects = processor._process_temporal_responses(test_responses)
    
    assert isinstance(temporal_aspects, TemporalAspects)
    assert isinstance(temporal_aspects.primary_cycle, TemporalCycle)
    assert temporal_aspects.primary_cycle.type == "solar"
    assert temporal_aspects.primary_cycle.duration == 24
    assert temporal_aspects.primary_cycle.phase == 0.0
    assert temporal_aspects.flow_type == "cyclical"
    assert temporal_aspects.stability == 0.6
    assert isinstance(temporal_aspects.variations, list)

def test_process_energy_responses(processor, test_responses):
    """Test processing energy responses."""
    energy_aspects = processor._process_energy_responses(test_responses)
    
    assert isinstance(energy_aspects, EnergyAspects)
    assert energy_aspects.signature_type == "celestial"
    assert isinstance(energy_aspects.primary_flow, EnergyFlow)
    assert energy_aspects.primary_flow.direction == "radiating"
    assert energy_aspects.primary_flow.intensity == 0.8
    assert energy_aspects.primary_flow.frequency == 528.0
    assert isinstance(energy_aspects.resonance, list)
    assert isinstance(energy_aspects.harmonics, list)

def test_process_responses_empty(processor):
    """Test processing empty responses."""
    traits = processor.process_responses([])
    
    assert isinstance(traits, VisualTraits)
    assert traits.form.base_form == "undefined"
    assert traits.color.primary_color == [0, 0, 0]
    assert traits.geometry.base_pattern == "undefined"
    assert traits.temporal.primary_cycle.type == "solar"
    assert traits.energy.signature_type == "elemental"

def test_process_responses_invalid_options(processor):
    """Test processing responses with invalid options."""
    responses = [
        InterviewResponse(
            question_id="form_base_type",
            selected_option="invalid_form"
        ),
        InterviewResponse(
            question_id="color_primary",
            selected_option="invalid_color"
        ),
        InterviewResponse(
            question_id="geometry_pattern",
            selected_option="invalid_pattern"
        ),
        InterviewResponse(
            question_id="temporal_cycle",
            selected_option="invalid_cycle"
        ),
        InterviewResponse(
            question_id="energy_type",
            selected_option="invalid_energy"
        )
    ]
    
    traits = processor.process_responses(responses)
    
    assert traits.form.base_form == "invalid_form"  # Falls back to option value
    assert traits.color.primary_color == [0, 0, 0]  # Falls back to default
    assert traits.geometry.base_pattern == "invalid_pattern"  # Falls back to option value
    assert traits.temporal.primary_cycle.type == "invalid_cycle"  # Falls back to option value
    assert traits.energy.signature_type == "invalid_energy"  # Falls back to option value

def test_mapping_functions(processor):
    """Test various mapping functions."""
    # Test complexity mapping
    assert processor._map_complexity_level("simple") == 1
    assert processor._map_complexity_level("complex") == 3
    assert processor._map_complexity_level("invalid") == 1
    
    # Test pattern speed mapping
    assert processor._map_pattern_speed("static") == 0
    assert processor._map_pattern_speed("pulsing") == 2
    assert processor._map_pattern_speed("invalid") == 0
    
    # Test motion mapping
    assert processor._map_motion_speed("static") == 0
    assert processor._map_motion_speed("rotating") == 2
    assert processor._map_motion_speed("invalid") == 0
    
    # Test temporal phase mapping
    assert processor._map_temporal_phase("solar") == 0.0
    assert processor._map_temporal_phase("lunar") == 0.25
    assert processor._map_temporal_phase("invalid") == 0.0
    
    # Test stability factor mapping
    assert processor._map_stability_factor("stable") == 0.6
    assert processor._map_stability_factor("unstable") == 0.2
    assert processor._map_stability_factor("invalid") == 0.6
    
    # Test energy intensity mapping
    assert processor._map_energy_intensity("moderate") == 0.4
    assert processor._map_energy_intensity("intense") == 0.8
    assert processor._map_energy_intensity("invalid") == 0.4 