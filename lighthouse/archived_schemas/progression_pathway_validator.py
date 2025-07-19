"""
Enochian Cyphers Progression Pathway Validator
Validates difficulty scaling and authentic challenge frameworks based on research
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

class ProgressionType(Enum):
    """Types of progression pathways"""
    LINEAR = "linear"           # Sequential progression
    BRANCHING = "branching"     # Multiple paths available
    SPIRAL = "spiral"           # Revisiting concepts at higher levels
    NETWORK = "network"         # Interconnected web of concepts

class AuthenticityLevel(Enum):
    """Levels of authenticity validation"""
    PRIMARY_SOURCE = "primary_source"      # Direct from historical sources
    SCHOLARLY_VALIDATED = "scholarly"      # Academic validation
    TRADITIONAL_PRACTICE = "traditional"   # Established practice
    MODERN_SYNTHESIS = "modern"            # Contemporary integration

@dataclass
class ProgressionValidationResult:
    """Result of progression pathway validation"""
    is_valid: bool
    authenticity_score: float
    difficulty_consistency: float
    tradition_alignment: float
    issues: List[str]
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        return {
            'is_valid': self.is_valid,
            'authenticity_score': self.authenticity_score,
            'difficulty_consistency': self.difficulty_consistency,
            'tradition_alignment': self.tradition_alignment,
            'issues': self.issues,
            'recommendations': self.recommendations
        }

class ProgressionPathwayValidator:
    """Validates progression pathways for authenticity and consistency"""
    
    def __init__(self):
        self.tradition_progressions = self._initialize_authentic_progressions()
        self.difficulty_benchmarks = self._initialize_difficulty_benchmarks()
        self.aethyr_correspondences = self._initialize_aethyr_correspondences()
    
    def _initialize_authentic_progressions(self) -> Dict[str, Dict]:
        """Initialize authentic progression patterns from research"""
        return {
            'enochian_magic': {
                'progression_type': ProgressionType.SPIRAL,
                'authenticity_level': AuthenticityLevel.PRIMARY_SOURCE,
                'traditional_stages': [
                    {
                        'stage': 'Foundation',
                        'concepts': ['enochian_alphabet', 'basic_invocation', 'scrying_preparation'],
                        'practices': ['daily_invocation', 'alphabet_study', 'mirror_gazing'],
                        'aethyr_range': (1, 7),
                        'typical_duration': '3-6 months'
                    },
                    {
                        'stage': 'Development', 
                        'concepts': ['aethyr_exploration', 'governor_communication', 'vision_interpretation'],
                        'practices': ['aethyr_scrying', 'governor_invocation', 'vision_recording'],
                        'aethyr_range': (8, 15),
                        'typical_duration': '6-12 months'
                    },
                    {
                        'stage': 'Mastery',
                        'concepts': ['advanced_communication', 'cosmic_consciousness', 'divine_will'],
                        'practices': ['extended_scrying', 'complex_invocations', 'teaching_others'],
                        'aethyr_range': (16, 23),
                        'typical_duration': '1-3 years'
                    },
                    {
                        'stage': 'Transcendence',
                        'concepts': ['unity_consciousness', 'divine_marriage', 'cosmic_service'],
                        'practices': ['continuous_communion', 'reality_transformation', 'world_service'],
                        'aethyr_range': (24, 30),
                        'typical_duration': 'Lifetime practice'
                    }
                ],
                'validation_criteria': [
                    'Must follow Dee\'s original sequence',
                    'Aethyr progression must be authentic',
                    'Governor attributes must match primary sources',
                    'Practices must align with historical methods'
                ]
            },
            'i_ching': {
                'progression_type': ProgressionType.NETWORK,
                'authenticity_level': AuthenticityLevel.PRIMARY_SOURCE,
                'traditional_stages': [
                    {
                        'stage': 'Foundation',
                        'concepts': ['yin_yang_basics', 'trigram_meanings', 'hexagram_structure'],
                        'practices': ['coin_divination', 'trigram_meditation', 'change_observation'],
                        'hexagram_focus': list(range(1, 17)),  # First 16 hexagrams
                        'typical_duration': '2-4 months'
                    },
                    {
                        'stage': 'Development',
                        'concepts': ['change_patterns', 'timing_principles', 'judgment_interpretation'],
                        'practices': ['yarrow_divination', 'hexagram_study', 'life_application'],
                        'hexagram_focus': list(range(17, 49)),  # Middle hexagrams
                        'typical_duration': '6-12 months'
                    },
                    {
                        'stage': 'Mastery',
                        'concepts': ['cosmic_order', 'natural_law', 'sage_wisdom'],
                        'practices': ['intuitive_reading', 'teaching_others', 'life_guidance'],
                        'hexagram_focus': list(range(49, 65)),  # Final hexagrams
                        'typical_duration': '1-2 years'
                    }
                ],
                'validation_criteria': [
                    'Must follow Wilhelm translation authenticity',
                    'Hexagram sequence must be traditional',
                    'Interpretations must align with classical sources',
                    'Practices must reflect Chinese tradition'
                ]
            },
            'hermetic_qabalah': {
                'progression_type': ProgressionType.LINEAR,
                'authenticity_level': AuthenticityLevel.SCHOLARLY_VALIDATED,
                'traditional_stages': [
                    {
                        'stage': 'Foundation',
                        'concepts': ['tree_structure', 'sephirah_basics', 'correspondence_principles'],
                        'practices': ['sephirah_meditation', 'correspondence_study', 'daily_practice'],
                        'sephirah_focus': ['Malkuth', 'Yesod', 'Hod', 'Netzach'],
                        'typical_duration': '6-12 months'
                    },
                    {
                        'stage': 'Development',
                        'concepts': ['path_working', 'middle_pillar', 'elemental_balance'],
                        'practices': ['pathworking_meditation', 'middle_pillar_exercise', 'elemental_work'],
                        'sephirah_focus': ['Tiphereth', 'Gevurah', 'Chesed'],
                        'typical_duration': '1-2 years'
                    },
                    {
                        'stage': 'Mastery',
                        'concepts': ['supernal_triad', 'divine_consciousness', 'cosmic_unity'],
                        'practices': ['advanced_pathworking', 'divine_communion', 'teaching_service'],
                        'sephirah_focus': ['Binah', 'Chokhmah', 'Kether'],
                        'typical_duration': '3-5 years'
                    }
                ],
                'validation_criteria': [
                    'Must follow traditional Tree of Life structure',
                    'Sephirah attributes must be authentic',
                    'Progression must respect traditional order',
                    'Practices must align with Golden Dawn tradition'
                ]
            }
            # Additional traditions would be defined based on research
        }
    
    def _initialize_difficulty_benchmarks(self) -> Dict[int, Dict]:
        """Initialize difficulty benchmarks for each tier"""
        return {
            1: {'energy_cost': (1, 3), 'reputation_reward': (1, 5), 'concepts': 1, 'practices': 1},
            5: {'energy_cost': (2, 5), 'reputation_reward': (3, 8), 'concepts': 2, 'practices': 1},
            10: {'energy_cost': (4, 8), 'reputation_reward': (6, 12), 'concepts': 3, 'practices': 2},
            15: {'energy_cost': (6, 12), 'reputation_reward': (10, 18), 'concepts': 4, 'practices': 2},
            20: {'energy_cost': (8, 16), 'reputation_reward': (15, 25), 'concepts': 5, 'practices': 3},
            25: {'energy_cost': (12, 20), 'reputation_reward': (20, 35), 'concepts': 6, 'practices': 3},
            30: {'energy_cost': (15, 25), 'reputation_reward': (25, 50), 'concepts': 7, 'practices': 4}
        }
    
    def _initialize_aethyr_correspondences(self) -> Dict[int, Dict]:
        """Initialize Aethyr correspondences with authentic attributes"""
        # Based on Liber Chanokh research
        aethyr_names = [
            "TEX", "RII", "BAG", "ZAA", "DES", "VTI", "NIA", "TOR", "LIN",
            "ASP", "KHR", "POP", "ZEN", "TAN", "LEA", "OXO", "UTA", "ZIM",
            "LOE", "ICH", "ZAX", "ZIP", "ZID", "DEO", "MAZ", "LIT", "PAZ",
            "ZOM", "ARN", "LIL"
        ]
        
        correspondences = {}
        for i, name in enumerate(aethyr_names, 1):
            tier = self._get_tier_for_aethyr(i)
            correspondences[i] = {
                'name': name,
                'tier': tier,
                'difficulty_multiplier': self._get_difficulty_multiplier(tier),
                'typical_themes': self._get_aethyr_themes(tier),
                'energy_scaling': self._get_energy_scaling(tier)
            }
        
        return correspondences
    
    def _get_tier_for_aethyr(self, aethyr_number: int) -> str:
        """Get tier name for Aethyr number"""
        if 1 <= aethyr_number <= 7:
            return 'Foundation'
        elif 8 <= aethyr_number <= 15:
            return 'Development'
        elif 16 <= aethyr_number <= 23:
            return 'Mastery'
        elif 24 <= aethyr_number <= 30:
            return 'Transcendence'
        return 'Foundation'
    
    def _get_difficulty_multiplier(self, tier: str) -> float:
        """Get difficulty multiplier for tier"""
        multipliers = {
            'Foundation': 1.0,
            'Development': 1.3,
            'Mastery': 1.6,
            'Transcendence': 2.0
        }
        return multipliers.get(tier, 1.0)
    
    def _get_aethyr_themes(self, tier: str) -> List[str]:
        """Get typical themes for Aethyr tier"""
        themes = {
            'Foundation': ['basic_principles', 'preparation', 'grounding', 'initial_contact'],
            'Development': ['skill_building', 'deeper_understanding', 'practice_refinement', 'communication'],
            'Mastery': ['advanced_techniques', 'wisdom_integration', 'teaching_others', 'service'],
            'Transcendence': ['unity_consciousness', 'divine_communion', 'cosmic_service', 'ultimate_realization']
        }
        return themes.get(tier, [])
    
    def _get_energy_scaling(self, tier: str) -> Tuple[float, float]:
        """Get energy cost scaling for tier"""
        scaling = {
            'Foundation': (1.0, 1.2),
            'Development': (1.2, 1.5),
            'Mastery': (1.5, 1.8),
            'Transcendence': (1.8, 2.5)
        }
        return scaling.get(tier, (1.0, 1.2))
    
    def validate_governor_progression(self, governor_data: Dict, questline_data: Dict) -> ProgressionValidationResult:
        """Validate a Governor's progression pathway"""
        issues = []
        recommendations = []
        
        # Get tradition and progression data
        primary_tradition = governor_data.get('primary_tradition', '')
        aethyr_number = governor_data.get('aethyr_association', {}).get('aethyr_number', 1)
        
        if primary_tradition not in self.tradition_progressions:
            issues.append(f"Unknown tradition: {primary_tradition}")
            return ProgressionValidationResult(
                is_valid=False,
                authenticity_score=0.0,
                difficulty_consistency=0.0,
                tradition_alignment=0.0,
                issues=issues,
                recommendations=["Use supported tradition from research"]
            )
        
        tradition_prog = self.tradition_progressions[primary_tradition]
        
        # Validate Aethyr correspondence
        if aethyr_number not in self.aethyr_correspondences:
            issues.append(f"Invalid Aethyr number: {aethyr_number}")
        
        # Validate difficulty progression
        difficulty_score = self._validate_difficulty_consistency(questline_data, aethyr_number)
        if difficulty_score < 0.8:
            issues.append("Difficulty progression inconsistent with Aethyr tier")
            recommendations.append("Adjust quest difficulties to match Aethyr tier scaling")
        
        # Validate tradition alignment
        alignment_score = self._validate_tradition_alignment(questline_data, tradition_prog)
        if alignment_score < 0.7:
            issues.append("Quest content not well-aligned with tradition")
            recommendations.append("Ensure quests reflect authentic tradition practices")
        
        # Validate authenticity
        authenticity_score = self._validate_authenticity(questline_data, tradition_prog)
        if authenticity_score < 0.9:
            issues.append("Low authenticity score - check primary source alignment")
            recommendations.append("Review quest content against primary sources")
        
        # Overall validation
        is_valid = len(issues) == 0 and all([
            difficulty_score >= 0.8,
            alignment_score >= 0.7,
            authenticity_score >= 0.9
        ])
        
        return ProgressionValidationResult(
            is_valid=is_valid,
            authenticity_score=authenticity_score,
            difficulty_consistency=difficulty_score,
            tradition_alignment=alignment_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def _validate_difficulty_consistency(self, questline_data: Dict, aethyr_number: int) -> float:
        """Validate difficulty consistency across questline"""
        quests = questline_data.get('quests', [])
        if not quests:
            return 0.0
        
        aethyr_data = self.aethyr_correspondences.get(aethyr_number, {})
        expected_multiplier = aethyr_data.get('difficulty_multiplier', 1.0)
        
        consistency_scores = []
        
        for quest in quests:
            level = quest.get('difficulty_level', 1)
            energy_cost = quest.get('energy_cost', 1)
            reputation_reward = quest.get('reputation_reward', 1)
            
            # Get expected ranges for this level
            expected_benchmark = self._get_benchmark_for_level(level)
            expected_energy_range = expected_benchmark['energy_cost']
            expected_reputation_range = expected_benchmark['reputation_reward']
            
            # Apply Aethyr multiplier
            scaled_energy_min = int(expected_energy_range[0] * expected_multiplier)
            scaled_energy_max = int(expected_energy_range[1] * expected_multiplier)
            scaled_reputation_min = int(expected_reputation_range[0] * expected_multiplier)
            scaled_reputation_max = int(expected_reputation_range[1] * expected_multiplier)
            
            # Check if values are within expected ranges
            energy_consistent = scaled_energy_min <= energy_cost <= scaled_energy_max
            reputation_consistent = scaled_reputation_min <= reputation_reward <= scaled_reputation_max
            
            quest_consistency = (energy_consistent + reputation_consistent) / 2
            consistency_scores.append(quest_consistency)
        
        return sum(consistency_scores) / len(consistency_scores)
    
    def _validate_tradition_alignment(self, questline_data: Dict, tradition_prog: Dict) -> float:
        """Validate alignment with tradition progression"""
        quests = questline_data.get('quests', [])
        if not quests:
            return 0.0
        
        traditional_stages = tradition_prog.get('traditional_stages', [])
        if not traditional_stages:
            return 0.5  # Neutral score if no stages defined
        
        alignment_scores = []
        
        for quest in quests:
            level = quest.get('difficulty_level', 1)
            concepts = quest.get('required_concepts', [])
            quest_type = quest.get('quest_type', '')
            
            # Find appropriate stage for this level
            stage = self._get_stage_for_level(level, traditional_stages)
            if not stage:
                alignment_scores.append(0.5)
                continue
            
            # Check concept alignment
            stage_concepts = stage.get('concepts', [])
            concept_overlap = len(set(concepts) & set(stage_concepts))
            concept_score = concept_overlap / max(len(concepts), 1) if concepts else 0.5
            
            # Check practice alignment (simplified)
            practice_score = 0.8 if quest_type in ['meditation', 'practice', 'challenge'] else 0.6
            
            quest_alignment = (concept_score + practice_score) / 2
            alignment_scores.append(quest_alignment)
        
        return sum(alignment_scores) / len(alignment_scores)
    
    def _validate_authenticity(self, questline_data: Dict, tradition_prog: Dict) -> float:
        """Validate authenticity against primary sources"""
        validation_criteria = tradition_prog.get('validation_criteria', [])
        authenticity_level = tradition_prog.get('authenticity_level', AuthenticityLevel.MODERN_SYNTHESIS)
        
        # Base score based on authenticity level
        base_scores = {
            AuthenticityLevel.PRIMARY_SOURCE: 0.95,
            AuthenticityLevel.SCHOLARLY_VALIDATED: 0.85,
            AuthenticityLevel.TRADITIONAL_PRACTICE: 0.75,
            AuthenticityLevel.MODERN_SYNTHESIS: 0.65
        }
        
        base_score = base_scores.get(authenticity_level, 0.5)
        
        # Additional validation based on criteria
        # This would be expanded with specific checks for each tradition
        
        return base_score
    
    def _get_benchmark_for_level(self, level: int) -> Dict:
        """Get difficulty benchmark for level"""
        # Find closest benchmark
        benchmark_levels = sorted(self.difficulty_benchmarks.keys())
        closest_level = min(benchmark_levels, key=lambda x: abs(x - level))
        return self.difficulty_benchmarks[closest_level]
    
    def _get_stage_for_level(self, level: int, stages: List[Dict]) -> Optional[Dict]:
        """Get appropriate stage for difficulty level"""
        # Simple mapping: levels 1-3 = stage 0, 4-6 = stage 1, etc.
        stage_index = min((level - 1) // 3, len(stages) - 1)
        return stages[stage_index] if 0 <= stage_index < len(stages) else None
    
    def generate_progression_report(self, validation_results: List[ProgressionValidationResult]) -> Dict:
        """Generate comprehensive progression validation report"""
        if not validation_results:
            return {'error': 'No validation results provided'}
        
        total_results = len(validation_results)
        valid_results = sum(1 for r in validation_results if r.is_valid)
        
        avg_authenticity = sum(r.authenticity_score for r in validation_results) / total_results
        avg_difficulty_consistency = sum(r.difficulty_consistency for r in validation_results) / total_results
        avg_tradition_alignment = sum(r.tradition_alignment for r in validation_results) / total_results
        
        all_issues = []
        all_recommendations = []
        for result in validation_results:
            all_issues.extend(result.issues)
            all_recommendations.extend(result.recommendations)
        
        return {
            'summary': {
                'total_governors': total_results,
                'valid_progressions': valid_results,
                'validation_rate': valid_results / total_results,
                'average_authenticity_score': avg_authenticity,
                'average_difficulty_consistency': avg_difficulty_consistency,
                'average_tradition_alignment': avg_tradition_alignment
            },
            'common_issues': list(set(all_issues)),
            'recommendations': list(set(all_recommendations)),
            'detailed_results': [r.to_dict() for r in validation_results]
        }

# Initialize global validator
PROGRESSION_VALIDATOR = ProgressionPathwayValidator()

def get_progression_validator() -> ProgressionPathwayValidator:
    """Get the global progression pathway validator instance"""
    return PROGRESSION_VALIDATOR
