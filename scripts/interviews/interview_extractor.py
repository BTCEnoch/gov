#!/usr/bin/env python3
"""
Enochian Cyphers Interview Data Extractor

Extracts interview data from existing governor profiles and creates the isolated
interview directory structure as recommended by expert feedback.

This addresses the need for modular architecture by separating interview data
from core profiles, enabling better engine integration and TAP Protocol optimization.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedResponse:
    """Single extracted interview response"""
    question_id: int
    question: str
    answer: str
    reasoning: str
    authenticity_sources: List[str]
    phase: str
    authenticity_score: float

@dataclass
class ExtractedInterview:
    """Complete extracted interview for a governor"""
    governor_id: str
    governor_name: str
    title: str
    aethyr: str
    element: str
    responses: List[ExtractedResponse]
    total_responses: int
    overall_authenticity_score: float
    extraction_timestamp: str

class InterviewExtractor:
    """Extracts interview data from governor profiles"""
    
    def __init__(self, profiles_path: str = "governor_profiles", output_path: str = "interviews"):
        self.profiles_path = Path(profiles_path)
        self.output_path = Path(output_path)
        self.extracted_interviews = {}
        self.topic_index = {}
        self.tradition_index = {}
        
        # Create output directories
        self.output_path.mkdir(exist_ok=True)
        (self.output_path / "governors").mkdir(exist_ok=True)
        (self.output_path / "indexes").mkdir(exist_ok=True)
    
    def extract_all_interviews(self) -> Dict[str, ExtractedInterview]:
        """Extract interview data from all governor profiles"""
        logger.info("Extracting interview data from all governor profiles...")
        
        profile_files = list(self.profiles_path.glob("*_complete_interview.json"))
        
        if len(profile_files) != 91:
            logger.warning(f"Expected 91 governor profiles, found {len(profile_files)}")
        
        for profile_file in profile_files:
            try:
                governor_name = profile_file.stem.replace("_complete_interview", "")
                extracted = self._extract_single_interview(profile_file, governor_name)
                if extracted:
                    self.extracted_interviews[governor_name] = extracted
                    self._index_interview(extracted)
                    
            except Exception as e:
                logger.error(f"Error extracting interview from {profile_file}: {e}")
        
        logger.info(f"Extracted interviews for {len(self.extracted_interviews)} governors")
        return self.extracted_interviews
    
    def _extract_single_interview(self, profile_file: Path, governor_name: str) -> Optional[ExtractedInterview]:
        """Extract interview data from a single governor profile"""
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Extract basic governor info
            gov_profile = profile_data.get('governor_profile', {})
            title = gov_profile.get('title', '')
            aethyr = gov_profile.get('aethyr', '')
            element = gov_profile.get('element', '')
            
            # Extract interview data from phases section
            phases_data = profile_data.get('phases', {})

            if not phases_data:
                logger.warning(f"No phases found for {governor_name}")
                return None

            responses = []
            total_authenticity = 0.0
            phase_count = 0

            # Process each phase
            for key, value in phases_data.items():
                if key.startswith('phase_') and isinstance(value, dict):
                    phase_responses = self._extract_phase_responses(value, governor_name)
                    responses.extend(phase_responses)

                    # Track authenticity
                    phase_auth = value.get('authenticity_score', 0.0)
                    if phase_auth > 0:
                        total_authenticity += phase_auth
                        phase_count += 1
            
            # Calculate overall authenticity
            overall_authenticity = total_authenticity / phase_count if phase_count > 0 else 0.0
            
            extracted = ExtractedInterview(
                governor_id=governor_name,
                governor_name=governor_name,
                title=title,
                aethyr=aethyr,
                element=element,
                responses=responses,
                total_responses=len(responses),
                overall_authenticity_score=overall_authenticity,
                extraction_timestamp=datetime.now().isoformat()
            )
            
            return extracted
            
        except Exception as e:
            logger.error(f"Error extracting interview for {governor_name}: {e}")
            return None
    
    def _extract_phase_responses(self, phase_data: Dict[str, Any], governor_name: str) -> List[ExtractedResponse]:
        """Extract responses from a single interview phase"""
        responses = []
        phase_name = phase_data.get('phase', 'unknown')
        phase_auth = phase_data.get('authenticity_score', 0.0)
        
        for response_data in phase_data.get('responses', []):
            try:
                response = ExtractedResponse(
                    question_id=response_data.get('question_number', 0),
                    question=response_data.get('question', ''),
                    answer=response_data.get('answer', ''),
                    reasoning=response_data.get('reasoning', ''),
                    authenticity_sources=response_data.get('authenticity_sources', []),
                    phase=phase_name,
                    authenticity_score=phase_auth
                )
                responses.append(response)
            except Exception as e:
                logger.error(f"Error extracting response for {governor_name}: {e}")
        
        return responses
    
    def _index_interview(self, interview: ExtractedInterview):
        """Create indexes for fast querying"""
        # Topic index - extract keywords from questions and answers
        for response in interview.responses:
            keywords = self._extract_keywords(response.question + " " + response.answer)
            for keyword in keywords:
                if keyword not in self.topic_index:
                    self.topic_index[keyword] = []
                self.topic_index[keyword].append({
                    'governor_id': interview.governor_id,
                    'question_id': response.question_id,
                    'relevance': 1.0  # Could be enhanced with TF-IDF
                })
        
        # Tradition index - map to lighthouse traditions
        traditions = self._map_to_traditions(interview)
        for tradition in traditions:
            if tradition not in self.tradition_index:
                self.tradition_index[tradition] = []
            self.tradition_index[tradition].append(interview.governor_id)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        import re
        
        # Common words to filter out
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words, filter common words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in common_words]
        
        return list(set(keywords))
    
    def _map_to_traditions(self, interview: ExtractedInterview) -> List[str]:
        """Map interview content to lighthouse traditions"""
        traditions = ['enochian_magic']  # Always include Enochian base
        
        # Add traditions based on content analysis
        content = " ".join([r.question + " " + r.answer for r in interview.responses]).lower()
        
        tradition_keywords = {
            'hermetic_qabalah': ['qabalah', 'sephirot', 'tree of life', 'hermetic'],
            'tarot': ['tarot', 'arcana', 'cards', 'divination'],
            'astrology': ['astrology', 'zodiac', 'planets', 'houses'],
            'alchemy': ['alchemy', 'transmutation', 'philosopher', 'stone'],
            'golden_dawn': ['golden dawn', 'ceremonial', 'ritual'],
            'chaos_magic': ['chaos', 'paradigm', 'belief', 'gnosis'],
            'i_ching': ['i ching', 'hexagram', 'trigram', 'change'],
            'sacred_geometry': ['geometry', 'sacred', 'geometric', 'pattern'],
            'taoism': ['tao', 'yin', 'yang', 'balance'],
            'sufism': ['sufi', 'mystical', 'divine', 'spiritual']
        }
        
        for tradition, keywords in tradition_keywords.items():
            if any(keyword in content for keyword in keywords):
                traditions.append(tradition)
        
        return traditions
    
    def save_extracted_interviews(self):
        """Save extracted interviews to individual files"""
        logger.info("Saving extracted interviews...")
        
        for governor_id, interview in self.extracted_interviews.items():
            # Save individual governor interview
            output_file = self.output_path / "governors" / f"{governor_id.lower()}.json"
            
            interview_data = {
                'governor_id': interview.governor_id,
                'governor_name': interview.governor_name,
                'title': interview.title,
                'aethyr': interview.aethyr,
                'element': interview.element,
                'total_responses': interview.total_responses,
                'overall_authenticity_score': interview.overall_authenticity_score,
                'extraction_timestamp': interview.extraction_timestamp,
                'responses': [asdict(response) for response in interview.responses]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(interview_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.extracted_interviews)} individual interview files")
    
    def save_indexes(self):
        """Save search indexes"""
        logger.info("Saving search indexes...")
        
        # Save topic index
        topic_index_file = self.output_path / "indexes" / "topic_index.json"
        with open(topic_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.topic_index, f, indent=2, ensure_ascii=False)
        
        # Save tradition index
        tradition_index_file = self.output_path / "indexes" / "tradition_index.json"
        with open(tradition_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.tradition_index, f, indent=2, ensure_ascii=False)
        
        logger.info("Saved search indexes")
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Generate extraction statistics"""
        total_responses = sum(len(interview.responses) for interview in self.extracted_interviews.values())
        avg_authenticity = sum(interview.overall_authenticity_score for interview in self.extracted_interviews.values()) / len(self.extracted_interviews) if self.extracted_interviews else 0
        
        return {
            'total_governors': len(self.extracted_interviews),
            'total_responses': total_responses,
            'average_responses_per_governor': total_responses / len(self.extracted_interviews) if self.extracted_interviews else 0,
            'average_authenticity_score': avg_authenticity,
            'total_topics_indexed': len(self.topic_index),
            'total_traditions_mapped': len(self.tradition_index),
            'extraction_timestamp': datetime.now().isoformat()
        }

def main():
    """Main extraction function"""
    logger.info("Starting Governor Interview Data Extraction")
    
    # Create extractor
    extractor = InterviewExtractor()
    
    # Extract all interviews
    interviews = extractor.extract_all_interviews()
    
    # Save extracted data
    extractor.save_extracted_interviews()
    extractor.save_indexes()
    
    # Generate and save statistics
    stats = extractor.generate_statistics()
    stats_file = Path("interviews") / "extraction_statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    # Display results
    logger.info(f"\n=== INTERVIEW EXTRACTION COMPLETE ===")
    logger.info(f"Total Governors: {stats['total_governors']}")
    logger.info(f"Total Responses: {stats['total_responses']}")
    logger.info(f"Average Responses per Governor: {stats['average_responses_per_governor']:.1f}")
    logger.info(f"Average Authenticity Score: {stats['average_authenticity_score']:.3f}")
    logger.info(f"Topics Indexed: {stats['total_topics_indexed']}")
    logger.info(f"Traditions Mapped: {stats['total_traditions_mapped']}")
    
    return extractor

if __name__ == "__main__":
    main()
