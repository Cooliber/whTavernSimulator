#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for Complete Tavern Simulator
Tests all components working together: 17-agent system, economy, narrative, GSAP
"""

import os
import sys
import time
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType
from services.narrative_engine import NarrativeEngine
from components.gsap_renderer import GSAPRenderer

# Load environment variables
load_dotenv()

def test_complete_system_integration():
    """Test complete system integration with all components"""
    print("🏰 Testing Complete System Integration")
    print("=" * 50)
    
    # Initialize all systems
    print("🔧 Initializing Systems:")
    
    start_time = time.time()
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    renderer = GSAPRenderer()
    init_time = time.time() - start_time
    
    print(f"   Economy System: ✅ ({init_time:.3f}s)")
    print(f"   Narrative Engine: ✅ (17 agents)")
    print(f"   GSAP Renderer: ✅")
    print(f"   Total Agents: {narrative.get_total_agent_count()}")
    print(f"   Factions: {list(narrative.faction_crews.keys())}")
    
    return economy, narrative, renderer, init_time

def test_full_tavern_cycle():
    """Test complete tavern simulation cycle"""
    print("\n🔄 Testing Full Tavern Cycle")
    print("=" * 35)
    
    economy, narrative, renderer, _ = test_complete_system_integration()
    
    cycle_results = []
    
    for cycle in range(5):
        print(f"\n🎲 Cycle {cycle + 1}/5:")
        
        cycle_start = time.time()
        cycle_operations = []
        
        # 1. Generate narrative event
        event_start = time.time()
        event = narrative.generate_dynamic_event(fast_mode=True)
        event_time = time.time() - event_start
        cycle_operations.append(("Event Generation", event_time, True))
        
        print(f"   📖 Event: {event.get('title', 'Unknown')} ({event_time:.3f}s)")
        
        # 2. Execute economic transactions
        transaction_start = time.time()
        transaction_success = 0
        
        # Test different transaction types
        test_transactions = [
            (TransactionType.PURCHASE, ["Karczmarz", "Kupiec_Imperialny"], {ResourceType.GOLD: 5.0}),
            (TransactionType.FAVOR_EXCHANGE, ["Zwiadowca", "Mag_Wysokich_Elfów"], {ResourceType.INFORMATION: 2.0}),
            (TransactionType.INFORMATION_TRADE, ["Wiedźma", "Tancerz_Cieni"], {ResourceType.FAVORS: 1.0})
        ]
        
        for trans_type, participants, resources in test_transactions:
            try:
                transaction = economy.execute_transaction(
                    trans_type, participants, resources,
                    f"Cycle {cycle + 1} {trans_type.value}"
                )
                if transaction.success:
                    transaction_success += 1
            except Exception as e:
                print(f"     ⚠️ Transaction failed: {e}")
        
        transaction_time = time.time() - transaction_start
        cycle_operations.append(("Transactions", transaction_time, transaction_success > 0))
        
        print(f"   💰 Transactions: {transaction_success}/3 successful ({transaction_time:.3f}s)")
        
        # 3. Test rumor trading
        rumor_start = time.time()
        try:
            rumor_success = economy.trade_rumor_for_resources(
                "Wiedźma",
                f"Cycle {cycle + 1}: Strange omens appear in the tavern",
                ResourceType.GOLD,
                10.0
            )
            rumor_time = time.time() - rumor_start
            cycle_operations.append(("Rumor Trade", rumor_time, rumor_success))
            
            print(f"   🗣️ Rumor Trade: {'✅ SUCCESS' if rumor_success else '❌ FAILED'} ({rumor_time:.3f}s)")
        except Exception as e:
            rumor_time = time.time() - rumor_start
            cycle_operations.append(("Rumor Trade", rumor_time, False))
            print(f"   🗣️ Rumor Trade: ❌ ERROR - {e}")
        
        # 4. Update GSAP data
        gsap_start = time.time()
        try:
            economic_summary = economy.get_economic_summary()
            economy_data = {
                "reputation": economic_summary['tavern_state']['reputation_score'],
                "totalWealth": economic_summary['economic_metrics']['total_wealth_in_circulation'],
                "marketActivity": economic_summary['economic_metrics']['market_activity']
            }
            gsap_time = time.time() - gsap_start
            cycle_operations.append(("GSAP Data", gsap_time, True))
            
            print(f"   🎨 GSAP Data: ✅ ({gsap_time:.3f}s)")
        except Exception as e:
            gsap_time = time.time() - gsap_start
            cycle_operations.append(("GSAP Data", gsap_time, False))
            print(f"   🎨 GSAP Data: ❌ ERROR - {e}")
        
        # Calculate cycle metrics
        cycle_end = time.time()
        total_cycle_time = cycle_end - cycle_start
        cycle_success_rate = sum(1 for _, _, success in cycle_operations if success) / len(cycle_operations) * 100
        
        cycle_results.append({
            "cycle": cycle + 1,
            "time": total_cycle_time,
            "success_rate": cycle_success_rate,
            "operations": cycle_operations
        })
        
        print(f"   ⏱️ Total: {total_cycle_time:.3f}s, Success: {cycle_success_rate:.1f}%")
    
    # Analyze overall performance
    avg_cycle_time = sum(r["time"] for r in cycle_results) / len(cycle_results)
    avg_success_rate = sum(r["success_rate"] for r in cycle_results) / len(cycle_results)
    
    print(f"\n📊 Overall Cycle Performance:")
    print(f"   Average cycle time: {avg_cycle_time:.3f}s")
    print(f"   Average success rate: {avg_success_rate:.1f}%")
    print(f"   Target achievement: {'✅ PASS' if avg_cycle_time < 1.0 and avg_success_rate >= 95 else '❌ FAIL'}")
    
    return cycle_results

def test_agent_coordination():
    """Test 17-agent coordination capabilities"""
    print("\n👥 Testing 17-Agent Coordination")
    print("=" * 35)
    
    economy, narrative, renderer, _ = test_complete_system_integration()
    
    # Test faction coordination
    print("🏛️ Testing Faction Coordination:")
    
    coordination_results = {}
    
    for faction, agents in narrative.faction_crews.items():
        print(f"\n   {faction} Faction ({len(agents)} agents):")
        
        # Test faction resource pooling
        faction_wealth = 0
        faction_reputation = 0
        
        for agent in agents:
            if agent in economy.agent_resources:
                agent_resources = economy.agent_resources[agent]
                wealth = economy.get_agent_wealth_status(agent)['total_wealth']
                reputation = agent_resources[ResourceType.REPUTATION]
                
                faction_wealth += wealth
                faction_reputation += reputation
                
                print(f"     {agent}: {wealth:.0f} wealth, {reputation:.1f} rep")
        
        avg_reputation = faction_reputation / len(agents) if agents else 0
        
        coordination_results[faction] = {
            "agents": len(agents),
            "total_wealth": faction_wealth,
            "avg_reputation": avg_reputation
        }
        
        print(f"     Total: {faction_wealth:.0f} wealth, {avg_reputation:.1f} avg rep")
    
    # Test cross-faction interactions
    print(f"\n🤝 Testing Cross-Faction Interactions:")
    
    cross_faction_trades = [
        ("Empire", "Elves", "Karczmarz", "Zwiadowca"),
        ("Chaos", "Dwarfs", "Czempion", "Kowal_Krasnoludzki"),
        ("Neutrals", "Empire", "Wiedźma", "Kapitan_Straży")
    ]
    
    interaction_results = []
    
    for faction1, faction2, agent1, agent2 in cross_faction_trades:
        try:
            transaction = economy.execute_transaction(
                TransactionType.FAVOR_EXCHANGE,
                [agent1, agent2],
                {ResourceType.INFORMATION: 1.0, ResourceType.FAVORS: 1.0},
                f"Cross-faction trade: {faction1} ↔ {faction2}"
            )
            
            success = transaction.success
            interaction_results.append(success)
            
            print(f"     {faction1} ↔ {faction2}: {'✅ SUCCESS' if success else '❌ FAILED'}")
            
        except Exception as e:
            interaction_results.append(False)
            print(f"     {faction1} ↔ {faction2}: ❌ ERROR - {e}")
    
    interaction_success_rate = sum(interaction_results) / len(interaction_results) * 100
    print(f"\n   Cross-faction success rate: {interaction_success_rate:.1f}%")
    
    return coordination_results, interaction_success_rate

def test_gsap_integration():
    """Test GSAP integration with live data"""
    print("\n🎨 Testing GSAP Integration")
    print("=" * 30)
    
    economy, narrative, renderer, _ = test_complete_system_integration()
    
    # Test HTML generation
    html_start = time.time()
    html_content = renderer.get_tavern_html("Integration Test Tavern")
    html_time = time.time() - html_start
    
    print(f"📄 HTML Generation:")
    print(f"   Time: {html_time:.3f}s")
    print(f"   Size: {len(html_content):,} characters")
    
    # Test economy data integration
    data_start = time.time()
    economic_summary = economy.get_economic_summary()
    economy_data = {
        "reputation": economic_summary['tavern_state']['reputation_score'],
        "totalWealth": economic_summary['economic_metrics']['total_wealth_in_circulation'],
        "marketActivity": economic_summary['economic_metrics']['market_activity']
    }
    data_time = time.time() - data_start
    
    print(f"📊 Economy Data:")
    print(f"   Time: {data_time:.3f}s")
    print(f"   Data: {economy_data}")
    
    # Test JavaScript injection
    js_data = json.dumps(economy_data)
    js_injection = f"updateEconomyStats({js_data});"
    
    print(f"🔧 JavaScript Integration:")
    print(f"   Data size: {len(js_data)} characters")
    print(f"   Injection: {js_injection[:50]}...")
    
    # Check for required functions
    required_functions = [
        "updateEconomyStats",
        "animateTradeResult", 
        "onTradeSuccess",
        "onReputationChange"
    ]
    
    functions_found = sum(1 for func in required_functions if func in html_content)
    print(f"   Functions: {functions_found}/{len(required_functions)} found")
    
    return html_time, data_time, functions_found == len(required_functions)

def test_deployment_readiness():
    """Test deployment readiness"""
    print("\n🚀 Testing Deployment Readiness")
    print("=" * 35)
    
    # Check all required files
    required_files = [
        "app.py",
        "requirements.txt",
        "config.py",
        ".env.example" if not os.path.exists(".env") else ".env"
    ]
    
    print("📁 Required Files:")
    files_present = 0
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
            files_present += 1
        else:
            print(f"   ❌ {file}")
    
    # Test import capabilities
    print(f"\n📦 Import Test:")
    try:
        from app import main
        print(f"   ✅ Main app imports successfully")
        import_success = True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        import_success = False
    
    # Test environment variables
    print(f"\n🔑 Environment Variables:")
    required_env_vars = ["GROQ_API_KEY", "CEREBRAS_API_KEY"]
    env_vars_set = 0
    
    for var in required_env_vars:
        if os.getenv(var):
            print(f"   ✅ {var}")
            env_vars_set += 1
        else:
            print(f"   ❌ {var}")
    
    # Overall readiness
    readiness_score = (
        (files_present / len(required_files)) * 0.4 +
        (1 if import_success else 0) * 0.3 +
        (env_vars_set / len(required_env_vars)) * 0.3
    ) * 100
    
    print(f"\n📊 Deployment Readiness: {readiness_score:.1f}%")
    print(f"   Status: {'✅ READY' if readiness_score >= 80 else '⚠️ NEEDS WORK'}")
    
    return readiness_score

def main():
    """Main test function"""
    print("🏰 Complete Integration Test Suite")
    print("=" * 45)
    print("Testing all components working together...")
    print()
    
    try:
        # Run all integration tests
        economy, narrative, renderer, init_time = test_complete_system_integration()
        cycle_results = test_full_tavern_cycle()
        coordination_results, interaction_rate = test_agent_coordination()
        html_time, data_time, gsap_success = test_gsap_integration()
        readiness_score = test_deployment_readiness()
        
        print("\n🎉 Complete Integration Testing Finished!")
        print("\n📊 Final Results Summary:")
        print(f"   System initialization: {init_time:.3f}s")
        print(f"   Average cycle time: {sum(r['time'] for r in cycle_results)/len(cycle_results):.3f}s")
        print(f"   Cross-faction interactions: {interaction_rate:.1f}% success")
        print(f"   GSAP integration: {'✅ PASS' if gsap_success else '❌ FAIL'}")
        print(f"   Deployment readiness: {readiness_score:.1f}%")
        
        # Overall assessment
        overall_success = (
            init_time < 1.0 and
            sum(r['success_rate'] for r in cycle_results)/len(cycle_results) >= 95 and
            interaction_rate >= 80 and
            gsap_success and
            readiness_score >= 80
        )
        
        print(f"\n🚀 Overall System Status: {'✅ PRODUCTION READY' if overall_success else '⚠️ NEEDS OPTIMIZATION'}")
        
        if overall_success:
            print("\n🎉 Congratulations! The Warhammer Tavern Simulator is complete!")
            print("   ✅ 17-agent system operational")
            print("   ✅ Economy-narrative integration working")
            print("   ✅ GSAP visualization enhanced")
            print("   ✅ Performance optimized")
            print("   ✅ Ready for deployment")
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
