#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse Cleanup Verification Script
Verifies that the cleanup and deduplication was successful.

This script validates:
1. Correct number of tradition files (22 + master index)
2. No redundant files remain
3. All merged files contain expected entry counts
4. Master index reflects the changes
5. Essential directories and files are preserved
"""

import json
import os
from typing import Dict, List

class CleanupVerification:
    def __init__(self, traditions_path: str = "traditions"):
        self.traditions_path = traditions_path
        self.expected_merged_files = {
            "astrology.json": 220,  # 115 + 105
            "hermetic_qabalah.json": 235,  # 110 + 125  
            "quantum_physics.json": 195,  # 100 + 95
            "taoism.json": 200  # 110 + 90
        }
        self.removed_files = [
            "natal_astrology.json",
            "traditional_kabbalah.json", 
            "digital_physics.json",
            "i_ching.json"
        ]
        
    def verify_file_count(self) -> bool:
        """Verify we have exactly 22 tradition files + master index."""
        if not os.path.exists(self.traditions_path):
            print(f"❌ Traditions directory not found: {self.traditions_path}")
            return False
            
        files = [f for f in os.listdir(self.traditions_path) if f.endswith('.json')]
        tradition_files = [f for f in files if f != 'lighthouse_master_index.json']
        
        print(f"📁 Found {len(tradition_files)} tradition files + master index")
        
        if len(tradition_files) == 22:
            print("✅ Correct number of tradition files (22)")
            return True
        else:
            print(f"❌ Expected 22 tradition files, found {len(tradition_files)}")
            print(f"Files: {sorted(tradition_files)}")
            return False
            
    def verify_removed_files(self) -> bool:
        """Verify that redundant files were successfully removed."""
        success = True
        
        for removed_file in self.removed_files:
            file_path = os.path.join(self.traditions_path, removed_file)
            if os.path.exists(file_path):
                print(f"❌ Redundant file still exists: {removed_file}")
                success = False
            else:
                print(f"✅ Redundant file removed: {removed_file}")
                
        return success
        
    def verify_merged_files(self) -> bool:
        """Verify that merged files contain expected entry counts."""
        success = True
        
        for filename, expected_count in self.expected_merged_files.items():
            file_path = os.path.join(self.traditions_path, filename)
            
            if not os.path.exists(file_path):
                print(f"❌ Merged file missing: {filename}")
                success = False
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                actual_count = len(data)
                if actual_count == expected_count:
                    print(f"✅ {filename}: {actual_count} entries (expected {expected_count})")
                else:
                    print(f"❌ {filename}: {actual_count} entries (expected {expected_count})")
                    success = False
                    
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
                success = False
                
        return success
        
    def verify_master_index(self) -> bool:
        """Verify master index reflects the changes."""
        index_path = os.path.join(self.traditions_path, "lighthouse_master_index.json")
        
        if not os.path.exists(index_path):
            print("❌ Master index file missing")
            return False
            
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                
            # Check tradition count
            if index_data.get('total_traditions') == 22:
                print("✅ Master index shows correct tradition count (22)")
            else:
                print(f"❌ Master index shows {index_data.get('total_traditions')} traditions (expected 22)")
                return False
                
            # Check for merge history
            if 'merge_history' in index_data:
                print("✅ Master index contains merge history")
                merge_info = index_data['merge_history']
                
                if 'merges_performed' in merge_info:
                    merges = merge_info['merges_performed']
                    print(f"✅ Recorded {len(merges)} merge operations")
                    
                    for merged_file, stats in merges.items():
                        print(f"   - {merged_file}: {stats['primary_count']} + {stats['secondary_count']} = {stats['merged_count']}")
                else:
                    print("❌ Merge history missing merge details")
                    return False
            else:
                print("❌ Master index missing merge history")
                return False
                
            # Check that removed traditions are not in the list
            traditions_list = index_data.get('traditions', [])
            removed_traditions = [f.replace('.json', '') for f in self.removed_files]
            
            for removed_tradition in removed_traditions:
                if removed_tradition in traditions_list:
                    print(f"❌ Removed tradition still in master index: {removed_tradition}")
                    return False
                    
            print("✅ Removed traditions not found in master index")
            return True
            
        except Exception as e:
            print(f"❌ Error reading master index: {e}")
            return False
            
    def verify_redundant_directories_removed(self) -> bool:
        """Verify redundant directories were removed."""
        redundant_dirs = ["complete_lighthouse", "migrate_lighthouse", "__pycache__"]
        success = True
        
        for dir_name in redundant_dirs:
            if os.path.exists(dir_name):
                print(f"❌ Redundant directory still exists: {dir_name}")
                success = False
            else:
                print(f"✅ Redundant directory removed: {dir_name}")
                
        return success
        
    def verify_backup_preserved(self) -> bool:
        """Verify that backup was created and preserved."""
        backup_dirs = [d for d in os.listdir('.') if d.startswith('traditions_backup_')]
        
        if backup_dirs:
            print(f"✅ Backup preserved: {backup_dirs[0]}")
            return True
        else:
            print("❌ No backup directory found")
            return False
            
    def run_verification(self) -> bool:
        """Run complete verification process."""
        print("=== Enochian Cyphers Lighthouse Cleanup Verification ===")
        print("Verifying cleanup and deduplication success...\n")
        
        checks = [
            ("File Count", self.verify_file_count),
            ("Removed Files", self.verify_removed_files), 
            ("Merged Files", self.verify_merged_files),
            ("Master Index", self.verify_master_index),
            ("Redundant Directories", self.verify_redundant_directories_removed),
            ("Backup Preservation", self.verify_backup_preserved)
        ]
        
        results = {}
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"\n--- {check_name} Verification ---")
            result = check_func()
            results[check_name] = result
            if not result:
                all_passed = False
                
        # Print summary
        print("\n=== Verification Summary ===")
        for check_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{check_name}: {status}")
            
        if all_passed:
            print("\n🎉 All verifications PASSED!")
            print("Lighthouse knowledge base cleanup successful.")
            print("AI confusion prevention complete - ready for Herald development.")
        else:
            print("\n⚠️  Some verifications FAILED!")
            print("Please review the issues above before proceeding.")
            
        return all_passed

if __name__ == "__main__":
    verifier = CleanupVerification()
    success = verifier.run_verification()
    exit(0 if success else 1)
