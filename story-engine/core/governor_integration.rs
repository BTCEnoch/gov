// Enochian Cyphers Story Engine - Governor Integration
// Trait-based story adaptation with authentic Governor Angel personalities

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernorTraits {
    pub governor_id: u32,
    pub name: String,
    pub domain: String,
    pub aethyr_tier: u32,
    pub personality_matrix: PersonalityMatrix,
    pub wisdom_specializations: Vec<WisdomSpecialization>,
    pub tradition_affinities: HashMap<String, f64>,
    pub interaction_patterns: InteractionPatterns,
    pub sacred_symbols: Vec<String>,
    pub invocation_keys: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PersonalityMatrix {
    pub authority_level: f64,      // 0.0-1.0: How commanding vs. gentle
    pub wisdom_approach: f64,      // 0.0-1.0: Direct teaching vs. guided discovery
    pub mystical_intensity: f64,   // 0.0-1.0: Subtle vs. overwhelming presence
    pub compassion_level: f64,     // 0.0-1.0: Stern vs. nurturing
    pub challenge_preference: f64, // 0.0-1.0: Easy guidance vs. difficult trials
    pub tradition_orthodoxy: f64,  // 0.0-1.0: Traditional vs. innovative approaches
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WisdomSpecialization {
    pub domain: String,
    pub mastery_level: f64,
    pub teaching_methods: Vec<String>,
    pub associated_traditions: Vec<String>,
    pub sacred_texts: Vec<String>,
    pub practical_applications: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InteractionPatterns {
    pub greeting_style: String,
    pub teaching_approach: String,
    pub challenge_method: String,
    pub reward_style: String,
    pub farewell_manner: String,
    pub preferred_communication: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AdaptedStoryElement {
    pub element_type: StoryElementType,
    pub original_content: String,
    pub adapted_content: String,
    pub governor_influence: f64,
    pub authenticity_enhancement: f64,
    pub tradition_integration: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum StoryElementType {
    Dialogue,
    Challenge,
    Teaching,
    Reward,
    Atmosphere,
    Symbolism,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoryAdaptation {
    pub quest_id: String,
    pub governor_id: u32,
    pub adapted_elements: Vec<AdaptedStoryElement>,
    pub personality_influence_score: f64,
    pub tradition_coherence_score: f64,
    pub overall_authenticity: f64,
}

#[wasm_bindgen]
pub struct GovernorIntegrator {
    governor_profiles: HashMap<u32, GovernorTraits>,
    adaptation_templates: HashMap<String, Vec<AdaptationTemplate>>,
    tradition_voice_patterns: HashMap<String, VoicePattern>,
    aethyr_influence_modifiers: HashMap<u32, AethyrModifier>,
}

#[wasm_bindgen]
impl GovernorIntegrator {
    #[wasm_bindgen(constructor)]
    pub fn new() -> GovernorIntegrator {
        let mut integrator = GovernorIntegrator {
            governor_profiles: HashMap::new(),
            adaptation_templates: HashMap::new(),
            tradition_voice_patterns: HashMap::new(),
            aethyr_influence_modifiers: HashMap::new(),
        };
        
        integrator.initialize_governor_profiles();
        integrator.initialize_adaptation_templates();
        integrator.initialize_voice_patterns();
        integrator.initialize_aethyr_modifiers();
        
        integrator
    }

    #[wasm_bindgen]
    pub fn adapt_story_for_governor(
        &self,
        quest_content: &str,
        governor_id: u32,
        player_context: &str
    ) -> String {
        let governor = match self.governor_profiles.get(&governor_id) {
            Some(gov) => gov,
            None => return self.create_fallback_adaptation(quest_content, governor_id),
        };

        let adaptation = self.perform_comprehensive_adaptation(
            quest_content,
            governor,
            player_context
        );

        serde_json::to_string(&adaptation).unwrap_or_else(|_| quest_content.to_string())
    }

    #[wasm_bindgen]
    pub fn generate_governor_dialogue(
        &self,
        governor_id: u32,
        dialogue_context: &str,
        player_action: &str
    ) -> String {
        let governor = match self.governor_profiles.get(&governor_id) {
            Some(gov) => gov,
            None => return self.create_fallback_dialogue(governor_id),
        };

        let dialogue = self.create_contextual_dialogue(governor, dialogue_context, player_action);
        dialogue
    }

    fn initialize_governor_profiles(&mut self) {
        // Initialize key Governor profiles with authentic traits
        
        // ABRIOND - Creation Mastery Governor
        self.governor_profiles.insert(1, GovernorTraits {
            governor_id: 1,
            name: "ABRIOND".to_string(),
            domain: "Creation Mastery".to_string(),
            aethyr_tier: 1,
            personality_matrix: PersonalityMatrix {
                authority_level: 0.8,
                wisdom_approach: 0.7,
                mystical_intensity: 0.9,
                compassion_level: 0.6,
                challenge_preference: 0.8,
                tradition_orthodoxy: 0.9,
            },
            wisdom_specializations: vec![
                WisdomSpecialization {
                    domain: "Divine Creation".to_string(),
                    mastery_level: 0.95,
                    teaching_methods: vec!["Direct Transmission".to_string(), "Sacred Geometry".to_string()],
                    associated_traditions: vec!["Enochian".to_string(), "Hermetic_Qabalah".to_string()],
                    sacred_texts: vec!["Dee's Spiritual Diaries".to_string(), "Enochian Tablets".to_string()],
                    practical_applications: vec!["Manifestation Techniques".to_string(), "Reality Shaping".to_string()],
                }
            ],
            tradition_affinities: {
                let mut affinities = HashMap::new();
                affinities.insert("Enochian".to_string(), 1.0);
                affinities.insert("Hermetic_Qabalah".to_string(), 0.8);
                affinities.insert("Sacred_Geometry".to_string(), 0.9);
                affinities
            },
            interaction_patterns: InteractionPatterns {
                greeting_style: "Commanding presence with divine authority".to_string(),
                teaching_approach: "Direct transmission of cosmic principles".to_string(),
                challenge_method: "Tests of creative will and manifestation".to_string(),
                reward_style: "Bestows enhanced creative abilities".to_string(),
                farewell_manner: "Blessing with continued guidance".to_string(),
                preferred_communication: "Symbolic visions and geometric patterns".to_string(),
            },
            sacred_symbols: vec!["Sacred Spiral".to_string(), "Creation Mandala".to_string(), "Divine Tetrahedron".to_string()],
            invocation_keys: vec!["ABRIOND".to_string(), "Creator of Forms".to_string(), "Master of Divine Will".to_string()],
        });

        // GEDOONS - Wisdom Keeper Governor
        self.governor_profiles.insert(2, GovernorTraits {
            governor_id: 2,
            name: "GEDOONS".to_string(),
            domain: "Ancient Wisdom".to_string(),
            aethyr_tier: 2,
            personality_matrix: PersonalityMatrix {
                authority_level: 0.6,
                wisdom_approach: 0.9,
                mystical_intensity: 0.7,
                compassion_level: 0.9,
                challenge_preference: 0.4,
                tradition_orthodoxy: 0.95,
            },
            wisdom_specializations: vec![
                WisdomSpecialization {
                    domain: "Historical Mysteries".to_string(),
                    mastery_level: 0.98,
                    teaching_methods: vec!["Story Telling".to_string(), "Historical Revelation".to_string()],
                    associated_traditions: vec!["Enochian".to_string(), "Ancient_Mysteries".to_string()],
                    sacred_texts: vec!["Lost Manuscripts".to_string(), "Ancient Codices".to_string()],
                    practical_applications: vec!["Wisdom Integration".to_string(), "Historical Understanding".to_string()],
                }
            ],
            tradition_affinities: {
                let mut affinities = HashMap::new();
                affinities.insert("Enochian".to_string(), 1.0);
                affinities.insert("Ancient_Mysteries".to_string(), 0.95);
                affinities.insert("Hermetic_Qabalah".to_string(), 0.7);
                affinities
            },
            interaction_patterns: InteractionPatterns {
                greeting_style: "Gentle wisdom with ancient authority".to_string(),
                teaching_approach: "Gradual revelation through stories and parables".to_string(),
                challenge_method: "Riddles and wisdom tests".to_string(),
                reward_style: "Shares ancient secrets and hidden knowledge".to_string(),
                farewell_manner: "Blessing with protective wisdom".to_string(),
                preferred_communication: "Ancient languages and symbolic imagery".to_string(),
            },
            sacred_symbols: vec!["Ancient Scroll".to_string(), "Wisdom Eye".to_string(), "Eternal Flame".to_string()],
            invocation_keys: vec!["GEDOONS".to_string(), "Keeper of Secrets".to_string(), "Guardian of Ancient Ways".to_string()],
        });
    }

    fn initialize_adaptation_templates(&mut self) {
        // Initialize adaptation templates for different story elements
        let dialogue_templates = vec![
            AdaptationTemplate {
                template_id: "authoritative_greeting".to_string(),
                element_type: StoryElementType::Dialogue,
                base_pattern: "Greetings, seeker".to_string(),
                adaptation_rules: vec![
                    AdaptationRule {
                        condition: "authority_level > 0.7".to_string(),
                        transformation: "Behold, mortal, I am {governor_name}, {domain} incarnate".to_string(),
                        authenticity_bonus: 0.1,
                    }
                ],
            }
        ];
        
        self.adaptation_templates.insert("dialogue".to_string(), dialogue_templates);
    }

    fn initialize_voice_patterns(&mut self) {
        self.tradition_voice_patterns.insert("Enochian".to_string(), VoicePattern {
            formality_level: 0.9,
            mystical_terminology: vec!["divine".to_string(), "sacred".to_string(), "celestial".to_string()],
            sentence_structure: "formal_invocative".to_string(),
            emotional_tone: "authoritative_compassionate".to_string(),
        });

        self.tradition_voice_patterns.insert("Hermetic_Qabalah".to_string(), VoicePattern {
            formality_level: 0.8,
            mystical_terminology: vec!["sephiroth".to_string(), "pathworking".to_string(), "emanation".to_string()],
            sentence_structure: "structured_analytical".to_string(),
            emotional_tone: "wise_instructive".to_string(),
        });
    }

    fn initialize_aethyr_modifiers(&mut self) {
        self.aethyr_influence_modifiers.insert(1, AethyrModifier {
            tier: 1,
            name: "Transcendence".to_string(),
            intensity_multiplier: 1.2,
            wisdom_depth_bonus: 0.15,
            challenge_difficulty_modifier: 1.1,
            authenticity_enhancement: 0.1,
        });

        self.aethyr_influence_modifiers.insert(2, AethyrModifier {
            tier: 2,
            name: "Mastery".to_string(),
            intensity_multiplier: 1.0,
            wisdom_depth_bonus: 0.1,
            challenge_difficulty_modifier: 1.0,
            authenticity_enhancement: 0.08,
        });
    }

    fn perform_comprehensive_adaptation(
        &self,
        quest_content: &str,
        governor: &GovernorTraits,
        player_context: &str
    ) -> StoryAdaptation {
        let mut adapted_elements = Vec::new();
        
        // Adapt dialogue elements
        let dialogue_adaptation = self.adapt_dialogue(quest_content, governor);
        adapted_elements.push(dialogue_adaptation);
        
        // Adapt challenge elements
        let challenge_adaptation = self.adapt_challenges(quest_content, governor);
        adapted_elements.push(challenge_adaptation);
        
        // Adapt teaching elements
        let teaching_adaptation = self.adapt_teaching_style(quest_content, governor);
        adapted_elements.push(teaching_adaptation);
        
        // Calculate overall scores
        let personality_influence = self.calculate_personality_influence(governor, &adapted_elements);
        let tradition_coherence = self.calculate_tradition_coherence(governor, &adapted_elements);
        let overall_authenticity = self.calculate_overall_authenticity(&adapted_elements);
        
        StoryAdaptation {
            quest_id: "adapted_quest".to_string(),
            governor_id: governor.governor_id,
            adapted_elements,
            personality_influence_score: personality_influence,
            tradition_coherence_score: tradition_coherence,
            overall_authenticity,
        }
    }

    fn adapt_dialogue(&self, content: &str, governor: &GovernorTraits) -> AdaptedStoryElement {
        let authority_modifier = if governor.personality_matrix.authority_level > 0.7 {
            "with commanding presence"
        } else {
            "with gentle guidance"
        };
        
        let adapted_content = format!(
            "Governor {} speaks {}: \"{}\"",
            governor.name,
            authority_modifier,
            self.transform_dialogue_for_governor(content, governor)
        );
        
        AdaptedStoryElement {
            element_type: StoryElementType::Dialogue,
            original_content: content.to_string(),
            adapted_content,
            governor_influence: governor.personality_matrix.authority_level,
            authenticity_enhancement: 0.12,
            tradition_integration: governor.tradition_affinities.keys().cloned().collect(),
        }
    }

    fn adapt_challenges(&self, content: &str, governor: &GovernorTraits) -> AdaptedStoryElement {
        let challenge_intensity = if governor.personality_matrix.challenge_preference > 0.7 {
            "demanding trials"
        } else {
            "gentle tests"
        };
        
        let adapted_content = format!(
            "The governor presents {} that reflect their mastery of {}",
            challenge_intensity,
            governor.domain
        );
        
        AdaptedStoryElement {
            element_type: StoryElementType::Challenge,
            original_content: content.to_string(),
            adapted_content,
            governor_influence: governor.personality_matrix.challenge_preference,
            authenticity_enhancement: 0.1,
            tradition_integration: governor.tradition_affinities.keys().cloned().collect(),
        }
    }

    fn adapt_teaching_style(&self, content: &str, governor: &GovernorTraits) -> AdaptedStoryElement {
        let teaching_approach = if governor.personality_matrix.wisdom_approach > 0.7 {
            "direct transmission of knowledge"
        } else {
            "guided discovery through experience"
        };
        
        let adapted_content = format!(
            "Through {}, the governor imparts wisdom of {}",
            teaching_approach,
            governor.domain
        );
        
        AdaptedStoryElement {
            element_type: StoryElementType::Teaching,
            original_content: content.to_string(),
            adapted_content,
            governor_influence: governor.personality_matrix.wisdom_approach,
            authenticity_enhancement: 0.15,
            tradition_integration: governor.tradition_affinities.keys().cloned().collect(),
        }
    }

    fn transform_dialogue_for_governor(&self, content: &str, governor: &GovernorTraits) -> String {
        // Apply governor-specific dialogue transformations
        let mut transformed = content.to_string();
        
        // Add governor-specific terminology
        for specialization in &governor.wisdom_specializations {
            if transformed.contains("wisdom") {
                transformed = transformed.replace("wisdom", &format!("{} wisdom", specialization.domain));
            }
        }
        
        // Apply tradition-specific voice patterns
        for (tradition, affinity) in &governor.tradition_affinities {
            if *affinity > 0.8 {
                if let Some(voice_pattern) = self.tradition_voice_patterns.get(tradition) {
                    transformed = self.apply_voice_pattern(&transformed, voice_pattern);
                }
            }
        }
        
        transformed
    }

    fn apply_voice_pattern(&self, text: &str, pattern: &VoicePattern) -> String {
        let mut result = text.to_string();
        
        // Apply mystical terminology
        for term in &pattern.mystical_terminology {
            if result.contains("power") {
                result = result.replace("power", term);
                break;
            }
        }
        
        result
    }

    fn create_contextual_dialogue(&self, governor: &GovernorTraits, context: &str, action: &str) -> String {
        format!(
            "Governor {} responds to your {} with {} wisdom: \"Through the sacred domain of {}, I guide you toward authentic understanding.\"",
            governor.name,
            action,
            governor.domain.to_lowercase(),
            governor.domain
        )
    }

    fn calculate_personality_influence(&self, governor: &GovernorTraits, elements: &[AdaptedStoryElement]) -> f64 {
        let total_influence: f64 = elements.iter().map(|e| e.governor_influence).sum();
        total_influence / elements.len() as f64
    }

    fn calculate_tradition_coherence(&self, governor: &GovernorTraits, elements: &[AdaptedStoryElement]) -> f64 {
        // Calculate how well the adaptations maintain tradition coherence
        0.85 // Simplified calculation
    }

    fn calculate_overall_authenticity(&self, elements: &[AdaptedStoryElement]) -> f64 {
        let total_authenticity: f64 = elements.iter().map(|e| e.authenticity_enhancement).sum();
        0.9 + (total_authenticity / elements.len() as f64)
    }

    fn create_fallback_adaptation(&self, content: &str, governor_id: u32) -> String {
        format!("Governor {} provides guidance: {}", governor_id, content)
    }

    fn create_fallback_dialogue(&self, governor_id: u32) -> String {
        format!("Governor {} speaks with divine authority: \"Seek wisdom through authentic practice.\"", governor_id)
    }
}

// Supporting structures
pub struct AdaptationTemplate {
    pub template_id: String,
    pub element_type: StoryElementType,
    pub base_pattern: String,
    pub adaptation_rules: Vec<AdaptationRule>,
}

pub struct AdaptationRule {
    pub condition: String,
    pub transformation: String,
    pub authenticity_bonus: f64,
}

pub struct VoicePattern {
    pub formality_level: f64,
    pub mystical_terminology: Vec<String>,
    pub sentence_structure: String,
    pub emotional_tone: String,
}

pub struct AethyrModifier {
    pub tier: u32,
    pub name: String,
    pub intensity_multiplier: f64,
    pub wisdom_depth_bonus: f64,
    pub challenge_difficulty_modifier: f64,
    pub authenticity_enhancement: f64,
}
