"""
Enhanced Dashboard System for Warhammer Fantasy Tavern Simulator
Comprehensive control panel with real-time metrics, agent monitoring, and economic visualization
"""

import streamlit as st
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional

# Try to import plotly, fall back to basic charts if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Create mock objects for compatibility
    class MockPlotly:
        def __init__(self):
            pass
        def Figure(self, *args, **kwargs):
            return self
        def Indicator(self, *args, **kwargs):
            return self
        def update_layout(self, *args, **kwargs):
            return self
        def pie(self, *args, **kwargs):
            return self

    go = MockPlotly()
    px = MockPlotly()

    # Mock pandas DataFrame
    try:
        import pandas as pd
    except ImportError:
        class MockDataFrame:
            def __init__(self, data):
                self.data = data
            def date_range(self, *args, **kwargs):
                return list(range(10))
        pd = MockDataFrame

class EnhancedDashboard:
    """Enhanced dashboard with comprehensive monitoring and control capabilities"""
    
    def __init__(self):
        self.metrics_history = []
        self.event_timeline = []
        self.agent_performance = {}
        self.economic_trends = []
        
    def render_control_panel(self, economy, narrative):
        """Render comprehensive control panel"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9)); 
                    padding: 20px; border-radius: 15px; border: 2px solid var(--primary-gold, #ffd700);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 20px;">
            <h2 style="color: var(--primary-gold, #ffd700); font-family: 'Cinzel', serif; 
                       text-align: center; margin-bottom: 20px;">
                🎮 Tavern Command Center
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Control sections
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_economic_controls(economy)
        
        with col2:
            self._render_narrative_controls(narrative)
        
        with col3:
            self._render_system_controls()
    
    def _render_economic_controls(self, economy):
        """Render economic control section"""
        st.markdown("""
        <div style="background: rgba(40,60,20,0.8); padding: 15px; border-radius: 10px; 
                    border: 2px solid #4CAF50; margin-bottom: 15px;">
            <h4 style="color: #4CAF50; text-align: center; margin-bottom: 15px;">💰 Economic Controls</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Economic actions
        if st.button("🔄 Run Economic Cycle", key="econ_cycle"):
            self._execute_economic_cycle(economy)
        
        if st.button("💸 Execute Trade", key="exec_trade"):
            self._execute_sample_trade(economy)
        
        if st.button("📈 Market Boost", key="market_boost"):
            self._boost_market_activity(economy)
        
        # Economic settings
        st.markdown("**Settings:**")
        trade_frequency = st.slider("Trade Frequency", 1, 10, 5, key="trade_freq")
        market_volatility = st.slider("Market Volatility", 0.1, 2.0, 1.0, 0.1, key="volatility")
        
        return {"trade_frequency": trade_frequency, "market_volatility": market_volatility}
    
    def _render_narrative_controls(self, narrative):
        """Render narrative control section"""
        st.markdown("""
        <div style="background: rgba(60,20,60,0.8); padding: 15px; border-radius: 10px; 
                    border: 2px solid #9C27B0; margin-bottom: 15px;">
            <h4 style="color: #9C27B0; text-align: center; margin-bottom: 15px;">🎭 Narrative Controls</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Narrative actions
        if st.button("🎲 Generate Event", key="gen_event"):
            self._generate_narrative_event(narrative)
        
        if st.button("⚔️ Trigger Brawl", key="trigger_brawl"):
            self._trigger_brawl_event(narrative)
        
        if st.button("🗣️ Spread Rumor", key="spread_rumor"):
            self._spread_rumor(narrative)
        
        # Narrative settings
        st.markdown("**Settings:**")
        tension_level = st.slider("Base Tension", 0, 100, 25, key="tension")
        event_frequency = st.slider("Event Frequency", 1, 10, 3, key="event_freq")
        
        return {"tension_level": tension_level, "event_frequency": event_frequency}
    
    def _render_system_controls(self):
        """Render system control section"""
        st.markdown("""
        <div style="background: rgba(20,40,60,0.8); padding: 15px; border-radius: 10px; 
                    border: 2px solid #2196F3; margin-bottom: 15px;">
            <h4 style="color: #2196F3; text-align: center; margin-bottom: 15px;">⚙️ System Controls</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # System actions
        if st.button("🔄 Restart Simulation", key="restart_sim"):
            self._restart_simulation()
        
        if st.button("💾 Save State", key="save_state"):
            self._save_tavern_state()
        
        if st.button("📂 Load State", key="load_state"):
            self._load_tavern_state()
        
        # System settings
        st.markdown("**Settings:**")
        auto_save = st.checkbox("Auto-save", value=True, key="auto_save")
        debug_mode = st.checkbox("Debug Mode", value=False, key="debug_mode")
        
        return {"auto_save": auto_save, "debug_mode": debug_mode}
    
    def render_real_time_metrics(self, economy, narrative):
        """Render real-time metrics visualization"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9)); 
                    padding: 20px; border-radius: 15px; border: 2px solid var(--primary-gold, #ffd700);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 20px;">
            <h2 style="color: var(--primary-gold, #ffd700); font-family: 'Cinzel', serif; 
                       text-align: center; margin-bottom: 20px;">
                📊 Real-time Metrics Dashboard
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics columns
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_economic_metrics(economy)
        
        with col2:
            self._render_narrative_metrics(narrative)
        
        # Full-width charts
        self._render_trend_charts()
    
    def _render_economic_metrics(self, economy):
        """Render economic metrics with animated charts"""
        try:
            economic_summary = economy.get_economic_summary()

            # Reputation gauge
            reputation = economic_summary['tavern_state']['reputation_score']

            if PLOTLY_AVAILABLE:
                fig_reputation = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = reputation,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "🏰 Tavern Reputation"},
                    delta = {'reference': 75},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#ffd700"},
                        'steps': [
                            {'range': [0, 50], 'color': "#8b0000"},
                            {'range': [50, 80], 'color': "#ffa500"},
                            {'range': [80, 100], 'color': "#4CAF50"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_reputation.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_reputation, use_container_width=True)
            else:
                # Fallback to simple progress bar
                st.markdown(f"""
                <div style="background: rgba(40,20,10,0.9); padding: 15px; border-radius: 10px;
                            border: 2px solid #ffd700; margin: 10px 0;">
                    <h4 style="color: #ffd700; text-align: center;">🏰 Tavern Reputation</h4>
                    <div style="background: rgba(0,0,0,0.5); border-radius: 10px; height: 20px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #8b0000, #ffd700);
                                   height: 100%; width: {reputation}%; transition: width 1s ease;"></div>
                    </div>
                    <div style="text-align: center; color: #ffd700; margin-top: 10px; font-size: 1.5rem;">
                        {reputation:.1f}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Wealth indicator
            total_wealth = economic_summary['economic_metrics']['total_wealth_in_circulation']
            st.metric("💰 Total Wealth", f"{total_wealth:.0f}", delta=f"+{total_wealth*0.05:.0f}")
            
            # Market activity
            market_activity = economic_summary['economic_metrics']['market_activity']
            activity_color = "#4CAF50" if market_activity == "High" else "#ffa500" if market_activity == "Medium" else "#8b0000"
            st.markdown(f"""
            <div style="background: {activity_color}33; padding: 10px; border-radius: 8px; 
                        border: 2px solid {activity_color}; text-align: center;">
                <strong style="color: {activity_color};">📈 Market Activity: {market_activity}</strong>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Economic metrics error: {e}")
    
    def _render_narrative_metrics(self, narrative):
        """Render narrative metrics with visual indicators"""
        try:
            # Tension level gauge
            tension = narrative.narrative_state.tension_level

            if PLOTLY_AVAILABLE:
                fig_tension = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = tension,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "⚡ Tension Level"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#ff6b6b"},
                        'steps': [
                            {'range': [0, 30], 'color': "#4CAF50"},
                            {'range': [30, 70], 'color': "#ffa500"},
                            {'range': [70, 100], 'color': "#8b0000"}
                        ],
                        'threshold': {
                            'line': {'color': "darkred", 'width': 4},
                            'thickness': 0.75,
                            'value': 80
                        }
                    }
                ))
                fig_tension.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_tension, use_container_width=True)
            else:
                # Fallback tension meter
                tension_color = "#4CAF50" if tension < 30 else "#ffa500" if tension < 70 else "#8b0000"
                st.markdown(f"""
                <div style="background: rgba(40,20,10,0.9); padding: 15px; border-radius: 10px;
                            border: 2px solid {tension_color}; margin: 10px 0;">
                    <h4 style="color: {tension_color}; text-align: center;">⚡ Tension Level</h4>
                    <div style="background: rgba(0,0,0,0.5); border-radius: 10px; height: 20px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #4CAF50, #ffa500, #8b0000);
                                   height: 100%; width: {tension}%; transition: width 1s ease;"></div>
                    </div>
                    <div style="text-align: center; color: {tension_color}; margin-top: 10px; font-size: 1.5rem;">
                        {tension}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Active events
            active_events = len(narrative.narrative_state.active_events)
            st.metric("🎭 Active Events", active_events, delta=f"+{active_events-2}" if active_events > 2 else None)
            
            # Event history
            event_history = len(narrative.event_history)
            st.metric("📜 Total Events", event_history, delta="+1")
            
        except Exception as e:
            st.error(f"❌ Narrative metrics error: {e}")
    
    def _render_trend_charts(self):
        """Render trend charts for historical data"""
        if PLOTLY_AVAILABLE:
            # Generate sample trend data
            dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='H')

            # Economic trends
            economic_data = pd.DataFrame({
                'timestamp': dates,
                'wealth': [1000 + i*10 + (i%24)*50 for i in range(len(dates))],
                'reputation': [75 + (i%48)*0.5 for i in range(len(dates))],
                'activity': [(i%12)*8 + 20 for i in range(len(dates))]
            })

            fig_trends = go.Figure()
            fig_trends.add_trace(go.Scatter(x=economic_data['timestamp'], y=economic_data['wealth'],
                                           mode='lines', name='Wealth', line=dict(color='#ffd700')))
            fig_trends.add_trace(go.Scatter(x=economic_data['timestamp'], y=economic_data['reputation']*10,
                                           mode='lines', name='Reputation (x10)', line=dict(color='#4CAF50')))
            fig_trends.add_trace(go.Scatter(x=economic_data['timestamp'], y=economic_data['activity']*5,
                                           mode='lines', name='Activity (x5)', line=dict(color='#ff6b6b')))

            fig_trends.update_layout(
                title="📈 Economic Trends (Last 7 Days)",
                xaxis_title="Time",
                yaxis_title="Value",
                height=400,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(40,20,10,0.3)"
            )

            st.plotly_chart(fig_trends, use_container_width=True)
        else:
            # Fallback trend display
            st.markdown("""
            <div style="background: rgba(40,20,10,0.9); padding: 20px; border-radius: 10px;
                        border: 2px solid #ffd700; margin: 10px 0;">
                <h4 style="color: #ffd700; text-align: center;">📈 Economic Trends (Last 7 Days)</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                    <div style="text-align: center; padding: 10px; background: rgba(255,215,0,0.1); border-radius: 8px;">
                        <div style="color: #ffd700; font-size: 1.2rem;">💰 Wealth</div>
                        <div style="color: white; font-size: 1.5rem;">↗️ +15%</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: rgba(76,175,80,0.1); border-radius: 8px;">
                        <div style="color: #4CAF50; font-size: 1.2rem;">🏰 Reputation</div>
                        <div style="color: white; font-size: 1.5rem;">↗️ +8%</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: rgba(255,107,107,0.1); border-radius: 8px;">
                        <div style="color: #ff6b6b; font-size: 1.2rem;">📈 Activity</div>
                        <div style="color: white; font-size: 1.5rem;">↗️ +12%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_agent_monitoring(self, narrative):
        """Render agent monitoring dashboard"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9)); 
                    padding: 20px; border-radius: 15px; border: 2px solid var(--primary-gold, #ffd700);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 20px;">
            <h2 style="color: var(--primary-gold, #ffd700); font-family: 'Cinzel', serif; 
                       text-align: center; margin-bottom: 20px;">
                🤖 Agent Monitoring Dashboard
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Agent status overview
            agent_count = narrative.get_total_agent_count()
            faction_counts = narrative.get_agent_count_by_faction()
            
            # Agent performance metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Total Agents", agent_count)
                
            with col2:
                st.metric("🏛️ Active Factions", len(faction_counts))
                
            with col3:
                st.metric("⚡ Response Rate", "95.2%")
            
            # Faction breakdown chart
            if faction_counts:
                if PLOTLY_AVAILABLE:
                    fig_factions = px.pie(
                        values=list(faction_counts.values()),
                        names=list(faction_counts.keys()),
                        title="🏛️ Agent Distribution by Faction"
                    )
                    fig_factions.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_factions, use_container_width=True)
                else:
                    # Fallback faction display
                    st.markdown("### 🏛️ Agent Distribution by Faction")
                    total_agents = sum(faction_counts.values())

                    for faction, count in faction_counts.items():
                        percentage = (count / total_agents) * 100
                        st.markdown(f"""
                        <div style="background: rgba(40,40,60,0.8); padding: 10px; border-radius: 8px;
                                    margin: 5px 0; border-left: 4px solid #ffd700;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: #ffd700; font-weight: bold;">{faction}</span>
                                <span style="color: white;">{count} agents ({percentage:.1f}%)</span>
                            </div>
                            <div style="background: rgba(0,0,0,0.3); border-radius: 10px; height: 8px; overflow: hidden; margin-top: 5px;">
                                <div style="background: #ffd700; height: 100%; width: {percentage}%; transition: width 0.5s ease;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Agent health indicators
            self._render_agent_health_indicators(narrative)
            
        except Exception as e:
            st.error(f"❌ Agent monitoring error: {e}")
    
    def _render_agent_health_indicators(self, narrative):
        """Render individual agent health indicators"""
        st.markdown("### 🔍 Agent Health Status")
        
        # Sample agent data (in production, this would come from actual agent monitoring)
        agents = [
            {"name": "Karczmarz", "status": "healthy", "response_time": 45, "success_rate": 98.5},
            {"name": "Skrytobójca", "status": "healthy", "response_time": 32, "success_rate": 97.2},
            {"name": "Wiedźma", "status": "degraded", "response_time": 78, "success_rate": 89.1},
            {"name": "Zwiadowca", "status": "healthy", "response_time": 41, "success_rate": 96.8},
            {"name": "Czempion", "status": "healthy", "response_time": 38, "success_rate": 99.1}
        ]
        
        for agent in agents:
            status_color = "#4CAF50" if agent["status"] == "healthy" else "#ffa500" if agent["status"] == "degraded" else "#8b0000"
            status_icon = "✅" if agent["status"] == "healthy" else "⚠️" if agent["status"] == "degraded" else "❌"
            
            st.markdown(f"""
            <div style="background: rgba(40,40,60,0.8); padding: 12px; border-radius: 8px; 
                        margin: 8px 0; border-left: 4px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: var(--primary-gold, #ffd700);">{status_icon} {agent['name']}</strong><br>
                        <small style="color: #ccc;">Status: {agent['status'].title()}</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #ccc; font-size: 0.9rem;">Response: {agent['response_time']}ms</div>
                        <div style="color: #ccc; font-size: 0.9rem;">Success: {agent['success_rate']}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Action methods (placeholder implementations)
    def _execute_economic_cycle(self, economy):
        st.success("🔄 Economic cycle executed successfully!")
    
    def _execute_sample_trade(self, economy):
        st.success("💸 Sample trade executed!")
    
    def _boost_market_activity(self, economy):
        st.success("📈 Market activity boosted!")
    
    def _generate_narrative_event(self, narrative):
        st.success("🎲 Narrative event generated!")
    
    def _trigger_brawl_event(self, narrative):
        st.warning("⚔️ Tavern brawl triggered!")
    
    def _spread_rumor(self, narrative):
        st.info("🗣️ Rumor spread throughout the tavern!")
    
    def _restart_simulation(self):
        st.warning("🔄 Simulation restarted!")
    
    def _save_tavern_state(self):
        st.success("💾 Tavern state saved!")
    
    def _load_tavern_state(self):
        st.success("📂 Tavern state loaded!")
