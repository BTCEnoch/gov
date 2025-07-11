# 🏛️ Enochian Governor Generator

A Bitcoin L1-native system for generating and managing 91 Governor Angels with authentic mystical knowledge from 18 traditions.

## Core Architecture

```
🏛️ THE LIGHTHOUSE (Knowledge Base)
    ↓ feeds wisdom to ↓
👑 GOVERNOR ANGELS (91 Unique AI Entities) 
    ↓ generate ↓
🎮 GAME CONTENT (Storylines/Events/Challenges/Riddles)
    ↓ delivered through ↓  
🌐 INTERACTIVE EXPERIENCES (Web/Game Interfaces)
```

## 📁 Complete Project Directory Map

**GitHub Repository:** https://github.com/BTCEnoch/gov

### 🔧 Root Configuration Files
- [`Cargo.toml`](https://github.com/BTCEnoch/gov/blob/main/Cargo.toml) - Rust project configuration
- [`Cargo.lock`](https://github.com/BTCEnoch/gov/blob/main/Cargo.lock) - Rust dependency lock file
- [`.gitignore`](https://github.com/BTCEnoch/gov/blob/main/.gitignore) - Git ignore patterns
- [`README.md`](https://github.com/BTCEnoch/gov/blob/main/README.md) - Project documentation

### 🏗️ Core System Components
**Base Path:** [`/core`](https://github.com/BTCEnoch/gov/tree/main/core)

#### 🎮 Game Assets
- [`/core/game_assets/`](https://github.com/BTCEnoch/gov/tree/main/core/game_assets)
  - [`/visual_aspects/`](https://github.com/BTCEnoch/gov/tree/main/core/game_assets/visual_aspects)
    - [`base.py`](https://github.com/BTCEnoch/gov/blob/main/core/game_assets/visual_aspects/base.py) - Base visual system
    - [`bitcoin_optimized.py`](https://github.com/BTCEnoch/gov/blob/main/core/game_assets/visual_aspects/bitcoin_optimized.py) - Bitcoin-optimized visuals
    - [`schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/game_assets/visual_aspects/schemas.py) - Visual data schemas

#### 👑 Governor Angels System
- [`/core/governors/`](https://github.com/BTCEnoch/gov/tree/main/core/governors)
  - [`/bitcoin/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/bitcoin) - Bitcoin L1 integration
    - [`inscriptions.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/bitcoin/inscriptions.py) - Ordinal inscriptions
    - [`ordinals.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/bitcoin/ordinals.py) - Ordinals management
    - [`schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/bitcoin/schemas.py) - Bitcoin schemas
    - [`state.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/bitcoin/state.py) - State management
  - [`/profiles/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/profiles) - 91 Governor profiles
    - [`ABRIOND.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/profiles/ABRIOND.json) - Governor ABRIOND profile
    - [`ADVORPT.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/profiles/ADVORPT.json) - Governor ADVORPT profile
    - [`AMBRIOL.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/profiles/AMBRIOL.json) - Governor AMBRIOL profile
    - *[+88 more Governor profiles...]*

#### 🔮 Mystical Traits System
- [`/core/governors/traits/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits)
  - [`generator.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/generator.py) - Trait generation engine
  - [`/archetypal_correspondences/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/archetypal_correspondences)
    - [`numerology.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/archetypal_correspondences/numerology.json) - Numerology correspondences
    - [`sephirot.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/archetypal_correspondences/sephirot.json) - Sephirotic correspondences
    - [`tarot.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/archetypal_correspondences/tarot.json) - Tarot correspondences
  - [`/schemas/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/schemas)
    - [`core_schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/schemas/core_schemas.py) - Core trait schemas
    - [`trait_schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/schemas/trait_schemas.py) - Trait-specific schemas

#### 🏛️ The Lighthouse (Knowledge Base)
- [`/core/governors/traits/knowledge_base/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base)
  - [`README.md`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/knowledge_base/README.md) - Knowledge base documentation
  - [`traditions.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/knowledge_base/traditions.json) - 18 mystical traditions
  - [`specializations.json`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/knowledge_base/specializations.json) - Knowledge specializations
  - [`enochian_knowledge_database.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/knowledge_base/enochian_knowledge_database.py) - Enochian knowledge
  - [`unified_knowledge_retriever.py`](https://github.com/BTCEnoch/gov/blob/main/core/governors/traits/knowledge_base/unified_knowledge_retriever.py) - Knowledge retrieval system

##### 🌍 Western Traditions
- [`/western/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/western)
  - [`/hermetic_philosophy/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/western/hermetic_philosophy) - Hermetic tradition
  - [`/kabbalistic_mysticism/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/western/kabbalistic_mysticism) - Kabbalistic tradition
  - [`/thelema/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/western/thelema) - Thelemic tradition

##### 🌏 Eastern Traditions
- [`/eastern/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/eastern)
  - [`/i_ching/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/eastern/i_ching) - I Ching system
  - [`/taoism/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/eastern/taoism) - Taoist tradition
  - [`/kuji_kiri/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/eastern/kuji_kiri) - Kuji-Kiri tradition

##### 🌐 Universal Traditions
- [`/universal/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/universal)
  - [`/tarot_knowledge/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/universal/tarot_knowledge) - Tarot system
  - [`/egyptian_magic/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/universal/egyptian_magic) - Egyptian magic
  - [`/chaos_magic/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/universal/chaos_magic) - Chaos magic
  - [`/sufi_mysticism/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/universal/sufi_mysticism) - Sufi tradition

##### 🏛️ Ancient Traditions
- [`/ancient/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/ancient)
  - [`/celtic_druidic/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/ancient/celtic_druidic) - Celtic Druidic tradition
  - [`/norse_traditions/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/ancient/norse_traditions) - Norse traditions
  - [`/classical_philosophy/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/ancient/classical_philosophy) - Classical philosophy

##### 🔬 Modern Synthesis
- [`/modern/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/modern)
  - [`/quantum_physics/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/modern/quantum_physics) - Quantum mysticism

##### 🗂️ Esoteric Systems
- [`/esoteric/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/esoteric)
  - [`/enochian/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/esoteric/enochian) - Enochian magic
  - [`/gnostic_traditions/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/esoteric/gnostic_traditions) - Gnostic traditions
  - [`/sacred_geometry/`](https://github.com/BTCEnoch/gov/tree/main/core/governors/traits/knowledge_base/esoteric/sacred_geometry) - Sacred geometry

#### 🔮 Mystical Systems Implementation
- [`/core/mystical_systems/`](https://github.com/BTCEnoch/gov/tree/main/core/mystical_systems)
  - [`/enochian_system/`](https://github.com/BTCEnoch/gov/tree/main/core/mystical_systems/enochian_system)
    - [`enochian_system.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/enochian_system/enochian_system.py) - Core Enochian system
    - [`cli.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/enochian_system/cli.py) - Command line interface
    - [`/data/enochian_database.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/enochian_system/data/enochian_database.py) - Enochian database
    - [`/relationships/relationship_engine.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/enochian_system/relationships/relationship_engine.py) - Relationship engine
    - [`/ritual_mechanics/ritual_engine.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/enochian_system/ritual_mechanics/ritual_engine.py) - Ritual mechanics
  - [`/tarot_system/`](https://github.com/BTCEnoch/gov/tree/main/core/mystical_systems/tarot_system)
    - [`tarot_system.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/tarot_system/tarot_system.py) - Tarot system core
    - [`/data/tarot_cards_database.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/tarot_system/data/tarot_cards_database.py) - Tarot cards database
    - [`/engines/reading_engine.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/tarot_system/engines/reading_engine.py) - Reading engine
    - [`/spreads/spread_definitions.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/tarot_system/spreads/spread_definitions.py) - Spread definitions
    - [`/ui/card_render.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/tarot_system/ui/card_render.py) - Card rendering
  - [`/iching_system/`](https://github.com/BTCEnoch/gov/tree/main/core/mystical_systems/iching_system)
    - [`iching_system.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/iching_system/iching_system.py) - I Ching system
    - [`/data/hexagram_database.py`](https://github.com/BTCEnoch/gov/blob/main/core/mystical_systems/iching_system/data/hexagram_database.py) - Hexagram database

#### 🎯 Quest System
- [`/core/questlines/`](https://github.com/BTCEnoch/gov/tree/main/core/questlines)
  - [`/templates/quest_template_manager.py`](https://github.com/BTCEnoch/gov/blob/main/core/questlines/templates/quest_template_manager.py) - Quest template manager

#### 🛠️ Utilities
- [`/core/utils/`](https://github.com/BTCEnoch/gov/tree/main/core/utils)
  - [`/bitcoin/art_generation.py`](https://github.com/BTCEnoch/gov/blob/main/core/utils/bitcoin/art_generation.py) - Bitcoin art generation
  - [`/mystical/`](https://github.com/BTCEnoch/gov/tree/main/core/utils/mystical) - Mystical utilities
    - [`base.py`](https://github.com/BTCEnoch/gov/blob/main/core/utils/mystical/base.py) - Base mystical utilities
    - [`bitcoin_integration.py`](https://github.com/BTCEnoch/gov/blob/main/core/utils/mystical/bitcoin_integration.py) - Bitcoin integration

#### 🏛️ Lighthouse Schema
- [`/core/lighthouse/schemas/`](https://github.com/BTCEnoch/gov/tree/main/core/lighthouse/schemas)
  - [`discovery_schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/lighthouse/schemas/discovery_schemas.py) - Discovery schemas
  - [`knowledge_schemas.py`](https://github.com/BTCEnoch/gov/blob/main/core/lighthouse/schemas/knowledge_schemas.py) - Knowledge schemas

### 📊 Data Sources
- [`/data/`](https://github.com/BTCEnoch/gov/tree/main/data)
  - [`aethyrs.json`](https://github.com/BTCEnoch/gov/blob/main/data/aethyrs.json) - Enochian Aethyrs data
  - [`/knowledge/`](https://github.com/BTCEnoch/gov/tree/main/data/knowledge) - Knowledge data sources

### 📚 Documentation
- [`/docs/`](https://github.com/BTCEnoch/gov/tree/main/docs)
  - [`/architecture/`](https://github.com/BTCEnoch/gov/tree/main/docs/architecture) - Architecture documentation
    - [`overview.md`](https://github.com/BTCEnoch/gov/blob/main/docs/architecture/overview.md) - System overview
    - [`high_level_overview_trac.md`](https://github.com/BTCEnoch/gov/blob/main/docs/architecture/high_level_overview_trac.md) - TRAC systems overview
    - [`storyline_generator_architecture.md`](https://github.com/BTCEnoch/gov/blob/main/docs/architecture/storyline_generator_architecture.md) - Storyline architecture
    - [`/diagrams/`](https://github.com/BTCEnoch/gov/tree/main/docs/architecture/diagrams) - Architecture diagrams
      - [`core_architecture.md`](https://github.com/BTCEnoch/gov/blob/main/docs/architecture/diagrams/core_architecture.md) - Core architecture diagram
      - [`data_flow.md`](https://github.com/BTCEnoch/gov/blob/main/docs/architecture/diagrams/data_flow.md) - Data flow diagram
  - [`/trac_docs/`](https://github.com/BTCEnoch/gov/tree/main/docs/trac_docs) - TRAC protocol documentation
    - [`ui_build_checklist_trac.md`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/ui_build_checklist_trac.md) - UI build checklist
    - [`template_psudocode_samples_trac.md`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/template_psudocode_samples_trac.md) - TRAC pseudocode samples
    - [`trac_build_review.md`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/trac_build_review.md) - TRAC build review
    - [`TAP_TRAC_RESOURCES.md`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/TAP_TRAC_RESOURCES.md) - TAP/TRAC resources
    - [`utility_matrix.md`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/utility_matrix.md) - Utility matrix
    - [`manifest_automation_system.py`](https://github.com/BTCEnoch/gov/blob/main/docs/trac_docs/manifest_automation_system.py) - Manifest automation

### 🧪 Test Suites
- [`/tests/`](https://github.com/BTCEnoch/gov/tree/main/tests)
  - [`/core/`](https://github.com/BTCEnoch/gov/tree/main/tests/core) - Core system tests
    - [`test_bitcoin_integration.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/test_bitcoin_integration.py) - Bitcoin integration tests
    - [`test_bitcoin_kabbalah.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/test_bitcoin_kabbalah.py) - Bitcoin-Kabbalah tests
    - [`test_bitcoin_tarot.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/test_bitcoin_tarot.py) - Bitcoin-Tarot tests
    - [`/enochian_system/`](https://github.com/BTCEnoch/gov/tree/main/tests/core/enochian_system) - Enochian system tests
      - [`test_enochian_system.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/enochian_system/test_enochian_system.py) - Enochian system tests
      - [`test_cli.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/enochian_system/test_cli.py) - CLI tests
    - [`/governors/`](https://github.com/BTCEnoch/gov/tree/main/tests/core/governors) - Governor tests
      - [`test_profile_generator.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/governors/test_profile_generator.py) - Profile generator tests
      - [`test_visual_aspects.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/governors/test_visual_aspects.py) - Visual aspects tests
      - [`/traits/`](https://github.com/BTCEnoch/gov/tree/main/tests/core/governors/traits) - Trait tests
        - [`test_trait_generator.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/governors/traits/test_trait_generator.py) - Trait generator tests
        - [`test_knowledge_mapper.py`](https://github.com/BTCEnoch/gov/blob/main/tests/core/governors/traits/test_knowledge_mapper.py) - Knowledge mapper tests

### 🚀 Rust/WASM Implementation
- [`/src/`](https://github.com/BTCEnoch/gov/tree/main/src)
  - [`lib.rs`](https://github.com/BTCEnoch/gov/blob/main/src/lib.rs) - Rust library entry point
- [`/pkg/`](https://github.com/BTCEnoch/gov/tree/main/pkg) - WASM package output
  - [`package.json`](https://github.com/BTCEnoch/gov/blob/main/pkg/package.json) - NPM package configuration
  - [`enochian_cyphers.js`](https://github.com/BTCEnoch/gov/blob/main/pkg/enochian_cyphers.js) - JavaScript bindings
  - [`enochian_cyphers_bg.wasm`](https://github.com/BTCEnoch/gov/blob/main/pkg/enochian_cyphers_bg.wasm) - WASM binary

### 🎮 Prototypes
- [`/prototypes/`](https://github.com/BTCEnoch/gov/tree/main/prototypes)
  - [`index.html`](https://github.com/BTCEnoch/gov/blob/main/prototypes/index.html) - HTML prototype
  - [`sketch.js`](https://github.com/BTCEnoch/gov/blob/main/prototypes/sketch.js) - JavaScript prototype
  - [`server.js`](https://github.com/BTCEnoch/gov/blob/main/prototypes/server.js) - Node.js server
  - [`package.json`](https://github.com/BTCEnoch/gov/blob/main/prototypes/package.json) - Prototype dependencies

### 🔧 Development Tools
- [`grok_custom_instructions.md`](https://github.com/BTCEnoch/gov/blob/main/grok_custom_instructions.md) - Grok AI custom instructions
- [`/engines/`](https://github.com/BTCEnoch/gov/tree/main/engines) - Procedural generation engines
- [`/onchain/`](https://github.com/BTCEnoch/gov/tree/main/onchain) - Bitcoin L1 integration

## Technical Specifications

- **Zero web dependencies** - Pure Bitcoin L1 implementation
- **Bitcoin-native randomness** - Cryptographically secure generation
- **Ordinals-compatible** - 400kb size limit compliance
- **WASM-compiled core** - High-performance execution
- **Deterministic generation** - Reproducible results
- **O(1) verification complexity** - Efficient validation
- **TAP Protocol integration** - Advanced programmable tokens
- **Trac Systems compatibility** - Decentralized state management

## Setup & Development

### Prerequisites
1. Install Rust and wasm-pack
2. Install Python 3.8+
3. Install Node.js (for prototypes)

### Build Instructions
```bash
# Build WASM package
wasm-pack build

# Run Python tests
python -m pytest tests/

# Run Rust tests
cargo test

# Start prototype server
cd prototypes && node server.js
```

### Key Features
- **91 Unique Governor Angels** - Each with distinct personalities and specializations
- **18 Mystical Traditions** - Comprehensive sacred wisdom integration
- **Bitcoin L1 Native** - Full on-chain functionality
- **Decentralized Architecture** - Zero infrastructure dependencies
- **Authentic Knowledge Base** - Historically accurate mystical content
- **Dynamic Content Generation** - AI-powered storylines and quests
- **Progressive Web App** - Cross-platform compatibility
- **Autonomous Economics** - Self-regulating tokenomics

## Contributing

See individual module READMEs for specific contribution guidelines. All contributions must maintain historical accuracy for mystical content and Bitcoin L1 compatibility.

## License

MIT License - See [`LICENSE`](https://github.com/BTCEnoch/gov/blob/main/LICENSE) for details.

---

**Repository Stats:**
- **Total Files:** 500+ files across all modules
- **Lines of Code:** 50,000+ lines (Python, Rust, JavaScript)
- **Test Coverage:** 200+ test files
- **Documentation:** 50+ documentation files
- **Knowledge Entries:** 1,000+ mystical knowledge entries
- **Governor Profiles:** 91 unique AI entities 