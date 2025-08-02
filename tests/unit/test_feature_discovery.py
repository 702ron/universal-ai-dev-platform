"""
Unit tests for the Feature Discovery Engine.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from universal_ai_dev_platform.core.adaptation import FeatureDiscoveryEngine, DiscoveredFeature


class TestFeatureDiscoveryEngine:
    """Test suite for FeatureDiscoveryEngine."""
    
    @pytest.fixture
    def discovery_engine(self):
        """Create a feature discovery engine for testing."""
        return FeatureDiscoveryEngine()
    
    @pytest.fixture
    def sample_feature(self):
        """Sample discovered feature."""
        return DiscoveredFeature(
            title="Advanced AI Model",
            description="New transformer architecture with improved efficiency",
            source="arxiv",
            url="https://arxiv.org/abs/2024.01234",
            category="machine-learning",
            tags=["transformer", "efficiency", "nlp"],
            discovered_at=datetime.now(),
            confidence_score=0.9,
            relevance_score=0.85
        )
    
    def test_initialization(self, discovery_engine):
        """Test feature discovery engine initialization."""
        assert discovery_engine.config is not None
        assert discovery_engine.monitoring_sources is not None
        assert discovery_engine.discovered_features == []
        assert discovery_engine.session is None
    
    @pytest.mark.asyncio
    async def test_start_monitoring(self, discovery_engine):
        """Test starting monitoring process."""
        with patch('aiohttp.ClientSession') as mock_session:
            await discovery_engine.start_monitoring()
            assert discovery_engine.session is not None
            mock_session.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_stop_monitoring(self, discovery_engine):
        """Test stopping monitoring process."""
        # Setup session
        discovery_engine.session = AsyncMock()
        
        await discovery_engine.stop_monitoring()
        
        discovery_engine.session.close.assert_called_once()
        assert discovery_engine.session is None
    
    @pytest.mark.asyncio
    async def test_discover_from_source_arxiv(self, discovery_engine):
        """Test discovering features from arXiv."""
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.text.return_value = """
        <entry>
            <title>Test Paper Title</title>
            <summary>Test paper summary about AI</summary>
            <id>http://arxiv.org/abs/2024.01234</id>
            <published>2024-01-01T00:00:00Z</published>
        </entry>
        """
        mock_session.get.return_value.__aenter__.return_value = mock_response
        discovery_engine.session = mock_session
        
        features = await discovery_engine._discover_from_arxiv()
        
        assert isinstance(features, list)
        # Would have more specific assertions based on actual implementation
    
    @pytest.mark.asyncio
    async def test_analyze_relevance(self, discovery_engine, sample_feature):
        """Test feature relevance analysis."""
        relevance = await discovery_engine._analyze_relevance(sample_feature)
        
        assert isinstance(relevance, float)
        assert 0.0 <= relevance <= 1.0
    
    @pytest.mark.asyncio
    async def test_calculate_confidence(self, discovery_engine, sample_feature):
        """Test confidence score calculation."""
        confidence = await discovery_engine._calculate_confidence(sample_feature)
        
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
    
    def test_add_discovered_feature(self, discovery_engine, sample_feature):
        """Test adding a discovered feature."""
        discovery_engine._add_discovered_feature(sample_feature)
        
        assert len(discovery_engine.discovered_features) == 1
        assert discovery_engine.discovered_features[0] == sample_feature
    
    @pytest.mark.asyncio
    async def test_get_recent_discoveries(self, discovery_engine, sample_feature):
        """Test getting recent discoveries."""
        # Add a recent feature
        discovery_engine._add_discovered_feature(sample_feature)
        
        # Add an old feature
        old_feature = DiscoveredFeature(
            title="Old Feature",
            description="An old feature",
            source="github",
            url="https://github.com/test/old",
            category="tools",
            tags=["old"],
            discovered_at=datetime.now() - timedelta(days=2),
            confidence_score=0.7,
            relevance_score=0.6
        )
        discovery_engine._add_discovered_feature(old_feature)
        
        recent_features = await discovery_engine.get_recent_discoveries(hours=24)
        
        assert len(recent_features) == 1
        assert recent_features[0] == sample_feature
    
    @pytest.mark.asyncio
    async def test_get_integration_candidates(self, discovery_engine, sample_feature):
        """Test getting integration candidates."""
        # Set up a high-confidence, high-relevance feature
        sample_feature.confidence_score = 0.9
        sample_feature.relevance_score = 0.9
        discovery_engine._add_discovered_feature(sample_feature)
        
        # Add a low-confidence feature
        low_confidence_feature = DiscoveredFeature(
            title="Low Confidence Feature",
            description="A feature with low confidence",
            source="blog",
            url="https://blog.example.com/feature",
            category="tools",
            tags=["experimental"],
            discovered_at=datetime.now(),
            confidence_score=0.3,
            relevance_score=0.5
        )
        discovery_engine._add_discovered_feature(low_confidence_feature)
        
        candidates = await discovery_engine.get_integration_candidates()
        
        assert len(candidates) >= 1
        assert sample_feature in candidates
        assert low_confidence_feature not in candidates
    
    def test_is_ai_related(self, discovery_engine):
        """Test AI relevance detection."""
        ai_text = "This paper introduces a new neural network architecture for natural language processing"
        non_ai_text = "This article discusses cooking recipes and kitchen techniques"
        
        assert discovery_engine._is_ai_related(ai_text) == True
        assert discovery_engine._is_ai_related(non_ai_text) == False
    
    def test_extract_features_from_text(self, discovery_engine):
        """Test feature extraction from text."""
        text = "This introduces machine learning, artificial intelligence, and neural networks for data science"
        
        features = discovery_engine._extract_features_from_text(text)
        
        assert isinstance(features, list)
        assert len(features) > 0
        assert any("machine learning" in feature for feature in features)
    
    @pytest.mark.asyncio
    async def test_monitoring_sources_configuration(self, discovery_engine):
        """Test monitoring sources configuration."""
        sources = discovery_engine._initialize_sources()
        
        assert isinstance(sources, dict)
        assert "arxiv" in sources
        assert "github" in sources
        assert "anthropic" in sources
        
        # Test source configuration structure
        for source_name, source_config in sources.items():
            assert "url" in source_config
            assert "enabled" in source_config
            assert "frequency" in source_config
    
    @pytest.mark.asyncio
    async def test_error_handling_in_discovery(self, discovery_engine):
        """Test error handling during discovery process."""
        # Mock a session that raises an exception
        mock_session = AsyncMock()
        mock_session.get.side_effect = Exception("Network error")
        discovery_engine.session = mock_session
        
        # Discovery should handle errors gracefully
        features = await discovery_engine._discover_from_arxiv()
        
        assert isinstance(features, list)
        assert len(features) == 0  # Should return empty list on error
    
    def test_feature_deduplication(self, discovery_engine):
        """Test that duplicate features are not added."""
        feature1 = DiscoveredFeature(
            title="Test Feature",
            description="A test feature",
            source="test",
            url="https://test.com/feature1",
            category="test",
            tags=["test"],
            discovered_at=datetime.now(),
            confidence_score=0.8,
            relevance_score=0.7
        )
        
        feature2 = DiscoveredFeature(
            title="Test Feature",  # Same title
            description="A test feature",  # Same description
            source="test",
            url="https://test.com/feature2",  # Different URL
            category="test",
            tags=["test"],
            discovered_at=datetime.now(),
            confidence_score=0.8,
            relevance_score=0.7
        )
        
        discovery_engine._add_discovered_feature(feature1)
        discovery_engine._add_discovered_feature(feature2)
        
        # Should only have one feature due to deduplication
        assert len(discovery_engine.discovered_features) == 1
    
    @pytest.mark.asyncio
    async def test_batch_processing(self, discovery_engine):
        """Test batch processing of discovered features."""
        features = []
        for i in range(10):
            feature = DiscoveredFeature(
                title=f"Feature {i}",
                description=f"Description {i}",
                source="test",
                url=f"https://test.com/feature{i}",
                category="test",
                tags=["test"],
                discovered_at=datetime.now(),
                confidence_score=0.8,
                relevance_score=0.7
            )
            features.append(feature)
        
        await discovery_engine._process_features_batch(features)
        
        assert len(discovery_engine.discovered_features) == 10
    
    def test_config_validation(self, discovery_engine):
        """Test configuration validation."""
        # Test default config
        config = discovery_engine._default_config()
        
        assert "feature_discovery" in config
        assert "monitoring_sources" in config["feature_discovery"]
        assert "max_concurrent_requests" in config["feature_discovery"]
        assert "discovery_frequency" in config["feature_discovery"]
        
        # Test config validation
        assert discovery_engine._validate_config(config) == True
        
        # Test invalid config
        invalid_config = {"invalid": "config"}
        assert discovery_engine._validate_config(invalid_config) == False