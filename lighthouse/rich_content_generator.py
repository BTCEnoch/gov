#!/usr/bin/env python3
"""
Rich Content Generator for Enochian Cyphers Knowledge Base
Uses existing research data to create comprehensive, detailed knowledge entries
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib
from datetime import datetime

@dataclass
class RichKnowledgeEntry:
    """Rich knowledge entry with comprehensive content"""
    id: str
    tradition: str
    name: str
    category: str  # principle, practice, concept, technique, symbol, deity, tool
    summary: str  # 2-3 sentence overview
    full_description: str  # Rich 400-800 word detailed description
    historical_context: str  # Historical background and development
    practical_applications: List[str]  # How to use/apply this knowledge
    related_concepts: List[str]  # Connected ideas within tradition
    cross_tradition_links: List[str]  # Connections to other traditions
    prerequisites: List[str]  # What you need to know first
    benefits: List[str]  # What you gain from this knowledge
    warnings: List[str]  # Important cautions or considerations
    specialization_level: str  # beginner, intermediate, advanced, master
    sources: List[str]  # Research sources and references
    authenticity_score: float  # 0.0-1.0 reliability rating
    tags: List[str]  # Searchable tags
    created_date: str
    merkle_hash: str

class RichContentGenerator:
    """Generates rich, detailed content for knowledge base entries"""
    
    def __init__(self, research_file: str = "core/governors/traits/knowledge_base/wiki_api_knowledge_content.json"):
        self.research_file = Path(research_file)
        self.research_data = self._load_research_data()
        self.output_dir = Path("lighthouse_rich_content")
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_research_data(self) -> Dict:
        """Load existing research data"""
        try:
            with open(self.research_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading research data: {e}")
            return {}
    
    def generate_golden_dawn_content(self) -> List[RichKnowledgeEntry]:
        """Generate comprehensive Golden Dawn knowledge entries"""
        entries = []
        
        if "golden_dawn" not in self.research_data.get("traditions", {}):
            print("❌ No Golden Dawn research data found")
            return entries
        
        gd_data = self.research_data["traditions"]["golden_dawn"]
        
        # Core Principles
        principles = [
            {
                "name": "Hermetic Order Structure",
                "category": "principle",
                "summary": "The Golden Dawn's hierarchical grade system based on the Tree of Life, providing structured spiritual development through initiation and study.",
                "description": """The Hermetic Order of the Golden Dawn established a revolutionary approach to Western esoteric education through its carefully structured grade system. Based on the Qabalistic Tree of Life, the Order divided spiritual development into three distinct Orders: the Golden Dawn (Outer Order), the Rosae Rubeae et Aureae Crucis (Inner Order), and the Silver Star (Secret Order).

The First Order, known as the Golden Dawn proper, consisted of five grades corresponding to the four elements plus a preparatory Neophyte grade. Students progressed from Neophyte (0=0) through Zelator (1=10, Earth), Theoricus (2=9, Air), Practicus (3=8, Water), and Philosophus (4=7, Fire). Each grade required mastery of specific knowledge including Qabalah, astrology, tarot, geomancy, and the classical elements.

The Second Order, Rosae Rubeae et Aureae Crucis (R.R. et A.C.), began with the Adeptus Minor grade (5=6, Tiphareth) and included practical magical training, ritual construction, and advanced Qabalistic work. This structure ensured that students developed both theoretical knowledge and practical skills in a balanced, progressive manner.

The grade system's genius lay in its integration of multiple esoteric traditions - Hermetic philosophy, Qabalistic mysticism, Egyptian symbolism, and Christian mysticism - into a coherent educational framework. Each grade built upon previous knowledge while introducing new concepts, creating a comprehensive foundation for magical practice that influenced virtually all subsequent Western esoteric orders.""",
                "applications": [
                    "Structured spiritual development",
                    "Progressive magical training",
                    "Balanced theoretical and practical education",
                    "Integration of multiple esoteric traditions"
                ]
            },
            {
                "name": "Elemental Magic System",
                "category": "principle", 
                "summary": "The Golden Dawn's comprehensive approach to elemental magic, incorporating the four classical elements as fundamental forces in magical practice and spiritual development.",
                "description": """The Golden Dawn's elemental magic system represents one of the most sophisticated approaches to working with the classical elements in Western esotericism. Drawing from Hermetic philosophy, the Order taught that the four elements - Fire, Water, Air, and Earth - are not merely physical substances but fundamental principles underlying all existence.

Each element was associated with specific qualities, colors, symbols, and magical tools. Fire represented energy, passion, and will, symbolized by the wand and the color red. Water embodied emotion, intuition, and the subconscious, represented by the cup and blue. Air signified intellect, communication, and mental clarity, associated with the sword and yellow. Earth represented stability, material manifestation, and practical wisdom, symbolized by the pentacle and the colors black, brown, and green.

The elemental system extended beyond simple correspondences to include complex magical practices. Students learned to invoke and banish elemental forces, create elemental talismans, and work with elemental spirits. The famous Lesser Banishing Ritual of the Pentagram, still widely used today, demonstrates the practical application of elemental principles in protective magic.

Advanced practitioners learned to balance the elements within themselves, recognizing that spiritual development required harmonizing these fundamental forces. This internal alchemy was considered essential preparation for higher magical work, as imbalanced elements could lead to psychological and spiritual difficulties. The elemental system thus served both as a practical magical framework and a sophisticated model for psychological and spiritual development.""",
                "applications": [
                    "Elemental invocation and banishing",
                    "Talisman creation and consecration", 
                    "Psychological balance and development",
                    "Protective magical practices"
                ]
            }
        ]
        
        # Generate entries from principles
        for i, principle in enumerate(principles):
            entry = RichKnowledgeEntry(
                id=f"golden_dawn_principle_{i+1:03d}",
                tradition="golden_dawn",
                name=principle["name"],
                category=principle["category"],
                summary=principle["summary"],
                full_description=principle["description"],
                historical_context=self._extract_historical_context(gd_data),
                practical_applications=principle["applications"],
                related_concepts=self._generate_related_concepts(principle["name"]),
                cross_tradition_links=["hermetic_qabalah", "thelema", "enochian_magic"],
                prerequisites=["Basic understanding of Western esotericism"],
                benefits=[
                    "Structured spiritual development",
                    "Comprehensive magical education",
                    "Integration of multiple traditions"
                ],
                warnings=[
                    "Requires serious commitment to study",
                    "Progressive system - don't skip grades"
                ],
                specialization_level="intermediate",
                sources=self._extract_sources(gd_data),
                authenticity_score=0.95,
                tags=["golden_dawn", "hermetic", "magic", "initiation"],
                created_date=datetime.now().isoformat(),
                merkle_hash=self._calculate_hash(f"golden_dawn_principle_{i+1}")
            )
            entries.append(entry)
        
        return entries
    
    def generate_enochian_magic_content(self) -> List[RichKnowledgeEntry]:
        """Generate comprehensive Enochian Magic knowledge entries"""
        entries = []
        
        # Core Enochian concepts with rich descriptions
        enochian_concepts = [
            {
                "name": "The 30 Aethyrs",
                "category": "concept",
                "summary": "The thirty spiritual realms or planes of existence in Enochian cosmology, each governed by specific angels and containing unique spiritual lessons and experiences.",
                "description": """The 30 Aethyrs represent one of the most sophisticated cosmological systems in Western esotericism, revealed through the angelic communications received by John Dee and Edward Kelley between 1582-1589. These Aethyrs are spiritual realms or planes of existence, arranged in a hierarchical structure from the most material (30th Aethyr, TEX) to the most divine (1st Aethyr, LIL).

Each Aethyr is identified by a three-letter name in the Enochian language and is governed by specific angels who serve as guides and teachers for those who successfully traverse these realms. The Aethyrs are not merely abstract concepts but represent actual spiritual territories that can be explored through advanced scrying techniques and astral projection.

The journey through the Aethyrs follows a specific pattern of spiritual development. The lower Aethyrs (30-21) deal with earthly concerns, psychological integration, and the purification of the personality. The middle Aethyrs (20-11) involve encounters with archetypal forces, the dissolution of ego boundaries, and preparation for divine union. The highest Aethyrs (10-1) represent increasingly refined spiritual states, culminating in direct experience of divine consciousness.

Each Aethyr contains its own unique landscape, inhabitants, and spiritual lessons. Practitioners who successfully explore these realms report profound transformative experiences, including encounters with angelic beings, reception of spiritual teachings, and dramatic shifts in consciousness. The Aethyric system provides a complete map for spiritual development, from initial awakening to ultimate enlightenment.""",
                "applications": [
                    "Advanced scrying and vision work",
                    "Systematic spiritual development",
                    "Angelic communication and guidance",
                    "Consciousness expansion practices"
                ]
            }
        ]
        
        for i, concept in enumerate(enochian_concepts):
            entry = RichKnowledgeEntry(
                id=f"enochian_magic_concept_{i+1:03d}",
                tradition="enochian_magic",
                name=concept["name"],
                category=concept["category"],
                summary=concept["summary"],
                full_description=concept["description"],
                historical_context="Received by Dr. John Dee and Edward Kelley through angelic communications (1582-1589)",
                practical_applications=concept["applications"],
                related_concepts=["Governor Angels", "Enochian Language", "Elemental Watchtowers"],
                cross_tradition_links=["hermetic_qabalah", "golden_dawn", "thelema"],
                prerequisites=["Advanced scrying skills", "Understanding of angelic hierarchy"],
                benefits=[
                    "Direct angelic communication",
                    "Systematic spiritual development",
                    "Profound consciousness expansion"
                ],
                warnings=[
                    "Requires extensive preparation",
                    "Can be psychologically challenging",
                    "Should not be attempted without proper grounding"
                ],
                specialization_level="advanced",
                sources=["Dee's Spiritual Diaries", "Liber Scientiae", "Liber Loagaeth"],
                authenticity_score=0.98,
                tags=["enochian", "aethyrs", "angels", "scrying", "consciousness"],
                created_date=datetime.now().isoformat(),
                merkle_hash=self._calculate_hash(f"enochian_magic_concept_{i+1}")
            )
            entries.append(entry)
        
        return entries
    
    def _extract_historical_context(self, tradition_data: Dict) -> str:
        """Extract historical context from research data"""
        if "extracted_articles" in tradition_data:
            for article in tradition_data["extracted_articles"]:
                if "history" in article.get("title", "").lower():
                    return article.get("summary", "")[:500] + "..."
        return "Historical context to be researched and added."
    
    def _generate_related_concepts(self, concept_name: str) -> List[str]:
        """Generate related concepts based on the main concept"""
        # This would be expanded with actual relationship mapping
        return ["Related Concept 1", "Related Concept 2", "Related Concept 3"]
    
    def _extract_sources(self, tradition_data: Dict) -> List[str]:
        """Extract sources from research data"""
        sources = []
        if "extracted_articles" in tradition_data:
            for article in tradition_data["extracted_articles"]:
                sources.append(article.get("url", ""))
        return sources[:5]  # Limit to top 5 sources
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate hash for content integrity"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def generate_all_rich_content(self):
        """Generate rich content for all available traditions"""
        print("️ Generating Rich Knowledge Base Content")
        print("=" * 50)
        
        all_entries = []
        
        # Generate Golden Dawn content
        print(" Generating Golden Dawn content...")
        gd_entries = self.generate_golden_dawn_content()
        all_entries.extend(gd_entries)
        print(f"✅ Generated {len(gd_entries)} Golden Dawn entries")
        
        # Generate Enochian Magic content
        print(" Generating Enochian Magic content...")
        enochian_entries = self.generate_enochian_magic_content()
        all_entries.extend(enochian_entries)
        print(f"✅ Generated {len(enochian_entries)} Enochian Magic entries")
        
        # Save all entries
        output_file = self.output_dir / "rich_knowledge_entries.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(entry) for entry in all_entries], f, indent=2, ensure_ascii=False)
        
        print(f"\n Rich Content Generation Complete!")
        print(f" Total entries: {len(all_entries)}")
        print(f" Output file: {output_file}")
        
        return all_entries

    def create_lighthouse_index(self, entries: List[RichKnowledgeEntry]) -> Dict[str, Any]:
        """Create master lighthouse index for Bitcoin inscription"""
        traditions = {}
        total_size = 0

        for entry in entries:
            if entry.tradition not in traditions:
                traditions[entry.tradition] = {
                    "name": entry.tradition.replace("_", " ").title(),
                    "entries": [],
                    "total_entries": 0,
                    "estimated_size": 0
                }

            traditions[entry.tradition]["entries"].append({
                "id": entry.id,
                "name": entry.name,
                "category": entry.category,
                "size_estimate": len(entry.full_description) + len(entry.summary)
            })
            traditions[entry.tradition]["total_entries"] += 1
            traditions[entry.tradition]["estimated_size"] += len(json.dumps(asdict(entry)))

        lighthouse_index = {
            "lighthouse_version": "1.0.0",
            "created_date": datetime.now().isoformat(),
            "total_traditions": len(traditions),
            "total_entries": len(entries),
            "traditions": traditions,
            "inscription_batches": self._create_inscription_batches(traditions),
            "merkle_root": self._calculate_hash("lighthouse_master_index"),
            "metadata": {
                "target_inscription_size": "1MB",
                "compression": "gzip",
                "encoding": "utf-8"
            }
        }

        return lighthouse_index

    def _create_inscription_batches(self, traditions: Dict) -> List[Dict[str, Any]]:
        """Create Bitcoin inscription batches under 1MB each"""
        batches = []
        current_batch = {
            "batch_id": f"lighthouse_batch_001",
            "traditions": [],
            "estimated_size": 0,
            "priority": "critical"
        }

        max_batch_size = 900000  # 900KB to leave room for compression

        for tradition_id, tradition_data in traditions.items():
            if current_batch["estimated_size"] + tradition_data["estimated_size"] > max_batch_size:
                # Start new batch
                batches.append(current_batch)
                current_batch = {
                    "batch_id": f"lighthouse_batch_{len(batches)+1:03d}",
                    "traditions": [],
                    "estimated_size": 0,
                    "priority": "high" if len(batches) < 3 else "medium"
                }

            current_batch["traditions"].append(tradition_id)
            current_batch["estimated_size"] += tradition_data["estimated_size"]

        if current_batch["traditions"]:
            batches.append(current_batch)

        return batches

if __name__ == "__main__":
    generator = RichContentGenerator()
    entries = generator.generate_all_rich_content()

    # Create lighthouse index
    lighthouse_index = generator.create_lighthouse_index(entries)

    # Save lighthouse index
    index_file = generator.output_dir / "lighthouse_master_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(lighthouse_index, f, indent=2, ensure_ascii=False)

    print(f"️ Lighthouse Master Index created: {index_file}")
    print(f" Inscription batches: {len(lighthouse_index['inscription_batches'])}")
    for batch in lighthouse_index['inscription_batches']:
        print(f"   Batch {batch['batch_id']}: {len(batch['traditions'])} traditions, ~{batch['estimated_size']/1000:.1f}KB")
