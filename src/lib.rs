use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

// Make our module available to JavaScript
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

// Core types
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GovernorData {
    name: String,
    aethyr: String,
    primary_traits: Vec<Trait>,
    secondary_traits: Vec<Trait>,
    power_level: u8,
    sigil_data: String, // Base64 encoded sigil representation
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

// WASM-exposed wrapper
#[wasm_bindgen]
pub struct Governor {
    data: GovernorData
}

#[wasm_bindgen]
impl Governor {
    #[wasm_bindgen(constructor)]
    pub fn new(name: String) -> Governor {
        Governor {
            data: GovernorData {
                name,
                aethyr: String::new(),
                primary_traits: Vec::new(),
                secondary_traits: Vec::new(),
                power_level: 0,
                sigil_data: String::new(),
            }
        }
    }

    #[wasm_bindgen]
    pub fn generate_traits(&mut self) -> Result<String, JsValue> {
        // Deterministic trait generation based on name
        let seed = self.calculate_seed();
        
        // Generate primary traits (2-3)
        let num_primary = 2 + (seed % 2) as usize;
        self.data.primary_traits = self.generate_trait_set(num_primary, seed, true);
        
        // Generate secondary traits (1-2)
        let num_secondary = 1 + (seed % 2) as usize;
        self.data.secondary_traits = self.generate_trait_set(num_secondary, seed + 1, false);
        
        // Calculate power level based on traits
        self.data.power_level = self.calculate_power_level();
        
        // Return JSON representation
        serde_json::to_string(&self.data).map_err(|e| JsValue::from_str(&e.to_string()))
    }

    // Internal helper functions
    fn calculate_seed(&self) -> u32 {
        let mut seed = 0u32;
        for (i, c) in self.data.name.chars().enumerate() {
            seed = seed.wrapping_add((c as u32).wrapping_mul(i as u32 + 1));
        }
        seed
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