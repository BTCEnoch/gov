#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: Setup and Initialization Script
Validates installation and prepares the lighthouse system
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def check_python_version() -> bool:
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_lighthouse_structure() -> bool:
    """Validate lighthouse directory structure"""
    required_dirs = [
        "lighthouse/complete_lighthouse",
        "divination_systems",
        "utilities",
        "docs"
    ]
    
    required_files = [
        "lighthouse/complete_lighthouse/lighthouse_master_index.json",
        "divination_systems/tarot_engine.py",
        "divination_systems/i_ching_engine.py",
        "divination_systems/astrology_engine.py",
        "utilities/content_indexer.py"
    ]
    
    print("🔍 Checking lighthouse structure...")
    
    # Check directories
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            return False
        print(f"✅ Directory found: {dir_path}")
    
    # Check files
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing file: {file_path}")
            return False
        print(f"✅ File found: {file_path}")
    
    return True

def validate_lighthouse_content() -> Tuple[bool, Dict]:
    """Validate lighthouse content integrity"""
    print("📚 Validating lighthouse content...")
    
    master_index_file = Path("lighthouse/complete_lighthouse/lighthouse_master_index.json")
    
    if not master_index_file.exists():
        print("❌ Master index file not found")
        return False, {}
    
    try:
        with open(master_index_file, 'r', encoding='utf-8') as f:
            master_index = json.load(f)
        
        total_traditions = master_index.get("total_traditions", 0)
        total_entries = master_index.get("total_entries", 0)
        traditions = master_index.get("traditions", {})
        
        print(f"✅ Master index loaded successfully")
        print(f"   📊 Total traditions: {total_traditions}")
        print(f"   📚 Total entries: {total_entries}")
        
        # Validate tradition files
        missing_files = []
        for tradition_name, tradition_info in traditions.items():
            tradition_file = Path(f"lighthouse/complete_lighthouse/{tradition_name}.json")
            if not tradition_file.exists():
                missing_files.append(tradition_name)
        
        if missing_files:
            print(f"❌ Missing tradition files: {', '.join(missing_files)}")
            return False, master_index
        
        print(f"✅ All {len(traditions)} tradition files found")
        
        return True, master_index
        
    except Exception as e:
        print(f"❌ Error validating content: {e}")
        return False, {}

def test_divination_systems() -> bool:
    """Test divination systems functionality"""
    print("🔮 Testing divination systems...")
    
    try:
        # Test imports
        sys.path.append(str(Path.cwd()))
        
        from divination_systems.tarot_engine import TarotEngine
        from divination_systems.i_ching_engine import IChingEngine
        from divination_systems.astrology_engine import AstrologyEngine
        from divination_systems.divination_master import DivinationMaster
        
        print("✅ All divination modules imported successfully")
        
        # Test basic functionality
        tarot = TarotEngine("lighthouse/complete_lighthouse")
        print(f"✅ Tarot engine initialized with {len(tarot.deck)} cards")
        
        iching = IChingEngine("lighthouse/complete_lighthouse")
        print(f"✅ I Ching engine initialized with {len(iching.hexagrams)} hexagrams")
        
        astrology = AstrologyEngine("lighthouse/complete_lighthouse")
        print(f"✅ Astrology engine initialized with {len(astrology.signs)} signs")
        
        divination_master = DivinationMaster("lighthouse/complete_lighthouse")
        print("✅ Divination master initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing divination systems: {e}")
        return False

def test_content_indexer() -> bool:
    """Test content indexing system"""
    print("🗂️ Testing content indexer...")
    
    try:
        sys.path.append(str(Path.cwd()))
        
        from utilities.content_indexer import ContentIndexer
        
        indexer = ContentIndexer("lighthouse/complete_lighthouse")
        print(f"✅ Content indexer initialized")
        print(f"   📚 Indexed {len(indexer.content_index)} entries")
        print(f"   🏛️ Mapped {len(indexer.tradition_maps)} traditions")
        
        # Test search functionality
        results = indexer.search("tarot", limit=3)
        print(f"✅ Search test successful - found {len(results)} results for 'tarot'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content indexer: {e}")
        return False

def generate_system_report() -> Dict:
    """Generate comprehensive system report"""
    print("📋 Generating system report...")
    
    report = {
        "lighthouse_version": "4.0.0-complete",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "installation_path": str(Path.cwd()),
        "components": {
            "lighthouse_core": False,
            "divination_systems": False,
            "content_indexer": False,
            "documentation": False
        },
        "content_stats": {},
        "recommendations": []
    }
    
    # Check components
    if Path("lighthouse/complete_lighthouse").exists():
        report["components"]["lighthouse_core"] = True
    
    if Path("divination_systems").exists():
        report["components"]["divination_systems"] = True
    
    if Path("utilities/content_indexer.py").exists():
        report["components"]["content_indexer"] = True
    
    if Path("docs").exists():
        report["components"]["documentation"] = True
    
    # Get content stats
    master_index_file = Path("lighthouse/complete_lighthouse/lighthouse_master_index.json")
    if master_index_file.exists():
        try:
            with open(master_index_file, 'r', encoding='utf-8') as f:
                master_index = json.load(f)
            report["content_stats"] = {
                "total_traditions": master_index.get("total_traditions", 0),
                "total_entries": master_index.get("total_entries", 0),
                "categories": master_index.get("categories", {}),
                "completion_percentage": master_index.get("completion_percentage", 0)
            }
        except:
            pass
    
    # Generate recommendations
    if not all(report["components"].values()):
        report["recommendations"].append("Some components are missing - check installation")
    
    if report["content_stats"].get("total_entries", 0) < 2500:
        report["recommendations"].append("Content appears incomplete - verify lighthouse data")
    
    if not report["recommendations"]:
        report["recommendations"].append("System appears fully functional and ready for use")
    
    return report

def main():
    """Main setup and validation routine"""
    print("🏛️ Enochian Cyphers Lighthouse Setup & Validation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check structure
    if not check_lighthouse_structure():
        print("\n❌ Lighthouse structure validation failed")
        sys.exit(1)
    
    # Validate content
    content_valid, master_index = validate_lighthouse_content()
    if not content_valid:
        print("\n❌ Content validation failed")
        sys.exit(1)
    
    # Test divination systems
    if not test_divination_systems():
        print("\n❌ Divination systems test failed")
        sys.exit(1)
    
    # Test content indexer
    if not test_content_indexer():
        print("\n❌ Content indexer test failed")
        sys.exit(1)
    
    # Generate report
    report = generate_system_report()
    
    print("\n" + "=" * 60)
    print("🎉 LIGHTHOUSE SETUP COMPLETE")
    print("=" * 60)
    print(f"✅ All systems operational")
    print(f"📊 {report['content_stats'].get('total_traditions', 0)} traditions with {report['content_stats'].get('total_entries', 0)} entries")
    print(f"🔮 Divination systems ready")
    print(f"🗂️ Content indexing operational")
    print(f"📚 Documentation available")
    
    print("\n🚀 Ready for integration with:")
    print("   - Governor Angels (personality and decision systems)")
    print("   - Story Engine (quest generation and narrative)")
    print("   - Bitcoin L1 (inscription deployment)")
    
    print(f"\n💡 Recommendations:")
    for rec in report["recommendations"]:
        print(f"   - {rec}")
    
    # Save report
    with open("lighthouse_setup_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Setup report saved to: lighthouse_setup_report.json")

if __name__ == "__main__":
    main()
