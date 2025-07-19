#!/usr/bin/env python3
"""
Simple Backslash Fixer
Direct fix for double backslashes in file paths within JSON files

This script specifically targets and fixes double backslashes in file_path values
while preserving all other JSON structure and escape sequences.
"""

import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SIMPLE FIXER] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_backslash_fix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleBackslashFixer:
    """Simple fixer for double backslashes in file paths"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "simple_fix_backups"
        
        # Statistics
        self.stats = {
            'files_processed': 0,
            'files_fixed': 0,
            'double_backslashes_fixed': 0,
            'backups_created': 0,
            'errors': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Simple Backslash Fixer initialized")

    def fix_file_paths_in_json(self, data):
        """Recursively fix double backslashes in file_path values"""
        fixes_made = 0
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "file_path" and isinstance(value, str) and "\\\\" in value:
                    # Fix double backslashes in file paths
                    original_value = value
                    fixed_value = value.replace("\\\\", "\\")
                    data[key] = fixed_value
                    fixes_made += original_value.count("\\\\")
                    logger.debug(f"Fixed file_path: {original_value} -> {fixed_value}")
                elif isinstance(value, (dict, list)):
                    # Recursively process nested structures
                    fixes_made += self.fix_file_paths_in_json(value)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    fixes_made += self.fix_file_paths_in_json(item)
        
        return fixes_made

    def fix_json_file(self, file_path: Path) -> bool:
        """Fix a single JSON file"""
        try:
            logger.info(f"Processing: {file_path}")
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Fix file paths
            fixes_made = self.fix_file_paths_in_json(data)
            
            if fixes_made > 0:
                # Create backup
                self._create_backup(file_path)
                
                # Write fixed JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=True, sort_keys=False)
                
                # Update statistics
                self.stats['double_backslashes_fixed'] += fixes_made
                
                logger.info(f"Fixed: {file_path} - {fixes_made} double backslashes corrected")
                return True
            else:
                logger.debug(f"No fixes needed: {file_path}")
                return False
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            self.stats['errors'] += 1
            return False
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.simple.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def fix_specific_files(self, file_list: list) -> dict:
        """Fix specific files with known double backslash issues"""
        logger.info("COMMENCING SIMPLE BACKSLASH FIXING")
        logger.info(f"Target: {len(file_list)} specific files with double backslash issues")
        
        for file_path_str in file_list:
            file_path = Path(file_path_str)
            
            if file_path.exists():
                self.stats['files_processed'] += 1
                
                was_fixed = self.fix_json_file(file_path)
                
                if was_fixed:
                    self.stats['files_fixed'] += 1
            else:
                logger.warning(f"File not found: {file_path}")
        
        # Generate report
        report = {
            'simple_fix_timestamp': datetime.now().isoformat(),
            'simple_fix_statistics': self.stats,
            'fix_success': self.stats['errors'] == 0,
            'files_targeted': file_list
        }
        
        # Log results
        logger.info("SIMPLE BACKSLASH FIXING COMPLETE")
        logger.info(f"Files processed: {self.stats['files_processed']}")
        logger.info(f"Files fixed: {self.stats['files_fixed']}")
        logger.info(f"Double backslashes fixed: {self.stats['double_backslashes_fixed']}")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

def invoke_simple_fix():
    """Invoke simple backslash fixing for specific problematic files"""
    logger.info("INVOKING SIMPLE BACKSLASH FIXING")
    logger.info("Sacred Mission: Fix double backslashes in file_path values")
    
    # Initialize fixer
    fixer = SimpleBackslashFixer()
    
    # Target specific files that we know have double backslash issues
    target_files = [
        "lighthouse/traditions/lighthouse_master_index.json",
        "lighthouse/archived_schemas/cross_reference_schema.json",
        "lighthouse/archived_schemas/governor_angel_schema.json",
        "lighthouse/archived_schemas/mystical_entry_schema.json"
    ]
    
    # Execute fixing
    report = fixer.fix_specific_files(target_files)
    
    # Export report
    with open("simple_backslash_fix_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Simple backslash fixing complete")
    return report

if __name__ == "__main__":
    # Run the simple fix
    invoke_simple_fix()
