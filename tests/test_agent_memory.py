#!/usr/bin/env python3
"""
Test Agent Memory System for persistent context and cross-agent communication
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.agent_memory import (
    AgentMemorySystem, MemoryType, MemoryImportance, 
    agent_memory_system, cleanup_memory_system
)

# Load environment variables
load_dotenv()

def test_memory_storage_and_retrieval():
    """Test basic memory storage and retrieval"""
    print("🧠 Testing Memory Storage and Retrieval")
    print("=" * 45)
    
    memory_system = agent_memory_system
    
    # Store various types of memories for Karczmarz
    memories = [
        {
            "type": MemoryType.OBSERVATION,
            "content": "Hooded figures entered tavern at midnight, whispering in corner",
            "importance": MemoryImportance.HIGH,
            "context": {"time": "midnight", "location": "corner_table", "patron_count": 8},
            "tags": ["suspicious", "hooded_figures", "midnight"]
        },
        {
            "type": MemoryType.INTERACTION,
            "content": "Served ale to merchant who mentioned missing caravan",
            "importance": MemoryImportance.MEDIUM,
            "context": {"patron_type": "merchant", "topic": "missing_caravan"},
            "tags": ["merchant", "caravan", "missing"]
        },
        {
            "type": MemoryType.EMOTION,
            "content": "Feeling uneasy about the increasing tension in tavern",
            "importance": MemoryImportance.MEDIUM,
            "context": {"tension_level": 7, "emotional_state": "uneasy"},
            "tags": ["tension", "unease", "atmosphere"]
        },
        {
            "type": MemoryType.THREAT,
            "content": "Noticed patron with concealed weapon under cloak",
            "importance": MemoryImportance.CRITICAL,
            "context": {"threat_level": 8, "weapon_type": "unknown", "patron_description": "tall_hooded"},
            "tags": ["weapon", "threat", "concealed"]
        }
    ]
    
    stored_ids = []
    for memory_data in memories:
        memory_id = memory_system.store_memory(
            agent_id="Karczmarz",
            memory_type=memory_data["type"],
            content=memory_data["content"],
            importance=memory_data["importance"],
            context=memory_data["context"],
            tags=memory_data["tags"]
        )
        stored_ids.append(memory_id)
        print(f"✅ Stored memory: {memory_data['content'][:50]}...")
    
    # Test retrieval with different filters
    print(f"\n📋 Testing Memory Retrieval:")
    
    # Get all memories
    all_memories = memory_system.retrieve_memories("Karczmarz")
    print(f"   All memories: {len(all_memories)} found")
    
    # Get only high importance memories
    high_importance = memory_system.retrieve_memories(
        "Karczmarz", 
        importance_threshold=MemoryImportance.HIGH
    )
    print(f"   High importance: {len(high_importance)} found")
    
    # Get only threat memories
    threat_memories = memory_system.retrieve_memories(
        "Karczmarz",
        memory_type=MemoryType.THREAT
    )
    print(f"   Threat memories: {len(threat_memories)} found")
    
    return memory_system, stored_ids

def test_cross_agent_communication():
    """Test communication between agents"""
    print("\n💬 Testing Cross-Agent Communication")
    print("=" * 40)
    
    memory_system = agent_memory_system
    
    # Test message sending
    messages = [
        ("Karczmarz", "Skrytobójca", "Suspicious hooded figures in corner table", "alert"),
        ("Skrytobójca", "Zwiadowca", "Investigating potential threats, maintain watch", "coordination"),
        ("Zwiadowca", "Karczmarz", "Confirmed: armed individuals, recommend caution", "report"),
        ("Wiedźma", "Karczmarz", "Dark energies surround the hooded ones", "mystical_insight")
    ]
    
    for from_agent, to_agent, message, msg_type in messages:
        success = memory_system.send_message(from_agent, to_agent, message, msg_type)
        print(f"✅ {from_agent} → {to_agent}: {message[:40]}...")
    
    # Test message retrieval
    print(f"\n📨 Message Retrieval:")
    for agent in ["Karczmarz", "Skrytobójca", "Zwiadowca", "Wiedźma"]:
        messages = memory_system.get_messages(agent)
        print(f"   {agent}: {len(messages)} unread messages")
        for msg in messages:
            print(f"      From {msg['from']}: {msg['message'][:30]}...")
    
    return memory_system

def test_memory_sharing():
    """Test memory sharing between agents"""
    print("\n🤝 Testing Memory Sharing")
    print("=" * 30)
    
    memory_system = agent_memory_system
    
    # Store a critical memory for Skrytobójca
    critical_memory_id = memory_system.store_memory(
        agent_id="Skrytobójca",
        memory_type=MemoryType.THREAT,
        content="Identified hooded figures as Chaos cultists with ritual daggers",
        importance=MemoryImportance.CRITICAL,
        context={"threat_level": 9, "cult_type": "chaos", "weapons": "ritual_daggers"},
        related_agents=["Karczmarz", "Zwiadowca", "Wiedźma"],
        tags=["chaos", "cultists", "ritual", "daggers", "critical"]
    )
    
    print(f"✅ Stored critical memory: {critical_memory_id}")
    
    # Share the memory with other agents
    success = memory_system.share_memory(
        "Skrytobójca", 
        critical_memory_id, 
        ["Karczmarz", "Zwiadowca", "Wiedźma"]
    )
    
    print(f"✅ Memory shared: {success}")
    
    # Check if other agents can access the shared memory
    for agent in ["Karczmarz", "Zwiadowca", "Wiedźma"]:
        shared_memories = memory_system.retrieve_memories(agent, include_shared=True)
        shared_count = sum(1 for m in shared_memories if "[SHARED]" in m.content)
        print(f"   {agent}: {shared_count} shared memories accessible")
    
    return memory_system

def test_relationship_tracking():
    """Test relationship tracking between agents"""
    print("\n❤️ Testing Relationship Tracking")
    print("=" * 35)
    
    memory_system = agent_memory_system
    
    # Simulate various interactions that affect relationships
    interactions = [
        ("Karczmarz", "Skrytobójca", 0.2, "Shared critical information"),
        ("Skrytobójca", "Zwiadowca", 0.3, "Successful coordination"),
        ("Wiedźma", "Karczmarz", 0.1, "Provided mystical insight"),
        ("Zwiadowca", "Skrytobójca", 0.2, "Confirmed threat assessment"),
        ("Karczmarz", "Wiedźma", 0.1, "Appreciated mystical help")
    ]
    
    for agent1, agent2, change, reason in interactions:
        memory_system.update_relationship(agent1, agent2, change)
        print(f"✅ {agent1} ↔ {agent2}: +{change} ({reason})")
    
    # Display relationship matrix
    print(f"\n📊 Relationship Matrix:")
    agents = ["Karczmarz", "Skrytobójca", "Zwiadowca", "Wiedźma"]
    
    for agent1 in agents:
        relationships = memory_system.agent_relationships[agent1]
        print(f"   {agent1}:")
        for agent2 in agents:
            if agent1 != agent2:
                relationship = relationships.get(agent2, 0.0)
                print(f"      → {agent2}: {relationship:.2f}")
    
    return memory_system

def test_memory_search():
    """Test memory search functionality"""
    print("\n🔍 Testing Memory Search")
    print("=" * 25)
    
    memory_system = agent_memory_system
    
    # Search for specific terms
    search_terms = [
        "hooded figures",
        "threat",
        "chaos",
        "weapon",
        "caravan"
    ]
    
    for term in search_terms:
        results = memory_system.search_memories(term)
        print(f"🔍 '{term}': {len(results)} results found")
        
        for result in results[:2]:  # Show first 2 results
            print(f"   {result.agent_id}: {result.content[:50]}...")
    
    # Search in specific agent's memories
    print(f"\n🎯 Agent-specific search:")
    karczmarz_threats = memory_system.search_memories(
        "threat", 
        agent_id="Karczmarz",
        memory_types=[MemoryType.THREAT, MemoryType.OBSERVATION]
    )
    print(f"   Karczmarz threat memories: {len(karczmarz_threats)} found")
    
    return memory_system

def test_agent_context():
    """Test comprehensive agent context retrieval"""
    print("\n🎭 Testing Agent Context Retrieval")
    print("=" * 40)
    
    memory_system = agent_memory_system
    
    # Get comprehensive context for each agent
    agents = ["Karczmarz", "Skrytobójca", "Zwiadowca", "Wiedźma"]
    
    for agent in agents:
        context = memory_system.get_agent_context(agent, context_size=10)
        
        print(f"📋 {agent} Context:")
        print(f"   Recent memories: {len(context['recent_memories'])}")
        print(f"   Recent messages: {len(context['recent_messages'])}")
        print(f"   Relationships: {len(context['relationships'])}")
        print(f"   Total memories: {context['memory_stats']['total_memories']}")
        print(f"   Avg importance: {context['memory_stats']['avg_importance']:.2f}")
        print()
    
    return memory_system

def test_persistence():
    """Test memory persistence (save/load)"""
    print("💾 Testing Memory Persistence")
    print("=" * 30)
    
    memory_system = agent_memory_system
    
    # Get current stats
    stats_before = memory_system.get_system_stats()
    print(f"📊 Before save:")
    print(f"   Total memories: {stats_before['total_memories']}")
    print(f"   Total agents: {stats_before['total_agents']}")
    print(f"   Shared memories: {stats_before['total_shared_memories']}")
    
    # Save memories
    memory_system.save_memories()
    print(f"✅ Memories saved to disk")
    
    # Create new instance and load
    new_memory_system = AgentMemorySystem()
    stats_after = new_memory_system.get_system_stats()
    
    print(f"\n📊 After load:")
    print(f"   Total memories: {stats_after['total_memories']}")
    print(f"   Total agents: {stats_after['total_agents']}")
    print(f"   Shared memories: {stats_after['total_shared_memories']}")
    
    # Verify data integrity
    success = (stats_before['total_memories'] == stats_after['total_memories'] and
              stats_before['total_agents'] == stats_after['total_agents'])
    
    print(f"✅ Persistence test: {'PASSED' if success else 'FAILED'}")
    
    return memory_system

def main():
    """Main test function"""
    print("🧠 Agent Memory System Test Suite")
    print("=" * 45)
    
    try:
        # Run all tests
        memory_system, stored_ids = test_memory_storage_and_retrieval()
        test_cross_agent_communication()
        test_memory_sharing()
        test_relationship_tracking()
        test_memory_search()
        test_agent_context()
        test_persistence()
        
        # Final system statistics
        print("\n📊 Final System Statistics")
        print("=" * 30)
        final_stats = memory_system.get_system_stats()
        
        for key, value in final_stats.items():
            if key != "agent_stats":
                print(f"   {key}: {value}")
        
        print("\n🎉 Agent Memory System testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ Memory storage and retrieval")
        print("   ✅ Cross-agent communication")
        print("   ✅ Memory sharing")
        print("   ✅ Relationship tracking")
        print("   ✅ Memory search")
        print("   ✅ Agent context retrieval")
        print("   ✅ Persistence (save/load)")
        
    finally:
        # Cleanup
        cleanup_memory_system()

if __name__ == "__main__":
    main()
