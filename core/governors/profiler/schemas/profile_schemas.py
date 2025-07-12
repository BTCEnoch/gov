"""
Governor Profile Schemas
Defines data structures for governor profiles
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class MysticalAttribute(BaseModel):
    """A mystical attribute of a governor"""
    name: str = Field(..., description="Name of the attribute")
    value: Any = Field(..., description="Value of the attribute")
    source: str = Field(..., description="Source of the attribute (e.g. 'lighthouse', 'tarot')")

class GovernorProfile(BaseModel):
    """Complete profile for a Governor"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Governor name")
    rank: int = Field(..., description="Governor rank (1-91)")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Mystical attributes")
    relationships: Dict[str, List[str]] = Field(default_factory=dict, description="Related entity IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Profile creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic model configuration"""
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        } 