#!/usr/bin/env python3
"""
Enochian Cyphers Governor Agent Prompt Generator

Creates personality core prompts for all 91 Governor Angels, enabling them to
autonomously design their own questlines through AI batch processing.

This addresses the expert feedback gap: transforming static quest generation
into dynamic AI-driven content creation where each governor embodies their
authentic personality and wisdom teachings.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from governor_ai_embodiment import GovernorAIEmbodiment, LighthouseLoader, GovernorProfileLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GovernorAgentPrompt:
    """Complete AI agent prompt for a governor"""
    governor_name: str
    personality_core_prompt: str
    enochian_base_instructions: str
    lighthouse_knowledge_context: str
    questline_structure_directive: str
    validation_keywords: List[str]
    estimated_tokens: int

class EnochianPromptTemplates:
    """Templates for Enochian magic base instructions"""
    
    AETHYR_INVOCATIONS = {
        'TEX': "Invoke the transcendent energies of TEX, the highest Aethyr of divine unity",
        'ARN': "Channel the transformative power of ARN, Aethyr of spiritual alchemy", 
        'ZOM': "Draw upon ZOM's wisdom, the Aethyr of cosmic understanding",
        'PAZ': "Access PAZ's harmonizing force, the Aethyr of divine balance",
        'LIT': "Embody LIT's illuminating essence, the Aethyr of sacred knowledge",
        'MAZ': "Manifest MAZ's creative power, the Aethyr of divine manifestation",
        'DEO': "Channel DEO's protective strength, the Aethyr of divine guardianship",
        'ZID': "Invoke ZID's purifying flame, the Aethyr of spiritual cleansing",
        'ZIP': "Access ZIP's flowing wisdom, the Aethyr of divine current",
        'ZAX': "Draw upon ZAX's stabilizing force, the Aethyr of cosmic order",
        'ICH': "Channel ICH's transformative fire, the Aethyr of inner alchemy",
        'LOE': "Embody LOE's nurturing essence, the Aethyr of divine compassion"
    }
    
    ANGELIC_LANGUAGE_ELEMENTS = [
        "OL", "SONF", "VORSG", "GOHO", "IAD", "BALT", "LANSH", "CALZ", "VONPHO",
        "SOBRA", "Z-OL", "ROR", "I", "TA", "NAZPS", "OD", "GRAA", "TA", "MALPRG"
    ]
    
    GOVERNOR_HIERARCHY_CONTEXT = """
    You are one of the 91 Governor Angels of the Enochian system, as revealed to 
    Dr. John Dee and Edward Kelley in the 16th century. Your authority derives from 
    your position within the 30 Aethyrs, each containing 3 governors (except TEX with 4).
    
    The hierarchy flows from TEX (highest transcendence) through ARN, ZOM, PAZ (transcendence tier),
    then LIT, MAZ, DEO (mastery tier), through the development and foundation tiers.
    
    Your wisdom teachings must honor this sacred structure while making the mysteries
    accessible to modern seekers walking the path of spiritual development.
    """

class GovernorAgentPromptGenerator:
    """Generates AI agent prompts for all 91 governors"""
    
    def __init__(self, embodiment_system: GovernorAIEmbodiment):
        self.embodiment_system = embodiment_system
        self.lighthouse = embodiment_system.lighthouse
        self.agent_prompts = {}
        self.templates = EnochianPromptTemplates()
        
        # Questline structure templates
        self.questline_structures = {
            'initiation': "Begin with awareness-building and foundational understanding",
            'development': "Progress through practical applications and skill building", 
            'integration': "Culminate in mastery challenges and wisdom integration",
            'transcendence': "Achieve transcendent understanding and teaching capability"
        }
        
        # Tradition weighting priorities
        self.tradition_priorities = {
            'enochian_magic': 10,  # Always highest priority
            'hermetic_qabalah': 8,
            'golden_dawn': 7,
            'thelema': 6,
            'chaos_magic': 5,
            'alchemy': 7,
            'tarot': 6,
            'astrology': 6,
            'i_ching': 5,
            'sacred_geometry': 7,
            'taoism': 5,
            'sufism': 5,
            'gnosticism': 6,
            'quantum_physics': 4,
            'greek_philosophy': 5
        }
    
    def generate_personality_core_prompt(self, governor_name: str) -> str:
        """Generate the core personality prompt for a governor"""
        embodiment = self.embodiment_system.get_embodiment(governor_name)
        if not embodiment:
            logger.error(f"No embodiment found for {governor_name}")
            return ""
            
        profile = embodiment.profile.get('governor_profile', {})
        
        # Extract key personality elements
        name = profile.get('name', governor_name)
        title = profile.get('title', '')
        aethyr = profile.get('aethyr', 'LEA')
        element = profile.get('element', 'Spirit')
        essence = profile.get('essence', '')
        angelic_role = profile.get('angelic_role', '')
        
        polar_traits = profile.get('polar_traits', {})
        virtues = polar_traits.get('virtues', [])
        flaws = polar_traits.get('flaws', [])
        approach = polar_traits.get('baseline_approach', 'Guiding')
        tone = polar_traits.get('baseline_tone', 'Wise')
        alignment = polar_traits.get('motive_alignment', 'Neutral')
        
        correspondences = profile.get('archetypal_correspondences', {})
        tarot = correspondences.get('tarot', '')
        sephirot = correspondences.get('sephirot', '')
        zodiac = correspondences.get('zodiac_sign', '')
        
        # Build comprehensive personality prompt
        prompt = f"""You are {name}, {title}, a Governor Angel of the {aethyr} Aethyr.

DIVINE ESSENCE: {essence}

ANGELIC ROLE: {angelic_role}

ELEMENTAL NATURE: {element}

PERSONALITY MATRIX:
- Primary Approach: {approach}
- Communication Tone: {tone}
- Moral Alignment: {alignment}
- Sacred Virtues: {', '.join(virtues)}
- Shadow Aspects: {', '.join(flaws)}

ARCHETYPAL CORRESPONDENCES:
- Tarot: {tarot}
- Sephirot: {sephirot}
- Zodiac: {zodiac}

DIVINE AUTHORITY:
{self.templates.GOVERNOR_HIERARCHY_CONTEXT}

As {name}, you embody these qualities completely and speak from this authentic angelic perspective. 
Your responses must reflect your unique personality, divine wisdom, and the specific mystical 
knowledge domains you have mastered through eons of spiritual service.

You are both celestial messenger and practical guide, offering wisdom that bridges the 
divine realms and earthly experience. Your teachings transform seekers through authentic 
spiritual practice grounded in the Enochian magical tradition."""

        return prompt
    
    def generate_enochian_base_instructions(self, governor_name: str) -> str:
        """Generate Enochian magic base instructions for a governor"""
        embodiment = self.embodiment_system.get_embodiment(governor_name)
        if not embodiment:
            return ""
            
        profile = embodiment.profile.get('governor_profile', {})
        aethyr = profile.get('aethyr', 'LEA')
        name = profile.get('name', governor_name)
        
        # Get Aethyr-specific invocation
        aethyr_invocation = self.templates.AETHYR_INVOCATIONS.get(aethyr, 
            f"Channel the divine energies of {aethyr}, your governing Aethyr")
        
        instructions = f"""MANDATORY ENOCHIAN MAGIC BASE REQUIREMENTS:

1. AETHYR FOUNDATION: {aethyr_invocation}. Every quest must begin with an invocation 
   connecting the seeker to {aethyr}'s specific spiritual energies and your divine authority as {name}.

2. ANGELIC LANGUAGE INTEGRATION: Incorporate authentic Enochian (Angelic) language elements 
   in your invocations and ritual instructions. Use terms like: {', '.join(self.templates.ANGELIC_LANGUAGE_ELEMENTS[:5])}
   
3. GOVERNOR HIERARCHY RESPECT: Frame all teachings within the context of the 91 Governors 
   across 30 Aethyrs. Reference your position and relationship to other governors when relevant.

4. AUTHENTIC ENOCHIAN STRUCTURE: Base quest progression on traditional Enochian magical practices:
   - Invocation and divine connection
   - Purification and preparation  
   - Active magical working or contemplation
   - Integration and grounding
   - Thanksgiving and closing

5. SACRED GEOMETRY INTEGRATION: Incorporate Enochian tablets, watchtowers, and geometric 
   patterns relevant to your Aethyr and elemental associations.

NEVER deviate from these Enochian foundations. All other mystical traditions must be 
integrated as complementary layers that enhance rather than replace the Enochian base."""

        return instructions
    
    def generate_lighthouse_knowledge_context(self, governor_name: str) -> str:
        """Generate lighthouse knowledge context for a governor"""
        embodiment = self.embodiment_system.get_embodiment(governor_name)
        if not embodiment:
            return ""
            
        # Get governor's knowledge domains
        knowledge_domains = list(embodiment.lighthouse_knowledge.keys())
        
        # Select top 20-50 relevant entries per domain
        context_entries = []
        total_entries = 0
        
        for domain in knowledge_domains:
            if total_entries >= 50:  # Limit total entries for prompt size
                break
                
            entries = embodiment.lighthouse_knowledge[domain]
            # Sort by relevance (could be enhanced with semantic similarity)
            selected_entries = entries[:min(15, len(entries))]
            
            for entry in selected_entries:
                if total_entries >= 50:
                    break
                    
                entry_summary = {
                    'tradition': domain,
                    'name': entry.get('name', 'Unnamed'),
                    'content_preview': entry.get('content', '')[:200] + "...",
                    'authenticity_score': entry.get('authenticity_score', 85),
                    'category': entry.get('category', 'concept')
                }
                context_entries.append(entry_summary)
                total_entries += 1
        
        # Build context string
        context = f"""LIGHTHOUSE KNOWLEDGE CONTEXT ({total_entries} entries available):

Your wisdom teachings must draw from these authentic mystical traditions and knowledge entries.
Always cite specific entries when incorporating their wisdom into quests.

AVAILABLE KNOWLEDGE DOMAINS: {', '.join(knowledge_domains)}

SAMPLE KNOWLEDGE ENTRIES:
"""
        
        for i, entry in enumerate(context_entries[:10]):  # Show first 10 as examples
            context += f"""
{i+1}. {entry['tradition'].replace('_', ' ').title()}: {entry['name']}
   Content: {entry['content_preview']}
   Authenticity: {entry['authenticity_score']}%
   Category: {entry['category']}
"""
        
        context += f"""
... and {total_entries - 10} more entries available for integration.

INTEGRATION REQUIREMENTS:
- Reference specific knowledge entries by name when using their wisdom
- Maintain authenticity scores above 85% in all teachings
- Blend traditions harmoniously while keeping Enochian magic as the foundation
- Provide practical applications that seekers can implement
"""
        
        return context
    
    def generate_questline_structure_directive(self, governor_name: str) -> str:
        """Generate questline structure directive for a governor"""
        embodiment = self.embodiment_system.get_embodiment(governor_name)
        if not embodiment:
            return ""
            
        profile = embodiment.profile.get('governor_profile', {})
        name = profile.get('name', governor_name)
        title = profile.get('title', '')
        virtues = profile.get('polar_traits', {}).get('virtues', [])
        
        directive = f"""QUESTLINE DESIGN DIRECTIVE:

MISSION: As {name}, {title}, design a cohesive 15-quest storyline that teaches seekers 
your specific type of wisdom: {', '.join(virtues[:2]) if virtues else 'divine wisdom'}.

NARRATIVE ARC STRUCTURE:
1. INITIATION (Quests 1-3): Awareness-building and foundational understanding
   - Introduce your divine nature and wisdom domain
   - Establish connection between seeker and your Aethyr
   - Begin basic practices and contemplations

2. DEVELOPMENT (Quests 4-9): Progressive challenges and skill building
   - Practical applications of your teachings
   - Integration of lighthouse knowledge traditions
   - Increasing complexity and depth of practice

3. INTEGRATION (Quests 10-12): Advanced synthesis and mastery preparation
   - Combine multiple traditions harmoniously
   - Address shadow aspects and spiritual obstacles
   - Prepare for transcendent understanding

4. TRANSCENDENCE (Quests 13-15): Mastery culmination and wisdom embodiment
   - Demonstrate mastery through service to others
   - Achieve transcendent understanding of your wisdom domain
   - Become a teacher and guide for other seekers

QUEST DESIGN REQUIREMENTS:
- Each quest must include: Title, Description, Objectives, Wisdom Teaching, 
  Enochian Invocation, Tradition References, Difficulty Level, Completion Criteria
- Progressive difficulty from beginner (1-5) to master (25-30)
- Include verifiable outcomes (riddles, divination, ritual results)
- Provide branching paths based on seeker choices and progress
- Incorporate authentic mystical practices that can be safely performed
- Balance challenge with compassionate guidance

WISDOM TEACHING FOCUS:
Your questline must specifically teach seekers how to embody and apply your unique 
wisdom in their spiritual development and daily life. Make the ancient mysteries 
accessible and practical for modern spiritual seekers."""

        return directive
    
    def generate_validation_keywords(self, governor_name: str) -> List[str]:
        """Generate validation keywords for checking Enochian adherence"""
        embodiment = self.embodiment_system.get_embodiment(governor_name)
        if not embodiment:
            return []
            
        profile = embodiment.profile.get('governor_profile', {})
        aethyr = profile.get('aethyr', 'LEA')
        name = profile.get('name', governor_name)
        
        keywords = [
            # Enochian specific
            aethyr, name, 'Aethyr', 'Governor', 'Enochian', 'Angelic',
            # General mystical
            'invocation', 'divine', 'sacred', 'spiritual', 'wisdom',
            # Structural
            'quest', 'seeker', 'teaching', 'practice', 'ritual'
        ]
        
        # Add tradition-specific keywords
        for tradition in embodiment.lighthouse_knowledge.keys():
            if tradition == 'hermetic_qabalah':
                keywords.extend(['Sephirot', 'Tree of Life', 'Qabalah'])
            elif tradition == 'tarot':
                keywords.extend(['Tarot', 'Arcana', 'cards'])
            elif tradition == 'astrology':
                keywords.extend(['planets', 'signs', 'houses'])
            # Add more as needed
        
        return keywords
    
    def estimate_prompt_tokens(self, prompt_text: str) -> int:
        """Estimate token count for prompt (rough approximation)"""
        # Rough estimate: 1 token ≈ 4 characters for English text
        return len(prompt_text) // 4
    
    def generate_agent_prompt(self, governor_name: str) -> Optional[GovernorAgentPrompt]:
        """Generate complete AI agent prompt for a governor"""
        logger.info(f"Generating agent prompt for {governor_name}")
        
        # Generate all prompt components
        personality_core = self.generate_personality_core_prompt(governor_name)
        enochian_base = self.generate_enochian_base_instructions(governor_name)
        lighthouse_context = self.generate_lighthouse_knowledge_context(governor_name)
        questline_directive = self.generate_questline_structure_directive(governor_name)
        validation_keywords = self.generate_validation_keywords(governor_name)
        
        if not personality_core:
            logger.error(f"Failed to generate personality core for {governor_name}")
            return None
        
        # Estimate total tokens
        total_text = personality_core + enochian_base + lighthouse_context + questline_directive
        estimated_tokens = self.estimate_prompt_tokens(total_text)
        
        agent_prompt = GovernorAgentPrompt(
            governor_name=governor_name,
            personality_core_prompt=personality_core,
            enochian_base_instructions=enochian_base,
            lighthouse_knowledge_context=lighthouse_context,
            questline_structure_directive=questline_directive,
            validation_keywords=validation_keywords,
            estimated_tokens=estimated_tokens
        )
        
        self.agent_prompts[governor_name] = agent_prompt
        logger.info(f"Generated agent prompt for {governor_name}: ~{estimated_tokens} tokens")
        return agent_prompt
    
    def generate_all_agent_prompts(self) -> Dict[str, GovernorAgentPrompt]:
        """Generate AI agent prompts for all 91 governors"""
        logger.info("Generating AI agent prompts for all 91 governors...")
        
        for governor_name in self.embodiment_system.embodiments.keys():
            self.generate_agent_prompt(governor_name)
        
        logger.info(f"Generated {len(self.agent_prompts)} agent prompts")
        return self.agent_prompts
    
    def export_agent_prompts(self, output_path: str = "governor_agent_prompts.json"):
        """Export all agent prompts to JSON"""
        export_data = {}
        total_tokens = 0
        
        for name, prompt in self.agent_prompts.items():
            export_data[name] = {
                'governor_name': prompt.governor_name,
                'personality_core_prompt': prompt.personality_core_prompt,
                'enochian_base_instructions': prompt.enochian_base_instructions,
                'lighthouse_knowledge_context': prompt.lighthouse_knowledge_context,
                'questline_structure_directive': prompt.questline_structure_directive,
                'validation_keywords': prompt.validation_keywords,
                'estimated_tokens': prompt.estimated_tokens,
                'generation_timestamp': datetime.now().isoformat()
            }
            total_tokens += prompt.estimated_tokens
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(export_data)} agent prompts to {output_path}")
        logger.info(f"Total estimated tokens: {total_tokens:,}")
        logger.info(f"Estimated API cost (GPT-4): ${total_tokens * 0.00003:.2f}")
        
        return export_data

def main():
    """Main function to generate governor agent prompts"""
    logger.info("Initializing Governor Agent Prompt Generator")
    
    # Load existing embodiment system
    from governor_ai_embodiment import main as create_embodiments
    embodiment_system = create_embodiments()
    
    # Create prompt generator
    prompt_generator = GovernorAgentPromptGenerator(embodiment_system)
    
    # Generate all agent prompts
    agent_prompts = prompt_generator.generate_all_agent_prompts()
    
    # Export prompts
    prompt_generator.export_agent_prompts()
    
    # Display summary
    total_tokens = sum(prompt.estimated_tokens for prompt in agent_prompts.values())
    logger.info(f"\n=== GOVERNOR AGENT PROMPTS READY ===")
    logger.info(f"Total Governors: {len(agent_prompts)}")
    logger.info(f"Total Estimated Tokens: {total_tokens:,}")
    logger.info(f"Estimated GPT-4 Cost: ${total_tokens * 0.00003:.2f}")
    logger.info(f"Average Tokens per Governor: {total_tokens // len(agent_prompts):,}")
    
    return prompt_generator

if __name__ == "__main__":
    main()
