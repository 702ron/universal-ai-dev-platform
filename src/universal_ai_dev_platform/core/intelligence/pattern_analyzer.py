"""
Pattern Analyzer

Analyzes code patterns, architectural decisions, and development practices to build
intelligent recommendations and learn from successful project implementations.
"""

import asyncio
import logging
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, Counter
from enum import Enum

logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Types of patterns that can be detected."""
    ARCHITECTURAL = "architectural"
    DESIGN = "design"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    CODE_ORGANIZATION = "code_organization"
    API_DESIGN = "api_design"


class PatternConfidence(Enum):
    """Confidence levels for pattern detection."""
    LOW = "low"        # 0.0 - 0.4
    MEDIUM = "medium"  # 0.4 - 0.7
    HIGH = "high"      # 0.7 - 0.9
    VERY_HIGH = "very_high"  # 0.9 - 1.0


@dataclass
class DetectedPattern:
    """Represents a detected pattern in code or project structure."""
    
    pattern_id: str
    pattern_type: PatternType
    name: str
    description: str
    confidence: float  # 0.0 to 1.0
    confidence_level: PatternConfidence
    
    # Evidence and context
    evidence_files: List[str]
    code_examples: List[str]
    usage_frequency: int
    first_seen: datetime
    last_seen: datetime
    
    # Analysis
    benefits: List[str]
    drawbacks: List[str]
    recommendations: List[str]
    related_patterns: List[str]
    
    # Metrics
    complexity_score: float
    maintainability_impact: float
    performance_impact: float
    security_impact: float
    
    # Metadata
    detection_method: str
    analysis_version: str
    metadata: Dict[str, Any]


@dataclass
class PatternAnalysisResult:
    """Complete pattern analysis results for a project."""
    
    project_path: str
    analysis_timestamp: datetime
    patterns_detected: List[DetectedPattern]
    pattern_summary: Dict[PatternType, int]
    overall_pattern_score: float
    recommendations: List[str]
    anti_patterns: List[DetectedPattern]
    learning_insights: List[str]


class PatternAnalyzer:
    """
    Analyzes code and project structures to detect patterns, anti-patterns, and best practices.
    Learns from successful implementations to provide intelligent recommendations.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.pattern_definitions = self._load_pattern_definitions()
        self.anti_pattern_definitions = self._load_anti_pattern_definitions()
        self.learning_database = PatternLearningDatabase()
        
    def _default_config(self) -> Dict:
        """Default configuration for pattern analysis."""
        return {
            "confidence_threshold": 0.6,
            "min_evidence_files": 2,
            "max_analysis_depth": 5,
            "pattern_categories": [
                "architectural",
                "design", 
                "security",
                "performance",
                "testing",
                "deployment"
            ],
            "file_type_weights": {
                ".py": 1.0,
                ".js": 1.0,
                ".ts": 1.0,
                ".java": 1.0,
                ".go": 1.0,
                ".rs": 1.0,
                ".cpp": 0.8,
                ".yaml": 0.6,
                ".json": 0.6,
                ".md": 0.3
            }
        }
    
    def _load_pattern_definitions(self) -> Dict[str, Dict]:
        """Load pattern detection definitions."""
        return {
            "mvc_pattern": {
                "type": PatternType.ARCHITECTURAL,
                "name": "Model-View-Controller (MVC)",
                "description": "Separation of concerns through MVC architecture",
                "indicators": {
                    "directory_structure": ["models", "views", "controllers"],
                    "file_patterns": [r".*Controller\.py", r".*Model\.py", r".*View\.py"],
                    "content_patterns": [
                        r"class.*Controller",
                        r"class.*Model",
                        r"class.*View"
                    ]
                },
                "min_confidence": 0.6,
                "benefits": [
                    "Clear separation of concerns",
                    "Improved maintainability",
                    "Better testability"
                ],
                "recommendations": [
                    "Ensure controllers remain thin",
                    "Keep business logic in models",
                    "Minimize view logic"
                ]
            },
            
            "repository_pattern": {
                "type": PatternType.DESIGN,
                "name": "Repository Pattern",
                "description": "Data access abstraction layer",
                "indicators": {
                    "file_patterns": [r".*Repository\.py", r".*Repo\.py"],
                    "content_patterns": [
                        r"class.*Repository",
                        r"def\s+find_by_",
                        r"def\s+save\(",
                        r"def\s+delete\(",
                        r"interface.*Repository"
                    ]
                },
                "min_confidence": 0.5,
                "benefits": [
                    "Centralized data access logic",
                    "Improved testability with mocking",
                    "Database technology independence"
                ],
                "recommendations": [
                    "Use dependency injection for repositories",
                    "Create repository interfaces",
                    "Implement unit of work pattern"
                ]
            },
            
            "dependency_injection": {
                "type": PatternType.DESIGN,
                "name": "Dependency Injection",
                "description": "Inversion of control through dependency injection",
                "indicators": {
                    "content_patterns": [
                        r"@inject",
                        r"@Injectable",
                        r"\.inject\(",
                        r"constructor.*inject",
                        r"def __init__.*inject"
                    ],
                    "file_patterns": [r".*container\.py", r".*injector\.py"],
                    "framework_indicators": ["django", "spring", "nestjs", "inversify"]
                },
                "min_confidence": 0.4,
                "benefits": [
                    "Loose coupling between components",
                    "Improved testability",
                    "Better configuration management"
                ],
                "recommendations": [
                    "Use constructor injection when possible",
                    "Avoid service locator anti-pattern",
                    "Register dependencies in container"
                ]
            },
            
            "clean_architecture": {
                "type": PatternType.ARCHITECTURAL,
                "name": "Clean Architecture",
                "description": "Layered architecture with dependency inversion",
                "indicators": {
                    "directory_structure": [
                        "domain", "application", "infrastructure", "presentation",
                        "entities", "use_cases", "interfaces", "frameworks"
                    ],
                    "content_patterns": [
                        r"class.*UseCase",
                        r"class.*Entity",
                        r"interface.*Repository",
                        r"class.*Service"
                    ]
                },
                "min_confidence": 0.7,
                "benefits": [
                    "Independence from frameworks",
                    "Independence from UI",
                    "Independence from database",
                    "Testable architecture"
                ],
                "recommendations": [
                    "Keep domain layer pure",
                    "Use interfaces for external dependencies",
                    "Implement use cases for business logic"
                ]
            },
            
            "microservices_pattern": {
                "type": PatternType.ARCHITECTURAL,
                "name": "Microservices Architecture",
                "description": "Distributed system of loosely coupled services",
                "indicators": {
                    "directory_structure": ["services", "microservices"],
                    "file_patterns": [
                        r"docker-compose\.yml",
                        r"Dockerfile",
                        r"service\.py",
                        r".*-service"
                    ],
                    "content_patterns": [
                        r"@app\.route",
                        r"FastAPI\(",
                        r"express\(\)",
                        r"service.*discovery"
                    ]
                },
                "min_confidence": 0.6,
                "benefits": [
                    "Independent deployability",
                    "Technology diversity",
                    "Fault isolation",
                    "Scalability"
                ],
                "recommendations": [
                    "Implement proper service discovery",
                    "Use API gateways",
                    "Implement circuit breakers",
                    "Monitor service health"
                ]
            },
            
            "factory_pattern": {
                "type": PatternType.DESIGN,
                "name": "Factory Pattern",
                "description": "Object creation abstraction",
                "indicators": {
                    "content_patterns": [
                        r"class.*Factory",
                        r"def\s+create_",
                        r"def\s+make_",
                        r"@staticmethod.*create",
                        r"factory_method"
                    ]
                },
                "min_confidence": 0.4,
                "benefits": [
                    "Encapsulated object creation",
                    "Flexible object instantiation",
                    "Reduced coupling"
                ],
                "recommendations": [
                    "Use abstract factories for families of objects",
                    "Consider builder pattern for complex objects",
                    "Document factory methods clearly"
                ]
            },
            
            "observer_pattern": {
                "type": PatternType.DESIGN,
                "name": "Observer Pattern",
                "description": "Event-driven communication pattern",
                "indicators": {
                    "content_patterns": [
                        r"class.*Observer",
                        r"def\s+notify",
                        r"def\s+subscribe",
                        r"def\s+unsubscribe",
                        r"addEventListener",
                        r"@event_listener"
                    ]
                },
                "min_confidence": 0.5,
                "benefits": [
                    "Loose coupling between subjects and observers",
                    "Dynamic subscription/unsubscription",
                    "Support for broadcast communication"
                ],
                "recommendations": [
                    "Avoid memory leaks with proper unsubscription",
                    "Consider async/await for event handling",
                    "Use typed events when possible"
                ]
            },
            
            "singleton_pattern": {
                "type": PatternType.DESIGN,
                "name": "Singleton Pattern",
                "description": "Single instance class",
                "indicators": {
                    "content_patterns": [
                        r"class.*Singleton",
                        r"_instance\s*=\s*None",
                        r"__new__.*instance",
                        r"getInstance\(\)",
                        r"@singleton"
                    ]
                },
                "min_confidence": 0.6,
                "benefits": [
                    "Controlled access to single instance",
                    "Reduced memory footprint"
                ],
                "drawbacks": [
                    "Difficult to test",
                    "Hidden dependencies",
                    "Violates single responsibility principle"
                ],
                "recommendations": [
                    "Consider dependency injection instead",
                    "Use sparingly and only when truly needed",
                    "Make thread-safe if required"
                ]
            },
            
            "api_versioning": {
                "type": PatternType.API_DESIGN,
                "name": "API Versioning",
                "description": "Structured API version management",
                "indicators": {
                    "content_patterns": [
                        r"/api/v\d+",
                        r"version\s*=\s*[\"']\d+",
                        r"API_VERSION",
                        r"@version\(",
                        r"Accept:.*version"
                    ],
                    "file_patterns": [r"v\d+.*\.py", r".*v\d+.*"]
                },
                "min_confidence": 0.5,
                "benefits": [
                    "Backward compatibility",
                    "Controlled API evolution",
                    "Clear version strategy"
                ],
                "recommendations": [
                    "Use semantic versioning",
                    "Document version deprecation timeline",
                    "Provide migration guides"
                ]
            },
            
            "circuit_breaker": {
                "type": PatternType.PERFORMANCE,
                "name": "Circuit Breaker Pattern",
                "description": "Fault tolerance pattern for external services",
                "indicators": {
                    "content_patterns": [
                        r"CircuitBreaker",
                        r"circuit.*breaker",
                        r"failure_threshold",
                        r"recovery_timeout",
                        r"@circuit_breaker"
                    ]
                },
                "min_confidence": 0.7,
                "benefits": [
                    "Prevents cascading failures",
                    "Improves system resilience",
                    "Fast failure detection"
                ],
                "recommendations": [
                    "Set appropriate failure thresholds",
                    "Implement proper fallback mechanisms",
                    "Monitor circuit breaker states"
                ]
            }
        }
    
    def _load_anti_pattern_definitions(self) -> Dict[str, Dict]:
        """Load anti-pattern detection definitions."""
        return {
            "god_object": {
                "type": PatternType.DESIGN,
                "name": "God Object Anti-pattern",
                "description": "Class with too many responsibilities",
                "indicators": {
                    "content_patterns": [
                        r"class\s+\w*Manager\w*",
                        r"class\s+\w*Helper\w*",
                        r"class\s+\w*Util\w*"
                    ],
                    "metrics": {
                        "lines_of_code": 500,
                        "method_count": 20,
                        "dependency_count": 10
                    }
                },
                "severity": "high",
                "recommendations": [
                    "Break down into smaller, focused classes",
                    "Apply single responsibility principle",
                    "Use composition over inheritance"
                ]
            },
            
            "copy_paste_programming": {
                "type": PatternType.CODE_ORGANIZATION,
                "name": "Copy-Paste Programming",
                "description": "Duplicated code blocks indicating poor abstraction",
                "indicators": {
                    "metrics": {
                        "code_duplication_percentage": 15
                    }
                },
                "severity": "medium",
                "recommendations": [
                    "Extract common code into functions",
                    "Create reusable modules",
                    "Use inheritance or composition"
                ]
            },
            
            "hard_coded_values": {
                "type": PatternType.SECURITY,
                "name": "Hard-coded Configuration",
                "description": "Configuration values embedded in code",
                "indicators": {
                    "content_patterns": [
                        r"password\s*=\s*[\"'][^\"']+[\"']",
                        r"api_key\s*=\s*[\"'][^\"']+[\"']",
                        r"secret\s*=\s*[\"'][^\"']+[\"']",
                        r"host\s*=\s*[\"']localhost[\"']",
                        r"port\s*=\s*\d+"
                    ]
                },
                "severity": "high",
                "recommendations": [
                    "Use environment variables",
                    "Implement configuration management",
                    "Never commit secrets to version control"
                ]
            }
        }
    
    async def analyze_patterns(self, project_path: str) -> PatternAnalysisResult:
        """
        Perform comprehensive pattern analysis of a project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Complete pattern analysis results
        """
        logger.info(f"Starting pattern analysis for: {project_path}")
        
        project_path = Path(project_path)
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        try:
            # Collect project files for analysis
            project_files = await self._collect_project_files(project_path)
            
            # Parallel pattern detection
            tasks = [
                self._detect_architectural_patterns(project_files),
                self._detect_design_patterns(project_files),
                self._detect_api_patterns(project_files),
                self._detect_security_patterns(project_files),
                self._detect_performance_patterns(project_files),
                self._detect_anti_patterns(project_files)
            ]
            
            results = await asyncio.gather(*tasks)
            
            detected_patterns = []
            anti_patterns = []
            
            # Combine results
            for result_set in results[:-1]:  # All except anti-patterns
                detected_patterns.extend(result_set)
            
            anti_patterns = results[-1]  # Last result is anti-patterns
            
            # Filter patterns by confidence threshold
            filtered_patterns = [
                pattern for pattern in detected_patterns
                if pattern.confidence >= self.config["confidence_threshold"]
            ]
            
            # Generate pattern summary
            pattern_summary = self._generate_pattern_summary(filtered_patterns)
            
            # Calculate overall pattern score
            overall_score = self._calculate_overall_pattern_score(
                filtered_patterns, anti_patterns
            )
            
            # Generate recommendations
            recommendations = await self._generate_pattern_recommendations(
                filtered_patterns, anti_patterns
            )
            
            # Extract learning insights
            learning_insights = await self._extract_learning_insights(
                filtered_patterns, project_path
            )
            
            result = PatternAnalysisResult(
                project_path=str(project_path),
                analysis_timestamp=datetime.now(),
                patterns_detected=filtered_patterns,
                pattern_summary=pattern_summary,
                overall_pattern_score=overall_score,
                recommendations=recommendations,
                anti_patterns=anti_patterns,
                learning_insights=learning_insights
            )
            
            # Store patterns in learning database
            await self.learning_database.store_patterns(result)
            
            logger.info(f"Pattern analysis complete: {len(filtered_patterns)} patterns detected")
            return result
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            raise
    
    async def _collect_project_files(self, project_path: Path) -> List[Dict[str, Any]]:
        """Collect project files for analysis."""
        files = []
        
        try:
            for file_path in project_path.rglob("*"):
                if (file_path.is_file() and 
                    not self._should_ignore_file(file_path) and
                    file_path.suffix in self.config["file_type_weights"]):
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        files.append({
                            "path": str(file_path),
                            "relative_path": str(file_path.relative_to(project_path)),
                            "content": content,
                            "size": len(content),
                            "lines": content.count('\n') + 1,
                            "extension": file_path.suffix,
                            "weight": self.config["file_type_weights"].get(file_path.suffix, 0.5)
                        })
                        
                    except Exception as e:
                        logger.debug(f"Could not read file {file_path}: {e}")
                        continue
            
            logger.info(f"Collected {len(files)} files for analysis")
            return files
            
        except Exception as e:
            logger.error(f"Error collecting project files: {e}")
            return []
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored during analysis."""
        ignore_patterns = [
            "node_modules", "__pycache__", ".git", ".venv", "venv",
            "target", "build", "dist", ".pytest_cache", ".coverage",
            "*.pyc", "*.pyo", "*.log", "*.tmp"
        ]
        
        path_str = str(file_path).lower()
        return any(pattern in path_str for pattern in ignore_patterns)
    
    async def _detect_architectural_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect architectural patterns in the project."""
        patterns = []
        
        architectural_pattern_names = [
            "mvc_pattern", "clean_architecture", "microservices_pattern"
        ]
        
        for pattern_name in architectural_pattern_names:
            pattern_def = self.pattern_definitions[pattern_name]
            pattern = await self._detect_single_pattern(pattern_name, pattern_def, files)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    async def _detect_design_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect design patterns in the project."""
        patterns = []
        
        design_pattern_names = [
            "repository_pattern", "dependency_injection", "factory_pattern",
            "observer_pattern", "singleton_pattern"
        ]
        
        for pattern_name in design_pattern_names:
            pattern_def = self.pattern_definitions[pattern_name]
            pattern = await self._detect_single_pattern(pattern_name, pattern_def, files)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    async def _detect_api_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect API design patterns."""
        patterns = []
        
        api_pattern_names = ["api_versioning"]
        
        for pattern_name in api_pattern_names:
            pattern_def = self.pattern_definitions[pattern_name]
            pattern = await self._detect_single_pattern(pattern_name, pattern_def, files)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    async def _detect_security_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect security-related patterns."""
        patterns = []
        
        # Security patterns would be defined in pattern_definitions
        # For now, this is a placeholder
        
        return patterns
    
    async def _detect_performance_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect performance-related patterns."""
        patterns = []
        
        performance_pattern_names = ["circuit_breaker"]
        
        for pattern_name in performance_pattern_names:
            if pattern_name in self.pattern_definitions:
                pattern_def = self.pattern_definitions[pattern_name]
                pattern = await self._detect_single_pattern(pattern_name, pattern_def, files)
                if pattern:
                    patterns.append(pattern)
        
        return patterns
    
    async def _detect_anti_patterns(self, files: List[Dict]) -> List[DetectedPattern]:
        """Detect anti-patterns in the project."""
        anti_patterns = []
        
        for pattern_name, pattern_def in self.anti_pattern_definitions.items():
            pattern = await self._detect_single_anti_pattern(pattern_name, pattern_def, files)
            if pattern:
                anti_patterns.append(pattern)
        
        return anti_patterns
    
    async def _detect_single_pattern(self, pattern_name: str, pattern_def: Dict, 
                                   files: List[Dict]) -> Optional[DetectedPattern]:
        """Detect a single pattern in the project files."""
        evidence_files = []
        code_examples = []
        usage_count = 0
        confidence_score = 0.0
        
        indicators = pattern_def.get("indicators", {})
        
        # Check directory structure indicators
        if "directory_structure" in indicators:
            dir_score = self._check_directory_structure(
                indicators["directory_structure"], files
            )
            confidence_score += dir_score * 0.4
        
        # Check file pattern indicators
        if "file_patterns" in indicators:
            file_score, file_evidence = self._check_file_patterns(
                indicators["file_patterns"], files
            )
            confidence_score += file_score * 0.3
            evidence_files.extend(file_evidence)
        
        # Check content pattern indicators
        if "content_patterns" in indicators:
            content_score, content_evidence, examples = self._check_content_patterns(
                indicators["content_patterns"], files
            )
            confidence_score += content_score * 0.3
            evidence_files.extend(content_evidence)
            code_examples.extend(examples)
            usage_count = len(examples)
        
        # Apply minimum confidence threshold
        min_confidence = pattern_def.get("min_confidence", 0.5)
        if confidence_score < min_confidence:
            return None
        
        # Determine confidence level
        if confidence_score >= 0.9:
            confidence_level = PatternConfidence.VERY_HIGH
        elif confidence_score >= 0.7:
            confidence_level = PatternConfidence.HIGH
        elif confidence_score >= 0.4:
            confidence_level = PatternConfidence.MEDIUM
        else:
            confidence_level = PatternConfidence.LOW
        
        # Calculate impact scores
        complexity_score = self._calculate_complexity_impact(pattern_def, usage_count)
        maintainability_impact = self._calculate_maintainability_impact(pattern_def)
        performance_impact = self._calculate_performance_impact(pattern_def)
        security_impact = self._calculate_security_impact(pattern_def)
        
        return DetectedPattern(
            pattern_id=f"{pattern_name}_{hash(str(evidence_files))}",
            pattern_type=pattern_def["type"],
            name=pattern_def["name"],
            description=pattern_def["description"],
            confidence=confidence_score,
            confidence_level=confidence_level,
            evidence_files=list(set(evidence_files)),
            code_examples=code_examples[:5],  # Limit to 5 examples
            usage_frequency=usage_count,
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            benefits=pattern_def.get("benefits", []),
            drawbacks=pattern_def.get("drawbacks", []),
            recommendations=pattern_def.get("recommendations", []),
            related_patterns=[],
            complexity_score=complexity_score,
            maintainability_impact=maintainability_impact,
            performance_impact=performance_impact,
            security_impact=security_impact,
            detection_method="static_analysis",
            analysis_version="1.0.0",
            metadata={"pattern_definition": pattern_name}
        )
    
    async def _detect_single_anti_pattern(self, pattern_name: str, pattern_def: Dict,
                                        files: List[Dict]) -> Optional[DetectedPattern]:
        """Detect a single anti-pattern in the project files."""
        # Similar to _detect_single_pattern but for anti-patterns
        # Implementation would be similar but focused on negative patterns
        return None  # Placeholder
    
    def _check_directory_structure(self, required_dirs: List[str], files: List[Dict]) -> float:
        """Check if required directory structure exists."""
        all_paths = {Path(f["relative_path"]).parent for f in files}
        all_dirs = {str(path) for path in all_paths}
        
        found_dirs = sum(1 for req_dir in required_dirs 
                        if any(req_dir in dir_path for dir_path in all_dirs))
        
        return found_dirs / len(required_dirs) if required_dirs else 0.0
    
    def _check_file_patterns(self, file_patterns: List[str], 
                           files: List[Dict]) -> Tuple[float, List[str]]:
        """Check if file patterns exist in the project."""
        evidence_files = []
        pattern_matches = 0
        
        for pattern in file_patterns:
            for file_info in files:
                if re.search(pattern, file_info["relative_path"], re.IGNORECASE):
                    pattern_matches += 1
                    evidence_files.append(file_info["relative_path"])
        
        # Score based on number of matching patterns
        score = min(pattern_matches / len(file_patterns), 1.0) if file_patterns else 0.0
        return score, evidence_files
    
    def _check_content_patterns(self, content_patterns: List[str], 
                              files: List[Dict]) -> Tuple[float, List[str], List[str]]:
        """Check if content patterns exist in project files."""
        evidence_files = []
        code_examples = []
        total_matches = 0
        
        for pattern in content_patterns:
            pattern_matches = 0
            for file_info in files:
                matches = re.findall(pattern, file_info["content"], re.IGNORECASE | re.MULTILINE)
                if matches:
                    pattern_matches += len(matches)
                    evidence_files.append(file_info["relative_path"])
                    
                    # Extract code examples
                    for match in matches[:2]:  # Limit to 2 examples per file
                        lines = file_info["content"].split('\n')
                        for i, line in enumerate(lines):
                            if re.search(pattern, line, re.IGNORECASE):
                                # Get context around the match
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                context = '\n'.join(lines[start:end])
                                code_examples.append(context)
                                break
            
            total_matches += pattern_matches
        
        # Score based on pattern density
        if content_patterns and files:
            avg_matches_per_pattern = total_matches / len(content_patterns)
            score = min(avg_matches_per_pattern / 10, 1.0)  # Normalize to max of 1.0
        else:
            score = 0.0
        
        return score, evidence_files, code_examples
    
    def _calculate_complexity_impact(self, pattern_def: Dict, usage_count: int) -> float:
        """Calculate complexity impact of the pattern."""
        # Patterns like microservices increase complexity
        complexity_patterns = ["microservices_pattern", "clean_architecture"]
        if pattern_def.get("name", "").lower() in complexity_patterns:
            return 0.7 + (usage_count * 0.05)
        return 0.3 + (usage_count * 0.02)
    
    def _calculate_maintainability_impact(self, pattern_def: Dict) -> float:
        """Calculate maintainability impact of the pattern."""
        # Most good patterns improve maintainability
        if pattern_def.get("benefits"):
            maintainability_keywords = ["maintainability", "testability", "separation"]
            benefits_text = " ".join(pattern_def["benefits"]).lower()
            if any(keyword in benefits_text for keyword in maintainability_keywords):
                return 0.8
        return 0.5
    
    def _calculate_performance_impact(self, pattern_def: Dict) -> float:
        """Calculate performance impact of the pattern."""
        performance_patterns = ["circuit_breaker", "singleton_pattern"]
        if any(perf_pattern in pattern_def.get("name", "").lower() 
               for perf_pattern in performance_patterns):
            return 0.7
        return 0.5
    
    def _calculate_security_impact(self, pattern_def: Dict) -> float:
        """Calculate security impact of the pattern."""
        if pattern_def.get("type") == PatternType.SECURITY:
            return 0.8
        return 0.5
    
    def _generate_pattern_summary(self, patterns: List[DetectedPattern]) -> Dict[PatternType, int]:
        """Generate summary of detected patterns by type."""
        summary = defaultdict(int)
        for pattern in patterns:
            summary[pattern.pattern_type] += 1
        return dict(summary)
    
    def _calculate_overall_pattern_score(self, patterns: List[DetectedPattern], 
                                       anti_patterns: List[DetectedPattern]) -> float:
        """Calculate overall pattern quality score."""
        if not patterns and not anti_patterns:
            return 0.5  # Neutral score
        
        # Positive score from good patterns
        positive_score = sum(pattern.confidence for pattern in patterns)
        
        # Negative score from anti-patterns
        negative_score = sum(anti_pattern.confidence for anti_pattern in anti_patterns)
        
        # Normalize to 0-1 scale
        total_patterns = len(patterns) + len(anti_patterns)
        if total_patterns == 0:
            return 0.5
        
        net_score = (positive_score - negative_score) / total_patterns
        return max(0.0, min(1.0, (net_score + 1.0) / 2.0))  # Normalize to 0-1
    
    async def _generate_pattern_recommendations(self, patterns: List[DetectedPattern],
                                              anti_patterns: List[DetectedPattern]) -> List[str]:
        """Generate recommendations based on detected patterns."""
        recommendations = []
        
        # Recommendations from detected patterns
        for pattern in patterns:
            recommendations.extend(pattern.recommendations)
        
        # Recommendations from anti-patterns
        for anti_pattern in anti_patterns:
            recommendations.extend(anti_pattern.recommendations)
        
        # Remove duplicates and return
        return list(set(recommendations))
    
    async def _extract_learning_insights(self, patterns: List[DetectedPattern], 
                                       project_path: Path) -> List[str]:
        """Extract learning insights from the analysis."""
        insights = []
        
        # Pattern distribution insights
        pattern_types = [pattern.pattern_type for pattern in patterns]
        type_counts = Counter(pattern_types)
        
        if type_counts.get(PatternType.ARCHITECTURAL, 0) > 2:
            insights.append("Strong architectural pattern usage indicates mature design")
        
        if type_counts.get(PatternType.DESIGN, 0) > 3:
            insights.append("Rich design pattern usage suggests good OOP practices")
        
        # Confidence insights
        high_confidence_patterns = [p for p in patterns if p.confidence > 0.8]
        if len(high_confidence_patterns) > len(patterns) * 0.7:
            insights.append("Consistent pattern implementation across the project")
        
        return insights


class PatternLearningDatabase:
    """Database for storing and learning from detected patterns."""
    
    def __init__(self):
        self.patterns_db = []  # In-memory storage for now
    
    async def store_patterns(self, analysis_result: PatternAnalysisResult):
        """Store pattern analysis results for learning."""
        self.patterns_db.append(analysis_result)
        logger.info(f"Stored pattern analysis for {analysis_result.project_path}")
    
    async def get_pattern_insights(self, pattern_type: PatternType) -> List[str]:
        """Get insights about a specific pattern type from historical data."""
        # TODO: Implement pattern learning and insight generation
        return []


# Example usage
if __name__ == "__main__":
    async def main():
        analyzer = PatternAnalyzer()
        
        # Analyze patterns in a project
        project_path = "/path/to/your/project"
        result = await analyzer.analyze_patterns(project_path)
        
        print(f"Project: {result.project_path}")
        print(f"Patterns detected: {len(result.patterns_detected)}")
        print(f"Overall score: {result.overall_pattern_score:.2f}")
        
        print("\nDetected Patterns:")
        for pattern in result.patterns_detected:
            print(f"- {pattern.name} ({pattern.confidence:.2f} confidence)")
        
        print("\nRecommendations:")
        for recommendation in result.recommendations:
            print(f"- {recommendation}")
    
    asyncio.run(main())