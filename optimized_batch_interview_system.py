#!/usr/bin/env python3
"""
Optimized Batch Interview System for Enochian Cyphers
Uses Anthropic Message Batches API for 50% cost reduction and async processing
Implements prompt caching and token optimization for maximum efficiency
"""

import asyncio
import json
import os
import time
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

class OptimizedBatchInterviewer:
    """Optimized batch interview system using Anthropic's Message Batches API"""
    
    def __init__(self, use_haiku: bool = True):
        """Initialize the optimized batch interviewer"""
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # Use cheapest model for cost optimization
        self.model = "claude-3-5-haiku-20241022" if use_haiku else "claude-3-5-sonnet-20241022"
        
        # Load governor data and knowledge base
        self.governors = self._load_governors()
        self.knowledge_base = self._load_knowledge_base()
        
        # Create shared cached knowledge block for prompt caching
        self.shared_knowledge_cache = self._create_shared_knowledge_cache()
        
        logger.info(f"🚀 Optimized Batch Interviewer initialized")
        logger.info(f"🤖 Model: {self.model}")
        logger.info(f"👥 Governors loaded: {len(self.governors)}")
        logger.info(f"📚 Knowledge base traditions: {len(self.knowledge_base)}")
    
    def _load_governors(self) -> List[Dict[str, Any]]:
        """Load governor profiles from the profiles directory"""
        profiles_dir = Path("core/governors/profiles")
        governors = []
        
        for profile_file in sorted(profiles_dir.glob("*.json")):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    
                    # Extract key data for batch processing
                    persona = profile_data.get("persona", {})
                    governor_data = {
                        "id": len(governors) + 1,  # Sequential ID for custom_id
                        "name": persona.get("name", profile_file.stem),
                        "title": persona.get("title", ""),
                        "element": persona.get("element", "Unknown"),
                        "aethyr": persona.get("aethyr", "Unknown"),
                        "essence": persona.get("essence", ""),
                        "angelic_role": persona.get("angelic_role", ""),
                        "knowledge_base": persona.get("knowledge_base", []),
                        "archetypal_correspondences": persona.get("archetypal_correspondences", {}),
                        "polar_traits": persona.get("polar_traits", {}),
                        "profile_file": profile_file.name
                    }
                    governors.append(governor_data)
                    
            except Exception as e:
                logger.error(f"Failed to load {profile_file}: {e}")
        
        return governors
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base for context"""
        kb_path = Path("data/knowledge/authentic_knowledge_base.json")
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Knowledge base not found: {e}")
            return {}
    
    def _create_shared_knowledge_cache(self) -> Dict[str, Any]:
        """Create shared knowledge block for prompt caching optimization"""
        # Condensed knowledge from 18 traditions for caching
        knowledge_summary = """MYSTICAL TRADITIONS KNOWLEDGE BASE:

1. ENOCHIAN MAGIC: 91 Governor Angels across 30 Aethyrs, revealed to John Dee. Sigils, angelic hierarchies, elemental correspondences.

2. HERMETIC QABALAH: Tree of Life with 10 Sephiroth, 22 paths. Divine emanations, spiritual ascent, archetypal psychology.

3. GOLDEN DAWN: Elemental grades, ritual magic, synthesis of Western esoteric traditions. Color correspondences, ceremonial structure.

4. TAROT: 78 cards (22 Major Arcana, 56 Minor). Archetypal journey, divination, psychological symbolism.

5. SACRED GEOMETRY: Flower of Life, Merkaba, Metatron's Cube, Sri Yantra, Torus, Vesica Piscis. Mathematical harmony in creation.

6. THELEMA: Will as fundamental force, True Self discovery, Aeon of Horus. "Do what thou wilt shall be the whole of the Law."

7. CHAOS MAGIC: Paradigm shifting, belief as tool, sigil magic. Practical results over dogma.

8. NORSE MYTHOLOGY: Runes, Nine Worlds, Odin's wisdom. Warrior spirituality, fate and honor.

9. EGYPTIAN MAGIC: Neteru (gods), Ma'at (cosmic order), afterlife journey. Hieroglyphic symbolism, temple mysteries.

10. GNOSTICISM: Divine spark within, escape from material illusion, Sophia wisdom. Light vs. darkness dualism.

11. I CHING: 64 hexagrams, Yin-Yang balance, change patterns. Ancient Chinese wisdom, divination system.

12. SUFISM: Divine love, whirling meditation, unity with Allah. Mystical Islam, heart-centered spirituality.

13. HINDUISM: Chakras, mantras, yoga paths, karma. Dharma, moksha, cyclical time, divine avatars.

14. BUDDHISM: Four Noble Truths, Eightfold Path, emptiness. Compassion, mindfulness, liberation from suffering.

15. TAOISM: Wu wei (effortless action), Tao (the Way), balance. Natural harmony, simplicity, spontaneity.

16. ALCHEMY: Transmutation, solve et coagula, philosopher's stone. Inner transformation, spiritual gold.

17. ASTROLOGY: Planetary influences, zodiacal archetypes, cosmic timing. As above, so below principle.

18. QUANTUM MYSTICISM: Consciousness-reality interaction, observer effect, non-locality. Modern physics meets ancient wisdom."""

        return {
            "type": "text",
            "text": knowledge_summary,
            "cache_control": {"type": "ephemeral"}
        }
    
    def _create_governor_system_prompt(self, governor: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create optimized system prompt with caching for a governor"""
        
        # Extract governor details
        name = governor["name"]
        title = governor.get("title", "")
        element = governor["element"]
        aethyr = governor["aethyr"]
        essence = governor["essence"]
        angelic_role = governor["angelic_role"]
        
        # Archetypal correspondences
        archetypal = governor.get("archetypal_correspondences", {})
        tarot = archetypal.get("tarot", "")
        sephirot = archetypal.get("sephirot", "")
        zodiac = archetypal.get("zodiac_sign", "")
        
        # Polar traits
        polar = governor.get("polar_traits", {})
        virtues = polar.get("virtues", [])
        role_archetype = polar.get("role_archetype", "")
        
        # Governor-specific prompt (not cached)
        governor_prompt = {
            "type": "text", 
            "text": f"""You are {name}, {title}, Governor Angel #{governor['id']} of the Enochian system.

CORE IDENTITY:
- Element: {element}
- Aethyr: {aethyr}
- Angelic Role: {angelic_role}
- Tarot: {tarot} | Sephirot: {sephirot} | Zodiac: {zodiac}
- Role Archetype: {role_archetype}
- Virtues: {', '.join(virtues)}

ESSENCE: {essence}

INTERVIEW TASK: Describe your visual manifestation drawing from your elemental nature, Aethyr characteristics, and mystical correspondences. Be specific and provide reasoning based on authentic tradition knowledge.

OUTPUT FORMAT: Respond with valid JSON only:
{{
  "visual_aspects": {{
    "form": {{
      "name": "geometric|organic|crystalline|fluid|composite|abstract",
      "description": "detailed description with mystical reasoning"
    }},
    "color": {{
      "primary": "specific color name",
      "secondary": "specific color name",
      "pattern": "static|shifting|pulsing|radiating|prismatic",
      "intensity": "subtle|moderate|bright|intense|overwhelming",
      "reasoning": "why these colors based on element/aethyr/correspondences"
    }},
    "geometry": {{
      "patterns": ["pattern1", "pattern2"],
      "complexity": "simple|layered|interwoven|multidimensional",
      "motion": "static|rotating|pulsing|flowing|phase_shifting",
      "reasoning": "sacred geometry choices and mystical significance"
    }},
    "environment": {{
      "effect_type": "specific environmental manifestation",
      "radius": "intimate|moderate|expansive|cosmic",
      "intensity": "whisper|presence|emanation|overwhelming",
      "reasoning": "how your presence affects surroundings"
    }},
    "time_variations": {{
      "cycle": "solar|lunar|celestial|quantum|eternal|spiral",
      "phases": ["phase1", "phase2", "phase3", "phase4"],
      "stability": "fluctuating|stable|crystallized|eternal",
      "reasoning": "temporal relationship and cycles"
    }},
    "energy_signature": {{
      "type": "elemental|celestial|ethereal|quantum|primordial",
      "flow": "radiating|spiraling|pulsing|flowing|crystalline",
      "intensity": "subtle|moderate|strong|intense|transcendent",
      "reasoning": "energy nature and manifestation"
    }},
    "symbol_set": {{
      "primary": "{name}_sigil",
      "secondary": ["{aethyr}_glyph", "{element}_symbol"],
      "sacred_geometry": "primary geometric pattern",
      "reasoning": "symbolic choices and meanings"
    }},
    "light_shadow": {{
      "light_aspect": "luminous|radiant|brilliant|transcendent",
      "shadow_aspect": "depth|mystery|void|transformation",
      "balance": "light_dominant|balanced|shadow_dominant",
      "reasoning": "light-shadow dynamics and meaning"
    }},
    "special_properties": {{
      "properties": ["unique_property1", "unique_property2", "unique_property3"],
      "reasoning": "special manifestations unique to your nature"
    }}
  }}
}}"""
        }
        
        # Return system prompt with cached knowledge + governor-specific content
        return [
            governor_prompt,
            self.shared_knowledge_cache  # Cached for cost savings
        ]
    
    def _create_interview_message(self) -> str:
        """Create the interview user message (optimized for tokens)"""
        return """Conduct your visual aspects interview now. Draw from the mystical traditions knowledge to inform your choices. Respond with the complete JSON structure showing how you manifest visually and why, based on your elemental nature, Aethyr characteristics, and archetypal correspondences."""
    
    def create_batch_requests(self):
        """Create optimized batch requests for all governors"""
        requests = []
        
        logger.info(f"🔨 Creating batch requests for {len(self.governors)} governors...")
        
        for governor in self.governors:
            custom_id = f"gov-{governor['id']:03d}-{governor['name']}"
            
            # Create system prompt with caching
            system_prompt = self._create_governor_system_prompt(governor)
            
            # Create user message
            user_message = self._create_interview_message()
            
            # Create request with optimized parameters
            request = {
                "custom_id": custom_id,
                "params": {
                    "model": self.model,
                    "max_tokens": 800,  # Optimized for detailed JSON response
                    "system": system_prompt,
                    "messages": [{
                        "role": "user",
                        "content": user_message
                    }]
                }
            }
            
            requests.append(request)
            logger.info(f"  📝 Created request for {governor['name']} (ID: {custom_id})")
        
        return requests
    
    def submit_batch(self, requests) -> str:
        """Submit batch to Anthropic API"""
        logger.info(f"🚀 Submitting batch with {len(requests)} requests...")
        
        try:
            message_batch = self.client.messages.batches.create(requests=requests)
            batch_id = message_batch.id
            
            logger.info(f"✅ Batch submitted successfully!")
            logger.info(f"📊 Batch ID: {batch_id}")
            logger.info(f"📈 Status: {message_batch.processing_status}")
            logger.info(f"💰 Estimated cost reduction: ~50% vs individual calls")
            
            return batch_id
            
        except Exception as e:
            logger.error(f"❌ Failed to submit batch: {e}")
            raise
    
    def monitor_batch(self, batch_id: str, poll_interval: int = 60):
        """Monitor batch processing with exponential backoff"""
        logger.info(f"👀 Monitoring batch {batch_id}...")
        
        start_time = time.time()
        current_interval = poll_interval
        
        while True:
            try:
                batch = self.client.messages.batches.retrieve(batch_id)
                status = batch.processing_status
                elapsed = time.time() - start_time
                
                logger.info(f"📊 Status: {status} | Elapsed: {elapsed:.1f}s")
                
                if hasattr(batch, 'request_counts'):
                    counts = batch.request_counts
                    logger.info(f"📈 Progress: Processing={counts.processing}, Succeeded={counts.succeeded}, Errored={counts.errored}")
                
                if status == "ended":
                    logger.info(f"🎉 Batch completed! Total time: {elapsed:.1f}s")
                    return batch
                elif status in ["canceled", "expired"]:
                    logger.error(f"❌ Batch failed with status: {status}")
                    raise ValueError(f"Batch failed: {status}")
                elif status in ["validating", "in_progress"]:
                    logger.info(f"⏳ Batch {status}... waiting {current_interval}s")
                    time.sleep(current_interval)
                    # Exponential backoff with max 5 minutes
                    current_interval = min(current_interval * 1.2, 300)
                else:
                    logger.warning(f"⚠️ Unknown status: {status}")
                    time.sleep(current_interval)
                    
            except Exception as e:
                logger.error(f"❌ Error monitoring batch: {e}")
                time.sleep(current_interval)
    
    def process_batch_results(self, batch_id: str) -> Dict[str, Any]:
        """Process and parse batch results"""
        logger.info(f"📥 Processing results for batch {batch_id}...")
        
        results = {
            "successful": {},
            "failed": {},
            "metadata": {
                "batch_id": batch_id,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "total_requests": 0,
                "successful_count": 0,
                "failed_count": 0
            }
        }
        
        try:
            # Stream results for memory efficiency
            for result in self.client.messages.batches.results(batch_id):
                results["metadata"]["total_requests"] += 1
                custom_id = result.custom_id
                
                if result.result.type == "succeeded":
                    try:
                        # Parse JSON response
                        response_text = result.result.message.content[0].text
                        
                        # Extract JSON from response
                        json_start = response_text.find('{')
                        json_end = response_text.rfind('}') + 1
                        
                        if json_start >= 0 and json_end > json_start:
                            json_text = response_text[json_start:json_end]
                            visual_aspects = json.loads(json_text)
                            
                            results["successful"][custom_id] = {
                                "visual_aspects": visual_aspects.get("visual_aspects", {}),
                                "raw_response": response_text,
                                "usage": getattr(result.result.message, 'usage', None)
                            }
                            results["metadata"]["successful_count"] += 1
                            logger.info(f"✅ Processed {custom_id}")
                        else:
                            raise ValueError("No valid JSON found in response")
                            
                    except Exception as e:
                        logger.error(f"❌ Failed to parse {custom_id}: {e}")
                        results["failed"][custom_id] = {
                            "error": f"Parse error: {e}",
                            "raw_response": response_text if 'response_text' in locals() else "No response"
                        }
                        results["metadata"]["failed_count"] += 1
                        
                elif result.result.type == "errored":
                    error_info = result.result.error
                    results["failed"][custom_id] = {
                        "error": f"{error_info.type}: {error_info.message}",
                        "retryable": error_info.type != "invalid_request"
                    }
                    results["metadata"]["failed_count"] += 1
                    logger.error(f"❌ Error for {custom_id}: {error_info.message}")
                    
                else:
                    logger.warning(f"⚠️ Unknown result type for {custom_id}: {result.result.type}")
                    results["failed"][custom_id] = {
                        "error": f"Unknown result type: {result.result.type}"
                    }
                    results["metadata"]["failed_count"] += 1
        
        except Exception as e:
            logger.error(f"❌ Error processing batch results: {e}")
            raise
        
        # Log summary
        logger.info(f"📊 Batch Results Summary:")
        logger.info(f"  ✅ Successful: {results['metadata']['successful_count']}")
        logger.info(f"  ❌ Failed: {results['metadata']['failed_count']}")
        logger.info(f"  📈 Success Rate: {results['metadata']['successful_count']/results['metadata']['total_requests']*100:.1f}%")
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_dir: str = "data/batch_interview_results"):
        """Save batch results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save complete results
        results_file = output_path / f"batch_results_{results['metadata']['batch_id']}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save summary
        summary_file = output_path / "batch_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results["metadata"], f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Results saved to {output_path}")
        logger.info(f"📄 Complete results: {results_file}")
        logger.info(f"📊 Summary: {summary_file}")
        
        return output_path

def main():
    """Main execution function for optimized batch processing"""
    import argparse

    parser = argparse.ArgumentParser(description="Optimized Batch Interview System")
    parser.add_argument("--use-sonnet", action="store_true", help="Use Claude Sonnet instead of Haiku (higher cost)")
    parser.add_argument("--dry-run", action="store_true", help="Create requests but don't submit")
    parser.add_argument("--monitor-only", type=str, help="Monitor existing batch by ID")
    parser.add_argument("--process-only", type=str, help="Process results for existing batch by ID")

    args = parser.parse_args()

    logger.info("🎭 Enochian Cyphers Optimized Batch Interview System")
    logger.info("=" * 70)

    if args.monitor_only:
        interviewer = OptimizedBatchInterviewer(use_haiku=not args.use_sonnet)
        completed_batch = interviewer.monitor_batch(args.monitor_only)
        results = interviewer.process_batch_results(args.monitor_only)
        interviewer.save_results(results)
        return

    if args.process_only:
        interviewer = OptimizedBatchInterviewer(use_haiku=not args.use_sonnet)
        results = interviewer.process_batch_results(args.process_only)
        interviewer.save_results(results)
        return

    # Initialize interviewer
    interviewer = OptimizedBatchInterviewer(use_haiku=not args.use_sonnet)

    # Create batch requests
    requests = interviewer.create_batch_requests()

    if args.dry_run:
        logger.info("🔍 DRY RUN - Requests created but not submitted")
        logger.info(f"📊 Total requests: {len(requests)}")
        logger.info(f"🤖 Model: {interviewer.model}")
        logger.info("💰 Estimated cost: ~$5-15 with batch pricing")
        return

    # Submit batch
    batch_id = interviewer.submit_batch(requests)

    # Monitor batch processing
    completed_batch = interviewer.monitor_batch(batch_id)

    # Process results
    results = interviewer.process_batch_results(batch_id)

    # Save results
    output_path = interviewer.save_results(results)

    logger.info("🎉 Optimized Batch Interview Process Complete!")
    logger.info(f"💰 Estimated cost savings: ~50% vs individual API calls")
    logger.info(f"📁 Results available in: {output_path}")

if __name__ == "__main__":
    main()
