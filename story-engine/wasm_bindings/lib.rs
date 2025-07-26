// Enochian Cyphers Story Engine - WASM Bindings
// Main WASM interface for browser integration

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// Import our core modules
mod narrative_generator;
mod branching_logic;
mod governor_integration;
mod trac_state_manager;

use narrative_generator::NarrativeGenerator;
use branching_logic::BranchingEngine;
use governor_integration::GovernorIntegrator;
use trac_state_manager::TracStateManager;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoryEngineConfig {
    pub enable_p2p_sync: bool,
    pub authenticity_threshold: f64,
    pub max_concurrent_quests: u32,
    pub tradition_weighting: HashMap<String, f64>,
    pub governor_interaction_cooldown: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestGenerationRequest {
    pub player_id: String,
    pub governor_id: u32,
    pub player_context: PlayerContext,
    pub quest_seed: u32,
    pub difficulty_preference: u32,
    pub tradition_focus: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlayerContext {
    pub completed_quests: Vec<String>,
    pub tradition_mastery: HashMap<String, f64>,
    pub governor_relationships: HashMap<String, f64>,
    pub current_energy: u32,
    pub sacred_items: Vec<String>,
    pub aethyr_access: Vec<u32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeneratedQuest {
    pub quest_id: String,
    pub title: String,
    pub description: String,
    pub objectives: Vec<String>,
    pub wisdom_taught: String,
    pub choice_branches: Vec<QuestChoice>,
    pub authenticity_score: f64,
    pub estimated_duration: u32,
    pub tradition_integration: Vec<String>,
    pub governor_dialogue: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestChoice {
    pub choice_id: String,
    pub description: String,
    pub consequences: Vec<String>,
    pub difficulty_modifier: f64,
    pub tradition_alignment: f64,
    pub authenticity_impact: f64,
}

#[wasm_bindgen]
pub struct EnochianStoryEngine {
    narrative_generator: NarrativeGenerator,
    branching_engine: BranchingEngine,
    governor_integrator: GovernorIntegrator,
    trac_state_manager: TracStateManager,
    config: StoryEngineConfig,
    initialized: bool,
}

#[wasm_bindgen]
impl EnochianStoryEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> EnochianStoryEngine {
        console_error_panic_hook::set_once();
        
        EnochianStoryEngine {
            narrative_generator: NarrativeGenerator::new(),
            branching_engine: BranchingEngine::new(),
            governor_integrator: GovernorIntegrator::new(),
            trac_state_manager: TracStateManager::new(),
            config: StoryEngineConfig::default(),
            initialized: false,
        }
    }

    #[wasm_bindgen]
    pub fn initialize(&mut self, config_json: &str) -> String {
        let config: StoryEngineConfig = match serde_json::from_str(config_json) {
            Ok(cfg) => cfg,
            Err(e) => {
                return format!("Configuration error: {}", e);
            }
        };

        self.config = config;
        self.initialized = true;

        "Story Engine initialized successfully".to_string()
    }

    #[wasm_bindgen]
    pub fn generate_quest(&self, request_json: &str) -> String {
        if !self.initialized {
            return "Error: Story Engine not initialized".to_string();
        }

        let request: QuestGenerationRequest = match serde_json::from_str(request_json) {
            Ok(req) => req,
            Err(e) => return format!("Request parsing error: {}", e),
        };

        // Generate base narrative
        let narrative_json = self.narrative_generator.generate_quest_narrative(
            request.governor_id,
            &serde_json::to_string(&request.player_context).unwrap_or_default(),
            request.quest_seed
        );

        // Generate branching choices
        let branches_json = self.branching_engine.generate_quest_branches(
            &format!("quest_{}", request.quest_seed),
            &serde_json::to_string(&request.player_context).unwrap_or_default(),
            request.quest_seed
        );

        // Adapt for governor personality
        let adapted_narrative = self.governor_integrator.adapt_story_for_governor(
            &narrative_json,
            request.governor_id,
            &serde_json::to_string(&request.player_context).unwrap_or_default()
        );

        // Generate governor dialogue
        let dialogue = self.governor_integrator.generate_governor_dialogue(
            request.governor_id,
            "quest_introduction",
            "player_approaches"
        );

        // Combine into final quest
        let quest = self.create_complete_quest(
            &narrative_json,
            &branches_json,
            &adapted_narrative,
            &dialogue,
            &request
        );

        serde_json::to_string(&quest).unwrap_or_else(|_| "{}".to_string())
    }

    #[wasm_bindgen]
    pub fn process_quest_choice(&mut self, choice_json: &str) -> String {
        if !self.initialized {
            return "Error: Story Engine not initialized".to_string();
        }

        // Process the choice through the state manager
        let transition_result = self.trac_state_manager.propose_state_transition(
            choice_json,
            "authenticity_proof_placeholder"
        );

        // If P2P sync is enabled, handle consensus
        if self.config.enable_p2p_sync {
            // In a real implementation, this would trigger P2P validation
            let _validation_result = self.trac_state_manager.validate_transition(
                "transition_id_placeholder",
                "local_validator"
            );
        }

        transition_result
    }

    #[wasm_bindgen]
    pub fn get_player_state(&self, player_id: &str) -> String {
        self.trac_state_manager.get_current_state()
    }

    #[wasm_bindgen]
    pub fn initialize_player(&mut self, player_id: &str) -> String {
        self.trac_state_manager.initialize_player_state(player_id)
    }

    #[wasm_bindgen]
    pub fn get_consensus_status(&self) -> String {
        self.trac_state_manager.get_consensus_status()
    }

    #[wasm_bindgen]
    pub fn validate_authenticity(&self, content: &str) -> f64 {
        // Simplified authenticity validation
        let mut score = 0.85;
        let content_lower = content.to_lowercase();

        // Enochian keyword scoring
        let enochian_keywords = ["enochian", "aethyr", "governor", "angel", "dee", "kelley"];
        for keyword in &enochian_keywords {
            if content_lower.contains(keyword) {
                score += 0.02;
            }
        }

        // Tradition integration bonus
        let traditions = ["hermetic", "qabalah", "thelema", "golden dawn"];
        for tradition in &traditions {
            if content_lower.contains(tradition) {
                score += 0.01;
            }
        }

        score.min(1.0)
    }

    #[wasm_bindgen]
    pub fn get_engine_status(&self) -> String {
        let status = EngineStatus {
            initialized: self.initialized,
            p2p_enabled: self.config.enable_p2p_sync,
            authenticity_threshold: self.config.authenticity_threshold,
            active_validators: 3, // Simplified
            pending_transitions: 0, // Would query from state manager
        };

        serde_json::to_string(&status).unwrap_or_else(|_| "{}".to_string())
    }

    fn create_complete_quest(
        &self,
        narrative_json: &str,
        branches_json: &str,
        adapted_narrative: &str,
        dialogue: &str,
        request: &QuestGenerationRequest
    ) -> GeneratedQuest {
        // Parse the generated components
        let base_narrative: serde_json::Value = serde_json::from_str(narrative_json).unwrap_or_default();
        let branches: Vec<serde_json::Value> = serde_json::from_str(branches_json).unwrap_or_default();

        // Create quest choices from branches
        let mut quest_choices = Vec::new();
        for (i, branch) in branches.iter().enumerate() {
            let choice = QuestChoice {
                choice_id: format!("choice_{}", i + 1),
                description: branch.get("choice_description")
                    .and_then(|v| v.as_str())
                    .unwrap_or("Continue on the mystical path")
                    .to_string(),
                consequences: vec![
                    "Advance spiritual understanding".to_string(),
                    "Gain governor's favor".to_string(),
                    "Unlock new wisdom".to_string(),
                ],
                difficulty_modifier: branch.get("difficulty_level")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(1.0),
                tradition_alignment: 0.85,
                authenticity_impact: 0.1,
            };
            quest_choices.push(choice);
        }

        GeneratedQuest {
            quest_id: format!("quest_{}_{}", request.governor_id, request.quest_seed),
            title: base_narrative.get("title")
                .and_then(|v| v.as_str())
                .unwrap_or("Sacred Enochian Quest")
                .to_string(),
            description: base_narrative.get("description")
                .and_then(|v| v.as_str())
                .unwrap_or("A mystical journey of spiritual advancement")
                .to_string(),
            objectives: base_narrative.get("objectives")
                .and_then(|v| v.as_array())
                .map(|arr| arr.iter().filter_map(|v| v.as_str().map(|s| s.to_string())).collect())
                .unwrap_or_else(|| vec![
                    "Study sacred principles".to_string(),
                    "Practice spiritual techniques".to_string(),
                    "Achieve enlightenment".to_string(),
                ]),
            wisdom_taught: base_narrative.get("wisdom_taught")
                .and_then(|v| v.as_str())
                .unwrap_or("Fundamental mystical wisdom")
                .to_string(),
            choice_branches: quest_choices,
            authenticity_score: base_narrative.get("authenticity_score")
                .and_then(|v| v.as_f64())
                .unwrap_or(0.85),
            estimated_duration: 30, // 30 minutes
            tradition_integration: request.tradition_focus.clone(),
            governor_dialogue: dialogue.to_string(),
        }
    }
}

impl Default for StoryEngineConfig {
    fn default() -> Self {
        let mut tradition_weighting = HashMap::new();
        tradition_weighting.insert("Enochian".to_string(), 0.6);
        tradition_weighting.insert("Hermetic_Qabalah".to_string(), 0.2);
        tradition_weighting.insert("Thelema".to_string(), 0.1);
        tradition_weighting.insert("Golden_Dawn".to_string(), 0.1);

        StoryEngineConfig {
            enable_p2p_sync: false,
            authenticity_threshold: 0.85,
            max_concurrent_quests: 3,
            tradition_weighting,
            governor_interaction_cooldown: 144, // 144 blocks (24 hours)
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineStatus {
    pub initialized: bool,
    pub p2p_enabled: bool,
    pub authenticity_threshold: f64,
    pub active_validators: u32,
    pub pending_transitions: u32,
}

// WASM-specific utilities
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen]
pub fn set_panic_hook() {
    console_error_panic_hook::set_once();
}

// Export key functions for JavaScript integration
#[wasm_bindgen]
pub fn create_story_engine() -> EnochianStoryEngine {
    EnochianStoryEngine::new()
}

#[wasm_bindgen]
pub fn validate_quest_authenticity(content: &str) -> f64 {
    let engine = EnochianStoryEngine::new();
    engine.validate_authenticity(content)
}
