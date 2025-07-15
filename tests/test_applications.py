#!/usr/bin/env python3
"""
Test script to verify both applications are running correctly
"""

import requests
import time
import sys
from typing import Dict, List

def test_application(url: str, name: str) -> Dict:
    """Test if an application is responding correctly"""
    try:
        response = requests.get(url, timeout=10)
        status = "✅ RUNNING" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
        
        return {
            "name": name,
            "url": url,
            "status": status,
            "response_time": response.elapsed.total_seconds(),
            "content_length": len(response.content)
        }
    except requests.exceptions.RequestException as e:
        return {
            "name": name,
            "url": url,
            "status": f"❌ FAILED ({str(e)})",
            "response_time": 0,
            "content_length": 0
        }

def run_tests() -> List[Dict]:
    """Run tests on all applications"""
    applications = [
        {
            "name": "Three.js Integration Test",
            "url": "http://localhost:8502"
        },
        {
            "name": "Main Warhammer Tavern Simulator",
            "url": "http://localhost:8503"
        },
        {
            "name": "Agent Animation Test",
            "url": "http://localhost:8504"
        }
    ]
    
    results = []
    
    print("🧪 Testing Warhammer Tavern Simulator Applications...")
    print("=" * 60)
    
    for app in applications:
        print(f"Testing {app['name']}...")
        result = test_application(app['url'], app['name'])
        results.append(result)
        
        print(f"  Status: {result['status']}")
        print(f"  Response Time: {result['response_time']:.3f}s")
        print(f"  Content Size: {result['content_length']} bytes")
        print()
    
    return results

def print_summary(results: List[Dict]):
    """Print test summary"""
    print("📊 Test Summary")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if "✅" in r['status'])
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    if failed_tests > 0:
        print("❌ Failed Tests:")
        for result in results:
            if "❌" in result['status']:
                print(f"  - {result['name']}: {result['status']}")
        print()
    
    print("🌐 Application URLs:")
    for result in results:
        status_icon = "✅" if "✅" in result['status'] else "❌"
        print(f"  {status_icon} {result['name']}: {result['url']}")

def check_performance():
    """Check basic performance metrics"""
    print("⚡ Performance Check")
    print("=" * 60)
    
    # Test Three.js Integration
    try:
        start_time = time.time()
        response = requests.get("http://localhost:8502", timeout=5)
        load_time = time.time() - start_time
        
        print(f"Three.js Integration Load Time: {load_time:.3f}s")
        
        if load_time < 3.0:
            print("✅ Load time is excellent (< 3s)")
        elif load_time < 5.0:
            print("⚠️ Load time is acceptable (< 5s)")
        else:
            print("❌ Load time is slow (> 5s)")
            
    except Exception as e:
        print(f"❌ Failed to test Three.js performance: {e}")
    
    # Test Main Application
    try:
        start_time = time.time()
        response = requests.get("http://localhost:8503", timeout=5)
        load_time = time.time() - start_time
        
        print(f"Main Application Load Time: {load_time:.3f}s")
        
        if load_time < 2.0:
            print("✅ Load time is excellent (< 2s)")
        elif load_time < 4.0:
            print("⚠️ Load time is acceptable (< 4s)")
        else:
            print("❌ Load time is slow (> 4s)")
            
    except Exception as e:
        print(f"❌ Failed to test main app performance: {e}")

def main():
    """Main test function"""
    print("🏰 Warhammer Tavern Simulator - Application Test Suite")
    print("=" * 60)
    print()
    
    # Run basic connectivity tests
    results = run_tests()
    
    # Print summary
    print_summary(results)
    print()
    
    # Check performance
    check_performance()
    print()
    
    # Final recommendations
    print("🎯 Recommendations")
    print("=" * 60)
    
    all_passed = all("✅" in r['status'] for r in results)
    
    if all_passed:
        print("✅ All applications are running successfully!")
        print("🌟 You can now test the Three.js integration features:")
        print("   - Interactive 3D tavern environment")
        print("   - Character animations and interactions")
        print("   - Real-time performance monitoring")
        print("   - Quality settings and VR support")
        print()
        print("🔗 Access URLs:")
        print("   - Three.js Demo: http://localhost:8502")
        print("   - Main Simulator: http://localhost:8503")
    else:
        print("❌ Some applications failed to start.")
        print("💡 Troubleshooting steps:")
        print("   1. Check if ports 8502 and 8503 are available")
        print("   2. Verify virtual environment is activated")
        print("   3. Check for any missing dependencies")
        print("   4. Review application logs for errors")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
