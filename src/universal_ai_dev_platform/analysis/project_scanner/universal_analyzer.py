"""
Universal Project Analyzer

Comprehensive analysis engine that can understand any project type, technology stack,
and provide intelligent insights for improvement and enhancement.
"""

import asyncio
import json
import logging
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict

import tree_sitter
from tree_sitter import Language, Parser
import ast_grep
from packaging import version

logger = logging.getLogger(__name__)


@dataclass
class TechnologyStack:
    """Represents detected technology stack information."""
    
    primary_language: str
    secondary_languages: List[str]
    frameworks: List[str]
    databases: List[str]
    build_tools: List[str]
    package_managers: List[str]
    deployment_targets: List[str]
    development_tools: List[str]
    confidence_score: float


@dataclass
class ArchitecturePattern:
    """Represents detected architecture patterns."""
    
    pattern_name: str
    confidence: float
    description: str
    evidence: List[str]
    recommendations: List[str]


@dataclass
class ProjectHealth:
    """Comprehensive project health assessment."""
    
    overall_score: float  # 0-100
    code_quality: float
    security_score: float
    performance_score: float
    maintainability_score: float
    test_coverage: Optional[float]
    documentation_score: float
    dependency_health: float
    issues: List[str]
    recommendations: List[str]


@dataclass
class ProjectAnalysis:
    """Complete project analysis results."""
    
    project_path: str
    project_name: str
    project_type: str
    technology_stack: TechnologyStack
    architecture_patterns: List[ArchitecturePattern]
    health_assessment: ProjectHealth
    file_structure: Dict[str, Any]
    dependencies: Dict[str, List[str]]
    configuration_files: List[str]
    enhancement_opportunities: List[str]
    migration_recommendations: List[str]
    estimated_complexity: str  # "simple", "moderate", "complex", "enterprise"
    analysis_metadata: Dict[str, Any]


class UniversalProjectAnalyzer:
    """
    Universal project analyzer that can understand and analyze any type of software project.
    Uses multiple analysis techniques including AST parsing, pattern matching, and heuristics.
    """
    
    def __init__(self):
        self.supported_languages = {
            "python": [".py", ".pyw", ".pyx"],
            "javascript": [".js", ".jsx", ".mjs"],
            "typescript": [".ts", ".tsx"],
            "rust": [".rs"],
            "go": [".go"],
            "java": [".java"],
            "cpp": [".cpp", ".cxx", ".cc", ".c"],
            "csharp": [".cs"],
            "php": [".php"],
            "ruby": [".rb"],
            "swift": [".swift"],
            "kotlin": [".kt", ".kts"],
            "scala": [".scala"],
        }
        
        self.framework_patterns = self._load_framework_patterns()
        self.architecture_patterns = self._load_architecture_patterns()
        self.project_type_indicators = self._load_project_type_indicators()
        
        # Initialize parsers for supported languages
        self.parsers = {}
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize Tree-sitter parsers for supported languages."""
        # In a real implementation, you would need to compile and load Tree-sitter grammars
        # This is a placeholder for the parser initialization
        logger.info("Initializing language parsers...")
        
        # TODO: Load actual Tree-sitter parsers
        # self.parsers["python"] = Parser()
        # self.parsers["python"].set_language(Language(python_lib, "python"))
    
    def _load_framework_patterns(self) -> Dict[str, Dict]:
        """Load framework detection patterns."""
        return {
            "react": {
                "files": ["package.json"],
                "content_patterns": [
                    r'"react":\s*"[^"]*"',
                    r'import.*from\s+[\'"]react[\'"]',
                    r'from\s+[\'"]react[\'"]'
                ],
                "directory_patterns": ["src/components", "src/hooks"],
                "confidence_boost": 0.3
            },
            "vue": {
                "files": ["package.json", "vue.config.js"],
                "content_patterns": [
                    r'"vue":\s*"[^"]*"',
                    r'<template>.*</template>',
                    r'export\s+default\s*{.*template:'
                ],
                "confidence_boost": 0.3
            },
            "angular": {
                "files": ["angular.json", "package.json"],
                "content_patterns": [
                    r'"@angular/core":\s*"[^"]*"',
                    r'@Component\s*\(',
                    r'@Injectable\s*\('
                ],
                "confidence_boost": 0.3
            },
            "express": {
                "files": ["package.json"],
                "content_patterns": [
                    r'"express":\s*"[^"]*"',
                    r'require\([\'"]express[\'"]\)',
                    r'app\.get\s*\(',
                    r'app\.listen\s*\('
                ],
                "confidence_boost": 0.2
            },
            "django": {
                "files": ["manage.py", "settings.py", "requirements.txt"],
                "content_patterns": [
                    r'from\s+django',
                    r'import\s+django',
                    r'DJANGO_SETTINGS_MODULE'
                ],
                "directory_patterns": ["templates", "static"],
                "confidence_boost": 0.3
            },
            "flask": {
                "files": ["app.py", "requirements.txt"],
                "content_patterns": [
                    r'from\s+flask',
                    r'import\s+Flask',
                    r'app\s*=\s*Flask\s*\('
                ],
                "confidence_boost": 0.2
            },
            "nextjs": {
                "files": ["next.config.js", "package.json"],
                "content_patterns": [
                    r'"next":\s*"[^"]*"',
                    r'import.*from\s+[\'"]next[\'"]'
                ],
                "directory_patterns": ["pages", "app"],
                "confidence_boost": 0.3
            },
            "fastapi": {
                "files": ["main.py", "requirements.txt"],
                "content_patterns": [
                    r'from\s+fastapi',
                    r'import\s+FastAPI',
                    r'app\s*=\s*FastAPI\s*\('
                ],
                "confidence_boost": 0.2
            }
        }
    
    def _load_architecture_patterns(self) -> Dict[str, Dict]:
        """Load architecture pattern detection rules."""
        return {
            "microservices": {
                "indicators": [
                    "multiple package.json/requirements.txt files",
                    "docker-compose.yml with multiple services",
                    "kubernetes deployment files",
                    "service discovery configuration"
                ],
                "file_patterns": ["docker-compose.yml", "k8s/", "services/"],
                "confidence_threshold": 0.6
            },
            "monolithic": {
                "indicators": [
                    "single large application structure",
                    "centralized configuration",
                    "single deployment unit"
                ],
                "confidence_threshold": 0.4
            },
            "mvc": {
                "indicators": [
                    "models/, views/, controllers/ directories",
                    "clear separation of concerns",
                    "routing configuration"
                ],
                "directory_patterns": ["models", "views", "controllers"],
                "confidence_threshold": 0.5
            },
            "clean_architecture": {
                "indicators": [
                    "domain/, application/, infrastructure/ layers",
                    "dependency inversion patterns",
                    "interface segregation"
                ],
                "directory_patterns": ["domain", "application", "infrastructure"],
                "confidence_threshold": 0.6
            },
            "jamstack": {
                "indicators": [
                    "static site generation",
                    "API integration patterns",
                    "CDN deployment configuration"
                ],
                "file_patterns": ["netlify.toml", "vercel.json", "gatsby-config.js"],
                "confidence_threshold": 0.5
            }
        }
    
    def _load_project_type_indicators(self) -> Dict[str, Dict]:
        """Load project type detection indicators."""
        return {
            "web_application": {
                "indicators": ["package.json", "index.html", "src/", "public/"],
                "frameworks": ["react", "vue", "angular", "svelte"],
                "confidence_boost": 0.3
            },
            "api_service": {
                "indicators": ["main.py", "app.py", "server.js", "routes/"],
                "frameworks": ["express", "fastapi", "django", "flask"],
                "confidence_boost": 0.3
            },
            "mobile_app": {
                "indicators": ["App.js", "android/", "ios/", "pubspec.yaml"],
                "frameworks": ["react-native", "flutter", "ionic"],
                "confidence_boost": 0.4
            },
            "desktop_app": {
                "indicators": ["main.py", "main.cpp", "MainWindow.xaml"],
                "frameworks": ["electron", "tauri", "qt", "wpf"],
                "confidence_boost": 0.3
            },
            "cli_tool": {
                "indicators": ["setup.py", "Cargo.toml", "go.mod", "main.go"],
                "patterns": ["command-line", "cli", "terminal"],
                "confidence_boost": 0.2
            },
            "library": {
                "indicators": ["setup.py", "lib.rs", "index.js", "package.json"],
                "patterns": ["library", "package", "module"],
                "confidence_boost": 0.2
            },
            "data_science": {
                "indicators": ["*.ipynb", "requirements.txt", "data/", "models/"],
                "patterns": ["jupyter", "pandas", "numpy", "scikit-learn"],
                "confidence_boost": 0.3
            },
            "game": {
                "indicators": ["Assets/", "Scenes/", "*.unity", "*.godot"],
                "frameworks": ["unity", "godot", "unreal"],
                "confidence_boost": 0.4
            }
        }
    
    async def analyze_project(self, project_path: str) -> ProjectAnalysis:
        """
        Perform comprehensive analysis of a project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Complete project analysis results
        """
        logger.info(f"Starting analysis of project: {project_path}")
        
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        try:
            # Parallel analysis tasks
            tasks = [
                self._analyze_file_structure(project_path),
                self._detect_technology_stack(project_path),
                self._detect_architecture_patterns(project_path),
                self._assess_project_health(project_path),
                self._analyze_dependencies(project_path),
                self._identify_configuration_files(project_path),
            ]
            
            results = await asyncio.gather(*tasks)
            
            file_structure = results[0]
            tech_stack = results[1]
            architecture_patterns = results[2]
            health_assessment = results[3]
            dependencies = results[4]
            config_files = results[5]
            
            # Determine project type and complexity
            project_type = await self._determine_project_type(
                project_path, tech_stack, file_structure
            )
            complexity = self._estimate_complexity(
                file_structure, tech_stack, dependencies
            )
            
            # Generate enhancement opportunities and recommendations
            enhancement_opportunities = await self._identify_enhancement_opportunities(
                tech_stack, architecture_patterns, health_assessment
            )
            migration_recommendations = await self._generate_migration_recommendations(
                tech_stack, architecture_patterns
            )
            
            analysis = ProjectAnalysis(
                project_path=str(project_path),
                project_name=project_path.name,
                project_type=project_type,
                technology_stack=tech_stack,
                architecture_patterns=architecture_patterns,
                health_assessment=health_assessment,
                file_structure=file_structure,
                dependencies=dependencies,
                configuration_files=config_files,
                enhancement_opportunities=enhancement_opportunities,
                migration_recommendations=migration_recommendations,
                estimated_complexity=complexity,
                analysis_metadata={
                    "analysis_version": "1.0.0",
                    "analysis_timestamp": asyncio.get_event_loop().time(),
                    "analyzer_version": "0.1.0"
                }
            )
            
            logger.info(f"Analysis completed for {project_path.name}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing project {project_path}: {e}")
            raise
    
    async def _analyze_file_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze project file structure and organization."""
        structure = {
            "total_files": 0,
            "directories": [],
            "file_types": defaultdict(int),
            "largest_files": [],
            "depth": 0,
            "organization_score": 0.0
        }
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip hidden and common ignore directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d not in ['node_modules', '__pycache__', 'target', 'dist', 'build']]
                
                current_depth = len(Path(root).relative_to(project_path).parts)
                structure["depth"] = max(structure["depth"], current_depth)
                
                for file in files:
                    if file.startswith('.'):
                        continue
                        
                    file_path = Path(root) / file
                    structure["total_files"] += 1
                    
                    # Count file types
                    suffix = file_path.suffix.lower()
                    structure["file_types"][suffix] += 1
                    
                    # Track largest files
                    try:
                        size = file_path.stat().st_size
                        structure["largest_files"].append((str(file_path), size))
                    except OSError:
                        pass
            
            # Sort and limit largest files
            structure["largest_files"].sort(key=lambda x: x[1], reverse=True)
            structure["largest_files"] = structure["largest_files"][:10]
            
            # Calculate organization score based on structure patterns
            structure["organization_score"] = self._calculate_organization_score(
                project_path, structure
            )
            
        except Exception as e:
            logger.error(f"Error analyzing file structure: {e}")
        
        return structure
    
    def _calculate_organization_score(self, project_path: Path, structure: Dict) -> float:
        """Calculate how well-organized the project structure is."""
        score = 0.0
        
        # Check for common organizational patterns
        common_dirs = ['src', 'lib', 'tests', 'docs', 'config']
        found_dirs = [d for d in common_dirs if (project_path / d).exists()]
        score += len(found_dirs) * 0.1
        
        # Penalize excessive depth
        if structure["depth"] > 6:
            score -= 0.2
        elif structure["depth"] < 3:
            score -= 0.1
        
        # Reward reasonable file distribution
        if 10 <= structure["total_files"] <= 1000:
            score += 0.2
        
        return min(max(score, 0.0), 1.0)
    
    async def _detect_technology_stack(self, project_path: Path) -> TechnologyStack:
        """Detect the technology stack used in the project."""
        detected_tech = {
            "languages": defaultdict(float),
            "frameworks": defaultdict(float),
            "databases": defaultdict(float),
            "build_tools": defaultdict(float),
            "package_managers": defaultdict(float),
            "deployment_targets": defaultdict(float),
            "development_tools": defaultdict(float)
        }
        
        # Analyze file extensions for primary language
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'target']]
            
            for file in files:
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                
                # Detect languages by file extensions
                for lang, extensions in self.supported_languages.items():
                    if suffix in extensions:
                        detected_tech["languages"][lang] += 1
        
        # Analyze configuration files and package manifests
        await self._analyze_package_files(project_path, detected_tech)
        
        # Detect frameworks based on patterns
        await self._detect_frameworks(project_path, detected_tech)
        
        # Normalize scores and determine primary language
        total_lang_files = sum(detected_tech["languages"].values())
        if total_lang_files > 0:
            for lang in detected_tech["languages"]:
                detected_tech["languages"][lang] /= total_lang_files
        
        # Determine primary and secondary languages
        sorted_languages = sorted(
            detected_tech["languages"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        primary_language = sorted_languages[0][0] if sorted_languages else "unknown"
        secondary_languages = [lang for lang, score in sorted_languages[1:3] if score > 0.1]
        
        # Calculate overall confidence
        confidence = self._calculate_tech_stack_confidence(detected_tech)
        
        return TechnologyStack(
            primary_language=primary_language,
            secondary_languages=secondary_languages,
            frameworks=list(detected_tech["frameworks"].keys()),
            databases=list(detected_tech["databases"].keys()),
            build_tools=list(detected_tech["build_tools"].keys()),
            package_managers=list(detected_tech["package_managers"].keys()),
            deployment_targets=list(detected_tech["deployment_targets"].keys()),
            development_tools=list(detected_tech["development_tools"].keys()),
            confidence_score=confidence
        )
    
    async def _analyze_package_files(self, project_path: Path, detected_tech: Dict):
        """Analyze package manifests and configuration files."""
        package_files = {
            "package.json": self._analyze_package_json,
            "requirements.txt": self._analyze_requirements_txt,
            "Cargo.toml": self._analyze_cargo_toml,
            "go.mod": self._analyze_go_mod,
            "pom.xml": self._analyze_pom_xml,
            "build.gradle": self._analyze_gradle,
        }
        
        for filename, analyzer in package_files.items():
            file_path = project_path / filename
            if file_path.exists():
                try:
                    await analyzer(file_path, detected_tech)
                except Exception as e:
                    logger.error(f"Error analyzing {filename}: {e}")
    
    async def _analyze_package_json(self, file_path: Path, detected_tech: Dict):
        """Analyze package.json for Node.js projects."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            detected_tech["package_managers"]["npm"] += 1.0
            
            # Check dependencies for frameworks
            all_deps = {}
            all_deps.update(data.get("dependencies", {}))
            all_deps.update(data.get("devDependencies", {}))
            
            framework_mappings = {
                "react": "react",
                "vue": "vue",
                "@angular/core": "angular",
                "express": "express",
                "next": "nextjs",
                "nuxt": "nuxtjs",
                "svelte": "svelte",
                "electron": "electron",
                "typescript": "typescript"
            }
            
            for dep, framework in framework_mappings.items():
                if dep in all_deps:
                    detected_tech["frameworks"][framework] += 0.8
            
            # Detect build tools
            build_tools = {
                "webpack": "webpack",
                "vite": "vite", 
                "rollup": "rollup",
                "parcel": "parcel",
                "esbuild": "esbuild"
            }
            
            for tool, name in build_tools.items():
                if tool in all_deps:
                    detected_tech["build_tools"][name] += 0.6
            
        except Exception as e:
            logger.error(f"Error parsing package.json: {e}")
    
    async def _analyze_requirements_txt(self, file_path: Path, detected_tech: Dict):
        """Analyze requirements.txt for Python projects."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            detected_tech["package_managers"]["pip"] += 1.0
            
            framework_patterns = {
                "django": r"django[>=<~!]",
                "flask": r"flask[>=<~!]", 
                "fastapi": r"fastapi[>=<~!]",
                "tornado": r"tornado[>=<~!]",
                "pyramid": r"pyramid[>=<~!]"
            }
            
            for framework, pattern in framework_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    detected_tech["frameworks"][framework] += 0.8
            
            # Detect data science frameworks
            ds_frameworks = ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"]
            for framework in ds_frameworks:
                if framework in content.lower():
                    detected_tech["frameworks"][framework] += 0.6
            
        except Exception as e:
            logger.error(f"Error parsing requirements.txt: {e}")
    
    async def _analyze_cargo_toml(self, file_path: Path, detected_tech: Dict):
        """Analyze Cargo.toml for Rust projects."""
        detected_tech["package_managers"]["cargo"] += 1.0
        detected_tech["build_tools"]["cargo"] += 1.0
        # TODO: Add more detailed Rust dependency analysis
    
    async def _analyze_go_mod(self, file_path: Path, detected_tech: Dict):
        """Analyze go.mod for Go projects."""
        detected_tech["package_managers"]["go_modules"] += 1.0
        detected_tech["build_tools"]["go"] += 1.0
        # TODO: Add more detailed Go dependency analysis
    
    async def _analyze_pom_xml(self, file_path: Path, detected_tech: Dict):
        """Analyze pom.xml for Java projects."""
        detected_tech["package_managers"]["maven"] += 1.0
        detected_tech["build_tools"]["maven"] += 1.0
        # TODO: Add more detailed Maven dependency analysis
    
    async def _analyze_gradle(self, file_path: Path, detected_tech: Dict):
        """Analyze build.gradle for Java/Kotlin projects."""
        detected_tech["package_managers"]["gradle"] += 1.0
        detected_tech["build_tools"]["gradle"] += 1.0
        # TODO: Add more detailed Gradle dependency analysis
    
    async def _detect_frameworks(self, project_path: Path, detected_tech: Dict):
        """Detect frameworks based on file patterns and content."""
        for framework, patterns in self.framework_patterns.items():
            confidence = 0.0
            
            # Check for specific files
            for file_pattern in patterns.get("files", []):
                if (project_path / file_pattern).exists():
                    confidence += 0.3
            
            # Check directory patterns
            for dir_pattern in patterns.get("directory_patterns", []):
                if (project_path / dir_pattern).exists():
                    confidence += 0.2
            
            # Check content patterns in relevant files
            content_confidence = await self._check_content_patterns(
                project_path, patterns.get("content_patterns", [])
            )
            confidence += content_confidence
            
            if confidence > 0.5:
                detected_tech["frameworks"][framework] += confidence
    
    async def _check_content_patterns(self, project_path: Path, patterns: List[str]) -> float:
        """Check for content patterns in project files."""
        confidence = 0.0
        files_checked = 0
        max_files = 20  # Limit to avoid performance issues
        
        try:
            for root, dirs, files in os.walk(project_path):
                if files_checked >= max_files:
                    break
                
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d not in ['node_modules', '__pycache__']]
                
                for file in files[:5]:  # Check max 5 files per directory
                    if files_checked >= max_files:
                        break
                    
                    file_path = Path(root) / file
                    if file_path.suffix in ['.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rs']:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(10000)  # Read first 10KB
                            
                            for pattern in patterns:
                                if re.search(pattern, content, re.IGNORECASE):
                                    confidence += 0.1
                            
                            files_checked += 1
                            
                        except Exception:
                            continue  # Skip files that can't be read
        
        except Exception as e:
            logger.error(f"Error checking content patterns: {e}")
        
        return min(confidence, 0.8)  # Cap at 0.8
    
    def _calculate_tech_stack_confidence(self, detected_tech: Dict) -> float:
        """Calculate overall confidence in technology stack detection."""
        total_signals = 0
        for category in detected_tech.values():
            total_signals += len(category)
        
        # Base confidence on number of detection signals
        if total_signals >= 10:
            return 0.9
        elif total_signals >= 5:
            return 0.7
        elif total_signals >= 2:
            return 0.5
        else:
            return 0.3
    
    async def _detect_architecture_patterns(self, project_path: Path) -> List[ArchitecturePattern]:
        """Detect architectural patterns in the project."""
        patterns = []
        
        for pattern_name, config in self.architecture_patterns.items():
            confidence = await self._assess_architecture_pattern(
                project_path, pattern_name, config
            )
            
            if confidence >= config.get("confidence_threshold", 0.5):
                pattern = ArchitecturePattern(
                    pattern_name=pattern_name,
                    confidence=confidence,
                    description=f"Detected {pattern_name.replace('_', ' ')} architecture pattern",
                    evidence=config.get("indicators", []),
                    recommendations=self._get_pattern_recommendations(pattern_name)
                )
                patterns.append(pattern)
        
        return patterns
    
    async def _assess_architecture_pattern(self, project_path: Path, pattern_name: str, config: Dict) -> float:
        """Assess confidence for a specific architecture pattern."""
        confidence = 0.0
        
        # Check for file patterns
        for file_pattern in config.get("file_patterns", []):
            if list(project_path.glob(file_pattern)):
                confidence += 0.3
        
        # Check for directory patterns
        for dir_pattern in config.get("directory_patterns", []):
            if (project_path / dir_pattern).exists():
                confidence += 0.2
        
        # Additional pattern-specific logic
        if pattern_name == "microservices":
            # Look for multiple service directories or docker-compose
            service_indicators = 0
            if (project_path / "docker-compose.yml").exists():
                service_indicators += 1
            
            # Count potential service directories
            service_dirs = ["services", "apps", "microservices"]
            for service_dir in service_dirs:
                if (project_path / service_dir).exists():
                    subdirs = list((project_path / service_dir).iterdir())
                    if len([d for d in subdirs if d.is_dir()]) > 1:
                        service_indicators += 1
            
            confidence += service_indicators * 0.25
        
        return min(confidence, 1.0)
    
    def _get_pattern_recommendations(self, pattern_name: str) -> List[str]:
        """Get recommendations for detected architecture patterns."""
        recommendations = {
            "microservices": [
                "Consider implementing service mesh for communication",
                "Ensure proper monitoring and distributed tracing",
                "Implement circuit breaker patterns for resilience"
            ],
            "monolithic": [
                "Consider modularization for better maintainability",
                "Implement clear module boundaries",
                "Plan for potential future microservices migration"
            ],
            "mvc": [
                "Ensure clear separation of concerns",
                "Consider implementing dependency injection",
                "Add comprehensive testing for each layer"
            ]
        }
        
        return recommendations.get(pattern_name, [])
    
    async def _assess_project_health(self, project_path: Path) -> ProjectHealth:
        """Assess overall project health across multiple dimensions."""
        health = ProjectHealth(
            overall_score=0.0,
            code_quality=0.0,
            security_score=0.0,
            performance_score=0.0,
            maintainability_score=0.0,
            test_coverage=None,
            documentation_score=0.0,
            dependency_health=0.0,
            issues=[],
            recommendations=[]
        )
        
        try:
            # Assess different health dimensions
            health.code_quality = await self._assess_code_quality(project_path)
            health.security_score = await self._assess_security(project_path)
            health.maintainability_score = await self._assess_maintainability(project_path)
            health.documentation_score = await self._assess_documentation(project_path)
            health.dependency_health = await self._assess_dependency_health(project_path)
            
            # Calculate overall score
            scores = [
                health.code_quality,
                health.security_score,
                health.maintainability_score,
                health.documentation_score,
                health.dependency_health
            ]
            health.overall_score = sum(scores) / len(scores) * 100
            
            # Generate issues and recommendations
            health.issues = await self._identify_health_issues(project_path, health)
            health.recommendations = await self._generate_health_recommendations(health)
            
        except Exception as e:
            logger.error(f"Error assessing project health: {e}")
        
        return health
    
    async def _assess_code_quality(self, project_path: Path) -> float:
        """Assess code quality based on various metrics."""
        score = 0.5  # Base score
        
        # Check for linting configuration
        lint_configs = [".eslintrc", ".pylintrc", "pyproject.toml", "tslint.json"]
        for config in lint_configs:
            if (project_path / config).exists():
                score += 0.15
                break
        
        # Check for code formatting configuration
        format_configs = [".prettierrc", ".black", "rustfmt.toml"]
        for config in format_configs:
            if (project_path / config).exists():
                score += 0.1
                break
        
        # TODO: Add more sophisticated code quality analysis
        # - Cyclomatic complexity analysis
        # - Code duplication detection
        # - Naming convention analysis
        
        return min(score, 1.0)
    
    async def _assess_security(self, project_path: Path) -> float:
        """Assess security posture of the project."""
        score = 0.5  # Base score
        
        # Check for security-related files
        security_files = [".github/workflows/security.yml", "SECURITY.md"]
        for file in security_files:
            if (project_path / file).exists():
                score += 0.1
        
        # Check for dependency scanning
        if (project_path / ".github/workflows").exists():
            # Look for dependency scanning in CI
            score += 0.1
        
        # TODO: Add more sophisticated security analysis
        # - Dependency vulnerability scanning
        # - Secret detection
        # - Security best practices validation
        
        return min(score, 1.0)
    
    async def _assess_maintainability(self, project_path: Path) -> float:
        """Assess code maintainability."""
        score = 0.5  # Base score
        
        # Check for proper project structure
        common_dirs = ["src", "lib", "tests", "docs"]
        found_dirs = sum(1 for d in common_dirs if (project_path / d).exists())
        score += found_dirs * 0.05
        
        # Check for CI/CD configuration
        ci_configs = [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile"]
        for config in ci_configs:
            if (project_path / config).exists():
                score += 0.15
                break
        
        return min(score, 1.0)
    
    async def _assess_documentation(self, project_path: Path) -> float:
        """Assess documentation quality and completeness."""
        score = 0.0
        
        # Check for README
        readme_files = ["README.md", "README.txt", "README.rst"]
        for readme in readme_files:
            if (project_path / readme).exists():
                score += 0.4
                break
        
        # Check for additional documentation
        doc_dirs = ["docs", "documentation", "wiki"]
        for doc_dir in doc_dirs:
            if (project_path / doc_dir).exists():
                score += 0.2
                break
        
        # Check for API documentation
        api_docs = ["openapi.yml", "swagger.yml", "api.md"]
        for api_doc in api_docs:
            if (project_path / api_doc).exists():
                score += 0.2
                break
        
        # Check for changelog
        changelogs = ["CHANGELOG.md", "HISTORY.md", "RELEASES.md"]
        for changelog in changelogs:
            if (project_path / changelog).exists():
                score += 0.1
                break
        
        # Check for contributing guidelines
        contributing = ["CONTRIBUTING.md", "CONTRIBUTE.md"]
        for contrib in contributing:
            if (project_path / contrib).exists():
                score += 0.1
                break
        
        return min(score, 1.0)
    
    async def _assess_dependency_health(self, project_path: Path) -> float:
        """Assess health of project dependencies."""
        score = 0.7  # Base score assuming reasonable health
        
        # TODO: Implement sophisticated dependency health analysis
        # - Check for outdated dependencies
        # - Analyze dependency tree complexity
        # - Check for security vulnerabilities in dependencies
        # - Assess dependency license compatibility
        
        return score
    
    async def _identify_health_issues(self, project_path: Path, health: ProjectHealth) -> List[str]:
        """Identify specific health issues in the project."""
        issues = []
        
        if health.code_quality < 0.6:
            issues.append("Code quality below recommended threshold")
        
        if health.security_score < 0.7:
            issues.append("Security practices need improvement")
        
        if health.documentation_score < 0.5:
            issues.append("Documentation is incomplete")
        
        if not (project_path / "tests").exists() and not list(project_path.glob("**/test_*.py")):
            issues.append("No test directory or test files found")
        
        return issues
    
    async def _generate_health_recommendations(self, health: ProjectHealth) -> List[str]:
        """Generate recommendations for improving project health."""
        recommendations = []
        
        if health.code_quality < 0.8:
            recommendations.append("Add code linting and formatting tools")
        
        if health.security_score < 0.8:
            recommendations.append("Implement dependency vulnerability scanning")
        
        if health.documentation_score < 0.7:
            recommendations.append("Improve project documentation")
        
        if health.overall_score < 70:
            recommendations.append("Consider implementing CI/CD pipeline")
        
        return recommendations
    
    async def _analyze_dependencies(self, project_path: Path) -> Dict[str, List[str]]:
        """Analyze project dependencies."""
        dependencies = {
            "production": [],
            "development": [],
            "optional": []
        }
        
        # TODO: Implement dependency analysis for different package managers
        # - npm/yarn (package.json)
        # - pip (requirements.txt, setup.py, pyproject.toml)
        # - cargo (Cargo.toml)
        # - go modules (go.mod)
        # - maven (pom.xml)
        # - gradle (build.gradle)
        
        return dependencies
    
    async def _identify_configuration_files(self, project_path: Path) -> List[str]:
        """Identify configuration files in the project."""
        config_patterns = [
            "*.json", "*.yml", "*.yaml", "*.toml", "*.ini", "*.conf",
            ".env*", "Dockerfile", "docker-compose.yml", "Makefile"
        ]
        
        config_files = []
        for pattern in config_patterns:
            config_files.extend([str(f) for f in project_path.glob(pattern)])
        
        return config_files
    
    async def _determine_project_type(self, project_path: Path, tech_stack: TechnologyStack, file_structure: Dict) -> str:
        """Determine the primary type of the project."""
        type_scores = defaultdict(float)
        
        # Score based on technology stack
        for project_type, indicators in self.project_type_indicators.items():
            score = 0.0
            
            # Check framework alignment
            for framework in indicators.get("frameworks", []):
                if framework in tech_stack.frameworks:
                    score += indicators.get("confidence_boost", 0.2)
            
            # Check file/directory indicators
            for indicator in indicators.get("indicators", []):
                if (project_path / indicator).exists():
                    score += 0.1
            
            type_scores[project_type] = score
        
        # Return the highest scoring type, or "unknown" if no clear match
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "unknown"
    
    def _estimate_complexity(self, file_structure: Dict, tech_stack: TechnologyStack, dependencies: Dict) -> str:
        """Estimate project complexity level."""
        complexity_score = 0
        
        # File count contribution
        file_count = file_structure.get("total_files", 0)
        if file_count > 1000:
            complexity_score += 3
        elif file_count > 100:
            complexity_score += 2
        elif file_count > 10:
            complexity_score += 1
        
        # Technology diversity contribution
        total_tech = (len(tech_stack.frameworks) + 
                     len(tech_stack.databases) + 
                     len(tech_stack.build_tools))
        if total_tech > 10:
            complexity_score += 3
        elif total_tech > 5:
            complexity_score += 2
        elif total_tech > 2:
            complexity_score += 1
        
        # Directory depth contribution
        depth = file_structure.get("depth", 0)
        if depth > 8:
            complexity_score += 2
        elif depth > 5:
            complexity_score += 1
        
        # Map score to complexity level
        if complexity_score >= 7:
            return "enterprise"
        elif complexity_score >= 5:
            return "complex"
        elif complexity_score >= 3:
            return "moderate"
        else:
            return "simple"
    
    async def _identify_enhancement_opportunities(self, tech_stack: TechnologyStack, 
                                                patterns: List[ArchitecturePattern], 
                                                health: ProjectHealth) -> List[str]:
        """Identify opportunities for project enhancement."""
        opportunities = []
        
        # Health-based opportunities
        if health.overall_score < 70:
            opportunities.append("Implement comprehensive testing strategy")
        
        if health.security_score < 0.8:
            opportunities.append("Add security scanning and best practices")
        
        if health.documentation_score < 0.7:
            opportunities.append("Improve project documentation and API docs")
        
        # Technology-based opportunities
        if "typescript" not in tech_stack.frameworks and tech_stack.primary_language == "javascript":
            opportunities.append("Consider migrating to TypeScript for better type safety")
        
        if not any("docker" in tool.lower() for tool in tech_stack.development_tools):
            opportunities.append("Add Docker containerization for consistent environments")
        
        # Architecture-based opportunities
        monolithic_patterns = [p for p in patterns if p.pattern_name == "monolithic"]
        if monolithic_patterns and len(tech_stack.frameworks) > 3:
            opportunities.append("Consider microservices architecture for better scalability")
        
        return opportunities
    
    async def _generate_migration_recommendations(self, tech_stack: TechnologyStack, 
                                                patterns: List[ArchitecturePattern]) -> List[str]:
        """Generate technology migration recommendations."""
        recommendations = []
        
        # Language migration recommendations
        if tech_stack.primary_language == "python" and "2." in str(tech_stack):
            recommendations.append("Migrate from Python 2 to Python 3")
        
        # Framework migration recommendations
        if "express" in tech_stack.frameworks:
            recommendations.append("Consider Fastify or NestJS for better performance and structure")
        
        if "vue" in tech_stack.frameworks:
            # Check for Vue 2 vs Vue 3
            recommendations.append("Ensure migration to Vue 3 for better performance")
        
        # Database migration recommendations
        if "sqlite" in tech_stack.databases and len(patterns) > 0:
            recommendations.append("Consider PostgreSQL for production scalability")
        
        return recommendations
    
    def to_dict(self, analysis: ProjectAnalysis) -> Dict[str, Any]:
        """Convert analysis results to dictionary format."""
        return asdict(analysis)
    
    def to_json(self, analysis: ProjectAnalysis, indent: int = 2) -> str:
        """Convert analysis results to JSON format."""
        return json.dumps(self.to_dict(analysis), indent=indent, default=str)


# Example usage
if __name__ == "__main__":
    async def main():
        analyzer = UniversalProjectAnalyzer()
        
        # Analyze a project
        project_path = "/path/to/your/project"
        analysis = await analyzer.analyze_project(project_path)
        
        print(f"Project: {analysis.project_name}")
        print(f"Type: {analysis.project_type}")
        print(f"Primary Language: {analysis.technology_stack.primary_language}")
        print(f"Frameworks: {analysis.technology_stack.frameworks}")
        print(f"Health Score: {analysis.health_assessment.overall_score:.1f}/100")
        print(f"Complexity: {analysis.estimated_complexity}")
        
        print("\nEnhancement Opportunities:")
        for opportunity in analysis.enhancement_opportunities:
            print(f"- {opportunity}")
    
    asyncio.run(main())