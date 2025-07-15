#!/usr/bin/env python3
"""
Health Check Endpoints for Warhammer Fantasy Tavern Simulator
Provides HTTP endpoints for container health checks and monitoring
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from services.health_monitor import health_monitor
import structlog

logger = structlog.get_logger()

class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health check endpoints"""
    
    def do_GET(self):
        """Handle GET requests for health endpoints"""
        try:
            if self.path == '/health':
                self.handle_health_check()
            elif self.path == '/health/live':
                self.handle_liveness_check()
            elif self.path == '/health/ready':
                self.handle_readiness_check()
            elif self.path == '/metrics':
                self.handle_prometheus_metrics()
            elif self.path == '/status':
                self.handle_status_check()
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            logger.error("Health endpoint error", error=str(e))
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_health_check(self):
        """Comprehensive health check endpoint"""
        try:
            health_report = health_monitor.check_health()
            
            self.send_response(health_report["status_code"])
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            response = json.dumps(health_report, indent=2)
            self.wfile.write(response.encode())
            
        except Exception as e:
            self.send_error(500, f"Health check failed: {str(e)}")
    
    def handle_liveness_check(self):
        """Simple liveness check - is the application running?"""
        try:
            response = {
                "status": "alive",
                "timestamp": time.time(),
                "service": "warhammer-tavern-simulator"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Liveness check failed: {str(e)}")
    
    def handle_readiness_check(self):
        """Readiness check - is the application ready to serve traffic?"""
        try:
            # Test core components
            from services.tavern_economy import TavernEconomySystem
            from services.narrative_engine import NarrativeEngine
            from components.gsap_renderer import GSAPRenderer
            
            # Quick functionality test
            economy = TavernEconomySystem()
            narrative = NarrativeEngine(economy_system=economy)
            renderer = GSAPRenderer()
            
            # Verify basic operations work
            agent_count = narrative.get_total_agent_count()
            economic_summary = economy.get_economic_summary()
            html_size = len(renderer.get_tavern_html("Health Check"))
            
            if agent_count >= 18 and html_size > 50000:
                status = "ready"
                status_code = 200
            else:
                status = "not_ready"
                status_code = 503
            
            response = {
                "status": status,
                "timestamp": time.time(),
                "checks": {
                    "agent_count": agent_count,
                    "economy_initialized": bool(economic_summary),
                    "gsap_renderer_size": html_size
                },
                "service": "warhammer-tavern-simulator"
            }
            
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            response = {
                "status": "not_ready",
                "timestamp": time.time(),
                "error": str(e),
                "service": "warhammer-tavern-simulator"
            }
            
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
    
    def handle_prometheus_metrics(self):
        """Prometheus metrics endpoint"""
        try:
            metrics = health_monitor.get_prometheus_metrics()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; version=0.0.4; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            self.wfile.write(metrics.encode())
            
        except Exception as e:
            self.send_error(500, f"Metrics generation failed: {str(e)}")
    
    def handle_status_check(self):
        """Simple status endpoint"""
        try:
            response = {
                "service": "warhammer-tavern-simulator",
                "version": "1.0.0",
                "status": "running",
                "timestamp": time.time(),
                "uptime": time.time() - health_monitor.start_time
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Status check failed: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to use structured logging"""
        logger.info("Health endpoint access", 
                   method=self.command,
                   path=self.path,
                   client=self.client_address[0])

class HealthServer:
    """Health check server for running alongside the main application"""
    
    def __init__(self, port=8502):
        self.port = port
        self.server = None
        self.thread = None
        
    def start(self):
        """Start the health check server in a separate thread"""
        try:
            self.server = HTTPServer(('0.0.0.0', self.port), HealthHandler)
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            
            logger.info("Health check server started", port=self.port)
            
        except Exception as e:
            logger.error("Failed to start health check server", error=str(e))
    
    def stop(self):
        """Stop the health check server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("Health check server stopped")

# Global health server instance
health_server = HealthServer()

def start_health_server():
    """Start the health check server"""
    health_server.start()

def stop_health_server():
    """Stop the health check server"""
    health_server.stop()

if __name__ == "__main__":
    # Run standalone health server for testing
    print("🏥 Starting standalone health check server...")
    
    try:
        server = HTTPServer(('0.0.0.0', 8502), HealthHandler)
        print("🏥 Health check server running on http://0.0.0.0:8502")
        print("📊 Available endpoints:")
        print("  - /health - Comprehensive health check")
        print("  - /health/live - Liveness probe")
        print("  - /health/ready - Readiness probe")
        print("  - /metrics - Prometheus metrics")
        print("  - /status - Simple status")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Health server stopped")
        server.shutdown()
    except Exception as e:
        print(f"❌ Health server error: {e}")
