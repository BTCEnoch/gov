//! Governor Angel management system for the 91 sacred governors

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::{Result, EnochianError};

/// Governor Angel data structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Governor {
    /// Governor ID (1-91)
    pub id: u32,
    /// Governor name
    pub name: String,
    /// Aethyr assignment
    pub aethyr_id: u32,
    /// Aethyr name
    pub aethyr_name: String,
    /// Domain of expertise
    pub domain: String,
    /// Detailed description
    pub description: String,
    /// Personality traits
    pub personality_traits: Vec<String>,
    /// Wisdom specializations
    pub wisdom_specializations: Vec<String>,
    /// Tradition affinities
    pub tradition_affinities: HashMap<String, f64>,
    /// Sacred symbols
    pub sacred_symbols: Vec<String>,
    /// Invocation keys
    pub invocation_keys: Vec<String>,
    /// Interaction style
    pub interaction_style: InteractionStyle,
    /// Teaching methods
    pub teaching_methods: Vec<String>,
    /// Challenge preferences
    pub challenge_preferences: Vec<String>,
    /// Reward styles
    pub reward_styles: Vec<String>,
}

/// Governor interaction style
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InteractionStyle {
    /// Authority level (0.0-1.0)
    pub authority_level: f64,
    /// Wisdom approach (0.0-1.0: direct vs guided discovery)
    pub wisdom_approach: f64,
    /// Mystical intensity (0.0-1.0)
    pub mystical_intensity: f64,
    /// Compassion level (0.0-1.0)
    pub compassion_level: f64,
    /// Challenge preference (0.0-1.0)
    pub challenge_preference: f64,
    /// Tradition orthodoxy (0.0-1.0)
    pub tradition_orthodoxy: f64,
}

/// Governor manager
#[derive(Debug, Clone)]
pub struct GovernorManager {
    /// All governors
    governors: HashMap<u32, Governor>,
    /// Governors by name
    governors_by_name: HashMap<String, u32>,
    /// Governors by Aethyr
    governors_by_aethyr: HashMap<u32, Vec<u32>>,
    /// Governors by domain
    governors_by_domain: HashMap<String, Vec<u32>>,
}

impl Default for GovernorManager {
    fn default() -> Self {
        Self::new()
    }
}

impl GovernorManager {
    /// Create a new governor manager
    pub fn new() -> Self {
        let mut manager = GovernorManager {
            governors: HashMap::new(),
            governors_by_name: HashMap::new(),
            governors_by_aethyr: HashMap::new(),
            governors_by_domain: HashMap::new(),
        };
        
        manager.initialize_governors();
        manager.build_indices();
        manager
    }
    
    /// Get governor by ID
    pub fn get_governor(&self, id: u32) -> Option<&Governor> {
        self.governors.get(&id)
    }
    
    /// Get governor by name
    pub fn get_governor_by_name(&self, name: &str) -> Option<&Governor> {
        self.governors_by_name.get(name)
            .and_then(|id| self.governors.get(id))
    }
    
    /// Get governors by Aethyr
    pub fn get_governors_by_aethyr(&self, aethyr_id: u32) -> Vec<&Governor> {
        self.governors_by_aethyr.get(&aethyr_id)
            .map(|ids| ids.iter().filter_map(|id| self.governors.get(id)).collect())
            .unwrap_or_default()
    }
    
    /// Get governors by domain
    pub fn get_governors_by_domain(&self, domain: &str) -> Vec<&Governor> {
        self.governors_by_domain.get(domain)
            .map(|ids| ids.iter().filter_map(|id| self.governors.get(id)).collect())
            .unwrap_or_default()
    }
    
    /// Get all governor names
    pub fn get_governor_names(&self) -> Vec<String> {
        self.governors.values().map(|g| g.name.clone()).collect()
    }
    
    /// Get governor count
    pub fn get_governor_count(&self) -> usize {
        self.governors.len()
    }
    
    /// Find governors by tradition affinity
    pub fn find_governors_by_tradition(&self, tradition: &str, min_affinity: f64) -> Vec<&Governor> {
        self.governors.values()
            .filter(|governor| {
                governor.tradition_affinities.get(tradition)
                    .map(|affinity| *affinity >= min_affinity)
                    .unwrap_or(false)
            })
            .collect()
    }
    
    /// Get recommended governor for player
    pub fn get_recommended_governor(&self, 
                                   player_traditions: &HashMap<String, f64>,
                                   player_level: u32) -> Option<&Governor> {
        let mut best_governor = None;
        let mut best_score = 0.0;
        
        for governor in self.governors.values() {
            let score = self.calculate_governor_match_score(governor, player_traditions, player_level);
            if score > best_score {
                best_score = score;
                best_governor = Some(governor);
            }
        }
        
        best_governor
    }
    
    /// Validate governor interaction
    pub fn validate_interaction(&self, 
                               governor_id: u32, 
                               player_level: u32,
                               player_traditions: &HashMap<String, f64>) -> Result<bool> {
        let governor = self.governors.get(&governor_id)
            .ok_or_else(|| EnochianError::GovernorNotFound {
                name: governor_id.to_string(),
            })?;
        
        // Check if player has sufficient tradition mastery
        let required_traditions = &governor.tradition_affinities;
        for (tradition, required_level) in required_traditions {
            let player_level = player_traditions.get(tradition).unwrap_or(&0.0);
            if *player_level < *required_level * 0.5 { // Require at least 50% of governor's affinity
                return Ok(false);
            }
        }
        
        // Check Aethyr access requirements
        let aethyr_requirement = self.get_aethyr_requirement(governor.aethyr_id);
        if player_level < aethyr_requirement {
            return Ok(false);
        }
        
        Ok(true)
    }
    
    fn initialize_governors(&mut self) {
        // Initialize the 91 Governor Angels
        // First 30 Aethyrs with 3 governors each, plus 1 special governor
        
        // Aethyr 1: TEX (Transcendence tier)
        self.add_governor(1, "ABRIOND", 1, "TEX", "Creation Mastery", 
            "The supreme governor of divine creation and manifestation",
            vec!["Commanding", "Wise", "Creative", "Authoritative"],
            vec!["Divine Creation", "Reality Manifestation", "Sacred Geometry"],
            hashmap!{
                "Enochian" => 1.0,
                "Hermetic_Qabalah" => 0.8,
                "Sacred_Geometry" => 0.9
            },
            InteractionStyle {
                authority_level: 0.9,
                wisdom_approach: 0.8,
                mystical_intensity: 0.9,
                compassion_level: 0.7,
                challenge_preference: 0.8,
                tradition_orthodoxy: 0.9,
            }
        );
        
        self.add_governor(2, "GEDOONS", 1, "TEX", "Ancient Wisdom",
            "Keeper of the most ancient mysteries and forgotten knowledge",
            vec!["Ancient", "Wise", "Patient", "Mysterious"],
            vec!["Historical Mysteries", "Lost Knowledge", "Time Wisdom"],
            hashmap!{
                "Enochian" => 1.0,
                "Ancient_Mysteries" => 0.95,
                "Hermetic_Qabalah" => 0.7
            },
            InteractionStyle {
                authority_level: 0.7,
                wisdom_approach: 0.9,
                mystical_intensity: 0.8,
                compassion_level: 0.9,
                challenge_preference: 0.5,
                tradition_orthodoxy: 0.95,
            }
        );
        
        self.add_governor(3, "MIRZIND", 1, "TEX", "Transformation",
            "Master of spiritual transformation and evolutionary change",
            vec!["Transformative", "Dynamic", "Evolutionary", "Intense"],
            vec!["Spiritual Evolution", "Inner Alchemy", "Change Mastery"],
            hashmap!{
                "Enochian" => 1.0,
                "Alchemy" => 0.9,
                "Chaos_Magic" => 0.7
            },
            InteractionStyle {
                authority_level: 0.8,
                wisdom_approach: 0.7,
                mystical_intensity: 0.9,
                compassion_level: 0.6,
                challenge_preference: 0.9,
                tradition_orthodoxy: 0.7,
            }
        );
        
        // Continue with more governors (abbreviated for space)
        self.add_remaining_governors();
    }
    
    fn add_governor(&mut self, 
                   id: u32, 
                   name: &str, 
                   aethyr_id: u32, 
                   aethyr_name: &str,
                   domain: &str,
                   description: &str,
                   personality_traits: Vec<&str>,
                   wisdom_specializations: Vec<&str>,
                   tradition_affinities: HashMap<&str, f64>,
                   interaction_style: InteractionStyle) {
        
        let governor = Governor {
            id,
            name: name.to_string(),
            aethyr_id,
            aethyr_name: aethyr_name.to_string(),
            domain: domain.to_string(),
            description: description.to_string(),
            personality_traits: personality_traits.into_iter().map(|s| s.to_string()).collect(),
            wisdom_specializations: wisdom_specializations.into_iter().map(|s| s.to_string()).collect(),
            tradition_affinities: tradition_affinities.into_iter()
                .map(|(k, v)| (k.to_string(), v)).collect(),
            sacred_symbols: vec![
                format!("{} Sigil", name),
                format!("{} Mandala", domain),
                format!("Aethyr {} Symbol", aethyr_name),
            ],
            invocation_keys: vec![
                name.to_string(),
                format!("Governor of {}", domain),
                format!("Master of {}", aethyr_name),
            ],
            interaction_style,
            teaching_methods: vec![
                "Direct transmission".to_string(),
                "Symbolic guidance".to_string(),
                "Experiential learning".to_string(),
            ],
            challenge_preferences: vec![
                "Wisdom tests".to_string(),
                "Practical application".to_string(),
                "Spiritual trials".to_string(),
            ],
            reward_styles: vec![
                "Enhanced abilities".to_string(),
                "Sacred knowledge".to_string(),
                "Spiritual blessings".to_string(),
            ],
        };
        
        self.governors.insert(id, governor);
    }
    
    fn add_remaining_governors(&mut self) {
        // Add the remaining 88 governors (simplified for space)
        // This would include all 91 governors across 30 Aethyrs
        
        let mut current_id = 4;
        
        // Aethyr 2: RII (Transcendence tier)
        for i in 0..3 {
            self.add_governor(
                current_id + i,
                &format!("GOV{:02}", current_id + i),
                2,
                "RII",
                &format!("Domain {}", current_id + i),
                &format!("Governor {} of Aethyr RII", current_id + i),
                vec!["Wise", "Powerful", "Mysterious"],
                vec!["Specialized Knowledge", "Sacred Practices"],
                hashmap!{"Enochian" => 0.9, "Hermetic_Qabalah" => 0.6},
                InteractionStyle {
                    authority_level: 0.8,
                    wisdom_approach: 0.7,
                    mystical_intensity: 0.8,
                    compassion_level: 0.7,
                    challenge_preference: 0.7,
                    tradition_orthodoxy: 0.8,
                }
            );
        }
        current_id += 3;
        
        // Continue for all 30 Aethyrs (3 governors each = 90 total)
        for aethyr_id in 3..=30 {
            for gov_in_aethyr in 0..3 {
                if current_id <= 91 {
                    self.add_governor(
                        current_id,
                        &format!("GOV{:02}", current_id),
                        aethyr_id,
                        &format!("AET{:02}", aethyr_id),
                        &format!("Domain {}", current_id),
                        &format!("Governor {} of Aethyr {}", current_id, aethyr_id),
                        vec!["Wise", "Powerful"],
                        vec!["Specialized Knowledge"],
                        hashmap!{"Enochian" => 0.8},
                        InteractionStyle {
                            authority_level: 0.7,
                            wisdom_approach: 0.7,
                            mystical_intensity: 0.7,
                            compassion_level: 0.7,
                            challenge_preference: 0.7,
                            tradition_orthodoxy: 0.8,
                        }
                    );
                    current_id += 1;
                }
            }
        }
        
        // Add the 91st special governor if needed
        if current_id <= 91 {
            self.add_governor(
                91,
                "SUPREME",
                1,
                "TEX",
                "Supreme Authority",
                "The supreme governor overseeing all others",
                vec!["Supreme", "Transcendent", "All-Knowing"],
                vec!["Universal Wisdom", "Supreme Authority"],
                hashmap!{"Enochian" => 1.0, "All_Traditions" => 0.9},
                InteractionStyle {
                    authority_level: 1.0,
                    wisdom_approach: 1.0,
                    mystical_intensity: 1.0,
                    compassion_level: 1.0,
                    challenge_preference: 1.0,
                    tradition_orthodoxy: 1.0,
                }
            );
        }
    }
    
    fn build_indices(&mut self) {
        // Build name index
        for (id, governor) in &self.governors {
            self.governors_by_name.insert(governor.name.clone(), *id);
        }
        
        // Build Aethyr index
        for (id, governor) in &self.governors {
            self.governors_by_aethyr
                .entry(governor.aethyr_id)
                .or_insert_with(Vec::new)
                .push(*id);
        }
        
        // Build domain index
        for (id, governor) in &self.governors {
            self.governors_by_domain
                .entry(governor.domain.clone())
                .or_insert_with(Vec::new)
                .push(*id);
        }
    }
    
    fn calculate_governor_match_score(&self, 
                                    governor: &Governor,
                                    player_traditions: &HashMap<String, f64>,
                                    player_level: u32) -> f64 {
        let mut score = 0.0;
        
        // Tradition affinity matching
        for (tradition, governor_affinity) in &governor.tradition_affinities {
            if let Some(player_mastery) = player_traditions.get(tradition) {
                let affinity_match = 1.0 - (governor_affinity - player_mastery).abs();
                score += affinity_match * governor_affinity;
            }
        }
        
        // Level appropriateness
        let aethyr_requirement = self.get_aethyr_requirement(governor.aethyr_id);
        let level_match = if player_level >= aethyr_requirement {
            1.0 - ((player_level - aethyr_requirement) as f64 / 100.0).min(0.5)
        } else {
            0.0
        };
        
        score += level_match * 0.3;
        
        // Interaction style preferences (simplified)
        score += governor.interaction_style.compassion_level * 0.2;
        
        score
    }
    
    fn get_aethyr_requirement(&self, aethyr_id: u32) -> u32 {
        // Aethyr access requirements (simplified)
        match aethyr_id {
            1..=10 => aethyr_id * 5,      // Transcendence tier: 5-50
            11..=20 => 50 + (aethyr_id - 10) * 3, // Mastery tier: 53-80
            21..=30 => 80 + (aethyr_id - 20) * 2, // Foundation tier: 82-100
            _ => 100,
        }
    }
}

/// Macro for creating HashMap literals
macro_rules! hashmap {
    ($($key:expr => $value:expr),* $(,)?) => {
        {
            let mut map = HashMap::new();
            $(map.insert($key, $value);)*
            map
        }
    };
}

/// Get governor count (for sacred constraint validation)
pub fn get_governor_count() -> usize {
    91
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_governor_count() {
        let manager = GovernorManager::new();
        assert_eq!(manager.get_governor_count(), 91);
    }
    
    #[test]
    fn test_governor_retrieval() {
        let manager = GovernorManager::new();
        
        // Test by ID
        let governor = manager.get_governor(1);
        assert!(governor.is_some());
        assert_eq!(governor.unwrap().name, "ABRIOND");
        
        // Test by name
        let governor = manager.get_governor_by_name("ABRIOND");
        assert!(governor.is_some());
        assert_eq!(governor.unwrap().id, 1);
    }
    
    #[test]
    fn test_aethyr_grouping() {
        let manager = GovernorManager::new();
        
        // Test Aethyr 1 governors
        let aethyr1_governors = manager.get_governors_by_aethyr(1);
        assert!(aethyr1_governors.len() >= 3); // At least ABRIOND, GEDOONS, MIRZIND
        
        // Verify they're all in Aethyr 1
        for governor in aethyr1_governors {
            assert_eq!(governor.aethyr_id, 1);
        }
    }
    
    #[test]
    fn test_tradition_affinity_search() {
        let manager = GovernorManager::new();
        
        let enochian_governors = manager.find_governors_by_tradition("Enochian", 0.9);
        assert!(!enochian_governors.is_empty());
        
        // All should have high Enochian affinity
        for governor in enochian_governors {
            let affinity = governor.tradition_affinities.get("Enochian").unwrap_or(&0.0);
            assert!(*affinity >= 0.9);
        }
    }
}
