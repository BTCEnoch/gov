#!/usr/bin/env python3
"""
Enochian Cyphers Content Metrics Validator

Implements comprehensive content metrics validation and response count verification.
Addresses expert feedback Gap #7: Testing & Validation Infrastructure - 
"Build content metrics validation and verify claimed metrics (4,453 responses, 2,565 entries)".

This system provides:
- Verification of claimed metrics against actual repository state
- Content count validation across all traditions and governors
- Response count verification for interview data
- Quality metrics tracking and authenticity scoring
- Discrepancy identification and reporting

Maintains structural care by placing in /validation directory for comprehensive
system validation and metrics tracking.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContentMetrics:
    """Content metrics data structure"""
    metric_type: str
    claimed_count: int
    actual_count: int
    discrepancy: int
    accuracy_percentage: float
    validation_timestamp: str
    details: Dict[str, Any]

@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    report_id: str
    validation_timestamp: str
    total_metrics_validated: int
    passed_validations: int
    failed_validations: int
    overall_accuracy: float
    metrics: List[ContentMetrics]
    recommendations: List[str]
    sacred_constraints_compliance: bool

class ContentMetricsValidator:
    """Comprehensive content metrics validation system"""
    
    def __init__(self):
        self.lighthouse_dir = Path("lighthouse/complete_lighthouse")
        self.governor_profiles_dir = Path("governor_profiles")
        self.interviews_dir = Path("interviews")
        self.validation_dir = Path("validation/reports")
        self.validation_dir.mkdir(parents=True, exist_ok=True)
        
        # Expected metrics based on expert feedback and project claims
        self.expected_metrics = {
            "traditions": 26,
            "knowledge_entries": 2565,
            "governors": 91,
            "interview_responses": 4453,
            "aethyrs": 30,
            "ai_generated_quests": 9126,
            "authenticity_threshold": 0.958  # 95.8%
        }
        
        logger.info("Content Metrics Validator initialized")
    
    def validate_tradition_count(self) -> ContentMetrics:
        """Validate the count of sacred traditions"""
        logger.info("Validating tradition count")
        
        claimed_count = self.expected_metrics["traditions"]
        actual_count = 0
        details = {"traditions": []}
        
        if self.lighthouse_dir.exists():
            tradition_files = [f for f in self.lighthouse_dir.glob("*.json") 
                             if f.name != "lighthouse_master_index.json"]
            actual_count = len(tradition_files)
            details["traditions"] = [f.stem for f in tradition_files]
        
        discrepancy = actual_count - claimed_count
        accuracy = (min(actual_count, claimed_count) / max(actual_count, claimed_count)) * 100 if max(actual_count, claimed_count) > 0 else 0
        
        return ContentMetrics(
            metric_type="traditions",
            claimed_count=claimed_count,
            actual_count=actual_count,
            discrepancy=discrepancy,
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def validate_knowledge_entries(self) -> ContentMetrics:
        """Validate the count of knowledge entries across all traditions"""
        logger.info("Validating knowledge entries count")
        
        claimed_count = self.expected_metrics["knowledge_entries"]
        actual_count = 0
        details = {"tradition_counts": {}, "total_by_category": {}}
        
        if self.lighthouse_dir.exists():
            for tradition_file in self.lighthouse_dir.glob("*.json"):
                if tradition_file.name == "lighthouse_master_index.json":
                    continue
                
                with open(tradition_file, 'r', encoding='utf-8') as f:
                    tradition_data = json.load(f)
                
                tradition_name = tradition_data.get("tradition_info", {}).get("name", tradition_file.stem)
                entries = tradition_data.get("entries", [])
                entry_count = len(entries)
                
                actual_count += entry_count
                details["tradition_counts"][tradition_name] = entry_count
                
                # Categorize by tradition category
                category = tradition_data.get("tradition_info", {}).get("category", "unknown")
                if category not in details["total_by_category"]:
                    details["total_by_category"][category] = 0
                details["total_by_category"][category] += entry_count
        
        discrepancy = actual_count - claimed_count
        accuracy = (min(actual_count, claimed_count) / max(actual_count, claimed_count)) * 100 if max(actual_count, claimed_count) > 0 else 0
        
        return ContentMetrics(
            metric_type="knowledge_entries",
            claimed_count=claimed_count,
            actual_count=actual_count,
            discrepancy=discrepancy,
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def validate_governor_count(self) -> ContentMetrics:
        """Validate the count of Governor Angels"""
        logger.info("Validating governor count")
        
        claimed_count = self.expected_metrics["governors"]
        actual_count = 0
        details = {"governors": [], "aethyr_distribution": {}}
        
        if self.governor_profiles_dir.exists():
            governor_files = list(self.governor_profiles_dir.glob("*.json"))
            actual_count = len(governor_files)
            
            for governor_file in governor_files:
                governor_name = governor_file.stem
                details["governors"].append(governor_name)
                
                # Try to extract aethyr information
                try:
                    with open(governor_file, 'r', encoding='utf-8') as f:
                        governor_data = json.load(f)
                    
                    aethyr = governor_data.get("aethyr", "unknown")
                    if aethyr not in details["aethyr_distribution"]:
                        details["aethyr_distribution"][aethyr] = 0
                    details["aethyr_distribution"][aethyr] += 1
                except Exception as e:
                    logger.warning(f"Could not read governor file {governor_file}: {e}")
        
        discrepancy = actual_count - claimed_count
        accuracy = (min(actual_count, claimed_count) / max(actual_count, claimed_count)) * 100 if max(actual_count, claimed_count) > 0 else 0
        
        return ContentMetrics(
            metric_type="governors",
            claimed_count=claimed_count,
            actual_count=actual_count,
            discrepancy=discrepancy,
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def validate_interview_responses(self) -> ContentMetrics:
        """Validate the count of interview responses"""
        logger.info("Validating interview responses count")
        
        claimed_count = self.expected_metrics["interview_responses"]
        actual_count = 0
        details = {"response_sources": [], "governors_with_interviews": []}
        
        # Check multiple possible locations for interview data
        interview_locations = [
            self.interviews_dir,
            Path("interviews/governors"),
            self.governor_profiles_dir
        ]
        
        for location in interview_locations:
            if location.exists():
                details["response_sources"].append(str(location))
                
                for interview_file in location.glob("*.json"):
                    try:
                        with open(interview_file, 'r', encoding='utf-8') as f:
                            interview_data = json.load(f)
                        
                        # Count responses based on file structure
                        if isinstance(interview_data, list):
                            actual_count += len(interview_data)
                        elif isinstance(interview_data, dict):
                            # Check for interview responses in various formats
                            if "interview_responses" in interview_data:
                                responses = interview_data["interview_responses"]
                                if isinstance(responses, list):
                                    actual_count += len(responses)
                                elif isinstance(responses, dict):
                                    actual_count += len(responses)
                            elif "responses" in interview_data:
                                responses = interview_data["responses"]
                                if isinstance(responses, list):
                                    actual_count += len(responses)
                                elif isinstance(responses, dict):
                                    actual_count += len(responses)
                            else:
                                # Count top-level keys as potential responses
                                actual_count += len([k for k in interview_data.keys() 
                                                   if not k.startswith("_") and k != "metadata"])
                        
                        details["governors_with_interviews"].append(interview_file.stem)
                        
                    except Exception as e:
                        logger.warning(f"Could not read interview file {interview_file}: {e}")
        
        discrepancy = actual_count - claimed_count
        accuracy = (min(actual_count, claimed_count) / max(actual_count, claimed_count)) * 100 if max(actual_count, claimed_count) > 0 else 0
        
        return ContentMetrics(
            metric_type="interview_responses",
            claimed_count=claimed_count,
            actual_count=actual_count,
            discrepancy=discrepancy,
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def validate_aethyr_distribution(self) -> ContentMetrics:
        """Validate the distribution of governors across Aethyrs"""
        logger.info("Validating Aethyr distribution")
        
        claimed_count = self.expected_metrics["aethyrs"]
        actual_count = 0
        details = {"aethyr_counts": {}, "tex_governors": [], "distribution_valid": False}
        
        if self.governor_profiles_dir.exists():
            aethyr_counts = {}
            
            for governor_file in self.governor_profiles_dir.glob("*.json"):
                try:
                    with open(governor_file, 'r', encoding='utf-8') as f:
                        governor_data = json.load(f)
                    
                    aethyr = governor_data.get("aethyr", "unknown")
                    if aethyr != "unknown":
                        if aethyr not in aethyr_counts:
                            aethyr_counts[aethyr] = 0
                        aethyr_counts[aethyr] += 1
                        
                        if aethyr == "TEX":
                            details["tex_governors"].append(governor_file.stem)
                
                except Exception as e:
                    logger.warning(f"Could not read governor file {governor_file}: {e}")
            
            actual_count = len(aethyr_counts)
            details["aethyr_counts"] = aethyr_counts
            
            # Validate sacred distribution (TEX=4, others=3)
            tex_count = aethyr_counts.get("TEX", 0)
            other_counts = [count for aethyr, count in aethyr_counts.items() if aethyr != "TEX"]
            
            details["distribution_valid"] = (
                tex_count == 4 and 
                all(count == 3 for count in other_counts) and
                len(aethyr_counts) == 30
            )
        
        discrepancy = actual_count - claimed_count
        accuracy = (min(actual_count, claimed_count) / max(actual_count, claimed_count)) * 100 if max(actual_count, claimed_count) > 0 else 0
        
        return ContentMetrics(
            metric_type="aethyrs",
            claimed_count=claimed_count,
            actual_count=actual_count,
            discrepancy=discrepancy,
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def validate_authenticity_scores(self) -> ContentMetrics:
        """Validate authenticity scores across all content"""
        logger.info("Validating authenticity scores")
        
        claimed_threshold = self.expected_metrics["authenticity_threshold"]
        total_entries = 0
        high_authenticity_entries = 0
        details = {"tradition_authenticity": {}, "low_authenticity_entries": []}
        
        if self.lighthouse_dir.exists():
            for tradition_file in self.lighthouse_dir.glob("*.json"):
                if tradition_file.name == "lighthouse_master_index.json":
                    continue
                
                with open(tradition_file, 'r', encoding='utf-8') as f:
                    tradition_data = json.load(f)
                
                tradition_name = tradition_data.get("tradition_info", {}).get("name", tradition_file.stem)
                entries = tradition_data.get("entries", [])
                
                tradition_high_auth = 0
                tradition_total = len(entries)
                
                for entry in entries:
                    total_entries += 1
                    authenticity_score = entry.get("authenticity_score", 0.0)
                    
                    if authenticity_score >= claimed_threshold:
                        high_authenticity_entries += 1
                        tradition_high_auth += 1
                    else:
                        details["low_authenticity_entries"].append({
                            "tradition": tradition_name,
                            "entry_id": entry.get("id", "unknown"),
                            "score": authenticity_score
                        })
                
                if tradition_total > 0:
                    details["tradition_authenticity"][tradition_name] = {
                        "high_authenticity": tradition_high_auth,
                        "total": tradition_total,
                        "percentage": (tradition_high_auth / tradition_total) * 100
                    }
        
        actual_percentage = (high_authenticity_entries / total_entries) * 100 if total_entries > 0 else 0
        claimed_percentage = claimed_threshold * 100
        
        discrepancy = actual_percentage - claimed_percentage
        accuracy = (min(actual_percentage, claimed_percentage) / max(actual_percentage, claimed_percentage)) * 100 if max(actual_percentage, claimed_percentage) > 0 else 0
        
        return ContentMetrics(
            metric_type="authenticity_scores",
            claimed_count=int(claimed_percentage),
            actual_count=int(actual_percentage),
            discrepancy=int(discrepancy),
            accuracy_percentage=accuracy,
            validation_timestamp=datetime.now().isoformat(),
            details=details
        )
    
    def generate_comprehensive_report(self) -> ValidationReport:
        """Generate comprehensive validation report"""
        logger.info("Generating comprehensive validation report")
        
        # Run all validations
        validations = [
            self.validate_tradition_count(),
            self.validate_knowledge_entries(),
            self.validate_governor_count(),
            self.validate_interview_responses(),
            self.validate_aethyr_distribution(),
            self.validate_authenticity_scores()
        ]
        
        # Calculate overall statistics
        total_metrics = len(validations)
        passed_validations = sum(1 for v in validations if v.accuracy_percentage >= 90.0)
        failed_validations = total_metrics - passed_validations
        overall_accuracy = sum(v.accuracy_percentage for v in validations) / total_metrics if total_metrics > 0 else 0
        
        # Generate recommendations
        recommendations = []
        for validation in validations:
            if validation.accuracy_percentage < 90.0:
                if validation.metric_type == "interview_responses":
                    recommendations.append(f"Verify interview response count: claimed {validation.claimed_count}, found {validation.actual_count}")
                elif validation.metric_type == "authenticity_scores":
                    recommendations.append(f"Improve authenticity scores: {len(validation.details.get('low_authenticity_entries', []))} entries below threshold")
                else:
                    recommendations.append(f"Address {validation.metric_type} discrepancy: {validation.discrepancy}")
        
        # Check sacred constraints compliance
        sacred_compliance = (
            validations[0].actual_count == 26 and  # traditions
            validations[2].actual_count == 91 and  # governors
            validations[4].details.get("distribution_valid", False)  # aethyr distribution
        )
        
        # Create report
        report = ValidationReport(
            report_id=hashlib.sha256(f"validation_{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            validation_timestamp=datetime.now().isoformat(),
            total_metrics_validated=total_metrics,
            passed_validations=passed_validations,
            failed_validations=failed_validations,
            overall_accuracy=overall_accuracy,
            metrics=validations,
            recommendations=recommendations,
            sacred_constraints_compliance=sacred_compliance
        )
        
        # Save report
        report_file = self.validation_dir / f"content_metrics_report_{report.report_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation report saved: {report_file}")
        return report

def main():
    """Main execution function"""
    logger.info("=== ENOCHIAN CYPHERS CONTENT METRICS VALIDATOR ===")
    
    # Initialize validator
    validator = ContentMetricsValidator()
    
    # Generate comprehensive report
    report = validator.generate_comprehensive_report()
    
    # Display results
    logger.info(f"\n=== VALIDATION RESULTS ===")
    logger.info(f"Total Metrics Validated: {report.total_metrics_validated}")
    logger.info(f"Passed Validations: {report.passed_validations}")
    logger.info(f"Failed Validations: {report.failed_validations}")
    logger.info(f"Overall Accuracy: {report.overall_accuracy:.1f}%")
    logger.info(f"Sacred Constraints Compliance: {report.sacred_constraints_compliance}")
    
    logger.info(f"\n=== DETAILED METRICS ===")
    for metric in report.metrics:
        logger.info(f"{metric.metric_type}: {metric.actual_count}/{metric.claimed_count} ({metric.accuracy_percentage:.1f}%)")
    
    if report.recommendations:
        logger.info(f"\n=== RECOMMENDATIONS ===")
        for i, rec in enumerate(report.recommendations, 1):
            logger.info(f"{i}. {rec}")
    
    return validator

if __name__ == "__main__":
    main()
