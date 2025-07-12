"""Visual aspects schema definitions."""

from typing import List, Optional
from pydantic import BaseModel, Field

class VisualTraits(BaseModel):
    """Visual traits for a governor"""
    form_type: str = Field(..., description="Base form type")
    color_scheme: List[str] = Field(default_factory=list, description="Color palette")
    geometry_patterns: List[str] = Field(default_factory=list, description="Sacred geometry patterns")
    environmental_effects: List[str] = Field(default_factory=list, description="Environmental manifestations")
    time_variations: List[str] = Field(default_factory=list, description="Temporal variations")
    energy_signature: List[str] = Field(default_factory=list, description="Energy characteristics")
    symbol_set: List[str] = Field(default_factory=list, description="Associated symbols")
    light_shadow: dict = Field(default_factory=dict, description="Light/shadow dynamics")
    special_properties: List[str] = Field(default_factory=list, description="Special visual properties") 