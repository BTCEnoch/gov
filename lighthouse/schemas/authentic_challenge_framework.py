"""
Enochian Cyphers Authentic Challenge Framework
Creates authentic mystical challenges based on primary source research
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import json

class ChallengeType(Enum):
    """Types of authentic mystical challenges"""
    CONTEMPLATIVE = "contemplative"     # Meditation and reflection
    PRACTICAL = "practical"             # Hands-on practice
    INTELLECTUAL = "intellectual"       # Study and analysis
    EXPERIENTIAL = "experiential"       # Direct experience
    CREATIVE = "creative"               # Creative expression
    SERVICE = "service"                 # Service to others
    SYNTHESIS = "synthesis"             # Integration of knowledge

class AuthenticitySource(Enum):
    """Sources of authenticity for challenges"""
    PRIMARY_TEXT = "primary_text"           # Direct from historical texts
    TRADITIONAL_PRACTICE = "traditional"   # Established traditional practice
    SCHOLARLY_RECONSTRUCTION = "scholarly" # Academic reconstruction
    MODERN_ADAPTATION = "modern"           # Contemporary adaptation

@dataclass
class ChallengeComponent:
    """Individual component of a mystical challenge"""
    name: str
    description: str
    instructions: List[str]
    success_criteria: List[str]
    time_requirement: str
    difficulty_modifier: float
    authenticity_source: AuthenticitySource
    primary_source_reference: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'success_criteria': self.success_criteria,
            'time_requirement': self.time_requirement,
            'difficulty_modifier': self.difficulty_modifier,
            'authenticity_source': self.authenticity_source.value,
            'primary_source_reference': self.primary_source_reference
        }

@dataclass
class AuthenticChallenge:
    """Complete authentic mystical challenge"""
    id: str
    title: str
    tradition: str
    challenge_type: ChallengeType
    difficulty_tier: int
    components: List[ChallengeComponent]
    wisdom_teaching: str
    historical_context: str
    modern_relevance: str
    energy_cost: int
    reputation_reward: int
    prerequisites: List[str] = field(default_factory=list)
    follow_up_challenges: List[str] = field(default_factory=list)
    cross_references: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'tradition': self.tradition,
            'challenge_type': self.challenge_type.value,
            'difficulty_tier': self.difficulty_tier,
            'components': [comp.to_dict() for comp in self.components],
            'wisdom_teaching': self.wisdom_teaching,
            'historical_context': self.historical_context,
            'modern_relevance': self.modern_relevance,
            'energy_cost': self.energy_cost,
            'reputation_reward': self.reputation_reward,
            'prerequisites': self.prerequisites,
            'follow_up_challenges': self.follow_up_challenges,
            'cross_references': self.cross_references
        }

class AuthenticChallengeFramework:
    """Framework for generating authentic mystical challenges"""
    
    def __init__(self):
        self.tradition_challenges = self._initialize_tradition_challenges()
        self.component_library = self._initialize_component_library()
        self.wisdom_teachings = self._initialize_wisdom_teachings()
    
    def _initialize_tradition_challenges(self) -> Dict[str, Dict]:
        """Initialize authentic challenge patterns for each tradition"""
        return {
            'enochian_magic': {
                'primary_sources': [
                    'John Dee\'s Five Books of Mystery',
                    'Liber Chanokh (Liber LXXXIV)',
                    'True & Faithful Relation'
                ],
                'challenge_patterns': {
                    'scrying_progression': {
                        'description': 'Progressive scrying through the Aethyrs',
                        'components': ['preparation', 'invocation', 'scrying', 'recording', 'interpretation'],
                        'authenticity': AuthenticitySource.PRIMARY_TEXT,
                        'difficulty_scaling': 'aethyr_based'
                    },
                    'governor_communion': {
                        'description': 'Communication with Governor Angels',
                        'components': ['research', 'preparation', 'invocation', 'communion', 'service'],
                        'authenticity': AuthenticitySource.PRIMARY_TEXT,
                        'difficulty_scaling': 'governor_hierarchy'
                    },
                    'enochian_key_mastery': {
                        'description': 'Mastery of the 48 Enochian Keys',
                        'components': ['study', 'pronunciation', 'vibration', 'invocation', 'integration'],
                        'authenticity': AuthenticitySource.PRIMARY_TEXT,
                        'difficulty_scaling': 'key_complexity'
                    }
                }
            },
            'i_ching': {
                'primary_sources': [
                    'Wilhelm Translation of Book of Changes',
                    'Traditional Chinese commentaries',
                    'Ten Wings (Shi Yi)'
                ],
                'challenge_patterns': {
                    'hexagram_mastery': {
                        'description': 'Deep study and application of hexagrams',
                        'components': ['study', 'contemplation', 'divination', 'application', 'integration'],
                        'authenticity': AuthenticitySource.PRIMARY_TEXT,
                        'difficulty_scaling': 'hexagram_complexity'
                    },
                    'change_navigation': {
                        'description': 'Using I Ching wisdom to navigate life changes',
                        'components': ['situation_analysis', 'consultation', 'interpretation', 'action', 'reflection'],
                        'authenticity': AuthenticitySource.TRADITIONAL_PRACTICE,
                        'difficulty_scaling': 'life_complexity'
                    },
                    'sage_development': {
                        'description': 'Cultivating sage-like wisdom and perspective',
                        'components': ['study', 'meditation', 'practice', 'teaching', 'service'],
                        'authenticity': AuthenticitySource.TRADITIONAL_PRACTICE,
                        'difficulty_scaling': 'wisdom_depth'
                    }
                }
            },
            'hermetic_qabalah': {
                'primary_sources': [
                    'Colin Low\'s Notes on Kabbalah',
                    'Golden Dawn materials',
                    'Traditional Hermetic texts'
                ],
                'challenge_patterns': {
                    'sephirah_exploration': {
                        'description': 'Deep exploration of each Sephirah',
                        'components': ['study', 'meditation', 'pathworking', 'integration', 'service'],
                        'authenticity': AuthenticitySource.SCHOLARLY_RECONSTRUCTION,
                        'difficulty_scaling': 'sephirah_level'
                    },
                    'tree_ascension': {
                        'description': 'Progressive ascension of the Tree of Life',
                        'components': ['preparation', 'purification', 'ascension', 'integration', 'descent'],
                        'authenticity': AuthenticitySource.TRADITIONAL_PRACTICE,
                        'difficulty_scaling': 'tree_level'
                    },
                    'correspondence_mastery': {
                        'description': 'Mastery of Hermetic correspondences',
                        'components': ['study', 'memorization', 'application', 'synthesis', 'teaching'],
                        'authenticity': AuthenticitySource.TRADITIONAL_PRACTICE,
                        'difficulty_scaling': 'correspondence_complexity'
                    }
                }
            }
            # Additional traditions would be defined based on research
        }
    
    def _initialize_component_library(self) -> Dict[str, List[ChallengeComponent]]:
        """Initialize library of authentic challenge components"""
        return {
            'enochian_magic': [
                ChallengeComponent(
                    name="Aethyr Scrying Preparation",
                    description="Prepare for scrying an Aethyr according to Dee's methods",
                    instructions=[
                        "Study the Aethyr name and its traditional associations",
                        "Prepare sacred space with appropriate symbols",
                        "Enter meditative state through prayer or invocation",
                        "Focus intention on receiving authentic visions"
                    ],
                    success_criteria=[
                        "Demonstrate understanding of Aethyr significance",
                        "Properly prepare sacred space",
                        "Achieve appropriate meditative state",
                        "Maintain clear intention throughout"
                    ],
                    time_requirement="30-45 minutes",
                    difficulty_modifier=1.0,
                    authenticity_source=AuthenticitySource.PRIMARY_TEXT,
                    primary_source_reference="John Dee's Five Books of Mystery, Sessions with Edward Kelley"
                ),
                ChallengeComponent(
                    name="Governor Angel Research",
                    description="Research a specific Governor Angel from primary sources",
                    instructions=[
                        "Study available historical references to the Governor",
                        "Identify traditional attributes and correspondences",
                        "Research the Governor's role in Enochian hierarchy",
                        "Prepare appropriate invocation or approach"
                    ],
                    success_criteria=[
                        "Demonstrate accurate knowledge of Governor attributes",
                        "Show understanding of hierarchical position",
                        "Prepare authentic invocation method",
                        "Respect traditional protocols"
                    ],
                    time_requirement="2-3 hours",
                    difficulty_modifier=1.2,
                    authenticity_source=AuthenticitySource.PRIMARY_TEXT,
                    primary_source_reference="Liber Chanokh, Governor Angel listings"
                )
            ],
            'i_ching': [
                ChallengeComponent(
                    name="Hexagram Deep Study",
                    description="Comprehensive study of a specific hexagram",
                    instructions=[
                        "Study the hexagram structure and trigram composition",
                        "Read and contemplate the Judgment text",
                        "Meditate on the Image and its symbolism",
                        "Study the individual line meanings",
                        "Research traditional commentaries"
                    ],
                    success_criteria=[
                        "Demonstrate understanding of hexagram structure",
                        "Explain the Judgment in your own words",
                        "Interpret the Image symbolism",
                        "Apply line meanings to situations",
                        "Show familiarity with traditional interpretations"
                    ],
                    time_requirement="3-4 hours",
                    difficulty_modifier=1.0,
                    authenticity_source=AuthenticitySource.PRIMARY_TEXT,
                    primary_source_reference="Wilhelm Translation, Book of Changes"
                ),
                ChallengeComponent(
                    name="Change Pattern Recognition",
                    description="Identify and work with patterns of change",
                    instructions=[
                        "Observe a situation undergoing change",
                        "Identify the underlying pattern using I Ching principles",
                        "Consult the I Ching for guidance",
                        "Apply the wisdom received",
                        "Reflect on the outcome"
                    ],
                    success_criteria=[
                        "Accurately identify change patterns",
                        "Properly consult the I Ching",
                        "Apply guidance appropriately",
                        "Demonstrate learning from the process",
                        "Show integration of wisdom"
                    ],
                    time_requirement="1-2 weeks",
                    difficulty_modifier=1.3,
                    authenticity_source=AuthenticitySource.TRADITIONAL_PRACTICE,
                    primary_source_reference="Traditional Chinese divination practices"
                )
            ]
            # Additional tradition components would be defined
        }
    
    def _initialize_wisdom_teachings(self) -> Dict[str, List[str]]:
        """Initialize authentic wisdom teachings for each tradition"""
        return {
            'enochian_magic': [
                "The Aethyrs are not places but states of consciousness",
                "Governor Angels serve the divine will, not personal desires",
                "True scrying reveals divine wisdom, not future events",
                "Enochian magic is about spiritual transformation, not material gain"
            ],
            'i_ching': [
                "Change is the only constant in the universe",
                "Proper timing aligns action with natural flow",
                "The sage acts in harmony with the Tao",
                "Understanding comes through contemplation, not force"
            ],
            'hermetic_qabalah': [
                "As above, so below - the microcosm reflects the macrocosm",
                "The Tree of Life is a map of consciousness",
                "True knowledge comes through direct experience",
                "Service to others is service to the divine"
            ]
        }
    
    def generate_challenge(self, tradition: str, difficulty_tier: int, 
                          challenge_type: ChallengeType, governor_data: Optional[Dict] = None) -> AuthenticChallenge:
        """Generate an authentic challenge for a specific tradition and difficulty"""
        
        if tradition not in self.tradition_challenges:
            raise ValueError(f"Unsupported tradition: {tradition}")
        
        tradition_data = self.tradition_challenges[tradition]
        challenge_patterns = tradition_data['challenge_patterns']
        
        # Select appropriate challenge pattern
        pattern_name = self._select_challenge_pattern(challenge_patterns, challenge_type, difficulty_tier)
        pattern = challenge_patterns[pattern_name]
        
        # Generate challenge components
        components = self._generate_challenge_components(
            tradition, pattern, difficulty_tier, governor_data
        )
        
        # Calculate energy cost and reputation reward
        energy_cost = self._calculate_energy_cost(components, difficulty_tier)
        reputation_reward = self._calculate_reputation_reward(components, difficulty_tier)
        
        # Select wisdom teaching
        wisdom_teaching = random.choice(self.wisdom_teachings.get(tradition, ["Seek wisdom through practice."]))
        
        # Generate challenge
        challenge = AuthenticChallenge(
            id=f"{tradition}_{pattern_name}_{difficulty_tier}_{random.randint(1000, 9999)}",
            title=self._generate_challenge_title(pattern, difficulty_tier, governor_data),
            tradition=tradition,
            challenge_type=challenge_type,
            difficulty_tier=difficulty_tier,
            components=components,
            wisdom_teaching=wisdom_teaching,
            historical_context=self._generate_historical_context(tradition, pattern),
            modern_relevance=self._generate_modern_relevance(pattern, challenge_type),
            energy_cost=energy_cost,
            reputation_reward=reputation_reward,
            prerequisites=self._generate_prerequisites(difficulty_tier, tradition),
            cross_references=self._generate_cross_references(tradition, pattern_name)
        )
        
        return challenge
    
    def _select_challenge_pattern(self, patterns: Dict, challenge_type: ChallengeType, 
                                 difficulty_tier: int) -> str:
        """Select appropriate challenge pattern"""
        # Simple selection logic - could be more sophisticated
        pattern_names = list(patterns.keys())
        
        # Prefer patterns that match the challenge type
        if challenge_type == ChallengeType.CONTEMPLATIVE:
            preferred = [name for name in pattern_names if 'meditation' in name or 'study' in name]
        elif challenge_type == ChallengeType.PRACTICAL:
            preferred = [name for name in pattern_names if 'practice' in name or 'mastery' in name]
        elif challenge_type == ChallengeType.EXPERIENTIAL:
            preferred = [name for name in pattern_names if 'communion' in name or 'scrying' in name]
        else:
            preferred = pattern_names
        
        return random.choice(preferred if preferred else pattern_names)
    
    def _generate_challenge_components(self, tradition: str, pattern: Dict, 
                                     difficulty_tier: int, governor_data: Optional[Dict]) -> List[ChallengeComponent]:
        """Generate components for the challenge"""
        available_components = self.component_library.get(tradition, [])
        if not available_components:
            # Generate basic components if none available
            return self._generate_basic_components(pattern, difficulty_tier)
        
        # Select appropriate components based on pattern
        pattern_components = pattern.get('components', [])
        selected_components = []
        
        for comp_type in pattern_components:
            # Find matching components
            matching = [comp for comp in available_components if comp_type in comp.name.lower()]
            if matching:
                component = random.choice(matching)
                # Adjust difficulty modifier based on tier
                adjusted_component = self._adjust_component_difficulty(component, difficulty_tier)
                selected_components.append(adjusted_component)
        
        return selected_components
    
    def _generate_basic_components(self, pattern: Dict, difficulty_tier: int) -> List[ChallengeComponent]:
        """Generate basic components when none are available"""
        basic_components = []
        component_types = pattern.get('components', ['study', 'practice', 'reflection'])
        
        for comp_type in component_types:
            component = ChallengeComponent(
                name=f"{comp_type.title()} Component",
                description=f"Engage in {comp_type} related to this challenge",
                instructions=[f"Complete the {comp_type} requirements"],
                success_criteria=[f"Demonstrate competency in {comp_type}"],
                time_requirement="30-60 minutes",
                difficulty_modifier=1.0 + (difficulty_tier - 1) * 0.1,
                authenticity_source=AuthenticitySource.MODERN_ADAPTATION
            )
            basic_components.append(component)
        
        return basic_components
    
    def _adjust_component_difficulty(self, component: ChallengeComponent, difficulty_tier: int) -> ChallengeComponent:
        """Adjust component difficulty based on tier"""
        # Create a copy with adjusted difficulty
        adjusted = ChallengeComponent(
            name=component.name,
            description=component.description,
            instructions=component.instructions.copy(),
            success_criteria=component.success_criteria.copy(),
            time_requirement=component.time_requirement,
            difficulty_modifier=component.difficulty_modifier * (1.0 + (difficulty_tier - 1) * 0.1),
            authenticity_source=component.authenticity_source,
            primary_source_reference=component.primary_source_reference
        )
        
        return adjusted
    
    def _calculate_energy_cost(self, components: List[ChallengeComponent], difficulty_tier: int) -> int:
        """Calculate energy cost for challenge"""
        base_cost = len(components) * 2
        difficulty_multiplier = 1.0 + (difficulty_tier - 1) * 0.2
        component_multiplier = sum(comp.difficulty_modifier for comp in components) / len(components)
        
        total_cost = int(base_cost * difficulty_multiplier * component_multiplier)
        return max(1, min(25, total_cost))  # Clamp to valid range
    
    def _calculate_reputation_reward(self, components: List[ChallengeComponent], difficulty_tier: int) -> int:
        """Calculate reputation reward for challenge"""
        base_reward = difficulty_tier * 2
        component_bonus = len(components)
        authenticity_bonus = sum(
            2 if comp.authenticity_source == AuthenticitySource.PRIMARY_TEXT else 1
            for comp in components
        )
        
        total_reward = base_reward + component_bonus + authenticity_bonus
        return max(1, min(50, total_reward))  # Clamp to valid range
    
    def _generate_challenge_title(self, pattern: Dict, difficulty_tier: int, 
                                 governor_data: Optional[Dict]) -> str:
        """Generate appropriate title for challenge"""
        base_title = pattern.get('description', 'Mystical Challenge')
        
        if governor_data:
            governor_name = governor_data.get('name', 'Unknown')
            return f"{base_title} with {governor_name}"
        else:
            tier_names = {
                range(1, 8): "Foundation",
                range(8, 16): "Development", 
                range(16, 24): "Mastery",
                range(24, 31): "Transcendence"
            }
            
            tier_name = "Foundation"
            for tier_range, name in tier_names.items():
                if difficulty_tier in tier_range:
                    tier_name = name
                    break
            
            return f"{base_title} - {tier_name} Level"
    
    def _generate_historical_context(self, tradition: str, pattern: Dict) -> str:
        """Generate historical context for challenge"""
        tradition_contexts = {
            'enochian_magic': "Based on the angelic communications received by Dr. John Dee and Edward Kelley in the 16th century.",
            'i_ching': "Rooted in ancient Chinese wisdom dating back over 3,000 years to the Zhou Dynasty.",
            'hermetic_qabalah': "Drawing from the Western esoteric tradition and Golden Dawn practices."
        }
        
        return tradition_contexts.get(tradition, "Based on authentic mystical traditions.")
    
    def _generate_modern_relevance(self, pattern: Dict, challenge_type: ChallengeType) -> str:
        """Generate modern relevance statement"""
        relevance_templates = {
            ChallengeType.CONTEMPLATIVE: "Develops mindfulness and inner awareness in our fast-paced world.",
            ChallengeType.PRACTICAL: "Provides practical tools for personal and spiritual development.",
            ChallengeType.EXPERIENTIAL: "Offers direct experience of mystical states and expanded consciousness.",
            ChallengeType.SYNTHESIS: "Integrates ancient wisdom with contemporary understanding."
        }
        
        return relevance_templates.get(challenge_type, "Bridges ancient wisdom with modern life.")
    
    def _generate_prerequisites(self, difficulty_tier: int, tradition: str) -> List[str]:
        """Generate prerequisites for challenge"""
        prerequisites = []
        
        if difficulty_tier > 5:
            prerequisites.append(f"Basic understanding of {tradition.replace('_', ' ')}")
        
        if difficulty_tier > 10:
            prerequisites.append("Previous completion of foundation-level challenges")
        
        if difficulty_tier > 20:
            prerequisites.append("Advanced practitioner status")
        
        return prerequisites
    
    def _generate_cross_references(self, tradition: str, pattern_name: str) -> Dict[str, List[str]]:
        """Generate cross-references to related content"""
        return {
            'related_traditions': [],  # Would be populated based on synergies
            'mystical_entries': [],    # Would reference specific knowledge entries
            'other_challenges': [],    # Would reference related challenges
            'study_materials': []      # Would reference additional study materials
        }

# Initialize global framework
AUTHENTIC_CHALLENGE_FRAMEWORK = AuthenticChallengeFramework()

def get_challenge_framework() -> AuthenticChallengeFramework:
    """Get the global authentic challenge framework instance"""
    return AUTHENTIC_CHALLENGE_FRAMEWORK
