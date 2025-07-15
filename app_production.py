#!/usr/bin/env python3
"""
Warhammer Fantasy Tavern Simulator - Production Edition
Enhanced frontend with robust error handling, monitoring, and containerized deployment
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import json
import time
import traceback
from datetime import datetime
from dotenv import load_dotenv
import structlog

# Load environment variables
load_dotenv()

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Import components with error handling
try:
    from services.tavern_economy import TavernEconomySystem, ResourceType, TransactionType
    from services.narrative_engine import NarrativeEngine
    from services.agent_memory import AgentMemorySystem
    from components.gsap_renderer import GSAPRenderer
    from services.health_monitor import health_monitor
    logger.info("All core components imported successfully")
except ImportError as e:
    logger.error("Failed to import core components", error=str(e))
    st.error(f"❌ Critical Error: Failed to import components - {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🏰 Warhammer Tavern Simulator - Production",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with production styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #6b3e2a 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffd700;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffd700;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .agent-status {
        background: rgba(40,40,60,0.9);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #ffd700;
    }
    .health-indicator {
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        margin: 5px 0;
    }
    .health-healthy { background-color: #28a745; color: white; }
    .health-degraded { background-color: #ffc107; color: black; }
    .health-unhealthy { background-color: #dc3545; color: white; }
    .performance-metric {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
@st.cache_resource
def initialize_systems():
    """Initialize all integrated systems with comprehensive error handling"""
    try:
        logger.info("Initializing tavern systems")
        start_time = time.time()
        
        # Initialize core systems
        economy = TavernEconomySystem()
        narrative = NarrativeEngine(economy_system=economy)
        renderer = GSAPRenderer()
        
        init_time = time.time() - start_time
        
        # Record successful initialization
        health_monitor.record_transaction(success=True, response_time=init_time)
        
        logger.info("Systems initialized successfully", 
                   init_time=init_time,
                   agent_count=narrative.get_total_agent_count(),
                   factions=list(narrative.faction_crews.keys()))
        
        return economy, narrative, renderer, init_time
        
    except Exception as e:
        logger.error("Failed to initialize systems", error=str(e), traceback=traceback.format_exc())
        health_monitor.record_transaction(success=False)
        st.error(f"❌ System Initialization Failed: {e}")
        st.stop()

def display_health_status():
    """Display system health status"""
    try:
        health_report = health_monitor.check_health()
        
        # Health indicator
        status = health_report["status"]
        if status == "healthy":
            health_class = "health-healthy"
            health_icon = "✅"
        elif status == "degraded":
            health_class = "health-degraded"
            health_icon = "⚠️"
        else:
            health_class = "health-unhealthy"
            health_icon = "❌"
        
        st.markdown(f"""
        <div class="health-indicator {health_class}">
            {health_icon} System Status: {status.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        # Performance metrics
        metrics = health_report["metrics"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="performance-metric">
                <strong>CPU</strong><br>
                {metrics['cpu_percent']:.1f}%
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="performance-metric">
                <strong>Memory</strong><br>
                {metrics['memory_percent']:.1f}%
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="performance-metric">
                <strong>Uptime</strong><br>
                {metrics['uptime_seconds']:.0f}s
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="performance-metric">
                <strong>Response</strong><br>
                {metrics['response_time_ms']:.1f}ms
            </div>
            """, unsafe_allow_html=True)
        
        # Show issues if any
        if health_report.get("issues"):
            st.warning(f"⚠️ Issues detected: {', '.join(health_report['issues'])}")
            
    except Exception as e:
        logger.error("Failed to display health status", error=str(e))
        st.error(f"❌ Health monitoring error: {e}")

def main():
    """Main application function with enhanced error handling"""
    try:
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🏰 Warhammer Fantasy Tavern Simulator</h1>
            <h3>Production Edition - 18-Agent System with GSAP Visualization</h3>
            <p>Powered by CrewAI + Groq + Cerebras + Enhanced Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display health status
        display_health_status()
        
        # Initialize systems
        economy, narrative, renderer, init_time = initialize_systems()
        
        # Sidebar controls
        with st.sidebar:
            st.header("🎮 Tavern Controls")
            
            # System status
            st.subheader("📊 System Status")
            agent_count = narrative.get_total_agent_count()
            faction_counts = narrative.get_agent_count_by_faction()
            
            st.metric("Total Agents", agent_count)
            st.metric("Initialization Time", f"{init_time:.3f}s")
            
            for faction, count in faction_counts.items():
                st.metric(f"{faction} Faction", count)
            
            # Performance monitoring
            st.subheader("⚡ Performance")
            
            if st.button("📊 Health Check"):
                with st.spinner("Running health check..."):
                    health_report = health_monitor.check_health()
                    st.json(health_report)
            
            if st.button("📈 Prometheus Metrics"):
                with st.spinner("Generating metrics..."):
                    metrics = health_monitor.get_prometheus_metrics()
                    st.text_area("Prometheus Metrics", metrics, height=200)
            
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
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # GSAP Visualization
            st.subheader("🎨 Live Tavern Visualization")
            
            try:
                # Get current economic state for GSAP
                economic_summary = economy.get_economic_summary()
                
                # Generate GSAP HTML with current data
                gsap_html = renderer.get_tavern_html("Production Tavern")
                
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
                
            except Exception as e:
                logger.error("GSAP visualization error", error=str(e))
                st.error(f"❌ Visualization Error: {e}")
                st.info("🔧 Fallback: Basic economy display")
                st.json(economy_data)
        
        with col2:
            # System metrics and logs
            display_system_metrics(economy, narrative)
            display_recent_activity(economy, narrative)
            
    except Exception as e:
        logger.error("Main application error", error=str(e), traceback=traceback.format_exc())
        st.error(f"❌ Application Error: {e}")
        st.info("🔧 Please refresh the page or contact support")

# Import the rest of the functions from the original app
def run_economic_cycle(economy, narrative):
    """Run a complete economic cycle with monitoring"""
    with st.spinner("Running economic cycle..."):
        start_time = time.time()
        
        try:
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
                    logger.error("Transaction failed", error=str(e))
                    st.error(f"Transaction failed: {e}")
            
            end_time = time.time()
            cycle_time = end_time - start_time
            
            # Record performance
            health_monitor.record_transaction(success=True, response_time=cycle_time)
            
            st.success(f"✅ Economic cycle completed in {cycle_time:.3f}s")
            st.info(f"Generated event: {event.get('title', 'Unknown')}")
            st.info(f"Executed {len(transactions)} transactions")
            
        except Exception as e:
            health_monitor.record_transaction(success=False)
            logger.error("Economic cycle failed", error=str(e))
            st.error(f"❌ Economic cycle failed: {e}")

def generate_narrative_event(narrative):
    """Generate a narrative event with monitoring"""
    with st.spinner("Generating narrative event..."):
        start_time = time.time()

        try:
            event = narrative.generate_dynamic_event(fast_mode=True)

            response_time = time.time() - start_time
            health_monitor.record_transaction(success=True, response_time=response_time)

            st.success("✅ Event generated!")
            st.json({
                "title": event.get("title", "Unknown"),
                "type": event.get("type", "Unknown"),
                "description": event.get("description", "No description"),
                "tension_change": event.get("tension_change", 0),
                "participants": event.get("participants", [])
            })

        except Exception as e:
            health_monitor.record_transaction(success=False)
            logger.error("Event generation failed", error=str(e))
            st.error(f"❌ Event generation failed: {e}")

def execute_sample_trade(economy):
    """Execute a sample trade with monitoring"""
    with st.spinner("Executing trade..."):
        start_time = time.time()

        try:
            transaction = economy.execute_transaction(
                TransactionType.FAVOR_EXCHANGE,
                ["Zwiadowca", "Mag_Wysokich_Elfów"],
                {ResourceType.INFORMATION: 3.0, ResourceType.FAVORS: 1.0},
                "Sample trade from production interface"
            )

            response_time = time.time() - start_time
            health_monitor.record_transaction(success=transaction.success, response_time=response_time)

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
            health_monitor.record_transaction(success=False)
            logger.error("Trade execution failed", error=str(e))
            st.error(f"❌ Trade error: {e}")

def execute_rumor_trade(economy):
    """Execute a rumor trade with monitoring"""
    with st.spinner("Trading rumor..."):
        start_time = time.time()

        try:
            success = economy.trade_rumor_for_resources(
                "Wiedźma",
                "Strange lights seen in the forest at midnight",
                ResourceType.GOLD,
                20.0
            )

            response_time = time.time() - start_time
            health_monitor.record_transaction(success=success, response_time=response_time)

            if success:
                st.success("✅ Rumor trade successful!")
            else:
                st.error("❌ Rumor trade failed!")

        except Exception as e:
            health_monitor.record_transaction(success=False)
            logger.error("Rumor trade failed", error=str(e))
            st.error(f"❌ Rumor trade error: {e}")

def display_system_metrics(economy, narrative):
    """Display current system metrics with enhanced monitoring"""
    st.subheader("📊 System Metrics")

    try:
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

        # Performance metrics
        health_report = health_monitor.check_health()
        metrics = health_report["metrics"]

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Transaction Rate", f"{metrics['transaction_rate']:.1f}/s")
        st.metric("Error Rate", f"{metrics['error_rate']:.1f}%")
        st.metric("Avg Response Time", f"{metrics['response_time_ms']:.1f}ms")
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        logger.error("Failed to display system metrics", error=str(e))
        st.error(f"❌ Metrics error: {e}")

def display_recent_activity(economy, narrative):
    """Display recent activity logs with enhanced formatting"""
    st.subheader("📝 Recent Activity")

    try:
        # Recent transactions
        if economy.transaction_history:
            st.write("**Recent Transactions:**")
            for transaction in economy.transaction_history[-3:]:
                status_icon = "✅" if transaction.success else "❌"
                st.markdown(f"""
                <div class="agent-status">
                    {status_icon} <strong>{transaction.transaction_type.value}</strong><br>
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
                    🎲 <strong>{event.get('title', 'Unknown Event')}</strong><br>
                    {event.get('description', 'No description')}<br>
                    <small>Type: {event.get('type', 'Unknown')}</small>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        logger.error("Failed to display recent activity", error=str(e))
        st.error(f"❌ Activity log error: {e}")

if __name__ == "__main__":
    main()
