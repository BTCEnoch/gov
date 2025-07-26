#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse Validation & Completion Script

Validates the enhanced lighthouse knowledge base against expert specifications:
- Ensures all 26 sacred traditions are present and properly structured
- Validates JSON schema compliance
- Checks content completeness (25+ entries per required array)
- Estimates Bitcoin L1 inscription size (<1MB requirement)
- Generates comprehensive status report

Based on expert feedback for complete knowledge base structure.
"""

import json
import os
import gzip
from typing import Dict, List, Any, Tuple
from datetime import datetime

class LighthouseValidator:
    def __init__(self, traditions_dir: str = "lighthouse/traditions"):
        self.traditions_dir = traditions_dir
        self.enhanced_dir = os.path.join(traditions_dir, "enhanced")
        
        # Expert-specified 26 Sacred Traditions
        self.required_traditions = [
            # MAGICK SYSTEMS (7)
            "enochian_magic", "hermetic_qabalah", "thelema", "celtic_druidic", 
            "chaos_magic", "alchemy", "golden_dawn",
            
            # PHILOSOPHY (6) 
            "taoism", "traditional_kabbalah", "sufism", "gnosticism", 
            "norse_traditions", "greek_philosophy",
            
            # DIVINATION SYSTEMS (6)
            "tarot", "i_ching", "astrology", "egyptian_magic", 
            "shamanism", "numerology",
            
            # SCIENCE & REALITY (7)
            "sacred_geometry", "quantum_physics", "kuji_kiri", "greek_mythology",
            "digital_physics", "m_theory", "natal_astrology"  # Adding missing 26th
        ]
        
        self.required_structure = {
            "tradition_id": str,
            "tradition_name": str, 
            "category": str,
            "overview": str,
            "historical_context": str,
            "core_principles": list,
            "practices": list,
            "sub_practices": list,
            "cross_tradition_connections": list,
            "governor_applications": dict,
            "authenticity_sources": list
        }
        
        self.minimum_counts = {
            "core_principles": 25,
            "practices": 25,
            "sub_practices": 25,
            "cross_tradition_connections": 25,
            "authenticity_sources": 10
        }

    def validate_tradition_structure(self, tradition_data: Dict) -> Tuple[bool, List[str]]:
        """Validate tradition follows required JSON structure"""
        errors = []
        
        # Check required top-level fields
        for field, expected_type in self.required_structure.items():
            if field not in tradition_data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(tradition_data[field], expected_type):
                errors.append(f"Field {field} should be {expected_type.__name__}, got {type(tradition_data[field]).__name__}")
        
        # Check minimum array lengths
        for field, min_count in self.minimum_counts.items():
            if field in tradition_data and isinstance(tradition_data[field], list):
                actual_count = len(tradition_data[field])
                if actual_count < min_count:
                    errors.append(f"{field} has {actual_count} entries, requires minimum {min_count}")
        
        # Validate core_principles structure
        if "core_principles" in tradition_data:
            for i, principle in enumerate(tradition_data["core_principles"]):
                if not isinstance(principle, dict):
                    errors.append(f"core_principles[{i}] should be object")
                else:
                    required_fields = ["name", "description", "practical_applications", "related_concepts"]
                    for field in required_fields:
                        if field not in principle:
                            errors.append(f"core_principles[{i}] missing {field}")
        
        # Validate practices structure  
        if "practices" in tradition_data:
            for i, practice in enumerate(tradition_data["practices"]):
                if not isinstance(practice, dict):
                    errors.append(f"practices[{i}] should be object")
                else:
                    required_fields = ["name", "type", "description", "instructions", "prerequisites", "benefits", "warnings"]
                    for field in required_fields:
                        if field not in practice:
                            errors.append(f"practices[{i}] missing {field}")
        
        return len(errors) == 0, errors

    def estimate_inscription_size(self, tradition_data: Dict) -> int:
        """Estimate compressed size for Bitcoin L1 inscription"""
        json_str = json.dumps(tradition_data, separators=(',', ':'))
        json_bytes = json_str.encode('utf-8')
        compressed = gzip.compress(json_bytes)
        return len(compressed)

    def validate_all_traditions(self) -> Dict[str, Any]:
        """Comprehensive validation of all enhanced traditions"""
        print("🔍 Validating Enochian Cyphers Lighthouse Enhancement...")
        
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "total_required": len(self.required_traditions),
            "traditions_found": 0,
            "traditions_valid": 0,
            "total_size_bytes": 0,
            "total_size_mb": 0.0,
            "bitcoin_compliant": False,
            "missing_traditions": [],
            "invalid_traditions": [],
            "tradition_details": {},
            "summary": {}
        }
        
        # Check each required tradition
        for tradition_id in self.required_traditions:
            tradition_path = os.path.join(self.enhanced_dir, f"{tradition_id}_enhanced.json")
            
            if not os.path.exists(tradition_path):
                validation_results["missing_traditions"].append(tradition_id)
                print(f"❌ Missing: {tradition_id}")
                continue
            
            try:
                with open(tradition_path, 'r', encoding='utf-8') as f:
                    tradition_data = json.load(f)
                
                validation_results["traditions_found"] += 1
                
                # Validate structure
                is_valid, errors = self.validate_tradition_structure(tradition_data)
                
                # Estimate size
                size_bytes = self.estimate_inscription_size(tradition_data)
                validation_results["total_size_bytes"] += size_bytes
                
                tradition_detail = {
                    "valid": is_valid,
                    "errors": errors,
                    "size_bytes": size_bytes,
                    "size_kb": round(size_bytes / 1024, 2),
                    "core_principles_count": len(tradition_data.get("core_principles", [])),
                    "practices_count": len(tradition_data.get("practices", [])),
                    "sub_practices_count": len(tradition_data.get("sub_practices", [])),
                    "cross_connections_count": len(tradition_data.get("cross_tradition_connections", [])),
                    "authenticity_sources_count": len(tradition_data.get("authenticity_sources", []))
                }
                
                validation_results["tradition_details"][tradition_id] = tradition_detail
                
                if is_valid:
                    validation_results["traditions_valid"] += 1
                    print(f"✅ Valid: {tradition_id} ({tradition_detail['size_kb']}kb)")
                else:
                    validation_results["invalid_traditions"].append({
                        "tradition": tradition_id,
                        "errors": errors
                    })
                    print(f"⚠️  Invalid: {tradition_id} - {len(errors)} errors")
                    
            except Exception as e:
                validation_results["invalid_traditions"].append({
                    "tradition": tradition_id,
                    "errors": [f"JSON parsing error: {str(e)}"]
                })
                print(f"❌ Error: {tradition_id} - {str(e)}")
        
        # Calculate totals
        validation_results["total_size_mb"] = round(validation_results["total_size_bytes"] / (1024 * 1024), 2)
        validation_results["bitcoin_compliant"] = validation_results["total_size_mb"] < 1.0
        
        # Generate summary
        validation_results["summary"] = {
            "completion_percentage": round((validation_results["traditions_found"] / validation_results["total_required"]) * 100, 1),
            "validity_percentage": round((validation_results["traditions_valid"] / max(validation_results["traditions_found"], 1)) * 100, 1),
            "bitcoin_ready": validation_results["bitcoin_compliant"],
            "missing_count": len(validation_results["missing_traditions"]),
            "invalid_count": len(validation_results["invalid_traditions"])
        }
        
        return validation_results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive validation report"""
        report = f"""
# Enochian Cyphers Lighthouse Validation Report
Generated: {results['timestamp']}

## Summary
- **Traditions Found**: {results['traditions_found']}/{results['total_required']} ({results['summary']['completion_percentage']}%)
- **Valid Traditions**: {results['traditions_valid']}/{results['traditions_found']} ({results['summary']['validity_percentage']}%)
- **Total Size**: {results['total_size_mb']} MB
- **Bitcoin L1 Compliant**: {'✅ Yes' if results['bitcoin_compliant'] else '❌ No (>1MB)'}

## Missing Traditions ({len(results['missing_traditions'])})
"""
        for tradition in results['missing_traditions']:
            report += f"- {tradition}\n"
        
        report += f"\n## Invalid Traditions ({len(results['invalid_traditions'])})\n"
        for invalid in results['invalid_traditions']:
            report += f"- **{invalid['tradition']}**: {len(invalid['errors'])} errors\n"
            for error in invalid['errors'][:3]:  # Show first 3 errors
                report += f"  - {error}\n"
        
        report += "\n## Tradition Details\n"
        for tradition_id, details in results['tradition_details'].items():
            status = "✅" if details['valid'] else "❌"
            report += f"- {status} **{tradition_id}** ({details['size_kb']}kb)\n"
            report += f"  - Core Principles: {details['core_principles_count']}\n"
            report += f"  - Practices: {details['practices_count']}\n"
            report += f"  - Sub-Practices: {details['sub_practices_count']}\n"
            report += f"  - Cross-Connections: {details['cross_connections_count']}\n"
            report += f"  - Authenticity Sources: {details['authenticity_sources_count']}\n"
        
        report += f"""
## Next Steps
1. {'✅' if results['summary']['missing_count'] == 0 else '❌'} Create missing traditions
2. {'✅' if results['summary']['invalid_count'] == 0 else '❌'} Fix validation errors
3. {'✅' if results['bitcoin_compliant'] else '❌'} Optimize for <1MB Bitcoin inscription
4. 🔄 Expand [EXPAND] placeholders with authentic content
5. 🔄 Integrate with TAP Protocol for hypertoken evolution
"""
        return report

    def create_missing_tradition(self, tradition_id: str):
        """Create missing tradition with basic structure"""
        print(f"🔧 Creating missing tradition: {tradition_id}")
        
        # Determine category
        categories = {
            "natal_astrology": "divination"
        }
        
        tradition_data = {
            "tradition_id": tradition_id,
            "tradition_name": tradition_id.replace("_", " ").title(),
            "category": categories.get(tradition_id, "science"),
            "overview": f"[EXPAND: Overview of {tradition_id} tradition]",
            "historical_context": f"[EXPAND: Historical context of {tradition_id}]",
            "core_principles": [{"name": f"Principle {i+1}", "description": "[EXPAND]", "practical_applications": ["[EXPAND]"], "related_concepts": ["[EXPAND]"]} for i in range(25)],
            "practices": [{"name": f"Practice {i+1}", "type": "study", "description": "[EXPAND]", "instructions": "[EXPAND]", "prerequisites": ["[EXPAND]"], "benefits": ["[EXPAND]"], "warnings": ["[EXPAND]"]} for i in range(25)],
            "sub_practices": [{"name": f"Sub-Practice {i+1}", "parent_practice": f"Practice {(i%5)+1}", "description": "[EXPAND]", "specialization_level": "intermediate", "unique_aspects": ["[EXPAND]"]} for i in range(25)],
            "cross_tradition_connections": [{"connected_tradition": "hermetic_qabalah", "connection_type": "complementary", "description": "[EXPAND]"} for i in range(25)],
            "governor_applications": {
                "personality_influences": ["[EXPAND]"],
                "decision_making_patterns": ["[EXPAND]"],
                "communication_styles": ["[EXPAND]"],
                "quest_generation_themes": ["[EXPAND]"]
            },
            "authenticity_sources": [{"type": "historical", "source": "[EXPAND]", "reliability_score": 0.9} for i in range(10)]
        }
        
        output_path = os.path.join(self.enhanced_dir, f"{tradition_id}_enhanced.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tradition_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {tradition_id}_enhanced.json")

if __name__ == "__main__":
    validator = LighthouseValidator()
    
    # Run validation
    results = validator.validate_all_traditions()
    
    # Create missing traditions
    for missing_tradition in results["missing_traditions"]:
        validator.create_missing_tradition(missing_tradition)
    
    # Generate and save report
    report = validator.generate_report(results)
    
    with open("lighthouse_validation_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📊 Validation Complete!")
    print(f"📄 Report saved to: lighthouse_validation_report.md")
    print(f"🎯 Status: {results['traditions_found']}/{results['total_required']} traditions, {results['total_size_mb']}MB")
