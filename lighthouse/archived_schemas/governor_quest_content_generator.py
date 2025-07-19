"""
Enochian Cyphers Governor Quest Content Generator
Generates authentic quest content for each Governor Angel based on completed research
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

class QuestType(Enum):
    """Types of quests based on mystical practices"""
    MEDITATION = "meditation"
    CHALLENGE = "challenge"
    RIDDLE = "riddle"
    PRACTICE = "practice"
    SYNTHESIS = "synthesis"
    TRANSCENDENCE = "transcendence"

class DifficultyTier(Enum):
    """Difficulty tiers mapped to Enochian Aethyrs"""
    FOUNDATION = (1, 7)      # TEX-ZAA
    DEVELOPMENT = (8, 15)    # BAG-ZIM
    MASTERY = (16, 23)       # LOE-ASP
    TRANSCENDENCE = (24, 30) # KHR-LIL

@dataclass
class QuestTemplate:
    """Template for generating specific quest content"""
    id: str
    title_template: str
    description_template: str
    quest_type: QuestType
    difficulty_range: Tuple[int, int]
    energy_cost_range: Tuple[int, int]
    reputation_reward_range: Tuple[int, int]
    required_concepts: List[str]
    tradition_specific: bool = True
    
    def generate_quest(self, governor_data: Dict, tradition_knowledge: Dict) -> Dict:
        """Generate specific quest from template"""
        # Implementation would use template variables and tradition knowledge
        pass

class GovernorQuestContentGenerator:
    """Generates quest content for Governor Angels based on authentic research"""
    
    def __init__(self):
        self.tradition_knowledge = self._load_tradition_knowledge()
        self.quest_templates = self._initialize_quest_templates()
        self.aethyr_mappings = self._initialize_aethyr_mappings()
        
    def _load_tradition_knowledge(self) -> Dict[str, Dict]:
        """Load authentic knowledge from completed research phases"""
        # This would load from the research data populated in Phases 1-5
        return {
            'enochian_magic': {
                'core_concepts': ['aethyr', 'governor', 'enochian_key', 'sigil', 'scrying'],
                'practices': ['invocation', 'vision_work', 'angelic_communication'],
                'wisdom_themes': ['divine_will', 'cosmic_order', 'spiritual_hierarchy'],
                'authentic_sources': {
                    'primary': 'John Dee\'s Five Books of Mystery',
                    'secondary': 'Liber Chanokh (Liber LXXXIV)',
                    'validation': 'Sacred Texts Archive verification'
                },
                'key_teachings': [
                    'The 30 Aethyrs represent progressive spiritual realms',
                    'Governor Angels rule specific regions of consciousness',
                    'Enochian Keys unlock communication with angelic hierarchy',
                    'Scrying reveals divine wisdom through symbolic vision'
                ]
            },
            'i_ching': {
                'core_concepts': ['hexagram', 'trigram', 'yin_yang', 'judgment', 'image'],
                'practices': ['divination', 'meditation', 'contemplation', 'decision_making'],
                'wisdom_themes': ['change', 'balance', 'natural_order', 'timing'],
                'authentic_sources': {
                    'primary': 'Wilhelm Translation of Book of Changes',
                    'secondary': 'Traditional Chinese commentaries',
                    'validation': 'University of Parma online text'
                },
                'key_teachings': [
                    'Change is the only constant in the universe',
                    'Yin and Yang represent complementary forces',
                    'Proper timing aligns action with natural flow',
                    'Hexagrams reveal patterns of transformation'
                ]
            },
            'hermetic_qabalah': {
                'core_concepts': ['sephirah', 'tree_of_life', 'path', 'correspondence'],
                'practices': ['meditation', 'pathworking', 'correspondence_study'],
                'wisdom_themes': ['consciousness', 'emanation', 'divine_attributes'],
                'authentic_sources': {
                    'primary': 'Colin Low\'s Notes on Kabbalah',
                    'secondary': 'Sacred Texts Archive materials',
                    'validation': 'Cross-referenced with scholarly sources'
                },
                'key_teachings': [
                    'Ten Sephiroth represent stages of consciousness',
                    'Tree of Life maps divine emanation process',
                    'As above, so below - correspondence principle',
                    'Pathworking develops spiritual understanding'
                ]
            },
            'tarot': {
                'core_concepts': ['major_arcana', 'minor_arcana', 'suit', 'symbolism'],
                'practices': ['divination', 'meditation', 'symbolic_study'],
                'wisdom_themes': ['journey', 'archetypes', 'life_lessons'],
                'authentic_sources': {
                    'primary': 'Rider-Waite-Smith deck meanings',
                    'secondary': 'Labyrinthos Academy documentation',
                    'validation': 'Traditional interpretations confirmed'
                },
                'key_teachings': [
                    'Major Arcana represents the Fool\'s spiritual journey',
                    'Minor Arcana reflects daily life experiences',
                    'Symbols carry universal archetypal meanings',
                    'Cards reveal hidden patterns and guidance'
                ]
            }
            # Additional traditions would be loaded from research data
        }
    
    def _initialize_quest_templates(self) -> Dict[str, List[QuestTemplate]]:
        """Initialize quest templates for each tradition"""
        templates = {
            'enochian_magic': [
                QuestTemplate(
                    id="enochian_scrying_basic",
                    title_template="Scrying the {aethyr_name} Aethyr",
                    description_template="Enter a meditative state and attempt to scry the {aethyr_name} Aethyr. Record your visions and interpret their symbolic meaning according to Enochian tradition.",
                    quest_type=QuestType.MEDITATION,
                    difficulty_range=(1, 10),
                    energy_cost_range=(3, 8),
                    reputation_reward_range=(5, 15),
                    required_concepts=['aethyr', 'scrying', 'vision']
                ),
                QuestTemplate(
                    id="enochian_key_invocation",
                    title_template="Invoke the {key_number} Enochian Key",
                    description_template="Study and properly invoke the {key_number} Enochian Key. Focus on the vibrational qualities of the Enochian language and its effect on consciousness.",
                    quest_type=QuestType.PRACTICE,
                    difficulty_range=(5, 20),
                    energy_cost_range=(5, 12),
                    reputation_reward_range=(10, 25),
                    required_concepts=['enochian_key', 'invocation', 'vibration']
                ),
                QuestTemplate(
                    id="governor_communication",
                    title_template="Commune with Governor {governor_name}",
                    description_template="Establish communication with Governor {governor_name} through proper ritual preparation and invocation. Seek wisdom regarding {wisdom_theme}.",
                    quest_type=QuestType.CHALLENGE,
                    difficulty_range=(10, 30),
                    energy_cost_range=(8, 20),
                    reputation_reward_range=(15, 40),
                    required_concepts=['governor', 'communication', 'ritual']
                )
            ],
            'i_ching': [
                QuestTemplate(
                    id="hexagram_meditation",
                    title_template="Meditate on Hexagram {hexagram_number}: {hexagram_name}",
                    description_template="Contemplate the meaning of Hexagram {hexagram_number} ({hexagram_name}). Study the Judgment, Image, and changing lines. Apply its wisdom to a current life situation.",
                    quest_type=QuestType.MEDITATION,
                    difficulty_range=(1, 15),
                    energy_cost_range=(2, 6),
                    reputation_reward_range=(3, 12),
                    required_concepts=['hexagram', 'judgment', 'contemplation']
                ),
                QuestTemplate(
                    id="trigram_balance",
                    title_template="Balance the {trigram_name} Trigram Energy",
                    description_template="Work with the {trigram_name} trigram to understand its elemental qualities. Practice exercises to balance this energy within yourself.",
                    quest_type=QuestType.PRACTICE,
                    difficulty_range=(3, 12),
                    energy_cost_range=(4, 8),
                    reputation_reward_range=(6, 16),
                    required_concepts=['trigram', 'balance', 'elemental']
                ),
                QuestTemplate(
                    id="change_navigation",
                    title_template="Navigate Change with {principle} Principle",
                    description_template="Apply the I Ching principle of {principle} to navigate a period of change in your life. Document insights and outcomes.",
                    quest_type=QuestType.SYNTHESIS,
                    difficulty_range=(8, 25),
                    energy_cost_range=(6, 15),
                    reputation_reward_range=(12, 30),
                    required_concepts=['change', 'principle', 'application']
                )
            ]
            # Additional tradition templates would be defined here
        }
        return templates
    
    def _initialize_aethyr_mappings(self) -> Dict[int, Dict]:
        """Initialize Aethyr mappings with authentic names and attributes"""
        # Based on research from Liber Chanokh
        aethyr_names = [
            "TEX", "RII", "BAG", "ZAA", "DES", "VTI", "NIA", "TOR", "LIN",
            "ASP", "KHR", "POP", "ZEN", "TAN", "LEA", "OXO", "UTA", "ZIM",
            "LOE", "ICH", "ZAX", "ZIP", "ZID", "DEO", "MAZ", "LIT", "PAZ",
            "ZOM", "ARN", "LIL"
        ]
        
        mappings = {}
        for i, name in enumerate(aethyr_names, 1):
            tier = self._get_difficulty_tier(i)
            mappings[i] = {
                'name': name,
                'number': i,
                'tier': tier,
                'description': f"The {name} Aethyr - {tier.name.title()} level spiritual realm"
            }
        
        return mappings
    
    def _get_difficulty_tier(self, aethyr_number: int) -> DifficultyTier:
        """Get difficulty tier for Aethyr number"""
        for tier in DifficultyTier:
            min_tier, max_tier = tier.value
            if min_tier <= aethyr_number <= max_tier:
                return tier
        return DifficultyTier.FOUNDATION
    
    def generate_governor_questline(self, governor_id: int, governor_data: Dict) -> Dict:
        """Generate complete questline for a Governor Angel"""
        primary_tradition = governor_data.get('primary_tradition', 'enochian_magic')
        secondary_traditions = governor_data.get('secondary_traditions', [])
        aethyr_number = governor_data.get('aethyr_association', {}).get('aethyr_number', 1)
        
        questline = {
            'governor_id': governor_id,
            'governor_name': governor_data.get('name', f'Governor_{governor_id}'),
            'primary_tradition': primary_tradition,
            'aethyr_association': self.aethyr_mappings.get(aethyr_number, {}),
            'total_quests': 0,
            'difficulty_progression': [],
            'quests': []
        }
        
        # Generate quests for each difficulty level
        difficulty_levels = self._calculate_difficulty_progression(aethyr_number)
        
        for level_data in difficulty_levels:
            level_quests = self._generate_level_quests(
                level_data, primary_tradition, secondary_traditions, governor_data
            )
            questline['quests'].extend(level_quests)
            questline['difficulty_progression'].append({
                'level': level_data['level'],
                'quest_count': len(level_quests),
                'reputation_required': level_data['reputation_required'],
                'energy_cost_range': level_data['energy_cost_range']
            })
        
        questline['total_quests'] = len(questline['quests'])
        
        return questline
    
    def _calculate_difficulty_progression(self, aethyr_number: int) -> List[Dict]:
        """Calculate difficulty progression based on Aethyr tier"""
        base_tier = self._get_difficulty_tier(aethyr_number)
        
        # Standard 10-level progression with Aethyr-based scaling
        levels = []
        for level in range(1, 11):
            # Scale difficulty based on Aethyr tier
            tier_multiplier = {
                DifficultyTier.FOUNDATION: 1.0,
                DifficultyTier.DEVELOPMENT: 1.3,
                DifficultyTier.MASTERY: 1.6,
                DifficultyTier.TRANSCENDENCE: 2.0
            }[base_tier]
            
            base_reputation = level * 10
            scaled_reputation = int(base_reputation * tier_multiplier)
            
            levels.append({
                'level': level,
                'reputation_required': min(scaled_reputation, 100),
                'energy_cost_range': {
                    'min': max(1, int(level * tier_multiplier)),
                    'max': min(25, int((level + 5) * tier_multiplier))
                },
                'quest_count_range': (6, 12) if level <= 5 else (8, 15)
            })
        
        return levels
    
    def _generate_level_quests(self, level_data: Dict, primary_tradition: str, 
                              secondary_traditions: List[str], governor_data: Dict) -> List[Dict]:
        """Generate quests for a specific difficulty level"""
        quest_count = random.randint(*level_data['quest_count_range'])
        level_quests = []
        
        # Get templates for primary tradition
        primary_templates = self.quest_templates.get(primary_tradition, [])
        
        # Filter templates by difficulty
        suitable_templates = [
            template for template in primary_templates
            if (template.difficulty_range[0] <= level_data['level'] <= template.difficulty_range[1])
        ]
        
        if not suitable_templates:
            # Fallback to basic templates
            suitable_templates = primary_templates[:3] if primary_templates else []
        
        # Generate primary tradition quests (70% of total)
        primary_count = int(quest_count * 0.7)
        for i in range(primary_count):
            if suitable_templates:
                template = random.choice(suitable_templates)
                quest = self._generate_quest_from_template(
                    template, level_data, governor_data, primary_tradition
                )
                level_quests.append(quest)
        
        # Generate secondary tradition quests (20% of total)
        secondary_count = int(quest_count * 0.2)
        for tradition in secondary_traditions[:2]:  # Max 2 secondary traditions
            if tradition in self.quest_templates:
                secondary_templates = self.quest_templates[tradition]
                suitable_secondary = [
                    t for t in secondary_templates
                    if t.difficulty_range[0] <= level_data['level'] <= t.difficulty_range[1]
                ]
                
                if suitable_secondary:
                    template = random.choice(suitable_secondary)
                    quest = self._generate_quest_from_template(
                        template, level_data, governor_data, tradition
                    )
                    level_quests.append(quest)
        
        # Generate synthesis quests (10% of total)
        synthesis_count = quest_count - len(level_quests)
        for i in range(synthesis_count):
            synthesis_quest = self._generate_synthesis_quest(
                level_data, governor_data, primary_tradition, secondary_traditions
            )
            level_quests.append(synthesis_quest)
        
        return level_quests
    
    def _generate_quest_from_template(self, template: QuestTemplate, level_data: Dict,
                                    governor_data: Dict, tradition: str) -> Dict:
        """Generate specific quest from template"""
        # Get tradition knowledge
        tradition_knowledge = self.tradition_knowledge.get(tradition, {})
        
        # Calculate quest parameters
        energy_cost = random.randint(*level_data['energy_cost_range'])
        reputation_reward = random.randint(*template.reputation_reward_range)
        
        # Generate quest content
        quest = {
            'id': f"{governor_data.get('id', 1)}_{template.id}_{level_data['level']}_{random.randint(1000, 9999)}",
            'title': self._fill_template(template.title_template, governor_data, tradition_knowledge),
            'description': self._fill_template(template.description_template, governor_data, tradition_knowledge),
            'quest_type': template.quest_type.value,
            'tradition': tradition,
            'difficulty_level': level_data['level'],
            'energy_cost': energy_cost,
            'reputation_reward': reputation_reward,
            'required_concepts': template.required_concepts,
            'completion_criteria': self._generate_completion_criteria(template, tradition_knowledge),
            'wisdom_teaching': self._select_wisdom_teaching(tradition_knowledge),
            'cross_references': self._generate_cross_references(tradition, template.required_concepts)
        }
        
        return quest
    
    def _fill_template(self, template_str: str, governor_data: Dict, tradition_knowledge: Dict) -> str:
        """Fill template string with actual values"""
        # This would implement template variable substitution
        # For now, return template as-is with basic substitutions
        result = template_str
        
        # Basic substitutions
        if '{governor_name}' in result:
            result = result.replace('{governor_name}', governor_data.get('name', 'Unknown'))
        
        if '{aethyr_name}' in result:
            aethyr_assoc = governor_data.get('aethyr_association', {})
            result = result.replace('{aethyr_name}', aethyr_assoc.get('aethyr_name', 'TEX'))
        
        return result
    
    def _generate_completion_criteria(self, template: QuestTemplate, tradition_knowledge: Dict) -> List[str]:
        """Generate completion criteria for quest"""
        criteria = []
        
        if template.quest_type == QuestType.MEDITATION:
            criteria = [
                "Complete 20-minute focused meditation session",
                "Record insights and symbolic impressions",
                "Demonstrate understanding of core concepts"
            ]
        elif template.quest_type == QuestType.PRACTICE:
            criteria = [
                "Perform practice correctly according to tradition",
                "Document experience and results",
                "Show integration of technique"
            ]
        elif template.quest_type == QuestType.CHALLENGE:
            criteria = [
                "Successfully complete the challenge requirements",
                "Demonstrate mastery of required skills",
                "Reflect on lessons learned"
            ]
        
        return criteria
    
    def _select_wisdom_teaching(self, tradition_knowledge: Dict) -> str:
        """Select appropriate wisdom teaching for quest"""
        teachings = tradition_knowledge.get('key_teachings', [])
        return random.choice(teachings) if teachings else "Seek wisdom through direct experience."
    
    def _generate_cross_references(self, tradition: str, concepts: List[str]) -> Dict:
        """Generate cross-references to related content"""
        return {
            'related_traditions': [],  # Would be populated based on concept analysis
            'mystical_entries': [],    # Would reference specific knowledge entries
            'prerequisite_quests': [], # Would reference earlier quests
            'follow_up_quests': []     # Would reference later quests
        }
    
    def _generate_synthesis_quest(self, level_data: Dict, governor_data: Dict,
                                 primary_tradition: str, secondary_traditions: List[str]) -> Dict:
        """Generate cross-tradition synthesis quest"""
        # This would create quests that combine multiple traditions
        return {
            'id': f"{governor_data.get('id', 1)}_synthesis_{level_data['level']}_{random.randint(1000, 9999)}",
            'title': f"Synthesis: {primary_tradition.replace('_', ' ').title()} Integration",
            'description': f"Integrate wisdom from {primary_tradition} with insights from secondary traditions.",
            'quest_type': QuestType.SYNTHESIS.value,
            'tradition': 'synthesis',
            'difficulty_level': level_data['level'],
            'energy_cost': random.randint(*level_data['energy_cost_range']),
            'reputation_reward': level_data['level'] * 3,
            'required_concepts': ['synthesis', 'integration', 'wisdom'],
            'completion_criteria': [
                "Identify connections between traditions",
                "Create synthesis framework",
                "Apply integrated understanding"
            ],
            'wisdom_teaching': "True wisdom emerges from the synthesis of diverse paths.",
            'cross_references': {
                'primary_tradition': primary_tradition,
                'secondary_traditions': secondary_traditions
            }
        }

# Initialize global generator
QUEST_CONTENT_GENERATOR = GovernorQuestContentGenerator()

def get_quest_content_generator() -> GovernorQuestContentGenerator:
    """Get the global quest content generator instance"""
    return QUEST_CONTENT_GENERATOR
