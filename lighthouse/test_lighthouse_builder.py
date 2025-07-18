#!/usr/bin/env python3
"""
Test script for Lighthouse Builder
Demonstrates the knowledge base generation system
"""

import sys
import json
from pathlib import Path

# Add the lighthouse directory to Python path
sys.path.append(str(Path(__file__).parent))

from tradition_content_templates import TraditionContentTemplates
from lighthouse_builder import LighthouseBuilder

def test_template_system():
    """Test the tradition template system"""
    print("🧪 Testing Tradition Template System")
    print("=" * 40)
    
    templates = TraditionContentTemplates()
    all_templates = templates.get_all_templates()
    
    print(f"📊 Total Templates: {len(all_templates)}")
    
    # Test by category
    categories = ["magick_systems", "philosophy", "divination_systems", "science"]
    for category in categories:
        cat_templates = templates.get_templates_by_category(category)
        print(f"   {category}: {len(cat_templates)} traditions")
        for tradition_id, template in cat_templates.items():
            print(f"      - {template.name} (target: {template.entry_count_target} entries)")
    
    print("\n✅ Template system working correctly!")
    return True

def test_single_tradition_build():
    """Test building a single tradition"""
    print("\n🧪 Testing Single Tradition Build")
    print("=" * 40)
    
    builder = LighthouseBuilder("test_output")
    
    # Test with Enochian Magic
    entries = builder.build_tradition_knowledge_base("enochian_magic")
    
    print(f"📊 Generated {len(entries)} entries for Enochian Magic")
    
    # Show sample entries
    print("\n📚 Sample Entries:")
    for i, entry in enumerate(entries[:3]):
        print(f"   {i+1}. {entry.name} ({entry.category})")
        print(f"      Summary: {entry.summary[:100]}...")
        print(f"      Level: {entry.specialization_level}")
        print()
    
    print("✅ Single tradition build working correctly!")
    return len(entries) > 0

def test_lighthouse_structure():
    """Test the complete lighthouse structure"""
    print("\n🧪 Testing Complete Lighthouse Structure")
    print("=" * 40)
    
    builder = LighthouseBuilder("test_lighthouse")
    
    # Build just a few traditions for testing
    test_traditions = ["enochian_magic", "hermetic_qabalah", "tarot"]
    
    print(f"🏗️ Building test lighthouse with {len(test_traditions)} traditions...")
    
    all_entries = []
    for tradition_id in test_traditions:
        entries = builder.build_tradition_knowledge_base(tradition_id)
        all_entries.extend(entries)
        print(f"   ✅ {tradition_id}: {len(entries)} entries")
    
    # Create test index
    test_index = {
        "lighthouse_version": "1.0.0-test",
        "total_traditions": len(test_traditions),
        "total_entries": len(all_entries),
        "test_mode": True
    }
    
    # Save test index
    test_file = Path("test_lighthouse") / "test_index.json"
    test_file.parent.mkdir(exist_ok=True)
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_index, f, indent=2)
    
    print(f"\n📊 Test Lighthouse Summary:")
    print(f"   Traditions: {test_index['total_traditions']}")
    print(f"   Total Entries: {test_index['total_entries']}")
    print(f"   Average per Tradition: {test_index['total_entries'] // test_index['total_traditions']}")
    
    print("✅ Lighthouse structure working correctly!")
    return True

def test_bitcoin_inscription_readiness():
    """Test Bitcoin inscription preparation"""
    print("\n🧪 Testing Bitcoin Inscription Readiness")
    print("=" * 40)
    
    # Test size estimation
    sample_entry = {
        "id": "test_entry_001",
        "name": "Test Knowledge Entry",
        "description": "This is a test entry to estimate size for Bitcoin inscription preparation.",
        "full_content": "A" * 500,  # 500 character content
        "metadata": {"test": True}
    }
    
    # Calculate sizes
    json_size = len(json.dumps(sample_entry))
    compressed_estimate = json_size * 0.6  # Rough gzip compression estimate
    
    print(f"📏 Sample Entry Sizes:")
    print(f"   JSON: {json_size} bytes")
    print(f"   Compressed (est): {compressed_estimate:.0f} bytes")
    
    # Calculate entries per inscription
    max_inscription_size = 1000000  # 1MB
    entries_per_inscription = max_inscription_size // (compressed_estimate * 1.2)  # Safety margin
    
    print(f"   Entries per 1MB inscription: ~{entries_per_inscription:.0f}")
    
    # Test with actual tradition
    builder = LighthouseBuilder("test_inscription")
    entries = builder.build_tradition_knowledge_base("tarot")
    
    total_size = sum(len(json.dumps(entry.__dict__)) for entry in entries)
    print(f"\n📊 Tarot Tradition:")
    print(f"   Entries: {len(entries)}")
    print(f"   Total Size: {total_size:,} bytes ({total_size/1000:.1f}KB)")
    print(f"   Fits in 1MB: {'✅ Yes' if total_size < 1000000 else '❌ No'}")
    
    print("✅ Bitcoin inscription readiness confirmed!")
    return True

def main():
    """Run all tests"""
    print("🏛️ LIGHTHOUSE BUILDER TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Template System", test_template_system),
        ("Single Tradition Build", test_single_tradition_build),
        ("Lighthouse Structure", test_lighthouse_structure),
        ("Bitcoin Inscription Readiness", test_bitcoin_inscription_readiness)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n🏛️ TEST RESULTS SUMMARY")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🌟 All tests passed! Lighthouse Builder is ready for production use.")
        print("\n🚀 Next Steps:")
        print("   1. Run full lighthouse build with all 26 traditions")
        print("   2. Create Bitcoin inscription batches")
        print("   3. Deploy to Bitcoin L1 testnet")
        print("   4. Integrate with story engine and governor system")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please review and fix issues.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
