"""
Pytest configuration and fixtures for Universal AI Development Platform tests.
"""

import asyncio
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, AsyncMock

# Test fixtures for the Universal AI Development Platform


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_project_structure(temp_dir: Path) -> Path:
    """Create a sample project structure for testing."""
    project_dir = temp_dir / "sample_project"
    project_dir.mkdir()
    
    # Create basic project files
    (project_dir / "package.json").write_text("""{
  "name": "sample-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}""")
    
    (project_dir / "tsconfig.json").write_text("""{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler"
  }
}""")
    
    # Create source directory structure
    src_dir = project_dir / "src"
    src_dir.mkdir()
    
    (src_dir / "App.tsx").write_text("""
import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Sample React App</h1>
    </div>
  );
}

export default App;
""")
    
    (src_dir / "main.tsx").write_text("""
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""")
    
    # Create components directory
    components_dir = src_dir / "components"
    components_dir.mkdir()
    
    (components_dir / "Button.tsx").write_text("""
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ children, onClick }: ButtonProps) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
""")
    
    return project_dir


@pytest.fixture
def mock_feature_discovery():
    """Mock feature discovery engine for testing."""
    mock = AsyncMock()
    mock.start_monitoring = AsyncMock()
    mock.stop_monitoring = AsyncMock()
    mock.get_recent_discoveries = AsyncMock(return_value=[])
    mock.get_integration_candidates = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_compatibility_analyzer():
    """Mock compatibility analyzer for testing."""
    mock = AsyncMock()
    mock.analyze_feature = AsyncMock()
    return mock


@pytest.fixture
def mock_agent_orchestrator():
    """Mock agent orchestrator for testing."""
    mock = AsyncMock()
    mock.orchestrate_workflow = AsyncMock()
    mock.get_available_agents = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_universal_analyzer():
    """Mock universal analyzer for testing."""
    mock = AsyncMock()
    mock.analyze_project = AsyncMock()
    return mock


@pytest.fixture
def sample_discovered_feature():
    """Sample discovered feature for testing."""
    from universal_ai_dev_platform.core.adaptation import DiscoveredFeature
    from datetime import datetime
    
    return DiscoveredFeature(
        title="New AI Feature",
        description="A revolutionary new AI capability",
        source="arxiv",
        url="https://arxiv.org/abs/2024.12345",
        category="machine-learning",
        tags=["ai", "ml", "innovation"],
        discovered_at=datetime.now(),
        confidence_score=0.85,
        relevance_score=0.92
    )


@pytest.fixture
def sample_compatibility_assessment():
    """Sample compatibility assessment for testing."""
    from universal_ai_dev_platform.core.adaptation import CompatibilityAssessment, CompatibilityStatus, IntegrationComplexity
    
    return CompatibilityAssessment(
        feature_id="test-feature",
        status=CompatibilityStatus.COMPATIBLE,
        confidence=0.9,
        complexity=IntegrationComplexity.LOW,
        estimated_effort_hours=4,
        requirements=[],
        conflicts=[],
        recommendations=["Ready for integration"],
        risk_factors=[],
        integration_plan={
            "steps": ["Add dependency", "Configure", "Test"],
            "timeline": "1-2 days"
        }
    )


@pytest.fixture
def sample_project_analysis():
    """Sample project analysis result for testing."""
    from universal_ai_dev_platform.analysis.project_scanner import ProjectAnalysisResult
    
    return ProjectAnalysisResult(
        project_path="/test/project",
        project_name="test-project",
        project_type="web-app",
        languages_detected={"typescript": 85.0, "javascript": 15.0},
        frameworks_detected={"react": 0.95, "vite": 0.9},
        architecture_patterns=["component-based", "spa"],
        health_metrics={
            "code_quality": 0.85,
            "test_coverage": 0.70,
            "documentation": 0.60,
            "maintainability": 0.80,
            "security": 0.75
        },
        dependencies_analysis={
            "total_dependencies": 25,
            "outdated_dependencies": 3,
            "security_vulnerabilities": 0,
            "license_issues": 0
        },
        recommendations=[
            "Add more unit tests",
            "Update outdated dependencies",
            "Improve documentation coverage"
        ],
        enhancement_opportunities=[
            "Consider adding TypeScript strict mode",
            "Implement automated testing pipeline",
            "Add performance monitoring"
        ],
        metadata={
            "analysis_duration": 2.5,
            "files_analyzed": 15,
            "loc": 1250
        }
    )


@pytest.fixture
def test_config():
    """Test configuration for the platform."""
    return {
        "adaptation": {
            "feature_discovery": {
                "enabled": True,
                "frequency": 3600,
                "max_concurrent_requests": 10
            },
            "compatibility_analysis": {
                "enabled": True,
                "confidence_threshold": 0.7
            }
        },
        "orchestration": {
            "max_agents": 20,
            "timeout": 300,
            "retry_attempts": 3
        },
        "analysis": {
            "confidence_threshold": 0.6,
            "max_depth": 5,
            "cache_enabled": True
        },
        "monitoring": {
            "enabled": True,
            "log_level": "DEBUG",
            "metrics_interval": 60
        }
    }


@pytest.fixture
def mock_health_monitor():
    """Mock health monitor for testing."""
    mock = Mock()
    mock.start_monitoring = AsyncMock()
    mock.stop_monitoring = AsyncMock()
    mock.get_health_status = AsyncMock(return_value={
        "overall_health": "healthy",
        "health_score": 0.95,
        "monitoring_enabled": True,
        "recent_alerts": [],
        "key_metrics": {}
    })
    mock.record_metric = Mock()
    mock.create_alert = Mock()
    return mock


# Test data constants
TEST_PROJECT_TYPES = [
    "web-app",
    "api-service", 
    "mobile-app",
    "ai-project"
]

TEST_TECH_STACKS = {
    "web-app": ["react-typescript", "vue-typescript", "nextjs-full-stack"],
    "api-service": ["fastapi-postgresql", "express-typescript", "go-gin"],
    "mobile-app": ["react-native-expo", "flutter", "ios-native"],
    "ai-project": ["pytorch-fastapi", "tensorflow-flask", "scikit-streamlit"]
}

TEST_FEATURES = {
    "web-app": ["auth", "routing", "state-management", "testing"],
    "api-service": ["auth", "validation", "documentation", "monitoring"],
    "mobile-app": ["navigation", "auth", "push-notifications", "offline-support"],
    "ai-project": ["data-processing", "model-training", "api-endpoints", "mlops"]
}


# Async test utilities
@pytest.fixture
def async_test_client():
    """Async test client for API testing."""
    # This would be configured for actual API testing
    # For now, return a mock
    return AsyncMock()


# Test database fixtures (if needed)
@pytest.fixture
def test_database():
    """Test database for integration tests."""
    # This would set up a test database
    # For now, return a mock
    return Mock()


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Automatic cleanup after each test."""
    yield
    # Perform any necessary cleanup
    # Reset global state, clear caches, etc.
    pass