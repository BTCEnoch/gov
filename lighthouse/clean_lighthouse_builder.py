#!/usr/bin/env python3
"""
Clean Lighthouse Builder - Removes spam and creates essential knowledge base
Focuses on unique, valuable content only
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class CleanKnowledgeEntry:
    """Clean, essential knowledge entry without spam"""
    id: str
    name: str
    description: str  # Concise, unique description only
    category: str     # principle, practice, concept, symbol, tool
    applications: List[str]  # Specific, actionable applications
    connections: List[str]   # Cross-tradition links
    level: str       # beginner, intermediate, advanced
    source: str      # Specific, real source

class CleanLighthouseBuilder:
    """Builds clean, spam-free lighthouse with essential content only"""
    
    def __init__(self):
        self.output_dir = Path("lighthouse_clean")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_essential_traditions(self) -> Dict[str, List[CleanKnowledgeEntry]]:
        """Create essential knowledge entries for core traditions"""
        traditions = {}
        
        # ENOCHIAN MAGIC - Core essentials only
        traditions["enochian_magic"] = [
            CleanKnowledgeEntry(
                id="enochian_001",
                name="30 Aethyrs",
                description="Thirty spiritual realms from TEX (30th, material) to LIL (1st, divine). Each Aethyr contains specific angels, lessons, and consciousness states accessible through scrying.",
                category="concept",
                applications=["Astral projection", "Consciousness expansion", "Angelic communication", "Spiritual development"],
                connections=["hermetic_qabalah", "golden_dawn"],
                level="advanced",
                source="Dee's Spiritual Diaries (1582-1589)"
            ),
            CleanKnowledgeEntry(
                id="enochian_002", 
                name="91 Governor Angels",
                description="Angelic beings governing the Aethyrs. Each has specific name, sigil, and expertise. Three governors per Aethyr (except LIL with one). Provide guidance and teaching.",
                category="concept",
                applications=["Personal guidance", "Specialized knowledge", "Magical assistance", "Spiritual protection"],
                connections=["hermetic_qabalah", "golden_dawn"],
                level="advanced",
                source="Liber Scientiae, Dee's angelic communications"
            ),
            CleanKnowledgeEntry(
                id="enochian_003",
                name="Enochian Language",
                description="Sacred angelic language with unique grammar and syntax. Used for invocations, prayers, and magical operations. Each word carries specific vibrational qualities.",
                category="tool",
                applications=["Ritual invocation", "Prayer", "Magical operations", "Angelic communication"],
                connections=["golden_dawn", "thelema"],
                level="intermediate",
                source="Liber Loagaeth, Dee's linguistic records"
            ),
            CleanKnowledgeEntry(
                id="enochian_004",
                name="Elemental Watchtowers",
                description="Four tablets containing names of angels, spirits, and magical squares for each element (Fire, Water, Air, Earth). Used for elemental magic and invocation.",
                category="tool",
                applications=["Elemental magic", "Spirit invocation", "Magical squares", "Protective work"],
                connections=["golden_dawn", "hermetic_qabalah"],
                level="intermediate",
                source="Liber Scientiae, Watchtower tablets"
            ),
            CleanKnowledgeEntry(
                id="enochian_005",
                name="Sigil of Ameth",
                description="Primary protective seal used in Enochian operations. Complex geometric design containing divine names and angelic signatures for protection and invocation.",
                category="symbol",
                applications=["Protection", "Invocation", "Consecration", "Ritual preparation"],
                connections=["sacred_geometry", "hermetic_qabalah"],
                level="intermediate",
                source="Dee's magical records, Liber Mysteriorum"
            )
        ]
        
        # HERMETIC QABALAH - Core essentials only
        traditions["hermetic_qabalah"] = [
            CleanKnowledgeEntry(
                id="qabalah_001",
                name="Tree of Life",
                description="Central glyph showing 10 sephiroth (divine emanations) connected by 22 paths. Maps structure of reality, consciousness, and spiritual development from Malkuth to Kether.",
                category="concept",
                applications=["Meditation", "Pathworking", "Magical correspondences", "Spiritual mapping"],
                connections=["tarot", "astrology", "golden_dawn"],
                level="intermediate",
                source="Sepher Yetzirah, Golden Dawn teachings"
            ),
            CleanKnowledgeEntry(
                id="qabalah_002",
                name="Four Worlds",
                description="Four levels of reality: Atziluth (Archetypal), Briah (Creative), Yetzirah (Formative), Assiah (Material). Shows how divine energy manifests through increasingly dense levels.",
                category="concept",
                applications=["Understanding manifestation", "Magical operations", "Consciousness work", "Reality mapping"],
                connections=["alchemy", "golden_dawn"],
                level="advanced",
                source="Zohar, Lurianic Kabbalah"
            ),
            CleanKnowledgeEntry(
                id="qabalah_003",
                name="Pathworking",
                description="Guided meditation journey along Tree of Life paths to gain spiritual insights. Each path corresponds to tarot trump and specific experiences.",
                category="practice",
                applications=["Spiritual development", "Inner guidance", "Symbolic understanding", "Consciousness expansion"],
                connections=["tarot", "golden_dawn"],
                level="intermediate",
                source="Golden Dawn practices, modern Qabalistic meditation"
            )
        ]
        
        # TAROT - Core essentials only
        traditions["tarot"] = [
            CleanKnowledgeEntry(
                id="tarot_001",
                name="Major Arcana",
                description="22 trump cards representing major life themes and spiritual journey from Fool (0) to World (21). Each corresponds to Hebrew letter and Tree of Life path.",
                category="concept",
                applications=["Life guidance", "Spiritual development", "Archetypal understanding", "Personal growth"],
                connections=["hermetic_qabalah", "astrology", "golden_dawn"],
                level="beginner",
                source="Rider-Waite-Smith deck, Golden Dawn correspondences"
            ),
            CleanKnowledgeEntry(
                id="tarot_002",
                name="Minor Arcana",
                description="56 cards in four suits (Wands/Fire, Cups/Water, Swords/Air, Pentacles/Earth). Ace through 10 plus court cards. Represents daily life and elemental energies.",
                category="concept",
                applications=["Daily guidance", "Practical decisions", "Elemental balance", "Situational insight"],
                connections=["hermetic_qabalah", "golden_dawn"],
                level="beginner",
                source="Traditional tarot structure, Golden Dawn elemental correspondences"
            )
        ]
        
        return traditions
    
    def create_clean_lighthouse(self):
        """Create clean, essential lighthouse without spam"""
        print("🧹 Creating Clean Lighthouse (Spam-Free)")
        print("=" * 45)
        
        traditions = self.create_essential_traditions()
        total_entries = 0
        
        # Save individual tradition files
        for tradition_id, entries in traditions.items():
            tradition_file = self.output_dir / f"{tradition_id}.json"
            with open(tradition_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(entry) for entry in entries], f, indent=2, ensure_ascii=False)
            
            total_entries += len(entries)
            print(f"✅ {tradition_id}: {len(entries)} essential entries")
        
        # Create clean master index
        clean_index = {
            "lighthouse_version": "2.0.0-clean",
            "created_date": datetime.now().isoformat(),
            "philosophy": "Quality over quantity - essential knowledge only",
            "total_traditions": len(traditions),
            "total_entries": total_entries,
            "spam_removed": True,
            "traditions": {
                tradition_id: {
                    "name": tradition_id.replace("_", " ").title(),
                    "entry_count": len(entries),
                    "file_path": f"{tradition_id}.json"
                }
                for tradition_id, entries in traditions.items()
            },
            "size_comparison": {
                "original_entries": 2678,
                "clean_entries": total_entries,
                "reduction_ratio": f"{((2678 - total_entries) / 2678 * 100):.1f}% spam removed"
            }
        }
        
        # Save clean master index
        index_file = self.output_dir / "clean_lighthouse_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(clean_index, f, indent=2, ensure_ascii=False)
        
        print(f"\n🌟 Clean Lighthouse Complete!")
        print(f"📊 Original entries: 2,678 (mostly spam)")
        print(f"📊 Clean entries: {total_entries} (essential only)")
        print(f"📊 Spam removed: {((2678 - total_entries) / 2678 * 100):.1f}%")
        print(f"📁 Output: {self.output_dir}")
        
        return clean_index
    
    def analyze_spam_patterns(self):
        """Analyze what was spam in the original lighthouse"""
        spam_patterns = {
            "template_bloat": [
                "Historical Development: [repeated historical_context]",
                "Within the tradition of [X], [concept] represents a fundamental aspect...",
                "Practical Applications: [restated practical_applications array]",
                "Integration with Other Traditions: [restated cross_tradition_links]",
                "Modern Relevance: In contemporary spiritual practice...",
                "Advanced Considerations: For advanced practitioners..."
            ],
            "redundant_fields": [
                "full_description repeating summary",
                "historical_context repeated in full_description", 
                "practical_applications restated as prose",
                "cross_tradition_links explained again"
            ],
            "meaningless_content": [
                "Enhanced understanding of [concept name]",
                "Traditional [tradition] texts",
                "Basic understanding of tradition",
                "Requires serious study",
                "Advanced [Tradition] Practice [number]"
            ],
            "artificial_inflation": [
                "Generated entries to reach target counts",
                "Repetitive concept variations",
                "Generic practice templates"
            ]
        }
        
        print("\n🔍 SPAM ANALYSIS:")
        for category, patterns in spam_patterns.items():
            print(f"\n{category.upper()}:")
            for pattern in patterns:
                print(f"   ❌ {pattern}")
        
        return spam_patterns

if __name__ == "__main__":
    builder = CleanLighthouseBuilder()
    
    # Analyze spam first
    builder.analyze_spam_patterns()
    
    # Create clean lighthouse
    clean_index = builder.create_clean_lighthouse()
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"   Use the clean lighthouse for actual development")
    print(f"   Original lighthouse was 95%+ spam and template bloat")
    print(f"   Clean version contains only essential, unique knowledge")
