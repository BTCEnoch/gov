"""
Base Governor Profile Generator
Core functionality for generating governor profiles
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

from core.governors.profiler.schemas.profile_schemas import GovernorProfile, MysticalAttribute
from core.governors.traits.knowledge_base.unified_knowledge_retriever import UnifiedKnowledgeRetriever
from core.utils.mystical.base import MysticalEntity
from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseGovernorGenerator:
    """Base class for generating Governor profiles"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the base generator"""
        self.config = config or {}
        self.knowledge_retriever = UnifiedKnowledgeRetriever()
        self.logger = logger
        
    def generate_profile(
        self,
        governor_id: str,
        name: str,
        rank: int,
        mystical_data: Dict[str, Any]
    ) -> GovernorProfile:
        """
        Generate a complete Governor profile
        
        Args:
            governor_id: Unique identifier for the governor
            name: Governor's name
            rank: Governor's rank (1-91)
            mystical_data: Additional mystical attributes and data
            
        Returns:
            Complete governor profile
        """
        try:
            # Create base profile
            now = datetime.now()
            profile = GovernorProfile(
                id=governor_id,
                name=name,
                rank=rank,
                attributes=[],
                relationships={},
                metadata={},
                created_at=now,
                updated_at=now
            )
            
            # Add mystical attributes
            if "attributes" in mystical_data:
                profile.attributes.extend(mystical_data["attributes"])
                
            # Add relationships
            if "relationships" in mystical_data:
                profile.relationships.update(mystical_data["relationships"])
                
            # Add metadata
            if "metadata" in mystical_data:
                profile.metadata.update(mystical_data["metadata"])
                
            # Enrich with knowledge base data
            self._enrich_with_knowledge(profile)
                
            return profile
            
        except Exception as e:
            self.logger.error(f"Failed to generate profile: {e}")
            raise
            
    def _enrich_with_knowledge(self, profile: GovernorProfile) -> None:
        """
        Enrich profile with knowledge from the Lighthouse
        
        Args:
            profile: Governor profile to enrich
        """
        try:
            # Get relevant knowledge entries
            entries = self.knowledge_retriever.search_by_tag(profile.name)
            
            # Add knowledge-based attributes
            for entry in entries:
                if entry.knowledge_type == "trait":
                    profile.attributes.append(
                        MysticalAttribute(
                            name=entry.id,
                            value=str(entry),  # Convert entry to string representation
                            source="lighthouse"
                        )
                    )
                    
            self.logger.info(f"Enriched profile with {len(entries)} knowledge entries")
            
        except Exception as e:
            self.logger.error(f"Failed to enrich profile with knowledge: {e}")
            # Continue without knowledge enrichment 