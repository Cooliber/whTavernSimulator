"""
GSAP HTML renderer for ultra animations
Separated from main app for modularity
"""

import json
from typing import Dict, List, Optional
from config import ui_config, GSAP_CDN_BASE, REQUIRED_GSAP_PLUGINS

class GSAPRenderer:
    """Handles GSAP HTML generation and animation orchestration"""
    
    def __init__(self):
        self.animation_queue = []
        self.active_animations = {}
    
    def get_gsap_cdn_links(self) -> str:
        """Generate GSAP CDN script tags"""
        scripts = []
        for plugin in REQUIRED_GSAP_PLUGINS:
            scripts.append(f'<script src="{GSAP_CDN_BASE}/{plugin}"></script>')
        return '\n        '.join(scripts)
    
    def get_faction_css(self) -> str:
        """Generate faction-specific CSS classes"""
        css_rules = []
        
        for faction, color in ui_config.faction_colors.items():
            css_rules.append(f"""
            .faction-{faction} {{ 
                background: linear-gradient(135deg, {color} 0%, {self._darken_color(color)} 100%);
                border-color: {self._lighten_color(color)};
            }}""")
        
        return '\n            '.join(css_rules)
    
    def _darken_color(self, color: str) -> str:
        """Darken a hex color for gradients"""
        # Simple darkening - in production, use proper color manipulation
        if color.startswith('#'):
            return color.replace('#', '#4')  # Simplified
        return color
    
    def _lighten_color(self, color: str) -> str:
        """Lighten a hex color for borders"""
        # Simple lightening - in production, use proper color manipulation
        if color.startswith('#'):
            return color.replace('#', '#f')  # Simplified
        return color
    
    def get_tavern_html(self, tavern_name: str = "The Mysterious Tavern") -> str:
        """Generate complete GSAP-powered tavern HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            {self.get_gsap_cdn_links()}
            <style>
                {self._get_base_css()}
                {self.get_faction_css()}
                {self._get_animation_css()}
            </style>
        </head>
        <body>
            <div id="tavern-main" class="tavern-container">
                {self._get_background_elements()}
                {self._get_tavern_header(tavern_name)}
                {self._get_characters_section()}
                {self._get_agents_section()}
                {self._get_status_sections()}
                {self._get_relationships_section()}
            </div>
            
            <script>
                {self._get_gsap_initialization()}
                {self._get_animation_functions()}
                {self._get_agent_animations()}
                {self._get_global_functions()}
            </script>
        </body>
        </html>
        """
    
    def _get_base_css(self) -> str:
        """Base CSS styles for tavern"""
        return """
                .tavern-container {
                    background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #6b3e2a 100%);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                    position: relative;
                    overflow: hidden;
                    min-height: 600px;
                }
                
                .character-icon {
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    margin: 8px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    border: 4px solid #ffd700;
                    opacity: 0;
                    transform: translateX(-100px) scale(0.5);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                    overflow: hidden;
                }
                
                .character-icon:hover {
                    transform: scale(1.15) rotate(5deg);
                    box-shadow: 0 8px 25px rgba(255,215,0,0.5);
                }
                
                .character-symbol {
                    font-size: 24px;
                    color: white;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                    z-index: 2;
                    position: relative;
                }
                
                .agent-box {
                    background: linear-gradient(45deg, rgba(0,0,0,0.7), rgba(50,50,50,0.7));
                    border: 2px solid #ffd700;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    min-height: 120px;
                    position: relative;
                    overflow: hidden;
                }
                
                .agent-status {
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .agent-avatar {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    margin-right: 10px;
                    background: linear-gradient(45deg, #ffd700, #ffed4e);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                }
                
                .reasoning-trace {
                    background: rgba(0,0,0,0.3);
                    border-radius: 5px;
                    padding: 8px;
                    margin-top: 5px;
                    font-family: monospace;
                    font-size: 12px;
                    color: #ccc;
                    max-height: 60px;
                    overflow-y: auto;
                }
                
                .emotion-indicator {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    font-size: 20px;
                    animation: emotionPulse 2s ease-in-out infinite;
                }
                
                @keyframes emotionPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.2); }
                }

                /* Enhanced Agent Styles for 138% GSAP Utilization */
                .agents-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }

                .agent-box {
                    background: linear-gradient(135deg, rgba(40,40,60,0.9), rgba(60,60,80,0.9));
                    border: 2px solid rgba(255,215,0,0.3);
                    border-radius: 12px;
                    padding: 15px;
                    position: relative;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    opacity: 0;
                    transform: translateY(30px);
                    will-change: transform, box-shadow;
                }

                .agent-box:hover {
                    border-color: rgba(255,215,0,0.6);
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(255,215,0,0.2);
                }

                .agent-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                }

                .agent-name {
                    font-weight: bold;
                    color: #ffd700;
                    font-size: 16px;
                }

                .agent-status {
                    font-size: 20px;
                    animation: statusPulse 2s ease-in-out infinite;
                }

                .agent-role {
                    color: #ccc;
                    font-size: 12px;
                    margin-bottom: 10px;
                    font-style: italic;
                }

                .reasoning-trace {
                    background: rgba(0,0,0,0.4);
                    border-radius: 6px;
                    padding: 8px;
                    margin: 8px 0;
                    font-family: 'Courier New', monospace;
                    font-size: 11px;
                    color: #aaa;
                    min-height: 40px;
                    border-left: 3px solid rgba(255,215,0,0.5);
                    position: relative;
                    overflow: hidden;
                }

                .reasoning-trace::before {
                    content: '💭';
                    position: absolute;
                    top: 5px;
                    right: 5px;
                    opacity: 0.6;
                }

                .emotion-indicators {
                    display: flex;
                    gap: 8px;
                    margin-top: 10px;
                    flex-wrap: wrap;
                }

                .emotion {
                    font-size: 16px;
                    padding: 4px 6px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 12px;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }

                .emotion:hover {
                    background: rgba(255,215,0,0.2);
                    transform: scale(1.2);
                }

                @keyframes statusPulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.3); opacity: 0.7; }
                }

                @keyframes thinkingGlow {
                    0%, 100% { box-shadow: 0 0 10px rgba(255,215,0,0.3); }
                    50% { box-shadow: 0 0 25px rgba(255,215,0,0.8); }
                }

                .agent-thinking {
                    animation: thinkingGlow 1.5s ease-in-out infinite;
                }

                /* Communication Flow Styles */
                #communication-canvas {
                    background: rgba(0,0,0,0.2);
                    border-radius: 8px;
                    border: 1px solid rgba(255,215,0,0.2);
                }

                .comm-line {
                    stroke: #ffd700;
                    stroke-width: 2;
                    opacity: 0;
                    stroke-dasharray: 5,5;
                    animation: commFlow 2s ease-in-out infinite;
                }

                @keyframes commFlow {
                    0% { stroke-dashoffset: 10; opacity: 0; }
                    50% { opacity: 1; }
                    100% { stroke-dashoffset: 0; opacity: 0; }
                }
        """
    
    def _get_animation_css(self) -> str:
        """Animation-specific CSS"""
        return """
                .rumour-text {
                    color: #dda0dd;
                    font-style: italic;
                    opacity: 0;
                    transform: translateY(20px);
                    padding: 10px;
                    margin: 5px 0;
                    background: linear-gradient(45deg, rgba(221,160,221,0.2), rgba(147,112,219,0.2));
                    border-radius: 8px;
                    border: 1px solid rgba(221,160,221,0.3);
                }
                
                .tension-meter {
                    width: 100%;
                    height: 20px;
                    background: #333;
                    border-radius: 10px;
                    overflow: hidden;
                    margin: 10px 0;
                }
                
                .tension-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #00ff00 0%, #ffff00 50%, #ff0000 100%);
                    width: 0%;
                    transition: width 0.5s ease;
                }
                
                .particle {
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: #ffd700;
                    border-radius: 50%;
                    pointer-events: none;
                }
                
                .smoke-particle {
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                }

                /* Economy Dashboard Styles */
                .economy-dashboard {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 15px 0;
                }

                .economy-stat {
                    background: rgba(0,0,0,0.4);
                    border: 1px solid rgba(255,215,0,0.3);
                    border-radius: 8px;
                    padding: 12px;
                    position: relative;
                    overflow: hidden;
                }

                .stat-label {
                    display: block;
                    color: #ffd700;
                    font-size: 12px;
                    font-weight: bold;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                }

                .stat-bar {
                    position: relative;
                    height: 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    overflow: hidden;
                }

                .stat-fill {
                    height: 100%;
                    width: 0%;
                    border-radius: 10px;
                    transition: width 0.8s ease;
                    position: relative;
                }

                .reputation-fill {
                    background: linear-gradient(90deg, #ff4444 0%, #ffff44 50%, #44ff44 100%);
                }

                .wealth-fill {
                    background: linear-gradient(90deg, #ffd700 0%, #ffed4e 100%);
                }

                .activity-fill {
                    background: linear-gradient(90deg, #4444ff 0%, #44ffff 100%);
                }

                .stat-value {
                    position: absolute;
                    top: 50%;
                    right: 8px;
                    transform: translateY(-50%);
                    color: white;
                    font-size: 11px;
                    font-weight: bold;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                }

                .trade-particles-container {
                    position: relative;
                    height: 60px;
                    margin-top: 10px;
                    overflow: hidden;
                    border-radius: 8px;
                    background: rgba(0,0,0,0.2);
                }

                .trade-particle {
                    position: absolute;
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    pointer-events: none;
                }

                .trade-success {
                    background: radial-gradient(circle, #44ff44 0%, #00ff00 100%);
                    box-shadow: 0 0 8px #44ff44;
                }

                .trade-failure {
                    background: radial-gradient(circle, #ff4444 0%, #ff0000 100%);
                    box-shadow: 0 0 8px #ff4444;
                }

                .resource-flow {
                    position: absolute;
                    font-size: 10px;
                    color: #ffd700;
                    font-weight: bold;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                    pointer-events: none;
                }
        """
    
    def _get_background_elements(self) -> str:
        """Background atmospheric elements"""
        return """
                <div id="tavern-background" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0;">
                    <div class="smoke-particle" style="top: 10%; left: 20%;"></div>
                    <div class="smoke-particle" style="top: 30%; left: 70%;"></div>
                    <div class="smoke-particle" style="top: 60%; left: 40%;"></div>
                </div>
        """
    
    def _get_tavern_header(self, tavern_name: str) -> str:
        """Tavern title and header"""
        return f"""
                <h2 id="tavern-title" style="color: #ffd700; text-align: center; opacity: 0; transform: translateY(-30px);">
                    {tavern_name}
                </h2>
        """
    
    def _get_characters_section(self) -> str:
        """Characters display section"""
        return """
                <div id="characters-container" style="text-align: center; margin: 20px 0;">
                    <h3 style="color: #ddd; opacity: 0;" id="characters-title">Tavern Patrons</h3>
                    <div id="characters-list">
                        <!-- Characters will be populated by JavaScript -->
                    </div>
                </div>
        """
    
    def _get_agents_section(self) -> str:
        """AI Agents display section with enhanced GSAP support"""
        return """
                <div id="agents-container" style="margin: 20px 0;">
                    <h3 style="color: #ddd; opacity: 0;" id="agents-title">🤖 Multi-Agent AI System</h3>
                    <div id="agents-list" class="agents-grid">
                        <!-- Agent boxes with thinking animations -->
                        <div id="agent-karczmarz" class="agent-box" data-agent="Karczmarz">
                            <div class="agent-header">
                                <span class="agent-name">🍺 Karczmarz</span>
                                <span class="agent-status">💭</span>
                            </div>
                            <div class="agent-role">Tavern Keeper</div>
                            <div class="reasoning-trace">Observing tavern...</div>
                            <div class="emotion-indicators">
                                <span class="emotion alertness">⚠️</span>
                                <span class="emotion satisfaction">😊</span>
                                <span class="emotion suspicion">🤔</span>
                            </div>
                        </div>

                        <div id="agent-skrytobojca" class="agent-box" data-agent="Skrytobójca">
                            <div class="agent-header">
                                <span class="agent-name">🗡️ Skrytobójca</span>
                                <span class="agent-status">👁️</span>
                            </div>
                            <div class="agent-role">Shadow Agent</div>
                            <div class="reasoning-trace">Watching from shadows...</div>
                            <div class="emotion-indicators">
                                <span class="emotion stealth">🌙</span>
                                <span class="emotion alertness">⚡</span>
                                <span class="emotion cunning">🎭</span>
                            </div>
                        </div>

                        <div id="agent-wiedzma" class="agent-box" data-agent="Wiedźma">
                            <div class="agent-header">
                                <span class="agent-name">🔮 Wiedźma</span>
                                <span class="agent-status">✨</span>
                            </div>
                            <div class="agent-role">Mystic Oracle</div>
                            <div class="reasoning-trace">Reading ethereal currents...</div>
                            <div class="emotion-indicators">
                                <span class="emotion mystical">🌟</span>
                                <span class="emotion wisdom">📜</span>
                                <span class="emotion prophecy">🔮</span>
                            </div>
                        </div>

                        <div id="agent-zwiadowca" class="agent-box" data-agent="Zwiadowca">
                            <div class="agent-header">
                                <span class="agent-name">🏹 Zwiadowca</span>
                                <span class="agent-status">🔍</span>
                            </div>
                            <div class="agent-role">Scout</div>
                            <div class="reasoning-trace">Scanning for threats...</div>
                            <div class="emotion-indicators">
                                <span class="emotion alertness">👀</span>
                                <span class="emotion curiosity">🗺️</span>
                                <span class="emotion vigilance">🛡️</span>
                            </div>
                        </div>

                        <div id="agent-czempion" class="agent-box" data-agent="Czempion">
                            <div class="agent-header">
                                <span class="agent-name">⚔️ Czempion</span>
                                <span class="agent-status">🔥</span>
                            </div>
                            <div class="agent-role">Chaos Champion</div>
                            <div class="reasoning-trace">Seeking chaos opportunities...</div>
                            <div class="emotion-indicators">
                                <span class="emotion aggression">💀</span>
                                <span class="emotion chaos">🌪️</span>
                                <span class="emotion corruption">🖤</span>
                            </div>
                        </div>
                    </div>

                    <!-- Communication Flow Visualization -->
                    <div id="communication-canvas" style="position: relative; height: 100px; margin-top: 20px;">
                        <svg id="comm-svg" width="100%" height="100" style="position: absolute; top: 0; left: 0;">
                            <!-- Communication lines will be drawn here -->
                        </svg>
                    </div>
                </div>
        """
    
    def _get_status_sections(self) -> str:
        """Status displays (tension, events, rumors, economy)"""
        return """
                <div id="tension-container" style="margin: 20px 0;">
                    <h4 style="color: #ddd; opacity: 0;" id="tension-title">Tavern Tension</h4>
                    <div class="tension-meter">
                        <div id="tension-fill" class="tension-fill"></div>
                    </div>
                </div>

                <div id="economy-container" style="margin: 20px 0;">
                    <h4 style="color: #ddd; opacity: 0;" id="economy-title">💰 Tavern Economy</h4>
                    <div class="economy-dashboard">
                        <div class="economy-stat">
                            <span class="stat-label">Reputation</span>
                            <div class="stat-bar">
                                <div id="reputation-fill" class="stat-fill reputation-fill"></div>
                                <span id="reputation-value" class="stat-value">50</span>
                            </div>
                        </div>
                        <div class="economy-stat">
                            <span class="stat-label">Total Wealth</span>
                            <div class="stat-bar">
                                <div id="wealth-fill" class="stat-fill wealth-fill"></div>
                                <span id="wealth-value" class="stat-value">1000</span>
                            </div>
                        </div>
                        <div class="economy-stat">
                            <span class="stat-label">Market Activity</span>
                            <div class="stat-bar">
                                <div id="activity-fill" class="stat-fill activity-fill"></div>
                                <span id="activity-value" class="stat-value">0</span>
                            </div>
                        </div>
                    </div>
                    <div id="trade-particles" class="trade-particles-container"></div>
                </div>

                <div id="events-container" style="margin: 20px 0;">
                    <h4 style="color: #ddd; opacity: 0;" id="events-title">Current Events</h4>
                    <div id="events-list" style="color: #ccc;">
                        <!-- Events will be populated -->
                    </div>
                </div>

                <div id="rumours-container" style="margin: 20px 0;">
                    <h4 style="color: #ddd; opacity: 0;" id="rumours-title">Tavern Rumours</h4>
                    <div id="rumours-list">
                        <!-- Rumours will be populated -->
                    </div>
                </div>
        """
    
    def _get_relationships_section(self) -> str:
        """Relationships graph section"""
        return """
                <div id="relationships-container" style="margin: 20px 0;">
                    <h4 style="color: #ddd; opacity: 0;" id="relationships-title">Character Relationships</h4>
                    <svg id="relationships-graph" width="100%" height="300" style="background: rgba(0,0,0,0.2); border-radius: 10px;">
                        <!-- Relationship graph will be drawn here -->
                    </svg>
                </div>
        """
    
    def _get_gsap_initialization(self) -> str:
        """GSAP initialization and setup"""
        return """
                // Register GSAP plugins - pushing to 138% capability!
                gsap.registerPlugin(ScrollTrigger, TextPlugin, MorphSVGPlugin, DrawSVGPlugin, PixiPlugin, Flip, CustomEase);
                
                // Custom easing for ultra-smooth animations
                CustomEase.create("tavernEase", "M0,0 C0.25,0.46 0.45,0.94 1,1");
                CustomEase.create("brawlEase", "M0,0 C0.68,-0.55 0.265,1.55 1,1");
                
                // Performance optimization context
                let ctx = gsap.context(() => {
                    // Set global performance optimizations
                    gsap.config({
                        force3D: true,
                        nullTargetWarn: false,
                        trialWarn: false
                    });
                    
                    // Enable GPU acceleration
                    gsap.set("*", { force3D: true });
                    gsap.ticker.fps(60);
                });
                
                // Master timeline for tavern reveal with parallax and smoke effects
                const masterTimeline = gsap.timeline({
                    paused: true,
                    onComplete: () => console.log("🏰 Tavern fully revealed!")
                });

                // Build the master reveal sequence
                buildTavernRevealSequence();
        """
    
    def _get_animation_functions(self) -> str:
        """Core animation functions with tavern generation reveal"""
        return """
                // Master Tavern Generation Reveal Sequence
                function buildTavernRevealSequence() {
                    // Phase 1: Background atmosphere reveal (0-2s)
                    masterTimeline
                        .to("#tavern-background", {
                            duration: 2,
                            opacity: 1,
                            ease: "power2.out"
                        })
                        .to(".smoke-particle", {
                            duration: 3,
                            y: -50,
                            opacity: 0.7,
                            scale: 1.5,
                            ease: "power1.out",
                            stagger: 0.3,
                            repeat: -1,
                            yoyo: true
                        }, 0.5);

                    // Phase 2: Tavern title reveal with bounce (1-3s)
                    masterTimeline
                        .to("#tavern-title", {
                            duration: 1.5,
                            opacity: 1,
                            y: 0,
                            ease: "bounce.out",
                            scale: 1.1
                        }, 1)
                        .to("#tavern-title", {
                            duration: 0.5,
                            scale: 1,
                            ease: "elastic.out(1, 0.3)"
                        });

                    // Phase 3: Characters section reveal (2.5-4s)
                    masterTimeline
                        .to("#characters-title", {
                            duration: 0.8,
                            opacity: 1,
                            y: 0,
                            ease: "power2.out"
                        }, 2.5)
                        .call(initializeCharacterEntrance, [], 3);

                    // Phase 4: Agents section reveal with stagger (3.5-6s)
                    masterTimeline
                        .to("#agents-title", {
                            duration: 0.8,
                            opacity: 1,
                            y: 0,
                            ease: "power2.out"
                        }, 3.5)
                        .call(initializeAgentAnimations, [], 4);

                    // Phase 5: Status sections reveal (5-7s)
                    masterTimeline
                        .to("#tension-title, #events-title, #rumours-title, #relationships-title", {
                            duration: 0.6,
                            opacity: 1,
                            y: 0,
                            ease: "power2.out",
                            stagger: 0.2
                        }, 5);

                    // Phase 6: Final parallax effect (6-8s)
                    masterTimeline
                        .to("#tavern-main", {
                            duration: 2,
                            backgroundPosition: "50% 100%",
                            ease: "power1.inOut"
                        }, 6)
                        .call(() => {
                            createParticleSystem();
                            console.log("🎉 Tavern generation complete!");
                        }, [], 7);
                }

                // Enhanced particle system for tavern atmosphere
                function createParticleSystem() {
                    const container = document.getElementById('tavern-main');
                    if (!container) return;

                    // Create floating particles
                    for (let i = 0; i < 20; i++) {
                        const particle = document.createElement('div');
                        particle.className = 'particle';
                        particle.style.left = Math.random() * 100 + '%';
                        particle.style.top = Math.random() * 100 + '%';
                        container.appendChild(particle);

                        // Animate particle floating
                        gsap.to(particle, {
                            duration: 3 + Math.random() * 4,
                            x: (Math.random() - 0.5) * 200,
                            y: (Math.random() - 0.5) * 200,
                            opacity: 0.3 + Math.random() * 0.4,
                            scale: 0.5 + Math.random() * 1,
                            ease: "sine.inOut",
                            repeat: -1,
                            yoyo: true,
                            delay: Math.random() * 2
                        });
                    }
                }

                // Character entrance initialization
                function initializeCharacterEntrance() {
                    // This will be called when characters are populated
                    console.log("🎭 Characters entrance ready");
                }

                // Character entrance animation functions
                function animateCharacterEntrance(characterData) {
                    const charactersList = document.getElementById('characters-list');
                    if (!charactersList || !characterData) return;

                    const characterIcon = document.createElement('div');
                    characterIcon.className = `character-icon faction-${characterData.faction}`;
                    characterIcon.innerHTML = `<span class="character-symbol">${characterData.symbol}</span>`;

                    charactersList.appendChild(characterIcon);

                    // Entrance animation with bounce
                    gsap.fromTo(characterIcon,
                        {
                            opacity: 0,
                            x: -100,
                            scale: 0.5,
                            rotation: -180
                        },
                        {
                            opacity: 1,
                            x: 0,
                            scale: 1,
                            rotation: 0,
                            duration: 1.2,
                            ease: "bounce.out",
                            delay: Math.random() * 0.5
                        }
                    );
                }

                // Brawl animation functions
                function triggerBrawlAnimation(participants) {
                    if (!participants || participants.length < 2) return;

                    const brawlTL = gsap.timeline();

                    participants.forEach((participant, index) => {
                        const element = document.querySelector(`[data-character="${participant}"]`);
                        if (element) {
                            brawlTL.to(element, {
                                duration: 0.3,
                                x: (index % 2 === 0 ? 20 : -20),
                                rotation: (index % 2 === 0 ? 15 : -15),
                                ease: "rough({ template: none.out, strength: 2, points: 20, taper: none, randomize: true, clamp: false})"
                            }, index * 0.1)
                            .to(element, {
                                duration: 0.5,
                                x: 0,
                                rotation: 0,
                                ease: "elastic.out(1, 0.3)"
                            });
                        }
                    });
                }

                // Rumour spreading functions
                function animateRumourSpread(rumourText, sourceCharacter) {
                    const rumoursList = document.getElementById('rumours-list');
                    if (!rumoursList) return;

                    const rumourElement = document.createElement('div');
                    rumourElement.className = 'rumour-text';
                    rumourElement.textContent = rumourText;
                    rumoursList.appendChild(rumourElement);

                    // Rumour reveal animation
                    gsap.fromTo(rumourElement,
                        {
                            opacity: 0,
                            y: 20,
                            scale: 0.8
                        },
                        {
                            opacity: 1,
                            y: 0,
                            scale: 1,
                            duration: 0.8,
                            ease: "back.out(1.7)"
                        }
                    );

                    // Auto-remove after 10 seconds
                    gsap.to(rumourElement, {
                        opacity: 0,
                        y: -20,
                        duration: 0.5,
                        delay: 10,
                        onComplete: () => rumourElement.remove()
                    });
                }

                // Tension meter update
                function updateTensionMeter(tensionLevel) {
                    const tensionFill = document.getElementById('tension-fill');
                    if (!tensionFill) return;

                    gsap.to(tensionFill, {
                        width: `${Math.min(tensionLevel * 100, 100)}%`,
                        duration: 1,
                        ease: "power2.out"
                    });
                }

                // Economy visualization functions
                function updateEconomyStats(economyData) {
                    if (!economyData) return;

                    // Update reputation bar
                    const reputationFill = document.getElementById('reputation-fill');
                    const reputationValue = document.getElementById('reputation-value');
                    if (reputationFill && reputationValue) {
                        gsap.to(reputationFill, {
                            width: `${Math.min(economyData.reputation || 50, 100)}%`,
                            duration: 1.2,
                            ease: "bounce.out"
                        });
                        gsap.to(reputationValue, {
                            innerHTML: Math.round(economyData.reputation || 50),
                            duration: 1,
                            ease: "power2.out"
                        });
                    }

                    // Update wealth bar
                    const wealthFill = document.getElementById('wealth-fill');
                    const wealthValue = document.getElementById('wealth-value');
                    if (wealthFill && wealthValue) {
                        const wealthPercent = Math.min((economyData.totalWealth || 1000) / 50000 * 100, 100);
                        gsap.to(wealthFill, {
                            width: `${wealthPercent}%`,
                            duration: 1.5,
                            ease: "elastic.out(1, 0.3)"
                        });
                        gsap.to(wealthValue, {
                            innerHTML: Math.round(economyData.totalWealth || 1000),
                            duration: 1.2,
                            ease: "power2.out"
                        });
                    }

                    // Update activity bar
                    const activityFill = document.getElementById('activity-fill');
                    const activityValue = document.getElementById('activity-value');
                    if (activityFill && activityValue) {
                        const activityPercent = Math.min((economyData.marketActivity || 0) / 100 * 100, 100);
                        gsap.to(activityFill, {
                            width: `${activityPercent}%`,
                            duration: 1,
                            ease: "power2.out"
                        });
                        gsap.to(activityValue, {
                            innerHTML: economyData.marketActivity || 0,
                            duration: 0.8,
                            ease: "power2.out"
                        });
                    }
                }

                // Trade success/failure particle effects
                function animateTradeResult(success, tradeData) {
                    const container = document.getElementById('trade-particles');
                    if (!container) return;

                    // Create particle burst
                    for (let i = 0; i < (success ? 8 : 4); i++) {
                        const particle = document.createElement('div');
                        particle.className = `trade-particle ${success ? 'trade-success' : 'trade-failure'}`;

                        // Random starting position
                        particle.style.left = '50%';
                        particle.style.top = '50%';
                        container.appendChild(particle);

                        // Animate particle explosion
                        gsap.fromTo(particle, {
                            scale: 0,
                            opacity: 1
                        }, {
                            x: (Math.random() - 0.5) * 200,
                            y: (Math.random() - 0.5) * 100,
                            scale: 1 + Math.random() * 0.5,
                            opacity: 0,
                            duration: 1.5 + Math.random() * 0.5,
                            ease: "power2.out",
                            delay: Math.random() * 0.2,
                            onComplete: () => particle.remove()
                        });
                    }

                    // Show trade details
                    if (tradeData) {
                        animateResourceFlow(tradeData);
                    }
                }

                // Resource flow animation
                function animateResourceFlow(tradeData) {
                    const container = document.getElementById('trade-particles');
                    if (!container || !tradeData.resources) return;

                    Object.entries(tradeData.resources).forEach((resource, index) => {
                        const [resourceType, amount] = resource;

                        const flowElement = document.createElement('div');
                        flowElement.className = 'resource-flow';
                        flowElement.innerHTML = `${resourceType}: ${amount > 0 ? '+' : ''}${amount}`;
                        flowElement.style.left = '10px';
                        flowElement.style.top = `${10 + index * 15}px`;
                        container.appendChild(flowElement);

                        // Animate resource flow text
                        gsap.fromTo(flowElement, {
                            opacity: 0,
                            x: -20,
                            scale: 0.8
                        }, {
                            opacity: 1,
                            x: 0,
                            scale: 1,
                            duration: 0.8,
                            ease: "back.out(1.7)",
                            delay: index * 0.1
                        });

                        // Fade out after display
                        gsap.to(flowElement, {
                            opacity: 0,
                            y: -20,
                            duration: 0.5,
                            delay: 3 + index * 0.1,
                            onComplete: () => flowElement.remove()
                        });
                    });
                }

                // Relationship graph functions
                function createRelationshipsGraph(relationships) {
                    const svg = document.getElementById('relationships-graph');
                    if (!svg || !relationships) return;

                    // Clear existing content
                    svg.innerHTML = '';

                    // Create relationship visualization
                    relationships.forEach((rel, index) => {
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        line.setAttribute('x1', rel.from.x);
                        line.setAttribute('y1', rel.from.y);
                        line.setAttribute('x2', rel.to.x);
                        line.setAttribute('y2', rel.to.y);
                        line.setAttribute('stroke', rel.type === 'positive' ? '#00ff00' : '#ff0000');
                        line.setAttribute('stroke-width', Math.abs(rel.strength) * 3);
                        line.setAttribute('opacity', 0);

                        svg.appendChild(line);

                        // Animate line appearance
                        gsap.to(line, {
                            opacity: 0.7,
                            duration: 0.5,
                            delay: index * 0.1,
                            ease: "power2.out"
                        });
                    });
                }
        """
    
    def _get_agent_animations(self) -> str:
        """Enhanced Agent-specific animations with 138% GSAP utilization"""
        return """
                // Advanced Agent Animations with GSAP 3.12.5 Features

                // Initialize agent entrance animations
                function initializeAgentAnimations() {
                    const agentBoxes = gsap.utils.toArray('.agent-box');

                    // Staggered entrance with custom ease
                    gsap.fromTo(agentBoxes,
                        {
                            opacity: 0,
                            y: 50,
                            scale: 0.8,
                            rotationX: -15
                        },
                        {
                            opacity: 1,
                            y: 0,
                            scale: 1,
                            rotationX: 0,
                            duration: 1.2,
                            ease: "back.out(1.7)",
                            stagger: {
                                amount: 0.8,
                                from: "start"
                            }
                        }
                    );
                }

                // Enhanced thinking animation with TextPlugin
                function animateAgentThinking(agentId, reasoningSteps = []) {
                    const agentBox = document.getElementById(agentId);
                    const statusIcon = agentBox.querySelector('.agent-status');
                    const reasoningTrace = agentBox.querySelector('.reasoning-trace');

                    if (!agentBox) return;

                    // Create thinking timeline
                    const thinkingTL = gsap.timeline();

                    // Pulse effect with custom ease
                    thinkingTL.to(agentBox, {
                        duration: 0.6,
                        boxShadow: "0 0 30px rgba(255,215,0,0.8), inset 0 0 20px rgba(255,215,0,0.3)",
                        scale: 1.02,
                        ease: "power2.inOut"
                    })
                    .to(statusIcon, {
                        duration: 0.3,
                        rotation: 360,
                        scale: 1.3,
                        ease: "back.out(1.7)"
                    }, 0)
                    .to(agentBox, {
                        duration: 0.6,
                        boxShadow: "0 0 15px rgba(255,215,0,0.4)",
                        scale: 1,
                        ease: "power2.out"
                    })
                    .to(statusIcon, {
                        duration: 0.3,
                        rotation: 0,
                        scale: 1,
                        ease: "elastic.out(1, 0.3)"
                    }, "-=0.3");

                    // Animate reasoning steps if provided
                    if (reasoningSteps.length > 0) {
                        animateReasoningSteps(agentId, reasoningSteps);
                    }
                }

                // Advanced reasoning trace with TextPlugin stagger
                function animateReasoningSteps(agentId, steps) {
                    const reasoningTrace = document.querySelector(`#${agentId} .reasoning-trace`);
                    if (!reasoningTrace || !steps.length) return;

                    const stepTL = gsap.timeline();

                    steps.forEach((step, index) => {
                        stepTL.to(reasoningTrace, {
                            duration: 0.4,
                            text: {
                                value: step,
                                delimiter: ""
                            },
                            ease: "none"
                        })
                        .to(reasoningTrace, {
                            duration: 0.2,
                            backgroundColor: "rgba(255,215,0,0.2)",
                            ease: "power2.out"
                        }, "-=0.2")
                        .to(reasoningTrace, {
                            duration: 0.3,
                            backgroundColor: "rgba(0,0,0,0.4)",
                            ease: "power2.out"
                        })
                        .to({}, { duration: 0.8 }); // Pause between steps
                    });
                }

                // Communication flow visualization with DrawSVG
                function animateCommunicationFlow(fromAgent, toAgent, message, priority = 5) {
                    const svg = document.getElementById('comm-svg');
                    const fromBox = document.getElementById(`agent-${fromAgent.toLowerCase()}`);
                    const toBox = document.getElementById(`agent-${toAgent.toLowerCase()}`);

                    if (!fromBox || !toBox || !svg) return;

                    // Calculate positions
                    const fromRect = fromBox.getBoundingClientRect();
                    const toRect = toBox.getBoundingClientRect();
                    const svgRect = svg.getBoundingClientRect();

                    const fromX = fromRect.left + fromRect.width/2 - svgRect.left;
                    const fromY = fromRect.top + fromRect.height/2 - svgRect.top;
                    const toX = toRect.left + toRect.width/2 - svgRect.left;
                    const toY = toRect.top + toRect.height/2 - svgRect.top;

                    // Create communication line
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', fromX);
                    line.setAttribute('y1', fromY);
                    line.setAttribute('x2', toX);
                    line.setAttribute('y2', toY);
                    line.setAttribute('class', 'comm-line');
                    line.setAttribute('stroke-width', Math.min(priority, 5));

                    svg.appendChild(line);

                    // Animate line drawing
                    gsap.fromTo(line,
                        {
                            drawSVG: "0% 0%",
                            opacity: 0
                        },
                        {
                            drawSVG: "0% 100%",
                            opacity: 1,
                            duration: 1.5,
                            ease: "power2.out",
                            onComplete: () => {
                                // Fade out after animation
                                gsap.to(line, {
                                    opacity: 0,
                                    duration: 0.5,
                                    delay: 1,
                                    onComplete: () => line.remove()
                                });
                            }
                        }
                    );

                    // Pulse receiving agent
                    gsap.to(toBox, {
                        duration: 0.3,
                        scale: 1.05,
                        boxShadow: "0 0 20px rgba(0,255,255,0.6)",
                        yoyo: true,
                        repeat: 1,
                        ease: "power2.inOut"
                    });
                }

                // Emotion indicator animations with MorphSVG-like effects
                function animateEmotionChange(agentId, emotion, intensity = 1.0) {
                    const agentBox = document.getElementById(agentId);
                    const emotionElements = agentBox.querySelectorAll('.emotion');

                    emotionElements.forEach(el => {
                        if (el.classList.contains(emotion)) {
                            gsap.to(el, {
                                duration: 0.5,
                                scale: 1 + (intensity * 0.5),
                                backgroundColor: `rgba(255,215,0,${intensity * 0.3})`,
                                ease: "elastic.out(1, 0.3)",
                                yoyo: true,
                                repeat: 1
                            });
                        }
                    });
                }

                // Master coordination animation
                function animateAgentCoordination(agents, coordinationType = "threat_response") {
                    const agentBoxes = agents.map(agent =>
                        document.getElementById(`agent-${agent.toLowerCase()}`)
                    ).filter(Boolean);

                    if (!agentBoxes.length) return;

                    const coordTL = gsap.timeline();

                    // Synchronized pulse
                    coordTL.to(agentBoxes, {
                        duration: 0.8,
                        boxShadow: "0 0 25px rgba(255,100,100,0.8)",
                        scale: 1.03,
                        ease: "power2.inOut",
                        stagger: 0.1
                    })
                    .to(agentBoxes, {
                        duration: 0.8,
                        boxShadow: "0 0 15px rgba(255,215,0,0.4)",
                        scale: 1,
                        ease: "power2.out",
                        stagger: 0.05
                    });
                }

                // Enhanced Real-Time Agent Status Updates
                function animateAgentMemoryUpdate(agentId, memoryType, importance) {
                    const agentBox = document.getElementById(agentId);
                    if (!agentBox) return;

                    const memoryIndicator = agentBox.querySelector('.memory-indicator') || createMemoryIndicator(agentBox);

                    // Color based on memory importance
                    const colors = {
                        1: "#4CAF50", // Low - Green
                        2: "#FF9800", // Medium - Orange
                        3: "#F44336", // High - Red
                        4: "#9C27B0"  // Critical - Purple
                    };

                    const color = colors[importance] || "#4CAF50";

                    // Animate memory update
                    gsap.timeline()
                        .to(memoryIndicator, {
                            duration: 0.3,
                            scale: 1.5,
                            backgroundColor: color,
                            boxShadow: `0 0 20px ${color}`,
                            ease: "back.out(1.7)"
                        })
                        .to(memoryIndicator, {
                            duration: 0.5,
                            scale: 1,
                            boxShadow: `0 0 5px ${color}`,
                            ease: "elastic.out(1, 0.3)"
                        })
                        .to(memoryIndicator, {
                            duration: 2,
                            backgroundColor: "rgba(255,255,255,0.2)",
                            boxShadow: "0 0 5px rgba(255,255,255,0.2)",
                            ease: "power2.out"
                        });
                }

                function createMemoryIndicator(agentBox) {
                    const indicator = document.createElement('div');
                    indicator.className = 'memory-indicator';
                    indicator.style.cssText = `
                        position: absolute;
                        top: 5px;
                        left: 5px;
                        width: 12px;
                        height: 12px;
                        border-radius: 50%;
                        background: rgba(255,255,255,0.2);
                        border: 2px solid rgba(255,255,255,0.4);
                        z-index: 10;
                    `;
                    agentBox.appendChild(indicator);
                    return indicator;
                }

                // Enhanced Decision Animation
                function animateAgentDecision(agentId, decisionType, confidence) {
                    const agentBox = document.getElementById(agentId);
                    if (!agentBox) return;

                    const decisionOverlay = createDecisionOverlay(agentBox, decisionType);

                    // Decision animation based on confidence
                    const duration = confidence > 0.8 ? 0.5 : 1.0; // Quick for high confidence
                    const intensity = confidence * 0.5 + 0.3; // Scale intensity with confidence

                    gsap.timeline()
                        .fromTo(decisionOverlay, {
                            opacity: 0,
                            scale: 0.5,
                            rotation: -180
                        }, {
                            opacity: intensity,
                            scale: 1,
                            rotation: 0,
                            duration: duration,
                            ease: "back.out(1.7)"
                        })
                        .to(decisionOverlay, {
                            opacity: 0,
                            scale: 1.2,
                            duration: 0.8,
                            delay: 1.5,
                            ease: "power2.out",
                            onComplete: () => decisionOverlay.remove()
                        });
                }

                function createDecisionOverlay(agentBox, decisionType) {
                    const overlay = document.createElement('div');
                    overlay.className = 'decision-overlay';

                    const icons = {
                        'attack': '⚔️',
                        'defend': '🛡️',
                        'investigate': '🔍',
                        'communicate': '💬',
                        'retreat': '🏃',
                        'cast_spell': '✨',
                        'observe': '👁️'
                    };

                    overlay.innerHTML = icons[decisionType] || '❓';
                    overlay.style.cssText = `
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        font-size: 24px;
                        z-index: 20;
                        pointer-events: none;
                        text-shadow: 0 0 10px rgba(255,215,0,0.8);
                    `;

                    agentBox.appendChild(overlay);
                    return overlay;
                }

                // Alert Animation System
                function animateAgentAlert(agentId, alertType, urgency = 5) {
                    const agentBox = document.getElementById(agentId);
                    if (!agentBox) return;

                    const alertColors = {
                        'threat': '#FF4444',
                        'opportunity': '#44FF44',
                        'communication': '#4444FF',
                        'memory': '#FF44FF',
                        'decision': '#FFFF44'
                    };

                    const color = alertColors[alertType] || '#FF4444';
                    const intensity = Math.min(urgency / 10, 1);

                    // Create pulsing border effect
                    gsap.timeline({ repeat: Math.floor(urgency / 2) })
                        .to(agentBox, {
                            duration: 0.2,
                            borderColor: color,
                            borderWidth: `${2 + intensity * 3}px`,
                            boxShadow: `0 0 ${10 + intensity * 20}px ${color}`,
                            ease: "power2.out"
                        })
                        .to(agentBox, {
                            duration: 0.3,
                            borderColor: "rgba(255,215,0,0.3)",
                            borderWidth: "2px",
                            boxShadow: "0 5px 15px rgba(0,0,0,0.2)",
                            ease: "power2.out"
                        });
                }

                // Advanced Reasoning Flow Visualization
                function animateReasoningFlow(agentId, reasoningChain) {
                    const agentBox = document.getElementById(agentId);
                    const reasoningTrace = agentBox?.querySelector('.reasoning-trace');
                    if (!reasoningTrace || !reasoningChain.length) return;

                    const flowTL = gsap.timeline();

                    // Clear existing content
                    reasoningTrace.innerHTML = '';

                    reasoningChain.forEach((step, index) => {
                        const stepElement = document.createElement('div');
                        stepElement.className = 'reasoning-step';
                        stepElement.innerHTML = `
                            <span class="step-number">${index + 1}</span>
                            <span class="step-content">${step.content}</span>
                            <span class="step-confidence">${Math.round(step.confidence * 100)}%</span>
                        `;
                        stepElement.style.cssText = `
                            display: flex;
                            align-items: center;
                            margin: 2px 0;
                            padding: 2px 4px;
                            border-radius: 3px;
                            background: rgba(0,0,0,0.2);
                            font-size: 10px;
                            opacity: 0;
                            transform: translateX(-20px);
                        `;

                        reasoningTrace.appendChild(stepElement);

                        // Animate step appearance
                        flowTL.to(stepElement, {
                            duration: 0.4,
                            opacity: step.confidence,
                            x: 0,
                            ease: "back.out(1.7)"
                        }, index * 0.2);

                        // Highlight based on confidence
                        if (step.confidence > 0.8) {
                            flowTL.to(stepElement, {
                                duration: 0.2,
                                backgroundColor: "rgba(76,175,80,0.3)",
                                ease: "power2.out"
                            }, index * 0.2 + 0.4);
                        }
                    });

                    // Auto-scroll to show latest reasoning
                    flowTL.to(reasoningTrace, {
                        duration: 0.3,
                        scrollTop: reasoningTrace.scrollHeight,
                        ease: "power2.out"
                    });
                }
        """
    
    def _get_global_functions(self) -> str:
        """Enhanced global functions for Streamlit communication"""
        return """
                // Enhanced Global Functions for Multi-Agent System
                window.animateCharacterEntrance = animateCharacterEntrance;
                window.triggerBrawlAnimation = triggerBrawlAnimation;
                window.animateRumourSpread = animateRumourSpread;
                window.updateTensionMeter = updateTensionMeter;
                window.createRelationshipsGraph = createRelationshipsGraph;

                // Enhanced Agent Functions
                window.animateAgentThinking = animateAgentThinking;
                window.animateReasoningSteps = animateReasoningSteps;
                window.animateCommunicationFlow = animateCommunicationFlow;
                window.animateEmotionChange = animateEmotionChange;
                window.animateAgentCoordination = animateAgentCoordination;
                window.initializeAgentAnimations = initializeAgentAnimations;

                // Real-time Status Functions
                window.updateAgentStatus = updateAgentStatus;
                window.animateAgentMemoryUpdate = animateAgentMemoryUpdate;
                window.animateAgentDecision = animateAgentDecision;
                window.animateAgentAlert = animateAgentAlert;
                window.animateReasoningFlow = animateReasoningFlow;

                // Economy visualization functions
                window.updateEconomyStats = updateEconomyStats;
                window.animateTradeResult = animateTradeResult;
                window.animateResourceFlow = animateResourceFlow;

                // Economy event handlers
                window.onTradeSuccess = (tradeData) => {
                    animateTradeResult(true, tradeData);
                    console.log("💰 Trade successful:", tradeData);
                };

                window.onTradeFailed = (tradeData) => {
                    animateTradeResult(false, tradeData);
                    console.log("💸 Trade failed:", tradeData);
                };

                window.onReputationChange = (oldRep, newRep, change) => {
                    updateEconomyStats({reputation: newRep});
                    if (change > 0) {
                        console.log(`📈 Reputation increased: ${oldRep} → ${newRep} (+${change})`);
                    } else {
                        console.log(`📉 Reputation decreased: ${oldRep} → ${newRep} (${change})`);
                    }
                };

                // Master initialization
                window.initializeTavern = initializeTavern;

                // Enhanced tavern initialization
                function initializeTavern() {
                    // Initialize base timeline
                    if (typeof masterTimeline !== 'undefined') {
                        masterTimeline.play();
                    }

                    // Initialize agent animations
                    initializeAgentAnimations();

                    // Set up agent interaction listeners
                    setupAgentInteractions();
                }

                // Agent interaction setup
                function setupAgentInteractions() {
                    const agentBoxes = document.querySelectorAll('.agent-box');

                    agentBoxes.forEach(box => {
                        box.addEventListener('mouseenter', () => {
                            gsap.to(box, {
                                duration: 0.3,
                                y: -5,
                                boxShadow: "0 10px 25px rgba(255,215,0,0.3)",
                                ease: "power2.out"
                            });
                        });

                        box.addEventListener('mouseleave', () => {
                            gsap.to(box, {
                                duration: 0.3,
                                y: 0,
                                boxShadow: "0 5px 15px rgba(0,0,0,0.2)",
                                ease: "power2.out"
                            });
                        });

                        box.addEventListener('click', () => {
                            const agentName = box.dataset.agent;
                            if (agentName) {
                                animateAgentThinking(`agent-${agentName.toLowerCase()}`);
                            }
                        });
                    });
                }

                // Initialize on DOM ready
                document.addEventListener('DOMContentLoaded', initializeTavern);

                // Enhanced cleanup on page unload
                window.addEventListener('beforeunload', () => {
                    if (typeof ctx !== 'undefined') {
                        ctx.revert();
                    }
                    gsap.killTweensOf("*");
                });

                // Utility function for agent status updates
                window.updateAgentStatus = function(agentId, status, reasoning = "") {
                    const agentBox = document.getElementById(agentId);
                    if (!agentBox) return;

                    const statusIcon = agentBox.querySelector('.agent-status');
                    const reasoningTrace = agentBox.querySelector('.reasoning-trace');

                    if (statusIcon) {
                        gsap.to(statusIcon, {
                            duration: 0.3,
                            scale: 1.2,
                            rotation: 180,
                            ease: "back.out(1.7)",
                            onComplete: () => {
                                statusIcon.textContent = status;
                                gsap.to(statusIcon, {
                                    duration: 0.3,
                                    scale: 1,
                                    rotation: 0,
                                    ease: "elastic.out(1, 0.3)"
                                });
                            }
                        });
                    }

                    if (reasoningTrace && reasoning) {
                        gsap.to(reasoningTrace, {
                            duration: 0.3,
                            text: {
                                value: reasoning,
                                delimiter: ""
                            },
                            ease: "none"
                        });
                    }
                };
        """
