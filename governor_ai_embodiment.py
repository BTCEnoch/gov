#!/usr/bin/env python3
"""
Enochian Cyphers Governor AI Embodiment System

This system creates fully educated AI embodiments of the 91 Governor Angels
by combining their detailed profiles with the lighthouse knowledge base.
Each governor becomes an autonomous AI entity capable of generating
personalized questlines and interactions.
"""

import json
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GovernorKnowledge:
    """Represents a governor's combined profile and knowledge base"""
    name: str
    profile: Dict[str, Any]
    lighthouse_knowledge: Dict[str, List[Dict[str, Any]]]
    personality_prompt: str
    knowledge_summary: str

class LighthouseLoader:
    """Loads and indexes the complete lighthouse knowledge base"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.master_index = {}
        self.knowledge_base = {}
        
    def load_master_index(self) -> Dict[str, Any]:
        """Load the lighthouse master index"""
        index_path = self.lighthouse_path / "lighthouse_master_index.json"
        
        if not index_path.exists():
            raise FileNotFoundError(f"Master index not found at {index_path}")
            
        with open(index_path, 'r', encoding='utf-8') as f:
            self.master_index = json.load(f)
            
        logger.info(f"Loaded lighthouse index: {self.master_index['total_entries']} entries across {self.master_index['total_traditions']} traditions")
        return self.master_index
    
    def load_tradition(self, tradition_name: str) -> List[Dict[str, Any]]:
        """Load a specific tradition's knowledge entries"""
        if tradition_name not in self.master_index.get('traditions', {}):
            logger.warning(f"Tradition '{tradition_name}' not found in master index")
            return []
            
        tradition_info = self.master_index['traditions'][tradition_name]
        file_path = self.lighthouse_path / tradition_info['file_path'].replace('complete_lighthouse/', '')
        
        if not file_path.exists():
            logger.warning(f"Tradition file not found: {file_path}")
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
                entries = tradition_data.get('entries', [])
                logger.info(f"Loaded {len(entries)} entries for {tradition_name}")
                return entries
        except Exception as e:
            logger.error(f"Error loading tradition {tradition_name}: {e}")
            return []
    
    def load_all_traditions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load all tradition knowledge bases"""
        if not self.master_index:
            self.load_master_index()
            
        for tradition_name in self.master_index['traditions'].keys():
            self.knowledge_base[tradition_name] = self.load_tradition(tradition_name)
            
        total_entries = sum(len(entries) for entries in self.knowledge_base.values())
        logger.info(f"Loaded complete knowledge base: {total_entries} total entries")
        return self.knowledge_base
    
    def get_relevant_knowledge(self, knowledge_systems: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """Get knowledge entries relevant to a governor's knowledge systems"""
        relevant_knowledge = {}
        
        for category, system in knowledge_systems.items():
            # Map governor knowledge systems to lighthouse traditions
            tradition_mapping = {
                'hermetic_magic': 'hermetic_qabalah',
                'enochian_magic': 'enochian_magic',
                'chaos_magic': 'chaos_magic',
                'golden_dawn': 'golden_dawn',
                'thelemic_magic': 'thelema',
                'geomancy': 'hermetic_qabalah',  # Geomancy is part of hermetic tradition
                'tarot': 'tarot',
                'astrology': 'astrology',
                'i_ching': 'i_ching',
                'stoicism': 'greek_philosophy',
                'platonism': 'greek_philosophy',
                'systems_theory': 'quantum_physics',  # Modern systems thinking
                'quantum_physics': 'quantum_physics',
                'sacred_geometry': 'sacred_geometry',
                'numerology': 'numerology',
                'shamanism': 'shamanism',
                'sufism': 'sufism',
                'gnosticism': 'gnosticism',
                'norse_traditions': 'norse_traditions',
                'egyptian_magic': 'egyptian_magic',
                'celtic_druidic': 'celtic_druidic',
                'kuji_kiri': 'kuji_kiri',
                'taoism': 'taoism',
                'digital_physics': 'digital_physics',
                'm_theory': 'm_theory',
                'natal_astrology': 'natal_astrology'
            }
            
            tradition_name = tradition_mapping.get(system, system)
            if tradition_name in self.knowledge_base:
                relevant_knowledge[tradition_name] = self.knowledge_base[tradition_name]
                logger.debug(f"Mapped {system} -> {tradition_name}: {len(self.knowledge_base[tradition_name])} entries")
            else:
                logger.warning(f"No lighthouse tradition found for {system}")
                
        return relevant_knowledge

class GovernorProfileLoader:
    """Loads and processes governor profiles"""
    
    def __init__(self, profiles_path: str = "governor_profiles"):
        self.profiles_path = Path(profiles_path)
        self.profiles = {}
        
    def load_all_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load all 91 governor profiles"""
        profile_files = list(self.profiles_path.glob("*_complete_interview.json"))
        
        if len(profile_files) != 91:
            logger.warning(f"Expected 91 governor profiles, found {len(profile_files)}")
            
        for profile_file in profile_files:
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    governor_name = profile_data['governor_name']
                    self.profiles[governor_name] = profile_data
                    logger.debug(f"Loaded profile for {governor_name}")
            except Exception as e:
                logger.error(f"Error loading profile {profile_file}: {e}")
                
        logger.info(f"Loaded {len(self.profiles)} governor profiles")
        return self.profiles
    
    def get_profile(self, governor_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific governor's profile"""
        return self.profiles.get(governor_name)

class GovernorAIEmbodiment:
    """Creates AI embodiments of governors with full knowledge integration"""
    
    def __init__(self, lighthouse_loader: LighthouseLoader, profile_loader: GovernorProfileLoader):
        self.lighthouse = lighthouse_loader
        self.profiles = profile_loader
        self.embodiments = {}
        
    def create_embodiment(self, governor_name: str) -> Optional[GovernorKnowledge]:
        """Create a complete AI embodiment for a governor"""
        profile = self.profiles.get_profile(governor_name)
        if not profile:
            logger.error(f"No profile found for governor {governor_name}")
            return None
            
        # Extract knowledge systems from profile
        knowledge_systems = profile.get('governor_profile', {}).get('knowledge_base', {})
        if not knowledge_systems:
            logger.warning(f"No knowledge systems found for {governor_name}")
            knowledge_systems = {}
            
        # Get relevant lighthouse knowledge
        lighthouse_knowledge = self.lighthouse.get_relevant_knowledge(knowledge_systems)
        
        # Build personality prompt
        personality_prompt = self._build_personality_prompt(profile)
        
        # Create knowledge summary
        knowledge_summary = self._create_knowledge_summary(lighthouse_knowledge)
        
        embodiment = GovernorKnowledge(
            name=governor_name,
            profile=profile,
            lighthouse_knowledge=lighthouse_knowledge,
            personality_prompt=personality_prompt,
            knowledge_summary=knowledge_summary
        )
        
        self.embodiments[governor_name] = embodiment
        logger.info(f"Created AI embodiment for {governor_name} with {len(lighthouse_knowledge)} knowledge domains")
        return embodiment
    
    def _build_personality_prompt(self, profile: Dict[str, Any]) -> str:
        """Build a comprehensive personality prompt for the governor"""
        gov_profile = profile.get('governor_profile', {})
        
        name = gov_profile.get('name', 'Unknown')
        title = gov_profile.get('title', '')
        essence = gov_profile.get('essence', '')
        aethyr = gov_profile.get('aethyr', '')
        element = gov_profile.get('element', '')
        angelic_role = gov_profile.get('angelic_role', '')
        
        # Extract personality traits
        polar_traits = gov_profile.get('polar_traits', {})
        virtues = polar_traits.get('virtues', [])
        flaws = polar_traits.get('flaws', [])
        approach = polar_traits.get('baseline_approach', '')
        tone = polar_traits.get('baseline_tone', '')
        alignment = polar_traits.get('motive_alignment', '')
        archetype = polar_traits.get('role_archetype', '')
        
        # Extract correspondences
        correspondences = gov_profile.get('archetypal_correspondences', {})
        tarot = correspondences.get('tarot', '')
        sephirot = correspondences.get('sephirot', '')
        zodiac = correspondences.get('zodiac_sign', '')
        
        prompt = f"""You are {name}, {title}, a Governor Angel of the {aethyr} Aethyr.

ESSENCE: {essence}

ANGELIC ROLE: {angelic_role}

ELEMENTAL NATURE: {element}

PERSONALITY MATRIX:
- Primary Approach: {approach}
- Communication Tone: {tone}
- Moral Alignment: {alignment}
- Archetypal Role: {archetype}

VIRTUES: {', '.join(virtues)}
SHADOW ASPECTS: {', '.join(flaws)}

CORRESPONDENCES:
- Tarot: {tarot}
- Sephirot: {sephirot}
- Zodiac: {zodiac}

You embody these qualities completely and speak from this authentic angelic perspective. Your responses should reflect your unique personality, wisdom, and the specific knowledge domains you've mastered. You are both divine messenger and practical guide, offering wisdom that bridges the celestial and terrestrial realms.

When creating quests or interactions, draw upon your specific knowledge base while maintaining your distinctive personality and approach."""

        return prompt
    
    def _create_knowledge_summary(self, lighthouse_knowledge: Dict[str, List[Dict[str, Any]]]) -> str:
        """Create a summary of the governor's knowledge base"""
        if not lighthouse_knowledge:
            return "No specific knowledge domains assigned."
            
        summary_parts = []
        total_entries = 0
        
        for tradition, entries in lighthouse_knowledge.items():
            entry_count = len(entries)
            total_entries += entry_count
            
            # Get sample entry names for context
            sample_names = [entry.get('name', 'Unnamed') for entry in entries[:3]]
            sample_text = ', '.join(sample_names)
            if len(entries) > 3:
                sample_text += f", and {len(entries) - 3} more"
                
            summary_parts.append(f"- {tradition.replace('_', ' ').title()}: {entry_count} entries ({sample_text})")
            
        summary = f"KNOWLEDGE BASE SUMMARY ({total_entries} total entries):\n" + '\n'.join(summary_parts)
        return summary
    
    def create_all_embodiments(self) -> Dict[str, GovernorKnowledge]:
        """Create AI embodiments for all 91 governors"""
        logger.info("Creating AI embodiments for all governors...")
        
        for governor_name in self.profiles.profiles.keys():
            self.create_embodiment(governor_name)
            
        logger.info(f"Created {len(self.embodiments)} governor AI embodiments")
        return self.embodiments
    
    def get_embodiment(self, governor_name: str) -> Optional[GovernorKnowledge]:
        """Get a specific governor's AI embodiment"""
        return self.embodiments.get(governor_name)
    
    def export_embodiments(self, output_path: str = "governor_ai_embodiments.json"):
        """Export all embodiments to JSON for use by other systems"""
        export_data = {}
        
        for name, embodiment in self.embodiments.items():
            export_data[name] = {
                'name': embodiment.name,
                'personality_prompt': embodiment.personality_prompt,
                'knowledge_summary': embodiment.knowledge_summary,
                'knowledge_domains': list(embodiment.lighthouse_knowledge.keys()),
                'total_knowledge_entries': sum(len(entries) for entries in embodiment.lighthouse_knowledge.values()),
                'profile_summary': {
                    'title': embodiment.profile.get('governor_profile', {}).get('title', ''),
                    'aethyr': embodiment.profile.get('governor_profile', {}).get('aethyr', ''),
                    'element': embodiment.profile.get('governor_profile', {}).get('element', ''),
                    'virtues': embodiment.profile.get('governor_profile', {}).get('polar_traits', {}).get('virtues', []),
                    'knowledge_systems': embodiment.profile.get('governor_profile', {}).get('knowledge_base', {})
                }
            }
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Exported {len(export_data)} governor embodiments to {output_path}")

def main():
    """Main function to create the governor AI embodiment system"""
    logger.info("Initializing Enochian Cyphers Governor AI Embodiment System")
    
    # Initialize loaders
    lighthouse_loader = LighthouseLoader()
    profile_loader = GovernorProfileLoader()
    
    # Load data
    logger.info("Loading lighthouse knowledge base...")
    lighthouse_loader.load_all_traditions()
    
    logger.info("Loading governor profiles...")
    profile_loader.load_all_profiles()
    
    # Create AI embodiment system
    embodiment_system = GovernorAIEmbodiment(lighthouse_loader, profile_loader)
    
    # Create all embodiments
    embodiments = embodiment_system.create_all_embodiments()
    
    # Export for use by other systems
    embodiment_system.export_embodiments()
    
    # Display summary
    logger.info(f"\n=== GOVERNOR AI EMBODIMENT SYSTEM READY ===")
    logger.info(f"Total Governors: {len(embodiments)}")
    logger.info(f"Total Knowledge Entries: {sum(len(emb.lighthouse_knowledge) for emb in embodiments.values())}")
    
    # Show sample embodiment
    if embodiments:
        sample_name = list(embodiments.keys())[0]
        sample = embodiments[sample_name]
        logger.info(f"\nSample Embodiment - {sample_name}:")
        logger.info(f"Knowledge Domains: {list(sample.lighthouse_knowledge.keys())}")
        logger.info(f"Total Knowledge Entries: {sum(len(entries) for entries in sample.lighthouse_knowledge.values())}")
    
    return embodiment_system

if __name__ == "__main__":
    main()
