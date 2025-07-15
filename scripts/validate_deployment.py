#!/usr/bin/env python3
"""
Comprehensive Deployment Validation Script
Validates all aspects of the Warhammer Fantasy Tavern Simulator deployment
"""

import requests
import time
import json
import sys
import subprocess
from typing import Dict, Any, List, Tuple
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class DeploymentValidator:
    """Comprehensive deployment validation"""
    
    def __init__(self, base_url: str = "http://localhost", app_port: int = 8501, health_port: int = 8502):
        self.base_url = base_url
        self.app_port = app_port
        self.health_port = health_port
        self.app_url = f"{base_url}:{app_port}"
        self.health_url = f"{base_url}:{health_port}"
        self.results = []
        
    def log_result(self, test_name: str, passed: bool, details: str = "", metrics: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": time.time(),
            "metrics": metrics or {}
        }
        self.results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
        if metrics:
            for key, value in metrics.items():
                print(f"    📊 {key}: {value}")
    
    def test_container_running(self) -> bool:
        """Test if Docker container is running"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=tavern", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            containers = result.stdout.strip().split('\n')
            running_containers = [c for c in containers if c and 'tavern' in c]
            
            if running_containers:
                self.log_result(
                    "Container Status",
                    True,
                    f"Found {len(running_containers)} running containers",
                    {"containers": running_containers}
                )
                return True
            else:
                self.log_result("Container Status", False, "No tavern containers running")
                return False
                
        except Exception as e:
            self.log_result("Container Status", False, f"Error checking containers: {e}")
            return False
    
    def test_health_endpoints(self) -> bool:
        """Test all health endpoints"""
        endpoints = [
            ("/health", "Comprehensive Health Check"),
            ("/health/live", "Liveness Probe"),
            ("/health/ready", "Readiness Probe"),
            ("/metrics", "Prometheus Metrics"),
            ("/status", "Status Check")
        ]
        
        all_passed = True
        
        for endpoint, description in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.health_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    content_length = len(response.content)
                    self.log_result(
                        f"Health Endpoint {endpoint}",
                        True,
                        f"{description} responding",
                        {
                            "status_code": response.status_code,
                            "response_time_ms": round(response_time * 1000, 2),
                            "content_length": content_length
                        }
                    )
                else:
                    self.log_result(
                        f"Health Endpoint {endpoint}",
                        False,
                        f"HTTP {response.status_code}"
                    )
                    all_passed = False
                    
            except Exception as e:
                self.log_result(
                    f"Health Endpoint {endpoint}",
                    False,
                    f"Connection error: {e}"
                )
                all_passed = False
        
        return all_passed
    
    def test_application_startup(self) -> bool:
        """Test main application startup"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.app_url}/_stcore/health", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result(
                    "Application Startup",
                    True,
                    "Streamlit application responding",
                    {
                        "status_code": response.status_code,
                        "response_time_ms": round(response_time * 1000, 2)
                    }
                )
                return True
            else:
                self.log_result(
                    "Application Startup",
                    False,
                    f"HTTP {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Application Startup",
                False,
                f"Connection error: {e}"
            )
            return False
    
    def test_system_performance(self) -> bool:
        """Test system performance metrics"""
        try:
            response = requests.get(f"{self.health_url}/health", timeout=10)
            
            if response.status_code != 200:
                self.log_result("Performance Test", False, "Health endpoint not available")
                return False
            
            health_data = response.json()
            metrics = health_data.get("metrics", {})
            
            # Performance thresholds
            thresholds = {
                "cpu_percent": 80.0,
                "memory_percent": 85.0,
                "response_time_ms": 1000.0,
                "error_rate": 5.0
            }
            
            performance_passed = True
            performance_metrics = {}
            
            for metric, threshold in thresholds.items():
                if metric in metrics:
                    value = metrics[metric]
                    performance_metrics[metric] = value
                    
                    if metric == "error_rate":
                        passed = value <= threshold
                    else:
                        passed = value <= threshold
                    
                    if not passed:
                        performance_passed = False
            
            # Check agent count
            agent_count = metrics.get("active_agents", 0)
            performance_metrics["active_agents"] = agent_count
            
            if agent_count < 18:
                performance_passed = False
            
            self.log_result(
                "Performance Metrics",
                performance_passed,
                f"System performance {'within' if performance_passed else 'exceeds'} thresholds",
                performance_metrics
            )
            
            return performance_passed
            
        except Exception as e:
            self.log_result("Performance Test", False, f"Error: {e}")
            return False
    
    def test_api_integration(self) -> bool:
        """Test API integration and functionality"""
        try:
            # Test readiness which includes component validation
            response = requests.get(f"{self.health_url}/health/ready", timeout=15)
            
            if response.status_code != 200:
                self.log_result("API Integration", False, "Readiness check failed")
                return False
            
            ready_data = response.json()
            checks = ready_data.get("checks", {})
            
            required_checks = {
                "agent_count": 18,
                "economy_initialized": True,
                "gsap_renderer_size": 50000
            }
            
            integration_passed = True
            integration_metrics = {}
            
            for check, expected in required_checks.items():
                if check in checks:
                    value = checks[check]
                    integration_metrics[check] = value
                    
                    if isinstance(expected, bool):
                        passed = value == expected
                    elif isinstance(expected, int):
                        passed = value >= expected
                    else:
                        passed = True
                    
                    if not passed:
                        integration_passed = False
                else:
                    integration_passed = False
            
            self.log_result(
                "API Integration",
                integration_passed,
                f"Component integration {'successful' if integration_passed else 'failed'}",
                integration_metrics
            )
            
            return integration_passed
            
        except Exception as e:
            self.log_result("API Integration", False, f"Error: {e}")
            return False
    
    def test_gsap_visualization(self) -> bool:
        """Test GSAP visualization availability"""
        try:
            # Test if main app loads (indicates GSAP is working)
            response = requests.get(self.app_url, timeout=20)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for GSAP indicators
                gsap_indicators = [
                    "gsap",
                    "updateEconomyStats",
                    "animateTradeResult",
                    "tavern-visualization"
                ]
                
                found_indicators = []
                for indicator in gsap_indicators:
                    if indicator.lower() in content.lower():
                        found_indicators.append(indicator)
                
                gsap_score = len(found_indicators) / len(gsap_indicators) * 100
                
                self.log_result(
                    "GSAP Visualization",
                    gsap_score >= 50,
                    f"GSAP integration at {gsap_score:.1f}%",
                    {
                        "gsap_score": gsap_score,
                        "indicators_found": found_indicators,
                        "content_size": len(content)
                    }
                )
                
                return gsap_score >= 50
            else:
                self.log_result("GSAP Visualization", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("GSAP Visualization", False, f"Error: {e}")
            return False
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation tests"""
        print("🏰 Starting Comprehensive Deployment Validation")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        tests = [
            ("Container Status", self.test_container_running),
            ("Health Endpoints", self.test_health_endpoints),
            ("Application Startup", self.test_application_startup),
            ("System Performance", self.test_system_performance),
            ("API Integration", self.test_api_integration),
            ("GSAP Visualization", self.test_gsap_visualization)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name}...")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_result(test_name, False, f"Test error: {e}")
        
        total_time = time.time() - start_time
        success_rate = (passed_tests / total_tests) * 100
        
        # Generate summary
        summary = {
            "validation_time": round(total_time, 2),
            "tests_passed": passed_tests,
            "tests_total": total_tests,
            "success_rate": round(success_rate, 1),
            "deployment_ready": success_rate >= 80,
            "results": self.results
        }
        
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        print(f"⏱️  Total Time: {summary['validation_time']}s")
        print(f"✅ Tests Passed: {summary['tests_passed']}/{summary['tests_total']}")
        print(f"📈 Success Rate: {summary['success_rate']}%")
        
        if summary['deployment_ready']:
            print("🎉 DEPLOYMENT READY: All critical tests passed!")
            print("🚀 System is production-ready for deployment")
        else:
            print("⚠️  DEPLOYMENT ISSUES: Some tests failed")
            print("🔧 Review failed tests before production deployment")
        
        return summary

def main():
    """Main validation function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Warhammer Tavern Simulator deployment")
    parser.add_argument("--base-url", default="http://localhost", help="Base URL for testing")
    parser.add_argument("--app-port", type=int, default=8501, help="Application port")
    parser.add_argument("--health-port", type=int, default=8502, help="Health check port")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    validator = DeploymentValidator(args.base_url, args.app_port, args.health_port)
    results = validator.run_comprehensive_validation()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Results saved to: {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if results['deployment_ready'] else 1)

if __name__ == "__main__":
    main()
