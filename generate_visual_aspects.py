#!/usr/bin/env python3
"""
Streamlined Visual Aspects Generator for Enochian Cyphers
Generates visual aspects for all 91 Governor Angels using deterministic Bitcoin-native randomness
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VisualAspectsGenerator:
    """Generate visual aspects for Governor Angels using deterministic methods"""
    
    def __init__(self):
        self.profiles_dir = Path("core/governors/profiles")
        self.output_dir = Path("data/generated_visual_aspects")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Visual aspect mappings based on mystical traditions
        self.form_types = ["geometric", "organic", "crystalline", "fluid", "composite", "abstract"]
        self.colors = ["golden", "silver", "azure", "emerald", "crimson", "violet", "obsidian", "pearl"]
        self.geometry_patterns = ["flower_of_life", "merkaba", "metatron_cube", "sri_yantra", "torus", "vesica_piscis"]
        self.energy_signatures = ["radiant", "pulsing", "spiraling", "flowing", "crystalline", "quantum_field"]
        self.temporal_cycles = ["solar", "lunar", "celestial", "quantum", "eternal", "spiral"]
        
    def get_bitcoin_entropy(self, governor_name: str) -> str:
        """Generate deterministic entropy from governor name (Bitcoin-native approach)"""
        # Use SHA256 (Bitcoin's hash function) for deterministic randomness
        return hashlib.sha256(governor_name.encode()).hexdigest()
    
    def select_from_entropy(self, options: List[str], entropy: str, offset: int = 0) -> str:
        """Select an option deterministically based on entropy"""
        entropy_slice = entropy[offset:offset+8]
        index = int(entropy_slice, 16) % len(options)
        return options[index]
    
    def generate_visual_aspects(self, governor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual aspects for a single governor"""
        governor_name = governor_data["governor_name"]
        entropy = self.get_bitcoin_entropy(governor_name)
        
        # Extract governor traits for context
        persona = governor_data.get("persona", {})
        element = persona.get("element", "Unknown")
        aethyr = persona.get("aethyr", "Unknown")
        essence = persona.get("essence", "")
        
        # Generate visual aspects based on entropy and governor traits
        visual_aspects = {
            "form": {
                "name": self.select_from_entropy(self.form_types, entropy, 0),
                "description": f"Manifests as {self.select_from_entropy(self.form_types, entropy, 0)} patterns reflecting {element} elemental nature"
            },
            "color": {
                "primary": self.select_from_entropy(self.colors, entropy, 8),
                "secondary": self.select_from_entropy(self.colors, entropy, 16),
                "pattern": "shifting" if int(entropy[24:32], 16) % 2 else "static",
                "intensity": ["subtle", "moderate", "bright", "intense"][int(entropy[32:40], 16) % 4]
            },
            "geometry": {
                "patterns": [
                    self.select_from_entropy(self.geometry_patterns, entropy, 40),
                    self.select_from_entropy(self.geometry_patterns, entropy, 48)
                ],
                "complexity": ["simple", "layered", "interwoven", "multidimensional"][int(entropy[56:64], 16) % 4],
                "motion": ["static", "rotating", "pulsing", "flowing"][int(entropy[0:8], 16) % 4]
            },
            "environment": {
                "effect_type": f"{element.lower()}_resonance",
                "radius": ["intimate", "moderate", "expansive", "cosmic"][int(entropy[8:16], 16) % 4],
                "intensity": ["whisper", "presence", "emanation", "overwhelming"][int(entropy[16:24], 16) % 4]
            },
            "time_variations": {
                "cycle": self.select_from_entropy(self.temporal_cycles, entropy, 24),
                "phases": ["dawn", "noon", "dusk", "midnight"],
                "stability": ["fluctuating", "stable", "crystallized", "eternal"][int(entropy[32:40], 16) % 4]
            },
            "energy_signature": {
                "type": self.select_from_entropy(self.energy_signatures, entropy, 40),
                "flow": ["radiating", "spiraling", "pulsing", "flowing"][int(entropy[48:56], 16) % 4],
                "intensity": ["subtle", "moderate", "strong", "transcendent"][int(entropy[56:64], 16) % 4]
            },
            "symbol_set": {
                "primary": f"{governor_name}_sigil",
                "secondary": [f"{aethyr}_glyph", f"{element}_symbol"],
                "sacred_geometry": self.select_from_entropy(self.geometry_patterns, entropy, 0)
            },
            "light_shadow": {
                "light_aspect": "luminous" if int(entropy[0:16], 16) % 2 else "radiant",
                "shadow_aspect": "depth" if int(entropy[16:32], 16) % 2 else "mystery",
                "balance": ["light_dominant", "balanced", "shadow_dominant"][int(entropy[32:48], 16) % 3]
            },
            "special_properties": self.generate_special_properties(governor_name, element, entropy)
        }
        
        return visual_aspects
    
    def generate_special_properties(self, governor_name: str, element: str, entropy: str) -> List[str]:
        """Generate special visual properties based on governor characteristics"""
        properties = []
        
        # Element-based properties
        element_properties = {
            "Fire": ["flame_aura", "heat_shimmer", "spark_emanation"],
            "Water": ["mist_formation", "tidal_pulse", "reflection_depth"],
            "Air": ["wind_patterns", "ethereal_transparency", "sound_visualization"],
            "Earth": ["crystalline_growth", "stone_resonance", "mineral_gleam"]
        }
        
        if element in element_properties:
            properties.extend(element_properties[element])
        
        # Entropy-based unique properties
        unique_props = [
            "dimensional_shift", "time_distortion", "reality_ripple",
            "consciousness_bridge", "void_touch", "creation_spark"
        ]
        
        # Select 2-3 unique properties based on entropy
        for i in range(2):
            prop = self.select_from_entropy(unique_props, entropy, i * 8)
            if prop not in properties:
                properties.append(prop)
        
        return properties
    
    def process_all_governors(self) -> Dict[str, Any]:
        """Process all governor profiles and generate visual aspects"""
        results = {}
        processed_count = 0
        
        logger.info("🎨 Starting visual aspects generation for all governors...")
        
        # Process each governor profile
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    governor_data = json.load(f)
                
                governor_name = governor_data["governor_name"]
                logger.info(f"  🔮 Processing {governor_name}...")
                
                # Generate visual aspects
                visual_aspects = self.generate_visual_aspects(governor_data)
                
                # Update the governor profile with visual aspects
                governor_data["visual_aspects"] = visual_aspects
                
                # Save updated profile
                with open(profile_file, 'w', encoding='utf-8') as f:
                    json.dump(governor_data, f, indent=2, ensure_ascii=False)
                
                results[governor_name] = visual_aspects
                processed_count += 1
                
            except Exception as e:
                logger.error(f"❌ Error processing {profile_file.name}: {e}")
        
        logger.info(f"✅ Processed {processed_count} governors successfully!")
        return results
    
    def save_summary(self, results: Dict[str, Any]):
        """Save a summary of generated visual aspects"""
        summary = {
            "generation_timestamp": "2025-07-11T20:22:00Z",
            "total_governors": len(results),
            "generation_method": "deterministic_bitcoin_entropy",
            "visual_categories": [
                "form", "color", "geometry", "environment", 
                "time_variations", "energy_signature", "symbol_set", 
                "light_shadow", "special_properties"
            ],
            "governors_processed": sorted(results.keys())
        }
        
        summary_path = self.output_dir / "generation_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Summary saved to {summary_path}")

def main():
    """Main execution function"""
    logger.info("🚀 Enochian Cyphers Visual Aspects Generator")
    logger.info("=" * 50)
    
    generator = VisualAspectsGenerator()
    
    # Generate visual aspects for all governors
    results = generator.process_all_governors()
    
    # Save summary
    generator.save_summary(results)
    
    logger.info("🎉 Visual aspects generation complete!")
    logger.info(f"📁 Updated profiles in: {generator.profiles_dir}")
    logger.info(f"📊 Summary in: {generator.output_dir}")

if __name__ == "__main__":
    main()
