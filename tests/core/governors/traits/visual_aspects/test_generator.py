#!/usr/bin/env python3
"""Tests for the Visual Aspects Generator"""

import pytest
from pathlib import Path
import json
from core.governors.traits.visual_aspects.generator import VisualAspectsGenerator

@pytest.fixture
def sample_governor_data():
    """Sample governor data for testing"""
    return {
        "governor_name": "TEST_GOV",
        "persona": {
            "name": "TEST_GOV",
            "element": "Air",
            "aethyr": "LIL",
            "angelic_role": "Test Angel",
            "knowledge_base": [
                "hermetic_qabalah",
                "enochian_magic"
            ],
            "archetypal_correspondences": {
                "tarot": "The Hermit",
                "sephirot": "Hod",
                "zodiac_sign": "Virgo",
                "zodiac_angel": "Raphael",
                "numerology": 6
            },
            "polar_traits": {
                "baseline_approach": "Prophesying",
                "baseline_tone": "Analytical",
                "motive_alignment": "Lawful Neutral",
                "role_archetype": "Herald",
                "orientation": "Balanced",
                "polarity": "Balanced Flux",
                "self_regard": "Resolute",
                "virtues": [
                    "Vision",
                    "Prudence",
                    "Discernment"
                ],
                "flaws": [
                    "Obsession",
                    "Rigidity"
                ]
            },
            "approaches": {
                "bad": "Testing",
                "average": "Prophesying",
                "good": "Guiding"
            },
            "tones": {
                "bad": "Stern",
                "average": "Analytical",
                "good": "Direct"
            }
        }
    }

@pytest.fixture
def generator():
    """Initialize generator for testing"""
    return VisualAspectsGenerator()

def test_generate_visual_aspects(generator, sample_governor_data):
    """Test complete visual aspects generation"""
    aspects = generator.generate_visual_aspects(sample_governor_data)
    
    # Verify all required fields are present
    assert "form" in aspects
    assert "color" in aspects
    assert "geometry" in aspects
    assert "environment" in aspects
    assert "time_variations" in aspects
    assert "energy_signature" in aspects
    assert "symbol_set" in aspects
    assert "light_shadow" in aspects
    assert "special_properties" in aspects
    
    # Verify form generation
    assert aspects["form"]["name"] == "Ethereal"
    assert "luminous" in aspects["form"]["description"].lower()
    
    # Verify color generation
    assert aspects["color"] in ["SILVER", "WHITE", "AZURE"]
    
    # Verify geometry generation
    assert "FRACTAL" in aspects["geometry"]["patterns"]
    assert aspects["geometry"]["complexity"] == 3
    
    # Verify environment generation
    assert aspects["environment"]["effect_type"] == "transforming"
    assert aspects["environment"]["radius"] == "regional"
    assert aspects["environment"]["intensity"] == "moderate"
    
    # Verify time variations
    assert aspects["time_variations"] == "constant"
    
    # Verify energy signature
    assert aspects["energy_signature"] == "stable"
    
    # Verify light/shadow balance
    assert aspects["light_shadow"] == "radiant"
    
def test_generate_form(generator, sample_governor_data):
    """Test form generation specifically"""
    form = generator._generate_form(sample_governor_data["persona"])
    assert form["name"] == "Ethereal"
    assert "interactions" in form
    assert len(form["interactions"]) == 3
    
def test_generate_color(generator):
    """Test color generation"""
    color = generator._generate_color("Fire", "LIL")
    assert color in ["GOLDEN", "CRIMSON", "PLASMA"]
    
def test_generate_geometry(generator):
    """Test geometry generation"""
    correspondences = {"zodiac_sign": "Virgo"}
    geometry = generator._generate_geometry("LIL", correspondences)
    assert "patterns" in geometry
    assert "complexity" in geometry
    assert geometry["complexity"] == 3
    
def test_generate_environment(generator):
    """Test environment generation"""
    polar_traits = {"polarity": "Balanced Flux", "orientation": "Balanced"}
    env = generator._generate_environment(polar_traits)
    assert env["effect_type"] == "transforming"
    assert env["radius"] == "regional"
    assert env["intensity"] == "moderate"
    
def test_generate_special_properties(generator, sample_governor_data):
    """Test special properties generation"""
    props = generator._generate_special_properties(sample_governor_data["persona"])
    assert isinstance(props, list)
    assert len(props) > 0  # Should find some properties from knowledge base 