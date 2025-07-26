# Enochian Cyphers Scripts Directory

This directory contains all executable scripts organized by functionality and purpose. Each script is categorized into logical subdirectories for easy navigation and maintenance.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This comprehensive index
├── build/                       # Build and compilation scripts
├── deployment/                  # Deployment and production scripts
├── divination/                  # Divination system engines
├── governors/                   # Governor Angel system scripts
├── interviews/                  # Interview system scripts
├── lighthouse/                  # Lighthouse knowledge base scripts
├── onchain/                     # Bitcoin L1 and blockchain integration
├── setup/                       # System setup and initialization scripts
├── utilities/                   # Utility and support scripts
└── validation/                  # Testing and validation scripts
```

## 🏗️ Build Scripts (`build/`)

### `build-wasm.sh`
**Purpose**: Compiles Rust code to WebAssembly for browser integration
**Usage**: `./scripts/build/build-wasm.sh`
**Dependencies**: Rust toolchain, wasm-pack
**Output**: WASM binaries in `pkg/` directory
**Description**: Essential for creating browser-compatible WebAssembly modules from the Rust codebase, enabling client-side execution of core Enochian Cyphers logic.

## 🚀 Deployment Scripts (`deployment/`)

### `sacred_deployment_orchestrator.py`
**Purpose**: Orchestrates complete system deployment across all layers
**Usage**: `python scripts/deployment/sacred_deployment_orchestrator.py`
**Dependencies**: Python 3.8+, all system components
**Output**: Deployed system with verification reports
**Description**: Comprehensive deployment system that coordinates Bitcoin L1 integration, lighthouse deployment, and UI layer activation.

### `optimized_quest_engine.py`
**Purpose**: Production-optimized quest generation engine
**Usage**: `python scripts/deployment/optimized_quest_engine.py`
**Dependencies**: Python 3.8+, lighthouse knowledge base
**Output**: Optimized quest generation system
**Description**: High-performance quest engine designed for production deployment with enhanced efficiency and scalability.

## 🔮 Divination Scripts (`divination/`)

### `divination_master.py`
**Purpose**: Unified interface for all divination systems
**Usage**: `python scripts/divination/divination_master.py`
**Dependencies**: Python 3.8+, lighthouse knowledge base
**Output**: Integrated divination readings
**Description**: Master controller that coordinates Tarot, I Ching, and Astrology systems for comprehensive mystical guidance.

### `tarot_engine.py`
**Purpose**: Complete 78-card Tarot divination system
**Usage**: `python scripts/divination/tarot_engine.py`
**Dependencies**: Python 3.8+, tarot tradition data
**Output**: Tarot readings with interpretations
**Description**: Authentic Tarot system with full card meanings, spreads, and mystical interpretations.

### `i_ching_engine.py`
**Purpose**: 64 hexagram I Ching oracle system
**Usage**: `python scripts/divination/i_ching_engine.py`
**Dependencies**: Python 3.8+, I Ching tradition data
**Output**: Hexagram readings with changing lines
**Description**: Traditional I Ching system with complete hexagram interpretations and wisdom guidance.

### `astrology_engine.py`
**Purpose**: Comprehensive astrological chart generation
**Usage**: `python scripts/divination/astrology_engine.py`
**Dependencies**: Python 3.8+, astrology tradition data
**Output**: Astrological charts and interpretations
**Description**: Full astrological system with planetary aspects, houses, and natal chart generation.

## 👑 Governor Scripts (`governors/`)

### `batch_governor_quest_generator.py`
**Purpose**: Generates quest content for all 91 Governor Angels in batch  
**Usage**: `python scripts/governors/batch_governor_quest_generator.py`  
**Dependencies**: Python 3.8+, lighthouse knowledge base  
**Output**: Quest JSON files in `generated_questlines/`  
**Description**: Creates comprehensive quest narratives for each Governor Angel, integrating with the 26 sacred traditions and ensuring mystical authenticity.

### `governor_agent_prompt_generator.py`
**Purpose**: Generates AI prompts for Governor Angel embodiment  
**Usage**: `python scripts/governors/governor_agent_prompt_generator.py`  
**Dependencies**: Python 3.8+, governor profiles  
**Output**: `governor_agent_prompts.json`  
**Description**: Creates structured prompts for AI systems to embody individual Governor Angels with authentic personalities and knowledge.

### `governor_ai_embodiment.py`
**Purpose**: AI embodiment system for Governor Angels  
**Usage**: `python scripts/governors/governor_ai_embodiment.py`  
**Dependencies**: Python 3.8+, AI API access  
**Output**: `governor_ai_embodiments.json`  
**Description**: Implements AI-driven Governor Angel personalities using the lighthouse knowledge base and individual governor profiles.

### `governor_interview_engine.py`
**Purpose**: Conducts structured interviews with Governor Angels  
**Usage**: `python scripts/governors/governor_interview_engine.py`  
**Dependencies**: Python 3.8+, interview questions framework  
**Output**: Individual governor interview JSON files  
**Description**: Systematic interview process for each Governor Angel to extract personality traits, knowledge, and quest generation capabilities.

### `governor_interview_integration.py`
**Purpose**: Integrates interview results into the governor system
**Usage**: `python scripts/governors/governor_interview_integration.py`
**Dependencies**: Python 3.8+, completed interviews
**Output**: `governor_interview_integration.json`
**Description**: Processes and integrates interview data into the broader Governor Angel framework for enhanced AI embodiment.

### `enhanced_ai_persona_loader.py` ✨ NEW
**Purpose**: Simulates consciousness boot-up for 91 Governor Angels
**Usage**: `python scripts/governors/enhanced_ai_persona_loader.py`
**Dependencies**: Python 3.8+, governor profiles, lighthouse knowledge base
**Output**: `governor_ai_personas.json`
**Description**: 6-phase consciousness simulation that creates unique AI personas embodying individual Governor Angels with their traits, knowledge, and creative synthesis capabilities.

### `enhanced_batch_content_generator.py` ✨ NEW
**Purpose**: Orchestrates 91 simultaneous AI agents for unique content creation
**Usage**: `python scripts/governors/enhanced_batch_content_generator.py`
**Dependencies**: Python 3.8+, AI API access, booted personas
**Output**: Organized content directories with dialogues, challenges, quests, rewards, teachings
**Description**: Batch processing system where each AI agent creates content as their specific persona, generating unique inventories of interactions, challenges, and wisdom teachings.

### `master_ai_orchestrator.py` ✨ NEW
**Purpose**: Complete orchestration of persona booting and content generation
**Usage**: `python scripts/governors/master_ai_orchestrator.py`
**Dependencies**: Python 3.8+, AI API access, all system components
**Output**: Complete content generation system with statistics and integration guides
**Description**: Master coordination system that boots all 91 personas and orchestrates simultaneous content generation, creating thousands of unique content pieces ready for game integration.

## 🎤 Interview Scripts (`interviews/`)

### `interview_extractor.py`
**Purpose**: Extracts and processes governor interview data
**Usage**: `python scripts/interviews/interview_extractor.py`
**Dependencies**: Python 3.8+, governor profiles
**Output**: Extracted interview data files
**Description**: Systematic extraction of interview responses from Governor Angel profiles for analysis and integration.

### `interview_loader.py`
**Purpose**: Loads and manages interview data for processing
**Usage**: `python scripts/interviews/interview_loader.py`
**Dependencies**: Python 3.8+, interview data files
**Output**: Structured interview data objects
**Description**: Efficient loading and management system for governor interview data with indexing and search capabilities.

## 🏮 Lighthouse Scripts (`lighthouse/`)

### `tradition_deduplication_script.py`
**Purpose**: Merges overlapping tradition files to prevent AI confusion  
**Usage**: `python scripts/lighthouse/tradition_deduplication_script.py`  
**Dependencies**: Python 3.8+, lighthouse traditions directory  
**Output**: Merged tradition files, backup directory  
**Description**: ✅ **COMPLETED** - Successfully merged 4 pairs of overlapping traditions (astrology/natal_astrology, hermetic_qabalah/traditional_kabbalah, quantum_physics/digital_physics, taoism/i_ching) while preserving all 2,565+ entries.

### `cleanup_redundant_files.py`
**Purpose**: Removes redundant directories and files from lighthouse  
**Usage**: `python scripts/lighthouse/cleanup_redundant_files.py`  
**Dependencies**: Python 3.8+, lighthouse directory structure  
**Output**: Cleaned directory structure, cleanup report  
**Description**: ✅ **COMPLETED** - Removed redundant directories (complete_lighthouse, migrate_lighthouse, __pycache__) and temporary files while preserving essential data.

### `cleanup_verification.py`
**Purpose**: Verifies successful completion of lighthouse cleanup operations
**Usage**: `python scripts/lighthouse/cleanup_verification.py`
**Dependencies**: Python 3.8+, cleaned lighthouse structure
**Output**: Verification report with pass/fail status
**Description**: ✅ **COMPLETED** - Comprehensive verification system that confirmed all cleanup operations succeeded with 6/6 checks passed.

### `authentic_content_populator.py`
**Purpose**: Populates lighthouse with authentic mystical content
**Usage**: `python scripts/lighthouse/authentic_content_populator.py`
**Dependencies**: Python 3.8+, source materials
**Output**: Populated tradition files with authentic content
**Description**: Comprehensive content population system that ensures mystical authenticity and historical accuracy.

### `comprehensive_knowledge_generator.py`
**Purpose**: Generates comprehensive knowledge base entries
**Usage**: `python scripts/lighthouse/comprehensive_knowledge_generator.py`
**Dependencies**: Python 3.8+, tradition templates
**Output**: Complete knowledge base with cross-references
**Description**: Advanced knowledge generation system that creates rich, interconnected mystical content.

### `lighthouse_builder.py`
**Purpose**: Core lighthouse construction and management system
**Usage**: `python scripts/lighthouse/lighthouse_builder.py`
**Dependencies**: Python 3.8+, tradition data
**Output**: Complete lighthouse knowledge base structure
**Description**: Primary lighthouse construction system that builds and maintains the sacred knowledge repository.

### `resilient_quest_generator.py`
**Purpose**: Production-ready quest generation with error handling
**Usage**: `python scripts/lighthouse/resilient_quest_generator.py`
**Dependencies**: Python 3.8+, lighthouse knowledge base
**Output**: Generated quest files with resilient error handling
**Description**: Robust quest generation system designed for production use with comprehensive error handling and recovery.

## ⚡ OnChain Scripts (`onchain/`)

### `tap_inscriber.py`
**Purpose**: TAP Protocol inscription and compression system
**Usage**: `python scripts/onchain/tap_inscriber.py`
**Dependencies**: Python 3.8+, TAP Protocol access
**Output**: Compressed inscriptions for Bitcoin L1
**Description**: Advanced inscription system that compresses lighthouse content for Bitcoin L1 deployment via TAP Protocol.

### `tap_protocol_integration.py`
**Purpose**: Complete TAP Protocol integration for hypertokens
**Usage**: `python scripts/onchain/tap_protocol_integration.py`
**Dependencies**: Python 3.8+, Bitcoin L1 access
**Output**: Hypertoken evolution mechanics
**Description**: Comprehensive TAP Protocol integration enabling quest hypertokens with evolutionary traits and cross-token interactions.

### `autonomous_tokenomics.py`
**Purpose**: Self-regulating economic mechanisms
**Usage**: `python scripts/onchain/autonomous_tokenomics.py`
**Dependencies**: Python 3.8+, market data access
**Output**: Dynamic pricing and economic balance
**Description**: Advanced tokenomics system with dynamic pricing, automatic burns, and market balancing for sustainable economics.

### `comprehensive_integration.py`
**Purpose**: Unified on-chain integration system
**Usage**: `python scripts/onchain/comprehensive_integration.py`
**Dependencies**: Python 3.8+, all on-chain components
**Output**: Complete Bitcoin L1 integration
**Description**: Master integration system that coordinates all on-chain components for seamless Bitcoin L1 operation.

## ⚙️ Setup Scripts (`setup/`)

### `setup_batch_ai_system.py`
**Purpose**: Initializes the batch AI processing system
**Usage**: `python scripts/setup/setup_batch_ai_system.py`
**Dependencies**: Python 3.8+, AI API credentials
**Output**: Configured AI batch processing system
**Description**: Sets up the infrastructure for batch processing of Governor Angel AI embodiment, including API connections and processing queues.

## 🔧 Utility Scripts (`utilities/`)

### `content_indexer.py`
**Purpose**: Indexes and organizes content for efficient retrieval
**Usage**: `python scripts/utilities/content_indexer.py`
**Dependencies**: Python 3.8+, content files
**Output**: Indexed content database
**Description**: Advanced indexing system that creates searchable indexes of all mystical content for rapid retrieval and cross-referencing.

### `beta_feedback_collector.py`
**Purpose**: Collects and processes beta user feedback
**Usage**: `python scripts/utilities/beta_feedback_collector.py`
**Dependencies**: Python 3.8+, feedback data sources
**Output**: Processed feedback reports
**Description**: Comprehensive feedback collection system for beta testing phases with analysis and reporting capabilities.

### `market_validator.py`
**Purpose**: Validates market mechanisms and economic balance
**Usage**: `python scripts/utilities/market_validator.py`
**Dependencies**: Python 3.8+, economic data
**Output**: Market validation reports
**Description**: Economic validation system that ensures market mechanisms are balanced and sustainable for long-term operation.

### `json_linebreak_cleaner.py` ✨ NEW
**Purpose**: Fixes \n\n linebreak issues in JSON files across the project
**Usage**: `python scripts/utilities/json_linebreak_cleaner.py`
**Dependencies**: Python 3.8+, JSON files
**Output**: Cleaned JSON files with proper linebreaks, backup files, cleanup report
**Description**: Scans all JSON files in the project and converts literal \n\n strings to actual linebreaks for proper formatting while preserving JSON structure.

## 🧪 Validation Scripts (`validation/`)

### `content_metrics_validator.py`
**Purpose**: Validates content authenticity and mystical accuracy
**Usage**: `python scripts/validation/content_metrics_validator.py`
**Dependencies**: Python 3.8+, reference sources
**Output**: Content validation reports
**Description**: Comprehensive validation system that ensures all mystical content maintains authenticity and historical accuracy.

### `test_comprehensive_validation.py`
**Purpose**: Comprehensive system testing and validation
**Usage**: `python scripts/validation/test_comprehensive_validation.py`
**Dependencies**: Python 3.8+, all system components
**Output**: Complete system validation report
**Description**: Master testing system with 15+ test cases covering all aspects of the Enochian Cyphers system including P2P consensus.

### `setup_lighthouse.py`
**Purpose**: Initializes the Lighthouse knowledge base system  
**Usage**: `python scripts/setup/setup_lighthouse.py`  
**Dependencies**: Python 3.8+, tradition source files  
**Output**: Fully configured lighthouse directory structure  
**Description**: Comprehensive setup script that initializes the 26 sacred traditions, creates the master index, and prepares the knowledge base for production use.

## 🔧 Usage Guidelines

### Prerequisites
- **Python 3.8+** for all Python scripts
- **Rust toolchain** for WASM compilation
- **API Keys** for AI-dependent scripts (Anthropic Claude)
- **Lighthouse Knowledge Base** must be initialized before running dependent scripts

### Execution Order for New Installations
1. **Setup Phase**: Initialize core systems
   ```bash
   python scripts/setup/setup_lighthouse.py
   python scripts/setup/setup_batch_ai_system.py
   ```

2. **Build Phase**: Compile WASM modules
   ```bash
   ./scripts/build/build-wasm.sh
   ```

3. **Content Phase**: Generate lighthouse content
   ```bash
   python scripts/lighthouse/lighthouse_builder.py
   python scripts/lighthouse/comprehensive_knowledge_generator.py
   ```

4. **Governor Phase**: Generate governor content
   ```bash
   python scripts/governors/governor_agent_prompt_generator.py
   python scripts/governors/batch_governor_quest_generator.py
   python scripts/interviews/interview_extractor.py
   ```

5. **AI Persona Phase**: Boot AI personas and generate unique content ✨ NEW
   ```bash
   # Complete orchestration (recommended)
   python scripts/governors/master_ai_orchestrator.py

   # Or step-by-step:
   python scripts/governors/enhanced_ai_persona_loader.py
   python scripts/governors/enhanced_batch_content_generator.py
   ```

6. **Integration Phase**: Integrate all systems
   ```bash
   python scripts/divination/divination_master.py
   python scripts/onchain/comprehensive_integration.py
   ```

7. **Validation Phase**: Test and validate
   ```bash
   python scripts/validation/content_metrics_validator.py
   python scripts/validation/test_comprehensive_validation.py
   ```

8. **Deployment Phase**: Deploy to production
   ```bash
   python scripts/deployment/sacred_deployment_orchestrator.py
   ```

### Script Dependencies
- **Setup Scripts**: Can run independently, should run first
- **Build Scripts**: Require Rust toolchain and source code
- **Lighthouse Scripts**: Require initialized lighthouse knowledge base
- **Governor Scripts**: Require lighthouse + governor profiles
- **Interview Scripts**: Require governor profiles and interview data
- **Divination Scripts**: Require lighthouse knowledge base and tradition data
- **OnChain Scripts**: Require Bitcoin L1 access and TAP Protocol integration
- **Validation Scripts**: Require all system components for comprehensive testing
- **Utility Scripts**: Support other scripts, minimal dependencies
- **Deployment Scripts**: Require all components for production deployment

## 🚨 Important Notes

### Completed Operations
The following scripts have been successfully executed and their operations are complete:
- ✅ `tradition_deduplication_script.py` - Lighthouse optimization completed
- ✅ `cleanup_redundant_files.py` - Directory cleanup completed  
- ✅ `cleanup_verification.py` - Verification passed (6/6 checks)

### Production Readiness
- **Lighthouse Knowledge Base**: Optimized and ready for Herald prototype development
- **Governor System**: Complete with 91 Governor Angels and AI embodiment
- **Build System**: WASM compilation ready for browser deployment
- **Setup Scripts**: Tested and validated for new installations

### Backup and Safety
- All cleanup operations create backups before making changes
- Verification scripts confirm successful operations
- Rollback procedures documented in individual script headers

---

**For Technical Support**: Refer to individual script documentation or the comprehensive project documentation in `docs/summary_documents/`
