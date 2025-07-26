#!/usr/bin/env python3
"""
Direct JSON Linebreak Fixer
Specifically targets the \n issues in governor JSON files

This script directly processes the problematic JSON files and converts
literal \n characters to actual linebreaks in the JSON string values.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

def fix_json_file(file_path):
    """Fix linebreaks in a specific JSON file"""
    print(f"Processing {file_path}...")
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")
    
    # Read the file as text first
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original \n occurrences
    original_count = content.count('\\n')
    print(f"Found {original_count} literal \\n sequences")
    
    # Parse as JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False
    
    # Function to recursively fix strings
    def fix_strings(obj):
        if isinstance(obj, dict):
            return {key: fix_strings(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [fix_strings(item) for item in obj]
        elif isinstance(obj, str):
            # Replace literal \n with actual newlines
            return obj.replace('\\n', '\n')
        else:
            return obj
    
    # Fix all strings in the data
    fixed_data = fix_strings(data)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    # Verify the fix
    with open(file_path, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    new_count = new_content.count('\\n')
    print(f"After fix: {new_count} literal \\n sequences remaining")
    print(f"Fixed {original_count - new_count} linebreak issues")
    
    return True

def main():
    """Fix the specific problematic files"""
    files_to_fix = [
        "governor_agent_prompts.json",
        "governor_ai_embodiments.json", 
        "governor_interview_integration.json"
    ]
    
    print("🔧 Direct JSON Linebreak Fixer")
    print("=" * 40)
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            success = fix_json_file(file_path)
            if success:
                print(f"✅ Successfully fixed {file_path}")
            else:
                print(f"❌ Failed to fix {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")
        print("-" * 40)
    
    print("🎉 Direct linebreak fixing complete!")

if __name__ == "__main__":
    main()
