"""
Enochian Cyphers Authenticity Scoring System
Comprehensive validation metrics for mystical content authenticity
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import re
from datetime import datetime
import hashlib

class SourceType(Enum):
    """Types of authenticity sources"""
    PRIMARY_HISTORICAL = "primary_historical"       # Original historical texts
    SCHOLARLY_ACADEMIC = "scholarly_academic"       # Peer-reviewed academic sources
    TRADITIONAL_PRACTICE = "traditional_practice"   # Established traditional practices
    CROSS_REFERENCED = "cross_referenced"           # Multiple source confirmation
    RECONSTRUCTED = "reconstructed"                 # Scholarly reconstruction
    MODERN_SYNTHESIS = "modern_synthesis"           # Contemporary integration

class ValidationLevel(Enum):
    """Levels of validation rigor"""
    STRICT = "strict"           # 95%+ authenticity required
    STANDARD = "standard"       # 85%+ authenticity required
    MODERATE = "moderate"       # 75%+ authenticity required
    LENIENT = "lenient"         # 65%+ authenticity required

@dataclass
class SourceReference:
    """Reference to an authenticity source"""
    title: str
    author: str
    publication_date: str
    source_type: SourceType
    url: Optional[str] = None
    isbn: Optional[str] = None
    page_reference: Optional[str] = None
    reliability_score: float = 1.0
    access_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'author': self.author,
            'publication_date': self.publication_date,
            'source_type': self.source_type.value,
            'url': self.url,
            'isbn': self.isbn,
            'page_reference': self.page_reference,
            'reliability_score': self.reliability_score,
            'access_date': self.access_date
        }

@dataclass
class AuthenticityScore:
    """Comprehensive authenticity score for content"""
    overall_score: float
    source_quality_score: float
    cross_reference_score: float
    historical_accuracy_score: float
    cultural_sensitivity_score: float
    primary_sources: List[SourceReference]
    validation_notes: List[str]
    uncertainty_flags: List[str]
    last_validated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'overall_score': self.overall_score,
            'source_quality_score': self.source_quality_score,
            'cross_reference_score': self.cross_reference_score,
            'historical_accuracy_score': self.historical_accuracy_score,
            'cultural_sensitivity_score': self.cultural_sensitivity_score,
            'primary_sources': [source.to_dict() for source in self.primary_sources],
            'validation_notes': self.validation_notes,
            'uncertainty_flags': self.uncertainty_flags,
            'last_validated': self.last_validated
        }

class AuthenticityScoringSystem:
    """Comprehensive system for scoring content authenticity"""
    
    def __init__(self):
        self.source_reliability_weights = self._initialize_source_weights()
        self.tradition_validators = self._initialize_tradition_validators()
        self.cross_reference_database = self._initialize_cross_reference_db()
        self.cultural_sensitivity_guidelines = self._initialize_cultural_guidelines()
    
    def _initialize_source_weights(self) -> Dict[SourceType, float]:
        """Initialize reliability weights for different source types"""
        return {
            SourceType.PRIMARY_HISTORICAL: 1.0,      # Highest weight
            SourceType.SCHOLARLY_ACADEMIC: 0.9,      # High academic credibility
            SourceType.CROSS_REFERENCED: 0.85,       # Multiple source confirmation
            SourceType.TRADITIONAL_PRACTICE: 0.8,    # Established practice
            SourceType.RECONSTRUCTED: 0.7,           # Scholarly reconstruction
            SourceType.MODERN_SYNTHESIS: 0.6         # Contemporary interpretation
        }
    
    def _initialize_tradition_validators(self) -> Dict[str, Dict]:
        """Initialize validation criteria for each tradition"""
        return {
            'enochian_magic': {
                'primary_sources': [
                    'John Dee\'s Five Books of Mystery',
                    'Liber Chanokh (Liber LXXXIV)',
                    'True & Faithful Relation'
                ],
                'key_concepts': [
                    'aethyr', 'governor', 'enochian_key', 'sigil', 'scrying',
                    'angelic_hierarchy', 'divine_will', 'spiritual_realm'
                ],
                'authenticity_markers': [
                    'proper_aethyr_names', 'correct_governor_attributes',
                    'authentic_enochian_language', 'historical_context'
                ],
                'common_errors': [
                    'modern_new_age_additions', 'fictional_elaborations',
                    'incorrect_aethyr_sequence', 'non_historical_attributes'
                ],
                'validation_weight': 1.0
            },
            'i_ching': {
                'primary_sources': [
                    'Wilhelm Translation of Book of Changes',
                    'Traditional Chinese commentaries',
                    'Ten Wings (Shi Yi)'
                ],
                'key_concepts': [
                    'hexagram', 'trigram', 'yin_yang', 'judgment', 'image',
                    'change', 'dao', 'wu_wei', 'natural_order'
                ],
                'authenticity_markers': [
                    'correct_hexagram_sequence', 'traditional_interpretations',
                    'chinese_philosophical_context', 'wilhelm_translation_accuracy'
                ],
                'common_errors': [
                    'western_psychological_interpretations', 'new_age_additions',
                    'incorrect_hexagram_meanings', 'cultural_misappropriation'
                ],
                'validation_weight': 1.0
            },
            'hermetic_qabalah': {
                'primary_sources': [
                    'Colin Low\'s Notes on Kabbalah',
                    'Golden Dawn materials',
                    'Traditional Hermetic texts'
                ],
                'key_concepts': [
                    'sephirah', 'tree_of_life', 'path', 'correspondence',
                    'emanation', 'divine_attributes', 'consciousness'
                ],
                'authenticity_markers': [
                    'correct_sephirah_attributes', 'traditional_correspondences',
                    'golden_dawn_accuracy', 'hermetic_principles'
                ],
                'common_errors': [
                    'confusion_with_jewish_kabbalah', 'modern_inventions',
                    'incorrect_correspondences', 'oversimplification'
                ],
                'validation_weight': 0.9  # Slightly lower due to reconstruction
            }
            # Additional traditions would be defined based on research
        }
    
    def _initialize_cross_reference_db(self) -> Dict[str, List[str]]:
        """Initialize cross-reference database for validation"""
        return {
            'enochian_aethyrs': [
                'LIL', 'ARN', 'ZOM', 'PAZ', 'LIT', 'MAZ', 'DEO', 'ZID', 'ZIP', 'ZAX',
                'ICH', 'LOE', 'ZIM', 'UTA', 'OXO', 'LEA', 'TAN', 'ZEN', 'POP', 'KHR',
                'ASP', 'LIN', 'TOR', 'NIA', 'VTI', 'DES', 'ZAA', 'BAG', 'RII', 'TEX'
            ],
            'i_ching_hexagrams': [f"hexagram_{i}" for i in range(1, 65)],
            'qabalah_sephiroth': [
                'Kether', 'Chokhmah', 'Binah', 'Chesed', 'Gevurah',
                'Tiphereth', 'Netzach', 'Hod', 'Yesod', 'Malkuth'
            ],
            'tarot_major_arcana': [
                'The Fool', 'The Magician', 'The High Priestess', 'The Empress',
                'The Emperor', 'The Hierophant', 'The Lovers', 'The Chariot',
                'Strength', 'The Hermit', 'Wheel of Fortune', 'Justice',
                'The Hanged Man', 'Death', 'Temperance', 'The Devil',
                'The Tower', 'The Star', 'The Moon', 'The Sun',
                'Judgement', 'The World'
            ]
        }
    
    def _initialize_cultural_guidelines(self) -> Dict[str, List[str]]:
        """Initialize cultural sensitivity guidelines"""
        return {
            'general': [
                'Respect traditional cultural contexts',
                'Avoid appropriation and misrepresentation',
                'Acknowledge source cultures appropriately',
                'Use authentic terminology and concepts'
            ],
            'eastern_traditions': [
                'Respect Chinese philosophical context for I Ching',
                'Acknowledge Japanese cultural context for Kuji-Kiri',
                'Use proper Sanskrit/Chinese terminology',
                'Avoid Western psychological overlays'
            ],
            'indigenous_traditions': [
                'Respect shamanic traditions as sacred practices',
                'Acknowledge specific cultural origins',
                'Avoid generic "shamanism" generalizations',
                'Use culturally appropriate terminology'
            ],
            'abrahamic_traditions': [
                'Distinguish between Jewish Kabbalah and Hermetic Qabalah',
                'Respect Islamic context for Sufism',
                'Use appropriate Hebrew/Arabic terminology',
                'Acknowledge religious significance'
            ]
        }
    
    def score_content_authenticity(self, content: Dict, tradition: str, 
                                  validation_level: ValidationLevel = ValidationLevel.STANDARD) -> AuthenticityScore:
        """Score content authenticity comprehensively"""
        
        # Initialize scoring components
        source_quality_score = 0.0
        cross_reference_score = 0.0
        historical_accuracy_score = 0.0
        cultural_sensitivity_score = 0.0
        
        validation_notes = []
        uncertainty_flags = []
        primary_sources = []
        
        # Extract content information
        title = content.get('title', '')
        full_content = content.get('full_content', '')
        authenticity_data = content.get('authenticity', {})
        tags = content.get('tags', [])
        
        # Score source quality
        source_quality_score, source_notes, sources = self._score_source_quality(
            authenticity_data, tradition
        )
        validation_notes.extend(source_notes)
        primary_sources.extend(sources)
        
        # Score cross-reference validation
        cross_reference_score, cross_ref_notes = self._score_cross_references(
            content, tradition
        )
        validation_notes.extend(cross_ref_notes)
        
        # Score historical accuracy
        historical_accuracy_score, historical_notes, historical_flags = self._score_historical_accuracy(
            content, tradition
        )
        validation_notes.extend(historical_notes)
        uncertainty_flags.extend(historical_flags)
        
        # Score cultural sensitivity
        cultural_sensitivity_score, cultural_notes = self._score_cultural_sensitivity(
            content, tradition
        )
        validation_notes.extend(cultural_notes)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            source_quality_score,
            cross_reference_score,
            historical_accuracy_score,
            cultural_sensitivity_score,
            tradition
        )
        
        # Apply validation level requirements
        if not self._meets_validation_level(overall_score, validation_level):
            uncertainty_flags.append(f"Does not meet {validation_level.value} validation requirements")
        
        return AuthenticityScore(
            overall_score=overall_score,
            source_quality_score=source_quality_score,
            cross_reference_score=cross_reference_score,
            historical_accuracy_score=historical_accuracy_score,
            cultural_sensitivity_score=cultural_sensitivity_score,
            primary_sources=primary_sources,
            validation_notes=validation_notes,
            uncertainty_flags=uncertainty_flags
        )
    
    def _score_source_quality(self, authenticity_data: Dict, tradition: str) -> Tuple[float, List[str], List[SourceReference]]:
        """Score the quality of sources used"""
        notes = []
        sources = []
        
        primary_source = authenticity_data.get('primary_source', '')
        source_url = authenticity_data.get('source_url', '')
        cross_references = authenticity_data.get('cross_references', [])
        
        if not primary_source:
            notes.append("No primary source specified")
            return 0.0, notes, sources
        
        # Check against known reliable sources for tradition
        tradition_data = self.tradition_validators.get(tradition, {})
        reliable_sources = tradition_data.get('primary_sources', [])
        
        source_score = 0.0
        
        # Score primary source
        for reliable_source in reliable_sources:
            if reliable_source.lower() in primary_source.lower():
                source_score = 0.9
                notes.append(f"Primary source matches reliable source: {reliable_source}")
                
                # Create source reference
                source_ref = SourceReference(
                    title=primary_source,
                    author="Historical/Traditional",
                    publication_date="Historical",
                    source_type=SourceType.PRIMARY_HISTORICAL,
                    url=source_url if source_url else None,
                    reliability_score=1.0
                )
                sources.append(source_ref)
                break
        
        if source_score == 0.0:
            # Check if it's a scholarly source
            if any(term in primary_source.lower() for term in ['university', 'academic', 'journal', 'encyclopedia']):
                source_score = 0.7
                notes.append("Source appears to be academic/scholarly")
                source_type = SourceType.SCHOLARLY_ACADEMIC
            else:
                source_score = 0.5
                notes.append("Source reliability unclear")
                source_type = SourceType.MODERN_SYNTHESIS
            
            source_ref = SourceReference(
                title=primary_source,
                author="Unknown",
                publication_date="Unknown",
                source_type=source_type,
                url=source_url if source_url else None,
                reliability_score=source_score
            )
            sources.append(source_ref)
        
        # Bonus for cross-references
        if cross_references:
            cross_ref_bonus = min(0.1, len(cross_references) * 0.02)
            source_score += cross_ref_bonus
            notes.append(f"Cross-reference bonus: {cross_ref_bonus:.2f}")
        
        return min(1.0, source_score), notes, sources
    
    def _score_cross_references(self, content: Dict, tradition: str) -> Tuple[float, List[str]]:
        """Score cross-reference validation"""
        notes = []
        
        # Check for authentic terminology
        full_content = content.get('full_content', '').lower()
        title = content.get('title', '').lower()
        tags = [tag.lower() for tag in content.get('tags', [])]
        
        all_text = f"{title} {full_content} {' '.join(tags)}"
        
        # Get cross-reference database for tradition
        tradition_refs = []
        for key, refs in self.cross_reference_database.items():
            if tradition.replace('_', '') in key or any(t in key for t in tradition.split('_')):
                tradition_refs.extend([ref.lower() for ref in refs])
        
        if not tradition_refs:
            notes.append("No cross-reference database available for tradition")
            return 0.5, notes
        
        # Count matches
        matches = 0
        total_refs = len(tradition_refs)
        
        for ref in tradition_refs:
            if ref.lower() in all_text:
                matches += 1
        
        if matches == 0:
            score = 0.0
            notes.append("No authentic terminology found in cross-reference check")
        else:
            score = min(1.0, matches / max(1, total_refs * 0.1))  # Need 10% match for full score
            notes.append(f"Cross-reference matches: {matches}/{total_refs} ({score:.2f})")
        
        return score, notes
    
    def _score_historical_accuracy(self, content: Dict, tradition: str) -> Tuple[float, List[str], List[str]]:
        """Score historical accuracy"""
        notes = []
        flags = []
        
        tradition_data = self.tradition_validators.get(tradition, {})
        common_errors = tradition_data.get('common_errors', [])
        authenticity_markers = tradition_data.get('authenticity_markers', [])
        
        full_content = content.get('full_content', '').lower()
        
        # Check for common errors
        error_count = 0
        for error in common_errors:
            if error.replace('_', ' ') in full_content:
                error_count += 1
                flags.append(f"Potential error detected: {error}")
        
        # Check for authenticity markers
        marker_count = 0
        for marker in authenticity_markers:
            if marker.replace('_', ' ') in full_content:
                marker_count += 1
        
        # Calculate score
        if error_count > 0:
            error_penalty = min(0.5, error_count * 0.1)
            notes.append(f"Error penalty: {error_penalty:.2f}")
        else:
            error_penalty = 0.0
        
        if marker_count > 0:
            marker_bonus = min(0.5, marker_count * 0.1)
            notes.append(f"Authenticity marker bonus: {marker_bonus:.2f}")
        else:
            marker_bonus = 0.0
        
        base_score = 0.7  # Neutral starting point
        final_score = max(0.0, min(1.0, base_score + marker_bonus - error_penalty))
        
        return final_score, notes, flags
    
    def _score_cultural_sensitivity(self, content: Dict, tradition: str) -> Tuple[float, List[str]]:
        """Score cultural sensitivity"""
        notes = []
        
        # Get relevant guidelines
        guidelines = self.cultural_sensitivity_guidelines.get('general', [])
        
        # Add tradition-specific guidelines
        if 'chinese' in tradition or 'i_ching' in tradition or 'taoism' in tradition:
            guidelines.extend(self.cultural_sensitivity_guidelines.get('eastern_traditions', []))
        elif 'shamanism' in tradition:
            guidelines.extend(self.cultural_sensitivity_guidelines.get('indigenous_traditions', []))
        elif 'kabbalah' in tradition or 'sufism' in tradition:
            guidelines.extend(self.cultural_sensitivity_guidelines.get('abrahamic_traditions', []))
        
        # Simple heuristic scoring (could be more sophisticated)
        full_content = content.get('full_content', '').lower()
        
        # Check for respectful language
        respectful_terms = ['traditional', 'authentic', 'historical', 'cultural', 'sacred']
        disrespectful_terms = ['primitive', 'superstitious', 'backwards', 'exotic']
        
        respectful_count = sum(1 for term in respectful_terms if term in full_content)
        disrespectful_count = sum(1 for term in disrespectful_terms if term in full_content)
        
        if disrespectful_count > 0:
            score = max(0.0, 0.8 - disrespectful_count * 0.2)
            notes.append(f"Potentially insensitive language detected")
        else:
            score = min(1.0, 0.8 + respectful_count * 0.05)
            notes.append("No obvious cultural sensitivity issues")
        
        return score, notes
    
    def _calculate_overall_score(self, source_quality: float, cross_reference: float,
                               historical_accuracy: float, cultural_sensitivity: float,
                               tradition: str) -> float:
        """Calculate weighted overall authenticity score"""
        
        tradition_data = self.tradition_validators.get(tradition, {})
        tradition_weight = tradition_data.get('validation_weight', 0.8)
        
        # Weighted average with tradition-specific adjustment
        weights = {
            'source_quality': 0.35,
            'cross_reference': 0.25,
            'historical_accuracy': 0.25,
            'cultural_sensitivity': 0.15
        }
        
        weighted_score = (
            source_quality * weights['source_quality'] +
            cross_reference * weights['cross_reference'] +
            historical_accuracy * weights['historical_accuracy'] +
            cultural_sensitivity * weights['cultural_sensitivity']
        )
        
        # Apply tradition weight
        final_score = weighted_score * tradition_weight
        
        return min(1.0, max(0.0, final_score))
    
    def _meets_validation_level(self, score: float, level: ValidationLevel) -> bool:
        """Check if score meets validation level requirements"""
        thresholds = {
            ValidationLevel.STRICT: 0.95,
            ValidationLevel.STANDARD: 0.85,
            ValidationLevel.MODERATE: 0.75,
            ValidationLevel.LENIENT: 0.65
        }
        
        return score >= thresholds.get(level, 0.85)
    
    def batch_score_content(self, content_list: List[Dict], tradition: str,
                           validation_level: ValidationLevel = ValidationLevel.STANDARD) -> Dict[str, AuthenticityScore]:
        """Score multiple content items in batch"""
        results = {}
        
        for content in content_list:
            content_id = content.get('id', f"unknown_{hash(str(content))}")
            try:
                score = self.score_content_authenticity(content, tradition, validation_level)
                results[content_id] = score
            except Exception as e:
                # Create error score
                results[content_id] = AuthenticityScore(
                    overall_score=0.0,
                    source_quality_score=0.0,
                    cross_reference_score=0.0,
                    historical_accuracy_score=0.0,
                    cultural_sensitivity_score=0.0,
                    primary_sources=[],
                    validation_notes=[f"Scoring error: {str(e)}"],
                    uncertainty_flags=["Scoring failed"]
                )
        
        return results
    
    def generate_authenticity_report(self, scores: Dict[str, AuthenticityScore]) -> Dict:
        """Generate comprehensive authenticity report"""
        if not scores:
            return {'error': 'No scores provided'}
        
        total_items = len(scores)
        valid_scores = [score for score in scores.values() if score.overall_score > 0]
        
        if not valid_scores:
            return {'error': 'No valid scores found'}
        
        avg_overall = sum(score.overall_score for score in valid_scores) / len(valid_scores)
        avg_source_quality = sum(score.source_quality_score for score in valid_scores) / len(valid_scores)
        avg_cross_reference = sum(score.cross_reference_score for score in valid_scores) / len(valid_scores)
        avg_historical = sum(score.historical_accuracy_score for score in valid_scores) / len(valid_scores)
        avg_cultural = sum(score.cultural_sensitivity_score for score in valid_scores) / len(valid_scores)
        
        high_quality_count = sum(1 for score in valid_scores if score.overall_score >= 0.9)
        medium_quality_count = sum(1 for score in valid_scores if 0.7 <= score.overall_score < 0.9)
        low_quality_count = sum(1 for score in valid_scores if score.overall_score < 0.7)
        
        all_flags = []
        all_notes = []
        for score in valid_scores:
            all_flags.extend(score.uncertainty_flags)
            all_notes.extend(score.validation_notes)
        
        return {
            'summary': {
                'total_items': total_items,
                'valid_items': len(valid_scores),
                'average_overall_score': avg_overall,
                'average_source_quality': avg_source_quality,
                'average_cross_reference': avg_cross_reference,
                'average_historical_accuracy': avg_historical,
                'average_cultural_sensitivity': avg_cultural
            },
            'quality_distribution': {
                'high_quality': high_quality_count,
                'medium_quality': medium_quality_count,
                'low_quality': low_quality_count
            },
            'common_issues': {
                'uncertainty_flags': list(set(all_flags)),
                'validation_notes': list(set(all_notes))
            },
            'timestamp': datetime.now().isoformat()
        }

class CrossReferenceValidator:
    """Validates cross-references between mystical entries and traditions"""

    def __init__(self, scoring_system: AuthenticityScoringSystem):
        self.scoring_system = scoring_system
        self.synergy_patterns = self._initialize_synergy_patterns()

    def _initialize_synergy_patterns(self) -> Dict[str, Dict]:
        """Initialize known synergy patterns between traditions"""
        return {
            'enochian_hermetic': {
                'strength': 0.8,
                'type': 'historical',
                'common_elements': ['angelic_hierarchy', 'divine_emanation', 'spiritual_ascension'],
                'validation_criteria': ['golden_dawn_connection', 'ceremonial_magic_overlap']
            },
            'i_ching_taoism': {
                'strength': 0.9,
                'type': 'cultural',
                'common_elements': ['yin_yang', 'natural_order', 'wu_wei', 'change_principles'],
                'validation_criteria': ['chinese_philosophical_context', 'traditional_integration']
            },
            'qabalah_tarot': {
                'strength': 0.85,
                'type': 'systematic',
                'common_elements': ['tree_of_life', 'sephiroth', 'path_correspondences'],
                'validation_criteria': ['golden_dawn_system', 'traditional_correspondences']
            },
            'egyptian_hermetic': {
                'strength': 0.75,
                'type': 'historical',
                'common_elements': ['hermes_thoth', 'divine_wisdom', 'magical_practices'],
                'validation_criteria': ['historical_connection', 'hermetic_tradition']
            }
        }

    def validate_cross_reference(self, entry_a: Dict, entry_b: Dict) -> Dict:
        """Validate a cross-reference between two entries"""
        tradition_a = entry_a.get('tradition', '')
        tradition_b = entry_b.get('tradition', '')

        # Check for known synergy patterns
        synergy_key = f"{tradition_a}_{tradition_b}"
        reverse_key = f"{tradition_b}_{tradition_a}"

        synergy_data = self.synergy_patterns.get(synergy_key) or self.synergy_patterns.get(reverse_key)

        if not synergy_data:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'reason': 'No known synergy pattern between traditions',
                'suggestions': ['Research historical connections', 'Verify conceptual overlap']
            }

        # Validate common elements
        content_a = entry_a.get('full_content', '').lower()
        content_b = entry_b.get('full_content', '').lower()
        tags_a = [tag.lower() for tag in entry_a.get('tags', [])]
        tags_b = [tag.lower() for tag in entry_b.get('tags', [])]

        all_text_a = f"{content_a} {' '.join(tags_a)}"
        all_text_b = f"{content_b} {' '.join(tags_b)}"

        common_elements = synergy_data.get('common_elements', [])
        shared_elements = []

        for element in common_elements:
            element_clean = element.replace('_', ' ')
            if element_clean in all_text_a and element_clean in all_text_b:
                shared_elements.append(element)

        if not shared_elements:
            return {
                'is_valid': False,
                'confidence': 0.2,
                'reason': 'No shared conceptual elements found',
                'suggestions': ['Add conceptual bridges', 'Clarify connections']
            }

        # Calculate confidence based on shared elements and synergy strength
        element_ratio = len(shared_elements) / len(common_elements)
        base_strength = synergy_data.get('strength', 0.5)
        confidence = base_strength * element_ratio

        return {
            'is_valid': confidence >= 0.5,
            'confidence': confidence,
            'shared_elements': shared_elements,
            'synergy_type': synergy_data.get('type', 'unknown'),
            'reason': f"Shared {len(shared_elements)} of {len(common_elements)} common elements",
            'suggestions': [] if confidence >= 0.7 else ['Strengthen conceptual connections']
        }

class UncertaintyFlaggingSystem:
    """System for flagging uncertain or questionable content"""

    def __init__(self):
        self.uncertainty_patterns = self._initialize_uncertainty_patterns()
        self.confidence_thresholds = self._initialize_confidence_thresholds()

    def _initialize_uncertainty_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate uncertainty"""
        return {
            'language_indicators': [
                'possibly', 'might be', 'could be', 'perhaps', 'allegedly',
                'supposedly', 'reportedly', 'some say', 'it is said',
                'according to legend', 'mythically', 'purportedly'
            ],
            'source_issues': [
                'unverified', 'disputed', 'controversial', 'debated',
                'uncertain origin', 'modern addition', 'reconstruction',
                'interpretation', 'adaptation', 'synthesis'
            ],
            'content_flags': [
                'new age', 'modern interpretation', 'contemporary view',
                'personal gnosis', 'channeled', 'revealed', 'intuitive',
                'psychic', 'clairvoyant', 'visionary'
            ]
        }

    def _initialize_confidence_thresholds(self) -> Dict[str, float]:
        """Initialize confidence thresholds for different content types"""
        return {
            'historical_fact': 0.9,
            'traditional_practice': 0.8,
            'scholarly_interpretation': 0.7,
            'modern_synthesis': 0.6,
            'personal_experience': 0.4
        }

    def flag_uncertainties(self, content: Dict) -> List[str]:
        """Flag potential uncertainties in content"""
        flags = []

        full_content = content.get('full_content', '').lower()
        title = content.get('title', '').lower()

        all_text = f"{title} {full_content}"

        # Check for uncertainty language
        for indicator in self.uncertainty_patterns['language_indicators']:
            if indicator in all_text:
                flags.append(f"Uncertainty language detected: '{indicator}'")

        # Check for source issues
        for issue in self.uncertainty_patterns['source_issues']:
            if issue in all_text:
                flags.append(f"Source reliability issue: '{issue}'")

        # Check for content flags
        for flag_term in self.uncertainty_patterns['content_flags']:
            if flag_term in all_text:
                flags.append(f"Content authenticity concern: '{flag_term}'")

        # Check authenticity score if available
        authenticity = content.get('authenticity', {})
        validation_score = authenticity.get('validation_score', 1.0)

        if validation_score < 0.7:
            flags.append(f"Low validation score: {validation_score:.2f}")

        return flags

# Initialize global systems
AUTHENTICITY_SCORING_SYSTEM = AuthenticityScoringSystem()
CROSS_REFERENCE_VALIDATOR = CrossReferenceValidator(AUTHENTICITY_SCORING_SYSTEM)
UNCERTAINTY_FLAGGING_SYSTEM = UncertaintyFlaggingSystem()

def get_authenticity_scoring_system() -> AuthenticityScoringSystem:
    """Get the global authenticity scoring system instance"""
    return AUTHENTICITY_SCORING_SYSTEM

def get_cross_reference_validator() -> CrossReferenceValidator:
    """Get the global cross-reference validator instance"""
    return CROSS_REFERENCE_VALIDATOR

def get_uncertainty_flagging_system() -> UncertaintyFlaggingSystem:
    """Get the global uncertainty flagging system instance"""
    return UNCERTAINTY_FLAGGING_SYSTEM
