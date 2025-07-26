// Enochian Cyphers Build Script
// Custom build configuration for WASM compilation and optimization

use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=story-engine/");
    println!("cargo:rerun-if-changed=ui/");
    
    let target = env::var("TARGET").unwrap_or_default();
    let profile = env::var("PROFILE").unwrap_or_default();
    
    // Configure for WASM target
    if target.contains("wasm32") {
        configure_wasm_build();
    }
    
    // Optimize for release builds
    if profile == "release" {
        configure_release_optimizations();
    }
    
    // Generate build metadata
    generate_build_metadata();
    
    // Validate sacred constraints
    validate_sacred_constraints();
}

fn configure_wasm_build() {
    println!("cargo:rustc-cfg=wasm_target");
    
    // Set WASM-specific flags
    println!("cargo:rustc-link-arg=--import-memory");
    println!("cargo:rustc-link-arg=--max-memory=67108864"); // 64MB max memory
    
    // Enable WASM optimizations
    if env::var("CARGO_CFG_TARGET_ARCH").unwrap_or_default() == "wasm32" {
        println!("cargo:rustc-env=WASM_BINDGEN_SPLIT_LINKED_MODULES=1");
        println!("cargo:rustc-env=WASM_BINDGEN_DEMANGLE_NAME_SECTION=1");
    }
}

fn configure_release_optimizations() {
    // Enable additional optimizations for release builds
    println!("cargo:rustc-cfg=optimized_build");
    
    // Link-time optimization flags
    println!("cargo:rustc-link-arg=-s"); // Strip symbols
    println!("cargo:rustc-link-arg=--gc-sections"); // Remove unused sections
    
    // Size optimizations for Ordinals compliance
    println!("cargo:rustc-env=CARGO_CFG_OPTIMIZE_SIZE=1");
}

fn generate_build_metadata() {
    let build_time = chrono::Utc::now().format("%Y-%m-%d %H:%M:%S UTC").to_string();
    let git_hash = get_git_hash().unwrap_or_else(|| "unknown".to_string());
    let version = env::var("CARGO_PKG_VERSION").unwrap_or_else(|_| "0.1.0".to_string());
    
    let metadata = format!(
        r#"
// Auto-generated build metadata
pub const BUILD_TIME: &str = "{}";
pub const GIT_HASH: &str = "{}";
pub const VERSION: &str = "{}";
pub const SACRED_ARCHITECTURE_VERSION: &str = "6-layer-v1.0";
pub const TRADITION_COUNT: usize = 26;
pub const GOVERNOR_COUNT: usize = 91;
pub const AETHYR_COUNT: usize = 30;
"#,
        build_time, git_hash, version
    );
    
    let out_dir = env::var("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("build_metadata.rs");
    fs::write(&dest_path, metadata).expect("Failed to write build metadata");
    
    println!("cargo:rustc-env=BUILD_METADATA_PATH={}", dest_path.display());
}

fn validate_sacred_constraints() {
    // Validate that sacred constraints are maintained
    let mut violations = Vec::new();
    
    // Check tradition count
    if let Ok(traditions_dir) = fs::read_dir("lighthouse/traditions") {
        let tradition_count = traditions_dir.count();
        if tradition_count != 26 {
            violations.push(format!("Expected 26 traditions, found {}", tradition_count));
        }
    }
    
    // Check governor profiles
    if let Ok(governors_dir) = fs::read_dir("governor_profiles") {
        let governor_count = governors_dir.count();
        if governor_count != 91 {
            violations.push(format!("Expected 91 governors, found {}", governor_count));
        }
    }
    
    // Check story engine structure
    if !Path::new("story-engine/core").exists() {
        violations.push("Story engine core directory missing".to_string());
    }
    
    if !violations.is_empty() {
        eprintln!("Sacred constraint violations detected:");
        for violation in &violations {
            eprintln!("  - {}", violation);
        }
        panic!("Build failed due to sacred constraint violations");
    }
    
    println!("cargo:warning=Sacred constraints validated successfully");
}

fn get_git_hash() -> Option<String> {
    let output = Command::new("git")
        .args(&["rev-parse", "--short", "HEAD"])
        .output()
        .ok()?;
    
    if output.status.success() {
        Some(String::from_utf8_lossy(&output.stdout).trim().to_string())
    } else {
        None
    }
}
