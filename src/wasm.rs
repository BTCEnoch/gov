//! WASM bindings for browser integration

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;
#[cfg(feature = "wasm")]
use serde::{Deserialize, Serialize};
#[cfg(feature = "wasm")]
use std::collections::HashMap;
#[cfg(feature = "wasm")]
use crate::{EnochianCore, SystemConfig, GameState, QuestData, AuthenticityScorer, Result};

#[cfg(feature = "wasm")]
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
    
    #[wasm_bindgen(js_namespace = console)]
    fn error(s: &str);
}

#[cfg(feature = "wasm")]
macro_rules! console_log {
    ($($t:tt)*) => (log(&format_args!($($t)*).to_string()))
}

#[cfg(feature = "wasm")]
macro_rules! console_error {
    ($($t:tt)*) => (error(&format_args!($($t)*).to_string()))
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct EnochianWasm {
    core: EnochianCore,
    authenticity_scorer: AuthenticityScorer,
    initialized: bool,
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl EnochianWasm {
    #[wasm_bindgen(constructor)]
    pub fn new() -> EnochianWasm {
        console_error_panic_hook::set_once();
        
        let config = SystemConfig::default();
        let core = EnochianCore::new(config);
        let authenticity_scorer = AuthenticityScorer::new();
        
        EnochianWasm {
            core,
            authenticity_scorer,
            initialized: false,
        }
    }
    
    #[wasm_bindgen]
    pub fn initialize(&mut self, config_json: Option<String>) -> Result<(), JsValue> {
        console_log!("Initializing Enochian Cyphers WASM...");
        
        // Parse configuration if provided
        if let Some(config_str) = config_json {
            match serde_json::from_str::<SystemConfig>(&config_str) {
                Ok(config) => {
                    self.core = EnochianCore::new(config);
                },
                Err(e) => {
                    console_error!("Failed to parse configuration: {}", e);
                    return Err(JsValue::from_str(&format!("Configuration error: {}", e)));
                }
            }
        }
        
        // Initialize core system
        match self.core.initialize() {
            Ok(_) => {
                self.initialized = true;
                console_log!("Enochian Cyphers WASM initialized successfully");
                Ok(())
            },
            Err(e) => {
                console_error!("Failed to initialize core: {}", e);
                Err(JsValue::from_str(&format!("Initialization error: {}", e)))
            }
        }
    }
    
    #[wasm_bindgen]
    pub fn create_player(&mut self, player_id: String) -> Result<String, JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        match self.core.create_player_state(player_id) {
            Ok(state) => {
                match serde_json::to_string(state) {
                    Ok(json) => Ok(json),
                    Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
                }
            },
            Err(e) => Err(JsValue::from_str(&format!("Player creation error: {}", e)))
        }
    }
    
    #[wasm_bindgen]
    pub fn get_player_state(&self, player_id: String) -> Result<String, JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        match self.core.get_player_state(&player_id) {
            Some(state) => {
                match serde_json::to_string(state) {
                    Ok(json) => Ok(json),
                    Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
                }
            },
            None => Err(JsValue::from_str("Player not found"))
        }
    }
    
    #[wasm_bindgen]
    pub fn register_quest(&mut self, quest_json: String) -> Result<(), JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        let quest: QuestData = serde_json::from_str(&quest_json)
            .map_err(|e| JsValue::from_str(&format!("Quest parsing error: {}", e)))?;
        
        self.core.register_quest(quest)
            .map_err(|e| JsValue::from_str(&format!("Quest registration error: {}", e)))
    }
    
    #[wasm_bindgen]
    pub fn start_quest(&mut self, player_id: String, quest_id: String) -> Result<(), JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        self.core.start_quest(&player_id, &quest_id)
            .map_err(|e| JsValue::from_str(&format!("Quest start error: {}", e)))
    }
    
    #[wasm_bindgen]
    pub fn complete_quest(&mut self, player_id: String, quest_id: String) -> Result<String, JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        match self.core.complete_quest(&player_id, &quest_id) {
            Ok(rewards) => {
                match serde_json::to_string(&rewards) {
                    Ok(json) => Ok(json),
                    Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
                }
            },
            Err(e) => Err(JsValue::from_str(&format!("Quest completion error: {}", e)))
        }
    }
    
    #[wasm_bindgen]
    pub fn calculate_authenticity(&self, 
                                 content: String, 
                                 tradition: String,
                                 sources_json: Option<String>) -> Result<String, JsValue> {
        let sources = if let Some(sources_str) = sources_json {
            serde_json::from_str::<Vec<String>>(&sources_str)
                .map_err(|e| JsValue::from_str(&format!("Sources parsing error: {}", e)))?
        } else {
            Vec::new()
        };
        
        match self.authenticity_scorer.calculate_authenticity(&content, &tradition, &sources, None) {
            Ok(score) => {
                match serde_json::to_string(&score) {
                    Ok(json) => Ok(json),
                    Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
                }
            },
            Err(e) => Err(JsValue::from_str(&format!("Authenticity calculation error: {}", e)))
        }
    }
    
    #[wasm_bindgen]
    pub fn quick_authenticity_score(&self, content: String) -> f64 {
        self.authenticity_scorer.quick_score(&content)
    }
    
    #[wasm_bindgen]
    pub fn validate_authenticity_threshold(&self, 
                                         content: String, 
                                         tradition: String,
                                         threshold: f64) -> Result<bool, JsValue> {
        self.authenticity_scorer.validate_authenticity_threshold(&content, &tradition, threshold)
            .map_err(|e| JsValue::from_str(&format!("Validation error: {}", e)))
    }
    
    #[wasm_bindgen]
    pub fn get_system_statistics(&self) -> Result<String, JsValue> {
        if !self.initialized {
            return Err(JsValue::from_str("System not initialized"));
        }
        
        let stats = self.core.get_statistics();
        match serde_json::to_string(&stats) {
            Ok(json) => Ok(json),
            Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
        }
    }
    
    #[wasm_bindgen]
    pub fn get_system_info(&self) -> String {
        let info = crate::get_system_info();
        serde_json::to_string(&info).unwrap_or_else(|_| "{}".to_string())
    }
    
    #[wasm_bindgen]
    pub fn validate_sacred_constraints(&self) -> Result<(), JsValue> {
        crate::validate_sacred_constraints()
            .map_err(|e| JsValue::from_str(&format!("Sacred constraint violation: {}", e)))
    }
    
    #[wasm_bindgen]
    pub fn get_tradition_names(&self) -> Vec<String> {
        crate::traditions::TraditionManager::new().get_tradition_names()
    }
    
    #[wasm_bindgen]
    pub fn get_governor_names(&self) -> Vec<String> {
        crate::governors::GovernorManager::new().get_governor_names()
    }
    
    #[wasm_bindgen]
    pub fn get_tradition_weight(&self, tradition: String) -> f64 {
        crate::traditions::TraditionManager::new().get_tradition_weight(&tradition)
    }
    
    #[wasm_bindgen]
    pub fn calculate_tradition_compatibility(&self, tradition1: String, tradition2: String) -> f64 {
        crate::traditions::TraditionManager::new().calculate_compatibility(&tradition1, &tradition2)
    }
    
    #[wasm_bindgen]
    pub fn get_governor_by_name(&self, name: String) -> Result<String, JsValue> {
        let manager = crate::governors::GovernorManager::new();
        match manager.get_governor_by_name(&name) {
            Some(governor) => {
                match serde_json::to_string(governor) {
                    Ok(json) => Ok(json),
                    Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
                }
            },
            None => Err(JsValue::from_str("Governor not found"))
        }
    }
    
    #[wasm_bindgen]
    pub fn find_governors_by_tradition(&self, tradition: String, min_affinity: f64) -> Result<String, JsValue> {
        let manager = crate::governors::GovernorManager::new();
        let governors = manager.find_governors_by_tradition(&tradition, min_affinity);
        
        let governor_names: Vec<String> = governors.iter().map(|g| g.name.clone()).collect();
        match serde_json::to_string(&governor_names) {
            Ok(json) => Ok(json),
            Err(e) => Err(JsValue::from_str(&format!("Serialization error: {}", e)))
        }
    }
    
    #[wasm_bindgen]
    pub fn get_build_metadata(&self) -> String {
        serde_json::json!({
            "version": crate::VERSION,
            "build_time": crate::BUILD_TIME,
            "git_hash": crate::GIT_HASH,
            "architecture_version": crate::SACRED_ARCHITECTURE_VERSION,
            "tradition_count": crate::TRADITION_COUNT,
            "governor_count": crate::GOVERNOR_COUNT,
            "aethyr_count": crate::AETHYR_COUNT,
        }).to_string()
    }
    
    #[wasm_bindgen]
    pub fn is_initialized(&self) -> bool {
        self.initialized
    }
}

// Utility functions for WASM
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn set_panic_hook() {
    console_error_panic_hook::set_once();
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn init_logger() {
    console_log!("Enochian Cyphers WASM logger initialized");
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn get_version() -> String {
    crate::VERSION.to_string()
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn get_build_time() -> String {
    crate::BUILD_TIME.to_string()
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn get_git_hash() -> String {
    crate::GIT_HASH.to_string()
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn validate_ordinals_size_limit(content: &str) -> bool {
    content.len() <= crate::constants::MAX_ORDINALS_SIZE
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn compress_for_ordinals(content: &str) -> Result<String, JsValue> {
    use std::io::Write;
    
    let mut encoder = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::best());
    encoder.write_all(content.as_bytes())
        .map_err(|e| JsValue::from_str(&format!("Compression error: {}", e)))?;
    
    let compressed = encoder.finish()
        .map_err(|e| JsValue::from_str(&format!("Compression finalization error: {}", e)))?;
    
    if compressed.len() > crate::constants::MAX_ORDINALS_SIZE {
        return Err(JsValue::from_str("Content too large even after compression"));
    }
    
    Ok(base64::encode(compressed))
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn decompress_from_ordinals(compressed_base64: &str) -> Result<String, JsValue> {
    use std::io::Read;
    
    let compressed = base64::decode(compressed_base64)
        .map_err(|e| JsValue::from_str(&format!("Base64 decode error: {}", e)))?;
    
    let mut decoder = flate2::read::GzDecoder::new(&compressed[..]);
    let mut decompressed = String::new();
    decoder.read_to_string(&mut decompressed)
        .map_err(|e| JsValue::from_str(&format!("Decompression error: {}", e)))?;
    
    Ok(decompressed)
}

// JavaScript integration helpers
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct WasmConfig {
    authenticity_threshold: f64,
    max_concurrent_quests: u32,
    enable_p2p_sync: bool,
    enable_bitcoin_integration: bool,
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl WasmConfig {
    #[wasm_bindgen(constructor)]
    pub fn new() -> WasmConfig {
        WasmConfig {
            authenticity_threshold: 0.95,
            max_concurrent_quests: 3,
            enable_p2p_sync: false,
            enable_bitcoin_integration: false,
        }
    }
    
    #[wasm_bindgen(getter)]
    pub fn authenticity_threshold(&self) -> f64 {
        self.authenticity_threshold
    }
    
    #[wasm_bindgen(setter)]
    pub fn set_authenticity_threshold(&mut self, threshold: f64) {
        self.authenticity_threshold = threshold.max(0.8).min(1.0);
    }
    
    #[wasm_bindgen(getter)]
    pub fn max_concurrent_quests(&self) -> u32 {
        self.max_concurrent_quests
    }
    
    #[wasm_bindgen(setter)]
    pub fn set_max_concurrent_quests(&mut self, max_quests: u32) {
        self.max_concurrent_quests = max_quests.max(1).min(10);
    }
    
    #[wasm_bindgen(getter)]
    pub fn enable_p2p_sync(&self) -> bool {
        self.enable_p2p_sync
    }
    
    #[wasm_bindgen(setter)]
    pub fn set_enable_p2p_sync(&mut self, enable: bool) {
        self.enable_p2p_sync = enable;
    }
    
    #[wasm_bindgen(getter)]
    pub fn enable_bitcoin_integration(&self) -> bool {
        self.enable_bitcoin_integration
    }
    
    #[wasm_bindgen(setter)]
    pub fn set_enable_bitcoin_integration(&mut self, enable: bool) {
        self.enable_bitcoin_integration = enable;
    }
    
    #[wasm_bindgen]
    pub fn to_json(&self) -> String {
        let mut tradition_weighting = HashMap::new();
        tradition_weighting.insert("Enochian".to_string(), 0.6);
        tradition_weighting.insert("Hermetic_Qabalah".to_string(), 0.15);
        tradition_weighting.insert("Thelema".to_string(), 0.08);
        tradition_weighting.insert("Golden_Dawn".to_string(), 0.07);
        tradition_weighting.insert("Chaos_Magic".to_string(), 0.05);
        
        let config = SystemConfig {
            authenticity_threshold: self.authenticity_threshold,
            max_concurrent_quests: self.max_concurrent_quests,
            tradition_weighting,
            governor_interaction_cooldown: 144,
            enable_p2p_sync: self.enable_p2p_sync,
            enable_bitcoin_integration: self.enable_bitcoin_integration,
        };
        
        serde_json::to_string(&config).unwrap_or_else(|_| "{}".to_string())
    }
}

// Export main WASM interface
#[cfg(feature = "wasm")]
pub use EnochianWasm as EnochianCyphersWasm;

// Re-export for convenience
#[cfg(not(feature = "wasm"))]
pub struct EnochianWasm;

#[cfg(not(feature = "wasm"))]
impl EnochianWasm {
    pub fn new() -> Self {
        EnochianWasm
    }
}
