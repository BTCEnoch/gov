#!/usr/bin/env python3
"""
Enochian Cyphers Dynamic Lighthouse Retrieval Engine

Implements weighted knowledge retrieval system with 60% Enochian base weighting,
O(1) indexing, and dynamic blending for authentic quest content generation.

This addresses expert feedback Phase 1: "Optimize Lighthouse for Weighted, Dynamic Retrieval"
- Weighted sampling with 60% Enochian priority
- O(1) retrieval via pre-built indexes
- Source citation embedding for authenticity
- Dynamic domain blending for Governor specializations
- Real-time authenticity scoring integration

Maintains structural care by placing in /lighthouse directory for knowledge
base components and retrieval systems.
"""

import json
import random
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WeightedKnowledgeEntry:
    """Knowledge entry with weighting and authenticity metadata"""
    id: str
    tradition: str
    name: str
    category: str
    summary: str
    description: str
    historical_context: str
    practical_applications: List[str]
    cross_references: List[str]
    prerequisites: List[str]
    benefits: List[str]
    warnings: List[str]
    difficulty_level: str
    authenticity_score: float
    sources: List[str]
    enochian_weight: float  # 0.0 to 1.0 based on Enochian content
    domain_relevance: Dict[str, float]  # Governor domain relevance scores
    retrieval_priority: float  # Combined weighting for retrieval
    citation_metadata: Dict[str, Any]

@dataclass
class RetrievalQuery:
    """Query parameters for weighted retrieval"""
    governor_domain: str
    num_entries: int = 30
    enochian_weight: float = 0.6
    min_authenticity: float = 0.8
    difficulty_levels: List[str] = None
    categories: List[str] = None
    exclude_traditions: List[str] = None

@dataclass
class RetrievalResult:
    """Result of weighted knowledge retrieval"""
    query: RetrievalQuery
    entries: List[WeightedKnowledgeEntry]
    total_available: int
    enochian_percentage: float
    average_authenticity: float
    domain_coverage: Dict[str, int]
    retrieval_metadata: Dict[str, Any]

class DynamicLighthouseRetriever:
    """Dynamic weighted retrieval engine for Lighthouse knowledge base"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.master_index = {}
        self.weighted_entries = {}
        self.domain_indexes = {}
        self.enochian_index = {}
        self.authenticity_index = {}
        self.citation_index = {}
        
        # Load and index all knowledge
        self._load_master_index()
        self._build_weighted_entries()
        self._build_retrieval_indexes()
        
        logger.info(f"Dynamic Lighthouse Retriever initialized with {len(self.weighted_entries)} entries")
    
    def _load_master_index(self):
        """Load master index from lighthouse"""
        index_path = self.lighthouse_path / "lighthouse_master_index.json"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                self.master_index = json.load(f)
            logger.info(f"Loaded master index: {self.master_index.get('total_entries', 0)} entries")
        else:
            logger.error(f"Master index not found at {index_path}")
    
    def _build_weighted_entries(self):
        """Build weighted entries from all tradition files"""
        traditions = self.master_index.get('traditions', {})

        for tradition_id, tradition_info in traditions.items():
            # Handle both absolute and relative paths
            file_path_str = tradition_info['file_path']
            if file_path_str.startswith('complete_lighthouse/'):
                # Path is relative to lighthouse directory
                file_path = self.lighthouse_path / file_path_str.replace('complete_lighthouse/', '')
            else:
                # Path is relative to current directory
                file_path = Path(file_path_str)

            if file_path.exists():
                self._process_tradition_file(tradition_id, file_path)
            else:
                logger.warning(f"Tradition file not found: {file_path}")

        logger.info(f"Built {len(self.weighted_entries)} weighted entries")
    
    def _process_tradition_file(self, tradition_id: str, file_path: Path):
        """Process individual tradition file and create weighted entries"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)

            entries = tradition_data.get('entries', [])
            logger.info(f"Processing {len(entries)} entries from {tradition_id}")

            for i, entry in enumerate(entries):
                if isinstance(entry, dict):
                    weighted_entry = self._create_weighted_entry(tradition_id, entry)
                    self.weighted_entries[weighted_entry.id] = weighted_entry
                else:
                    logger.warning(f"Skipping non-dict entry at index {i} in {tradition_id}: {type(entry)}")

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def _create_weighted_entry(self, tradition_id: str, entry: Dict) -> WeightedKnowledgeEntry:
        """Create weighted entry with Enochian scoring and domain relevance"""
        try:
            # Calculate Enochian weight based on content analysis
            enochian_weight = self._calculate_enochian_weight(entry)

            # Calculate domain relevance for different governor specializations
            domain_relevance = self._calculate_domain_relevance(entry)

            # Calculate retrieval priority (combines Enochian weight, authenticity, domain relevance)
            retrieval_priority = self._calculate_retrieval_priority(entry, enochian_weight, domain_relevance)

            # Build citation metadata
            citation_metadata = self._build_citation_metadata(entry)

            # Ensure all required fields have defaults
            entry_id = entry.get('id', f"{tradition_id}_{abs(hash(str(entry.get('name', 'unknown'))))}")

            return WeightedKnowledgeEntry(
                id=entry_id,
                tradition=tradition_id,
                name=entry.get('name', 'Unknown'),
                category=entry.get('category', 'unknown'),
                summary=entry.get('summary', ''),
                description=entry.get('description', ''),
                historical_context=entry.get('historical_context', ''),
                practical_applications=entry.get('practical_applications', []) if isinstance(entry.get('practical_applications'), list) else [],
                cross_references=entry.get('cross_references', []) if isinstance(entry.get('cross_references'), list) else [],
                prerequisites=entry.get('prerequisites', []) if isinstance(entry.get('prerequisites'), list) else [],
                benefits=entry.get('benefits', []) if isinstance(entry.get('benefits'), list) else [],
                warnings=entry.get('warnings', []) if isinstance(entry.get('warnings'), list) else [],
                difficulty_level=entry.get('difficulty_level', 'intermediate'),
                authenticity_score=float(entry.get('authenticity_score', 0.85)),
                sources=entry.get('sources', []) if isinstance(entry.get('sources'), list) else [],
                enochian_weight=enochian_weight,
                domain_relevance=domain_relevance,
                retrieval_priority=retrieval_priority,
                citation_metadata=citation_metadata
            )
        except Exception as e:
            logger.error(f"Error creating weighted entry for {tradition_id}: {e}")
            logger.error(f"Entry data: {entry}")
            raise
    
    def _calculate_enochian_weight(self, entry: Dict) -> float:
        """Calculate Enochian weight based on content analysis"""
        content = f"{entry.get('name', '')} {entry.get('description', '')} {entry.get('summary', '')}"
        
        # Enochian keywords with weights
        enochian_keywords = {
            'enochian': 1.0, 'aethyr': 0.9, 'governor': 0.8, 'angel': 0.7,
            'dee': 0.8, 'kelley': 0.7, 'watchtower': 0.9, 'tablet': 0.8,
            'sigil': 0.6, 'invocation': 0.7, 'scrying': 0.6, 'vision': 0.5,
            'elemental': 0.4, 'planetary': 0.4, 'sephiroth': 0.3, 'qabalah': 0.3
        }
        
        total_weight = 0.0
        word_count = len(content.split())
        
        for keyword, weight in enochian_keywords.items():
            count = len(re.findall(rf'\b{keyword}\b', content.lower()))
            if count > 0:
                total_weight += (count / word_count) * weight
        
        # Boost for Enochian tradition
        if entry.get('tradition') == 'enochian_magic':
            total_weight += 0.5
        
        return min(1.0, total_weight)
    
    def _calculate_domain_relevance(self, entry: Dict) -> Dict[str, float]:
        """Calculate relevance to different governor domains"""
        content = f"{entry.get('name', '')} {entry.get('description', '')} {entry.get('summary', '')}"
        
        # Domain keywords mapping
        domain_keywords = {
            'knowledge': ['wisdom', 'learning', 'study', 'understanding', 'insight'],
            'protection': ['guard', 'shield', 'defend', 'protect', 'safety'],
            'transformation': ['change', 'evolve', 'transform', 'mutation', 'growth'],
            'divination': ['prophecy', 'vision', 'foresight', 'oracle', 'scrying'],
            'healing': ['heal', 'cure', 'restore', 'balance', 'harmony'],
            'creation': ['create', 'manifest', 'build', 'form', 'generate'],
            'destruction': ['destroy', 'banish', 'dissolve', 'end', 'break'],
            'communication': ['speak', 'communicate', 'message', 'word', 'language']
        }
        
        relevance = {}
        for domain, keywords in domain_keywords.items():
            score = 0.0
            for keyword in keywords:
                count = len(re.findall(rf'\b{keyword}\b', content.lower()))
                score += count * 0.1
            relevance[domain] = min(1.0, score)
        
        return relevance
    
    def _calculate_retrieval_priority(self, entry: Dict, enochian_weight: float, domain_relevance: Dict[str, float]) -> float:
        """Calculate overall retrieval priority"""
        authenticity = entry.get('authenticity_score', 0.85)
        max_domain_relevance = max(domain_relevance.values()) if domain_relevance else 0.0
        
        # Weighted combination: 40% Enochian, 30% authenticity, 30% domain relevance
        priority = (enochian_weight * 0.4) + (authenticity * 0.3) + (max_domain_relevance * 0.3)
        return priority
    
    def _build_citation_metadata(self, entry: Dict) -> Dict[str, Any]:
        """Build citation metadata for authenticity tracking"""
        return {
            'primary_sources': entry.get('sources', []),
            'cross_references': entry.get('cross_references', []),
            'historical_period': self._extract_historical_period(entry.get('historical_context', '')),
            'authenticity_markers': self._extract_authenticity_markers(entry),
            'citation_quality': self._assess_citation_quality(entry.get('sources', []))
        }
    
    def _extract_historical_period(self, context: str) -> str:
        """Extract historical period from context"""
        # Simple pattern matching for common periods
        periods = {
            r'16th century|1500s|1582|1589': '16th_century',
            r'17th century|1600s': '17th_century', 
            r'18th century|1700s': '18th_century',
            r'19th century|1800s': '19th_century',
            r'20th century|1900s': '20th_century',
            r'ancient|classical': 'ancient',
            r'medieval|middle ages': 'medieval',
            r'renaissance': 'renaissance'
        }
        
        for pattern, period in periods.items():
            if re.search(pattern, context.lower()):
                return period
        return 'unknown'
    
    def _extract_authenticity_markers(self, entry: Dict) -> List[str]:
        """Extract authenticity markers from entry"""
        markers = []
        content = f"{entry.get('description', '')} {entry.get('historical_context', '')}"
        
        # Look for specific authenticity indicators
        if 'john dee' in content.lower() or 'edward kelley' in content.lower():
            markers.append('primary_source_attribution')
        if 'liber' in content.lower() or 'manuscript' in content.lower():
            markers.append('manuscript_reference')
        if any(year in content for year in ['1582', '1583', '1584', '1589']):
            markers.append('historical_dating')
        if 'spiritual diaries' in content.lower():
            markers.append('diary_reference')
        
        return markers
    
    def _assess_citation_quality(self, sources: List[str]) -> str:
        """Assess quality of citations"""
        if not sources:
            return 'none'
        
        primary_indicators = ['dee', 'kelley', 'manuscript', 'original', 'primary']
        secondary_indicators = ['scholar', 'academic', 'research', 'study']
        
        has_primary = any(any(indicator in source.lower() for indicator in primary_indicators) for source in sources)
        has_secondary = any(any(indicator in source.lower() for indicator in secondary_indicators) for source in sources)
        
        if has_primary and len(sources) >= 3:
            return 'excellent'
        elif has_primary:
            return 'good'
        elif has_secondary:
            return 'fair'
        else:
            return 'basic'

    def _build_retrieval_indexes(self):
        """Build O(1) retrieval indexes for efficient querying"""
        logger.info("Building retrieval indexes...")

        # Build Enochian index (entries with high Enochian weight)
        self.enochian_index = {
            entry_id: entry for entry_id, entry in self.weighted_entries.items()
            if entry.enochian_weight >= 0.3
        }

        # Build domain indexes
        for entry_id, entry in self.weighted_entries.items():
            for domain, relevance in entry.domain_relevance.items():
                if relevance >= 0.2:  # Threshold for domain relevance
                    if domain not in self.domain_indexes:
                        self.domain_indexes[domain] = {}
                    self.domain_indexes[domain][entry_id] = entry

        # Build authenticity index (high-quality entries)
        self.authenticity_index = {
            entry_id: entry for entry_id, entry in self.weighted_entries.items()
            if entry.authenticity_score >= 0.8
        }

        # Build citation index (well-sourced entries)
        self.citation_index = {
            entry_id: entry for entry_id, entry in self.weighted_entries.items()
            if entry.citation_metadata['citation_quality'] in ['excellent', 'good']
        }

        logger.info(f"Built indexes: Enochian={len(self.enochian_index)}, "
                   f"Domains={len(self.domain_indexes)}, "
                   f"Authenticity={len(self.authenticity_index)}, "
                   f"Citations={len(self.citation_index)}")

    def weighted_knowledge_retrieval(self, query: RetrievalQuery) -> RetrievalResult:
        """Main weighted retrieval method implementing expert guidance"""
        logger.info(f"Retrieving knowledge for domain: {query.governor_domain}")

        # Get candidate pools
        enochian_candidates = list(self.enochian_index.values())
        domain_candidates = list(self.domain_indexes.get(query.governor_domain, {}).values())

        # Filter by authenticity and other criteria
        enochian_candidates = self._filter_candidates(enochian_candidates, query)
        domain_candidates = self._filter_candidates(domain_candidates, query)

        # Calculate target counts based on weighting
        enochian_count = int(query.num_entries * query.enochian_weight)
        domain_count = query.num_entries - enochian_count

        # Sample weighted entries
        selected_entries = []

        # Sample Enochian entries (60% by default)
        if enochian_candidates and enochian_count > 0:
            enochian_sample = self._weighted_sample(
                enochian_candidates,
                min(enochian_count, len(enochian_candidates)),
                weight_key='retrieval_priority'
            )
            selected_entries.extend(enochian_sample)

        # Sample domain-specific entries (40% by default)
        if domain_candidates and domain_count > 0:
            # Remove already selected entries to avoid duplicates
            available_domain = [e for e in domain_candidates if e.id not in [se.id for se in selected_entries]]
            if available_domain:
                domain_sample = self._weighted_sample(
                    available_domain,
                    min(domain_count, len(available_domain)),
                    weight_key='retrieval_priority'
                )
                selected_entries.extend(domain_sample)

        # Fill remaining slots if needed
        if len(selected_entries) < query.num_entries:
            remaining_needed = query.num_entries - len(selected_entries)
            all_candidates = list(self.weighted_entries.values())
            available_remaining = [e for e in all_candidates if e.id not in [se.id for se in selected_entries]]
            available_remaining = self._filter_candidates(available_remaining, query)

            if available_remaining:
                additional_sample = self._weighted_sample(
                    available_remaining,
                    min(remaining_needed, len(available_remaining)),
                    weight_key='retrieval_priority'
                )
                selected_entries.extend(additional_sample)

        # Calculate result metadata
        enochian_percentage = len([e for e in selected_entries if e.enochian_weight >= 0.3]) / len(selected_entries) * 100 if selected_entries else 0
        average_authenticity = sum(e.authenticity_score for e in selected_entries) / len(selected_entries) if selected_entries else 0

        domain_coverage = {}
        for entry in selected_entries:
            for domain, relevance in entry.domain_relevance.items():
                if relevance >= 0.2:
                    domain_coverage[domain] = domain_coverage.get(domain, 0) + 1

        retrieval_metadata = {
            'query_timestamp': datetime.now().isoformat(),
            'total_candidates': len(enochian_candidates) + len(domain_candidates),
            'enochian_candidates': len(enochian_candidates),
            'domain_candidates': len(domain_candidates),
            'selection_method': 'weighted_priority_sampling',
            'authenticity_threshold': query.min_authenticity
        }

        return RetrievalResult(
            query=query,
            entries=selected_entries,
            total_available=len(self.weighted_entries),
            enochian_percentage=enochian_percentage,
            average_authenticity=average_authenticity,
            domain_coverage=domain_coverage,
            retrieval_metadata=retrieval_metadata
        )

    def _filter_candidates(self, candidates: List[WeightedKnowledgeEntry], query: RetrievalQuery) -> List[WeightedKnowledgeEntry]:
        """Filter candidates based on query criteria"""
        filtered = candidates

        # Filter by authenticity
        if query.min_authenticity:
            filtered = [e for e in filtered if e.authenticity_score >= query.min_authenticity]

        # Filter by difficulty levels
        if query.difficulty_levels:
            filtered = [e for e in filtered if e.difficulty_level in query.difficulty_levels]

        # Filter by categories
        if query.categories:
            filtered = [e for e in filtered if e.category in query.categories]

        # Exclude traditions
        if query.exclude_traditions:
            filtered = [e for e in filtered if e.tradition not in query.exclude_traditions]

        return filtered

    def _weighted_sample(self, candidates: List[WeightedKnowledgeEntry], count: int, weight_key: str) -> List[WeightedKnowledgeEntry]:
        """Perform weighted sampling based on specified weight key"""
        if not candidates or count <= 0:
            return []

        # Extract weights
        weights = [getattr(entry, weight_key) for entry in candidates]

        # Handle edge case where all weights are 0
        if sum(weights) == 0:
            return random.sample(candidates, min(count, len(candidates)))

        # Weighted random sampling
        selected = []
        available = candidates.copy()
        available_weights = weights.copy()

        for _ in range(min(count, len(available))):
            if not available:
                break

            # Normalize weights
            total_weight = sum(available_weights)
            if total_weight == 0:
                # Fallback to random selection
                idx = random.randint(0, len(available) - 1)
            else:
                # Weighted selection
                rand_val = random.uniform(0, total_weight)
                cumulative = 0
                idx = 0
                for i, weight in enumerate(available_weights):
                    cumulative += weight
                    if rand_val <= cumulative:
                        idx = i
                        break

            selected.append(available.pop(idx))
            available_weights.pop(idx)

        return selected

    def get_retrieval_statistics(self) -> Dict[str, Any]:
        """Get comprehensive retrieval statistics"""
        total_entries = len(self.weighted_entries)

        # Enochian statistics
        high_enochian = len([e for e in self.weighted_entries.values() if e.enochian_weight >= 0.5])
        medium_enochian = len([e for e in self.weighted_entries.values() if 0.2 <= e.enochian_weight < 0.5])

        # Authenticity statistics
        high_auth = len([e for e in self.weighted_entries.values() if e.authenticity_score >= 0.9])
        medium_auth = len([e for e in self.weighted_entries.values() if 0.8 <= e.authenticity_score < 0.9])

        # Domain coverage
        domain_stats = {}
        for domain in self.domain_indexes:
            domain_stats[domain] = len(self.domain_indexes[domain])

        # Citation quality distribution
        citation_stats = {}
        for entry in self.weighted_entries.values():
            quality = entry.citation_metadata['citation_quality']
            citation_stats[quality] = citation_stats.get(quality, 0) + 1

        return {
            'total_entries': total_entries,
            'enochian_distribution': {
                'high_weight': high_enochian,
                'medium_weight': medium_enochian,
                'percentage_high': (high_enochian / total_entries * 100) if total_entries > 0 else 0
            },
            'authenticity_distribution': {
                'high_score': high_auth,
                'medium_score': medium_auth,
                'percentage_high': (high_auth / total_entries * 100) if total_entries > 0 else 0
            },
            'domain_coverage': domain_stats,
            'citation_quality': citation_stats,
            'index_sizes': {
                'enochian_index': len(self.enochian_index),
                'domain_indexes': {k: len(v) for k, v in self.domain_indexes.items()},
                'authenticity_index': len(self.authenticity_index),
                'citation_index': len(self.citation_index)
            }
        }

    def export_weighted_entries(self, output_path: str = "lighthouse/weighted_entries_export.json"):
        """Export weighted entries for analysis"""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_entries': len(self.weighted_entries),
            'retrieval_statistics': self.get_retrieval_statistics(),
            'weighted_entries': {
                entry_id: asdict(entry) for entry_id, entry in self.weighted_entries.items()
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported weighted entries to {output_path}")

def test_dynamic_retrieval():
    """Test the dynamic retrieval system"""
    logger.info("=== TESTING DYNAMIC LIGHTHOUSE RETRIEVAL ===")

    # Initialize retriever
    retriever = DynamicLighthouseRetriever()

    # Test queries for different governor domains
    test_queries = [
        RetrievalQuery(governor_domain="knowledge", num_entries=20, enochian_weight=0.6),
        RetrievalQuery(governor_domain="protection", num_entries=15, enochian_weight=0.7),
        RetrievalQuery(governor_domain="divination", num_entries=25, enochian_weight=0.5),
        RetrievalQuery(governor_domain="transformation", num_entries=30, min_authenticity=0.9)
    ]

    results = []
    for query in test_queries:
        logger.info(f"\nTesting query: {query.governor_domain} domain")
        result = retriever.weighted_knowledge_retrieval(query)
        results.append(result)

        logger.info(f"Retrieved {len(result.entries)} entries")
        logger.info(f"Enochian percentage: {result.enochian_percentage:.1f}%")
        logger.info(f"Average authenticity: {result.average_authenticity:.3f}")
        logger.info(f"Domain coverage: {result.domain_coverage}")

    # Display overall statistics
    stats = retriever.get_retrieval_statistics()
    logger.info(f"\n=== RETRIEVAL SYSTEM STATISTICS ===")
    logger.info(f"Total entries indexed: {stats['total_entries']}")
    logger.info(f"High Enochian weight entries: {stats['enochian_distribution']['high_weight']} ({stats['enochian_distribution']['percentage_high']:.1f}%)")
    logger.info(f"High authenticity entries: {stats['authenticity_distribution']['high_score']} ({stats['authenticity_distribution']['percentage_high']:.1f}%)")
    logger.info(f"Domain coverage: {stats['domain_coverage']}")
    logger.info(f"Citation quality: {stats['citation_quality']}")

    # Export results
    retriever.export_weighted_entries()

    # Test performance (O(1) retrieval)
    import time
    start_time = time.time()
    for _ in range(100):
        query = RetrievalQuery(governor_domain="knowledge", num_entries=10)
        retriever.weighted_knowledge_retrieval(query)
    end_time = time.time()

    avg_time = (end_time - start_time) / 100
    logger.info(f"\nPerformance test: Average retrieval time: {avg_time:.4f} seconds")
    logger.info(f"Retrieval rate: {1/avg_time:.1f} queries/second")

    return retriever, results

if __name__ == "__main__":
    test_dynamic_retrieval()
