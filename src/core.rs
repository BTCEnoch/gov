//! Core functionality for the Enochian Cyphers system

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::{Result, EnochianError};

/// Core Enochian Cyphers system
#[derive(Debug, Clone)]
pub struct EnochianCore {
    /// System configuration
    pub config: SystemConfig,
    /// Current game states
    pub game_states: HashMap<String, GameState>,
    /// Quest registry
    pub quest_registry: HashMap<String, QuestData>,
    /// Initialized status
    pub initialized: bool,
}

/// System configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemConfig {
    /// Authenticity threshold
    pub authenticity_threshold: f64,
    /// Maximum concurrent quests per player
    pub max_concurrent_quests: u32,
    /// Tradition weighting
    pub tradition_weighting: HashMap<String, f64>,
    /// Governor interaction cooldown (in blocks)
    pub governor_interaction_cooldown: u32,
    /// Enable P2P synchronization
    pub enable_p2p_sync: bool,
    /// Enable Bitcoin L1 integration
    pub enable_bitcoin_integration: bool,
}

/// Game state for a player
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameState {
    /// Player identifier
    pub player_id: String,
    /// Current block height
    pub block_height: u64,
    /// Completed quests
    pub completed_quests: Vec<String>,
    /// Active quests
    pub active_quests: Vec<String>,
    /// Tradition mastery levels
    pub tradition_mastery: HashMap<String, f64>,
    /// Governor relationships
    pub governor_relationships: HashMap<String, f64>,
    /// Reputation scores
    pub reputation_scores: HashMap<String, f64>,
    /// Owned hypertokens
    pub owned_hypertokens: Vec<String>,
    /// Sacred items
    pub sacred_items: Vec<String>,
    /// Current energy level
    pub energy_level: u32,
    /// Accessible Aethyr levels
    pub aethyr_access: Vec<u32>,
    /// Bitcoin balance in satoshis
    pub balance_sats: u64,
    /// Staked amount
    pub staked_amount: u64,
    /// Pending rewards
    pub pending_rewards: u64,
    /// Overall authenticity score
    pub authenticity_score: f64,
    /// Last update timestamp
    pub last_update: String,
    /// State version
    pub version: u32,
}

/// Quest data structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestData {
    /// Quest identifier
    pub quest_id: String,
    /// Quest title
    pub title: String,
    /// Quest description
    pub description: String,
    /// Quest objectives
    pub objectives: Vec<String>,
    /// Wisdom taught
    pub wisdom_taught: String,
    /// Choice branches
    pub choice_branches: Vec<QuestChoice>,
    /// Authenticity score
    pub authenticity_score: f64,
    /// Estimated duration in minutes
    pub estimated_duration: u32,
    /// Tradition integration
    pub tradition_integration: Vec<String>,
    /// Associated governor
    pub governor_name: String,
    /// Difficulty level
    pub difficulty_level: u32,
    /// Required energy
    pub required_energy: u32,
    /// Rewards
    pub rewards: QuestRewards,
    /// Creation timestamp
    pub created_at: String,
}

/// Quest choice structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestChoice {
    /// Choice identifier
    pub choice_id: String,
    /// Choice description
    pub description: String,
    /// Consequences
    pub consequences: Vec<String>,
    /// Difficulty modifier
    pub difficulty_modifier: f64,
    /// Tradition alignment
    pub tradition_alignment: f64,
    /// Authenticity impact
    pub authenticity_impact: f64,
    /// Required traditions
    pub required_traditions: Vec<String>,
    /// Energy cost
    pub energy_cost: u32,
}

/// Quest rewards
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestRewards {
    /// Experience points
    pub experience: u32,
    /// Reputation changes
    pub reputation_changes: HashMap<String, f64>,
    /// Tradition mastery gains
    pub tradition_mastery_gains: HashMap<String, f64>,
    /// Governor relationship changes
    pub governor_relationship_changes: HashMap<String, f64>,
    /// Bitcoin rewards in satoshis
    pub bitcoin_rewards: u64,
    /// Sacred items gained
    pub sacred_items: Vec<String>,
    /// Hypertoken rewards
    pub hypertoken_rewards: Vec<String>,
    /// Aethyr access gained
    pub aethyr_access_gained: Vec<u32>,
}

impl Default for SystemConfig {
    fn default() -> Self {
        let mut tradition_weighting = HashMap::new();
        tradition_weighting.insert("Enochian".to_string(), 0.6);
        tradition_weighting.insert("Hermetic_Qabalah".to_string(), 0.15);
        tradition_weighting.insert("Thelema".to_string(), 0.1);
        tradition_weighting.insert("Golden_Dawn".to_string(), 0.1);
        tradition_weighting.insert("Chaos_Magic".to_string(), 0.05);
        
        SystemConfig {
            authenticity_threshold: 0.95,
            max_concurrent_quests: 3,
            tradition_weighting,
            governor_interaction_cooldown: 144, // 24 hours at 10min blocks
            enable_p2p_sync: false,
            enable_bitcoin_integration: false,
        }
    }
}

impl EnochianCore {
    /// Create a new Enochian Core instance
    pub fn new(config: SystemConfig) -> Self {
        EnochianCore {
            config,
            game_states: HashMap::new(),
            quest_registry: HashMap::new(),
            initialized: false,
        }
    }
    
    /// Initialize the core system
    pub fn initialize(&mut self) -> Result<()> {
        // Validate configuration
        self.validate_config()?;
        
        // Initialize subsystems
        self.initialize_subsystems()?;
        
        self.initialized = true;
        log::info!("Enochian Core initialized successfully");
        Ok(())
    }
    
    /// Create a new player game state
    pub fn create_player_state(&mut self, player_id: String) -> Result<&GameState> {
        if self.game_states.contains_key(&player_id) {
            return Err(EnochianError::Generic {
                message: format!("Player {} already exists", player_id),
            });
        }
        
        let game_state = GameState {
            player_id: player_id.clone(),
            block_height: 0,
            completed_quests: Vec::new(),
            active_quests: Vec::new(),
            tradition_mastery: {
                let mut mastery = HashMap::new();
                mastery.insert("Enochian".to_string(), 0.1);
                mastery
            },
            governor_relationships: HashMap::new(),
            reputation_scores: HashMap::new(),
            owned_hypertokens: Vec::new(),
            sacred_items: Vec::new(),
            energy_level: 25,
            aethyr_access: vec![1], // Start with access to first Aethyr
            balance_sats: 0,
            staked_amount: 0,
            pending_rewards: 0,
            authenticity_score: 0.85,
            last_update: chrono::Utc::now().to_rfc3339(),
            version: 1,
        };
        
        self.game_states.insert(player_id.clone(), game_state);
        Ok(self.game_states.get(&player_id).unwrap())
    }
    
    /// Get player game state
    pub fn get_player_state(&self, player_id: &str) -> Option<&GameState> {
        self.game_states.get(player_id)
    }
    
    /// Update player game state
    pub fn update_player_state(&mut self, player_id: &str, state: GameState) -> Result<()> {
        if !self.game_states.contains_key(player_id) {
            return Err(EnochianError::Generic {
                message: format!("Player {} not found", player_id),
            });
        }
        
        // Validate state update
        self.validate_state_update(&state)?;
        
        self.game_states.insert(player_id.to_string(), state);
        Ok(())
    }
    
    /// Register a quest
    pub fn register_quest(&mut self, quest: QuestData) -> Result<()> {
        // Validate quest
        self.validate_quest(&quest)?;
        
        self.quest_registry.insert(quest.quest_id.clone(), quest);
        Ok(())
    }
    
    /// Get quest data
    pub fn get_quest(&self, quest_id: &str) -> Option<&QuestData> {
        self.quest_registry.get(quest_id)
    }
    
    /// Start a quest for a player
    pub fn start_quest(&mut self, player_id: &str, quest_id: &str) -> Result<()> {
        let player_state = self.game_states.get_mut(player_id)
            .ok_or_else(|| EnochianError::Generic {
                message: format!("Player {} not found", player_id),
            })?;
        
        let quest = self.quest_registry.get(quest_id)
            .ok_or_else(|| EnochianError::Generic {
                message: format!("Quest {} not found", quest_id),
            })?;
        
        // Check if player can start quest
        self.validate_quest_start(player_state, quest)?;
        
        // Add quest to active quests
        player_state.active_quests.push(quest_id.to_string());
        player_state.energy_level = player_state.energy_level.saturating_sub(quest.required_energy);
        player_state.last_update = chrono::Utc::now().to_rfc3339();
        player_state.version += 1;
        
        log::info!("Player {} started quest {}", player_id, quest_id);
        Ok(())
    }
    
    /// Complete a quest for a player
    pub fn complete_quest(&mut self, player_id: &str, quest_id: &str) -> Result<QuestRewards> {
        let player_state = self.game_states.get_mut(player_id)
            .ok_or_else(|| EnochianError::Generic {
                message: format!("Player {} not found", player_id),
            })?;
        
        let quest = self.quest_registry.get(quest_id)
            .ok_or_else(|| EnochianError::Generic {
                message: format!("Quest {} not found", quest_id),
            })?;
        
        // Check if quest is active
        if !player_state.active_quests.contains(&quest_id.to_string()) {
            return Err(EnochianError::Generic {
                message: format!("Quest {} is not active for player {}", quest_id, player_id),
            });
        }
        
        // Remove from active quests and add to completed
        player_state.active_quests.retain(|q| q != quest_id);
        player_state.completed_quests.push(quest_id.to_string());
        
        // Apply rewards
        self.apply_quest_rewards(player_state, &quest.rewards)?;
        
        player_state.last_update = chrono::Utc::now().to_rfc3339();
        player_state.version += 1;
        
        log::info!("Player {} completed quest {}", player_id, quest_id);
        Ok(quest.rewards.clone())
    }
    
    /// Get system statistics
    pub fn get_statistics(&self) -> serde_json::Value {
        serde_json::json!({
            "total_players": self.game_states.len(),
            "total_quests": self.quest_registry.len(),
            "active_quests": self.game_states.values()
                .map(|state| state.active_quests.len())
                .sum::<usize>(),
            "completed_quests": self.game_states.values()
                .map(|state| state.completed_quests.len())
                .sum::<usize>(),
            "average_authenticity": self.game_states.values()
                .map(|state| state.authenticity_score)
                .sum::<f64>() / self.game_states.len() as f64,
            "total_hypertokens": self.game_states.values()
                .map(|state| state.owned_hypertokens.len())
                .sum::<usize>(),
        })
    }
    
    fn validate_config(&self) -> Result<()> {
        if self.config.authenticity_threshold < 0.8 || self.config.authenticity_threshold > 1.0 {
            return Err(EnochianError::SacredConstraintViolation {
                constraint: "Authenticity threshold must be between 0.8 and 1.0".to_string(),
            });
        }
        
        if self.config.max_concurrent_quests == 0 || self.config.max_concurrent_quests > 10 {
            return Err(EnochianError::SacredConstraintViolation {
                constraint: "Max concurrent quests must be between 1 and 10".to_string(),
            });
        }
        
        // Validate Enochian weighting
        let enochian_weight = self.config.tradition_weighting.get("Enochian").unwrap_or(&0.0);
        if *enochian_weight < 0.5 {
            return Err(EnochianError::SacredConstraintViolation {
                constraint: "Enochian tradition must have at least 50% weighting".to_string(),
            });
        }
        
        Ok(())
    }
    
    fn initialize_subsystems(&mut self) -> Result<()> {
        // Initialize tradition system
        log::info!("Initializing tradition system...");
        
        // Initialize governor system
        log::info!("Initializing governor system...");
        
        // Initialize authenticity system
        log::info!("Initializing authenticity system...");
        
        Ok(())
    }
    
    fn validate_state_update(&self, state: &GameState) -> Result<()> {
        // Validate energy level
        if state.energy_level > 25 {
            return Err(EnochianError::Generic {
                message: "Energy level cannot exceed 25".to_string(),
            });
        }
        
        // Validate authenticity score
        if state.authenticity_score < 0.0 || state.authenticity_score > 1.0 {
            return Err(EnochianError::Generic {
                message: "Authenticity score must be between 0.0 and 1.0".to_string(),
            });
        }
        
        // Validate tradition mastery
        for (_, mastery) in &state.tradition_mastery {
            if *mastery < 0.0 || *mastery > 1.0 {
                return Err(EnochianError::Generic {
                    message: "Tradition mastery must be between 0.0 and 1.0".to_string(),
                });
            }
        }
        
        Ok(())
    }
    
    fn validate_quest(&self, quest: &QuestData) -> Result<()> {
        // Validate authenticity score
        if quest.authenticity_score < self.config.authenticity_threshold {
            return Err(EnochianError::AuthenticityError {
                message: format!(
                    "Quest authenticity {} below threshold {}",
                    quest.authenticity_score,
                    self.config.authenticity_threshold
                ),
            });
        }
        
        // Validate difficulty level
        if quest.difficulty_level == 0 || quest.difficulty_level > 10 {
            return Err(EnochianError::Generic {
                message: "Quest difficulty must be between 1 and 10".to_string(),
            });
        }
        
        // Validate required energy
        if quest.required_energy > 25 {
            return Err(EnochianError::Generic {
                message: "Quest cannot require more than 25 energy".to_string(),
            });
        }
        
        Ok(())
    }
    
    fn validate_quest_start(&self, player_state: &GameState, quest: &QuestData) -> Result<()> {
        // Check energy requirement
        if player_state.energy_level < quest.required_energy {
            return Err(EnochianError::Generic {
                message: format!(
                    "Insufficient energy: {} required, {} available",
                    quest.required_energy,
                    player_state.energy_level
                ),
            });
        }
        
        // Check concurrent quest limit
        if player_state.active_quests.len() >= self.config.max_concurrent_quests as usize {
            return Err(EnochianError::Generic {
                message: format!(
                    "Maximum concurrent quests reached: {}",
                    self.config.max_concurrent_quests
                ),
            });
        }
        
        // Check if quest already completed
        if player_state.completed_quests.contains(&quest.quest_id) {
            return Err(EnochianError::Generic {
                message: format!("Quest {} already completed", quest.quest_id),
            });
        }
        
        // Check if quest already active
        if player_state.active_quests.contains(&quest.quest_id) {
            return Err(EnochianError::Generic {
                message: format!("Quest {} already active", quest.quest_id),
            });
        }
        
        Ok(())
    }
    
    fn apply_quest_rewards(&self, player_state: &mut GameState, rewards: &QuestRewards) -> Result<()> {
        // Apply reputation changes
        for (category, change) in &rewards.reputation_changes {
            let current = player_state.reputation_scores.get(category).unwrap_or(&0.0);
            player_state.reputation_scores.insert(category.clone(), current + change);
        }
        
        // Apply tradition mastery gains
        for (tradition, gain) in &rewards.tradition_mastery_gains {
            let current = player_state.tradition_mastery.get(tradition).unwrap_or(&0.0);
            let new_mastery = (current + gain).min(1.0);
            player_state.tradition_mastery.insert(tradition.clone(), new_mastery);
        }
        
        // Apply governor relationship changes
        for (governor, change) in &rewards.governor_relationship_changes {
            let current = player_state.governor_relationships.get(governor).unwrap_or(&0.0);
            let new_relationship = (current + change).min(1.0).max(-1.0);
            player_state.governor_relationships.insert(governor.clone(), new_relationship);
        }
        
        // Apply Bitcoin rewards
        player_state.balance_sats += rewards.bitcoin_rewards;
        
        // Add sacred items
        for item in &rewards.sacred_items {
            if !player_state.sacred_items.contains(item) {
                player_state.sacred_items.push(item.clone());
            }
        }
        
        // Add hypertoken rewards
        for token in &rewards.hypertoken_rewards {
            if !player_state.owned_hypertokens.contains(token) {
                player_state.owned_hypertokens.push(token.clone());
            }
        }
        
        // Add Aethyr access
        for aethyr in &rewards.aethyr_access_gained {
            if !player_state.aethyr_access.contains(aethyr) {
                player_state.aethyr_access.push(*aethyr);
            }
        }
        
        Ok(())
    }
}
