#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: Content Indexing and Mapping System
Utility base for indexing, searching, and mapping all lighthouse content
"""

import json
import re
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict

@dataclass
class ContentEntry:
    """Indexed content entry"""
    id: str
    tradition: str
    name: str
    category: str
    keywords: List[str]
    description: str
    cross_references: List[str]
    file_path: str
    authenticity_score: float

@dataclass
class SearchResult:
    """Search result with relevance scoring"""
    entry: ContentEntry
    relevance_score: float
    match_type: str  # exact, keyword, description, cross_reference
    matched_terms: List[str]

@dataclass
class TraditionMap:
    """Tradition mapping with relationships"""
    name: str
    category: str
    entry_count: int
    related_traditions: List[str]
    key_concepts: List[str]
    difficulty_distribution: Dict[str, int]

class ContentIndexer:
    """Complete content indexing and mapping system"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.content_index: Dict[str, ContentEntry] = {}
        self.keyword_index: Dict[str, Set[str]] = defaultdict(set)
        self.tradition_maps: Dict[str, TraditionMap] = {}
        self.cross_reference_graph: Dict[str, Set[str]] = defaultdict(set)
        self.category_index: Dict[str, Set[str]] = defaultdict(set)
        
        self._build_index()
    
    def _build_index(self) -> None:
        """Build complete content index from lighthouse files"""
        print(" Building lighthouse content index...")
        
        # Load master index
        master_index_file = self.lighthouse_path / "lighthouse_master_index.json"
        if master_index_file.exists():
            with open(master_index_file, 'r', encoding='utf-8') as f:
                master_index = json.load(f)
            
            traditions = master_index.get("traditions", {})
        else:
            # Fallback: scan directory for tradition files
            traditions = self._scan_tradition_files()
        
        # Index each tradition
        for tradition_name, tradition_info in traditions.items():
            self._index_tradition(tradition_name, tradition_info)
        
        # Build cross-reference graph
        self._build_cross_reference_graph()
        
        # Build tradition maps
        self._build_tradition_maps()
        
        print(f"✅ Indexed {len(self.content_index)} entries across {len(self.tradition_maps)} traditions")
    
    def _scan_tradition_files(self) -> Dict[str, Dict]:
        """Scan directory for tradition files"""
        traditions = {}
        for file_path in self.lighthouse_path.glob("*.json"):
            if file_path.name != "lighthouse_master_index.json":
                tradition_name = file_path.stem
                traditions[tradition_name] = {
                    "display_name": tradition_name.replace("_", " ").title(),
                    "file_path": str(file_path)
                }
        return traditions
    
    def _index_tradition(self, tradition_name: str, tradition_info: Dict) -> None:
        """Index all entries in a tradition"""
        tradition_file = self.lighthouse_path / f"{tradition_name}.json"
        
        if not tradition_file.exists():
            print(f"⚠️ Tradition file not found: {tradition_file}")
            return
        
        try:
            with open(tradition_file, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            entries = tradition_data.get("entries", [])
            for entry_data in entries:
                content_entry = ContentEntry(
                    id=entry_data["id"],
                    tradition=tradition_name,
                    name=entry_data["name"],
                    category=entry_data.get("category", "concept"),
                    keywords=self._extract_keywords(entry_data),
                    description=entry_data.get("description", ""),
                    cross_references=entry_data.get("cross_references", []),
                    file_path=str(tradition_file),
                    authenticity_score=entry_data.get("authenticity_score", 0.8)
                )
                
                # Add to main index
                self.content_index[content_entry.id] = content_entry
                
                # Add to keyword index
                for keyword in content_entry.keywords:
                    self.keyword_index[keyword.lower()].add(content_entry.id)
                
                # Add to category index
                self.category_index[content_entry.category].add(content_entry.id)
                
        except Exception as e:
            print(f"⚠️ Error indexing {tradition_name}: {e}")
    
    def _extract_keywords(self, entry_data: Dict) -> List[str]:
        """Extract keywords from entry data"""
        keywords = []
        
        # Explicit keywords
        if "keywords" in entry_data:
            keywords.extend(entry_data["keywords"])
        
        # Extract from name
        name_words = re.findall(r'\b\w+\b', entry_data.get("name", ""))
        keywords.extend([word.lower() for word in name_words if len(word) > 3])
        
        # Extract from practical applications
        if "practical_applications" in entry_data:
            for app in entry_data["practical_applications"]:
                app_words = re.findall(r'\b\w+\b', app)
                keywords.extend([word.lower() for word in app_words if len(word) > 4])
        
        # Extract from benefits
        if "benefits" in entry_data:
            for benefit in entry_data["benefits"]:
                benefit_words = re.findall(r'\b\w+\b', benefit)
                keywords.extend([word.lower() for word in benefit_words if len(word) > 4])
        
        # Remove duplicates and common words
        stop_words = {"the", "and", "for", "with", "this", "that", "from", "they", "have", "been", "will"}
        keywords = list(set([kw for kw in keywords if kw not in stop_words]))
        
        return keywords[:20]  # Limit to top 20 keywords
    
    def _build_cross_reference_graph(self) -> None:
        """Build cross-reference relationship graph"""
        for entry in self.content_index.values():
            for ref in entry.cross_references:
                self.cross_reference_graph[entry.tradition].add(ref)
                self.cross_reference_graph[ref].add(entry.tradition)
    
    def _build_tradition_maps(self) -> None:
        """Build tradition relationship maps"""
        tradition_stats = defaultdict(lambda: {
            "entries": [],
            "categories": defaultdict(int),
            "difficulties": defaultdict(int)
        })
        
        # Collect statistics
        for entry in self.content_index.values():
            tradition_stats[entry.tradition]["entries"].append(entry)
            tradition_stats[entry.tradition]["categories"][entry.category] += 1
        
        # Build tradition maps
        for tradition_name, stats in tradition_stats.items():
            # Get tradition category from master index or infer
            tradition_category = self._infer_tradition_category(tradition_name)
            
            # Get related traditions from cross-references
            related_traditions = list(self.cross_reference_graph[tradition_name])
            
            # Extract key concepts (most common keywords)
            all_keywords = []
            for entry in stats["entries"]:
                all_keywords.extend(entry.keywords)
            
            keyword_counts = defaultdict(int)
            for keyword in all_keywords:
                keyword_counts[keyword] += 1
            
            key_concepts = [kw for kw, count in sorted(keyword_counts.items(), 
                                                     key=lambda x: x[1], reverse=True)[:10]]
            
            tradition_map = TraditionMap(
                name=tradition_name,
                category=tradition_category,
                entry_count=len(stats["entries"]),
                related_traditions=related_traditions,
                key_concepts=key_concepts,
                difficulty_distribution=dict(stats["difficulties"])
            )
            
            self.tradition_maps[tradition_name] = tradition_map
    
    def _infer_tradition_category(self, tradition_name: str) -> str:
        """Infer tradition category from name"""
        magick_systems = ["enochian", "hermetic", "thelema", "golden_dawn", "chaos", "alchemy", "celtic"]
        philosophy = ["taoism", "kabbalah", "sufism", "gnosticism", "greek_philosophy", "shamanism"]
        divination = ["tarot", "i_ching", "astrology", "natal", "numerology", "kuji"]
        science = ["quantum", "digital", "m_theory", "sacred_geometry", "norse", "egyptian", "greek_mythology"]
        
        tradition_lower = tradition_name.lower()
        
        if any(term in tradition_lower for term in magick_systems):
            return "magick_systems"
        elif any(term in tradition_lower for term in philosophy):
            return "philosophy"
        elif any(term in tradition_lower for term in divination):
            return "divination_systems"
        elif any(term in tradition_lower for term in science):
            return "science_reality"
        else:
            return "universal"
    
    def search(self, query: str, limit: int = 20, min_relevance: float = 0.1) -> List[SearchResult]:
        """Search content with relevance scoring"""
        query_terms = [term.lower().strip() for term in re.findall(r'\b\w+\b', query)]
        results = []
        
        for entry in self.content_index.values():
            relevance_score, match_type, matched_terms = self._calculate_relevance(entry, query_terms)
            
            if relevance_score >= min_relevance:
                result = SearchResult(
                    entry=entry,
                    relevance_score=relevance_score,
                    match_type=match_type,
                    matched_terms=matched_terms
                )
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, entry: ContentEntry, query_terms: List[str]) -> Tuple[float, str, List[str]]:
        """Calculate relevance score for entry"""
        score = 0.0
        match_type = "none"
        matched_terms = []
        
        # Exact name match (highest score)
        if any(term in entry.name.lower() for term in query_terms):
            score += 1.0
            match_type = "exact"
            matched_terms.extend([term for term in query_terms if term in entry.name.lower()])
        
        # Keyword matches
        keyword_matches = [term for term in query_terms if term in [kw.lower() for kw in entry.keywords]]
        if keyword_matches:
            score += 0.8 * len(keyword_matches) / len(query_terms)
            if match_type == "none":
                match_type = "keyword"
            matched_terms.extend(keyword_matches)
        
        # Description matches
        description_matches = [term for term in query_terms if term in entry.description.lower()]
        if description_matches:
            score += 0.5 * len(description_matches) / len(query_terms)
            if match_type == "none":
                match_type = "description"
            matched_terms.extend(description_matches)
        
        # Cross-reference matches
        cross_ref_matches = [term for term in query_terms if any(term in ref.lower() for ref in entry.cross_references)]
        if cross_ref_matches:
            score += 0.3 * len(cross_ref_matches) / len(query_terms)
            if match_type == "none":
                match_type = "cross_reference"
            matched_terms.extend(cross_ref_matches)
        
        # Boost by authenticity score
        score *= entry.authenticity_score
        
        return score, match_type, list(set(matched_terms))
    
    def get_tradition_map(self, tradition_name: str) -> Optional[TraditionMap]:
        """Get tradition relationship map"""
        return self.tradition_maps.get(tradition_name)
    
    def get_related_content(self, entry_id: str, limit: int = 10) -> List[ContentEntry]:
        """Get content related to specific entry"""
        if entry_id not in self.content_index:
            return []
        
        entry = self.content_index[entry_id]
        related = []
        
        # Find entries with shared keywords
        for other_entry in self.content_index.values():
            if other_entry.id == entry_id:
                continue
            
            shared_keywords = set(entry.keywords) & set(other_entry.keywords)
            if shared_keywords:
                related.append((other_entry, len(shared_keywords)))
        
        # Sort by number of shared keywords
        related.sort(key=lambda x: x[1], reverse=True)
        
        return [entry for entry, _ in related[:limit]]
    
    def get_tradition_overview(self) -> Dict[str, Any]:
        """Get complete tradition overview"""
        overview = {
            "total_entries": len(self.content_index),
            "total_traditions": len(self.tradition_maps),
            "categories": {},
            "top_keywords": [],
            "cross_reference_density": 0
        }
        
        # Category breakdown
        for category, entry_ids in self.category_index.items():
            overview["categories"][category] = len(entry_ids)
        
        # Top keywords across all content
        all_keywords = []
        for entry in self.content_index.values():
            all_keywords.extend(entry.keywords)
        
        keyword_counts = defaultdict(int)
        for keyword in all_keywords:
            keyword_counts[keyword] += 1
        
        overview["top_keywords"] = [kw for kw, count in sorted(keyword_counts.items(), 
                                                              key=lambda x: x[1], reverse=True)[:20]]
        
        # Cross-reference density
        total_refs = sum(len(refs) for refs in self.cross_reference_graph.values())
        overview["cross_reference_density"] = total_refs / len(self.tradition_maps) if self.tradition_maps else 0
        
        return overview
    
    def export_index(self, filename: str) -> None:
        """Export complete index to file"""
        export_data = {
            "content_index": {entry_id: asdict(entry) for entry_id, entry in self.content_index.items()},
            "tradition_maps": {name: asdict(tmap) for name, tmap in self.tradition_maps.items()},
            "overview": self.get_tradition_overview(),
            "export_timestamp": self._get_timestamp()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f" Index exported to: {filename}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

if __name__ == "__main__":
    # Example usage
    indexer = ContentIndexer()
    
    # Search example
    results = indexer.search("tarot divination cards")
    print(f"Found {len(results)} results for 'tarot divination cards'")
    
    for result in results[:3]:
        print(f"- {result.entry.name} (Score: {result.relevance_score:.2f})")
    
    # Get tradition overview
    overview = indexer.get_tradition_overview()
    print(f"\nLighthouse Overview:")
    print(f"Total entries: {overview['total_entries']}")
    print(f"Total traditions: {overview['total_traditions']}")
    print(f"Top keywords: {', '.join(overview['top_keywords'][:5])}")
