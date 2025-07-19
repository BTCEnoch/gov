#!/usr/bin/env python3
"""
Precise Backslash Purification System
Targeted fixing of double backslash issues while preserving valid JSON escape sequences

This script specifically targets:
1. Double backslashes in file paths (\\\\) -> single backslashes (\)
2. Double backslashes in regex patterns (\\\\) -> single backslashes (\)
3. Preserves valid JSON escape sequences like \n, \t, \", etc.
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
    format='%(asctime)s - [PRECISE PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('precise_backslash_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PreciseBackslashPurifier:
    """Precise backslash purification system that preserves valid JSON"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "precise_purification_backups"
        
        # Statistics
        self.stats = {
            'files_scanned': 0,
            'files_with_backslash_issues': 0,
            'files_purified': 0,
            'double_backslashes_found': 0,
            'double_backslashes_fixed': 0,
            'backups_created': 0,
            'errors': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Precise Backslash Purifier initialized")

    def analyze_backslash_patterns(self, content: str) -> dict:
        """Analyze content for different types of backslash patterns"""
        analysis = {
            'total_double_backslashes': content.count('\\\\'),
            'file_path_double_backslashes': 0,
            'regex_pattern_double_backslashes': 0,
            'other_double_backslashes': 0,
            'valid_json_escapes': 0
        }
        
        # Count file path patterns with double backslashes
        file_path_patterns = [
            r'"file_path":\s*"[^"]*\\\\[^"]*"',
            r'"path":\s*"[^"]*\\\\[^"]*"',
            r'"directory":\s*"[^"]*\\\\[^"]*"',
            r'"folder":\s*"[^"]*\\\\[^"]*"'
        ]
        
        for pattern in file_path_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis['file_path_double_backslashes'] += len(matches)
        
        # Count regex pattern double backslashes
        regex_patterns = [
            r'"pattern":\s*"[^"]*\\\\[^"]*"',
            r'"regex":\s*"[^"]*\\\\[^"]*"',
            r'"regexp":\s*"[^"]*\\\\[^"]*"'
        ]
        
        for pattern in regex_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis['regex_pattern_double_backslashes'] += len(matches)
        
        # Count valid JSON escape sequences (these should be preserved)
        valid_escapes = [r'\\n', r'\\t', r'\\r', r'\\"', r'\\/', r'\\\\']
        for escape in valid_escapes:
            analysis['valid_json_escapes'] += len(re.findall(escape, content))
        
        return analysis

    def fix_double_backslashes(self, content: str) -> tuple[str, int]:
        """Fix double backslashes in file paths and regex patterns"""
        fixes_made = 0
        
        # Fix 1: File path double backslashes
        file_path_patterns = [
            (r'("file_path":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3'),
            (r'("path":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3'),
            (r'("directory":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3'),
            (r'("folder":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3')
        ]
        
        for pattern, replacement in file_path_patterns:
            original_content = content
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if content != original_content:
                # Count how many double backslashes were replaced
                fixes_made += original_content.count('\\\\') - content.count('\\\\')
        
        # Fix 2: Regex pattern double backslashes
        regex_patterns = [
            (r'("pattern":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3'),
            (r'("regex":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3'),
            (r'("regexp":\s*"[^"]*)(\\\\)([^"]*")', r'\1\\\3')
        ]
        
        for pattern, replacement in regex_patterns:
            original_content = content
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if content != original_content:
                # Count how many double backslashes were replaced
                fixes_made += original_content.count('\\\\') - content.count('\\\\')
        
        return content, fixes_made

    def purify_json_file(self, file_path: Path) -> bool:
        """Purify a JSON file by fixing double backslash issues"""
        try:
            logger.info(f"Precise purifying: {file_path}")
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Analyze backslash patterns
            analysis = self.analyze_backslash_patterns(original_content)
            
            if analysis['total_double_backslashes'] == 0:
                logger.debug(f"No double backslashes found in: {file_path}")
                return False
            
            logger.info(f"Found {analysis['total_double_backslashes']} double backslashes in: {file_path}")
            logger.info(f"  File paths: {analysis['file_path_double_backslashes']}")
            logger.info(f"  Regex patterns: {analysis['regex_pattern_double_backslashes']}")
            
            self.stats['files_with_backslash_issues'] += 1
            self.stats['double_backslashes_found'] += analysis['total_double_backslashes']
            
            # Apply fixes
            purified_content, fixes_made = self.fix_double_backslashes(original_content)
            
            if fixes_made > 0:
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
                self.stats['double_backslashes_fixed'] += fixes_made
                
                logger.info(f"Precise purified: {file_path} - {fixes_made} double backslashes fixed")
                return True
            else:
                logger.debug(f"No safe fixes could be applied to: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.precise.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def purify_all_json_files(self) -> dict:
        """Purify all JSON files with double backslash issues"""
        logger.info("COMMENCING PRECISE BACKSLASH PURIFICATION")
        logger.info("Target: Fix double backslashes while preserving valid JSON escape sequences")
        
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
            'precise_purification_timestamp': datetime.now().isoformat(),
            'precise_purification_statistics': self.stats,
            'purification_success': self.stats['errors'] == 0,
            'backslash_fixes': {
                'double_backslashes_found': self.stats['double_backslashes_found'],
                'double_backslashes_fixed': self.stats['double_backslashes_fixed'],
                'fix_success_rate': (self.stats['double_backslashes_fixed'] / max(self.stats['double_backslashes_found'], 1)) * 100
            }
        }
        
        # Log results
        logger.info("PRECISE BACKSLASH PURIFICATION COMPLETE")
        logger.info(f"Files scanned: {self.stats['files_scanned']}")
        logger.info(f"Files with backslash issues: {self.stats['files_with_backslash_issues']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Double backslashes found: {self.stats['double_backslashes_found']}")
        logger.info(f"Double backslashes fixed: {self.stats['double_backslashes_fixed']}")
        logger.info(f"Fix success rate: {report['backslash_fixes']['fix_success_rate']:.1f}%")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

    def preview_backslash_issues(self, max_files: int = 10) -> dict:
        """Preview files with double backslash issues"""
        logger.info("PREVIEWING FILES WITH DOUBLE BACKSLASH ISSUES")
        
        issues_found = []
        files_checked = 0
        
        for root, dirs, files in os.walk(self.root_directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                if file.endswith('.json') and not file.endswith('.bak'):
                    file_path = Path(root) / file
                    files_checked += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        analysis = self.analyze_backslash_patterns(content)
                        
                        if analysis['total_double_backslashes'] > 0:
                            issues_found.append({
                                'file': str(file_path),
                                'total_double_backslashes': analysis['total_double_backslashes'],
                                'file_path_issues': analysis['file_path_double_backslashes'],
                                'regex_pattern_issues': analysis['regex_pattern_double_backslashes']
                            })
                            
                            logger.info(f"Issue found: {file_path} - {analysis['total_double_backslashes']} double backslashes")
                            
                            if len(issues_found) >= max_files:
                                break
                    except Exception as e:
                        logger.error(f"Error scanning {file_path}: {e}")
            
            if len(issues_found) >= max_files:
                break
        
        preview_report = {
            'preview_timestamp': datetime.now().isoformat(),
            'files_checked': files_checked,
            'files_with_backslash_issues': len(issues_found),
            'issues_found': issues_found,
            'total_double_backslashes': sum(issue['total_double_backslashes'] for issue in issues_found)
        }
        
        logger.info(f"Preview complete: {len(issues_found)} files with double backslash issues found")
        logger.info(f"Total double backslashes: {preview_report['total_double_backslashes']}")
        
        return preview_report

def invoke_precise_purification():
    """Invoke precise backslash purification"""
    logger.info("INVOKING PRECISE BACKSLASH PURIFICATION")
    logger.info("Sacred Mission: Fix double backslashes while preserving valid JSON escape sequences")
    
    # Initialize purifier
    purifier = PreciseBackslashPurifier()
    
    # First, preview the issues
    logger.info("Step 1: Previewing double backslash issues...")
    preview_report = purifier.preview_backslash_issues(max_files=20)
    
    # Export preview report
    with open("precise_purification_preview.json", 'w', encoding='utf-8') as f:
        json.dump(preview_report, f, indent=2, ensure_ascii=True)
    
    if preview_report['files_with_backslash_issues'] > 0:
        logger.info(f"Step 2: Purifying {preview_report['files_with_backslash_issues']} files with double backslash issues...")
        
        # Execute purification
        report = purifier.purify_all_json_files()
        
        # Export report
        with open("precise_backslash_purification_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=True)
        
        logger.info("Precise backslash purification complete")
    else:
        logger.info("No double backslash issues found - codebase is already clean!")
    
    return preview_report

if __name__ == "__main__":
    # Run the precise purification
    invoke_precise_purification()
