// Enochian Cyphers Story Engine - Narrative Generator
// WASM-compatible procedural narrative generation with authentic mystical integration

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernorProfile {
    pub id: u32,
    pub name: String,
    pub aethyr_id: u32,
    pub domain: String,
    pub tradition_affinities: Vec<String>,
    pub personality_matrix: HashMap<String, f64>,
    pub wisdom_specializations: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AethyrData {
    pub id: u32,
    pub name: String,
    pub tier: String,
    pub mystical_properties: Vec<String>,
    pub elemental_associations: HashMap<String, f64>,
    pub sacred_geometry: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NarrativeTemplate {
    pub template_id: String,
    pub tradition: String,
    pub base_structure: String,
    pub mystical_elements: Vec<String>,
    pub choice_points: Vec<String>,
    pub authenticity_markers: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeneratedNarrative {
    pub quest_id: String,
    pub title: String,
    pub description: String,
    pub objectives: Vec<String>,
    pub wisdom_taught: String,
    pub choice_branches: Vec<ChoiceBranch>,
    pub authenticity_score: f64,
    pub tradition_integration: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChoiceBranch {
    pub choice_id: String,
    pub description: String,
    pub consequences: Vec<String>,
    pub tradition_alignment: f64,
    pub difficulty_modifier: f64,
}

#[wasm_bindgen]
pub struct NarrativeGenerator {
    governor_profiles: HashMap<u32, GovernorProfile>,
    aethyr_data: HashMap<u32, AethyrData>,
    narrative_templates: HashMap<String, NarrativeTemplate>,
    lighthouse_db: LighthouseDatabase,
    i_ching_engine: IChingEngine,
}

#[wasm_bindgen]
impl NarrativeGenerator {
    #[wasm_bindgen(constructor)]
    pub fn new() -> NarrativeGenerator {
        NarrativeGenerator {
            governor_profiles: HashMap::new(),
            aethyr_data: HashMap::new(),
            narrative_templates: HashMap::new(),
            lighthouse_db: LighthouseDatabase::new(),
            i_ching_engine: IChingEngine::new(),
        }
    }

    #[wasm_bindgen]
    pub fn generate_quest_narrative(
        &self,
        gov_id: u32,
        player_traits: &str,
        quest_seed: u32
    ) -> String {
        // Fetch Governor profile and Aethyr data
        let governor = match self.governor_profiles.get(&gov_id) {
            Some(gov) => gov,
            None => return self.generate_fallback_narrative(gov_id, quest_seed),
        };
        
        let aethyr = match self.aethyr_data.get(&governor.aethyr_id) {
            Some(aethyr) => aethyr,
            None => return self.generate_fallback_narrative(gov_id, quest_seed),
        };

        // Generate I Ching hexagram for branching
        let hexagram = self.i_ching_engine.generate_from_seed(quest_seed);

        // Create narrative with authentic mystical integration
        let base_narrative = self.create_base_story(governor, aethyr);
        let enhanced_narrative = self.apply_tradition_enhancements(
            base_narrative,
            &governor.tradition_affinities
        );

        // Add branching choices based on hexagram
        let choices = self.generate_choices_from_hexagram(&hexagram, player_traits);

        // Combine into final narrative
        let final_narrative = GeneratedNarrative {
            quest_id: format!("{}_{}", governor.name, quest_seed),
            title: format!("The Sacred Path of {}", governor.domain),
            description: enhanced_narrative,
            objectives: self.generate_objectives(governor, &hexagram),
            wisdom_taught: format!("Enhanced {} mastery through authentic Enochian practices", governor.domain),
            choice_branches: choices,
            authenticity_score: self.calculate_authenticity(&enhanced_narrative, &governor.tradition_affinities),
            tradition_integration: governor.tradition_affinities.clone(),
        };

        serde_json::to_string(&final_narrative).unwrap_or_else(|_| "{}".to_string())
    }

    fn create_base_story(&self, governor: &GovernorProfile, aethyr: &AethyrData) -> String {
        format!(
            "In the sacred realm of {}, Governor {} manifests their divine wisdom through the mystical properties of {}. \
            The seeker approaches this celestial being, drawn by the {} energies that emanate from the {} tier of existence. \
            Through authentic Enochian invocations and sacred geometry patterns of {}, the path of enlightenment unfolds.",
            aethyr.name,
            governor.name,
            aethyr.mystical_properties.join(", "),
            governor.domain,
            aethyr.tier,
            aethyr.sacred_geometry
        )
    }

    fn apply_tradition_enhancements(&self, base_narrative: String, traditions: &[String]) -> String {
        let mut enhanced = base_narrative;
        
        for tradition in traditions {
            match tradition.as_str() {
                "Enochian" => {
                    enhanced.push_str(" The ancient Enochian tablets reveal their secrets through divine angelic communication.");
                },
                "Hermetic_Qabalah" => {
                    enhanced.push_str(" The Tree of Life illuminates the path through the Sephiroth of wisdom.");
                },
                "Thelema" => {
                    enhanced.push_str(" The True Will manifests through the sacred formula of Thelemic practice.");
                },
                "Golden_Dawn" => {
                    enhanced.push_str(" The Golden Dawn rituals provide the ceremonial framework for transformation.");
                },
                "Chaos_Magic" => {
                    enhanced.push_str(" Paradigm shifting techniques allow flexible adaptation to mystical realities.");
                },
                _ => {
                    enhanced.push_str(&format!(" The wisdom of {} tradition guides the spiritual journey.", tradition));
                }
            }
        }
        
        enhanced
    }

    fn generate_choices_from_hexagram(&self, hexagram: &IChingHexagram, player_traits: &str) -> Vec<ChoiceBranch> {
        let mut choices = Vec::new();
        
        // Generate 3 choice branches based on hexagram lines
        for i in 0..3 {
            let choice = ChoiceBranch {
                choice_id: format!("choice_{}", i + 1),
                description: format!("Follow the {} path of {}", 
                    hexagram.get_line_meaning(i),
                    hexagram.get_element_association(i)
                ),
                consequences: vec![
                    format!("Gain {} wisdom", hexagram.get_virtue(i)),
                    format!("Develop {} abilities", hexagram.get_skill(i)),
                    "Advance spiritual understanding".to_string(),
                ],
                tradition_alignment: hexagram.get_alignment_score(i),
                difficulty_modifier: hexagram.get_difficulty_modifier(i),
            };
            choices.push(choice);
        }
        
        choices
    }

    fn generate_objectives(&self, governor: &GovernorProfile, hexagram: &IChingHexagram) -> Vec<String> {
        vec![
            format!("Study the enhanced principles of {}", governor.domain),
            format!("Practice {}-based meditation with Enochian invocations", governor.domain.to_lowercase()),
            format!("Integrate {}'s enhanced wisdom into spiritual practice", governor.name),
            format!("Achieve mastery through authentic {} methods", 
                governor.tradition_affinities.first().unwrap_or(&"mystical".to_string())
            ),
            "Receive governor's enhanced blessing".to_string(),
        ]
    }

    fn calculate_authenticity(&self, narrative: &str, traditions: &[String]) -> f64 {
        let mut score = 0.85; // Base authenticity score
        
        // Enochian keyword scoring
        let enochian_keywords = ["enochian", "aethyr", "governor", "angel", "dee", "kelley", "watchtower"];
        let narrative_lower = narrative.to_lowercase();
        
        for keyword in &enochian_keywords {
            if narrative_lower.contains(keyword) {
                score += 0.02;
            }
        }
        
        // Tradition integration bonus
        for tradition in traditions {
            if tradition == "Enochian" {
                score += 0.05; // Extra bonus for Enochian primacy
            } else {
                score += 0.02;
            }
        }
        
        score.min(1.0)
    }

    fn generate_fallback_narrative(&self, gov_id: u32, quest_seed: u32) -> String {
        let fallback = GeneratedNarrative {
            quest_id: format!("fallback_{}", quest_seed),
            title: "Sacred Enochian Invocation".to_string(),
            description: "A fundamental quest in Enochian wisdom and spiritual advancement through authentic angelic communication.".to_string(),
            objectives: vec![
                "Study basic Enochian principles".to_string(),
                "Practice angelic invocation".to_string(),
                "Develop spiritual awareness".to_string(),
            ],
            wisdom_taught: "Foundation Enochian practices".to_string(),
            choice_branches: vec![],
            authenticity_score: 0.85,
            tradition_integration: vec!["Enochian".to_string()],
        };
        
        serde_json::to_string(&fallback).unwrap_or_else(|_| "{}".to_string())
    }
}

// Supporting structures (simplified for WASM compatibility)
pub struct LighthouseDatabase {
    // Simplified database interface
}

impl LighthouseDatabase {
    pub fn new() -> Self {
        LighthouseDatabase {}
    }
    
    pub fn get_aethyr_data(&self, aethyr_id: u32) -> AethyrData {
        // Fallback Aethyr data
        AethyrData {
            id: aethyr_id,
            name: format!("Aethyr_{}", aethyr_id),
            tier: "Transcendence".to_string(),
            mystical_properties: vec!["Divine Wisdom".to_string(), "Spiritual Illumination".to_string()],
            elemental_associations: HashMap::new(),
            sacred_geometry: "Sacred Spiral".to_string(),
        }
    }
}

pub struct IChingEngine {
    // I Ching hexagram generation engine
}

impl IChingEngine {
    pub fn new() -> Self {
        IChingEngine {}
    }
    
    pub fn generate_from_seed(&self, seed: u32) -> IChingHexagram {
        IChingHexagram::new(seed)
    }
}

pub struct IChingHexagram {
    pub hexagram_number: u32,
    pub name: String,
    pub meaning: String,
}

impl IChingHexagram {
    pub fn new(seed: u32) -> Self {
        let hexagram_number = (seed % 64) + 1;
        IChingHexagram {
            hexagram_number,
            name: format!("Hexagram {}", hexagram_number),
            meaning: "Transformation through wisdom".to_string(),
        }
    }
    
    pub fn get_line_meaning(&self, line: usize) -> String {
        match line {
            0 => "contemplative".to_string(),
            1 => "active".to_string(),
            2 => "balanced".to_string(),
            _ => "mystical".to_string(),
        }
    }
    
    pub fn get_element_association(&self, line: usize) -> String {
        match line {
            0 => "earth wisdom".to_string(),
            1 => "fire transformation".to_string(),
            2 => "water intuition".to_string(),
            _ => "air knowledge".to_string(),
        }
    }
    
    pub fn get_virtue(&self, line: usize) -> String {
        match line {
            0 => "patience".to_string(),
            1 => "courage".to_string(),
            2 => "wisdom".to_string(),
            _ => "understanding".to_string(),
        }
    }
    
    pub fn get_skill(&self, line: usize) -> String {
        match line {
            0 => "meditation".to_string(),
            1 => "invocation".to_string(),
            2 => "divination".to_string(),
            _ => "contemplation".to_string(),
        }
    }
    
    pub fn get_alignment_score(&self, line: usize) -> f64 {
        match line {
            0 => 0.85,
            1 => 0.90,
            2 => 0.95,
            _ => 0.80,
        }
    }
    
    pub fn get_difficulty_modifier(&self, line: usize) -> f64 {
        match line {
            0 => 1.0,
            1 => 1.2,
            2 => 1.5,
            _ => 0.8,
        }
    }
}
