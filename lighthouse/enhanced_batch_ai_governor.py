#!/usr/bin/env python3
"""
Enochian Cyphers Enhanced Batch AI Governor Engine

Implements enhanced batch quest generation with asyncio parallelism for 91 governors,
targeting 75-125 quests each (~9,126 total). Integrates with Dynamic Lighthouse 
Retrieval and hypertoken evolution hooks.

This addresses expert feedback Phase 2: "Scale AI Governor Content Engine with Batch API Parallelism"
- Asyncio parallel processing for 91 governors
- Integration with Dynamic Lighthouse weighted retrieval
- Hypertoken evolution hooks for quest completion
- Authentic content grounding via Enochian base + domain blending
- Performance optimization for large-scale content generation

Maintains structural care by placing in /lighthouse directory for AI content
generation components integrated with knowledge base systems.
"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import random

# Import our Dynamic Lighthouse Retriever
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from dynamic_retriever import DynamicLighthouseRetriever, RetrievalQuery

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EnhancedQuest:
    """Enhanced quest with Lighthouse knowledge integration"""
    quest_id: str
    title: str
    description: str
    objectives: List[str]
    wisdom_taught: str
    enochian_invocation: str
    tradition_references: List[str]
    difficulty_level: int
    completion_criteria: List[str]
    rewards_suggestion: str
    branching_paths: Optional[Dict[str, str]]
    lighthouse_sources: List[str]  # Source knowledge entries
    authenticity_score: float
    hypertoken_evolution: Dict[str, Any]
    domain_relevance: Dict[str, float]

@dataclass
class EnhancedGovernorQuestline:
    """Enhanced questline with Lighthouse integration and metadata"""
    governor_name: str
    questline_title: str
    narrative_arc: str
    total_quests: int
    quests: List[EnhancedQuest]
    wisdom_focus: str
    lighthouse_knowledge_base: List[str]  # Knowledge entry IDs used
    average_authenticity: float
    enochian_percentage: float
    domain_coverage: Dict[str, int]
    generation_metadata: Dict[str, Any]
    hypertoken_evolutions: List[Dict[str, Any]]

@dataclass
class BatchGenerationConfig:
    """Configuration for batch AI generation"""
    target_quests_per_governor: int = 100
    min_quests_per_governor: int = 75
    max_quests_per_governor: int = 125
    enochian_weight: float = 0.6
    min_authenticity: float = 0.8
    max_concurrent_governors: int = 10
    lighthouse_entries_per_quest: int = 5
    enable_hypertoken_evolution: bool = True
    cost_limit_usd: float = 100.0
    api_provider: str = "mock"  # mock, openai, anthropic

class EnhancedBatchAIGovernor:
    """Enhanced batch AI governor engine with Lighthouse integration"""
    
    def __init__(self, config: BatchGenerationConfig = None):
        self.config = config or BatchGenerationConfig()
        self.lighthouse_retriever = DynamicLighthouseRetriever()
        self.governor_profiles = {}
        self.aethyr_mappings = {}
        self.generation_stats = {
            'total_governors_processed': 0,
            'total_quests_generated': 0,
            'total_lighthouse_retrievals': 0,
            'average_authenticity': 0.0,
            'generation_time': 0.0,
            'api_calls_made': 0,
            'cost_incurred': 0.0
        }
        
        # Load governor data
        self._load_governor_profiles()
        self._load_aethyr_mappings()
        
        logger.info(f"Enhanced Batch AI Governor initialized with {len(self.governor_profiles)} governors")
    
    def _load_governor_profiles(self):
        """Load governor profiles from interviews"""
        profiles_dir = Path("governor_profiles")
        if profiles_dir.exists():
            for profile_file in profiles_dir.glob("*_complete_interview.json"):
                try:
                    with open(profile_file, 'r', encoding='utf-8') as f:
                        profile_data = json.load(f)
                    
                    governor_name = profile_file.stem.replace('_complete_interview', '')
                    self.governor_profiles[governor_name] = profile_data
                    
                except Exception as e:
                    logger.warning(f"Error loading profile {profile_file}: {e}")
        
        logger.info(f"Loaded {len(self.governor_profiles)} governor profiles")
    
    def _load_aethyr_mappings(self):
        """Load Aethyr mappings for governor specializations"""
        mappings_file = Path("governor_profiles/aethyr_mappings.json")
        if mappings_file.exists():
            try:
                with open(mappings_file, 'r', encoding='utf-8') as f:
                    self.aethyr_mappings = json.load(f)
                logger.info("Loaded Aethyr mappings")
            except Exception as e:
                logger.warning(f"Error loading Aethyr mappings: {e}")
    
    def _determine_governor_domain(self, governor_name: str) -> str:
        """Determine primary domain for governor based on profile and Aethyr"""
        # Default domains based on common governor specializations
        domain_keywords = {
            'knowledge': ['wisdom', 'learning', 'understanding', 'insight', 'study'],
            'protection': ['guard', 'shield', 'defend', 'protect', 'safety'],
            'transformation': ['change', 'evolve', 'transform', 'growth', 'mutation'],
            'divination': ['prophecy', 'vision', 'foresight', 'oracle', 'scrying'],
            'healing': ['heal', 'cure', 'restore', 'balance', 'harmony'],
            'creation': ['create', 'manifest', 'build', 'form', 'generate'],
            'destruction': ['destroy', 'banish', 'dissolve', 'end', 'break'],
            'communication': ['speak', 'communicate', 'message', 'word', 'language']
        }
        
        # Check governor profile for domain indicators
        profile = self.governor_profiles.get(governor_name, {})
        profile_text = json.dumps(profile).lower()
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(profile_text.count(keyword) for keyword in keywords)
            domain_scores[domain] = score
        
        # Return domain with highest score, default to 'knowledge'
        return max(domain_scores, key=domain_scores.get) if max(domain_scores.values()) > 0 else 'knowledge'
    
    async def _retrieve_lighthouse_knowledge(self, governor_name: str, domain: str, num_entries: int = 5) -> Tuple[List[Any], Dict[str, Any]]:
        """Retrieve weighted knowledge from Lighthouse for quest generation"""
        query = RetrievalQuery(
            governor_domain=domain,
            num_entries=num_entries,
            enochian_weight=self.config.enochian_weight,
            min_authenticity=self.config.min_authenticity
        )
        
        result = self.lighthouse_retriever.weighted_knowledge_retrieval(query)
        self.generation_stats['total_lighthouse_retrievals'] += 1
        
        return result.entries, {
            'enochian_percentage': result.enochian_percentage,
            'average_authenticity': result.average_authenticity,
            'domain_coverage': result.domain_coverage,
            'total_available': result.total_available
        }
    
    def _create_hypertoken_evolution(self, governor_name: str, quest_id: str, lighthouse_entries: List[Any]) -> Dict[str, Any]:
        """Create hypertoken evolution data for quest"""
        if not self.config.enable_hypertoken_evolution:
            return {}
        
        # Calculate evolution parameters based on lighthouse knowledge
        avg_authenticity = sum(entry.authenticity_score for entry in lighthouse_entries) / len(lighthouse_entries) if lighthouse_entries else 0.8
        enochian_influence = sum(entry.enochian_weight for entry in lighthouse_entries) / len(lighthouse_entries) if lighthouse_entries else 0.5
        
        # Determine evolution traits based on content
        traits = []
        if avg_authenticity >= 0.9:
            traits.append("authentic_wisdom")
        if enochian_influence >= 0.5:
            traits.append("enochian_resonance")
        
        # Add domain-specific traits
        domain_traits = set()
        for entry in lighthouse_entries:
            for domain, relevance in entry.domain_relevance.items():
                if relevance >= 0.3:
                    domain_traits.add(f"{domain}_mastery")
        traits.extend(list(domain_traits))
        
        return {
            'token_id': f"{governor_name}_{quest_id}_hypertoken",
            'evolution_stage': 'nascent',
            'wisdom_level': int(avg_authenticity * 10),
            'enochian_resonance': enochian_influence,
            'traits': traits,
            'evolution_potential': avg_authenticity * enochian_influence,
            'creation_timestamp': datetime.now().isoformat()
        }
    
    async def _mock_ai_generation(self, governor_name: str, lighthouse_entries: List[Any], domain: str, quest_count: int) -> List[EnhancedQuest]:
        """Mock AI generation for testing (replace with real API calls)"""
        quests = []
        
        for i in range(quest_count):
            # Simulate AI processing time
            await asyncio.sleep(0.01)
            
            quest_id = f"{governor_name}_QUEST_{i+1:03d}"
            
            # Select random lighthouse entries for this quest
            quest_entries = random.sample(lighthouse_entries, min(self.config.lighthouse_entries_per_quest, len(lighthouse_entries)))
            
            # Calculate quest authenticity based on source entries
            quest_authenticity = sum(entry.authenticity_score for entry in quest_entries) / len(quest_entries) if quest_entries else 0.8
            
            # Create hypertoken evolution
            hypertoken_evolution = self._create_hypertoken_evolution(governor_name, quest_id, quest_entries)
            
            # Calculate domain relevance
            domain_relevance = {}
            for entry in quest_entries:
                for domain_name, relevance in entry.domain_relevance.items():
                    domain_relevance[domain_name] = max(domain_relevance.get(domain_name, 0), relevance)
            
            quest = EnhancedQuest(
                quest_id=quest_id,
                title=f"The {random.choice(['Sacred', 'Hidden', 'Ancient', 'Mystical'])} Path of {quest_entries[0].name if quest_entries else 'Wisdom'}",
                description=f"A quest inspired by {quest_entries[0].tradition if quest_entries else 'ancient wisdom'} teachings, guiding seekers through {domain} mastery via Enochian invocations.",
                objectives=[
                    f"Study the principles of {quest_entries[0].name if quest_entries else 'wisdom'}",
                    f"Practice {domain}-based meditation techniques",
                    f"Integrate {governor_name}'s guidance into daily practice"
                ],
                wisdom_taught=f"{domain.title()} mastery through {quest_entries[0].tradition if quest_entries else 'traditional'} principles",
                enochian_invocation=f"OL SONF VORSG {governor_name} GOHO IAD BALT",  # Mock Enochian
                tradition_references=[entry.tradition for entry in quest_entries],
                difficulty_level=random.randint(3, 8),
                completion_criteria=[
                    "Demonstrate understanding of core principles",
                    "Complete practical exercises",
                    "Receive governor's blessing"
                ],
                rewards_suggestion=f"Enhanced {domain} abilities and {governor_name} attunement",
                branching_paths={
                    "success": f"Advanced {domain} mastery path",
                    "failure": f"Foundational {domain} review"
                },
                lighthouse_sources=[entry.id for entry in quest_entries],
                authenticity_score=quest_authenticity,
                hypertoken_evolution=hypertoken_evolution,
                domain_relevance=domain_relevance
            )
            
            quests.append(quest)
        
        return quests

    async def generate_governor_questline(self, governor_name: str) -> Optional[EnhancedGovernorQuestline]:
        """Generate enhanced questline for a single governor with Lighthouse integration"""
        logger.info(f"Generating enhanced questline for {governor_name}")

        try:
            # Determine governor's primary domain
            domain = self._determine_governor_domain(governor_name)

            # Retrieve Lighthouse knowledge for this governor
            lighthouse_entries, retrieval_metadata = await self._retrieve_lighthouse_knowledge(
                governor_name, domain, num_entries=20
            )

            if not lighthouse_entries:
                logger.warning(f"No lighthouse entries found for {governor_name} in domain {domain}")
                return None

            # Determine quest count (75-125 range)
            quest_count = random.randint(self.config.min_quests_per_governor, self.config.max_quests_per_governor)

            # Generate quests using AI (mock for now)
            quests = await self._mock_ai_generation(governor_name, lighthouse_entries, domain, quest_count)

            # Calculate questline metadata
            lighthouse_knowledge_base = [entry.id for entry in lighthouse_entries]
            average_authenticity = sum(quest.authenticity_score for quest in quests) / len(quests) if quests else 0.0
            enochian_percentage = retrieval_metadata.get('enochian_percentage', 0.0)

            # Calculate domain coverage
            domain_coverage = {}
            for quest in quests:
                for domain_name, relevance in quest.domain_relevance.items():
                    if relevance >= 0.2:
                        domain_coverage[domain_name] = domain_coverage.get(domain_name, 0) + 1

            # Collect hypertoken evolutions
            hypertoken_evolutions = [quest.hypertoken_evolution for quest in quests if quest.hypertoken_evolution]

            questline = EnhancedGovernorQuestline(
                governor_name=governor_name,
                questline_title=f"The Sacred Path of {governor_name}: {domain.title()} Mastery",
                narrative_arc=f"A comprehensive journey through {domain} mastery guided by Governor {governor_name}, integrating Enochian wisdom with {', '.join(set(entry.tradition for entry in lighthouse_entries[:3]))} traditions.",
                total_quests=len(quests),
                quests=quests,
                wisdom_focus=f"{domain.title()} mastery through Enochian-grounded practice",
                lighthouse_knowledge_base=lighthouse_knowledge_base,
                average_authenticity=average_authenticity,
                enochian_percentage=enochian_percentage,
                domain_coverage=domain_coverage,
                generation_metadata={
                    'generation_timestamp': datetime.now().isoformat(),
                    'lighthouse_retrieval_metadata': retrieval_metadata,
                    'primary_domain': domain,
                    'quest_generation_method': 'enhanced_ai_batch',
                    'config_used': asdict(self.config)
                },
                hypertoken_evolutions=hypertoken_evolutions
            )

            # Update generation stats
            self.generation_stats['total_governors_processed'] += 1
            self.generation_stats['total_quests_generated'] += len(quests)

            logger.info(f"Generated {len(quests)} quests for {governor_name} with {average_authenticity:.3f} avg authenticity")
            return questline

        except Exception as e:
            logger.error(f"Error generating questline for {governor_name}: {e}")
            return None

    async def batch_generate_all_questlines(self, governor_names: List[str] = None) -> List[EnhancedGovernorQuestline]:
        """Generate questlines for all governors using async batch processing"""
        start_time = time.time()

        # Use all available governors if none specified
        if governor_names is None:
            governor_names = list(self.governor_profiles.keys())

        logger.info(f"Starting batch generation for {len(governor_names)} governors")

        # Create semaphore to limit concurrent operations
        semaphore = asyncio.Semaphore(self.config.max_concurrent_governors)

        async def generate_with_semaphore(governor_name: str):
            async with semaphore:
                return await self.generate_governor_questline(governor_name)

        # Execute all generations concurrently
        tasks = [generate_with_semaphore(name) for name in governor_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter successful results
        questlines = []
        for i, result in enumerate(results):
            if isinstance(result, EnhancedGovernorQuestline):
                questlines.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Error generating questline for {governor_names[i]}: {result}")

        # Update final stats
        end_time = time.time()
        self.generation_stats['generation_time'] = end_time - start_time
        self.generation_stats['average_authenticity'] = (
            sum(q.average_authenticity for q in questlines) / len(questlines) if questlines else 0.0
        )

        logger.info(f"Batch generation complete: {len(questlines)} questlines generated in {self.generation_stats['generation_time']:.2f}s")
        return questlines

    def export_questlines(self, questlines: List[EnhancedGovernorQuestline], output_path: str = "lighthouse/enhanced_questlines_export.json"):
        """Export generated questlines with full metadata"""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'generation_statistics': self.generation_stats,
            'configuration': asdict(self.config),
            'total_questlines': len(questlines),
            'total_quests': sum(q.total_quests for q in questlines),
            'questlines': {
                questline.governor_name: asdict(questline) for questline in questlines
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(questlines)} questlines to {output_path}")

    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive generation statistics"""
        return {
            **self.generation_stats,
            'lighthouse_retriever_stats': self.lighthouse_retriever.get_retrieval_statistics(),
            'config': asdict(self.config),
            'governors_available': len(self.governor_profiles),
            'aethyr_mappings_loaded': bool(self.aethyr_mappings)
        }

async def test_enhanced_batch_ai():
    """Test the enhanced batch AI governor system"""
    logger.info("=== TESTING ENHANCED BATCH AI GOVERNOR SYSTEM ===")

    # Initialize with test configuration
    config = BatchGenerationConfig(
        target_quests_per_governor=10,  # Reduced for testing
        min_quests_per_governor=8,
        max_quests_per_governor=12,
        max_concurrent_governors=5,
        api_provider="mock"
    )

    ai_engine = EnhancedBatchAIGovernor(config)

    # Test single governor generation
    test_governors = list(ai_engine.governor_profiles.keys())[:3]  # Test with first 3 governors
    logger.info(f"Testing with governors: {test_governors}")

    # Generate questlines
    questlines = await ai_engine.batch_generate_all_questlines(test_governors)

    # Display results
    logger.info(f"\n=== GENERATION RESULTS ===")
    for questline in questlines:
        logger.info(f"Governor: {questline.governor_name}")
        logger.info(f"  Quests: {questline.total_quests}")
        logger.info(f"  Authenticity: {questline.average_authenticity:.3f}")
        logger.info(f"  Enochian %: {questline.enochian_percentage:.1f}%")
        logger.info(f"  Domain Coverage: {questline.domain_coverage}")
        logger.info(f"  Hypertoken Evolutions: {len(questline.hypertoken_evolutions)}")

    # Export results
    ai_engine.export_questlines(questlines)

    # Display statistics
    stats = ai_engine.get_generation_statistics()
    logger.info(f"\n=== SYSTEM STATISTICS ===")
    logger.info(f"Total Governors Processed: {stats['total_governors_processed']}")
    logger.info(f"Total Quests Generated: {stats['total_quests_generated']}")
    logger.info(f"Total Lighthouse Retrievals: {stats['total_lighthouse_retrievals']}")
    logger.info(f"Average Authenticity: {stats['average_authenticity']:.3f}")
    logger.info(f"Generation Time: {stats['generation_time']:.2f}s")
    logger.info(f"Lighthouse Stats: {stats['lighthouse_retriever_stats']['total_entries']} entries indexed")

    return ai_engine, questlines

if __name__ == "__main__":
    asyncio.run(test_enhanced_batch_ai())
