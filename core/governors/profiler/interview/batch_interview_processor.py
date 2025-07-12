"""Batch processor for governor interviews"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

from core.utils.custom_logging import setup_logger
from core.governors.generator import GovernorProfile
from core.governors.traits.visual_aspects.schemas import VisualTraits
from core.governors.traits.generator import TraitGenerator

logger = setup_logger(__name__)

class BatchInterviewProcessor:
    """Processes multiple governors through the interview system"""
    
    def __init__(self, knowledge_base_path: str, max_concurrent: int = 5):
        """Initialize the batch processor"""
        self.knowledge_base_path = Path(knowledge_base_path)
        self.max_concurrent = max_concurrent
        self.logger = logger
        self.trait_generator = TraitGenerator()
        
    def load_governor_profiles(self, profiles_dir: str) -> List[GovernorProfile]:
        """Load governor profiles from JSON files"""
        profiles_path = Path(profiles_dir)
        profiles = []
        
        try:
            for profile_file in profiles_path.glob("*.json"):
                with open(profile_file, "r") as f:
                    profile_data = json.load(f)
                    profiles.append(GovernorProfile(**profile_data))
        except Exception as e:
            self.logger.error(f"Error loading profiles: {e}")
            raise
            
        return profiles

    async def process_interviews(self, profiles: List[GovernorProfile]) -> Dict[str, VisualTraits]:
        """Process interviews for multiple governors"""
        results = {}
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_single(profile: GovernorProfile):
            async with semaphore:
                try:
                    # Process interview and generate visual traits
                    visual_traits = await self._process_interview(profile)
                    results[profile.id] = visual_traits
                except Exception as e:
                    self.logger.error(f"Error processing {profile.id}: {e}")
                    
        await asyncio.gather(*[process_single(p) for p in profiles])
        return results

    def save_results(self, results: Dict[str, VisualTraits], output_dir: str) -> None:
        """Save interview results to JSON files.
        
        Args:
            results: Dictionary mapping governor IDs to their visual traits
            output_dir: Directory to save results in
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for governor_id, traits in results.items():
            try:
                output_file = output_path / f"{governor_id}_visual_traits.json"
                with open(output_file, "w") as f:
                    # Convert Pydantic model to dict for serialization
                    json.dump(traits.dict(), f, indent=2)
                self.logger.info(f"Saved results for {governor_id}")
            except Exception as e:
                self.logger.error(f"Error saving results for {governor_id}: {e}")
                raise

    async def _process_interview(self, profile: GovernorProfile) -> VisualTraits:
        """Process a single governor interview
        
        Args:
            profile: The governor profile to process
            
        Returns:
            Generated visual traits for the governor
        """
        try:
            # Generate visual traits using the trait generator
            visual_traits = self.trait_generator._generate_visual_traits(
                governor_id=profile.id,
                governor_number=profile.rank
            )
            return visual_traits
        except Exception as e:
            self.logger.error(f"Failed to process interview for {profile.id}: {e}")
            raise 