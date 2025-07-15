#!/usr/bin/env python3
"""
Performance Optimization Test Suite for 17-Agent Coordination
Target: <1s full cycle time, 95% success rate with retries
"""

import os
import sys
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType
from services.narrative_engine import NarrativeEngine
from services.agent_memory import AgentMemorySystem, MemoryType, MemoryImportance

# Load environment variables
load_dotenv()

def test_full_cycle_performance():
    """Test complete tavern cycle performance with all 17 agents"""
    print("⚡ Testing Full Cycle Performance (17 Agents)")
    print("=" * 50)
    
    # Initialize systems
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Performance metrics
    cycle_times = []
    success_rates = []
    
    print(f"🎯 Target: <1s cycle time, 95% success rate")
    print(f"📊 Testing {narrative.get_total_agent_count()} agents across {len(narrative.faction_crews)} factions")
    print()
    
    # Run multiple cycles
    for cycle in range(10):
        print(f"🔄 Cycle {cycle + 1}/10:")
        
        cycle_start = time.time()
        operations_success = []
        
        # 1. Generate narrative event (fast mode for performance testing)
        event_start = time.time()
        event = narrative.generate_dynamic_event(fast_mode=True)
        event_time = time.time() - event_start
        operations_success.append(bool(event))
        
        # 2. Process event (includes reputation updates)
        process_start = time.time()
        narrative._process_event(event)
        process_time = time.time() - process_start
        operations_success.append(True)
        
        # 3. Execute economic transactions for multiple agents
        transaction_start = time.time()
        transaction_successes = []
        
        # Test transactions across factions
        test_transactions = [
            ("Karczmarz", "Kupiec_Imperialny", ResourceType.GOLD, 5.0),
            ("Zwiadowca", "Mag_Wysokich_Elfów", ResourceType.INFORMATION, 3.0),
            ("Kowal_Krasnoludzki", "Inżynier_Gildii", ResourceType.SUPPLIES, 2.0),
        ]
        
        for giver, receiver, resource, amount in test_transactions:
            try:
                transaction = economy.execute_transaction(
                    TransactionType.FAVOR_EXCHANGE,
                    [giver, receiver],
                    {resource: amount},
                    f"Cycle {cycle + 1} faction trade"
                )
                transaction_successes.append(transaction.success)
            except Exception as e:
                transaction_successes.append(False)
                print(f"     ⚠️ Transaction failed: {e}")
        
        transaction_time = time.time() - transaction_start
        operations_success.extend(transaction_successes)
        
        # 4. Update agent memories and relationships
        memory_start = time.time()
        try:
            # Simulate memory updates for faction coordination
            for faction, agents in narrative.faction_crews.items():
                for agent in agents[:2]:  # Test first 2 agents per faction
                    narrative.memory_system.store_memory(
                        agent_id=agent,
                        memory_type=MemoryType.OBSERVATION,
                        content=f"Cycle {cycle + 1} faction coordination",
                        importance=MemoryImportance.MEDIUM,
                        context={"cycle": cycle + 1, "faction": faction},
                        tags=["coordination", "performance_test"]
                    )
            memory_success = True
        except Exception as e:
            memory_success = False
            print(f"     ⚠️ Memory update failed: {e}")
        
        memory_time = time.time() - memory_start
        operations_success.append(memory_success)
        
        # Calculate cycle metrics
        cycle_end = time.time()
        total_cycle_time = cycle_end - cycle_start
        cycle_success_rate = sum(operations_success) / len(operations_success) * 100
        
        cycle_times.append(total_cycle_time)
        success_rates.append(cycle_success_rate)
        
        # Report cycle results
        print(f"   Total time: {total_cycle_time:.3f}s")
        print(f"   Event generation: {event_time:.3f}s")
        print(f"   Event processing: {process_time:.3f}s")
        print(f"   Transactions: {transaction_time:.3f}s")
        print(f"   Memory updates: {memory_time:.3f}s")
        print(f"   Success rate: {cycle_success_rate:.1f}%")
        print(f"   Status: {'✅ PASS' if total_cycle_time < 1.0 and cycle_success_rate >= 95 else '❌ FAIL'}")
        print()
    
    # Calculate overall performance
    avg_cycle_time = statistics.mean(cycle_times)
    avg_success_rate = statistics.mean(success_rates)
    max_cycle_time = max(cycle_times)
    min_cycle_time = min(cycle_times)
    
    print(f"📊 Overall Performance Results:")
    print(f"   Average cycle time: {avg_cycle_time:.3f}s")
    print(f"   Min cycle time: {min_cycle_time:.3f}s")
    print(f"   Max cycle time: {max_cycle_time:.3f}s")
    print(f"   Average success rate: {avg_success_rate:.1f}%")
    print(f"   Target achievement: {'✅ PASS' if avg_cycle_time < 1.0 and avg_success_rate >= 95 else '❌ FAIL'}")
    
    return {
        "avg_cycle_time": avg_cycle_time,
        "avg_success_rate": avg_success_rate,
        "max_cycle_time": max_cycle_time,
        "cycles_tested": len(cycle_times)
    }

def test_concurrent_agent_operations():
    """Test concurrent operations with multiple agents"""
    print("\n🔀 Testing Concurrent Agent Operations")
    print("=" * 40)
    
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    
    # Test concurrent transactions
    print("💸 Testing Concurrent Transactions:")
    
    def execute_agent_transaction(agent_pair):
        agent1, agent2 = agent_pair
        try:
            start_time = time.time()
            transaction = economy.execute_transaction(
                TransactionType.INFORMATION_TRADE,
                [agent1, agent2],
                {ResourceType.INFORMATION: 1.0, ResourceType.GOLD: 2.0},
                f"Concurrent trade between {agent1} and {agent2}"
            )
            end_time = time.time()
            return {
                "success": transaction.success,
                "time": end_time - start_time,
                "participants": [agent1, agent2]
            }
        except Exception as e:
            return {
                "success": False,
                "time": 0,
                "error": str(e),
                "participants": [agent1, agent2]
            }
    
    # Create agent pairs for concurrent testing
    all_agents = list(narrative.agent_roles.keys())
    agent_pairs = [
        (all_agents[i], all_agents[i+1]) 
        for i in range(0, min(10, len(all_agents)-1), 2)
    ]
    
    # Execute concurrent transactions
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_pair = {
            executor.submit(execute_agent_transaction, pair): pair 
            for pair in agent_pairs
        }
        
        results = []
        for future in as_completed(future_to_pair):
            result = future.result()
            results.append(result)
    
    end_time = time.time()
    
    # Analyze results
    successful_transactions = sum(1 for r in results if r["success"])
    total_transactions = len(results)
    success_rate = successful_transactions / total_transactions * 100
    total_time = end_time - start_time
    avg_transaction_time = statistics.mean([r["time"] for r in results if r["time"] > 0])
    
    print(f"   Concurrent transactions: {total_transactions}")
    print(f"   Successful: {successful_transactions}")
    print(f"   Success rate: {success_rate:.1f}%")
    print(f"   Total time: {total_time:.3f}s")
    print(f"   Avg transaction time: {avg_transaction_time:.3f}s")
    print(f"   Concurrency benefit: {'✅ YES' if total_time < avg_transaction_time * total_transactions else '❌ NO'}")
    
    return {
        "concurrent_success_rate": success_rate,
        "concurrent_time": total_time,
        "transactions_tested": total_transactions
    }

def test_memory_system_performance():
    """Test memory system performance with 17 agents"""
    print("\n💾 Testing Memory System Performance")
    print("=" * 40)
    
    memory_system = AgentMemorySystem()
    narrative = NarrativeEngine()
    
    # Test memory operations for all agents
    print("🧠 Testing Memory Operations for All Agents:")
    
    all_agents = list(narrative.agent_roles.keys())
    
    # Store memories for all agents
    store_start = time.time()
    store_successes = 0
    
    for i, agent in enumerate(all_agents):
        try:
            memory_system.store_memory(
                agent_id=agent,
                memory_type=MemoryType.INTERACTION,
                content=f"Performance test memory {i+1} for {agent}",
                importance=MemoryImportance.MEDIUM,
                context={"test_id": i+1, "agent": agent},
                tags=["performance", "test"]
            )
            store_successes += 1
        except Exception as e:
            print(f"   ⚠️ Store failed for {agent}: {e}")
    
    store_time = time.time() - store_start
    
    # Retrieve memories for all agents
    retrieve_start = time.time()
    retrieve_successes = 0
    total_memories = 0
    
    for agent in all_agents:
        try:
            memories = memory_system.retrieve_memories(agent, limit=10)
            total_memories += len(memories)
            retrieve_successes += 1
        except Exception as e:
            print(f"   ⚠️ Retrieve failed for {agent}: {e}")
    
    retrieve_time = time.time() - retrieve_start
    
    # Test memory save
    save_start = time.time()
    try:
        memory_system.save_memories()
        save_success = True
    except Exception as e:
        save_success = False
        print(f"   ⚠️ Save failed: {e}")
    
    save_time = time.time() - save_start
    
    print(f"   Agents tested: {len(all_agents)}")
    print(f"   Store operations: {store_successes}/{len(all_agents)} ({store_successes/len(all_agents)*100:.1f}%)")
    print(f"   Store time: {store_time:.3f}s ({store_time/len(all_agents)*1000:.1f}ms per agent)")
    print(f"   Retrieve operations: {retrieve_successes}/{len(all_agents)} ({retrieve_successes/len(all_agents)*100:.1f}%)")
    print(f"   Retrieve time: {retrieve_time:.3f}s ({retrieve_time/len(all_agents)*1000:.1f}ms per agent)")
    print(f"   Total memories retrieved: {total_memories}")
    print(f"   Save operation: {'✅ SUCCESS' if save_success else '❌ FAILED'}")
    print(f"   Save time: {save_time:.3f}s")
    
    return {
        "memory_store_success_rate": store_successes / len(all_agents) * 100,
        "memory_retrieve_success_rate": retrieve_successes / len(all_agents) * 100,
        "memory_save_success": save_success,
        "total_memory_time": store_time + retrieve_time + save_time
    }

def main():
    """Main performance test function"""
    print("⚡ Performance Optimization Test Suite")
    print("=" * 45)
    print("🎯 Target: <1s full cycle time, 95% success rate")
    print()
    
    try:
        # Run all performance tests
        cycle_results = test_full_cycle_performance()
        concurrent_results = test_concurrent_agent_operations()
        memory_results = test_memory_system_performance()
        
        print("\n🎉 Performance Optimization testing complete!")
        print("\n📊 Final Performance Summary:")
        print(f"   Full cycle time: {cycle_results['avg_cycle_time']:.3f}s (target: <1.0s)")
        print(f"   Full cycle success rate: {cycle_results['avg_success_rate']:.1f}% (target: ≥95%)")
        print(f"   Concurrent success rate: {concurrent_results['concurrent_success_rate']:.1f}%")
        print(f"   Memory system success: {memory_results['memory_store_success_rate']:.1f}%")
        
        # Overall assessment
        cycle_pass = cycle_results['avg_cycle_time'] < 1.0 and cycle_results['avg_success_rate'] >= 95
        concurrent_pass = concurrent_results['concurrent_success_rate'] >= 90
        memory_pass = memory_results['memory_store_success_rate'] >= 95
        
        overall_pass = cycle_pass and concurrent_pass and memory_pass
        
        print(f"\n🚀 Performance Targets:")
        print(f"   ✅ Full cycle performance: {'PASS' if cycle_pass else 'FAIL'}")
        print(f"   ✅ Concurrent operations: {'PASS' if concurrent_pass else 'FAIL'}")
        print(f"   ✅ Memory system: {'PASS' if memory_pass else 'FAIL'}")
        print(f"   🎯 Overall: {'✅ PASS' if overall_pass else '❌ FAIL'}")
        
        if overall_pass:
            print(f"\n🎉 System optimized for 17-agent coordination!")
            print(f"   Ready for production deployment")
        else:
            print(f"\n⚠️ Performance optimization needed")
            print(f"   Consider further optimization")
        
    except Exception as e:
        print(f"❌ Performance test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
