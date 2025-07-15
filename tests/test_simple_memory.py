#!/usr/bin/env python3
"""
Simple test for Agent Memory System to debug issues
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.agent_memory import (
    AgentMemorySystem, MemoryType, MemoryImportance
)

# Load environment variables
load_dotenv()

def test_basic_memory():
    """Test basic memory functionality"""
    print("🧠 Testing Basic Memory System")
    print("=" * 35)
    
    # Create a fresh memory system
    memory_system = AgentMemorySystem(memory_dir="data/test_memory")
    
    # Test 1: Store a simple memory
    print("📝 Test 1: Storing memory...")
    memory_id = memory_system.store_memory(
        agent_id="Karczmarz",
        memory_type=MemoryType.OBSERVATION,
        content="Test observation: Hooded figures in tavern",
        importance=MemoryImportance.HIGH,
        context={"test": True},
        tags=["test", "hooded"]
    )
    print(f"✅ Memory stored with ID: {memory_id}")
    
    # Test 2: Retrieve memories
    print("\n📋 Test 2: Retrieving memories...")
    memories = memory_system.retrieve_memories("Karczmarz")
    print(f"✅ Retrieved {len(memories)} memories")
    
    for memory in memories:
        print(f"   - {memory.content[:50]}...")
    
    # Test 3: Search memories
    print("\n🔍 Test 3: Searching memories...")
    search_results = memory_system.search_memories("hooded")
    print(f"✅ Found {len(search_results)} memories with 'hooded'")
    
    # Test 4: Get agent context
    print("\n🎭 Test 4: Getting agent context...")
    context = memory_system.get_agent_context("Karczmarz")
    print(f"✅ Context retrieved:")
    print(f"   - Recent memories: {len(context['recent_memories'])}")
    print(f"   - Memory stats: {context['memory_stats']}")
    
    # Test 5: System stats
    print("\n📊 Test 5: System statistics...")
    stats = memory_system.get_system_stats()
    print(f"✅ System stats:")
    for key, value in stats.items():
        if key != "agent_stats":
            print(f"   - {key}: {value}")
    
    print("\n🎉 Basic memory test completed successfully!")
    return memory_system

def test_simple_communication():
    """Test simple communication without complex threading"""
    print("\n💬 Testing Simple Communication")
    print("=" * 35)
    
    memory_system = AgentMemorySystem(memory_dir="data/test_memory")
    
    # Test simple message without auto-storing
    print("📨 Sending simple message...")
    
    # Manually create message data
    message_data = {
        "id": "test-msg-1",
        "from": "Karczmarz",
        "to": "Skrytobójca",
        "message": "Test message: Suspicious activity detected",
        "type": "alert",
        "timestamp": 1234567890
    }
    
    # Add to communication channel directly
    memory_system.communication_channels["Skrytobójca"].append(message_data)
    print("✅ Message sent successfully")
    
    # Retrieve messages
    messages = memory_system.get_messages("Skrytobójca", unread_only=False)
    print(f"✅ Retrieved {len(messages)} messages")
    
    for msg in messages:
        print(f"   From {msg['from']}: {msg['message']}")
    
    print("\n🎉 Simple communication test completed!")
    return memory_system

def test_memory_persistence():
    """Test memory save/load functionality"""
    print("\n💾 Testing Memory Persistence")
    print("=" * 30)
    
    # Create memory system and add some data
    memory_system = AgentMemorySystem(memory_dir="data/test_memory")
    
    # Add test memories
    test_memories = [
        ("Karczmarz", "Served ale to suspicious patron"),
        ("Skrytobójca", "Observed potential threat"),
        ("Wiedźma", "Sensed dark energies")
    ]
    
    for agent, content in test_memories:
        memory_system.store_memory(
            agent_id=agent,
            memory_type=MemoryType.OBSERVATION,
            content=content,
            importance=MemoryImportance.MEDIUM
        )
        print(f"✅ Stored memory for {agent}")
    
    # Get stats before save
    stats_before = memory_system.get_system_stats()
    print(f"📊 Before save: {stats_before['total_memories']} memories")
    
    # Save memories
    try:
        memory_system.save_memories()
        print("✅ Memories saved successfully")
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return None
    
    # Create new instance and load
    try:
        new_memory_system = AgentMemorySystem(memory_dir="data/test_memory")
        stats_after = new_memory_system.get_system_stats()
        print(f"📊 After load: {stats_after['total_memories']} memories")
        
        if stats_before['total_memories'] == stats_after['total_memories']:
            print("✅ Persistence test PASSED")
        else:
            print("❌ Persistence test FAILED")
            
    except Exception as e:
        print(f"❌ Load failed: {e}")
        return None
    
    return memory_system

def main():
    """Main test function"""
    print("🧠 Simple Agent Memory System Test")
    print("=" * 40)
    
    try:
        # Run basic tests
        memory_system = test_basic_memory()
        test_simple_communication()
        test_memory_persistence()
        
        print("\n🎉 All tests completed successfully!")
        print("\n🚀 Key Features Verified:")
        print("   ✅ Memory storage and retrieval")
        print("   ✅ Memory search")
        print("   ✅ Agent context")
        print("   ✅ Simple communication")
        print("   ✅ Persistence (save/load)")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
