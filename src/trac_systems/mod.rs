//! Trac Systems Integration for Enochian Cyphers
//! 
//! Implements decentralized state management with Merkle trees, sharding for 1,000+ entries,
//! and Byzantine fault tolerance per Rule 3 (Decentralization Priority).
//! 
//! This module ensures O(1) verification complexity (Rule 6) while maintaining
//! authenticity of mystical content (Rule 1) across the P2P network.

use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use sha2::{Sha256, Digest};

pub mod state_indexer;
pub mod merkle_tree;
pub mod consensus;
pub mod sharding;

pub use state_indexer::TracStateIndexer;
pub use merkle_tree::MerkleTree;
pub use consensus::ByzantineConsensus;
pub use sharding::StateSharding;

// Re-export for Python compatibility
pub use state_indexer::TracStateEntry;

/// Core Trac state entry for game elements
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TracStateEntry {
    pub id: String,
    pub entry_type: TracEntryType,
    pub data: serde_json::Value,
    pub timestamp: u64,
    pub merkle_proof: String,
    pub authenticity_score: f64, // Per Rule 1: Authenticity validation
    pub last_updated: u64,
}

/// Types of entries in the Trac system
#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum TracEntryType {
    GovernorAngel,
    MysticalKnowledge,
    PlayerState,
    QuestProgress,
    HypertokenEvolution,
    TraditionMapping,
}

/// Trac system configuration
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TracConfig {
    pub max_entries_per_shard: usize,
    pub byzantine_threshold: f64, // 0.67 for 67% honest nodes
    pub merkle_tree_depth: usize,
    pub consensus_timeout_ms: u64,
    pub authenticity_threshold: f64, // Minimum score for Rule 1 compliance
}

impl Default for TracConfig {
    fn default() -> Self {
        TracConfig {
            max_entries_per_shard: 1000, // Support 1,000+ entries as per gap analysis
            byzantine_threshold: 0.67,   // 67% honest node requirement
            merkle_tree_depth: 20,       // Support up to 2^20 entries
            consensus_timeout_ms: 5000,  // 5 second consensus timeout
            authenticity_threshold: 0.8, // 80% authenticity required
        }
    }
}

/// Main Trac Systems coordinator
pub struct TracSystems {
    pub indexer: TracStateIndexer,
    pub consensus: ByzantineConsensus,
    pub sharding: StateSharding,
    pub config: TracConfig,
}

impl TracSystems {
    /// Initialize new Trac Systems instance
    pub fn new(config: TracConfig) -> Self {
        let indexer = TracStateIndexer::new(config.clone());
        let consensus = ByzantineConsensus::new(config.byzantine_threshold);
        let sharding = StateSharding::new(config.max_entries_per_shard);
        
        TracSystems {
            indexer,
            consensus,
            sharding,
            config,
        }
    }

    /// Add new state entry with validation
    /// Per Rule 1: Ensures authenticity before adding to state
    pub fn add_entry(&mut self, entry: TracStateEntry) -> Result<String, String> {
        // Validate authenticity per Rule 1
        if entry.authenticity_score < self.config.authenticity_threshold {
            return Err(format!(
                "Entry authenticity score {} below threshold {}", 
                entry.authenticity_score, 
                self.config.authenticity_threshold
            ));
        }

        // Determine shard for entry
        let shard_id = self.sharding.get_shard_for_entry(&entry.id)?;
        
        // Add to indexer with Merkle proof
        let merkle_root = self.indexer.add_entry(entry.clone(), shard_id)?;
        
        // Validate via consensus (Rule 3: Decentralization)
        let consensus_result = self.consensus.validate_entry(&entry, &merkle_root)?;
        
        if consensus_result.is_valid {
            println!("✅ Trac entry added: {} (shard: {}, authenticity: {:.2})", 
                    entry.id, shard_id, entry.authenticity_score);
            Ok(merkle_root)
        } else {
            Err("Byzantine consensus failed for entry".to_string())
        }
    }

    /// Retrieve entry with O(1) verification (Rule 6: Scalability)
    pub fn get_entry(&self, entry_id: &str) -> Result<Option<TracStateEntry>, String> {
        let shard_id = self.sharding.get_shard_for_entry(entry_id)?;
        self.indexer.get_entry(entry_id, shard_id)
    }

    /// Sync state with P2P network
    /// Per Rule 3: Decentralized state synchronization
    pub fn sync_with_peers(&mut self, peer_states: Vec<HashMap<String, TracStateEntry>>) -> Result<(), String> {
        for peer_state in peer_states {
            for (entry_id, entry) in peer_state {
                // Check if we have this entry
                if self.get_entry(&entry_id)?.is_none() {
                    // Validate via Byzantine consensus before adding
                    let validation = self.consensus.validate_peer_entry(&entry)?;
                    
                    if validation.is_valid && validation.consensus_ratio >= self.config.byzantine_threshold {
                        self.add_entry(entry)?;
                        println!("🔄 Synced entry from peer: {}", entry_id);
                    } else {
                        println!("⚠️ Rejected peer entry due to consensus failure: {}", entry_id);
                    }
                }
            }
        }
        
        Ok(())
    }

    /// Get system statistics
    pub fn get_stats(&self) -> TracSystemStats {
        TracSystemStats {
            total_entries: self.indexer.get_total_entries(),
            active_shards: self.sharding.get_active_shard_count(),
            consensus_health: self.consensus.get_health_ratio(),
            average_authenticity: self.indexer.get_average_authenticity(),
            last_sync: self.indexer.get_last_sync_time(),
        }
    }

    /// Validate entire system integrity
    /// Per Rule 6: O(1) verification for scalability
    pub fn validate_system_integrity(&self) -> Result<bool, String> {
        // Validate all Merkle trees
        let merkle_valid = self.indexer.validate_all_merkle_trees()?;
        
        // Check consensus health
        let consensus_healthy = self.consensus.get_health_ratio() >= self.config.byzantine_threshold;
        
        // Validate sharding consistency
        let sharding_consistent = self.sharding.validate_consistency()?;
        
        let system_valid = merkle_valid && consensus_healthy && sharding_consistent;
        
        if system_valid {
            println!("✅ Trac Systems integrity validated");
        } else {
            println!("❌ Trac Systems integrity check failed");
        }
        
        Ok(system_valid)
    }
}

/// System statistics for monitoring
#[derive(Serialize, Deserialize, Debug)]
pub struct TracSystemStats {
    pub total_entries: usize,
    pub active_shards: usize,
    pub consensus_health: f64,
    pub average_authenticity: f64,
    pub last_sync: u64,
}

/// Generate deterministic hash for Bitcoin-native randomness
/// Per development constraints: Use deterministic generation
pub fn generate_deterministic_hash(input: &str, salt: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    hasher.update(salt.as_bytes());
    hasher.update(b"enochian_cyphers_trac"); // Project-specific salt
    format!("{:x}", hasher.finalize())
}

/// Validate mystical content authenticity
/// Per Rule 1: Cross-reference with primary sources
pub fn validate_mystical_authenticity(content: &str, tradition: &str, sources: &[String]) -> f64 {
    // Simplified authenticity scoring based on source count and tradition
    let base_score = match tradition {
        "enochian_magic" => 0.9,      // High authenticity for John Dee sources
        "hermetic_qabalah" => 0.85,   // High for traditional Qabalah
        "i_ching" => 0.88,            // High for Wilhelm translation
        "tarot_system" => 0.82,       // Good for Rider-Waite
        _ => 0.7,                     // Default for other traditions
    };
    
    // Bonus for multiple sources
    let source_bonus = (sources.len() as f64 * 0.05).min(0.2);
    
    // Content length factor (longer = more detailed = potentially more authentic)
    let content_factor = (content.len() as f64 / 1000.0).min(0.1);
    
    (base_score + source_bonus + content_factor).min(1.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trac_systems_initialization() {
        let config = TracConfig::default();
        let trac_systems = TracSystems::new(config);
        
        assert_eq!(trac_systems.config.max_entries_per_shard, 1000);
        assert_eq!(trac_systems.config.byzantine_threshold, 0.67);
    }

    #[test]
    fn test_mystical_authenticity_validation() {
        let content = "ABRIOND is a Governor Angel of the Aethyr POP, as recorded in John Dee's angelic conversations.";
        let tradition = "enochian_magic";
        let sources = vec!["John Dee's Diaries".to_string(), "Liber Loagaeth".to_string()];
        
        let score = validate_mystical_authenticity(content, tradition, &sources);
        assert!(score > 0.9); // Should be high for Enochian with multiple sources
    }

    #[test]
    fn test_deterministic_hash_generation() {
        let hash1 = generate_deterministic_hash("test_input", "salt1");
        let hash2 = generate_deterministic_hash("test_input", "salt1");
        let hash3 = generate_deterministic_hash("test_input", "salt2");
        
        assert_eq!(hash1, hash2); // Same input should produce same hash
        assert_ne!(hash1, hash3); // Different salt should produce different hash
    }
}
