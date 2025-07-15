#!/usr/bin/env python3
"""
Test Groq API integration for complex reasoning and narrative planning
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import LLMService, LLMRequest, LLMProvider

# Load environment variables
load_dotenv()

def test_groq_complex_reasoning():
    """Test Groq API for complex reasoning scenarios"""
    print("🧠 Testing Groq API for Complex Reasoning")
    print("=" * 50)

    # Debug API key loading
    from config import api_config
    print(f"🔑 Debug - Groq API key loaded: {bool(api_config.groq_api_key)}")
    print(f"🔑 Debug - Cerebras API key loaded: {bool(api_config.cerebras_api_key)}")

    llm_service = LLMService()
    
    # Test scenario 1: Strategic planning
    planning_request = LLMRequest(
        prompt="A group of suspicious hooded figures has entered the tavern. They're whispering in a corner and one keeps glancing at the exit. What should I do?",
        system_message="You are the tavern keeper. You must balance customer service with security concerns.",
        agent_name="Karczmarz",
        provider=LLMProvider.GROQ,
        max_tokens=800,
        temperature=0.7,
        context={
            "tavern_tension": 45,
            "current_patrons": 12,
            "time_of_day": "evening",
            "recent_events": ["merchant caravan arrived", "rumors of bandits nearby"]
        }
    )
    
    print("📋 Scenario 1: Strategic Planning")
    response = llm_service.call_llm(planning_request)
    print(f"✅ Success: {response.success}")
    print(f"🕒 Response time: {response.response_time:.2f}s")
    print(f"📝 Response: {response.content[:200]}...")
    print()
    
    # Test scenario 2: Narrative generation
    narrative_request = LLMRequest(
        prompt="Create a dramatic event that could unfold in the tavern tonight involving the mysterious hooded figures.",
        system_message="You are a master storyteller creating engaging Warhammer Fantasy narratives.",
        agent_name="Wiedźma",
        provider=LLMProvider.GROQ,
        max_tokens=600,
        temperature=0.8,
        context={
            "setting": "The Prancing Pony tavern",
            "atmosphere": "tense",
            "key_npcs": ["hooded figures", "merchant", "local guards"]
        }
    )
    
    print("📖 Scenario 2: Narrative Generation")
    response = llm_service.call_llm(narrative_request)
    print(f"✅ Success: {response.success}")
    print(f"🕒 Response time: {response.response_time:.2f}s")
    print(f"📝 Response: {response.content[:200]}...")
    print()
    
    # Test scenario 3: Multi-step reasoning
    reasoning_request = LLMRequest(
        prompt="Analyze the political implications if these hooded figures are: 1) Chaos cultists, 2) Imperial spies, or 3) Merchant guild representatives. What are the consequences of each possibility?",
        system_message="You are a cunning shadow agent who understands political intrigue.",
        agent_name="Skrytobójca",
        provider=LLMProvider.GROQ,
        max_tokens=1000,
        temperature=0.6,
        context={
            "location": "Border town tavern",
            "political_climate": "unstable",
            "recent_tensions": ["trade disputes", "chaos incursions", "imperial taxation"]
        }
    )
    
    print("🎭 Scenario 3: Multi-step Political Analysis")
    response = llm_service.call_llm(reasoning_request)
    print(f"✅ Success: {response.success}")
    print(f"🕒 Response time: {response.response_time:.2f}s")
    print(f"📝 Response: {response.content[:300]}...")
    print()
    
    return llm_service

def test_cerebras_quick_responses():
    """Test Cerebras API for quick responses"""
    print("⚡ Testing Cerebras API for Quick Responses")
    print("=" * 50)

    llm_service = LLMService()
    
    # Test quick dialogue
    dialogue_request = LLMRequest(
        prompt="A patron asks you about the hooded figures. Respond quickly and naturally.",
        system_message="You are a chatty tavern patron who loves gossip.",
        agent_name="Zwiadowca",
        provider=LLMProvider.CEREBRAS,
        max_tokens=150,
        temperature=0.9
    )
    
    print("💬 Quick Dialogue Test")
    response = llm_service.call_llm(dialogue_request)
    print(f"✅ Success: {response.success}")
    print(f"🕒 Response time: {response.response_time:.2f}s")
    print(f"📝 Response: {response.content}")
    print()

    return llm_service

def test_provider_selection():
    """Test automatic provider selection based on task type"""
    print("🎯 Testing Provider Selection Logic")
    print("=" * 50)
    
    llm_service = LLMService()
    
    # Test different task types
    task_types = [
        "complex_reasoning",
        "planning", 
        "narrative",
        "quick_response",
        "dialogue",
        "simple_decision"
    ]
    
    for task_type in task_types:
        recommended_provider = llm_service.get_best_provider_for_task(task_type)
        print(f"📋 Task: {task_type} → Recommended: {recommended_provider.value}")
    
    print()
    return llm_service

def main():
    """Main test function"""
    print("🏰 Groq API Integration Test Suite")
    print("=" * 60)
    
    # Test Groq for complex reasoning
    llm_service = test_groq_complex_reasoning()

    # Test Cerebras for quick responses (use same service instance)
    llm_service = test_cerebras_quick_responses()

    # Test provider selection
    test_provider_selection()
    
    # Show statistics
    print("📊 Provider Statistics")
    print("=" * 30)
    stats = llm_service.get_provider_stats()
    for provider, stat in stats.items():
        print(f"{provider}:")
        print(f"  Requests: {stat['requests']}")
        print(f"  Success Rate: {stat['success_rate']:.2%}")
        print(f"  Avg Response Time: {stat['avg_response_time']:.3f}s")
        print()
    
    print("🎉 Integration test complete!")

if __name__ == "__main__":
    main()
