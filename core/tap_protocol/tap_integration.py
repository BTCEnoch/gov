#!/usr/bin/env python3
"""
Enochian Cyphers: TAP Protocol Integration Module
Per expert guidance: Research GitHub specs (Trac-Systems/tap-protocol-specs) and implement 
hypertoken creation/evolution using Coinkite library as base.

Implements TAP Protocol functions for Bitcoin L1 native hypertoken management.
"""

import json
import hashlib
import time
import secrets
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TapInscription:
    """TAP Protocol inscription structure per official specs"""
    p: str = "tap"  # Protocol identifier
    op: str = ""    # Operation: token-deploy, token-mint, token-transfer, etc.
    tick: str = ""  # Token ticker (3-32 symbols)
    amt: Optional[str] = None    # Amount for mint/transfer
    max: Optional[str] = None    # Max supply for deploy
    lim: Optional[str] = None    # Mint limit for deploy
    dta: Optional[str] = None    # Data field (max 512 bytes)

@dataclass
class HypertokenMetadata:
    """Enhanced metadata for Enochian Cyphers hypertokens"""
    governor_name: str
    tradition_affinities: List[str]
    evolution_stage: int
    mystical_resonance: float
    rarity_tier: str
    utility_functions: List[str]
    creation_timestamp: int
    bitcoin_block_height: Optional[int] = None

@dataclass
class EvolutionEvent:
    """Hypertoken evolution event tracking"""
    timestamp: int
    event_type: str  # achievement, quest_completion, tradition_mastery
    trigger: str
    old_properties: Dict[str, Any]
    new_properties: Dict[str, Any]
    mutation_hash: str

class TapProtocolIntegrator:
    """
    TAP Protocol integration for Enochian Cyphers
    Implements hypertoken creation, evolution, and Bitcoin L1 inscription
    """
    
    def __init__(self):
        self.inscription_cache = {}
        self.evolution_log = []
        self.rarity_tiers = {
            "common": {"min_resonance": 0.0, "max_resonance": 0.3, "multiplier": 1.0},
            "uncommon": {"min_resonance": 0.3, "max_resonance": 0.6, "multiplier": 1.5},
            "rare": {"min_resonance": 0.6, "max_resonance": 0.8, "multiplier": 2.0},
            "epic": {"min_resonance": 0.8, "max_resonance": 0.95, "multiplier": 3.0},
            "legendary": {"min_resonance": 0.95, "max_resonance": 1.0, "multiplier": 5.0}
        }
    
    def create_governor_hypertoken(self, governor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create TAP hypertoken for Governor Angel
        Per expert guidance: Each Governor Angel has associated hypertoken with unique properties
        """
        # Generate ticker from governor name (TAP spec: 3-32 symbols)
        ticker = self._generate_ticker(governor_data["name"])
        
        # Calculate mystical resonance and rarity
        mystical_resonance = self._calculate_mystical_resonance(governor_data)
        rarity_tier = self._determine_rarity_tier(mystical_resonance)
        
        # Create hypertoken metadata
        metadata = HypertokenMetadata(
            governor_name=governor_data["name"],
            tradition_affinities=governor_data.get("traditions", []),
            evolution_stage=1,
            mystical_resonance=mystical_resonance,
            rarity_tier=rarity_tier,
            utility_functions=self._generate_utility_functions(governor_data),
            creation_timestamp=int(time.time()),
            bitcoin_block_height=None  # Would be set during actual inscription
        )
        
        # Create TAP deployment inscription
        deploy_inscription = TapInscription(
            op="token-deploy",
            tick=ticker,
            max="21000000",  # Bitcoin-inspired max supply
            lim="1000",      # Mint limit per inscription
            dta=self._create_metadata_string(metadata)
        )
        
        # Generate hypertoken structure
        hypertoken = {
            "token_id": f"gov_{governor_data['name'].lower()}",
            "ticker": ticker,
            "metadata": asdict(metadata),
            "tap_inscription": asdict(deploy_inscription),
            "evolution_history": [],
            "current_supply": 0,
            "max_supply": 21000000,
            "utility_score": self._calculate_utility_score(metadata),
            "inscription_ready": True
        }
        
        return hypertoken
    
    def evolve_hypertoken(self, hypertoken: Dict[str, Any], achievement: str, 
                         context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evolve hypertoken based on player achievements
        Per expert guidance: Tokens evolve based on player interactions and achievements
        """
        old_metadata = hypertoken["metadata"].copy()
        
        # Calculate evolution parameters
        evolution_boost = self._calculate_evolution_boost(achievement, context)
        new_resonance = min(1.0, old_metadata["mystical_resonance"] + evolution_boost)
        new_stage = old_metadata["evolution_stage"] + 1
        
        # Update metadata
        new_metadata = old_metadata.copy()
        new_metadata.update({
            "evolution_stage": new_stage,
            "mystical_resonance": new_resonance,
            "rarity_tier": self._determine_rarity_tier(new_resonance)
        })
        
        # Add new utility functions based on evolution
        new_utilities = self._generate_evolution_utilities(achievement, new_stage)
        new_metadata["utility_functions"].extend(new_utilities)
        
        # Create evolution event
        evolution_event = EvolutionEvent(
            timestamp=int(time.time()),
            event_type=context.get("event_type", "achievement"),
            trigger=achievement,
            old_properties=old_metadata,
            new_properties=new_metadata,
            mutation_hash=self._generate_mutation_hash(old_metadata, new_metadata)
        )
        
        # Update hypertoken
        hypertoken["metadata"] = new_metadata
        hypertoken["evolution_history"].append(asdict(evolution_event))
        hypertoken["utility_score"] = self._calculate_utility_score(new_metadata)
        
        # Create evolution inscription (token-mint with evolution data)
        evolution_inscription = TapInscription(
            op="token-mint",
            tick=hypertoken["ticker"],
            amt="1",  # Mint 1 token for evolution
            dta=f"EVOLUTION:{achievement}:STAGE_{new_stage}"
        )
        
        hypertoken["latest_evolution_inscription"] = asdict(evolution_inscription)
        
        self.evolution_log.append(evolution_event)
        
        return hypertoken
    
    def create_tap_inscription_json(self, hypertoken: Dict[str, Any], 
                                  operation: str = "deploy") -> str:
        """
        Create TAP Protocol compatible inscription JSON
        Per TAP specs: Must be under 400kb for Ordinals compatibility
        """
        if operation == "deploy":
            inscription_data = hypertoken["tap_inscription"]
        elif operation == "evolution":
            inscription_data = hypertoken.get("latest_evolution_inscription", {})
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # Ensure compliance with TAP specs
        inscription_json = json.dumps(inscription_data, separators=(',', ':'))
        
        # Check size limit (400kb for Ordinals)
        if len(inscription_json.encode('utf-8')) > 400 * 1024:
            raise ValueError("Inscription exceeds 400kb Ordinals limit")
        
        return inscription_json
    
    def _generate_ticker(self, governor_name: str) -> str:
        """Generate TAP-compatible ticker from governor name"""
        # TAP spec: 3-32 symbols, Unicode allowed
        if len(governor_name) >= 3:
            return governor_name[:8].upper()  # Use first 8 chars
        else:
            return f"GOV{governor_name}".upper()[:8]
    
    def _calculate_mystical_resonance(self, governor_data: Dict[str, Any]) -> float:
        """Calculate mystical resonance based on governor properties"""
        base_resonance = 0.5
        
        # Factor in traditions
        tradition_count = len(governor_data.get("traditions", []))
        tradition_bonus = min(0.3, tradition_count * 0.05)
        
        # Factor in traits
        traits = governor_data.get("primary_traits", []) + governor_data.get("secondary_traits", [])
        trait_bonus = min(0.2, len(traits) * 0.03)
        
        # Add deterministic randomness based on name
        name_hash = hashlib.sha256(governor_data["name"].encode()).hexdigest()
        name_bonus = int(name_hash[:2], 16) / 255 * 0.1  # 0-0.1 range
        
        total_resonance = base_resonance + tradition_bonus + trait_bonus + name_bonus
        return min(1.0, total_resonance)
    
    def _determine_rarity_tier(self, mystical_resonance: float) -> str:
        """Determine rarity tier based on mystical resonance"""
        for tier, bounds in self.rarity_tiers.items():
            if bounds["min_resonance"] <= mystical_resonance < bounds["max_resonance"]:
                return tier
        return "legendary"  # For resonance >= 0.95
    
    def _generate_utility_functions(self, governor_data: Dict[str, Any]) -> List[str]:
        """Generate utility functions based on governor properties"""
        utilities = ["basic_divination", "knowledge_access"]
        
        # Add tradition-specific utilities
        traditions = governor_data.get("traditions", [])
        for tradition in traditions:
            if "enochian" in tradition.lower():
                utilities.append("angelic_communication")
            elif "tarot" in tradition.lower():
                utilities.append("card_reading_enhancement")
            elif "qabalah" in tradition.lower():
                utilities.append("tree_of_life_navigation")
        
        return utilities
    
    def _calculate_evolution_boost(self, achievement: str, context: Dict[str, Any]) -> float:
        """Calculate evolution boost based on achievement type"""
        boost_map = {
            "quest_completion": 0.05,
            "tradition_mastery": 0.1,
            "rare_knowledge_unlock": 0.08,
            "mystical_breakthrough": 0.15,
            "community_contribution": 0.03
        }
        
        base_boost = boost_map.get(achievement, 0.02)
        
        # Apply context modifiers
        difficulty_multiplier = context.get("difficulty_multiplier", 1.0)
        rarity_multiplier = context.get("rarity_multiplier", 1.0)
        
        return base_boost * difficulty_multiplier * rarity_multiplier
    
    def _generate_evolution_utilities(self, achievement: str, stage: int) -> List[str]:
        """Generate new utility functions based on evolution"""
        new_utilities = []
        
        if stage >= 3:
            new_utilities.append("advanced_divination")
        if stage >= 5:
            new_utilities.append("reality_manipulation")
        if stage >= 10:
            new_utilities.append("dimensional_access")
        
        # Achievement-specific utilities
        if "tradition_mastery" in achievement:
            new_utilities.append(f"master_{achievement.split('_')[0]}")
        
        return new_utilities
    
    def _calculate_utility_score(self, metadata) -> float:
        """Calculate overall utility score for hypertoken"""
        # Handle both dict and dataclass metadata
        if hasattr(metadata, 'mystical_resonance'):
            base_score = metadata.mystical_resonance * 100
            stage_bonus = metadata.evolution_stage * 10
            utility_bonus = len(metadata.utility_functions) * 5
            rarity_multiplier = self.rarity_tiers[metadata.rarity_tier]["multiplier"]
        else:
            base_score = metadata["mystical_resonance"] * 100
            stage_bonus = metadata["evolution_stage"] * 10
            utility_bonus = len(metadata["utility_functions"]) * 5
            rarity_multiplier = self.rarity_tiers[metadata["rarity_tier"]]["multiplier"]

        return (base_score + stage_bonus + utility_bonus) * rarity_multiplier
    
    def _create_metadata_string(self, metadata: HypertokenMetadata) -> str:
        """Create compact metadata string for TAP inscription (max 512 bytes)"""
        compact_data = {
            "gov": metadata.governor_name,
            "stage": metadata.evolution_stage,
            "resonance": round(metadata.mystical_resonance, 3),
            "rarity": metadata.rarity_tier,
            "traditions": metadata.tradition_affinities[:3]  # Limit for space
        }
        
        metadata_str = json.dumps(compact_data, separators=(',', ':'))
        
        # Ensure under 512 bytes
        if len(metadata_str.encode('utf-8')) > 512:
            # Truncate traditions if needed
            compact_data["traditions"] = compact_data["traditions"][:1]
            metadata_str = json.dumps(compact_data, separators=(',', ':'))
        
        return metadata_str
    
    def _generate_mutation_hash(self, old_props: Dict, new_props: Dict) -> str:
        """Generate unique hash for evolution mutation"""
        mutation_data = {
            "old": old_props,
            "new": new_props,
            "timestamp": int(time.time()),
            "nonce": secrets.token_hex(8)
        }
        
        mutation_str = json.dumps(mutation_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(mutation_str.encode()).hexdigest()

# Example usage and testing
if __name__ == "__main__":
    # Initialize TAP integrator
    tap_integrator = TapProtocolIntegrator()
    
    # Sample governor data
    sample_governor = {
        "name": "ABRIOND",
        "aethyr": "POP",
        "traditions": ["enochian_magic", "hermetic_qabalah"],
        "primary_traits": [
            {"name": "Celestial Protector", "influence": 0.8},
            {"name": "Ethereal Seer", "influence": 0.7}
        ],
        "secondary_traits": [
            {"name": "Divine Warrior", "influence": 0.5}
        ]
    }
    
    # Create hypertoken
    print("🔮 Creating Governor Hypertoken...")
    hypertoken = tap_integrator.create_governor_hypertoken(sample_governor)
    
    print(f"✅ Hypertoken created for {sample_governor['name']}")
    print(f"📊 Ticker: {hypertoken['ticker']}")
    print(f"🎯 Rarity: {hypertoken['metadata']['rarity_tier']}")
    print(f"⚡ Utility Score: {hypertoken['utility_score']:.2f}")
    
    # Create TAP inscription
    inscription_json = tap_integrator.create_tap_inscription_json(hypertoken)
    print(f"\n📜 TAP Inscription JSON ({len(inscription_json)} bytes):")
    print(inscription_json)
    
    # Evolve hypertoken
    print("\n🚀 Evolving hypertoken...")
    evolved_token = tap_integrator.evolve_hypertoken(
        hypertoken, 
        "tradition_mastery", 
        {"difficulty_multiplier": 1.5, "event_type": "achievement"}
    )
    
    print(f"✨ Evolution complete! New stage: {evolved_token['metadata']['evolution_stage']}")
    print(f"📈 New resonance: {evolved_token['metadata']['mystical_resonance']:.3f}")
    print(f"🎖️ New rarity: {evolved_token['metadata']['rarity_tier']}")
    
    print("\n🎉 TAP Protocol Integration Demo Complete!")
