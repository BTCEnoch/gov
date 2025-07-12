"""
Governor Profile Generator

This module handles the generation of governor profiles, including their
mystical attributes, relationships, and metadata.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from core.utils.mystical.base import MysticalEntity, MysticalAttribute
from core.utils.custom_logging import setup_logger
from core.governors.traits.generator import TraitGenerator
from core.governors.traits.schemas.mystical_schemas import GovernorTraits

logger = setup_logger("governor_profile")

class GovernorProfile(BaseModel):
    """Base profile for a Governor"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Governor name")
    rank: int = Field(..., description="Governor rank (1-91)")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Mystical attributes")
    relationships: Dict[str, List[str]] = Field(default_factory=dict, description="Related entity IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    traits: Optional[GovernorTraits] = Field(None, description="Generated governor traits")

class GovernorProfileGenerator:
    """Generates Governor profiles with mystical attributes"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the profile generator"""
        self.config = config or {}
        self.logger = logger
        self.trait_generator = TraitGenerator()
        
    def generate_profile(
        self,
        governor_id: str,
        name: str,
        rank: int,
        mystical_data: Dict[str, Any]
    ) -> GovernorProfile:
        """Generate a Governor profile with traits
        
        Args:
            governor_id: Unique identifier for the governor
            name: Governor's name
            rank: Governor's rank (1-91)
            mystical_data: Additional mystical attributes and data
            
        Returns:
            Complete governor profile with generated traits
        """
        try:
            # Generate traits first
            traits = self.trait_generator.generate_governor_traits(
                governor_id=governor_id,
                governor_number=rank,
                seed_data=mystical_data.get("seed_data")
            )
            
            # Create base profile with traits
            profile = GovernorProfile(
                id=governor_id,
                name=name,
                rank=rank,
                attributes=[],
                relationships={},
                metadata={},
                traits=traits
            )
            
            # Add mystical attributes
            if "attributes" in mystical_data:
                profile.attributes.extend(mystical_data["attributes"])
                
            # Add relationships
            if "relationships" in mystical_data:
                profile.relationships.update(mystical_data["relationships"])
                
            # Add metadata
            if "metadata" in mystical_data:
                profile.metadata.update(mystical_data["metadata"])
                
            return profile
            
        except Exception as e:
            self.logger.error(f"Failed to generate profile: {e}")
            raise 