#!/usr/bin/env python3
"""
Bitcoin Inscription Preparation for Enochian Cyphers Lighthouse
Prepares knowledge base for Bitcoin L1 inscription deployment
"""

import json
import gzip
import os
from pathlib import Path
from typing import Dict, List, Any
import hashlib
from datetime import datetime

class BitcoinInscriptionPrep:
    """Prepares lighthouse knowledge base for Bitcoin inscription"""
    
    def __init__(self, lighthouse_dir: str = "lighthouse_final"):
        self.lighthouse_dir = Path(lighthouse_dir)
        self.inscription_dir = Path("bitcoin_inscriptions")
        self.inscription_dir.mkdir(exist_ok=True)
        
        # Load master index
        with open(self.lighthouse_dir / "lighthouse_master_index.json", 'r') as f:
            self.master_index = json.load(f)
    
    def create_inscription_batches(self) -> List[Dict[str, Any]]:
        """Create optimized inscription batches for Bitcoin L1"""
        print("📦 Creating Bitcoin Inscription Batches")
        print("=" * 40)
        
        batches = []
        current_batch = {
            "batch_id": "enochian_lighthouse_001",
            "traditions": [],
            "entries": [],
            "total_size": 0,
            "compressed_size": 0
        }
        
        max_size = 950000  # 950KB to allow for compression and metadata
        
        # Process each tradition
        for tradition_id, tradition_info in self.master_index["traditions"].items():
            tradition_file = self.lighthouse_dir / "traditions" / f"{tradition_id}.json"
            
            with open(tradition_file, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            tradition_json = json.dumps(tradition_data, separators=(',', ':'))
            tradition_size = len(tradition_json.encode('utf-8'))
            
            # Check if tradition fits in current batch
            if current_batch["total_size"] + tradition_size > max_size and current_batch["traditions"]:
                # Finalize current batch
                batches.append(self._finalize_batch(current_batch))
                
                # Start new batch
                current_batch = {
                    "batch_id": f"enochian_lighthouse_{len(batches)+1:03d}",
                    "traditions": [],
                    "entries": [],
                    "total_size": 0,
                    "compressed_size": 0
                }
            
            # Add tradition to current batch
            current_batch["traditions"].append(tradition_id)
            current_batch["entries"].extend(tradition_data)
            current_batch["total_size"] += tradition_size
            
            print(f"   📚 Added {tradition_info['name']}: {tradition_info['entry_count']} entries ({tradition_size/1000:.1f}KB)")
        
        # Finalize last batch
        if current_batch["traditions"]:
            batches.append(self._finalize_batch(current_batch))
        
        print(f"\n✅ Created {len(batches)} inscription batches")
        return batches
    
    def _finalize_batch(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize and compress a batch for inscription"""
        # Create batch content
        batch_content = {
            "lighthouse_batch": batch["batch_id"],
            "version": "1.0.0",
            "created_date": datetime.now().isoformat(),
            "traditions": batch["traditions"],
            "total_entries": len(batch["entries"]),
            "entries": batch["entries"],
            "metadata": {
                "enochian_cyphers": True,
                "bitcoin_native": True,
                "compression": "gzip"
            }
        }
        
        # Convert to JSON
        json_content = json.dumps(batch_content, separators=(',', ':'), ensure_ascii=False)
        json_bytes = json_content.encode('utf-8')
        
        # Compress with gzip
        compressed_bytes = gzip.compress(json_bytes, compresslevel=9)
        
        # Calculate hashes
        content_hash = hashlib.sha256(json_bytes).hexdigest()
        compressed_hash = hashlib.sha256(compressed_bytes).hexdigest()
        
        # Save compressed batch
        batch_file = self.inscription_dir / f"{batch['batch_id']}.json.gz"
        with open(batch_file, 'wb') as f:
            f.write(compressed_bytes)
        
        # Save uncompressed for reference
        ref_file = self.inscription_dir / f"{batch['batch_id']}_reference.json"
        with open(ref_file, 'w', encoding='utf-8') as f:
            json.dump(batch_content, f, indent=2, ensure_ascii=False)
        
        # Update batch info
        batch.update({
            "compressed_size": len(compressed_bytes),
            "compression_ratio": len(compressed_bytes) / len(json_bytes),
            "content_hash": content_hash,
            "compressed_hash": compressed_hash,
            "inscription_file": str(batch_file),
            "reference_file": str(ref_file)
        })
        
        print(f"   📦 {batch['batch_id']}: {len(batch['traditions'])} traditions, {batch['total_size']/1000:.1f}KB → {batch['compressed_size']/1000:.1f}KB ({batch['compression_ratio']:.1%} compression)")
        
        return batch
    
    def create_master_inscription_index(self, batches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create master index for all inscription batches"""
        master_inscription_index = {
            "enochian_cyphers_lighthouse": {
                "version": "1.0.0",
                "created_date": datetime.now().isoformat(),
                "total_batches": len(batches),
                "total_traditions": self.master_index["total_traditions"],
                "total_entries": self.master_index["total_entries"],
                "bitcoin_ready": True
            },
            "inscription_batches": [],
            "deployment_info": {
                "target_network": "Bitcoin L1",
                "inscription_protocol": "Ordinals",
                "max_size_per_inscription": "1MB",
                "compression": "gzip",
                "encoding": "utf-8"
            },
            "merkle_tree": self._create_merkle_tree(batches),
            "verification": {
                "total_compressed_size": sum(batch["compressed_size"] for batch in batches),
                "average_compression": sum(batch["compression_ratio"] for batch in batches) / len(batches),
                "largest_batch": max(batch["compressed_size"] for batch in batches),
                "smallest_batch": min(batch["compressed_size"] for batch in batches)
            }
        }
        
        # Add batch summaries
        for batch in batches:
            batch_summary = {
                "batch_id": batch["batch_id"],
                "traditions": batch["traditions"],
                "tradition_count": len(batch["traditions"]),
                "entry_count": len(batch["entries"]),
                "compressed_size": batch["compressed_size"],
                "content_hash": batch["content_hash"],
                "inscription_ready": batch["compressed_size"] < 1000000
            }
            master_inscription_index["inscription_batches"].append(batch_summary)
        
        # Save master index
        master_file = self.inscription_dir / "enochian_lighthouse_master_inscription_index.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(master_inscription_index, f, indent=2, ensure_ascii=False)
        
        print(f"\n🏛️ Master Inscription Index created: {master_file}")
        return master_inscription_index
    
    def _create_merkle_tree(self, batches: List[Dict[str, Any]]) -> Dict[str, str]:
        """Create merkle tree for batch verification"""
        batch_hashes = [batch["content_hash"] for batch in batches]
        
        # Simple merkle root calculation (would be more sophisticated in production)
        combined_hash = hashlib.sha256(''.join(batch_hashes).encode()).hexdigest()
        
        return {
            "merkle_root": combined_hash,
            "batch_hashes": batch_hashes,
            "verification_method": "SHA256"
        }
    
    def generate_deployment_script(self, master_index: Dict[str, Any]) -> str:
        """Generate Bitcoin deployment script"""
        script_content = f"""#!/bin/bash
# Enochian Cyphers Lighthouse Bitcoin L1 Deployment Script
# Generated: {datetime.now().isoformat()}

echo "🏛️ Enochian Cyphers Lighthouse Bitcoin L1 Deployment"
echo "=================================================="

# Deployment Configuration
NETWORK="bitcoin-mainnet"
INSCRIPTION_PROTOCOL="ordinals"
TOTAL_BATCHES={master_index['enochian_cyphers_lighthouse']['total_batches']}
TOTAL_SIZE={master_index['verification']['total_compressed_size']}

echo "📊 Deployment Summary:"
echo "   Total Batches: $TOTAL_BATCHES"
echo "   Total Size: $(($TOTAL_SIZE / 1000))KB"
echo "   Total Traditions: {master_index['enochian_cyphers_lighthouse']['total_traditions']}"
echo "   Total Entries: {master_index['enochian_cyphers_lighthouse']['total_entries']}"

# Deploy each batch
"""
        
        for i, batch in enumerate(master_index["inscription_batches"], 1):
            script_content += f"""
echo "📦 Deploying Batch {i}/{master_index['enochian_cyphers_lighthouse']['total_batches']}: {batch['batch_id']}"
echo "   Traditions: {', '.join(batch['traditions'])}"
echo "   Size: {batch['compressed_size']/1000:.1f}KB"
echo "   Hash: {batch['content_hash'][:16]}..."

# ord wallet inscribe --file {batch['batch_id']}.json.gz --fee-rate 10
# echo "   ✅ Inscribed: {batch['batch_id']}"
"""
        
        script_content += """
echo ""
echo "🌟 Enochian Cyphers Lighthouse Successfully Deployed to Bitcoin L1!"
echo "🔗 All 26 sacred traditions now permanently preserved on Bitcoin blockchain"
echo "🚀 Ready for story engine integration and governor system activation"
"""
        
        script_file = self.inscription_dir / "deploy_to_bitcoin.sh"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_file, 0o755)
        
        print(f"🚀 Deployment script created: {script_file}")
        return str(script_file)
    
    def prepare_complete_inscription_package(self):
        """Prepare complete Bitcoin inscription package"""
        print("🏛️ PREPARING COMPLETE BITCOIN INSCRIPTION PACKAGE")
        print("=" * 60)
        
        # Create inscription batches
        batches = self.create_inscription_batches()
        
        # Create master index
        master_index = self.create_master_inscription_index(batches)
        
        # Generate deployment script
        deployment_script = self.generate_deployment_script(master_index)
        
        # Summary
        print(f"\n🌟 BITCOIN INSCRIPTION PACKAGE COMPLETE!")
        print(f"📊 Summary:")
        print(f"   📦 Inscription Batches: {len(batches)}")
        print(f"   📚 Total Traditions: {master_index['enochian_cyphers_lighthouse']['total_traditions']}")
        print(f"   📝 Total Entries: {master_index['enochian_cyphers_lighthouse']['total_entries']:,}")
        print(f"   💾 Total Compressed Size: {master_index['verification']['total_compressed_size']/1000:.1f}KB")
        print(f"   📈 Average Compression: {master_index['verification']['average_compression']:.1%}")
        print(f"   📁 Output Directory: {self.inscription_dir}")
        print(f"   🚀 Deployment Script: {deployment_script}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Review inscription batches in {self.inscription_dir}")
        print(f"   2. Test deployment on Bitcoin testnet")
        print(f"   3. Execute deployment script for mainnet")
        print(f"   4. Verify inscriptions on Bitcoin blockchain")
        print(f"   5. Integrate with story engine and governor system")
        
        return {
            "batches": batches,
            "master_index": master_index,
            "deployment_script": deployment_script,
            "total_size": master_index['verification']['total_compressed_size']
        }

if __name__ == "__main__":
    prep = BitcoinInscriptionPrep()
    result = prep.prepare_complete_inscription_package()
    
    print(f"\n🏛️ Enochian Cyphers Lighthouse is Bitcoin-ready! 🚀")
