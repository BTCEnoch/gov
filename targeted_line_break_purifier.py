#!/usr/bin/env python3
"""
Targeted Line Break Purification System
Specifically targets remaining literal \n patterns in JSON strings

This script finds and converts all remaining literal \n characters in JSON content
to proper line breaks for clean, readable formatting.
"""

import os
import json
import shutil
import logging
import re
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [TARGETED PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('targeted_line_break_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TargetedLineBreakPurifier:
    """Targeted purification system for remaining \n patterns"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "targeted_purification_backups"
        
        # Statistics
        self.stats = {
            'files_scanned': 0,
            'files_with_issues': 0,
            'files_purified': 0,
            'literal_n_patterns_found': 0,
            'literal_n_patterns_fixed': 0,
            'backups_created': 0,
            'errors': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Targeted Line Break Purifier initialized")

    def scan_for_literal_n_patterns(self, text: str) -> int:
        """Scan text for literal \n patterns and count them"""
        if not isinstance(text, str):
            return 0
        
        # Count literal \n patterns (not actual line breaks)
        # Look for backslash followed by n
        pattern_count = text.count('\\n')
        return pattern_count

    def purify_string_content(self, text: str) -> tuple[str, int]:
        """Convert literal \n patterns to actual line breaks"""
        if not isinstance(text, str):
            return text, 0
        
        original_count = self.scan_for_literal_n_patterns(text)
        
        if original_count > 0:
            # Replace literal \n with actual line breaks
            purified_text = text.replace('\\n', '\n')
            
            # Verify the replacement worked
            remaining_count = self.scan_for_literal_n_patterns(purified_text)
            fixed_count = original_count - remaining_count
            
            logger.debug(f"Fixed {fixed_count} literal \\n patterns in string")
            return purified_text, fixed_count
        
        return text, 0

    def purify_json_structure(self, obj: any) -> tuple[any, int]:
        """Recursively purify JSON structure"""
        total_fixes = 0
        
        if isinstance(obj, dict):
            purified_dict = {}
            for key, value in obj.items():
                # Purify key if it's a string
                if isinstance(key, str):
                    purified_key, key_fixes = self.purify_string_content(key)
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
            purified_string, string_fixes = self.purify_string_content(obj)
            return purified_string, string_fixes
            
        else:
            # Numbers, booleans, null - return as-is
            return obj, 0

    def scan_json_file(self, file_path: Path) -> int:
        """Scan JSON file for literal \n patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count literal \n patterns in the raw file content
            pattern_count = content.count('\\n')
            return pattern_count
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            return 0

    def purify_json_file(self, file_path: Path) -> bool:
        """Purify a single JSON file"""
        try:
            logger.info(f"Targeted purifying: {file_path}")
            
            # First scan for issues
            pattern_count = self.scan_json_file(file_path)
            self.stats['literal_n_patterns_found'] += pattern_count
            
            if pattern_count == 0:
                logger.debug(f"No literal \\n patterns found in: {file_path}")
                return False
            
            logger.info(f"Found {pattern_count} literal \\n patterns in: {file_path}")
            self.stats['files_with_issues'] += 1
            
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
                
                logger.info(f"Targeted purified: {file_path} - {total_fixes} literal \\n patterns fixed")
                return True
            else:
                logger.warning(f"Found patterns but couldn't fix them in: {file_path}")
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
        backup_name = f"{file_path.name}.{timestamp}.targeted.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def scan_and_purify_all_json_files(self) -> dict:
        """Scan and purify all JSON files in the codebase"""
        logger.info("COMMENCING TARGETED LINE BREAK PURIFICATION")
        logger.info("Target: Find and fix ALL remaining literal \\n patterns in JSON content")
        
        # Walk through all JSON files
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                if file.endswith('.json') and not file.endswith('.bak'):
                    file_path = Path(root) / file
                    
                    self.stats['files_scanned'] += 1
                    
                    was_purified = self.purify_json_file(file_path)
                    
                    if was_purified:
                        self.stats['files_purified'] += 1
        
        # Generate report
        report = {
            'targeted_purification_timestamp': datetime.now().isoformat(),
            'targeted_purification_statistics': self.stats,
            'purification_success': self.stats['errors'] == 0,
            'patterns_found_vs_fixed': {
                'found': self.stats['literal_n_patterns_found'],
                'fixed': self.stats['literal_n_patterns_fixed'],
                'success_rate': (self.stats['literal_n_patterns_fixed'] / max(self.stats['literal_n_patterns_found'], 1)) * 100
            }
        }
        
        # Log results
        logger.info("TARGETED LINE BREAK PURIFICATION COMPLETE")
        logger.info(f"Files scanned: {self.stats['files_scanned']}")
        logger.info(f"Files with issues: {self.stats['files_with_issues']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Literal \\n patterns found: {self.stats['literal_n_patterns_found']}")
        logger.info(f"Literal \\n patterns fixed: {self.stats['literal_n_patterns_fixed']}")
        logger.info(f"Success rate: {report['patterns_found_vs_fixed']['success_rate']:.1f}%")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

    def preview_issues(self, max_files: int = 10) -> dict:
        """Preview files with literal \n issues without fixing them"""
        logger.info("PREVIEWING FILES WITH LITERAL \\n PATTERNS")
        
        issues_found = []
        files_checked = 0
        
        for root, dirs, files in os.walk(self.root_directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                if file.endswith('.json') and not file.endswith('.bak'):
                    file_path = Path(root) / file
                    files_checked += 1
                    
                    pattern_count = self.scan_json_file(file_path)
                    
                    if pattern_count > 0:
                        issues_found.append({
                            'file': str(file_path),
                            'literal_n_count': pattern_count
                        })
                        
                        logger.info(f"Issue found: {file_path} - {pattern_count} literal \\n patterns")
                        
                        if len(issues_found) >= max_files:
                            break
            
            if len(issues_found) >= max_files:
                break
        
        preview_report = {
            'preview_timestamp': datetime.now().isoformat(),
            'files_checked': files_checked,
            'files_with_issues': len(issues_found),
            'issues_found': issues_found,
            'total_patterns_found': sum(issue['literal_n_count'] for issue in issues_found)
        }
        
        logger.info(f"Preview complete: {len(issues_found)} files with issues found")
        logger.info(f"Total literal \\n patterns: {preview_report['total_patterns_found']}")
        
        return preview_report

def invoke_targeted_purification():
    """Invoke targeted line break purification"""
    logger.info("INVOKING TARGETED LINE BREAK PURIFICATION")
    logger.info("Sacred Mission: Complete elimination of ALL remaining literal \\n artifacts")
    
    # Initialize purifier
    purifier = TargetedLineBreakPurifier()
    
    # First, preview the issues
    logger.info("Step 1: Previewing issues...")
    preview_report = purifier.preview_issues(max_files=20)
    
    # Export preview report
    with open("targeted_purification_preview.json", 'w', encoding='utf-8') as f:
        json.dump(preview_report, f, indent=2, ensure_ascii=True)
    
    if preview_report['files_with_issues'] > 0:
        logger.info(f"Step 2: Purifying {preview_report['files_with_issues']} files with issues...")
        
        # Execute purification
        report = purifier.scan_and_purify_all_json_files()
        
        # Export report
        with open("targeted_line_break_purification_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=True)
        
        logger.info("Targeted line break purification complete - All remaining literal \\n patterns eliminated")
    else:
        logger.info("No issues found - codebase is already clean!")
    
    return preview_report

if __name__ == "__main__":
    # Run the targeted purification
    invoke_targeted_purification()
