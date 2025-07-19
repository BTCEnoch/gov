#!/usr/bin/env python3
"""
Enochian Cyphers Codebase Inventory & Classification System
Complete analysis and categorization of all files according to sacred architecture

This script performs comprehensive inventory and classification of the entire codebase
according to the 6-layer sacred architecture and core mission requirements.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [INVENTORY] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('codebase_inventory_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CodebaseInventoryAnalyzer:
    """Comprehensive codebase inventory and classification system"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        
        # Sacred 6-Layer Architecture Classification
        self.layer_classifications = {
            'layer_1_bitcoin_l1': [],      # Bitcoin L1 integration
            'layer_2_lighthouse': [],      # Lighthouse knowledge base
            'layer_3_governors': [],       # 91 Governor Angels
            'layer_4_story_engine': [],    # Story/Quest generation
            'layer_5_game_mechanics': [],  # Game mechanics & divination
            'layer_6_ui': []               # User interface
        }
        
        # File importance classifications
        self.importance_classifications = {
            'crucial': [],          # Essential for core functionality
            'non_crucial': [],      # Useful but not essential
            'non_useful': []        # Redundant, outdated, or unnecessary
        }
        
        # File type statistics
        self.file_stats = {
            'total_files': 0,
            'total_size_bytes': 0,
            'file_types': {},
            'directory_counts': {},
            'largest_files': [],
            'backup_files': 0,
            'log_files': 0,
            'python_files': 0,
            'json_files': 0,
            'markdown_files': 0
        }
        
        logger.info("Codebase Inventory Analyzer initialized")

    def analyze_file_importance(self, file_path: Path) -> str:
        """Classify file importance based on sacred architecture requirements"""
        file_str = str(file_path).lower()
        file_name = file_path.name.lower()
        
        # CRUCIAL FILES - Essential for core functionality
        crucial_patterns = [
            # Core sacred architecture files
            'lighthouse/traditions/',
            'lighthouse/complete_lighthouse/',
            'lighthouse/bitcoin_inscriptions/',
            'governor_profiles/',
            'interviews/governors/',
            'onchain/',
            
            # Essential Python engines
            'engines/',
            'divination_systems/',
            
            # Core configuration and requirements
            'requirements.txt',
            'readme.md',
            'project_overview.md',
            
            # TAP Protocol and Bitcoin integration
            'tap_',
            'bitcoin_',
            'onchain_',
            
            # Governor AI systems
            'governor_ai_',
            'governor_interview_',
            'governor_agent_',
            
            # Core lighthouse systems
            'lighthouse_builder',
            'quest_engine',
            'knowledge_base',
            
            # Sacred traditions (exactly 26)
            '/traditions/',
            '/complete_lighthouse/',
        ]
        
        # NON-USEFUL FILES - Redundant, outdated, or unnecessary
        non_useful_patterns = [
            # Backup directories and files
            'backup',
            '.bak',
            '_backups/',
            
            # Log files
            '.log',
            
            # Temporary and cache files
            '__pycache__',
            '.pyc',
            
            # Purification scripts (completed their purpose)
            'clean_sacred_codex.py',
            'enhanced_sacred_purifier.py',
            'final_line_break_purifier.py',
            'raw_line_break_purifier.py',
            'targeted_line_break_purifier.py',
            'universal_escape_purifier.py',
            'comprehensive_escape_purifier.py',
            'precise_backslash_purifier.py',
            'simple_backslash_fixer.py',
            
            # Purification reports (historical)
            'purification_report',
            'purification_preview',
            'purification.log',
            
            # Test and validation reports (can be regenerated)
            'test_report',
            'validation_report',
            'content_metrics_report',
            
            # Archived schemas (superseded)
            'archived_schemas/',
            
            # Migration directories (completed)
            'migrate_lighthouse/',
        ]
        
        # Check for non-useful patterns first
        for pattern in non_useful_patterns:
            if pattern in file_str:
                return 'non_useful'
        
        # Check for crucial patterns
        for pattern in crucial_patterns:
            if pattern in file_str:
                return 'crucial'
        
        # Everything else is non-crucial
        return 'non_crucial'

    def classify_by_sacred_layer(self, file_path: Path) -> str:
        """Classify file according to the 6-layer sacred architecture"""
        file_str = str(file_path).lower()
        
        # Layer 1: Bitcoin L1 Integration
        layer_1_patterns = [
            'onchain/',
            'bitcoin_',
            'tap_',
            'trac_',
            'inscription',
            'hypertoken'
        ]
        
        # Layer 2: Lighthouse Knowledge Base
        layer_2_patterns = [
            'lighthouse/',
            'traditions/',
            'complete_lighthouse/',
            'citations/',
            'knowledge_base'
        ]
        
        # Layer 3: Governor Angels (91 total)
        layer_3_patterns = [
            'governor_profiles/',
            'interviews/',
            'governor_ai_',
            'governor_agent_',
            'governor_interview_'
        ]
        
        # Layer 4: Story Engine
        layer_4_patterns = [
            'quest_',
            'story_',
            'questlines_',
            'narrative_',
            'content_generator'
        ]
        
        # Layer 5: Game Mechanics
        layer_5_patterns = [
            'engines/',
            'divination_systems/',
            'game_mechanics',
            'astrology_',
            'tarot_',
            'i_ching_'
        ]
        
        # Layer 6: UI (minimal in current implementation)
        layer_6_patterns = [
            'ui/',
            'interface/',
            'frontend/',
            'web/'
        ]
        
        # Check each layer
        for pattern in layer_1_patterns:
            if pattern in file_str:
                return 'layer_1_bitcoin_l1'
        
        for pattern in layer_2_patterns:
            if pattern in file_str:
                return 'layer_2_lighthouse'
        
        for pattern in layer_3_patterns:
            if pattern in file_str:
                return 'layer_3_governors'
        
        for pattern in layer_4_patterns:
            if pattern in file_str:
                return 'layer_4_story_engine'
        
        for pattern in layer_5_patterns:
            if pattern in file_str:
                return 'layer_5_game_mechanics'
        
        for pattern in layer_6_patterns:
            if pattern in file_str:
                return 'layer_6_ui'
        
        # Default to documentation/infrastructure
        return 'infrastructure'

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze individual file and return classification data"""
        try:
            file_size = file_path.stat().st_size
            file_ext = file_path.suffix.lower()
            
            # Classify importance and layer
            importance = self.analyze_file_importance(file_path)
            layer = self.classify_by_sacred_layer(file_path)
            
            # Update statistics
            self.file_stats['total_files'] += 1
            self.file_stats['total_size_bytes'] += file_size
            
            if file_ext not in self.file_stats['file_types']:
                self.file_stats['file_types'][file_ext] = 0
            self.file_stats['file_types'][file_ext] += 1
            
            # Count specific file types
            if file_ext == '.py':
                self.file_stats['python_files'] += 1
            elif file_ext == '.json':
                self.file_stats['json_files'] += 1
            elif file_ext == '.md':
                self.file_stats['markdown_files'] += 1
            elif file_ext == '.log':
                self.file_stats['log_files'] += 1
            elif '.bak' in str(file_path):
                self.file_stats['backup_files'] += 1
            
            # Track largest files
            file_info = {
                'path': str(file_path),
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2),
                'extension': file_ext,
                'importance': importance,
                'layer': layer
            }
            
            self.file_stats['largest_files'].append(file_info)
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None

    def perform_complete_inventory(self) -> Dict:
        """Perform complete codebase inventory and classification"""
        logger.info("COMMENCING COMPLETE CODEBASE INVENTORY")
        logger.info("Sacred Mission: Comprehensive analysis and classification")
        
        start_time = datetime.now()
        
        # Walk through all files
        for root, dirs, files in os.walk(self.root_directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Track directory counts
            dir_path = Path(root)
            dir_name = dir_path.name
            if dir_name not in self.file_stats['directory_counts']:
                self.file_stats['directory_counts'][dir_name] = 0
            self.file_stats['directory_counts'][dir_name] += len(files)
            
            for file in files:
                if not file.startswith('.'):  # Skip hidden files
                    file_path = Path(root) / file
                    file_info = self.analyze_file(file_path)
                    
                    if file_info:
                        # Classify by importance
                        importance = file_info['importance']
                        self.importance_classifications[importance].append(file_info)
                        
                        # Classify by layer
                        layer = file_info['layer']
                        if layer in self.layer_classifications:
                            self.layer_classifications[layer].append(file_info)
        
        # Sort largest files
        self.file_stats['largest_files'].sort(key=lambda x: x['size_bytes'], reverse=True)
        self.file_stats['largest_files'] = self.file_stats['largest_files'][:20]  # Top 20
        
        # Calculate summary statistics
        processing_time = (datetime.now() - start_time).total_seconds()
        total_size_mb = round(self.file_stats['total_size_bytes'] / (1024 * 1024), 2)
        
        # Generate comprehensive report
        report = {
            'inventory_timestamp': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'codebase_summary': {
                'total_files': self.file_stats['total_files'],
                'total_size_mb': total_size_mb,
                'python_files': self.file_stats['python_files'],
                'json_files': self.file_stats['json_files'],
                'markdown_files': self.file_stats['markdown_files'],
                'backup_files': self.file_stats['backup_files'],
                'log_files': self.file_stats['log_files']
            },
            'sacred_layer_distribution': {
                layer: len(files) for layer, files in self.layer_classifications.items()
            },
            'importance_distribution': {
                importance: len(files) for importance, files in self.importance_classifications.items()
            },
            'file_type_distribution': self.file_stats['file_types'],
            'directory_distribution': self.file_stats['directory_counts'],
            'largest_files': self.file_stats['largest_files'],
            'detailed_classifications': {
                'crucial_files': self.importance_classifications['crucial'],
                'non_crucial_files': self.importance_classifications['non_crucial'],
                'non_useful_files': self.importance_classifications['non_useful'],
                'layer_classifications': self.layer_classifications
            }
        }
        
        # Log summary
        logger.info("COMPLETE CODEBASE INVENTORY FINISHED")
        logger.info(f"Total files analyzed: {self.file_stats['total_files']}")
        logger.info(f"Total codebase size: {total_size_mb} MB")
        logger.info(f"Crucial files: {len(self.importance_classifications['crucial'])}")
        logger.info(f"Non-crucial files: {len(self.importance_classifications['non_crucial'])}")
        logger.info(f"Non-useful files: {len(self.importance_classifications['non_useful'])}")
        logger.info(f"Processing time: {processing_time:.2f} seconds")
        
        return report

def invoke_codebase_inventory():
    """Invoke complete codebase inventory and classification"""
    logger.info("INVOKING COMPLETE CODEBASE INVENTORY")
    logger.info("Sacred Mission: Comprehensive analysis of Enochian Cyphers codebase")
    
    # Initialize analyzer
    analyzer = CodebaseInventoryAnalyzer()
    
    # Execute complete inventory
    report = analyzer.perform_complete_inventory()
    
    # Export comprehensive report
    with open("complete_codebase_inventory_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Complete codebase inventory analysis finished")
    logger.info("Report exported to: complete_codebase_inventory_report.json")
    
    return report

if __name__ == "__main__":
    # Run the complete inventory
    invoke_codebase_inventory()
