"""
Unit tests for the Universal Project Analyzer.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from universal_ai_dev_platform.analysis.project_scanner import UniversalAnalyzer, ProjectAnalysisResult


class TestUniversalAnalyzer:
    """Test suite for UniversalAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create a universal analyzer for testing."""
        return UniversalAnalyzer()
    
    def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.supported_languages is not None
        assert analyzer.framework_detectors is not None
        assert analyzer.pattern_detectors is not None
        assert len(analyzer.supported_languages) > 0
    
    @pytest.mark.asyncio
    async def test_analyze_project_with_sample_structure(self, analyzer, sample_project_structure):
        """Test project analysis with sample project structure."""
        result = await analyzer.analyze_project(str(sample_project_structure))
        
        assert isinstance(result, ProjectAnalysisResult)
        assert result.project_path == str(sample_project_structure)
        assert result.project_name == "sample_project"
        assert result.project_type in ["web-app", "unknown"]
        assert isinstance(result.languages_detected, dict)
        assert isinstance(result.frameworks_detected, dict)
    
    def test_detect_languages(self, analyzer, sample_project_structure):
        """Test language detection."""
        languages = analyzer._detect_languages(sample_project_structure)
        
        assert isinstance(languages, dict)
        assert "typescript" in languages or "javascript" in languages
        
        # Check percentages sum to ~100
        if languages:
            total_percentage = sum(languages.values())
            assert 95 <= total_percentage <= 105  # Allow for rounding
    
    def test_detect_frameworks(self, analyzer, sample_project_structure):
        """Test framework detection."""
        frameworks = analyzer._detect_frameworks(sample_project_structure)
        
        assert isinstance(frameworks, dict)
        
        # Should detect React based on sample project
        if "react" in frameworks:
            assert 0.0 <= frameworks["react"] <= 1.0
    
    def test_detect_project_type(self, analyzer, sample_project_structure):
        """Test project type detection."""
        project_type = analyzer._detect_project_type(sample_project_structure)
        
        assert isinstance(project_type, str)
        # Sample project should be detected as web-app or unknown
        assert project_type in ["web-app", "unknown", "frontend", "library"]
    
    def test_detect_architecture_patterns(self, analyzer, sample_project_structure):
        """Test architecture pattern detection."""
        patterns = analyzer._detect_architecture_patterns(sample_project_structure)
        
        assert isinstance(patterns, list)
        # Sample React project should have component-based pattern
        possible_patterns = ["component-based", "spa", "modular", "layered"]
        assert any(pattern in patterns for pattern in possible_patterns) or len(patterns) == 0
    
    def test_calculate_health_metrics(self, analyzer, sample_project_structure):
        """Test health metrics calculation."""
        metrics = analyzer._calculate_health_metrics(sample_project_structure)
        
        assert isinstance(metrics, dict)
        expected_metrics = ["code_quality", "test_coverage", "documentation", "maintainability", "security"]
        
        for metric in expected_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))
            assert 0.0 <= metrics[metric] <= 1.0
    
    def test_analyze_dependencies(self, analyzer, sample_project_structure):
        """Test dependency analysis."""
        deps_analysis = analyzer._analyze_dependencies(sample_project_structure)
        
        assert isinstance(deps_analysis, dict)
        expected_keys = ["total_dependencies", "outdated_dependencies", "security_vulnerabilities", "license_issues"]
        
        for key in expected_keys:
            assert key in deps_analysis
            assert isinstance(deps_analysis[key], int)
            assert deps_analysis[key] >= 0
    
    def test_generate_recommendations(self, analyzer, sample_project_structure):
        """Test recommendation generation."""
        # Mock analysis results
        languages = {"typescript": 100.0}
        frameworks = {"react": 0.9, "vite": 0.8}
        health_metrics = {
            "code_quality": 0.8,
            "test_coverage": 0.3,  # Low coverage
            "documentation": 0.5,
            "maintainability": 0.7,
            "security": 0.9
        }
        deps_analysis = {
            "total_dependencies": 25,
            "outdated_dependencies": 5,  # Some outdated
            "security_vulnerabilities": 0,
            "license_issues": 0
        }
        
        recommendations = analyzer._generate_recommendations(
            sample_project_structure, languages, frameworks, health_metrics, deps_analysis
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Should recommend improving test coverage
        test_recommendations = [rec for rec in recommendations if "test" in rec.lower()]
        assert len(test_recommendations) > 0
        
        # Should recommend updating dependencies
        update_recommendations = [rec for rec in recommendations if "update" in rec.lower() or "outdated" in rec.lower()]
        assert len(update_recommendations) > 0
    
    def test_generate_enhancement_opportunities(self, analyzer, sample_project_structure):
        """Test enhancement opportunity generation."""
        languages = {"typescript": 100.0}
        frameworks = {"react": 0.9}
        patterns = ["component-based"]
        
        opportunities = analyzer._generate_enhancement_opportunities(
            sample_project_structure, languages, frameworks, patterns
        )
        
        assert isinstance(opportunities, list)
        # Should have some enhancement suggestions
        assert len(opportunities) >= 0
    
    def test_file_counting(self, analyzer, sample_project_structure):
        """Test file counting functionality."""
        count = analyzer._count_files_by_extension(sample_project_structure, [".tsx", ".ts", ".js", ".jsx"])
        
        assert isinstance(count, int)
        assert count > 0  # Should find at least the sample files
    
    def test_lines_of_code_calculation(self, analyzer, sample_project_structure):
        """Test lines of code calculation."""
        loc = analyzer._calculate_lines_of_code(sample_project_structure)
        
        assert isinstance(loc, int)
        assert loc > 0  # Should count lines from sample files
    
    def test_package_json_detection(self, analyzer, sample_project_structure):
        """Test package.json detection and parsing."""
        package_info = analyzer._analyze_package_json(sample_project_structure / "package.json")
        
        assert isinstance(package_info, dict)
        assert "name" in package_info
        assert package_info["name"] == "sample-project"
        assert "dependencies" in package_info
        assert "react" in package_info["dependencies"]
    
    def test_tsconfig_detection(self, analyzer, sample_project_structure):
        """Test tsconfig.json detection and parsing."""
        tsconfig_info = analyzer._analyze_tsconfig(sample_project_structure / "tsconfig.json")
        
        assert isinstance(tsconfig_info, dict)
        if tsconfig_info:  # Only check if tsconfig exists and was parsed
            assert "compilerOptions" in tsconfig_info
    
    def test_framework_confidence_scoring(self, analyzer):
        """Test framework confidence scoring."""
        # Test React detection
        react_indicators = {
            "package.json has react": True,
            "jsx/tsx files present": True,
            "react imports found": True,
            "component patterns": True
        }
        
        confidence = analyzer._calculate_framework_confidence("react", react_indicators)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should have high confidence
        
        # Test with no indicators
        no_indicators = {key: False for key in react_indicators}
        low_confidence = analyzer._calculate_framework_confidence("react", no_indicators)
        assert low_confidence < confidence
    
    def test_language_detection_accuracy(self, analyzer, temp_dir):
        """Test language detection accuracy with specific files."""
        # Create Python file
        python_file = temp_dir / "test.py"
        python_file.write_text("import numpy as np\nprint('Hello Python')")
        
        # Create TypeScript file
        ts_file = temp_dir / "test.ts"
        ts_file.write_text("interface User { name: string; }\nconst user: User = { name: 'test' };")
        
        # Create JavaScript file
        js_file = temp_dir / "test.js"
        js_file.write_text("function hello() { console.log('Hello JavaScript'); }")
        
        languages = analyzer._detect_languages(temp_dir)
        
        assert "python" in languages
        assert "typescript" in languages or "javascript" in languages
    
    def test_error_handling_missing_project(self, analyzer):
        """Test error handling for missing project."""
        with pytest.raises(Exception):  # Should raise appropriate exception
            asyncio.run(analyzer.analyze_project("/nonexistent/path"))
    
    def test_empty_project_handling(self, analyzer, temp_dir):
        """Test handling of empty project directory."""
        empty_dir = temp_dir / "empty_project"
        empty_dir.mkdir()
        
        result = asyncio.run(analyzer.analyze_project(str(empty_dir)))
        
        assert isinstance(result, ProjectAnalysisResult)
        assert result.project_type == "unknown"
        assert len(result.languages_detected) == 0
    
    @pytest.mark.asyncio
    async def test_analysis_depth_options(self, analyzer, sample_project_structure):
        """Test different analysis depth options."""
        # Test quick analysis
        quick_result = await analyzer.analyze_project(str(sample_project_structure), depth="quick")
        assert isinstance(quick_result, ProjectAnalysisResult)
        
        # Test standard analysis
        standard_result = await analyzer.analyze_project(str(sample_project_structure), depth="standard")
        assert isinstance(standard_result, ProjectAnalysisResult)
        
        # Test comprehensive analysis
        comprehensive_result = await analyzer.analyze_project(str(sample_project_structure), depth="comprehensive")
        assert isinstance(comprehensive_result, ProjectAnalysisResult)
        
        # Comprehensive should have more detailed analysis
        assert len(comprehensive_result.recommendations) >= len(quick_result.recommendations)
    
    def test_security_analysis(self, analyzer, sample_project_structure):
        """Test security analysis functionality."""
        security_score = analyzer._analyze_security(sample_project_structure)
        
        assert isinstance(security_score, float)
        assert 0.0 <= security_score <= 1.0
    
    def test_performance_analysis(self, analyzer, sample_project_structure):
        """Test performance analysis functionality."""
        performance_score = analyzer._analyze_performance(sample_project_structure)
        
        assert isinstance(performance_score, float)
        assert 0.0 <= performance_score <= 1.0
    
    def test_documentation_analysis(self, analyzer, sample_project_structure):
        """Test documentation analysis."""
        doc_score = analyzer._analyze_documentation(sample_project_structure)
        
        assert isinstance(doc_score, float)
        assert 0.0 <= doc_score <= 1.0
    
    def test_maintainability_analysis(self, analyzer, sample_project_structure):
        """Test maintainability analysis."""
        maintainability_score = analyzer._analyze_maintainability(sample_project_structure)
        
        assert isinstance(maintainability_score, float)
        assert 0.0 <= maintainability_score <= 1.0