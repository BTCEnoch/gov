"""Tests for visual aspect mappings."""
import pytest

from core.governors.profiler.interview.visual_mappings import (
    VisualMappings,
    ColorMapping,
    FormMapping,
    GeometryMapping
)

def test_color_mappings():
    """Test color mapping functionality."""
    # Test valid color
    azure = VisualMappings.get_color_mapping("azure")
    assert isinstance(azure, ColorMapping)
    assert azure.rgb == (0, 127, 255)
    assert azure.energy == "celestial"
    assert azure.vibration == "high"
    assert "truth" in azure.associations
    
    # Test case insensitivity
    golden = VisualMappings.get_color_mapping("GOLDEN")
    assert isinstance(golden, ColorMapping)
    assert golden.rgb == (255, 215, 0)
    
    # Test invalid color
    invalid = VisualMappings.get_color_mapping("invalid")
    assert invalid is None
    
    # Test RGB helper
    rgb = VisualMappings.get_color_rgb("emerald")
    assert rgb == (0, 168, 107)
    
    # Test invalid RGB helper
    invalid_rgb = VisualMappings.get_color_rgb("invalid")
    assert invalid_rgb == (0, 0, 0)

def test_form_mappings():
    """Test form mapping functionality."""
    # Test valid form
    geometric = VisualMappings.get_form_mapping("geometric")
    assert isinstance(geometric, FormMapping)
    assert geometric.base_form == "geometric"
    assert "precise" in geometric.characteristics
    assert "pattern_matching" in geometric.interactions
    
    # Test case insensitivity
    organic = VisualMappings.get_form_mapping("ORGANIC")
    assert isinstance(organic, FormMapping)
    assert organic.base_form == "organic"
    
    # Test invalid form
    invalid = VisualMappings.get_form_mapping("invalid")
    assert invalid is None
    
    # Test description helper
    desc = VisualMappings.get_form_description("crystalline")
    assert "crystal-like" in desc.lower()
    
    # Test invalid description helper
    invalid_desc = VisualMappings.get_form_description("invalid")
    assert invalid_desc == ""

def test_geometry_mappings():
    """Test geometry mapping functionality."""
    # Test valid geometry
    merkaba = VisualMappings.get_geometry_mapping("merkaba")
    assert isinstance(merkaba, GeometryMapping)
    assert merkaba.base_pattern == "merkaba"
    assert merkaba.dimension == 3
    assert merkaba.symmetry_points == 8
    assert "ascension" in merkaba.properties
    assert merkaba.energy_multiplier == 2.0
    
    # Test case insensitivity
    torus = VisualMappings.get_geometry_mapping("TORUS")
    assert isinstance(torus, GeometryMapping)
    assert torus.base_pattern == "torus"
    
    # Test invalid geometry
    invalid = VisualMappings.get_geometry_mapping("invalid")
    assert invalid is None
    
    # Test properties helper
    props = VisualMappings.get_geometry_properties("flower_of_life")
    assert "creation" in props
    assert "unity" in props
    
    # Test invalid properties helper
    invalid_props = VisualMappings.get_geometry_properties("invalid")
    assert invalid_props == []

def test_color_mapping_dataclass():
    """Test ColorMapping dataclass."""
    mapping = ColorMapping(
        rgb=(255, 0, 0),
        energy="test",
        vibration="high",
        associations=["test1", "test2"]
    )
    
    assert mapping.rgb == (255, 0, 0)
    assert mapping.energy == "test"
    assert mapping.vibration == "high"
    assert mapping.associations == ["test1", "test2"]

def test_form_mapping_dataclass():
    """Test FormMapping dataclass."""
    mapping = FormMapping(
        base_form="test",
        description="test description",
        characteristics=["test1", "test2"],
        interactions=["test3", "test4"]
    )
    
    assert mapping.base_form == "test"
    assert mapping.description == "test description"
    assert mapping.characteristics == ["test1", "test2"]
    assert mapping.interactions == ["test3", "test4"]

def test_geometry_mapping_dataclass():
    """Test GeometryMapping dataclass."""
    mapping = GeometryMapping(
        base_pattern="test",
        dimension=2,
        symmetry_points=4,
        properties=["test1", "test2"],
        energy_multiplier=1.5
    )
    
    assert mapping.base_pattern == "test"
    assert mapping.dimension == 2
    assert mapping.symmetry_points == 4
    assert mapping.properties == ["test1", "test2"]
    assert mapping.energy_multiplier == 1.5 