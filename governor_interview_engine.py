#!/usr/bin/env python3
"""
Enochian Cyphers Governor Interview Engine

Provides structured access to the extensive interview data from all 91 Governor Angels.
Integrates seamlessly with existing engines (AI embodiment, quest generation, divination)
to provide rich, authentic responses based on actual governor interview content.

This addresses expert feedback by making the governor interview Q&A data accessible
to our engines in a structured, searchable format.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class InterviewResponse:
    """Single interview response from a governor"""
    question_number: int
    question: str
    answer: str
    reasoning: str
    authenticity_sources: List[str]
    phase: str
    governor_name: str

@dataclass
class InterviewPhase:
    """Complete interview phase with all responses"""
    phase_name: str
    governor_name: str
    responses: List[InterviewResponse]
    phase_summary: str
    authenticity_score: float
    parsing_success: bool

@dataclass
class GovernorInterview:
    """Complete interview data for a governor"""
    governor_name: str
    phases: Dict[str, InterviewPhase]
    total_phases: int
    completed_phases: int
    overall_authenticity_score: float
    successful_phases: int
    parsing_success_rate: float

class GovernorInterviewEngine:
    """Engine for accessing and querying governor interview data"""
    
    def __init__(self, profiles_path: str = "governor_profiles"):
        self.profiles_path = Path(profiles_path)
        self.interviews = {}
        self.response_index = {}  # For fast searching
        self.topic_index = {}     # For topic-based queries
        self.question_index = {}  # For question-based queries
        
    def load_all_interviews(self) -> Dict[str, GovernorInterview]:
        """Load interview data from all 91 governor profiles"""
        logger.info("Loading governor interview data...")
        
        profile_files = list(self.profiles_path.glob("*_complete_interview.json"))
        
        if len(profile_files) != 91:
            logger.warning(f"Expected 91 governor profiles, found {len(profile_files)}")
        
        for profile_file in profile_files:
            try:
                governor_name = profile_file.stem.replace("_complete_interview", "")
                interview = self._load_single_interview(profile_file, governor_name)
                if interview:
                    self.interviews[governor_name] = interview
                    self._index_interview(interview)
                    
            except Exception as e:
                logger.error(f"Error loading interview from {profile_file}: {e}")
        
        logger.info(f"Loaded interviews for {len(self.interviews)} governors")
        return self.interviews
    
    def _load_single_interview(self, profile_file: Path, governor_name: str) -> Optional[GovernorInterview]:
        """Load interview data from a single governor profile"""
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Extract interview data from the full_profile section
            full_profile = profile_data.get('governor_profile', {}).get('full_profile', {})
            
            if not full_profile:
                logger.warning(f"No full_profile found for {governor_name}")
                return None
            
            phases = {}
            
            # Process each phase in the interview
            for key, value in full_profile.items():
                if key.startswith('phase_') and isinstance(value, dict):
                    phase = self._parse_interview_phase(value, governor_name)
                    if phase:
                        phases[key] = phase
            
            # Extract summary data
            summary = full_profile.get('summary', {})
            
            interview = GovernorInterview(
                governor_name=governor_name,
                phases=phases,
                total_phases=summary.get('total_phases', len(phases)),
                completed_phases=summary.get('completed_phases', len(phases)),
                overall_authenticity_score=summary.get('overall_authenticity_score', 0.0),
                successful_phases=summary.get('successful_phases', len(phases)),
                parsing_success_rate=summary.get('parsing_success_rate', 100.0)
            )
            
            return interview
            
        except Exception as e:
            logger.error(f"Error parsing interview for {governor_name}: {e}")
            return None
    
    def _parse_interview_phase(self, phase_data: Dict[str, Any], governor_name: str) -> Optional[InterviewPhase]:
        """Parse a single interview phase"""
        try:
            phase_name = phase_data.get('phase', 'unknown')
            responses = []
            
            # Parse individual responses
            for response_data in phase_data.get('responses', []):
                response = InterviewResponse(
                    question_number=response_data.get('question_number', 0),
                    question=response_data.get('question', ''),
                    answer=response_data.get('answer', ''),
                    reasoning=response_data.get('reasoning', ''),
                    authenticity_sources=response_data.get('authenticity_sources', []),
                    phase=phase_name,
                    governor_name=governor_name
                )
                responses.append(response)
            
            phase = InterviewPhase(
                phase_name=phase_name,
                governor_name=governor_name,
                responses=responses,
                phase_summary=phase_data.get('phase_summary', ''),
                authenticity_score=phase_data.get('authenticity_score', 0.0),
                parsing_success=phase_data.get('parsing_success', True)
            )
            
            return phase
            
        except Exception as e:
            logger.error(f"Error parsing phase for {governor_name}: {e}")
            return None
    
    def _index_interview(self, interview: GovernorInterview):
        """Create searchable indexes for the interview"""
        governor_name = interview.governor_name
        
        # Index all responses for fast searching
        for phase in interview.phases.values():
            for response in phase.responses:
                # Response index by governor
                if governor_name not in self.response_index:
                    self.response_index[governor_name] = []
                self.response_index[governor_name].append(response)
                
                # Topic index (extract keywords from questions and answers)
                keywords = self._extract_keywords(response.question + " " + response.answer)
                for keyword in keywords:
                    if keyword not in self.topic_index:
                        self.topic_index[keyword] = []
                    self.topic_index[keyword].append(response)
                
                # Question index
                question_key = response.question.lower().strip()
                if question_key not in self.question_index:
                    self.question_index[question_key] = []
                self.question_index[question_key].append(response)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        # Extract words, convert to lowercase, filter out common words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in common_words]
        
        # Return unique keywords
        return list(set(keywords))
    
    def get_governor_interview(self, governor_name: str) -> Optional[GovernorInterview]:
        """Get complete interview for a specific governor"""
        return self.interviews.get(governor_name)
    
    def search_responses_by_topic(self, topic: str, limit: int = 10) -> List[InterviewResponse]:
        """Search for responses related to a specific topic"""
        topic_lower = topic.lower()
        matching_responses = []
        
        # Direct keyword match
        if topic_lower in self.topic_index:
            matching_responses.extend(self.topic_index[topic_lower])
        
        # Fuzzy matching in questions and answers
        for governor_name, responses in self.response_index.items():
            for response in responses:
                if (topic_lower in response.question.lower() or 
                    topic_lower in response.answer.lower()):
                    if response not in matching_responses:
                        matching_responses.append(response)
        
        return matching_responses[:limit]
    
    def search_responses_by_question(self, question_pattern: str, limit: int = 10) -> List[InterviewResponse]:
        """Search for responses to similar questions"""
        pattern_lower = question_pattern.lower()
        matching_responses = []
        
        for question, responses in self.question_index.items():
            if pattern_lower in question:
                matching_responses.extend(responses)
        
        return matching_responses[:limit]
    
    def get_governor_wisdom_on_topic(self, governor_name: str, topic: str) -> List[InterviewResponse]:
        """Get a specific governor's wisdom on a particular topic"""
        governor_responses = self.response_index.get(governor_name, [])
        topic_lower = topic.lower()
        
        matching_responses = []
        for response in governor_responses:
            if (topic_lower in response.question.lower() or 
                topic_lower in response.answer.lower()):
                matching_responses.append(response)
        
        return matching_responses
    
    def get_all_governors_on_topic(self, topic: str) -> Dict[str, List[InterviewResponse]]:
        """Get all governors' perspectives on a specific topic"""
        results = {}
        
        for governor_name in self.interviews.keys():
            governor_responses = self.get_governor_wisdom_on_topic(governor_name, topic)
            if governor_responses:
                results[governor_name] = governor_responses
        
        return results
    
    def get_phase_responses(self, governor_name: str, phase_name: str) -> List[InterviewResponse]:
        """Get all responses from a specific interview phase"""
        interview = self.interviews.get(governor_name)
        if not interview:
            return []
        
        phase = interview.phases.get(phase_name)
        if not phase:
            return []
        
        return phase.responses
    
    def get_high_authenticity_responses(self, min_score: float = 0.9) -> List[InterviewResponse]:
        """Get responses with high authenticity scores"""
        high_auth_responses = []
        
        for interview in self.interviews.values():
            for phase in interview.phases.values():
                if phase.authenticity_score >= min_score:
                    high_auth_responses.extend(phase.responses)
        
        return high_auth_responses
    
    def export_interview_index(self, output_path: str = "governor_interview_index.json"):
        """Export searchable interview index"""
        index_data = {
            'total_governors': len(self.interviews),
            'total_responses': sum(len(responses) for responses in self.response_index.values()),
            'total_topics': len(self.topic_index),
            'governors': list(self.interviews.keys()),
            'available_topics': list(self.topic_index.keys())[:100],  # Top 100 topics
            'generation_timestamp': datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported interview index to {output_path}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the interview data"""
        total_responses = sum(len(responses) for responses in self.response_index.values())
        total_phases = sum(len(interview.phases) for interview in self.interviews.values())
        
        avg_authenticity = sum(interview.overall_authenticity_score for interview in self.interviews.values()) / len(self.interviews) if self.interviews else 0
        
        return {
            'total_governors': len(self.interviews),
            'total_phases': total_phases,
            'total_responses': total_responses,
            'total_indexed_topics': len(self.topic_index),
            'average_authenticity_score': avg_authenticity,
            'average_responses_per_governor': total_responses / len(self.interviews) if self.interviews else 0
        }

def main():
    """Main function to initialize and test the interview engine"""
    logger.info("Initializing Governor Interview Engine")
    
    # Create interview engine
    interview_engine = GovernorInterviewEngine()
    
    # Load all interviews
    interviews = interview_engine.load_all_interviews()
    
    # Export index
    interview_engine.export_interview_index()
    
    # Display statistics
    stats = interview_engine.get_statistics()
    logger.info(f"\n=== GOVERNOR INTERVIEW ENGINE READY ===")
    logger.info(f"Total Governors: {stats['total_governors']}")
    logger.info(f"Total Interview Phases: {stats['total_phases']}")
    logger.info(f"Total Responses: {stats['total_responses']}")
    logger.info(f"Total Indexed Topics: {stats['total_indexed_topics']}")
    logger.info(f"Average Authenticity Score: {stats['average_authenticity_score']:.3f}")
    logger.info(f"Average Responses per Governor: {stats['average_responses_per_governor']:.1f}")
    
    # Test search functionality
    logger.info("\n=== TESTING SEARCH FUNCTIONALITY ===")
    
    # Test topic search
    magic_responses = interview_engine.search_responses_by_topic("magic", limit=3)
    logger.info(f"Found {len(magic_responses)} responses about 'magic'")
    
    # Test governor-specific wisdom
    if interviews:
        sample_governor = list(interviews.keys())[0]
        wisdom_responses = interview_engine.get_governor_wisdom_on_topic(sample_governor, "wisdom")
        logger.info(f"{sample_governor} has {len(wisdom_responses)} responses about 'wisdom'")
    
    return interview_engine

if __name__ == "__main__":
    main()
