#!/usr/bin/env python3
"""
Comprehensive Knowledge Base Generator for Enochian Cyphers Lighthouse
Creates rich, detailed content for all 26 sacred traditions
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

@dataclass
class KnowledgeEntry:
    """Individual knowledge entry with rich content"""
    id: str
    name: str
    description: str
    type: str  # principle, practice, sub_practice, concept
    content: str  # Rich 200-500 word content
    practical_applications: List[str]
    related_concepts: List[str]
    prerequisites: List[str]
    benefits: List[str]
    warnings: List[str]
    specialization_level: str  # beginner, intermediate, advanced, master
    authenticity_score: float
    sources: List[str]

@dataclass
class TraditionData:
    """Complete tradition with all knowledge entries"""
    tradition_id: str
    tradition_name: str
    category: str
    overview: str
    historical_context: str
    core_principles: List[KnowledgeEntry]
    practices: List[KnowledgeEntry]
    sub_practices: List[KnowledgeEntry]
    concepts: List[KnowledgeEntry]
    cross_tradition_connections: List[Dict[str, Any]]
    governor_applications: Dict[str, List[str]]
    authenticity_sources: List[Dict[str, Any]]
    total_entries: int
    merkle_hash: str

class ComprehensiveKnowledgeGenerator:
    """Generates comprehensive knowledge base for all 26 traditions"""
    
    def __init__(self, output_dir: str = "lighthouse_knowledge_base"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 26 Sacred Traditions
        self.traditions = {
            # MAGICK SYSTEMS (7)
            "enochian_magic": {
                "name": "Enochian Magic",
                "category": "magick_systems",
                "overview": "Angelic communication system received by John Dee and Edward Kelley, featuring the 30 Aethyrs, 91 Governor Angels, and the Enochian language for divine invocation and spiritual transformation.",
                "entry_count": 120
            },
            "hermetic_qabalah": {
                "name": "Hermetic Qabalah", 
                "category": "magick_systems",
                "overview": "Western esoteric interpretation of Jewish Kabbalah, featuring the Tree of Life, 22 paths, 10 sephiroth, and practical magical applications for spiritual development and divine union.",
                "entry_count": 110
            },
            "thelema": {
                "name": "Thelema",
                "category": "magick_systems", 
                "overview": "Aleister Crowley's magical and philosophical system based on 'Do what thou wilt shall be the whole of the Law,' emphasizing True Will discovery and Holy Guardian Angel contact.",
                "entry_count": 105
            },
            "celtic_druidic": {
                "name": "Celtic Druidic Traditions",
                "category": "magick_systems",
                "overview": "Ancient Celtic spiritual practices including grove work, seasonal festivals, tree magic, Ogham divination, and connection with the natural world and Celtic deities.",
                "entry_count": 100
            },
            "chaos_magic": {
                "name": "Chaos Magic",
                "category": "magick_systems",
                "overview": "Modern magical paradigm emphasizing belief as a tool, sigil magic, paradigm shifting, and practical results over dogmatic adherence to any single system.",
                "entry_count": 95
            },
            "alchemy": {
                "name": "Alchemy",
                "category": "magick_systems",
                "overview": "Ancient art of transformation combining chemistry, philosophy, and spirituality, seeking the Philosopher's Stone and the Great Work of spiritual and material transmutation.",
                "entry_count": 115
            },
            "golden_dawn": {
                "name": "Golden Dawn",
                "category": "magick_systems",
                "overview": "Influential Western magical order combining Hermetic Qabalah, astrology, alchemy, and ceremonial magic in a structured grade system for spiritual development.",
                "entry_count": 108
            },
            
            # PHILOSOPHY (6)
            "taoism": {
                "name": "Taoism",
                "category": "philosophy",
                "overview": "Chinese philosophical and spiritual tradition emphasizing the Dao as ultimate reality, wu wei (effortless action), yin-yang balance, and harmony with natural order.",
                "entry_count": 110
            },
            "traditional_kabbalah": {
                "name": "Traditional Jewish Kabbalah",
                "category": "philosophy", 
                "overview": "Jewish mystical tradition exploring the nature of divinity, creation, and the soul through the Tree of Life, Ein Sof, and practices for spiritual elevation and tikkun olam.",
                "entry_count": 125
            },
            "sufism": {
                "name": "Sufism",
                "category": "philosophy",
                "overview": "Islamic mystical tradition emphasizing direct experience of divine love, fana (ego dissolution), dhikr (remembrance), and the path of spiritual purification.",
                "entry_count": 105
            },
            "gnosticism": {
                "name": "Gnosticism", 
                "category": "philosophy",
                "overview": "Early Christian mystical movement emphasizing gnosis (direct spiritual knowledge), the divine spark within, liberation from material illusion, and return to the Pleroma.",
                "entry_count": 100
            },
            "norse_traditions": {
                "name": "Norse Traditions",
                "category": "philosophy",
                "overview": "Scandinavian spiritual and cultural system featuring the Nine Worlds, runic wisdom, concepts of wyrd (fate), honor culture, and connection with Norse deities.",
                "entry_count": 95
            },
            "greek_philosophy": {
                "name": "Greek Philosophy",
                "category": "philosophy",
                "overview": "Classical philosophical traditions including Platonic ideals, Aristotelian logic, Stoic wisdom, and Neoplatonic mysticism forming the foundation of Western thought.",
                "entry_count": 115
            }
        }
    
    def generate_tradition_content(self, tradition_id: str) -> TraditionData:
        """Generate comprehensive content for a single tradition"""
        tradition_info = self.traditions[tradition_id]
        
        # Generate core principles (15-20 entries)
        core_principles = self._generate_core_principles(tradition_id, tradition_info)
        
        # Generate practices (25-35 entries)
        practices = self._generate_practices(tradition_id, tradition_info)
        
        # Generate sub-practices (40-60 entries)
        sub_practices = self._generate_sub_practices(tradition_id, tradition_info, practices)
        
        # Generate concepts (20-30 entries)
        concepts = self._generate_concepts(tradition_id, tradition_info)
        
        # Generate cross-tradition connections
        connections = self._generate_cross_connections(tradition_id)
        
        # Generate governor applications
        governor_apps = self._generate_governor_applications(tradition_id, tradition_info)
        
        # Create tradition data
        tradition_data = TraditionData(
            tradition_id=tradition_id,
            tradition_name=tradition_info["name"],
            category=tradition_info["category"],
            overview=tradition_info["overview"],
            historical_context=self._generate_historical_context(tradition_id),
            core_principles=core_principles,
            practices=practices,
            sub_practices=sub_practices,
            concepts=concepts,
            cross_tradition_connections=connections,
            governor_applications=governor_apps,
            authenticity_sources=self._generate_authenticity_sources(tradition_id),
            total_entries=len(core_principles) + len(practices) + len(sub_practices) + len(concepts),
            merkle_hash=self._calculate_merkle_hash(tradition_id)
        )
        
        return tradition_data
    
    def _generate_core_principles(self, tradition_id: str, tradition_info: Dict) -> List[KnowledgeEntry]:
        """Generate core principles for a tradition"""
        # This would be expanded with actual content generation
        # For now, creating template structure
        principles = []
        
        principle_templates = {
            "enochian_magic": [
                "Angelic Communication", "Aethyric Exploration", "Enochian Language",
                "Elemental Watchtowers", "Governor Angel Hierarchy", "Divine Names",
                "Scrying Techniques", "Invocation Methods", "Spiritual Transformation"
            ],
            "hermetic_qabalah": [
                "Tree of Life", "Sephirotic Emanation", "Path Working", 
                "Divine Names", "Gematria", "Correspondences", "As Above So Below",
                "Microcosm Macrocosm", "Hermetic Axioms"
            ]
        }
        
        template_principles = principle_templates.get(tradition_id, [
            "Core Principle 1", "Core Principle 2", "Core Principle 3"
        ])
        
        for i, principle_name in enumerate(template_principles):
            principle = KnowledgeEntry(
                id=f"{tradition_id}_principle_{i+1:03d}",
                name=principle_name,
                description=f"Fundamental principle of {tradition_info['name']}",
                type="principle",
                content=f"[RICH CONTENT TO BE GENERATED] - Comprehensive 300-500 word explanation of {principle_name} within the context of {tradition_info['name']}. This would include historical development, practical applications, spiritual significance, and integration with other aspects of the tradition.",
                practical_applications=[f"Application 1 of {principle_name}", f"Application 2 of {principle_name}"],
                related_concepts=[f"Related concept 1", f"Related concept 2"],
                prerequisites=["Basic understanding of tradition"],
                benefits=[f"Benefit 1 of {principle_name}", f"Benefit 2 of {principle_name}"],
                warnings=[f"Caution regarding {principle_name}"],
                specialization_level="intermediate",
                authenticity_score=0.95,
                sources=[f"Traditional source for {principle_name}"]
            )
            principles.append(principle)
        
        return principles
    
    def _generate_practices(self, tradition_id: str, tradition_info: Dict) -> List[KnowledgeEntry]:
        """Generate practices for a tradition"""
        # Template implementation - would be expanded with real content
        return []
    
    def _generate_sub_practices(self, tradition_id: str, tradition_info: Dict, practices: List[KnowledgeEntry]) -> List[KnowledgeEntry]:
        """Generate sub-practices for a tradition"""
        # Template implementation - would be expanded with real content
        return []
    
    def _generate_concepts(self, tradition_id: str, tradition_info: Dict) -> List[KnowledgeEntry]:
        """Generate concepts for a tradition"""
        # Template implementation - would be expanded with real content
        return []
    
    def _generate_cross_connections(self, tradition_id: str) -> List[Dict[str, Any]]:
        """Generate cross-tradition connections"""
        return []
    
    def _generate_governor_applications(self, tradition_id: str, tradition_info: Dict) -> Dict[str, List[str]]:
        """Generate governor applications"""
        return {
            "personality_influences": [f"Influence from {tradition_info['name']}"],
            "decision_making_patterns": [f"Decision pattern from {tradition_info['name']}"],
            "communication_styles": [f"Communication style from {tradition_info['name']}"],
            "quest_generation_themes": [f"Quest theme from {tradition_info['name']}"]
        }
    
    def _generate_historical_context(self, tradition_id: str) -> str:
        """Generate historical context"""
        return f"[HISTORICAL CONTEXT TO BE GENERATED] - Comprehensive historical background for {tradition_id}"
    
    def _generate_authenticity_sources(self, tradition_id: str) -> List[Dict[str, Any]]:
        """Generate authenticity sources"""
        return [
            {
                "type": "historical",
                "source": f"Primary historical source for {tradition_id}",
                "reliability_score": 0.9
            }
        ]
    
    def _calculate_merkle_hash(self, tradition_id: str) -> str:
        """Calculate merkle hash for tradition"""
        return hashlib.sha256(f"{tradition_id}_{datetime.now().isoformat()}".encode()).hexdigest()
    
    def generate_all_traditions(self):
        """Generate comprehensive knowledge base for all 26 traditions"""
        print("️ Generating Comprehensive Knowledge Base for 26 Sacred Traditions")
        print("=" * 70)
        
        for tradition_id in self.traditions.keys():
            print(f" Generating {self.traditions[tradition_id]['name']}...")
            tradition_data = self.generate_tradition_content(tradition_id)
            
            # Save tradition data
            output_file = self.output_dir / f"{tradition_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(tradition_data), f, indent=2, ensure_ascii=False)
            
            print(f"✅ Completed {tradition_data.tradition_name}: {tradition_data.total_entries} entries")
        
        print("\n Knowledge Base Generation Complete!")
        print(f" Output directory: {self.output_dir}")

if __name__ == "__main__":
    generator = ComprehensiveKnowledgeGenerator()
    generator.generate_all_traditions()
