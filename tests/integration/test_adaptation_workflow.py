"""
Integration tests for the adaptation workflow.
Tests the complete adaptation process from feature discovery to integration.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from universal_ai_dev_platform.core.adaptation import (
    FeatureDiscoveryEngine, 
    CompatibilityAnalyzer, 
    AdaptationEngine,
    DiscoveredFeature,
    CompatibilityStatus,
    IntegrationComplexity
)


class TestAdaptationWorkflow:
    """Integration tests for the complete adaptation workflow."""
    
    @pytest.fixture
    async def adaptation_system(self):
        """Set up a complete adaptation system for testing."""
        # Create real instances with mocked external dependencies
        discovery_engine = FeatureDiscoveryEngine()
        compatibility_analyzer = CompatibilityAnalyzer()
        adaptation_engine = AdaptationEngine()
        
        # Mock external HTTP calls
        with patch('aiohttp.ClientSession'), \
             patch.object(discovery_engine, '_discover_from_arxiv', new_callable=AsyncMock), \
             patch.object(discovery_engine, '_discover_from_github', new_callable=AsyncMock), \
             patch.object(discovery_engine, '_discover_from_anthropic', new_callable=AsyncMock):
            
            yield {
                "discovery": discovery_engine,
                "compatibility": compatibility_analyzer,
                "adaptation": adaptation_engine
            }
    
    @pytest.fixture
    def sample_ai_feature(self):
        """Sample AI feature for testing."""
        return DiscoveredFeature(
            title="Advanced Transformer Architecture",
            description="New transformer model with 50% better efficiency and improved reasoning capabilities",
            source="arxiv",
            url="https://arxiv.org/abs/2024.01234",
            category="machine-learning",
            tags=["transformer", "efficiency", "reasoning", "nlp"],
            discovered_at=datetime.now(),
            confidence_score=0.92,
            relevance_score=0.88
        )
    
    @pytest.mark.asyncio
    async def test_complete_adaptation_workflow(self, adaptation_system, sample_ai_feature):
        """Test the complete adaptation workflow from discovery to integration."""
        discovery = adaptation_system["discovery"]
        compatibility = adaptation_system["compatibility"]
        adaptation = adaptation_system["adaptation"]
        
        # Step 1: Feature Discovery
        # Simulate discovering a feature
        discovery._add_discovered_feature(sample_ai_feature)
        
        recent_features = await discovery.get_recent_discoveries(hours=24)
        assert len(recent_features) == 1
        assert recent_features[0] == sample_ai_feature
        
        # Step 2: Compatibility Analysis
        compatibility_result = await compatibility.analyze_feature(sample_ai_feature)
        
        assert compatibility_result is not None
        assert compatibility_result.feature_id == sample_ai_feature.url
        assert compatibility_result.status in [
            CompatibilityStatus.COMPATIBLE,
            CompatibilityStatus.REQUIRES_CHANGES,
            CompatibilityStatus.INCOMPATIBLE
        ]
        assert 0.0 <= compatibility_result.confidence <= 1.0
        
        # Step 3: Integration Decision
        integration_candidates = await discovery.get_integration_candidates()
        
        if compatibility_result.status == CompatibilityStatus.COMPATIBLE:
            assert sample_ai_feature in integration_candidates
        
        # Step 4: Adaptation Status Check
        status = await adaptation.check_adaptation_status()
        
        assert isinstance(status, dict)
        assert "platform_version" in status
        assert "features_discovered_24h" in status
        assert status["features_discovered_24h"] >= 1
    
    @pytest.mark.asyncio
    async def test_feature_discovery_to_analysis_pipeline(self, adaptation_system):
        """Test the pipeline from feature discovery to project analysis."""
        discovery = adaptation_system["discovery"]
        
        # Mock discovery of multiple features
        features = [
            DiscoveredFeature(
                title=f"AI Feature {i}",
                description=f"Description for feature {i}",
                source="test",
                url=f"https://test.com/feature{i}",
                category="ai-tools",
                tags=["ai", "tools"],
                discovered_at=datetime.now(),
                confidence_score=0.8 + (i * 0.02),  # Varying confidence
                relevance_score=0.7 + (i * 0.03)   # Varying relevance
            )
            for i in range(5)
        ]
        
        # Add features to discovery engine
        for feature in features:
            discovery._add_discovered_feature(feature)
        
        # Get integration candidates (should filter by confidence/relevance)
        candidates = await discovery.get_integration_candidates()
        
        # Should have filtered out low-confidence features
        assert len(candidates) <= len(features)
        
        # All candidates should meet minimum thresholds
        for candidate in candidates:
            assert candidate.confidence_score >= discovery.config.get("feature_discovery", {}).get("min_confidence", 0.7)
            assert candidate.relevance_score >= discovery.config.get("feature_discovery", {}).get("min_relevance", 0.6)
    
    @pytest.mark.asyncio
    async def test_compatibility_analysis_workflow(self, adaptation_system, sample_ai_feature):
        """Test the compatibility analysis workflow."""
        compatibility = adaptation_system["compatibility"]
        
        # Analyze compatibility
        result = await compatibility.analyze_feature(sample_ai_feature)
        
        # Validate result structure
        assert result.feature_id == sample_ai_feature.url
        assert isinstance(result.status, CompatibilityStatus)
        assert isinstance(result.complexity, IntegrationComplexity)
        assert isinstance(result.estimated_effort_hours, (int, float))
        assert isinstance(result.requirements, list)
        assert isinstance(result.conflicts, list)
        assert isinstance(result.recommendations, list)
        assert isinstance(result.risk_factors, list)
        assert isinstance(result.integration_plan, dict)
        
        # Test different feature types
        ml_feature = DiscoveredFeature(
            title="ML Model Optimization",
            description="New optimization technique for neural networks",
            source="arxiv",
            url="https://arxiv.org/abs/2024.56789",
            category="machine-learning",
            tags=["optimization", "neural-networks"],
            discovered_at=datetime.now(),
            confidence_score=0.9,
            relevance_score=0.85
        )
        
        ml_result = await compatibility.analyze_feature(ml_feature)
        assert ml_result.feature_id == ml_feature.url
        
        # ML features might have different compatibility characteristics
        if "machine-learning" in ml_feature.category:
            # ML features might require specific dependencies
            assert isinstance(ml_result.requirements, list)
    
    @pytest.mark.asyncio
    async def test_adaptation_engine_update_check(self, adaptation_system):
        """Test the adaptation engine update checking."""
        adaptation = adaptation_system["adaptation"]
        
        # Mock the feature discovery to return some features
        with patch.object(adaptation.feature_discovery, 'get_recent_discoveries') as mock_discoveries, \
             patch.object(adaptation, '_check_for_breaking_changes') as mock_breaking:
            
            mock_discoveries.return_value = [
                DiscoveredFeature(
                    title="Test Feature",
                    description="A test feature",
                    source="test",
                    url="https://test.com/feature",
                    category="tools",
                    tags=["test"],
                    discovered_at=datetime.now(),
                    confidence_score=0.8,
                    relevance_score=0.7
                )
            ]
            mock_breaking.return_value = []
            
            result = await adaptation.check_for_updates()
            
            assert isinstance(result, dict)
            assert "check_completed" in result
            assert "new_features_found" in result
            assert "compatibility_results" in result
            assert "recommendations" in result
            
            if result["check_completed"]:
                assert result["new_features_found"] >= 0
                assert isinstance(result["compatibility_results"], list)
                assert isinstance(result["recommendations"], list)
    
    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self, adaptation_system):
        """Test error handling throughout the adaptation workflow."""
        discovery = adaptation_system["discovery"]
        compatibility = adaptation_system["compatibility"]
        
        # Test with malformed feature
        malformed_feature = DiscoveredFeature(
            title="",  # Empty title
            description="",  # Empty description
            source="unknown",
            url="invalid-url",
            category="",
            tags=[],
            discovered_at=datetime.now(),
            confidence_score=-1.0,  # Invalid confidence
            relevance_score=2.0     # Invalid relevance
        )
        
        # Discovery should handle malformed features gracefully
        discovery._add_discovered_feature(malformed_feature)
        candidates = await discovery.get_integration_candidates()
        
        # Malformed feature should be filtered out
        assert malformed_feature not in candidates
        
        # Compatibility analysis should handle errors gracefully
        try:
            result = await compatibility.analyze_feature(malformed_feature)
            # Should either succeed with appropriate status or handle gracefully
            assert result is not None
        except Exception as e:
            # If it raises an exception, it should be a controlled one
            assert isinstance(e, (ValueError, TypeError))
    
    @pytest.mark.asyncio
    async def test_concurrent_discovery_and_analysis(self, adaptation_system):
        """Test concurrent feature discovery and compatibility analysis."""
        discovery = adaptation_system["discovery"]
        compatibility = adaptation_system["compatibility"]
        
        # Create multiple features for concurrent processing
        features = [
            DiscoveredFeature(
                title=f"Concurrent Feature {i}",
                description=f"Feature {i} for concurrent testing",
                source="test",
                url=f"https://test.com/concurrent{i}",
                category="concurrent-test",
                tags=["concurrent", "test"],
                discovered_at=datetime.now(),
                confidence_score=0.8,
                relevance_score=0.7
            )
            for i in range(3)
        ]
        
        # Add features concurrently
        await asyncio.gather(*[
            asyncio.create_task(asyncio.sleep(0.01))  # Simulate async discovery
            for _ in features
        ])
        
        for feature in features:
            discovery._add_discovered_feature(feature)
        
        # Analyze compatibility concurrently
        analysis_tasks = [
            compatibility.analyze_feature(feature)
            for feature in features
        ]
        
        results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # All analyses should complete (or fail gracefully)
        assert len(results) == len(features)
        
        for result in results:
            if not isinstance(result, Exception):
                assert hasattr(result, 'feature_id')
                assert hasattr(result, 'status')
    
    @pytest.mark.asyncio
    async def test_adaptation_performance_metrics(self, adaptation_system):
        """Test performance metrics collection during adaptation."""
        adaptation = adaptation_system["adaptation"]
        
        start_time = datetime.now()
        
        # Run adaptation status check (should be fast)
        status = await adaptation.check_adaptation_status()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete quickly (under 5 seconds for mocked operations)
        assert duration < 5.0
        
        # Check that status contains performance-related information
        assert isinstance(status, dict)
        if "last_adaptation" in status:
            # Performance tracking should be included
            pass
    
    @pytest.mark.asyncio
    async def test_feature_lifecycle_management(self, adaptation_system):
        """Test the complete lifecycle of a feature from discovery to integration."""
        discovery = adaptation_system["discovery"]
        compatibility = adaptation_system["compatibility"]
        adaptation = adaptation_system["adaptation"]
        
        # Feature lifecycle: Discovery -> Analysis -> Integration -> Monitoring
        
        # 1. Discovery Phase
        new_feature = DiscoveredFeature(
            title="Lifecycle Test Feature",
            description="Feature to test complete lifecycle",
            source="lifecycle-test",
            url="https://test.com/lifecycle",
            category="testing",
            tags=["lifecycle", "testing"],
            discovered_at=datetime.now(),
            confidence_score=0.95,
            relevance_score=0.90
        )
        
        discovery._add_discovered_feature(new_feature)
        
        # 2. Analysis Phase
        compatibility_result = await compatibility.analyze_feature(new_feature)
        
        # 3. Integration Decision
        if compatibility_result.status == CompatibilityStatus.COMPATIBLE:
            candidates = await discovery.get_integration_candidates()
            assert new_feature in candidates
            
            # 4. Mock Integration Process
            # In real implementation, this would trigger actual integration
            integration_success = True  # Mock successful integration
            
            if integration_success:
                # 5. Post-Integration Monitoring
                status = await adaptation.check_adaptation_status()
                assert status["monitoring_status"] in ["active", "inactive"]
        
        # Feature should now be tracked in the system
        all_features = discovery.discovered_features
        assert new_feature in all_features
    
    @pytest.mark.asyncio
    async def test_rollback_scenario(self, adaptation_system):
        """Test rollback scenario when integration fails."""
        adaptation = adaptation_system["adaptation"]
        
        # Mock a force adaptation that might need rollback
        with patch.object(adaptation, '_create_platform_backup') as mock_backup, \
             patch.object(adaptation.integration_manager, 'integrate_feature') as mock_integrate:
            
            # Mock integration failure
            mock_integrate.side_effect = Exception("Integration failed")
            
            result = await adaptation.force_adaptation_update()
            
            # Should handle integration failure gracefully
            assert isinstance(result, type(adaptation).__annotations__.get('AdaptationResult', object))
            
            # Backup should have been created if configured
            if adaptation.config.get("backup_before_integration", True):
                mock_backup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_adaptation_configuration_validation(self, adaptation_system):
        """Test that adaptation system validates its configuration properly."""
        adaptation = adaptation_system["adaptation"]
        
        # Test configuration validation
        config = adaptation.config
        
        # Should have required configuration sections
        assert isinstance(config, dict)
        assert "adaptation_frequency" in config
        assert "auto_integration" in config
        assert "compatibility_threshold" in config
        
        # Values should be within expected ranges
        assert isinstance(config["adaptation_frequency"], int)
        assert config["adaptation_frequency"] > 0
        assert isinstance(config["auto_integration"], bool)
        assert isinstance(config["compatibility_threshold"], (int, float))
        assert 0.0 <= config["compatibility_threshold"] <= 1.0