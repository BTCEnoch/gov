#!/usr/bin/env python3
"""
Update Governor Profiles with AI Interview Results
Merges AI-generated visual aspects back into the governor profile files
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProfileUpdater:
    """Updates governor profiles with AI interview results"""
    
    def __init__(self, results_dir: str = "data/ai_interview_results", profiles_dir: str = "core/governors/profiles"):
        self.results_dir = Path(results_dir)
        self.profiles_dir = Path(profiles_dir)
        
    def load_interview_results(self) -> Dict[str, Any]:
        """Load all AI interview results"""
        results = {}
        
        for result_file in self.results_dir.glob("*_interview.json"):
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    governor_name = result_data.get("governor_name")
                    if governor_name:
                        results[governor_name] = result_data
            except Exception as e:
                logger.error(f"Failed to load {result_file}: {e}")
        
        logger.info(f"📁 Loaded {len(results)} interview results")
        return results
    
    def update_governor_profile(self, governor_name: str, interview_result: Dict[str, Any]) -> bool:
        """Update a single governor profile with interview results"""
        profile_file = self.profiles_dir / f"{governor_name}.json"
        
        if not profile_file.exists():
            logger.error(f"❌ Profile file not found: {profile_file}")
            return False
        
        try:
            # Load existing profile
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Extract visual aspects from interview result
            visual_aspects = interview_result.get("visual_aspects", {})
            
            if not visual_aspects:
                logger.warning(f"⚠️  No visual aspects found for {governor_name}")
                return False
            
            # Update profile with AI-generated visual aspects
            profile_data["visual_aspects"] = visual_aspects
            
            # Add metadata about the AI generation
            profile_data["ai_generation_metadata"] = {
                "generated_by": "anthropic_claude_ai_interview",
                "timestamp": interview_result.get("timestamp"),
                "model_used": "claude-3-5-sonnet-20241022",
                "interview_method": "role_play_based"
            }
            
            # Save updated profile
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Updated profile for {governor_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update profile for {governor_name}: {e}")
            return False
    
    def update_all_profiles(self) -> Dict[str, int]:
        """Update all governor profiles with AI interview results"""
        results = self.load_interview_results()
        
        if not results:
            logger.error("❌ No interview results found!")
            return {"updated": 0, "failed": 0, "skipped": 0}
        
        stats = {"updated": 0, "failed": 0, "skipped": 0}
        
        logger.info(f"🔄 Updating {len(results)} governor profiles...")
        
        for governor_name, interview_result in results.items():
            # Check if interview was successful
            if "error" in interview_result:
                logger.warning(f"⚠️  Skipping {governor_name} - interview had errors")
                stats["skipped"] += 1
                continue
            
            if self.update_governor_profile(governor_name, interview_result):
                stats["updated"] += 1
            else:
                stats["failed"] += 1
        
        return stats
    
    def create_visual_aspects_summary(self, output_file: str = "data/ai_interview_results/visual_aspects_summary.json"):
        """Create a summary of all generated visual aspects"""
        results = self.load_interview_results()
        
        summary = {
            "total_governors": len(results),
            "successful_generations": 0,
            "failed_generations": 0,
            "visual_categories_analysis": {
                "form_types": {},
                "primary_colors": {},
                "geometry_patterns": {},
                "energy_types": {},
                "temporal_cycles": {}
            },
            "governors_by_element": {},
            "generation_timestamp": None
        }
        
        for governor_name, result in results.items():
            if "error" in result:
                summary["failed_generations"] += 1
                continue
                
            summary["successful_generations"] += 1
            
            visual_aspects = result.get("visual_aspects", {})
            
            # Analyze form types
            form_name = visual_aspects.get("form", {}).get("name", "unknown")
            summary["visual_categories_analysis"]["form_types"][form_name] = \
                summary["visual_categories_analysis"]["form_types"].get(form_name, 0) + 1
            
            # Analyze colors
            primary_color = visual_aspects.get("color", {}).get("primary", "unknown")
            summary["visual_categories_analysis"]["primary_colors"][primary_color] = \
                summary["visual_categories_analysis"]["primary_colors"].get(primary_color, 0) + 1
            
            # Analyze geometry patterns
            geometry_patterns = visual_aspects.get("geometry", {}).get("patterns", [])
            for pattern in geometry_patterns:
                summary["visual_categories_analysis"]["geometry_patterns"][pattern] = \
                    summary["visual_categories_analysis"]["geometry_patterns"].get(pattern, 0) + 1
            
            # Analyze energy types
            energy_type = visual_aspects.get("energy_signature", {}).get("type", "unknown")
            summary["visual_categories_analysis"]["energy_types"][energy_type] = \
                summary["visual_categories_analysis"]["energy_types"].get(energy_type, 0) + 1
            
            # Analyze temporal cycles
            temporal_cycle = visual_aspects.get("time_variations", {}).get("cycle", "unknown")
            summary["visual_categories_analysis"]["temporal_cycles"][temporal_cycle] = \
                summary["visual_categories_analysis"]["temporal_cycles"].get(temporal_cycle, 0) + 1
        
        # Save summary
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Visual aspects summary saved to {output_path}")
        return summary

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Update governor profiles with AI interview results")
    
    parser.add_argument(
        "--results-dir",
        type=str,
        default="data/ai_interview_results",
        help="Directory containing AI interview results"
    )
    
    parser.add_argument(
        "--profiles-dir", 
        type=str,
        default="core/governors/profiles",
        help="Directory containing governor profiles to update"
    )
    
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only generate summary, don't update profiles"
    )
    
    args = parser.parse_args()
    
    logger.info("🔄 Governor Profile Updater")
    logger.info("=" * 40)
    
    updater = ProfileUpdater(args.results_dir, args.profiles_dir)
    
    if args.summary_only:
        logger.info("📊 Generating visual aspects summary only...")
        summary = updater.create_visual_aspects_summary()
        logger.info(f"✅ Summary complete - {summary['successful_generations']} successful generations")
    else:
        # Update all profiles
        stats = updater.update_all_profiles()
        
        # Generate summary
        summary = updater.create_visual_aspects_summary()
        
        # Print final results
        logger.info("🎉 Profile Update Complete!")
        logger.info(f"✅ Updated: {stats['updated']}")
        logger.info(f"❌ Failed: {stats['failed']}")
        logger.info(f"⚠️  Skipped: {stats['skipped']}")
        logger.info(f"📊 Summary generated with {summary['successful_generations']} visual aspects")

if __name__ == "__main__":
    main()
