use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;

// Include new modules for gap resolution
pub mod trac_systems;
pub mod p2p_networking;

// Make our module available to JavaScript
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

// TAP Protocol Integration - Core Types
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TapToken {
    pub token_id: String,
    pub metadata: TokenMetadata,
    pub evolution_history: Vec<EvolutionEvent>,
    pub utility_functions: Vec<UtilityFunction>,
    pub rarity_score: u32,
    pub mutation_potential: f64,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TokenMetadata {
    pub tick: String,
    pub max_supply: u64,
    pub current_supply: u64,
    pub decimals: u8,
    pub description: String,
    pub image_data: Option<String>, // Base64 encoded image under 400kb
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct EvolutionEvent {
    pub timestamp: u64,
    pub event_type: String,
    pub old_state: String,
    pub new_state: String,
    pub trigger: String, // Achievement, quest completion, etc.
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct UtilityFunction {
    pub name: String,
    pub description: String,
    pub requirements: Vec<String>,
    pub effects: Vec<String>,
}

// Enhanced Governor Angel Structure (per expert guidance)
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GovernorAngel {
    pub name: String,
    pub aethyr: String,
    pub traditions: Vec<TraditionAffinity>,
    pub hypertoken: TapToken,
    pub knowledge_specializations: Vec<String>,
    pub mystical_resonance: f64,
    pub evolution_stage: u8,
    pub bitcoin_address: String,
    pub primary_traits: Vec<Trait>,
    pub secondary_traits: Vec<Trait>,
    pub power_level: u8,
    pub sigil_data: String, // Base64 encoded sigil representation
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TraditionAffinity {
    pub tradition_name: String,
    pub affinity_level: f64, // 0.0 to 1.0
    pub specializations: Vec<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Trait {
    name: String,
    category: TraitCategory,
    influence: f32, // 0.0 to 1.0
    description: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum TraitCategory {
    Guardian,
    Mystic,
    Warrior,
    Scholar,
    Healer,
    Creator,
}

// Game State Structure (per expert guidance)
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GameState {
    pub player_id: String,
    pub governors: HashMap<String, GovernorAngel>,
    pub active_quests: Vec<Quest>,
    pub knowledge_unlocked: std::collections::HashSet<String>,
    pub hypertoken_portfolio: Vec<TapToken>,
    pub merkle_root: String,
    pub last_sync: u64,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Quest {
    pub id: String,
    pub title: String,
    pub description: String,
    pub branches: Vec<QuestBranch>,
    pub rewards: Vec<String>,
    pub requirements: Vec<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct QuestBranch {
    pub choice_text: String,
    pub consequences: Vec<String>,
    pub next_quest_id: Option<String>,
}

// WASM-exposed wrapper for Governor Angel
#[wasm_bindgen]
pub struct Governor {
    data: GovernorAngel
}

#[wasm_bindgen]
impl Governor {
    #[wasm_bindgen(constructor)]
    pub fn new(name: String) -> Governor {
        // Create default hypertoken for this Governor Angel
        let hypertoken = TapToken {
            token_id: format!("gov_{}", name.to_lowercase()),
            metadata: TokenMetadata {
                tick: format!("GOV{}", &name[..3.min(name.len())]),
                max_supply: 21000000, // Bitcoin-inspired supply
                current_supply: 0,
                decimals: 8,
                description: format!("Hypertoken for Governor Angel {}", name),
                image_data: None,
            },
            evolution_history: Vec::new(),
            utility_functions: Vec::new(),
            rarity_score: 0,
            mutation_potential: 0.5,
        };

        Governor {
            data: GovernorAngel {
                name: name.clone(),
                aethyr: String::new(),
                traditions: Vec::new(),
                hypertoken,
                knowledge_specializations: Vec::new(),
                mystical_resonance: 0.0,
                evolution_stage: 1,
                bitcoin_address: String::new(),
                primary_traits: Vec::new(),
                secondary_traits: Vec::new(),
                power_level: 0,
                sigil_data: String::new(),
            }
        }
    }

    #[wasm_bindgen]
    pub fn generate_traits(&mut self) -> Result<String, JsValue> {
        // Deterministic trait generation based on name (Bitcoin-native randomness)
        let seed = self.calculate_bitcoin_seed();

        // Generate primary traits (2-3)
        let num_primary = 2 + (seed % 2) as usize;
        self.data.primary_traits = self.generate_trait_set(num_primary, seed, true);

        // Generate secondary traits (1-2)
        let num_secondary = 1 + (seed % 2) as usize;
        self.data.secondary_traits = self.generate_trait_set(num_secondary, seed + 1, false);

        // Calculate power level based on traits
        self.data.power_level = self.calculate_power_level();

        // Calculate mystical resonance
        self.data.mystical_resonance = self.calculate_mystical_resonance();

        // Return JSON representation
        serde_json::to_string(&self.data).map_err(|e| JsValue::from_str(&e.to_string()))
    }

    // TAP Protocol Integration Functions (per expert guidance)
    #[wasm_bindgen]
    pub fn create_hypertoken(&mut self, metadata_json: &str) -> Result<String, JsValue> {
        // Parse metadata and create TAP-compatible hypertoken
        let metadata: TokenMetadata = serde_json::from_str(metadata_json)
            .map_err(|e| JsValue::from_str(&format!("Invalid metadata: {}", e)))?;

        let hypertoken = TapToken {
            token_id: format!("{}_{}", self.data.name, metadata.tick),
            metadata,
            evolution_history: Vec::new(),
            utility_functions: Vec::new(),
            rarity_score: self.calculate_rarity_score(),
            mutation_potential: 0.5,
        };

        self.data.hypertoken = hypertoken;

        // Return TAP-compatible JSON for inscription
        self.generate_tap_inscription()
    }

    #[wasm_bindgen]
    pub fn evolve_hypertoken(&mut self, achievement: &str) -> Result<String, JsValue> {
        // Implement hypertoken evolution based on achievements (per Rule 4)
        let evolution_event = EvolutionEvent {
            timestamp: js_sys::Date::now() as u64,
            event_type: "achievement".to_string(),
            old_state: format!("stage_{}", self.data.evolution_stage),
            new_state: format!("stage_{}", self.data.evolution_stage + 1),
            trigger: achievement.to_string(),
        };

        self.data.hypertoken.evolution_history.push(evolution_event);
        self.data.evolution_stage += 1;
        self.data.hypertoken.mutation_potential += 0.1;

        // Recalculate rarity based on evolution
        self.data.hypertoken.rarity_score = self.calculate_rarity_score();

        Ok(format!("Hypertoken evolved to stage {}", self.data.evolution_stage))
    }

    // Internal helper functions - Bitcoin-native randomness (per expert guidance)
    fn calculate_bitcoin_seed(&self) -> u32 {
        // Use Bitcoin-native randomness via name hash (simulated block hash approach)
        let mut seed = 0u32;
        for (i, c) in self.data.name.chars().enumerate() {
            seed = seed.wrapping_add((c as u32).wrapping_mul(i as u32 + 1));
        }
        // Add deterministic component based on Bitcoin principles
        seed = seed.wrapping_mul(21000000); // Bitcoin max supply as entropy
        seed
    }

    fn calculate_mystical_resonance(&self) -> f64 {
        // Calculate resonance based on traditions and traits
        let trait_influence: f64 = self.data.primary_traits.iter()
            .map(|t| t.influence as f64)
            .sum::<f64>() * 0.7;

        let secondary_influence: f64 = self.data.secondary_traits.iter()
            .map(|t| t.influence as f64)
            .sum::<f64>() * 0.3;

        (trait_influence + secondary_influence) / (self.data.primary_traits.len() + self.data.secondary_traits.len()) as f64
    }

    fn calculate_rarity_score(&self) -> u32 {
        // Calculate rarity based on evolution stage, traits, and mystical resonance
        let base_rarity = (self.data.evolution_stage as f64 * 100.0) as u32;
        let trait_bonus = (self.data.mystical_resonance * 500.0) as u32;
        let evolution_bonus = self.data.hypertoken.evolution_history.len() as u32 * 50;

        base_rarity + trait_bonus + evolution_bonus
    }

    fn generate_tap_inscription(&self) -> Result<String, JsValue> {
        // Generate TAP Protocol compatible inscription JSON (per specs)
        let tap_inscription = serde_json::json!({
            "p": "tap",
            "op": "token-deploy",
            "tick": self.data.hypertoken.metadata.tick,
            "max": self.data.hypertoken.metadata.max_supply.to_string(),
            "lim": "1000",
            "dta": format!("Governor Angel: {} - Evolution Stage: {}",
                          self.data.name, self.data.evolution_stage)
        });

        serde_json::to_string(&tap_inscription)
            .map_err(|e| JsValue::from_str(&format!("TAP inscription error: {}", e)))
    }

    fn generate_trait_set(&self, count: usize, seed: u32, is_primary: bool) -> Vec<Trait> {
        let mut traits = Vec::new();
        let mut local_seed = seed;

        for i in 0..count {
            local_seed = local_seed.wrapping_add(i as u32);
            let trait_data = self.generate_single_trait(local_seed, is_primary);
            traits.push(trait_data);
        }

        traits
    }

    fn generate_single_trait(&self, seed: u32, is_primary: bool) -> Trait {
        let categories = [
            TraitCategory::Guardian,
            TraitCategory::Mystic,
            TraitCategory::Warrior,
            TraitCategory::Scholar,
            TraitCategory::Healer,
            TraitCategory::Creator,
        ];

        let category_index = (seed % categories.len() as u32) as usize;
        let influence_base = if is_primary { 0.7 } else { 0.3 };
        let influence_variation = (seed % 30) as f32 / 100.0;

        Trait {
            name: self.get_trait_name(&categories[category_index]),
            category: categories[category_index].clone(),
            influence: (influence_base + influence_variation).min(1.0),
            description: self.get_trait_description(&categories[category_index]),
        }
    }

    fn get_trait_name(&self, category: &TraitCategory) -> String {
        match category {
            TraitCategory::Guardian => "Celestial Protector".to_string(),
            TraitCategory::Mystic => "Ethereal Seer".to_string(),
            TraitCategory::Warrior => "Divine Warrior".to_string(),
            TraitCategory::Scholar => "Cosmic Sage".to_string(),
            TraitCategory::Healer => "Spiritual Healer".to_string(),
            TraitCategory::Creator => "Reality Shaper".to_string(),
        }
    }

    fn get_trait_description(&self, category: &TraitCategory) -> String {
        match category {
            TraitCategory::Guardian => "Protects the sacred boundaries between realms".to_string(),
            TraitCategory::Mystic => "Perceives the hidden threads of reality".to_string(),
            TraitCategory::Warrior => "Channels divine energy in combat".to_string(),
            TraitCategory::Scholar => "Holds ancient wisdom of the cosmos".to_string(),
            TraitCategory::Healer => "Mends spiritual and physical wounds".to_string(),
            TraitCategory::Creator => "Shapes reality through divine will".to_string(),
        }
    }

    fn calculate_power_level(&self) -> u8 {
        let primary_influence: f32 = self.data.primary_traits.iter()
            .map(|t| t.influence)
            .sum();
            
        let secondary_influence: f32 = self.data.secondary_traits.iter()
            .map(|t| t.influence)
            .sum();

        ((primary_influence + secondary_influence * 0.5) * 100.0) as u8
    }
}

// Test module
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_governor_creation() {
        let governor = Governor::new("OCCODON".to_string());
        assert_eq!(governor.data.name, "OCCODON");
    }

    #[test]
    fn test_trait_generation() {
        let mut governor = Governor::new("OCCODON".to_string());
        let result = governor.generate_traits();
        assert!(result.is_ok());
        
        // Verify trait counts
        assert!(governor.data.primary_traits.len() >= 2);
        assert!(governor.data.primary_traits.len() <= 3);
        assert!(governor.data.secondary_traits.len() >= 1);
        assert!(governor.data.secondary_traits.len() <= 2);
    }
} 