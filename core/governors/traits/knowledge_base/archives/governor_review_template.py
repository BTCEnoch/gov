#!/usr/bin/env python3
"""
Governor Review Template System
==============================

This script creates structured review templates for governors to evaluate and
potentially update their personality profiles and knowledge base selections
based on enhanced trait definitions and tradition summaries.

Part 1: Core template structure and review prompt generation
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from core.governors.traits.knowledge_base.archives.enhanced_trait_indexer import (
    EnhancedTraitIndexer, 
    EnhancedTraitIndex,
    TraitDefinition
)

# Configure logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('governor_review_template.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ReviewSection:
    """Section of the review template"""
    title: str
    description: str
    current_selections: List[str]
    available_options: Dict[str, str]  # trait_id -> trait_name
    guidance: str

@dataclass
class GovernorReviewTemplate:
    """Complete review template for a governor"""
    governor_name: str
    governor_number: int
    current_profile_summary: Dict[str, Any]
    review_sections: List[ReviewSection]
    enochian_magic_mandatory: bool = True
    additional_traditions_required: int = 4

class GovernorReviewTemplateGenerator:
    """Generates structured review templates for governor profile evaluation"""
    
    def __init__(
            self,
            tradition_index_file: str = "../../data/knowledge/indexes/tradition_index.json",
            governor_profiles_dir: str = "../../governor_dossier"):
        """Initialize the template generator"""
        self.logger = logging.getLogger(__name__)
        self.tradition_index_file = Path(tradition_index_file)
        self.governor_profiles_dir = Path(governor_profiles_dir)
        self.tradition_index = self._load_tradition_index()
        
        # Use enhanced trait indexer directly
        self.trait_indexer = EnhancedTraitIndexer()
        self.trait_index: EnhancedTraitIndex = self.trait_indexer.build_enhanced_index()
        
        self.logger.info("Governor Review Template Generator initialized")
        self.logger.info(f"Loaded trait index with {self.trait_index.total_traits} traits")

    def _load_tradition_index(self) -> Optional[Dict[str, Any]]:
        """Load the tradition index"""
        if not self.tradition_index_file.exists():
            self.logger.error(f"Tradition index file not found: {self.tradition_index_file}")
            return None
        
        try:
            with open(self.tradition_index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded tradition index")
            return data
        except Exception as e:
            self.logger.error(f"Error loading tradition index: {e}")
            return None

    def get_traits_by_category(self, category: str) -> List[TraitDefinition]:
        """Get all traits for a specific category"""
        traits = []
        for trait_id, trait_def in self.trait_index.trait_definitions.items():
            if trait_def.category == category:
                traits.append(trait_def)
        return traits

    def get_trait_definition(self, trait_id: str) -> Optional[TraitDefinition]:
        """Get trait definition by ID"""
        return self.trait_index.trait_definitions.get(trait_id)

    def get_trait_info(self, trait_id: str) -> Dict[str, str]:
        """Get trait information in a dictionary format"""
        trait = self.get_trait_definition(trait_id)
        if not trait:
            return {
                "name": "Unknown",
                "definition": "Definition not found",
                "category": "Unknown",
                "usage_context": "Context not found",
                "ai_personality_impact": "Impact not defined"
            }
        
        return {
            "name": trait.name,
            "definition": trait.definition,
            "category": trait.category,
            "usage_context": trait.usage_context,
            "ai_personality_impact": trait.ai_personality_impact
        }

    def load_governor_profile(self, governor_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific governor's profile"""
        profile_file = Path(__file__).parent.parent.parent / "governor_dossier" / f"{governor_name}.json"
        
        if not profile_file.exists():
            self.logger.error(f"Governor profile not found: {profile_file}")
            return None
        
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded profile for {governor_name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading governor profile {governor_name}: {e}")
            return None

    def create_knowledge_base_section(self, current_selections: List[str], governor_profile: Dict[str, Any]) -> ReviewSection:
        """Create knowledge base selection review section with thoughtful selection guidance"""
        # Get traits for the category
        traits = self.get_traits_by_category("knowledge_base")
        
        # Convert traits to the format needed for ReviewSection
        available_options = {
            trait_id: trait_def.name 
            for trait_id, trait_def in self.trait_index.trait_definitions.items()
            if trait_def.category == "knowledge_base"
        }
        
        # Generate guidance based on current selections
        guidance = self._generate_selection_guidance(current_selections, traits)
        
        return ReviewSection(
            title="Knowledge Base Selection",
            description="Select the mystical traditions that resonate with this governor's essence",
            current_selections=current_selections,
            available_options=available_options,
            guidance=guidance
        )

    def _generate_selection_guidance(self, current_selections: List[str], traits: List[TraitDefinition]) -> str:
        """Generate guidance for trait selection"""
        if not current_selections:
            return "Consider the governor's core nature and select traditions that align with their essence."
        
        # Get current trait info
        current_traits = []
        for trait_id in current_selections:
            trait = self.get_trait_definition(trait_id)
            if trait:
                current_traits.append(trait)
        
        # Generate guidance based on selected traits
        guidance_parts = []
        for trait in current_traits:
            guidance_parts.append(f"- {trait.name}: {trait.usage_context}")
        
        return "\n".join([
            "Current selections suggest the following focus areas:",
            *guidance_parts,
            "\nConsider how additional traditions might complement or balance these aspects."
        ])

    def create_personality_trait_section(self, trait_category: str, current_value: str, governor_profile: Dict[str, Any]) -> ReviewSection:
        """Create personality trait selection review section"""
        # Get traits for the category
        traits = self.get_traits_by_category(trait_category)
        
        # Convert traits to the format needed for ReviewSection
        available_options = {
            trait_id: trait_def.name 
            for trait_id, trait_def in self.trait_index.trait_definitions.items()
            if trait_def.category == trait_category
        }
        
        if not available_options:
            return ReviewSection(
                title=f"{trait_category.title()} Selection Error",
                description=f"No {trait_category} traits available",
                current_selections=[],
                available_options={},
                guidance="No traits available for this category."
            )
        
        # Get current trait info for guidance
        current_trait = None
        if current_value:
            current_trait = self.get_trait_definition(current_value)
        
        # Generate guidance
        if current_trait:
            guidance = f"""
Current Selection: {current_trait.name}
Definition: {current_trait.definition}
Impact: {current_trait.ai_personality_impact}

Consider if this trait truly represents the governor's essence.
Review other options that might better align with their personality.
""".strip()
        else:
            guidance = f"""
Select a {trait_category} trait that best represents this governor's personality.
Consider how each trait will influence their behavior and decision-making.
""".strip()
        
        return ReviewSection(
            title=f"{trait_category.title()} Selection",
            description=f"Select the {trait_category} that best represents this governor's personality",
            current_selections=[current_value] if current_value else [],
            available_options=available_options,
            guidance=guidance
        )

    def create_complete_review_template(self, governor_name: str) -> Optional[GovernorReviewTemplate]:
        """Create complete review template for a governor"""
        # Load governor profile
        profile = self.load_governor_profile(governor_name)
        if not profile:
            return None
        
        # Extract current personality data
        personality = profile.get("personality", {})
        knowledge_base_selections = profile.get("knowledge_base_selections", [])
        
        # Create profile summary
        profile_summary = {
            "name": profile.get("name", governor_name),
            "title": profile.get("title", ""),
            "aethyr": profile.get("aethyr", ""),
            "current_traditions": len(knowledge_base_selections),
            "total_personality_traits": len([v for v in personality.values() if v])
        }
        
        # Create review sections
        review_sections = []
        
        # 1. Knowledge Base Selection Review
        kb_section = self.create_knowledge_base_section(knowledge_base_selections, profile)
        review_sections.append(kb_section)
        
        # 2. Personality Trait Reviews
        trait_categories = [
            ("virtues", "virtue"),
            ("flaws", "flaw"), 
            ("approaches", "approach"),
            ("tones", "tone"),
            ("alignments", "motive_alignment"),
            ("roles", "role_archtype"),
            ("orientations", "orientation_io"),
            ("polarities", "polarity_cd"),
            ("self_regard", "self_regard")
        ]
        
        for category, profile_key in trait_categories:
            current_value = personality.get(profile_key, "")
            trait_section = self.create_personality_trait_section(category, current_value, profile)
            review_sections.append(trait_section)
        
        # Create complete template
        template = GovernorReviewTemplate(
            governor_name=governor_name,
            governor_number=profile.get("governor_number", 0),
            current_profile_summary=profile_summary,
            review_sections=review_sections
        )
        
        self.logger.info(f"Created complete review template for {governor_name}")
        return template

    def save_review_template(self, template: GovernorReviewTemplate, output_dir: str = "review_templates") -> bool:
        """Save a review template to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        output_file = output_path / f"{template.governor_name}_review_template.json"
        
        try:
            template_dict = asdict(template)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(template_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Review template saved: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving review template for {template.governor_name}: {e}")
            return False

    def generate_batch_review_templates(self, governor_names: Optional[List[str]] = None) -> int:
        """Generate review templates for multiple governors"""
        if governor_names is None:
            # Get all governor profile files
            profile_files = list(self.governor_profiles_dir.glob("*.json"))
            governor_names = [f.stem for f in profile_files]
        
        generated_count = 0
        
        for governor_name in governor_names[:5]:  # Limit for testing
            template = self.create_complete_review_template(governor_name)
            if template:
                if self.save_review_template(template):
                    generated_count += 1
                    self.logger.info(f"Generated template {generated_count}: {governor_name}")
            else:
                self.logger.warning(f"Failed to create template for {governor_name}")
        
        self.logger.info(f"Generated {generated_count} review templates")
        return generated_count

def main():
    """Test the complete governor review template generator"""
    print("Testing Complete Governor Review Template Generator...")
    
    try:
        generator = GovernorReviewTemplateGenerator()
        
        # Check if indexes loaded
        if not generator.trait_index:
            print("ERROR: Could not load trait index")
            return False
        
        if not generator.tradition_index:
            print("ERROR: Could not load tradition index")
            return False
        
        print(f"Trait index loaded: {generator.trait_index.total_traits} traits")
        print(f"Tradition index loaded: {generator.tradition_index.get('total_traditions', 0)} traditions")
        
        # Test trait category access
        virtues = generator.get_traits_by_category("virtues")
        print(f"Virtues available: {len(virtues)}")
        
        flaws = generator.get_traits_by_category("flaws")
        print(f"Flaws available: {len(flaws)}")
        
        # Test knowledge base section creation
        current_selections = ["enochian_magic", "hermetic_tradition", "kabbalah", "sacred_geometry"]
        kb_section = generator.create_knowledge_base_section(current_selections, {})
        print(f"\nKnowledge base section created:")
        print(f"  Available traditions: {len(kb_section.available_options)}")
        print(f"  Current selections: {len(kb_section.current_selections)}")
        
        # Test complete template creation for a sample governor
        print(f"\nTesting complete template creation...")
        sample_governor = "ABRIOND"  # First governor from the list
        
        template = generator.create_complete_review_template(sample_governor)
        if template:
            print(f"Template created for {template.governor_name}:")
            print(f"  Governor number: {template.governor_number}")
            print(f"  Review sections: {len(template.review_sections)}")
            print(f"  Current traditions: {template.current_profile_summary.get('current_traditions', 0)}")
            
            # Save the template
            if generator.save_review_template(template):
                print(f"  Template saved successfully!")
            
            # Show section summary
            print(f"\n  Review sections summary:")
            for section in template.review_sections:
                print(f"    • {section.title}: {len(section.available_options)} options")
        else:
            print(f"ERROR: Could not create template for {sample_governor}")
        
        # Test batch generation (limited to 3 governors for testing)
        print(f"\nTesting batch template generation...")
        generated_count = generator.generate_batch_review_templates()
        print(f"Generated {generated_count} review templates")
        
        print("\nGovernor Review Template Generator test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 