"""
Risk Analyzer

Advanced risk assessment system that analyzes security risks, maintenance burden,
and other project risks using pattern recognition and threat modeling.
"""

import asyncio
import logging
import numpy as np
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import hashlib

from .predictive_intelligence import PredictionResult, PredictionType, PredictionConfidence

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk severity levels."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(Enum):
    """Categories of risks that can be analyzed."""
    SECURITY_VULNERABILITY = "security_vulnerability"
    MAINTENANCE_BURDEN = "maintenance_burden"
    DEPENDENCY_RISK = "dependency_risk"
    COMPLIANCE_RISK = "compliance_risk"
    OPERATIONAL_RISK = "operational_risk"
    DATA_RISK = "data_risk"


@dataclass
class RiskAssessment:
    """Detailed risk assessment with quantified analysis."""
    category: RiskCategory
    risk_level: RiskLevel
    probability: float
    impact_score: float
    risk_score: float  # probability * impact
    affected_components: List[str]
    mitigation_strategies: List[str]
    time_to_mitigation: str  # estimated time to implement mitigations


class RiskAnalyzer:
    """
    Comprehensive risk analysis system using security patterns, dependency analysis,
    and maintenance metrics to assess project risks.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the risk analyzer."""
        self.config = config or {}
        self.risk_patterns = self._load_risk_patterns()
        self.security_rules = self._initialize_security_rules()
        self.risk_weights = self._initialize_risk_weights()
    
    def _load_risk_patterns(self) -> Dict[str, Dict]:
        """Load known risk patterns and indicators."""
        return {
            "security_patterns": {
                "sql_injection_risk": {
                    "indicators": ["dynamic_sql", "string_concatenation_queries", "user_input_queries"],
                    "severity_multiplier": 3.0,
                    "common_in": ["web-app", "api-service"]
                },
                "xss_risk": {
                    "indicators": ["user_content_rendering", "dynamic_html", "unescaped_output"],
                    "severity_multiplier": 2.5,
                    "common_in": ["web-app", "frontend"]
                },
                "authentication_bypass": {
                    "indicators": ["weak_session_management", "insecure_tokens", "missing_auth"],
                    "severity_multiplier": 4.0,
                    "common_in": ["web-app", "api-service", "mobile-app"]
                },
                "data_exposure": {
                    "indicators": ["logging_sensitive_data", "error_message_leaks", "debug_enabled"],
                    "severity_multiplier": 3.5,
                    "common_in": ["all"]
                }
            },
            "dependency_patterns": {
                "outdated_dependencies": {
                    "risk_factors": ["age_months", "known_vulnerabilities", "maintenance_status"],
                    "severity_multiplier": 2.0
                },
                "license_conflicts": {
                    "risk_factors": ["incompatible_licenses", "gpl_viral", "commercial_restrictions"],
                    "severity_multiplier": 1.5
                },
                "supply_chain_risk": {
                    "risk_factors": ["unmaintained_packages", "single_maintainer", "typosquatting"],
                    "severity_multiplier": 2.5
                }
            },
            "maintenance_patterns": {
                "code_complexity": {
                    "thresholds": {"low": 5, "medium": 10, "high": 20},
                    "multiplier": 1.5
                },
                "technical_debt": {
                    "indicators": ["code_duplication", "quick_fixes", "documentation_gaps"],
                    "multiplier": 2.0
                },
                "team_knowledge_risk": {
                    "indicators": ["single_point_of_failure", "poor_documentation", "complex_logic"],
                    "multiplier": 2.5
                }
            }
        }
    
    def _initialize_security_rules(self) -> Dict[str, Dict]:
        """Initialize security analysis rules."""
        return {
            "input_validation": {
                "weight": 0.8,
                "checks": ["sanitization", "validation", "encoding"]
            },
            "authentication": {
                "weight": 0.9,
                "checks": ["strong_auth", "session_management", "access_control"]
            },
            "data_protection": {
                "weight": 0.8,
                "checks": ["encryption", "secure_storage", "transmission_security"]
            },
            "error_handling": {
                "weight": 0.6,
                "checks": ["secure_errors", "logging_security", "information_disclosure"]
            },
            "dependency_security": {
                "weight": 0.7,
                "checks": ["vulnerability_scanning", "update_frequency", "license_compliance"]
            }
        }
    
    def _initialize_risk_weights(self) -> Dict[str, float]:
        """Initialize weights for different risk factors."""
        return {
            "security_score": 0.35,
            "complexity": 0.20,
            "dependencies": 0.20,
            "maintenance": 0.15,
            "team_factors": 0.10
        }
    
    async def analyze_risks(self, project_context: Dict[str, Any], 
                          timeline: str) -> List[PredictionResult]:
        """
        Analyze comprehensive project risks.
        
        Args:
            project_context: Current project state and metrics
            timeline: Risk assessment timeline
            
        Returns:
            List of risk predictions
        """
        logger.info("Analyzing project risks...")
        
        predictions = []
        
        try:
            # Run risk analyses in parallel
            risk_tasks = [
                self._analyze_security_risks(project_context, timeline),
                self._analyze_maintenance_risks(project_context, timeline),
                self._analyze_dependency_risks(project_context, timeline),
                self._analyze_operational_risks(project_context, timeline)
            ]
            
            risk_results = await asyncio.gather(*risk_tasks, return_exceptions=True)
            
            # Process results
            for result in risk_results:
                if isinstance(result, PredictionResult):
                    predictions.append(result)
                elif isinstance(result, list):
                    predictions.extend(result)
                elif isinstance(result, Exception):
                    logger.warning(f"Risk analysis failed: {result}")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return []
    
    async def _analyze_security_risks(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Analyze security vulnerabilities and risks."""
        try:
            health_metrics = project_context.get("health_metrics", {})
            project_type = project_context.get("project_type", "web-app")
            frameworks = project_context.get("frameworks_detected", {})
            
            factors = []
            risk_score = 0.0
            
            # Security score analysis
            security_score = health_metrics.get("security", 0.8)
            if security_score < 0.7:
                security_impact = (0.7 - security_score) * 2
                risk_score += security_impact * 0.4
                factors.append(f"Low security score ({security_score:.1%})")
            
            # Project type specific risks
            type_risks = {
                "web-app": ["XSS", "CSRF", "SQL injection", "Authentication bypass"],
                "api-service": ["Injection attacks", "Broken authentication", "Data exposure"],
                "mobile-app": ["Insecure data storage", "Weak encryption", "API security"],
                "ai-project": ["Model poisoning", "Data privacy", "Algorithmic bias"]
            }
            
            project_risk_factors = type_risks.get(project_type, ["General security risks"])
            risk_score += len(project_risk_factors) * 0.05
            factors.append(f"Project type risks: {', '.join(project_risk_factors[:2])}")
            
            # Framework-specific security considerations
            risky_frameworks = {"express": 0.1, "flask": 0.1, "django": 0.05}
            for framework, confidence in frameworks.items():
                if framework in risky_frameworks:
                    framework_risk = risky_frameworks[framework] * confidence
                    risk_score += framework_risk
                    factors.append(f"Framework security considerations: {framework}")
            
            # Dependency security (simulated based on count)
            complexity_metrics = project_context.get("complexity_metrics", {})
            dependency_count = complexity_metrics.get("dependency_count", 20)
            if dependency_count > 50:
                dep_risk = min(0.3, (dependency_count - 50) / 200)
                risk_score += dep_risk
                factors.append(f"High dependency count increases attack surface ({dependency_count})")
            
            # Authentication and authorization risks
            if project_type in ["web-app", "api-service", "mobile-app"]:
                # Assume auth complexity based on project size
                loc = complexity_metrics.get("lines_of_code", 10000)
                if loc > 30000:  # Larger projects likely have complex auth
                    risk_score += 0.2
                    factors.append("Complex authentication requirements in large application")
            
            # Data handling risks
            if project_type in ["web-app", "api-service", "ai-project"]:
                risk_score += 0.15
                factors.append("Data handling and privacy compliance requirements")
            
            probability = min(0.90, risk_score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = self._calculate_security_severity(probability, project_type)
            
            return PredictionResult(
                prediction_type=PredictionType.SECURITY_RISK,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Security risks identified with {probability:.1%} likelihood of issues",
                predicted_issues=[
                    "Potential security vulnerabilities",
                    "Data breach risks",
                    "Compliance violations",
                    "Authentication/authorization bypasses"
                ],
                impact_areas=["Data security", "User trust", "Legal compliance", "Business reputation"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement comprehensive security testing",
                    "Conduct security code reviews",
                    "Add input validation and sanitization",
                    "Implement proper authentication and authorization",
                    "Regular security dependency updates"
                ],
                prevention_strategies=[
                    "Security-first development practices",
                    "Automated security scanning in CI/CD",
                    "Regular penetration testing",
                    "Security training for development team",
                    "Threat modeling for new features"
                ],
                prediction_id=f"security_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="risk_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "security_score": security_score,
                    "project_type_risks": project_risk_factors,
                    "dependency_count": dependency_count,
                    "risk_score": risk_score
                }
            )
            
        except Exception as e:
            logger.error(f"Security risk analysis failed: {e}")
            return None
    
    async def _analyze_maintenance_risks(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Analyze maintenance burden and technical debt risks."""
        try:
            health_metrics = project_context.get("health_metrics", {})
            complexity_metrics = project_context.get("complexity_metrics", {})
            team_metrics = project_context.get("team_metrics", {})
            
            factors = []
            risk_score = 0.0
            
            # Code quality impact on maintenance
            code_quality = health_metrics.get("code_quality", 0.8)
            if code_quality < 0.7:
                quality_impact = (0.7 - code_quality) * 2
                risk_score += quality_impact * 0.3
                factors.append(f"Low code quality increases maintenance burden ({code_quality:.1%})")
            
            # Complexity impact
            complexity = complexity_metrics.get("cyclomatic_complexity", 2.0)
            if complexity > 6:
                complexity_impact = min(0.4, (complexity - 6) / 10)
                risk_score += complexity_impact
                factors.append(f"High code complexity ({complexity:.1f})")
            
            # Documentation impact
            documentation = health_metrics.get("documentation", 0.8)
            if documentation < 0.6:
                doc_impact = (0.6 - documentation) * 1.5
                risk_score += doc_impact * 0.2
                factors.append(f"Poor documentation increases maintenance risk ({documentation:.1%})")
            
            # Team size vs. codebase size
            team_size = team_metrics.get("team_size", 5)
            loc = complexity_metrics.get("lines_of_code", 10000)
            lines_per_developer = loc / team_size if team_size > 0 else 10000
            
            if lines_per_developer > 15000:
                team_risk = min(0.3, (lines_per_developer - 15000) / 25000)
                risk_score += team_risk
                factors.append(f"High code-to-developer ratio ({lines_per_developer:.0f} lines/dev)")
            
            # Technical debt accumulation
            maintainability = health_metrics.get("maintainability", 0.8)
            if maintainability < 0.7:
                debt_risk = (0.7 - maintainability) * 1.8
                risk_score += debt_risk * 0.25
                factors.append(f"Technical debt accumulation ({maintainability:.1%})")
            
            # Testing coverage impact
            test_coverage = health_metrics.get("test_coverage", 0.8)
            if test_coverage < 0.7:
                test_risk = (0.7 - test_coverage) * 1.5
                risk_score += test_risk * 0.2
                factors.append(f"Low test coverage increases maintenance risk ({test_coverage:.1%})")
            
            probability = min(0.85, risk_score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.MAINTENANCE_BURDEN,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Maintenance burden risks identified with {probability:.1%} likelihood",
                predicted_issues=[
                    "Increasing time to implement features",
                    "Higher bug fix costs",
                    "Developer productivity decline",
                    "Knowledge transfer difficulties"
                ],
                impact_areas=["Development velocity", "Code quality", "Team efficiency", "Project costs"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement regular refactoring cycles",
                    "Improve code documentation",
                    "Increase test coverage",
                    "Establish coding standards",
                    "Consider team training and knowledge sharing"
                ],
                prevention_strategies=[
                    "Continuous code quality monitoring",
                    "Technical debt tracking and planning",
                    "Regular architecture reviews",
                    "Automated quality gates",
                    "Pair programming and code reviews"
                ],
                prediction_id=f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="risk_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "code_quality": code_quality,
                    "complexity": complexity,
                    "documentation": documentation,
                    "lines_per_developer": lines_per_developer,
                    "risk_score": risk_score
                }
            )
            
        except Exception as e:
            logger.error(f"Maintenance risk analysis failed: {e}")
            return None
    
    async def _analyze_dependency_risks(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Analyze dependency-related risks including security and maintenance."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            dependency_count = complexity_metrics.get("dependency_count", 20)
            
            factors = []
            risk_score = 0.0
            
            # High dependency count risks
            if dependency_count > 75:
                dep_risk = min(0.5, (dependency_count - 75) / 150)
                risk_score += dep_risk
                factors.append(f"Very high dependency count ({dependency_count})")
            elif dependency_count > 40:
                dep_risk = min(0.3, (dependency_count - 40) / 100)
                risk_score += dep_risk
                factors.append(f"High dependency count ({dependency_count})")
            
            # Project size correlation with dependency risks
            loc = complexity_metrics.get("lines_of_code", 10000)
            if loc > 50000:
                # Larger projects more likely to have outdated dependencies
                size_risk = min(0.3, (loc - 50000) / 200000)
                risk_score += size_risk
                factors.append("Large codebase likely has dependency management challenges")
            
            # Security vulnerability surface area
            if dependency_count > 30:
                security_surface = min(0.4, dependency_count / 200)
                risk_score += security_surface
                factors.append("Large dependency tree increases security attack surface")
            
            # License compliance risks
            if dependency_count > 50:
                license_risk = min(0.2, (dependency_count - 50) / 200)
                risk_score += license_risk
                factors.append("Complex license compliance with many dependencies")
            
            # Maintenance burden from dependencies
            if dependency_count > 60:
                maint_risk = min(0.3, (dependency_count - 60) / 150)
                risk_score += maint_risk
                factors.append("High maintenance burden from dependency updates")
            
            # Simulate outdated dependency risk based on project characteristics
            # (In real implementation, this would analyze actual dependency ages)
            if loc > 30000 or dependency_count > 50:
                risk_score += 0.25
                factors.append("Likely outdated dependencies requiring security updates")
            
            probability = min(0.90, risk_score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.SECURITY_RISK,  # Dependency risks are primarily security risks
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Dependency risks identified with {probability:.1%} likelihood",
                predicted_issues=[
                    "Security vulnerabilities in dependencies",
                    "Breaking changes in dependency updates",
                    "License compliance violations",
                    "Dependency conflict resolution issues",
                    "Supply chain attack risks"
                ],
                impact_areas=["Security", "Legal compliance", "Stability", "Development velocity"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement automated dependency scanning",
                    "Regular dependency security audits",
                    "Establish dependency update policies",
                    "Use dependency management tools",
                    "Monitor security advisories",
                    "License compliance tracking"
                ],
                prevention_strategies=[
                    "Automated vulnerability scanning in CI/CD",
                    "Dependency pinning and lock files",
                    "Regular security updates schedule",
                    "Minimal dependency principle",
                    "Supply chain security best practices"
                ],
                prediction_id=f"dependencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="risk_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "dependency_count": dependency_count,
                    "lines_of_code": loc,
                    "risk_score": risk_score,
                    "security_surface_area": dependency_count
                }
            )
            
        except Exception as e:
            logger.error(f"Dependency risk analysis failed: {e}")
            return None
    
    async def _analyze_operational_risks(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Analyze operational and deployment risks."""
        try:
            health_metrics = project_context.get("health_metrics", {})
            complexity_metrics = project_context.get("complexity_metrics", {})
            project_type = project_context.get("project_type", "web-app")
            
            factors = []
            risk_score = 0.0
            
            # Deployment complexity
            if project_type in ["web-app", "api-service"]:
                risk_score += 0.2
                factors.append(f"Deployment complexity for {project_type}")
            
            # Performance risks affecting operations
            performance = health_metrics.get("performance", 0.8)
            if performance < 0.6:
                perf_risk = (0.6 - performance) * 2
                risk_score += perf_risk * 0.3
                factors.append(f"Performance issues may impact operations ({performance:.1%})")
            
            # Architecture risks
            architecture = health_metrics.get("architecture", 0.8)
            if architecture < 0.7:
                arch_risk = (0.7 - architecture) * 1.5
                risk_score += arch_risk * 0.2
                factors.append(f"Architecture issues may cause operational problems ({architecture:.1%})")
            
            # Scalability risks
            complexity = complexity_metrics.get("cyclomatic_complexity", 2.0)
            loc = complexity_metrics.get("lines_of_code", 10000)
            
            if complexity > 8 or loc > 75000:
                scale_risk = min(0.3, max((complexity - 8) / 10, (loc - 75000) / 200000))
                risk_score += scale_risk
                factors.append("Application complexity may limit operational scalability")
            
            # Monitoring and observability gaps
            if project_type in ["web-app", "api-service"]:
                # Assume monitoring needs based on complexity
                if loc > 30000:
                    risk_score += 0.15
                    factors.append("Complex application requires comprehensive monitoring")
            
            # Data handling operational risks
            if project_type in ["web-app", "api-service", "ai-project"]:
                risk_score += 0.1
                factors.append("Data handling operations require backup and recovery procedures")
            
            probability = min(0.80, risk_score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "medium" if probability > 0.5 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.SECURITY_RISK,  # Operational risks can be classified as security risks
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Operational risks identified with {probability:.1%} likelihood",
                predicted_issues=[
                    "Service availability issues",
                    "Performance degradation in production",
                    "Deployment failures",
                    "Monitoring and alerting gaps",
                    "Data backup and recovery challenges"
                ],
                impact_areas=["Service reliability", "User experience", "Business continuity"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement comprehensive monitoring and alerting",
                    "Establish deployment automation and rollback procedures",
                    "Create disaster recovery and backup strategies",
                    "Performance testing and capacity planning",
                    "Incident response procedures"
                ],
                prevention_strategies=[
                    "Infrastructure as code",
                    "Automated testing in staging environments",
                    "Blue-green deployment strategies",
                    "Health checks and circuit breakers",
                    "Regular disaster recovery testing"
                ],
                prediction_id=f"operational_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="risk_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "project_type": project_type,
                    "performance_score": performance,
                    "architecture_score": architecture,
                    "risk_score": risk_score
                }
            )
            
        except Exception as e:
            logger.error(f"Operational risk analysis failed: {e}")
            return None
    
    def _calculate_security_severity(self, probability: float, project_type: str) -> str:
        """Calculate security risk severity based on probability and project type."""
        base_severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
        
        # Adjust based on project type
        high_risk_types = ["web-app", "api-service", "ai-project"]
        if project_type in high_risk_types and probability > 0.5:
            if base_severity == "medium":
                return "high"
            elif base_severity == "high" and probability > 0.8:
                return "critical"
        
        return base_severity
    
    def _calculate_confidence(self, probability: float, factor_count: int) -> PredictionConfidence:
        """Calculate prediction confidence based on probability and available factors."""
        confidence_score = (probability * 0.6) + (min(1.0, factor_count / 5) * 0.4)
        
        if confidence_score >= 0.8:
            return PredictionConfidence.VERY_HIGH
        elif confidence_score >= 0.65:
            return PredictionConfidence.HIGH
        elif confidence_score >= 0.45:
            return PredictionConfidence.MEDIUM
        elif confidence_score >= 0.25:
            return PredictionConfidence.LOW
        else:
            return PredictionConfidence.VERY_LOW


# Example usage
if __name__ == "__main__":
    async def main():
        analyzer = RiskAnalyzer()
        
        # Example project context
        project_context = {
            "project_type": "web-app",
            "health_metrics": {
                "security": 0.65,
                "code_quality": 0.70,
                "performance": 0.60,
                "architecture": 0.75,
                "documentation": 0.50,
                "maintainability": 0.65,
                "test_coverage": 0.55
            },
            "complexity_metrics": {
                "cyclomatic_complexity": 7.5,
                "lines_of_code": 85000,
                "dependency_count": 95
            },
            "frameworks_detected": {
                "express": 0.9,
                "react": 0.8
            },
            "team_metrics": {
                "team_size": 4,
                "experience_level": "intermediate"
            }
        }
        
        predictions = await analyzer.analyze_risks(project_context, "2months")
        
        print(f"Generated {len(predictions)} risk predictions:")
        for pred in predictions:
            if pred:
                print(f"\n- {pred.description}")
                print(f"  Type: {pred.prediction_type.value}")
                print(f"  Probability: {pred.probability:.1%}")
                print(f"  Confidence: {pred.confidence.value}")
                print(f"  Severity: {pred.severity}")
                print(f"  Key factors: {', '.join(pred.factors[:2])}")
    
    asyncio.run(main())