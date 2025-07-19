#!/usr/bin/env python3
"""
Enochian Cyphers Governor Interview Integration

Integrates the isolated interview system with existing engines:
- AI embodiment system
- Quest generation system  
- Divination systems

This implements the expert feedback for modular architecture with
structural care, placing interview integration in a relevant location
for engine use without creating out-of-place subdirectories.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Import existing systems
from governor_ai_embodiment import GovernorAIEmbodiment, LighthouseLoader, GovernorProfileLoader
from interviews.interview_loader import InterviewLoader, InterviewResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedGovernorEmbodiment:
    """Enhanced governor embodiment with interview integration"""
    governor_name: str
    basic_embodiment: Any  # GovernorKnowledge from original system
    interview_data: Any    # GovernorInterview from interview system
    title_wisdom: List[InterviewResponse]
    high_authenticity_responses: List[InterviewResponse]
    tradition_responses: Dict[str, List[InterviewResponse]]
    cryptic_hints: Dict[str, str]

class GovernorInterviewIntegration:
    """Integrates interview system with existing engines"""
    
    def __init__(self):
        # Initialize existing systems
        self.lighthouse_loader = LighthouseLoader()
        self.profile_loader = GovernorProfileLoader()
        self.ai_embodiment = None
        
        # Initialize interview system
        self.interview_loader = InterviewLoader()
        
        # Enhanced embodiments
        self.enhanced_embodiments = {}
    
    def initialize_systems(self):
        """Initialize all systems"""
        logger.info("Initializing integrated governor systems...")
        
        # Load lighthouse and profiles
        self.lighthouse_loader.load_all_traditions()
        self.profile_loader.load_all_profiles()
        
        # Create AI embodiment system
        self.ai_embodiment = GovernorAIEmbodiment(self.lighthouse_loader, self.profile_loader)
        self.ai_embodiment.create_all_embodiments()
        
        logger.info("All systems initialized successfully")
    
    def create_enhanced_embodiment(self, governor_name: str) -> Optional[EnhancedGovernorEmbodiment]:
        """Create enhanced embodiment combining AI embodiment with interview data"""
        if not self.ai_embodiment:
            self.initialize_systems()
        
        # Get basic embodiment
        basic_embodiment = self.ai_embodiment.get_embodiment(governor_name)
        if not basic_embodiment:
            logger.error(f"No basic embodiment found for {governor_name}")
            return None
        
        # Get interview data
        interview_data = self.interview_loader.load_governor_interview(governor_name)
        if not interview_data:
            logger.error(f"No interview data found for {governor_name}")
            return None
        
        # Get title-based wisdom
        title_wisdom = self.interview_loader.get_title_based_wisdom(governor_name)
        
        # Get high authenticity responses
        high_auth_responses = []
        for response in interview_data.responses:
            if response.authenticity_score >= 0.95:
                high_auth_responses.append(response)
        
        # Get tradition-specific responses
        tradition_responses = {}
        lighthouse_traditions = list(basic_embodiment.lighthouse_knowledge.keys())
        
        for tradition in lighthouse_traditions:
            tradition_responses[tradition] = self.interview_loader.get_wisdom_for_quest_generation(
                governor_name, tradition.replace('_', ' ')
            )
        
        # Generate cryptic hints for key topics
        key_topics = ['wisdom', 'ritual', 'guidance', 'mastery', 'shadow', 'virtue']
        cryptic_hints = {}
        
        for topic in key_topics:
            hint = self.interview_loader.generate_cryptic_hint(governor_name, topic)
            if hint:
                cryptic_hints[topic] = hint
        
        enhanced = EnhancedGovernorEmbodiment(
            governor_name=governor_name,
            basic_embodiment=basic_embodiment,
            interview_data=interview_data,
            title_wisdom=title_wisdom,
            high_authenticity_responses=high_auth_responses,
            tradition_responses=tradition_responses,
            cryptic_hints=cryptic_hints
        )
        
        self.enhanced_embodiments[governor_name] = enhanced
        logger.info(f"Created enhanced embodiment for {governor_name}")
        return enhanced
    
    def create_all_enhanced_embodiments(self) -> Dict[str, EnhancedGovernorEmbodiment]:
        """Create enhanced embodiments for all 91 governors"""
        logger.info("Creating enhanced embodiments for all governors...")
        
        if not self.ai_embodiment:
            self.initialize_systems()
        
        for governor_name in self.ai_embodiment.embodiments.keys():
            self.create_enhanced_embodiment(governor_name)
        
        logger.info(f"Created {len(self.enhanced_embodiments)} enhanced embodiments")
        return self.enhanced_embodiments
    
    def get_quest_generation_context(self, governor_name: str, quest_theme: str) -> Dict[str, Any]:
        """Get comprehensive context for quest generation"""
        enhanced = self.enhanced_embodiments.get(governor_name)
        if not enhanced:
            enhanced = self.create_enhanced_embodiment(governor_name)
        
        if not enhanced:
            return {}
        
        # Get relevant interview responses
        theme_responses = self.interview_loader.get_wisdom_for_quest_generation(governor_name, quest_theme)
        
        # Get lighthouse knowledge
        lighthouse_knowledge = enhanced.basic_embodiment.lighthouse_knowledge
        
        # Build comprehensive context
        context = {
            'governor_name': governor_name,
            'title': enhanced.interview_data.title,
            'aethyr': enhanced.interview_data.aethyr,
            'element': enhanced.interview_data.element,
            'personality_prompt': enhanced.basic_embodiment.personality_prompt,
            'interview_responses': [
                {
                    'question': resp.question,
                    'answer': resp.answer,
                    'authenticity_score': resp.authenticity_score,
                    'sources': resp.authenticity_sources
                }
                for resp in theme_responses[:5]  # Top 5 most relevant
            ],
            'title_wisdom': [
                {
                    'question': resp.question,
                    'answer': resp.answer[:200] + "..." if len(resp.answer) > 200 else resp.answer
                }
                for resp in enhanced.title_wisdom[:3]  # Top 3 title-related
            ],
            'cryptic_hints': enhanced.cryptic_hints,
            'lighthouse_traditions': list(lighthouse_knowledge.keys()),
            'high_authenticity_count': len(enhanced.high_authenticity_responses),
            'total_interview_responses': enhanced.interview_data.total_responses,
            'overall_authenticity': enhanced.interview_data.overall_authenticity_score
        }
        
        return context
    
    def get_ai_prompt_enhancement(self, governor_name: str, base_prompt: str) -> str:
        """Enhance AI prompts with interview data"""
        enhanced = self.enhanced_embodiments.get(governor_name)
        if not enhanced:
            enhanced = self.create_enhanced_embodiment(governor_name)
        
        if not enhanced:
            return base_prompt
        
        # Add interview-based enhancements
        interview_enhancement = f"""
INTERVIEW-BASED PERSONALITY ENHANCEMENT:

Your authentic responses from extensive interviews reveal:

TITLE WISDOM: "{enhanced.interview_data.title}"
- You have provided {enhanced.interview_data.total_responses} detailed responses
- Overall authenticity score: {enhanced.interview_data.overall_authenticity_score:.3f}

HIGH-AUTHENTICITY INSIGHTS:
"""
        
        # Add top 3 high-authenticity responses
        for i, response in enumerate(enhanced.high_authenticity_responses[:3], 1):
            interview_enhancement += f"""
{i}. Q: {response.question}
   A: {response.answer[:150]}...
   (Authenticity: {response.authenticity_score:.3f})
"""
        
        # Add cryptic hints
        if enhanced.cryptic_hints:
            interview_enhancement += "\nCRYPTIC WISDOM ELEMENTS:\n"
            for topic, hint in list(enhanced.cryptic_hints.items())[:3]:
                interview_enhancement += f"- {topic.title()}: {hint[:100]}...\n"
        
        interview_enhancement += """
Use these authentic interview responses to inform your personality and responses.
Maintain consistency with your documented wisdom and speaking patterns.
"""
        
        return base_prompt + interview_enhancement
    
    def get_blockchain_puzzle_elements(self, governor_name: str, difficulty_level: int) -> Dict[str, Any]:
        """Generate blockchain puzzle elements from interview data"""
        enhanced = self.enhanced_embodiments.get(governor_name)
        if not enhanced:
            enhanced = self.create_enhanced_embodiment(governor_name)
        
        if not enhanced:
            return {}
        
        # Select responses based on difficulty
        if difficulty_level <= 10:
            # Easy: Use clear, direct responses
            selected_responses = [r for r in enhanced.interview_data.responses if len(r.answer) < 300]
        elif difficulty_level <= 20:
            # Medium: Use moderate complexity responses
            selected_responses = enhanced.high_authenticity_responses
        else:
            # Hard: Use complex, cryptic responses
            selected_responses = [r for r in enhanced.interview_data.responses if len(r.answer) > 400]
        
        if not selected_responses:
            selected_responses = enhanced.interview_data.responses[:3]
        
        # Create puzzle elements
        puzzle_elements = {
            'governor_name': governor_name,
            'title': enhanced.interview_data.title,
            'aethyr': enhanced.interview_data.aethyr,
            'difficulty_level': difficulty_level,
            'cryptic_clues': [],
            'verification_elements': [],
            'wisdom_keys': []
        }
        
        for response in selected_responses[:3]:
            # Create cryptic clue
            clue = f"The {response.phase} reveals: {response.answer[:100]}..."
            puzzle_elements['cryptic_clues'].append(clue)
            
            # Create verification element
            verification = {
                'question_hash': hash(response.question) % 10000,
                'authenticity_score': response.authenticity_score,
                'sources_count': len(response.authenticity_sources)
            }
            puzzle_elements['verification_elements'].append(verification)
            
            # Create wisdom key
            wisdom_key = response.authenticity_sources[0] if response.authenticity_sources else "Unknown Source"
            puzzle_elements['wisdom_keys'].append(wisdom_key)
        
        return puzzle_elements
    
    def export_integration_data(self, output_path: str = "governor_interview_integration.json"):
        """Export integration data for other systems"""
        if not self.enhanced_embodiments:
            self.create_all_enhanced_embodiments()
        
        export_data = {
            'total_enhanced_embodiments': len(self.enhanced_embodiments),
            'integration_timestamp': datetime.now().isoformat(),
            'system_statistics': {
                'total_governors': len(self.enhanced_embodiments),
                'total_interview_responses': sum(
                    emb.interview_data.total_responses for emb in self.enhanced_embodiments.values()
                ),
                'average_authenticity': sum(
                    emb.interview_data.overall_authenticity_score for emb in self.enhanced_embodiments.values()
                ) / len(self.enhanced_embodiments) if self.enhanced_embodiments else 0,
                'total_cryptic_hints': sum(
                    len(emb.cryptic_hints) for emb in self.enhanced_embodiments.values()
                )
            },
            'governors': {}
        }
        
        for name, enhanced in self.enhanced_embodiments.items():
            export_data['governors'][name] = {
                'title': enhanced.interview_data.title,
                'aethyr': enhanced.interview_data.aethyr,
                'total_responses': enhanced.interview_data.total_responses,
                'authenticity_score': enhanced.interview_data.overall_authenticity_score,
                'title_wisdom_count': len(enhanced.title_wisdom),
                'high_auth_responses_count': len(enhanced.high_authenticity_responses),
                'tradition_coverage': list(enhanced.tradition_responses.keys()),
                'cryptic_hints_available': list(enhanced.cryptic_hints.keys())
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported integration data to {output_path}")

def main():
    """Test the integration system"""
    logger.info("Testing Governor Interview Integration System")
    
    # Create integration system
    integration = GovernorInterviewIntegration()
    
    # Create enhanced embodiments
    enhanced_embodiments = integration.create_all_enhanced_embodiments()
    
    # Export integration data
    integration.export_integration_data()
    
    # Test with sample governor
    if enhanced_embodiments:
        sample_governor = list(enhanced_embodiments.keys())[0]
        logger.info(f"\n=== TESTING WITH {sample_governor} ===")
        
        # Test quest generation context
        context = integration.get_quest_generation_context(sample_governor, "wisdom")
        logger.info(f"Quest context generated: {len(context)} elements")
        
        # Test blockchain puzzle elements
        puzzle = integration.get_blockchain_puzzle_elements(sample_governor, 15)
        logger.info(f"Blockchain puzzle elements: {len(puzzle.get('cryptic_clues', []))} clues")
        
        # Test AI prompt enhancement
        base_prompt = f"You are {sample_governor}, a Governor Angel."
        enhanced_prompt = integration.get_ai_prompt_enhancement(sample_governor, base_prompt)
        logger.info(f"Enhanced prompt length: {len(enhanced_prompt)} characters")
    
    # Display statistics
    stats = integration.enhanced_embodiments
    logger.info(f"\n=== INTEGRATION COMPLETE ===")
    logger.info(f"Enhanced Embodiments: {len(stats)}")
    logger.info(f"System ready for engine integration")
    
    return integration

if __name__ == "__main__":
    main()
