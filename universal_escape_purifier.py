#!/usr/bin/env python3
"""
Universal Escape Sequence Purification System
Comprehensive purification across ALL JSON files in the entire codebase

This script systematically processes every JSON file to eliminate:
1. Double backslashes (\\) in file paths and regex patterns
2. Literal \n patterns that should be actual line breaks
3. All escape sequence artifacts while preserving JSON validity
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
    format='%(asctime)s - [UNIVERSAL PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('universal_escape_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UniversalEscapePurifier:
    """Universal escape sequence purification system for entire codebase"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "universal_purification_backups"
        
        # Statistics
        self.stats = {
            'files_scanned': 0,
            'files_with_issues': 0,
            'files_purified': 0,
            'double_backslashes_found': 0,
            'double_backslashes_fixed': 0,
            'literal_n_found': 0,
            'literal_n_fixed': 0,
            'backups_created': 0,
            'errors': 0,
            'directories_processed': set(),
            'file_types_processed': {}
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Universal Escape Purifier initialized")
        logger.info(f"Root directory: {self.root_directory}")
        logger.info(f"Backup directory: {self.backup_directory}")

    def scan_file_for_issues(self, file_path: Path) -> dict:
        """Scan file for escape sequence issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = {
                'double_backslashes': content.count('\\\\'),
                'literal_n_patterns': content.count('\\n'),
                'file_size': len(content),
                'has_issues': False
            }
            
            issues['has_issues'] = issues['double_backslashes'] > 0 or issues['literal_n_patterns'] > 0
            
            return issues
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            return {'double_backslashes': 0, 'literal_n_patterns': 0, 'file_size': 0, 'has_issues': False}

    def smart_fix_content(self, content: str, file_path: Path) -> tuple[str, dict]:
        """Apply intelligent fixes based on file content and context"""
        fixes = {
            'double_backslashes_fixed': 0,
            'literal_n_fixed': 0,
            'total_changes': 0
        }
        
        original_content = content
        
        # Fix 1: File paths with double backslashes
        # Pattern: "file_path": "path\\\\with\\\\double\\\\backslashes"
        file_path_pattern = r'"file_path":\s*"([^"]*\\\\[^"]*)"'
        def fix_file_path(match):
            path_value = match.group(1)
            fixed_path = path_value.replace('\\\\', '\\')
            return f'"file_path": "{fixed_path}"'
        
        content, file_path_fixes = re.subn(file_path_pattern, fix_file_path, content)
        fixes['double_backslashes_fixed'] += file_path_fixes
        
        # Fix 2: Regex patterns with double backslashes
        # Pattern: "pattern": "regex\\\\pattern"
        regex_pattern = r'"pattern":\s*"([^"]*\\\\[^"]*)"'
        def fix_regex_pattern(match):
            pattern_value = match.group(1)
            fixed_pattern = pattern_value.replace('\\\\', '\\')
            return f'"pattern": "{fixed_pattern}"'
        
        content, regex_fixes = re.subn(regex_pattern, fix_regex_pattern, content)
        fixes['double_backslashes_fixed'] += regex_fixes
        
        # Fix 3: Literal \n in descriptive text fields
        # Only convert \n to line breaks in fields that should contain formatted text
        text_fields = [
            'description', 'full_description', 'personality_prompt', 'essence', 
            'summary', 'content', 'text', 'details', 'historical_context',
            'practical_applications', 'modern_relevance', 'advanced_considerations'
        ]
        
        for field in text_fields:
            # Pattern: "field_name": "text with \\n patterns"
            field_pattern = rf'"{field}":\s*"([^"]*\\n[^"]*)"'
            def fix_text_field(match):
                text_value = match.group(1)
                # Only fix if it's a substantial text block (>50 chars) with multiple \n
                if len(text_value) > 50 and text_value.count('\\n') >= 2:
                    fixed_text = text_value.replace('\\n', '\n')
                    return f'"{field}": "{fixed_text}"'
                return match.group(0)
            
            content, text_fixes = re.subn(field_pattern, fix_text_field, content, flags=re.DOTALL)
            fixes['literal_n_fixed'] += text_fixes
        
        fixes['total_changes'] = fixes['double_backslashes_fixed'] + fixes['literal_n_fixed']
        
        if fixes['total_changes'] > 0:
            logger.debug(f"Applied {fixes['total_changes']} fixes to {file_path}")
        
        return content, fixes

    def purify_json_file(self, file_path: Path) -> bool:
        """Purify a single JSON file"""
        try:
            # Scan for issues first
            issues = self.scan_file_for_issues(file_path)
            
            if not issues['has_issues']:
                return False
            
            logger.info(f"Processing: {file_path}")
            logger.info(f"  Issues found - Double backslashes: {issues['double_backslashes']}, Literal \\n: {issues['literal_n_patterns']}")
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply fixes
            purified_content, fixes = self.smart_fix_content(original_content, file_path)
            
            if fixes['total_changes'] > 0:
                # Validate JSON integrity
                try:
                    json.loads(purified_content)
                except json.JSONDecodeError as e:
                    logger.error(f"Purification would break JSON in {file_path}: {e}")
                    self.stats['errors'] += 1
                    return False
                
                # Create backup
                self._create_backup(file_path)
                
                # Write purified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(purified_content)
                
                # Update statistics
                self.stats['double_backslashes_fixed'] += fixes['double_backslashes_fixed']
                self.stats['literal_n_fixed'] += fixes['literal_n_fixed']
                
                logger.info(f"  Purified: {fixes['double_backslashes_fixed']} backslashes, {fixes['literal_n_fixed']} literal \\n")
                return True
            else:
                logger.debug(f"  No safe fixes could be applied to {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.universal.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def discover_all_json_files(self) -> list:
        """Discover all JSON files in the entire codebase"""
        json_files = []
        
        logger.info("Discovering all JSON files in codebase...")
        
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            # Track directories processed
            self.stats['directories_processed'].add(root)
            
            for file in files:
                if file.endswith('.json') and not file.endswith('.bak'):
                    file_path = Path(root) / file
                    json_files.append(file_path)
                    
                    # Track file types
                    parent_dir = file_path.parent.name
                    if parent_dir not in self.stats['file_types_processed']:
                        self.stats['file_types_processed'][parent_dir] = 0
                    self.stats['file_types_processed'][parent_dir] += 1
        
        logger.info(f"Discovered {len(json_files)} JSON files across {len(self.stats['directories_processed'])} directories")
        logger.info(f"File distribution: {dict(self.stats['file_types_processed'])}")
        
        return json_files

    def purify_all_files(self) -> dict:
        """Purify all JSON files in the entire codebase"""
        logger.info("COMMENCING UNIVERSAL ESCAPE SEQUENCE PURIFICATION")
        logger.info("Target: ALL JSON files in the entire codebase")
        
        # Discover all JSON files
        all_json_files = self.discover_all_json_files()
        
        # Process each file
        for file_path in all_json_files:
            self.stats['files_scanned'] += 1
            
            # Scan for issues
            issues = self.scan_file_for_issues(file_path)
            
            if issues['has_issues']:
                self.stats['files_with_issues'] += 1
                self.stats['double_backslashes_found'] += issues['double_backslashes']
                self.stats['literal_n_found'] += issues['literal_n_patterns']
                
                # Attempt purification
                was_purified = self.purify_json_file(file_path)
                
                if was_purified:
                    self.stats['files_purified'] += 1
        
        # Generate comprehensive report
        report = {
            'universal_purification_timestamp': datetime.now().isoformat(),
            'universal_purification_statistics': {
                'files_scanned': self.stats['files_scanned'],
                'files_with_issues': self.stats['files_with_issues'],
                'files_purified': self.stats['files_purified'],
                'double_backslashes_found': self.stats['double_backslashes_found'],
                'double_backslashes_fixed': self.stats['double_backslashes_fixed'],
                'literal_n_found': self.stats['literal_n_found'],
                'literal_n_fixed': self.stats['literal_n_fixed'],
                'backups_created': self.stats['backups_created'],
                'errors': self.stats['errors']
            },
            'directories_processed': list(self.stats['directories_processed']),
            'file_types_processed': self.stats['file_types_processed'],
            'purification_success': self.stats['errors'] == 0,
            'coverage_analysis': {
                'total_files_discovered': len(all_json_files),
                'files_needing_purification': self.stats['files_with_issues'],
                'purification_coverage': (self.stats['files_purified'] / max(self.stats['files_with_issues'], 1)) * 100,
                'total_artifacts_found': self.stats['double_backslashes_found'] + self.stats['literal_n_found'],
                'total_artifacts_fixed': self.stats['double_backslashes_fixed'] + self.stats['literal_n_fixed']
            }
        }
        
        # Log comprehensive results
        logger.info("UNIVERSAL ESCAPE SEQUENCE PURIFICATION COMPLETE")
        logger.info(f"Files scanned: {self.stats['files_scanned']}")
        logger.info(f"Files with issues: {self.stats['files_with_issues']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Double backslashes found: {self.stats['double_backslashes_found']}")
        logger.info(f"Double backslashes fixed: {self.stats['double_backslashes_fixed']}")
        logger.info(f"Literal \\n found: {self.stats['literal_n_found']}")
        logger.info(f"Literal \\n fixed: {self.stats['literal_n_fixed']}")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info(f"Purification coverage: {report['coverage_analysis']['purification_coverage']:.1f}%")
        
        return report

def invoke_universal_purification():
    """Invoke universal escape sequence purification"""
    logger.info("INVOKING UNIVERSAL ESCAPE SEQUENCE PURIFICATION")
    logger.info("Sacred Mission: Complete purification of ALL JSON files across the entire codebase")
    
    # Initialize purifier
    purifier = UniversalEscapePurifier()
    
    # Execute universal purification
    report = purifier.purify_all_files()
    
    # Export comprehensive report
    with open("universal_escape_purification_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Universal escape sequence purification complete - All JSON files processed")
    return report

if __name__ == "__main__":
    # Run the universal purification
    invoke_universal_purification()
