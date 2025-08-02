#!/usr/bin/env python3
"""
Universal AI Development Platform - Quick Start Examples

This file demonstrates the basic usage of the Universal AI Development Platform
for common development tasks.
"""

import asyncio
import tempfile
import json
from pathlib import Path

# Add the src directory to the path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from universal_ai_dev_platform import (
    UniversalProjectAnalyzer,
    ProjectIntelligence,
    AgentOrchestrator,
    AdaptationEngine
)


async def example_1_analyze_project():
    """
    Example 1: Analyze an existing project
    
    This example shows how to use the Universal Project Analyzer to understand
    any codebase and get intelligent recommendations.
    """
    print("🔍 Example 1: Project Analysis")
    print("-" * 40)
    
    # Create a sample project for analysis
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        
        # Create sample files
        (project_path / "package.json").write_text(json.dumps({
            "name": "sample-react-app",
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@types/react": "^18.0.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            }
        }, indent=2))
        
        (project_path / "src" / "App.tsx").parent.mkdir(exist_ok=True)
        (project_path / "src" / "App.tsx").write_text("""
import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to My App</h1>
        <p>This is a sample React application.</p>
      </header>
    </div>
  );
}

export default App;
""")
        
        # Analyze the project
        analyzer = UniversalProjectAnalyzer()
        try:
            result = await analyzer.analyze_project(str(project_path))
            
            print(f"✅ Project analyzed successfully!")
            print(f"   Project Type: {result.project_type}")
            print(f"   Languages: {list(result.languages_detected.keys())}")
            print(f"   Frameworks: {list(result.frameworks_detected.keys())}")
            print(f"   Health Score: {result.health_metrics.get('overall', 'N/A')}")
            print(f"   Recommendations: {len(result.recommendations)}")
            
            if result.recommendations:
                print("\n💡 Top Recommendations:")
                for i, rec in enumerate(result.recommendations[:3], 1):
                    print(f"   {i}. {rec}")
                    
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    print()


async def example_2_adaptation_monitoring():
    """
    Example 2: Monitor AI industry adaptations
    
    This example shows how to use the Adaptation Engine to stay current
    with AI industry changes and automatically discover new capabilities.
    """
    print("🔄 Example 2: Adaptation Monitoring")
    print("-" * 40)
    
    try:
        # Initialize the adaptation engine
        adaptation_engine = AdaptationEngine()
        
        # Check current adaptation status
        status = await adaptation_engine.check_adaptation_status()
        
        print(f"✅ Adaptation status retrieved!")
        print(f"   Platform Version: {status.get('platform_version', 'Unknown')}")
        print(f"   Features Discovered (24h): {status.get('features_discovered_24h', 0)}")
        print(f"   Integration Candidates: {status.get('integration_candidates', 0)}")
        print(f"   Auto Integration: {status.get('auto_integration_enabled', False)}")
        print(f"   Monitoring Status: {status.get('monitoring_status', 'Unknown')}")
        
        # Check for new updates
        print("\n🔍 Checking for new AI features...")
        update_result = await adaptation_engine.check_for_updates()
        
        if update_result.get("check_completed"):
            print(f"✅ Update check completed!")
            print(f"   New Features Found: {update_result.get('new_features_found', 0)}")
            print(f"   Integration Ready: {update_result.get('integration_ready', 0)}")
            print(f"   Requires Changes: {update_result.get('requires_changes', 0)}")
            print(f"   Incompatible: {update_result.get('incompatible', 0)}")
            
            recommendations = update_result.get('recommendations', [])
            if recommendations:
                print("\n💡 Adaptation Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
        else:
            print(f"❌ Update check failed: {update_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Adaptation monitoring failed: {e}")
    
    print()


async def example_3_intelligence_insights():
    """
    Example 3: Get AI-powered project intelligence
    
    This example demonstrates how to use Project Intelligence to get
    predictive insights and optimization recommendations.
    """
    print("🧠 Example 3: Project Intelligence")
    print("-" * 40)
    
    try:
        # Initialize project intelligence
        intelligence = ProjectIntelligence()
        
        # Create a mock project context
        project_context = {
            "path": "/sample/project",
            "type": "web-app",
            "languages": {"typescript": 80, "javascript": 20},
            "frameworks": {"react": 0.9, "express": 0.8},
            "health_metrics": {
                "code_quality": 0.75,
                "test_coverage": 0.60,
                "documentation": 0.50,
                "security": 0.85
            }
        }
        
        # Get predictive insights
        insights = await intelligence.generate_insights(project_context)
        
        print(f"✅ Intelligence insights generated!")
        print(f"   Analysis Type: {insights.get('analysis_type', 'Predictive')}")
        print(f"   Confidence: {insights.get('confidence', 0):.2f}")
        print(f"   Priority Areas: {len(insights.get('priority_areas', []))}")
        
        priority_areas = insights.get('priority_areas', [])
        if priority_areas:
            print("\n🎯 Priority Areas for Improvement:")
            for i, area in enumerate(priority_areas[:3], 1):
                print(f"   {i}. {area}")
        
        predictions = insights.get('predictions', [])
        if predictions:
            print(f"\n🔮 Predictions ({len(predictions)} total):")
            for i, prediction in enumerate(predictions[:2], 1):
                print(f"   {i}. {prediction}")
                
    except Exception as e:
        print(f"❌ Intelligence analysis failed: {e}")
    
    print()


async def example_4_agent_orchestration():
    """
    Example 4: Multi-agent workflow orchestration
    
    This example shows how to coordinate multiple AI agents for complex
    development tasks with parallel execution.
    """
    print("🎭 Example 4: Agent Orchestration")
    print("-" * 40)
    
    try:
        # Initialize the agent orchestrator
        orchestrator = AgentOrchestrator()
        
        # Define a workflow specification
        from universal_ai_dev_platform.core.orchestration import WorkflowSpecification, WorkflowPriority
        
        workflow_spec = WorkflowSpecification(
            name="project-enhancement",
            project_path="/sample/project",
            max_agents=5,
            priority=WorkflowPriority.NORMAL,
            dry_run=True,  # Safe to run as example
            monitoring=True,
            tasks=[
                {"name": "code-review", "type": "analysis"},
                {"name": "test-enhancement", "type": "testing"},
                {"name": "documentation-update", "type": "documentation"}
            ],
            dependencies={
                "test-enhancement": ["code-review"],
                "documentation-update": ["code-review"]
            },
            required_agents=["code-quality-analyzer", "test-strategist"],
            preferred_agents=["documentation-specialist", "security-auditor"],
            agent_constraints={}
        )
        
        # Execute the workflow
        result = await orchestrator.orchestrate_workflow(workflow_spec)
        
        print(f"✅ Workflow orchestration completed!")
        print(f"   Workflow ID: {result.workflow_id}")
        print(f"   Status: {result.status}")
        print(f"   Agents Used: {len(result.agent_results)}")
        print(f"   Total Duration: {result.total_duration:.2f}s")
        print(f"   Success Rate: {result.success_rate:.2%}")
        
        if result.agent_results:
            print(f"\n🤖 Agent Results:")
            for agent_name, agent_result in list(result.agent_results.items())[:3]:
                status = agent_result.get('status', 'unknown')
                print(f"   • {agent_name}: {status}")
        
        if result.workflow_outputs:
            print(f"\n📋 Workflow Outputs: {len(result.workflow_outputs)} items")
            
    except Exception as e:
        print(f"❌ Agent orchestration failed: {e}")
    
    print()


async def main():
    """
    Run all examples to demonstrate the Universal AI Development Platform capabilities.
    """
    print("🚀 Universal AI Development Platform - Quick Start Examples")
    print("=" * 60)
    print()
    
    # Run examples sequentially
    await example_1_analyze_project()
    await example_2_adaptation_monitoring()
    await example_3_intelligence_insights()
    await example_4_agent_orchestration()
    
    print("🎉 All examples completed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Try the CLI commands: uai analyze ./my-project")
    print("2. Create a new project: uai create web-app my-new-app")
    print("3. Run orchestrated workflows: uai orchestrate feature-development")
    print("4. Monitor adaptations: uai adapt --status")
    print()
    print("📚 For more information, see:")
    print("   - README.md for overview")
    print("   - docs/GETTING_STARTED.md for detailed guide")
    print("   - docs/DEVELOPMENT.md for development setup")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())