#!/usr/bin/env python3
"""
CLI tool for batch processing governor visual aspects through interviews
"""

import asyncio
import argparse
import logging
from pathlib import Path
import sys
import json
from typing import Optional

from .batch_interview_processor import BatchInterviewProcessor
from ...generator import GovernorProfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Batch process governor visual aspects through interviews"
    )
    
    parser.add_argument(
        "--profiles-dir",
        type=str,
        required=True,
        help="Directory containing governor profile JSON files"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save generated visual aspects"
    )
    
    parser.add_argument(
        "--knowledge-base",
        type=str,
        required=True,
        help="Path to knowledge base directory"
    )
    
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=5,
        help="Maximum number of concurrent interviews (default: 5)"
    )
    
    parser.add_argument(
        "--governor-filter",
        type=str,
        help="Optional comma-separated list of governor IDs to process"
    )
    
    return parser.parse_args()

async def process_governors(args) -> bool:
    """
    Process governors through the interview system
    Returns True if successful, False otherwise
    """
    try:
        # Initialize processor
        processor = BatchInterviewProcessor(
            args.knowledge_base,
            max_concurrent=args.max_concurrent
        )
        
        # Load governor profiles
        logger.info("Loading governor profiles from %s", args.profiles_dir)
        all_governors = processor.load_governor_profiles(args.profiles_dir)
        
        if not all_governors:
            logger.error("No governor profiles found in %s", args.profiles_dir)
            return False
            
        # Filter governors if specified
        governors = all_governors
        if args.governor_filter:
            governor_ids = set(args.governor_filter.split(","))
            governors = [g for g in all_governors if g.id in governor_ids]
            logger.info(
                "Filtered to %d governors from filter list: %s",
                len(governors),
                args.governor_filter
            )
            
        if not governors:
            logger.error("No governors to process after filtering")
            return False
            
        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Process governors
        logger.info("Processing %d governors...", len(governors))
        results = await processor.process_interviews(governors)
        
        # Save results
        logger.info("Saving results to %s", args.output_dir)
        processor.save_results(results, args.output_dir)
        
        # Generate summary
        summary = {
            "total_governors": len(governors),
            "processed": len(results),
            "success_rate": len(results) / len(governors) * 100,
            "processed_governors": sorted(results.keys())
        }
        
        summary_path = output_path / "processing_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
            
        logger.info("Processing complete! Summary saved to %s", summary_path)
        logger.info("Processed %d/%d governors (%.1f%%)",
                   len(results), len(governors),
                   summary["success_rate"])
                   
        return True
        
    except Exception as e:
        logger.error("Failed to process governors: %s", e, exc_info=True)
        return False

def main():
    """Main entry point"""
    args = parse_args()
    
    try:
        success = asyncio.run(process_governors(args))
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 