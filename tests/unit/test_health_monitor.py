"""
Unit tests for the Health Monitor.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from universal_ai_dev_platform.monitoring import HealthMonitor, HealthMetric, HealthCheck, Alert


class TestHealthMonitor:
    """Test suite for HealthMonitor."""
    
    @pytest.fixture
    def health_monitor(self):
        """Create a health monitor for testing."""
        return HealthMonitor()
    
    @pytest.fixture
    def sample_health_metric(self):
        """Sample health metric for testing."""
        return HealthMetric(
            name="cpu_usage",
            value=75.5,
            unit="%",
            timestamp=datetime.now(),
            tags={"host": "localhost"},
            threshold=80.0,
            status="healthy"
        )
    
    @pytest.fixture
    def sample_health_check(self):
        """Sample health check for testing."""
        mock_function = AsyncMock(return_value=True)
        return HealthCheck(
            name="test_check",
            check_function=mock_function,
            interval=60,
            timeout=30,
            enabled=True
        )
    
    @pytest.fixture
    def sample_alert(self):
        """Sample alert for testing."""
        return Alert(
            id="test_alert_001",
            name="High CPU Usage",
            severity="warning",
            message="CPU usage exceeded 80%",
            timestamp=datetime.now(),
            metadata={"cpu_value": 85.2}
        )
    
    def test_initialization(self, health_monitor):
        """Test health monitor initialization."""
        assert health_monitor.config is not None
        assert isinstance(health_monitor.metrics, dict)
        assert isinstance(health_monitor.health_checks, dict)
        assert isinstance(health_monitor.alerts, list)
        assert health_monitor.is_running is False
    
    def test_record_metric(self, health_monitor):
        """Test recording a health metric."""
        health_monitor.record_metric("test_metric", 42.0, "units", {"tag": "value"}, 50.0)
        
        assert "test_metric" in health_monitor.metrics
        metric = health_monitor.metrics["test_metric"]
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.unit == "units"
        assert metric.tags == {"tag": "value"}
        assert metric.threshold == 50.0
        assert metric.status == "healthy"  # Below threshold
    
    def test_record_metric_with_threshold_warning(self, health_monitor):
        """Test recording a metric that exceeds warning threshold."""
        health_monitor.record_metric("warning_metric", 85.0, "%", threshold=80.0)
        
        metric = health_monitor.metrics["warning_metric"]
        assert metric.status == "warning"
    
    def test_record_metric_with_threshold_critical(self, health_monitor):
        """Test recording a metric that exceeds critical threshold."""
        health_monitor.record_metric("critical_metric", 100.0, "%", threshold=80.0)
        
        metric = health_monitor.metrics["critical_metric"]
        assert metric.status == "critical"
    
    def test_add_health_check(self, health_monitor, sample_health_check):
        """Test adding a health check."""
        health_monitor.add_health_check(
            "test_check",
            sample_health_check.check_function,
            interval=60,
            timeout=30
        )
        
        assert "test_check" in health_monitor.health_checks
        check = health_monitor.health_checks["test_check"]
        assert check.name == "test_check"
        assert check.interval == 60
        assert check.timeout == 30
        assert check.enabled is True
    
    def test_create_alert(self, health_monitor):
        """Test creating an alert."""
        health_monitor.create_alert(
            "test_alert",
            "Test Alert",
            "warning",
            "This is a test alert",
            {"test": "metadata"}
        )
        
        assert len(health_monitor.alerts) == 1
        alert = health_monitor.alerts[0]
        assert alert.id == "test_alert"
        assert alert.name == "Test Alert"
        assert alert.severity == "warning"
        assert alert.message == "This is a test alert"
        assert alert.metadata == {"test": "metadata"}
        assert alert.resolved is False
    
    @pytest.mark.asyncio
    async def test_get_health_status(self, health_monitor):
        """Test getting overall health status."""
        # Add some metrics
        health_monitor.record_metric("cpu_usage", 50.0, "%", threshold=80.0)
        health_monitor.record_metric("memory_usage", 60.0, "%", threshold=85.0)
        
        # Add an alert
        health_monitor.create_alert("test", "Test Alert", "warning", "Test message")
        
        status = await health_monitor.get_health_status()
        
        assert isinstance(status, dict)
        assert "overall_health" in status
        assert "health_score" in status
        assert "timestamp" in status
        assert "monitoring_enabled" in status
        assert "recent_alerts" in status
        assert "key_metrics" in status
        assert "uptime" in status
        
        assert status["overall_health"] in ["healthy", "degraded", "unhealthy"]
        assert isinstance(status["health_score"], float)
        assert 0.0 <= status["health_score"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_health_check_execution(self, health_monitor):
        """Test health check execution."""
        check_function = AsyncMock(return_value=True)
        health_monitor.add_health_check("test_check", check_function, interval=1)
        
        # Manually run health checks
        await health_monitor._run_health_checks()
        
        check = health_monitor.health_checks["test_check"]
        assert check.last_run is not None
        assert check.last_result is True
        assert check.consecutive_failures == 0
        check_function.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, health_monitor):
        """Test health check failure handling."""
        check_function = AsyncMock(return_value=False)
        health_monitor.add_health_check("failing_check", check_function, interval=1)
        
        # Run health checks multiple times to trigger consecutive failures
        for _ in range(4):
            await health_monitor._run_health_checks()
        
        check = health_monitor.health_checks["failing_check"]
        assert check.consecutive_failures >= 3
        
        # Should have created an alert for consecutive failures
        failure_alerts = [alert for alert in health_monitor.alerts if "failing_check" in alert.id]
        assert len(failure_alerts) > 0
    
    @pytest.mark.asyncio
    async def test_health_check_timeout(self, health_monitor):
        """Test health check timeout handling."""
        async def slow_check():
            await asyncio.sleep(2)  # Longer than timeout
            return True
        
        health_monitor.add_health_check("slow_check", slow_check, interval=1, timeout=1)
        
        await health_monitor._run_health_checks()
        
        check = health_monitor.health_checks["slow_check"]
        assert check.consecutive_failures > 0  # Should have failed due to timeout
    
    @pytest.mark.asyncio
    async def test_system_resource_check(self, health_monitor):
        """Test system resource health check."""
        result = await health_monitor._check_system_resources()
        
        assert isinstance(result, bool)
        # Should return True unless system is really under stress
    
    @pytest.mark.asyncio
    async def test_disk_space_check(self, health_monitor):
        """Test disk space health check."""
        result = await health_monitor._check_disk_space()
        
        assert isinstance(result, bool)
        # Should return True unless disk is really full
    
    @pytest.mark.asyncio
    async def test_metrics_collection(self, health_monitor):
        """Test metrics collection."""
        with patch('psutil.cpu_percent', return_value=75.0), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk, \
             patch('psutil.net_io_counters') as mock_net, \
             patch('psutil.pids', return_value=list(range(100))):
            
            # Mock memory
            mock_memory.return_value.percent = 60.0
            
            # Mock disk
            mock_disk_obj = Mock()
            mock_disk_obj.total = 1000000000  # 1GB
            mock_disk_obj.used = 500000000    # 500MB
            mock_disk_obj.free = 500000000    # 500MB
            mock_disk.return_value = mock_disk_obj
            
            # Mock network
            mock_net_obj = Mock()
            mock_net_obj.bytes_sent = 1000000
            mock_net_obj.bytes_recv = 2000000
            mock_net.return_value = mock_net_obj
            
            await health_monitor._collect_system_metrics()
            
            # Check that metrics were recorded
            assert "cpu_usage_percent" in health_monitor.metrics
            assert "memory_usage_percent" in health_monitor.metrics
            assert "disk_usage_percent" in health_monitor.metrics
            assert "network_bytes_sent" in health_monitor.metrics
            assert "network_bytes_recv" in health_monitor.metrics
            assert "process_count" in health_monitor.metrics
    
    @pytest.mark.asyncio
    async def test_health_score_calculation(self, health_monitor):
        """Test health score calculation."""
        # Add healthy metrics
        health_monitor.record_metric("metric1", 50.0, "%", threshold=80.0)  # healthy
        health_monitor.record_metric("metric2", 85.0, "%", threshold=80.0)  # warning
        health_monitor.record_metric("metric3", 100.0, "%", threshold=80.0) # critical
        
        score = await health_monitor._calculate_health_score()
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        # With 1 healthy, 1 warning, 1 critical: (1.0 + 0.5 + 0.0) / 3 = 0.5
        assert abs(score - 0.5) < 0.1
    
    @pytest.mark.asyncio
    async def test_alert_processing(self, health_monitor, sample_alert):
        """Test alert processing."""
        health_monitor.alerts.append(sample_alert)
        
        with patch('builtins.print') as mock_print:
            await health_monitor._process_alert(sample_alert)
            mock_print.assert_called_once()
    
    def test_config_loading(self, temp_dir):
        """Test configuration loading."""
        # Create a test config file
        config_path = temp_dir / "test_monitoring.yml"
        config_content = """
global:
  enabled: true
  metrics_interval: 30
platform_health:
  system:
    enabled: true
    alerts:
      high_cpu:
        threshold: 90
        severity: warning
"""
        config_path.write_text(config_content)
        
        monitor = HealthMonitor(str(config_path))
        
        assert monitor.config["global"]["enabled"] is True
        assert monitor.config["global"]["metrics_interval"] == 30
        assert monitor.config["platform_health"]["system"]["alerts"]["high_cpu"]["threshold"] == 90
    
    def test_default_config(self, health_monitor):
        """Test default configuration."""
        config = health_monitor._default_config()
        
        assert isinstance(config, dict)
        assert "global" in config
        assert "platform_health" in config
        assert config["global"]["enabled"] is True
    
    def test_uptime_calculation(self, health_monitor):
        """Test uptime calculation."""
        uptime = health_monitor._get_uptime()
        
        assert isinstance(uptime, str)
        # Should be in format like "1:23:45" or "1 day, 2:34:56"
    
    @pytest.mark.asyncio
    async def test_alert_cleanup(self, health_monitor):
        """Test old alert cleanup."""
        # Add old alert
        old_alert = Alert(
            id="old_alert",
            name="Old Alert",
            severity="info",
            message="Old message",
            timestamp=datetime.now() - timedelta(days=10)
        )
        health_monitor.alerts.append(old_alert)
        
        # Add recent alert
        recent_alert = Alert(
            id="recent_alert",
            name="Recent Alert", 
            severity="info",
            message="Recent message",
            timestamp=datetime.now()
        )
        health_monitor.alerts.append(recent_alert)
        
        await health_monitor._process_pending_alerts()
        
        # Old alert should be removed, recent should remain
        alert_ids = [alert.id for alert in health_monitor.alerts]
        assert "old_alert" not in alert_ids
        assert "recent_alert" in alert_ids
    
    @pytest.mark.asyncio
    async def test_monitoring_lifecycle(self, health_monitor):
        """Test monitoring start/stop lifecycle."""
        assert health_monitor.is_running is False
        
        # Start monitoring (will run briefly)
        start_task = asyncio.create_task(health_monitor.start_monitoring())
        
        # Give it a moment to start
        await asyncio.sleep(0.1)
        assert health_monitor.is_running is True
        
        # Stop monitoring
        await health_monitor.stop_monitoring()
        
        # Cancel the monitoring task
        start_task.cancel()
        try:
            await start_task
        except asyncio.CancelledError:
            pass
        
        assert health_monitor.is_running is False