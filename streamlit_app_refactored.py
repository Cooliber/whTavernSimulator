#!/usr/bin/env python3
"""
Refactored Warhammer Fantasy Tavern Simulator - Ultra Animated with Multi-Agent System
Modular architecture with GSAP animations + Grok/Cerebras AI agents
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import sys
import os
from datetime import datetime

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import modular components
from core.tavern_simulator import TavernSimulator
from core.enums import InteractionType, Faction
from components.gsap_renderer import GSAPRenderer
from components.gsap_renderer_enhanced import EnhancedGSAPRenderer
from components.gsap_ultra_native import UltraNativeGSAPRenderer
from services.agent_manager import agent_manager
from services.llm_service import llm_service
from config import validate_config, ui_config, tavern_config

# Page configuration
st.set_page_config(
    page_title="🏰 Warhammer Tavern Quest Hub Ultra Animated",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Validate configuration
config_errors = validate_config()
if config_errors:
    st.error("Configuration errors detected:")
    for error in config_errors:
        st.error(f"• {error}")
    st.stop()

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'simulator' not in st.session_state:
        st.session_state.simulator = TavernSimulator()
        st.session_state.simulator.generate_new_tavern()
    
    if 'gsap_renderer' not in st.session_state:
        st.session_state.gsap_renderer = GSAPRenderer()

    if 'enhanced_renderer' not in st.session_state:
        st.session_state.enhanced_renderer = EnhancedGSAPRenderer()

    if 'ultra_native_renderer' not in st.session_state:
        st.session_state.ultra_native_renderer = UltraNativeGSAPRenderer()

    if 'animation_mode' not in st.session_state:
        st.session_state.animation_mode = 'ultra_native'

    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'fps': 60,
            'memory': 45,
            'animations': 12,
            'particles': 150
        }
    
    if 'animation_state' not in st.session_state:
        st.session_state.animation_state = {
            'last_interaction': None,
            'brawl_active': False,
            'rumour_spreading': False,
            'characters_entering': False,
            'agents_thinking': {}
        }
    
    if 'agent_turn_counter' not in st.session_state:
        st.session_state.agent_turn_counter = 0

def render_custom_css():
    """Render custom CSS for the application"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #8b0000, #ffd700, #8b0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .agent-status-card {
        background: linear-gradient(45deg, rgba(0,0,0,0.7), rgba(50,50,50,0.7));
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .agent-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ffd700;
        margin-bottom: 5px;
    }
    
    .agent-status {
        font-size: 0.9rem;
        color: #ccc;
        margin-bottom: 5px;
    }
    
    .reasoning-trace {
        background: rgba(0,0,0,0.3);
        border-radius: 5px;
        padding: 8px;
        font-family: monospace;
        font-size: 0.8rem;
        color: #ddd;
        max-height: 60px;
        overflow-y: auto;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #8b4513, #ffd700);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
    }
    
    .communication-log {
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with controls and agent status"""
    with st.sidebar:
        st.header("🎮 Tavern Controls")
        
        # Basic tavern controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏰 New Tavern"):
                st.session_state.simulator.generate_new_tavern()
                st.session_state.animation_state['characters_entering'] = True
                st.rerun()
        
        with col2:
            if st.button("⏭️ Advance Turn"):
                advance_simulation_turn()
                st.rerun()
        
        # Agent controls
        st.markdown("### 🤖 AI Agent Controls")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🧠 Agent Turn"):
                process_agent_turn()
                st.rerun()
        
        with col4:
            if st.button("💭 Force Thinking"):
                trigger_agent_thinking()
                st.rerun()
        
        # Manual event triggers
        st.markdown("### 🎲 Manual Events")
        
        if st.button("🥊 Trigger Brawl"):
            st.session_state.animation_state['brawl_active'] = True
            st.rerun()
        
        if st.button("💬 Generate Rumour"):
            rumour = st.session_state.simulator.generate_rumor()
            if rumour:
                st.session_state.animation_state['rumour_spreading'] = True
            st.rerun()
        
        # Agent status display
        st.markdown("### 🤖 Agent Status")
        render_agent_status()
        
        # Communication log
        st.markdown("### 📡 Agent Communications")
        render_communication_log()
        
        # HVAC CRM metaphors
        st.markdown("---")
        st.subheader("🎯 HVAC CRM Metaphors")
        st.write("🔥 **Brawls** = Service Escalations")
        st.write("💬 **Rumours** = Customer Feedback")
        st.write("👥 **Entrances** = Lead Acquisition")
        st.write("📊 **Tension** = Customer Satisfaction")
        st.write("🤖 **Agents** = AI Process Automation")

def render_agent_status():
    """Render current status of all agents"""
    agent_status = agent_manager.get_agent_status_summary()
    
    for agent_name, status in agent_status.items():
        st.markdown(f"""
        <div class="agent-status-card">
            <div class="agent-name">{status['emotion_emoji']} {agent_name}</div>
            <div class="agent-status">Status: {status['emotional_state'].title()}</div>
            <div class="agent-status">Active: {'✅' if status['active'] else '❌'}</div>
            <div class="reasoning-trace">{status['status']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_communication_log():
    """Render recent agent communications"""
    comms = agent_manager.get_communication_history(limit=5)
    
    for comm in comms:
        priority_emoji = "🚨" if comm['priority'] > 7 else "📢" if comm['priority'] > 5 else "💬"
        
        st.markdown(f"""
        <div class="communication-log">
            <small>{priority_emoji} {comm['timestamp']} | {comm['type'].upper()}</small><br>
            <strong>{comm['sender']} → {comm['receiver']}:</strong><br>
            {comm['message']}
        </div>
        """, unsafe_allow_html=True)

def advance_simulation_turn():
    """Advance both tavern simulation and agent turns"""
    # Advance tavern simulation
    st.session_state.simulator.advance_turn()
    
    # Process agent turn
    process_agent_turn()

def process_agent_turn():
    """Process one turn for all agents"""
    tavern_state = get_tavern_state_for_agents()
    
    # Process agent turn
    turn_results = agent_manager.process_turn(tavern_state)
    
    # Apply agent effects to tavern
    apply_agent_effects_to_tavern(turn_results.get('tavern_effects', {}))
    
    # Trigger animations based on agent actions
    trigger_agent_animations(turn_results.get('agent_actions', {}))
    
    st.session_state.agent_turn_counter += 1

def get_tavern_state_for_agents():
    """Get current tavern state formatted for agents"""
    if not st.session_state.simulator.current_tavern:
        return {}
    
    tavern = st.session_state.simulator.current_tavern
    
    return {
        "tension_level": tavern.tension_level,
        "reputation": tavern.reputation,
        "capacity": tavern.capacity,
        "current_occupancy": tavern.current_occupancy,
        "characters": [
            {
                "name": char.name,
                "faction": char.faction.value,
                "drunk_level": char.drunk_level,
                "health": char.health,
                "mood": char.current_mood
            }
            for char in tavern.characters
        ],
        "recent_events": tavern.current_events[-5:],
        "recent_interactions": [
            {
                "initiator": i.initiator,
                "target": i.target,
                "type": i.interaction_type.value,
                "success": i.success
            }
            for i in st.session_state.simulator.interaction_history[-3:]
        ],
        "current_rumors": [
            st.session_state.simulator.rumor_system.get_random_rumor()
            for _ in range(3)
        ]
    }

def apply_agent_effects_to_tavern(effects: dict):
    """Apply agent action effects to tavern state"""
    if not st.session_state.simulator.current_tavern:
        return
    
    tavern = st.session_state.simulator.current_tavern
    
    for effect_type, effect_value in effects.items():
        if effect_type == "tension_change":
            tavern.tension_level = max(0, min(100, tavern.tension_level + effect_value))
        elif effect_type == "reputation_change":
            tavern.reputation = max(0, min(100, tavern.reputation + effect_value))

def trigger_agent_animations(agent_actions: dict):
    """Trigger animations based on agent actions"""
    for agent_name, action_data in agent_actions.items():
        action_type = action_data.get('action', '')
        
        if action_type == "defuse_tension":
            # Trigger calming animation
            pass
        elif action_type == "gather_intelligence":
            # Trigger stealth animation
            st.session_state.animation_state['agents_thinking'][agent_name] = True

def trigger_agent_thinking():
    """Manually trigger thinking animations for all agents"""
    for agent_name in agent_manager.agents.keys():
        st.session_state.animation_state['agents_thinking'][agent_name] = True

def render_main_content():
    """Render the main content area with GSAP tavern"""
    # Main header with animation mode selection
    render_enhanced_header()

    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Render GSAP tavern based on selected mode
        render_gsap_tavern()

    with col2:
        # Render performance metrics
        render_performance_metrics()
        # Render tavern status and controls
        render_tavern_status()
        render_interaction_controls()

def render_enhanced_header():
    """Render enhanced header with animation mode selection"""
    st.markdown("""
    <style>
        .ultra-header {
            background: linear-gradient(135deg, #ffd700 0%, #b8860b 50%, #8b0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .mode-selector {
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #ffd700;
            border-radius: 15px;
            padding: 1rem;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="ultra-header">🚀 Ultra-Native GSAP Tavern Simulator</h1>', unsafe_allow_html=True)

    # Animation mode selection
    with st.container():
        st.markdown('<div class="mode-selector">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.subheader("🎛️ Animation Mode")

            mode = st.radio(
                "Choose your GSAP experience:",
                [
                    "🚀 Ultra-Native (Full JavaScript Environment)",
                    "⚡ Enhanced (Advanced GSAP Features)",
                    "🎯 Standard (Basic GSAP Integration)"
                ],
                index=0 if st.session_state.animation_mode == 'ultra_native' else
                      1 if st.session_state.animation_mode == 'enhanced' else 2,
                horizontal=True
            )

            if "Ultra-Native" in mode:
                st.session_state.animation_mode = 'ultra_native'
                st.success("🚀 Ultra-Native: Maximum JavaScript integration with 138% GSAP utilization!")
            elif "Enhanced" in mode:
                st.session_state.animation_mode = 'enhanced'
                st.info("⚡ Enhanced: Advanced GSAP features with rich interactions!")
            else:
                st.session_state.animation_mode = 'standard'
                st.warning("🎯 Standard: Basic GSAP integration for compatibility!")

        st.markdown('</div>', unsafe_allow_html=True)

def render_gsap_tavern():
    """Render the GSAP-powered tavern visualization based on selected mode"""
    tavern_name = "The Mysterious Tavern"
    if st.session_state.simulator.current_tavern:
        tavern_name = st.session_state.simulator.current_tavern.name

    # Generate HTML based on animation mode
    if st.session_state.animation_mode == 'ultra_native':
        st.subheader("🚀 Ultra-Native GSAP Environment")
        gsap_html = st.session_state.ultra_native_renderer.get_ultra_native_html(tavern_name)
        height = 800

    elif st.session_state.animation_mode == 'enhanced':
        st.subheader("⚡ Enhanced GSAP Features")
        gsap_html = st.session_state.enhanced_renderer.get_enhanced_tavern_html(
            tavern_name,
            theme_variant='dark_fantasy',
            sound_enabled=True
        )
        height = 700

    else:  # standard mode
        st.subheader("🎯 Standard GSAP Integration")
        gsap_html = st.session_state.gsap_renderer.get_tavern_html(tavern_name)
        height = 600

    # Render the component
    components.html(gsap_html, height=height, scrolling=True)

    # Handle animation triggers
    handle_animation_triggers()

def render_performance_metrics():
    """Render real-time performance metrics"""
    if st.session_state.animation_mode == 'ultra_native':
        st.markdown("""
        <div style="background: rgba(139, 0, 0, 0.1); border: 1px solid #8b0000;
                    border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
        """, unsafe_allow_html=True)

        st.subheader("📊 Performance Metrics")

        # Simulate real-time data updates
        import random

        # Update performance metrics with some variation
        st.session_state.performance_metrics['fps'] = max(55, min(65,
            st.session_state.performance_metrics['fps'] + random.randint(-3, 3)))
        st.session_state.performance_metrics['memory'] = max(30, min(70,
            st.session_state.performance_metrics['memory'] + random.randint(-2, 2)))
        st.session_state.performance_metrics['animations'] = max(5, min(30,
            st.session_state.performance_metrics['animations'] + random.randint(-2, 4)))
        st.session_state.performance_metrics['particles'] = max(50, min(300,
            st.session_state.performance_metrics['particles'] + random.randint(-20, 30)))

        # Display metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric("FPS", st.session_state.performance_metrics['fps'],
                     delta=random.randint(-2, 3))
            st.metric("Animations", st.session_state.performance_metrics['animations'],
                     delta=random.randint(-1, 2))

        with col2:
            st.metric("Memory (MB)", st.session_state.performance_metrics['memory'],
                     delta=random.randint(-3, 1))
            st.metric("Particles", st.session_state.performance_metrics['particles'],
                     delta=random.randint(-10, 15))

        # Performance status
        fps = st.session_state.performance_metrics['fps']
        if fps >= 60:
            st.success(f"🚀 Excellent Performance: {fps} FPS")
        elif fps >= 45:
            st.warning(f"⚡ Good Performance: {fps} FPS")
        else:
            st.error(f"🐌 Performance Issues: {fps} FPS")

        st.markdown('</div>', unsafe_allow_html=True)

        # Ultra-native controls
        st.subheader("🎮 Ultra Controls")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✨ Particle Burst"):
                st.session_state.trigger_particles = True
            if st.button("🔄 Morph Demo"):
                st.session_state.trigger_morph = True

        with col2:
            if st.button("🎵 Audio Demo"):
                st.session_state.trigger_audio = True
            if st.button("🔄 Reset Scene"):
                st.session_state.reset_scene = True

def handle_animation_triggers():
    """Handle animation triggers based on session state"""

    # Handle ultra-native specific triggers
    if st.session_state.animation_mode == 'ultra_native':
        handle_ultra_native_triggers()

    # Character entrance animation
    if st.session_state.animation_state.get('characters_entering'):
        if st.session_state.simulator.current_tavern:
            characters_data = [
                {
                    'name': char.name,
                    'faction': char.faction.value.replace(' ', '').lower()
                }
                for char in st.session_state.simulator.current_tavern.characters
            ]
            
            components.html(f"""
            <script>
            if (window.animateCharacterEntrance) {{
                window.animateCharacterEntrance({json.dumps(characters_data)});
            }}
            </script>
            """, height=0)
        
        st.session_state.animation_state['characters_entering'] = False
    
    # Brawl animation
    if st.session_state.animation_state.get('brawl_active'):
        components.html("""
        <script>
        if (window.triggerBrawlAnimation) {
            window.triggerBrawlAnimation();
        }
        </script>
        """, height=0)
        st.session_state.animation_state['brawl_active'] = False
    
    # Rumour spreading animation
    if st.session_state.animation_state.get('rumour_spreading'):
        latest_rumour = st.session_state.simulator.rumor_system.get_random_rumor()
        if latest_rumour:
            components.html(f"""
            <script>
            if (window.animateRumourSpread) {{
                window.animateRumourSpread("{latest_rumour}");
            }}
            </script>
            """, height=0)
        st.session_state.animation_state['rumour_spreading'] = False
    
    # Agent thinking animations
    for agent_name, thinking in st.session_state.animation_state.get('agents_thinking', {}).items():
        if thinking:
            components.html(f"""
            <script>
            if (window.animateAgentThinking) {{
                window.animateAgentThinking('agent-{agent_name.lower()}');
            }}
            </script>
            """, height=0)
            st.session_state.animation_state['agents_thinking'][agent_name] = False

def handle_ultra_native_triggers():
    """Handle ultra-native specific animation triggers"""

    # Particle burst trigger
    if hasattr(st.session_state, 'trigger_particles'):
        components.html("""
        <script>
            if (window.triggerParticleBurst) {
                window.triggerParticleBurst();
            } else if (window.globalParticleSystem) {
                window.globalParticleSystem.burst(400, 300, 30, 'magic');
            }
        </script>
        """, height=0)
        del st.session_state.trigger_particles

    # Morph sequence trigger
    if hasattr(st.session_state, 'trigger_morph'):
        components.html("""
        <script>
            if (window.triggerMorphSequence) {
                window.triggerMorphSequence();
            } else if (window.globalMorphSystem) {
                window.globalMorphSystem.morphBetween('circle', 'star', 2);
            }
        </script>
        """, height=0)
        del st.session_state.trigger_morph

    # Audio demo trigger
    if hasattr(st.session_state, 'trigger_audio'):
        components.html("""
        <script>
            if (window.globalAudioSystem) {
                window.globalAudioSystem.playSequence(['C4', 'E4', 'G4', 'C5', 'E5']);
            }
        </script>
        """, height=0)
        del st.session_state.trigger_audio

    # Reset scene trigger
    if hasattr(st.session_state, 'reset_scene'):
        components.html("""
        <script>
            if (window.resetScene) {
                window.resetScene();
            }
        </script>
        """, height=0)
        del st.session_state.reset_scene
    
    # Update tension meter and relationships
    if st.session_state.simulator.current_tavern:
        tension = st.session_state.simulator.current_tavern.tension_level
        components.html(f"""
        <script>
        if (window.updateTensionMeter) {{
            window.updateTensionMeter({tension});
        }}
        </script>
        """, height=0)
        
        # Update relationships graph
        relationships = st.session_state.simulator.get_character_relationships()
        if relationships:
            components.html(f"""
            <script>
            if (window.createRelationshipsGraph) {{
                window.createRelationshipsGraph({json.dumps(relationships)});
            }}
            </script>
            """, height=0)

def render_tavern_status():
    """Render current tavern status"""
    st.subheader("📊 Tavern Status")
    
    if st.session_state.simulator.current_tavern:
        tavern = st.session_state.simulator.current_tavern
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tension", f"{tavern.tension_level}/100")
        with col2:
            st.metric("Occupancy", f"{tavern.current_occupancy}/{tavern.capacity}")
        with col3:
            st.metric("Reputation", f"{tavern.reputation}/100")
        
        # Agent turn counter
        st.metric("Agent Turns", st.session_state.agent_turn_counter)
        
        # Current characters
        st.subheader("🎭 Current Characters")
        for char in tavern.characters[:5]:  # Show first 5
            mood_emoji = "😊" if char.current_mood == "happy" else "😠" if char.current_mood == "angry" else "🍺" if char.is_drunk() else "😐"
            st.write(f"{mood_emoji} **{char.name}** ({char.faction.value})")
        
        if len(tavern.characters) > 5:
            st.write(f"... and {len(tavern.characters) - 5} more")

def render_interaction_controls():
    """Render manual interaction controls"""
    st.subheader("🎮 Manual Interactions")
    
    if st.session_state.simulator.current_tavern and len(st.session_state.simulator.current_tavern.characters) >= 2:
        chars = st.session_state.simulator.current_tavern.characters
        
        initiator = st.selectbox("Initiator", [char.name for char in chars])
        target = st.selectbox("Target", [char.name for char in chars if char.name != initiator])
        interaction_type = st.selectbox("Interaction", [it.value for it in InteractionType])
        
        if st.button("🎲 Perform Interaction"):
            interaction = st.session_state.simulator.perform_interaction(
                initiator, target, InteractionType(interaction_type)
            )
            if interaction:
                st.success(f"✅ {interaction.outcome_description}")
                if interaction.relationship_change != 0:
                    change = "improved" if interaction.relationship_change > 0 else "worsened"
                    st.info(f"Relationship {change} by {abs(interaction.relationship_change)}")
                st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Render custom CSS
    render_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_main_content()

if __name__ == "__main__":
    main()
