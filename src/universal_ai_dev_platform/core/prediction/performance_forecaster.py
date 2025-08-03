"""
Performance Forecaster

Advanced performance prediction system that forecasts application performance
characteristics, bottlenecks, and scalability limits based on current metrics.
"""

import asyncio
import logging
import numpy as np
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import math

from .predictive_intelligence import PredictionResult, PredictionType, PredictionConfidence

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Types of performance metrics to forecast."""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    MEMORY_USAGE = "memory_usage"
    CPU_UTILIZATION = "cpu_utilization"
    DATABASE_PERFORMANCE = "database_performance"
    SCALABILITY_LIMIT = "scalability_limit"


@dataclass
class PerformancePrediction:
    """Specific performance prediction with detailed forecasting."""
    metric: PerformanceMetric
    current_value: float
    predicted_value: float
    trend: str  # improving, stable, degrading
    confidence_interval: Tuple[float, float]
    bottleneck_likelihood: float


class PerformanceForecaster:
    """
    Advanced performance forecasting system using trend analysis, regression models,
    and performance pattern recognition to predict future performance characteristics.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the performance forecaster."""
        self.config = config or {}
        self.performance_models = self._initialize_models()
        self.baseline_metrics = self._load_baseline_metrics()
    
    def _initialize_models(self) -> Dict[str, Dict]:
        """Initialize performance prediction models."""
        return {
            "response_time_model": {
                "factors": ["complexity", "data_size", "concurrent_users", "database_queries"],
                "weights": [0.3, 0.25, 0.25, 0.2],
                "baseline_response_time": 200  # milliseconds
            },
            "throughput_model": {
                "factors": ["cpu_cores", "memory_available", "io_capacity", "concurrency"],
                "weights": [0.35, 0.25, 0.25, 0.15],
                "baseline_throughput": 1000  # requests per second
            },
            "memory_model": {
                "factors": ["data_structures", "caching_strategy", "object_lifecycle", "gc_efficiency"],
                "weights": [0.4, 0.25, 0.2, 0.15],
                "baseline_memory": 512  # MB
            },
            "scalability_model": {
                "factors": ["architecture_pattern", "database_design", "caching_layers", "statelessness"],
                "weights": [0.4, 0.3, 0.2, 0.1],
                "scale_factors": {"horizontal": 1.0, "vertical": 0.7, "hybrid": 1.2}
            }
        }
    
    def _load_baseline_metrics(self) -> Dict[str, float]:
        """Load baseline performance metrics for comparison."""
        return {
            "web_app_response_time": 150,  # ms
            "api_response_time": 50,       # ms
            "database_query_time": 10,     # ms
            "memory_per_user": 5,          # MB
            "cpu_per_request": 2,          # %
            "max_concurrent_users": 1000
        }
    
    async def forecast_performance(self, project_context: Dict[str, Any], 
                                 timeline: str) -> List[PredictionResult]:
        """
        Forecast performance characteristics for the given timeline.
        
        Args:
            project_context: Current project state and metrics
            timeline: Prediction timeline
            
        Returns:
            List of performance predictions
        """
        logger.info("Forecasting performance characteristics...")
        
        predictions = []
        
        try:
            # Run performance forecasts in parallel
            forecast_tasks = [
                self._forecast_response_time(project_context, timeline),
                self._forecast_scalability(project_context, timeline),
                self._forecast_resource_usage(project_context, timeline),
                self._forecast_bottlenecks(project_context, timeline)
            ]
            
            forecast_results = await asyncio.gather(*forecast_tasks, return_exceptions=True)
            
            # Process results
            for result in forecast_results:
                if isinstance(result, PredictionResult):
                    predictions.append(result)
                elif isinstance(result, list):
                    predictions.extend(result)
                elif isinstance(result, Exception):
                    logger.warning(f"Performance forecast failed: {result}")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Performance forecasting failed: {e}")
            return []
    
    async def _forecast_response_time(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Forecast application response time trends."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            health_metrics = project_context.get("health_metrics", {})
            project_type = project_context.get("project_type", "web-app")
            
            # Base response time by project type
            base_response_time = self.baseline_metrics.get(f"{project_type}_response_time", 150)
            
            factors = []
            multiplier = 1.0
            
            # Code complexity impact
            complexity = complexity_metrics.get("cyclomatic_complexity", 2.0)
            if complexity > 5:
                complexity_factor = 1 + ((complexity - 5) * 0.1)
                multiplier *= complexity_factor
                factors.append(f"High code complexity ({complexity:.1f})")
            
            # Lines of code impact (larger codebases tend to be slower)
            loc = complexity_metrics.get("lines_of_code", 10000)
            if loc > 50000:
                size_factor = 1 + min(0.5, (loc - 50000) / 200000)
                multiplier *= size_factor
                factors.append(f"Large codebase ({loc:,} lines)")
            
            # Database complexity (more queries = slower response)
            dependency_count = complexity_metrics.get("dependency_count", 20)
            if dependency_count > 30:
                db_factor = 1 + ((dependency_count - 30) * 0.01)
                multiplier *= db_factor
                factors.append(f"High dependency count ({dependency_count})")
            
            # Performance optimization level
            performance_score = health_metrics.get("performance", 0.8)
            if performance_score < 0.7:
                perf_factor = 1 + ((0.7 - performance_score) * 2)
                multiplier *= perf_factor
                factors.append(f"Low performance optimization ({performance_score:.1%})")
            
            # Calculate predicted response time
            predicted_response_time = base_response_time * multiplier
            
            # Determine severity and probability
            performance_degradation = multiplier - 1.0
            probability = min(0.95, performance_degradation * 1.5)
            confidence = self._calculate_confidence(probability, len(factors))
            
            # Severity based on response time thresholds
            if predicted_response_time > 1000:
                severity = "critical"
            elif predicted_response_time > 500:
                severity = "high"
            elif predicted_response_time > 200:
                severity = "medium"
            else:
                severity = "low"
            
            return PredictionResult(
                prediction_type=PredictionType.PERFORMANCE_FORECAST,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Response time predicted to be {predicted_response_time:.0f}ms (current baseline: {base_response_time}ms)",
                predicted_issues=[
                    f"Average response time: {predicted_response_time:.0f}ms",
                    "User experience degradation",
                    "Potential timeout issues"
                ] if predicted_response_time > 300 else [
                    f"Acceptable response time: {predicted_response_time:.0f}ms"
                ],
                impact_areas=["User experience", "Conversion rates", "SEO rankings"] if predicted_response_time > 300 else ["User satisfaction"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement caching strategies",
                    "Optimize database queries",
                    "Consider code splitting and lazy loading",
                    "Profile and optimize hot paths"
                ] if predicted_response_time > 300 else [
                    "Continue current performance practices"
                ],
                prevention_strategies=[
                    "Performance testing in CI/CD",
                    "Regular performance monitoring",
                    "Performance budgets implementation",
                    "Continuous profiling"
                ],
                prediction_id=f"response_time_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="perf_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "predicted_response_time_ms": predicted_response_time,
                    "baseline_response_time_ms": base_response_time,
                    "performance_multiplier": multiplier
                }
            )
            
        except Exception as e:
            logger.error(f"Response time forecasting failed: {e}")
            return None
    
    async def _forecast_scalability(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Forecast scalability characteristics and limits."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            health_metrics = project_context.get("health_metrics", {})
            frameworks = project_context.get("frameworks_detected", {})
            
            factors = []
            scalability_score = 1.0
            
            # Architecture patterns impact
            architecture_score = health_metrics.get("architecture", 0.8)
            if architecture_score < 0.7:
                arch_impact = (0.7 - architecture_score) * 2
                scalability_score -= arch_impact * 0.4
                factors.append(f"Suboptimal architecture patterns ({architecture_score:.1%})")
            
            # Database design impact (simulated based on complexity)
            dependency_count = complexity_metrics.get("dependency_count", 20)
            if dependency_count > 50:
                db_impact = min(0.3, (dependency_count - 50) / 100)
                scalability_score -= db_impact
                factors.append(f"Potential database scalability issues ({dependency_count} dependencies)")
            
            # Framework scalability characteristics
            scalable_frameworks = {"react", "vue", "fastapi", "express", "go"}
            detected_frameworks = set(frameworks.keys())
            if detected_frameworks.intersection(scalable_frameworks):
                scalability_score += 0.1
                factors.append("Scalable frameworks detected")
            
            # Code complexity impact on scalability
            complexity = complexity_metrics.get("cyclomatic_complexity", 2.0)
            if complexity > 8:
                complexity_impact = min(0.4, (complexity - 8) / 10)
                scalability_score -= complexity_impact
                factors.append(f"High complexity may limit scalability ({complexity:.1f})")
            
            # Calculate scalability metrics
            scalability_score = max(0.1, min(1.0, scalability_score))
            max_concurrent_users = int(self.baseline_metrics["max_concurrent_users"] * scalability_score)
            
            # Determine if this is a problem
            probability = 1.0 - scalability_score if scalability_score < 0.7 else 0.2
            confidence = self._calculate_confidence(probability, len(factors))
            
            severity = "high" if scalability_score < 0.5 else "medium" if scalability_score < 0.7 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.PERFORMANCE_FORECAST,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Scalability forecast: {max_concurrent_users:,} max concurrent users (score: {scalability_score:.1%})",
                predicted_issues=[
                    f"Estimated user capacity: {max_concurrent_users:,}",
                    "Performance degradation under load",
                    "Potential system bottlenecks"
                ] if scalability_score < 0.7 else [
                    f"Good scalability potential: {max_concurrent_users:,} users"
                ],
                impact_areas=["User capacity", "System stability", "Growth potential"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Implement horizontal scaling strategies",
                    "Optimize database for scale",
                    "Add load balancing",
                    "Consider microservices architecture"
                ] if scalability_score < 0.7 else [
                    "Monitor scaling metrics",
                    "Plan for gradual capacity increases"
                ],
                prevention_strategies=[
                    "Load testing implementation",
                    "Scalability-first architecture",
                    "Performance monitoring at scale",
                    "Capacity planning processes"
                ],
                prediction_id=f"scalability_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="perf_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "scalability_score": scalability_score,
                    "max_concurrent_users": max_concurrent_users,
                    "scaling_confidence": confidence.value
                }
            )
            
        except Exception as e:
            logger.error(f"Scalability forecasting failed: {e}")
            return None
    
    async def _forecast_resource_usage(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Forecast memory and CPU resource usage trends."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            project_type = project_context.get("project_type", "web-app")
            
            factors = []
            memory_multiplier = 1.0
            cpu_multiplier = 1.0
            
            # Base resource usage
            base_memory = self.baseline_metrics["memory_per_user"] * 100  # MB for 100 users
            base_cpu = self.baseline_metrics["cpu_per_request"] * 100     # % for 100 requests
            
            # Code size impact
            loc = complexity_metrics.get("lines_of_code", 10000)
            if loc > 30000:
                size_factor = 1 + ((loc - 30000) / 100000)
                memory_multiplier *= size_factor
                cpu_multiplier *= size_factor * 0.8  # CPU scales less with code size
                factors.append(f"Large codebase impact ({loc:,} lines)")
            
            # Dependency impact
            dependency_count = complexity_metrics.get("dependency_count", 20)
            if dependency_count > 40:
                dep_factor = 1 + ((dependency_count - 40) / 200)
                memory_multiplier *= dep_factor
                factors.append(f"High dependency overhead ({dependency_count} dependencies)")
            
            # Project type specific adjustments
            type_adjustments = {
                "ai-project": {"memory": 3.0, "cpu": 2.5},
                "mobile-app": {"memory": 0.5, "cpu": 0.7},
                "api-service": {"memory": 1.2, "cpu": 1.5},
                "web-app": {"memory": 1.0, "cpu": 1.0}
            }
            
            adjustments = type_adjustments.get(project_type, {"memory": 1.0, "cpu": 1.0})
            memory_multiplier *= adjustments["memory"]
            cpu_multiplier *= adjustments["cpu"]
            
            if adjustments["memory"] > 1.5 or adjustments["cpu"] > 1.5:
                factors.append(f"Higher resource requirements for {project_type}")
            
            # Calculate predicted usage
            predicted_memory = base_memory * memory_multiplier
            predicted_cpu = base_cpu * cpu_multiplier
            
            # Determine if this is concerning
            resource_concern = max(memory_multiplier - 1, cpu_multiplier - 1)
            probability = min(0.9, resource_concern * 1.5)
            confidence = self._calculate_confidence(probability, len(factors))
            
            severity = "high" if resource_concern > 1.0 else "medium" if resource_concern > 0.5 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.PERFORMANCE_FORECAST,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Resource usage forecast: {predicted_memory:.0f}MB memory, {predicted_cpu:.1f}% CPU (per 100 users/requests)",
                predicted_issues=[
                    f"Memory usage: {predicted_memory:.0f}MB",
                    f"CPU utilization: {predicted_cpu:.1f}%",
                    "Potential resource constraints"
                ] if resource_concern > 0.5 else [
                    f"Reasonable resource usage: {predicted_memory:.0f}MB memory, {predicted_cpu:.1f}% CPU"
                ],
                impact_areas=["System capacity", "Infrastructure costs", "Response times"],
                severity=severity,
                factors=factors,
                recommendations=[
                    "Monitor resource usage patterns",
                    "Implement memory optimization strategies",
                    "Consider resource pooling",
                    "Plan infrastructure scaling"
                ] if resource_concern > 0.5 else [
                    "Continue current resource management",
                    "Monitor for usage trends"
                ],
                prevention_strategies=[
                    "Resource monitoring and alerting",
                    "Memory profiling and optimization",
                    "Capacity planning processes",
                    "Auto-scaling implementation"
                ],
                prediction_id=f"resources_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="perf_v1.0",
                data_points_analyzed=len(factors),
                metadata={
                    "predicted_memory_mb": predicted_memory,
                    "predicted_cpu_percent": predicted_cpu,
                    "memory_multiplier": memory_multiplier,
                    "cpu_multiplier": cpu_multiplier
                }
            )
            
        except Exception as e:
            logger.error(f"Resource usage forecasting failed: {e}")
            return None
    
    async def _forecast_bottlenecks(self, project_context: Dict, timeline: str) -> PredictionResult:
        """Forecast potential performance bottlenecks."""
        try:
            complexity_metrics = project_context.get("complexity_metrics", {})
            health_metrics = project_context.get("health_metrics", {})
            
            bottlenecks = []
            probability = 0.0
            
            # Database bottleneck prediction
            dependency_count = complexity_metrics.get("dependency_count", 20)
            if dependency_count > 40:
                db_bottleneck_prob = min(0.8, (dependency_count - 40) / 60)
                probability = max(probability, db_bottleneck_prob)
                bottlenecks.append({
                    "type": "Database queries",
                    "probability": db_bottleneck_prob,
                    "description": "High dependency count suggests complex data operations"
                })
            
            # Frontend bottleneck (for web apps)
            project_type = project_context.get("project_type", "web-app")
            if project_type == "web-app":
                loc = complexity_metrics.get("lines_of_code", 10000)
                if loc > 50000:
                    frontend_bottleneck_prob = min(0.7, (loc - 50000) / 100000)
                    probability = max(probability, frontend_bottleneck_prob)
                    bottlenecks.append({
                        "type": "Frontend bundle size",
                        "probability": frontend_bottleneck_prob,
                        "description": "Large codebase may result in slow loading times"
                    })
            
            # Memory bottleneck
            complexity = complexity_metrics.get("cyclomatic_complexity", 2.0)
            if complexity > 7:
                memory_bottleneck_prob = min(0.6, (complexity - 7) / 10)
                probability = max(probability, memory_bottleneck_prob)
                bottlenecks.append({
                    "type": "Memory allocation",
                    "probability": memory_bottleneck_prob,
                    "description": "High complexity may lead to inefficient memory usage"
                })
            
            # API bottleneck (for API services)
            if project_type == "api-service":
                performance_score = health_metrics.get("performance", 0.8)
                if performance_score < 0.6:
                    api_bottleneck_prob = (0.6 - performance_score) * 2
                    probability = max(probability, api_bottleneck_prob)
                    bottlenecks.append({
                        "type": "API endpoint performance",
                        "probability": api_bottleneck_prob,
                        "description": "Low performance score indicates potential API slowdowns"
                    })
            
            confidence = self._calculate_confidence(probability, len(bottlenecks))
            severity = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
            
            return PredictionResult(
                prediction_type=PredictionType.PERFORMANCE_FORECAST,
                confidence=confidence,
                probability=probability,
                timeline=timeline,
                description=f"Performance bottleneck analysis: {len(bottlenecks)} potential bottlenecks identified",
                predicted_issues=[
                    f"{bottleneck['type']}: {bottleneck['probability']:.1%} likelihood"
                    for bottleneck in bottlenecks
                ] if bottlenecks else ["No significant bottlenecks predicted"],
                impact_areas=["System throughput", "User experience", "Scalability"],
                severity=severity,
                factors=[bottleneck["description"] for bottleneck in bottlenecks],
                recommendations=[
                    "Profile application performance under load",
                    "Implement performance monitoring",
                    "Optimize identified bottleneck areas",
                    "Consider performance testing in CI/CD"
                ] if bottlenecks else [
                    "Continue performance monitoring",
                    "Maintain current optimization practices"
                ],
                prevention_strategies=[
                    "Regular performance profiling",
                    "Load testing implementation",
                    "Performance budgets and monitoring",
                    "Code review for performance impact"
                ],
                prediction_id=f"bottlenecks_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                created_at=datetime.now(),
                model_version="perf_v1.0",
                data_points_analyzed=len(bottlenecks),
                metadata={
                    "bottlenecks": bottlenecks,
                    "max_bottleneck_probability": probability
                }
            )
            
        except Exception as e:
            logger.error(f"Bottleneck forecasting failed: {e}")
            return None
    
    def _calculate_confidence(self, probability: float, factor_count: int) -> PredictionConfidence:
        """Calculate prediction confidence based on probability and available factors."""
        confidence_score = (probability * 0.6) + (min(1.0, factor_count / 4) * 0.4)
        
        if confidence_score >= 0.8:
            return PredictionConfidence.VERY_HIGH
        elif confidence_score >= 0.65:
            return PredictionConfidence.HIGH
        elif confidence_score >= 0.45:
            return PredictionConfidence.MEDIUM
        elif confidence_score >= 0.25:
            return PredictionConfidence.LOW
        else:
            return PredictionConfidence.VERY_LOW


# Example usage
if __name__ == "__main__":
    async def main():
        forecaster = PerformanceForecaster()
        
        # Example project context
        project_context = {
            "project_type": "web-app",
            "complexity_metrics": {
                "cyclomatic_complexity": 6.5,
                "lines_of_code": 75000,
                "dependency_count": 65
            },
            "health_metrics": {
                "performance": 0.65,
                "architecture": 0.70
            },
            "frameworks_detected": {
                "react": 0.9,
                "express": 0.8
            }
        }
        
        predictions = await forecaster.forecast_performance(project_context, "3months")
        
        print(f"Generated {len(predictions)} performance predictions:")
        for pred in predictions:
            if pred:
                print(f"\n- {pred.description}")
                print(f"  Probability: {pred.probability:.1%}")
                print(f"  Confidence: {pred.confidence.value}")
                print(f"  Severity: {pred.severity}")
    
    asyncio.run(main())