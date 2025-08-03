#!/usr/bin/env python3
"""
Universal AI Development Platform - Setup and Configuration Script

This script handles the complete setup and configuration of the Universal AI Development Platform,
including environment setup, dependency installation, and initial configuration.
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlatformSetup:
    """Main setup and configuration class for the Universal AI Development Platform."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the setup manager."""
        self.project_root = project_root or Path(__file__).parent.parent
        self.config_dir = self.project_root / "config"
        self.src_dir = self.project_root / "src"
        self.scripts_dir = self.project_root / "scripts"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are installed."""
        logger.info("🔍 Checking prerequisites...")
        
        requirements = {
            "python": {"cmd": [sys.executable, "--version"], "min_version": "3.11"},
            "git": {"cmd": ["git", "--version"], "min_version": "2.0"},
            "pip": {"cmd": [sys.executable, "-m", "pip", "--version"], "min_version": "20.0"}
        }
        
        all_good = True
        for name, req in requirements.items():
            try:
                result = subprocess.run(req["cmd"], capture_output=True, text=True, check=True)
                logger.info(f"✅ {name}: {result.stdout.strip()}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error(f"❌ {name}: Not found or version too old")
                all_good = False
        
        return all_good
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        logger.info("📦 Installing dependencies...")
        
        try:
            # Install main dependencies
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", "."
            ], cwd=self.project_root, check=True)
            
            # Install development dependencies
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"
            ], cwd=self.project_root, check=True)
            
            logger.info("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_default_config(self) -> bool:
        """Create default configuration files."""
        logger.info("⚙️ Creating default configuration...")
        
        try:
            # Main platform configuration
            platform_config = {
                "platform": {
                    "name": "Universal AI Development Platform",
                    "version": "0.1.0",
                    "environment": "development"
                },
                "analysis": {
                    "default_depth": "standard",
                    "confidence_threshold": 0.7,
                    "max_analysis_time": 300,
                    "cache_enabled": True,
                    "cache_ttl": 3600
                },
                "orchestration": {
                    "max_agents": 20,
                    "default_timeout": 300,
                    "retry_attempts": 3,
                    "load_balancing": "intelligent",
                    "agent_communication": "shared_state"
                },
                "adaptation": {
                    "auto_discovery": True,
                    "discovery_frequency": 3600,
                    "auto_integration": False,
                    "compatibility_threshold": 0.8,
                    "backup_before_integration": True
                },
                "monitoring": {
                    "enabled": True,
                    "log_level": "INFO",
                    "metrics_interval": 60,
                    "health_check_interval": 30,
                    "retention_period": "30d"
                }
            }
            
            config_file = self.config_dir / "platform.yml"
            with open(config_file, 'w') as f:
                yaml.dump(platform_config, f, default_flow_style=False, sort_keys=False)
            
            # Agent configuration
            agent_config = {
                "agents": {
                    "available": [
                        "system-architect", "general-purpose", "backend-developer",
                        "frontend-developer", "database-specialist", "api-designer",
                        "test-strategist", "code-quality-analyzer", "security-auditor",
                        "performance-optimizer", "devops-engineer", "ui-ux-designer",
                        "documentation-specialist", "debugger", "meta-agent"
                    ],
                    "coordination": {
                        "communication_protocol": "shared_state",
                        "conflict_resolution": "priority_based",
                        "load_balancing": "capability_aware"
                    },
                    "specializations": {
                        "system-architect": {"domains": ["architecture", "design", "scalability"]},
                        "security-auditor": {"domains": ["security", "compliance", "vulnerabilities"]},
                        "performance-optimizer": {"domains": ["performance", "optimization", "profiling"]}
                    }
                }
            }
            
            agents_file = self.config_dir / "agents.yml"
            with open(agents_file, 'w') as f:
                yaml.dump(agent_config, f, default_flow_style=False, sort_keys=False)
            
            # Environment configuration
            env_file = self.project_root / ".env.example"
            env_content = """# Universal AI Development Platform Environment Configuration

# API Keys (optional, for enhanced features)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here

# Platform Configuration
UAI_LOG_LEVEL=INFO
UAI_MAX_AGENTS=20
UAI_ANALYSIS_DEPTH=standard
UAI_AUTO_ADAPTATION=false

# Feature Discovery
UAI_DISCOVERY_FREQUENCY=3600
UAI_AUTO_INTEGRATION=false

# Monitoring
UAI_MONITORING_ENABLED=true
UAI_METRICS_INTERVAL=60

# Development
UAI_DEBUG=false
UAI_CACHE_ENABLED=true
"""
            
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            logger.info("✅ Default configuration created")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create configuration: {e}")
            return False
    
    def setup_database(self) -> bool:
        """Set up local database for platform data."""
        logger.info("🗄️ Setting up database...")
        
        try:
            # Create data directory
            data_dir = self.project_root / "data"
            data_dir.mkdir(exist_ok=True)
            
            # Create SQLite database for platform data
            db_file = data_dir / "platform.db"
            
            # For now, just create the file - actual schema will be created on first use
            db_file.touch()
            
            logger.info(f"✅ Database setup complete: {db_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            return False
    
    def configure_git_hooks(self) -> bool:
        """Configure Git hooks for development."""
        logger.info("🪝 Setting up Git hooks...")
        
        try:
            hooks_dir = self.project_root / ".git" / "hooks"
            if not hooks_dir.exists():
                logger.warning("⚠️ Git repository not found, skipping Git hooks")
                return True
            
            # Pre-commit hook
            pre_commit_content = """#!/bin/bash
# Universal AI Development Platform - Pre-commit hook

echo "🔍 Running pre-commit checks..."

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -x --tb=short

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi

# Run linting
echo "🔍 Running code quality checks..."
python -m ruff check src/ --fix
python -m black src/ tests/

echo "✅ Pre-commit checks passed"
"""
            
            pre_commit_file = hooks_dir / "pre-commit"
            with open(pre_commit_file, 'w') as f:
                f.write(pre_commit_content)
            
            # Make executable
            import stat
            pre_commit_file.chmod(pre_commit_file.stat().st_mode | stat.S_IEXEC)
            
            logger.info("✅ Git hooks configured")
            return True
            
        except Exception as e:
            logger.error(f"❌ Git hooks setup failed: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify that the installation is working correctly."""
        logger.info("🧪 Verifying installation...")
        
        try:
            # Test CLI import
            import_test = subprocess.run([
                sys.executable, "-c", 
                "from universal_ai_dev_platform.cli import main; print('✅ CLI import successful')"
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if import_test.returncode != 0:
                logger.error(f"❌ CLI import failed: {import_test.stderr}")
                return False
            
            logger.info(import_test.stdout.strip())
            
            # Test CLI help command
            help_test = subprocess.run([
                sys.executable, "-m", "universal_ai_dev_platform.cli", "--help"
            ], cwd=self.src_dir, capture_output=True, text=True)
            
            if help_test.returncode != 0:
                logger.error(f"❌ CLI help failed: {help_test.stderr}")
                return False
            
            logger.info("✅ CLI help command working")
            
            # Test basic functionality
            logger.info("✅ Installation verification complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Installation verification failed: {e}")
            return False
    
    def create_workspace_config(self) -> bool:
        """Create workspace configuration for development tools."""
        logger.info("🛠️ Creating workspace configuration...")
        
        try:
            # VS Code configuration
            vscode_dir = self.project_root / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            # VS Code settings
            vscode_settings = {
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.ruffEnabled": True,
                "python.formatting.provider": "black",
                "python.testing.pytestEnabled": True,
                "python.testing.pytestArgs": ["tests/"],
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/.pytest_cache": True,
                    "**/node_modules": True
                }
            }
            
            with open(vscode_dir / "settings.json", 'w') as f:
                json.dump(vscode_settings, f, indent=2)
            
            # VS Code launch configuration
            launch_config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "CLI Debug",
                        "type": "python",
                        "request": "launch",
                        "module": "universal_ai_dev_platform.cli",
                        "args": ["--help"],
                        "console": "integratedTerminal"
                    },
                    {
                        "name": "Run Tests",
                        "type": "python",
                        "request": "launch",
                        "module": "pytest",
                        "args": ["tests/", "-v"],
                        "console": "integratedTerminal"
                    }
                ]
            }
            
            with open(vscode_dir / "launch.json", 'w') as f:
                json.dump(launch_config, f, indent=2)
            
            logger.info("✅ Workspace configuration created")
            return True
            
        except Exception as e:
            logger.error(f"❌ Workspace configuration failed: {e}")
            return False
    
    async def run_complete_setup(self) -> bool:
        """Run the complete setup process."""
        logger.info("🚀 Starting Universal AI Development Platform setup...")
        logger.info("=" * 60)
        
        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Dependencies", self.install_dependencies),
            ("Configuration", self.create_default_config),
            ("Database", self.setup_database),
            ("Git Hooks", self.configure_git_hooks),
            ("Workspace", self.create_workspace_config),
            ("Verification", self.verify_installation)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n📋 Step: {step_name}")
            logger.info("-" * 40)
            
            if not step_func():
                logger.error(f"❌ Setup failed at step: {step_name}")
                return False
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Universal AI Development Platform setup complete!")
        logger.info("\n📋 Next steps:")
        logger.info("1. Copy .env.example to .env and configure your API keys")
        logger.info("2. Run: uai --help")
        logger.info("3. Try: uai analyze .")
        logger.info("4. Create a project: uai create web-app my-project")
        logger.info("\n📚 Documentation:")
        logger.info("- Getting Started: docs/GETTING_STARTED.md")
        logger.info("- Development: docs/DEVELOPMENT.md")
        logger.info("- Examples: examples/")
        
        return True


def main():
    """Main entry point for the setup script."""
    parser = argparse.ArgumentParser(
        description="Universal AI Development Platform Setup Script"
    )
    parser.add_argument(
        "--configure-all", action="store_true",
        help="Run complete setup and configuration"
    )
    parser.add_argument(
        "--prerequisites-only", action="store_true",
        help="Only check prerequisites"
    )
    parser.add_argument(
        "--config-only", action="store_true",
        help="Only create configuration files"
    )
    parser.add_argument(
        "--verify-only", action="store_true",
        help="Only verify installation"
    )
    parser.add_argument(
        "--project-root", type=Path,
        help="Path to project root directory"
    )
    
    args = parser.parse_args()
    
    # Initialize setup manager
    setup = PlatformSetup(args.project_root)
    
    if args.configure_all:
        # Run complete setup
        success = asyncio.run(setup.run_complete_setup())
        sys.exit(0 if success else 1)
    
    elif args.prerequisites_only:
        success = setup.check_prerequisites()
        sys.exit(0 if success else 1)
    
    elif args.config_only:
        success = setup.create_default_config()
        sys.exit(0 if success else 1)
    
    elif args.verify_only:
        success = setup.verify_installation()
        sys.exit(0 if success else 1)
    
    else:
        # Default: show help and run basic setup
        parser.print_help()
        print("\n" + "=" * 60)
        print("🚀 Universal AI Development Platform Setup")
        print("=" * 60)
        print("\nFor complete setup, run:")
        print("  python scripts/setup.py --configure-all")


if __name__ == "__main__":
    main()