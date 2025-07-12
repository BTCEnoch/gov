"""Tests for the batch interview processor."""
import json
import pytest
from pathlib import Path
import asyncio
from unittest.mock import Mock, patch

from core.governors.profiler.interview.batch_interview_processor import BatchInterviewProcessor
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
def test_dir(tmp_path):
    """Create test directory structure."""
    # Create templates directory
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    # Create visual templates
    template_file = templates_dir / "visual_templates.json"
    with open(template_file, 'w') as f:
        json.dump({
            "form_mappings": {
                "form_base_type": {
                    "geometric": {
                        "base_form": "geometric",
                        "description": "Test form"
                    }
                }
            },
            "color_mappings": {
                "color_primary": {
                    "azure": {
                        "rgb": [0, 127, 255],
                        "energy": "test",
                        "vibration": "high"
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
                }
            }
        }, f)
        
    # Create profiles directory
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    
    # Create test profiles
    for gov_id in ["TEST001", "TEST002"]:
        profile_file = profiles_dir / f"{gov_id}.json"
        with open(profile_file, 'w') as f:
            json.dump({"id": gov_id}, f)
            
    return tmp_path

@pytest.fixture
def processor(test_dir):
    """Create batch processor instance."""
    return BatchInterviewProcessor(test_dir)

@pytest.fixture
def mock_visual_traits():
    """Create mock visual traits."""
    return VisualTraits(
        form=FormAspects(
            base_form="geometric",
            description="Test form",
            complexity=1,
            detail_density="low"
        ),
        color=ColorAspects(
            primary_color=[0, 127, 255],
            energy_type="test",
            vibration="high",
            pattern=ColorPattern(
                type="static",
                speed=0
            )
        ),
        geometry=GeometryAspects(
            base_pattern="merkaba",
            dimension=3,
            symmetry_points=8,
            motion=GeometryMotion(
                type="static",
                speed=0,
                complexity=1
            )
        ),
        temporal=TemporalAspects(
            primary_cycle=TemporalCycle(
                type="solar",
                duration=24,
                phase=0.0
            ),
            flow_type="linear",
            stability=0.6,
            variations=["dawn", "noon", "dusk", "midnight"]
        ),
        energy=EnergyAspects(
            signature_type="celestial",
            primary_flow=EnergyFlow(
                direction="radiating",
                intensity=0.8,
                frequency=528.0
            ),
            resonance=["solar", "lunar", "stellar"],
            harmonics=[1.0, 1.618, 2.236]
        )
    )

def test_load_governor_ids(test_dir):
    """Test loading governor IDs."""
    processor = BatchInterviewProcessor(test_dir)
    governor_ids = processor.load_governor_profiles(test_dir / "profiles")
    
    assert len(governor_ids) == 2
    assert "TEST001" in governor_ids
    assert "TEST002" in governor_ids

@pytest.mark.asyncio
async def test_process_single_governor(processor):
    """Test processing a single governor."""
    result = await processor._process_single_governor("TEST001")
    
    assert isinstance(result, tuple)
    assert result[0] == "TEST001"
    assert isinstance(result[1], list)
    assert all(isinstance(r, InterviewResponse) for r in result[1])
    
    # Verify all aspects are covered
    response_ids = {r.question_id for r in result[1]}
    assert "form_base_type" in response_ids
    assert "color_primary" in response_ids
    assert "geometry_pattern" in response_ids
    assert "temporal_cycle" in response_ids
    assert "energy_type" in response_ids

@pytest.mark.asyncio
async def test_process_governors(processor, mock_visual_traits):
    """Test processing multiple governors."""
    with patch.object(processor.content_processor, 'process_responses', return_value=mock_visual_traits):
        results = await processor.process_governors(["TEST001", "TEST002"])
        
    assert len(results) == 2
    assert "TEST001" in results
    assert "TEST002" in results
    assert all(isinstance(traits, VisualTraits) for traits in results.values())
    
    # Verify all aspects are present
    traits = results["TEST001"]
    assert isinstance(traits.form, FormAspects)
    assert isinstance(traits.color, ColorAspects)
    assert isinstance(traits.geometry, GeometryAspects)
    assert isinstance(traits.temporal, TemporalAspects)
    assert isinstance(traits.energy, EnergyAspects)

def test_save_results(processor, tmp_path, mock_visual_traits):
    """Test saving results to files."""
    results = {
        "TEST001": mock_visual_traits,
        "TEST002": mock_visual_traits
    }
    
    output_dir = tmp_path / "output"
    processor.save_results(results, output_dir)
    
    # Verify files were created
    assert (output_dir / "TEST001_visual.json").exists()
    assert (output_dir / "TEST002_visual.json").exists()
    
    # Verify file contents
    with open(output_dir / "TEST001_visual.json") as f:
        data = json.load(f)
        assert "form" in data
        assert "color" in data
        assert "geometry" in data
        assert "temporal" in data
        assert "energy" in data
        
        # Verify temporal aspects
        assert data["temporal"]["primary_cycle"]["type"] == "solar"
        assert data["temporal"]["flow_type"] == "linear"
        assert data["temporal"]["stability"] == 0.6
        
        # Verify energy aspects
        assert data["energy"]["signature_type"] == "celestial"
        assert data["energy"]["primary_flow"]["direction"] == "radiating"
        assert data["energy"]["primary_flow"]["intensity"] == 0.8

def test_process_batch_results(processor, mock_visual_traits):
    """Test processing batch results."""
    with patch.object(processor.content_processor, 'process_responses', return_value=mock_visual_traits):
        batch_results = [
            ("TEST001", [
                InterviewResponse(question_id="test", selected_option="test")
            ]),
            ("TEST002", [
                InterviewResponse(question_id="test", selected_option="test")
            ])
        ]
        
        results = processor._process_batch_results(batch_results)
        
    assert len(results) == 2
    assert all(isinstance(traits, VisualTraits) for traits in results.values())
    
    # Verify all aspects are processed
    traits = results["TEST001"]
    assert traits.temporal.primary_cycle.type == "solar"
    assert traits.energy.signature_type == "celestial"

def test_get_placeholder_response(processor):
    """Test getting placeholder responses."""
    mock_question = Mock()
    mock_question.options = ["option1", "option2"]
    
    response = processor._get_placeholder_response(mock_question)
    assert response == "option1" 