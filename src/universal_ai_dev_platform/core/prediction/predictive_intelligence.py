"""
Predictive Intelligence

Main predictive modeling system that uses ML and statistical analysis to predict
development issues, performance impacts, and architectural evolution needs.
"""

import asyncio
import logging
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class PredictionType(Enum):
    """Types of predictions the system can make."""
    ISSUE_PREDICTION = "issue_prediction"
    PERFORMANCE_FORECAST = "performance_forecast"
    SECURITY_RISK = "security_risk"
    ARCHITECTURE_EVOLUTION = "architecture_evolution"
    MAINTENANCE_BURDEN = "maintenance_burden"
    SCALABILITY_LIMITS = "scalability_limits"


class PredictionConfidence(Enum):
    """Confidence levels for predictions."""
    VERY_LOW = "very_low"
    LOW = "low" 
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class PredictionResult:
    """Result of a predictive analysis."""
    
    prediction_type: PredictionType
    confidence: PredictionConfidence
    probability: float  # 0.0 to 1.0
    timeline: str  # e.g., "1week", "1month", "3months"
    
    # Prediction details
    description: str
    predicted_issues: List[str]
    impact_areas: List[str]
    severity: str  # low, medium, high, critical
    
    # Supporting data
    factors: List[str]
    recommendations: List[str]
    prevention_strategies: List[str]
    
    # Metadata
    prediction_id: str
    created_at: datetime
    model_version: str
    data_points_analyzed: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class PredictiveIntelligence:
    """
    Main predictive intelligence system that combines multiple models and techniques
    to provide accurate predictions about development projects.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the predictive intelligence system."""
        self.config = config or self._default_config()
        self.models = {}
        self.historical_data = []
        self.prediction_cache = {}
        self._initialize_models()
    
    def _default_config(self) -> Dict:
        """Default configuration for predictive intelligence."""
        return {
            "prediction": {
                "default_timeline": "1month",
                "confidence_threshold": 0.6,
                "cache_ttl": 3600,
                "max_predictions_per_analysis": 10,
                "enable_ml_models": True,
                "historical_data_limit": 1000
            },
            "models": {
                "issue_prediction": {
                    "enabled": True,
                    "weight": 1.0,
                    "features": ["complexity", "test_coverage", "code_quality", "dependencies"]
                },
                "performance_forecast": {
                    "enabled": True,
                    "weight": 1.0,
                    "features": ["architecture", "data_patterns", "load_metrics", "resource_usage"]
                },
                "risk_assessment": {
                    "enabled": True,
                    "weight": 0.8,
                    "features": ["security_score", "dependency_age", "maintainability", "complexity"]
                }
            }
        }
    
    def _initialize_models(self):
        """Initialize prediction models."""
        logger.info("Initializing predictive models...")
        
        # Import model classes
        from .issue_predictor import IssuePredictor
        from .performance_forecaster import PerformanceForecaster
        from .risk_analyzer import RiskAnalyzer
        
        # Initialize models
        self.models = {
            "issue_predictor": IssuePredictor(self.config),
            "performance_forecaster": PerformanceForecaster(self.config),
            "risk_analyzer": RiskAnalyzer(self.config)
        }
        
        logger.info(f"Initialized {len(self.models)} prediction models")
    
    async def predict_project_future(self, project_context: Dict[str, Any], 
                                   timeline: str = "1month") -> List[PredictionResult]:
        """
        Generate comprehensive predictions for a project's future.
        
        Args:
            project_context: Current project state and metrics
            timeline: Prediction timeline (1week, 1month, 3months, 6months)
            
        Returns:
            List of prediction results ordered by confidence and impact
        """
        logger.info(f"Generating predictions for timeline: {timeline}")
        
        predictions = []
        
        try:
            # Run predictions from all models in parallel
            prediction_tasks = []
            
            if self.config["models"]["issue_prediction"]["enabled"]:
                prediction_tasks.append(
                    self._predict_issues(project_context, timeline)
                )
            
            if self.config["models"]["performance_forecast"]["enabled"]:
                prediction_tasks.append(
                    self._predict_performance(project_context, timeline)
                )
            
            if self.config["models"]["risk_assessment"]["enabled"]:
                prediction_tasks.append(
                    self._predict_risks(project_context, timeline)
                )
            
            # Wait for all predictions
            model_results = await asyncio.gather(*prediction_tasks, return_exceptions=True)
            
            # Collect successful predictions
            for result in model_results:
                if isinstance(result, list):
                    predictions.extend(result)
                elif isinstance(result, PredictionResult):
                    predictions.append(result)
                elif isinstance(result, Exception):
                    logger.warning(f"Prediction model failed: {result}")
            
            # Add meta-predictions (cross-model insights)
            meta_predictions = await self._generate_meta_predictions(
                project_context, predictions, timeline
            )
            predictions.extend(meta_predictions)
            
            # Sort by confidence and impact
            predictions = self._rank_predictions(predictions)
            
            # Limit to max predictions
            max_predictions = self.config["prediction"]["max_predictions_per_analysis"]
            predictions = predictions[:max_predictions]
            
            logger.info(f"Generated {len(predictions)} predictions")
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction generation failed: {e}")
            return []
    
    async def _predict_issues(self, project_context: Dict, timeline: str) -> List[PredictionResult]:
        """Predict potential development issues."""
        issue_predictor = self.models["issue_predictor"]
        return await issue_predictor.predict_issues(project_context, timeline)
    
    async def _predict_performance(self, project_context: Dict, timeline: str) -> List[PredictionResult]:
        """Predict performance characteristics."""
        performance_forecaster = self.models["performance_forecaster"]
        return await performance_forecaster.forecast_performance(project_context, timeline)
    
    async def _predict_risks(self, project_context: Dict, timeline: str) -> List[PredictionResult]:
        """Predict security and maintenance risks."""
        risk_analyzer = self.models["risk_analyzer"]
        return await risk_analyzer.analyze_risks(project_context, timeline)
    
    async def _generate_meta_predictions(self, project_context: Dict, 
                                       base_predictions: List[PredictionResult],
                                       timeline: str) -> List[PredictionResult]:
        """
        Generate meta-predictions based on cross-model analysis.
        These are higher-level insights derived from multiple prediction models.
        """
        meta_predictions = []
        
        try:
            # Analyze prediction patterns
            issue_count = len([p for p in base_predictions if p.prediction_type == PredictionType.ISSUE_PREDICTION])
            perf_issues = len([p for p in base_predictions if p.prediction_type == PredictionType.PERFORMANCE_FORECAST])
            security_risks = len([p for p in base_predictions if p.prediction_type == PredictionType.SECURITY_RISK])
            
            # Meta-prediction: Architecture evolution need
            if issue_count > 3 or perf_issues > 2:
                architecture_prediction = PredictionResult(
                    prediction_type=PredictionType.ARCHITECTURE_EVOLUTION,
                    confidence=PredictionConfidence.HIGH if issue_count > 5 else PredictionConfidence.MEDIUM,
                    probability=min(0.9, 0.1 * issue_count + 0.15 * perf_issues),
                    timeline=timeline,
                    description="Architecture refactoring may be needed due to accumulating technical debt",
                    predicted_issues=["Technical debt accumulation", "Scalability constraints"],
                    impact_areas=["Maintainability", "Performance", "Developer productivity"],
                    severity="medium" if issue_count < 5 else "high",
                    factors=[
                        f"Multiple issues predicted ({issue_count})",
                        f"Performance concerns identified ({perf_issues})",
                        "Cross-cutting concerns detected"
                    ],
                    recommendations=[
                        "Consider architectural review and refactoring",
                        "Implement design patterns for better maintainability",
                        "Plan for incremental improvements"
                    ],
                    prevention_strategies=[
                        "Regular architecture reviews",
                        "Continuous refactoring",
                        "Design pattern adoption"
                    ],
                    prediction_id=f"meta_arch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    created_at=datetime.now(),
                    model_version="meta_v1.0",
                    data_points_analyzed=len(base_predictions)
                )
                meta_predictions.append(architecture_prediction)
            
            # Meta-prediction: Maintenance burden
            total_severity_score = sum([
                {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(p.severity, 0)
                for p in base_predictions
            ])
            
            if total_severity_score > 6:
                maintenance_prediction = PredictionResult(
                    prediction_type=PredictionType.MAINTENANCE_BURDEN,
                    confidence=PredictionConfidence.HIGH,
                    probability=min(0.95, total_severity_score / 20),
                    timeline=timeline,
                    description="High maintenance burden expected due to multiple risk factors",
                    predicted_issues=["Increased maintenance effort", "Developer productivity decline"],
                    impact_areas=["Development velocity", "Team satisfaction", "Code quality"],
                    severity="high" if total_severity_score > 10 else "medium",
                    factors=[
                        f"High cumulative severity score ({total_severity_score})",
                        f"Multiple risk areas identified ({len(base_predictions)})",
                        "Cross-functional impact predicted"
                    ],
                    recommendations=[
                        "Prioritize preventive maintenance",
                        "Implement automated quality gates",
                        "Consider team training and tooling improvements"
                    ],
                    prevention_strategies=[
                        "Proactive code reviews",
                        "Automated testing expansion",
                        "Technical debt tracking"
                    ],
                    prediction_id=f"meta_maint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    created_at=datetime.now(),
                    model_version="meta_v1.0",
                    data_points_analyzed=len(base_predictions)
                )
                meta_predictions.append(maintenance_prediction)
            
            return meta_predictions
            
        except Exception as e:
            logger.error(f"Meta-prediction generation failed: {e}")
            return []
    
    def _rank_predictions(self, predictions: List[PredictionResult]) -> List[PredictionResult]:
        """Rank predictions by importance (confidence + impact + severity)."""
        def prediction_score(pred: PredictionResult) -> float:
            confidence_scores = {
                PredictionConfidence.VERY_LOW: 0.1,
                PredictionConfidence.LOW: 0.3,
                PredictionConfidence.MEDIUM: 0.5,
                PredictionConfidence.HIGH: 0.7,
                PredictionConfidence.VERY_HIGH: 0.9
            }
            
            severity_scores = {
                "low": 0.2,
                "medium": 0.5,
                "high": 0.8,
                "critical": 1.0
            }
            
            confidence_score = confidence_scores.get(pred.confidence, 0.5)
            severity_score = severity_scores.get(pred.severity, 0.5)
            probability_score = pred.probability
            
            # Weighted scoring
            return (confidence_score * 0.4 + severity_score * 0.4 + probability_score * 0.2)
        
        return sorted(predictions, key=prediction_score, reverse=True)
    
    async def analyze_prediction_accuracy(self, historical_predictions: List[Dict]) -> Dict[str, float]:
        """
        Analyze the accuracy of past predictions to improve future models.
        
        Args:
            historical_predictions: Past predictions with actual outcomes
            
        Returns:
            Accuracy metrics for each prediction type
        """
        accuracy_metrics = {}
        
        try:
            prediction_types = set(p.get("prediction_type") for p in historical_predictions)
            
            for pred_type in prediction_types:
                type_predictions = [p for p in historical_predictions if p.get("prediction_type") == pred_type]
                
                if len(type_predictions) < 5:  # Need minimum data points
                    continue
                
                correct_predictions = sum(1 for p in type_predictions if p.get("actual_outcome") == p.get("predicted_outcome"))
                accuracy = correct_predictions / len(type_predictions)
                
                accuracy_metrics[pred_type] = accuracy
            
            # Overall accuracy
            if accuracy_metrics:
                accuracy_metrics["overall"] = sum(accuracy_metrics.values()) / len(accuracy_metrics)
            
            return accuracy_metrics
            
        except Exception as e:
            logger.error(f"Accuracy analysis failed: {e}")
            return {}
    
    async def update_models_with_feedback(self, prediction_id: str, actual_outcome: Dict[str, Any]):
        """
        Update prediction models based on actual outcomes (reinforcement learning).
        
        Args:
            prediction_id: ID of the original prediction
            actual_outcome: What actually happened
        """
        try:
            # Store feedback for model improvement
            feedback_entry = {
                "prediction_id": prediction_id,
                "actual_outcome": actual_outcome,
                "feedback_timestamp": datetime.now().isoformat(),
                "model_version": "v1.0"
            }
            
            # In a real implementation, this would update ML models
            # For now, we store the feedback for future analysis
            self.historical_data.append(feedback_entry)
            
            # Limit historical data size
            max_history = self.config["prediction"]["historical_data_limit"]
            if len(self.historical_data) > max_history:
                self.historical_data = self.historical_data[-max_history:]
            
            logger.info(f"Stored feedback for prediction {prediction_id}")
            
        except Exception as e:
            logger.error(f"Model update failed: {e}")
    
    def get_prediction_insights(self, predictions: List[PredictionResult]) -> Dict[str, Any]:
        """
        Generate high-level insights from a set of predictions.
        
        Args:
            predictions: List of prediction results
            
        Returns:
            Summary insights and recommendations
        """
        if not predictions:
            return {"message": "No predictions available"}
        
        insights = {
            "summary": {
                "total_predictions": len(predictions),
                "high_confidence_count": len([p for p in predictions if p.confidence in [PredictionConfidence.HIGH, PredictionConfidence.VERY_HIGH]]),
                "critical_issues": len([p for p in predictions if p.severity == "critical"]),
                "average_probability": sum(p.probability for p in predictions) / len(predictions)
            },
            "top_concerns": [
                {
                    "type": pred.prediction_type.value,
                    "description": pred.description,
                    "probability": pred.probability,
                    "timeline": pred.timeline
                }
                for pred in predictions[:3]  # Top 3 predictions
            ],
            "recommended_actions": [],
            "prevention_strategies": []
        }
        
        # Collect unique recommendations and strategies
        all_recommendations = []
        all_strategies = []
        
        for pred in predictions:
            all_recommendations.extend(pred.recommendations)
            all_strategies.extend(pred.prevention_strategies)
        
        # Deduplicate and prioritize
        insights["recommended_actions"] = list(set(all_recommendations))[:5]
        insights["prevention_strategies"] = list(set(all_strategies))[:5]
        
        return insights


# Example usage
if __name__ == "__main__":
    async def main():
        predictor = PredictiveIntelligence()
        
        # Example project context
        project_context = {
            "project_type": "web-app",
            "languages": {"typescript": 80, "javascript": 20},
            "frameworks": {"react": 0.9, "express": 0.8},
            "health_metrics": {
                "code_quality": 0.75,
                "test_coverage": 0.60,
                "documentation": 0.50,
                "security": 0.85,
                "performance": 0.70
            },
            "complexity_metrics": {
                "cyclomatic_complexity": 2.5,
                "lines_of_code": 15000,
                "file_count": 120,
                "dependency_count": 45
            },
            "team_metrics": {
                "team_size": 5,
                "experience_level": "intermediate",
                "velocity": 0.8
            }
        }
        
        # Generate predictions
        predictions = await predictor.predict_project_future(project_context, "1month")
        
        print(f"Generated {len(predictions)} predictions:")
        for i, pred in enumerate(predictions, 1):
            print(f"\n{i}. {pred.prediction_type.value}")
            print(f"   Confidence: {pred.confidence.value}")
            print(f"   Probability: {pred.probability:.2f}")
            print(f"   Description: {pred.description}")
            print(f"   Severity: {pred.severity}")
        
        # Get insights
        insights = predictor.get_prediction_insights(predictions)
        print(f"\nInsights: {insights['summary']}")
    
    asyncio.run(main())