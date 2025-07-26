//! Tradition management system for the 26 sacred traditions

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::{Result, EnochianError};

/// Tradition data structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Tradition {
    /// Tradition name
    pub name: String,
    /// Tradition description
    pub description: String,
    /// Historical period
    pub historical_period: String,
    /// Key concepts
    pub key_concepts: Vec<String>,
    /// Primary sources
    pub primary_sources: Vec<String>,
    /// Historical figures
    pub historical_figures: Vec<String>,
    /// Practices and methods
    pub practices: Vec<String>,
    /// Compatibility with other traditions
    pub compatibility: HashMap<String, f64>,
    /// Authenticity weight in scoring
    pub authenticity_weight: f64,
    /// Minimum authenticity threshold
    pub minimum_threshold: f64,
    /// Sacred symbols
    pub sacred_symbols: Vec<String>,
    /// Core principles
    pub core_principles: Vec<String>,
}

/// Tradition manager
#[derive(Debug, Clone)]
pub struct TraditionManager {
    /// All traditions
    traditions: HashMap<String, Tradition>,
    /// Tradition weights
    weights: HashMap<String, f64>,
    /// Synergy matrix
    synergy_matrix: HashMap<String, HashMap<String, f64>>,
}

impl Default for TraditionManager {
    fn default() -> Self {
        Self::new()
    }
}

impl TraditionManager {
    /// Create a new tradition manager
    pub fn new() -> Self {
        let mut manager = TraditionManager {
            traditions: HashMap::new(),
            weights: HashMap::new(),
            synergy_matrix: HashMap::new(),
        };
        
        manager.initialize_traditions();
        manager.initialize_weights();
        manager.initialize_synergies();
        manager
    }
    
    /// Get tradition by name
    pub fn get_tradition(&self, name: &str) -> Option<&Tradition> {
        self.traditions.get(name)
    }
    
    /// Get all tradition names
    pub fn get_tradition_names(&self) -> Vec<String> {
        self.traditions.keys().cloned().collect()
    }
    
    /// Get tradition count
    pub fn get_tradition_count(&self) -> usize {
        self.traditions.len()
    }
    
    /// Get tradition weight
    pub fn get_tradition_weight(&self, name: &str) -> f64 {
        self.weights.get(name).copied().unwrap_or(0.0)
    }
    
    /// Calculate tradition compatibility
    pub fn calculate_compatibility(&self, tradition1: &str, tradition2: &str) -> f64 {
        if let Some(tradition) = self.traditions.get(tradition1) {
            tradition.compatibility.get(tradition2).copied().unwrap_or(0.5)
        } else {
            0.5
        }
    }
    
    /// Get tradition synergy
    pub fn get_synergy(&self, tradition1: &str, tradition2: &str) -> f64 {
        self.synergy_matrix
            .get(tradition1)
            .and_then(|synergies| synergies.get(tradition2))
            .copied()
            .unwrap_or(0.0)
    }
    
    /// Validate tradition combination
    pub fn validate_combination(&self, traditions: &[String]) -> Result<f64> {
        if traditions.is_empty() {
            return Err(EnochianError::Generic {
                message: "No traditions specified".to_string(),
            });
        }
        
        // Check if all traditions exist
        for tradition in traditions {
            if !self.traditions.contains_key(tradition) {
                return Err(EnochianError::TraditionNotSupported {
                    tradition: tradition.clone(),
                });
            }
        }
        
        // Calculate combination score
        let mut total_score = 0.0;
        let mut pair_count = 0;
        
        for i in 0..traditions.len() {
            for j in (i + 1)..traditions.len() {
                let synergy = self.get_synergy(&traditions[i], &traditions[j]);
                total_score += synergy;
                pair_count += 1;
            }
        }
        
        let combination_score = if pair_count > 0 {
            total_score / pair_count as f64
        } else {
            1.0 // Single tradition
        };
        
        Ok(combination_score)
    }
    
    /// Get recommended traditions for a given tradition
    pub fn get_recommended_combinations(&self, base_tradition: &str) -> Vec<(String, f64)> {
        let mut recommendations = Vec::new();
        
        if let Some(synergies) = self.synergy_matrix.get(base_tradition) {
            for (tradition, synergy) in synergies {
                if *synergy > 0.7 {
                    recommendations.push((tradition.clone(), *synergy));
                }
            }
        }
        
        recommendations.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        recommendations
    }
    
    fn initialize_traditions(&mut self) {
        // 1. Enochian (Primary tradition - 60% weight)
        self.traditions.insert("Enochian".to_string(), Tradition {
            name: "Enochian".to_string(),
            description: "The angelic language and magical system received by Dr. John Dee and Edward Kelley in the 16th century".to_string(),
            historical_period: "1582-1587".to_string(),
            key_concepts: vec![
                "Angelic communication".to_string(),
                "Aethyr exploration".to_string(),
                "Watchtower magic".to_string(),
                "Governor Angels".to_string(),
                "Enochian language".to_string(),
                "Scrying".to_string(),
            ],
            primary_sources: vec![
                "John Dee's Spiritual Diaries".to_string(),
                "The Enochian Tablets".to_string(),
                "Liber Loagaeth".to_string(),
            ],
            historical_figures: vec![
                "John Dee".to_string(),
                "Edward Kelley".to_string(),
                "Queen Elizabeth I".to_string(),
            ],
            practices: vec![
                "Angelic invocation".to_string(),
                "Aethyr pathworking".to_string(),
                "Enochian chess".to_string(),
                "Watchtower rituals".to_string(),
            ],
            compatibility: HashMap::new(),
            authenticity_weight: 1.0,
            minimum_threshold: 0.85,
            sacred_symbols: vec![
                "Sigillum Dei Aemeth".to_string(),
                "Watchtower Tablets".to_string(),
                "Enochian Letters".to_string(),
            ],
            core_principles: vec![
                "Divine communication".to_string(),
                "Angelic hierarchy".to_string(),
                "Sacred geometry".to_string(),
            ],
        });
        
        // 2. Hermetic Qabalah
        self.traditions.insert("Hermetic_Qabalah".to_string(), Tradition {
            name: "Hermetic_Qabalah".to_string(),
            description: "The Western esoteric interpretation of Jewish Kabbalah, focusing on the Tree of Life".to_string(),
            historical_period: "Medieval-Renaissance".to_string(),
            key_concepts: vec![
                "Tree of Life".to_string(),
                "Sephiroth".to_string(),
                "Pathworking".to_string(),
                "Divine emanation".to_string(),
                "Gematria".to_string(),
            ],
            primary_sources: vec![
                "Sefer Yetzirah".to_string(),
                "Zohar".to_string(),
                "Golden Dawn manuscripts".to_string(),
            ],
            historical_figures: vec![
                "Moses de León".to_string(),
                "Isaac Luria".to_string(),
                "Samuel Liddell MacGregor Mathers".to_string(),
            ],
            practices: vec![
                "Tree of Life meditation".to_string(),
                "Pathworking".to_string(),
                "Divine name vibration".to_string(),
            ],
            compatibility: HashMap::new(),
            authenticity_weight: 0.8,
            minimum_threshold: 0.80,
            sacred_symbols: vec![
                "Tree of Life".to_string(),
                "Hebrew letters".to_string(),
                "Sephirotic symbols".to_string(),
            ],
            core_principles: vec![
                "As above, so below".to_string(),
                "Divine emanation".to_string(),
                "Unity of opposites".to_string(),
            ],
        });
        
        // 3. Thelema
        self.traditions.insert("Thelema".to_string(), Tradition {
            name: "Thelema".to_string(),
            description: "The philosophical and magical system developed by Aleister Crowley".to_string(),
            historical_period: "20th century".to_string(),
            key_concepts: vec![
                "True Will".to_string(),
                "Love is the law".to_string(),
                "Aeon of Horus".to_string(),
                "Magick".to_string(),
            ],
            primary_sources: vec![
                "The Book of the Law".to_string(),
                "Magick in Theory and Practice".to_string(),
                "The Vision and the Voice".to_string(),
            ],
            historical_figures: vec![
                "Aleister Crowley".to_string(),
                "Rose Edith Kelly".to_string(),
                "Aiwass".to_string(),
            ],
            practices: vec![
                "Liber Resh".to_string(),
                "Star Ruby".to_string(),
                "Gnostic Mass".to_string(),
            ],
            compatibility: HashMap::new(),
            authenticity_weight: 0.7,
            minimum_threshold: 0.75,
            sacred_symbols: vec![
                "Unicursal Hexagram".to_string(),
                "Rose Cross".to_string(),
                "Ankh".to_string(),
            ],
            core_principles: vec![
                "Do what thou wilt".to_string(),
                "Every man and woman is a star".to_string(),
                "Love under will".to_string(),
            ],
        });
        
        // 4. Golden Dawn
        self.traditions.insert("Golden_Dawn".to_string(), Tradition {
            name: "Golden_Dawn".to_string(),
            description: "The Hermetic Order of the Golden Dawn magical system".to_string(),
            historical_period: "Late 19th century".to_string(),
            key_concepts: vec![
                "Grade system".to_string(),
                "Elemental magic".to_string(),
                "Ritual magic".to_string(),
                "Initiation".to_string(),
            ],
            primary_sources: vec![
                "Golden Dawn manuscripts".to_string(),
                "Cipher manuscripts".to_string(),
                "Flying rolls".to_string(),
            ],
            historical_figures: vec![
                "Samuel Liddell MacGregor Mathers".to_string(),
                "William Wynn Westcott".to_string(),
                "William Robert Woodman".to_string(),
            ],
            practices: vec![
                "Lesser Banishing Ritual of the Pentagram".to_string(),
                "Middle Pillar".to_string(),
                "Tattwas".to_string(),
            ],
            compatibility: HashMap::new(),
            authenticity_weight: 0.75,
            minimum_threshold: 0.78,
            sacred_symbols: vec![
                "Pentagram".to_string(),
                "Hexagram".to_string(),
                "Rose Cross".to_string(),
            ],
            core_principles: vec![
                "Knowledge and conversation".to_string(),
                "Elemental balance".to_string(),
                "Gradual initiation".to_string(),
            ],
        });
        
        // 5. Chaos Magic
        self.traditions.insert("Chaos_Magic".to_string(), Tradition {
            name: "Chaos_Magic".to_string(),
            description: "A postmodern magical practice emphasizing results over dogma".to_string(),
            historical_period: "Late 20th century".to_string(),
            key_concepts: vec![
                "Paradigm shifting".to_string(),
                "Gnosis".to_string(),
                "Sigil magic".to_string(),
                "Belief as tool".to_string(),
            ],
            primary_sources: vec![
                "Liber Null".to_string(),
                "Condensed Chaos".to_string(),
                "Prime Chaos".to_string(),
            ],
            historical_figures: vec![
                "Peter J. Carroll".to_string(),
                "Ray Sherwin".to_string(),
                "Austin Osman Spare".to_string(),
            ],
            practices: vec![
                "Sigil creation".to_string(),
                "Gnosis induction".to_string(),
                "Paradigm adoption".to_string(),
            ],
            compatibility: HashMap::new(),
            authenticity_weight: 0.6,
            minimum_threshold: 0.70,
            sacred_symbols: vec![
                "Chaos star".to_string(),
                "Sigils".to_string(),
                "Octarine".to_string(),
            ],
            core_principles: vec![
                "Nothing is true, everything is permitted".to_string(),
                "Results over theory".to_string(),
                "Paradigmatic flexibility".to_string(),
            ],
        });
        
        // Add remaining 21 traditions (abbreviated for space)
        self.add_remaining_traditions();
    }
    
    fn add_remaining_traditions(&mut self) {
        // 6-26: Additional traditions (simplified entries)
        let additional_traditions = vec![
            ("Alchemy", "The ancient art of transformation", 0.7),
            ("Astrology", "The study of celestial influences", 0.65),
            ("Tarot", "Divination through symbolic cards", 0.6),
            ("I_Ching", "Chinese divination system", 0.65),
            ("Runes", "Norse divination system", 0.6),
            ("Celtic_Druidism", "Ancient Celtic spiritual practices", 0.65),
            ("Egyptian_Magic", "Ancient Egyptian magical practices", 0.7),
            ("Greek_Mysteries", "Ancient Greek mystery traditions", 0.7),
            ("Gnosticism", "Early Christian mystical tradition", 0.75),
            ("Sufism", "Islamic mystical tradition", 0.8),
            ("Tantra", "Hindu/Buddhist esoteric practices", 0.75),
            ("Zen_Buddhism", "Japanese Buddhist meditation", 0.7),
            ("Christian_Mysticism", "Christian contemplative tradition", 0.75),
            ("Jewish_Mysticism", "Traditional Jewish Kabbalah", 0.8),
            ("Shamanism", "Indigenous spiritual practices", 0.65),
            ("Witchcraft", "Traditional European witchcraft", 0.6),
            ("Voodoo", "Afro-Caribbean spiritual tradition", 0.6),
            ("Santeria", "Afro-Cuban religious tradition", 0.6),
            ("Discordianism", "Modern chaotic philosophy", 0.5),
            ("Satanism", "Left-hand path philosophy", 0.5),
            ("Luciferianism", "Light-bearer philosophy", 0.55),
        ];
        
        for (name, description, weight) in additional_traditions {
            self.traditions.insert(name.to_string(), Tradition {
                name: name.to_string(),
                description: description.to_string(),
                historical_period: "Various".to_string(),
                key_concepts: vec![format!("{} practices", name)],
                primary_sources: vec![format!("{} texts", name)],
                historical_figures: vec![format!("{} practitioners", name)],
                practices: vec![format!("{} methods", name)],
                compatibility: HashMap::new(),
                authenticity_weight: weight,
                minimum_threshold: 0.70,
                sacred_symbols: vec![format!("{} symbols", name)],
                core_principles: vec![format!("{} principles", name)],
            });
        }
    }
    
    fn initialize_weights(&mut self) {
        // Sacred constraint: Enochian must have 60% weighting
        self.weights.insert("Enochian".to_string(), 0.6);
        self.weights.insert("Hermetic_Qabalah".to_string(), 0.15);
        self.weights.insert("Thelema".to_string(), 0.08);
        self.weights.insert("Golden_Dawn".to_string(), 0.07);
        self.weights.insert("Chaos_Magic".to_string(), 0.05);
        
        // Remaining traditions share the remaining 5%
        let remaining_weight = 0.05;
        let remaining_count = self.traditions.len() - 5;
        let individual_weight = remaining_weight / remaining_count as f64;
        
        for name in self.traditions.keys() {
            if !self.weights.contains_key(name) {
                self.weights.insert(name.clone(), individual_weight);
            }
        }
    }
    
    fn initialize_synergies(&mut self) {
        // Initialize synergy matrix
        for tradition1 in self.traditions.keys() {
            let mut synergies = HashMap::new();
            
            for tradition2 in self.traditions.keys() {
                if tradition1 != tradition2 {
                    let synergy = self.calculate_base_synergy(tradition1, tradition2);
                    synergies.insert(tradition2.clone(), synergy);
                }
            }
            
            self.synergy_matrix.insert(tradition1.clone(), synergies);
        }
    }
    
    fn calculate_base_synergy(&self, tradition1: &str, tradition2: &str) -> f64 {
        // High synergy combinations
        match (tradition1, tradition2) {
            ("Enochian", "Hermetic_Qabalah") | ("Hermetic_Qabalah", "Enochian") => 0.9,
            ("Enochian", "Golden_Dawn") | ("Golden_Dawn", "Enochian") => 0.85,
            ("Enochian", "Thelema") | ("Thelema", "Enochian") => 0.8,
            ("Hermetic_Qabalah", "Golden_Dawn") | ("Golden_Dawn", "Hermetic_Qabalah") => 0.9,
            ("Hermetic_Qabalah", "Thelema") | ("Thelema", "Hermetic_Qabalah") => 0.85,
            ("Golden_Dawn", "Thelema") | ("Thelema", "Golden_Dawn") => 0.8,
            ("Chaos_Magic", "Thelema") | ("Thelema", "Chaos_Magic") => 0.75,
            ("Alchemy", "Hermetic_Qabalah") | ("Hermetic_Qabalah", "Alchemy") => 0.8,
            ("Astrology", "Hermetic_Qabalah") | ("Hermetic_Qabalah", "Astrology") => 0.75,
            ("Tarot", "Golden_Dawn") | ("Golden_Dawn", "Tarot") => 0.8,
            _ => 0.5, // Default neutral synergy
        }
    }
}

/// Get tradition count (for sacred constraint validation)
pub fn get_tradition_count() -> usize {
    26
}

/// Get tradition weight (for sacred constraint validation)
pub fn get_tradition_weight(tradition: &str) -> f64 {
    let manager = TraditionManager::new();
    manager.get_tradition_weight(tradition)
}
