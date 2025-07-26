#!/usr/bin/env python3
"""
Final Linebreak Fixer
Specifically targets literal \n characters in JSON string values
"""

import json
import shutil
from datetime import datetime

def fix_literal_newlines_in_file(file_path):
    """Fix literal \n characters in JSON string values"""
    print(f"Processing {file_path}...")
    
    # Create backup
    backup_path = f"{file_path}.final_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")
    
    # Read and parse JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Function to fix literal \n in strings
    def fix_literal_newlines(obj):
        if isinstance(obj, dict):
            return {key: fix_literal_newlines(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [fix_literal_newlines(item) for item in obj]
        elif isinstance(obj, str):
            # Only replace if it contains literal \n (not actual newlines)
            if '\\n' in obj and '\n' not in obj:
                fixed = obj.replace('\\n', '\n')
                print(f"Fixed string with {obj.count('\\n')} literal newlines")
                return fixed
            return obj
        else:
            return obj
    
    # Fix the data
    fixed_data = fix_literal_newlines(data)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed {file_path}")
    return True

def main():
    """Fix the specific files with literal \n issues"""
    files_to_check = [
        "governor_ai_embodiments.json",
        "governor_agent_prompts.json"
    ]
    
    print("🔧 Final Linebreak Fixer")
    print("=" * 40)
    
    for file_path in files_to_check:
        try:
            # Test if file has literal \n issues
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check a sample string for literal \n
            sample_found = False
            for key, value in data.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, str) and '\\n' in subvalue and '\n' not in subvalue:
                            print(f"Found literal \\n in {file_path} - {key}.{subkey}")
                            sample_found = True
                            break
                if sample_found:
                    break
            
            if sample_found:
                fix_literal_newlines_in_file(file_path)
            else:
                print(f"✅ {file_path} already has proper newlines")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
        
        print("-" * 40)
    
    print("🎉 Final linebreak fixing complete!")

if __name__ == "__main__":
    main()
