#!/usr/bin/env python3
"""
Test Three.js Integration for Warhammer Tavern Simulator
Demonstrates advanced 3D visualization capabilities
"""

import streamlit as st
import sys
import os
from typing import List

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.threejs_integration import (
    ThreeJSIntegration, 
    Character3D, 
    TavernEnvironment, 
    RenderQuality
)

def create_sample_characters() -> List[Character3D]:
    """Create sample characters for testing"""
    characters = [
        Character3D(
            id="karczmarz",
            name="Karczmarz",
            faction="Empire",
            position={"x": 0, "y": 0, "z": -5},
            rotation={"x": 0, "y": 0, "z": 0},
            scale={"x": 1, "y": 1, "z": 1},
            animation_state="idle",
            emotion="neutral",
            health=1.0
        ),
        Character3D(
            id="skrytobojca",
            name="Skrytobójca",
            faction="Chaos",
            position={"x": -3, "y": 0, "z": 2},
            rotation={"x": 0, "y": 45, "z": 0},
            scale={"x": 1, "y": 1, "z": 1},
            animation_state="sneaking",
            emotion="suspicious",
            health=0.8
        ),
        Character3D(
            id="wiedzma",
            name="Wiedźma",
            faction="Undead",
            position={"x": 3, "y": 0, "z": 2},
            rotation={"x": 0, "y": -30, "z": 0},
            scale={"x": 1, "y": 1, "z": 1},
            animation_state="casting",
            emotion="mysterious",
            health=0.9
        ),
        Character3D(
            id="czempion",
            name="Czempion",
            faction="Empire",
            position={"x": 0, "y": 0, "z": 5},
            rotation={"x": 0, "y": 180, "z": 0},
            scale={"x": 1.2, "y": 1.2, "z": 1.2},
            animation_state="guarding",
            emotion="vigilant",
            health=1.0
        ),
        Character3D(
            id="zwiadowca",
            name="Zwiadowca",
            faction="Elf",
            position={"x": -5, "y": 0, "z": 0},
            rotation={"x": 0, "y": 90, "z": 0},
            scale={"x": 0.9, "y": 0.9, "z": 0.9},
            animation_state="observing",
            emotion="alert",
            health=0.7
        )
    ]
    return characters

def create_sample_environment() -> TavernEnvironment:
    """Create sample tavern environment"""
    return TavernEnvironment(
        lighting={
            "ambient": {"color": 0x404040, "intensity": 0.3},
            "directional": {"color": 0xffffff, "intensity": 0.8, "position": [10, 10, 5]},
            "fireplace": {"color": 0xff4500, "intensity": 2, "position": [-8, 2, 0]}
        },
        weather="clear",
        time_of_day="evening",
        atmosphere={
            "fog": {"color": 0x1a1a1a, "near": 10, "far": 50},
            "particles": ["dust", "smoke"],
            "sounds": ["crackling_fire", "ambient_chatter"]
        },
        interactive_objects=[
            {
                "type": "bar",
                "position": {"x": 0, "y": 1, "z": -8},
                "action": "show_drinks_menu"
            },
            {
                "type": "fireplace",
                "position": {"x": -8, "y": 1, "z": 0},
                "action": "show_warmth_effect"
            },
            {
                "type": "table",
                "position": {"x": 4, "y": 1, "z": 4},
                "action": "show_conversation_options"
            },
            {
                "type": "stage",
                "position": {"x": 8, "y": 1, "z": -4},
                "action": "show_performance_menu"
            }
        ]
    )

def create_sample_relationships():
    """Create sample character relationships"""
    return [
        {
            "from": "karczmarz",
            "to": "czempion",
            "type": "trust",
            "strength": 0.8,
            "description": "The innkeeper trusts the champion"
        },
        {
            "from": "skrytobojca",
            "to": "wiedzma",
            "type": "alliance",
            "strength": 0.6,
            "description": "Dark alliance between assassin and witch"
        },
        {
            "from": "czempion",
            "to": "skrytobojca",
            "type": "suspicion",
            "strength": 0.9,
            "description": "Champion is highly suspicious of the assassin"
        },
        {
            "from": "zwiadowca",
            "to": "wiedzma",
            "type": "curiosity",
            "strength": 0.4,
            "description": "Scout is curious about the witch's powers"
        },
        {
            "from": "karczmarz",
            "to": "zwiadowca",
            "type": "friendship",
            "strength": 0.7,
            "description": "Old friendship between innkeeper and scout"
        }
    ]

def main():
    """Main application"""
    st.set_page_config(
        page_title="Three.js Warhammer Tavern",
        page_icon="🏰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏰 Three.js Warhammer Tavern Simulator")
    st.markdown("**Advanced 3D visualization with real-time character interactions**")
    
    # Initialize Three.js integration
    threejs = ThreeJSIntegration()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Controls")
        
        # Quality settings
        quality = st.selectbox(
            "Render Quality",
            options=[q.value for q in RenderQuality],
            index=2  # Default to HIGH
        )
        threejs.quality_settings = RenderQuality(quality)
        
        # VR support
        enable_vr = st.checkbox("Enable VR Support", value=False)
        
        # Adaptive quality
        adaptive_quality = st.checkbox("Adaptive Quality", value=True)
        threejs.adaptive_quality = adaptive_quality
        
        # Height setting
        height = st.slider("Component Height", 400, 1000, 800)
        
        st.markdown("---")
        st.header("📊 Performance")
        
        # Performance dashboard
        threejs.performance_monitor.render_performance_dashboard()
        
        st.markdown("---")
        st.header("👥 Characters")
        
        # Character selection
        characters = create_sample_characters()
        selected_character = st.selectbox(
            "Focus on Character",
            options=[char.name for char in characters],
            index=0
        )
        
        # Character details
        if selected_character:
            char = next(c for c in characters if c.name == selected_character)
            st.write(f"**Faction:** {char.faction}")
            st.write(f"**Health:** {char.health:.1%}")
            st.write(f"**Emotion:** {char.emotion}")
            st.write(f"**State:** {char.animation_state}")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🌟 3D Tavern Environment")
        
        # Create sample data
        characters = create_sample_characters()
        environment = create_sample_environment()
        relationships = create_sample_relationships()
        
        # Render Three.js component
        component_data = threejs.render_3d_tavern(
            characters=characters,
            environment=environment,
            relationships=relationships,
            height=height,
            enable_vr=enable_vr
        )
        
        # Display component return data
        if component_data:
            st.json(component_data)
    
    with col2:
        st.subheader("🔧 Features")
        
        st.markdown("""
        **3D Visualization:**
        - ✅ Interactive 3D characters
        - ✅ Detailed tavern environment
        - ✅ Real-time lighting effects
        - ✅ Particle systems
        - ✅ Camera controls
        
        **Performance:**
        - ✅ 60+ FPS targeting
        - ✅ Adaptive quality
        - ✅ GPU acceleration
        - ✅ Memory optimization
        - ✅ Real-time monitoring
        
        **Interactions:**
        - ✅ Character selection
        - ✅ Object interactions
        - ✅ Relationship visualization
        - ✅ Animation triggers
        - ✅ Spatial audio (planned)
        
        **Advanced:**
        - ✅ WebXR/VR support
        - ✅ Post-processing effects
        - ✅ Dynamic shadows
        - ✅ LOD optimization
        - ✅ Mobile compatibility
        """)
        
        st.markdown("---")
        st.subheader("📈 Performance Targets")
        
        # Performance targets display
        targets = {
            "Desktop FPS": "60+",
            "Mobile FPS": "30+",
            "Bundle Size": "<5MB",
            "Memory Usage": "<100MB",
            "Load Time": "<3s"
        }
        
        for metric, target in targets.items():
            st.metric(metric, target)
        
        st.markdown("---")
        st.subheader("🎯 Next Steps")
        
        st.markdown("""
        1. **Character Models**: Load GLTF models
        2. **Animations**: Add skeletal animations
        3. **Physics**: Implement collision detection
        4. **Audio**: Add spatial audio system
        5. **Networking**: Multi-user support
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🏰 Warhammer Tavern Simulator - Three.js Integration Demo<br>
        Built with Streamlit, Three.js, and advanced WebGL techniques
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
