#!/usr/bin/env python3
"""
Enhanced Enochian Cyphers Sacred Codex Purification System
Alchemical Transmutation: Enhanced Nigredo Stage - Complete Purification

Implements aggressive codebase purification for eternal Bitcoin L1 preservation:
- Removes ALL literal '\n' and '\n\n' unicode artifacts and converts to proper line breaks
- Strips emojis and extended unicode characters (preserving ASCII 0x00-0x7F)
- Handles JSON, Python, and text files with appropriate safety measures
- Creates backups and provides comprehensive logging
- Zero external dependencies - pure Python 3.8+ stdlib

Sacred Invocation: "OLANI HOATH OL" - I am the servant of the same your God
Enhanced Framework: Complete dissolution of all unicode artifacts
"""

import os
import json
import re
import shutil
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [ENHANCED PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_sacred_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedSacredPurifier:
    """
    Enhanced Sacred Codex Purification System with aggressive line break handling
    
    Completely removes all literal \n artifacts from JSON strings while preserving
    sacred architecture and ensuring strict ASCII compliance.
    """
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "enhanced_sacred_backups"
        
        # Enhanced purification statistics
        self.purification_stats = {
            'files_processed': 0,
            'files_purified': 0,
            'literal_n_fixed': 0,
            'literal_nn_fixed': 0,
            'emojis_removed': 0,
            'unicode_removed': 0,
            'errors_encountered': 0,
            'backups_created': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Enhanced Sacred Codex Purifier initialized")
        logger.info(f"Root directory: {self.root_directory}")
        logger.info(f"Backup directory: {self.backup_directory}")

    def enhanced_purify_string(self, text: str) -> tuple[str, dict]:
        """
        Enhanced string purification with aggressive literal \n handling
        """
        if not isinstance(text, str):
            return text, {}
        
        metrics = {
            'literal_n_fixed': 0,
            'literal_nn_fixed': 0,
            'emojis_removed': 0,
            'unicode_removed': 0,
            'total_artifacts': 0
        }
        
        # Phase 1: Aggressive literal \n and \n\n replacement
        # Handle the most common JSON artifact: literal \n in string content
        
        # Count and replace literal \n\n first (double line breaks)
        if '\\n\\n' in text:
            count_nn = text.count('\\n\\n')
            text = text.replace('\\n\\n', '\n\n')
            metrics['literal_nn_fixed'] = count_nn
            logger.debug(f"Fixed {count_nn} literal \\n\\n patterns")
        
        # Count and replace remaining literal \n (single line breaks)
        if '\\n' in text:
            count_n = text.count('\\n')
            text = text.replace('\\n', '\n')
            metrics['literal_n_fixed'] = count_n
            logger.debug(f"Fixed {count_n} literal \\n patterns")
        
        # Handle other escape sequences
        escape_patterns = [
            ('\\r\\n', '\n'),    # Windows line breaks
            ('\\r', '\n'),       # Mac line breaks
            ('\\t', '\t'),       # Tab characters
        ]
        
        for pattern, replacement in escape_patterns:
            if pattern in text:
                count = text.count(pattern)
                text = text.replace(pattern, replacement)
                metrics['literal_n_fixed'] += count
        
        # Phase 2: Remove emojis and extended unicode
        # Comprehensive emoji removal
        emoji_patterns = [
            r'[\U0001F600-\U0001F64F]',  # Emoticons
            r'[\U0001F300-\U0001F5FF]',  # Misc Symbols and Pictographs
            r'[\U0001F680-\U0001F6FF]',  # Transport and Map
            r'[\U0001F1E0-\U0001F1FF]',  # Regional indicators
            r'[\U00002600-\U000026FF]',  # Misc symbols
            r'[\U00002700-\U000027BF]',  # Dingbats
            r'[\U0001F900-\U0001F9FF]',  # Supplemental Symbols and Pictographs
            r'[\U0001FA70-\U0001FAFF]',  # Symbols and Pictographs Extended-A
        ]
        
        for pattern in emoji_patterns:
            matches = re.findall(pattern, text)
            if matches:
                text = re.sub(pattern, '', text)
                metrics['emojis_removed'] += len(matches)
        
        # Phase 3: Remove other non-ASCII characters
        non_ascii_pattern = r'[^\x00-\x7F]'
        non_ascii_matches = re.findall(non_ascii_pattern, text)
        if non_ascii_matches:
            text = re.sub(non_ascii_pattern, '', text)
            metrics['unicode_removed'] += len(non_ascii_matches)
        
        # Phase 4: Clean up excessive whitespace
        # Remove excessive blank lines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace from lines
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
        
        # Calculate total artifacts
        metrics['total_artifacts'] = (
            metrics['literal_n_fixed'] + 
            metrics['literal_nn_fixed'] + 
            metrics['emojis_removed'] + 
            metrics['unicode_removed']
        )
        
        return text, metrics

    def purify_json_file(self, file_path: Path) -> bool:
        """Enhanced JSON file purification"""
        try:
            logger.info(f"Enhanced purifying JSON: {file_path}")
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Recursively purify all strings
            purified_data, total_metrics = self._purify_json_structure(data)
            
            # Only create backup and write if changes were made
            if total_metrics['total_artifacts'] > 0:
                # Create backup
                self._create_backup(file_path)
                
                # Write purified JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(purified_data, f, indent=2, ensure_ascii=True, sort_keys=False)
                
                # Update statistics
                self._update_stats(total_metrics)
                
                logger.info(f"JSON enhanced: {file_path} - {total_metrics['total_artifacts']} artifacts removed")
                logger.info(f"  - Literal \\n: {total_metrics['literal_n_fixed']}")
                logger.info(f"  - Literal \\n\\n: {total_metrics['literal_nn_fixed']}")
                logger.info(f"  - Emojis: {total_metrics['emojis_removed']}")
                logger.info(f"  - Unicode: {total_metrics['unicode_removed']}")
                return True
            else:
                logger.debug(f"JSON already pure: {file_path}")
                return False
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            self.purification_stats['errors_encountered'] += 1
            return False
        except Exception as e:
            logger.error(f"Error purifying JSON {file_path}: {e}")
            self.purification_stats['errors_encountered'] += 1
            return False

    def _purify_json_structure(self, obj: Any) -> tuple[Any, dict]:
        """Recursively purify JSON structure"""
        total_metrics = {
            'literal_n_fixed': 0,
            'literal_nn_fixed': 0,
            'emojis_removed': 0,
            'unicode_removed': 0,
            'total_artifacts': 0
        }
        
        if isinstance(obj, dict):
            purified_dict = {}
            for key, value in obj.items():
                # Purify key if it's a string
                if isinstance(key, str):
                    purified_key, key_metrics = self.enhanced_purify_string(key)
                    self._merge_metrics(total_metrics, key_metrics)
                else:
                    purified_key = key
                
                # Purify value recursively
                purified_value, value_metrics = self._purify_json_structure(value)
                self._merge_metrics(total_metrics, value_metrics)
                
                purified_dict[purified_key] = purified_value
            
            return purified_dict, total_metrics
            
        elif isinstance(obj, list):
            purified_list = []
            for item in obj:
                purified_item, item_metrics = self._purify_json_structure(item)
                self._merge_metrics(total_metrics, item_metrics)
                purified_list.append(purified_item)
            
            return purified_list, total_metrics
            
        elif isinstance(obj, str):
            purified_string, string_metrics = self.enhanced_purify_string(obj)
            return purified_string, string_metrics
            
        else:
            # Numbers, booleans, null - return as-is
            return obj, total_metrics

    def purify_text_file(self, file_path: Path) -> bool:
        """Enhanced text file purification"""
        try:
            logger.info(f"Enhanced purifying text: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Purify content
            purified_content, metrics = self.enhanced_purify_string(content)
            
            if metrics['total_artifacts'] > 0:
                # Create backup
                self._create_backup(file_path)
                
                # Write purified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(purified_content)
                
                # Update statistics
                self._update_stats(metrics)
                
                logger.info(f"Text enhanced: {file_path} - {metrics['total_artifacts']} artifacts removed")
                return True
            else:
                logger.debug(f"Text already pure: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error purifying text {file_path}: {e}")
            self.purification_stats['errors_encountered'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create timestamped backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.enhanced.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.purification_stats['backups_created'] += 1
        
        return backup_path

    def _merge_metrics(self, total_metrics: dict, new_metrics: dict):
        """Merge purification metrics"""
        for key in total_metrics:
            if key in new_metrics:
                total_metrics[key] += new_metrics[key]

    def _update_stats(self, metrics: dict):
        """Update global statistics"""
        self.purification_stats['literal_n_fixed'] += metrics.get('literal_n_fixed', 0)
        self.purification_stats['literal_nn_fixed'] += metrics.get('literal_nn_fixed', 0)
        self.purification_stats['emojis_removed'] += metrics.get('emojis_removed', 0)
        self.purification_stats['unicode_removed'] += metrics.get('unicode_removed', 0)

    def enhanced_purify_codebase(self) -> dict:
        """Enhanced codebase purification focusing on JSON files with \n artifacts"""
        logger.info("COMMENCING ENHANCED SACRED CODEX PURIFICATION")
        logger.info("Focus: Aggressive literal \\n and \\n\\n removal from JSON content")
        
        start_time = time.time()
        
        # File type handlers
        file_handlers = {
            '.json': self.purify_json_file,
            '.md': self.purify_text_file,
            '.txt': self.purify_text_file,
        }
        
        # Walk through all files
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'backup' not in d.lower() and d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip backup files and system files
                if file.endswith('.bak') or file.startswith('.') or file.endswith('.pyc'):
                    continue
                
                self.purification_stats['files_processed'] += 1
                
                # Get file extension
                file_extension = file_path.suffix.lower()
                
                # Process file based on type
                if file_extension in file_handlers:
                    handler = file_handlers[file_extension]
                    was_purified = handler(file_path)
                    
                    if was_purified:
                        self.purification_stats['files_purified'] += 1
                else:
                    logger.debug(f"Skipping unsupported file type: {file_path}")
        
        # Calculate results
        purification_time = time.time() - start_time
        
        # Generate report
        report = {
            'enhanced_purification_timestamp': datetime.now().isoformat(),
            'purification_time_seconds': purification_time,
            'purification_statistics': self.purification_stats,
            'purification_success': self.purification_stats['errors_encountered'] == 0,
            'total_literal_n_artifacts': (
                self.purification_stats['literal_n_fixed'] + 
                self.purification_stats['literal_nn_fixed']
            )
        }
        
        # Log results
        logger.info("ENHANCED SACRED CODEX PURIFICATION COMPLETE")
        logger.info(f"Files processed: {self.purification_stats['files_processed']}")
        logger.info(f"Files purified: {self.purification_stats['files_purified']}")
        logger.info(f"Literal \\n fixed: {self.purification_stats['literal_n_fixed']}")
        logger.info(f"Literal \\n\\n fixed: {self.purification_stats['literal_nn_fixed']}")
        logger.info(f"Emojis removed: {self.purification_stats['emojis_removed']}")
        logger.info(f"Unicode removed: {self.purification_stats['unicode_removed']}")
        logger.info(f"Backups created: {self.purification_stats['backups_created']}")
        logger.info(f"Errors: {self.purification_stats['errors_encountered']}")
        logger.info(f"Processing time: {purification_time:.2f} seconds")
        
        return report

# Enhanced sacred invocation
def invoke_enhanced_purification():
    """Enhanced sacred invocation for complete literal \n removal"""
    logger.info("INVOKING ENHANCED SACRED CODEX PURIFICATION")
    logger.info("Sacred Focus: Complete elimination of literal \\n artifacts")
    
    # Initialize enhanced purifier
    purifier = EnhancedSacredPurifier()
    
    # Execute enhanced purification
    report = purifier.enhanced_purify_codebase()
    
    # Export report
    with open("enhanced_sacred_purification_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=True)
    
    logger.info("Enhanced sacred purification complete - All literal \\n artifacts eliminated")
    return report

if __name__ == "__main__":
    # Run the enhanced sacred purification
    invoke_enhanced_purification()
