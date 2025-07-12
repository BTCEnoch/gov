"""Schemas for mystical and personality traits."""
from dataclasses import dataclass
from typing import Dict, List, Optional, TYPE_CHECKING

from enum import Enum, auto

if TYPE_CHECKING:
    from core.governors.traits.visual_aspects.schemas import VisualTraits

class ElementType(Enum):
    """Elemental types"""
    FIRE = auto()
    WATER = auto()
    AIR = auto()
    EARTH = auto()
    SPIRIT = auto()

class AlignmentType(Enum):
    """Alignment types"""
    CELESTIAL = auto()
    TERRESTRIAL = auto()
    ETHEREAL = auto()
    PRIMAL = auto()
    COSMIC = auto()

@dataclass
class CanonicalTraits:
    """Core canonical traits"""
    personality: List[str]
    element: ElementType
    alignment: AlignmentType
    zodiac: str
    number: int

@dataclass
class EnhancedTraits:
    """Enhanced trait definitions"""
    archetype: str
    teaching_style: str
    approach: str
    tone: str
    specialties: List[str]

@dataclass
class MysticalTraits:
    """Mystical alignments and correspondences"""
    element: ElementType
    alignment: AlignmentType
    zodiac: str
    tarot: str
    sephirot: str
    angel: str
    number: int

@dataclass
class PersonalityTraits:
    """Personality characteristics"""
    archetype: str
    primary_traits: List[str]
    secondary_traits: List[str]
    teaching_style: str
    approach: str
    tone: str

@dataclass
class GovernorTraits:
    """Complete set of governor traits"""
    canonical: CanonicalTraits
    enhanced: EnhancedTraits
    mystical: MysticalTraits
    personality: PersonalityTraits
    visual: Optional['VisualTraits'] = None  # Forward reference to avoid circular import 