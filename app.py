#!/usr/bin/env python3
"""
Warhammer Fantasy Tavern Simulator - Complete Integrated Application
Final integration of all components: 17-agent system, economy, narrative, GSAP visualization
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all integrated components
from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType
from services.narrative_engine import NarrativeEngine
from services.agent_memory import AgentMemorySystem
from components.gsap_renderer import GSAPRenderer
from components.agent_response_animator import AgentResponseAnimator, AgentResponse

# Page configuration
st.set_page_config(
    page_title="🏰 Warhammer Tavern Simulator - Complete Edition",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #6b3e2a 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffd700;
        text-align: center;
    }
    .metric-card {
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffd700;
        margin: 10px 0;
    }
    .agent-status {
        background: rgba(40,40,60,0.9);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #ffd700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
@st.cache_resource
def initialize_systems():
    """Initialize all integrated systems"""
    economy = TavernEconomySystem()
    narrative = NarrativeEngine(economy_system=economy)
    renderer = GSAPRenderer()
    agent_animator = AgentResponseAnimator()
    return economy, narrative, renderer, agent_animator

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏰 Warhammer Fantasy Tavern Simulator</h1>
        <h3>Complete Edition with 17-Agent System, Economy & GSAP Visualization</h3>
        <p>Powered by CrewAI + Groq + Cerebras + GSAP 138% Utilization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize systems
    economy, narrative, renderer, agent_animator = initialize_systems()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Tavern Controls")
        
        # System status
        st.subheader("📊 System Status")
        agent_count = narrative.get_total_agent_count()
        faction_counts = narrative.get_agent_count_by_faction()
        
        st.metric("Total Agents", agent_count)
        for faction, count in faction_counts.items():
            st.metric(f"{faction} Faction", count)
        
        # Economy controls
        st.subheader("💰 Economy Controls")
        
        if st.button("🔄 Run Economic Cycle"):
            run_economic_cycle(economy, narrative)
        
        if st.button("🎲 Generate Event"):
            generate_narrative_event(narrative)
        
        if st.button("💸 Execute Trade"):
            execute_sample_trade(economy)
        
        if st.button("🗣️ Trade Rumor"):
            execute_rumor_trade(economy)
        
        # Performance controls
        st.subheader("⚡ Performance")
        
        if st.button("🧪 Run Performance Test"):
            run_performance_test(economy, narrative)
        
        if st.button("💾 Save State"):
            save_system_state(economy, narrative)
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["🎨 Tavern Visualization", "🎭 Agent Responses", "📊 System Metrics"])

    with tab1:
        # GSAP Visualization
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("🎨 Live Tavern Visualization")
        
        # Get current economic state for GSAP
        economic_summary = economy.get_economic_summary()
        
        # Generate GSAP HTML with current data
        gsap_html = renderer.get_tavern_html("The Complete Tavern")
        
        # Add JavaScript to update economy data
        economy_data = {
            "reputation": economic_summary['tavern_state']['reputation_score'],
            "totalWealth": economic_summary['economic_metrics']['total_wealth_in_circulation'],
            "marketActivity": economic_summary['economic_metrics']['market_activity']
        }
        
        # Inject economy data into GSAP
        gsap_html_with_data = gsap_html.replace(
            "console.log(\"💰 Economy visualization system ready!\");",
            f"""
            console.log("💰 Economy visualization system ready!");
            // Update with current data
            setTimeout(() => {{
                if (typeof updateEconomyStats === 'function') {{
                    updateEconomyStats({json.dumps(economy_data)});
                }}
            }}, 1000);
            """
        )
        
            # Display GSAP component
            components.html(gsap_html_with_data, height=800, scrolling=True)

        with col2:
            # System metrics and logs
            display_system_metrics(economy, narrative)
            display_recent_activity(economy, narrative)

    with tab2:
        # Agent Response Animation System
        st.subheader("🎭 Agent Response Animation System")

        col1, col2 = st.columns([3, 1])

        with col1:
            # Create sample agents for demonstration
            sample_agents = [
                {"id": "karczmarz", "name": "Karczmarz", "role": "Innkeeper", "faction": "Empire"},
                {"id": "skrytobojca", "name": "Skrytobójca", "role": "Assassin", "faction": "Chaos"},
                {"id": "wiedzma", "name": "Wiedźma", "role": "Witch", "faction": "Undead"},
                {"id": "czempion", "name": "Czempion", "role": "Champion", "faction": "Empire"},
                {"id": "zwiadowca", "name": "Zwiadowca", "role": "Scout", "faction": "Elf"}
            ]

            # Render agent response system
            agent_animator.render_agent_response_system(agents=sample_agents, height=700)

        with col2:
            st.subheader("🎮 Agent Controls")

            # Test agent responses
            if st.button("🧠 Test Thinking"):
                response = AgentResponse(
                    agent_id="karczmarz",
                    agent_name="Karczmarz",
                    response_type="thinking",
                    content="Analyzing tavern situation...",
                    confidence=0.8,
                    emotion="focused",
                    reasoning_steps=["Observing", "Analyzing", "Planning"],
                    timestamp=datetime.now(),
                    duration=3.0,
                    priority=2
                )
                agent_animator.add_agent_response(response)

            if st.button("💬 Test Speaking"):
                response = AgentResponse(
                    agent_id="wiedzma",
                    agent_name="Wiedźma",
                    response_type="speaking",
                    content="The spirits whisper of change...",
                    confidence=0.7,
                    emotion="mystical",
                    reasoning_steps=["Channeling", "Interpreting", "Speaking"],
                    timestamp=datetime.now(),
                    duration=4.0,
                    priority=3
                )
                agent_animator.add_agent_response(response)

            if st.button("🚨 Test Alert"):
                response = AgentResponse(
                    agent_id="skrytobojca",
                    agent_name="Skrytobójca",
                    response_type="alerting",
                    content="Threat detected!",
                    confidence=0.95,
                    emotion="urgent",
                    reasoning_steps=["Detecting", "Analyzing", "Alerting"],
                    timestamp=datetime.now(),
                    duration=1.5,
                    priority=4
                )
                agent_animator.add_agent_response(response)

            if st.button("🧹 Clear Responses"):
                agent_animator.clear_agent_responses()

            # Performance metrics
            st.subheader("📊 Animation Metrics")
            metrics = agent_animator.get_performance_metrics()
            st.metric("FPS", f"{metrics.get('fps', 60)}")
            st.metric("Queue Size", f"{metrics.get('queue_size', 0)}")

    with tab3:
        # System Metrics Tab
        st.subheader("📊 Complete System Metrics")

        col1, col2 = st.columns(2)

        with col1:
            display_system_metrics(economy, narrative)

        with col2:
            display_recent_activity(economy, narrative)

def run_economic_cycle(economy, narrative):
    """Run a complete economic cycle"""
    with st.spinner("Running economic cycle..."):
        start_time = time.time()
        
        # Generate event
        event = narrative.generate_dynamic_event(fast_mode=True)
        
        # Execute some transactions
        transactions = []
        for i in range(3):
            try:
                transaction = economy.execute_transaction(
                    TransactionType.PURCHASE,
                    ["Karczmarz", "Kupiec_Imperialny"],
                    {ResourceType.GOLD: 5.0},
                    f"Cycle transaction {i+1}"
                )
                transactions.append(transaction)
            except Exception as e:
                st.error(f"Transaction failed: {e}")
        
        end_time = time.time()
        
        st.success(f"✅ Economic cycle completed in {end_time - start_time:.3f}s")
        st.info(f"Generated event: {event.get('title', 'Unknown')}")
        st.info(f"Executed {len(transactions)} transactions")

def generate_narrative_event(narrative):
    """Generate a narrative event"""
    with st.spinner("Generating narrative event..."):
        event = narrative.generate_dynamic_event(fast_mode=True)
        
        st.success("✅ Event generated!")
        st.json({
            "title": event.get("title", "Unknown"),
            "type": event.get("type", "Unknown"),
            "description": event.get("description", "No description"),
            "tension_change": event.get("tension_change", 0),
            "participants": event.get("participants", [])
        })

def execute_sample_trade(economy):
    """Execute a sample trade"""
    with st.spinner("Executing trade..."):
        try:
            transaction = economy.execute_transaction(
                TransactionType.FAVOR_EXCHANGE,
                ["Zwiadowca", "Mag_Wysokich_Elfów"],
                {ResourceType.INFORMATION: 3.0, ResourceType.FAVORS: 1.0},
                "Sample trade from app interface"
            )
            
            if transaction.success:
                st.success("✅ Trade successful!")
                st.json({
                    "participants": transaction.participants,
                    "resources": {str(k): v for k, v in transaction.resources_exchanged.items()},
                    "description": transaction.description
                })
            else:
                st.error("❌ Trade failed!")
                
        except Exception as e:
            st.error(f"Trade error: {e}")

def execute_rumor_trade(economy):
    """Execute a rumor trade"""
    with st.spinner("Trading rumor..."):
        try:
            success = economy.trade_rumor_for_resources(
                "Wiedźma",
                "Strange lights seen in the forest at midnight",
                ResourceType.GOLD,
                20.0
            )
            
            if success:
                st.success("✅ Rumor trade successful!")
            else:
                st.error("❌ Rumor trade failed!")
                
        except Exception as e:
            st.error(f"Rumor trade error: {e}")

def run_performance_test(economy, narrative):
    """Run performance test"""
    with st.spinner("Running performance test..."):
        start_time = time.time()
        
        # Test multiple operations
        operations = 0
        for i in range(10):
            # Generate event
            event = narrative.generate_dynamic_event(fast_mode=True)
            operations += 1
            
            # Execute transaction
            try:
                transaction = economy.execute_transaction(
                    TransactionType.PURCHASE,
                    ["Karczmarz", "TavernMarket"],
                    {ResourceType.GOLD: 1.0},
                    f"Performance test {i+1}"
                )
                operations += 1
            except:
                pass
        
        end_time = time.time()
        total_time = end_time - start_time
        
        st.success(f"✅ Performance test completed!")
        st.metric("Operations", operations)
        st.metric("Total Time", f"{total_time:.3f}s")
        st.metric("Ops/Second", f"{operations/total_time:.1f}")

def save_system_state(economy, narrative):
    """Save current system state"""
    with st.spinner("Saving system state..."):
        try:
            # Save memories
            economy.memory_system.save_memories()
            
            # Get current state
            state = {
                "timestamp": datetime.now().isoformat(),
                "economy": economy.get_economic_summary(),
                "narrative": {
                    "tension_level": narrative.narrative_state.tension_level,
                    "active_events": len(narrative.narrative_state.active_events),
                    "agent_count": narrative.get_total_agent_count()
                }
            }
            
            st.success("✅ System state saved!")
            st.json(state)
            
        except Exception as e:
            st.error(f"Save failed: {e}")

def display_system_metrics(economy, narrative):
    """Display current system metrics"""
    st.subheader("📊 System Metrics")
    
    # Economy metrics
    economic_summary = economy.get_economic_summary()
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Tavern Reputation", f"{economic_summary['tavern_state']['reputation_score']:.1f}/100")
    st.metric("Total Wealth", f"{economic_summary['economic_metrics']['total_wealth_in_circulation']:.0f}")
    st.metric("Market Activity", economic_summary['economic_metrics']['market_activity'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Narrative metrics
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Tension Level", f"{narrative.narrative_state.tension_level}/100")
    st.metric("Active Events", len(narrative.narrative_state.active_events))
    st.metric("Event History", len(narrative.event_history))
    st.markdown('</div>', unsafe_allow_html=True)

def display_recent_activity(economy, narrative):
    """Display recent activity logs"""
    st.subheader("📝 Recent Activity")
    
    # Recent transactions
    if economy.transaction_history:
        st.write("**Recent Transactions:**")
        for transaction in economy.transaction_history[-3:]:
            st.markdown(f"""
            <div class="agent-status">
                <strong>{transaction.transaction_type.value}</strong><br>
                {transaction.description}<br>
                <small>Participants: {', '.join(transaction.participants)}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent events
    if narrative.event_history:
        st.write("**Recent Events:**")
        for event in narrative.event_history[-3:]:
            st.markdown(f"""
            <div class="agent-status">
                <strong>{event.get('title', 'Unknown Event')}</strong><br>
                {event.get('description', 'No description')}<br>
                <small>Type: {event.get('type', 'Unknown')}</small>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
