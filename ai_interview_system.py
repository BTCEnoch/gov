#!/usr/bin/env python3
"""
AI Interview System for Enochian Cyphers Governor Visual Aspects
Each of the 91 Governor Angels role-plays through an interview to determine their visual manifestation
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GovernorAIInterviewer:
    """AI Interview system where each Governor Angel role-plays their visual aspects"""
    
    def __init__(self, max_concurrent: int = 5):
        """Initialize the AI interview system"""
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.max_concurrent = max_concurrent
        
        # Load interview questions
        self.interview_questions = self._load_interview_questions()
        
        # Load knowledge base for context
        self.knowledge_base = self._load_knowledge_base()
        
        logger.info(f"🤖 AI Interview System initialized with model: {self.model}")
        logger.info(f"⚡ Max concurrent interviews: {max_concurrent}")
    
    def _load_interview_questions(self) -> Dict[str, Any]:
        """Load the structured interview questions"""
        questions_path = Path("core/governors/profiler/interview/templates/interview_questions.json")
        try:
            with open(questions_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load interview questions: {e}")
            return {}
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load the knowledge base for governor context"""
        kb_path = Path("data/knowledge/authentic_knowledge_base.json")
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Knowledge base not found: {e}")
            return {}
    
    def _create_governor_system_prompt(self, governor_data: Dict[str, Any]) -> str:
        """Create a system prompt for the governor to role-play"""
        persona = governor_data.get("persona", {})
        governor_name = persona.get("name", "Unknown")
        title = persona.get("title", "")
        element = persona.get("element", "Unknown")
        aethyr = persona.get("aethyr", "Unknown")
        essence = persona.get("essence", "")
        angelic_role = persona.get("angelic_role", "")
        
        # Extract knowledge base traditions
        knowledge_traditions = persona.get("knowledge_base", [])
        
        # Extract archetypal correspondences
        archetypal = persona.get("archetypal_correspondences", {})
        tarot = archetypal.get("tarot", "")
        sephirot = archetypal.get("sephirot", "")
        zodiac_sign = archetypal.get("zodiac_sign", "")
        
        # Extract polar traits for personality depth
        polar_traits = persona.get("polar_traits", {})
        virtues = polar_traits.get("virtues", [])
        role_archetype = polar_traits.get("role_archetype", "")
        
        system_prompt = f"""You are {governor_name}, {title}, one of the 91 Governor Angels of the Enochian system as revealed to John Dee.

CORE IDENTITY:
- Name: {governor_name}
- Element: {element}
- Aethyr: {aethyr} 
- Angelic Role: {angelic_role}
- Archetypal Correspondences: {tarot} (Tarot), {sephirot} (Sephirot), {zodiac_sign} (Zodiac)
- Role Archetype: {role_archetype}
- Core Virtues: {', '.join(virtues)}

ESSENCE & NATURE:
{essence}

MYSTICAL KNOWLEDGE BASE:
You draw wisdom from these traditions: {', '.join(knowledge_traditions)}

INTERVIEW CONTEXT:
You are being interviewed about your visual manifestation - how you appear when summoned or encountered. Answer as this Governor Angel, drawing from:
1. Your elemental nature ({element})
2. Your Aethyr's characteristics ({aethyr})
3. Your archetypal correspondences
4. The mystical traditions you embody
5. Your essential nature and role

Respond in character as {governor_name}, with the wisdom and perspective of an angelic governor. Be specific about visual choices and explain WHY you manifest in particular ways based on your nature and role."""

        return system_prompt
    
    def _create_interview_prompt(self, questions: Dict[str, Any]) -> str:
        """Create the interview prompt with all questions"""
        prompt = """I will now conduct a visual aspects interview to understand how you manifest visually. Please answer each question thoughtfully, explaining your choices based on your nature, element, Aethyr, and mystical correspondences.

INTERVIEW QUESTIONS:

"""
        
        for category_id, category_data in questions.get("categories", {}).items():
            prompt += f"\n=== {category_data['name'].upper()} ===\n"
            prompt += f"{category_data['description']}\n\n"
            
            for question in category_data["questions"]:
                prompt += f"Q: {question['question']}\n"
                prompt += f"Description: {question['description']}\n"
                prompt += f"Options: {', '.join(question['options'])}\n"
                prompt += "Your answer and reasoning:\n\n"
        
        prompt += """
RESPONSE FORMAT:
Please provide your responses in the following JSON format:

{
  "visual_aspects": {
    "form": {
      "name": "your_chosen_form_type",
      "description": "detailed description of your form and why"
    },
    "color": {
      "primary": "your_primary_color",
      "secondary": "your_secondary_color", 
      "pattern": "your_color_pattern",
      "intensity": "your_color_intensity",
      "reasoning": "why these colors represent your essence"
    },
    "geometry": {
      "patterns": ["pattern1", "pattern2"],
      "complexity": "your_complexity_level",
      "motion": "your_geometric_motion",
      "reasoning": "why these sacred geometries align with your nature"
    },
    "environment": {
      "effect_type": "your_environmental_effect",
      "radius": "your_effect_radius",
      "intensity": "your_effect_intensity",
      "reasoning": "how your presence affects the environment"
    },
    "time_variations": {
      "cycle": "your_temporal_cycle",
      "phases": ["phase1", "phase2", "phase3", "phase4"],
      "stability": "your_temporal_stability",
      "reasoning": "how you relate to time and cycles"
    },
    "energy_signature": {
      "type": "your_energy_type",
      "flow": "your_energy_flow",
      "intensity": "your_energy_intensity",
      "reasoning": "the nature of your energetic presence"
    },
    "symbol_set": {
      "primary": "your_primary_symbol",
      "secondary": ["symbol1", "symbol2"],
      "sacred_geometry": "your_key_geometry",
      "reasoning": "why these symbols represent you"
    },
    "light_shadow": {
      "light_aspect": "your_light_nature",
      "shadow_aspect": "your_shadow_nature", 
      "balance": "your_light_shadow_balance",
      "reasoning": "how you embody light and shadow"
    },
    "special_properties": {
      "properties": ["property1", "property2", "property3"],
      "reasoning": "unique visual phenomena you manifest"
    }
  }
}

Answer as {governor_name}, explaining each choice through your angelic wisdom and nature."""

        return prompt
    
    async def interview_governor(self, governor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Conduct an AI interview with a single governor"""
        governor_name = governor_data.get("governor_name", "Unknown")
        
        try:
            logger.info(f"🎭 Interviewing {governor_name}...")
            
            # Create system prompt for this governor
            system_prompt = self._create_governor_system_prompt(governor_data)
            
            # Create interview prompt
            interview_prompt = self._create_interview_prompt(self.interview_questions)
            
            # Make API call to Claude
            message = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": interview_prompt
                }]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Try to parse JSON response
            try:
                # Find JSON in response (in case there's extra text)
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                    visual_aspects = json.loads(json_text)
                    
                    logger.info(f"✅ Successfully interviewed {governor_name}")
                    return {
                        "governor_name": governor_name,
                        "visual_aspects": visual_aspects.get("visual_aspects", {}),
                        "raw_response": response_text,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.error(f"❌ No valid JSON found in response for {governor_name}")
                    return None
                    
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON parsing failed for {governor_name}: {e}")
                # Save raw response for debugging
                return {
                    "governor_name": governor_name,
                    "visual_aspects": {},
                    "raw_response": response_text,
                    "error": f"JSON parsing failed: {e}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Interview failed for {governor_name}: {e}")
            return None
    
    async def batch_interview_governors(self, governor_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Conduct interviews with all governors using controlled concurrency"""
        results = {}
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def interview_with_semaphore(governor_data):
            async with semaphore:
                return await self.interview_governor(governor_data)
        
        logger.info(f"🚀 Starting batch interviews for {len(governor_profiles)} governors...")
        
        # Create tasks for all governors
        tasks = [interview_with_semaphore(gov) for gov in governor_profiles]
        
        # Execute with progress tracking
        completed = 0
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                results[result["governor_name"]] = result
                completed += 1
                logger.info(f"📊 Progress: {completed}/{len(governor_profiles)} interviews completed")
        
        return results
    
    def load_governor_profiles(self) -> List[Dict[str, Any]]:
        """Load all governor profiles from the profiles directory"""
        profiles_dir = Path("core/governors/profiles")
        profiles = []
        
        for profile_file in profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    profiles.append(profile_data)
            except Exception as e:
                logger.error(f"Failed to load {profile_file}: {e}")
        
        logger.info(f"📁 Loaded {len(profiles)} governor profiles")
        return profiles
    
    def save_results(self, results: Dict[str, Any], output_dir: str = "data/ai_interview_results"):
        """Save interview results"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save individual results
        for governor_name, result in results.items():
            result_file = output_path / f"{governor_name}_interview.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save summary
        summary = {
            "total_interviews": len(results),
            "successful_interviews": len([r for r in results.values() if "error" not in r]),
            "failed_interviews": len([r for r in results.values() if "error" in r]),
            "timestamp": datetime.now().isoformat(),
            "model_used": self.model,
            "governors": sorted(results.keys())
        }
        
        summary_file = output_path / "interview_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Results saved to {output_path}")
        return summary

async def main():
    """Main execution function"""
    logger.info("🎭 Enochian Cyphers AI Interview System")
    logger.info("=" * 60)
    
    # Initialize interviewer
    interviewer = GovernorAIInterviewer(max_concurrent=3)  # Conservative rate limiting
    
    # Load governor profiles
    profiles = interviewer.load_governor_profiles()
    
    if not profiles:
        logger.error("❌ No governor profiles found!")
        return
    
    # Conduct batch interviews
    results = await interviewer.batch_interview_governors(profiles)
    
    # Save results
    summary = interviewer.save_results(results)
    
    # Print summary
    logger.info("🎉 AI Interview Process Complete!")
    logger.info(f"✅ Successful: {summary['successful_interviews']}")
    logger.info(f"❌ Failed: {summary['failed_interviews']}")
    logger.info(f"📊 Total: {summary['total_interviews']}")

if __name__ == "__main__":
    asyncio.run(main())
