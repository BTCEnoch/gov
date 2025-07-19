"""
Enochian Cyphers Tagging and Categorization System
Comprehensive tagging system for mystical entries and Governor Angels
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum
import json

class TagCategory(Enum):
    """Primary tag categories for organization"""
    TRADITION = "tradition"
    PRACTICE = "practice"
    CONCEPT = "concept"
    ELEMENT = "element"
    PLANET = "planet"
    DIFFICULTY = "difficulty"
    QUEST_TYPE = "quest_type"
    HISTORICAL = "historical"
    SYMBOLIC = "symbolic"
    PRACTICAL = "practical"

class DifficultyTier(Enum):
    """Difficulty tiers mapped to Enochian Aethyrs"""
    FOUNDATION = "foundation"      # Tiers 1-7 (TEX-ZAA)
    DEVELOPMENT = "development"    # Tiers 8-15 (BAG-ZIM)
    MASTERY = "mastery"           # Tiers 16-23 (LOE-ASP)
    TRANSCENDENCE = "transcendence" # Tiers 24-30 (KHR-LIL)

@dataclass
class Tag:
    """Individual tag with metadata"""
    name: str
    category: TagCategory
    description: str
    aliases: List[str] = field(default_factory=list)
    parent_tags: List[str] = field(default_factory=list)
    child_tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    authenticity_verified: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'aliases': self.aliases,
            'parent_tags': self.parent_tags,
            'child_tags': self.child_tags,
            'usage_count': self.usage_count,
            'authenticity_verified': self.authenticity_verified
        }

class TaggingSystem:
    """Comprehensive tagging system for Enochian Cyphers"""
    
    def __init__(self):
        self.tags: Dict[str, Tag] = {}
        self.category_index: Dict[TagCategory, Set[str]] = {
            category: set() for category in TagCategory
        }
        self._initialize_core_tags()
    
    def _initialize_core_tags(self):
        """Initialize core tags based on completed research"""
        
        # Tradition tags (18 traditions from research)
        tradition_tags = [
            ("enochian_magic", "Enochian Magic system from John Dee's primary sources"),
            ("i_ching", "Chinese Book of Changes with Wilhelm translation"),
            ("hermetic_qabalah", "Hermetic Tree of Life and Sephiroth system"),
            ("tarot", "78-card Rider-Waite-Smith deck symbolism"),
            ("egyptian_magic", "Ancient Egyptian magical practices and deities"),
            ("celtic_druidic", "Celtic Ogham script and tree correspondences"),
            ("norse_traditions", "Norse Nine Worlds cosmology and Elder Futhark"),
            ("taoism", "Taoist philosophy with Wu Wei and Five Elements"),
            ("kuji_kiri", "Japanese Nine Hand Seals esoteric practices"),
            ("chaos_magic", "Modern chaos magic with sigil creation"),
            ("thelema", "Crowley's Thelemic system and True Will philosophy"),
            ("sacred_geometry", "Platonic solids and Golden Ratio principles"),
            ("quantum_physics", "Quantum consciousness and observer effect"),
            ("alchemy", "Medieval alchemical Great Work and transmutation"),
            ("natal_chart_astrology", "Natal chart astrology with birth chart interpretation and planetary transits"),
            ("shamanism", "Cross-cultural shamanic practices and altered states"),
            ("traditional_kabbalah", "Traditional Jewish Kabbalah with Zohar"),
            ("sufism", "Islamic mysticism with Sufi masters and practices"),
            ("gnosticism", "Gnostic Christianity with hidden knowledge and divine spark teachings"),
            ("greek_mythology", "Classical Greek mythology with gods, heroes, and cosmic narratives")
        ]
        
        for name, desc in tradition_tags:
            self.add_tag(name, TagCategory.TRADITION, desc)
        
        # Elemental tags
        elemental_tags = [
            ("fire", "Fire element - passion, energy, transformation"),
            ("water", "Water element - emotion, flow, adaptability"),
            ("air", "Air element - intellect, communication, balance"),
            ("earth", "Earth element - stability, structure, material world"),
            ("spirit", "Spirit element - divine connection, transcendence")
        ]
        
        for name, desc in elemental_tags:
            self.add_tag(name, TagCategory.ELEMENT, desc)
        
        # Planetary tags
        planetary_tags = [
            ("sun", "Solar energy - consciousness, vitality, leadership"),
            ("moon", "Lunar energy - intuition, cycles, reflection"),
            ("mercury", "Mercurial energy - communication, intellect, adaptability"),
            ("venus", "Venusian energy - love, beauty, harmony"),
            ("mars", "Martian energy - action, courage, conflict"),
            ("jupiter", "Jovian energy - expansion, wisdom, abundance"),
            ("saturn", "Saturnian energy - structure, discipline, limitation")
        ]
        
        for name, desc in planetary_tags:
            self.add_tag(name, TagCategory.PLANET, desc)
        
        # Practice tags
        practice_tags = [
            ("meditation", "Contemplative practices and mindfulness"),
            ("divination", "Fortune-telling and oracle practices"),
            ("ritual", "Ceremonial and ritual practices"),
            ("energy_work", "Energy manipulation and healing"),
            ("symbol_work", "Symbolic interpretation and creation"),
            ("breathwork", "Breathing techniques and pranayama"),
            ("visualization", "Mental imagery and guided visualization"),
            ("chanting", "Vocal practices and mantras")
        ]
        
        for name, desc in practice_tags:
            self.add_tag(name, TagCategory.PRACTICE, desc)
        
        # Concept tags
        concept_tags = [
            ("consciousness", "States and nature of consciousness"),
            ("transformation", "Personal and spiritual transformation"),
            ("balance", "Harmony and equilibrium principles"),
            ("transcendence", "Going beyond ordinary limitations"),
            ("unity", "Oneness and interconnectedness"),
            ("duality", "Polarity and complementary opposites"),
            ("cycles", "Cyclical patterns and rhythms"),
            ("hierarchy", "Levels and gradations of being")
        ]
        
        for name, desc in concept_tags:
            self.add_tag(name, TagCategory.CONCEPT, desc)
        
        # Difficulty tags based on Aethyr tiers
        difficulty_tags = [
            ("foundation", "Foundation level (Aethyrs 1-7) - Basic principles"),
            ("development", "Development level (Aethyrs 8-15) - Skill building"),
            ("mastery", "Mastery level (Aethyrs 16-23) - Advanced practice"),
            ("transcendence", "Transcendence level (Aethyrs 24-30) - Ultimate realization")
        ]
        
        for name, desc in difficulty_tags:
            self.add_tag(name, TagCategory.DIFFICULTY, desc)
        
        # Quest type tags
        quest_tags = [
            ("meditation_quest", "Contemplative and meditative challenges"),
            ("challenge_quest", "Active challenges requiring skill"),
            ("riddle_quest", "Intellectual puzzles and riddles"),
            ("practice_quest", "Hands-on practice and application"),
            ("synthesis_quest", "Cross-tradition synthesis challenges"),
            ("transcendence_quest", "Ultimate realization challenges")
        ]
        
        for name, desc in quest_tags:
            self.add_tag(name, TagCategory.QUEST_TYPE, desc)
    
    def add_tag(self, name: str, category: TagCategory, description: str, 
                aliases: List[str] = None, parent_tags: List[str] = None) -> Tag:
        """Add a new tag to the system"""
        if name in self.tags:
            return self.tags[name]
        
        tag = Tag(
            name=name,
            category=category,
            description=description,
            aliases=aliases or [],
            parent_tags=parent_tags or []
        )
        
        self.tags[name] = tag
        self.category_index[category].add(name)
        
        # Update parent-child relationships
        if parent_tags:
            for parent_name in parent_tags:
                if parent_name in self.tags:
                    self.tags[parent_name].child_tags.append(name)
        
        return tag
    
    def get_tags_by_category(self, category: TagCategory) -> List[Tag]:
        """Get all tags in a specific category"""
        return [self.tags[name] for name in self.category_index[category]]
    
    def suggest_tags(self, content: str, tradition: str = None) -> List[str]:
        """Suggest relevant tags based on content analysis"""
        suggested = []
        content_lower = content.lower()
        
        # Add tradition tag if specified
        if tradition and tradition in self.tags:
            suggested.append(tradition)
        
        # Analyze content for relevant tags
        for tag_name, tag in self.tags.items():
            # Check if tag name or aliases appear in content
            if tag_name.replace('_', ' ') in content_lower:
                suggested.append(tag_name)
                continue
            
            for alias in tag.aliases:
                if alias.lower() in content_lower:
                    suggested.append(tag_name)
                    break
        
        # Remove duplicates and limit suggestions
        return list(set(suggested))[:10]
    
    def validate_tag_combination(self, tags: List[str]) -> Dict[str, any]:
        """Validate a combination of tags for consistency"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'suggestions': [],
            'conflicts': []
        }
        
        # Check for conflicting elements
        elements = [tag for tag in tags if tag in self.category_index[TagCategory.ELEMENT]]
        if len(elements) > 2:
            validation_result['warnings'].append(
                f"Multiple elements detected: {elements}. Consider limiting to 1-2 primary elements."
            )
        
        # Check for conflicting planets
        planets = [tag for tag in tags if tag in self.category_index[TagCategory.PLANET]]
        if len(planets) > 3:
            validation_result['warnings'].append(
                f"Multiple planets detected: {planets}. Consider limiting to 1-3 primary planets."
            )
        
        # Suggest missing complementary tags
        if any(tag in self.category_index[TagCategory.PRACTICE] for tag in tags):
            if not any(tag in self.category_index[TagCategory.CONCEPT] for tag in tags):
                validation_result['suggestions'].append(
                    "Consider adding conceptual tags to complement practice tags."
                )
        
        return validation_result
    
    def export_tag_hierarchy(self) -> Dict:
        """Export complete tag hierarchy for JSON schema"""
        hierarchy = {}
        
        for category in TagCategory:
            category_tags = {}
            for tag_name in self.category_index[category]:
                tag = self.tags[tag_name]
                category_tags[tag_name] = {
                    'description': tag.description,
                    'aliases': tag.aliases,
                    'parent_tags': tag.parent_tags,
                    'child_tags': tag.child_tags,
                    'usage_count': tag.usage_count
                }
            hierarchy[category.value] = category_tags
        
        return hierarchy
    
    def get_tag_statistics(self) -> Dict:
        """Get comprehensive statistics about tag usage"""
        stats = {
            'total_tags': len(self.tags),
            'category_counts': {
                category.value: len(self.category_index[category]) 
                for category in TagCategory
            },
            'most_used_tags': sorted(
                [(tag.name, tag.usage_count) for tag in self.tags.values()],
                key=lambda x: x[1], reverse=True
            )[:10],
            'authenticity_verified_count': sum(
                1 for tag in self.tags.values() if tag.authenticity_verified
            )
        }
        
        return stats

# Initialize global tagging system
GLOBAL_TAGGING_SYSTEM = TaggingSystem()

def get_tagging_system() -> TaggingSystem:
    """Get the global tagging system instance"""
    return GLOBAL_TAGGING_SYSTEM
