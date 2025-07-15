#!/usr/bin/env python3
"""
Test Enhanced GSAP Economy Visualization
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.gsap_renderer import GSAPRenderer
from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType

# Load environment variables
load_dotenv()

def test_gsap_economy_html_generation():
    """Test that GSAP renderer generates economy visualization HTML"""
    print("🎨 Testing GSAP Economy HTML Generation")
    print("=" * 45)
    
    renderer = GSAPRenderer()
    
    # Generate complete tavern HTML
    html_content = renderer.get_tavern_html("Test Economy Tavern")
    
    # Check for economy-specific elements
    economy_elements = [
        'id="economy-container"',
        'id="reputation-fill"',
        'id="wealth-fill"',
        'id="activity-fill"',
        'class="economy-dashboard"',
        'class="trade-particles-container"',
        'updateEconomyStats',
        'animateTradeResult',
        'onTradeSuccess',
        'onReputationChange'
    ]
    
    print(f"📊 Checking for economy visualization elements:")
    missing_elements = []
    
    for element in economy_elements:
        if element in html_content:
            print(f"   ✅ {element}")
        else:
            print(f"   ❌ {element}")
            missing_elements.append(element)
    
    if missing_elements:
        print(f"\n⚠️ Missing elements: {len(missing_elements)}")
        for element in missing_elements:
            print(f"     - {element}")
    else:
        print(f"\n✅ All economy elements present!")
    
    # Check HTML structure
    html_size = len(html_content)
    print(f"\n📏 HTML Content:")
    print(f"   Size: {html_size:,} characters")
    print(f"   Lines: {html_content.count(chr(10)):,}")
    
    # Verify GSAP CDN links
    gsap_plugins = ['gsap.min.js', 'ScrollTrigger.min.js', 'TextPlugin.min.js']
    gsap_found = sum(1 for plugin in gsap_plugins if plugin in html_content)
    print(f"   GSAP plugins: {gsap_found}/{len(gsap_plugins)}")
    
    return html_content, len(missing_elements) == 0

def test_economy_integration():
    """Test economy system integration with GSAP visualization"""
    print("\n💰 Testing Economy-GSAP Integration")
    print("=" * 40)
    
    economy = TavernEconomySystem()
    renderer = GSAPRenderer()
    
    # Get initial economic state
    initial_summary = economy.get_economic_summary()
    print(f"📊 Initial Economic State:")
    print(f"   Tavern Reputation: {initial_summary['tavern_state']['reputation_score']:.1f}")
    print(f"   Total Wealth: {initial_summary['economic_metrics']['total_wealth_in_circulation']:.1f}")
    print(f"   Market Activity: {initial_summary['economic_metrics']['market_activity']}")
    
    # Simulate some economic activity
    print(f"\n🔄 Simulating Economic Activity:")
    
    # Execute some transactions
    transactions = []
    for i in range(5):
        try:
            transaction = economy.execute_transaction(
                TransactionType.PURCHASE,
                ["Karczmarz", "Kupiec_Imperialny"],
                {ResourceType.GOLD: 10.0, ResourceType.SUPPLIES: 5.0},
                f"Test transaction {i+1} for GSAP visualization"
            )
            transactions.append(transaction)
            print(f"   Transaction {i+1}: {'✅ SUCCESS' if transaction.success else '❌ FAILED'}")
        except Exception as e:
            print(f"   Transaction {i+1}: ❌ ERROR - {e}")
    
    # Get updated economic state
    updated_summary = economy.get_economic_summary()
    print(f"\n📊 Updated Economic State:")
    print(f"   Tavern Reputation: {updated_summary['tavern_state']['reputation_score']:.1f}")
    print(f"   Total Wealth: {updated_summary['economic_metrics']['total_wealth_in_circulation']:.1f}")
    print(f"   Market Activity: {updated_summary['economic_metrics']['market_activity']}")
    
    # Calculate changes
    rep_change = updated_summary['tavern_state']['reputation_score'] - initial_summary['tavern_state']['reputation_score']
    wealth_change = updated_summary['economic_metrics']['total_wealth_in_circulation'] - initial_summary['economic_metrics']['total_wealth_in_circulation']
    activity_change = updated_summary['economic_metrics']['market_activity'] - initial_summary['economic_metrics']['market_activity']
    
    print(f"\n📈 Economic Changes:")
    print(f"   Reputation: {rep_change:+.1f}")
    print(f"   Wealth: {wealth_change:+.1f}")
    print(f"   Activity: {activity_change:+.1f}")
    
    # Test JavaScript data structure for GSAP
    economy_data = {
        "reputation": updated_summary['tavern_state']['reputation_score'],
        "totalWealth": updated_summary['economic_metrics']['total_wealth_in_circulation'],
        "marketActivity": updated_summary['economic_metrics']['market_activity']
    }
    
    print(f"\n🎨 GSAP Economy Data Structure:")
    print(f"   {economy_data}")
    
    return economy_data, len(transactions)

def test_trade_visualization_data():
    """Test trade result data for GSAP visualization"""
    print("\n💸 Testing Trade Visualization Data")
    print("=" * 40)
    
    economy = TavernEconomySystem()
    
    # Test successful trade
    print("🔄 Testing Successful Trade:")
    try:
        success_trade = economy.execute_transaction(
            TransactionType.FAVOR_EXCHANGE,
            ["Zwiadowca", "Mag_Wysokich_Elfów"],
            {ResourceType.INFORMATION: 5.0, ResourceType.FAVORS: 2.0},
            "Successful trade for GSAP visualization"
        )
        
        trade_data = {
            "success": success_trade.success,
            "participants": success_trade.participants,
            "resources": {
                "Information": 5.0,
                "Favors": 2.0
            },
            "description": success_trade.description
        }
        
        print(f"   Success: {trade_data['success']}")
        print(f"   Participants: {', '.join(trade_data['participants'])}")
        print(f"   Resources: {trade_data['resources']}")
        print(f"   GSAP Data: {trade_data}")
        
    except Exception as e:
        print(f"   ❌ Trade failed: {e}")
        trade_data = {"success": False, "error": str(e)}
    
    # Test rumor trade
    print(f"\n🗣️ Testing Rumor Trade:")
    try:
        rumor_success = economy.trade_rumor_for_resources(
            "Wiedźma",
            "Ancient artifacts hidden beneath the tavern cellar",
            ResourceType.GOLD,
            15.0
        )
        
        rumor_data = {
            "success": rumor_success,
            "trader": "Wiedźma",
            "rumor": "Ancient artifacts hidden beneath the tavern cellar",
            "resource": "Gold",
            "amount": 15.0
        }
        
        print(f"   Success: {rumor_data['success']}")
        print(f"   Trader: {rumor_data['trader']}")
        print(f"   Resource: {rumor_data['resource']} ({rumor_data['amount']})")
        print(f"   GSAP Data: {rumor_data}")
        
    except Exception as e:
        print(f"   ❌ Rumor trade failed: {e}")
        rumor_data = {"success": False, "error": str(e)}
    
    return trade_data, rumor_data

def test_performance_with_visualization():
    """Test performance impact of economy visualization"""
    print("\n⚡ Testing Performance with Economy Visualization")
    print("=" * 50)
    
    renderer = GSAPRenderer()
    economy = TavernEconomySystem()
    
    # Test HTML generation performance
    start_time = time.time()
    html_content = renderer.get_tavern_html("Performance Test Tavern")
    html_time = time.time() - start_time
    
    print(f"🎨 HTML Generation Performance:")
    print(f"   Time: {html_time:.3f}s")
    print(f"   Size: {len(html_content):,} characters")
    print(f"   Rate: {len(html_content)/html_time:,.0f} chars/sec")
    
    # Test economy data preparation
    start_time = time.time()
    for i in range(10):
        summary = economy.get_economic_summary()
        economy_data = {
            "reputation": summary['tavern_state']['reputation_score'],
            "totalWealth": summary['economic_metrics']['total_wealth_in_circulation'],
            "marketActivity": summary['economic_metrics']['market_activity']
        }
    end_time = time.time()
    
    data_time = (end_time - start_time) / 10
    print(f"\n📊 Economy Data Preparation:")
    print(f"   Avg time per update: {data_time:.3f}s")
    print(f"   Updates per second: {1/data_time:.1f}")
    
    # Overall performance assessment
    total_time = html_time + data_time
    print(f"\n🚀 Overall Performance:")
    print(f"   Total time: {total_time:.3f}s")
    print(f"   Ready for real-time updates: {'✅ YES' if data_time < 0.1 else '❌ NO'}")
    
    return html_time, data_time

def main():
    """Main test function"""
    print("🎨 GSAP Economy Visualization Test Suite")
    print("=" * 50)
    
    try:
        # Run all tests
        html_content, html_success = test_gsap_economy_html_generation()
        economy_data, transaction_count = test_economy_integration()
        trade_data, rumor_data = test_trade_visualization_data()
        html_time, data_time = test_performance_with_visualization()
        
        print("\n🎉 GSAP Economy Visualization testing complete!")
        print("\n🚀 Key Features Demonstrated:")
        print(f"   ✅ Economy HTML generation: {'PASS' if html_success else 'FAIL'}")
        print(f"   ✅ Economy data integration: {transaction_count} transactions")
        print(f"   ✅ Trade visualization data: {'PASS' if trade_data.get('success') else 'FAIL'}")
        print(f"   ✅ Rumor trade visualization: {'PASS' if rumor_data.get('success') else 'FAIL'}")
        print(f"   ✅ Performance optimization: {data_time:.3f}s per update")
        
        print(f"\n📊 Final Assessment:")
        overall_success = (
            html_success and 
            transaction_count > 0 and 
            data_time < 0.1
        )
        print(f"   Overall: {'✅ PASS' if overall_success else '❌ FAIL'}")
        
        if overall_success:
            print(f"\n🎉 GSAP Economy Visualization system ready!")
            print(f"   HTML size: {len(html_content):,} characters")
            print(f"   Update rate: {1/data_time:.1f} updates/sec")
            print(f"   Ready for production deployment")
        else:
            print(f"\n⚠️ System needs optimization")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
