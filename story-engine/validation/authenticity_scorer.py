#!/usr/bin/env python3
"""
Enochian Cyphers Story Engine - Authenticity Scorer
Enhanced authenticity validation system with tradition-specific scoring
"""

import json
import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AuthenticityScore:
    overall_score: float
    tradition_alignment: float
    historical_accuracy: float
    spiritual_depth: float
    practical_applicability: float
    source_quality: float
    detailed_breakdown: Dict[str, float]
    validation_notes: List[str]
    improvement_suggestions: List[str]

class EnhancedAuthenticityScorer:
    """Enhanced authenticity scoring with tradition-specific validation"""
    
    def __init__(self):
        self.tradition_validators = self._initialize_tradition_validators()
        self.enochian_keywords = self._initialize_enochian_keywords()
        self.historical_markers = self._initialize_historical_markers()
        self.spiritual_depth_indicators = self._initialize_spiritual_indicators()
        self.source_quality_markers = self._initialize_source_markers()
        
    def _initialize_tradition_validators(self) -> Dict[str, Dict]:
        """Initialize tradition-specific validation criteria"""
        return {
            "Enochian": {
                "primary_sources": [
                    "John Dee Spiritual Diaries",
                    "Edward Kelley Communications",
                    "Enochian Tablets",
                    "Watchtower Manuscripts"
                ],
                "key_concepts": [
                    "angelic communication", "aethyr", "watchtower", "governor",
                    "enochian language", "scrying", "spiritual diary", "celestial hierarchy"
                ],
                "historical_figures": ["john dee", "edward kelley", "elizabeth i"],
                "authenticity_weight": 1.0,
                "minimum_threshold": 0.85
            },
            "Hermetic_Qabalah": {
                "primary_sources": [
                    "Sefer Yetzirah",
                    "Zohar",
                    "Golden Dawn Manuscripts",
                    "Tree of Life Studies"
                ],
                "key_concepts": [
                    "sephiroth", "tree of life", "pathworking", "emanation",
                    "divine names", "qabalah", "hermetic", "mystical union"
                ],
                "historical_figures": ["moses de leon", "isaac luria", "mathers"],
                "authenticity_weight": 0.8,
                "minimum_threshold": 0.80
            },
            "Thelema": {
                "primary_sources": [
                    "Book of the Law",
                    "Crowley Works",
                    "Thelemic Texts",
                    "Magick in Theory and Practice"
                ],
                "key_concepts": [
                    "true will", "thelema", "aeon", "magick",
                    "do what thou wilt", "love is the law", "babalon", "chaos"
                ],
                "historical_figures": ["aleister crowley", "rose kelly", "aiwass"],
                "authenticity_weight": 0.7,
                "minimum_threshold": 0.75
            },
            "Golden_Dawn": {
                "primary_sources": [
                    "Golden Dawn Manuscripts",
                    "Ritual Texts",
                    "Cipher Manuscripts",
                    "Order Documents"
                ],
                "key_concepts": [
                    "golden dawn", "ritual magic", "ceremonial", "initiation",
                    "grade system", "elemental", "pentagram", "hexagram"
                ],
                "historical_figures": ["mathers", "westcott", "woodman", "yeats"],
                "authenticity_weight": 0.75,
                "minimum_threshold": 0.78
            }
        }
    
    def _initialize_enochian_keywords(self) -> Dict[str, float]:
        """Initialize Enochian-specific keywords with weights"""
        return {
            # Core Enochian terms (highest weight)
            "enochian": 3.0,
            "aethyr": 2.8,
            "governor": 2.5,
            "watchtower": 2.5,
            "angel": 2.0,
            "angelic": 2.0,
            
            # Historical figures (high weight)
            "john dee": 2.8,
            "edward kelley": 2.8,
            "dee": 2.5,
            "kelley": 2.5,
            
            # Enochian concepts (medium-high weight)
            "scrying": 2.2,
            "spiritual diary": 2.2,
            "tablet": 2.0,
            "celestial": 1.8,
            "divine": 1.8,
            "sacred": 1.5,
            
            # Practice-related terms (medium weight)
            "invocation": 1.8,
            "communion": 1.6,
            "vision": 1.5,
            "mystical": 1.4,
            "spiritual": 1.3,
            "wisdom": 1.2,
            
            # Supporting terms (lower weight)
            "enlightenment": 1.1,
            "transcendence": 1.1,
            "transformation": 1.0,
            "practice": 0.8,
            "meditation": 0.8
        }
    
    def _initialize_historical_markers(self) -> Dict[str, float]:
        """Initialize historical accuracy markers"""
        return {
            # Specific dates and periods
            "1582": 2.5,
            "1583": 2.5,
            "1584": 2.5,
            "16th century": 2.0,
            "elizabethan": 2.0,
            "renaissance": 1.8,
            
            # Historical context
            "mortlake": 2.2,
            "prague": 2.0,
            "rudolph ii": 2.0,
            "elizabeth i": 1.8,
            "court astrologer": 1.8,
            
            # Authentic practices
            "crystal ball": 1.5,
            "showstone": 2.0,
            "obsidian mirror": 1.8,
            "angelic conversations": 2.2
        }
    
    def _initialize_spiritual_indicators(self) -> List[str]:
        """Initialize spiritual depth indicators"""
        return [
            "spiritual development",
            "inner transformation",
            "divine communion",
            "mystical union",
            "sacred wisdom",
            "enlightenment",
            "transcendence",
            "spiritual practice",
            "authentic tradition",
            "higher consciousness",
            "divine guidance",
            "spiritual growth"
        ]
    
    def _initialize_source_markers(self) -> Dict[str, float]:
        """Initialize source quality markers"""
        return {
            "primary source": 2.5,
            "original manuscript": 2.3,
            "historical document": 2.0,
            "scholarly research": 1.8,
            "academic study": 1.8,
            "peer reviewed": 1.5,
            "authentic tradition": 1.8,
            "traditional practice": 1.5,
            "verified historical": 2.0
        }
    
    def calculate_comprehensive_authenticity(
        self, 
        content: str, 
        tradition: str = "Enochian",
        sources: List[str] = None,
        context: Dict = None
    ) -> AuthenticityScore:
        """Calculate comprehensive authenticity score"""
        
        if sources is None:
            sources = []
        if context is None:
            context = {}
            
        # Initialize scoring components
        tradition_score = self._score_tradition_alignment(content, tradition)
        historical_score = self._score_historical_accuracy(content, tradition)
        spiritual_score = self._score_spiritual_depth(content)
        practical_score = self._score_practical_applicability(content)
        source_score = self._score_source_quality(sources, tradition)
        
        # Calculate weighted overall score
        weights = {
            "tradition_alignment": 0.30,
            "historical_accuracy": 0.25,
            "spiritual_depth": 0.20,
            "practical_applicability": 0.15,
            "source_quality": 0.10
        }
        
        overall_score = (
            tradition_score * weights["tradition_alignment"] +
            historical_score * weights["historical_accuracy"] +
            spiritual_score * weights["spiritual_depth"] +
            practical_score * weights["practical_applicability"] +
            source_score * weights["source_quality"]
        )
        
        # Apply tradition-specific weighting
        tradition_data = self.tradition_validators.get(tradition, {})
        tradition_weight = tradition_data.get("authenticity_weight", 1.0)
        overall_score *= tradition_weight
        
        # Generate detailed breakdown
        detailed_breakdown = {
            "tradition_alignment": tradition_score,
            "historical_accuracy": historical_score,
            "spiritual_depth": spiritual_score,
            "practical_applicability": practical_score,
            "source_quality": source_score,
            "tradition_weight_applied": tradition_weight,
            "weighted_components": {
                "tradition": tradition_score * weights["tradition_alignment"],
                "historical": historical_score * weights["historical_accuracy"],
                "spiritual": spiritual_score * weights["spiritual_depth"],
                "practical": practical_score * weights["practical_applicability"],
                "sources": source_score * weights["source_quality"]
            }
        }
        
        # Generate validation notes and suggestions
        validation_notes = self._generate_validation_notes(
            content, tradition, tradition_score, historical_score, 
            spiritual_score, practical_score, source_score
        )
        
        improvement_suggestions = self._generate_improvement_suggestions(
            tradition_score, historical_score, spiritual_score, 
            practical_score, source_score, tradition
        )
        
        return AuthenticityScore(
            overall_score=min(1.0, overall_score),
            tradition_alignment=tradition_score,
            historical_accuracy=historical_score,
            spiritual_depth=spiritual_score,
            practical_applicability=practical_score,
            source_quality=source_score,
            detailed_breakdown=detailed_breakdown,
            validation_notes=validation_notes,
            improvement_suggestions=improvement_suggestions
        )
    
    def _score_tradition_alignment(self, content: str, tradition: str) -> float:
        """Score alignment with specific tradition"""
        tradition_data = self.tradition_validators.get(tradition, {})
        if not tradition_data:
            return 0.5  # Neutral score for unknown traditions
        
        content_lower = content.lower()
        word_count = max(len(content_lower.split()), 1)
        
        # Score key concepts
        concept_score = 0.0
        key_concepts = tradition_data.get("key_concepts", [])
        for concept in key_concepts:
            if concept in content_lower:
                concept_score += 1.0 / len(key_concepts)
        
        # Score historical figures
        figure_score = 0.0
        historical_figures = tradition_data.get("historical_figures", [])
        for figure in historical_figures:
            if figure in content_lower:
                figure_score += 1.0 / len(historical_figures)
        
        # Combine scores
        base_score = 0.6  # Base alignment score
        concept_bonus = concept_score * 0.3
        figure_bonus = figure_score * 0.1
        
        return min(1.0, base_score + concept_bonus + figure_bonus)
    
    def _score_historical_accuracy(self, content: str, tradition: str) -> float:
        """Score historical accuracy"""
        content_lower = content.lower()
        score = 0.7  # Base historical score
        
        # Check for historical markers
        for marker, weight in self.historical_markers.items():
            if marker in content_lower:
                score += weight * 0.02  # Small bonus per marker
        
        # Check for anachronisms (simplified)
        anachronisms = ["internet", "computer", "modern", "21st century", "smartphone"]
        for anachronism in anachronisms:
            if anachronism in content_lower:
                score -= 0.1  # Penalty for anachronisms
        
        return max(0.0, min(1.0, score))
    
    def _score_spiritual_depth(self, content: str) -> float:
        """Score spiritual depth and meaningfulness"""
        content_lower = content.lower()
        score = 0.6  # Base spiritual score
        
        # Check for spiritual depth indicators
        depth_count = 0
        for indicator in self.spiritual_depth_indicators:
            if indicator in content_lower:
                depth_count += 1
        
        # Calculate depth bonus
        if depth_count > 0:
            depth_bonus = min(0.3, depth_count * 0.05)
            score += depth_bonus
        
        # Check for superficial or materialistic content
        materialistic_terms = ["money", "wealth", "power over others", "control", "manipulation"]
        for term in materialistic_terms:
            if term in content_lower:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _score_practical_applicability(self, content: str) -> float:
        """Score practical applicability and safety"""
        content_lower = content.lower()
        score = 0.7  # Base practical score
        
        # Check for practical guidance
        practical_terms = ["practice", "method", "technique", "exercise", "meditation", "study"]
        practical_count = sum(1 for term in practical_terms if term in content_lower)
        
        if practical_count > 0:
            score += min(0.2, practical_count * 0.04)
        
        # Check for safety considerations
        safety_terms = ["safe", "ethical", "responsible", "balanced", "grounded"]
        safety_count = sum(1 for term in safety_terms if term in content_lower)
        
        if safety_count > 0:
            score += min(0.1, safety_count * 0.02)
        
        # Penalty for dangerous or unethical content
        dangerous_terms = ["harmful", "dangerous", "unethical", "manipulative", "coercive"]
        for term in dangerous_terms:
            if term in content_lower:
                score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _score_source_quality(self, sources: List[str], tradition: str) -> float:
        """Score quality of cited sources"""
        if not sources:
            return 0.5  # Neutral score for no sources
        
        tradition_data = self.tradition_validators.get(tradition, {})
        primary_sources = tradition_data.get("primary_sources", [])
        
        score = 0.0
        total_weight = 0.0
        
        for source in sources:
            source_lower = source.lower()
            source_score = 0.3  # Base source score
            
            # Check if it's a primary source
            for primary in primary_sources:
                if primary.lower() in source_lower:
                    source_score = 1.0
                    break
            
            # Check for source quality markers
            for marker, weight in self.source_quality_markers.items():
                if marker in source_lower:
                    source_score += weight * 0.1
            
            score += min(1.0, source_score)
            total_weight += 1.0
        
        return score / total_weight if total_weight > 0 else 0.5
    
    def _generate_validation_notes(
        self, content: str, tradition: str, tradition_score: float,
        historical_score: float, spiritual_score: float, 
        practical_score: float, source_score: float
    ) -> List[str]:
        """Generate validation notes"""
        notes = []
        
        if tradition_score >= 0.9:
            notes.append(f"Excellent alignment with {tradition} tradition")
        elif tradition_score >= 0.8:
            notes.append(f"Good alignment with {tradition} tradition")
        elif tradition_score < 0.7:
            notes.append(f"Weak alignment with {tradition} tradition - consider strengthening core concepts")
        
        if historical_score >= 0.9:
            notes.append("Strong historical accuracy")
        elif historical_score < 0.7:
            notes.append("Historical accuracy could be improved")
        
        if spiritual_score >= 0.9:
            notes.append("Excellent spiritual depth and meaning")
        elif spiritual_score < 0.7:
            notes.append("Consider deepening spiritual content")
        
        if practical_score >= 0.9:
            notes.append("Highly practical and applicable")
        elif practical_score < 0.7:
            notes.append("Could benefit from more practical guidance")
        
        if source_score >= 0.8:
            notes.append("Good source quality")
        elif source_score < 0.6:
            notes.append("Source quality could be improved")
        
        return notes
    
    def _generate_improvement_suggestions(
        self, tradition_score: float, historical_score: float,
        spiritual_score: float, practical_score: float, 
        source_score: float, tradition: str
    ) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if tradition_score < 0.8:
            tradition_data = self.tradition_validators.get(tradition, {})
            key_concepts = tradition_data.get("key_concepts", [])[:3]
            suggestions.append(f"Strengthen {tradition} alignment by incorporating: {', '.join(key_concepts)}")
        
        if historical_score < 0.8:
            suggestions.append("Improve historical accuracy with period-appropriate references")
        
        if spiritual_score < 0.8:
            suggestions.append("Deepen spiritual content with more meaningful insights")
        
        if practical_score < 0.8:
            suggestions.append("Add more practical guidance and safe methods")
        
        if source_score < 0.7:
            suggestions.append("Include references to primary sources and scholarly works")
        
        return suggestions

def main():
    """Test the authenticity scorer"""
    scorer = EnhancedAuthenticityScorer()
    
    test_content = """
    In the sacred realm of the Aethyr, Governor ABRIOND manifests divine wisdom through 
    authentic Enochian practices. Following the methods recorded in John Dee's spiritual 
    diaries from 1582-1584, the seeker approaches the angelic hierarchy with reverence 
    and proper preparation. Through scrying and invocation, the celestial beings share 
    their sacred knowledge for spiritual development and enlightenment.
    """
    
    test_sources = [
        "John Dee Spiritual Diaries",
        "Enochian Tablets",
        "Historical Manuscripts"
    ]
    
    result = scorer.calculate_comprehensive_authenticity(
        test_content, 
        tradition="Enochian",
        sources=test_sources
    )
    
    print(f"Overall Authenticity Score: {result.overall_score:.3f}")
    print(f"Tradition Alignment: {result.tradition_alignment:.3f}")
    print(f"Historical Accuracy: {result.historical_accuracy:.3f}")
    print(f"Spiritual Depth: {result.spiritual_depth:.3f}")
    print(f"Practical Applicability: {result.practical_applicability:.3f}")
    print(f"Source Quality: {result.source_quality:.3f}")
    
    print("\nValidation Notes:")
    for note in result.validation_notes:
        print(f"- {note}")
    
    print("\nImprovement Suggestions:")
    for suggestion in result.improvement_suggestions:
        print(f"- {suggestion}")

if __name__ == "__main__":
    main()
