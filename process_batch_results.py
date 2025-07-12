#!/usr/bin/env python3
"""
Process Optimized Batch Interview Results
Updates governor profiles with AI-generated visual aspects from batch processing
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchResultsProcessor:
    """Process batch interview results and update governor profiles"""
    
    def __init__(self, results_dir: str = "data/batch_interview_results", profiles_dir: str = "core/governors/profiles"):
        self.results_dir = Path(results_dir)
        self.profiles_dir = Path(profiles_dir)
        
    def find_latest_batch_results(self) -> Optional[Path]:
        """Find the most recent batch results file"""
        batch_files = list(self.results_dir.glob("batch_results_*.json"))
        if not batch_files:
            return None
        
        # Sort by modification time, return most recent
        latest_file = max(batch_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"📁 Found latest batch results: {latest_file}")
        return latest_file
    
    def load_batch_results(self, results_file: Optional[Path] = None) -> Dict[str, Any]:
        """Load batch results from file"""
        if results_file is None:
            results_file = self.find_latest_batch_results()
            
        if results_file is None or not results_file.exists():
            logger.error(f"❌ Batch results file not found: {results_file}")
            return {}
        
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
                
            logger.info(f"📊 Loaded batch results:")
            logger.info(f"  ✅ Successful: {results['metadata']['successful_count']}")
            logger.info(f"  ❌ Failed: {results['metadata']['failed_count']}")
            logger.info(f"  🤖 Model: {results['metadata']['model']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to load batch results: {e}")
            return {}
    
    def extract_governor_name_from_custom_id(self, custom_id: str) -> str:
        """Extract governor name from custom_id format: gov-001-OCCODON"""
        parts = custom_id.split('-')
        if len(parts) >= 3:
            return parts[2]  # Governor name is the third part
        return custom_id
    
    def update_governor_profile(self, governor_name: str, visual_aspects: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Update a single governor profile with batch results"""
        profile_file = self.profiles_dir / f"{governor_name}.json"
        
        if not profile_file.exists():
            logger.error(f"❌ Profile file not found: {profile_file}")
            return False
        
        try:
            # Load existing profile
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Update with AI-generated visual aspects
            profile_data["visual_aspects"] = visual_aspects
            
            # Add batch generation metadata
            profile_data["ai_generation_metadata"] = {
                "generated_by": "anthropic_batch_api",
                "batch_id": metadata.get("batch_id"),
                "timestamp": metadata.get("timestamp"),
                "model_used": metadata.get("model"),
                "generation_method": "optimized_batch_interview",
                "cost_optimized": True,
                "prompt_caching_used": True
            }
            
            # Save updated profile
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Updated profile for {governor_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update profile for {governor_name}: {e}")
            return False
    
    def process_all_results(self, results_file: Optional[Path] = None) -> Dict[str, int]:
        """Process all batch results and update governor profiles"""
        results = self.load_batch_results(results_file)
        
        if not results:
            logger.error("❌ No batch results to process!")
            return {"updated": 0, "failed": 0, "skipped": 0}
        
        successful_results = results.get("successful", {})
        metadata = results.get("metadata", {})
        
        stats = {"updated": 0, "failed": 0, "skipped": 0}
        
        logger.info(f"🔄 Processing {len(successful_results)} successful results...")
        
        for custom_id, result_data in successful_results.items():
            governor_name = self.extract_governor_name_from_custom_id(custom_id)
            visual_aspects = result_data.get("visual_aspects", {})
            
            if not visual_aspects:
                logger.warning(f"⚠️  No visual aspects found for {governor_name}")
                stats["skipped"] += 1
                continue
            
            if self.update_governor_profile(governor_name, visual_aspects, metadata):
                stats["updated"] += 1
            else:
                stats["failed"] += 1
        
        # Report failed results
        failed_results = results.get("failed", {})
        if failed_results:
            logger.warning(f"⚠️  {len(failed_results)} governors had failed interviews:")
            for custom_id, error_info in failed_results.items():
                governor_name = self.extract_governor_name_from_custom_id(custom_id)
                logger.warning(f"  ❌ {governor_name}: {error_info.get('error', 'Unknown error')}")
        
        return stats
    
    def create_visual_analysis_report(self, results_file: Optional[Path] = None) -> Dict[str, Any]:
        """Create detailed analysis of generated visual aspects"""
        results = self.load_batch_results(results_file)
        
        if not results:
            return {}
        
        successful_results = results.get("successful", {})
        analysis = {
            "total_governors": len(successful_results),
            "visual_categories_analysis": {
                "form_types": {},
                "primary_colors": {},
                "geometry_patterns": {},
                "energy_types": {},
                "temporal_cycles": {},
                "special_properties": {}
            },
            "element_distribution": {},
            "aethyr_distribution": {},
            "quality_metrics": {
                "avg_reasoning_length": 0,
                "governors_with_complete_data": 0,
                "unique_form_types": 0,
                "unique_color_combinations": 0
            },
            "cost_analysis": {
                "model_used": results["metadata"].get("model"),
                "batch_id": results["metadata"].get("batch_id"),
                "estimated_savings": "~50% vs individual API calls",
                "prompt_caching_benefit": "30-90% token reduction on shared knowledge"
            }
        }
        
        reasoning_lengths = []
        complete_data_count = 0
        
        for custom_id, result_data in successful_results.items():
            visual_aspects = result_data.get("visual_aspects", {})
            
            if not visual_aspects:
                continue
            
            # Check for complete data
            required_fields = ["form", "color", "geometry", "environment", "time_variations", "energy_signature"]
            if all(field in visual_aspects for field in required_fields):
                complete_data_count += 1
            
            # Analyze form types
            form_name = visual_aspects.get("form", {}).get("name", "unknown")
            analysis["visual_categories_analysis"]["form_types"][form_name] = \
                analysis["visual_categories_analysis"]["form_types"].get(form_name, 0) + 1
            
            # Analyze colors
            color_data = visual_aspects.get("color", {})
            primary_color = color_data.get("primary", "unknown")
            analysis["visual_categories_analysis"]["primary_colors"][primary_color] = \
                analysis["visual_categories_analysis"]["primary_colors"].get(primary_color, 0) + 1
            
            # Analyze geometry patterns
            geometry_patterns = visual_aspects.get("geometry", {}).get("patterns", [])
            for pattern in geometry_patterns:
                analysis["visual_categories_analysis"]["geometry_patterns"][pattern] = \
                    analysis["visual_categories_analysis"]["geometry_patterns"].get(pattern, 0) + 1
            
            # Analyze energy types
            energy_type = visual_aspects.get("energy_signature", {}).get("type", "unknown")
            analysis["visual_categories_analysis"]["energy_types"][energy_type] = \
                analysis["visual_categories_analysis"]["energy_types"].get(energy_type, 0) + 1
            
            # Analyze temporal cycles
            temporal_cycle = visual_aspects.get("time_variations", {}).get("cycle", "unknown")
            analysis["visual_categories_analysis"]["temporal_cycles"][temporal_cycle] = \
                analysis["visual_categories_analysis"]["temporal_cycles"].get(temporal_cycle, 0) + 1
            
            # Analyze special properties
            special_props = visual_aspects.get("special_properties", {}).get("properties", [])
            for prop in special_props:
                analysis["visual_categories_analysis"]["special_properties"][prop] = \
                    analysis["visual_categories_analysis"]["special_properties"].get(prop, 0) + 1
            
            # Collect reasoning lengths for quality metrics
            for category in visual_aspects.values():
                if isinstance(category, dict) and "reasoning" in category:
                    reasoning_lengths.append(len(category["reasoning"]))
        
        # Calculate quality metrics
        if reasoning_lengths:
            analysis["quality_metrics"]["avg_reasoning_length"] = sum(reasoning_lengths) / len(reasoning_lengths)
        
        analysis["quality_metrics"]["governors_with_complete_data"] = complete_data_count
        analysis["quality_metrics"]["unique_form_types"] = len(analysis["visual_categories_analysis"]["form_types"])
        analysis["quality_metrics"]["unique_color_combinations"] = len(analysis["visual_categories_analysis"]["primary_colors"])
        
        # Save analysis report
        report_file = self.results_dir / "visual_analysis_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Visual analysis report saved to {report_file}")
        return analysis

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Process optimized batch interview results")
    
    parser.add_argument(
        "--results-file",
        type=str,
        help="Specific batch results file to process (default: latest)"
    )
    
    parser.add_argument(
        "--results-dir",
        type=str,
        default="data/batch_interview_results",
        help="Directory containing batch results"
    )
    
    parser.add_argument(
        "--profiles-dir",
        type=str,
        default="core/governors/profiles",
        help="Directory containing governor profiles to update"
    )
    
    parser.add_argument(
        "--analysis-only",
        action="store_true",
        help="Only generate analysis report, don't update profiles"
    )
    
    args = parser.parse_args()
    
    logger.info("🔄 Batch Results Processor")
    logger.info("=" * 40)
    
    processor = BatchResultsProcessor(args.results_dir, args.profiles_dir)
    
    results_file = Path(args.results_file) if args.results_file else None
    
    if args.analysis_only:
        logger.info("📊 Generating analysis report only...")
        analysis = processor.create_visual_analysis_report(results_file)
        logger.info(f"✅ Analysis complete - {analysis.get('total_governors', 0)} governors analyzed")
    else:
        # Process all results and update profiles
        stats = processor.process_all_results(results_file)
        
        # Generate analysis report
        analysis = processor.create_visual_analysis_report(results_file)
        
        # Print final results
        logger.info("🎉 Batch Results Processing Complete!")
        logger.info(f"✅ Updated: {stats['updated']}")
        logger.info(f"❌ Failed: {stats['failed']}")
        logger.info(f"⚠️  Skipped: {stats['skipped']}")
        logger.info(f"📊 Analysis: {analysis.get('total_governors', 0)} governors analyzed")
        logger.info(f"💰 Cost optimized with ~50% savings via batch API")

if __name__ == "__main__":
    main()
