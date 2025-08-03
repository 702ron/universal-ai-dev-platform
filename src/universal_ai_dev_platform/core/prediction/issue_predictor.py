"""
Issue Predictor

Machine learning-based system for predicting potential development issues
before they occur, including bugs, technical debt, and maintainability problems.
"""

import asyncio
import logging
import numpy as np
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import math

from .predictive_intelligence import PredictionResult, PredictionType, PredictionConfidence

logger = logging.getLogger(__name__)


class IssueType(Enum):
    """Types of issues that can be predicted."""
    BUG_PRONE_CODE = "bug_prone_code"
    TECHNICAL_DEBT = "technical_debt"
    MAINTAINABILITY_DECLINE = "maintainability_decline"
    TESTING_GAPS = "testing_gaps"
    DEPENDENCY_ISSUES = "dependency_issues"
    PERFORMANCE_BOTTLENECK = "performance_bottleneck"
    SECURITY_VULNERABILITY = "security_vulnerability"
    SCALABILITY_PROBLEM = "scalability_problem"


@dataclass
class IssuePrediction:
    """Specific issue prediction with detailed analysis."""
    issue_type: IssueType
    probability: float
    severity: str
    affected_areas: List[str]
    root_causes: List[str]
    prevention_cost: str  # low, medium, high
    fix_cost: str  # low, medium, high, very_high


class IssuePredictor:
    """
    Advanced issue prediction system using statistical analysis and pattern recognition
    to identify potential problems before they manifest.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the issue predictor."""
        self.config = config or {}
        self.issue_patterns = self._load_issue_patterns()
        self.prediction_weights = self._initialize_weights()
    
    def _load_issue_patterns(self) -> Dict[str, Dict]:
        """Load known patterns that correlate with different types of issues."""
        return {
            "bug_prone_patterns": {
                "high_complexity": {"weight": 0.8, "threshold": 10},
                "low_test_coverage": {"weight": 0.9, "threshold": 0.6},
                "frequent_changes": {"weight": 0.6, "threshold": 5},
                "large_methods": {"weight": 0.7, "threshold": 50},
                "deep_inheritance": {"weight": 0.5, "threshold": 5}
            },
            "technical_debt_patterns": {
                "code_duplication": {"weight": 0.8, "threshold": 0.15},
                "outdated_dependencies": {"weight": 0.7, "threshold": 0.3},
                "documentation_gaps": {"weight": 0.6, "threshold": 0.4},
                "inconsistent_patterns": {"weight": 0.5, "threshold": 0.2},
                "quick_fixes": {"weight": 0.8, "threshold": 0.1}
            },
            "maintainability_patterns": {
                "coupling_ratio": {"weight": 0.9, "threshold": 0.7},
                "code_churn": {"weight": 0.6, "threshold": 0.5},
                "team_knowledge_concentration": {"weight": 0.7, "threshold": 0.8},
                "deprecated_apis": {"weight": 0.5, "threshold": 0.2}
            },
            "performance_patterns": {
                "n_plus_one_queries": {"weight": 0.9, "threshold": 0.1},
                "memory_leaks": {"weight": 0.8, "threshold": 0.1},
                "blocking_operations": {"weight": 0.7, "threshold": 0.2},
                "inefficient_algorithms": {"weight": 0.8, "threshold": 0.15}
            }
        }
    
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize weights for different prediction factors."""
        return {
            "code_quality": 0.25,
            "test_coverage": 0.20,
            "complexity": 0.15,
            "dependencies": 0.15,
            "team_factors": 0.10,
            "historical_patterns": 0.15
        }
    
    async def predict_issues(self, project_context: Dict[str, Any], 
                           timeline: str) -> List[PredictionResult]:
        """
        Predict potential issues for a project within the given timeline.
        
        Args:
            project_context: Current project state and metrics
            timeline: Prediction timeline
            
        Returns:
            List of issue predictions
        """
        logger.info("Predicting potential development issues...")
        
        predictions = []
        
        try:
            # Extract relevant metrics
            health_metrics = project_context.get("health_metrics", {})
            complexity_metrics = project_context.get("complexity_metrics", {})
            team_metrics = project_context.get("team_metrics", {})
            
            # Predict different types of issues
            issue_predictions = await asyncio.gather(
                self._predict_bug_prone_areas(health_metrics, complexity_metrics, timeline),
                self._predict_technical_debt(project_context, timeline),
                self._predict_maintainability_issues(project_context, timeline),
                self._predict_testing_gaps(health_metrics, timeline),
                self._predict_dependency_issues(project_context, timeline),
                return_exceptions=True
            )
            
            # Process results
            for result in issue_predictions:
                if isinstance(result, PredictionResult):
                    predictions.append(result)
                elif isinstance(result, list):
                    predictions.extend(result)
                elif isinstance(result, Exception):
                    logger.warning(f"Issue prediction failed: {result}")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Issue prediction failed: {e}")
            return []
    
    async def _predict_bug_prone_areas(self, health_metrics: Dict, 
                                     complexity_metrics: Dict, timeline: str) -> PredictionResult:
        """Predict areas likely to contain bugs."""
        try:
            # Calculate bug-proneness score
            factors = []
            score = 0.0
            
            # Low test coverage increases bug risk
            test_coverage = health_metrics.get("test_coverage", 0.8)
            if test_coverage < 0.7:
                coverage_impact = (0.7 - test_coverage) * 2  # Scale impact
                score += coverage_impact * 0.4
                factors.append(f"Low test coverage ({test_coverage:.1%})")
            
            # High complexity increases bug risk
            complexity = complexity_metrics.get("cyclomatic_complexity", 1.0)
            if complexity > 5:
                complexity_impact = min(1.0, (complexity - 5) / 10)
                score += complexity_impact * 0.3
                factors.append(f"High cyclomatic complexity ({complexity:.1f})")
            
            # Code quality impact
            code_quality = health_metrics.get("code_quality", 0.8)
            if code_quality < 0.7:
                quality_impact = (0.7 - code_quality) * 1.5
                score += quality_impact * 0.3
                factors.append(f"Low code quality score ({code_quality:.1%})")
            
            # Determine confidence and severity
            probability = min(0.95, score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.ISSUE_PREDICTION,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Bug-prone code areas identified with {probability:.1%} likelihood",
                predicted_issues=[
                    "Increased bug discovery rate",
                    "Quality assurance bottlenecks",
                    "Customer-reported issues"
                ],
                impact_areas=["User experience", "Development velocity", "Team productivity"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Increase test coverage in identified areas",
                    "Implement code complexity limits",
                    "Add automated quality gates",
                    "Conduct focused code reviews"
                ],
                prevention_strategies=[
                    "Test-driven development adoption",
                    "Continuous integration improvements",
                    "Static code analysis integration",
                    "Pair programming for complex areas"
                ],
                prediction_id=f"bug_prone_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="issue_v1.0",
                data_points_analyzed=len(health_metrics) + len(complexity_metrics)
            )
            
        except Exception as e:
            logger.error(f"Bug-prone area prediction failed: {e}")
            return None
    
    async def _predict_technical_debt(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Predict technical debt accumulation."""
        try:
            health_metrics = project_context.get("health_metrics", {})
            complexity_metrics = project_context.get("complexity_metrics", {})
            
            factors = []
            score = 0.0
            
            # Documentation gaps
            documentation = health_metrics.get("documentation", 0.8)
            if documentation < 0.6:
                doc_impact = (0.6 - documentation) * 1.5
                score += doc_impact * 0.3
                factors.append(f"Poor documentation coverage ({documentation:.1%})")
            
            # Dependency age and security
            dependency_count = complexity_metrics.get("dependency_count", 0)
            if dependency_count > 50:
                dep_impact = min(1.0, (dependency_count - 50) / 100)
                score += dep_impact * 0.2
                factors.append(f"High dependency count ({dependency_count})")
            
            # Code maintainability
            maintainability = health_metrics.get("maintainability", 0.8)
            if maintainability < 0.7:
                maint_impact = (0.7 - maintainability) * 1.2
                score += maint_impact * 0.3
                factors.append(f"Low maintainability score ({maintainability:.1%})")
            
            # Project size impact (larger projects accumulate debt faster)
            loc = complexity_metrics.get("lines_of_code", 10000)
            if loc > 50000:
                size_impact = min(0.5, (loc - 50000) / 200000)
                score += size_impact * 0.2
                factors.append(f"Large codebase ({loc:,} lines)")
            
            probability = min(0.90, score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.ISSUE_PREDICTION,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Technical debt accumulation predicted with {probability:.1%} likelihood",
                predicted_issues=[
                    "Increased development time",
                    "Reduced feature velocity",
                    "Higher maintenance costs",
                    "Developer frustration"
                ],
                impact_areas=["Development speed", "Code quality", "Team morale"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement regular refactoring cycles",
                    "Improve documentation standards",
                    "Establish code quality gates",
                    "Plan technical debt reduction sprints"
                ],
                prevention_strategies=[
                    "Continuous refactoring practices",
                    "Architecture decision records",
                    "Code review quality standards",
                    "Technical debt tracking and metrics"
                ],
                prediction_id=f"tech_debt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="issue_v1.0",
                data_points_analyzed=len(factors)
            )
            
        except Exception as e:
            logger.error(f"Technical debt prediction failed: {e}")
            return None
    
    async def _predict_maintainability_issues(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Predict maintainability decline."""
        try:
            health_metrics = project_context.get("health_metrics", {})
            team_metrics = project_context.get("team_metrics", {})
            
            factors = []
            score = 0.0
            
            # Team size vs codebase size
            team_size = team_metrics.get("team_size", 5)
            complexity_metrics = project_context.get("complexity_metrics", {})
            loc = complexity_metrics.get("lines_of_code", 10000)
            
            lines_per_developer = loc / team_size if team_size > 0 else 10000
            if lines_per_developer > 10000:
                team_impact = min(0.8, (lines_per_developer - 10000) / 20000)
                score += team_impact * 0.4
                factors.append(f"High lines per developer ratio ({lines_per_developer:.0f})")
            
            # Experience level impact
            experience = team_metrics.get("experience_level", "intermediate")
            if experience == "junior":
                score += 0.3
                factors.append("Junior team experience level")
            elif experience == "mixed":
                score += 0.1
                factors.append("Mixed team experience level")
            
            # Code quality trends
            code_quality = health_metrics.get("code_quality", 0.8)
            if code_quality < 0.6:
                quality_impact = (0.6 - code_quality) * 2
                score += quality_impact * 0.3
                factors.append(f"Declining code quality ({code_quality:.1%})")
            
            probability = min(0.85, score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.ISSUE_PREDICTION,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Maintainability decline predicted with {probability:.1%} likelihood",
                predicted_issues=[
                    "Increased time to implement features",
                    "Higher onboarding costs for new developers",
                    "Reduced code understandability",
                    "Increased bug fix time"
                ],
                impact_areas=["Developer productivity", "Code quality", "Team efficiency"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement coding standards and guidelines",
                    "Increase code review coverage",
                    "Provide team training on best practices",
                    "Introduce architectural documentation"
                ],
                prevention_strategies=[
                    "Regular code quality assessments",
                    "Continuous team education",
                    "Mentorship programs",
                    "Code complexity monitoring"
                ],
                prediction_id=f"maintainability_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="issue_v1.0",
                data_points_analyzed=len(factors)
            )
            
        except Exception as e:
            logger.error(f"Maintainability prediction failed: {e}")
            return None
    
    async def _predict_testing_gaps(self, health_metrics: Dict, timeline: str) -> PredictionResult:
        """Predict testing coverage and quality gaps."""
        try:
            test_coverage = health_metrics.get("test_coverage", 0.8)
            code_quality = health_metrics.get("code_quality", 0.8)
            
            factors = []
            score = 0.0
            
            # Low test coverage
            if test_coverage < 0.8:
                coverage_gap = (0.8 - test_coverage) * 2
                score += coverage_gap * 0.6
                factors.append(f"Below recommended test coverage ({test_coverage:.1%})")
            
            # Integration test indicators
            if test_coverage > 0.7 but code_quality < 0.7:
                # High coverage but low quality suggests unit-test-only approach
                score += 0.3
                factors.append("Potential integration testing gaps")
            
            # Testing strategy gaps
            if test_coverage < 0.6:
                score += 0.4
                factors.append("Critical testing coverage gaps")
            
            probability = min(0.90, score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "critical" if probability > 0.8 else "high" if probability > 0.6 else "medium"
            
            return PredictionResult(
                prediction_type=PredictionType.ISSUE_PREDICTION,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Testing gaps identified with {probability:.1%} likelihood of issues",
                predicted_issues=[
                    "Undetected bugs reaching production",
                    "Regression issues during releases",
                    "Difficult debugging and troubleshooting",
                    "Reduced confidence in deployments"
                ],
                impact_areas=["Product quality", "Release confidence", "Customer satisfaction"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Increase test coverage to 80%+ target",
                    "Implement integration and E2E testing",
                    "Add automated regression testing",
                    "Establish testing best practices"
                ],
                prevention_strategies=[
                    "Test-driven development adoption",
                    "Continuous integration with test gates",
                    "Testing pyramid implementation",
                    "Regular testing strategy reviews"
                ],
                prediction_id=f"testing_gaps_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="issue_v1.0",
                data_points_analyzed=2
            )
            
        except Exception as e:
            logger.error(f"Testing gaps prediction failed: {e}")
            return None
    
    async def _predict_dependency_issues(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Predict dependency-related issues."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            dependency_count = complexity_metrics.get("dependency_count", 20)
            
            factors = []
            score = 0.0
            
            # High dependency count
            if dependency_count > 100:
                dep_impact = min(0.8, (dependency_count - 100) / 200)
                score += dep_impact * 0.4
                factors.append(f"High dependency count ({dependency_count})")
            
            # Assume some dependencies are outdated (would be calculated from actual data)
            # For demo, simulate based on project age/size
            loc = complexity_metrics.get("lines_of_code", 10000)
            if loc > 30000:  # Larger projects likely have outdated deps
                score += 0.3
                factors.append("Likely outdated dependencies in large codebase")
            
            # Security implications
            if dependency_count > 50:
                score += 0.2
                factors.append("Increased security surface area")
            
            probability = min(0.85, score)
            confidence = self._calculate_confidence(probability, len(factors))
            severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.ISSUE_PREDICTION,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Dependency issues predicted with {probability:.1%} likelihood",
                predicted_issues=[
                    "Security vulnerabilities in dependencies",
                    "Breaking changes in dependency updates",
                    "License compliance issues",
                    "Dependency conflicts and resolution problems"
                ],
                impact_areas=["Security", "Stability", "Legal compliance"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement automated dependency scanning",
                    "Establish dependency update schedule",
                    "Monitor security advisories",
                    "Use dependency management tools"
                ],
                prevention_strategies=[
                    "Regular dependency audits",
                    "Automated security scanning",
                    "Dependency pinning strategies",
                    "License compliance checking"
                ],
                prediction_id=f"dependencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="issue_v1.0",
                data_points_analyzed=len(factors)
            )
            
        except Exception as e:
            logger.error(f"Dependency prediction failed: {e}")
            return None
    
    def _calculate_confidence(self, probability: float, factor_count: int) -> PredictionConfidence:
        """Calculate prediction confidence based on probability and available factors."""
        # More factors and higher probability = higher confidence
        confidence_score = (probability * 0.7) + (min(1.0, factor_count / 5) * 0.3)
        
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
        predictor = IssuePredictor()
        
        # Example project context
        project_context = {
            "health_metrics": {
                "code_quality": 0.65,
                "test_coverage": 0.45,
                "documentation": 0.40,
                "maintainability": 0.60
            },
            "complexity_metrics": {
                "cyclomatic_complexity": 8.5,
                "lines_of_code": 75000,
                "dependency_count": 120
            },
            "team_metrics": {
                "team_size": 4,
                "experience_level": "mixed"
            }
        }
        
        predictions = await predictor.predict_issues(project_context, "1month")
        
        print(f"Generated {len(predictions)} issue predictions:")
        for pred in predictions:
            if pred:
                print(f"\n- {pred.description}")
                print(f"  Probability: {pred.probability:.1%}")
                print(f"  Confidence: {pred.confidence.value}")
                print(f"  Factors: {', '.join(pred.factors[:2])}")
    
    asyncio.run(main())