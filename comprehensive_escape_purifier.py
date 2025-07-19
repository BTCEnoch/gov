#!/usr/bin/env python3
"""
Comprehensive Escape Sequence Purification System
Eliminates all remaining escape sequence artifacts

This script identifies and fixes:
1. Double backslashes (\\) that should be single backslashes (\)
2. Remaining literal \n patterns that should be actual line breaks
3. Other escape sequence artifacts while preserving valid JSON
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
    format='%(asctime)s - [COMPREHENSIVE PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comprehensive_escape_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveEscapePurifier:
    """Comprehensive escape sequence purification system"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "comprehensive_purification_backups"
        
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
            'errors': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Comprehensive Escape Purifier initialized")

    def analyze_escape_patterns(self, content: str) -> dict:
        """Analyze content for various escape sequence patterns"""
        analysis = {
            'double_backslashes': 0,
            'literal_n_patterns': 0,
            'file_path_backslashes': 0,
            'regex_pattern_backslashes': 0,
            'other_backslashes': 0
        }
        
        # Count double backslashes
        analysis['double_backslashes'] = content.count('\\\\')
        
        # Count literal \n patterns
        analysis['literal_n_patterns'] = content.count('\\n')
        
        # Count file path patterns (common in Windows paths)
        file_path_pattern = r'"[^"]*\\[^"]*"'
        file_path_matches = re.findall(file_path_pattern, content)
        analysis['file_path_backslashes'] = len(file_path_matches)
        
        # Count regex patterns
        regex_pattern = r'"pattern":\s*"[^"]*\\[^"]*"'
        regex_matches = re.findall(regex_pattern, content)
        analysis['regex_pattern_backslashes'] = len(regex_matches)
        
        return analysis

    def smart_purify_content(self, content: str) -> tuple[str, dict]:
        """Intelligently purify content based on context"""
        fixes = {
            'double_backslashes_fixed': 0,
            'literal_n_fixed': 0,
            'total_fixes': 0
        }
        
        original_content = content
        
        # Fix 1: Convert double backslashes in file paths to single backslashes
        # Pattern: "file_path": "path\\with\\double\\backslashes"
        def fix_file_paths(match):
            full_match = match.group(0)
            path_content = match.group(1)
            # Replace double backslashes with single backslashes in file paths
            fixed_path = path_content.replace('\\\\', '\\')
            return f'"file_path": "{fixed_path}"'
        
        file_path_pattern = r'"file_path":\s*"([^"]*)"'
        content, file_path_fixes = re.subn(file_path_pattern, fix_file_paths, content)
        if file_path_fixes > 0:
            fixes['double_backslashes_fixed'] += file_path_fixes
            logger.debug(f"Fixed {file_path_fixes} file path double backslashes")
        
        # Fix 2: Convert double backslashes in regex patterns to single backslashes
        # Pattern: "pattern": "regex\\with\\double\\backslashes"
        def fix_regex_patterns(match):
            full_match = match.group(0)
            pattern_content = match.group(1)
            # Replace double backslashes with single backslashes in regex patterns
            fixed_pattern = pattern_content.replace('\\\\', '\\')
            return f'"pattern": "{fixed_pattern}"'
        
        regex_pattern = r'"pattern":\s*"([^"]*)"'
        content, regex_fixes = re.subn(regex_pattern, fix_regex_patterns, content)
        if regex_fixes > 0:
            fixes['double_backslashes_fixed'] += regex_fixes
            logger.debug(f"Fixed {regex_fixes} regex pattern double backslashes")
        
        # Fix 3: Handle remaining literal \n patterns in specific contexts
        # Only convert \n to actual line breaks in long text content (like descriptions)
        def fix_literal_n_in_long_text(match):
            field_name = match.group(1)
            text_content = match.group(2)
            
            # Only fix \n in fields that should have line breaks
            line_break_fields = [
                'description', 'full_description', 'personality_prompt', 
                'essence', 'summary', 'content', 'text', 'details'
            ]
            
            if any(field in field_name.lower() for field in line_break_fields):
                # Convert literal \n to actual line breaks
                fixed_content = text_content.replace('\\n', '\n')
                return f'"{field_name}": "{fixed_content}"'
            else:
                # Leave as-is for other fields
                return match.group(0)
        
        # Pattern for long text fields that might contain literal \n
        long_text_pattern = r'"([^"]*(?:description|prompt|essence|summary|content|text|details)[^"]*)": "([^"]{100,})"'
        content, literal_n_fixes = re.subn(long_text_pattern, fix_literal_n_in_long_text, content, flags=re.IGNORECASE)
        if literal_n_fixes > 0:
            fixes['literal_n_fixed'] += literal_n_fixes
            logger.debug(f"Fixed {literal_n_fixes} literal \\n patterns in long text fields")
        
        fixes['total_fixes'] = fixes['double_backslashes_fixed'] + fixes['literal_n_fixed']
        
        return content, fixes

    def purify_json_file(self, file_path: Path) -> bool:
        """Purify a JSON file with comprehensive escape sequence fixes"""
        try:
            logger.info(f"Comprehensive purifying: {file_path}")
            
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Analyze patterns
            analysis = self.analyze_escape_patterns(original_content)
            
            total_issues = analysis['double_backslashes'] + analysis['literal_n_patterns']
            
            if total_issues == 0:
                logger.debug(f"No escape sequence issues found in: {file_path}")
                return False
            
            logger.info(f"Found issues in {file_path}:")
            logger.info(f"  - Double backslashes: {analysis['double_backslashes']}")
            logger.info(f"  - Literal \\n patterns: {analysis['literal_n_patterns']}")
            
            self.stats['files_with_issues'] += 1
            self.stats['double_backslashes_found'] += analysis['double_backslashes']
            self.stats['literal_n_found'] += analysis['literal_n_patterns']
            
            # Apply smart purification
            purified_content, fixes = self.smart_purify_content(original_content)
            
            if fixes['total_fixes'] > 0:
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
                
                logger.info(f"Comprehensive purified: {file_path}")
                logger.info(f"  - Double backslashes fixed: {fixes['double_backslashes_fixed']}")
                logger.info(f"  - Literal \\n fixed: {fixes['literal_n_fixed']}")
                return True
            else:
                logger.warning(f"Found issues but couldn't safely fix them in: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error purifying {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.comprehensive.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def purify_all_json_files(self) -> dict:
        """Purify all JSON files in the codebase"""
        logger.info("COMMENCING COMPREHENSIVE ESCAPE SEQUENCE PURIFICATION")
        logger.info("Target: Fix double backslashes and remaining literal \\n patterns")
        
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
            'comprehensive_purification_timestamp': datetime.now().isoformat(),
            'comprehensive_purification_statistics': self.stats,
            'purification_success': self.stats['errors'] == 0,
            'fixes_summary': {
                'double_backslashes': {
                    'found': self.stats['double_backslashes_found'],
                    'fixed': self.stats['double_backslashes_fixed'],
                    'success_rate': (self.stats['double_backslashes_fixed'] / max(self.stats['double_backslashes_found'], 1)) * 100
                },
                'literal_n_patterns': {
                    'found': self.stats['literal_n_found'],
                    'fixed': self.stats['literal_n_fixed'],
                    'success_rate': (self.stats['literal_n_fixed'] / max(self.stats['literal_n_found'], 1)) * 100
                }
            }
        }
        
        # Log results
        logger.info("COMPREHENSIVE ESCAPE SEQUENCE PURIFICATION COMPLETE")
        logger.info(f"Files scanned: {self.stats['files_scanned']}")
        logger.info(f"Files with issues: {self.stats['files_with_issues']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Double backslashes found: {self.stats['double_backslashes_found']}")
        logger.info(f"Double backslashes fixed: {self.stats['double_backslashes_fixed']}")
        logger.info(f"Literal \\n found: {self.stats['literal_n_found']}")
        logger.info(f"Literal \\n fixed: {self.stats['literal_n_fixed']}")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

def invoke_comprehensive_purification():
    """Invoke comprehensive escape sequence purification"""
    logger.info("INVOKING COMPREHENSIVE ESCAPE SEQUENCE PURIFICATION")
    logger.info("Sacred Mission: Complete elimination of ALL escape sequence artifacts")
    
    # Initialize purifier
    purifier = ComprehensiveEscapePurifier()
    
    # Execute comprehensive purification
    report = purifier.purify_all_json_files()
    
    # Export report
    with open("comprehensive_escape_purification_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Comprehensive escape sequence purification complete")
    return report

if __name__ == "__main__":
    # Run the comprehensive purification
    invoke_comprehensive_purification()
