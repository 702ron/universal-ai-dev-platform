"""
Compatibility Analyzer

Analyzes new AI features and capabilities for compatibility with the Universal AI Development Platform.
Provides intelligent assessment of integration potential and complexity.
"""

import asyncio
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from enum import Enum

logger = logging.getLogger(__name__)


class CompatibilityStatus(Enum):
    """Compatibility assessment status."""
    COMPATIBLE = "compatible"
    REQUIRES_CHANGES = "requires_changes"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"


class IntegrationComplexity(Enum):
    """Integration complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class CompatibilityAssessment:
    """Results of compatibility analysis for a discovered feature."""
    
    feature_id: str
    status: CompatibilityStatus
    complexity: IntegrationComplexity
    confidence: float  # 0.0 to 1.0
    
    # Detailed analysis
    api_compatibility: Dict[str, Any]
    dependency_impacts: List[str]
    breaking_changes: List[str]
    migration_requirements: List[str]
    
    # Integration planning
    estimated_effort: str  # "hours", "days", "weeks"
    prerequisites: List[str]
    risks: List[str]
    recommendations: List[str]
    
    # Metadata
    analysis_timestamp: datetime
    analysis_version: str


class CompatibilityAnalyzer:
    """
    Analyzes discovered AI features for compatibility with the Universal AI Development Platform.
    Provides detailed assessment of integration potential, complexity, and requirements.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.compatibility_rules = self._load_compatibility_rules()
        self.api_patterns = self._load_api_patterns()
        self.dependency_analyzer = DependencyCompatibilityAnalyzer()
        self.breaking_change_detector = BreakingChangeDetector()
        
    def _default_config(self) -> Dict:
        """Default configuration for compatibility analysis."""
        return {
            "compatibility_threshold": 0.7,
            "complexity_factors": {
                "api_changes": 0.3,
                "dependency_conflicts": 0.4,
                "breaking_changes": 0.5,
                "documentation_availability": -0.1
            },
            "supported_platforms": [
                "anthropic", "openai", "google", "huggingface",
                "github", "vercel", "supabase", "aws", "gcp", "azure"
            ],
            "integration_time_estimates": {
                "api_endpoint": "hours",
                "new_model": "days", 
                "protocol_change": "weeks",
                "architecture_change": "weeks"
            }
        }
    
    def _load_compatibility_rules(self) -> Dict[str, Dict]:
        """Load compatibility assessment rules."""
        return {
            "api_compatibility": {
                "rest_api": {
                    "patterns": [r"\/api\/v\d+", r"REST", r"HTTP"],
                    "compatibility_boost": 0.3,
                    "complexity_reduction": 0.2
                },
                "graphql": {
                    "patterns": [r"GraphQL", r"\/graphql", r"query\s*\{"],
                    "compatibility_boost": 0.2,
                    "complexity_reduction": 0.1
                },
                "websocket": {
                    "patterns": [r"WebSocket", r"ws://", r"wss://"],
                    "compatibility_boost": 0.2,
                    "complexity_increase": 0.1
                },
                "grpc": {
                    "patterns": [r"gRPC", r"protobuf", r"\.proto"],
                    "compatibility_boost": 0.1,
                    "complexity_increase": 0.2
                }
            },
            "authentication": {
                "oauth2": {
                    "patterns": [r"OAuth\s*2", r"authorization_code", r"client_credentials"],
                    "compatibility_boost": 0.3
                },
                "api_key": {
                    "patterns": [r"API\s*key", r"x-api-key", r"authorization:\s*bearer"],
                    "compatibility_boost": 0.4
                },
                "jwt": {
                    "patterns": [r"JWT", r"JSON\s*Web\s*Token", r"Bearer\s*token"],
                    "compatibility_boost": 0.3
                }
            },
            "data_formats": {
                "json": {
                    "patterns": [r"JSON", r"application/json"],
                    "compatibility_boost": 0.4
                },
                "yaml": {
                    "patterns": [r"YAML", r"\.yml", r"\.yaml"],
                    "compatibility_boost": 0.3
                },
                "protobuf": {
                    "patterns": [r"Protocol\s*Buffers", r"protobuf", r"\.proto"],
                    "compatibility_boost": 0.2,
                    "complexity_increase": 0.1
                }
            }
        }
    
    def _load_api_patterns(self) -> Dict[str, List[str]]:
        """Load API pattern recognition rules."""
        return {
            "openai_compatible": [
                r"completions",
                r"chat/completions", 
                r"embeddings",
                r"models",
                r"fine-tuning"
            ],
            "anthropic_compatible": [
                r"messages",
                r"complete",
                r"stream",
                r"tools",
                r"artifacts"
            ],
            "standard_patterns": [
                r"GET\s+/",
                r"POST\s+/",
                r"PUT\s+/",
                r"DELETE\s+/",
                r"application/json",
                r"authorization",
                r"rate\s*limit"
            ]
        }
    
    async def analyze_feature(self, feature) -> CompatibilityAssessment:
        """
        Perform comprehensive compatibility analysis of a discovered feature.
        
        Args:
            feature: DiscoveredFeature object to analyze
            
        Returns:
            Detailed compatibility assessment
        """
        logger.info(f"Analyzing compatibility for feature: {feature.title}")
        
        try:
            # Parallel analysis tasks
            tasks = [
                self._analyze_api_compatibility(feature),
                self._analyze_dependency_impacts(feature),
                self._detect_breaking_changes(feature),
                self._assess_integration_complexity(feature),
                self._estimate_integration_effort(feature)
            ]
            
            results = await asyncio.gather(*tasks)
            
            api_compatibility = results[0]
            dependency_impacts = results[1]
            breaking_changes = results[2] 
            complexity_assessment = results[3]
            effort_estimate = results[4]
            
            # Determine overall compatibility status
            status = self._determine_compatibility_status(
                api_compatibility, dependency_impacts, breaking_changes
            )
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(
                api_compatibility, complexity_assessment, feature
            )
            
            # Generate recommendations
            recommendations = await self._generate_integration_recommendations(
                feature, api_compatibility, complexity_assessment
            )
            
            assessment = CompatibilityAssessment(
                feature_id=f"{feature.source}_{hash(feature.title)}",
                status=status,
                complexity=complexity_assessment["level"],
                confidence=confidence,
                api_compatibility=api_compatibility,
                dependency_impacts=dependency_impacts,
                breaking_changes=breaking_changes,
                migration_requirements=complexity_assessment.get("migration_requirements", []),
                estimated_effort=effort_estimate,
                prerequisites=complexity_assessment.get("prerequisites", []),
                risks=complexity_assessment.get("risks", []),
                recommendations=recommendations,
                analysis_timestamp=datetime.now(),
                analysis_version="1.0.0"
            )
            
            logger.info(f"Compatibility analysis complete: {status.value} ({confidence:.2f} confidence)")
            return assessment
            
        except Exception as e:
            logger.error(f"Error analyzing feature compatibility: {e}")
            raise
    
    async def _analyze_api_compatibility(self, feature) -> Dict[str, Any]:
        """Analyze API compatibility of the feature."""
        compatibility = {
            "score": 0.0,
            "patterns_matched": [],
            "api_type": "unknown",
            "authentication": "unknown",
            "data_format": "unknown",
            "compatibility_issues": []
        }
        
        content = f"{feature.title} {feature.description}".lower()
        
        # Check API patterns
        for api_type, patterns in self.api_patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, content, re.IGNORECASE))
            if matches > 0:
                compatibility["patterns_matched"].append(api_type)
                compatibility["score"] += matches * 0.1
                
                if matches >= 2:  # Strong indication
                    compatibility["api_type"] = api_type
        
        # Check compatibility rules
        for category, rules in self.compatibility_rules.items():
            for rule_type, rule_config in rules.items():
                patterns = rule_config.get("patterns", [])
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        if category == "authentication":
                            compatibility["authentication"] = rule_type
                        elif category == "data_formats":
                            compatibility["data_format"] = rule_type
                        
                        boost = rule_config.get("compatibility_boost", 0.0)
                        compatibility["score"] += boost
        
        # Normalize score
        compatibility["score"] = min(compatibility["score"], 1.0)
        
        # Identify potential issues
        if compatibility["api_type"] == "unknown":
            compatibility["compatibility_issues"].append("Unknown API pattern - may require custom integration")
        
        if compatibility["authentication"] == "unknown":
            compatibility["compatibility_issues"].append("Authentication method not clearly specified")
        
        return compatibility
    
    async def _analyze_dependency_impacts(self, feature) -> List[str]:
        """Analyze potential dependency impacts."""
        impacts = []
        
        content = f"{feature.title} {feature.description}".lower()
        
        # Check for new dependency requirements
        dependency_indicators = [
            (r"requires?\s+python\s+(\d+\.\d+)", "Python version requirement"),
            (r"requires?\s+node\s+(\d+)", "Node.js version requirement"),
            (r"npm\s+install\s+([^\s]+)", "New npm dependency"),
            (r"pip\s+install\s+([^\s]+)", "New Python dependency"),
            (r"cargo\s+add\s+([^\s]+)", "New Rust dependency"),
            (r"go\s+get\s+([^\s]+)", "New Go dependency")
        ]
        
        for pattern, impact_type in dependency_indicators:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    impacts.append(f"{impact_type}: {match[0]}")
                else:
                    impacts.append(f"{impact_type}: {match}")
        
        # Check for breaking dependency changes
        breaking_indicators = [
            "breaking change",
            "deprecated",
            "no longer supported",
            "removed in version",
            "migrate from"
        ]
        
        for indicator in breaking_indicators:
            if indicator in content:
                impacts.append(f"Potential breaking change detected: {indicator}")
        
        return impacts
    
    async def _detect_breaking_changes(self, feature) -> List[str]:
        """Detect potential breaking changes."""
        breaking_changes = []
        
        content = f"{feature.title} {feature.description}".lower()
        
        breaking_patterns = [
            (r"breaking\s+change", "Explicit breaking change announcement"),
            (r"deprecated.*removed", "Deprecated feature removal"),
            (r"api\s+version\s+(\d+)", "API version change"),
            (r"no\s+longer\s+supported", "Feature discontinuation"),
            (r"migrate.*from.*to", "Migration requirement"),
            (r"incompatible\s+with", "Compatibility break")
        ]
        
        for pattern, change_type in breaking_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                breaking_changes.append(change_type)
        
        return breaking_changes
    
    async def _assess_integration_complexity(self, feature) -> Dict[str, Any]:
        """Assess the complexity of integrating the feature."""
        complexity_score = 0.0
        factors = []
        
        content = f"{feature.title} {feature.description}".lower()
        
        # Complexity factors
        complexity_indicators = [
            (r"new\s+protocol", 0.4, "New protocol implementation required"),
            (r"breaking\s+change", 0.3, "Breaking changes require migration"),
            (r"beta|alpha|experimental", 0.2, "Experimental feature - higher risk"),
            (r"authentication.*oauth", 0.1, "OAuth implementation needed"),
            (r"real-time|websocket|streaming", 0.2, "Real-time features add complexity"),
            (r"machine\s+learning|ml\s+model", 0.3, "ML integration complexity"),
            (r"custom\s+implementation", 0.3, "Custom implementation required")
        ]
        
        for pattern, weight, description in complexity_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                complexity_score += weight
                factors.append(description)
        
        # Determine complexity level
        if complexity_score >= 0.8:
            level = IntegrationComplexity.VERY_HIGH
        elif complexity_score >= 0.5:
            level = IntegrationComplexity.HIGH
        elif complexity_score >= 0.3:
            level = IntegrationComplexity.MEDIUM
        else:
            level = IntegrationComplexity.LOW
        
        # Generate requirements and risks based on complexity
        requirements = []
        risks = []
        prerequisites = []
        
        if level in [IntegrationComplexity.HIGH, IntegrationComplexity.VERY_HIGH]:
            requirements.append("Comprehensive testing strategy required")
            requirements.append("Gradual rollout with feature flags")
            risks.append("Potential for integration issues")
            risks.append("May require significant development time")
            prerequisites.append("Detailed technical documentation review")
        
        if "authentication" in content:
            prerequisites.append("Security review required")
            requirements.append("Authentication flow testing")
        
        if "api" in content:
            prerequisites.append("API documentation analysis")
            requirements.append("Endpoint compatibility verification")
        
        return {
            "level": level,
            "score": complexity_score,
            "factors": factors,
            "migration_requirements": requirements,
            "prerequisites": prerequisites,
            "risks": risks
        }
    
    async def _estimate_integration_effort(self, feature) -> str:
        """Estimate integration effort in time units."""
        content = f"{feature.title} {feature.description}".lower()
        
        # Effort estimation based on feature type
        if any(keyword in content for keyword in ["protocol", "architecture", "breaking"]):
            return "weeks"
        elif any(keyword in content for keyword in ["api", "authentication", "model"]):
            return "days"
        else:
            return "hours"
    
    def _determine_compatibility_status(self, api_compatibility: Dict, 
                                      dependency_impacts: List[str], 
                                      breaking_changes: List[str]) -> CompatibilityStatus:
        """Determine overall compatibility status."""
        
        # Check for clear incompatibility signals
        if breaking_changes:
            for change in breaking_changes:
                if any(keyword in change.lower() for keyword in ["incompatible", "no longer supported"]):
                    return CompatibilityStatus.INCOMPATIBLE
        
        # Check API compatibility score
        api_score = api_compatibility.get("score", 0.0)
        
        if api_score >= self.config["compatibility_threshold"]:
            if not dependency_impacts and not breaking_changes:
                return CompatibilityStatus.COMPATIBLE
            else:
                return CompatibilityStatus.REQUIRES_CHANGES
        elif api_score >= 0.4:
            return CompatibilityStatus.REQUIRES_CHANGES
        else:
            return CompatibilityStatus.INCOMPATIBLE
    
    def _calculate_confidence_score(self, api_compatibility: Dict, 
                                  complexity_assessment: Dict, 
                                  feature) -> float:
        """Calculate confidence score for the assessment."""
        base_confidence = 0.5
        
        # Boost confidence based on clear patterns
        api_score = api_compatibility.get("score", 0.0)
        base_confidence += api_score * 0.3
        
        # Boost confidence based on documentation quality
        if len(feature.description) > 100:  # Detailed description
            base_confidence += 0.1
        
        if feature.url and "docs" in feature.url:  # Official documentation
            base_confidence += 0.1
        
        # Reduce confidence for high complexity
        complexity_score = complexity_assessment.get("score", 0.0)
        base_confidence -= complexity_score * 0.1
        
        # Reduce confidence for unknown patterns
        if api_compatibility.get("api_type") == "unknown":
            base_confidence -= 0.2
        
        return max(min(base_confidence, 1.0), 0.1)  # Clamp between 0.1 and 1.0
    
    async def _generate_integration_recommendations(self, feature, 
                                                  api_compatibility: Dict, 
                                                  complexity_assessment: Dict) -> List[str]:
        """Generate specific integration recommendations."""
        recommendations = []
        
        # API-specific recommendations
        api_type = api_compatibility.get("api_type", "unknown")
        if api_type == "openai_compatible":
            recommendations.append("Use OpenAI client adapter for seamless integration")
        elif api_type == "anthropic_compatible":
            recommendations.append("Leverage existing Anthropic integration patterns")
        elif api_type == "unknown":
            recommendations.append("Create custom API client with comprehensive error handling")
        
        # Complexity-based recommendations
        complexity = complexity_assessment.get("level")
        if complexity in [IntegrationComplexity.HIGH, IntegrationComplexity.VERY_HIGH]:
            recommendations.append("Implement feature flags for gradual rollout")
            recommendations.append("Create comprehensive integration tests")
            recommendations.append("Set up monitoring and rollback procedures")
        
        # Authentication recommendations
        auth_type = api_compatibility.get("authentication", "unknown")
        if auth_type == "oauth2":
            recommendations.append("Implement OAuth2 flow with secure token storage")
        elif auth_type == "api_key":
            recommendations.append("Secure API key management with environment variables")
        elif auth_type == "unknown":
            recommendations.append("Review authentication documentation before implementation")
        
        # General recommendations
        recommendations.append("Test integration in isolated environment first")
        recommendations.append("Document integration process for future maintenance")
        
        if feature.confidence_score > 0.8:
            recommendations.append("High-value feature - prioritize for next integration cycle")
        
        return recommendations


class DependencyCompatibilityAnalyzer:
    """Analyzes dependency compatibility impacts."""
    
    async def analyze_dependencies(self, feature) -> Dict[str, Any]:
        """Analyze dependency impacts of a feature."""
        # TODO: Implement detailed dependency analysis
        return {
            "conflicts": [],
            "new_requirements": [],
            "version_impacts": []
        }


class BreakingChangeDetector:
    """Detects breaking changes in feature updates."""
    
    def detect_breaking_changes(self, feature) -> List[str]:
        """Detect potential breaking changes."""
        # TODO: Implement sophisticated breaking change detection
        return []


# Example usage
if __name__ == "__main__":
    async def main():
        from ..adaptation.feature_discovery import DiscoveredFeature
        from datetime import datetime
        
        # Mock feature for testing
        feature = DiscoveredFeature(
            source="https://docs.anthropic.com",
            title="New Claude API Tool Use Capabilities",
            description="Enhanced tool use with function calling and structured outputs",
            url="https://docs.anthropic.com/claude/docs/tool-use",
            category="api",
            discovered_at=datetime.now(),
            confidence_score=0.9,
            impact_assessment={"development_velocity": 0.8},
            integration_complexity="medium",
            compatibility_status="unknown",
            metadata={}
        )
        
        analyzer = CompatibilityAnalyzer()
        assessment = await analyzer.analyze_feature(feature)
        
        print(f"Feature: {feature.title}")
        print(f"Status: {assessment.status.value}")
        print(f"Complexity: {assessment.complexity.value}")
        print(f"Confidence: {assessment.confidence:.2f}")
        print(f"Estimated Effort: {assessment.estimated_effort}")
        print("\nRecommendations:")
        for rec in assessment.recommendations:
            print(f"- {rec}")
    
    asyncio.run(main())