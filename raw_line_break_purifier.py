#!/usr/bin/env python3
"""
Raw Line Break Purification System
Direct text replacement approach for literal \n patterns

This script works directly with raw file content to replace literal \n patterns
with actual line breaks, bypassing JSON parsing issues.
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
    format='%(asctime)s - [RAW PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('raw_line_break_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RawLineBreakPurifier:
    """Raw text-based purification system for literal \n patterns"""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "raw_purification_backups"
        
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
        
        logger.info("Raw Line Break Purifier initialized")

    def scan_file_for_literal_n(self, file_path: Path) -> int:
        """Scan file for literal \n patterns in raw content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count literal \n patterns (backslash followed by n)
            pattern_count = content.count('\\n')
            return pattern_count
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            return 0

    def purify_file_raw(self, file_path: Path) -> bool:
        """Purify file using raw text replacement"""
        try:
            logger.info(f"Raw purifying: {file_path}")
            
            # Read raw content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Count original patterns
            original_count = original_content.count('\\n')
            self.stats['literal_n_patterns_found'] += original_count
            
            if original_count == 0:
                logger.debug(f"No literal \\n patterns found in: {file_path}")
                return False
            
            logger.info(f"Found {original_count} literal \\n patterns in: {file_path}")
            self.stats['files_with_issues'] += 1
            
            # Replace literal \n with actual line breaks
            purified_content = original_content.replace('\\n', '\n')
            
            # Verify the replacement worked
            remaining_count = purified_content.count('\\n')
            fixed_count = original_count - remaining_count
            
            if fixed_count > 0:
                # Validate that the result is still valid JSON (for JSON files)
                if file_path.suffix.lower() == '.json':
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
                self.stats['literal_n_patterns_fixed'] += fixed_count
                
                logger.info(f"Raw purified: {file_path} - {fixed_count} literal \\n patterns fixed")
                return True
            else:
                logger.warning(f"Could not fix patterns in: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error purifying {file_path}: {e}")
            self.stats['errors'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.raw.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.stats['backups_created'] += 1
        
        return backup_path

    def purify_all_files(self, file_extensions: list = ['.json']) -> dict:
        """Purify all files with specified extensions"""
        logger.info("COMMENCING RAW LINE BREAK PURIFICATION")
        logger.info(f"Target: Direct replacement of literal \\n patterns in {file_extensions} files")
        
        # Walk through all files
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                
                # Check if file has target extension
                if file_path.suffix.lower() in file_extensions and not file.endswith('.bak'):
                    self.stats['files_scanned'] += 1
                    
                    was_purified = self.purify_file_raw(file_path)
                    
                    if was_purified:
                        self.stats['files_purified'] += 1
        
        # Generate report
        report = {
            'raw_purification_timestamp': datetime.now().isoformat(),
            'raw_purification_statistics': self.stats,
            'purification_success': self.stats['errors'] == 0,
            'patterns_found_vs_fixed': {
                'found': self.stats['literal_n_patterns_found'],
                'fixed': self.stats['literal_n_patterns_fixed'],
                'success_rate': (self.stats['literal_n_patterns_fixed'] / max(self.stats['literal_n_patterns_found'], 1)) * 100
            }
        }
        
        # Log results
        logger.info("RAW LINE BREAK PURIFICATION COMPLETE")
        logger.info(f"Files scanned: {self.stats['files_scanned']}")
        logger.info(f"Files with issues: {self.stats['files_with_issues']}")
        logger.info(f"Files purified: {self.stats['files_purified']}")
        logger.info(f"Literal \\n patterns found: {self.stats['literal_n_patterns_found']}")
        logger.info(f"Literal \\n patterns fixed: {self.stats['literal_n_patterns_fixed']}")
        logger.info(f"Success rate: {report['patterns_found_vs_fixed']['success_rate']:.1f}%")
        logger.info(f"Backups created: {self.stats['backups_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return report

    def preview_specific_files(self, file_list: list) -> dict:
        """Preview specific files for literal \n patterns"""
        logger.info("PREVIEWING SPECIFIC FILES FOR LITERAL \\n PATTERNS")
        
        issues_found = []
        
        for file_path_str in file_list:
            file_path = Path(file_path_str)
            
            if file_path.exists():
                pattern_count = self.scan_file_for_literal_n(file_path)
                
                if pattern_count > 0:
                    issues_found.append({
                        'file': str(file_path),
                        'literal_n_count': pattern_count
                    })
                    
                    logger.info(f"Issue found: {file_path} - {pattern_count} literal \\n patterns")
        
        preview_report = {
            'preview_timestamp': datetime.now().isoformat(),
            'files_checked': len(file_list),
            'files_with_issues': len(issues_found),
            'issues_found': issues_found,
            'total_patterns_found': sum(issue['literal_n_count'] for issue in issues_found)
        }
        
        logger.info(f"Preview complete: {len(issues_found)} files with issues found")
        logger.info(f"Total literal \\n patterns: {preview_report['total_patterns_found']}")
        
        return preview_report

def invoke_raw_purification():
    """Invoke raw line break purification"""
    logger.info("INVOKING RAW LINE BREAK PURIFICATION")
    logger.info("Sacred Mission: Direct elimination of literal \\n artifacts via raw text replacement")
    
    # Initialize purifier
    purifier = RawLineBreakPurifier()
    
    # Test with a few specific files first
    test_files = [
        "onchain/comprehensive_integration_data.json",
        "lighthouse/traditions/lighthouse_master_index.json"
    ]
    
    logger.info("Step 1: Testing with specific files...")
    preview_report = purifier.preview_specific_files(test_files)
    
    # Export preview report
    with open("raw_purification_preview.json", 'w', encoding='utf-8') as f:
        json.dump(preview_report, f, indent=2, ensure_ascii=True)
    
    if preview_report['files_with_issues'] > 0:
        logger.info(f"Step 2: Raw purifying {preview_report['files_with_issues']} test files...")
        
        # Purify just the test files first
        for issue in preview_report['issues_found']:
            file_path = Path(issue['file'])
            purifier.purify_file_raw(file_path)
        
        # Generate test report
        test_report = {
            'test_purification_timestamp': datetime.now().isoformat(),
            'test_files': test_files,
            'test_statistics': purifier.stats
        }
        
        # Export test report
        with open("raw_purification_test_report.json", 'w', encoding='utf-8') as f:
            json.dump(test_report, f, indent=2, ensure_ascii=True)
        
        logger.info("Raw purification test complete")
        
        # If test was successful, offer to run on all files
        if purifier.stats['errors'] == 0:
            logger.info("Test successful! Ready to run on all files.")
        else:
            logger.warning("Test had errors. Check logs before proceeding.")
    else:
        logger.info("No issues found in test files")
    
    return preview_report

if __name__ == "__main__":
    # Run the raw purification test
    invoke_raw_purification()
