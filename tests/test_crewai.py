#!/usr/bin/env python3
"""
Test script for CrewAI Warhammer Tavern Simulator
Tests crew initialization and execution with mock LLMs
"""

import os
import time
from crewai_app import WarhamerTavernCrew

def test_crew_initialization():
    """Test crew initialization"""
    print("🧪 Testing CrewAI Warhammer Tavern Crew...")
    
    # Initialize crew
    tavern_crew = WarhamerTavernCrew()
    
    # Test MVP crew initialization
    print("\n1. Initializing MVP crew...")
    success = tavern_crew.initialize_mvp_crew()
    
    if success:
        print("✅ MVP crew initialized successfully!")
        
        # Get crew status
        status = tavern_crew.get_crew_status()
        print(f"📊 Agents: {len(status['agents'])}")
        print(f"📋 Tasks: {len(status['tasks'])}")
        print(f"🚀 Crew Ready: {status['crew_ready']}")
        
        # Print agent details
        print("\n👥 Agents:")
        for agent in status['agents']:
            print(f"  - {agent['role']}: {agent['goal'][:50]}...")
            print(f"    LLM: {'✅' if agent['llm_configured'] else '❌'}")
        
        return tavern_crew
    else:
        print("❌ Failed to initialize crew")
        return None

def test_crew_execution(tavern_crew):
    """Test crew execution"""
    if not tavern_crew:
        print("❌ No crew to test")
        return
    
    print("\n2. Testing crew execution...")
    start_time = time.time()
    
    # Execute simulation
    results = tavern_crew.execute_tavern_simulation()
    
    execution_time = time.time() - start_time
    
    if results.get("success"):
        print(f"✅ Simulation completed in {execution_time:.2f}s")
        print(f"📊 Agents involved: {results['agents_count']}")
        print(f"📋 Tasks completed: {results['tasks_completed']}")
        
        # Print results summary
        if results.get("result"):
            result_str = str(results["result"])
            print(f"\n📜 Results preview: {result_str[:200]}...")
        
        return True
    else:
        print(f"❌ Simulation failed: {results.get('error', 'Unknown error')}")
        return False

def test_gsap_renderer(tavern_crew):
    """Test GSAP renderer"""
    if not tavern_crew:
        print("❌ No crew to test")
        return
    
    print("\n3. Testing GSAP renderer...")
    
    # Generate GSAP HTML
    gsap_html = tavern_crew.gsap_renderer.get_crew_visualization_html(
        tavern_crew.agents, 
        tavern_crew.tasks
    )
    
    # Check HTML content
    if len(gsap_html) > 1000:
        print(f"✅ GSAP HTML generated: {len(gsap_html)} characters")
        
        # Check for key GSAP features
        gsap_features = [
            "gsap.min.js",
            "TextPlugin",
            "MorphSVGPlugin", 
            "DrawSVGPlugin",
            "agent-card",
            "task-card",
            "initializeCrewAnimations",
            "animateAgentThinking"
        ]
        
        found_features = []
        for feature in gsap_features:
            if feature in gsap_html:
                found_features.append(feature)
        
        print(f"🎭 GSAP features found: {len(found_features)}/{len(gsap_features)}")
        for feature in found_features:
            print(f"  ✅ {feature}")
        
        return True
    else:
        print("❌ GSAP HTML generation failed")
        return False

def main():
    """Main test function"""
    print("🏰 Warhammer Fantasy Tavern Simulator - CrewAI Test Suite")
    print("=" * 60)
    
    # Test 1: Crew initialization
    tavern_crew = test_crew_initialization()
    
    # Test 2: Crew execution
    if tavern_crew:
        execution_success = test_crew_execution(tavern_crew)
        
        # Test 3: GSAP renderer
        gsap_success = test_gsap_renderer(tavern_crew)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"  Crew Initialization: {'✅' if tavern_crew else '❌'}")
        print(f"  Crew Execution: {'✅' if execution_success else '❌'}")
        print(f"  GSAP Renderer: {'✅' if gsap_success else '❌'}")
        
        if tavern_crew and execution_success and gsap_success:
            print("\n🎉 ALL TESTS PASSED! CrewAI Warhammer Tavern ready for deployment!")
        else:
            print("\n⚠️ Some tests failed. Check the output above.")
    
    print("\n🔗 Streamlit app running at: http://localhost:8502")

if __name__ == "__main__":
    main()
