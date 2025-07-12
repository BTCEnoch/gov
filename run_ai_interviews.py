#!/usr/bin/env python3
"""
CLI Runner for Enochian Cyphers AI Interview System
Provides easy command-line interface for running governor interviews
"""

import argparse
import asyncio
import sys
import os
from pathlib import Path
import logging

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ai_interview_system import GovernorAIInterviewer

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_environment():
    """Check if environment is properly configured"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not found in environment")
        print("Please ensure your .env file contains:")
        print("ANTHROPIC_API_KEY=your_api_key_here")
        return False
    
    # Check if required files exist
    required_files = [
        "core/governors/profiler/interview/templates/interview_questions.json",
        "core/governors/profiles",
        "data/knowledge/authentic_knowledge_base.json"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"⚠️  WARNING: {file_path} not found")
    
    return True

async def run_interviews(args):
    """Run the AI interview process"""
    if not check_environment():
        return False
    
    try:
        # Initialize interviewer with specified concurrency
        interviewer = GovernorAIInterviewer(max_concurrent=args.concurrent)
        
        # Load governor profiles
        profiles = interviewer.load_governor_profiles()
        
        if not profiles:
            print("❌ No governor profiles found!")
            return False
        
        # Filter governors if specified
        if args.governors:
            governor_names = set(args.governors.split(','))
            profiles = [p for p in profiles if p.get('governor_name') in governor_names]
            print(f"🎯 Filtering to {len(profiles)} specified governors")
        
        if args.limit:
            profiles = profiles[:args.limit]
            print(f"🔢 Limited to first {len(profiles)} governors")
        
        print(f"🎭 Starting interviews for {len(profiles)} governors...")
        
        # Conduct interviews
        results = await interviewer.batch_interview_governors(profiles)
        
        # Save results
        output_dir = args.output_dir or "data/ai_interview_results"
        summary = interviewer.save_results(results, output_dir)
        
        # Print final summary
        print("\n" + "="*60)
        print("🎉 AI INTERVIEW PROCESS COMPLETE!")
        print("="*60)
        print(f"✅ Successful interviews: {summary['successful_interviews']}")
        print(f"❌ Failed interviews: {summary['failed_interviews']}")
        print(f"📊 Total processed: {summary['total_interviews']}")
        print(f"💾 Results saved to: {output_dir}")
        
        if summary['failed_interviews'] > 0:
            print(f"\n⚠️  {summary['failed_interviews']} interviews failed - check logs for details")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Interview process interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Interview process failed: {e}")
        return False

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Interview System for Enochian Cyphers Governor Visual Aspects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interview all 91 governors (default)
  python run_ai_interviews.py
  
  # Interview specific governors
  python run_ai_interviews.py --governors "OCCODON,PASCOMB,VALGARS"
  
  # Interview first 5 governors only (for testing)
  python run_ai_interviews.py --limit 5
  
  # Use higher concurrency (be careful with rate limits)
  python run_ai_interviews.py --concurrent 5
  
  # Verbose logging
  python run_ai_interviews.py --verbose
        """
    )
    
    parser.add_argument(
        "--governors",
        type=str,
        help="Comma-separated list of specific governor names to interview"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of governors to interview (useful for testing)"
    )
    
    parser.add_argument(
        "--concurrent",
        type=int,
        default=3,
        help="Maximum concurrent interviews (default: 3, be careful with rate limits)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for results (default: data/ai_interview_results)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check configuration without running interviews"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    print("🎭 Enochian Cyphers AI Interview System")
    print("=" * 50)
    
    if args.dry_run:
        print("🔍 DRY RUN - Checking configuration...")
        if check_environment():
            print("✅ Environment configuration looks good!")
            
            # Load and show profile count
            interviewer = GovernorAIInterviewer(max_concurrent=1)
            profiles = interviewer.load_governor_profiles()
            print(f"📁 Found {len(profiles)} governor profiles")
            
            if args.governors:
                governor_names = set(args.governors.split(','))
                filtered = [p for p in profiles if p.get('governor_name') in governor_names]
                print(f"🎯 Would interview {len(filtered)} specified governors")
            elif args.limit:
                print(f"🔢 Would interview first {min(args.limit, len(profiles))} governors")
            else:
                print(f"🎭 Would interview all {len(profiles)} governors")
                
            print("🚀 Ready to run interviews!")
        else:
            print("❌ Configuration issues found - please fix before running")
        return
    
    # Run the interviews
    success = asyncio.run(run_interviews(args))
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
