// Enochian Cyphers Story Engine - Branching Logic
// I Ching-based quest progression with authentic mystical decision trees

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestBranch {
    pub branch_id: String,
    pub parent_quest_id: String,
    pub choice_description: String,
    pub consequences: Vec<Consequence>,
    pub tradition_requirements: Vec<String>,
    pub difficulty_level: u32,
    pub authenticity_impact: f64,
    pub next_quest_options: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Consequence {
    pub consequence_type: ConsequenceType,
    pub description: String,
    pub impact_value: f64,
    pub duration: ConsequenceDuration,
    pub tradition_alignment: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConsequenceType {
    ReputationChange,
    SkillGain,
    WisdomUnlock,
    TraditionMastery,
    GovernorRelationship,
    AethyrAccess,
    SacredKnowledge,
    EnergyModification,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConsequenceDuration {
    Temporary,
    Permanent,
    QuestLine,
    Conditional,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BranchingContext {
    pub player_reputation: HashMap<String, f64>,
    pub tradition_mastery: HashMap<String, f64>,
    pub governor_relationships: HashMap<String, f64>,
    pub completed_quests: Vec<String>,
    pub current_aethyr_access: Vec<u32>,
    pub energy_level: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IChingGuidance {
    pub hexagram_number: u32,
    pub hexagram_name: String,
    pub changing_lines: Vec<u32>,
    pub guidance_text: String,
    pub elemental_influence: String,
    pub recommended_action: String,
    pub caution_areas: Vec<String>,
}

#[wasm_bindgen]
pub struct BranchingEngine {
    branch_templates: HashMap<String, Vec<QuestBranch>>,
    consequence_rules: HashMap<String, Vec<ConsequenceRule>>,
    i_ching_mappings: HashMap<u32, IChingGuidance>,
    tradition_synergies: HashMap<String, Vec<String>>,
}

#[wasm_bindgen]
impl BranchingEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> BranchingEngine {
        let mut engine = BranchingEngine {
            branch_templates: HashMap::new(),
            consequence_rules: HashMap::new(),
            i_ching_mappings: HashMap::new(),
            tradition_synergies: HashMap::new(),
        };
        
        engine.initialize_i_ching_mappings();
        engine.initialize_tradition_synergies();
        engine.initialize_branch_templates();
        
        engine
    }

    #[wasm_bindgen]
    pub fn generate_quest_branches(
        &self,
        quest_id: &str,
        context: &str,
        seed: u32
    ) -> String {
        let branching_context: BranchingContext = match serde_json::from_str(context) {
            Ok(ctx) => ctx,
            Err(_) => self.create_default_context(),
        };

        // Generate I Ching guidance for branching
        let hexagram_number = (seed % 64) + 1;
        let i_ching_guidance = self.i_ching_mappings.get(&hexagram_number)
            .cloned()
            .unwrap_or_else(|| self.create_default_guidance(hexagram_number));

        // Generate branches based on I Ching and context
        let branches = self.create_contextual_branches(
            quest_id,
            &branching_context,
            &i_ching_guidance,
            seed
        );

        serde_json::to_string(&branches).unwrap_or_else(|_| "[]".to_string())
    }

    #[wasm_bindgen]
    pub fn evaluate_choice_consequences(
        &self,
        branch_id: &str,
        context: &str
    ) -> String {
        let branching_context: BranchingContext = match serde_json::from_str(context) {
            Ok(ctx) => ctx,
            Err(_) => self.create_default_context(),
        };

        let consequences = self.calculate_consequences(branch_id, &branching_context);
        serde_json::to_string(&consequences).unwrap_or_else(|_| "[]".to_string())
    }

    fn initialize_i_ching_mappings(&mut self) {
        // Initialize key I Ching hexagrams for quest branching
        self.i_ching_mappings.insert(1, IChingGuidance {
            hexagram_number: 1,
            hexagram_name: "The Creative".to_string(),
            changing_lines: vec![],
            guidance_text: "Pure creative force manifests through divine will and authentic action.".to_string(),
            elemental_influence: "Heaven".to_string(),
            recommended_action: "Take bold initiative in spiritual practice".to_string(),
            caution_areas: vec!["Avoid spiritual pride".to_string()],
        });

        self.i_ching_mappings.insert(2, IChingGuidance {
            hexagram_number: 2,
            hexagram_name: "The Receptive".to_string(),
            changing_lines: vec![],
            guidance_text: "Receptive wisdom allows divine knowledge to flow through humble acceptance.".to_string(),
            elemental_influence: "Earth".to_string(),
            recommended_action: "Practice receptive meditation and listening".to_string(),
            caution_areas: vec!["Avoid passive inaction".to_string()],
        });

        self.i_ching_mappings.insert(11, IChingGuidance {
            hexagram_number: 11,
            hexagram_name: "Peace".to_string(),
            changing_lines: vec![],
            guidance_text: "Harmony between heaven and earth creates perfect conditions for spiritual growth.".to_string(),
            elemental_influence: "Heaven over Earth".to_string(),
            recommended_action: "Seek balance in all mystical practices".to_string(),
            caution_areas: vec!["Maintain vigilance during peaceful times".to_string()],
        });

        // Add more hexagrams as needed...
    }

    fn initialize_tradition_synergies(&mut self) {
        self.tradition_synergies.insert("Enochian".to_string(), vec![
            "Hermetic_Qabalah".to_string(),
            "Golden_Dawn".to_string(),
            "Thelema".to_string(),
        ]);

        self.tradition_synergies.insert("Hermetic_Qabalah".to_string(), vec![
            "Enochian".to_string(),
            "Alchemy".to_string(),
            "Astrology".to_string(),
        ]);

        self.tradition_synergies.insert("Chaos_Magic".to_string(), vec![
            "Thelema".to_string(),
            "Discordianism".to_string(),
            "Modern_Witchcraft".to_string(),
        ]);
    }

    fn initialize_branch_templates(&mut self) {
        // Initialize common branching patterns
        let enochian_branches = vec![
            QuestBranch {
                branch_id: "enochian_invocation".to_string(),
                parent_quest_id: "template".to_string(),
                choice_description: "Perform traditional Enochian invocation".to_string(),
                consequences: vec![
                    Consequence {
                        consequence_type: ConsequenceType::TraditionMastery,
                        description: "Gain deeper understanding of Enochian practices".to_string(),
                        impact_value: 0.15,
                        duration: ConsequenceDuration::Permanent,
                        tradition_alignment: "Enochian".to_string(),
                    }
                ],
                tradition_requirements: vec!["Enochian".to_string()],
                difficulty_level: 3,
                authenticity_impact: 0.1,
                next_quest_options: vec!["advanced_enochian".to_string()],
            },
            QuestBranch {
                branch_id: "hermetic_synthesis".to_string(),
                parent_quest_id: "template".to_string(),
                choice_description: "Integrate Hermetic Qabalah principles".to_string(),
                consequences: vec![
                    Consequence {
                        consequence_type: ConsequenceType::WisdomUnlock,
                        description: "Unlock Tree of Life pathworking".to_string(),
                        impact_value: 0.2,
                        duration: ConsequenceDuration::Permanent,
                        tradition_alignment: "Hermetic_Qabalah".to_string(),
                    }
                ],
                tradition_requirements: vec!["Hermetic_Qabalah".to_string()],
                difficulty_level: 4,
                authenticity_impact: 0.12,
                next_quest_options: vec!["sephiroth_mastery".to_string()],
            },
        ];

        self.branch_templates.insert("Enochian".to_string(), enochian_branches);
    }

    fn create_contextual_branches(
        &self,
        quest_id: &str,
        context: &BranchingContext,
        guidance: &IChingGuidance,
        seed: u32
    ) -> Vec<QuestBranch> {
        let mut branches = Vec::new();
        
        // Generate 3 branches based on I Ching guidance
        for i in 0..3 {
            let branch_seed = seed + i;
            let difficulty = self.calculate_contextual_difficulty(context, i);
            
            let branch = QuestBranch {
                branch_id: format!("{}_{}", quest_id, i + 1),
                parent_quest_id: quest_id.to_string(),
                choice_description: self.generate_choice_description(guidance, i),
                consequences: self.generate_contextual_consequences(context, guidance, i),
                tradition_requirements: self.determine_tradition_requirements(context, i),
                difficulty_level: difficulty,
                authenticity_impact: self.calculate_authenticity_impact(guidance, i),
                next_quest_options: self.generate_next_options(quest_id, i),
            };
            
            branches.push(branch);
        }
        
        branches
    }

    fn generate_choice_description(&self, guidance: &IChingGuidance, branch_index: usize) -> String {
        match branch_index {
            0 => format!("Follow the {} path: {}", guidance.elemental_influence, guidance.recommended_action),
            1 => format!("Embrace the wisdom of {}: Seek deeper understanding through contemplation", guidance.hexagram_name),
            2 => format!("Transform through {}: Apply the hexagram's teaching to overcome challenges", guidance.hexagram_name),
            _ => "Continue on the mystical path".to_string(),
        }
    }

    fn generate_contextual_consequences(
        &self,
        context: &BranchingContext,
        guidance: &IChingGuidance,
        branch_index: usize
    ) -> Vec<Consequence> {
        let mut consequences = Vec::new();
        
        match branch_index {
            0 => {
                consequences.push(Consequence {
                    consequence_type: ConsequenceType::ReputationChange,
                    description: format!("Reputation increases with {} alignment", guidance.elemental_influence),
                    impact_value: 0.1,
                    duration: ConsequenceDuration::Permanent,
                    tradition_alignment: "Enochian".to_string(),
                });
            },
            1 => {
                consequences.push(Consequence {
                    consequence_type: ConsequenceType::WisdomUnlock,
                    description: "Unlock deeper mystical understanding".to_string(),
                    impact_value: 0.15,
                    duration: ConsequenceDuration::Permanent,
                    tradition_alignment: "Universal".to_string(),
                });
            },
            2 => {
                consequences.push(Consequence {
                    consequence_type: ConsequenceType::SkillGain,
                    description: "Develop advanced spiritual techniques".to_string(),
                    impact_value: 0.2,
                    duration: ConsequenceDuration::QuestLine,
                    tradition_alignment: "Mixed".to_string(),
                });
            },
            _ => {}
        }
        
        consequences
    }

    fn calculate_contextual_difficulty(&self, context: &BranchingContext, branch_index: usize) -> u32 {
        let base_difficulty = match branch_index {
            0 => 2, // Easier path
            1 => 3, // Moderate path
            2 => 4, // Challenging path
            _ => 2,
        };
        
        // Adjust based on player's tradition mastery
        let avg_mastery: f64 = context.tradition_mastery.values().sum::<f64>() / context.tradition_mastery.len() as f64;
        let mastery_modifier = if avg_mastery > 0.7 { 1 } else { 0 };
        
        (base_difficulty + mastery_modifier).min(5)
    }

    fn determine_tradition_requirements(&self, context: &BranchingContext, branch_index: usize) -> Vec<String> {
        match branch_index {
            0 => vec!["Enochian".to_string()],
            1 => vec!["Hermetic_Qabalah".to_string()],
            2 => vec!["Enochian".to_string(), "Hermetic_Qabalah".to_string()],
            _ => vec![],
        }
    }

    fn calculate_authenticity_impact(&self, guidance: &IChingGuidance, branch_index: usize) -> f64 {
        match branch_index {
            0 => 0.08, // Traditional approach
            1 => 0.12, // Wisdom-focused approach
            2 => 0.15, // Challenging synthesis approach
            _ => 0.05,
        }
    }

    fn generate_next_options(&self, quest_id: &str, branch_index: usize) -> Vec<String> {
        match branch_index {
            0 => vec![format!("{}_traditional_path", quest_id)],
            1 => vec![format!("{}_wisdom_path", quest_id)],
            2 => vec![format!("{}_synthesis_path", quest_id)],
            _ => vec![],
        }
    }

    fn calculate_consequences(&self, branch_id: &str, context: &BranchingContext) -> Vec<Consequence> {
        // Simplified consequence calculation
        vec![
            Consequence {
                consequence_type: ConsequenceType::ReputationChange,
                description: "Your choice affects your standing with the governors".to_string(),
                impact_value: 0.1,
                duration: ConsequenceDuration::Permanent,
                tradition_alignment: "Universal".to_string(),
            }
        ]
    }

    fn create_default_context(&self) -> BranchingContext {
        BranchingContext {
            player_reputation: HashMap::new(),
            tradition_mastery: HashMap::new(),
            governor_relationships: HashMap::new(),
            completed_quests: vec![],
            current_aethyr_access: vec![],
            energy_level: 25,
        }
    }

    fn create_default_guidance(&self, hexagram_number: u32) -> IChingGuidance {
        IChingGuidance {
            hexagram_number,
            hexagram_name: format!("Hexagram {}", hexagram_number),
            changing_lines: vec![],
            guidance_text: "Seek wisdom through authentic spiritual practice".to_string(),
            elemental_influence: "Universal".to_string(),
            recommended_action: "Follow the path of truth".to_string(),
            caution_areas: vec!["Avoid spiritual materialism".to_string()],
        }
    }
}

pub struct ConsequenceRule {
    pub rule_id: String,
    pub condition: String,
    pub consequence: Consequence,
}
