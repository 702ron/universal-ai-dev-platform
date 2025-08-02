"""
Health Monitor

System health monitoring and alerting for the Universal AI Development Platform.
Monitors platform health, adaptation processes, and user experience metrics.
"""

import asyncio
import logging
import psutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


@dataclass
class HealthMetric:
    """Individual health metric."""
    
    name: str
    value: float
    unit: str
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    threshold: Optional[float] = None
    status: str = "healthy"  # healthy, warning, critical


@dataclass
class HealthCheck:
    """Health check definition."""
    
    name: str
    check_function: Callable
    interval: int  # seconds
    timeout: int = 30
    enabled: bool = True
    last_run: Optional[datetime] = None
    last_result: Optional[bool] = None
    consecutive_failures: int = 0


@dataclass
class Alert:
    """Alert definition."""
    
    id: str
    name: str
    severity: str
    message: str
    timestamp: datetime
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class HealthMonitor:
    """
    Comprehensive health monitoring system for the Universal AI Development Platform.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.metrics: Dict[str, HealthMetric] = {}
        self.health_checks: Dict[str, HealthCheck] = {}
        self.alerts: List[Alert] = []
        self.is_running = False
        self._setup_health_checks()
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load monitoring configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent.parent / "config" / "monitoring.yml"
        
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load monitoring config: {e}. Using defaults.")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default monitoring configuration."""
        return {
            "global": {
                "enabled": True,
                "metrics_interval": 60,
                "health_check_interval": 30
            },
            "platform_health": {
                "system": {
                    "enabled": True,
                    "alerts": {
                        "high_cpu": {"threshold": 80, "severity": "warning"},
                        "high_memory": {"threshold": 85, "severity": "warning"},
                        "low_disk_space": {"threshold": 90, "severity": "error"}
                    }
                },
                "application": {
                    "enabled": True,
                    "alerts": {
                        "high_error_rate": {"threshold": 0.05, "severity": "error"}
                    }
                }
            }
        }
    
    def _setup_health_checks(self):
        """Setup default health checks."""
        # System health checks
        self.add_health_check(
            "system_resources",
            self._check_system_resources,
            interval=self.config.get("global", {}).get("metrics_interval", 60)
        )
        
        self.add_health_check(
            "disk_space",
            self._check_disk_space,
            interval=300  # 5 minutes
        )
        
        # Application health checks
        self.add_health_check(
            "feature_discovery",
            self._check_feature_discovery,
            interval=600  # 10 minutes
        )
        
        self.add_health_check(
            "agent_orchestration",
            self._check_agent_orchestration,
            interval=180  # 3 minutes
        )
    
    async def start_monitoring(self):
        """Start the health monitoring system."""
        if self.is_running:
            logger.warning("Health monitor already running")
            return
        
        self.is_running = True
        logger.info("Starting health monitoring system...")
        
        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._metrics_collection_loop()),
            asyncio.create_task(self._health_check_loop()),
            asyncio.create_task(self._alert_processing_loop())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Health monitoring error: {e}")
        finally:
            self.is_running = False
    
    async def stop_monitoring(self):
        """Stop the health monitoring system."""
        logger.info("Stopping health monitoring system...")
        self.is_running = False
    
    def add_health_check(self, name: str, check_function: Callable, 
                        interval: int = 60, timeout: int = 30, enabled: bool = True):
        """Add a new health check."""
        self.health_checks[name] = HealthCheck(
            name=name,
            check_function=check_function,
            interval=interval,
            timeout=timeout,
            enabled=enabled
        )
        logger.debug(f"Added health check: {name}")
    
    def record_metric(self, name: str, value: float, unit: str = "", 
                     tags: Optional[Dict[str, str]] = None, threshold: Optional[float] = None):
        """Record a health metric."""
        metric = HealthMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            tags=tags or {},
            threshold=threshold
        )
        
        # Determine status based on threshold
        if threshold is not None:
            if value > threshold:
                metric.status = "warning" if value < threshold * 1.2 else "critical"
        
        self.metrics[name] = metric
        logger.debug(f"Recorded metric: {name} = {value} {unit}")
    
    def create_alert(self, alert_id: str, name: str, severity: str, 
                    message: str, metadata: Optional[Dict[str, Any]] = None):
        """Create a new alert."""
        alert = Alert(
            id=alert_id,
            name=name,
            severity=severity,
            message=message,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        self.alerts.append(alert)
        logger.warning(f"Alert created: {severity.upper()} - {message}")
        
        # Process alert through channels
        asyncio.create_task(self._process_alert(alert))
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status."""
        now = datetime.now()
        
        # Calculate overall health score
        health_score = await self._calculate_health_score()
        
        # Get recent alerts
        recent_alerts = [
            {
                "id": alert.id,
                "name": alert.name,
                "severity": alert.severity,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "resolved": alert.resolved
            }
            for alert in self.alerts[-10:]  # Last 10 alerts
        ]
        
        # Get health check statuses
        health_checks_status = {}
        for name, check in self.health_checks.items():
            health_checks_status[name] = {
                "enabled": check.enabled,
                "last_run": check.last_run.isoformat() if check.last_run else None,
                "last_result": check.last_result,
                "consecutive_failures": check.consecutive_failures
            }
        
        # Get key metrics
        key_metrics = {}
        for name, metric in self.metrics.items():
            key_metrics[name] = {
                "value": metric.value,
                "unit": metric.unit,
                "status": metric.status,
                "timestamp": metric.timestamp.isoformat()
            }
        
        return {
            "overall_health": "healthy" if health_score > 0.8 else "degraded" if health_score > 0.6 else "unhealthy",
            "health_score": health_score,
            "timestamp": now.isoformat(),
            "monitoring_enabled": self.is_running,
            "recent_alerts": recent_alerts,
            "health_checks": health_checks_status,
            "key_metrics": key_metrics,
            "uptime": self._get_uptime()
        }
    
    async def _metrics_collection_loop(self):
        """Main metrics collection loop."""
        interval = self.config.get("global", {}).get("metrics_interval", 60)
        
        while self.is_running:
            try:
                await self._collect_system_metrics()
                await self._collect_application_metrics()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(interval)
    
    async def _health_check_loop(self):
        """Health check execution loop."""
        while self.is_running:
            try:
                await self._run_health_checks()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(30)
    
    async def _alert_processing_loop(self):
        """Alert processing loop."""
        while self.is_running:
            try:
                await self._process_pending_alerts()
                await asyncio.sleep(10)  # Process alerts every 10 seconds
            except Exception as e:
                logger.error(f"Alert processing error: {e}")
                await asyncio.sleep(10)
    
    async def _collect_system_metrics(self):
        """Collect system resource metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric("cpu_usage_percent", cpu_percent, "%", 
                             threshold=self.config.get("platform_health", {})
                             .get("system", {}).get("alerts", {})
                             .get("high_cpu", {}).get("threshold", 80))
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.record_metric("memory_usage_percent", memory.percent, "%",
                             threshold=self.config.get("platform_health", {})
                             .get("system", {}).get("alerts", {})
                             .get("high_memory", {}).get("threshold", 85))
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.record_metric("disk_usage_percent", disk_percent, "%",
                             threshold=self.config.get("platform_health", {})
                             .get("system", {}).get("alerts", {})
                             .get("low_disk_space", {}).get("threshold", 90))
            
            # Network I/O
            network = psutil.net_io_counters()
            self.record_metric("network_bytes_sent", network.bytes_sent, "bytes")
            self.record_metric("network_bytes_recv", network.bytes_recv, "bytes")
            
            # Process count
            process_count = len(psutil.pids())
            self.record_metric("process_count", process_count, "count")
            
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")
    
    async def _collect_application_metrics(self):
        """Collect application-specific metrics."""
        try:
            # These would be populated by the actual application components
            # For now, we'll set placeholder values
            
            self.record_metric("feature_discoveries_24h", 0, "count")
            self.record_metric("agent_executions_count", 0, "count")
            self.record_metric("project_analyses_count", 0, "count")
            self.record_metric("api_requests_count", 0, "count")
            self.record_metric("error_rate", 0.0, "rate")
            
        except Exception as e:
            logger.error(f"Application metrics collection failed: {e}")
    
    async def _run_health_checks(self):
        """Run all enabled health checks."""
        now = datetime.now()
        
        for name, check in self.health_checks.items():
            if not check.enabled:
                continue
            
            # Check if it's time to run this check
            if check.last_run and (now - check.last_run).total_seconds() < check.interval:
                continue
            
            try:
                # Run the health check with timeout
                result = await asyncio.wait_for(
                    check.check_function(), 
                    timeout=check.timeout
                )
                
                check.last_run = now
                check.last_result = result
                
                if result:
                    check.consecutive_failures = 0
                else:
                    check.consecutive_failures += 1
                    
                    # Create alert for consecutive failures
                    if check.consecutive_failures >= 3:
                        self.create_alert(
                            f"health_check_{name}",
                            f"Health Check Failed: {name}",
                            "error",
                            f"Health check '{name}' failed {check.consecutive_failures} times consecutively"
                        )
                
            except asyncio.TimeoutError:
                logger.warning(f"Health check '{name}' timed out")
                check.consecutive_failures += 1
            except Exception as e:
                logger.error(f"Health check '{name}' error: {e}")
                check.consecutive_failures += 1
    
    async def _check_system_resources(self) -> bool:
        """Check system resource availability."""
        try:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
            
            # System is healthy if all resources are below critical thresholds
            return cpu_percent < 95 and memory_percent < 95 and disk_percent < 95
        except Exception:
            return False
    
    async def _check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            disk = psutil.disk_usage('/')
            free_percent = (disk.free / disk.total) * 100
            return free_percent > 10  # At least 10% free space
        except Exception:
            return False
    
    async def _check_feature_discovery(self) -> bool:
        """Check feature discovery system health."""
        # TODO: Implement actual feature discovery health check
        # This would check if the discovery engine is running and responsive
        return True
    
    async def _check_agent_orchestration(self) -> bool:
        """Check agent orchestration system health."""
        # TODO: Implement actual agent orchestration health check
        # This would check if agents are responsive and not stuck
        return True
    
    async def _calculate_health_score(self) -> float:
        """Calculate overall health score (0.0 to 1.0)."""
        if not self.metrics:
            return 1.0
        
        total_score = 0.0
        metric_count = 0
        
        for metric in self.metrics.values():
            if metric.threshold is None:
                continue
            
            metric_count += 1
            if metric.status == "healthy":
                total_score += 1.0
            elif metric.status == "warning":
                total_score += 0.5
            else:  # critical
                total_score += 0.0
        
        return total_score / metric_count if metric_count > 0 else 1.0
    
    async def _process_alert(self, alert: Alert):
        """Process a single alert through configured channels."""
        try:
            # Console output
            if self.config.get("alerting", {}).get("channels", {}).get("console", {}).get("enabled", True):
                print(f"[{alert.severity.upper()}] {alert.message}")
            
            # File output
            file_config = self.config.get("alerting", {}).get("channels", {}).get("file", {})
            if file_config.get("enabled", False):
                log_path = Path(file_config.get("path", "logs/alerts.log"))
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(log_path, 'a') as f:
                    f.write(f"[{alert.timestamp.isoformat()}] {alert.severity}: {alert.message}\\n")
            
        except Exception as e:
            logger.error(f"Alert processing failed: {e}")
    
    async def _process_pending_alerts(self):
        """Process any pending alerts."""
        # Clean up old resolved alerts
        cutoff_time = datetime.now() - timedelta(days=7)
        self.alerts = [alert for alert in self.alerts if alert.timestamp > cutoff_time]
    
    def _get_uptime(self) -> str:
        """Get system uptime."""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_timedelta = timedelta(seconds=uptime_seconds)
            return str(uptime_timedelta).split('.')[0]  # Remove microseconds
        except Exception:
            return "unknown"


# Example usage
if __name__ == "__main__":
    async def main():
        monitor = HealthMonitor()
        
        # Get current health status
        status = await monitor.get_health_status()
        print("Health Status:")
        print(f"- Overall Health: {status['overall_health']}")
        print(f"- Health Score: {status['health_score']:.2f}")
        print(f"- Uptime: {status['uptime']}")
        
        # Start monitoring (would run continuously in production)
        # await monitor.start_monitoring()
    
    asyncio.run(main())