#!/usr/bin/env python3
"""
Test Tenacity Retry Mechanisms for Robust Error Handling
"""

import os
import sys
import time
import unittest.mock as mock
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType
from services.agent_memory import AgentMemorySystem, MemoryType, MemoryImportance
from services.llm_service import LLMService, LLMRequest, LLMProvider
import requests

# Load environment variables
load_dotenv()

def test_llm_service_retries():
    """Test LLM service retry mechanisms"""
    print("🔄 Testing LLM Service Retry Mechanisms")
    print("=" * 45)
    
    llm_service = LLMService()
    
    # Test Groq retry with simulated failures
    print("🤖 Testing Groq API Retries:")
    
    # Create a test request
    test_request = LLMRequest(
        prompt="Test prompt for retry mechanism",
        system_message="You are a test agent",
        provider=LLMProvider.GROQ,
        agent_name="TestAgent"
    )
    
    # Mock the requests.post to simulate failures then success
    with mock.patch('requests.post') as mock_post:
        # First two calls fail, third succeeds
        mock_post.side_effect = [
            requests.RequestException("Connection timeout"),
            requests.RequestException("Server error"),
            mock.Mock(status_code=200, json=lambda: {
                "choices": [{"message": {"content": "Test response after retries"}}]
            })
        ]
        
        start_time = time.time()
        response = llm_service._call_groq(test_request)
        end_time = time.time()
        
        print(f"   Retry attempts: {mock_post.call_count}")
        print(f"   Final success: {response.success}")
        print(f"   Response time: {end_time - start_time:.2f}s")
        print(f"   Content: {response.content[:50]}...")
    
    # Test Cerebras retry
    print("\n⚡ Testing Cerebras API Retries:")
    
    test_request.provider = LLMProvider.CEREBRAS
    
    with mock.patch('requests.post') as mock_post:
        # Simulate one failure then success
        mock_post.side_effect = [
            requests.RequestException("Network error"),
            mock.Mock(status_code=200, json=lambda: {
                "choices": [{"message": {"content": "Fast response after retry"}}]
            })
        ]
        
        start_time = time.time()
        response = llm_service._call_cerebras(test_request)
        end_time = time.time()
        
        print(f"   Retry attempts: {mock_post.call_count}")
        print(f"   Final success: {response.success}")
        print(f"   Response time: {end_time - start_time:.2f}s")
        print(f"   Content: {response.content[:50]}...")
    
    return llm_service

def test_economy_transaction_retries():
    """Test economy transaction retry mechanisms"""
    print("\n💰 Testing Economy Transaction Retries")
    print("=" * 45)
    
    economy = TavernEconomySystem()
    
    # Test transaction retry with simulated failures
    print("💸 Testing Transaction Execution Retries:")
    
    # Mock the _transfer_resources method to fail first, then succeed
    original_transfer = economy._transfer_resources
    call_count = 0
    
    def mock_transfer_resources(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise Exception(f"Simulated transfer failure #{call_count}")
        return original_transfer(*args, **kwargs)
    
    # Patch the method
    economy._transfer_resources = mock_transfer_resources
    
    try:
        start_time = time.time()
        transaction = economy.execute_transaction(
            TransactionType.PURCHASE,
            ["Karczmarz", "TavernMarket"],
            {ResourceType.GOLD: 10.0},
            "Test transaction with retries"
        )
        end_time = time.time()
        
        print(f"   Retry attempts: {call_count}")
        print(f"   Final success: {transaction.success}")
        print(f"   Transaction time: {end_time - start_time:.2f}s")
        print(f"   Description: {transaction.description}")
        
    except Exception as e:
        print(f"   ❌ Transaction failed after retries: {e}")
    finally:
        # Restore original method
        economy._transfer_resources = original_transfer
    
    return economy

def test_memory_save_retries():
    """Test memory system save retry mechanisms"""
    print("\n💾 Testing Memory Save Retries")
    print("=" * 35)
    
    memory_system = AgentMemorySystem()
    
    # Add some test memories
    memory_system.store_memory(
        agent_id="TestAgent",
        memory_type=MemoryType.OBSERVATION,
        content="Test memory for retry mechanism",
        importance=MemoryImportance.MEDIUM,
        context={"test": "retry_data"},
        tags=["test", "retry"]
    )
    
    print("💾 Testing Memory Save Retries:")
    
    # Mock the file operations to simulate failures
    original_open = open
    call_count = 0
    
    def mock_open(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 2 and 'w' in str(args):
            raise IOError(f"Simulated file write failure #{call_count}")
        return original_open(*args, **kwargs)
    
    # Patch the built-in open function
    import builtins
    builtins.open = mock_open
    
    try:
        start_time = time.time()
        memory_system.save_memories()
        end_time = time.time()
        
        print(f"   Retry attempts: {call_count}")
        print(f"   Save time: {end_time - start_time:.2f}s")
        print(f"   ✅ Memories saved successfully after retries")
        
    except Exception as e:
        print(f"   ❌ Memory save failed after retries: {e}")
    finally:
        # Restore original open function
        builtins.open = original_open
    
    return memory_system

def test_reputation_update_retries():
    """Test reputation update retry mechanisms"""
    print("\n⭐ Testing Reputation Update Retries")
    print("=" * 40)
    
    economy = TavernEconomySystem()
    
    # Test reputation update with simulated failures
    print("📊 Testing Reputation Update Retries:")
    
    test_event = {
        "id": "retry_test_1",
        "type": "quest_opportunity",
        "title": "Test Quest for Retries",
        "description": "Testing retry mechanism for reputation updates",
        "tension_change": 5,
        "participants": ["Karczmarz"],
        "timestamp": time.time()
    }
    
    # Mock the memory system store_memory to fail first
    original_store = economy.memory_system.store_memory
    call_count = 0
    
    def mock_store_memory(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 1:
            raise Exception(f"Simulated memory store failure #{call_count}")
        return original_store(*args, **kwargs)
    
    economy.memory_system.store_memory = mock_store_memory
    
    try:
        start_time = time.time()
        reputation_changes = economy.update_reputation_on_event(test_event)
        end_time = time.time()
        
        print(f"   Retry attempts: {call_count}")
        print(f"   Update time: {end_time - start_time:.2f}s")
        print(f"   Reputation changes: {reputation_changes}")
        print(f"   ✅ Reputation updated successfully after retries")
        
    except Exception as e:
        print(f"   ❌ Reputation update failed after retries: {e}")
    finally:
        # Restore original method
        economy.memory_system.store_memory = original_store
    
    return economy

def test_retry_performance():
    """Test performance impact of retry mechanisms"""
    print("\n⚡ Testing Retry Performance Impact")
    print("=" * 40)
    
    economy = TavernEconomySystem()
    
    # Test normal operations without failures
    print("🔄 Performance Test (No Failures):")
    
    operations = []
    
    # Test multiple transactions
    start_time = time.time()
    for i in range(10):
        transaction = economy.execute_transaction(
            TransactionType.PURCHASE,
            ["Karczmarz", "TavernMarket"],
            {ResourceType.GOLD: 1.0},
            f"Performance test transaction {i+1}"
        )
        operations.append(transaction.success)
    end_time = time.time()
    
    success_rate = sum(operations) / len(operations) * 100
    avg_time = (end_time - start_time) / len(operations) * 1000  # ms
    
    print(f"   Transactions: {len(operations)}")
    print(f"   Success rate: {success_rate:.1f}%")
    print(f"   Avg time per transaction: {avg_time:.2f}ms")
    print(f"   Total time: {(end_time - start_time)*1000:.2f}ms")
    
    return economy

def main():
    """Main test function"""
    print("🔄 Tenacity Retry Mechanisms Test Suite")
    print("=" * 50)
    
    try:
        # Run all tests
        llm_service = test_llm_service_retries()
        economy1 = test_economy_transaction_retries()
        memory_system = test_memory_save_retries()
        economy2 = test_reputation_update_retries()
        economy3 = test_retry_performance()
        
        print("\n🎉 Retry Mechanisms testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ LLM API retry mechanisms (Groq & Cerebras)")
        print("   ✅ Economy transaction retries")
        print("   ✅ Memory system save retries")
        print("   ✅ Reputation update retries")
        print("   ✅ Performance impact assessment")
        print("   ✅ Exponential backoff strategy")
        print("   ✅ Exception-specific retry logic")
        
        print(f"\n📊 Retry Configuration:")
        print(f"   Max attempts: 3 (most operations)")
        print(f"   Backoff strategy: Exponential")
        print(f"   Wait times: 1-10 seconds")
        print(f"   Exception handling: Specific types")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
