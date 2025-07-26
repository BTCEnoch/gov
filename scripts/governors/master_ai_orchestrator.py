#!/usr/bin/env python3
"""
Enochian Cyphers Master AI Orchestrator
Complete system for booting 91 AI personas and generating unique content

This master script orchestrates the complete process:
1. Boot all 91 Governor Angel AI personas with consciousness simulation
2. Load their traits, knowledge base, and creative synthesis
3. Generate unique content inventories for each persona
4. Export organized content for game integration

Each of the 91 agents becomes their own specific persona and creates
their own unique and individual inventory of interactions, dialog,
challenges, rewards, etc.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))

from enhanced_ai_persona_loader import EnhancedPersonaLoader
from enhanced_batch_content_generator import EnhancedBatchContentGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MasterAIOrchestrator:
    """Master orchestrator for the complete AI persona and content generation system"""
    
    def __init__(self, 
                 api_provider: str = "anthropic",
                 api_key: Optional[str] = None,
                 max_concurrent: int = 5,
                 rate_limit_delay: float = 1.0):
        
        self.api_provider = api_provider
        self.api_key = api_key or os.getenv(f"{api_provider.upper()}_API_KEY")
        self.max_concurrent = max_concurrent
        self.rate_limit_delay = rate_limit_delay
        
        # Initialize components
        self.persona_loader = EnhancedPersonaLoader()
        self.content_generator = EnhancedBatchContentGenerator(
            api_provider=api_provider,
            api_key=api_key,
            max_concurrent=max_concurrent,
            rate_limit_delay=rate_limit_delay
        )
        
        # Orchestration state
        self.orchestration_stats = {
            'start_time': None,
            'end_time': None,
            'personas_booted': 0,
            'personas_failed': 0,
            'content_generated': 0,
            'total_cost': 0.0,
            'phases_completed': []
        }
        
        # Default content distribution per governor
        self.default_content_distribution = {
            'dialogue': 5,      # 5 interactive dialogues per governor
            'challenge': 3,     # 3 mystical challenges per governor
            'quest': 3,         # 3 progressive quests per governor
            'reward': 2,        # 2 reward mechanisms per governor
            'teaching': 3       # 3 wisdom teachings per governor
        }
    
    def validate_prerequisites(self) -> bool:
        """Validate that all prerequisites are met"""
        logger.info("Validating prerequisites...")
        
        # Check API key
        if not self.api_key:
            logger.error(f"Missing API key for {self.api_provider}")
            return False
        
        # Check governor profiles directory
        profiles_path = Path("governor_profiles")
        if not profiles_path.exists():
            logger.error("Governor profiles directory not found")
            return False
        
        # Check lighthouse knowledge base
        lighthouse_path = Path("lighthouse/traditions")
        if not lighthouse_path.exists():
            logger.error("Lighthouse knowledge base not found")
            return False
        
        # Check for governor profile files
        profile_files = list(profiles_path.glob("*_complete_interview.json"))
        if len(profile_files) == 0:
            logger.error("No governor profile files found")
            return False
        
        logger.info(f"Prerequisites validated: {len(profile_files)} governor profiles found")
        return True
    
    async def phase_1_boot_personas(self) -> bool:
        """Phase 1: Boot all 91 AI personas with consciousness simulation"""
        logger.info("=" * 60)
        logger.info("PHASE 1: BOOTING AI PERSONAS")
        logger.info("=" * 60)
        
        try:
            # Boot all personas
            personas = self.persona_loader.boot_all_personas()
            
            self.orchestration_stats['personas_booted'] = len(personas)
            self.orchestration_stats['personas_failed'] = 91 - len(personas)  # Assuming 91 total
            
            if len(personas) == 0:
                logger.error("No personas successfully booted")
                return False
            
            # Export personas for content generation
            personas_file = self.persona_loader.export_personas("governor_ai_personas.json")
            
            logger.info(f"Phase 1 complete: {len(personas)} personas booted successfully")
            self.orchestration_stats['phases_completed'].append('persona_boot')
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {e}")
            return False
    
    async def phase_2_generate_content(self, content_distribution: Optional[Dict[str, int]] = None) -> bool:
        """Phase 2: Generate unique content for all personas"""
        logger.info("=" * 60)
        logger.info("PHASE 2: GENERATING UNIQUE CONTENT")
        logger.info("=" * 60)
        
        try:
            # Use provided distribution or default
            distribution = content_distribution or self.default_content_distribution
            
            # Load personas into content generator
            self.content_generator.load_personas("governor_ai_personas.json")
            
            # Generate all content
            generated_content = await self.content_generator.generate_all_content(distribution)
            
            # Update stats
            total_content = sum(len(content_list) for content_list in generated_content.values())
            self.orchestration_stats['content_generated'] = total_content
            self.orchestration_stats['total_cost'] = self.content_generator.generation_stats['total_cost']
            
            # Export content
            self.content_generator.export_generated_content("generated_content")
            
            logger.info(f"Phase 2 complete: {total_content} content pieces generated")
            self.orchestration_stats['phases_completed'].append('content_generation')
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {e}")
            return False
    
    async def phase_3_organize_output(self) -> bool:
        """Phase 3: Organize and validate all generated content"""
        logger.info("=" * 60)
        logger.info("PHASE 3: ORGANIZING OUTPUT")
        logger.info("=" * 60)
        
        try:
            # Create master content index
            content_index = {
                'generation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_governors': self.orchestration_stats['personas_booted'],
                    'total_content_pieces': self.orchestration_stats['content_generated'],
                    'content_distribution': self.default_content_distribution,
                    'total_cost': self.orchestration_stats['total_cost']
                },
                'governors': {},
                'content_types': list(self.default_content_distribution.keys()),
                'integration_ready': True
            }
            
            # Scan generated content directory
            content_dir = Path("generated_content")
            if content_dir.exists():
                for governor_dir in content_dir.iterdir():
                    if governor_dir.is_dir():
                        governor_name = governor_dir.name
                        content_index['governors'][governor_name] = {
                            'content_files': [],
                            'total_pieces': 0
                        }
                        
                        # Count content files
                        for content_file in governor_dir.glob("*.json"):
                            content_index['governors'][governor_name]['content_files'].append(content_file.name)
                            
                            # Count pieces in file
                            try:
                                with open(content_file, 'r', encoding='utf-8') as f:
                                    content_data = json.load(f)
                                    content_index['governors'][governor_name]['total_pieces'] += len(content_data)
                            except:
                                pass
            
            # Save master index
            with open("generated_content/master_content_index.json", 'w', encoding='utf-8') as f:
                json.dump(content_index, f, indent=2, ensure_ascii=False)
            
            # Create integration guide
            integration_guide = {
                'title': 'Enochian Cyphers AI-Generated Content Integration Guide',
                'description': 'Guide for integrating AI-generated governor content into the game system',
                'content_structure': {
                    'dialogues': 'Interactive conversation sequences with branching paths',
                    'challenges': 'Mystical tests and trials with difficulty scaling',
                    'quests': 'Progressive quest sequences with narrative arcs',
                    'rewards': 'Hypertoken evolution and reward mechanisms',
                    'teachings': 'Wisdom instruction and mystical knowledge'
                },
                'integration_steps': [
                    'Load content files from generated_content/{governor_name}/',
                    'Parse JSON content according to defined structures',
                    'Integrate with existing quest system and UI',
                    'Connect to TAP Protocol for hypertoken rewards',
                    'Implement P2P validation for content authenticity'
                ],
                'technical_requirements': [
                    'JSON parsing capability',
                    'TAP Protocol integration',
                    'Trac indexing support',
                    'P2P consensus validation',
                    'Bitcoin L1 inscription readiness'
                ]
            }
            
            with open("generated_content/integration_guide.json", 'w', encoding='utf-8') as f:
                json.dump(integration_guide, f, indent=2, ensure_ascii=False)
            
            logger.info("Phase 3 complete: Content organized and integration guide created")
            self.orchestration_stats['phases_completed'].append('output_organization')
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {e}")
            return False
    
    async def run_complete_orchestration(self, content_distribution: Optional[Dict[str, int]] = None) -> bool:
        """Run the complete orchestration process"""
        logger.info("🚀 STARTING MASTER AI ORCHESTRATION")
        logger.info("Booting 91 AI personas and generating unique content...")
        
        self.orchestration_stats['start_time'] = datetime.now()
        
        # Validate prerequisites
        if not self.validate_prerequisites():
            logger.error("Prerequisites validation failed")
            return False
        
        try:
            # Phase 1: Boot personas
            if not await self.phase_1_boot_personas():
                logger.error("Persona booting failed")
                return False
            
            # Phase 2: Generate content
            if not await self.phase_2_generate_content(content_distribution):
                logger.error("Content generation failed")
                return False
            
            # Phase 3: Organize output
            if not await self.phase_3_organize_output():
                logger.error("Output organization failed")
                return False
            
            # Complete
            self.orchestration_stats['end_time'] = datetime.now()
            duration = self.orchestration_stats['end_time'] - self.orchestration_stats['start_time']
            
            # Save final stats
            with open("orchestration_statistics.json", 'w', encoding='utf-8') as f:
                json.dump(self.orchestration_stats, f, indent=2, default=str)
            
            logger.info("🎉 MASTER AI ORCHESTRATION COMPLETE!")
            logger.info(f"Duration: {duration}")
            logger.info(f"Personas booted: {self.orchestration_stats['personas_booted']}")
            logger.info(f"Content generated: {self.orchestration_stats['content_generated']} pieces")
            logger.info(f"Total cost: ${self.orchestration_stats['total_cost']:.2f}")
            logger.info("All content ready for game integration!")
            
            return True
            
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            return False

async def main():
    """Main entry point for the master orchestrator"""
    
    # Configuration
    orchestrator = MasterAIOrchestrator(
        api_provider="anthropic",  # or "openai"
        max_concurrent=3,          # Adjust based on API limits
        rate_limit_delay=2.0       # Adjust based on API limits
    )
    
    # Custom content distribution (optional)
    custom_distribution = {
        'dialogue': 4,      # 4 interactive dialogues per governor
        'challenge': 2,     # 2 mystical challenges per governor
        'quest': 2,         # 2 progressive quests per governor
        'reward': 1,        # 1 reward mechanism per governor
        'teaching': 2       # 2 wisdom teachings per governor
    }
    
    # Run complete orchestration
    success = await orchestrator.run_complete_orchestration(custom_distribution)
    
    if success:
        print("\n✅ SUCCESS: All 91 AI personas booted and content generated!")
        print("Check the 'generated_content' directory for all unique content.")
        print("See 'orchestration_statistics.json' for detailed metrics.")
    else:
        print("\n❌ FAILED: Orchestration encountered errors.")
        print("Check 'ai_orchestrator.log' for detailed error information.")

if __name__ == "__main__":
    asyncio.run(main())
