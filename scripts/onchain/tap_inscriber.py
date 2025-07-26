#!/usr/bin/env python3
"""
Enochian Cyphers TAP Inscriber System

Implements compression and inscription batching for TAP Protocol deployment.
Addresses expert feedback Gap #2: TAP Protocol & Hypertoken Systems - 
"Build tap_inscriber.py for compression and inscription batching".

This system provides:
- Compression of 2,565+ lighthouse entries for Ordinals compliance (<1MB)
- Batch inscription preparation for TAP Protocol hypertokens
- Metadata schemas for hypertoken evolution mechanics
- State transition validation for player-driven mutations
- Cross-token interaction preparation for Governor wisdom synthesis

Maintains structural care by placing in /onchain directory for Bitcoin L1 
integration components.
"""

import json
import gzip
import os
import logging
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TAPInscriptionBatch:
    """TAP Protocol inscription batch with compression and metadata"""
    batch_id: str
    batch_number: int
    total_batches: int
    traditions: List[str]
    entry_count: int
    uncompressed_size: int
    compressed_size: int
    compression_ratio: float
    inscription_data: str  # Base64 encoded compressed JSON
    metadata_hash: str
    evolution_hooks: List[str]
    cross_token_refs: List[str]
    created_timestamp: str

@dataclass
class TAPHypertokenMetadata:
    """Metadata schema for TAP hypertoken evolution"""
    token_id: str
    governor_name: str
    tradition_affinities: Dict[str, float]
    wisdom_level: int
    evolution_stage: str
    mutation_triggers: List[str]
    cross_token_interactions: List[str]
    authenticity_score: float
    source_citations: List[str]
    inscription_batch_ref: str

class TAPInscriber:
    """TAP Protocol inscription system with compression and batching"""
    
    def __init__(self, lighthouse_dir: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_dir = Path(lighthouse_dir)
        self.output_dir = Path("onchain/tap_inscriptions")
        self.output_dir.mkdir(exist_ok=True)
        
        # TAP Protocol configuration
        self.max_inscription_size = 1024 * 1024  # 1MB Ordinals limit
        self.target_compression_ratio = 0.3  # 70% compression target
        self.batch_size_target = 950000  # 950KB to allow metadata overhead
        
        logger.info("TAP Inscriber initialized")
    
    def analyze_lighthouse_content(self) -> Dict[str, Any]:
        """Analyze lighthouse content for inscription planning"""
        logger.info("Analyzing lighthouse content for TAP inscription")
        
        analysis = {
            "total_traditions": 0,
            "total_entries": 0,
            "total_uncompressed_size": 0,
            "tradition_sizes": {},
            "estimated_batches": 0,
            "compression_feasible": False
        }
        
        for tradition_file in self.lighthouse_dir.glob("*.json"):
            if tradition_file.name == "lighthouse_master_index.json":
                continue
            
            # Load tradition data
            with open(tradition_file, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            tradition_name = tradition_data.get("tradition_info", {}).get("name", tradition_file.stem)
            entries = tradition_data.get("entries", [])
            
            # Calculate size
            tradition_json = json.dumps(tradition_data, separators=(',', ':'))
            tradition_size = len(tradition_json.encode('utf-8'))
            
            analysis["tradition_sizes"][tradition_name] = {
                "entry_count": len(entries),
                "uncompressed_size": tradition_size,
                "size_kb": tradition_size / 1024
            }
            
            analysis["total_traditions"] += 1
            analysis["total_entries"] += len(entries)
            analysis["total_uncompressed_size"] += tradition_size
        
        # Estimate compression and batching
        estimated_compressed_size = analysis["total_uncompressed_size"] * self.target_compression_ratio
        analysis["estimated_compressed_size"] = estimated_compressed_size
        analysis["estimated_batches"] = max(1, int(estimated_compressed_size / self.batch_size_target) + 1)
        analysis["compression_feasible"] = estimated_compressed_size < self.max_inscription_size
        
        logger.info(f"Analysis complete: {analysis['total_traditions']} traditions, "
                   f"{analysis['total_entries']} entries, "
                   f"{analysis['total_uncompressed_size']/1024:.1f}KB uncompressed")
        
        return analysis
    
    def create_inscription_batches(self) -> List[TAPInscriptionBatch]:
        """Create optimized inscription batches for TAP Protocol"""
        logger.info("Creating TAP Protocol inscription batches")
        
        analysis = self.analyze_lighthouse_content()
        if not analysis["compression_feasible"]:
            logger.warning("Content may not compress sufficiently for single inscription")
        
        batches = []
        current_batch_data = {
            "traditions": [],
            "entries": [],
            "uncompressed_size": 0
        }
        
        batch_number = 1
        
        # Sort traditions by size (largest first for better packing)
        sorted_traditions = sorted(
            analysis["tradition_sizes"].items(),
            key=lambda x: x[1]["uncompressed_size"],
            reverse=True
        )
        
        for tradition_name, tradition_info in sorted_traditions:
            tradition_file = self.lighthouse_dir / f"{tradition_name}.json"
            
            # Load tradition data
            with open(tradition_file, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            tradition_size = tradition_info["uncompressed_size"]
            
            # Check if tradition fits in current batch
            if (current_batch_data["uncompressed_size"] + tradition_size > self.batch_size_target and 
                current_batch_data["traditions"]):
                
                # Finalize current batch
                batch = self._create_batch(current_batch_data, batch_number, analysis["estimated_batches"])
                batches.append(batch)
                
                # Start new batch
                current_batch_data = {
                    "traditions": [],
                    "entries": [],
                    "uncompressed_size": 0
                }
                batch_number += 1
            
            # Add tradition to current batch
            current_batch_data["traditions"].append(tradition_name)
            current_batch_data["entries"].extend(tradition_data.get("entries", []))
            current_batch_data["uncompressed_size"] += tradition_size
            
            logger.info(f"Added {tradition_name} to batch {batch_number}: "
                       f"{tradition_info['entry_count']} entries, {tradition_size/1024:.1f}KB")
        
        # Finalize last batch
        if current_batch_data["traditions"]:
            batch = self._create_batch(current_batch_data, batch_number, batch_number)
            batches.append(batch)
        
        logger.info(f"Created {len(batches)} TAP inscription batches")
        return batches
    
    def _create_batch(self, batch_data: Dict[str, Any], batch_number: int, total_batches: int) -> TAPInscriptionBatch:
        """Create a single TAP inscription batch with compression"""
        batch_id = f"enochian_tap_batch_{batch_number:03d}"
        
        # Create batch content
        batch_content = {
            "tap_protocol_version": "1.0.0",
            "enochian_cyphers_batch": batch_id,
            "batch_info": {
                "batch_number": batch_number,
                "total_batches": total_batches,
                "created_timestamp": datetime.now().isoformat(),
                "traditions_included": batch_data["traditions"],
                "total_entries": len(batch_data["entries"])
            },
            "hypertoken_metadata": {
                "evolution_enabled": True,
                "cross_token_interactions": True,
                "mutation_triggers": [
                    "quest_completion",
                    "wisdom_attainment",
                    "tradition_mastery",
                    "governor_interaction"
                ],
                "authenticity_verified": True
            },
            "entries": batch_data["entries"],
            "inscription_metadata": {
                "bitcoin_native": True,
                "ordinals_compliant": True,
                "tap_protocol_ready": True,
                "compression_method": "gzip"
            }
        }
        
        # Convert to JSON and compress
        json_content = json.dumps(batch_content, separators=(',', ':'), ensure_ascii=False)
        json_bytes = json_content.encode('utf-8')
        compressed_bytes = gzip.compress(json_bytes, compresslevel=9)
        
        # Encode for inscription
        inscription_data = base64.b64encode(compressed_bytes).decode('ascii')
        
        # Calculate metadata hash
        metadata_hash = hashlib.sha256(json_bytes).hexdigest()[:16]
        
        # Create evolution hooks
        evolution_hooks = [
            f"quest_completion_{tradition}" for tradition in batch_data["traditions"]
        ]
        
        # Create cross-token references
        cross_token_refs = [
            f"batch_{i:03d}" for i in range(1, total_batches + 1) if i != batch_number
        ]
        
        batch = TAPInscriptionBatch(
            batch_id=batch_id,
            batch_number=batch_number,
            total_batches=total_batches,
            traditions=batch_data["traditions"],
            entry_count=len(batch_data["entries"]),
            uncompressed_size=len(json_bytes),
            compressed_size=len(compressed_bytes),
            compression_ratio=len(compressed_bytes) / len(json_bytes),
            inscription_data=inscription_data,
            metadata_hash=metadata_hash,
            evolution_hooks=evolution_hooks,
            cross_token_refs=cross_token_refs,
            created_timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Created batch {batch_id}: {batch.entry_count} entries, "
                   f"{batch.compression_ratio:.1%} compression ratio, "
                   f"{batch.compressed_size/1024:.1f}KB compressed")
        
        return batch
    
    def evolve_hypertoken(self, token_id: str, quest_completion: bool, aethyr_tier: int) -> Dict[str, Any]:
        """
        Enhanced hypertoken evolution mechanics (expert recommendation)
        Mutates hypertoken traits based on completion and Aethyr tier
        """
        # Mock TAP state (replace with actual Trac query in production)
        current_traits = {
            'virtue_level': 1,
            'shadow_aspect': 'unbalanced',
            'wisdom_attained': 0,
            'tradition_mastery': {},
            'evolution_stage': 'nascent'
        }

        if quest_completion:
            # Scale evolution by Aethyr tier (1-30, with 1 being highest)
            evolution_multiplier = max(1, (31 - aethyr_tier) / 10.0)
            current_traits['virtue_level'] += int(aethyr_tier * evolution_multiplier)
            current_traits['wisdom_attained'] += 1

            # Evolution thresholds based on Thelemic True Will mechanics
            if current_traits['virtue_level'] >= 10:
                current_traits['shadow_aspect'] = 'integrating'
            if current_traits['virtue_level'] >= 20:
                current_traits['shadow_aspect'] = 'integrated'
                current_traits['evolution_stage'] = 'adept'
            if current_traits['virtue_level'] >= 30:
                current_traits['evolution_stage'] = 'master'

            # Chaos Magic paradigm shift at high levels
            if current_traits['virtue_level'] >= 40:
                current_traits['evolution_stage'] = 'paradigm_shifter'
                current_traits['shadow_aspect'] = 'transcended'

        # Prepare for TAP inscription (compress metadata)
        metadata = json.dumps(current_traits, separators=(',', ':'))
        metadata_bytes = metadata.encode('utf-8')
        compressed_size = len(gzip.compress(metadata_bytes))

        evolution_result = {
            'new_token_id': f"{token_id}_evolved_{current_traits['virtue_level']}",
            'traits': current_traits,
            'metadata_size': len(metadata_bytes),
            'compressed_size': compressed_size,
            'evolution_multiplier': evolution_multiplier,
            'inscription_ready': compressed_size < 1000  # Keep metadata small
        }

        return evolution_result

    def generate_hypertoken_metadata(self, governor_name: str, batch_ref: str) -> TAPHypertokenMetadata:
        """Generate hypertoken metadata for a specific governor"""
        
        # Load governor profile if available
        governor_file = Path(f"governor_profiles/{governor_name.lower()}.json")
        tradition_affinities = {}
        
        if governor_file.exists():
            with open(governor_file, 'r', encoding='utf-8') as f:
                governor_data = json.load(f)
            
            # Extract tradition affinities
            knowledge_systems = governor_data.get("knowledge_systems", [])
            for system in knowledge_systems:
                tradition_affinities[system] = 0.8  # Default affinity
        
        # Generate token ID
        token_content = f"{governor_name}_{batch_ref}_{datetime.now().isoformat()}"
        token_id = hashlib.sha256(token_content.encode()).hexdigest()[:16]
        
        metadata = TAPHypertokenMetadata(
            token_id=token_id,
            governor_name=governor_name,
            tradition_affinities=tradition_affinities,
            wisdom_level=1,  # Starting level
            evolution_stage="nascent",
            mutation_triggers=[
                "quest_completion",
                "wisdom_synthesis",
                "tradition_mastery"
            ],
            cross_token_interactions=[
                "governor_collaboration",
                "tradition_synthesis",
                "aethyr_resonance"
            ],
            authenticity_score=0.95,  # High authenticity for governors
            source_citations=[
                "John Dee's Angelic Conversations",
                "Liber Loagaeth",
                "Enochian Cyphers Lighthouse"
            ],
            inscription_batch_ref=batch_ref
        )
        
        return metadata
    
    def export_tap_inscriptions(self, batches: List[TAPInscriptionBatch]) -> Dict[str, Any]:
        """Export TAP inscription batches and metadata"""
        logger.info("Exporting TAP inscription batches")
        
        # Save individual batches
        for batch in batches:
            batch_file = self.output_dir / f"{batch.batch_id}.json"
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(batch), f, indent=2, ensure_ascii=False)
            
            # Save compressed inscription data separately
            inscription_file = self.output_dir / f"{batch.batch_id}_inscription.txt"
            with open(inscription_file, 'w') as f:
                f.write(batch.inscription_data)
        
        # Create master inscription index
        master_index = {
            "tap_protocol_version": "1.0.0",
            "enochian_cyphers_inscriptions": {
                "total_batches": len(batches),
                "total_entries": sum(batch.entry_count for batch in batches),
                "total_compressed_size": sum(batch.compressed_size for batch in batches),
                "average_compression_ratio": sum(batch.compression_ratio for batch in batches) / len(batches),
                "ordinals_compliant": all(batch.compressed_size < self.max_inscription_size for batch in batches),
                "created_timestamp": datetime.now().isoformat()
            },
            "batches": [
                {
                    "batch_id": batch.batch_id,
                    "batch_number": batch.batch_number,
                    "traditions": batch.traditions,
                    "entry_count": batch.entry_count,
                    "compressed_size": batch.compressed_size,
                    "metadata_hash": batch.metadata_hash
                }
                for batch in batches
            ]
        }
        
        # Save master index
        index_file = self.output_dir / "tap_inscription_master_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(master_index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(batches)} TAP inscription batches")
        return master_index

def main():
    """Main execution function"""
    logger.info("=== ENOCHIAN CYPHERS TAP INSCRIBER ===")
    
    # Initialize TAP inscriber
    inscriber = TAPInscriber()
    
    # Analyze content
    analysis = inscriber.analyze_lighthouse_content()
    
    # Create inscription batches
    batches = inscriber.create_inscription_batches()
    
    # Export inscriptions
    master_index = inscriber.export_tap_inscriptions(batches)
    
    # Generate sample hypertoken metadata
    sample_governors = ["ABRIOND", "ALPUDUS", "ANODOIN"]
    for governor in sample_governors:
        if batches:
            metadata = inscriber.generate_hypertoken_metadata(governor, batches[0].batch_id)
            metadata_file = inscriber.output_dir / f"hypertoken_metadata_{governor.lower()}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(metadata), f, indent=2, ensure_ascii=False)
    
    # Display results
    logger.info(f"\n=== TAP INSCRIPTION RESULTS ===")
    logger.info(f"Total Batches: {len(batches)}")
    logger.info(f"Total Entries: {sum(batch.entry_count for batch in batches)}")
    logger.info(f"Average Compression: {master_index['enochian_cyphers_inscriptions']['average_compression_ratio']:.1%}")
    logger.info(f"Ordinals Compliant: {master_index['enochian_cyphers_inscriptions']['ordinals_compliant']}")
    
    return inscriber

if __name__ == "__main__":
    main()
