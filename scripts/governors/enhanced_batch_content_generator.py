#!/usr/bin/env python3
"""
Enochian Cyphers Enhanced Batch Content Generator
91 AI agents creating unique content simultaneously

This system takes booted AI personas and orchestrates simultaneous content generation
where each of the 91 Governor Angels creates their own unique inventory of:
- Interactive dialogues
- Mystical challenges  
- Progressive quests
- Reward mechanisms
- Wisdom teachings

Each agent operates as their specific persona, creating content that reflects
their individual wisdom, personality, and mystical practices.
"""

import json
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContentGenerationTask:
    """Individual content generation task for a persona"""
    governor_name: str
    task_type: str  # 'dialogue', 'challenge', 'quest', 'reward', 'teaching'
    difficulty_level: int
    content_count: int
    persona_prompt: str
    generation_context: Dict[str, Any]

@dataclass
class GeneratedContent:
    """Container for generated content from a persona"""
    governor_name: str
    content_type: str
    content_data: Dict[str, Any]
    generation_metadata: Dict[str, Any]
    validation_status: str

class EnhancedBatchContentGenerator:
    """Orchestrates 91 simultaneous AI agents for content generation"""
    
    def __init__(self, 
                 api_provider: str = "anthropic",
                 api_key: Optional[str] = None,
                 max_concurrent: int = 10,
                 rate_limit_delay: float = 1.0):
        self.api_provider = api_provider
        self.api_key = api_key or os.getenv(f"{api_provider.upper()}_API_KEY")
        self.max_concurrent = max_concurrent
        self.rate_limit_delay = rate_limit_delay
        
        self.personas = {}
        self.generated_content = {}
        self.generation_stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_cost': 0.0,
            'start_time': None,
            'end_time': None
        }
        
        # Content generation templates
        self.content_templates = {
            'dialogue': {
                'description': 'Interactive dialogue sequences with branching responses',
                'output_structure': {
                    'dialogue_id': 'unique_identifier',
                    'title': 'dialogue_title',
                    'context': 'setting_and_situation',
                    'opening_statement': 'initial_persona_message',
                    'response_options': [
                        {'option_text': 'player_choice', 'persona_response': 'ai_response', 'wisdom_taught': 'lesson'}
                    ],
                    'progression_paths': {'success': 'next_dialogue', 'failure': 'alternative_path'}
                }
            },
            'challenge': {
                'description': 'Mystical challenges that test understanding and commitment',
                'output_structure': {
                    'challenge_id': 'unique_identifier',
                    'title': 'challenge_title',
                    'description': 'challenge_description',
                    'challenge_type': 'puzzle|trial|test|riddle',
                    'difficulty_level': 'numeric_difficulty',
                    'requirements': ['prerequisite_knowledge'],
                    'solution_criteria': ['success_conditions'],
                    'rewards': {'hypertoken_evolution': 'reward_details'},
                    'failure_consequences': 'what_happens_on_failure'
                }
            },
            'quest': {
                'description': 'Progressive quest sequences with multiple objectives',
                'output_structure': {
                    'quest_id': 'unique_identifier',
                    'title': 'quest_title',
                    'narrative_arc': 'overall_story',
                    'objectives': ['objective_list'],
                    'wisdom_focus': 'primary_teaching',
                    'enochian_invocation': 'sacred_invocation',
                    'tradition_integration': ['relevant_traditions'],
                    'completion_rewards': {'hypertoken_mutations': 'evolution_details'},
                    'branching_outcomes': {'paths': 'alternative_routes'}
                }
            },
            'reward': {
                'description': 'Hypertoken evolution and reward mechanisms',
                'output_structure': {
                    'reward_id': 'unique_identifier',
                    'trigger_condition': 'what_earns_this_reward',
                    'hypertoken_evolution': {
                        'attribute_changes': 'stat_modifications',
                        'new_abilities': 'unlocked_capabilities',
                        'rarity_increase': 'rarity_progression'
                    },
                    'tap_protocol_data': 'bitcoin_l1_inscription_data',
                    'economic_value': 'autonomous_tokenomics_pricing'
                }
            },
            'teaching': {
                'description': 'Wisdom teachings and mystical instruction',
                'output_structure': {
                    'teaching_id': 'unique_identifier',
                    'title': 'teaching_title',
                    'wisdom_category': 'type_of_knowledge',
                    'instruction_text': 'detailed_teaching',
                    'practical_application': 'how_to_apply',
                    'tradition_sources': ['primary_source_references'],
                    'comprehension_test': 'understanding_verification',
                    'advancement_path': 'next_level_teachings'
                }
            }
        }
    
    def load_personas(self, personas_file: str = "governor_ai_personas.json") -> Dict[str, Any]:
        """Load booted AI personas from file"""
        try:
            with open(personas_file, 'r', encoding='utf-8') as f:
                self.personas = json.load(f)
            logger.info(f"Loaded {len(self.personas)} AI personas")
            return self.personas
        except Exception as e:
            logger.error(f"Error loading personas: {e}")
            return {}
    
    def create_generation_tasks(self, content_distribution: Dict[str, int]) -> List[ContentGenerationTask]:
        """Create content generation tasks for all personas"""
        tasks = []
        
        for governor_name, persona_data in self.personas.items():
            consciousness_prompt = persona_data.get('consciousness_prompt', '')
            generation_context = persona_data.get('content_generation_context', {})
            
            # Create tasks based on content distribution
            for content_type, count in content_distribution.items():
                for i in range(count):
                    # Scale difficulty based on content index
                    difficulty = min(10, max(1, (i // 2) + 1))  # Gradual difficulty increase
                    
                    task = ContentGenerationTask(
                        governor_name=governor_name,
                        task_type=content_type,
                        difficulty_level=difficulty,
                        content_count=1,
                        persona_prompt=consciousness_prompt,
                        generation_context=generation_context
                    )
                    tasks.append(task)
        
        logger.info(f"Created {len(tasks)} content generation tasks")
        return tasks
    
    async def generate_content_anthropic(self, task: ContentGenerationTask) -> Optional[GeneratedContent]:
        """Generate content using Anthropic Claude API"""
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            # Get content template
            template = self.content_templates.get(task.task_type, {})
            template_structure = template.get('output_structure', {})
            
            # Build generation prompt
            generation_prompt = f"""{task.persona_prompt}

CONTENT GENERATION TASK:
Create {task.task_type} content at difficulty level {task.difficulty_level}.

Content Type: {template.get('description', task.task_type)}

Required Output Structure (return as JSON):
{json.dumps(template_structure, indent=2)}

SPECIFIC REQUIREMENTS:
- Reflect your unique personality and wisdom in the content
- Integrate knowledge from your assigned traditions
- Scale difficulty appropriately for level {task.difficulty_level}
- Include authentic mystical elements and teachings
- Design for Bitcoin L1 inscription via TAP Protocol
- Ensure content supports hypertoken evolution mechanics

Generate exactly one piece of {task.task_type} content following the structure above."""

            response = await client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": generation_prompt}
                ]
            )
            
            content_text = response.content[0].text
            
            # Parse JSON response
            try:
                content_data = json.loads(content_text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
                if json_match:
                    content_data = json.loads(json_match.group())
                else:
                    logger.error(f"Failed to parse JSON for {task.governor_name} {task.task_type}")
                    return None
            
            # Calculate cost (approximate)
            prompt_tokens = len(generation_prompt.split()) * 1.3  # Rough estimate
            completion_tokens = len(content_text.split()) * 1.3
            cost = (prompt_tokens * 0.003 + completion_tokens * 0.015) / 1000  # Claude pricing
            
            self.generation_stats['total_cost'] += cost
            
            generated_content = GeneratedContent(
                governor_name=task.governor_name,
                content_type=task.task_type,
                content_data=content_data,
                generation_metadata={
                    'api_provider': 'anthropic',
                    'model': 'claude-3-5-sonnet-20240620',
                    'difficulty_level': task.difficulty_level,
                    'prompt_tokens': int(prompt_tokens),
                    'completion_tokens': int(completion_tokens),
                    'estimated_cost': cost,
                    'generation_timestamp': datetime.now().isoformat()
                },
                validation_status='pending'
            )
            
            logger.debug(f"Generated {task.task_type} for {task.governor_name} (difficulty {task.difficulty_level})")
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating content for {task.governor_name}: {e}")
            return None
    
    async def process_task_batch(self, tasks: List[ContentGenerationTask]) -> List[GeneratedContent]:
        """Process a batch of content generation tasks"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_single_task(task):
            async with semaphore:
                await asyncio.sleep(self.rate_limit_delay)  # Rate limiting
                return await self.generate_content_anthropic(task)
        
        results = await asyncio.gather(*[process_single_task(task) for task in tasks], return_exceptions=True)
        
        # Filter out None results and exceptions
        generated_content = []
        for result in results:
            if isinstance(result, GeneratedContent):
                generated_content.append(result)
                self.generation_stats['completed_tasks'] += 1
            else:
                self.generation_stats['failed_tasks'] += 1
        
        return generated_content
    
    async def generate_all_content(self, content_distribution: Dict[str, int]) -> Dict[str, List[GeneratedContent]]:
        """Generate all content for all 91 personas"""
        logger.info("Starting mass content generation for all 91 Governor Angels...")
        
        self.generation_stats['start_time'] = datetime.now()
        
        # Create all tasks
        tasks = self.create_generation_tasks(content_distribution)
        self.generation_stats['total_tasks'] = len(tasks)
        
        # Process tasks in batches to manage API limits
        batch_size = 50  # Adjust based on API limits
        all_generated_content = []
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(tasks) + batch_size - 1)//batch_size}")
            
            batch_content = await self.process_task_batch(batch)
            all_generated_content.extend(batch_content)
            
            # Progress update
            progress = (i + len(batch)) / len(tasks) * 100
            logger.info(f"Progress: {progress:.1f}% ({len(all_generated_content)} content pieces generated)")
        
        # Organize content by governor
        organized_content = {}
        for content in all_generated_content:
            if content.governor_name not in organized_content:
                organized_content[content.governor_name] = []
            organized_content[content.governor_name].append(content)
        
        self.generation_stats['end_time'] = datetime.now()
        self.generated_content = organized_content
        
        logger.info(f"Mass content generation complete!")
        logger.info(f"Generated content for {len(organized_content)} governors")
        logger.info(f"Total content pieces: {len(all_generated_content)}")
        logger.info(f"Total cost: ${self.generation_stats['total_cost']:.2f}")
        
        return organized_content
    
    def export_generated_content(self, output_dir: str = "generated_content"):
        """Export all generated content to organized files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export by governor
        for governor_name, content_list in self.generated_content.items():
            governor_dir = output_path / governor_name
            governor_dir.mkdir(exist_ok=True)
            
            # Organize by content type
            by_type = {}
            for content in content_list:
                content_type = content.content_type
                if content_type not in by_type:
                    by_type[content_type] = []
                by_type[content_type].append(asdict(content))
            
            # Save each content type
            for content_type, items in by_type.items():
                filename = governor_dir / f"{content_type}_content.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
        
        # Export generation statistics
        stats_file = output_path / "generation_statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.generation_stats, f, indent=2, default=str)
        
        logger.info(f"Exported all generated content to {output_dir}")
        return output_dir

# Example usage and configuration
async def main():
    """Example usage of the enhanced batch content generator"""
    
    # Initialize generator
    generator = EnhancedBatchContentGenerator(
        api_provider="anthropic",
        max_concurrent=5,  # Adjust based on API limits
        rate_limit_delay=1.0
    )
    
    # Load personas (assumes personas have been booted)
    generator.load_personas("governor_ai_personas.json")
    
    # Define content distribution per governor
    content_distribution = {
        'dialogue': 3,    # 3 interactive dialogues per governor
        'challenge': 2,   # 2 mystical challenges per governor  
        'quest': 2,       # 2 progressive quests per governor
        'reward': 1,      # 1 reward mechanism per governor
        'teaching': 2     # 2 wisdom teachings per governor
    }
    
    # Generate all content
    generated_content = await generator.generate_all_content(content_distribution)
    
    # Export results
    generator.export_generated_content("generated_content")
    
    print(f"Content generation complete!")
    print(f"Generated content for {len(generated_content)} governors")
    print(f"Total cost: ${generator.generation_stats['total_cost']:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
