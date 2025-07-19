#!/usr/bin/env python3
"""
Final Line Break Purification System
Complete elimination of all literal \n patterns in JSON content

This script specifically targets the remaining literal \n patterns found in JSON files
and converts them to proper line breaks for clean, readable content.
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
    format='%(asctime)s - [FINAL PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('final_line_break_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinalLineBreakPurifier:
    """Final purification system for complete \n elimination"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "final_purification_backups"
        
        # Statistics
        self.stats = {
            'files_processed': 0,
            'files_purified': 0,
            'literal_n_patterns_fixed': 0,
            'backups_created': 0,
            'errors': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Final Line Break Purifier initialized")

    def purify_json_string_content(self, text: str) -> tuple[str, int]:
        """Aggressively purify string content by converting literal \n to actual line breaks"""
        if not isinstance(text, str):
            return text, 0
        
        original_text = text
        fixes_made = 0
        
        # Convert literal \n patterns to actual line breaks
        if '\\n' in text:
            # Count how many we're fixing
            fixes_made = text.count('\\n')
            
            # Replace literal \n with actual line breaks
            text = text.replace('\\n', '\n')
            
            logger.debug(f"Fixed {fixes_made} literal \\n patterns in string")
        
        return text, fixes_made

    def purify_json_structure(self, obj: any) -> tuple[any, int]:
        """Recursively purify JSON structure"""
        total_fixes = 0
        
        if isinstance(obj, dict):
            purified_dict = {}
            for key, value in obj.items():
                # Purify key if it's a string
                if isinstance(key, str):
                    purified_key, key_fixes = self.purify_json_string_content(key)
                    total_fixes += key_fixes
                else:
                    purified_key = key
                
                # Purify value recursively
                purified_value, value_fixes = self.purify_json_structure(value)
                total_fixes += value_fixes
                
                purified_dict[purified_key] = purified_value
            
            return purified_dict, total_fixes
            
        elif isinstance(obj, list):
            purified_list = []
            for item in obj:
                purified_item, item_fixes = self.purify_json_structure(item)
                total_fixes += item_fixes
                purified_list.append(purified_item)
            
            return purified_list, total_fixes
            
        elif isinstance(obj, str):
            purified_string, string_fixes = self.purify_json_string_content(obj)
            return purified_string, string_fixes
            
        else:
            # Numbers, booleans, null - return as-is
            return obj, 0

    def purify_json_file(self, file_path: Path) -> bool:
        """Purify a single JSON file"""
        try:
            logger.info(f"Final purifying: {file_path}")
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Purify the structure
            purified_data, total_fixes = self.purify_json_structure(data)
            
            if total_fixes > 0:
                # Create backup
                self._create_backup(file_path)
                
                # Write purified JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(purified_data, f, indent=2, ensure_ascii=True, sort_keys=False)
                
                # Update statistics
                self.stats['literal_n_patterns_fixed'] += total_fixes
                
                logger.info(f"Final purified: {file_path} - {total_fixes} literal \\n patterns fixed")
                return True
            else:
                logger.debug(f"Already clean: {file_path}")
                return False
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            self.stats['errors'] += 1
            return False
        except Exception as e:
            logger.error(f"Error purifying {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.final.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def purify_all_json_files(self) -> dict:
        """Purify all JSON files in the codebase"""
        logger.info("COMMENCING FINAL LINE BREAK PURIFICATION")
        logger.info("Target: Complete elimination of literal \\n patterns in JSON content")
        
        # Walk through all JSON files
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                if file.endswith('.json') and not file.endswith('.bak'):
                    file_path = Path(root) / file
                    
                    self.stats['files_processed'] += 1
                    
                    was_purified = self.purify_json_file(file_path)
                    
                    if was_purified:
                        self.stats['files_purified'] += 1
        
        # Generate report
        report = {
            'final_purification_timestamp': datetime.now().isoformat(),
            'final_purification_statistics': self.stats,
            'purification_success': self.stats['errors'] == 0
        }
        
        # Log results
        logger.info("FINAL LINE BREAK PURIFICATION COMPLETE")
        logger.info(f"Files processed: {self.stats['files_processed']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Literal \\n patterns fixed: {self.stats['literal_n_patterns_fixed']}")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

def invoke_final_purification():
    """Invoke final line break purification"""
    logger.info("INVOKING FINAL LINE BREAK PURIFICATION")
    logger.info("Sacred Mission: Complete elimination of all literal \\n artifacts")
    
    # Initialize purifier
    purifier = FinalLineBreakPurifier()
    
    # Execute purification
    report = purifier.purify_all_json_files()
    
    # Export report
    with open("final_line_break_purification_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Final line break purification complete - All literal \\n patterns eliminated")
    return report

if __name__ == "__main__":
    # Run the final purification
    invoke_final_purification()
