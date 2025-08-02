"""
Universal AI Development Platform

A revolutionary AI-powered development platform that evolves with the industry.
"""

__version__ = "0.1.0"
__author__ = "Universal AI Dev Team"
__email__ = "team@universal-ai-dev.com"
__license__ = "MIT"

# Core modules
from .core.intelligence import ProjectIntelligence
from .core.orchestration import AgentOrchestrator
from .core.adaptation import AdaptationEngine
from .core.prediction import PredictiveIntelligence

# Main interfaces
from .analysis.project_scanner import UniversalProjectAnalyzer
from .workflows.initialization import ProjectInitializer
from .agents.coordination import AgentCoordinator

__all__ = [
    "ProjectIntelligence",
    "AgentOrchestrator", 
    "AdaptationEngine",
    "PredictiveIntelligence",
    "UniversalProjectAnalyzer",
    "ProjectInitializer",
    "AgentCoordinator",
]