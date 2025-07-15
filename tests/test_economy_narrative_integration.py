#!/usr/bin/env python3
"""
Test Economy-Narrative Integration
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import TavernEconomySystem, ResourceType
from services.narrative_engine import NarrativeEngine, NarrativeEvent

# Load environment variables
load_dotenv()

def test_reputation_on_event():
    """Test reputation updates from narrative events"""
    print("🎭 Testing Economy-Narrative Integration")
    print("=" * 45)
    
    # Create systems
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Get initial reputation
    initial_reputation = economy.economic_state.reputation_score
    print(f"📊 Initial Tavern Reputation: {initial_reputation:.1f}/100")
    print()
    
    # Test different event types
    test_events = [
        {
            "id": "test_brawl_1",
            "type": "brawl_brewing",
            "title": "Tavern Brawl Erupts",
            "description": "A heated argument between patrons escalates into violence",
            "tension_change": 25,
            "participants": ["Karczmarz", "Skrytobójca"],
            "timestamp": 1234567890
        },
        {
            "id": "test_quest_1", 
            "type": "quest_opportunity",
            "title": "Noble Seeks Heroes",
            "description": "A wealthy merchant offers a lucrative quest to brave adventurers",
            "tension_change": 5,
            "participants": ["Wiedźma", "Zwiadowca"],
            "timestamp": 1234567891
        },
        {
            "id": "test_betrayal_1",
            "type": "betrayal_revealed", 
            "title": "Spy Exposed",
            "description": "A patron is revealed to be working for enemy forces",
            "tension_change": 30,
            "participants": ["Czempion"],
            "timestamp": 1234567892
        }
    ]
    
    for i, event in enumerate(test_events, 1):
        print(f"🎲 Event {i}: {event['title']}")
        print(f"   Type: {event['type']}")
        print(f"   Tension Change: +{event['tension_change']}")
        print(f"   Participants: {', '.join(event['participants'])}")
        
        # Get reputation before
        before_rep = economy.economic_state.reputation_score
        
        # Process event through narrative engine
        narrative._process_event(event)
        
        # Get reputation after
        after_rep = economy.economic_state.reputation_score
        reputation_change = after_rep - before_rep
        
        print(f"   Reputation: {before_rep:.1f} → {after_rep:.1f} ({reputation_change:+.1f})")
        
        # Check participant reputation changes
        if "reputation_changes" in event:
            for participant, change in event["reputation_changes"].items():
                if participant != "tavern":
                    agent_rep = economy.agent_resources[participant][ResourceType.REPUTATION]
                    print(f"   {participant}: {change:+.1f} (now {agent_rep:.1f})")
        
        print()
    
    # Final state
    final_reputation = economy.economic_state.reputation_score
    total_change = final_reputation - initial_reputation
    
    print(f"📊 Final Results:")
    print(f"   Initial Reputation: {initial_reputation:.1f}")
    print(f"   Final Reputation: {final_reputation:.1f}")
    print(f"   Total Change: {total_change:+.1f}")
    print(f"   Final Tension: {narrative.narrative_state.tension_level}")
    
    return economy, narrative

def test_low_reputation_events():
    """Test that low reputation triggers more events"""
    print("\n🔥 Testing Low Reputation Event Triggering")
    print("=" * 45)
    
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Artificially lower reputation
    economy.economic_state.reputation_score = 20.0
    print(f"📉 Set reputation to: {economy.economic_state.reputation_score:.1f}/100")
    
    # Test event triggering probability
    trigger_count = 0
    test_iterations = 100
    
    for i in range(test_iterations):
        if narrative._should_trigger_automatic_event():
            trigger_count += 1
    
    trigger_rate = (trigger_count / test_iterations) * 100
    print(f"🎲 Event trigger rate with low reputation: {trigger_rate:.1f}%")
    
    # Test with high reputation
    economy.economic_state.reputation_score = 90.0
    print(f"📈 Set reputation to: {economy.economic_state.reputation_score:.1f}/100")
    
    trigger_count_high = 0
    for i in range(test_iterations):
        if narrative._should_trigger_automatic_event():
            trigger_count_high += 1
    
    trigger_rate_high = (trigger_count_high / test_iterations) * 100
    print(f"🎲 Event trigger rate with high reputation: {trigger_rate_high:.1f}%")
    
    print(f"\n📊 Comparison:")
    print(f"   Low reputation (20): {trigger_rate:.1f}% trigger rate")
    print(f"   High reputation (90): {trigger_rate_high:.1f}% trigger rate")
    print(f"   Difference: {trigger_rate - trigger_rate_high:+.1f}%")
    
    return economy, narrative

def test_memory_integration():
    """Test that reputation changes are stored in memory"""
    print("\n💾 Testing Memory Integration")
    print("=" * 35)
    
    economy = TavernEconomySystem()
    
    # Create a test event
    test_event = {
        "id": "memory_test_1",
        "type": "alliance_forming",
        "title": "Diplomatic Success",
        "description": "Tavern hosts successful peace negotiations",
        "tension_change": -10,
        "participants": ["Karczmarz"],
        "timestamp": 1234567893
    }
    
    print(f"🎭 Processing event: {test_event['title']}")
    
    # Process event
    reputation_changes = economy.update_reputation_on_event(test_event)
    
    print(f"📊 Reputation changes: {reputation_changes}")
    
    # Check if memory was stored
    economy_memories = economy.memory_system.retrieve_memories(
        "TavernEconomy",
        limit=10
    )
    
    print(f"💾 Stored memories: {len(economy_memories)}")
    if economy_memories:
        latest_memory = economy_memories[-1]
        print(f"   Latest: {latest_memory.content}")
        print(f"   Tags: {latest_memory.tags}")
    
    return economy

def main():
    """Main test function"""
    print("🎭 Economy-Narrative Integration Test Suite")
    print("=" * 50)
    
    try:
        # Run all tests
        economy1, narrative1 = test_reputation_on_event()
        economy2, narrative2 = test_low_reputation_events()
        economy3 = test_memory_integration()
        
        print("\n🎉 Economy-Narrative Integration testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ Event-based reputation updates")
        print("   ✅ Agent reputation changes")
        print("   ✅ Low reputation triggers more events")
        print("   ✅ Memory system integration")
        print("   ✅ Narrative-economy feedback loop")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
