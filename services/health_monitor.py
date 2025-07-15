#!/usr/bin/env python3
"""
Health Monitoring Service for Warhammer Fantasy Tavern Simulator
Provides comprehensive system health checks and monitoring capabilities
"""

import time
import psutil
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@dataclass
class HealthMetrics:
    """System health metrics"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_usage_percent: float
    uptime_seconds: float
    active_agents: int
    transaction_rate: float
    error_rate: float
    response_time_ms: float

class HealthMonitor:
    """Comprehensive health monitoring for the tavern simulator"""
    
    def __init__(self):
        self.start_time = time.time()
        self.transaction_count = 0
        self.error_count = 0
        self.response_times = []
        self.logger = logger.bind(component="health_monitor")
        
    def get_system_metrics(self) -> HealthMetrics:
        """Get current system health metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Application metrics
            uptime = time.time() - self.start_time
            avg_response_time = sum(self.response_times[-100:]) / len(self.response_times[-100:]) if self.response_times else 0
            transaction_rate = self.transaction_count / uptime if uptime > 0 else 0
            error_rate = self.error_count / max(self.transaction_count, 1) * 100
            
            metrics = HealthMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available_mb=memory.available / 1024 / 1024,
                disk_usage_percent=disk.percent,
                uptime_seconds=uptime,
                active_agents=18,  # Our 18-agent system
                transaction_rate=transaction_rate,
                error_rate=error_rate,
                response_time_ms=avg_response_time * 1000
            )
            
            self.logger.info("Health metrics collected", metrics=metrics.__dict__)
            return metrics
            
        except Exception as e:
            self.logger.error("Failed to collect health metrics", error=str(e))
            raise
    
    def record_transaction(self, success: bool = True, response_time: float = 0):
        """Record a transaction for metrics"""
        self.transaction_count += 1
        if not success:
            self.error_count += 1
        if response_time > 0:
            self.response_times.append(response_time)
            # Keep only last 1000 response times
            if len(self.response_times) > 1000:
                self.response_times = self.response_times[-1000:]
    
    def check_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        try:
            start_time = time.time()
            
            # Get system metrics
            metrics = self.get_system_metrics()
            
            # Determine health status
            health_issues = []
            
            if metrics.cpu_percent > 80:
                health_issues.append("High CPU usage")
            
            if metrics.memory_percent > 85:
                health_issues.append("High memory usage")
            
            if metrics.disk_usage_percent > 90:
                health_issues.append("High disk usage")
            
            if metrics.error_rate > 5:
                health_issues.append("High error rate")
            
            if metrics.response_time_ms > 1000:
                health_issues.append("Slow response times")
            
            # Overall status
            if not health_issues:
                status = "healthy"
                status_code = 200
            elif len(health_issues) <= 2:
                status = "degraded"
                status_code = 200
            else:
                status = "unhealthy"
                status_code = 503
            
            check_duration = time.time() - start_time
            
            health_report = {
                "status": status,
                "status_code": status_code,
                "timestamp": metrics.timestamp,
                "uptime_seconds": metrics.uptime_seconds,
                "check_duration_ms": check_duration * 1000,
                "metrics": metrics.__dict__,
                "issues": health_issues,
                "version": "1.0.0",
                "service": "warhammer-tavern-simulator"
            }
            
            self.logger.info("Health check completed", 
                           status=status, 
                           issues_count=len(health_issues),
                           check_duration_ms=check_duration * 1000)
            
            return health_report
            
        except Exception as e:
            self.logger.error("Health check failed", error=str(e))
            return {
                "status": "error",
                "status_code": 500,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "service": "warhammer-tavern-simulator"
            }
    
    def get_prometheus_metrics(self) -> str:
        """Generate Prometheus-compatible metrics"""
        try:
            metrics = self.get_system_metrics()
            
            prometheus_metrics = f"""# HELP tavern_cpu_percent CPU usage percentage
# TYPE tavern_cpu_percent gauge
tavern_cpu_percent {metrics.cpu_percent}

# HELP tavern_memory_percent Memory usage percentage
# TYPE tavern_memory_percent gauge
tavern_memory_percent {metrics.memory_percent}

# HELP tavern_uptime_seconds Application uptime in seconds
# TYPE tavern_uptime_seconds counter
tavern_uptime_seconds {metrics.uptime_seconds}

# HELP tavern_active_agents Number of active agents
# TYPE tavern_active_agents gauge
tavern_active_agents {metrics.active_agents}

# HELP tavern_transaction_rate Transactions per second
# TYPE tavern_transaction_rate gauge
tavern_transaction_rate {metrics.transaction_rate}

# HELP tavern_error_rate Error rate percentage
# TYPE tavern_error_rate gauge
tavern_error_rate {metrics.error_rate}

# HELP tavern_response_time_ms Average response time in milliseconds
# TYPE tavern_response_time_ms gauge
tavern_response_time_ms {metrics.response_time_ms}

# HELP tavern_transactions_total Total number of transactions
# TYPE tavern_transactions_total counter
tavern_transactions_total {self.transaction_count}

# HELP tavern_errors_total Total number of errors
# TYPE tavern_errors_total counter
tavern_errors_total {self.error_count}
"""
            
            return prometheus_metrics
            
        except Exception as e:
            self.logger.error("Failed to generate Prometheus metrics", error=str(e))
            return f"# Error generating metrics: {str(e)}\n"

# Global health monitor instance
health_monitor = HealthMonitor()
