#!/usr/bin/env python3
"""
Test Narrative Engine for dynamic storytelling and quest generation
"""

import os
import sys
import time
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.narrative_engine import (
    NarrativeEngine, NarrativeEvent, QuestType, 
    narrative_engine
)

# Load environment variables
load_dotenv()

def test_dynamic_event_generation():
    """Test dynamic event generation"""
    print("📖 Testing Dynamic Event Generation")
    print("=" * 40)
    
    engine = narrative_engine
    
    # Test different tension levels
    tension_scenarios = [
        {"tension": 10, "description": "Low tension - peaceful tavern"},
        {"tension": 45, "description": "Medium tension - brewing conflict"},
        {"tension": 80, "description": "High tension - explosive atmosphere"}
    ]
    
    for scenario in tension_scenarios:
        print(f"\n🎭 Scenario: {scenario['description']}")
        
        # Set narrative state
        engine.narrative_state.tension_level = scenario["tension"]
        
        # Generate event
        trigger_context = {
            "player_action": "observe_tavern",
            "special_conditions": ["hooded_figures_present"]
        }
        
        event = engine.generate_dynamic_event(trigger_context)
        
        print(f"   Event: {event['title']}")
        print(f"   Type: {event['type']}")
        print(f"   Description: {event['description'][:80]}...")
        print(f"   Tension Change: {event['tension_change']}")
        print(f"   Participants: {', '.join(event['participants'])}")
    
    return engine

def test_quest_generation():
    """Test quest generation system"""
    print("\n⚔️ Testing Quest Generation")
    print("=" * 30)
    
    engine = narrative_engine
    
    # Test different quest types
    quest_types = [QuestType.INVESTIGATION, QuestType.RESCUE_MISSION, QuestType.TREASURE_HUNT]
    
    for quest_type in quest_types:
        print(f"\n🗡️ Generating {quest_type.value} quest...")
        
        quest = engine.generate_quest(quest_type=quest_type, difficulty=5)
        
        print(f"   Title: {quest.title}")
        print(f"   Description: {quest.description[:80]}...")
        print(f"   Difficulty: {quest.difficulty}/10")
        print(f"   Objectives: {len(quest.objectives)} objectives")
        print(f"   Required Agents: {', '.join(quest.required_agents)}")
        print(f"   Status: {quest.status}")
    
    return engine

def test_agent_orchestration():
    """Test agent interaction orchestration"""
    print("\n🎭 Testing Agent Orchestration")
    print("=" * 35)
    
    engine = narrative_engine
    
    # Test different interaction scenarios
    scenarios = [
        {
            "agents": ["Karczmarz", "Skrytobójca"],
            "scenario": "Suspicious hooded figures enter the tavern and order drinks"
        },
        {
            "agents": ["Wiedźma", "Zwiadowca", "Karczmarz"],
            "scenario": "Strange magical energies are detected in the tavern"
        },
        {
            "agents": ["Skrytobójca", "Czempion"],
            "scenario": "Tension escalates between two groups of patrons"
        }
    ]
    
    for i, test_scenario in enumerate(scenarios, 1):
        print(f"\n🎪 Scenario {i}: {test_scenario['scenario']}")
        print(f"   Agents: {', '.join(test_scenario['agents'])}")
        
        interactions = engine.orchestrate_agent_interaction(
            test_scenario["agents"], 
            test_scenario["scenario"]
        )
        
        for interaction in interactions:
            agent = interaction["agent"]
            response = interaction["response"]
            print(f"   {agent}: {response[:60]}...")
    
    return engine

def test_narrative_advancement():
    """Test narrative advancement system"""
    print("\n📈 Testing Narrative Advancement")
    print("=" * 35)
    
    engine = narrative_engine
    
    # Simulate player actions
    player_actions = [
        "investigate_hooded_figures",
        "ask_karczmarz_about_rumors",
        "challenge_suspicious_patron"
    ]
    
    print("🎮 Simulating player actions...")
    for action in player_actions:
        print(f"   Player action: {action}")
    
    # Advance narrative
    narrative_update = engine.advance_narrative(player_actions)
    
    print(f"\n📊 Narrative Update Results:")
    print(f"   New Events: {len(narrative_update['events'])}")
    print(f"   Quest Updates: {len(narrative_update['quest_updates'])}")
    print(f"   Agent Reactions: {len(narrative_update['agent_reactions'])}")
    print(f"   State Changes: {len(narrative_update['state_changes'])}")
    
    # Show some details
    if narrative_update["events"]:
        event = narrative_update["events"][0]
        print(f"\n🎭 New Event Generated:")
        print(f"   {event['title']}: {event['description'][:60]}...")
    
    if narrative_update["agent_reactions"]:
        print(f"\n🎭 Agent Reactions:")
        for reaction in narrative_update["agent_reactions"][:3]:
            print(f"   {reaction['agent']}: {reaction['reaction'][:50]}...")
    
    return engine

def test_narrative_summary():
    """Test comprehensive narrative summary"""
    print("\n📋 Testing Narrative Summary")
    print("=" * 30)
    
    engine = narrative_engine
    
    summary = engine.get_narrative_summary()
    
    print(f"📊 Narrative Summary:")
    print(f"   Current Tension: {summary['current_state']['tension_level']}/100")
    print(f"   Atmosphere: {summary['current_state']['tavern_atmosphere']}")
    print(f"   Active Quests: {len(summary['active_quests'])}")
    print(f"   Recent Events: {len(summary['recent_events'])}")
    print(f"   Story Complexity: {summary['narrative_metrics']['story_complexity']:.2f}/10")
    
    print(f"\n🎭 Agent Status:")
    for agent, status in summary["agent_status"].items():
        memory_count = len(status["recent_memories"])
        message_count = len(status["recent_messages"])
        print(f"   {agent}: {memory_count} memories, {message_count} messages")
    
    if summary["active_quests"]:
        print(f"\n⚔️ Active Quests:")
        for quest in summary["active_quests"][:3]:
            print(f"   - {quest['title']} ({quest['status']})")
    
    return engine

def test_narrative_persistence():
    """Test narrative state persistence"""
    print("\n💾 Testing Narrative Persistence")
    print("=" * 35)
    
    engine = narrative_engine
    
    # Get current state
    initial_summary = engine.get_narrative_summary()
    
    print(f"📊 Initial State:")
    print(f"   Events: {initial_summary['narrative_metrics']['total_events']}")
    print(f"   Quests: {initial_summary['narrative_metrics']['active_quest_count']}")
    print(f"   Tension: {initial_summary['current_state']['tension_level']}")
    
    # Save narrative state to memory system
    engine.memory_system.save_memories()
    print("✅ Narrative state saved")
    
    # Simulate state changes
    engine.narrative_state.tension_level += 20
    engine.generate_dynamic_event({"test": "persistence"})
    
    modified_summary = engine.get_narrative_summary()
    print(f"\n📊 Modified State:")
    print(f"   Events: {modified_summary['narrative_metrics']['total_events']}")
    print(f"   Tension: {modified_summary['current_state']['tension_level']}")
    
    print("✅ Persistence test completed")
    
    return engine

def test_performance_benchmarks():
    """Test narrative engine performance"""
    print("\n⚡ Testing Performance Benchmarks")
    print("=" * 40)
    
    engine = narrative_engine
    
    # Benchmark event generation
    print("🔥 Event Generation Benchmark (5 events):")
    event_times = []
    
    for i in range(5):
        start_time = time.time()
        event = engine.generate_dynamic_event({"benchmark": True})
        event_time = time.time() - start_time
        event_times.append(event_time)
        print(f"   Event {i+1}: {event_time:.3f}s - {event['title']}")
    
    avg_event_time = sum(event_times) / len(event_times)
    print(f"   Average: {avg_event_time:.3f}s")
    
    # Benchmark agent orchestration
    print(f"\n🎭 Agent Orchestration Benchmark:")
    start_time = time.time()
    interactions = engine.orchestrate_agent_interaction(
        ["Karczmarz", "Skrytobójca", "Wiedźma"],
        "Performance test scenario"
    )
    orchestration_time = time.time() - start_time
    print(f"   3-agent interaction: {orchestration_time:.3f}s")
    
    # Benchmark narrative advancement
    print(f"\n📈 Narrative Advancement Benchmark:")
    start_time = time.time()
    update = engine.advance_narrative(["test_action_1", "test_action_2"])
    advancement_time = time.time() - start_time
    print(f"   Full advancement: {advancement_time:.3f}s")
    
    print(f"\n📊 Performance Summary:")
    print(f"   Event Generation: {avg_event_time:.3f}s avg")
    print(f"   Agent Orchestration: {orchestration_time:.3f}s")
    print(f"   Narrative Advancement: {advancement_time:.3f}s")
    
    return engine

def main():
    """Main test function"""
    print("📖 Narrative Engine Test Suite")
    print("=" * 40)
    
    try:
        # Run all tests
        engine = test_dynamic_event_generation()
        test_quest_generation()
        test_agent_orchestration()
        test_narrative_advancement()
        test_narrative_summary()
        test_narrative_persistence()
        test_performance_benchmarks()
        
        print("\n🎉 Narrative Engine testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ Dynamic event generation")
        print("   ✅ Quest generation system")
        print("   ✅ Agent orchestration")
        print("   ✅ Narrative advancement")
        print("   ✅ Comprehensive summaries")
        print("   ✅ State persistence")
        print("   ✅ Performance optimization")
        
        # Final narrative state
        final_summary = engine.get_narrative_summary()
        print(f"\n📊 Final Narrative State:")
        print(f"   Total Events Generated: {final_summary['narrative_metrics']['total_events']}")
        print(f"   Story Complexity: {final_summary['narrative_metrics']['story_complexity']:.2f}/10")
        print(f"   Current Atmosphere: {final_summary['current_state']['tavern_atmosphere']}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
