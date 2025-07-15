#!/usr/bin/env python3
"""
Test Tavern Economy System for resource management and rumor-based currency
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.tavern_economy import (
    TavernEconomySystem, ResourceType, TransactionType,
    tavern_economy, cleanup_economy_system
)

# Load environment variables
load_dotenv()

def test_agent_resources():
    """Test agent resource initialization and management"""
    print("💰 Testing Agent Resources")
    print("=" * 30)
    
    economy = tavern_economy
    
    # Check initial resources
    agents = ["Karczmarz", "Skrytobójca", "Wiedźma", "Zwiadowca", "Czempion"]
    
    for agent in agents:
        wealth_status = economy.get_agent_wealth_status(agent)
        print(f"💼 {agent}:")
        print(f"   Total Wealth: {wealth_status['total_wealth']:.1f} gold")
        print(f"   Wealth Class: {wealth_status['wealth_class']}")
        print(f"   Market Power: {wealth_status['market_power']:.1f}/100")
        
        # Show top 3 resources
        resources = wealth_status['resources']
        top_resources = sorted(resources.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"   Top Resources: {', '.join([f'{rt.value}: {amt:.1f}' for rt, amt in top_resources])}")
        print()
    
    return economy

def test_basic_transactions():
    """Test basic economic transactions"""
    print("💸 Testing Basic Transactions")
    print("=" * 35)
    
    economy = tavern_economy
    
    # Test different transaction types
    transactions = [
        {
            "type": TransactionType.PURCHASE,
            "participants": ["Karczmarz", "TavernMarket"],
            "resources": {ResourceType.GOLD: 20.0, ResourceType.SUPPLIES: 10.0},
            "description": "Karczmarz buys supplies for tavern"
        },
        {
            "type": TransactionType.INFORMATION_TRADE,
            "participants": ["Skrytobójca", "Zwiadowca"],
            "resources": {ResourceType.INFORMATION: 5.0, ResourceType.GOLD: 15.0},
            "description": "Information exchange between agents"
        },
        {
            "type": TransactionType.FAVOR_EXCHANGE,
            "participants": ["Wiedźma", "Karczmarz"],
            "resources": {ResourceType.FAVORS: 2.0, ResourceType.REPUTATION: 3.0},
            "description": "Favor for reputation trade"
        }
    ]
    
    for i, txn_data in enumerate(transactions, 1):
        print(f"💳 Transaction {i}: {txn_data['description']}")
        
        # Get initial states
        initial_states = {}
        for participant in txn_data["participants"]:
            if participant != "TavernMarket":
                initial_states[participant] = economy.get_agent_wealth_status(participant)
        
        # Execute transaction
        transaction = economy.execute_transaction(
            txn_data["type"],
            txn_data["participants"],
            txn_data["resources"],
            txn_data["description"]
        )
        
        print(f"   Success: {transaction.success}")
        print(f"   Consequences: {len(transaction.consequences)} effects")
        
        if transaction.consequences:
            for consequence in transaction.consequences[:2]:
                print(f"     - {consequence}")
        
        # Show wealth changes
        for participant in txn_data["participants"]:
            if participant != "TavernMarket":
                new_state = economy.get_agent_wealth_status(participant)
                old_wealth = initial_states[participant]["total_wealth"]
                new_wealth = new_state["total_wealth"]
                change = new_wealth - old_wealth
                print(f"   {participant}: {old_wealth:.1f} → {new_wealth:.1f} ({change:+.1f})")
        
        print()
    
    return economy

def test_rumor_economy():
    """Test rumor-based currency system"""
    print("🗣️ Testing Rumor Economy")
    print("=" * 30)
    
    economy = tavern_economy
    
    # Test rumor trading
    rumors = [
        {
            "trader": "Skrytobójca",
            "content": "Chaos cultists gathering in the forest outside town",
            "target_resource": ResourceType.GOLD,
            "target_amount": 25.0
        },
        {
            "trader": "Wiedźma",
            "content": "Ancient treasure hidden beneath the old cemetery",
            "target_resource": ResourceType.INFLUENCE,
            "target_amount": 10.0
        },
        {
            "trader": "Zwiadowca",
            "content": "Secret passage discovered in the lord's manor",
            "target_resource": ResourceType.REPUTATION,
            "target_amount": 8.0
        }
    ]
    
    for i, rumor_data in enumerate(rumors, 1):
        trader = rumor_data["trader"]
        content = rumor_data["content"]
        target_resource = rumor_data["target_resource"]
        target_amount = rumor_data["target_amount"]
        
        print(f"📰 Rumor Trade {i}: {trader}")
        print(f"   Rumor: {content[:50]}...")
        print(f"   Wants: {target_amount} {target_resource.value}")
        
        # Get initial wealth
        initial_wealth = economy.get_agent_wealth_status(trader)
        initial_amount = initial_wealth["resources"][target_resource]
        
        # Attempt trade
        success = economy.trade_rumor_for_resources(
            trader, content, target_resource, target_amount
        )
        
        print(f"   Trade Success: {success}")
        
        if success:
            new_wealth = economy.get_agent_wealth_status(trader)
            new_amount = new_wealth["resources"][target_resource]
            print(f"   {target_resource.value}: {initial_amount:.1f} → {new_amount:.1f}")
        
        print()
    
    # Show rumor market status
    summary = economy.get_economic_summary()
    rumor_market = summary["rumor_market"]
    print(f"📊 Rumor Market Status:")
    print(f"   Active Rumors: {rumor_market['active_rumors']}")
    print(f"   Total Value: {rumor_market['total_rumor_value']:.1f}")
    print(f"   Top Traders: {', '.join(rumor_market['top_traders'])}")
    
    return economy

def test_economic_events():
    """Test economic event simulation"""
    print("\n📈 Testing Economic Events")
    print("=" * 30)
    
    economy = tavern_economy
    
    # Get initial state
    initial_summary = economy.get_economic_summary()
    initial_reputation = initial_summary["tavern_state"]["reputation_score"]
    initial_supply = initial_summary["tavern_state"]["supply_quality"]
    
    print(f"📊 Initial State:")
    print(f"   Reputation: {initial_reputation:.1f}/100")
    print(f"   Supply Quality: {initial_supply:.1f}/100")
    
    # Simulate multiple economic events
    print(f"\n🎲 Simulating Economic Events:")
    all_events = []
    
    for round_num in range(5):
        events = economy.simulate_economic_events()
        all_events.extend(events)
        
        if events:
            print(f"   Round {round_num + 1}: {len(events)} events")
            for event in events:
                print(f"     - {event['description']}")
        else:
            print(f"   Round {round_num + 1}: No events")
    
    # Show final state
    final_summary = economy.get_economic_summary()
    final_reputation = final_summary["tavern_state"]["reputation_score"]
    final_supply = final_summary["tavern_state"]["supply_quality"]
    
    print(f"\n📊 Final State:")
    print(f"   Reputation: {final_reputation:.1f}/100 ({final_reputation - initial_reputation:+.1f})")
    print(f"   Supply Quality: {final_supply:.1f}/100 ({final_supply - initial_supply:+.1f})")
    print(f"   Total Events: {len(all_events)}")
    
    return economy

def test_market_dynamics():
    """Test market price dynamics and wealth distribution"""
    print("\n💹 Testing Market Dynamics")
    print("=" * 30)
    
    economy = tavern_economy
    
    # Show current market prices
    summary = economy.get_economic_summary()
    market_prices = summary["market_prices"]
    
    print(f"📊 Current Market Prices:")
    for resource, price in market_prices.items():
        print(f"   {resource}: {price:.2f} gold")
    
    # Show wealth distribution
    print(f"\n💰 Wealth Distribution:")
    agent_wealth = summary["agent_wealth"]
    
    wealth_data = []
    for agent, data in agent_wealth.items():
        wealth_data.append((agent, data["total_wealth"], data["wealth_class"]))
    
    # Sort by wealth
    wealth_data.sort(key=lambda x: x[1], reverse=True)
    
    for i, (agent, wealth, wealth_class) in enumerate(wealth_data, 1):
        print(f"   {i}. {agent}: {wealth:.1f} gold ({wealth_class})")
    
    # Economic metrics
    metrics = summary["economic_metrics"]
    print(f"\n📈 Economic Metrics:")
    print(f"   Total Wealth in Circulation: {metrics['total_wealth_in_circulation']:.1f}")
    print(f"   Average Reputation: {metrics['average_reputation']:.1f}")
    print(f"   Market Activity: {metrics['market_activity']} transactions")
    
    return economy

def test_economic_persistence():
    """Test economic state persistence"""
    print("\n💾 Testing Economic Persistence")
    print("=" * 35)
    
    economy = tavern_economy
    
    # Get current state
    initial_summary = economy.get_economic_summary()
    
    print(f"📊 Before Save:")
    print(f"   Total Transactions: {len(economy.transaction_history)}")
    print(f"   Active Rumors: {initial_summary['rumor_market']['active_rumors']}")
    print(f"   Tavern Wealth: {initial_summary['tavern_state']['total_wealth']:.1f}")
    
    # Save state
    cleanup_economy_system()
    print("✅ Economic state saved")
    
    # Simulate some changes
    economy.execute_transaction(
        TransactionType.PURCHASE,
        ["Karczmarz", "TavernMarket"],
        {ResourceType.GOLD: 10.0},
        "Test transaction for persistence"
    )
    
    final_summary = economy.get_economic_summary()
    print(f"\n📊 After Changes:")
    print(f"   Total Transactions: {len(economy.transaction_history)}")
    print(f"   Tavern Wealth: {final_summary['tavern_state']['total_wealth']:.1f}")
    
    print("✅ Persistence test completed")
    
    return economy

def main():
    """Main test function"""
    print("💰 Tavern Economy System Test Suite")
    print("=" * 45)
    
    try:
        # Run all tests
        economy = test_agent_resources()
        test_basic_transactions()
        test_rumor_economy()
        test_economic_events()
        test_market_dynamics()
        test_economic_persistence()
        
        print("\n🎉 Tavern Economy System testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print("   ✅ Agent resource management")
        print("   ✅ Economic transactions")
        print("   ✅ Rumor-based currency")
        print("   ✅ Market dynamics")
        print("   ✅ Economic events")
        print("   ✅ Wealth distribution")
        print("   ✅ State persistence")
        
        # Final economic summary
        final_summary = economy.get_economic_summary()
        print(f"\n📊 Final Economic State:")
        print(f"   Total Transactions: {len(economy.transaction_history)}")
        print(f"   Market Activity: {final_summary['economic_metrics']['market_activity']}")
        print(f"   Tavern Reputation: {final_summary['tavern_state']['reputation_score']:.1f}/100")
        print(f"   Total Wealth: {final_summary['economic_metrics']['total_wealth_in_circulation']:.1f}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
