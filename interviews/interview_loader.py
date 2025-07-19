#!/usr/bin/env python3
"""
Enochian Cyphers Interview Loader

Provides structured access to isolated governor interview data for engine integration.
Designed for use by AI embodiment, quest generation, and divination systems.

This implements the expert feedback recommendation for modular architecture,
enabling O(1) access to interview data with TAP Protocol optimization.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class InterviewResponse:
    """Single interview response"""
    question_id: int
    question: str
    answer: str
    reasoning: str
    authenticity_sources: List[str]
    phase: str
    authenticity_score: float

@dataclass
class GovernorInterview:
    """Complete governor interview data"""
    governor_id: str
    governor_name: str
    title: str
    aethyr: str
    element: str
    responses: List[InterviewResponse]
    total_responses: int
    overall_authenticity_score: float

class InterviewLoader:
    """Loader for governor interview data with engine integration"""
    
    def __init__(self, interviews_path: str = "interviews"):
        self.interviews_path = Path(interviews_path)
        self.governors_path = self.interviews_path / "governors"
        self.indexes_path = self.interviews_path / "indexes"
        
        # Load master questions
        self.master_questions = self._load_master_questions()
        
        # Load indexes
        self.topic_index = self._load_topic_index()
        self.tradition_index = self._load_tradition_index()
        
        # Cache for loaded interviews
        self.interview_cache = {}
    
    def _load_master_questions(self) -> Dict[int, Dict[str, Any]]:
        """Load master questions template"""
        questions_file = self.interviews_path / "questions.json"
        
        if not questions_file.exists():
            logger.warning(f"Master questions file not found: {questions_file}")
            return {}
        
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert to ID-indexed format
            questions = {}
            for q in data.get('standardized_questions', []):
                questions[q['id']] = q
            
            logger.info(f"Loaded {len(questions)} master questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error loading master questions: {e}")
            return {}
    
    def _load_topic_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load topic search index"""
        index_file = self.indexes_path / "topic_index.json"
        
        if not index_file.exists():
            logger.warning(f"Topic index not found: {index_file}")
            return {}
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading topic index: {e}")
            return {}
    
    def _load_tradition_index(self) -> Dict[str, List[str]]:
        """Load tradition mapping index"""
        index_file = self.indexes_path / "tradition_index.json"
        
        if not index_file.exists():
            logger.warning(f"Tradition index not found: {index_file}")
            return {}
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading tradition index: {e}")
            return {}
    
    def load_governor_interview(self, governor_id: str) -> Optional[GovernorInterview]:
        """Load interview data for a specific governor"""
        # Check cache first
        if governor_id in self.interview_cache:
            return self.interview_cache[governor_id]
        
        # Load from file
        interview_file = self.governors_path / f"{governor_id.lower()}.json"
        
        if not interview_file.exists():
            logger.warning(f"Interview file not found for {governor_id}: {interview_file}")
            return None
        
        try:
            with open(interview_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert responses to dataclass objects
            responses = []
            for resp_data in data.get('responses', []):
                response = InterviewResponse(
                    question_id=resp_data['question_id'],
                    question=resp_data['question'],
                    answer=resp_data['answer'],
                    reasoning=resp_data['reasoning'],
                    authenticity_sources=resp_data['authenticity_sources'],
                    phase=resp_data['phase'],
                    authenticity_score=resp_data['authenticity_score']
                )
                responses.append(response)
            
            interview = GovernorInterview(
                governor_id=data['governor_id'],
                governor_name=data['governor_name'],
                title=data['title'],
                aethyr=data['aethyr'],
                element=data['element'],
                responses=responses,
                total_responses=data['total_responses'],
                overall_authenticity_score=data['overall_authenticity_score']
            )
            
            # Cache for future use
            self.interview_cache[governor_id] = interview
            
            return interview
            
        except Exception as e:
            logger.error(f"Error loading interview for {governor_id}: {e}")
            return None
    
    def get_response(self, governor_id: str, question_id: int) -> Optional[InterviewResponse]:
        """Get specific response from a governor"""
        interview = self.load_governor_interview(governor_id)
        if not interview:
            return None
        
        for response in interview.responses:
            if response.question_id == question_id:
                return response
        
        return None
    
    def get_responses_by_topic(self, topic: str, limit: int = 10) -> List[Tuple[str, InterviewResponse]]:
        """Get responses related to a specific topic"""
        results = []
        
        # Use topic index for fast lookup
        topic_entries = self.topic_index.get(topic.lower(), [])
        
        for entry in topic_entries[:limit]:
            governor_id = entry['governor_id']
            question_id = entry['question_id']
            
            response = self.get_response(governor_id, question_id)
            if response:
                results.append((governor_id, response))
        
        return results
    
    def get_governors_by_tradition(self, tradition: str) -> List[str]:
        """Get governors associated with a specific tradition"""
        return self.tradition_index.get(tradition, [])
    
    def search_responses(self, query: str, limit: int = 10) -> List[Tuple[str, InterviewResponse]]:
        """Search responses by text content"""
        results = []
        query_lower = query.lower()
        
        # Get all governor files
        governor_files = list(self.governors_path.glob("*.json"))
        
        for gov_file in governor_files:
            governor_id = gov_file.stem.upper()
            interview = self.load_governor_interview(governor_id)
            
            if not interview:
                continue
            
            for response in interview.responses:
                if (query_lower in response.question.lower() or 
                    query_lower in response.answer.lower()):
                    results.append((governor_id, response))
                    
                    if len(results) >= limit:
                        return results
        
        return results
    
    def get_high_authenticity_responses(self, min_score: float = 0.95, limit: int = 20) -> List[Tuple[str, InterviewResponse]]:
        """Get responses with high authenticity scores"""
        results = []
        
        governor_files = list(self.governors_path.glob("*.json"))
        
        for gov_file in governor_files:
            governor_id = gov_file.stem.upper()
            interview = self.load_governor_interview(governor_id)
            
            if not interview:
                continue
            
            for response in interview.responses:
                if response.authenticity_score >= min_score:
                    results.append((governor_id, response))
        
        # Sort by authenticity score (highest first)
        results.sort(key=lambda x: x[1].authenticity_score, reverse=True)
        
        return results[:limit]
    
    def get_wisdom_for_quest_generation(self, governor_id: str, quest_theme: str) -> List[InterviewResponse]:
        """Get relevant wisdom responses for quest generation"""
        interview = self.load_governor_interview(governor_id)
        if not interview:
            return []
        
        # Filter responses relevant to quest theme
        relevant_responses = []
        theme_lower = quest_theme.lower()
        
        for response in interview.responses:
            if (theme_lower in response.question.lower() or 
                theme_lower in response.answer.lower() or
                any(theme_lower in source.lower() for source in response.authenticity_sources)):
                relevant_responses.append(response)
        
        # Sort by authenticity score
        relevant_responses.sort(key=lambda x: x.authenticity_score, reverse=True)
        
        return relevant_responses
    
    def get_title_based_wisdom(self, governor_id: str) -> List[InterviewResponse]:
        """Get wisdom responses that relate to the governor's title"""
        interview = self.load_governor_interview(governor_id)
        if not interview:
            return []
        
        # Extract key words from title
        title_words = interview.title.lower().replace("'", "").split()
        title_keywords = [word for word in title_words if len(word) > 3]
        
        relevant_responses = []
        
        for response in interview.responses:
            response_text = (response.question + " " + response.answer).lower()
            
            # Check if any title keywords appear in the response
            if any(keyword in response_text for keyword in title_keywords):
                relevant_responses.append(response)
        
        return relevant_responses
    
    def generate_cryptic_hint(self, governor_id: str, topic: str) -> Optional[str]:
        """Generate cryptic hint for blockchain puzzles based on interview data"""
        responses = self.get_wisdom_for_quest_generation(governor_id, topic)
        
        if not responses:
            return None
        
        # Use highest authenticity response
        best_response = max(responses, key=lambda x: x.authenticity_score)
        
        # Create cryptic hint by combining elements
        hint_elements = [
            f"The {best_response.phase} reveals:",
            best_response.answer[:100] + "...",
            f"Sources: {', '.join(best_response.authenticity_sources[:2])}"
        ]
        
        return " | ".join(hint_elements)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get loader statistics"""
        governor_files = list(self.governors_path.glob("*.json"))
        
        return {
            'total_governors': len(governor_files),
            'cached_interviews': len(self.interview_cache),
            'master_questions': len(self.master_questions),
            'indexed_topics': len(self.topic_index),
            'indexed_traditions': len(self.tradition_index),
            'loader_ready': True
        }

def main():
    """Test the interview loader"""
    logger.info("Testing Interview Loader")
    
    # Create loader
    loader = InterviewLoader()
    
    # Display statistics
    stats = loader.get_statistics()
    logger.info(f"\n=== INTERVIEW LOADER STATISTICS ===")
    for key, value in stats.items():
        logger.info(f"{key}: {value}")
    
    # Test loading a governor
    if stats['total_governors'] > 0:
        # Get first governor file
        first_gov_file = list(Path("interviews/governors").glob("*.json"))[0]
        governor_id = first_gov_file.stem.upper()
        
        logger.info(f"\n=== TESTING WITH {governor_id} ===")
        
        # Load interview
        interview = loader.load_governor_interview(governor_id)
        if interview:
            logger.info(f"Loaded interview: {interview.total_responses} responses")
            logger.info(f"Title: {interview.title}")
            logger.info(f"Authenticity: {interview.overall_authenticity_score:.3f}")
            
            # Test title-based wisdom
            title_wisdom = loader.get_title_based_wisdom(governor_id)
            logger.info(f"Title-based wisdom: {len(title_wisdom)} responses")
            
            # Test cryptic hint generation
            hint = loader.generate_cryptic_hint(governor_id, "wisdom")
            if hint:
                logger.info(f"Cryptic hint: {hint[:100]}...")
    
    return loader

if __name__ == "__main__":
    main()
