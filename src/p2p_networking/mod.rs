//! P2P Networking Module for Enochian Cyphers
//! 
//! Implements Kademlia DHT with Byzantine fault tolerance per Rule 3 (Decentralization Priority).
//! Provides offline-first architecture with P2P state synchronization.
//! 
//! This module ensures zero server dependencies while maintaining 67% honest node threshold
//! for network security and consensus.

use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use sha2::{Sha256, Digest};

pub mod kademlia_dht;
pub mod byzantine_consensus;
pub mod peer_discovery;
pub mod state_sync;

pub use kademlia_dht::{KademliaDHT, PeerNode, StorageResult};
pub use byzantine_consensus::ByzantineConsensus;
pub use peer_discovery::PeerDiscovery;
pub use state_sync::StateSync;

/// Peer node in the P2P network
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PeerNode {
    pub node_id: String,        // 160-bit Kademlia ID
    pub address: String,        // Network address (IP:Port or Bitcoin address)
    pub port: u16,
    pub last_seen: u64,
    pub reputation: f64,        // 0.0 to 1.0 for Byzantine fault tolerance
    pub capabilities: Vec<String>, // Services this peer provides
    pub distance: Option<u64>,  // XOR distance from local node
    pub is_trusted: bool,       // Manually trusted peers
}

/// Network message types
#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum NetworkMessage {
    Ping { timestamp: u64 },
    Pong { timestamp: u64 },
    FindNode { target_id: String },
    FindNodeResponse { nodes: Vec<PeerNode> },
    Store { key: String, value: String },
    StoreResponse { success: bool },
    FindValue { key: String },
    FindValueResponse { value: Option<String>, nodes: Vec<PeerNode> },
    StateSync { state_hash: String, entries: Vec<String> },
    StateSyncResponse { accepted: bool, conflicts: Vec<String> },
    ConsensusProposal { proposal_id: String, data: String },
    ConsensusVote { proposal_id: String, vote: bool, signature: String },
}

/// P2P network configuration
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct P2PConfig {
    pub k_bucket_size: usize,           // Kademlia k parameter (typically 20)
    pub alpha: usize,                   // Concurrency parameter (typically 3)
    pub byzantine_threshold: f64,       // 0.67 for 67% honest nodes
    pub reputation_threshold: f64,      // Minimum reputation to trust peer
    pub ping_timeout_ms: u64,          // Ping timeout in milliseconds
    pub consensus_timeout_ms: u64,      // Consensus timeout
    pub max_peers: usize,               // Maximum number of peers to maintain
    pub bootstrap_nodes: Vec<String>,   // Initial bootstrap nodes
}

impl Default for P2PConfig {
    fn default() -> Self {
        P2PConfig {
            k_bucket_size: 20,
            alpha: 3,
            byzantine_threshold: 0.67,
            reputation_threshold: 0.5,
            ping_timeout_ms: 5000,
            consensus_timeout_ms: 10000,
            max_peers: 200,
            bootstrap_nodes: Vec::new(),
        }
    }
}

/// Main P2P networking coordinator
pub struct P2PNetwork {
    pub local_node_id: String,
    pub dht: KademliaDHT,
    pub consensus: ByzantineConsensus,
    pub peer_discovery: PeerDiscovery,
    pub state_sync: StateSync,
    pub config: P2PConfig,
    pub is_online: bool,
}

impl P2PNetwork {
    /// Initialize new P2P network
    pub fn new(config: P2PConfig) -> Self {
        let local_node_id = Self::generate_node_id();
        let dht = KademliaDHT::new(local_node_id.clone(), config.clone());
        let consensus = ByzantineConsensus::new(config.byzantine_threshold);
        let peer_discovery = PeerDiscovery::new(config.clone());
        let state_sync = StateSync::new(local_node_id.clone());
        
        println!("🌐 P2P Network initialized with node ID: {}", &local_node_id[..16]);
        
        P2PNetwork {
            local_node_id,
            dht,
            consensus,
            peer_discovery,
            state_sync,
            config,
            is_online: false,
        }
    }

    /// Start P2P network (connect to bootstrap nodes)
    /// Per Rule 3: Decentralized network initialization
    pub fn start(&mut self) -> Result<(), String> {
        println!("🚀 Starting P2P network...");
        
        // Connect to bootstrap nodes
        for bootstrap_addr in &self.config.bootstrap_nodes.clone() {
            match self.connect_to_bootstrap(bootstrap_addr) {
                Ok(_) => println!("✅ Connected to bootstrap node: {}", bootstrap_addr),
                Err(e) => println!("⚠️ Failed to connect to bootstrap {}: {}", bootstrap_addr, e),
            }
        }
        
        // Start peer discovery
        self.peer_discovery.start_discovery()?;
        
        // Initialize DHT
        self.dht.bootstrap()?;
        
        self.is_online = true;
        println!("✅ P2P network online with {} peers", self.dht.get_peer_count());
        
        Ok(())
    }

    /// Stop P2P network gracefully
    pub fn stop(&mut self) -> Result<(), String> {
        println!("🛑 Stopping P2P network...");
        
        self.peer_discovery.stop_discovery()?;
        self.dht.shutdown()?;
        self.is_online = false;
        
        println!("✅ P2P network stopped");
        Ok(())
    }

    /// Store data in DHT with replication
    /// Per Rule 3: Decentralized data storage
    pub fn store_data(&mut self, key: &str, value: &str) -> Result<bool, String> {
        if !self.is_online {
            return Err("Network is offline".to_string());
        }
        
        // Store in DHT with Byzantine consensus
        let storage_result = self.dht.store(key, value)?;
        
        if storage_result.replica_count >= self.calculate_min_replicas() {
            // Validate via consensus
            let consensus_result = self.consensus.validate_storage(key, value, &storage_result.storing_peers)?;
            
            if consensus_result.is_valid {
                println!("💾 Data stored: {} (replicas: {})", key, storage_result.replica_count);
                Ok(true)
            } else {
                Err("Byzantine consensus failed for storage".to_string())
            }
        } else {
            Err(format!("Insufficient replicas: {} < {}", 
                       storage_result.replica_count, 
                       self.calculate_min_replicas()))
        }
    }

    /// Retrieve data from DHT with consensus validation
    pub fn retrieve_data(&mut self, key: &str) -> Result<Option<String>, String> {
        if !self.is_online {
            return Err("Network is offline".to_string());
        }
        
        // Retrieve from multiple peers
        let retrieval_results = self.dht.find_value(key)?;
        
        if retrieval_results.is_empty() {
            return Ok(None);
        }
        
        // Use Byzantine consensus to determine correct value
        let consensus_value = self.consensus.resolve_retrieval_conflicts(&retrieval_results)?;
        
        Ok(Some(consensus_value))
    }

    /// Synchronize game state with peers
    /// Per Rule 3: Decentralized state management
    pub fn sync_game_state(&mut self, local_state_hash: &str, 
                          state_entries: &[String]) -> Result<SyncResult, String> {
        if !self.is_online {
            return Err("Network is offline".to_string());
        }
        
        println!("🔄 Starting game state synchronization...");
        
        // Get peer state hashes
        let peer_states = self.query_peer_state_hashes()?;
        
        // Identify conflicts
        let mut conflicts = Vec::new();
        for (peer_id, peer_hash) in &peer_states {
            if peer_hash != local_state_hash {
                conflicts.push(peer_id.clone());
            }
        }
        
        if conflicts.is_empty() {
            println!("✅ All peers in sync");
            return Ok(SyncResult {
                status: SyncStatus::InSync,
                conflicts_resolved: 0,
                entries_updated: 0,
            });
        }
        
        println!("⚠️ Found {} state conflicts", conflicts.len());
        
        // Resolve conflicts via Byzantine consensus
        let resolution = self.state_sync.resolve_conflicts(&conflicts, state_entries)?;
        
        // Apply consensus resolution
        let consensus_result = self.consensus.validate_state_resolution(&resolution)?;
        
        if consensus_result.is_valid {
            println!("✅ State conflicts resolved via consensus");
            Ok(SyncResult {
                status: SyncStatus::Resolved,
                conflicts_resolved: conflicts.len(),
                entries_updated: resolution.updated_entries.len(),
            })
        } else {
            println!("❌ Failed to reach consensus on state resolution");
            Ok(SyncResult {
                status: SyncStatus::Failed,
                conflicts_resolved: 0,
                entries_updated: 0,
            })
        }
    }

    /// Get network statistics
    pub fn get_network_stats(&self) -> NetworkStats {
        NetworkStats {
            local_node_id: self.local_node_id.clone(),
            is_online: self.is_online,
            peer_count: self.dht.get_peer_count(),
            trusted_peer_count: self.dht.get_trusted_peer_count(),
            average_reputation: self.dht.get_average_reputation(),
            consensus_health: self.consensus.get_health_ratio(),
            last_sync: self.state_sync.get_last_sync_time(),
            network_latency_ms: self.peer_discovery.get_average_latency(),
        }
    }

    /// Generate 160-bit Kademlia node ID
    fn generate_node_id() -> String {
        let mut hasher = Sha256::new();
        hasher.update(std::time::SystemTime::now()
                     .duration_since(std::time::UNIX_EPOCH)
                     .unwrap()
                     .as_nanos()
                     .to_string()
                     .as_bytes());
        hasher.update(b"enochian_cyphers_p2p");
        
        // Take first 160 bits (20 bytes) for Kademlia compatibility
        let hash = hasher.finalize();
        hex::encode(&hash[..20])
    }

    /// Connect to bootstrap node
    fn connect_to_bootstrap(&mut self, bootstrap_addr: &str) -> Result<(), String> {
        // In production, this would establish actual network connection
        // For now, simulate successful connection
        let bootstrap_peer = PeerNode {
            node_id: Self::generate_node_id(),
            address: bootstrap_addr.to_string(),
            port: 8333, // Bitcoin default port
            last_seen: self.current_timestamp(),
            reputation: 1.0, // Bootstrap nodes are trusted
            capabilities: vec!["bootstrap".to_string(), "dht".to_string()],
            distance: None,
            is_trusted: true,
        };
        
        self.dht.add_peer(bootstrap_peer)?;
        Ok(())
    }

    /// Query peer state hashes for synchronization
    fn query_peer_state_hashes(&self) -> Result<HashMap<String, String>, String> {
        let mut peer_states = HashMap::new();
        
        // Get active peers from DHT
        let peers = self.dht.get_active_peers();
        
        for peer in peers.iter().take(10) { // Limit to 10 peers for efficiency
            if peer.reputation >= self.config.reputation_threshold {
                // Simulate state hash query (in production, send actual network message)
                let state_hash = format!("state_hash_{}", peer.node_id);
                peer_states.insert(peer.node_id.clone(), state_hash);
            }
        }
        
        Ok(peer_states)
    }

    /// Calculate minimum replicas needed for Byzantine fault tolerance
    fn calculate_min_replicas(&self) -> usize {
        let peer_count = self.dht.get_peer_count();
        if peer_count == 0 {
            return 1;
        }
        
        // Need at least 2f+1 replicas where f is number of Byzantine nodes
        let max_byzantine = ((1.0 - self.config.byzantine_threshold) * peer_count as f64) as usize;
        (2 * max_byzantine + 1).min(peer_count)
    }

    /// Get current timestamp
    fn current_timestamp(&self) -> u64 {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs()
    }
}

/// State synchronization result
#[derive(Serialize, Deserialize, Debug)]
pub struct SyncResult {
    pub status: SyncStatus,
    pub conflicts_resolved: usize,
    pub entries_updated: usize,
}

/// Synchronization status
#[derive(Serialize, Deserialize, Debug)]
pub enum SyncStatus {
    InSync,
    Resolved,
    Failed,
}

/// Network statistics
#[derive(Serialize, Deserialize, Debug)]
pub struct NetworkStats {
    pub local_node_id: String,
    pub is_online: bool,
    pub peer_count: usize,
    pub trusted_peer_count: usize,
    pub average_reputation: f64,
    pub consensus_health: f64,
    pub last_sync: u64,
    pub network_latency_ms: u64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p2p_network_initialization() {
        let config = P2PConfig::default();
        let network = P2PNetwork::new(config);
        
        assert!(!network.local_node_id.is_empty());
        assert!(!network.is_online);
        assert_eq!(network.config.byzantine_threshold, 0.67);
    }

    #[test]
    fn test_node_id_generation() {
        let id1 = P2PNetwork::generate_node_id();
        let id2 = P2PNetwork::generate_node_id();
        
        assert_ne!(id1, id2); // Should generate unique IDs
        assert_eq!(id1.len(), 40); // 160 bits = 20 bytes = 40 hex chars
    }

    #[test]
    fn test_min_replicas_calculation() {
        let config = P2PConfig::default();
        let mut network = P2PNetwork::new(config);
        
        // Add some mock peers to DHT for testing
        for i in 0..10 {
            let peer = PeerNode {
                node_id: format!("peer_{}", i),
                address: format!("192.168.1.{}", i),
                port: 8000,
                last_seen: network.current_timestamp(),
                reputation: 0.8,
                capabilities: vec!["dht".to_string()],
                distance: Some(i as u64),
                is_trusted: false,
            };
            network.dht.add_peer(peer).unwrap();
        }
        
        let min_replicas = network.calculate_min_replicas();
        assert!(min_replicas > 0);
        assert!(min_replicas <= 10); // Should not exceed peer count
    }
}
