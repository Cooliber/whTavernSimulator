#!/usr/bin/env python3
"""
Matrix-Style Chat Interface for Warhammer Tavern Simulator
Advanced conversation visualization with flowing text effects and multi-dimensional chat bubbles
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from .matrix_audio_system import MatrixAudioSystem
from .matrix_performance_optimizer import MatrixPerformanceOptimizer

@dataclass
class ChatMessage:
    """Enhanced chat message structure"""
    id: str
    sender: str
    receiver: str
    content: str
    message_type: str  # "whisper", "shout", "thought", "action", "magic"
    emotion: str  # "angry", "happy", "mysterious", "urgent", "calm"
    priority: int  # 1-10
    timestamp: datetime
    effects: List[str]  # ["matrix", "glow", "shake", "fade", "typewriter"]
    color_theme: str  # "gold", "red", "green", "blue", "purple"
    duration: float = 5.0

@dataclass
class ConversationFlow:
    """Tracks conversation flow and relationships"""
    participants: List[str]
    message_chain: List[str]  # Message IDs in order
    conversation_type: str  # "private", "group", "broadcast", "rumor"
    intensity: float  # 0.0 - 1.0
    active: bool = True

class MatrixChatInterface:
    """
    Advanced chat interface with Matrix-style effects and multi-dimensional conversations
    """
    
    def __init__(self):
        self.component_id = "matrix_chat_interface"
        self.audio_system = MatrixAudioSystem()
        self.performance_optimizer = MatrixPerformanceOptimizer()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state for chat interface"""
        if 'matrix_chat_state' not in st.session_state:
            st.session_state.matrix_chat_state = {
                'messages': [],
                'conversations': {},
                'active_effects': [],
                'chat_settings': {
                    'matrix_mode': True,
                    'auto_scroll': True,
                    'sound_enabled': True,
                    'effect_intensity': 0.8,
                    'max_messages': 100
                },
                'performance': {
                    'fps': 60,
                    'particles': 500,
                    'effects_quality': 'high'
                }
            }
    
    def add_message(self, message: ChatMessage):
        """Add a new message to the chat system"""
        # Convert to dict for session state
        message_dict = asdict(message)
        message_dict['timestamp'] = message.timestamp.isoformat()
        
        # Add to messages
        st.session_state.matrix_chat_state['messages'].append(message_dict)
        
        # Maintain message limit
        max_messages = st.session_state.matrix_chat_state['chat_settings']['max_messages']
        if len(st.session_state.matrix_chat_state['messages']) > max_messages:
            st.session_state.matrix_chat_state['messages'] = \
                st.session_state.matrix_chat_state['messages'][-max_messages:]
        
        # Update conversation flow
        self._update_conversation_flow(message)
        
        # Trigger rerun for real-time updates
        st.rerun()
    
    def render_matrix_chat(self, height: int = 700) -> Optional[Dict]:
        """Render the complete Matrix-style chat interface"""
        
        # Get current state
        messages = st.session_state.matrix_chat_state.get('messages', [])
        settings = st.session_state.matrix_chat_state.get('chat_settings', {})
        
        # Generate HTML with Matrix effects
        html_content = self._generate_matrix_chat_html(messages, settings)
        
        # Render component
        component_value = components.html(
            html_content,
            height=height,
            scrolling=False
        )
        
        return component_value
    
    def _generate_matrix_chat_html(self, messages: List[Dict], settings: Dict) -> str:
        """Generate complete HTML with Matrix-style chat effects"""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Matrix Chat Interface</title>
            
            <!-- GSAP Core and Plugins -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/MorphSVGPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/DrawSVGPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/PixiPlugin.min.js"></script>
            
            <!-- Particles.js for Matrix rain effect -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js"></script>
            
            <!-- Howler.js for sound effects -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
            
            <style>
                {self._get_matrix_chat_css()}
                {self.audio_system.get_audio_css()}
                {self.performance_optimizer.get_performance_css()}
            </style>
        </head>
        <body>
            <div id="matrix-chat-container">
                <!-- Matrix rain background -->
                <div id="matrix-rain"></div>
                
                <!-- Chat interface -->
                <div id="chat-interface">
                    <div id="chat-header">
                        <div class="header-title">🏰 Tavern Communications</div>
                        <div class="header-controls">
                            <button id="matrix-toggle" class="control-btn">Matrix Mode</button>
                            <button id="clear-chat" class="control-btn">Clear</button>
                        </div>
                    </div>
                    
                    <div id="chat-messages">
                        <div id="message-container"></div>
                    </div>
                    
                    <div id="chat-input-area">
                        <div id="typing-indicators"></div>
                        <div id="conversation-flows"></div>
                    </div>
                </div>
                
                <!-- Floating conversation bubbles -->
                <div id="floating-conversations"></div>
                
                <!-- Performance monitor -->
                <div id="performance-monitor">
                    <div class="metric">FPS: <span id="fps-display">60</span></div>
                    <div class="metric">Messages: <span id="message-count">0</span></div>
                    <div class="metric">Effects: <span id="effect-count">0</span></div>
                </div>

                <!-- Audio controls -->
                {self.audio_system.render_audio_controls()}

                <!-- Performance controls -->
                {self.performance_optimizer.render_performance_controls()}
            </div>
            
            <script>
                // Embedded data
                const MESSAGES_DATA = {json.dumps(messages)};
                const CHAT_SETTINGS = {json.dumps(settings)};
                
                // Initialize Matrix Chat System
                {self._get_matrix_chat_javascript()}

                // Initialize Audio System
                {self.audio_system.get_audio_javascript()}

                // Initialize Performance Optimizer
                {self.performance_optimizer.get_performance_javascript()}
            </script>
        </body>
        </html>
        """
    
    def _update_conversation_flow(self, message: ChatMessage):
        """Update conversation flow tracking"""
        conversations = st.session_state.matrix_chat_state.get('conversations', {})
        
        # Create conversation key
        participants = sorted([message.sender, message.receiver])
        conv_key = f"{participants[0]}_{participants[1]}"
        
        if conv_key not in conversations:
            conversations[conv_key] = {
                'participants': participants,
                'message_chain': [],
                'conversation_type': 'private',
                'intensity': 0.5,
                'active': True,
                'last_activity': datetime.now().isoformat()
            }
        
        # Update conversation
        conversations[conv_key]['message_chain'].append(message.id)
        conversations[conv_key]['last_activity'] = datetime.now().isoformat()
        conversations[conv_key]['active'] = True
        
        # Update intensity based on message priority and frequency
        if message.priority > 7:
            conversations[conv_key]['intensity'] = min(1.0, conversations[conv_key]['intensity'] + 0.2)
        
        st.session_state.matrix_chat_state['conversations'] = conversations
    
    def get_active_conversations(self) -> List[Dict]:
        """Get list of currently active conversations"""
        conversations = st.session_state.matrix_chat_state.get('conversations', {})
        active_convs = []
        
        for conv_key, conv_data in conversations.items():
            if conv_data.get('active', False):
                active_convs.append({
                    'key': conv_key,
                    'participants': conv_data['participants'],
                    'intensity': conv_data['intensity'],
                    'message_count': len(conv_data['message_chain']),
                    'last_activity': conv_data['last_activity']
                })
        
        return sorted(active_convs, key=lambda x: x['intensity'], reverse=True)
    
    def clear_chat(self):
        """Clear all chat messages and conversations"""
        st.session_state.matrix_chat_state['messages'] = []
        st.session_state.matrix_chat_state['conversations'] = {}
        st.session_state.matrix_chat_state['active_effects'] = []
        st.rerun()
    
    def set_chat_settings(self, **kwargs):
        """Update chat settings"""
        settings = st.session_state.matrix_chat_state.get('chat_settings', {})
        settings.update(kwargs)
        st.session_state.matrix_chat_state['chat_settings'] = settings
        st.rerun()

    def _get_matrix_chat_css(self) -> str:
        """Get CSS styles for Matrix chat interface"""
        return """
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Orbitron', monospace;
                background: #000;
                color: #00ff00;
                overflow: hidden;
                height: 100vh;
            }

            #matrix-chat-container {
                position: relative;
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #000000 0%, #001100 50%, #000000 100%);
            }

            #matrix-rain {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
                opacity: 0.3;
            }

            #chat-interface {
                position: relative;
                z-index: 10;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                backdrop-filter: blur(2px);
            }

            #chat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: rgba(0, 255, 0, 0.1);
                border-bottom: 2px solid #00ff00;
                box-shadow: 0 2px 10px rgba(0, 255, 0, 0.3);
            }

            .header-title {
                font-size: 24px;
                font-weight: 900;
                text-shadow: 0 0 10px #00ff00;
                animation: matrix-glow 2s ease-in-out infinite alternate;
            }

            .header-controls {
                display: flex;
                gap: 10px;
            }

            .control-btn {
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Orbitron', monospace;
                font-weight: 700;
                transition: all 0.3s ease;
            }

            .control-btn:hover {
                background: rgba(0, 255, 0, 0.4);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
                transform: scale(1.05);
            }

            #chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                position: relative;
            }

            #message-container {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .chat-message {
                position: relative;
                padding: 15px 20px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
                opacity: 0;
                transform: translateY(20px);
                animation: message-appear 0.5s ease-out forwards;
            }

            .message-sender {
                align-self: flex-start;
                background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.1));
                border-left: 4px solid #00ff00;
                margin-left: 0;
            }

            .message-receiver {
                align-self: flex-end;
                background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.1));
                border-right: 4px solid #ffd700;
                margin-right: 0;
            }

            .message-broadcast {
                align-self: center;
                background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(200, 0, 0, 0.1));
                border: 2px solid #ff0000;
                text-align: center;
                max-width: 90%;
            }

            .message-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
                font-size: 12px;
                opacity: 0.8;
            }

            .message-sender-name {
                font-weight: 700;
                text-shadow: 0 0 5px currentColor;
            }

            .message-timestamp {
                font-size: 10px;
                opacity: 0.6;
            }

            .message-content {
                font-size: 14px;
                line-height: 1.4;
                position: relative;
            }

            .message-effects {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 5;
            }

            /* Message type specific styles */
            .message-whisper {
                font-style: italic;
                opacity: 0.7;
                font-size: 12px;
            }

            .message-shout {
                font-weight: 900;
                text-transform: uppercase;
                font-size: 16px;
                animation: shout-pulse 0.5s ease-in-out;
            }

            .message-thought {
                font-style: italic;
                opacity: 0.6;
                border-style: dashed;
            }

            .message-action {
                background: rgba(255, 165, 0, 0.2);
                border-left: 4px solid #ff6600;
                font-weight: 700;
            }

            .message-magic {
                background: rgba(138, 43, 226, 0.2);
                border: 2px solid #8a2be2;
                animation: magic-shimmer 2s ease-in-out infinite;
            }

            /* Emotion-based colors */
            .emotion-angry { color: #ff4444; text-shadow: 0 0 10px #ff4444; }
            .emotion-happy { color: #44ff44; text-shadow: 0 0 10px #44ff44; }
            .emotion-mysterious { color: #8a2be2; text-shadow: 0 0 10px #8a2be2; }
            .emotion-urgent { color: #ff6600; text-shadow: 0 0 10px #ff6600; }
            .emotion-calm { color: #4488ff; text-shadow: 0 0 10px #4488ff; }

            #floating-conversations {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 15;
            }

            .floating-bubble {
                position: absolute;
                background: rgba(0, 255, 0, 0.8);
                color: #000;
                padding: 10px 15px;
                border-radius: 20px;
                font-size: 12px;
                max-width: 200px;
                opacity: 0;
                transform: scale(0.5);
                animation: bubble-float 3s ease-in-out forwards;
            }

            .floating-bubble::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid rgba(0, 255, 0, 0.8);
            }

            #performance-monitor {
                position: fixed;
                bottom: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #00ff00;
                padding: 10px;
                border-radius: 5px;
                font-size: 10px;
                z-index: 20;
            }

            .metric {
                margin: 2px 0;
                color: #00ff00;
            }

            /* Animations */
            @keyframes matrix-glow {
                0% { text-shadow: 0 0 10px #00ff00; }
                100% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }

            @keyframes message-appear {
                0% {
                    opacity: 0;
                    transform: translateY(20px) scale(0.9);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            @keyframes shout-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            @keyframes magic-shimmer {
                0%, 100% { box-shadow: 0 0 10px rgba(138, 43, 226, 0.5); }
                50% { box-shadow: 0 0 25px rgba(138, 43, 226, 0.8); }
            }

            @keyframes bubble-float {
                0% {
                    opacity: 0;
                    transform: scale(0.5) translateY(20px);
                }
                20% {
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }
                80% {
                    opacity: 1;
                    transform: scale(1) translateY(-10px);
                }
                100% {
                    opacity: 0;
                    transform: scale(0.8) translateY(-30px);
                }
            }

            /* Scrollbar styling */
            #chat-messages::-webkit-scrollbar {
                width: 8px;
            }

            #chat-messages::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
            }

            #chat-messages::-webkit-scrollbar-thumb {
                background: rgba(0, 255, 0, 0.5);
                border-radius: 4px;
            }

            #chat-messages::-webkit-scrollbar-thumb:hover {
                background: rgba(0, 255, 0, 0.8);
            }
        """

    def _get_matrix_chat_javascript(self) -> str:
        """Get JavaScript for Matrix chat effects"""
        return """
            // Global Matrix Chat System
            let matrixChatSystem = {
                messages: [],
                conversations: new Map(),
                activeEffects: new Set(),
                performanceMetrics: { fps: 60, messageCount: 0, effectCount: 0 },
                settings: {
                    matrixMode: true,
                    autoScroll: true,
                    soundEnabled: true,
                    effectIntensity: 0.8
                },
                isInitialized: false
            };

            // Initialize Matrix Chat System
            function initializeMatrixChat() {
                console.log('🔋 Initializing Matrix Chat Interface...');

                // Load embedded data
                matrixChatSystem.messages = MESSAGES_DATA || [];
                matrixChatSystem.settings = { ...matrixChatSystem.settings, ...CHAT_SETTINGS };

                // Initialize Matrix rain effect
                initializeMatrixRain();

                // Initialize GSAP settings
                gsap.config({
                    force3D: true,
                    nullTargetWarn: false
                });

                // Register custom eases
                gsap.registerEase("matrixGlow", "power2.inOut");
                gsap.registerEase("messageFlow", "back.out(1.7)");
                gsap.registerEase("bubbleFloat", "elastic.out(1, 0.3)");

                // Set up event listeners
                setupEventListeners();

                // Start performance monitoring
                startPerformanceMonitoring();

                // Render initial messages
                renderAllMessages();

                // Start animation loop
                startMatrixAnimationLoop();

                matrixChatSystem.isInitialized = true;
                console.log('✅ Matrix Chat System initialized successfully');
            }

            function initializeMatrixRain() {
                if (!matrixChatSystem.settings.matrixMode) return;

                // Create Matrix rain effect using particles.js
                particlesJS('matrix-rain', {
                    particles: {
                        number: { value: 100, density: { enable: true, value_area: 800 } },
                        color: { value: "#00ff00" },
                        shape: {
                            type: "char",
                            character: {
                                value: ["0", "1", "ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ"],
                                font: "Orbitron",
                                style: "",
                                weight: "400"
                            }
                        },
                        opacity: {
                            value: 0.8,
                            random: true,
                            anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false }
                        },
                        size: {
                            value: 16,
                            random: true,
                            anim: { enable: false, speed: 40, size_min: 0.1, sync: false }
                        },
                        line_linked: { enable: false },
                        move: {
                            enable: true,
                            speed: 3,
                            direction: "bottom",
                            random: false,
                            straight: true,
                            out_mode: "out",
                            bounce: false
                        }
                    },
                    interactivity: {
                        detect_on: "canvas",
                        events: {
                            onhover: { enable: false },
                            onclick: { enable: false },
                            resize: true
                        }
                    },
                    retina_detect: true
                });
            }

            function setupEventListeners() {
                // Matrix mode toggle
                const matrixToggle = document.getElementById('matrix-toggle');
                if (matrixToggle) {
                    matrixToggle.addEventListener('click', toggleMatrixMode);
                }

                // Clear chat button
                const clearBtn = document.getElementById('clear-chat');
                if (clearBtn) {
                    clearBtn.addEventListener('click', clearAllMessages);
                }

                // Auto-scroll on new messages
                const messageContainer = document.getElementById('message-container');
                if (messageContainer) {
                    const observer = new MutationObserver(() => {
                        if (matrixChatSystem.settings.autoScroll) {
                            scrollToBottom();
                        }
                    });
                    observer.observe(messageContainer, { childList: true });
                }
            }

            function renderAllMessages() {
                const container = document.getElementById('message-container');
                if (!container) return;

                // Clear existing messages
                container.innerHTML = '';

                // Render each message with staggered animation
                matrixChatSystem.messages.forEach((message, index) => {
                    setTimeout(() => {
                        renderMessage(message, index);
                    }, index * 100); // Stagger by 100ms
                });

                updateMessageCount();
            }

            function renderMessage(messageData, index = 0) {
                const container = document.getElementById('message-container');
                if (!container) return;

                // Create message element
                const messageEl = createMessageElement(messageData);
                container.appendChild(messageEl);

                // Apply Matrix effects
                applyMatrixEffects(messageEl, messageData);

                // Animate message appearance
                animateMessageAppearance(messageEl, index);

                // Play audio for message
                playMessageAudio(messageData.message_type, messageData.emotion, messageData.priority);

                // Create floating bubble if high priority
                if (messageData.priority > 7) {
                    createFloatingBubble(messageData);
                }

                // Update performance metrics
                matrixChatSystem.performanceMetrics.messageCount++;
                updatePerformanceDisplay();
            }

            function createMessageElement(messageData) {
                const messageEl = document.createElement('div');
                messageEl.className = `chat-message message-${getMessageAlignment(messageData)} message-${messageData.message_type} emotion-${messageData.emotion}`;
                messageEl.setAttribute('data-message-id', messageData.id);

                // Message header
                const headerEl = document.createElement('div');
                headerEl.className = 'message-header';
                headerEl.innerHTML = `
                    <span class="message-sender-name">${messageData.sender} → ${messageData.receiver}</span>
                    <span class="message-timestamp">${formatTimestamp(messageData.timestamp)}</span>
                `;

                // Message content
                const contentEl = document.createElement('div');
                contentEl.className = 'message-content';
                contentEl.textContent = messageData.content;

                // Effects container
                const effectsEl = document.createElement('div');
                effectsEl.className = 'message-effects';

                messageEl.appendChild(headerEl);
                messageEl.appendChild(contentEl);
                messageEl.appendChild(effectsEl);

                return messageEl;
            }

            function getMessageAlignment(messageData) {
                if (messageData.message_type === 'broadcast' || messageData.message_type === 'shout') {
                    return 'broadcast';
                }
                return Math.random() > 0.5 ? 'sender' : 'receiver';
            }

            function applyMatrixEffects(messageEl, messageData) {
                const effects = messageData.effects || [];
                const effectsContainer = messageEl.querySelector('.message-effects');

                effects.forEach(effect => {
                    switch (effect) {
                        case 'matrix':
                            applyMatrixTextEffect(messageEl);
                            break;
                        case 'glow':
                            applyGlowEffect(messageEl);
                            break;
                        case 'shake':
                            applyShakeEffect(messageEl);
                            break;
                        case 'typewriter':
                            applyTypewriterEffect(messageEl);
                            break;
                        case 'fade':
                            applyFadeEffect(messageEl);
                            break;
                    }
                });

                matrixChatSystem.activeEffects.add(messageData.id);
                matrixChatSystem.performanceMetrics.effectCount = matrixChatSystem.activeEffects.size;
            }

            function applyMatrixTextEffect(messageEl) {
                const contentEl = messageEl.querySelector('.message-content');
                const originalText = contentEl.textContent;
                const matrixChars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';

                // Create matrix reveal effect
                let revealIndex = 0;
                const revealInterval = setInterval(() => {
                    let displayText = '';

                    for (let i = 0; i < originalText.length; i++) {
                        if (i < revealIndex) {
                            displayText += originalText[i];
                        } else if (i === revealIndex) {
                            displayText += originalText[i];
                        } else {
                            displayText += matrixChars[Math.floor(Math.random() * matrixChars.length)];
                        }
                    }

                    contentEl.textContent = displayText;
                    revealIndex++;

                    if (revealIndex > originalText.length) {
                        clearInterval(revealInterval);
                        contentEl.textContent = originalText;
                    }
                }, 50);
            }

            function applyGlowEffect(messageEl) {
                gsap.to(messageEl, {
                    duration: 2,
                    boxShadow: "0 0 30px rgba(0, 255, 0, 0.8)",
                    ease: "matrixGlow",
                    repeat: -1,
                    yoyo: true
                });
            }

            function applyShakeEffect(messageEl) {
                gsap.to(messageEl, {
                    duration: 0.1,
                    x: "+=5",
                    yoyo: true,
                    repeat: 10,
                    ease: "power2.inOut"
                });
            }

            function applyTypewriterEffect(messageEl) {
                const contentEl = messageEl.querySelector('.message-content');
                const originalText = contentEl.textContent;
                contentEl.textContent = '';

                gsap.to(contentEl, {
                    duration: originalText.length * 0.05,
                    text: originalText,
                    ease: "none"
                });
            }

            function applyFadeEffect(messageEl) {
                gsap.fromTo(messageEl, {
                    opacity: 0,
                    scale: 0.8
                }, {
                    opacity: 1,
                    scale: 1,
                    duration: 1,
                    ease: "power2.out"
                });
            }

            function animateMessageAppearance(messageEl, index) {
                // Initial state
                gsap.set(messageEl, {
                    opacity: 0,
                    y: 30,
                    scale: 0.9
                });

                // Animate in
                gsap.to(messageEl, {
                    opacity: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.6,
                    delay: index * 0.1,
                    ease: "messageFlow"
                });
            }

            function createFloatingBubble(messageData) {
                const floatingContainer = document.getElementById('floating-conversations');
                if (!floatingContainer) return;

                const bubble = document.createElement('div');
                bubble.className = 'floating-bubble';
                bubble.textContent = messageData.content.substring(0, 50) + (messageData.content.length > 50 ? '...' : '');

                // Random position
                const x = Math.random() * (window.innerWidth - 200);
                const y = Math.random() * (window.innerHeight - 100);

                bubble.style.left = x + 'px';
                bubble.style.top = y + 'px';

                floatingContainer.appendChild(bubble);

                // Animate bubble
                gsap.fromTo(bubble, {
                    opacity: 0,
                    scale: 0.5,
                    y: 20
                }, {
                    opacity: 1,
                    scale: 1,
                    y: 0,
                    duration: 0.8,
                    ease: "bubbleFloat"
                });

                // Remove after animation
                setTimeout(() => {
                    gsap.to(bubble, {
                        opacity: 0,
                        scale: 0.8,
                        y: -20,
                        duration: 0.5,
                        ease: "power2.in",
                        onComplete: () => bubble.remove()
                    });
                }, messageData.duration * 1000);
            }

            function startMatrixAnimationLoop() {
                let frameCount = 0;
                let lastTime = performance.now();

                function animationFrame(currentTime) {
                    frameCount++;

                    // Calculate FPS
                    if (currentTime - lastTime >= 1000) {
                        matrixChatSystem.performanceMetrics.fps = Math.round(frameCount * 1000 / (currentTime - lastTime));
                        frameCount = 0;
                        lastTime = currentTime;
                        updatePerformanceDisplay();
                    }

                    // Continue loop
                    requestAnimationFrame(animationFrame);
                }

                requestAnimationFrame(animationFrame);
            }

            function startPerformanceMonitoring() {
                setInterval(() => {
                    // Monitor memory usage if available
                    if (performance.memory) {
                        const memoryMB = Math.round(performance.memory.usedJSHeapSize / 1048576);
                        console.log(`Memory usage: ${memoryMB}MB`);
                    }

                    // Clean up old effects
                    cleanupOldEffects();
                }, 5000);
            }

            function cleanupOldEffects() {
                const messages = document.querySelectorAll('.chat-message');
                const maxMessages = 50; // Keep only last 50 messages

                if (messages.length > maxMessages) {
                    for (let i = 0; i < messages.length - maxMessages; i++) {
                        const messageId = messages[i].getAttribute('data-message-id');
                        matrixChatSystem.activeEffects.delete(messageId);
                        messages[i].remove();
                    }
                }

                matrixChatSystem.performanceMetrics.effectCount = matrixChatSystem.activeEffects.size;
            }

            function updatePerformanceDisplay() {
                const fpsEl = document.getElementById('fps-display');
                const messageCountEl = document.getElementById('message-count');
                const effectCountEl = document.getElementById('effect-count');

                if (fpsEl) fpsEl.textContent = matrixChatSystem.performanceMetrics.fps;
                if (messageCountEl) messageCountEl.textContent = matrixChatSystem.performanceMetrics.messageCount;
                if (effectCountEl) effectCountEl.textContent = matrixChatSystem.performanceMetrics.effectCount;
            }

            function updateMessageCount() {
                matrixChatSystem.performanceMetrics.messageCount = document.querySelectorAll('.chat-message').length;
            }

            function toggleMatrixMode() {
                matrixChatSystem.settings.matrixMode = !matrixChatSystem.settings.matrixMode;

                if (matrixChatSystem.settings.matrixMode) {
                    initializeMatrixRain();
                    document.getElementById('matrix-toggle').textContent = 'Matrix Mode: ON';
                } else {
                    const rainEl = document.getElementById('matrix-rain');
                    if (rainEl) rainEl.innerHTML = '';
                    document.getElementById('matrix-toggle').textContent = 'Matrix Mode: OFF';
                }
            }

            function clearAllMessages() {
                const container = document.getElementById('message-container');
                if (container) {
                    gsap.to(container.children, {
                        opacity: 0,
                        y: -20,
                        duration: 0.3,
                        stagger: 0.05,
                        ease: "power2.in",
                        onComplete: () => {
                            container.innerHTML = '';
                            matrixChatSystem.messages = [];
                            matrixChatSystem.activeEffects.clear();
                            updatePerformanceDisplay();
                        }
                    });
                }
            }

            function scrollToBottom() {
                const chatMessages = document.getElementById('chat-messages');
                if (chatMessages) {
                    gsap.to(chatMessages, {
                        scrollTop: chatMessages.scrollHeight,
                        duration: 0.5,
                        ease: "power2.out"
                    });
                }
            }

            function formatTimestamp(timestamp) {
                const date = new Date(timestamp);
                return date.toLocaleTimeString('pl-PL', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
            }

            // Initialize when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeMatrixChat);
            } else {
                initializeMatrixChat();
            }
        """
