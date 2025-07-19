"""
Enochian Cyphers Data Integrity Validation System
Comprehensive validation for mystical entries, Governor Angels, and cross-references
"""

import json
import jsonschema
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import re
from datetime import datetime

@dataclass
class ValidationResult:
    """Result of data validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    authenticity_score: float
    completeness_score: float
    
    def to_dict(self) -> Dict:
        return {
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'suggestions': self.suggestions,
            'authenticity_score': self.authenticity_score,
            'completeness_score': self.completeness_score
        }

class DataIntegrityValidator:
    """Comprehensive data integrity validation system"""
    
    def __init__(self, schema_dir: str = "core/lighthouse/schemas"):
        self.schema_dir = Path(schema_dir)
        self.schemas = self._load_schemas()
        self.tradition_requirements = self._define_tradition_requirements()
        
    def _load_schemas(self) -> Dict[str, Dict]:
        """Load all JSON schemas"""
        schemas = {}
        schema_files = {
            'mystical_entry': 'mystical_entry_schema.json',
            'governor_angel': 'governor_angel_schema.json',
            'cross_reference': 'cross_reference_schema.json'
        }
        
        for schema_name, filename in schema_files.items():
            schema_path = self.schema_dir / filename
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schemas[schema_name] = json.load(f)
        
        return schemas
    
    def _define_tradition_requirements(self) -> Dict[str, Dict]:
        """Define minimum requirements for each tradition based on research"""
        return {
            'enochian_magic': {
                'min_entries': 30,  # 30 Aethyrs minimum
                'required_concepts': ['aethyr', 'governor', 'enochian_key', 'sigil'],
                'authenticity_sources': ['john_dee', 'liber_chanokh', 'five_books_mystery']
            },
            'i_ching': {
                'min_entries': 64,  # 64 hexagrams
                'required_concepts': ['hexagram', 'trigram', 'yin_yang', 'judgment'],
                'authenticity_sources': ['wilhelm_translation', 'book_of_changes']
            },
            'hermetic_qabalah': {
                'min_entries': 10,  # 10 Sephiroth minimum
                'required_concepts': ['sephirah', 'tree_of_life', 'path', 'correspondence'],
                'authenticity_sources': ['golden_dawn', 'regardie', 'hermetic_tradition']
            },
            'tarot': {
                'min_entries': 78,  # 78 cards
                'required_concepts': ['major_arcana', 'minor_arcana', 'suit', 'symbolism'],
                'authenticity_sources': ['rider_waite_smith', 'traditional_meanings']
            },
            'egyptian_magic': {
                'min_entries': 20,  # Major deities and practices
                'required_concepts': ['deity', 'heka', 'papyrus', 'hieroglyph'],
                'authenticity_sources': ['egyptian_papyri', 'historical_records']
            },
            'celtic_druidic': {
                'min_entries': 20,  # Ogham letters and practices
                'required_concepts': ['ogham', 'tree', 'seasonal_cycle', 'druid'],
                'authenticity_sources': ['ogham_stones', 'celtic_mythology']
            },
            'norse_traditions': {
                'min_entries': 15,  # Nine Worlds and major concepts
                'required_concepts': ['nine_worlds', 'rune', 'yggdrasil', 'aesir'],
                'authenticity_sources': ['prose_edda', 'poetic_edda', 'archaeological']
            },
            'taoism': {
                'min_entries': 15,  # Core principles and practices
                'required_concepts': ['dao', 'wu_wei', 'yin_yang', 'five_elements'],
                'authenticity_sources': ['dao_de_jing', 'zhuangzi', 'traditional_texts']
            },
            'kuji_kiri': {
                'min_entries': 9,   # Nine hand seals
                'required_concepts': ['mudra', 'syllable', 'meditation', 'protection'],
                'authenticity_sources': ['shugendo', 'buddhist_texts', 'ninja_traditions']
            },
            'chaos_magic': {
                'min_entries': 10,  # Core techniques and concepts
                'required_concepts': ['sigil', 'gnosis', 'paradigm', 'belief'],
                'authenticity_sources': ['peter_carroll', 'austin_spare', 'modern_practitioners']
            },
            'thelema': {
                'min_entries': 12,  # Core principles and practices
                'required_concepts': ['true_will', 'book_of_law', 'aiwass', 'magick'],
                'authenticity_sources': ['crowley_writings', 'book_of_law', 'aa_curriculum']
            },
            'sacred_geometry': {
                'min_entries': 8,   # Platonic solids and key ratios
                'required_concepts': ['platonic_solid', 'golden_ratio', 'fibonacci', 'proportion'],
                'authenticity_sources': ['mathematical_proofs', 'historical_architecture']
            },
            'quantum_physics': {
                'min_entries': 10,  # Key quantum concepts
                'required_concepts': ['observer_effect', 'consciousness', 'entanglement', 'superposition'],
                'authenticity_sources': ['peer_reviewed', 'stanford_encyclopedia', 'academic_sources']
            },
            'alchemy': {
                'min_entries': 12,  # Great Work stages and principles
                'required_concepts': ['great_work', 'transmutation', 'prima_materia', 'philosopher_stone'],
                'authenticity_sources': ['medieval_texts', 'paracelsus', 'hermetic_principles']
            },
            'natal_chart_astrology': {
                'min_entries': 20,  # Zodiac signs, planets, houses, and aspects
                'required_concepts': ['natal_chart', 'birth_time', 'planetary_positions', 'house_system', 'aspect_patterns'],
                'authenticity_sources': ['classical_astrology', 'ptolemy', 'traditional_sources', 'modern_natal_interpretation']
            },
            'shamanism': {
                'min_entries': 15,  # Cross-cultural practices
                'required_concepts': ['altered_state', 'spirit_guide', 'journey', 'healing'],
                'authenticity_sources': ['anthropological', 'ethnographic', 'cross_cultural']
            },
            'traditional_kabbalah': {
                'min_entries': 15,  # Sephiroth and key concepts
                'required_concepts': ['sephirah', 'zohar', 'ein_sof', 'tikkun_olam'],
                'authenticity_sources': ['hebrew_texts', 'zohar', 'scholarly_kabbalah']
            },
            'sufism': {
                'min_entries': 15,  # Masters and practices
                'required_concepts': ['dhikr', 'fana', 'tariqa', 'sufi_master'],
                'authenticity_sources': ['islamic_texts', 'sufi_masters', 'traditional_lineages']
            },
            'gnosticism': {
                'min_entries': 18,  # Aeons, archons, and key concepts
                'required_concepts': ['gnosis', 'pleroma', 'demiurge', 'aeon', 'archon', 'sophia'],
                'authenticity_sources': ['nag_hammadi', 'early_christian_texts', 'gnostic_gospels', 'scholarly_sources']
            },
            'greek_mythology': {
                'min_entries': 25,  # Gods, heroes, and major myths
                'required_concepts': ['olympian_gods', 'titans', 'heroes', 'creation_myths', 'underworld'],
                'authenticity_sources': ['homer', 'hesiod', 'classical_sources', 'mythological_compendiums']
            }
        }
    
    def validate_mystical_entry(self, entry_data: Dict) -> ValidationResult:
        """Validate a mystical entry against schema and content requirements"""
        errors = []
        warnings = []
        suggestions = []
        
        # Schema validation
        try:
            jsonschema.validate(entry_data, self.schemas['mystical_entry'])
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        
        # Content validation
        tradition = entry_data.get('tradition', '')
        if tradition in self.tradition_requirements:
            req = self.tradition_requirements[tradition]
            
            # Check required concepts
            content = entry_data.get('full_content', '').lower()
            tags = [tag.lower() for tag in entry_data.get('tags', [])]
            
            missing_concepts = []
            for concept in req['required_concepts']:
                if concept not in content and concept not in tags:
                    missing_concepts.append(concept)
            
            if missing_concepts:
                warnings.append(f"Missing key concepts for {tradition}: {missing_concepts}")
        
        # Authenticity validation
        authenticity = entry_data.get('authenticity', {})
        auth_score = authenticity.get('validation_score', 0.0)
        
        if auth_score < 0.9:
            warnings.append(f"Low authenticity score: {auth_score}. Consider additional source validation.")
        
        # Content quality checks
        content_length = len(entry_data.get('full_content', ''))
        if content_length < 100:
            errors.append("Content too short. Minimum 100 characters required.")
        elif content_length < 300:
            warnings.append("Content relatively short. Consider expanding for better context.")
        
        # Cross-reference validation
        cross_refs = entry_data.get('cross_references', {})
        related_entries = cross_refs.get('related_entries', [])
        
        # Validate entry ID format
        entry_id = entry_data.get('id', '')
        if not re.match(r'^[a-z0-9_]+_[0-9]{3}$', entry_id):
            errors.append(f"Invalid entry ID format: {entry_id}")
        
        # Calculate completeness score
        completeness_factors = [
            bool(entry_data.get('title')),
            bool(entry_data.get('summary')),
            bool(entry_data.get('full_content')),
            bool(entry_data.get('tags')),
            bool(authenticity.get('primary_source')),
            bool(cross_refs.get('related_entries')),
            auth_score > 0.8,
            content_length > 300
        ]
        completeness_score = sum(completeness_factors) / len(completeness_factors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            authenticity_score=auth_score,
            completeness_score=completeness_score
        )
    
    def validate_governor_angel(self, governor_data: Dict) -> ValidationResult:
        """Validate a Governor Angel against schema and requirements"""
        errors = []
        warnings = []
        suggestions = []
        
        # Schema validation
        try:
            jsonschema.validate(governor_data, self.schemas['governor_angel'])
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        
        # Governor-specific validation
        governor_id = governor_data.get('id', 0)
        if not (1 <= governor_id <= 91):
            errors.append(f"Invalid Governor ID: {governor_id}. Must be 1-91.")
        
        # Aethyr association validation
        aethyr_assoc = governor_data.get('aethyr_association', {})
        aethyr_num = aethyr_assoc.get('aethyr_number', 0)
        if not (1 <= aethyr_num <= 30):
            errors.append(f"Invalid Aethyr number: {aethyr_num}. Must be 1-30.")
        
        # Questline validation
        questline = governor_data.get('questline', {})
        total_quests = questline.get('total_quests', 0)
        if not (75 <= total_quests <= 125):
            warnings.append(f"Quest count {total_quests} outside recommended range (75-125).")
        
        # Tradition validation
        primary_tradition = governor_data.get('primary_tradition', '')
        if primary_tradition not in self.tradition_requirements:
            errors.append(f"Unknown primary tradition: {primary_tradition}")
        
        # Hypertoken validation
        hypertoken = governor_data.get('hypertoken_attributes', {})
        base_traits = hypertoken.get('base_traits', [])
        if len(base_traits) < 3:
            warnings.append("Governor should have at least 3 base traits for hypertoken.")
        
        # Calculate authenticity score based on Enochian validation
        metadata = governor_data.get('metadata', {})
        auth_validated = metadata.get('authenticity_validated', False)
        auth_score = 1.0 if auth_validated else 0.5
        
        # Calculate completeness score
        completeness_factors = [
            bool(governor_data.get('name')),
            bool(governor_data.get('core_wisdom')),
            bool(governor_data.get('personality_traits')),
            bool(questline.get('difficulty_progression')),
            bool(hypertoken.get('base_traits')),
            bool(aethyr_assoc.get('aethyr_name')),
            len(base_traits) >= 3,
            75 <= total_quests <= 125
        ]
        completeness_score = sum(completeness_factors) / len(completeness_factors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            authenticity_score=auth_score,
            completeness_score=completeness_score
        )
    
    def validate_cross_references(self, cross_ref_data: Dict) -> ValidationResult:
        """Validate cross-reference system integrity"""
        errors = []
        warnings = []
        suggestions = []
        
        # Schema validation
        try:
            jsonschema.validate(cross_ref_data, self.schemas['cross_reference'])
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        
        # Validate tradition mappings
        tradition_mappings = cross_ref_data.get('tradition_mappings', {})
        for tradition, mapping in tradition_mappings.items():
            if tradition in self.tradition_requirements:
                req = self.tradition_requirements[tradition]
                entry_count = mapping.get('total_entries', 0)
                
                if entry_count < req['min_entries']:
                    warnings.append(
                        f"Tradition {tradition} has {entry_count} entries, "
                        f"minimum recommended: {req['min_entries']}"
                    )
        
        # Validate knowledge graph integrity
        knowledge_graph = cross_ref_data.get('knowledge_graph', {})
        nodes = knowledge_graph.get('nodes', [])
        edges = knowledge_graph.get('edges', [])
        
        # Check for orphaned nodes
        node_ids = {node['id'] for node in nodes}
        referenced_ids = set()
        for edge in edges:
            referenced_ids.add(edge['source'])
            referenced_ids.add(edge['target'])
        
        orphaned_nodes = node_ids - referenced_ids
        if orphaned_nodes:
            warnings.append(f"Orphaned nodes detected: {list(orphaned_nodes)[:5]}...")
        
        # Check for broken references
        broken_refs = referenced_ids - node_ids
        if broken_refs:
            errors.append(f"Broken references detected: {list(broken_refs)[:5]}...")
        
        # Calculate metrics
        validation_metrics = cross_ref_data.get('validation_metrics', {})
        avg_auth_score = validation_metrics.get('average_authenticity_score', 0.0)
        
        completeness_factors = [
            bool(tradition_mappings),
            bool(knowledge_graph),
            len(nodes) > 0,
            len(edges) > 0,
            avg_auth_score > 0.8,
            len(orphaned_nodes) == 0,
            len(broken_refs) == 0
        ]
        completeness_score = sum(completeness_factors) / len(completeness_factors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            authenticity_score=avg_auth_score,
            completeness_score=completeness_score
        )
    
    def validate_complete_dataset(self, data_dir: str) -> Dict[str, ValidationResult]:
        """Validate complete dataset for integrity and completeness"""
        results = {}
        
        # This would iterate through all data files and validate them
        # Implementation would depend on actual data file structure
        
        return results
    
    def generate_validation_report(self, results: Dict[str, ValidationResult]) -> Dict:
        """Generate comprehensive validation report"""
        total_items = len(results)
        valid_items = sum(1 for r in results.values() if r.is_valid)
        
        avg_auth_score = sum(r.authenticity_score for r in results.values()) / total_items if total_items > 0 else 0
        avg_completeness = sum(r.completeness_score for r in results.values()) / total_items if total_items > 0 else 0
        
        all_errors = []
        all_warnings = []
        for result in results.values():
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
        
        return {
            'summary': {
                'total_items': total_items,
                'valid_items': valid_items,
                'validation_rate': valid_items / total_items if total_items > 0 else 0,
                'average_authenticity_score': avg_auth_score,
                'average_completeness_score': avg_completeness
            },
            'errors': {
                'total_errors': len(all_errors),
                'unique_errors': list(set(all_errors)),
                'most_common_errors': self._get_most_common(all_errors)
            },
            'warnings': {
                'total_warnings': len(all_warnings),
                'unique_warnings': list(set(all_warnings)),
                'most_common_warnings': self._get_most_common(all_warnings)
            },
            'recommendations': self._generate_recommendations(results),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_most_common(self, items: List[str], limit: int = 5) -> List[Tuple[str, int]]:
        """Get most common items with counts"""
        from collections import Counter
        return Counter(items).most_common(limit)
    
    def _generate_recommendations(self, results: Dict[str, ValidationResult]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Analyze common issues and suggest improvements
        low_auth_count = sum(1 for r in results.values() if r.authenticity_score < 0.9)
        if low_auth_count > len(results) * 0.2:
            recommendations.append(
                "Consider reviewing primary sources for entries with low authenticity scores."
            )
        
        low_completeness_count = sum(1 for r in results.values() if r.completeness_score < 0.8)
        if low_completeness_count > len(results) * 0.3:
            recommendations.append(
                "Focus on completing missing fields and cross-references for better integration."
            )
        
        return recommendations
