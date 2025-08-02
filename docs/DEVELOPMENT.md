# Development Guide

**Universal AI Development Platform - Development Setup and Contributing Guide**

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (recommended: 3.11 or 3.12)
- **Git** for version control
- **uv** (recommended) or **pip** for dependency management
- **Docker** (optional, for containerized development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/universal-ai-dev-platform.git
cd universal-ai-dev-platform
```

2. **Set up development environment**
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

3. **Verify installation**
```bash
uai --help
```

You should see the Universal AI Development Platform CLI help output.

## 🏗️ Architecture Overview

The Universal AI Development Platform is designed with adaptive architecture principles:

```
universal-ai-dev-platform/
├── src/universal_ai_dev_platform/          # Main package
│   ├── core/                               # Core intelligence systems
│   │   ├── adaptation/                     # Industry change adaptation
│   │   │   ├── feature_discovery.py       # Automated feature discovery
│   │   │   ├── compatibility_analyzer.py  # Compatibility assessment
│   │   │   └── adaptation_engine.py       # Main adaptation coordinator
│   │   ├── intelligence/                   # AI intelligence systems
│   │   │   ├── pattern_analyzer.py        # Code pattern recognition
│   │   │   └── project_intelligence.py    # Predictive intelligence
│   │   └── orchestration/                  # Agent coordination
│   │       └── agent_orchestrator.py      # Multi-agent workflows
│   ├── analysis/                           # Project analysis
│   │   └── project_scanner/
│   │       └── universal_analyzer.py      # Universal project analyzer
│   ├── workflows/                          # Development workflows
│   │   └── initialization/
│   │       └── project_initializer.py     # Project creation
│   └── cli.py                             # Command-line interface
├── templates/                             # Project templates
├── tests/                                 # Test suite
├── docs/                                  # Documentation
└── config/                               # Configuration files
```

## 🔧 Core Components

### 1. **Adaptive Architecture** (`core/adaptation/`)

The platform automatically adapts to AI industry changes:

- **Feature Discovery Engine**: Monitors 50+ AI sources for new capabilities
- **Compatibility Analyzer**: Assesses integration potential of new features
- **Adaptation Engine**: Coordinates safe integration of beneficial updates

### 2. **Universal Intelligence** (`core/intelligence/`)

AI-powered project analysis and optimization:

- **Pattern Analyzer**: Detects architectural and design patterns in any codebase
- **Project Intelligence**: Provides predictive insights and optimization recommendations

### 3. **Agent Orchestration** (`core/orchestration/`)

Coordinates 20+ specialized AI agents for complex workflows:

- **Multi-agent coordination**: Parallel execution with intelligent load balancing
- **Workflow management**: Predefined and custom workflow execution
- **Result aggregation**: Combines outputs from multiple agents

### 4. **Universal Analysis** (`analysis/`)

Comprehensive project understanding:

- **Technology stack detection**: Supports 12+ languages and frameworks
- **Health assessment**: Multi-dimensional project quality scoring
- **Enhancement recommendations**: AI-powered improvement suggestions

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m adaptation    # Adaptation tests only
```

### Test Structure

```
tests/
├── unit/               # Unit tests for individual components
├── integration/        # Integration tests for component interaction
├── adaptation/         # Tests for adaptive features
└── performance/        # Performance and load tests
```

### Writing Tests

Example test for the Pattern Analyzer:

```python
import pytest
from universal_ai_dev_platform.core.intelligence import PatternAnalyzer

@pytest.mark.asyncio
async def test_pattern_detection():
    analyzer = PatternAnalyzer()
    result = await analyzer.analyze_patterns("./sample-project")
    
    assert result.patterns_detected
    assert result.overall_pattern_score > 0
    assert len(result.recommendations) > 0
```

## 🎨 Code Style

### Formatting and Linting

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/
mypy src/
```

### Pre-commit Hooks

Set up pre-commit hooks to automatically format and lint:

```bash
pre-commit install
```

### Code Style Guidelines

- **Line length**: 88 characters (Black default)
- **Import sorting**: isort with Black compatibility
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for all public methods
- **Naming**: snake_case for functions/variables, PascalCase for classes

Example function with proper style:

```python
async def analyze_project_patterns(
    self, 
    project_path: str, 
    depth: str = "standard"
) -> PatternAnalysisResult:
    """
    Analyze patterns in a project with specified depth.
    
    Args:
        project_path: Path to the project directory
        depth: Analysis depth level
        
    Returns:
        Complete pattern analysis results
        
    Raises:
        ValueError: If project path doesn't exist
    """
    # Implementation here
    pass
```

## 🚢 Development Workflow

### 1. **Feature Development**

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes with tests
# ... implement feature ...

# Run tests and linting
pytest
black src/ tests/
ruff check src/

# Commit with conventional commits
git commit -m "feat: add new pattern detection capability"

# Push and create PR
git push origin feature/my-new-feature
```

### 2. **Adding New Agents**

To add a new specialized agent:

1. **Define agent capabilities** in `core/orchestration/agent_orchestrator.py`
2. **Add agent to available agents** list in config
3. **Implement agent selection logic** for appropriate workflows
4. **Add tests** for agent coordination
5. **Update documentation**

### 3. **Adding New Project Types**

To support a new project type:

1. **Add type to supported list** in `workflows/initialization/project_initializer.py`
2. **Create template** in `templates/project_types/`
3. **Add technology stack mapping** in config
4. **Implement feature implementations** for the project type
5. **Add validation rules**

### 4. **Adding New Analysis Patterns**

To add new pattern detection:

1. **Define pattern in pattern_definitions** in `core/intelligence/pattern_analyzer.py`
2. **Add detection indicators** (file patterns, content patterns, directory structure)
3. **Set confidence thresholds** and recommendations
4. **Add tests** with sample code demonstrating the pattern
5. **Update documentation**

## 🔍 Debugging

### CLI Debugging

```bash
# Enable verbose logging
uai --verbose analyze ./my-project

# Debug specific components
export UAI_LOG_LEVEL=DEBUG
uai analyze ./my-project
```

### Component Testing

```bash
# Test individual components
python -m universal_ai_dev_platform.core.adaptation.feature_discovery
python -m universal_ai_dev_platform.analysis.project_scanner.universal_analyzer
```

### Async Debugging

For debugging async components:

```python
import asyncio
import logging

# Enable asyncio debugging
logging.getLogger("asyncio").setLevel(logging.DEBUG)

# Run with debug mode
asyncio.run(main(), debug=True)
```

## 📊 Performance Considerations

### Optimization Guidelines

1. **Async/Await**: Use async for I/O operations (file reading, web requests)
2. **Parallel Processing**: Leverage agent orchestration for parallel work
3. **Caching**: Cache expensive computations (pattern analysis, API calls)
4. **Memory Management**: Use generators for large file processing
5. **Token Optimization**: Monitor and optimize AI API token usage

### Performance Testing

```bash
# Run performance tests
pytest tests/performance/ -v

# Profile specific functions
python -m cProfile -o profile.stats script.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

## 🤝 Contributing

### Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Implement changes** with comprehensive tests
3. **Update documentation** for any new features
4. **Run the full test suite** and ensure all checks pass
5. **Create a pull request** with clear description

### Code Review Guidelines

- **Test Coverage**: New code must have >90% test coverage
- **Documentation**: Public APIs must be documented
- **Performance**: No significant performance regressions
- **Compatibility**: Maintain backward compatibility
- **Security**: Follow security best practices

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new project type support for blockchain applications
fix: resolve pattern detection issue with nested directories
docs: update API documentation for intelligence module
test: add integration tests for agent orchestration
refactor: optimize pattern matching performance
```

## 🔧 Configuration

### Environment Variables

```bash
# API Keys (for external integrations)
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"

# Logging
export UAI_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export UAI_LOG_FILE="uai.log"

# Feature Discovery
export UAI_DISCOVERY_FREQUENCY="3600"  # seconds
export UAI_AUTO_INTEGRATION="false"

# Agent Configuration
export UAI_MAX_AGENTS="20"
export UAI_AGENT_TIMEOUT="300"
```

### Configuration Files

Create `config/development.yml`:

```yaml
# Development configuration
adaptation:
  feature_discovery:
    enabled: true
    frequency: 3600
    sources:
      - arxiv.org
      - github.blog
      - docs.anthropic.com

agents:
  max_concurrent: 20
  timeout: 300
  retry_attempts: 3

analysis:
  confidence_threshold: 0.6
  max_depth: 5
  cache_enabled: true
```

## 📚 Additional Resources

### Documentation

- **[API Reference](api-reference.md)**: Complete API documentation
- **[Architecture Guide](architecture.md)**: Detailed architecture overview
- **[User Guide](../README.md)**: User-facing documentation
- **[Contributing Guide](CONTRIBUTING.md)**: Detailed contributing guidelines

### External Resources

- **[Anthropic Claude Documentation](https://docs.anthropic.com/claude/docs)**
- **[OpenAI API Documentation](https://platform.openai.com/docs)**
- **[AsyncIO Best Practices](https://docs.python.org/3/library/asyncio-dev.html)**
- **[Conventional Commits](https://www.conventionalcommits.org/)**

### Community

- **[GitHub Issues](https://github.com/yourusername/universal-ai-dev-platform/issues)**: Bug reports and feature requests
- **[Discussions](https://github.com/yourusername/universal-ai-dev-platform/discussions)**: Community discussions
- **[Discord](https://discord.gg/your-server)**: Real-time community chat

## 🚨 Troubleshooting

### Common Issues

**Import errors**:
```bash
# Ensure package is installed in development mode
pip install -e ".[dev]"
```

**CLI not found**:
```bash
# Check if virtual environment is activated
which uai
# Should point to your venv

# Reinstall if necessary
pip uninstall universal-ai-dev-platform
pip install -e ".[dev]"
```

**Async errors**:
```python
# Ensure you're using asyncio.run() for top-level calls
asyncio.run(main())

# Not async context managers
async with analyzer.analyze() as result:
    # process result
```

**Pattern detection issues**:
```bash
# Enable debug logging to see detection details
export UAI_LOG_LEVEL=DEBUG
uai analyze ./project --verbose
```

### Getting Help

1. **Check existing issues** on GitHub
2. **Search documentation** for similar problems
3. **Enable debug logging** to get more information
4. **Create a minimal reproduction** of the issue
5. **Open an issue** with detailed information

---

Happy coding! 🚀 The Universal AI Development Platform is designed to evolve with you and the rapidly changing AI landscape.