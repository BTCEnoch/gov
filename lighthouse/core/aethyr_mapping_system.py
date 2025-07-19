#!/usr/bin/env python3
"""
Enochian Cyphers Governor-Aethyr Mapping System

Implements standardized Governor-Aethyr mappings for sacred architecture compliance.
Addresses expert feedback: "Create a mapping schema in governor_profiles/ enforcing 
91 Governors across 30 Aethyrs".

This system provides:
- Standardized mapping of 91 Governors across 30 Aethyrs
- Sacred distribution validation (TEX=4, others=3 each)
- O(1) query performance for Governor-Aethyr lookups
- Integration with hypertoken evolution mechanics
- Compliance with Enochian sacred geometry

Maintains structural care by placing in /governor_profiles directory for 
direct integration with Governor Angel profiles.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AethyrInfo:
    """Aethyr information with sacred properties"""
    name: str
    tier: int  # 1-30, with 1 being highest (TEX)
    governor_count: int
    governors: List[str]
    mystical_properties: Dict[str, Any]
    hypertoken_multiplier: float

@dataclass
class GovernorMapping:
    """Governor to Aethyr mapping with metadata"""
    governor_name: str
    aethyr_name: str
    aethyr_tier: int
    position_in_aethyr: int  # 1-4 for TEX, 1-3 for others
    mystical_correspondences: Dict[str, str]
    evolution_potential: int

class AethyrMappingSystem:
    """Standardized Governor-Aethyr mapping system"""
    
    def __init__(self, governor_profiles_dir: str = "governor_profiles"):
        self.governor_profiles_dir = Path(governor_profiles_dir)
        self.mapping_file = Path("lighthouse/core/aethyr_mappings.json")
        
        # Sacred Aethyr hierarchy (30 Aethyrs as per Enochian tradition)
        self.sacred_aethyrs = [
            "TEX", "ARN", "ZOM", "PAZ", "LIT", "MAZ", "DEO", "ZID", "ZIP", "ZAX",
            "ICH", "LOE", "ZIM", "UTI", "OXO", "LEA", "TAN", "ZEN", "POP", "CHR",
            "ASP", "LIN", "TOR", "NIA", "VTI", "ZAA", "BAG", "RII", "TEX", "LIL"
        ][:30]  # Ensure exactly 30
        
        # Initialize mappings
        self.aethyr_mappings = self._initialize_sacred_mappings()
        self.governor_to_aethyr = {}
        self.aethyr_to_governors = {}
        
        logger.info("Aethyr Mapping System initialized")
    
    def _initialize_sacred_mappings(self) -> Dict[str, AethyrInfo]:
        """Initialize sacred Aethyr mappings with mystical properties"""
        logger.info("Initializing sacred Aethyr mappings")
        
        mappings = {}
        
        for i, aethyr_name in enumerate(self.sacred_aethyrs):
            tier = i + 1
            
            # TEX (highest Aethyr) gets 4 governors, others get 3
            governor_count = 4 if aethyr_name == "TEX" else 3
            
            # Mystical properties based on Aethyr tier
            mystical_properties = {
                "element": self._get_elemental_correspondence(tier),
                "planetary_influence": self._get_planetary_influence(tier),
                "sephirotic_path": self._get_sephirotic_correspondence(tier),
                "tarot_correspondence": self._get_tarot_correspondence(tier),
                "i_ching_hexagram": self._get_i_ching_correspondence(tier)
            }
            
            # Hypertoken evolution multiplier (higher tiers = higher multipliers)
            hypertoken_multiplier = max(1.0, (31 - tier) / 10.0)
            
            mappings[aethyr_name] = AethyrInfo(
                name=aethyr_name,
                tier=tier,
                governor_count=governor_count,
                governors=[],  # Will be populated
                mystical_properties=mystical_properties,
                hypertoken_multiplier=hypertoken_multiplier
            )
        
        return mappings
    
    def _get_elemental_correspondence(self, tier: int) -> str:
        """Get elemental correspondence for Aethyr tier"""
        elements = ["Fire", "Water", "Air", "Earth", "Spirit"]
        return elements[(tier - 1) % len(elements)]
    
    def _get_planetary_influence(self, tier: int) -> str:
        """Get planetary influence for Aethyr tier"""
        planets = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
        return planets[(tier - 1) % len(planets)]
    
    def _get_sephirotic_correspondence(self, tier: int) -> str:
        """Get Sephirotic correspondence for Aethyr tier"""
        sephiroth = [
            "Kether", "Chokmah", "Binah", "Chesed", "Geburah", 
            "Tiphareth", "Netzach", "Hod", "Yesod", "Malkuth"
        ]
        return sephiroth[(tier - 1) % len(sephiroth)]
    
    def _get_tarot_correspondence(self, tier: int) -> str:
        """Get Tarot correspondence for Aethyr tier"""
        major_arcana = [
            "The Fool", "The Magician", "The High Priestess", "The Empress",
            "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
            "Strength", "The Hermit", "Wheel of Fortune", "Justice",
            "The Hanged Man", "Death", "Temperance", "The Devil",
            "The Tower", "The Star", "The Moon", "The Sun",
            "Judgement", "The World"
        ]
        return major_arcana[(tier - 1) % len(major_arcana)]
    
    def _get_i_ching_correspondence(self, tier: int) -> int:
        """Get I Ching hexagram correspondence for Aethyr tier"""
        return ((tier - 1) % 64) + 1
    
    def load_governor_profiles(self) -> List[str]:
        """Load all governor names from profile files"""
        logger.info("Loading governor profiles")
        
        governors = []
        for profile_file in self.governor_profiles_dir.glob("*_complete_interview.json"):
            governor_name = profile_file.stem.replace("_complete_interview", "")
            governors.append(governor_name)
        
        logger.info(f"Loaded {len(governors)} governor profiles")
        return sorted(governors)
    
    def create_sacred_mappings(self) -> Dict[str, Any]:
        """Create sacred mappings of 91 Governors to 30 Aethyrs"""
        logger.info("Creating sacred Governor-Aethyr mappings")
        
        governors = self.load_governor_profiles()
        
        if len(governors) != 91:
            logger.warning(f"Expected 91 governors, found {len(governors)}")
        
        # Distribute governors across Aethyrs
        governor_index = 0
        mappings = {}
        
        for aethyr_name, aethyr_info in self.aethyr_mappings.items():
            aethyr_governors = []
            
            for position in range(aethyr_info.governor_count):
                if governor_index < len(governors):
                    governor_name = governors[governor_index]
                    aethyr_governors.append(governor_name)
                    
                    # Create governor mapping
                    governor_mapping = GovernorMapping(
                        governor_name=governor_name,
                        aethyr_name=aethyr_name,
                        aethyr_tier=aethyr_info.tier,
                        position_in_aethyr=position + 1,
                        mystical_correspondences={
                            "element": aethyr_info.mystical_properties["element"],
                            "planet": aethyr_info.mystical_properties["planetary_influence"],
                            "sephirah": aethyr_info.mystical_properties["sephirotic_path"],
                            "tarot": aethyr_info.mystical_properties["tarot_correspondence"],
                            "i_ching": aethyr_info.mystical_properties["i_ching_hexagram"]
                        },
                        evolution_potential=int(aethyr_info.hypertoken_multiplier * 10)
                    )
                    
                    # Store mappings
                    self.governor_to_aethyr[governor_name] = governor_mapping
                    mappings[governor_name] = asdict(governor_mapping)
                    
                    governor_index += 1
            
            # Update Aethyr info with governors
            aethyr_info.governors = aethyr_governors
            self.aethyr_to_governors[aethyr_name] = aethyr_governors
        
        logger.info(f"Created mappings for {governor_index} governors across {len(self.aethyr_mappings)} Aethyrs")
        return mappings
    
    def validate_sacred_distribution(self) -> Dict[str, Any]:
        """Validate sacred distribution (TEX=4, others=3)"""
        logger.info("Validating sacred distribution")
        
        validation_results = {
            "valid": True,
            "total_governors": 0,
            "total_aethyrs": len(self.aethyr_mappings),
            "tex_governors": 0,
            "distribution_errors": []
        }
        
        for aethyr_name, governors in self.aethyr_to_governors.items():
            governor_count = len(governors)
            validation_results["total_governors"] += governor_count
            
            if aethyr_name == "TEX":
                validation_results["tex_governors"] = governor_count
                if governor_count != 4:
                    validation_results["valid"] = False
                    validation_results["distribution_errors"].append(
                        f"TEX Aethyr has {governor_count} governors, expected 4"
                    )
            else:
                if governor_count != 3:
                    validation_results["valid"] = False
                    validation_results["distribution_errors"].append(
                        f"Aethyr {aethyr_name} has {governor_count} governors, expected 3"
                    )
        
        # Validate totals
        if validation_results["total_governors"] != 91:
            validation_results["valid"] = False
            validation_results["distribution_errors"].append(
                f"Total governors: {validation_results['total_governors']}, expected 91"
            )
        
        if validation_results["total_aethyrs"] != 30:
            validation_results["valid"] = False
            validation_results["distribution_errors"].append(
                f"Total Aethyrs: {validation_results['total_aethyrs']}, expected 30"
            )
        
        return validation_results
    
    def get_governor_aethyr(self, governor_name: str) -> Optional[GovernorMapping]:
        """O(1) lookup for governor's Aethyr mapping"""
        return self.governor_to_aethyr.get(governor_name)
    
    def get_aethyr_governors(self, aethyr_name: str) -> List[str]:
        """Get all governors for a specific Aethyr"""
        return self.aethyr_to_governors.get(aethyr_name, [])
    
    def export_mappings(self) -> Dict[str, Any]:
        """Export complete mapping system"""
        logger.info("Exporting Aethyr mapping system")
        
        # Create mappings
        governor_mappings = self.create_sacred_mappings()
        
        # Validate distribution
        validation = self.validate_sacred_distribution()
        
        # Export data
        export_data = {
            "system_info": {
                "created_timestamp": datetime.now().isoformat(),
                "total_governors": len(governor_mappings),
                "total_aethyrs": len(self.aethyr_mappings),
                "sacred_distribution_valid": validation["valid"],
                "system_hash": hashlib.sha256(str(governor_mappings).encode()).hexdigest()[:16]
            },
            "aethyr_hierarchy": {name: asdict(info) for name, info in self.aethyr_mappings.items()},
            "governor_mappings": governor_mappings,
            "aethyr_to_governors": self.aethyr_to_governors,
            "validation_results": validation
        }
        
        # Save to file
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported mappings to {self.mapping_file}")
        return export_data

def main():
    """Main execution function"""
    logger.info("=== ENOCHIAN CYPHERS AETHYR MAPPING SYSTEM ===")
    
    # Initialize mapping system
    mapping_system = AethyrMappingSystem()
    
    # Export complete mappings
    export_data = mapping_system.export_mappings()
    
    # Display results
    logger.info(f"\n=== MAPPING RESULTS ===")
    logger.info(f"Total Governors: {export_data['system_info']['total_governors']}")
    logger.info(f"Total Aethyrs: {export_data['system_info']['total_aethyrs']}")
    logger.info(f"Sacred Distribution Valid: {export_data['system_info']['sacred_distribution_valid']}")
    
    if export_data['validation_results']['distribution_errors']:
        logger.warning("Distribution Errors:")
        for error in export_data['validation_results']['distribution_errors']:
            logger.warning(f"  - {error}")
    
    return mapping_system

if __name__ == "__main__":
    main()
