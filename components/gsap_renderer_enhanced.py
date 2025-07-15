"""
Enhanced GSAP HTML renderer for ultra animations with advanced UI/UX features
Separated from main app for modularity with enhanced interactive capabilities
"""

import json
from typing import Dict, List, Optional, Any
from config import ui_config, GSAP_CDN_BASE, REQUIRED_GSAP_PLUGINS

class EnhancedGSAPRenderer:
    """Enhanced GSAP HTML generation with advanced animations and interactive features"""
    
    def __init__(self):
        self.animation_queue = []
        self.active_animations = {}
        self.particle_systems = {}
        self.interactive_elements = {}
        self.sound_effects = {}
        self.theme_variants = {
            'dark_fantasy': {
                'primary': '#ffd700',
                'secondary': '#8b0000',
                'background': '#2c1810',
                'accent': '#b8860b'
            },
            'blood_moon': {
                'primary': '#ff6b6b',
                'secondary': '#4a0e0e',
                'background': '#1a0a0a',
                'accent': '#cc5555'
            },
            'golden_age': {
                'primary': '#ffd700',
                'secondary': '#fff8dc',
                'background': '#8b7355',
                'accent': '#daa520'
            },
            'shadow_realm': {
                'primary': '#9370db',
                'secondary': '#2e2e2e',
                'background': '#0a0a0a',
                'accent': '#6a5acd'
            }
        }
    
    def get_enhanced_gsap_cdn_links(self) -> str:
        """Generate enhanced GSAP CDN script tags with additional plugins"""
        enhanced_plugins = REQUIRED_GSAP_PLUGINS + [
            "MotionPathPlugin.min.js",
            "Physics2DPlugin.min.js",
            "ThrowPropsPlugin.min.js",
            "Draggable.min.js",
            "InertiaPlugin.min.js"
        ]
        
        scripts = []
        for plugin in enhanced_plugins:
            scripts.append(f'<script src="{GSAP_CDN_BASE}/{plugin}"></script>')
        
        # Add additional libraries for enhanced features
        scripts.extend([
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
        ])
        
        return '\n        '.join(scripts)
    
    def get_enhanced_faction_css(self, theme_variant: str = 'dark_fantasy') -> str:
        """Generate enhanced faction-specific CSS classes with theme variants"""
        theme = self.theme_variants.get(theme_variant, self.theme_variants['dark_fantasy'])
        css_rules = []
        
        for faction, color in ui_config.faction_colors.items():
            css_rules.append(f"""
            .faction-{faction} {{ 
                background: linear-gradient(135deg, {color} 0%, {self._darken_color(color)} 100%);
                border-color: {self._lighten_color(color)};
                box-shadow: 0 0 20px {color}33;
                transition: all 0.3s ease;
            }}
            
            .faction-{faction}:hover {{
                box-shadow: 0 0 30px {color}66;
                transform: translateY(-2px) scale(1.02);
            }}""")
        
        return '\n            '.join(css_rules)
    
    def _darken_color(self, color: str) -> str:
        """Enhanced color darkening with proper hex manipulation"""
        if color.startswith('#') and len(color) == 7:
            # Convert hex to RGB, darken, convert back
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Darken by 30%
            r = max(0, int(r * 0.7))
            g = max(0, int(g * 0.7))
            b = max(0, int(b * 0.7))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def _lighten_color(self, color: str) -> str:
        """Enhanced color lightening with proper hex manipulation"""
        if color.startswith('#') and len(color) == 7:
            # Convert hex to RGB, lighten, convert back
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Lighten by 30%
            r = min(255, int(r * 1.3))
            g = min(255, int(g * 1.3))
            b = min(255, int(b * 1.3))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def get_enhanced_tavern_html(self, tavern_name: str = "Enhanced Tavern", 
                                theme_variant: str = 'dark_fantasy',
                                animation_speed: float = 1.0,
                                sound_enabled: bool = True) -> str:
        """Generate complete enhanced GSAP-powered tavern HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{tavern_name} - Enhanced Visualization</title>
            {self.get_enhanced_gsap_cdn_links()}
            <style>
                {self._get_enhanced_base_css(theme_variant)}
                {self.get_enhanced_faction_css(theme_variant)}
                {self._get_enhanced_animation_css()}
                {self._get_particle_system_css()}
                {self._get_interactive_elements_css()}
            </style>
        </head>
        <body>
            <div id="enhanced-tavern-main" class="enhanced-tavern-container" data-theme="{theme_variant}">
                {self._get_enhanced_background_elements()}
                {self._get_enhanced_tavern_header(tavern_name)}
                {self._get_enhanced_characters_section()}
                {self._get_enhanced_agents_section()}
                {self._get_enhanced_status_sections()}
                {self._get_enhanced_relationships_section()}
                {self._get_interactive_tavern_map()}
                {self._get_particle_containers()}
                {self._get_audio_controls(sound_enabled)}
            </div>
            
            <script>
                // Enhanced configuration
                const ENHANCED_CONFIG = {{
                    theme: '{theme_variant}',
                    animationSpeed: {animation_speed},
                    soundEnabled: {str(sound_enabled).lower()},
                    tavernName: '{tavern_name}'
                }};
                
                {self._get_enhanced_gsap_initialization()}
                {self._get_enhanced_animation_functions()}
                {self._get_particle_system_functions()}
                {self._get_interactive_features()}
                {self._get_sound_system()}
                {self._get_enhanced_global_functions()}
                
                // Initialize enhanced features
                document.addEventListener('DOMContentLoaded', function() {{
                    initializeEnhancedTavern();
                }});
            </script>
        </body>
        </html>
        """
    
    def _get_enhanced_base_css(self, theme_variant: str) -> str:
        """Enhanced base CSS styles for tavern with theme support"""
        theme = self.theme_variants.get(theme_variant, self.theme_variants['dark_fantasy'])
        
        return f"""
                /* Enhanced tavern container with theme support */
                .enhanced-tavern-container {{
                    background: linear-gradient(135deg, {theme['background']} 0%, {self._darken_color(theme['background'])} 50%, {theme['background']} 100%);
                    border-radius: 20px;
                    padding: 25px;
                    margin: 15px 0;
                    box-shadow: 
                        0 15px 40px rgba(0,0,0,0.6),
                        inset 0 2px 4px rgba(255,255,255,0.1);
                    position: relative;
                    overflow: hidden;
                    min-height: 800px;
                    border: 3px solid {theme['accent']};
                }}
                
                .enhanced-tavern-container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="wood-grain" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M0,50 Q25,40 50,50 T100,50" stroke="{theme['accent']}" stroke-width="0.5" fill="none" opacity="0.1"/><path d="M0,25 Q25,15 50,25 T100,25" stroke="{theme['accent']}" stroke-width="0.3" fill="none" opacity="0.08"/><path d="M0,75 Q25,65 50,75 T100,75" stroke="{theme['accent']}" stroke-width="0.3" fill="none" opacity="0.08"/></pattern></defs><rect width="100" height="100" fill="url(%23wood-grain)"/></svg>');
                    opacity: 0.4;
                    pointer-events: none;
                    animation: woodGrainShift 20s ease-in-out infinite;
                }}
                
                @keyframes woodGrainShift {{
                    0%, 100% {{ transform: translateX(0); }}
                    50% {{ transform: translateX(10px); }}
                }}
                
                /* Enhanced character icons with interactive features */
                .enhanced-character-icon {{
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    margin: 12px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    cursor: pointer;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    border: 4px solid {theme['primary']};
                    opacity: 0;
                    transform: translateX(-150px) scale(0.3) rotate(-180deg);
                    box-shadow: 
                        0 8px 25px rgba(0,0,0,0.4),
                        0 0 20px {theme['primary']}33;
                    overflow: hidden;
                    background: linear-gradient(135deg, {theme['secondary']}, {self._darken_color(theme['secondary'])});
                }}
                
                .enhanced-character-icon:hover {{
                    transform: scale(1.25) rotate(10deg);
                    box-shadow: 
                        0 12px 35px rgba(0,0,0,0.6),
                        0 0 30px {theme['primary']}66;
                    border-color: {self._lighten_color(theme['primary'])};
                }}
                
                .enhanced-character-icon::before {{
                    content: '';
                    position: absolute;
                    top: -2px;
                    left: -2px;
                    right: -2px;
                    bottom: -2px;
                    background: conic-gradient(from 0deg, {theme['primary']}, {theme['accent']}, {theme['primary']});
                    border-radius: 50%;
                    z-index: -1;
                    animation: borderRotate 3s linear infinite;
                }}
                
                @keyframes borderRotate {{
                    to {{ transform: rotate(360deg); }}
                }}
                
                .character-symbol {{
                    font-size: 32px;
                    color: {theme['primary']};
                    text-shadow: 
                        2px 2px 4px rgba(0,0,0,0.8),
                        0 0 10px {theme['primary']};
                    z-index: 2;
                    position: relative;
                    animation: symbolPulse 2s ease-in-out infinite;
                }}
                
                @keyframes symbolPulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
        """
    
    def _get_enhanced_animation_css(self) -> str:
        """Enhanced animation CSS with advanced effects"""
        return """
                /* Enhanced particle effects */
                .particle {
                    position: absolute;
                    pointer-events: none;
                    border-radius: 50%;
                    opacity: 0;
                }
                
                .spark-particle {
                    background: radial-gradient(circle, #ffd700, #ff6b35);
                    width: 4px;
                    height: 4px;
                    box-shadow: 0 0 10px #ffd700;
                }
                
                .blood-particle {
                    background: radial-gradient(circle, #8b0000, #4a0000);
                    width: 6px;
                    height: 6px;
                    box-shadow: 0 0 8px #8b0000;
                }
                
                .magic-particle {
                    background: radial-gradient(circle, #9370db, #4b0082);
                    width: 5px;
                    height: 5px;
                    box-shadow: 0 0 12px #9370db;
                }
                
                /* Enhanced floating animations */
                @keyframes enhancedFloat {
                    0%, 100% { transform: translateY(0) rotate(0deg); }
                    25% { transform: translateY(-10px) rotate(2deg); }
                    50% { transform: translateY(-5px) rotate(0deg); }
                    75% { transform: translateY(-15px) rotate(-2deg); }
                }
                
                /* Enhanced glow effects */
                @keyframes enhancedGlow {
                    0%, 100% { 
                        box-shadow: 0 0 20px rgba(255,215,0,0.3);
                        filter: brightness(1);
                    }
                    50% { 
                        box-shadow: 0 0 40px rgba(255,215,0,0.8);
                        filter: brightness(1.3);
                    }
                }
                
                /* Interactive hover states */
                .interactive-element {
                    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    cursor: pointer;
                }

                .interactive-element:hover {
                    transform: translateY(-5px) scale(1.05);
                    filter: brightness(1.2);
                }
        """

    def _get_particle_system_css(self) -> str:
        """CSS for particle system effects"""
        return """
                /* Particle system containers */
                .particle-container {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    overflow: hidden;
                }

                .combat-particles {
                    z-index: 100;
                }

                .ambient-particles {
                    z-index: 1;
                }

                /* Candle flame effects */
                .candle-flame {
                    position: absolute;
                    width: 8px;
                    height: 12px;
                    background: radial-gradient(ellipse at center, #ffa500 0%, #ff6b35 50%, #ff0000 100%);
                    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
                    animation: candleFlicker 2s ease-in-out infinite;
                }

                @keyframes candleFlicker {
                    0%, 100% { transform: scale(1) rotate(-1deg); opacity: 0.9; }
                    25% { transform: scale(1.1) rotate(1deg); opacity: 1; }
                    50% { transform: scale(0.95) rotate(-0.5deg); opacity: 0.85; }
                    75% { transform: scale(1.05) rotate(0.5deg); opacity: 0.95; }
                }

                /* Smoke effects */
                .smoke-particle {
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    background: radial-gradient(circle, rgba(200,200,200,0.3) 0%, transparent 70%);
                    border-radius: 50%;
                    animation: smokeRise 4s ease-out infinite;
                }

                @keyframes smokeRise {
                    0% {
                        transform: translateY(0) scale(0.5) rotate(0deg);
                        opacity: 0.6;
                    }
                    50% {
                        transform: translateY(-50px) scale(1) rotate(180deg);
                        opacity: 0.3;
                    }
                    100% {
                        transform: translateY(-100px) scale(1.5) rotate(360deg);
                        opacity: 0;
                    }
                }
        """

    def _get_interactive_elements_css(self) -> str:
        """CSS for interactive elements"""
        return """
                /* Interactive tavern map */
                .tavern-map {
                    position: relative;
                    width: 100%;
                    height: 300px;
                    background: linear-gradient(135deg, rgba(60,40,20,0.8), rgba(80,60,40,0.8));
                    border-radius: 15px;
                    border: 2px solid var(--primary-gold, #ffd700);
                    margin: 20px 0;
                    overflow: hidden;
                }

                .map-zone {
                    position: absolute;
                    border: 2px solid transparent;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    cursor: pointer;
                    background: rgba(255,215,0,0.1);
                }

                .map-zone:hover {
                    border-color: var(--primary-gold, #ffd700);
                    background: rgba(255,215,0,0.2);
                    transform: scale(1.05);
                    box-shadow: 0 0 20px rgba(255,215,0,0.5);
                }

                .map-zone-label {
                    position: absolute;
                    bottom: 5px;
                    left: 5px;
                    color: var(--primary-gold, #ffd700);
                    font-size: 12px;
                    font-weight: bold;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                }

                /* Character portrait panels */
                .character-portrait {
                    position: relative;
                    width: 120px;
                    height: 120px;
                    border-radius: 15px;
                    border: 3px solid var(--primary-gold, #ffd700);
                    margin: 10px;
                    cursor: pointer;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    background: linear-gradient(135deg, rgba(40,40,60,0.9), rgba(60,60,80,0.9));
                    overflow: hidden;
                }

                .character-portrait:hover {
                    transform: translateY(-10px) scale(1.1);
                    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
                    border-color: #fff;
                }

                .character-portrait::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
                    transform: translateX(-100%);
                    transition: transform 0.6s ease;
                }

                .character-portrait:hover::before {
                    transform: translateX(100%);
                }

                /* Stat panels */
                .stat-panel {
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: linear-gradient(135deg, rgba(20,20,30,0.95), rgba(40,40,50,0.95));
                    border: 2px solid var(--primary-gold, #ffd700);
                    border-radius: 0 0 15px 15px;
                    padding: 15px;
                    transform: translateY(0);
                    transition: all 0.4s ease;
                    opacity: 0;
                    visibility: hidden;
                    z-index: 1000;
                }

                .character-portrait:hover .stat-panel {
                    transform: translateY(0);
                    opacity: 1;
                    visibility: visible;
                }

                /* Audio controls */
                .audio-controls {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: rgba(40,20,10,0.9);
                    border: 2px solid var(--primary-gold, #ffd700);
                    border-radius: 10px;
                    padding: 10px;
                    z-index: 1000;
                }

                .audio-button {
                    background: linear-gradient(135deg, var(--primary-gold, #ffd700), var(--dark-gold, #b8860b));
                    border: none;
                    border-radius: 5px;
                    padding: 8px 12px;
                    margin: 2px;
                    cursor: pointer;
                    color: var(--dark-brown, #2c1810);
                    font-weight: bold;
                    transition: all 0.3s ease;
                }

                .audio-button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 4px 15px rgba(255,215,0,0.5);
                }

                /* Drag and drop zones */
                .drop-zone {
                    border: 2px dashed transparent;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                    transition: all 0.3s ease;
                }

                .drop-zone.drag-over {
                    border-color: var(--primary-gold, #ffd700);
                    background: rgba(255,215,0,0.1);
                    transform: scale(1.02);
                }

                /* Chat bubbles */
                .chat-bubble {
                    position: absolute;
                    background: rgba(40,20,10,0.9);
                    border: 2px solid var(--primary-gold, #ffd700);
                    border-radius: 20px;
                    padding: 10px 15px;
                    max-width: 200px;
                    color: white;
                    font-size: 14px;
                    z-index: 500;
                    opacity: 0;
                    transform: scale(0.5) translateY(20px);
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                }

                .chat-bubble.show {
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }

                .chat-bubble::after {
                    content: '';
                    position: absolute;
                    bottom: -10px;
                    left: 20px;
                    width: 0;
                    height: 0;
                    border-left: 10px solid transparent;
                    border-right: 10px solid transparent;
                    border-top: 10px solid var(--primary-gold, #ffd700);
                }
        """

    def _get_enhanced_background_elements(self) -> str:
        """Generate enhanced background elements with particles and ambiance"""
        return """
            <!-- Enhanced background with particle systems -->
            <div class="particle-container ambient-particles" id="ambient-particles"></div>
            <div class="particle-container combat-particles" id="combat-particles"></div>

            <!-- Ambient candles -->
            <div class="candle-flame" style="top: 20px; left: 30px;"></div>
            <div class="candle-flame" style="top: 25px; right: 40px;"></div>
            <div class="candle-flame" style="bottom: 30px; left: 50px;"></div>
            <div class="candle-flame" style="bottom: 35px; right: 60px;"></div>

            <!-- Smoke effects -->
            <div class="smoke-particle" style="top: 15px; left: 35px; animation-delay: 0s;"></div>
            <div class="smoke-particle" style="top: 20px; right: 45px; animation-delay: 1s;"></div>
            <div class="smoke-particle" style="bottom: 25px; left: 55px; animation-delay: 2s;"></div>
        """

    def _get_enhanced_tavern_header(self, tavern_name: str) -> str:
        """Generate enhanced tavern header with interactive elements"""
        return f"""
            <div class="enhanced-tavern-header" style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: var(--primary-gold, #ffd700); font-size: 2.5rem;
                           text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 0 0 20px var(--primary-gold, #ffd700);
                           margin: 0; font-family: 'Cinzel', serif; animation: enhancedGlow 3s ease-in-out infinite;">
                    🏰 {tavern_name} 🏰
                </h1>
                <p style="color: #ccc; font-size: 1.2rem; margin: 10px 0; font-style: italic;">
                    "Where legends are born and tales are told"
                </p>

                <!-- Interactive reputation meter -->
                <div style="margin: 20px auto; width: 300px;">
                    <div style="background: rgba(0,0,0,0.5); border-radius: 20px; height: 20px; overflow: hidden; border: 2px solid var(--primary-gold, #ffd700);">
                        <div id="reputation-bar" style="background: linear-gradient(90deg, #8b0000, var(--primary-gold, #ffd700));
                                                      height: 100%; width: 75%; transition: width 1s ease;
                                                      box-shadow: 0 0 10px var(--primary-gold, #ffd700);"></div>
                    </div>
                    <div style="text-align: center; color: var(--primary-gold, #ffd700); margin-top: 5px; font-weight: bold;">
                        Tavern Reputation: <span id="reputation-value">75</span>/100
                    </div>
                </div>
            </div>
        """

    def _get_enhanced_characters_section(self) -> str:
        """Generate enhanced characters section with interactive portraits"""
        characters = [
            {"name": "Karczmarz", "symbol": "🍺", "role": "Tavern Keeper", "health": 85, "mood": "Content"},
            {"name": "Skrytobójca", "symbol": "🗡️", "role": "Shadow Agent", "health": 92, "mood": "Alert"},
            {"name": "Wiedźma", "symbol": "🔮", "role": "Witch", "health": 78, "mood": "Mysterious"},
            {"name": "Zwiadowca", "symbol": "🏹", "role": "Scout", "health": 88, "mood": "Vigilant"},
            {"name": "Czempion", "symbol": "⚔️", "role": "Champion", "health": 95, "mood": "Ready"}
        ]

        characters_html = """
            <div class="enhanced-characters-section" style="margin: 30px 0;">
                <h2 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px; font-family: 'Cinzel', serif;">
                    👥 Tavern Patrons
                </h2>
                <div class="characters-grid" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
        """

        for i, char in enumerate(characters):
            characters_html += f"""
                <div class="character-portrait interactive-element" id="char-{char['name'].lower()}"
                     data-character="{char['name']}" style="animation-delay: {i * 0.2}s;">
                    <div class="character-symbol" style="font-size: 3rem; text-align: center; line-height: 120px;">
                        {char['symbol']}
                    </div>

                    <!-- Enhanced stat panel -->
                    <div class="stat-panel">
                        <h4 style="color: var(--primary-gold, #ffd700); margin: 0 0 10px 0; text-align: center;">
                            {char['name']}
                        </h4>
                        <p style="color: #ccc; margin: 5px 0; font-size: 0.9rem; text-align: center;">
                            {char['role']}
                        </p>
                        <div style="margin: 10px 0;">
                            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                                <span style="color: #aaa;">Health:</span>
                                <span style="color: var(--primary-gold, #ffd700);">{char['health']}%</span>
                            </div>
                            <div style="background: rgba(0,0,0,0.5); border-radius: 10px; height: 8px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #8b0000, #00ff00); height: 100%; width: {char['health']}%; transition: width 0.5s ease;"></div>
                            </div>
                        </div>
                        <div style="text-align: center; margin-top: 10px;">
                            <span style="color: #aaa;">Mood: </span>
                            <span style="color: var(--primary-gold, #ffd700);">{char['mood']}</span>
                        </div>
                        <div style="display: flex; gap: 5px; margin-top: 10px; justify-content: center;">
                            <button class="audio-button" onclick="interactWithCharacter('{char['name']}', 'talk')" style="font-size: 0.8rem; padding: 5px 8px;">💬 Talk</button>
                            <button class="audio-button" onclick="interactWithCharacter('{char['name']}', 'trade')" style="font-size: 0.8rem; padding: 5px 8px;">🤝 Trade</button>
                        </div>
                    </div>
                </div>
            """

        characters_html += """
                </div>
            </div>
        """

        return characters_html

    def _get_enhanced_agents_section(self) -> str:
        """Generate enhanced agents section with real-time status"""
        return """
            <div class="enhanced-agents-section" style="margin: 30px 0;">
                <h2 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px; font-family: 'Cinzel', serif;">
                    🤖 AI Agent Status
                </h2>
                <div class="agents-grid" id="agents-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <!-- Agents will be dynamically populated -->
                </div>
            </div>
        """

    def _get_enhanced_status_sections(self) -> str:
        """Generate enhanced status sections with real-time metrics"""
        return """
            <div class="enhanced-status-sections" style="margin: 30px 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">

                    <!-- Economic Status -->
                    <div class="status-card" style="background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9));
                                                   border: 2px solid var(--primary-gold, #ffd700); border-radius: 15px; padding: 20px;">
                        <h3 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 15px;">💰 Economic Status</h3>
                        <div id="economic-metrics">
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <span style="color: #ccc;">Total Wealth:</span>
                                <span id="total-wealth" style="color: var(--primary-gold, #ffd700); font-weight: bold;">0</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <span style="color: #ccc;">Market Activity:</span>
                                <span id="market-activity" style="color: var(--primary-gold, #ffd700); font-weight: bold;">Low</span>
                            </div>
                            <div style="margin: 15px 0;">
                                <div style="color: #ccc; margin-bottom: 5px;">Prosperity Level:</div>
                                <div style="background: rgba(0,0,0,0.5); border-radius: 10px; height: 12px; overflow: hidden;">
                                    <div id="prosperity-bar" style="background: linear-gradient(90deg, #8b0000, var(--primary-gold, #ffd700));
                                                                   height: 100%; width: 60%; transition: width 1s ease;"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tension Meter -->
                    <div class="status-card" style="background: linear-gradient(135deg, rgba(60,20,20,0.9), rgba(80,30,30,0.9));
                                                   border: 2px solid #ff6b6b; border-radius: 15px; padding: 20px;">
                        <h3 style="color: #ff6b6b; text-align: center; margin-bottom: 15px;">⚡ Tension Meter</h3>
                        <div style="text-align: center;">
                            <div id="tension-gauge" style="width: 120px; height: 120px; margin: 0 auto; position: relative;
                                                          border: 4px solid #ff6b6b; border-radius: 50%;
                                                          background: conic-gradient(from 0deg, #00ff00 0deg, #ffff00 120deg, #ff6b6b 240deg, #8b0000 360deg);">
                                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                           width: 80px; height: 80px; background: rgba(0,0,0,0.8); border-radius: 50%;
                                           display: flex; align-items: center; justify-content: center;">
                                    <span id="tension-value" style="color: #ff6b6b; font-size: 1.5rem; font-weight: bold;">25</span>
                                </div>
                            </div>
                            <div style="color: #ccc; margin-top: 10px;">Current Tension Level</div>
                        </div>
                    </div>

                    <!-- Event Log -->
                    <div class="status-card" style="background: linear-gradient(135deg, rgba(40,40,60,0.9), rgba(60,60,80,0.9));
                                                   border: 2px solid #9370db; border-radius: 15px; padding: 20px;">
                        <h3 style="color: #9370db; text-align: center; margin-bottom: 15px;">📜 Recent Events</h3>
                        <div id="event-log" style="max-height: 200px; overflow-y: auto;">
                            <!-- Events will be dynamically populated -->
                        </div>
                    </div>

                </div>
            </div>
        """

    def _get_enhanced_relationships_section(self) -> str:
        """Generate enhanced relationships section with interactive network"""
        return """
            <div class="enhanced-relationships-section" style="margin: 30px 0;">
                <h2 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px; font-family: 'Cinzel', serif;">
                    🕸️ Relationship Network
                </h2>
                <div id="relationship-network" style="width: 100%; height: 400px;
                                                    background: linear-gradient(135deg, rgba(20,20,30,0.9), rgba(40,40,50,0.9));
                                                    border: 2px solid var(--primary-gold, #ffd700); border-radius: 15px;
                                                    position: relative; overflow: hidden;">
                    <canvas id="network-canvas" style="width: 100%; height: 100%;"></canvas>
                    <div id="network-controls" style="position: absolute; top: 10px; right: 10px;">
                        <button class="audio-button" onclick="toggleNetworkAnimation()" style="margin: 2px;">⏯️</button>
                        <button class="audio-button" onclick="resetNetworkView()" style="margin: 2px;">🔄</button>
                    </div>
                </div>
            </div>
        """

    def _get_interactive_tavern_map(self) -> str:
        """Generate interactive tavern map with clickable zones"""
        return """
            <div class="interactive-tavern-map" style="margin: 30px 0;">
                <h2 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px; font-family: 'Cinzel', serif;">
                    🗺️ Interactive Tavern Map
                </h2>
                <div class="tavern-map" id="tavern-map">
                    <!-- Bar Area -->
                    <div class="map-zone" style="top: 20px; left: 20px; width: 120px; height: 80px;"
                         onclick="selectMapZone('bar')" data-zone="bar">
                        <div class="map-zone-label">🍺 Bar</div>
                    </div>

                    <!-- Dining Area -->
                    <div class="map-zone" style="top: 20px; right: 20px; width: 140px; height: 100px;"
                         onclick="selectMapZone('dining')" data-zone="dining">
                        <div class="map-zone-label">🍽️ Dining</div>
                    </div>

                    <!-- Fireplace -->
                    <div class="map-zone" style="bottom: 20px; left: 30px; width: 100px; height: 60px;"
                         onclick="selectMapZone('fireplace')" data-zone="fireplace">
                        <div class="map-zone-label">🔥 Fireplace</div>
                    </div>

                    <!-- Private Rooms -->
                    <div class="map-zone" style="bottom: 20px; right: 30px; width: 110px; height: 70px;"
                         onclick="selectMapZone('rooms')" data-zone="rooms">
                        <div class="map-zone-label">🚪 Rooms</div>
                    </div>

                    <!-- Central Area -->
                    <div class="map-zone" style="top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 80px; border-radius: 50%;"
                         onclick="selectMapZone('center')" data-zone="center">
                        <div class="map-zone-label">🎭 Stage</div>
                    </div>
                </div>

                <!-- Zone Information Panel -->
                <div id="zone-info" style="margin-top: 20px; padding: 15px;
                                          background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9));
                                          border: 2px solid var(--primary-gold, #ffd700); border-radius: 10px;
                                          min-height: 60px; display: none;">
                    <h4 id="zone-title" style="color: var(--primary-gold, #ffd700); margin: 0 0 10px 0;"></h4>
                    <p id="zone-description" style="color: #ccc; margin: 0;"></p>
                    <div id="zone-actions" style="margin-top: 10px;"></div>
                </div>
            </div>
        """

    def _get_particle_containers(self) -> str:
        """Generate particle system containers"""
        return """
            <!-- Particle system containers for enhanced effects -->
            <div id="particles-js" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;"></div>
            <div id="combat-effects" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50;"></div>
            <div id="magic-effects" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 60;"></div>
        """

    def _get_audio_controls(self, sound_enabled: bool) -> str:
        """Generate audio controls panel"""
        return f"""
            <div class="audio-controls" id="audio-controls">
                <div style="color: var(--primary-gold, #ffd700); font-weight: bold; margin-bottom: 8px; text-align: center;">
                    🔊 Audio Controls
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                    <button class="audio-button" onclick="toggleAmbientSound()" id="ambient-btn">
                        {'🔊' if sound_enabled else '🔇'} Ambient
                    </button>
                    <button class="audio-button" onclick="toggleSFX()" id="sfx-btn">
                        {'🔊' if sound_enabled else '🔇'} SFX
                    </button>
                    <button class="audio-button" onclick="playTavernMusic()" id="music-btn">
                        🎵 Music
                    </button>
                </div>
                <div style="margin-top: 8px;">
                    <label style="color: #ccc; font-size: 0.8rem;">Volume:</label>
                    <input type="range" id="volume-slider" min="0" max="100" value="{'70' if sound_enabled else '0'}"
                           onchange="setMasterVolume(this.value)"
                           style="width: 100%; margin-top: 3px;">
                </div>
            </div>
        """

    def _get_enhanced_gsap_initialization(self) -> str:
        """Enhanced GSAP initialization with advanced features"""
        return """
                // Enhanced GSAP initialization - pushing to 150% capability!
                gsap.registerPlugin(
                    ScrollTrigger, TextPlugin, MorphSVGPlugin, DrawSVGPlugin,
                    PixiPlugin, Flip, CustomEase, MotionPathPlugin, Physics2DPlugin,
                    Draggable, InertiaPlugin
                );

                // Enhanced custom easing functions
                CustomEase.create("enhancedTavernEase", "M0,0 C0.25,0.46 0.45,0.94 1,1");
                CustomEase.create("enhancedBrawlEase", "M0,0 C0.68,-0.55 0.265,1.55 1,1");
                CustomEase.create("enhancedMagicEase", "M0,0 C0.175,0.885 0.32,1.275 1,1");
                CustomEase.create("enhancedFloatEase", "M0,0 C0.445,0.05 0.55,0.95 1,1");

                // Enhanced performance optimization context
                let enhancedCtx = gsap.context(() => {
                    // Set enhanced global performance optimizations
                    gsap.config({
                        force3D: true,
                        nullTargetWarn: false,
                        trialWarn: false,
                        autoSleep: 60
                    });

                    // Enable enhanced GPU acceleration
                    gsap.set("*", { force3D: true, transformPerspective: 1000 });
                    gsap.ticker.fps(60);
                    gsap.ticker.lagSmoothing(500, 33);
                });

                // Enhanced global variables
                let enhancedAnimationSpeed = ENHANCED_CONFIG.animationSpeed || 1.0;
                let enhancedSoundEnabled = ENHANCED_CONFIG.soundEnabled || false;
                let enhancedTheme = ENHANCED_CONFIG.theme || 'dark_fantasy';
                let enhancedParticleSystems = {};
                let enhancedSoundSystem = null;
                let enhancedNetworkAnimation = null;
                let enhancedActiveEffects = new Set();

                // Enhanced timeline management
                let enhancedMasterTimeline = gsap.timeline({ paused: false });
                let enhancedCharacterTimelines = new Map();
                let enhancedEffectTimelines = new Map();
        """

    def _get_enhanced_animation_functions(self) -> str:
        """Enhanced animation functions with advanced effects"""
        return """
                // Enhanced Character Entrance Animation
                function enhancedAnimateCharacterEntrance(characters) {
                    const characterElements = gsap.utils.toArray('.enhanced-character-icon');

                    // Enhanced staggered entrance with particle effects
                    const entranceTl = gsap.timeline();

                    entranceTl.fromTo(characterElements,
                        {
                            opacity: 0,
                            x: -200,
                            y: 50,
                            scale: 0.3,
                            rotation: -180,
                            filter: "blur(10px)"
                        },
                        {
                            opacity: 1,
                            x: 0,
                            y: 0,
                            scale: 1,
                            rotation: 0,
                            filter: "blur(0px)",
                            duration: 1.5 / enhancedAnimationSpeed,
                            ease: "enhancedTavernEase",
                            stagger: {
                                amount: 1.2 / enhancedAnimationSpeed,
                                from: "start",
                                onComplete: function() {
                                    // Trigger entrance particle effect
                                    createEntranceParticles(this.targets()[0]);
                                }
                            }
                        }
                    );

                    // Add floating animation after entrance
                    entranceTl.to(characterElements, {
                        y: "random(-10, 10)",
                        rotation: "random(-5, 5)",
                        duration: 3,
                        ease: "enhancedFloatEase",
                        repeat: -1,
                        yoyo: true,
                        stagger: 0.2
                    });

                    return entranceTl;
                }

                // Enhanced Brawl Animation with Particle Effects
                function enhancedTriggerBrawlAnimation(participants) {
                    const brawlTl = gsap.timeline();

                    participants.forEach((participant, index) => {
                        const element = document.querySelector(`[data-character="${participant}"]`);
                        if (element) {
                            // Enhanced shake animation with particles
                            brawlTl.to(element, {
                                x: "random(-20, 20)",
                                y: "random(-15, 15)",
                                rotation: "random(-10, 10)",
                                scale: "random(0.9, 1.1)",
                                duration: 0.1,
                                ease: "enhancedBrawlEase",
                                repeat: 10,
                                yoyo: true,
                                onStart: () => createCombatParticles(element),
                                onComplete: () => createBloodSplatter(element)
                            }, index * 0.2);
                        }
                    });

                    // Enhanced screen shake effect
                    brawlTl.to("#enhanced-tavern-main", {
                        x: "random(-5, 5)",
                        y: "random(-3, 3)",
                        duration: 0.05,
                        ease: "power2.inOut",
                        repeat: 20,
                        yoyo: true
                    }, 0);

                    // Enhanced tension meter spike
                    brawlTl.to("#tension-value", {
                        textContent: "random(70, 95)",
                        duration: 0.5,
                        ease: "power2.out",
                        onUpdate: function() {
                            updateTensionGauge(this.targets()[0].textContent);
                        }
                    }, 0.5);

                    return brawlTl;
                }

                // Enhanced Rumor Spread Animation
                function enhancedAnimateRumourSpread(rumor) {
                    const characters = gsap.utils.toArray('.enhanced-character-icon');
                    const spreadTl = gsap.timeline();

                    characters.forEach((char, index) => {
                        // Create enhanced chat bubble
                        const bubble = createEnhancedChatBubble(char, rumor);

                        spreadTl.fromTo(bubble, {
                            opacity: 0,
                            scale: 0.3,
                            y: 30
                        }, {
                            opacity: 1,
                            scale: 1,
                            y: 0,
                            duration: 0.6,
                            ease: "enhancedMagicEase"
                        }, index * 0.3)
                        .to(bubble, {
                            opacity: 0,
                            scale: 0.8,
                            y: -20,
                            duration: 0.4,
                            delay: 2,
                            ease: "power2.in",
                            onComplete: () => bubble.remove()
                        }, index * 0.3 + 2.5);

                        // Enhanced character glow effect
                        spreadTl.to(char, {
                            boxShadow: "0 0 30px rgba(255,215,0,0.8)",
                            duration: 0.3,
                            ease: "power2.out",
                            yoyo: true,
                            repeat: 1
                        }, index * 0.3);
                    });

                    return spreadTl;
                }
        """

    def _get_particle_system_functions(self) -> str:
        """JavaScript functions for particle system effects"""
        return """
                // Enhanced Particle System Functions

                function createEntranceParticles(element) {
                    const rect = element.getBoundingClientRect();
                    const container = document.getElementById('combat-effects');

                    for (let i = 0; i < 15; i++) {
                        const particle = document.createElement('div');
                        particle.className = 'particle spark-particle';
                        particle.style.left = rect.left + rect.width/2 + 'px';
                        particle.style.top = rect.top + rect.height/2 + 'px';
                        container.appendChild(particle);

                        gsap.to(particle, {
                            x: "random(-100, 100)",
                            y: "random(-80, -20)",
                            opacity: 1,
                            duration: 0.3,
                            ease: "power2.out"
                        });

                        gsap.to(particle, {
                            opacity: 0,
                            scale: 0,
                            duration: 0.5,
                            delay: 0.3,
                            ease: "power2.in",
                            onComplete: () => particle.remove()
                        });
                    }

                    if (enhancedSoundEnabled) {
                        playSound('entrance');
                    }
                }

                function createCombatParticles(element) {
                    const rect = element.getBoundingClientRect();
                    const container = document.getElementById('combat-effects');

                    for (let i = 0; i < 25; i++) {
                        const particle = document.createElement('div');
                        particle.className = 'particle spark-particle';
                        particle.style.left = rect.left + Math.random() * rect.width + 'px';
                        particle.style.top = rect.top + Math.random() * rect.height + 'px';
                        container.appendChild(particle);

                        gsap.fromTo(particle, {
                            opacity: 0,
                            scale: 0
                        }, {
                            opacity: 1,
                            scale: "random(0.5, 1.5)",
                            x: "random(-50, 50)",
                            y: "random(-40, 40)",
                            rotation: "random(0, 360)",
                            duration: 0.4,
                            ease: "power2.out"
                        });

                        gsap.to(particle, {
                            opacity: 0,
                            y: "+=30",
                            duration: 0.6,
                            delay: 0.2,
                            ease: "power2.in",
                            onComplete: () => particle.remove()
                        });
                    }

                    if (enhancedSoundEnabled) {
                        playSound('combat');
                    }
                }

                function createBloodSplatter(element) {
                    const rect = element.getBoundingClientRect();
                    const container = document.getElementById('combat-effects');

                    for (let i = 0; i < 12; i++) {
                        const particle = document.createElement('div');
                        particle.className = 'particle blood-particle';
                        particle.style.left = rect.left + rect.width/2 + 'px';
                        particle.style.top = rect.top + rect.height/2 + 'px';
                        container.appendChild(particle);

                        gsap.to(particle, {
                            x: "random(-80, 80)",
                            y: "random(-60, 60)",
                            opacity: 1,
                            scale: "random(0.8, 1.2)",
                            rotation: "random(0, 360)",
                            duration: 0.5,
                            ease: "power2.out"
                        });

                        gsap.to(particle, {
                            opacity: 0,
                            y: "+=20",
                            duration: 1,
                            delay: 0.5,
                            ease: "power2.in",
                            onComplete: () => particle.remove()
                        });
                    }
                }

                function createMagicParticles(element, type = 'magic') {
                    const rect = element.getBoundingClientRect();
                    const container = document.getElementById('magic-effects');

                    for (let i = 0; i < 20; i++) {
                        const particle = document.createElement('div');
                        particle.className = 'particle magic-particle';
                        particle.style.left = rect.left + rect.width/2 + 'px';
                        particle.style.top = rect.top + rect.height/2 + 'px';
                        container.appendChild(particle);

                        const angle = (i / 20) * Math.PI * 2;
                        const radius = 60;

                        gsap.to(particle, {
                            x: Math.cos(angle) * radius,
                            y: Math.sin(angle) * radius,
                            opacity: 1,
                            scale: "random(0.5, 1)",
                            rotation: angle * 180 / Math.PI,
                            duration: 1,
                            ease: "power2.out"
                        });

                        gsap.to(particle, {
                            opacity: 0,
                            scale: 0,
                            duration: 0.5,
                            delay: 1,
                            ease: "power2.in",
                            onComplete: () => particle.remove()
                        });
                    }

                    if (enhancedSoundEnabled) {
                        playSound('magic');
                    }
                }

                function initializeAmbientParticles() {
                    if (typeof particlesJS !== 'undefined') {
                        particlesJS('particles-js', {
                            particles: {
                                number: { value: 50 },
                                color: { value: "#ffd700" },
                                shape: { type: "circle" },
                                opacity: { value: 0.3, random: true },
                                size: { value: 2, random: true },
                                move: {
                                    enable: true,
                                    speed: 1,
                                    direction: "none",
                                    random: true,
                                    straight: false,
                                    out_mode: "out",
                                    bounce: false
                                }
                            },
                            interactivity: {
                                detect_on: "canvas",
                                events: {
                                    onhover: { enable: true, mode: "repulse" },
                                    onclick: { enable: true, mode: "push" }
                                }
                            }
                        });
                    }
                }
        """

    def _get_interactive_features(self) -> str:
        """JavaScript functions for interactive features"""
        return """
                // Enhanced Interactive Features

                function interactWithCharacter(characterName, actionType) {
                    const element = document.querySelector(`[data-character="${characterName}"]`);
                    if (!element) return;

                    // Enhanced interaction animation
                    gsap.to(element, {
                        scale: 1.2,
                        rotation: 5,
                        duration: 0.2,
                        ease: "power2.out",
                        yoyo: true,
                        repeat: 1
                    });

                    // Create interaction effect
                    if (actionType === 'talk') {
                        createEnhancedChatBubble(element, `Talking with ${characterName}...`);
                        if (enhancedSoundEnabled) playSound('talk');
                    } else if (actionType === 'trade') {
                        createMagicParticles(element, 'trade');
                        if (enhancedSoundEnabled) playSound('trade');
                    }

                    // Update interaction log
                    logInteraction(characterName, actionType);
                }

                function createEnhancedChatBubble(element, message) {
                    const bubble = document.createElement('div');
                    bubble.className = 'chat-bubble';
                    bubble.textContent = message;

                    const rect = element.getBoundingClientRect();
                    bubble.style.left = rect.left + rect.width/2 - 100 + 'px';
                    bubble.style.top = rect.top - 60 + 'px';

                    document.body.appendChild(bubble);

                    // Enhanced bubble animation
                    gsap.to(bubble, {
                        className: "+=show",
                        duration: 0.3,
                        ease: "enhancedMagicEase"
                    });

                    // Auto-remove after delay
                    setTimeout(() => {
                        gsap.to(bubble, {
                            className: "-=show",
                            duration: 0.3,
                            ease: "power2.in",
                            onComplete: () => bubble.remove()
                        });
                    }, 3000);

                    return bubble;
                }

                function selectMapZone(zoneName) {
                    // Deselect all zones
                    document.querySelectorAll('.map-zone').forEach(zone => {
                        zone.style.borderColor = 'transparent';
                        zone.style.transform = 'scale(1)';
                    });

                    // Select clicked zone
                    const selectedZone = document.querySelector(`[data-zone="${zoneName}"]`);
                    if (selectedZone) {
                        selectedZone.style.borderColor = 'var(--primary-gold, #ffd700)';
                        selectedZone.style.transform = 'scale(1.05)';

                        // Enhanced selection animation
                        gsap.fromTo(selectedZone, {
                            boxShadow: "0 0 0px rgba(255,215,0,0)"
                        }, {
                            boxShadow: "0 0 30px rgba(255,215,0,0.8)",
                            duration: 0.5,
                            ease: "power2.out",
                            yoyo: true,
                            repeat: 1
                        });
                    }

                    // Show zone information
                    showZoneInfo(zoneName);

                    if (enhancedSoundEnabled) {
                        playSound('select');
                    }
                }

                function showZoneInfo(zoneName) {
                    const zoneInfo = {
                        'bar': {
                            title: '🍺 The Bar',
                            description: 'The heart of the tavern where drinks flow and stories are shared.',
                            actions: ['Order Drink', 'Listen to Gossip', 'Start Conversation']
                        },
                        'dining': {
                            title: '🍽️ Dining Area',
                            description: 'Where patrons enjoy hearty meals and discuss business.',
                            actions: ['Order Food', 'Join Table', 'Eavesdrop']
                        },
                        'fireplace': {
                            title: '🔥 Fireplace',
                            description: 'A cozy spot for intimate conversations and warmth.',
                            actions: ['Warm Up', 'Tell Story', 'Rest']
                        },
                        'rooms': {
                            title: '🚪 Private Rooms',
                            description: 'Discrete chambers for private meetings and rest.',
                            actions: ['Rent Room', 'Private Meeting', 'Rest']
                        },
                        'center': {
                            title: '🎭 Central Stage',
                            description: 'The performance area where bards entertain and announcements are made.',
                            actions: ['Perform', 'Make Announcement', 'Watch Show']
                        }
                    };

                    const info = zoneInfo[zoneName];
                    if (info) {
                        document.getElementById('zone-title').textContent = info.title;
                        document.getElementById('zone-description').textContent = info.description;

                        const actionsDiv = document.getElementById('zone-actions');
                        actionsDiv.innerHTML = '';
                        info.actions.forEach(action => {
                            const button = document.createElement('button');
                            button.className = 'audio-button';
                            button.textContent = action;
                            button.onclick = () => performZoneAction(zoneName, action);
                            button.style.margin = '2px';
                            button.style.fontSize = '0.8rem';
                            actionsDiv.appendChild(button);
                        });

                        const zoneInfoPanel = document.getElementById('zone-info');
                        zoneInfoPanel.style.display = 'block';

                        // Enhanced reveal animation
                        gsap.fromTo(zoneInfoPanel, {
                            opacity: 0,
                            y: 20
                        }, {
                            opacity: 1,
                            y: 0,
                            duration: 0.4,
                            ease: "enhancedMagicEase"
                        });
                    }
                }

                function performZoneAction(zoneName, action) {
                    console.log(`Performing ${action} in ${zoneName}`);

                    // Enhanced action feedback
                    const message = `${action} in ${zoneName}`;
                    createEnhancedChatBubble(document.getElementById('tavern-map'), message);

                    // Zone-specific effects
                    const zoneElement = document.querySelector(`[data-zone="${zoneName}"]`);
                    if (zoneElement) {
                        createMagicParticles(zoneElement, 'action');
                    }

                    if (enhancedSoundEnabled) {
                        playSound('action');
                    }

                    logInteraction(zoneName, action);
                }

                function logInteraction(target, action) {
                    const timestamp = new Date().toLocaleTimeString();
                    const logEntry = `[${timestamp}] ${action} with ${target}`;
                    console.log('Enhanced Interaction:', logEntry);

                    // Could send to Streamlit via postMessage
                    if (window.parent) {
                        window.parent.postMessage({
                            type: 'interaction',
                            data: { target, action, timestamp }
                        }, '*');
                    }
                }
        """

    def _get_sound_system(self) -> str:
        """JavaScript functions for enhanced sound system"""
        return """
                // Enhanced Sound System using Howler.js

                let enhancedSounds = {};
                let masterVolume = 0.7;
                let ambientSound = null;

                function initializeEnhancedSoundSystem() {
                    if (typeof Howl === 'undefined') {
                        console.warn('Howler.js not loaded, sound system disabled');
                        return;
                    }

                    // Initialize sound effects
                    enhancedSounds = {
                        entrance: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.3,
                            rate: 1.2
                        }),
                        combat: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.5,
                            rate: 0.8
                        }),
                        magic: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.4,
                            rate: 1.5
                        }),
                        talk: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.2,
                            rate: 1.0
                        }),
                        trade: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.3,
                            rate: 0.9
                        }),
                        select: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.2,
                            rate: 1.3
                        }),
                        action: new Howl({
                            src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                            volume: 0.25,
                            rate: 1.1
                        })
                    };

                    // Initialize ambient sound
                    ambientSound = new Howl({
                        src: ['data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'],
                        volume: 0.1,
                        loop: true,
                        rate: 0.7
                    });

                    if (enhancedSoundEnabled) {
                        ambientSound.play();
                    }
                }

                function playSound(soundName) {
                    if (!enhancedSoundEnabled || !enhancedSounds[soundName]) return;

                    const sound = enhancedSounds[soundName];
                    sound.volume(masterVolume * sound._volume);
                    sound.play();
                }

                function toggleAmbientSound() {
                    if (!ambientSound) return;

                    if (ambientSound.playing()) {
                        ambientSound.pause();
                        document.getElementById('ambient-btn').textContent = '🔇 Ambient';
                    } else {
                        ambientSound.play();
                        document.getElementById('ambient-btn').textContent = '🔊 Ambient';
                    }
                }

                function toggleSFX() {
                    enhancedSoundEnabled = !enhancedSoundEnabled;
                    document.getElementById('sfx-btn').textContent = enhancedSoundEnabled ? '🔊 SFX' : '🔇 SFX';

                    if (!enhancedSoundEnabled && ambientSound) {
                        ambientSound.pause();
                    } else if (enhancedSoundEnabled && ambientSound) {
                        ambientSound.play();
                    }
                }

                function playTavernMusic() {
                    // Placeholder for tavern music
                    console.log('Playing tavern music...');
                    if (enhancedSoundEnabled) {
                        playSound('magic'); // Temporary placeholder
                    }
                }

                function setMasterVolume(volume) {
                    masterVolume = volume / 100;

                    // Update all sound volumes
                    Object.values(enhancedSounds).forEach(sound => {
                        if (sound.playing()) {
                            sound.volume(masterVolume * sound._volume);
                        }
                    });

                    if (ambientSound) {
                        ambientSound.volume(masterVolume * 0.1);
                    }
                }
        """

    def _get_enhanced_global_functions(self) -> str:
        """Enhanced global functions for tavern management"""
        return """
                // Enhanced Global Functions

                function initializeEnhancedTavern() {
                    console.log('🏰 Initializing Enhanced Tavern Systems...');

                    // Initialize all enhanced systems
                    initializeEnhancedSoundSystem();
                    initializeAmbientParticles();
                    initializeEnhancedAnimations();
                    initializeEnhancedInteractions();
                    initializeEnhancedNetworkVisualization();

                    // Start ambient effects
                    startAmbientEffects();

                    console.log('✅ Enhanced Tavern Systems Initialized!');
                }

                function initializeEnhancedAnimations() {
                    // Enhanced character entrance animation
                    const characters = gsap.utils.toArray('.enhanced-character-icon');
                    if (characters.length > 0) {
                        enhancedAnimateCharacterEntrance(characters);
                    }

                    // Enhanced floating animations for ambient elements
                    gsap.to('.candle-flame', {
                        y: "random(-3, 3)",
                        x: "random(-2, 2)",
                        rotation: "random(-5, 5)",
                        duration: "random(2, 4)",
                        ease: "sine.inOut",
                        repeat: -1,
                        yoyo: true,
                        stagger: 0.5
                    });
                }

                function initializeEnhancedInteractions() {
                    // Enhanced drag and drop for characters
                    if (typeof Draggable !== 'undefined') {
                        Draggable.create('.enhanced-character-icon', {
                            type: 'x,y',
                            bounds: '#enhanced-tavern-main',
                            inertia: true,
                            onDrag: function() {
                                gsap.to(this.target, {
                                    scale: 1.1,
                                    rotation: 5,
                                    duration: 0.2
                                });
                            },
                            onDragEnd: function() {
                                gsap.to(this.target, {
                                    scale: 1,
                                    rotation: 0,
                                    duration: 0.3,
                                    ease: "back.out(1.7)"
                                });

                                // Check for drop zones
                                checkDropZones(this.target);
                            }
                        });
                    }

                    // Enhanced hover effects
                    document.querySelectorAll('.interactive-element').forEach(element => {
                        element.addEventListener('mouseenter', function() {
                            gsap.to(this, {
                                scale: 1.05,
                                y: -5,
                                duration: 0.3,
                                ease: "power2.out"
                            });
                        });

                        element.addEventListener('mouseleave', function() {
                            gsap.to(this, {
                                scale: 1,
                                y: 0,
                                duration: 0.3,
                                ease: "power2.out"
                            });
                        });
                    });
                }

                function initializeEnhancedNetworkVisualization() {
                    const canvas = document.getElementById('network-canvas');
                    if (!canvas) return;

                    const ctx = canvas.getContext('2d');
                    canvas.width = canvas.offsetWidth;
                    canvas.height = canvas.offsetHeight;

                    // Enhanced network visualization with animated connections
                    const nodes = [
                        { x: 100, y: 100, name: 'Karczmarz', connections: ['Wiedźma', 'Zwiadowca'] },
                        { x: 300, y: 150, name: 'Wiedźma', connections: ['Skrytobójca'] },
                        { x: 200, y: 250, name: 'Skrytobójca', connections: ['Czempion'] },
                        { x: 400, y: 200, name: 'Zwiadowca', connections: ['Czempion'] },
                        { x: 250, y: 350, name: 'Czempion', connections: [] }
                    ];

                    function drawEnhancedNetwork() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        // Draw enhanced connections
                        ctx.strokeStyle = 'rgba(255, 215, 0, 0.6)';
                        ctx.lineWidth = 2;

                        nodes.forEach(node => {
                            node.connections.forEach(connectionName => {
                                const targetNode = nodes.find(n => n.name === connectionName);
                                if (targetNode) {
                                    ctx.beginPath();
                                    ctx.moveTo(node.x, node.y);
                                    ctx.lineTo(targetNode.x, targetNode.y);
                                    ctx.stroke();
                                }
                            });
                        });

                        // Draw enhanced nodes
                        nodes.forEach(node => {
                            ctx.fillStyle = 'rgba(255, 215, 0, 0.8)';
                            ctx.beginPath();
                            ctx.arc(node.x, node.y, 15, 0, Math.PI * 2);
                            ctx.fill();

                            ctx.fillStyle = '#2c1810';
                            ctx.font = '12px Arial';
                            ctx.textAlign = 'center';
                            ctx.fillText(node.name, node.x, node.y + 25);
                        });
                    }

                    // Enhanced animation loop
                    function animateNetwork() {
                        drawEnhancedNetwork();
                        requestAnimationFrame(animateNetwork);
                    }

                    animateNetwork();
                }

                function startAmbientEffects() {
                    // Enhanced ambient particle generation
                    setInterval(() => {
                        if (Math.random() < 0.3) {
                            createAmbientSparkle();
                        }
                    }, 2000);

                    // Enhanced candle flicker variations
                    setInterval(() => {
                        document.querySelectorAll('.candle-flame').forEach(flame => {
                            gsap.to(flame, {
                                opacity: "random(0.7, 1)",
                                scale: "random(0.9, 1.1)",
                                duration: 0.5,
                                ease: "power2.inOut"
                            });
                        });
                    }, 3000);
                }

                function createAmbientSparkle() {
                    const container = document.getElementById('ambient-particles');
                    if (!container) return;

                    const sparkle = document.createElement('div');
                    sparkle.className = 'particle spark-particle';
                    sparkle.style.left = Math.random() * container.offsetWidth + 'px';
                    sparkle.style.top = Math.random() * container.offsetHeight + 'px';
                    container.appendChild(sparkle);

                    gsap.fromTo(sparkle, {
                        opacity: 0,
                        scale: 0
                    }, {
                        opacity: 1,
                        scale: 1,
                        duration: 0.5,
                        ease: "power2.out"
                    });

                    gsap.to(sparkle, {
                        opacity: 0,
                        scale: 0,
                        duration: 1,
                        delay: 1,
                        ease: "power2.in",
                        onComplete: () => sparkle.remove()
                    });
                }

                function checkDropZones(draggedElement) {
                    const dropZones = document.querySelectorAll('.drop-zone');
                    const dragRect = draggedElement.getBoundingClientRect();

                    dropZones.forEach(zone => {
                        const zoneRect = zone.getBoundingClientRect();

                        if (dragRect.left < zoneRect.right &&
                            dragRect.right > zoneRect.left &&
                            dragRect.top < zoneRect.bottom &&
                            dragRect.bottom > zoneRect.top) {

                            // Enhanced drop effect
                            gsap.to(zone, {
                                backgroundColor: 'rgba(255, 215, 0, 0.3)',
                                duration: 0.3,
                                ease: "power2.out"
                            });

                            setTimeout(() => {
                                gsap.to(zone, {
                                    backgroundColor: 'transparent',
                                    duration: 0.5,
                                    ease: "power2.out"
                                });
                            }, 1000);

                            console.log('Enhanced drop detected!');
                        }
                    });
                }

                // Enhanced utility functions
                function updateEconomyStats(data) {
                    if (data.reputation !== undefined) {
                        document.getElementById('reputation-value').textContent = Math.round(data.reputation);
                        document.getElementById('reputation-bar').style.width = data.reputation + '%';
                    }

                    if (data.totalWealth !== undefined) {
                        document.getElementById('total-wealth').textContent = Math.round(data.totalWealth);
                    }

                    if (data.marketActivity !== undefined) {
                        document.getElementById('market-activity').textContent = data.marketActivity;
                    }
                }

                function updateTensionGauge(value) {
                    const gauge = document.getElementById('tension-gauge');
                    if (gauge) {
                        const rotation = (value / 100) * 360;
                        gauge.style.background = `conic-gradient(from ${rotation}deg, #00ff00 0deg, #ffff00 120deg, #ff6b6b 240deg, #8b0000 360deg)`;
                    }
                }

                function toggleNetworkAnimation() {
                    console.log('Toggling network animation...');
                    // Implementation for network animation toggle
                }

                function resetNetworkView() {
                    console.log('Resetting network view...');
                    // Implementation for network view reset
                }

                // Enhanced error handling
                window.addEventListener('error', function(e) {
                    console.error('Enhanced Tavern Error:', e.error);
                });

                console.log('🎮 Enhanced GSAP Tavern Renderer Loaded - 150% Capability!');
        """
