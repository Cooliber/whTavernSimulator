#!/usr/bin/env python3
"""
Test GSAP Agent Visualization with enhanced animations
"""

import os
import sys
import time
import streamlit as st
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.gsap_renderer import GSAPRenderer

# Load environment variables
load_dotenv()

def create_enhanced_agent_demo():
    """Create enhanced agent visualization demo"""
    
    renderer = GSAPRenderer()
    
    # Generate enhanced HTML with new visualization features
    demo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        {renderer.get_gsap_cdn_links()}
        <style>
            {renderer._get_base_css()}
            {renderer.get_faction_css()}
            {renderer._get_animation_css()}
            
            /* Enhanced Agent Visualization Styles */
            .agent-box {{
                position: relative;
                background: linear-gradient(135deg, rgba(40,40,60,0.9), rgba(60,60,80,0.9));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 12px;
                padding: 15px;
                margin: 10px;
                width: 300px;
                min-height: 180px;
                overflow: hidden;
                transition: all 0.3s ease;
                will-change: transform, box-shadow;
            }}
            
            .agent-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }}
            
            .agent-name {{
                font-weight: bold;
                color: #ffd700;
                font-size: 16px;
            }}
            
            .agent-status {{
                font-size: 20px;
                animation: statusPulse 2s ease-in-out infinite;
            }}
            
            .reasoning-trace {{
                background: rgba(0,0,0,0.4);
                border-radius: 6px;
                padding: 8px;
                margin: 8px 0;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                color: #aaa;
                min-height: 60px;
                max-height: 100px;
                overflow-y: auto;
                border-left: 3px solid rgba(255,215,0,0.5);
            }}
            
            .reasoning-step {{
                margin: 2px 0;
                padding: 2px 4px;
                border-radius: 3px;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            
            .step-number {{
                background: rgba(255,215,0,0.3);
                border-radius: 50%;
                width: 16px;
                height: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 8px;
                font-weight: bold;
            }}
            
            .step-content {{
                flex: 1;
                font-size: 9px;
            }}
            
            .step-confidence {{
                font-size: 8px;
                color: #888;
            }}
            
            .emotion-indicators {{
                display: flex;
                gap: 5px;
                margin-top: 8px;
                flex-wrap: wrap;
            }}
            
            .emotion {{
                font-size: 14px;
                padding: 2px 4px;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            
            .memory-indicator {{
                position: absolute;
                top: 5px;
                left: 5px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: rgba(255,255,255,0.2);
                border: 2px solid rgba(255,255,255,0.4);
                z-index: 10;
            }}
            
            .decision-overlay {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
                z-index: 20;
                pointer-events: none;
                text-shadow: 0 0 10px rgba(255,215,0,0.8);
            }}
            
            .demo-controls {{
                margin: 20px 0;
                padding: 15px;
                background: rgba(0,0,0,0.3);
                border-radius: 8px;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .demo-button {{
                padding: 8px 16px;
                background: linear-gradient(45deg, #ffd700, #ffed4e);
                color: #000;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            
            .demo-button:hover {{
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(255,215,0,0.3);
            }}
        </style>
    </head>
    <body>
        <div id="tavern-main" style="background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #6b3e2a 100%); padding: 20px; border-radius: 15px;">
            <h2 style="color: #ffd700; text-align: center; margin-bottom: 20px;">
                🏰 Enhanced GSAP Agent Visualization Demo
            </h2>
            
            <div class="demo-controls">
                <button class="demo-button" onclick="demoThinking()">🧠 Thinking</button>
                <button class="demo-button" onclick="demoMemoryUpdate()">💭 Memory</button>
                <button class="demo-button" onclick="demoDecision()">⚔️ Decision</button>
                <button class="demo-button" onclick="demoAlert()">🚨 Alert</button>
                <button class="demo-button" onclick="demoReasoningFlow()">🔄 Reasoning</button>
                <button class="demo-button" onclick="demoCommunication()">💬 Communication</button>
                <button class="demo-button" onclick="demoEmotions()">😊 Emotions</button>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px;">
                <!-- Karczmarz Agent -->
                <div id="agent-karczmarz" class="agent-box" data-agent="Karczmarz">
                    <div class="agent-header">
                        <span class="agent-name">🍺 Karczmarz</span>
                        <span class="agent-status">💭</span>
                    </div>
                    <div class="agent-role" style="color: #ccc; font-size: 12px; margin-bottom: 10px;">Tavern Keeper</div>
                    <div class="reasoning-trace">Observing tavern atmosphere...</div>
                    <div class="emotion-indicators">
                        <span class="emotion alertness">⚠️</span>
                        <span class="emotion satisfaction">😊</span>
                        <span class="emotion suspicion">🤔</span>
                    </div>
                </div>
                
                <!-- Skrytobójca Agent -->
                <div id="agent-skrytobojca" class="agent-box" data-agent="Skrytobójca">
                    <div class="agent-header">
                        <span class="agent-name">🗡️ Skrytobójca</span>
                        <span class="agent-status">👁️</span>
                    </div>
                    <div class="agent-role" style="color: #ccc; font-size: 12px; margin-bottom: 10px;">Shadow Agent</div>
                    <div class="reasoning-trace">Scanning for threats...</div>
                    <div class="emotion-indicators">
                        <span class="emotion stealth">🌙</span>
                        <span class="emotion alertness">⚡</span>
                        <span class="emotion cunning">🎭</span>
                    </div>
                </div>
                
                <!-- Wiedźma Agent -->
                <div id="agent-wiedzma" class="agent-box" data-agent="Wiedźma">
                    <div class="agent-header">
                        <span class="agent-name">🔮 Wiedźma</span>
                        <span class="agent-status">✨</span>
                    </div>
                    <div class="agent-role" style="color: #ccc; font-size: 12px; margin-bottom: 10px;">Mystic Oracle</div>
                    <div class="reasoning-trace">Reading ethereal currents...</div>
                    <div class="emotion-indicators">
                        <span class="emotion mystical">🌟</span>
                        <span class="emotion wisdom">📜</span>
                        <span class="emotion prophecy">🔮</span>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            {renderer._get_gsap_initialization()}
            {renderer._get_agent_animations()}
            {renderer._get_global_functions()}
            
            // Demo Functions
            function demoThinking() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const reasoningSteps = [
                    'Analyzing current situation...',
                    'Considering available options...',
                    'Evaluating potential outcomes...',
                    'Making decision...'
                ];
                animateAgentThinking(randomAgent, reasoningSteps);
            }}
            
            function demoMemoryUpdate() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const importance = Math.floor(Math.random() * 4) + 1;
                animateAgentMemoryUpdate(randomAgent, 'observation', importance);
            }}
            
            function demoDecision() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const decisions = ['attack', 'defend', 'investigate', 'communicate', 'cast_spell'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const randomDecision = decisions[Math.floor(Math.random() * decisions.length)];
                const confidence = Math.random();
                animateAgentDecision(randomAgent, randomDecision, confidence);
            }}
            
            function demoAlert() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const alertTypes = ['threat', 'opportunity', 'communication', 'memory'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const randomAlert = alertTypes[Math.floor(Math.random() * alertTypes.length)];
                const urgency = Math.floor(Math.random() * 10) + 1;
                animateAgentAlert(randomAgent, randomAlert, urgency);
            }}
            
            function demoReasoningFlow() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const reasoningChain = [
                    {{ content: 'Observe environment', confidence: 0.9 }},
                    {{ content: 'Identify potential threats', confidence: 0.7 }},
                    {{ content: 'Assess threat level', confidence: 0.8 }},
                    {{ content: 'Plan response strategy', confidence: 0.6 }},
                    {{ content: 'Execute action', confidence: 0.85 }}
                ];
                animateReasoningFlow(randomAgent, reasoningChain);
            }}
            
            function demoCommunication() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const fromAgent = agents[Math.floor(Math.random() * agents.length)];
                let toAgent = agents[Math.floor(Math.random() * agents.length)];
                while (toAgent === fromAgent) {{
                    toAgent = agents[Math.floor(Math.random() * agents.length)];
                }}
                animateCommunicationFlow(fromAgent.replace('agent-', ''), toAgent.replace('agent-', ''), 'Test message', 7);
            }}
            
            function demoEmotions() {{
                const agents = ['agent-karczmarz', 'agent-skrytobojca', 'agent-wiedzma'];
                const emotions = ['alertness', 'satisfaction', 'suspicion', 'stealth', 'cunning', 'mystical', 'wisdom'];
                const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
                const intensity = Math.random();
                animateEmotionChange(randomAgent, randomEmotion, intensity);
            }}
            
            // Initialize on load
            document.addEventListener('DOMContentLoaded', function() {{
                initializeAgentAnimations();
                
                // Auto-demo every 3 seconds
                setInterval(() => {{
                    const demos = [demoThinking, demoMemoryUpdate, demoAlert, demoEmotions];
                    const randomDemo = demos[Math.floor(Math.random() * demos.length)];
                    randomDemo();
                }}, 3000);
            }});
        </script>
    </body>
    </html>
    """
    
    return demo_html

def main():
    """Main demo function"""
    st.set_page_config(
        page_title="GSAP Agent Visualization Demo",
        page_icon="🏰",
        layout="wide"
    )
    
    st.title("🏰 Enhanced GSAP Agent Visualization Demo")
    st.markdown("**Real-time agent animations with reasoning traces, emotions, and status updates**")
    
    # Generate and display the demo
    demo_html = create_enhanced_agent_demo()
    
    # Display in Streamlit
    st.components.v1.html(demo_html, height=800, scrolling=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Features Demonstrated:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Agent Animations:**
        - 🧠 Thinking animations with reasoning steps
        - 💭 Memory update indicators
        - ⚔️ Decision overlays with confidence
        - 🚨 Alert system with urgency levels
        """)
    
    with col2:
        st.markdown("""
        **Visual Effects:**
        - 🔄 Real-time reasoning flow
        - 💬 Communication flow between agents
        - 😊 Emotion state changes
        - ⚡ Performance optimized (138% GSAP)
        """)
    
    st.markdown("---")
    st.markdown("**Click the demo buttons above to trigger different animations!**")

if __name__ == "__main__":
    main()
