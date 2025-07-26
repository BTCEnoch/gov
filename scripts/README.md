# Enochian Cyphers Scripts Directory

This directory contains all executable scripts organized by functionality and purpose. Each script is categorized into logical subdirectories for easy navigation and maintenance.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This comprehensive index
├── build/                       # Build and compilation scripts
├── governors/                   # Governor Angel system scripts
├── lighthouse/                  # Lighthouse knowledge base scripts
└── setup/                       # System setup and initialization scripts
```

## 🏗️ Build Scripts (`build/`)

### `build-wasm.sh`
**Purpose**: Compiles Rust code to WebAssembly for browser integration  
**Usage**: `./scripts/build/build-wasm.sh`  
**Dependencies**: Rust toolchain, wasm-pack  
**Output**: WASM binaries in `pkg/` directory  
**Description**: Essential for creating browser-compatible WebAssembly modules from the Rust codebase, enabling client-side execution of core Enochian Cyphers logic.

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

## ⚙️ Setup Scripts (`setup/`)

### `setup_batch_ai_system.py`
**Purpose**: Initializes the batch AI processing system  
**Usage**: `python scripts/setup/setup_batch_ai_system.py`  
**Dependencies**: Python 3.8+, AI API credentials  
**Output**: Configured AI batch processing system  
**Description**: Sets up the infrastructure for batch processing of Governor Angel AI embodiment, including API connections and processing queues.

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
1. **Setup Phase**: Run setup scripts first
   ```bash
   python scripts/setup/setup_lighthouse.py
   python scripts/setup/setup_batch_ai_system.py
   ```

2. **Build Phase**: Compile WASM modules
   ```bash
   ./scripts/build/build-wasm.sh
   ```

3. **Governor Phase**: Generate governor content
   ```bash
   python scripts/governors/governor_agent_prompt_generator.py
   python scripts/governors/batch_governor_quest_generator.py
   ```

4. **Optimization Phase**: Clean and optimize (if needed)
   ```bash
   python scripts/lighthouse/tradition_deduplication_script.py
   python scripts/lighthouse/cleanup_redundant_files.py
   python scripts/lighthouse/cleanup_verification.py
   ```

### Script Dependencies
- **Lighthouse Scripts**: Require initialized lighthouse knowledge base
- **Governor Scripts**: Require lighthouse + governor profiles
- **Setup Scripts**: Can run independently but should run first
- **Build Scripts**: Require Rust toolchain and source code

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
