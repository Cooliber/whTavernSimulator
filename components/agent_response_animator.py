#!/usr/bin/env python3
"""
Agent Response Animation System for Warhammer Tavern Simulator
Ensures every agent response is properly animated and displayed with GSAP
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class AgentResponse:
    """Structured agent response for animation"""
    agent_id: str
    agent_name: str
    response_type: str  # thinking, speaking, acting, deciding, alerting
    content: str
    confidence: float
    emotion: str
    reasoning_steps: List[str]
    timestamp: datetime
    duration: float = 3.0  # Animation duration in seconds
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical

@dataclass
class AnimationState:
    """Current animation state tracking"""
    active_animations: Dict[str, AgentResponse]
    animation_queue: List[AgentResponse]
    last_update: datetime
    performance_metrics: Dict[str, float]

class AgentResponseAnimator:
    """
    Manages and animates all agent responses with GSAP integration
    Ensures stable, calm operation with smooth animations
    """
    
    def __init__(self):
        self.component_id = "agent_response_animator"
        self.animation_state = AnimationState(
            active_animations={},
            animation_queue=[],
            last_update=datetime.now(),
            performance_metrics={"fps": 60, "memory": 0, "queue_size": 0}
        )
        
        # Initialize session state
        if 'agent_animator_state' not in st.session_state:
            st.session_state.agent_animator_state = {
                'responses': [],
                'active_agents': set(),
                'animation_enabled': True,
                'performance_mode': 'balanced'  # smooth, balanced, performance
            }
    
    def add_agent_response(self, response: AgentResponse):
        """Add a new agent response to the animation queue"""
        # Add to session state
        st.session_state.agent_animator_state['responses'].append(asdict(response))
        st.session_state.agent_animator_state['active_agents'].add(response.agent_id)
        
        # Add to animation queue
        self.animation_state.animation_queue.append(response)
        self.animation_state.performance_metrics['queue_size'] = len(self.animation_state.animation_queue)
        
        # Trigger animation update
        self._trigger_animation_update()
    
    def render_agent_response_system(self, agents: List[Dict], height: int = 600) -> Optional[Dict]:
        """Render the complete agent response animation system"""
        
        # Generate HTML with embedded agent data and animations
        html_content = self._generate_animation_html(agents)
        
        # Render component
        component_value = components.html(
            html_content,
            height=height,
            scrolling=False
        )
        
        # Process any return data
        if component_value and isinstance(component_value, dict):
            self._process_animation_feedback(component_value)
        
        return component_value
    
    def _generate_animation_html(self, agents: List[Dict]) -> str:
        """Generate complete HTML with GSAP animations for agent responses"""
        
        responses_data = st.session_state.agent_animator_state.get('responses', [])
        performance_mode = st.session_state.agent_animator_state.get('performance_mode', 'balanced')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Agent Response Animator</title>
            
            <!-- GSAP Core and Plugins -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/MorphSVGPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/DrawSVGPlugin.min.js"></script>
            
            <style>
                {self._get_animation_css()}
            </style>
        </head>
        <body>
            <div id="agent-response-container">
                <div id="agent-grid">
                    {self._generate_agent_grid_html(agents)}
                </div>
                
                <div id="response-overlay">
                    <div id="active-responses"></div>
                    <div id="response-queue"></div>
                </div>
                
                <div id="performance-monitor">
                    <div class="metric">FPS: <span id="fps-counter">60</span></div>
                    <div class="metric">Queue: <span id="queue-size">0</span></div>
                    <div class="metric">Active: <span id="active-count">0</span></div>
                </div>
            </div>
            
            <script>
                // Embedded data
                const AGENTS_DATA = {json.dumps(agents)};
                const RESPONSES_DATA = {json.dumps(responses_data)};
                const PERFORMANCE_MODE = "{performance_mode}";
                
                // Initialize animation system
                {self._get_animation_javascript()}
            </script>
        </body>
        </html>
        """
    
    def _get_animation_css(self) -> str:
        """Get CSS styles for agent response animations"""
        return """
            body {
                margin: 0;
                padding: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: #ffffff;
                overflow-x: hidden;
            }
            
            #agent-response-container {
                position: relative;
                width: 100%;
                height: 100vh;
            }
            
            #agent-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                padding: 20px;
            }
            
            .agent-card {
                background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 100%);
                border: 2px solid rgba(255, 215, 0, 0.3);
                border-radius: 12px;
                padding: 15px;
                position: relative;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .agent-card:hover {
                border-color: rgba(255, 215, 0, 0.6);
                transform: translateY(-2px);
            }
            
            .agent-header {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .agent-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: linear-gradient(45deg, #8b0000, #ff4500);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                margin-right: 10px;
            }
            
            .agent-name {
                font-size: 16px;
                font-weight: bold;
                color: #ffd700;
            }
            
            .agent-status {
                font-size: 12px;
                color: #cccccc;
                margin-top: 2px;
            }
            
            .agent-response-area {
                min-height: 60px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                position: relative;
                overflow: hidden;
            }
            
            .response-bubble {
                position: absolute;
                top: -50px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 215, 0, 0.9);
                color: #000;
                padding: 10px 15px;
                border-radius: 20px;
                font-size: 14px;
                max-width: 200px;
                text-align: center;
                z-index: 1000;
                opacity: 0;
                pointer-events: none;
            }
            
            .response-bubble::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid rgba(255, 215, 0, 0.9);
            }
            
            .thinking-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #ffd700;
                margin: 0 2px;
                opacity: 0.3;
            }
            
            .emotion-indicator {
                position: absolute;
                top: 10px;
                right: 10px;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: #00ff00;
                opacity: 0.7;
            }
            
            .confidence-bar {
                position: absolute;
                bottom: 5px;
                left: 10px;
                right: 10px;
                height: 3px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 2px;
                overflow: hidden;
            }
            
            .confidence-fill {
                height: 100%;
                background: linear-gradient(90deg, #ff4444, #ffff44, #44ff44);
                width: 0%;
                transition: width 0.5s ease;
            }
            
            #response-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 999;
            }
            
            #performance-monitor {
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.8);
                padding: 10px;
                border-radius: 8px;
                font-size: 12px;
                z-index: 1001;
            }
            
            .metric {
                margin: 2px 0;
                color: #ffd700;
            }
            
            /* Animation classes */
            .agent-thinking {
                animation: thinking-pulse 2s infinite;
            }
            
            .agent-speaking {
                animation: speaking-glow 1s ease-in-out;
            }
            
            .agent-deciding {
                animation: deciding-flash 0.5s ease-in-out;
            }
            
            .agent-alerting {
                animation: alerting-urgent 0.3s ease-in-out infinite;
            }
            
            @keyframes thinking-pulse {
                0%, 100% { box-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
                50% { box-shadow: 0 0 25px rgba(255, 215, 0, 0.8); }
            }
            
            @keyframes speaking-glow {
                0% { box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
                50% { box-shadow: 0 0 30px rgba(0, 255, 0, 0.8); }
                100% { box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
            }
            
            @keyframes deciding-flash {
                0% { background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 100%); }
                50% { background: linear-gradient(135deg, #4a2c1a 0%, #6b3e2a 100%); }
                100% { background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 100%); }
            }
            
            @keyframes alerting-urgent {
                0%, 100% { border-color: rgba(255, 0, 0, 0.5); }
                50% { border-color: rgba(255, 0, 0, 1); }
            }
        """
    
    def _generate_agent_grid_html(self, agents: List[Dict]) -> str:
        """Generate HTML for the agent grid"""
        html = ""
        for agent in agents:
            agent_id = agent.get('id', agent.get('name', 'unknown')).lower().replace(' ', '_')
            html += f"""
            <div class="agent-card" id="agent-{agent_id}" data-agent-id="{agent_id}">
                <div class="agent-header">
                    <div class="agent-avatar">{agent.get('name', 'A')[0]}</div>
                    <div>
                        <div class="agent-name">{agent.get('name', 'Unknown')}</div>
                        <div class="agent-status" id="status-{agent_id}">Ready</div>
                    </div>
                </div>
                
                <div class="agent-response-area" id="response-{agent_id}">
                    <div class="thinking-indicator"></div>
                    <div class="thinking-indicator"></div>
                    <div class="thinking-indicator"></div>
                </div>
                
                <div class="response-bubble" id="bubble-{agent_id}"></div>
                <div class="emotion-indicator" id="emotion-{agent_id}"></div>
                
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidence-{agent_id}"></div>
                </div>
            </div>
            """
        return html
    
    def _trigger_animation_update(self):
        """Trigger an animation update"""
        st.session_state.agent_animator_state['last_update'] = datetime.now().isoformat()
        # Force a rerun to update the component
        st.rerun()
    
    def _process_animation_feedback(self, data: Dict):
        """Process feedback from the animation system"""
        try:
            if 'performance' in data:
                self.animation_state.performance_metrics.update(data['performance'])
            
            if 'completed_animations' in data:
                # Remove completed animations from active list
                for agent_id in data['completed_animations']:
                    if agent_id in self.animation_state.active_animations:
                        del self.animation_state.active_animations[agent_id]
            
            if 'errors' in data:
                st.error(f"Animation errors: {data['errors']}")
                
        except Exception as e:
            st.error(f"Error processing animation feedback: {e}")
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        return self.animation_state.performance_metrics.copy()
    
    def clear_agent_responses(self, agent_id: Optional[str] = None):
        """Clear responses for a specific agent or all agents"""
        if agent_id:
            # Clear specific agent
            st.session_state.agent_animator_state['responses'] = [
                r for r in st.session_state.agent_animator_state['responses'] 
                if r.get('agent_id') != agent_id
            ]
            st.session_state.agent_animator_state['active_agents'].discard(agent_id)
        else:
            # Clear all
            st.session_state.agent_animator_state['responses'] = []
            st.session_state.agent_animator_state['active_agents'] = set()
        
        self._trigger_animation_update()
    
    def set_performance_mode(self, mode: str):
        """Set animation performance mode"""
        valid_modes = ['smooth', 'balanced', 'performance']
        if mode in valid_modes:
            st.session_state.agent_animator_state['performance_mode'] = mode
            self._trigger_animation_update()
    
    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent is currently active/animating"""
        return agent_id in st.session_state.agent_animator_state['active_agents']

    def _get_animation_javascript(self) -> str:
        """Get the main JavaScript animation code"""
        return """
            // Global animation system variables
            let animationSystem = {
                activeAnimations: new Map(),
                animationQueue: [],
                performanceMetrics: { fps: 60, memory: 0, queueSize: 0 },
                isRunning: false,
                frameCount: 0,
                lastTime: performance.now()
            };

            // Initialize the animation system
            function initializeAnimationSystem() {
                console.log('🎭 Initializing Agent Response Animation System...');

                // Set up performance monitoring
                setupPerformanceMonitoring();

                // Initialize GSAP settings
                gsap.config({
                    force3D: true,
                    nullTargetWarn: false
                });

                // Create custom eases for agent animations
                gsap.registerEase("agentThinking", "power2.inOut");
                gsap.registerEase("agentSpeaking", "back.out(1.7)");
                gsap.registerEase("agentDeciding", "elastic.out(1, 0.3)");

                // Start the animation loop
                startAnimationLoop();

                // Process initial responses
                processResponseQueue();

                console.log('✅ Animation system initialized successfully');
            }

            function setupPerformanceMonitoring() {
                setInterval(() => {
                    const now = performance.now();
                    const deltaTime = now - animationSystem.lastTime;

                    if (animationSystem.frameCount > 0) {
                        animationSystem.performanceMetrics.fps = Math.round(1000 / (deltaTime / animationSystem.frameCount));
                    }

                    if (performance.memory) {
                        animationSystem.performanceMetrics.memory = Math.round(performance.memory.usedJSHeapSize / 1048576);
                    }

                    animationSystem.performanceMetrics.queueSize = animationSystem.animationQueue.length;

                    // Update UI
                    updatePerformanceDisplay();

                    // Send metrics to Streamlit
                    sendMetricsToStreamlit();

                    animationSystem.frameCount = 0;
                    animationSystem.lastTime = now;
                }, 1000);
            }

            function updatePerformanceDisplay() {
                const fpsEl = document.getElementById('fps-counter');
                const queueEl = document.getElementById('queue-size');
                const activeEl = document.getElementById('active-count');

                if (fpsEl) fpsEl.textContent = animationSystem.performanceMetrics.fps;
                if (queueEl) queueEl.textContent = animationSystem.performanceMetrics.queueSize;
                if (activeEl) activeEl.textContent = animationSystem.activeAnimations.size;
            }

            function startAnimationLoop() {
                if (animationSystem.isRunning) return;

                animationSystem.isRunning = true;

                function animationFrame() {
                    animationSystem.frameCount++;

                    // Process animation queue
                    processResponseQueue();

                    // Update thinking indicators
                    updateThinkingIndicators();

                    // Continue loop
                    if (animationSystem.isRunning) {
                        requestAnimationFrame(animationFrame);
                    }
                }

                requestAnimationFrame(animationFrame);
            }

            function processResponseQueue() {
                // Process responses from RESPONSES_DATA
                RESPONSES_DATA.forEach((response, index) => {
                    if (!animationSystem.activeAnimations.has(response.agent_id)) {
                        animateAgentResponse(response);
                    }
                });
            }

            function animateAgentResponse(response) {
                const agentId = response.agent_id;
                const agentCard = document.getElementById(`agent-${agentId}`);

                if (!agentCard) {
                    console.warn(`Agent card not found: ${agentId}`);
                    return;
                }

                // Mark as active
                animationSystem.activeAnimations.set(agentId, response);

                // Animate based on response type
                switch (response.response_type) {
                    case 'thinking':
                        animateThinking(agentCard, response);
                        break;
                    case 'speaking':
                        animateSpeaking(agentCard, response);
                        break;
                    case 'acting':
                        animateActing(agentCard, response);
                        break;
                    case 'deciding':
                        animateDeciding(agentCard, response);
                        break;
                    case 'alerting':
                        animateAlerting(agentCard, response);
                        break;
                    default:
                        animateGenericResponse(agentCard, response);
                }
            }

            function animateThinking(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);
                const responseArea = document.getElementById(`response-${agentId}`);
                const thinkingDots = responseArea.querySelectorAll('.thinking-indicator');

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Thinking...",
                        color: "#ffaa00"
                    });
                }

                // Add thinking class
                agentCard.classList.add('agent-thinking');

                // Animate thinking dots
                gsap.to(thinkingDots, {
                    duration: 0.6,
                    opacity: 1,
                    scale: 1.2,
                    ease: "agentThinking",
                    stagger: 0.2,
                    repeat: -1,
                    yoyo: true
                });

                // Show reasoning steps if available
                if (response.reasoning_steps && response.reasoning_steps.length > 0) {
                    animateReasoningSteps(agentCard, response.reasoning_steps);
                }

                // Auto-complete after duration
                setTimeout(() => {
                    completeThinking(agentCard, response);
                }, response.duration * 1000);
            }

            function animateSpeaking(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);
                const bubble = document.getElementById(`bubble-${agentId}`);

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Speaking",
                        color: "#00ff00"
                    });
                }

                // Add speaking class
                agentCard.classList.add('agent-speaking');

                // Show speech bubble
                if (bubble) {
                    bubble.textContent = response.content;

                    gsap.fromTo(bubble, {
                        opacity: 0,
                        y: 20,
                        scale: 0.8
                    }, {
                        opacity: 1,
                        y: 0,
                        scale: 1,
                        duration: 0.5,
                        ease: "agentSpeaking"
                    });

                    // Hide after duration
                    setTimeout(() => {
                        gsap.to(bubble, {
                            opacity: 0,
                            y: -20,
                            scale: 0.8,
                            duration: 0.3,
                            ease: "power2.in"
                        });
                    }, response.duration * 1000);
                }

                // Auto-complete
                setTimeout(() => {
                    completeSpeaking(agentCard, response);
                }, response.duration * 1000);
            }

            function animateActing(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Acting",
                        color: "#ff6600"
                    });
                }

                // Action animation
                gsap.to(agentCard, {
                    duration: 0.4,
                    scale: 1.05,
                    rotation: 2,
                    ease: "power2.out",
                    yoyo: true,
                    repeat: 1
                });

                // Show confidence
                updateConfidenceBar(agentId, response.confidence);

                // Auto-complete
                setTimeout(() => {
                    completeAction(agentCard, response);
                }, response.duration * 1000);
            }

            function animateDeciding(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Deciding",
                        color: "#aa00ff"
                    });
                }

                // Add deciding class
                agentCard.classList.add('agent-deciding');

                // Decision animation
                gsap.to(agentCard, {
                    duration: 0.3,
                    boxShadow: "0 0 30px rgba(170, 0, 255, 0.8)",
                    ease: "agentDeciding",
                    repeat: 2,
                    yoyo: true
                });

                // Show confidence
                updateConfidenceBar(agentId, response.confidence);

                // Auto-complete
                setTimeout(() => {
                    completeDecision(agentCard, response);
                }, response.duration * 1000);
            }

            function animateAlerting(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "ALERT!",
                        color: "#ff0000"
                    });
                }

                // Add alerting class
                agentCard.classList.add('agent-alerting');

                // Urgent alert animation
                gsap.to(agentCard, {
                    duration: 0.2,
                    scale: 1.1,
                    boxShadow: "0 0 40px rgba(255, 0, 0, 1)",
                    ease: "power2.out",
                    repeat: 5,
                    yoyo: true
                });

                // Auto-complete
                setTimeout(() => {
                    completeAlert(agentCard, response);
                }, response.duration * 1000);
            }

            function animateGenericResponse(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                // Update status
                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Active",
                        color: "#ffd700"
                    });
                }

                // Generic pulse animation
                gsap.to(agentCard, {
                    duration: 0.5,
                    boxShadow: "0 0 20px rgba(255, 215, 0, 0.6)",
                    ease: "power2.inOut",
                    repeat: 1,
                    yoyo: true
                });

                // Auto-complete
                setTimeout(() => {
                    completeGenericResponse(agentCard, response);
                }, response.duration * 1000);
            }

            function updateConfidenceBar(agentId, confidence) {
                const confidenceBar = document.getElementById(`confidence-${agentId}`);
                if (confidenceBar) {
                    gsap.to(confidenceBar, {
                        duration: 0.8,
                        width: `${confidence * 100}%`,
                        ease: "power2.out"
                    });
                }
            }

            function updateThinkingIndicators() {
                // Animate thinking indicators for active thinking agents
                document.querySelectorAll('.agent-thinking .thinking-indicator').forEach((dot, index) => {
                    if (!dot.hasAttribute('data-animated')) {
                        dot.setAttribute('data-animated', 'true');
                        gsap.to(dot, {
                            duration: 0.6,
                            opacity: 1,
                            scale: 1.3,
                            delay: index * 0.2,
                            ease: "power2.inOut",
                            repeat: -1,
                            yoyo: true
                        });
                    }
                });
            }

            function completeThinking(agentCard, response) {
                agentCard.classList.remove('agent-thinking');
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                // Stop thinking dots
                const thinkingDots = agentCard.querySelectorAll('.thinking-indicator');
                gsap.to(thinkingDots, {
                    duration: 0.3,
                    opacity: 0.3,
                    scale: 1
                });

                completeAnimation(agentId);
            }

            function completeSpeaking(agentCard, response) {
                agentCard.classList.remove('agent-speaking');
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                completeAnimation(agentId);
            }

            function completeAction(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                completeAnimation(agentId);
            }

            function completeDecision(agentCard, response) {
                agentCard.classList.remove('agent-deciding');
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                completeAnimation(agentId);
            }

            function completeAlert(agentCard, response) {
                agentCard.classList.remove('agent-alerting');
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                completeAnimation(agentId);
            }

            function completeGenericResponse(agentCard, response) {
                const agentId = response.agent_id;
                const statusEl = document.getElementById(`status-${agentId}`);

                if (statusEl) {
                    gsap.to(statusEl, {
                        duration: 0.3,
                        text: "Ready",
                        color: "#ffffff"
                    });
                }

                completeAnimation(agentId);
            }

            function completeAnimation(agentId) {
                // Remove from active animations
                animationSystem.activeAnimations.delete(agentId);

                // Send completion notification to Streamlit
                sendCompletionToStreamlit(agentId);
            }

            function sendMetricsToStreamlit() {
                if (window.parent) {
                    window.parent.postMessage({
                        type: 'performance',
                        data: animationSystem.performanceMetrics
                    }, '*');
                }
            }

            function sendCompletionToStreamlit(agentId) {
                if (window.parent) {
                    window.parent.postMessage({
                        type: 'animation_complete',
                        agent_id: agentId
                    }, '*');
                }
            }

            // Initialize when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeAnimationSystem);
            } else {
                initializeAnimationSystem();
            }
        """
