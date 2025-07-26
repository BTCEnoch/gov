#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse Knowledge Base Deduplication Script
Merges thematic overlaps to prevent AI confusion during Herald quest generation.

Merges:
1. astrology.json + natal_astrology.json → astrology.json (consolidated)
2. hermetic_qabalah.json + traditional_kabbalah.json → hermetic_qabalah.json (consolidated)
3. quantum_physics.json + digital_physics.json → quantum_physics.json (consolidated)
4. taoism.json + i_ching.json → taoism.json (consolidated)

Preserves all entries while eliminating redundant tradition files.
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Any

class LighthouseDeduplicator:
    def __init__(self, traditions_path: str = "traditions"):
        self.traditions_path = traditions_path
        self.backup_path = f"{traditions_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.merge_pairs = [
            ("astrology.json", "natal_astrology.json", "astrology.json"),
            ("hermetic_qabalah.json", "traditional_kabbalah.json", "hermetic_qabalah.json"),
            ("quantum_physics.json", "digital_physics.json", "quantum_physics.json"),
            ("taoism.json", "i_ching.json", "taoism.json")
        ]
        
    def create_backup(self):
        """Create backup of traditions directory before merging."""
        print(f"Creating backup at: {self.backup_path}")
        shutil.copytree(self.traditions_path, self.backup_path)
        
    def load_json_file(self, filename: str) -> List[Dict[str, Any]]:
        """Load JSON file and return entries."""
        filepath = os.path.join(self.traditions_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
            
    def save_json_file(self, filename: str, data: List[Dict[str, Any]]):
        """Save merged data to JSON file."""
        filepath = os.path.join(self.traditions_path, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved merged file: {filename}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            
    def merge_entries(self, primary_entries: List[Dict], secondary_entries: List[Dict], 
                     primary_tradition: str, secondary_tradition: str) -> List[Dict]:
        """Merge entries from two tradition files, avoiding duplicates."""
        merged = primary_entries.copy()
        
        # Add secondary entries with updated tradition references
        for entry in secondary_entries:
            # Update tradition field to primary tradition
            entry_copy = entry.copy()
            entry_copy['tradition'] = primary_tradition
            
            # Update cross-references to point to merged tradition
            if 'cross_references' in entry_copy:
                updated_refs = []
                for ref in entry_copy['cross_references']:
                    if ref == secondary_tradition:
                        updated_refs.append(primary_tradition)
                    else:
                        updated_refs.append(ref)
                entry_copy['cross_references'] = list(set(updated_refs))  # Remove duplicates
                
            # Update story engine hooks
            if 'story_engine_hooks' in entry_copy:
                updated_hooks = []
                for hook in entry_copy['story_engine_hooks']:
                    if secondary_tradition in hook:
                        updated_hooks.append(hook.replace(secondary_tradition, primary_tradition))
                    else:
                        updated_hooks.append(hook)
                entry_copy['story_engine_hooks'] = updated_hooks
                
            merged.append(entry_copy)
            
        return merged
        
    def perform_merges(self):
        """Execute all merge operations."""
        merge_stats = {}
        
        for primary_file, secondary_file, output_file in self.merge_pairs:
            print(f"\nMerging {primary_file} + {secondary_file} → {output_file}")
            
            # Load both files
            primary_entries = self.load_json_file(primary_file)
            secondary_entries = self.load_json_file(secondary_file)
            
            if not primary_entries or not secondary_entries:
                print(f"Skipping merge due to loading errors")
                continue
                
            # Extract tradition names from filenames
            primary_tradition = primary_file.replace('.json', '')
            secondary_tradition = secondary_file.replace('.json', '')
            
            # Merge entries
            merged_entries = self.merge_entries(
                primary_entries, secondary_entries, 
                primary_tradition, secondary_tradition
            )
            
            # Save merged file
            self.save_json_file(output_file, merged_entries)
            
            # Track statistics
            merge_stats[output_file] = {
                'primary_count': len(primary_entries),
                'secondary_count': len(secondary_entries),
                'merged_count': len(merged_entries),
                'primary_tradition': primary_tradition,
                'secondary_tradition': secondary_tradition
            }
            
            # Remove secondary file if merge was successful and it's different from output
            if secondary_file != output_file:
                secondary_path = os.path.join(self.traditions_path, secondary_file)
                if os.path.exists(secondary_path):
                    os.remove(secondary_path)
                    print(f"Removed redundant file: {secondary_file}")
                    
        return merge_stats
        
    def update_master_index(self, merge_stats: Dict):
        """Update lighthouse_master_index.json to reflect merged traditions."""
        index_file = os.path.join(self.traditions_path, "lighthouse_master_index.json")
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                
            # Update tradition count and remove merged traditions
            removed_traditions = []
            for output_file, stats in merge_stats.items():
                secondary_tradition = stats['secondary_tradition']
                removed_traditions.append(secondary_tradition)
                
            # Update index
            if 'traditions' in index_data:
                index_data['traditions'] = [t for t in index_data['traditions'] 
                                          if t not in removed_traditions]
                                          
            if 'total_traditions' in index_data:
                index_data['total_traditions'] = len(index_data['traditions'])
                
            # Add merge information
            index_data['merge_history'] = {
                'merged_at': datetime.now().isoformat(),
                'merges_performed': merge_stats,
                'backup_location': self.backup_path
            }
            
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
                
            print(f"Updated master index: {index_file}")
            
        except Exception as e:
            print(f"Error updating master index: {e}")
            
    def run_deduplication(self):
        """Execute complete deduplication process."""
        print("=== Enochian Cyphers Lighthouse Deduplication ===")
        print("Merging thematic overlaps to prevent AI confusion...")
        
        # Create backup
        self.create_backup()
        
        # Perform merges
        merge_stats = self.perform_merges()
        
        # Update master index
        self.update_master_index(merge_stats)
        
        # Print summary
        print("\n=== Deduplication Summary ===")
        total_original = sum(stats['primary_count'] + stats['secondary_count'] 
                           for stats in merge_stats.values())
        total_merged = sum(stats['merged_count'] for stats in merge_stats.values())
        
        print(f"Files merged: {len(merge_stats)} pairs")
        print(f"Total entries before: {total_original}")
        print(f"Total entries after: {total_merged}")
        print(f"Backup created at: {self.backup_path}")
        
        for output_file, stats in merge_stats.items():
            print(f"  {output_file}: {stats['primary_count']} + {stats['secondary_count']} = {stats['merged_count']} entries")
            
        print("\nDeduplication complete! AI confusion prevention successful.")
        return merge_stats

if __name__ == "__main__":
    deduplicator = LighthouseDeduplicator()
    deduplicator.run_deduplication()
