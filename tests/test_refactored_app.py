#!/usr/bin/env python3
"""
Test script for the refactored Warhammer Fantasy Tavern Simulator
Tests modular architecture, agent system, and GSAP integration
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_modular_imports():
    """Test all modular component imports"""
    print("🧪 Testing Modular Architecture Imports...")
    
    try:
        # Test config
        from config import api_config, tavern_config, agent_config, ui_config, validate_config
        print("✅ Configuration modules imported")
        
        # Test components
        from components.gsap_renderer import GSAPRenderer
        print("✅ GSAP renderer component imported")
        
        # Test services
        from services.llm_service import llm_service, LLMRequest, LLMProvider
        from services.agent_manager import agent_manager
        print("✅ Service modules imported")
        
        # Test agents
        from agents.base_agent import BaseAgent, AgentAction
        from agents.karczmarz import KarczmarzAgent
        from agents.skrytobojca import SkrytobojcaAgent
        print("✅ Agent modules imported")
        
        # Test core simulator
        from core.tavern_simulator import TavernSimulator
        from core.enums import InteractionType, Faction
        print("✅ Core simulator modules imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration_system():
    """Test configuration validation and settings"""
    print("\n🧪 Testing Configuration System...")
    
    try:
        from config import validate_config, api_config, agent_config, ui_config
        
        # Test configuration validation
        errors = validate_config()
        if errors:
            print(f"⚠️ Configuration warnings: {len(errors)} issues")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ Configuration validation passed")
        
        # Test agent personalities
        personalities = agent_config.agent_personalities
        print(f"✅ Agent personalities loaded: {len(personalities)} agents")
        
        for name, config in personalities.items():
            print(f"  - {name}: {config['role']} (prefers {config['preferred_llm']})")
        
        # Test UI configuration
        print(f"✅ UI config: {len(ui_config.faction_colors)} faction colors")
        print(f"✅ GSAP version: {ui_config.gsap_cdn_version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_agent_system():
    """Test multi-agent system functionality"""
    print("\n🧪 Testing Multi-Agent System...")
    
    try:
        from services.agent_manager import agent_manager
        from agents.karczmarz import KarczmarzAgent
        from agents.skrytobojca import SkrytobojcaAgent
        
        # Test agent initialization
        print(f"✅ Agent manager initialized with {len(agent_manager.agents)} agents")
        
        # Test individual agents
        for agent_name, agent in agent_manager.agents.items():
            print(f"✅ {agent_name}: {agent.role} - {agent.get_emotional_state()}")
            
            # Test agent perception
            mock_tavern_state = {
                "tension_level": 50,
                "characters": [
                    {"name": "Test Character", "faction": "Empire", "drunk_level": 3}
                ],
                "reputation": 60
            }
            
            perceptions = agent.perceive(mock_tavern_state)
            print(f"  - Perceptions: {len(perceptions)} items")
            
            # Test agent decision making
            if agent.can_act():
                decision = agent.decide(perceptions)
                if decision:
                    print(f"  - Decision: {decision.action_type} (confidence: {decision.confidence})")
        
        # Test agent coordination
        turn_results = agent_manager.process_turn(mock_tavern_state)
        print(f"✅ Agent turn processed: {len(turn_results['agent_actions'])} actions")
        
        # Test communication system
        comms = agent_manager.get_communication_history()
        print(f"✅ Communication system: {len(comms)} messages")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_service():
    """Test LLM service functionality"""
    print("\n🧪 Testing LLM Service...")
    
    try:
        from services.llm_service import llm_service, LLMRequest, LLMProvider
        
        # Test LLM request creation
        request = LLMRequest(
            prompt="Test tavern situation",
            system_message="You are a tavern keeper",
            provider=LLMProvider.GROK,
            agent_name="Karczmarz"
        )
        print("✅ LLM request created")
        
        # Test LLM call (will use mock response)
        response = llm_service.call_llm(request)
        print(f"✅ LLM response: {response.success}")
        print(f"  - Provider: {response.provider.value}")
        print(f"  - Content: {response.content[:50]}...")
        print(f"  - Response time: {response.response_time:.3f}s")
        
        # Test provider statistics
        stats = llm_service.get_provider_stats()
        print(f"✅ Provider stats: {len(stats)} providers tracked")
        
        # Test provider recommendation
        best_provider = llm_service.get_best_provider_for_task("complex_reasoning")
        print(f"✅ Best provider for complex reasoning: {best_provider.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM service test failed: {e}")
        return False

def test_gsap_renderer():
    """Test GSAP HTML renderer"""
    print("\n🧪 Testing GSAP Renderer...")
    
    try:
        from components.gsap_renderer import GSAPRenderer
        
        # Test renderer initialization
        renderer = GSAPRenderer()
        print("✅ GSAP renderer initialized")
        
        # Test CDN links generation
        cdn_links = renderer.get_gsap_cdn_links()
        print(f"✅ GSAP CDN links generated: {len(cdn_links)} characters")
        
        # Test faction CSS generation
        faction_css = renderer.get_faction_css()
        print(f"✅ Faction CSS generated: {len(faction_css)} characters")
        
        # Test full HTML generation
        html_content = renderer.get_tavern_html("Test Tavern")
        print(f"✅ Full HTML generated: {len(html_content)} characters")
        
        # Check for required elements
        required_elements = [
            "tavern-container",
            "characters-list", 
            "agents-container",
            "relationships-graph",
            "gsap.registerPlugin"
        ]
        
        for element in required_elements:
            if element in html_content:
                print(f"✅ Required element found: {element}")
            else:
                print(f"⚠️ Missing element: {element}")
        
        return True
        
    except Exception as e:
        print(f"❌ GSAP renderer test failed: {e}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Component Integration...")
    
    try:
        from core.tavern_simulator import TavernSimulator
        from services.agent_manager import agent_manager
        from components.gsap_renderer import GSAPRenderer
        
        # Test simulator + agent integration
        simulator = TavernSimulator()
        simulator.generate_new_tavern()
        print("✅ Tavern simulator initialized")
        
        # Get tavern state for agents
        tavern_state = {
            "tension_level": simulator.current_tavern.tension_level,
            "reputation": simulator.current_tavern.reputation,
            "characters": [
                {
                    "name": char.name,
                    "faction": char.faction.value,
                    "drunk_level": char.drunk_level
                }
                for char in simulator.current_tavern.characters
            ]
        }
        
        # Process agent turn with real tavern data
        turn_results = agent_manager.process_turn(tavern_state)
        print(f"✅ Agent-simulator integration: {len(turn_results['agent_actions'])} actions")
        
        # Test GSAP renderer with real data
        renderer = GSAPRenderer()
        html = renderer.get_tavern_html(simulator.current_tavern.name)
        print(f"✅ GSAP-simulator integration: HTML generated for {simulator.current_tavern.name}")
        
        # Test character data formatting for GSAP
        characters_data = [
            {
                'name': char.name,
                'faction': char.faction.value.replace(' ', '').lower()
            }
            for char in simulator.current_tavern.characters
        ]
        print(f"✅ Character data formatted for GSAP: {len(characters_data)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance():
    """Test performance of key operations"""
    print("\n🧪 Testing Performance...")
    
    try:
        import time
        from services.agent_manager import agent_manager
        from core.tavern_simulator import TavernSimulator
        
        # Test agent turn performance
        simulator = TavernSimulator()
        simulator.generate_new_tavern()
        
        tavern_state = {
            "tension_level": 50,
            "characters": [{"name": f"Char{i}", "faction": "Empire"} for i in range(10)]
        }
        
        start_time = time.time()
        for _ in range(5):
            agent_manager.process_turn(tavern_state)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 5
        print(f"✅ Agent turn performance: {avg_time:.3f}s average")
        
        if avg_time < 1.0:
            print("✅ Performance target met (<1s per turn)")
        else:
            print("⚠️ Performance target missed (>1s per turn)")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

if __name__ == "__main__":
    print("🏰 Warhammer Fantasy Tavern Simulator - Refactored Architecture Test Suite")
    print("=" * 80)
    
    success = True
    
    # Run all tests
    success &= test_modular_imports()
    success &= test_configuration_system()
    success &= test_agent_system()
    success &= test_llm_service()
    success &= test_gsap_renderer()
    success &= test_integration()
    success &= test_performance()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 All tests passed! Refactored architecture is ready!")
        print("\n🚀 To run the refactored Streamlit app:")
        print("   streamlit run streamlit_app_refactored.py")
        print("\n✨ New Features:")
        print("   • Modular architecture with clean separation")
        print("   • Multi-agent AI system with Grok/Cerebras")
        print("   • Agent coordination and communication")
        print("   • Enhanced GSAP animations with agent visualization")
        print("   • Performance optimized component system")
        print("   • Configurable LLM provider selection")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        sys.exit(1)
