#!/usr/bin/env python3
"""
Universal AI Development Platform - API Usage Examples

This file demonstrates how to use the Universal AI Development Platform
programmatically through its Python API.
"""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

# Add the src directory to the path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from universal_ai_dev_platform import (
    UniversalProjectAnalyzer,
    ProjectIntelligence, 
    AgentOrchestrator,
    AdaptationEngine
)
from universal_ai_dev_platform.core.orchestration import WorkflowSpecification, WorkflowPriority
from universal_ai_dev_platform.monitoring import HealthMonitor


class DevelopmentWorkflow:
    """
    Example class showing how to integrate the Universal AI Development Platform
    into your development workflow programmatically.
    """
    
    def __init__(self):
        """Initialize the development workflow components."""
        self.analyzer = UniversalProjectAnalyzer()
        self.intelligence = ProjectIntelligence()
        self.orchestrator = AgentOrchestrator()
        self.adaptation_engine = AdaptationEngine()
        self.health_monitor = HealthMonitor()
    
    async def analyze_and_optimize_project(self, project_path: str) -> Dict[str, Any]:
        """
        Complete project analysis and optimization workflow.
        
        Args:
            project_path: Path to the project to analyze
            
        Returns:
            Dict containing analysis results and optimization recommendations
        """
        print(f"🔍 Analyzing project: {project_path}")
        
        # Step 1: Analyze the project
        analysis_result = await self.analyzer.analyze_project(
            project_path,
            depth="comprehensive"
        )
        
        print(f"✅ Analysis complete:")
        print(f"   Project Type: {analysis_result.project_type}")
        print(f"   Languages: {list(analysis_result.languages_detected.keys())}")
        print(f"   Health Score: {analysis_result.health_metrics.get('overall', 'N/A')}")
        
        # Step 2: Get intelligence insights
        project_context = {
            "path": project_path,
            "type": analysis_result.project_type,
            "languages": analysis_result.languages_detected,
            "frameworks": analysis_result.frameworks_detected,
            "health_metrics": analysis_result.health_metrics
        }
        
        intelligence_insights = await self.intelligence.generate_insights(project_context)
        
        print(f"🧠 Intelligence insights generated:")
        print(f"   Confidence: {intelligence_insights.get('confidence', 0):.2f}")
        print(f"   Priority Areas: {len(intelligence_insights.get('priority_areas', []))}")
        
        # Step 3: Create optimization workflow
        workflow_spec = WorkflowSpecification(
            name="project-optimization",
            project_path=project_path,
            max_agents=10,
            priority=WorkflowPriority.NORMAL,
            dry_run=False,
            monitoring=True,
            tasks=[
                {"name": "code-quality-analysis", "type": "analysis"},
                {"name": "security-audit", "type": "security"},
                {"name": "performance-optimization", "type": "optimization"}
            ],
            dependencies={
                "security-audit": ["code-quality-analysis"],
                "performance-optimization": ["code-quality-analysis"]
            },
            required_agents=["code-quality-analyzer", "security-auditor"],
            preferred_agents=["performance-optimizer", "documentation-specialist"],
            agent_constraints={}
        )
        
        # Step 4: Execute optimization workflow
        orchestration_result = await self.orchestrator.orchestrate_workflow(workflow_spec)
        
        print(f"🎭 Orchestration complete:")
        print(f"   Status: {orchestration_result.status}")
        print(f"   Agents Used: {len(orchestration_result.agent_results)}")
        print(f"   Success Rate: {orchestration_result.success_rate:.2%}")
        
        return {
            "analysis": analysis_result,
            "intelligence": intelligence_insights,
            "orchestration": orchestration_result
        }
    
    async def monitor_adaptation_status(self) -> Dict[str, Any]:
        """
        Monitor and check adaptation status for AI industry changes.
        
        Returns:
            Dict containing adaptation status and recommendations
        """
        print("🔄 Monitoring adaptation status...")
        
        # Check current adaptation status
        status = await self.adaptation_engine.check_adaptation_status()
        
        print(f"✅ Adaptation status:")
        print(f"   Platform Version: {status.get('platform_version', 'Unknown')}")
        print(f"   Features Discovered (24h): {status.get('features_discovered_24h', 0)}")
        print(f"   Monitoring Status: {status.get('monitoring_status', 'Unknown')}")
        
        # Check for updates
        update_result = await self.adaptation_engine.check_for_updates()
        
        if update_result.get("check_completed"):
            print(f"🔍 Update check results:")
            print(f"   New Features: {update_result.get('new_features_found', 0)}")
            print(f"   Integration Ready: {update_result.get('integration_ready', 0)}")
            
            recommendations = update_result.get('recommendations', [])
            if recommendations:
                print(f"💡 Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
        
        return {
            "status": status,
            "updates": update_result
        }
    
    async def health_check_workflow(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of the platform and projects.
        
        Returns:
            Dict containing health status information
        """
        print("❤️ Performing health check...")
        
        # Get platform health status
        health_status = await self.health_monitor.get_health_status()
        
        print(f"✅ Platform health:")
        print(f"   Overall Health: {health_status.get('overall_health', 'Unknown')}")
        print(f"   Health Score: {health_status.get('health_score', 0):.2f}")
        print(f"   Monitoring Enabled: {health_status.get('monitoring_enabled', False)}")
        
        # Check for alerts
        recent_alerts = health_status.get('recent_alerts', [])
        if recent_alerts:
            print(f"🚨 Recent alerts ({len(recent_alerts)}):")
            for alert in recent_alerts[:3]:
                print(f"   • {alert.get('severity', 'INFO')}: {alert.get('message', 'No message')}")
        else:
            print("✅ No recent alerts")
        
        return health_status
    
    async def create_project_from_template(self, project_type: str, project_name: str, 
                                         config: Dict[str, Any]) -> str:
        """
        Create a new project using the platform's project templates.
        
        Args:
            project_type: Type of project to create
            project_name: Name for the new project
            config: Configuration options for the project
            
        Returns:
            Path to the created project
        """
        print(f"🚀 Creating {project_type} project: {project_name}")
        
        # This would integrate with the ProjectInitializer
        # For demonstration, we'll create a simple structure
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / project_name
            project_path.mkdir()
            
            # Create basic project files based on type
            if project_type == "web-app":
                (project_path / "package.json").write_text(json.dumps({
                    "name": project_name,
                    "version": "1.0.0",
                    "scripts": {
                        "dev": "next dev",
                        "build": "next build",
                        "start": "next start"
                    },
                    "dependencies": {
                        "react": "^18.2.0",
                        "react-dom": "^18.2.0",
                        "next": "^13.0.0"
                    }
                }, indent=2))
                
                # Create src directory
                (project_path / "src").mkdir()
                (project_path / "src" / "pages").mkdir()
                (project_path / "src" / "pages" / "index.tsx").write_text("""
import React from 'react';

export default function Home() {
  return (
    <div>
      <h1>Welcome to {project_name}</h1>
      <p>Your new project is ready!</p>
    </div>
  );
}
""".format(project_name=project_name))
            
            elif project_type == "api-service":
                (project_path / "requirements.txt").write_text("""
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
""")
                
                (project_path / "main.py").write_text(f"""
from fastapi import FastAPI

app = FastAPI(title="{project_name}")

@app.get("/")
async def root():
    return {{"message": "Welcome to {project_name} API"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")
            
            print(f"✅ Project created at: {project_path}")
            
            # Analyze the new project
            analysis_result = await self.analyzer.analyze_project(str(project_path))
            print(f"📊 Initial analysis: {analysis_result.project_type} detected")
            
            return str(project_path)


async def demo_integration_workflow():
    """
    Demonstrate a complete integration workflow using the platform.
    """
    print("🎯 Universal AI Development Platform - Integration Demo")
    print("=" * 60)
    
    # Initialize the workflow
    workflow = DevelopmentWorkflow()
    
    # Create a sample project
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "demo-project"
        project_path.mkdir()
        
        # Create sample project files
        (project_path / "package.json").write_text(json.dumps({
            "name": "demo-project",
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "express": "^4.18.0"
            }
        }, indent=2))
        
        (project_path / "index.js").write_text("""
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
""")
        
        # Workflow 1: Analyze and optimize
        print("\n🔍 Workflow 1: Project Analysis and Optimization")
        print("-" * 50)
        analysis_results = await workflow.analyze_and_optimize_project(str(project_path))
        
        # Workflow 2: Monitor adaptations
        print("\n🔄 Workflow 2: Adaptation Monitoring")
        print("-" * 50)
        adaptation_results = await workflow.monitor_adaptation_status()
        
        # Workflow 3: Health check
        print("\n❤️ Workflow 3: Health Monitoring")
        print("-" * 50)
        health_results = await workflow.health_check_workflow()
        
        # Summary
        print("\n📊 Integration Demo Summary")
        print("=" * 60)
        print("✅ Project analysis completed")
        print("✅ Adaptation monitoring active")
        print("✅ Health monitoring operational")
        print("✅ All workflows executed successfully")
        
        return {
            "analysis": analysis_results,
            "adaptation": adaptation_results,
            "health": health_results
        }


async def main():
    """
    Main function to run the API usage examples.
    """
    print("🚀 Universal AI Development Platform - API Usage Examples")
    print("=" * 60)
    print()
    
    try:
        # Run the integration demo
        results = await demo_integration_workflow()
        
        print("\n🎉 API Demo completed successfully!")
        print("\nNext steps for integration:")
        print("1. Import the platform modules in your Python project")
        print("2. Create workflow classes for your specific use cases")
        print("3. Set up monitoring and adaptation in your CI/CD pipeline")
        print("4. Use the orchestration system for complex development tasks")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("This is expected in a demo environment without full dependencies.")
        print("In a real environment, all components would be properly configured.")


if __name__ == "__main__":
    # Run the API examples
    asyncio.run(main())