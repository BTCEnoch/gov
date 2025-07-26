#!/usr/bin/env python3
"""
Enochian Cyphers JSON Linebreak Cleaner
Fixes \n\n linebreak issues in JSON files by converting them to proper linebreaks

This script:
1. Scans all JSON files in the project
2. Identifies files with \n\n literal strings that should be linebreaks
3. Converts \n\n to actual linebreaks for proper formatting
4. Preserves JSON structure and validity
5. Creates backups before modification
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Union
import re

class JSONLinebreakCleaner:
    """Cleans up linebreak formatting issues in JSON files"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.cleaned_files = []
        self.backup_dir = Path("json_cleanup_backups")
        self.cleanup_log = []
        
    def log_action(self, message: str):
        """Log cleanup actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.cleanup_log.append(log_entry)
        print(log_entry)
    
    def create_backup_dir(self):
        """Create backup directory for original files"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self.log_action(f"Created backup directory: {self.backup_dir}")
    
    def find_json_files(self) -> List[Path]:
        """Find all JSON files in the project"""
        json_files = []
        
        # Scan common directories for JSON files
        scan_dirs = [
            "lighthouse/traditions",
            "governor_profiles", 
            "interviews",
            "onchain",
            "scripts",
            "docs",
            "validation",
            "generated_content"  # If it exists
        ]
        
        for scan_dir in scan_dirs:
            dir_path = self.root_path / scan_dir
            if dir_path.exists():
                json_files.extend(dir_path.rglob("*.json"))
        
        # Also check root directory
        json_files.extend(self.root_path.glob("*.json"))
        
        self.log_action(f"Found {len(json_files)} JSON files to scan")
        return json_files
    
    def needs_linebreak_cleanup(self, content: str) -> bool:
        """Check if content contains \n\n that should be converted to linebreaks"""
        # Look for literal \n\n strings (not actual newlines)
        return "\\n\\n" in content or "\\n" in content
    
    def clean_linebreaks_in_string(self, text: str) -> str:
        """Convert \n\n and \n to actual linebreaks in a string"""
        if not isinstance(text, str):
            return text
            
        # Convert literal \n\n to actual double linebreaks
        text = text.replace("\\n\\n", "\n\n")
        
        # Convert literal \n to actual linebreaks (but not if it's already a real newline)
        text = text.replace("\\n", "\n")
        
        return text
    
    def clean_json_object(self, obj: Union[Dict, List, str, Any]) -> Union[Dict, List, str, Any]:
        """Recursively clean linebreaks in JSON object"""
        if isinstance(obj, dict):
            return {key: self.clean_json_object(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_json_object(item) for item in obj]
        elif isinstance(obj, str):
            return self.clean_linebreaks_in_string(obj)
        else:
            return obj
    
    def backup_file(self, file_path: Path) -> Path:
        """Create backup of original file"""
        backup_path = self.backup_dir / f"{file_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def clean_json_file(self, file_path: Path) -> bool:
        """Clean linebreaks in a single JSON file"""
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if cleanup is needed
            if not self.needs_linebreak_cleanup(content):
                return False
            
            # Parse JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                self.log_action(f"❌ Invalid JSON in {file_path}: {e}")
                return False
            
            # Create backup
            backup_path = self.backup_file(file_path)
            self.log_action(f"📁 Backed up {file_path.name} to {backup_path.name}")
            
            # Clean linebreaks
            cleaned_data = self.clean_json_object(data)
            
            # Write cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
            
            self.log_action(f"✅ Cleaned linebreaks in {file_path}")
            self.cleaned_files.append(str(file_path))
            return True
            
        except Exception as e:
            self.log_action(f"❌ Error cleaning {file_path}: {e}")
            return False
    
    def clean_all_json_files(self) -> Dict[str, int]:
        """Clean linebreaks in all JSON files"""
        self.log_action("Starting JSON linebreak cleanup...")
        
        # Create backup directory
        self.create_backup_dir()
        
        # Find all JSON files
        json_files = self.find_json_files()
        
        # Clean each file
        stats = {
            'total_files': len(json_files),
            'cleaned_files': 0,
            'skipped_files': 0,
            'error_files': 0
        }
        
        for file_path in json_files:
            try:
                if self.clean_json_file(file_path):
                    stats['cleaned_files'] += 1
                else:
                    stats['skipped_files'] += 1
            except Exception as e:
                self.log_action(f"❌ Error processing {file_path}: {e}")
                stats['error_files'] += 1
        
        return stats
    
    def generate_cleanup_report(self) -> str:
        """Generate cleanup report"""
        report_path = "json_linebreak_cleanup_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Enochian Cyphers JSON Linebreak Cleanup Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Cleanup completed at: {datetime.now().isoformat()}\n")
            f.write(f"Purpose: Fix \\n\\n linebreak issues in JSON files\n\n")
            
            f.write("Cleanup Log:\n")
            f.write("-" * 20 + "\n")
            for log_entry in self.cleanup_log:
                f.write(log_entry + "\n")
            
            f.write(f"\nCleaned Files ({len(self.cleaned_files)}):\n")
            f.write("-" * 20 + "\n")
            for file_path in self.cleaned_files:
                f.write(f"- {file_path}\n")
        
        self.log_action(f"📄 Generated cleanup report: {report_path}")
        return report_path
    
    def run_cleanup(self) -> bool:
        """Execute complete JSON linebreak cleanup"""
        print("🧹 Enochian Cyphers JSON Linebreak Cleanup")
        print("=" * 45)
        print("Fixing \\n\\n linebreak issues in JSON files...")
        
        # Clean all files
        stats = self.clean_all_json_files()
        
        # Generate report
        report_path = self.generate_cleanup_report()
        
        # Print summary
        print("\n" + "=" * 45)
        print("📊 CLEANUP SUMMARY")
        print("=" * 45)
        print(f"Total JSON files scanned: {stats['total_files']}")
        print(f"Files cleaned: {stats['cleaned_files']}")
        print(f"Files skipped (no issues): {stats['skipped_files']}")
        print(f"Files with errors: {stats['error_files']}")
        print(f"Backup directory: {self.backup_dir}")
        print(f"Cleanup report: {report_path}")
        
        if stats['cleaned_files'] > 0:
            print(f"\n✅ Successfully cleaned {stats['cleaned_files']} JSON files!")
            print("All \\n\\n linebreak issues have been resolved.")
        else:
            print("\n✨ No linebreak issues found - all JSON files are clean!")
        
        return stats['error_files'] == 0

def main():
    """Main entry point"""
    cleaner = JSONLinebreakCleaner()
    success = cleaner.run_cleanup()
    
    if success:
        print("\n🎉 JSON linebreak cleanup completed successfully!")
    else:
        print("\n⚠️ JSON linebreak cleanup completed with some errors.")
        print("Check the cleanup report for details.")

if __name__ == "__main__":
    main()
