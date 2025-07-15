#!/usr/bin/env python3
"""
Test Agent Response Animation System
Demonstrates stable, calm agent response animations with GSAP
"""

import streamlit as st
import sys
import os
import time
import random
from datetime import datetime
from typing import List, Dict

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.agent_response_animator import AgentResponseAnimator, AgentResponse

def create_sample_agents() -> List[Dict]:
    """Create sample Warhammer agents for testing"""
    return [
        {
            "id": "karczmarz",
            "name": "Karczmarz",
            "role": "Innkeeper",
            "faction": "Empire",
            "status": "Ready"
        },
        {
            "id": "skrytobojca",
            "name": "Skrytobójca",
            "role": "Assassin",
            "faction": "Chaos",
            "status": "Ready"
        },
        {
            "id": "wiedzma",
            "name": "Wiedźma",
            "role": "Witch",
            "faction": "Undead",
            "status": "Ready"
        },
        {
            "id": "czempion",
            "name": "Czempion",
            "role": "Champion",
            "faction": "Empire",
            "status": "Ready"
        },
        {
            "id": "zwiadowca",
            "name": "Zwiadowca",
            "role": "Scout",
            "faction": "Elf",
            "status": "Ready"
        }
    ]

def create_sample_responses() -> List[AgentResponse]:
    """Create sample agent responses for testing"""
    responses = [
        AgentResponse(
            agent_id="karczmarz",
            agent_name="Karczmarz",
            response_type="thinking",
            content="Analyzing tavern situation...",
            confidence=0.8,
            emotion="focused",
            reasoning_steps=[
                "Observing customer behavior",
                "Checking inventory levels",
                "Assessing security situation"
            ],
            timestamp=datetime.now(),
            duration=3.0,
            priority=2
        ),
        AgentResponse(
            agent_id="skrytobojca",
            agent_name="Skrytobójca",
            response_type="alerting",
            content="Potential threat detected!",
            confidence=0.9,
            emotion="alert",
            reasoning_steps=[
                "Suspicious movement detected",
                "Evaluating threat level",
                "Preparing countermeasures"
            ],
            timestamp=datetime.now(),
            duration=2.0,
            priority=4
        ),
        AgentResponse(
            agent_id="wiedzma",
            agent_name="Wiedźma",
            response_type="speaking",
            content="The shadows whisper of dark tidings...",
            confidence=0.7,
            emotion="mysterious",
            reasoning_steps=[
                "Consulting mystical sources",
                "Interpreting omens",
                "Formulating prophecy"
            ],
            timestamp=datetime.now(),
            duration=4.0,
            priority=3
        ),
        AgentResponse(
            agent_id="czempion",
            agent_name="Czempion",
            response_type="deciding",
            content="Evaluating tactical options",
            confidence=0.85,
            emotion="determined",
            reasoning_steps=[
                "Assessing battlefield",
                "Considering strategies",
                "Making tactical decision"
            ],
            timestamp=datetime.now(),
            duration=2.5,
            priority=3
        ),
        AgentResponse(
            agent_id="zwiadowca",
            agent_name="Zwiadowca",
            response_type="acting",
            content="Gathering intelligence from the shadows",
            confidence=0.75,
            emotion="stealthy",
            reasoning_steps=[
                "Identifying information sources",
                "Planning reconnaissance",
                "Executing stealth mission"
            ],
            timestamp=datetime.now(),
            duration=3.5,
            priority=2
        )
    ]
    return responses

def main():
    """Main application"""
    st.set_page_config(
        page_title="Agent Response Animation Test",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🎭 Agent Response Animation System Test")
    st.markdown("**Testing stable, calm agent response animations with GSAP**")
    
    # Initialize animator
    animator = AgentResponseAnimator()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Animation Controls")
        
        # Performance mode
        performance_mode = st.selectbox(
            "Performance Mode",
            options=["smooth", "balanced", "performance"],
            index=1
        )
        animator.set_performance_mode(performance_mode)
        
        # Animation controls
        st.subheader("🎬 Test Animations")
        
        if st.button("🧠 Test Thinking Animation"):
            response = AgentResponse(
                agent_id="karczmarz",
                agent_name="Karczmarz",
                response_type="thinking",
                content="Contemplating the evening's events...",
                confidence=0.8,
                emotion="thoughtful",
                reasoning_steps=["Analyzing", "Processing", "Concluding"],
                timestamp=datetime.now(),
                duration=3.0,
                priority=2
            )
            animator.add_agent_response(response)
        
        if st.button("💬 Test Speaking Animation"):
            response = AgentResponse(
                agent_id="wiedzma",
                agent_name="Wiedźma",
                response_type="speaking",
                content="The spirits speak of change...",
                confidence=0.7,
                emotion="mystical",
                reasoning_steps=["Channeling", "Interpreting", "Communicating"],
                timestamp=datetime.now(),
                duration=4.0,
                priority=3
            )
            animator.add_agent_response(response)
        
        if st.button("⚡ Test Action Animation"):
            response = AgentResponse(
                agent_id="zwiadowca",
                agent_name="Zwiadowca",
                response_type="acting",
                content="Moving through the shadows...",
                confidence=0.9,
                emotion="focused",
                reasoning_steps=["Planning", "Executing", "Completing"],
                timestamp=datetime.now(),
                duration=2.5,
                priority=2
            )
            animator.add_agent_response(response)
        
        if st.button("🎯 Test Decision Animation"):
            response = AgentResponse(
                agent_id="czempion",
                agent_name="Czempion",
                response_type="deciding",
                content="Choosing the best course of action",
                confidence=0.85,
                emotion="determined",
                reasoning_steps=["Evaluating", "Weighing", "Deciding"],
                timestamp=datetime.now(),
                duration=2.0,
                priority=3
            )
            animator.add_agent_response(response)
        
        if st.button("🚨 Test Alert Animation"):
            response = AgentResponse(
                agent_id="skrytobojca",
                agent_name="Skrytobójca",
                response_type="alerting",
                content="DANGER DETECTED!",
                confidence=0.95,
                emotion="urgent",
                reasoning_steps=["Detecting", "Analyzing", "Alerting"],
                timestamp=datetime.now(),
                duration=1.5,
                priority=4
            )
            animator.add_agent_response(response)
        
        st.markdown("---")
        
        if st.button("🎲 Random Agent Response"):
            agents = create_sample_agents()
            responses = create_sample_responses()
            random_response = random.choice(responses)
            animator.add_agent_response(random_response)
        
        if st.button("🌊 Simulate Agent Conversation"):
            responses = create_sample_responses()
            for i, response in enumerate(responses):
                # Stagger the responses
                response.timestamp = datetime.now()
                animator.add_agent_response(response)
                time.sleep(0.5)  # Small delay between responses
        
        if st.button("🧹 Clear All Responses"):
            animator.clear_agent_responses()
        
        st.markdown("---")
        st.subheader("📊 Performance Metrics")
        
        metrics = animator.get_performance_metrics()
        st.metric("FPS", f"{metrics.get('fps', 60)}")
        st.metric("Memory", f"{metrics.get('memory', 0)} MB")
        st.metric("Queue Size", f"{metrics.get('queue_size', 0)}")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🏰 Agent Response Animation System")
        
        # Create sample agents
        agents = create_sample_agents()
        
        # Render the animation system
        component_data = animator.render_agent_response_system(
            agents=agents,
            height=700
        )
        
        # Display component return data
        if component_data:
            with st.expander("🔍 Component Data"):
                st.json(component_data)
    
    with col2:
        st.subheader("🎯 Features")
        
        st.markdown("""
        **Animation Types:**
        - 🧠 Thinking: Pulsing glow with reasoning steps
        - 💬 Speaking: Speech bubbles with content
        - ⚡ Acting: Scale and rotation effects
        - 🎯 Deciding: Confidence-based animations
        - 🚨 Alerting: Urgent flashing effects
        
        **Performance:**
        - 60+ FPS targeting
        - Memory optimization
        - Queue management
        - Real-time monitoring
        
        **Stability:**
        - Calm, smooth animations
        - Error handling
        - Graceful degradation
        - Performance adaptation
        """)
        
        st.markdown("---")
        st.subheader("🎮 Agent Status")
        
        # Show active agents
        active_agents = st.session_state.get('agent_animator_state', {}).get('active_agents', set())
        
        if active_agents:
            st.write("**Active Agents:**")
            for agent_id in active_agents:
                st.write(f"🎭 {agent_id}")
        else:
            st.write("No agents currently active")
        
        # Show response count
        response_count = len(st.session_state.get('agent_animator_state', {}).get('responses', []))
        st.metric("Total Responses", response_count)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🎭 Agent Response Animation System - Stable & Calm Operations<br>
        Built with GSAP 3.12.5 and advanced performance optimization
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
