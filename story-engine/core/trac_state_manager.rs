// Enochian Cyphers Story Engine - Trac State Manager
// P2P state synchronization and Byzantine fault tolerance for story progression

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoryState {
    pub player_id: String,
    pub current_quest_id: String,
    pub completed_quests: Vec<String>,
    pub active_branches: Vec<String>,
    pub governor_relationships: HashMap<String, f64>,
    pub tradition_mastery: HashMap<String, f64>,
    pub reputation_scores: HashMap<String, f64>,
    pub energy_level: u32,
    pub aethyr_access: Vec<u32>,
    pub sacred_items: Vec<String>,
    pub timestamp: u64,
    pub state_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StateTransition {
    pub transition_id: String,
    pub from_state_hash: String,
    pub to_state_hash: String,
    pub quest_action: QuestAction,
    pub consequences: Vec<StateConsequence>,
    pub validator_signatures: Vec<ValidatorSignature>,
    pub timestamp: u64,
    pub block_height: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestAction {
    pub action_type: ActionType,
    pub quest_id: String,
    pub choice_id: Option<String>,
    pub parameters: HashMap<String, String>,
    pub authenticity_proof: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ActionType {
    StartQuest,
    MakeChoice,
    CompleteQuest,
    InteractWithGovernor,
    UseSacredItem,
    PerformRitual,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StateConsequence {
    pub consequence_type: ConsequenceType,
    pub target: String,
    pub value_change: f64,
    pub duration: ConsequenceDuration,
    pub authenticity_impact: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConsequenceType {
    ReputationChange,
    TraditionMastery,
    GovernorRelationship,
    EnergyModification,
    ItemGain,
    ItemLoss,
    AethyrAccess,
    WisdomUnlock,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConsequenceDuration {
    Temporary,
    Permanent,
    QuestLine,
    Conditional,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidatorSignature {
    pub validator_id: String,
    pub signature: String,
    pub validation_timestamp: u64,
    pub authenticity_score: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsensusState {
    pub canonical_state: StoryState,
    pub pending_transitions: Vec<StateTransition>,
    pub validator_weights: HashMap<String, f64>,
    pub consensus_threshold: f64,
    pub last_finalized_block: u64,
}

#[wasm_bindgen]
pub struct TracStateManager {
    current_state: Option<StoryState>,
    pending_transitions: Vec<StateTransition>,
    validator_network: HashMap<String, ValidatorNode>,
    consensus_rules: ConsensusRules,
    state_history: Vec<StoryState>,
    authenticity_validators: Vec<String>,
}

#[wasm_bindgen]
impl TracStateManager {
    #[wasm_bindgen(constructor)]
    pub fn new() -> TracStateManager {
        TracStateManager {
            current_state: None,
            pending_transitions: Vec::new(),
            validator_network: HashMap::new(),
            consensus_rules: ConsensusRules::default(),
            state_history: Vec::new(),
            authenticity_validators: vec![
                "enochian_validator".to_string(),
                "hermetic_validator".to_string(),
                "tradition_validator".to_string(),
            ],
        }
    }

    #[wasm_bindgen]
    pub fn initialize_player_state(&mut self, player_id: &str) -> String {
        let initial_state = StoryState {
            player_id: player_id.to_string(),
            current_quest_id: "welcome_quest".to_string(),
            completed_quests: vec![],
            active_branches: vec![],
            governor_relationships: HashMap::new(),
            tradition_mastery: {
                let mut mastery = HashMap::new();
                mastery.insert("Enochian".to_string(), 0.1);
                mastery.insert("Hermetic_Qabalah".to_string(), 0.05);
                mastery
            },
            reputation_scores: HashMap::new(),
            energy_level: 25,
            aethyr_access: vec![],
            sacred_items: vec![],
            timestamp: self.get_current_timestamp(),
            state_hash: String::new(),
        };

        let state_hash = self.calculate_state_hash(&initial_state);
        let mut final_state = initial_state;
        final_state.state_hash = state_hash;

        self.current_state = Some(final_state.clone());
        self.state_history.push(final_state.clone());

        serde_json::to_string(&final_state).unwrap_or_else(|_| "{}".to_string())
    }

    #[wasm_bindgen]
    pub fn propose_state_transition(
        &mut self,
        quest_action: &str,
        authenticity_proof: &str
    ) -> String {
        let action: QuestAction = match serde_json::from_str(quest_action) {
            Ok(action) => action,
            Err(_) => return "Invalid quest action format".to_string(),
        };

        let current_state = match &self.current_state {
            Some(state) => state.clone(),
            None => return "No current state initialized".to_string(),
        };

        // Calculate consequences of the action
        let consequences = self.calculate_action_consequences(&action, &current_state);
        
        // Apply consequences to create new state
        let new_state = self.apply_consequences(&current_state, &consequences);
        
        // Create state transition
        let transition = StateTransition {
            transition_id: format!("{}_{}", action.quest_id, self.get_current_timestamp()),
            from_state_hash: current_state.state_hash.clone(),
            to_state_hash: self.calculate_state_hash(&new_state),
            quest_action: action,
            consequences,
            validator_signatures: vec![],
            timestamp: self.get_current_timestamp(),
            block_height: self.get_current_block_height(),
        };

        // Add to pending transitions for validation
        self.pending_transitions.push(transition.clone());

        serde_json::to_string(&transition).unwrap_or_else(|_| "{}".to_string())
    }

    #[wasm_bindgen]
    pub fn validate_transition(&mut self, transition_id: &str, validator_id: &str) -> String {
        let transition_index = match self.pending_transitions.iter().position(|t| t.transition_id == transition_id) {
            Some(index) => index,
            None => return "Transition not found".to_string(),
        };

        let transition = &self.pending_transitions[transition_index];
        
        // Perform authenticity validation
        let authenticity_score = self.validate_authenticity(&transition.quest_action);
        
        // Create validator signature
        let signature = ValidatorSignature {
            validator_id: validator_id.to_string(),
            signature: self.create_signature(transition, validator_id),
            validation_timestamp: self.get_current_timestamp(),
            authenticity_score,
        };

        // Add signature to transition
        self.pending_transitions[transition_index].validator_signatures.push(signature.clone());

        // Check if consensus is reached
        if self.check_consensus(&self.pending_transitions[transition_index]) {
            self.finalize_transition(transition_index);
        }

        serde_json::to_string(&signature).unwrap_or_else(|_| "{}".to_string())
    }

    #[wasm_bindgen]
    pub fn get_current_state(&self) -> String {
        match &self.current_state {
            Some(state) => serde_json::to_string(state).unwrap_or_else(|_| "{}".to_string()),
            None => "{}".to_string(),
        }
    }

    #[wasm_bindgen]
    pub fn get_consensus_status(&self) -> String {
        let consensus_state = ConsensusState {
            canonical_state: self.current_state.clone().unwrap_or_else(|| self.create_empty_state()),
            pending_transitions: self.pending_transitions.clone(),
            validator_weights: self.get_validator_weights(),
            consensus_threshold: self.consensus_rules.consensus_threshold,
            last_finalized_block: self.get_current_block_height(),
        };

        serde_json::to_string(&consensus_state).unwrap_or_else(|_| "{}".to_string())
    }

    fn calculate_action_consequences(&self, action: &QuestAction, current_state: &StoryState) -> Vec<StateConsequence> {
        let mut consequences = Vec::new();

        match action.action_type {
            ActionType::CompleteQuest => {
                // Reputation increase
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::ReputationChange,
                    target: "overall".to_string(),
                    value_change: 0.1,
                    duration: ConsequenceDuration::Permanent,
                    authenticity_impact: 0.05,
                });

                // Tradition mastery increase
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::TraditionMastery,
                    target: "Enochian".to_string(),
                    value_change: 0.05,
                    duration: ConsequenceDuration::Permanent,
                    authenticity_impact: 0.08,
                });
            },
            ActionType::InteractWithGovernor => {
                // Governor relationship improvement
                let governor_name = action.parameters.get("governor_name").unwrap_or(&"unknown".to_string()).clone();
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::GovernorRelationship,
                    target: governor_name,
                    value_change: 0.15,
                    duration: ConsequenceDuration::Permanent,
                    authenticity_impact: 0.1,
                });
            },
            ActionType::PerformRitual => {
                // Energy cost
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::EnergyModification,
                    target: "energy_level".to_string(),
                    value_change: -5.0,
                    duration: ConsequenceDuration::Temporary,
                    authenticity_impact: 0.0,
                });

                // Wisdom unlock
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::WisdomUnlock,
                    target: "ritual_knowledge".to_string(),
                    value_change: 1.0,
                    duration: ConsequenceDuration::Permanent,
                    authenticity_impact: 0.12,
                });
            },
            _ => {
                // Default consequence
                consequences.push(StateConsequence {
                    consequence_type: ConsequenceType::ReputationChange,
                    target: "overall".to_string(),
                    value_change: 0.01,
                    duration: ConsequenceDuration::Temporary,
                    authenticity_impact: 0.01,
                });
            }
        }

        consequences
    }

    fn apply_consequences(&self, current_state: &StoryState, consequences: &[StateConsequence]) -> StoryState {
        let mut new_state = current_state.clone();

        for consequence in consequences {
            match consequence.consequence_type {
                ConsequenceType::ReputationChange => {
                    let current_rep = new_state.reputation_scores.get(&consequence.target).unwrap_or(&0.0);
                    new_state.reputation_scores.insert(consequence.target.clone(), current_rep + consequence.value_change);
                },
                ConsequenceType::TraditionMastery => {
                    let current_mastery = new_state.tradition_mastery.get(&consequence.target).unwrap_or(&0.0);
                    new_state.tradition_mastery.insert(consequence.target.clone(), (current_mastery + consequence.value_change).min(1.0));
                },
                ConsequenceType::GovernorRelationship => {
                    let current_rel = new_state.governor_relationships.get(&consequence.target).unwrap_or(&0.0);
                    new_state.governor_relationships.insert(consequence.target.clone(), (current_rel + consequence.value_change).min(1.0));
                },
                ConsequenceType::EnergyModification => {
                    new_state.energy_level = ((new_state.energy_level as f64) + consequence.value_change).max(0.0).min(25.0) as u32;
                },
                ConsequenceType::ItemGain => {
                    new_state.sacred_items.push(consequence.target.clone());
                },
                ConsequenceType::AethyrAccess => {
                    if let Ok(aethyr_id) = consequence.target.parse::<u32>() {
                        if !new_state.aethyr_access.contains(&aethyr_id) {
                            new_state.aethyr_access.push(aethyr_id);
                        }
                    }
                },
                _ => {} // Handle other consequence types as needed
            }
        }

        new_state.timestamp = self.get_current_timestamp();
        new_state.state_hash = self.calculate_state_hash(&new_state);
        new_state
    }

    fn validate_authenticity(&self, action: &QuestAction) -> f64 {
        // Simplified authenticity validation
        let mut score = 0.85;

        // Check for Enochian elements
        if action.authenticity_proof.contains("enochian") {
            score += 0.1;
        }

        // Check for proper tradition alignment
        if action.parameters.contains_key("tradition") {
            score += 0.05;
        }

        score.min(1.0)
    }

    fn create_signature(&self, transition: &StateTransition, validator_id: &str) -> String {
        // Simplified signature creation (in real implementation, use cryptographic signatures)
        format!("{}_{}_{}_{}", validator_id, transition.transition_id, transition.timestamp, "signature_hash")
    }

    fn check_consensus(&self, transition: &StateTransition) -> bool {
        let required_signatures = (self.authenticity_validators.len() as f64 * self.consensus_rules.consensus_threshold).ceil() as usize;
        transition.validator_signatures.len() >= required_signatures
    }

    fn finalize_transition(&mut self, transition_index: usize) {
        let transition = self.pending_transitions.remove(transition_index);
        
        // Apply the transition to current state
        if let Some(current_state) = &self.current_state {
            let new_state = self.apply_consequences(current_state, &transition.consequences);
            self.current_state = Some(new_state.clone());
            self.state_history.push(new_state);
        }
    }

    fn calculate_state_hash(&self, state: &StoryState) -> String {
        // Simplified hash calculation (in real implementation, use proper cryptographic hashing)
        format!("hash_{}_{}_{}_{}", 
            state.player_id, 
            state.current_quest_id, 
            state.timestamp,
            state.completed_quests.len()
        )
    }

    fn get_current_timestamp(&self) -> u64 {
        // Simplified timestamp (in real implementation, use proper time source)
        1642680000 + (self.state_history.len() as u64 * 600) // Simulate 10-minute intervals
    }

    fn get_current_block_height(&self) -> u64 {
        // Simplified block height (in real implementation, query actual blockchain)
        800000 + (self.state_history.len() as u64)
    }

    fn get_validator_weights(&self) -> HashMap<String, f64> {
        let mut weights = HashMap::new();
        for validator in &self.authenticity_validators {
            weights.insert(validator.clone(), 1.0 / self.authenticity_validators.len() as f64);
        }
        weights
    }

    fn create_empty_state(&self) -> StoryState {
        StoryState {
            player_id: "empty".to_string(),
            current_quest_id: "none".to_string(),
            completed_quests: vec![],
            active_branches: vec![],
            governor_relationships: HashMap::new(),
            tradition_mastery: HashMap::new(),
            reputation_scores: HashMap::new(),
            energy_level: 0,
            aethyr_access: vec![],
            sacred_items: vec![],
            timestamp: 0,
            state_hash: "empty".to_string(),
        }
    }
}

// Supporting structures
pub struct ValidatorNode {
    pub node_id: String,
    pub authenticity_weight: f64,
    pub tradition_specialization: Vec<String>,
    pub reputation_score: f64,
}

#[derive(Debug, Clone)]
pub struct ConsensusRules {
    pub consensus_threshold: f64,
    pub max_pending_transitions: usize,
    pub authenticity_minimum: f64,
    pub validator_timeout: u64,
}

impl Default for ConsensusRules {
    fn default() -> Self {
        ConsensusRules {
            consensus_threshold: 0.67, // 2/3 majority
            max_pending_transitions: 100,
            authenticity_minimum: 0.85,
            validator_timeout: 3600, // 1 hour
        }
    }
}
