//! Enochian Cyphers - Bitcoin L1-native RPG with 6-layer sacred architecture
//! 
//! This crate provides the core functionality for the Enochian Cyphers game,
//! including story generation, authenticity validation, and Bitcoin L1 integration.

#![cfg_attr(docsrs, feature(doc_cfg))]
#![warn(missing_docs)]
#![warn(clippy::all)]
#![allow(clippy::too_many_arguments)]

// Include build metadata
include!(concat!(env!("OUT_DIR"), "/build_metadata.rs"));

// Core modules
pub mod core;
pub mod authenticity;
pub mod traditions;
pub mod governors;

// Feature-gated modules
#[cfg(feature = "story-engine")]
pub mod story_engine;

#[cfg(feature = "lighthouse")]
pub mod lighthouse;

#[cfg(feature = "tap-protocol")]
pub mod tap_protocol;

#[cfg(feature = "trac-indexer")]
pub mod trac_indexer;

#[cfg(feature = "wasm")]
pub mod wasm;

// Re-exports for convenience
pub use core::{EnochianCore, GameState, QuestData};
pub use authenticity::{AuthenticityScorer, AuthenticityScore};
pub use traditions::TraditionManager;
pub use governors::GovernorManager;

#[cfg(feature = "story-engine")]
pub use story_engine::StoryEngine;

#[cfg(feature = "wasm")]
pub use wasm::*;

/// Sacred architecture constants
pub mod constants {
    /// Number of sacred traditions
    pub const TRADITION_COUNT: usize = TRADITION_COUNT;
    
    /// Number of Governor Angels
    pub const GOVERNOR_COUNT: usize = GOVERNOR_COUNT;
    
    /// Number of Aethyr levels
    pub const AETHYR_COUNT: usize = AETHYR_COUNT;
    
    /// Minimum authenticity threshold
    pub const AUTHENTICITY_THRESHOLD: f64 = 0.95;
    
    /// Maximum Ordinals inscription size (1MB)
    pub const MAX_ORDINALS_SIZE: usize = 1_048_576;
    
    /// Enochian tradition weighting
    pub const ENOCHIAN_WEIGHTING: f64 = 0.6;
    
    /// Sacred architecture version
    pub const ARCHITECTURE_VERSION: &str = SACRED_ARCHITECTURE_VERSION;
}

/// Error types for the Enochian Cyphers system
#[derive(thiserror::Error, Debug)]
pub enum EnochianError {
    /// Authenticity validation failed
    #[error("Authenticity validation failed: {message}")]
    AuthenticityError { message: String },
    
    /// Sacred constraint violation
    #[error("Sacred constraint violation: {constraint}")]
    SacredConstraintViolation { constraint: String },
    
    /// Governor not found
    #[error("Governor {name} not found")]
    GovernorNotFound { name: String },
    
    /// Tradition not supported
    #[error("Tradition {tradition} not supported")]
    TraditionNotSupported { tradition: String },
    
    /// Quest generation failed
    #[error("Quest generation failed: {reason}")]
    QuestGenerationError { reason: String },
    
    /// Bitcoin integration error
    #[cfg(feature = "tap-protocol")]
    #[error("Bitcoin integration error: {message}")]
    BitcoinError { message: String },
    
    /// P2P network error
    #[cfg(feature = "trac-indexer")]
    #[error("P2P network error: {message}")]
    NetworkError { message: String },
    
    /// WASM runtime error
    #[cfg(feature = "wasm")]
    #[error("WASM runtime error: {message}")]
    WasmError { message: String },
    
    /// Serialization error
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    
    /// IO error
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    
    /// Generic error
    #[error("Enochian Cyphers error: {message}")]
    Generic { message: String },
}

/// Result type for Enochian Cyphers operations
pub type Result<T> = std::result::Result<T, EnochianError>;

/// Initialize the Enochian Cyphers system
pub fn initialize() -> Result<()> {
    // Initialize logging
    #[cfg(not(target_arch = "wasm32"))]
    env_logger::init();
    
    #[cfg(target_arch = "wasm32")]
    console_error_panic_hook::set_once();
    
    // Validate sacred constraints
    validate_sacred_constraints()?;
    
    log::info!("Enochian Cyphers initialized successfully");
    log::info!("Version: {}", VERSION);
    log::info!("Build time: {}", BUILD_TIME);
    log::info!("Git hash: {}", GIT_HASH);
    log::info!("Sacred architecture: {}", SACRED_ARCHITECTURE_VERSION);
    
    Ok(())
}

/// Validate sacred constraints at runtime
pub fn validate_sacred_constraints() -> Result<()> {
    // Validate tradition count
    if traditions::get_tradition_count() != constants::TRADITION_COUNT {
        return Err(EnochianError::SacredConstraintViolation {
            constraint: format!(
                "Expected {} traditions, found {}",
                constants::TRADITION_COUNT,
                traditions::get_tradition_count()
            ),
        });
    }
    
    // Validate governor count
    if governors::get_governor_count() != constants::GOVERNOR_COUNT {
        return Err(EnochianError::SacredConstraintViolation {
            constraint: format!(
                "Expected {} governors, found {}",
                constants::GOVERNOR_COUNT,
                governors::get_governor_count()
            ),
        });
    }
    
    // Validate Enochian primacy
    let enochian_weight = traditions::get_tradition_weight("Enochian");
    if (enochian_weight - constants::ENOCHIAN_WEIGHTING).abs() > 0.01 {
        return Err(EnochianError::SacredConstraintViolation {
            constraint: format!(
                "Enochian weighting must be {}, found {}",
                constants::ENOCHIAN_WEIGHTING,
                enochian_weight
            ),
        });
    }
    
    Ok(())
}

/// Get system information
pub fn get_system_info() -> serde_json::Value {
    serde_json::json!({
        "version": VERSION,
        "build_time": BUILD_TIME,
        "git_hash": GIT_HASH,
        "architecture_version": SACRED_ARCHITECTURE_VERSION,
        "tradition_count": constants::TRADITION_COUNT,
        "governor_count": constants::GOVERNOR_COUNT,
        "aethyr_count": constants::AETHYR_COUNT,
        "authenticity_threshold": constants::AUTHENTICITY_THRESHOLD,
        "enochian_weighting": constants::ENOCHIAN_WEIGHTING,
        "features": {
            "story_engine": cfg!(feature = "story-engine"),
            "lighthouse": cfg!(feature = "lighthouse"),
            "tap_protocol": cfg!(feature = "tap-protocol"),
            "trac_indexer": cfg!(feature = "trac-indexer"),
            "wasm": cfg!(feature = "wasm"),
            "server": cfg!(feature = "server"),
            "cli": cfg!(feature = "cli"),
        },
        "target": {
            "arch": env!("CARGO_CFG_TARGET_ARCH"),
            "os": env!("CARGO_CFG_TARGET_OS"),
            "family": env!("CARGO_CFG_TARGET_FAMILY"),
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_initialization() {
        assert!(initialize().is_ok());
    }
    
    #[test]
    fn test_sacred_constraints() {
        assert!(validate_sacred_constraints().is_ok());
    }
    
    #[test]
    fn test_system_info() {
        let info = get_system_info();
        assert!(info["version"].is_string());
        assert!(info["tradition_count"].as_u64().unwrap() == constants::TRADITION_COUNT as u64);
        assert!(info["governor_count"].as_u64().unwrap() == constants::GOVERNOR_COUNT as u64);
    }
    
    #[test]
    fn test_constants() {
        assert_eq!(constants::TRADITION_COUNT, 26);
        assert_eq!(constants::GOVERNOR_COUNT, 91);
        assert_eq!(constants::AETHYR_COUNT, 30);
        assert_eq!(constants::AUTHENTICITY_THRESHOLD, 0.95);
        assert_eq!(constants::ENOCHIAN_WEIGHTING, 0.6);
    }
}
