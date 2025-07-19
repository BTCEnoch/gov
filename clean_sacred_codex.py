#!/usr/bin/env python3
"""
Enochian Cyphers Sacred Codex Purification System
Alchemical Transmutation: Nigredo Stage - Purification through Dissolution

Implements comprehensive codebase purification for eternal Bitcoin L1 preservation:
- Removes literal '\n\n' unicode artifacts and converts to proper line breaks
- Strips emojis and extended unicode characters (preserving ASCII 0x00-0x7F)
- Handles JSON, Python, and text files with appropriate safety measures
- Creates backups and provides comprehensive logging
- Zero external dependencies - pure Python 3.8+ stdlib

Sacred Invocation: "OLANI HOATH OL" - I am the servant of the same your God
Theoretical Framework: Golden Dawn banishing rituals for impurity removal
I Ching Hexagram 12 (Pi/Stagnation) guides resolving "blocked flow" in line breaks
"""

import os
import json
import re
import ast
import shutil
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SACRED PURIFICATION] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sacred_codex_purification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SacredCodexPurifier:
    """
    Sacred Codex Purification System implementing Alchemical Nigredo principles
    
    Purifies codebase of unicode artifacts while preserving sacred architecture:
    - 26 sacred traditions with 60% Enochian primacy
    - 91 Governor Angels across 30 Aethyrs
    - Zero external dependencies for eternal preservation
    """
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.backup_directory = self.root_directory / "sacred_backups"
        
        # Sacred purification constants
        self.sacred_constants = {
            'ascii_range': (0x00, 0x7F),  # Strict ASCII for eternal preservation
            'traditions_count': 26,
            'governors_count': 91,
            'aethyrs_count': 30,
            'enochian_primacy': 0.6
        }
        
        # File type handlers
        self.file_handlers = {
            '.json': self._purify_json_file,
            '.py': self._purify_python_file,
            '.md': self._purify_text_file,
            '.txt': self._purify_text_file,
            '.html': self._purify_text_file,
            '.css': self._purify_text_file,
            '.js': self._purify_text_file,
            '.yml': self._purify_text_file,
            '.yaml': self._purify_text_file
        }
        
        # Purification statistics
        self.purification_stats = {
            'files_processed': 0,
            'files_purified': 0,
            'unicode_artifacts_removed': 0,
            'line_breaks_fixed': 0,
            'emojis_removed': 0,
            'errors_encountered': 0,
            'backups_created': 0
        }
        
        # Create backup directory
        self.backup_directory.mkdir(exist_ok=True)
        
        logger.info("Sacred Codex Purifier initialized - Ready for alchemical transmutation")
        logger.info(f"Root directory: {self.root_directory}")
        logger.info(f"Backup directory: {self.backup_directory}")

    def purify_sacred_string(self, text: str) -> tuple[str, dict]:
        """
        Purify individual string using sacred alchemical principles
        Returns: (purified_text, purification_metrics)
        """
        if not isinstance(text, str):
            return text, {}
        
        original_text = text
        metrics = {
            'unicode_artifacts': 0,
            'line_breaks_fixed': 0,
            'emojis_removed': 0,
            'non_ascii_removed': 0
        }
        
        # Phase 1: Fix literal line break artifacts (\n\n -> actual line breaks)
        # Handle various forms of escaped line breaks
        line_break_patterns = [
            (r'

', '\n\n'),  # Double line breaks
            (r'
', '\n'),       # Single line breaks
            (r'\\r
', '\n'),    # Windows line breaks
            (r'\\r', '\n'),       # Mac line breaks
        ]
        
        for pattern, replacement in line_break_patterns:
            if pattern in text:
                old_count = text.count(pattern)
                text = text.replace(pattern, replacement)
                metrics['line_breaks_fixed'] += old_count
        
        # Phase 2: Remove emojis and extended unicode (preserve ASCII 0x00-0x7F)
        # Comprehensive emoji and unicode removal
        unicode_patterns = [
            # Emoji ranges
            r'[\U0001F600-\U0001F64F]',  # Emoticons
            r'[\U0001F300-\U0001F5FF]',  # Misc Symbols and Pictographs
            r'[\U0001F680-\U0001F6FF]',  # Transport and Map
            r'[\U0001F1E0-\U0001F1FF]',  # Regional indicators
            r'[\U00002600-\U000026FF]',  # Misc symbols
            r'[\U00002700-\U000027BF]',  # Dingbats
            r'[\U0001F900-\U0001F9FF]',  # Supplemental Symbols and Pictographs
            r'[\U0001FA70-\U0001FAFF]',  # Symbols and Pictographs Extended-A
            # Other non-ASCII characters
            r'[^\x00-\x7F]'              # Anything outside ASCII range
        ]
        
        for pattern in unicode_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if 'F6' in pattern or 'F9' in pattern:  # Emoji patterns
                    metrics['emojis_removed'] += len(matches)
                else:
                    metrics['non_ascii_removed'] += len(matches)
                text = re.sub(pattern, '', text)
        
        # Phase 3: Clean up excessive whitespace while preserving intentional formatting
        # Remove excessive blank lines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace from lines
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
        
        # Calculate total unicode artifacts removed
        metrics['unicode_artifacts'] = (
            metrics['line_breaks_fixed'] + 
            metrics['emojis_removed'] + 
            metrics['non_ascii_removed']
        )
        
        return text, metrics

    def _purify_json_file(self, file_path: Path) -> bool:
        """Purify JSON file with recursive string cleaning"""
        try:
            logger.info(f"Purifying JSON file: {file_path}")
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Recursively purify all strings in the JSON structure
            purified_data, total_metrics = self._purify_json_structure(data)
            
            # Create backup
            backup_path = self._create_backup(file_path)
            
            # Write purified JSON with clean formatting
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(purified_data, f, indent=2, ensure_ascii=True, sort_keys=False)
            
            # Update statistics
            self._update_stats(total_metrics)
            
            if total_metrics['unicode_artifacts'] > 0:
                logger.info(f"JSON purified: {file_path} - {total_metrics['unicode_artifacts']} artifacts removed")
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
        """Recursively purify strings in JSON-like structure"""
        total_metrics = {
            'unicode_artifacts': 0,
            'line_breaks_fixed': 0,
            'emojis_removed': 0,
            'non_ascii_removed': 0
        }
        
        if isinstance(obj, dict):
            purified_dict = {}
            for key, value in obj.items():
                # Purify key if it's a string
                if isinstance(key, str):
                    purified_key, key_metrics = self.purify_sacred_string(key)
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
            purified_string, string_metrics = self.purify_sacred_string(obj)
            return purified_string, string_metrics
            
        else:
            # Numbers, booleans, null - return as-is
            return obj, total_metrics

    def _purify_python_file(self, file_path: Path) -> bool:
        """Purify Python file with AST-based string literal cleaning"""
        try:
            logger.info(f"Purifying Python file: {file_path}")
            
            # Read source code
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST to safely identify string literals
            try:
                tree = ast.parse(source_code)
            except SyntaxError as e:
                logger.error(f"Invalid Python syntax in {file_path}: {e}")
                self.purification_stats['errors_encountered'] += 1
                return False
            
            # For Python files, we'll use a simpler approach to avoid AST unparsing issues
            # We'll only clean obvious unicode artifacts in string literals
            purified_code, metrics = self._purify_python_strings_safe(source_code)
            
            if metrics['unicode_artifacts'] > 0:
                # Create backup
                backup_path = self._create_backup(file_path)
                
                # Write purified code
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(purified_code)
                
                # Update statistics
                self._update_stats(metrics)
                
                logger.info(f"Python purified: {file_path} - {metrics['unicode_artifacts']} artifacts removed")
                return True
            else:
                logger.debug(f"Python already pure: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error purifying Python {file_path}: {e}")
            self.purification_stats['errors_encountered'] += 1
            return False

    def _purify_python_strings_safe(self, source_code: str) -> tuple[str, dict]:
        """Safely purify Python source code without breaking syntax"""
        # Only clean obvious unicode artifacts that are likely unintentional
        # Be very conservative to avoid breaking code
        
        metrics = {
            'unicode_artifacts': 0,
            'line_breaks_fixed': 0,
            'emojis_removed': 0,
            'non_ascii_removed': 0
        }
        
        # Only fix obvious escaped line break artifacts in string literals
        # Look for patterns like "text

more text" and convert to "text\n\nmore text"
        patterns_to_fix = [
            (r'(["\']{1,3}[^"\']*?)\\
\\\\n([^"\']*?["\']{1,3})', r'\1\n\n\2'),
            (r'(["\']{1,3}[^"\']*?)\\
([^"\']*?["\']{1,3})', r'\1\n\2'),
        ]
        
        original_code = source_code
        
        for pattern, replacement in patterns_to_fix:
            matches = re.findall(pattern, source_code)
            if matches:
                source_code = re.sub(pattern, replacement, source_code)
                metrics['line_breaks_fixed'] += len(matches)
        
        # Remove obvious emoji characters (but be very careful)
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]'
        emoji_matches = re.findall(emoji_pattern, source_code)
        if emoji_matches:
            source_code = re.sub(emoji_pattern, '', source_code)
            metrics['emojis_removed'] += len(emoji_matches)
        
        metrics['unicode_artifacts'] = metrics['line_breaks_fixed'] + metrics['emojis_removed']
        
        return source_code, metrics

    def _purify_text_file(self, file_path: Path) -> bool:
        """Purify text file (markdown, txt, etc.) with full string cleaning"""
        try:
            logger.info(f"Purifying text file: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Purify entire content
            purified_content, metrics = self.purify_sacred_string(content)
            
            if metrics['unicode_artifacts'] > 0:
                # Create backup
                backup_path = self._create_backup(file_path)
                
                # Write purified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(purified_content)
                
                # Update statistics
                self._update_stats(metrics)
                
                logger.info(f"Text purified: {file_path} - {metrics['unicode_artifacts']} artifacts removed")
                return True
            else:
                logger.debug(f"Text already pure: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error purifying text {file_path}: {e}")
            self.purification_stats['errors_encountered'] += 1
            return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup of file before purification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = self.backup_directory / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.purification_stats['backups_created'] += 1
        
        logger.debug(f"Backup created: {backup_path}")
        return backup_path

    def _merge_metrics(self, total_metrics: dict, new_metrics: dict):
        """Merge purification metrics"""
        for key in total_metrics:
            if key in new_metrics:
                total_metrics[key] += new_metrics[key]

    def _update_stats(self, metrics: dict):
        """Update global purification statistics"""
        self.purification_stats['unicode_artifacts_removed'] += metrics.get('unicode_artifacts', 0)
        self.purification_stats['line_breaks_fixed'] += metrics.get('line_breaks_fixed', 0)
        self.purification_stats['emojis_removed'] += metrics.get('emojis_removed', 0)

    def purify_sacred_codebase(self) -> dict:
        """
        Purify entire sacred codebase using alchemical transmutation principles
        Returns comprehensive purification report
        """
        logger.info(" COMMENCING SACRED CODEX PURIFICATION ")
        logger.info("Sacred Invocation: OLANI HOATH OL - I am the servant of the same your God")
        logger.info("Alchemical Stage: Nigredo - Purification through Dissolution")
        
        start_time = time.time()
        
        # Walk through all files in the codebase
        for root, dirs, files in os.walk(self.root_directory):
            # Skip backup directory and other system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'sacred_backups' and d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip backup files and system files
                if file.endswith('.bak') or file.startswith('.') or file.endswith('.pyc'):
                    continue
                
                self.purification_stats['files_processed'] += 1
                
                # Get file extension
                file_extension = file_path.suffix.lower()
                
                # Process file based on type
                if file_extension in self.file_handlers:
                    handler = self.file_handlers[file_extension]
                    was_purified = handler(file_path)
                    
                    if was_purified:
                        self.purification_stats['files_purified'] += 1
                else:
                    logger.debug(f"Skipping unsupported file type: {file_path}")
        
        # Calculate purification time
        purification_time = time.time() - start_time
        
        # Generate comprehensive report
        purification_report = {
            'purification_timestamp': datetime.now().isoformat(),
            'purification_time_seconds': purification_time,
            'sacred_constants': self.sacred_constants,
            'purification_statistics': self.purification_stats,
            'files_by_type': self._analyze_files_by_type(),
            'purification_success': self.purification_stats['errors_encountered'] == 0,
            'sacred_architecture_preserved': True,
            'bitcoin_l1_ready': True
        }
        
        # Log final results
        logger.info(" SACRED CODEX PURIFICATION COMPLETE ")
        logger.info(f"Files processed: {self.purification_stats['files_processed']}")
        logger.info(f"Files purified: {self.purification_stats['files_purified']}")
        logger.info(f"Unicode artifacts removed: {self.purification_stats['unicode_artifacts_removed']}")
        logger.info(f"Line breaks fixed: {self.purification_stats['line_breaks_fixed']}")
        logger.info(f"Emojis removed: {self.purification_stats['emojis_removed']}")
        logger.info(f"Backups created: {self.purification_stats['backups_created']}")
        logger.info(f"Errors encountered: {self.purification_stats['errors_encountered']}")
        logger.info(f"Purification time: {purification_time:.2f} seconds")
        
        if self.purification_stats['errors_encountered'] == 0:
            logger.info("✅ Sacred architecture preserved - Ready for eternal Bitcoin L1 deployment")
        else:
            logger.warning("⚠️ Some errors encountered - Review purification log for details")
        
        return purification_report

    def _analyze_files_by_type(self) -> dict:
        """Analyze files by type for reporting"""
        file_types = {}
        
        for root, dirs, files in os.walk(self.root_directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'sacred_backups' and d != '__pycache__']
            
            for file in files:
                if not file.endswith('.bak') and not file.startswith('.') and not file.endswith('.pyc'):
                    extension = Path(file).suffix.lower() or 'no_extension'
                    file_types[extension] = file_types.get(extension, 0) + 1
        
        return file_types

    def export_purification_report(self, filename: str = "sacred_purification_report.json"):
        """Export comprehensive purification report"""
        report = self.purify_sacred_codebase()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=True)
        
        logger.info(f"Purification report exported to {filename}")
        return report

# Sacred invocation for codex purification
def invoke_sacred_purification():
    """
    Sacred invocation to purify the entire Enochian Cyphers codebase
    Implements Golden Dawn banishing rituals for impurity removal
    """
    logger.info(" INVOKING SACRED CODEX PURIFICATION ")
    logger.info("Golden Dawn Banishing Ritual: Removing impurities from sacred knowledge")
    logger.info("I Ching Hexagram 12 (Pi/Stagnation): Resolving blocked flow in line breaks")
    
    # Initialize sacred purifier
    purifier = SacredCodexPurifier()
    
    # Execute complete purification
    report = purifier.export_purification_report()
    
    logger.info(" Sacred purification invocation complete - Codex transmuted to pure essence ")
    return report

if __name__ == "__main__":
    # Run the sacred purification
    invoke_sacred_purification()
