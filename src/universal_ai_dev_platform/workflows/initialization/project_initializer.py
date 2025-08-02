"""
Project Initializer

Creates new projects from specifications using intelligent templates, best practices,
and AI-powered configuration based on requirements and technology choices.
"""

import asyncio
import json
import logging
import os
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import subprocess
import tempfile

logger = logging.getLogger(__name__)


@dataclass
class ProjectSpecification:
    """Complete specification for project creation."""
    
    name: str
    type: str  # web-app, mobile-app, api-service, etc.
    technology_stack: List[str]
    features: List[str]
    deployment_target: Optional[str]
    scale: str  # startup, enterprise, global
    compliance_requirements: List[str]
    template: Optional[str]
    ai_enhanced: bool
    output_directory: str
    
    # Additional configuration
    metadata: Dict[str, Any] = None
    custom_config: Dict[str, Any] = None


@dataclass
class ProjectCreationResult:
    """Results of project creation process."""
    
    success: bool
    project_path: str
    project_name: str
    project_type: str
    
    # Creation details
    template_used: str
    technologies_configured: List[str]
    features_implemented: List[str]
    files_created: List[str]
    
    # Validation results
    validation_passed: bool
    validation_errors: List[str]
    
    # Next steps
    setup_instructions: List[str]
    recommended_next_steps: List[str]
    
    # Metadata
    creation_timestamp: datetime
    creation_duration: float
    metadata: Dict[str, Any]


class ProjectInitializer:
    """
    Creates new projects with intelligent configuration, best practices,
    and production-ready setup based on specifications.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.template_manager = ProjectTemplateManager()
        self.dependency_manager = DependencyManager()
        self.configuration_generator = ConfigurationGenerator()
        self.validation_engine = ProjectValidationEngine()
        
    def _default_config(self) -> Dict:
        """Default configuration for project initialization."""
        return {
            "templates_directory": "templates/project_types",
            "supported_project_types": [
                "web-app", "mobile-app", "api-service", "desktop-app",
                "cli-tool", "library", "documentation", "ai-project",
                "blockchain", "game", "iot", "data-science"
            ],
            "default_features": {
                "web-app": ["routing", "state-management", "styling"],
                "api-service": ["authentication", "validation", "logging"],
                "mobile-app": ["navigation", "state-management", "offline-support"],
                "ai-project": ["data-processing", "model-training", "api-endpoints"]
            },
            "technology_stacks": {
                "web-app": {
                    "react": ["react", "typescript", "tailwind", "vite"],
                    "vue": ["vue", "typescript", "pinia", "vite"],
                    "angular": ["angular", "typescript", "angular-material"],
                    "svelte": ["svelte", "typescript", "tailwind", "vite"]
                },
                "api-service": {
                    "fastapi": ["python", "fastapi", "sqlalchemy", "alembic"],
                    "express": ["nodejs", "express", "typescript", "prisma"],
                    "django": ["python", "django", "postgresql", "redis"],
                    "go": ["go", "gin", "gorm", "postgresql"]
                }
            },
            "quality_standards": {
                "linting": True,
                "formatting": True,
                "testing": True,
                "ci_cd": True,
                "documentation": True
            }
        }
    
    async def create_project(self, spec: Dict[str, Any]) -> ProjectCreationResult:
        """
        Create a new project based on the specification.
        
        Args:
            spec: Project specification dictionary
            
        Returns:
            Complete project creation results
        """
        start_time = datetime.now()
        logger.info(f"Creating project: {spec.get('name', 'unnamed')}")
        
        try:
            # Convert dict to ProjectSpecification
            project_spec = ProjectSpecification(**spec)
            
            # Validate specification
            await self._validate_specification(project_spec)
            
            # Prepare project directory
            project_path = await self._prepare_project_directory(project_spec)
            
            # Select and prepare template
            template = await self.template_manager.select_template(project_spec)
            
            # Generate project structure
            files_created = await self._generate_project_structure(
                project_path, template, project_spec
            )
            
            # Configure dependencies
            technologies_configured = await self.dependency_manager.configure_dependencies(
                project_path, project_spec
            )
            
            # Generate configuration files
            await self.configuration_generator.generate_configurations(
                project_path, project_spec
            )
            
            # Implement requested features
            features_implemented = await self._implement_features(
                project_path, project_spec
            )
            
            # Add AI enhancements if requested
            if project_spec.ai_enhanced:
                await self._add_ai_enhancements(project_path, project_spec)
            
            # Validate created project
            validation_result = await self.validation_engine.validate_project(
                project_path, project_spec
            )
            
            # Generate setup instructions
            setup_instructions = await self._generate_setup_instructions(
                project_path, project_spec
            )
            
            # Calculate creation duration
            creation_duration = (datetime.now() - start_time).total_seconds()
            
            result = ProjectCreationResult(
                success=True,
                project_path=str(project_path),
                project_name=project_spec.name,
                project_type=project_spec.type,
                template_used=template.name,
                technologies_configured=technologies_configured,
                features_implemented=features_implemented,
                files_created=files_created,
                validation_passed=validation_result["passed"],
                validation_errors=validation_result["errors"],
                setup_instructions=setup_instructions,
                recommended_next_steps=await self._generate_next_steps(project_spec),
                creation_timestamp=start_time,
                creation_duration=creation_duration,
                metadata={
                    "template_version": template.version,
                    "initializer_version": "1.0.0",
                    "spec": asdict(project_spec)
                }
            )
            
            logger.info(f"Project created successfully in {creation_duration:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Project creation failed: {e}")
            
            # Return failure result
            creation_duration = (datetime.now() - start_time).total_seconds()
            return ProjectCreationResult(
                success=False,
                project_path="",
                project_name=spec.get("name", "unknown"),
                project_type=spec.get("type", "unknown"),
                template_used="",
                technologies_configured=[],
                features_implemented=[],
                files_created=[],
                validation_passed=False,
                validation_errors=[str(e)],
                setup_instructions=[],
                recommended_next_steps=[],
                creation_timestamp=start_time,
                creation_duration=creation_duration,
                metadata={"error": str(e)}
            )
    
    async def _validate_specification(self, spec: ProjectSpecification):
        """Validate project specification before creation."""
        errors = []
        
        # Validate project type
        if spec.type not in self.config["supported_project_types"]:
            errors.append(f"Unsupported project type: {spec.type}")
        
        # Validate project name
        if not spec.name or not spec.name.replace("-", "").replace("_", "").isalnum():
            errors.append("Project name must be alphanumeric (with hyphens/underscores)")
        
        # Validate output directory
        output_path = Path(spec.output_directory)
        if output_path.exists() and any(output_path.iterdir()):
            errors.append(f"Output directory already exists and is not empty: {spec.output_directory}")
        
        # Validate technology stack
        if spec.technology_stack:
            available_stacks = self.config["technology_stacks"].get(spec.type, {})
            if available_stacks and not any(
                tech in available_stacks for tech in spec.technology_stack
            ):
                errors.append(f"Technology stack not supported for {spec.type}")
        
        if errors:
            raise ValueError(f"Specification validation failed: {'; '.join(errors)}")
    
    async def _prepare_project_directory(self, spec: ProjectSpecification) -> Path:
        """Prepare the project directory structure."""
        project_path = Path(spec.output_directory).resolve()
        
        # Create directory if it doesn't exist
        project_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Prepared project directory: {project_path}")
        return project_path
    
    async def _generate_project_structure(self, project_path: Path, 
                                        template: 'ProjectTemplate', 
                                        spec: ProjectSpecification) -> List[str]:
        """Generate the basic project structure from template."""
        files_created = []
        
        try:
            # Copy template files to project directory
            template_files = await template.get_files()
            
            for template_file in template_files:
                target_path = project_path / template_file.relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Process template content with variables
                content = await self._process_template_content(
                    template_file.content, spec
                )
                
                target_path.write_text(content, encoding='utf-8')
                files_created.append(str(template_file.relative_path))
            
            logger.info(f"Created {len(files_created)} files from template")
            return files_created
            
        except Exception as e:
            logger.error(f"Error generating project structure: {e}")
            raise
    
    async def _process_template_content(self, content: str, 
                                      spec: ProjectSpecification) -> str:
        """Process template content with variable substitution."""
        # Simple template variable replacement
        variables = {
            "{{PROJECT_NAME}}": spec.name,
            "{{PROJECT_TYPE}}": spec.type,
            "{{AUTHOR_NAME}}": os.getenv("USER", "Developer"),
            "{{YEAR}}": str(datetime.now().year),
            "{{DESCRIPTION}}": f"A {spec.type} project built with Universal AI Dev Platform",
            "{{TECH_STACK}}": ", ".join(spec.technology_stack) if spec.technology_stack else "",
            "{{FEATURES}}": ", ".join(spec.features) if spec.features else ""
        }
        
        processed_content = content
        for variable, value in variables.items():
            processed_content = processed_content.replace(variable, value)
        
        return processed_content
    
    async def _implement_features(self, project_path: Path, 
                                spec: ProjectSpecification) -> List[str]:
        """Implement requested features in the project."""
        implemented_features = []
        
        feature_implementations = {
            "authentication": self._implement_authentication,
            "database": self._implement_database,
            "api": self._implement_api,
            "testing": self._implement_testing,
            "ci-cd": self._implement_ci_cd,
            "monitoring": self._implement_monitoring,
            "documentation": self._implement_documentation
        }
        
        for feature in spec.features:
            if feature in feature_implementations:
                try:
                    await feature_implementations[feature](project_path, spec)
                    implemented_features.append(feature)
                    logger.info(f"Implemented feature: {feature}")
                except Exception as e:
                    logger.error(f"Failed to implement feature {feature}: {e}")
        
        return implemented_features
    
    async def _implement_authentication(self, project_path: Path, spec: ProjectSpecification):
        """Implement authentication feature."""
        # TODO: Implement authentication setup based on project type
        pass
    
    async def _implement_database(self, project_path: Path, spec: ProjectSpecification):
        """Implement database configuration."""
        # TODO: Implement database setup based on technology stack
        pass
    
    async def _implement_api(self, project_path: Path, spec: ProjectSpecification):
        """Implement API configuration."""
        # TODO: Implement API setup based on project type
        pass
    
    async def _implement_testing(self, project_path: Path, spec: ProjectSpecification):
        """Implement testing framework."""
        # Create basic test structure
        test_dir = project_path / "tests"
        test_dir.mkdir(exist_ok=True)
        
        # Create test configuration based on technology stack
        if "python" in spec.technology_stack:
            # Python testing setup
            (test_dir / "__init__.py").touch()
            
            pytest_config = """[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
"""
            
            # Add to pyproject.toml if it exists
            pyproject_path = project_path / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, 'a') as f:
                    f.write(f"\n{pytest_config}")
        
        elif any(tech in spec.technology_stack for tech in ["javascript", "typescript", "node"]):
            # JavaScript/TypeScript testing setup
            jest_config = {
                "preset": "ts-jest" if "typescript" in spec.technology_stack else None,
                "testEnvironment": "node",
                "testMatch": ["**/__tests__/**/*.(test|spec).(js|ts)", "**/?(*.)(test|spec).(js|ts)"],
                "collectCoverageFrom": [
                    "src/**/*.(js|ts)",
                    "!src/**/*.d.ts"
                ]
            }
            
            with open(project_path / "jest.config.json", 'w') as f:
                json.dump(jest_config, f, indent=2)
    
    async def _implement_ci_cd(self, project_path: Path, spec: ProjectSpecification):
        """Implement CI/CD pipeline."""
        github_dir = project_path / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        # Create GitHub Actions workflow
        workflow_content = self._generate_github_workflow(spec)
        
        with open(github_dir / "ci.yml", 'w') as f:
            f.write(workflow_content)
    
    def _generate_github_workflow(self, spec: ProjectSpecification) -> str:
        """Generate GitHub Actions workflow content."""
        if "python" in spec.technology_stack:
            return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Lint with ruff
      run: ruff check .
    
    - name: Type check with mypy
      run: mypy .
    
    - name: Test with pytest
      run: pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
"""
        
        elif any(tech in spec.technology_stack for tech in ["javascript", "typescript", "node"]):
            return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]

    steps:
    - uses: actions/checkout@v3
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Type check
      run: npm run type-check
    
    - name: Test
      run: npm run test:coverage
    
    - name: Build
      run: npm run build
"""
        
        return """name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: echo "Add your test commands here"
"""
    
    async def _implement_monitoring(self, project_path: Path, spec: ProjectSpecification):
        """Implement monitoring and observability."""
        # TODO: Implement monitoring setup based on deployment target
        pass
    
    async def _implement_documentation(self, project_path: Path, spec: ProjectSpecification):
        """Implement documentation structure."""
        docs_dir = project_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Create basic documentation files
        readme_content = self._generate_readme(spec)
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Create additional documentation
        (docs_dir / "CONTRIBUTING.md").touch()
        (docs_dir / "API.md").touch()
        (docs_dir / "DEPLOYMENT.md").touch()
    
    def _generate_readme(self, spec: ProjectSpecification) -> str:
        """Generate README.md content."""
        return f"""# {spec.name}

{spec.name.replace('-', ' ').replace('_', ' ').title()} - A {spec.type} project

## Description

This project was generated using the Universal AI Development Platform.

## Technology Stack

{', '.join(spec.technology_stack) if spec.technology_stack else 'To be determined'}

## Features

{chr(10).join(f'- {feature}' for feature in spec.features) if spec.features else '- Basic project structure'}

## Getting Started

### Prerequisites

- [List prerequisites here]

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd {spec.name}
```

2. Install dependencies
```bash
# Add installation commands here
```

3. Set up environment
```bash
# Add environment setup commands here
```

### Usage

```bash
# Add usage examples here
```

## Development

### Running Tests

```bash
# Add test commands here
```

### Building

```bash
# Add build commands here
```

## Deployment

[Add deployment instructions here]

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Generated with ❤️ by [Universal AI Development Platform](https://github.com/yourusername/universal-ai-dev-platform)
"""
    
    async def _add_ai_enhancements(self, project_path: Path, spec: ProjectSpecification):
        """Add AI development enhancements to the project."""
        # TODO: Implement AI-specific enhancements
        # - Add AI agent integration templates
        # - Add MCP server configurations
        # - Add intelligent monitoring setup
        # - Add pattern recognition capabilities
        pass
    
    async def _generate_setup_instructions(self, project_path: Path, 
                                         spec: ProjectSpecification) -> List[str]:
        """Generate setup instructions for the created project."""
        instructions = [
            f"cd {spec.name}",
            "Review the README.md file for project overview"
        ]
        
        # Add technology-specific setup instructions
        if "python" in spec.technology_stack:
            instructions.extend([
                "Create a virtual environment: python -m venv venv",
                "Activate the virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)",
                "Install dependencies: pip install -e \".[dev]\""
            ])
        
        elif any(tech in spec.technology_stack for tech in ["javascript", "typescript", "node"]):
            instructions.extend([
                "Install dependencies: npm install",
                "Start development server: npm run dev"
            ])
        
        # Add feature-specific instructions
        if "database" in spec.features:
            instructions.append("Set up database configuration in environment variables")
        
        if "testing" in spec.features:
            instructions.append("Run tests to verify setup: npm test or pytest")
        
        return instructions
    
    async def _generate_next_steps(self, spec: ProjectSpecification) -> List[str]:
        """Generate recommended next steps for the project."""
        next_steps = [
            "Review and customize the generated code",
            "Set up version control (git init, first commit)",
            "Configure environment variables",
            "Set up continuous integration"
        ]
        
        # Add project-type specific next steps
        if spec.type == "web-app":
            next_steps.extend([
                "Design your component architecture",
                "Set up routing and navigation",
                "Implement your first feature"
            ])
        
        elif spec.type == "api-service":
            next_steps.extend([
                "Design your API endpoints",
                "Set up database schema",
                "Implement authentication"
            ])
        
        # Add deployment suggestions
        if spec.deployment_target:
            next_steps.append(f"Set up deployment to {spec.deployment_target}")
        
        return next_steps


class ProjectTemplateManager:
    """Manages project templates and template selection."""
    
    async def select_template(self, spec: ProjectSpecification) -> 'ProjectTemplate':
        """Select the best template for the project specification."""
        # TODO: Implement intelligent template selection
        # For now, return a basic template
        return ProjectTemplate(
            name=f"{spec.type}_basic",
            version="1.0.0",
            description=f"Basic {spec.type} template",
            files=[]
        )


class DependencyManager:
    """Manages project dependencies and package configurations."""
    
    async def configure_dependencies(self, project_path: Path, 
                                   spec: ProjectSpecification) -> List[str]:
        """Configure dependencies for the project."""
        configured = []
        
        # TODO: Implement dependency configuration based on technology stack
        # This would involve creating package.json, requirements.txt, etc.
        
        return configured


class ConfigurationGenerator:
    """Generates configuration files for projects."""
    
    async def generate_configurations(self, project_path: Path, 
                                    spec: ProjectSpecification):
        """Generate all necessary configuration files."""
        # TODO: Implement configuration file generation
        # - ESLint, Prettier configs for JS/TS
        # - pyproject.toml for Python
        # - Docker configurations
        # - Environment configuration templates
        pass


class ProjectValidationEngine:
    """Validates created projects for completeness and correctness."""
    
    async def validate_project(self, project_path: Path, 
                             spec: ProjectSpecification) -> Dict[str, Any]:
        """Validate the created project."""
        errors = []
        
        # Basic validation
        if not (project_path / "README.md").exists():
            errors.append("README.md is missing")
        
        # TODO: Implement comprehensive project validation
        # - Check all required files are present
        # - Validate configuration files
        # - Test that build processes work
        # - Verify dependencies are correctly specified
        
        return {
            "passed": len(errors) == 0,
            "errors": errors
        }


@dataclass
class ProjectTemplate:
    """Represents a project template."""
    
    name: str
    version: str
    description: str
    files: List['TemplateFile']
    
    async def get_files(self) -> List['TemplateFile']:
        """Get all template files."""
        return self.files


@dataclass
class TemplateFile:
    """Represents a template file."""
    
    relative_path: str
    content: str
    is_binary: bool = False


# Example usage
if __name__ == "__main__":
    async def main():
        initializer = ProjectInitializer()
        
        # Create a web application project
        spec = {
            "name": "my-web-app",
            "type": "web-app",
            "technology_stack": ["react", "typescript", "tailwind"],
            "features": ["authentication", "testing", "ci-cd"],
            "deployment_target": "vercel",
            "scale": "startup",
            "compliance_requirements": [],
            "template": None,
            "ai_enhanced": True,
            "output_directory": "./my-web-app"
        }
        
        result = await initializer.create_project(spec)
        
        if result.success:
            print(f"✅ Project created successfully!")
            print(f"Location: {result.project_path}")
            print(f"Template: {result.template_used}")
            print(f"Technologies: {', '.join(result.technologies_configured)}")
            print("\n📋 Setup Instructions:")
            for instruction in result.setup_instructions:
                print(f"  {instruction}")
        else:
            print(f"❌ Project creation failed:")
            for error in result.validation_errors:
                print(f"  - {error}")
    
    asyncio.run(main())