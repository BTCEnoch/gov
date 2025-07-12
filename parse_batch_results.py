#!/usr/bin/env python3
"""
Parse Anthropic Batch Results JSONL File
Extracts visual aspects from batch API results and updates governor profiles
Handles unicode cleaning to ensure ASCII-only output
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import unicodedata

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchResultsParser:
    """Parse batch results and update governor profiles with unicode cleaning"""
    
    def __init__(self, jsonl_file: str, profiles_dir: str = "core/governors/profiles"):
        self.jsonl_file = Path(jsonl_file)
        self.profiles_dir = Path(profiles_dir)
        
        # Unicode replacement mappings for common characters
        self.unicode_replacements = {
            # Quotes and apostrophes
            '"': '"',  # Left double quotation mark
            '"': '"',  # Right double quotation mark
            ''': "'",  # Left single quotation mark
            ''': "'",  # Right single quotation mark
            '`': "'",  # Grave accent
            '´': "'",  # Acute accent
            
            # Dashes and hyphens
            '–': '-',  # En dash
            '—': '-',  # Em dash
            '−': '-',  # Minus sign
            
            # Other common unicode
            '…': '...',  # Horizontal ellipsis
            '•': '*',    # Bullet
            '·': '*',    # Middle dot
            '°': ' degrees',  # Degree symbol
            '™': 'TM',   # Trademark
            '©': '(c)',  # Copyright
            '®': '(R)',  # Registered trademark
            
            # Mathematical symbols
            '×': 'x',    # Multiplication sign
            '÷': '/',    # Division sign
            '±': '+/-',  # Plus-minus sign
            
            # Fractions
            '½': '1/2',
            '¼': '1/4',
            '¾': '3/4',
            
            # Currency (if any)
            '€': 'EUR',
            '£': 'GBP',
            '¥': 'YEN',
        }
    
    def clean_unicode_text(self, text: str) -> str:
        """Clean unicode characters from text, converting to ASCII equivalents"""
        if not isinstance(text, str):
            return text
        
        # First, apply specific replacements
        cleaned = text
        for unicode_char, ascii_replacement in self.unicode_replacements.items():
            cleaned = cleaned.replace(unicode_char, ascii_replacement)
        
        # Then, normalize any remaining unicode to ASCII
        # This will convert accented characters to their base forms
        cleaned = unicodedata.normalize('NFKD', cleaned)
        cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
        
        return cleaned
    
    def clean_unicode_recursive(self, obj: Any) -> Any:
        """Recursively clean unicode from nested data structures"""
        if isinstance(obj, str):
            return self.clean_unicode_text(obj)
        elif isinstance(obj, dict):
            return {key: self.clean_unicode_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_unicode_recursive(item) for item in obj]
        else:
            return obj
    
    def extract_governor_name_from_custom_id(self, custom_id: str) -> str:
        """Extract governor name from custom_id format: gov-XXX-GOVERNORNAME"""
        parts = custom_id.split('-')
        if len(parts) >= 3:
            return parts[2]  # Governor name is the third part
        else:
            logger.error(f"Invalid custom_id format: {custom_id}")
            return custom_id
    
    def parse_visual_aspects_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse visual aspects JSON from the text field"""
        try:
            # Find JSON in the text (it should be the entire text, but let's be safe)
            text = text.strip()
            
            # Look for JSON boundaries
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = text[json_start:json_end]
                
                # Parse the JSON
                visual_data = json.loads(json_text)
                
                # Extract visual_aspects if it's nested
                if "visual_aspects" in visual_data:
                    return visual_data["visual_aspects"]
                else:
                    return visual_data
            else:
                logger.error("No valid JSON boundaries found in text")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Problematic text: {text[:200]}...")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing visual aspects: {e}")
            return None
    
    def parse_single_result(self, line: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Parse a single line from the JSONL file"""
        try:
            # Parse the line as JSON
            result_data = json.loads(line.strip())
            
            # Extract custom_id
            custom_id = result_data.get("custom_id", "")
            governor_name = self.extract_governor_name_from_custom_id(custom_id)
            
            # Check if result was successful
            result = result_data.get("result", {})
            if result.get("type") != "succeeded":
                logger.error(f"Result not successful for {governor_name}: {result.get('type')}")
                return None
            
            # Extract the text content
            message = result.get("message", {})
            content = message.get("content", [])
            
            if not content or len(content) == 0:
                logger.error(f"No content found for {governor_name}")
                return None
            
            text_content = content[0].get("text", "")
            
            # Parse visual aspects from the text
            visual_aspects = self.parse_visual_aspects_from_text(text_content)
            
            if visual_aspects is None:
                logger.error(f"Failed to parse visual aspects for {governor_name}")
                return None
            
            # Clean unicode from the visual aspects
            cleaned_visual_aspects = self.clean_unicode_recursive(visual_aspects)
            
            logger.info(f"✅ Parsed visual aspects for {governor_name}")
            return governor_name, cleaned_visual_aspects
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON line: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing line: {e}")
            return None
    
    def update_governor_profile(self, governor_name: str, visual_aspects: Dict[str, Any]) -> bool:
        """Update a governor profile with the parsed visual aspects"""
        profile_file = self.profiles_dir / f"{governor_name}.json"
        
        if not profile_file.exists():
            logger.error(f"❌ Profile file not found: {profile_file}")
            return False
        
        try:
            # Load existing profile
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Update visual aspects
            profile_data["visual_aspects"] = visual_aspects
            
            # Add metadata about the batch processing
            profile_data["ai_generation_metadata"] = {
                "generated_by": "anthropic_batch_api",
                "timestamp": "2025-01-11T20:00:00Z",
                "model_used": "claude-3-5-haiku-20241022",
                "generation_method": "optimized_batch_interview",
                "unicode_cleaned": True,
                "cost_optimized": True,
                "prompt_caching_used": True
            }
            
            # Save updated profile (ensure ASCII encoding)
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=True)
            
            logger.info(f"✅ Updated profile for {governor_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update profile for {governor_name}: {e}")
            return False
    
    def parse_all_results(self) -> Dict[str, int]:
        """Parse all results from the JSONL file and update profiles"""
        if not self.jsonl_file.exists():
            logger.error(f"❌ JSONL file not found: {self.jsonl_file}")
            return {"parsed": 0, "updated": 0, "failed": 0}
        
        stats = {"parsed": 0, "updated": 0, "failed": 0}
        
        logger.info(f"🔄 Parsing batch results from {self.jsonl_file}")
        
        try:
            with open(self.jsonl_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    
                    logger.info(f"📝 Processing line {line_num}...")
                    
                    # Parse the line
                    result = self.parse_single_result(line)
                    
                    if result is None:
                        stats["failed"] += 1
                        continue
                    
                    governor_name, visual_aspects = result
                    stats["parsed"] += 1
                    
                    # Update the profile
                    if self.update_governor_profile(governor_name, visual_aspects):
                        stats["updated"] += 1
                    else:
                        stats["failed"] += 1
        
        except Exception as e:
            logger.error(f"❌ Error reading JSONL file: {e}")
        
        return stats
    
    def create_summary_report(self, stats: Dict[str, int]) -> Dict[str, Any]:
        """Create a summary report of the parsing process"""
        summary = {
            "parsing_summary": {
                "total_lines_processed": stats["parsed"] + stats["failed"],
                "successfully_parsed": stats["parsed"],
                "profiles_updated": stats["updated"],
                "failed_operations": stats["failed"],
                "success_rate": f"{(stats['updated'] / max(stats['parsed'], 1)) * 100:.1f}%"
            },
            "unicode_cleaning": {
                "enabled": True,
                "replacements_applied": len(self.unicode_replacements),
                "ascii_encoding": True
            },
            "file_info": {
                "source_file": str(self.jsonl_file),
                "profiles_directory": str(self.profiles_dir),
                "total_governors": 91
            }
        }
        
        # Save summary
        summary_file = self.profiles_dir.parent / "batch_parsing_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=True)
        
        logger.info(f"📊 Summary report saved to {summary_file}")
        return summary

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Parse Anthropic batch results JSONL file")
    parser.add_argument("jsonl_file", help="Path to the JSONL results file")
    parser.add_argument("--profiles-dir", default="core/governors/profiles", help="Directory containing governor profiles")
    
    args = parser.parse_args()
    
    logger.info("🔄 Batch Results Parser")
    logger.info("=" * 40)
    
    # Initialize parser
    parser_instance = BatchResultsParser(args.jsonl_file, args.profiles_dir)
    
    # Parse all results
    stats = parser_instance.parse_all_results()
    
    # Create summary report
    summary = parser_instance.create_summary_report(stats)
    
    # Print final results
    logger.info("🎉 Batch Results Parsing Complete!")
    logger.info(f"📊 Parsed: {stats['parsed']}")
    logger.info(f"✅ Updated: {stats['updated']}")
    logger.info(f"❌ Failed: {stats['failed']}")
    logger.info(f"📈 Success Rate: {summary['parsing_summary']['success_rate']}")
    logger.info("🧹 Unicode cleaned and ASCII-encoded")

if __name__ == "__main__":
    main()
