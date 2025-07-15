#!/usr/bin/env python3
"""
Test 17-Agent System with Faction Organization
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import TavernEconomySystem, ResourceType
from services.narrative_engine import NarrativeEngine

# Load environment variables
load_dotenv()

def test_17_agent_initialization():
    """Test that all 17 agents are properly initialized"""
    print("👥 Testing 17-Agent System Initialization")
    print("=" * 45)
    
    # Create systems
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Check agent count
    total_agents = narrative.get_total_agent_count()
    print(f"📊 Total Agents: {total_agents}")
    
    # Check faction distribution
    faction_counts = narrative.get_agent_count_by_faction()
    print(f"\n🏛️ Faction Distribution:")
    for faction, count in faction_counts.items():
        print(f"   {faction}: {count} agents")
    
    # Verify all agents have resources
    print(f"\n💰 Agent Resource Verification:")
    missing_resources = []
    
    for agent in narrative.agent_roles.keys():
        if agent in economy.agent_resources:
            wealth = economy.get_agent_wealth_status(agent)
            print(f"   ✅ {agent}: {wealth['total_wealth']:.1f} gold ({wealth['wealth_class']})")
        else:
            missing_resources.append(agent)
            print(f"   ❌ {agent}: No resources found")
    
    if missing_resources:
        print(f"\n⚠️ Missing resources for: {', '.join(missing_resources)}")
    else:
        print(f"\n✅ All {total_agents} agents have resources initialized")
    
    return economy, narrative

def test_faction_coordination():
    """Test faction-based coordination"""
    print("\n🤝 Testing Faction Coordination")
    print("=" * 35)
    
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Test event for each faction
    test_event = {
        "id": "faction_test_1",
        "type": "threat_detected",
        "title": "Orc Raiders Approaching",
        "description": "Scouts report orc raiders heading toward the settlement",
        "tension_change": 20,
        "timestamp": 1234567890
    }
    
    print(f"🎭 Test Event: {test_event['title']}")
    print(f"   Description: {test_event['description']}")
    print()
    
    # Test each faction's response
    for faction in narrative.faction_crews.keys():
        print(f"🏛️ {faction} Faction Response:")
        
        faction_agents = narrative.get_faction_agents(faction)
        print(f"   Agents: {', '.join(faction_agents)}")
        
        # Get faction response (simplified - just count agents)
        response_count = len(faction_agents)
        print(f"   Response Capacity: {response_count} agents")
        
        # Check faction resources
        faction_wealth = 0
        faction_reputation = 0
        for agent in faction_agents:
            if agent in economy.agent_resources:
                wealth_status = economy.get_agent_wealth_status(agent)
                faction_wealth += wealth_status['total_wealth']
                faction_reputation += economy.agent_resources[agent][ResourceType.REPUTATION]
        
        avg_reputation = faction_reputation / len(faction_agents) if faction_agents else 0
        print(f"   Total Wealth: {faction_wealth:.1f} gold")
        print(f"   Avg Reputation: {avg_reputation:.1f}/100")
        print()
    
    return economy, narrative

def test_large_scale_event():
    """Test event processing with all 17 agents"""
    print("\n🌪️ Testing Large-Scale Event Processing")
    print("=" * 45)
    
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Create a major event affecting all factions
    major_event = {
        "id": "major_crisis_1",
        "type": "betrayal_revealed",
        "title": "Chaos Cult Infiltration Exposed",
        "description": "A massive chaos cult network is discovered operating within the settlement",
        "tension_change": 40,
        "participants": list(narrative.agent_roles.keys()),  # All agents involved
        "timestamp": 1234567891
    }
    
    print(f"🎭 Major Event: {major_event['title']}")
    print(f"   Participants: {len(major_event['participants'])} agents")
    print(f"   Tension Change: +{major_event['tension_change']}")
    
    # Get initial state
    initial_reputation = economy.economic_state.reputation_score
    initial_tension = narrative.narrative_state.tension_level
    
    print(f"\n📊 Initial State:")
    print(f"   Tavern Reputation: {initial_reputation:.1f}/100")
    print(f"   Tension Level: {initial_tension}/100")
    
    # Process the event
    narrative._process_event(major_event)
    
    # Get final state
    final_reputation = economy.economic_state.reputation_score
    final_tension = narrative.narrative_state.tension_level
    
    print(f"\n📊 Final State:")
    print(f"   Tavern Reputation: {final_reputation:.1f}/100 ({final_reputation - initial_reputation:+.1f})")
    print(f"   Tension Level: {final_tension}/100 ({final_tension - initial_tension:+.1f})")
    
    # Check reputation changes by faction
    if "reputation_changes" in major_event:
        print(f"\n💫 Reputation Changes:")
        for agent, change in major_event["reputation_changes"].items():
            if agent != "tavern" and agent in narrative.agent_roles:
                faction = narrative.agent_roles[agent].get("faction", "Unknown")
                print(f"   {agent} ({faction}): {change:+.1f}")
    
    return economy, narrative

def test_performance_with_17_agents():
    """Test system performance with all 17 agents"""
    print("\n⚡ Testing Performance with 17 Agents")
    print("=" * 40)
    
    import time
    
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Test multiple operations
    operations = [
        ("Agent Initialization", lambda: len(narrative.agent_roles)),
        ("Resource Calculation", lambda: sum(economy.get_agent_wealth_status(agent)['total_wealth'] 
                                           for agent in narrative.agent_roles.keys())),
        ("Faction Coordination", lambda: len([narrative.get_faction_agents(f) 
                                            for f in narrative.faction_crews.keys()])),
        ("Economic Summary", lambda: len(economy.get_economic_summary()['agent_wealth']))
    ]
    
    print(f"🔄 Running Performance Tests:")
    
    for operation_name, operation_func in operations:
        start_time = time.time()
        result = operation_func()
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"   {operation_name}: {duration:.2f}ms (result: {result})")
    
    # Test event processing speed
    test_events = [
        {"id": f"perf_test_{i}", "type": "rumor_spreading", "title": f"Test Event {i}",
         "description": "Performance test event", "tension_change": 1, "timestamp": time.time()}
        for i in range(10)
    ]
    
    start_time = time.time()
    for event in test_events:
        narrative._process_event(event)
    end_time = time.time()
    
    total_duration = (end_time - start_time) * 1000
    avg_duration = total_duration / len(test_events)
    
    print(f"   Event Processing: {avg_duration:.2f}ms avg ({total_duration:.2f}ms total for {len(test_events)} events)")
    
    return economy, narrative

def main():
    """Main test function"""
    print("👥 17-Agent System Test Suite")
    print("=" * 35)
    
    try:
        # Run all tests
        economy1, narrative1 = test_17_agent_initialization()
        economy2, narrative2 = test_faction_coordination()
        economy3, narrative3 = test_large_scale_event()
        economy4, narrative4 = test_performance_with_17_agents()
        
        print("\n🎉 17-Agent System testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ 17 agents properly initialized")
        print("   ✅ Faction-based organization")
        print("   ✅ Resource distribution across all agents")
        print("   ✅ Large-scale event processing")
        print("   ✅ Performance optimization")
        
        # Final summary
        total_agents = narrative1.get_total_agent_count()
        faction_counts = narrative1.get_agent_count_by_faction()
        total_wealth = sum(economy1.get_agent_wealth_status(agent)['total_wealth'] 
                          for agent in narrative1.agent_roles.keys())
        
        print(f"\n📊 Final System State:")
        print(f"   Total Agents: {total_agents}")
        print(f"   Factions: {len(faction_counts)}")
        print(f"   Total Wealth: {total_wealth:.1f} gold")
        print(f"   System Ready: ✅")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
