//! Authenticity validation and scoring system

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::{Result, EnochianError};

/// Authenticity score with detailed breakdown
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuthenticityScore {
    /// Overall authenticity score (0.0-1.0)
    pub overall_score: f64,
    /// Tradition alignment score
    pub tradition_alignment: f64,
    /// Historical accuracy score
    pub historical_accuracy: f64,
    /// Spiritual depth score
    pub spiritual_depth: f64,
    /// Practical applicability score
    pub practical_applicability: f64,
    /// Source quality score
    pub source_quality: f64,
    /// Detailed breakdown by component
    pub detailed_breakdown: HashMap<String, f64>,
    /// Validation notes
    pub validation_notes: Vec<String>,
    /// Improvement suggestions
    pub improvement_suggestions: Vec<String>,
}

/// Authenticity scorer with tradition-specific validation
#[derive(Debug, Clone)]
pub struct AuthenticityScorer {
    /// Tradition validators
    tradition_validators: HashMap<String, TraditionValidator>,
    /// Enochian keywords with weights
    enochian_keywords: HashMap<String, f64>,
    /// Historical markers
    historical_markers: HashMap<String, f64>,
    /// Spiritual depth indicators
    spiritual_indicators: Vec<String>,
    /// Source quality markers
    source_markers: HashMap<String, f64>,
}

/// Tradition-specific validator
#[derive(Debug, Clone)]
pub struct TraditionValidator {
    /// Primary sources for this tradition
    pub primary_sources: Vec<String>,
    /// Key concepts
    pub key_concepts: Vec<String>,
    /// Historical figures
    pub historical_figures: Vec<String>,
    /// Authenticity weight
    pub authenticity_weight: f64,
    /// Minimum threshold
    pub minimum_threshold: f64,
}

impl Default for AuthenticityScorer {
    fn default() -> Self {
        Self::new()
    }
}

impl AuthenticityScorer {
    /// Create a new authenticity scorer
    pub fn new() -> Self {
        let mut scorer = AuthenticityScorer {
            tradition_validators: HashMap::new(),
            enochian_keywords: HashMap::new(),
            historical_markers: HashMap::new(),
            spiritual_indicators: Vec::new(),
            source_markers: HashMap::new(),
        };
        
        scorer.initialize_validators();
        scorer.initialize_keywords();
        scorer.initialize_markers();
        scorer
    }
    
    /// Calculate comprehensive authenticity score
    pub fn calculate_authenticity(
        &self,
        content: &str,
        tradition: &str,
        sources: &[String],
        context: Option<&HashMap<String, serde_json::Value>>,
    ) -> Result<AuthenticityScore> {
        // Get tradition validator
        let validator = self.tradition_validators.get(tradition)
            .ok_or_else(|| EnochianError::TraditionNotSupported {
                tradition: tradition.to_string(),
            })?;
        
        // Calculate component scores
        let tradition_score = self.score_tradition_alignment(content, validator);
        let historical_score = self.score_historical_accuracy(content, tradition);
        let spiritual_score = self.score_spiritual_depth(content);
        let practical_score = self.score_practical_applicability(content);
        let source_score = self.score_source_quality(sources, tradition);
        
        // Calculate weighted overall score
        let weights = self.get_scoring_weights(tradition);
        let overall_score = (
            tradition_score * weights.tradition_alignment +
            historical_score * weights.historical_accuracy +
            spiritual_score * weights.spiritual_depth +
            practical_score * weights.practical_applicability +
            source_score * weights.source_quality
        ) * validator.authenticity_weight;
        
        // Generate detailed breakdown
        let mut detailed_breakdown = HashMap::new();
        detailed_breakdown.insert("tradition_alignment".to_string(), tradition_score);
        detailed_breakdown.insert("historical_accuracy".to_string(), historical_score);
        detailed_breakdown.insert("spiritual_depth".to_string(), spiritual_score);
        detailed_breakdown.insert("practical_applicability".to_string(), practical_score);
        detailed_breakdown.insert("source_quality".to_string(), source_score);
        detailed_breakdown.insert("tradition_weight".to_string(), validator.authenticity_weight);
        
        // Generate validation notes and suggestions
        let validation_notes = self.generate_validation_notes(
            tradition_score, historical_score, spiritual_score, 
            practical_score, source_score, tradition
        );
        
        let improvement_suggestions = self.generate_improvement_suggestions(
            tradition_score, historical_score, spiritual_score,
            practical_score, source_score, tradition
        );
        
        Ok(AuthenticityScore {
            overall_score: overall_score.min(1.0),
            tradition_alignment: tradition_score,
            historical_accuracy: historical_score,
            spiritual_depth: spiritual_score,
            practical_applicability: practical_score,
            source_quality: source_score,
            detailed_breakdown,
            validation_notes,
            improvement_suggestions,
        })
    }
    
    /// Validate content meets minimum authenticity threshold
    pub fn validate_authenticity_threshold(
        &self,
        content: &str,
        tradition: &str,
        threshold: f64,
    ) -> Result<bool> {
        let score = self.calculate_authenticity(content, tradition, &[], None)?;
        Ok(score.overall_score >= threshold)
    }
    
    /// Get quick authenticity score (simplified calculation)
    pub fn quick_score(&self, content: &str) -> f64 {
        let content_lower = content.to_lowercase();
        let mut score = 0.85; // Base score
        
        // Check for Enochian keywords
        for (keyword, weight) in &self.enochian_keywords {
            if content_lower.contains(keyword) {
                score += weight * 0.01; // Small bonus per keyword
            }
        }
        
        // Check for historical markers
        for (marker, weight) in &self.historical_markers {
            if content_lower.contains(marker) {
                score += weight * 0.005; // Smaller bonus for historical markers
            }
        }
        
        // Check for spiritual indicators
        let spiritual_count = self.spiritual_indicators.iter()
            .filter(|indicator| content_lower.contains(&indicator.to_lowercase()))
            .count();
        
        if spiritual_count > 0 {
            score += (spiritual_count as f64 * 0.01).min(0.05);
        }
        
        score.min(1.0)
    }
    
    fn initialize_validators(&mut self) {
        // Enochian validator
        self.tradition_validators.insert("Enochian".to_string(), TraditionValidator {
            primary_sources: vec![
                "John Dee Spiritual Diaries".to_string(),
                "Edward Kelley Communications".to_string(),
                "Enochian Tablets".to_string(),
                "Watchtower Manuscripts".to_string(),
            ],
            key_concepts: vec![
                "angelic communication".to_string(),
                "aethyr".to_string(),
                "watchtower".to_string(),
                "governor".to_string(),
                "enochian language".to_string(),
                "scrying".to_string(),
                "spiritual diary".to_string(),
                "celestial hierarchy".to_string(),
            ],
            historical_figures: vec![
                "john dee".to_string(),
                "edward kelley".to_string(),
                "elizabeth i".to_string(),
            ],
            authenticity_weight: 1.0,
            minimum_threshold: 0.85,
        });
        
        // Hermetic Qabalah validator
        self.tradition_validators.insert("Hermetic_Qabalah".to_string(), TraditionValidator {
            primary_sources: vec![
                "Sefer Yetzirah".to_string(),
                "Zohar".to_string(),
                "Golden Dawn Manuscripts".to_string(),
                "Tree of Life Studies".to_string(),
            ],
            key_concepts: vec![
                "sephiroth".to_string(),
                "tree of life".to_string(),
                "pathworking".to_string(),
                "emanation".to_string(),
                "divine names".to_string(),
                "qabalah".to_string(),
                "hermetic".to_string(),
                "mystical union".to_string(),
            ],
            historical_figures: vec![
                "moses de leon".to_string(),
                "isaac luria".to_string(),
                "mathers".to_string(),
            ],
            authenticity_weight: 0.8,
            minimum_threshold: 0.80,
        });
        
        // Add more tradition validators as needed...
    }
    
    fn initialize_keywords(&mut self) {
        // Core Enochian terms (highest weight)
        self.enochian_keywords.insert("enochian".to_string(), 3.0);
        self.enochian_keywords.insert("aethyr".to_string(), 2.8);
        self.enochian_keywords.insert("governor".to_string(), 2.5);
        self.enochian_keywords.insert("watchtower".to_string(), 2.5);
        self.enochian_keywords.insert("angel".to_string(), 2.0);
        self.enochian_keywords.insert("angelic".to_string(), 2.0);
        
        // Historical figures (high weight)
        self.enochian_keywords.insert("john dee".to_string(), 2.8);
        self.enochian_keywords.insert("edward kelley".to_string(), 2.8);
        self.enochian_keywords.insert("dee".to_string(), 2.5);
        self.enochian_keywords.insert("kelley".to_string(), 2.5);
        
        // Enochian concepts (medium-high weight)
        self.enochian_keywords.insert("scrying".to_string(), 2.2);
        self.enochian_keywords.insert("spiritual diary".to_string(), 2.2);
        self.enochian_keywords.insert("tablet".to_string(), 2.0);
        self.enochian_keywords.insert("celestial".to_string(), 1.8);
        self.enochian_keywords.insert("divine".to_string(), 1.8);
        self.enochian_keywords.insert("sacred".to_string(), 1.5);
        
        // Practice-related terms (medium weight)
        self.enochian_keywords.insert("invocation".to_string(), 1.8);
        self.enochian_keywords.insert("communion".to_string(), 1.6);
        self.enochian_keywords.insert("vision".to_string(), 1.5);
        self.enochian_keywords.insert("mystical".to_string(), 1.4);
        self.enochian_keywords.insert("spiritual".to_string(), 1.3);
        self.enochian_keywords.insert("wisdom".to_string(), 1.2);
    }
    
    fn initialize_markers(&mut self) {
        // Historical markers
        self.historical_markers.insert("1582".to_string(), 2.5);
        self.historical_markers.insert("1583".to_string(), 2.5);
        self.historical_markers.insert("1584".to_string(), 2.5);
        self.historical_markers.insert("16th century".to_string(), 2.0);
        self.historical_markers.insert("elizabethan".to_string(), 2.0);
        self.historical_markers.insert("renaissance".to_string(), 1.8);
        self.historical_markers.insert("mortlake".to_string(), 2.2);
        self.historical_markers.insert("prague".to_string(), 2.0);
        
        // Spiritual indicators
        self.spiritual_indicators = vec![
            "spiritual development".to_string(),
            "inner transformation".to_string(),
            "divine communion".to_string(),
            "mystical union".to_string(),
            "sacred wisdom".to_string(),
            "enlightenment".to_string(),
            "transcendence".to_string(),
            "spiritual practice".to_string(),
            "authentic tradition".to_string(),
            "higher consciousness".to_string(),
            "divine guidance".to_string(),
            "spiritual growth".to_string(),
        ];
        
        // Source quality markers
        self.source_markers.insert("primary source".to_string(), 2.5);
        self.source_markers.insert("original manuscript".to_string(), 2.3);
        self.source_markers.insert("historical document".to_string(), 2.0);
        self.source_markers.insert("scholarly research".to_string(), 1.8);
        self.source_markers.insert("academic study".to_string(), 1.8);
        self.source_markers.insert("peer reviewed".to_string(), 1.5);
        self.source_markers.insert("authentic tradition".to_string(), 1.8);
        self.source_markers.insert("traditional practice".to_string(), 1.5);
    }
    
    fn score_tradition_alignment(&self, content: &str, validator: &TraditionValidator) -> f64 {
        let content_lower = content.to_lowercase();
        let word_count = content_lower.split_whitespace().count().max(1);
        
        // Score key concepts
        let mut concept_score = 0.0;
        for concept in &validator.key_concepts {
            if content_lower.contains(concept) {
                concept_score += 1.0 / validator.key_concepts.len() as f64;
            }
        }
        
        // Score historical figures
        let mut figure_score = 0.0;
        for figure in &validator.historical_figures {
            if content_lower.contains(figure) {
                figure_score += 1.0 / validator.historical_figures.len() as f64;
            }
        }
        
        // Combine scores
        let base_score = 0.6;
        let concept_bonus = concept_score * 0.3;
        let figure_bonus = figure_score * 0.1;
        
        (base_score + concept_bonus + figure_bonus).min(1.0)
    }
    
    fn score_historical_accuracy(&self, content: &str, tradition: &str) -> f64 {
        let content_lower = content.to_lowercase();
        let mut score = 0.7; // Base historical score
        
        // Check for historical markers
        for (marker, weight) in &self.historical_markers {
            if content_lower.contains(marker) {
                score += weight * 0.02;
            }
        }
        
        // Check for anachronisms
        let anachronisms = ["internet", "computer", "modern", "21st century", "smartphone"];
        for anachronism in &anachronisms {
            if content_lower.contains(anachronism) {
                score -= 0.1;
            }
        }
        
        score.max(0.0).min(1.0)
    }
    
    fn score_spiritual_depth(&self, content: &str) -> f64 {
        let content_lower = content.to_lowercase();
        let mut score = 0.6; // Base spiritual score
        
        // Check for spiritual depth indicators
        let depth_count = self.spiritual_indicators.iter()
            .filter(|indicator| content_lower.contains(&indicator.to_lowercase()))
            .count();
        
        if depth_count > 0 {
            let depth_bonus = (depth_count as f64 * 0.05).min(0.3);
            score += depth_bonus;
        }
        
        // Check for superficial content
        let materialistic_terms = ["money", "wealth", "power over others", "control", "manipulation"];
        for term in &materialistic_terms {
            if content_lower.contains(term) {
                score -= 0.1;
            }
        }
        
        score.max(0.0).min(1.0)
    }
    
    fn score_practical_applicability(&self, content: &str) -> f64 {
        let content_lower = content.to_lowercase();
        let mut score = 0.7; // Base practical score
        
        // Check for practical guidance
        let practical_terms = ["practice", "method", "technique", "exercise", "meditation", "study"];
        let practical_count = practical_terms.iter()
            .filter(|term| content_lower.contains(*term))
            .count();
        
        if practical_count > 0 {
            score += (practical_count as f64 * 0.04).min(0.2);
        }
        
        // Check for safety considerations
        let safety_terms = ["safe", "ethical", "responsible", "balanced", "grounded"];
        let safety_count = safety_terms.iter()
            .filter(|term| content_lower.contains(*term))
            .count();
        
        if safety_count > 0 {
            score += (safety_count as f64 * 0.02).min(0.1);
        }
        
        // Penalty for dangerous content
        let dangerous_terms = ["harmful", "dangerous", "unethical", "manipulative", "coercive"];
        for term in &dangerous_terms {
            if content_lower.contains(term) {
                score -= 0.2;
            }
        }
        
        score.max(0.0).min(1.0)
    }
    
    fn score_source_quality(&self, sources: &[String], tradition: &str) -> f64 {
        if sources.is_empty() {
            return 0.5; // Neutral score for no sources
        }
        
        let validator = self.tradition_validators.get(tradition);
        let primary_sources = validator.map(|v| &v.primary_sources).unwrap_or(&vec![]);
        
        let mut total_score = 0.0;
        let mut total_weight = 0.0;
        
        for source in sources {
            let source_lower = source.to_lowercase();
            let mut source_score = 0.3; // Base source score
            
            // Check if it's a primary source
            for primary in primary_sources {
                if primary.to_lowercase().contains(&source_lower) || source_lower.contains(&primary.to_lowercase()) {
                    source_score = 1.0;
                    break;
                }
            }
            
            // Check for source quality markers
            for (marker, weight) in &self.source_markers {
                if source_lower.contains(marker) {
                    source_score += weight * 0.1;
                }
            }
            
            total_score += source_score.min(1.0);
            total_weight += 1.0;
        }
        
        if total_weight > 0.0 {
            total_score / total_weight
        } else {
            0.5
        }
    }
    
    fn get_scoring_weights(&self, tradition: &str) -> ScoringWeights {
        match tradition {
            "Enochian" => ScoringWeights {
                tradition_alignment: 0.35,
                historical_accuracy: 0.25,
                spiritual_depth: 0.20,
                practical_applicability: 0.15,
                source_quality: 0.05,
            },
            "Hermetic_Qabalah" => ScoringWeights {
                tradition_alignment: 0.30,
                historical_accuracy: 0.20,
                spiritual_depth: 0.25,
                practical_applicability: 0.15,
                source_quality: 0.10,
            },
            _ => ScoringWeights {
                tradition_alignment: 0.30,
                historical_accuracy: 0.25,
                spiritual_depth: 0.20,
                practical_applicability: 0.15,
                source_quality: 0.10,
            },
        }
    }
    
    fn generate_validation_notes(
        &self,
        tradition_score: f64,
        historical_score: f64,
        spiritual_score: f64,
        practical_score: f64,
        source_score: f64,
        tradition: &str,
    ) -> Vec<String> {
        let mut notes = Vec::new();
        
        if tradition_score >= 0.9 {
            notes.push(format!("Excellent alignment with {} tradition", tradition));
        } else if tradition_score >= 0.8 {
            notes.push(format!("Good alignment with {} tradition", tradition));
        } else if tradition_score < 0.7 {
            notes.push(format!("Weak alignment with {} tradition - consider strengthening core concepts", tradition));
        }
        
        if historical_score >= 0.9 {
            notes.push("Strong historical accuracy".to_string());
        } else if historical_score < 0.7 {
            notes.push("Historical accuracy could be improved".to_string());
        }
        
        if spiritual_score >= 0.9 {
            notes.push("Excellent spiritual depth and meaning".to_string());
        } else if spiritual_score < 0.7 {
            notes.push("Consider deepening spiritual content".to_string());
        }
        
        if practical_score >= 0.9 {
            notes.push("Highly practical and applicable".to_string());
        } else if practical_score < 0.7 {
            notes.push("Could benefit from more practical guidance".to_string());
        }
        
        if source_score >= 0.8 {
            notes.push("Good source quality".to_string());
        } else if source_score < 0.6 {
            notes.push("Source quality could be improved".to_string());
        }
        
        notes
    }
    
    fn generate_improvement_suggestions(
        &self,
        tradition_score: f64,
        historical_score: f64,
        spiritual_score: f64,
        practical_score: f64,
        source_score: f64,
        tradition: &str,
    ) -> Vec<String> {
        let mut suggestions = Vec::new();
        
        if tradition_score < 0.8 {
            if let Some(validator) = self.tradition_validators.get(tradition) {
                let key_concepts: Vec<&str> = validator.key_concepts.iter().take(3).map(|s| s.as_str()).collect();
                suggestions.push(format!("Strengthen {} alignment by incorporating: {}", tradition, key_concepts.join(", ")));
            }
        }
        
        if historical_score < 0.8 {
            suggestions.push("Improve historical accuracy with period-appropriate references".to_string());
        }
        
        if spiritual_score < 0.8 {
            suggestions.push("Deepen spiritual content with more meaningful insights".to_string());
        }
        
        if practical_score < 0.8 {
            suggestions.push("Add more practical guidance and safe methods".to_string());
        }
        
        if source_score < 0.7 {
            suggestions.push("Include references to primary sources and scholarly works".to_string());
        }
        
        suggestions
    }
}

/// Scoring weights for different components
#[derive(Debug, Clone)]
struct ScoringWeights {
    tradition_alignment: f64,
    historical_accuracy: f64,
    spiritual_depth: f64,
    practical_applicability: f64,
    source_quality: f64,
}
