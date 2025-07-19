#!/usr/bin/env python3
"""
Enochian Cyphers Batch AI System Setup

Sets up and tests the complete batch AI processing system for 91 Governor Angels.
Addresses expert feedback by implementing dynamic AI-driven quest generation.
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchAISystemSetup:
    """Setup and validation system for batch AI processing"""
    
    def __init__(self):
        self.root_path = Path(__file__).parent
        self.required_files = [
            'governor_ai_embodiment.py',
            'governor_agent_prompt_generator.py', 
            'batch_governor_quest_generator.py',
            'lighthouse/complete_lighthouse/lighthouse_master_index.json',
            'governor_profiles'
        ]
        self.setup_complete = False
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_packages = ['openai', 'anthropic', 'requests', 'pandas', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✓ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"✗ {package} is missing")
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Install with: pip install -r requirements.txt")
            return False
        
        logger.info("All dependencies are installed")
        return True
    
    def check_required_files(self) -> bool:
        """Check if required files exist"""
        logger.info("Checking required files...")
        
        missing_files = []
        for file_path in self.required_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                logger.info(f"✓ {file_path} exists")
            else:
                missing_files.append(file_path)
                logger.warning(f"✗ {file_path} is missing")
        
        if missing_files:
            logger.error(f"Missing files: {', '.join(missing_files)}")
            return False
        
        logger.info("All required files are present")
        return True
    
    def check_environment_config(self) -> bool:
        """Check environment configuration"""
        logger.info("Checking environment configuration...")
        
        # Check for .env file
        env_file = self.root_path / '.env'
        env_example = self.root_path / '.env.example'
        
        if not env_file.exists():
            if env_example.exists():
                logger.warning("No .env file found. Copy .env.example to .env and configure your API keys")
                return False
            else:
                logger.error("No .env.example file found")
                return False
        
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            logger.warning("python-dotenv not installed, using system environment variables")
        
        # Check API keys
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not openai_key and not anthropic_key:
            logger.error("No AI API keys configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
            return False
        
        if openai_key:
            logger.info("✓ OpenAI API key configured")
        if anthropic_key:
            logger.info("✓ Anthropic API key configured")
        
        return True
    
    def test_lighthouse_system(self) -> bool:
        """Test lighthouse knowledge base loading"""
        logger.info("Testing lighthouse system...")
        
        try:
            from governor_ai_embodiment import LighthouseLoader, GovernorProfileLoader
            
            # Test lighthouse loading
            lighthouse = LighthouseLoader()
            master_index = lighthouse.load_master_index()
            
            if master_index.get('total_entries', 0) < 2000:
                logger.error("Lighthouse knowledge base appears incomplete")
                return False
            
            logger.info(f"✓ Lighthouse loaded: {master_index['total_entries']} entries")
            
            # Test profile loading
            profiles = GovernorProfileLoader()
            all_profiles = profiles.load_all_profiles()
            
            if len(all_profiles) != 91:
                logger.error(f"Expected 91 governor profiles, found {len(all_profiles)}")
                return False
            
            logger.info(f"✓ Governor profiles loaded: {len(all_profiles)} profiles")
            return True
            
        except Exception as e:
            logger.error(f"Error testing lighthouse system: {e}")
            return False
    
    def test_ai_embodiment_system(self) -> bool:
        """Test AI embodiment system"""
        logger.info("Testing AI embodiment system...")
        
        try:
            from governor_ai_embodiment import main as create_embodiments
            
            # Create embodiments
            embodiment_system = create_embodiments()
            
            if len(embodiment_system.embodiments) != 91:
                logger.error(f"Expected 91 embodiments, created {len(embodiment_system.embodiments)}")
                return False
            
            logger.info(f"✓ AI embodiments created: {len(embodiment_system.embodiments)} governors")
            return True
            
        except Exception as e:
            logger.error(f"Error testing AI embodiment system: {e}")
            return False
    
    def test_prompt_generation(self) -> bool:
        """Test prompt generation system"""
        logger.info("Testing prompt generation system...")
        
        try:
            from governor_agent_prompt_generator import main as generate_prompts
            
            # Generate prompts
            prompt_generator = generate_prompts()
            
            if len(prompt_generator.agent_prompts) != 91:
                logger.error(f"Expected 91 prompts, generated {len(prompt_generator.agent_prompts)}")
                return False
            
            # Check prompt file exists
            prompts_file = self.root_path / 'governor_agent_prompts.json'
            if not prompts_file.exists():
                logger.error("Governor agent prompts file not created")
                return False
            
            logger.info(f"✓ Agent prompts generated: {len(prompt_generator.agent_prompts)} governors")
            return True
            
        except Exception as e:
            logger.error(f"Error testing prompt generation: {e}")
            return False
    
    async def test_batch_ai_system(self, test_count: int = 3) -> bool:
        """Test batch AI system with a small sample"""
        logger.info(f"Testing batch AI system with {test_count} governors...")
        
        try:
            from batch_governor_quest_generator import BatchGovernorQuestGenerator, BatchProcessingConfig
            
            # Create test configuration
            config = BatchProcessingConfig(
                api_provider=os.getenv('AI_PROVIDER', 'openai'),
                model_name=os.getenv('MODEL_NAME', 'gpt-4'),
                batch_size=test_count,
                delay_between_batches=5.0,
                max_retries=2,
                cost_limit_usd=5.0,  # Low limit for testing
                output_directory="test_questlines"
            )
            
            # Create generator
            generator = BatchGovernorQuestGenerator(config)
            
            # Load prompts
            agent_prompts = generator.load_agent_prompts()
            
            # Test with first few governors
            test_governors = list(agent_prompts.items())[:test_count]
            
            # Generate test batch
            batch_results = await generator.generate_batch(test_governors)
            
            if len(batch_results) == 0:
                logger.error("No questlines generated in test batch")
                return False
            
            logger.info(f"✓ Test batch completed: {len(batch_results)}/{test_count} successful")
            logger.info(f"✓ Total cost: ${generator.provider.total_cost:.4f}")
            
            # Save test results
            generator.save_questlines("test_batch_results.json", batch_results)
            
            return True
            
        except Exception as e:
            logger.error(f"Error testing batch AI system: {e}")
            return False
    
    def run_full_setup(self) -> bool:
        """Run complete setup and validation"""
        logger.info("=== ENOCHIAN CYPHERS BATCH AI SYSTEM SETUP ===")
        
        steps = [
            ("Dependencies", self.check_dependencies),
            ("Required Files", self.check_required_files),
            ("Environment Config", self.check_environment_config),
            ("Lighthouse System", self.test_lighthouse_system),
            ("AI Embodiment System", self.test_ai_embodiment_system),
            ("Prompt Generation", self.test_prompt_generation),
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            if not step_func():
                logger.error(f"Setup failed at: {step_name}")
                return False
        
        logger.info("\n--- Batch AI System Test ---")
        # Run async test
        try:
            result = asyncio.run(self.test_batch_ai_system())
            if not result:
                logger.error("Batch AI system test failed")
                return False
        except Exception as e:
            logger.error(f"Error running batch AI test: {e}")
            return False
        
        self.setup_complete = True
        logger.info("\n=== SETUP COMPLETE ===")
        logger.info("✓ All systems operational")
        logger.info("✓ Ready for full batch processing")
        logger.info("\nNext steps:")
        logger.info("1. Review test results in test_questlines/")
        logger.info("2. Adjust configuration in .env if needed")
        logger.info("3. Run: python batch_governor_quest_generator.py")
        
        return True

def main():
    """Main setup function"""
    setup = BatchAISystemSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-only":
        # Run only the batch AI test
        logger.info("Running batch AI test only...")
        try:
            result = asyncio.run(setup.test_batch_ai_system())
            if result:
                logger.info("✓ Batch AI test passed")
            else:
                logger.error("✗ Batch AI test failed")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Test error: {e}")
            sys.exit(1)
    else:
        # Run full setup
        success = setup.run_full_setup()
        if not success:
            logger.error("Setup failed")
            sys.exit(1)
        
        logger.info("Setup completed successfully!")

if __name__ == "__main__":
    main()
