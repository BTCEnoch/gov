#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse Cleanup Script
Removes redundant directories and files that could cause AI confusion.

This script removes:
1. complete_lighthouse/ directory (contains old unmerged tradition files)
2. migrate_lighthouse/ directory (empty directory)
3. Any __pycache__ directories
4. Any other redundant backup or duplicate directories

Preserves the main traditions/ directory with merged files.
"""

import os
import shutil
from datetime import datetime
from typing import List

class LighthouseCleanup:
    def __init__(self, lighthouse_path: str = "."):
        self.lighthouse_path = lighthouse_path
        self.cleanup_log = []
        
    def log_action(self, action: str):
        """Log cleanup actions."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        self.cleanup_log.append(log_entry)
        print(log_entry)
        
    def remove_directory(self, dir_path: str, reason: str):
        """Safely remove a directory and log the action."""
        full_path = os.path.join(self.lighthouse_path, dir_path)
        if os.path.exists(full_path):
            try:
                shutil.rmtree(full_path)
                self.log_action(f"REMOVED: {dir_path} - {reason}")
                return True
            except Exception as e:
                self.log_action(f"ERROR removing {dir_path}: {e}")
                return False
        else:
            self.log_action(f"SKIP: {dir_path} - Directory not found")
            return False
            
    def remove_file(self, file_path: str, reason: str):
        """Safely remove a file and log the action."""
        full_path = os.path.join(self.lighthouse_path, file_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                self.log_action(f"REMOVED: {file_path} - {reason}")
                return True
            except Exception as e:
                self.log_action(f"ERROR removing {file_path}: {e}")
                return False
        else:
            self.log_action(f"SKIP: {file_path} - File not found")
            return False
            
    def cleanup_redundant_directories(self):
        """Remove redundant directories that could cause AI confusion."""
        redundant_dirs = [
            ("complete_lighthouse", "Contains old unmerged tradition files with redundancies"),
            ("migrate_lighthouse", "Empty directory serving no purpose"),
            ("__pycache__", "Python cache directory not needed for production"),
        ]
        
        removed_count = 0
        for dir_name, reason in redundant_dirs:
            if self.remove_directory(dir_name, reason):
                removed_count += 1
                
        return removed_count
        
    def cleanup_backup_directories(self):
        """Remove old backup directories (keep only the most recent)."""
        backup_dirs = []
        
        # Find all backup directories
        for item in os.listdir(self.lighthouse_path):
            if item.startswith("traditions_backup_"):
                backup_dirs.append(item)
                
        # Sort by creation time (newest first)
        backup_dirs.sort(reverse=True)
        
        # Keep only the most recent backup, remove others
        removed_count = 0
        if len(backup_dirs) > 1:
            for old_backup in backup_dirs[1:]:  # Skip the first (newest) backup
                if self.remove_directory(old_backup, "Old backup directory (keeping only most recent)"):
                    removed_count += 1
                    
        if backup_dirs:
            self.log_action(f"KEPT: {backup_dirs[0]} - Most recent backup preserved")
            
        return removed_count
        
    def cleanup_temporary_files(self):
        """Remove temporary files that might cause confusion."""
        temp_patterns = [
            "*.tmp",
            "*.temp", 
            "*.bak",
            ".DS_Store",
            "Thumbs.db"
        ]
        
        removed_count = 0
        for root, dirs, files in os.walk(self.lighthouse_path):
            for file in files:
                for pattern in temp_patterns:
                    if file.endswith(pattern.replace("*", "")):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.lighthouse_path)
                        if self.remove_file(rel_path, f"Temporary file matching pattern {pattern}"):
                            removed_count += 1
                            
        return removed_count
        
    def verify_essential_files(self):
        """Verify that essential files are still present after cleanup."""
        essential_files = [
            "traditions/lighthouse_master_index.json",
            "traditions/enochian_magic.json",
            "traditions/hermetic_qabalah.json",
            "traditions/astrology.json",
            "traditions/taoism.json",
            "traditions/quantum_physics.json"
        ]
        
        missing_files = []
        for file_path in essential_files:
            full_path = os.path.join(self.lighthouse_path, file_path)
            if not os.path.exists(full_path):
                missing_files.append(file_path)
                
        if missing_files:
            self.log_action(f"WARNING: Missing essential files: {missing_files}")
            return False
        else:
            self.log_action("VERIFIED: All essential files present after cleanup")
            return True
            
    def generate_cleanup_report(self):
        """Generate a cleanup report."""
        report_path = os.path.join(self.lighthouse_path, "cleanup_report.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Enochian Cyphers Lighthouse Cleanup Report\n")
            f.write("=" * 50 + "\n\n")
            
            for log_entry in self.cleanup_log:
                f.write(log_entry + "\n")
                
            f.write(f"\nCleanup completed at: {datetime.now().isoformat()}\n")
            f.write("Purpose: Remove redundant files to prevent AI confusion during Herald development\n")
            
        self.log_action(f"CREATED: cleanup_report.txt - Detailed cleanup log")
        
    def run_cleanup(self):
        """Execute complete cleanup process."""
        print("=== Enochian Cyphers Lighthouse Cleanup ===")
        print("Removing redundant files to prevent AI confusion...")
        
        # Track cleanup statistics
        total_removed = 0
        
        # Cleanup redundant directories
        self.log_action("Starting redundant directory cleanup...")
        total_removed += self.cleanup_redundant_directories()
        
        # Cleanup old backups (keep most recent)
        self.log_action("Starting backup directory cleanup...")
        total_removed += self.cleanup_backup_directories()
        
        # Cleanup temporary files
        self.log_action("Starting temporary file cleanup...")
        total_removed += self.cleanup_temporary_files()
        
        # Verify essential files
        self.log_action("Verifying essential files...")
        verification_passed = self.verify_essential_files()
        
        # Generate report
        self.generate_cleanup_report()
        
        # Print summary
        print("\n=== Cleanup Summary ===")
        print(f"Total items removed: {total_removed}")
        print(f"Essential files verification: {'PASSED' if verification_passed else 'FAILED'}")
        print("Cleanup report saved to: cleanup_report.txt")
        
        if verification_passed:
            print("\n✅ Cleanup successful! AI confusion prevention complete.")
            print("The lighthouse knowledge base is now optimized for Herald development.")
        else:
            print("\n❌ Cleanup completed with warnings. Check cleanup_report.txt for details.")
            
        return total_removed, verification_passed

if __name__ == "__main__":
    cleanup = LighthouseCleanup()
    cleanup.run_cleanup()
