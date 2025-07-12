#!/usr/bin/env python3
"""
Clear Visual Aspects from Governor Profiles
Resets all visual_aspects fields to empty state for fresh AI interview population
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_empty_visual_aspects() -> Dict[str, Any]:
    """Return empty visual aspects structure"""
    return {
        "form": {
            "name": "",
            "description": ""
        },
        "color": {
            "primary": "",
            "secondary": "",
            "pattern": "",
            "intensity": "",
            "reasoning": ""
        },
        "geometry": {
            "patterns": [],
            "complexity": "",
            "motion": "",
            "reasoning": ""
        },
        "environment": {
            "effect_type": "",
            "radius": "",
            "intensity": "",
            "reasoning": ""
        },
        "time_variations": {
            "cycle": "",
            "phases": [],
            "stability": "",
            "reasoning": ""
        },
        "energy_signature": {
            "type": "",
            "flow": "",
            "intensity": "",
            "reasoning": ""
        },
        "symbol_set": {
            "primary": "",
            "secondary": [],
            "sacred_geometry": "",
            "reasoning": ""
        },
        "light_shadow": {
            "light_aspect": "",
            "shadow_aspect": "",
            "balance": "",
            "reasoning": ""
        },
        "special_properties": {
            "properties": [],
            "reasoning": ""
        }
    }

def clear_governor_visual_aspects(profile_file: Path) -> bool:
    """Clear visual aspects for a single governor profile"""
    try:
        # Load existing profile
        with open(profile_file, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        governor_name = profile_data.get("governor_name", profile_file.stem)
        
        # Reset visual aspects to empty structure
        profile_data["visual_aspects"] = get_empty_visual_aspects()
        
        # Remove any AI generation metadata if present
        if "ai_generation_metadata" in profile_data:
            del profile_data["ai_generation_metadata"]
        
        # Save updated profile
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Cleared visual aspects for {governor_name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to clear {profile_file}: {e}")
        return False

def clear_all_visual_aspects(profiles_dir: str = "core/governors/profiles") -> Dict[str, int]:
    """Clear visual aspects from all governor profiles"""
    profiles_path = Path(profiles_dir)
    
    if not profiles_path.exists():
        logger.error(f"❌ Profiles directory not found: {profiles_path}")
        return {"cleared": 0, "failed": 0}
    
    stats = {"cleared": 0, "failed": 0}
    
    logger.info(f"🧹 Clearing visual aspects from all governor profiles...")
    
    # Process all JSON files in the profiles directory
    for profile_file in profiles_path.glob("*.json"):
        if clear_governor_visual_aspects(profile_file):
            stats["cleared"] += 1
        else:
            stats["failed"] += 1
    
    return stats

def main():
    """Main execution function"""
    logger.info("🧹 Governor Visual Aspects Cleaner")
    logger.info("=" * 40)
    
    # Clear all visual aspects
    stats = clear_all_visual_aspects()
    
    # Print results
    logger.info("🎉 Visual Aspects Clearing Complete!")
    logger.info(f"✅ Cleared: {stats['cleared']} profiles")
    logger.info(f"❌ Failed: {stats['failed']} profiles")
    
    if stats["cleared"] > 0:
        logger.info("🎭 Profiles are now ready for AI interview population!")
    
    if stats["failed"] > 0:
        logger.warning(f"⚠️  {stats['failed']} profiles had issues - check logs")

if __name__ == "__main__":
    main()
