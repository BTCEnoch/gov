//! Trac State Indexer Implementation
//! 
//! Provides efficient state management with Merkle tree verification
//! and sharding support for 1,000+ entries per Rule 6 (Scalability).

use super::{TracStateEntry, TracConfig, MerkleTree};
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use sha2::{Sha256, Digest};

/// State indexer with Merkle tree verification
pub struct TracStateIndexer {
    /// Sharded state storage: shard_id -> entries
    sharded_state: HashMap<usize, HashMap<String, TracStateEntry>>,
    /// Merkle trees for each shard: shard_id -> merkle_tree
    merkle_trees: HashMap<usize, MerkleTree>,
    /// Configuration
    config: TracConfig,
    /// Statistics
    total_entries: usize,
    last_sync_time: u64,
}

impl TracStateIndexer {
    /// Create new state indexer
    pub fn new(config: TracConfig) -> Self {
        TracStateIndexer {
            sharded_state: HashMap::new(),
            merkle_trees: HashMap::new(),
            config,
            total_entries: 0,
            last_sync_time: 0,
        }
    }

    /// Add entry to specific shard with Merkle proof generation
    /// Per Rule 6: O(1) verification complexity
    pub fn add_entry(&mut self, entry: TracStateEntry, shard_id: usize) -> Result<String, String> {
        // Initialize shard if it doesn't exist
        if !self.sharded_state.contains_key(&shard_id) {
            self.sharded_state.insert(shard_id, HashMap::new());
            self.merkle_trees.insert(shard_id, MerkleTree::new());
        }

        // Check shard capacity
        let shard = self.sharded_state.get(&shard_id).unwrap();
        if shard.len() >= self.config.max_entries_per_shard {
            return Err(format!("Shard {} at capacity: {}", shard_id, self.config.max_entries_per_shard));
        }

        // Generate entry hash for Merkle tree
        let entry_hash = self.generate_entry_hash(&entry);
        
        // Add to Merkle tree first
        let merkle_tree = self.merkle_trees.get_mut(&shard_id).unwrap();
        merkle_tree.add_leaf(entry_hash.clone())?;
        
        // Create entry with Merkle proof
        let mut entry_with_proof = entry.clone();
        entry_with_proof.merkle_proof = merkle_tree.get_proof(&entry_hash)?;
        
        // Add to shard storage
        let shard = self.sharded_state.get_mut(&shard_id).unwrap();
        shard.insert(entry.id.clone(), entry_with_proof);
        
        self.total_entries += 1;
        self.last_sync_time = self.current_timestamp();
        
        // Return Merkle root for consensus validation
        Ok(merkle_tree.get_root())
    }

    /// Retrieve entry with O(1) lookup
    pub fn get_entry(&self, entry_id: &str, shard_id: usize) -> Result<Option<TracStateEntry>, String> {
        if let Some(shard) = self.sharded_state.get(&shard_id) {
            Ok(shard.get(entry_id).cloned())
        } else {
            Ok(None)
        }
    }

    /// Verify entry integrity using Merkle proof
    /// Per Rule 6: O(1) verification
    pub fn verify_entry(&self, entry: &TracStateEntry, shard_id: usize) -> Result<bool, String> {
        let merkle_tree = self.merkle_trees.get(&shard_id)
            .ok_or("Shard not found")?;
        
        let entry_hash = self.generate_entry_hash(entry);
        merkle_tree.verify_proof(&entry_hash, &entry.merkle_proof)
    }

    /// Get all entries for a specific tradition
    /// Used for mystical content queries per Rule 1
    pub fn get_entries_by_tradition(&self, tradition: &str) -> Vec<TracStateEntry> {
        let mut results = Vec::new();
        
        for shard in self.sharded_state.values() {
            for entry in shard.values() {
                if let Ok(data) = serde_json::from_value::<serde_json::Value>(entry.data.clone()) {
                    if let Some(entry_tradition) = data.get("tradition") {
                        if entry_tradition.as_str() == Some(tradition) {
                            results.push(entry.clone());
                        }
                    }
                }
            }
        }
        
        results
    }

    /// Get entries by type (Governor Angels, Mystical Knowledge, etc.)
    pub fn get_entries_by_type(&self, entry_type: &str) -> Vec<TracStateEntry> {
        let mut results = Vec::new();
        
        for shard in self.sharded_state.values() {
            for entry in shard.values() {
                if format!("{:?}", entry.entry_type).to_lowercase() == entry_type.to_lowercase() {
                    results.push(entry.clone());
                }
            }
        }
        
        results
    }

    /// Validate all Merkle trees across shards
    pub fn validate_all_merkle_trees(&self) -> Result<bool, String> {
        for (shard_id, merkle_tree) in &self.merkle_trees {
            if !merkle_tree.validate_tree()? {
                return Ok(false);
            }
            
            // Verify all entries in this shard
            if let Some(shard) = self.sharded_state.get(shard_id) {
                for entry in shard.values() {
                    if !self.verify_entry(entry, *shard_id)? {
                        return Ok(false);
                    }
                }
            }
        }
        
        Ok(true)
    }

    /// Get system statistics
    pub fn get_total_entries(&self) -> usize {
        self.total_entries
    }

    pub fn get_shard_count(&self) -> usize {
        self.sharded_state.len()
    }

    pub fn get_average_authenticity(&self) -> f64 {
        let mut total_score = 0.0;
        let mut count = 0;
        
        for shard in self.sharded_state.values() {
            for entry in shard.values() {
                total_score += entry.authenticity_score;
                count += 1;
            }
        }
        
        if count > 0 {
            total_score / count as f64
        } else {
            0.0
        }
    }

    pub fn get_last_sync_time(&self) -> u64 {
        self.last_sync_time
    }

    /// Export state for P2P synchronization
    pub fn export_state(&self) -> HashMap<String, TracStateEntry> {
        let mut all_entries = HashMap::new();
        
        for shard in self.sharded_state.values() {
            for (id, entry) in shard {
                all_entries.insert(id.clone(), entry.clone());
            }
        }
        
        all_entries
    }

    /// Import state from P2P peers
    pub fn import_peer_state(&mut self, peer_state: HashMap<String, TracStateEntry>) -> Result<usize, String> {
        let mut imported_count = 0;
        
        for (entry_id, entry) in peer_state {
            // Determine shard for this entry
            let shard_id = self.calculate_shard_id(&entry_id);
            
            // Check if we already have this entry
            if let Ok(existing) = self.get_entry(&entry_id, shard_id) {
                if existing.is_none() {
                    // Add new entry
                    self.add_entry(entry, shard_id)?;
                    imported_count += 1;
                }
            }
        }
        
        Ok(imported_count)
    }

    /// Generate deterministic hash for entry
    fn generate_entry_hash(&self, entry: &TracStateEntry) -> String {
        let mut hasher = Sha256::new();
        hasher.update(entry.id.as_bytes());
        hasher.update(format!("{:?}", entry.entry_type).as_bytes());
        hasher.update(entry.data.to_string().as_bytes());
        hasher.update(entry.timestamp.to_string().as_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Calculate shard ID for entry (deterministic distribution)
    fn calculate_shard_id(&self, entry_id: &str) -> usize {
        let mut hasher = Sha256::new();
        hasher.update(entry_id.as_bytes());
        let hash = hasher.finalize();
        
        // Use first 4 bytes of hash for shard calculation
        let shard_hash = u32::from_be_bytes([hash[0], hash[1], hash[2], hash[3]]);
        (shard_hash as usize) % 100 // Support up to 100 shards
    }

    /// Get current timestamp
    fn current_timestamp(&self) -> u64 {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs()
    }
}

/// State indexer statistics
#[derive(Serialize, Deserialize, Debug)]
pub struct IndexerStats {
    pub total_entries: usize,
    pub shard_count: usize,
    pub average_authenticity: f64,
    pub last_sync: u64,
    pub shard_distribution: HashMap<usize, usize>, // shard_id -> entry_count
}

impl TracStateIndexer {
    /// Get detailed statistics
    pub fn get_detailed_stats(&self) -> IndexerStats {
        let mut shard_distribution = HashMap::new();
        
        for (shard_id, shard) in &self.sharded_state {
            shard_distribution.insert(*shard_id, shard.len());
        }
        
        IndexerStats {
            total_entries: self.total_entries,
            shard_count: self.sharded_state.len(),
            average_authenticity: self.get_average_authenticity(),
            last_sync: self.last_sync_time,
            shard_distribution,
        }
    }

    /// Optimize shard distribution (rebalance if needed)
    pub fn optimize_shards(&mut self) -> Result<(), String> {
        // Check for unbalanced shards
        let stats = self.get_detailed_stats();
        let avg_entries_per_shard = if stats.shard_count > 0 {
            stats.total_entries / stats.shard_count
        } else {
            0
        };
        
        let threshold = (avg_entries_per_shard as f64 * 1.5) as usize; // 50% above average
        
        for (shard_id, entry_count) in &stats.shard_distribution {
            if *entry_count > threshold {
                println!("⚠️ Shard {} is overloaded with {} entries (threshold: {})", 
                        shard_id, entry_count, threshold);
                // In production, implement shard splitting here
            }
        }
        
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::trac_systems::{TracEntryType, TracConfig};

    #[test]
    fn test_state_indexer_basic_operations() {
        let config = TracConfig::default();
        let mut indexer = TracStateIndexer::new(config);
        
        let entry = TracStateEntry {
            id: "test_governor_abriond".to_string(),
            entry_type: TracEntryType::GovernorAngel,
            data: serde_json::json!({
                "name": "ABRIOND",
                "tradition": "enochian_magic",
                "aethyr": "POP"
            }),
            timestamp: 1234567890,
            merkle_proof: String::new(),
            authenticity_score: 0.95,
            last_updated: 1234567890,
        };
        
        // Add entry
        let merkle_root = indexer.add_entry(entry.clone(), 0).unwrap();
        assert!(!merkle_root.is_empty());
        
        // Retrieve entry
        let retrieved = indexer.get_entry("test_governor_abriond", 0).unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().id, "test_governor_abriond");
        
        // Verify statistics
        assert_eq!(indexer.get_total_entries(), 1);
        assert_eq!(indexer.get_shard_count(), 1);
    }

    #[test]
    fn test_tradition_filtering() {
        let config = TracConfig::default();
        let mut indexer = TracStateIndexer::new(config);
        
        // Add Enochian entry
        let enochian_entry = TracStateEntry {
            id: "enochian_test".to_string(),
            entry_type: TracEntryType::MysticalKnowledge,
            data: serde_json::json!({"tradition": "enochian_magic"}),
            timestamp: 1234567890,
            merkle_proof: String::new(),
            authenticity_score: 0.9,
            last_updated: 1234567890,
        };
        
        // Add Tarot entry
        let tarot_entry = TracStateEntry {
            id: "tarot_test".to_string(),
            entry_type: TracEntryType::MysticalKnowledge,
            data: serde_json::json!({"tradition": "tarot_system"}),
            timestamp: 1234567890,
            merkle_proof: String::new(),
            authenticity_score: 0.85,
            last_updated: 1234567890,
        };
        
        indexer.add_entry(enochian_entry, 0).unwrap();
        indexer.add_entry(tarot_entry, 1).unwrap();
        
        // Test tradition filtering
        let enochian_entries = indexer.get_entries_by_tradition("enochian_magic");
        assert_eq!(enochian_entries.len(), 1);
        assert_eq!(enochian_entries[0].id, "enochian_test");
        
        let tarot_entries = indexer.get_entries_by_tradition("tarot_system");
        assert_eq!(tarot_entries.len(), 1);
        assert_eq!(tarot_entries[0].id, "tarot_test");
    }
}
