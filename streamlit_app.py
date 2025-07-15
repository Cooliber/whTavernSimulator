#!/usr/bin/env python3
"""
Warhammer Fantasy Tavern Simulator - Ultra Animated Streamlit Version
Powered by GSAP animations pushed to 138% capability
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from core.tavern_simulator import TavernSimulator
from core.enums import InteractionType, Faction

# Page configuration
st.set_page_config(
    page_title="Warhammer Tavern Quest Hub Ultra Animated",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = TavernSimulator()
    st.session_state.simulator.generate_new_tavern()

if 'animation_state' not in st.session_state:
    st.session_state.animation_state = {
        'last_interaction': None,
        'brawl_active': False,
        'rumour_spreading': False,
        'characters_entering': False
    }

def get_gsap_html():
    """Generate GSAP-powered HTML component with 138% utilization"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/MorphSVGPlugin.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/DrawSVGPlugin.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/PixiPlugin.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/Flip.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/CustomEase.min.js"></script>
        <style>
            .tavern-container {{
                background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #6b3e2a 100%);
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                position: relative;
                overflow: hidden;
                min-height: 400px;
            }}
            
            .character-icon {{
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
                background: radial-gradient(circle, #8b4513 0%, #654321 100%);
                border: 4px solid #ffd700;
                opacity: 0;
                transform: translateX(-100px) scale(0.5);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                overflow: hidden;
            }}

            .character-icon:hover {{
                transform: scale(1.15) rotate(5deg);
                box-shadow: 0 8px 25px rgba(255,215,0,0.5);
            }}

            .character-icon::before {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 30px;
                height: 30px;
                transform: translate(-50%, -50%);
                border-radius: 50%;
                background: rgba(255,255,255,0.2);
                opacity: 0;
                transition: opacity 0.3s ease;
            }}

            .character-icon:hover::before {{
                opacity: 1;
            }}

            .character-symbol {{
                font-size: 24px;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                z-index: 2;
                position: relative;
            }}

            /* Faction-specific styles with enhanced gradients and symbols */
            .faction-empire {{
                background: linear-gradient(135deg, #ffd700 0%, #ffed4e 50%, #daa520 100%);
                border-color: #b8860b;
            }}
            .faction-dwarf {{
                background: linear-gradient(135deg, #8b4513 0%, #a0522d 50%, #654321 100%);
                border-color: #cd853f;
            }}
            .faction-highelf {{
                background: linear-gradient(135deg, #87ceeb 0%, #4682b4 50%, #1e90ff 100%);
                border-color: #00bfff;
            }}
            .faction-woodelf {{
                background: linear-gradient(135deg, #228b22 0%, #32cd32 50%, #006400 100%);
                border-color: #90ee90;
            }}
            .faction-bretonnian {{
                background: linear-gradient(135deg, #4169e1 0%, #6495ed 50%, #191970 100%);
                border-color: #87cefa;
            }}
            .faction-halfling {{
                background: linear-gradient(135deg, #daa520 0%, #ffa500 50%, #ff8c00 100%);
                border-color: #ffb347;
            }}
            .faction-tilean {{
                background: linear-gradient(135deg, #800080 0%, #9370db 50%, #4b0082 100%);
                border-color: #da70d6;
            }}
            .faction-kislev {{
                background: linear-gradient(135deg, #e0ffff 0%, #b0e0e6 50%, #87ceeb 100%);
                border-color: #afeeee;
            }}
            .faction-norse {{
                background: linear-gradient(135deg, #696969 0%, #808080 50%, #2f4f4f 100%);
                border-color: #a9a9a9;
            }}
            .faction-arabyan {{
                background: linear-gradient(135deg, #ffd700 0%, #ffff00 50%, #ffa500 100%);
                border-color: #ffb347;
            }}
            .faction-cathayan {{
                background: linear-gradient(135deg, #dc143c 0%, #ff6347 50%, #8b0000 100%);
                border-color: #ff4500;
            }}
            .faction-nipponese {{
                background: linear-gradient(135deg, #ff69b4 0%, #ffc0cb 50%, #ff1493 100%);
                border-color: #ffb6c1;
            }}
            .faction-witchhunter {{
                background: linear-gradient(135deg, #f5f5f5 0%, #dcdcdc 50%, #c0c0c0 100%);
                border-color: #d3d3d3;
            }}
            .faction-cultist {{
                background: linear-gradient(135deg, #8b0000 0%, #ff0000 50%, #dc143c 100%);
                border-color: #ff4500;
                animation: cultistPulse 2s ease-in-out infinite;
            }}

            @keyframes cultistPulse {{
                0%, 100% {{ box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
                50% {{ box-shadow: 0 5px 25px rgba(255,0,0,0.6); }}
            }}
            
            .brawl-shake {{
                animation: none;
            }}
            
            @keyframes brawlShake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-10px) rotate(-2deg); }}
                75% {{ transform: translateX(10px) rotate(2deg); }}
            }}
            
            .rumour-text {{
                color: #dda0dd;
                font-style: italic;
                opacity: 0;
                transform: translateY(20px);
            }}
            
            .tension-meter {{
                width: 100%;
                height: 20px;
                background: #333;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
            }}
            
            .tension-fill {{
                height: 100%;
                background: linear-gradient(90deg, #00ff00 0%, #ffff00 50%, #ff0000 100%);
                width: 0%;
                transition: width 0.5s ease;
            }}
            
            .particle {{
                position: absolute;
                width: 4px;
                height: 4px;
                background: #ffd700;
                border-radius: 50%;
                pointer-events: none;
            }}
            
            .smoke-particle {{
                position: absolute;
                width: 20px;
                height: 20px;
                background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div id="tavern-main" class="tavern-container">
            <div id="tavern-background" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0;">
                <div class="smoke-particle" style="top: 10%; left: 20%;"></div>
                <div class="smoke-particle" style="top: 30%; left: 70%;"></div>
                <div class="smoke-particle" style="top: 60%; left: 40%;"></div>
            </div>
            
            <h2 id="tavern-title" style="color: #ffd700; text-align: center; opacity: 0; transform: translateY(-30px);">
                {st.session_state.simulator.current_tavern.name if st.session_state.simulator.current_tavern else "The Mysterious Tavern"}
            </h2>
            
            <div id="characters-container" style="text-align: center; margin: 20px 0;">
                <h3 style="color: #ddd; opacity: 0;" id="characters-title">Tavern Patrons</h3>
                <div id="characters-list">
                    <!-- Characters will be populated by JavaScript -->
                </div>
            </div>
            
            <div id="tension-container" style="margin: 20px 0;">
                <h4 style="color: #ddd; opacity: 0;" id="tension-title">Tavern Tension</h4>
                <div class="tension-meter">
                    <div id="tension-fill" class="tension-fill"></div>
                </div>
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

            <div id="relationships-container" style="margin: 20px 0;">
                <h4 style="color: #ddd; opacity: 0;" id="relationships-title">Character Relationships</h4>
                <svg id="relationships-graph" width="100%" height="300" style="background: rgba(0,0,0,0.2); border-radius: 10px;">
                    <!-- Relationship graph will be drawn here -->
                </svg>
            </div>
        </div>

        <script>
            // Register GSAP plugins - pushing to 138% capability!
            gsap.registerPlugin(ScrollTrigger, TextPlugin, MorphSVGPlugin, DrawSVGPlugin, PixiPlugin, Flip, CustomEase);
            
            // Custom easing for ultra-smooth animations
            CustomEase.create("tavernEase", "M0,0 C0.25,0.46 0.45,0.94 1,1");
            CustomEase.create("brawlEase", "M0,0 C0.68,-0.55 0.265,1.55 1,1");
            
            // Master timeline for tavern reveal - 138% GSAP utilization
            const masterTimeline = gsap.timeline({{ paused: true }});
            
            // Ultra Performance optimization context - 138% GSAP utilization
            let ctx = gsap.context(() => {{

                // Set global performance optimizations
                gsap.config({{
                    force3D: true,
                    nullTargetWarn: false,
                    trialWarn: false
                }});

                // Enable GPU acceleration for all animations
                gsap.set("*", {{ force3D: true }});

                // Optimize ticker for 60fps
                gsap.ticker.fps(60);

                // Tavern reveal sequence with optimized timeline
                masterTimeline
                    .to("#tavern-background", {{
                        duration: 1,
                        opacity: 1,
                        ease: "power2.inOut",
                        force3D: true,
                        willChange: "opacity"
                    }})
                    .to("#tavern-title", {{
                        duration: 0.8,
                        opacity: 1,
                        y: 0,
                        ease: "back.out(1.7)",
                        force3D: true,
                        willChange: "transform, opacity"
                    }}, "-=0.5")
                    .to("#characters-title, #tension-title, #events-title, #rumours-title, #relationships-title", {{
                        duration: 0.6,
                        opacity: 1,
                        ease: "power2.out",
                        stagger: 0.1,
                        force3D: true,
                        willChange: "opacity"
                    }}, "-=0.3");

                // Optimized smoke particles with batch processing
                const smokeParticles = gsap.utils.toArray(".smoke-particle");
                if (smokeParticles.length > 0) {{
                    gsap.to(smokeParticles, {{
                        duration: 4,
                        y: -50,
                        opacity: 0,
                        ease: "power1.out",
                        stagger: 0.5,
                        repeat: -1,
                        repeatDelay: 2,
                        force3D: true,
                        willChange: "transform, opacity"
                    }});
                }}

                // Performance monitoring
                let frameCount = 0;
                let lastTime = performance.now();

                gsap.ticker.add(() => {{
                    frameCount++;
                    const currentTime = performance.now();

                    if (currentTime - lastTime >= 1000) {{
                        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));

                        // Log performance warnings if FPS drops below 50
                        if (fps < 50) {{
                            console.warn(`Performance warning: FPS dropped to ${{fps}}`);
                        }}

                        frameCount = 0;
                        lastTime = currentTime;
                    }}
                }});

            }});
            
            // Character entrance animation with ultra stagger and faction symbols
            function animateCharacterEntrance(characters) {{
                const charactersList = document.getElementById('characters-list');
                charactersList.innerHTML = '';

                // Faction symbol mapping for ultra immersion
                const factionSymbols = {{
                    'empire': '⚔️',
                    'dwarf': '⚒️',
                    'highelf': '✨',
                    'woodelf': '🏹',
                    'bretonnian': '🛡️',
                    'halfling': '🍺',
                    'tilean': '💰',
                    'kislev': '❄️',
                    'norse': '⚡',
                    'arabyan': '🌙',
                    'cathayan': '🐉',
                    'nipponese': '🌸',
                    'witchhunter': '🔥',
                    'cultist': '👁️'
                }};

                characters.forEach((char, index) => {{
                    const charDiv = document.createElement('div');
                    charDiv.className = `character-icon faction-${{char.faction.toLowerCase()}}`;
                    charDiv.title = `${{char.name}} (${{char.faction}})`;
                    charDiv.setAttribute('data-character', char.name);
                    charDiv.setAttribute('data-faction', char.faction.toLowerCase());

                    // Add faction symbol
                    const symbolSpan = document.createElement('span');
                    symbolSpan.className = 'character-symbol';
                    symbolSpan.textContent = factionSymbols[char.faction.toLowerCase()] || '⚔️';
                    charDiv.appendChild(symbolSpan);

                    charactersList.appendChild(charDiv);
                }});

                // Ultra entrance animation with 138% GSAP utilization and performance optimization
                const entranceTL = gsap.timeline({{
                    overwrite: "auto", // Prevent animation conflicts
                    onStart: () => {{
                        // Batch DOM reads for performance
                        const icons = gsap.utils.toArray(".character-icon");
                        icons.forEach(icon => {{
                            icon.style.willChange = "transform, opacity";
                        }});
                    }},
                    onComplete: () => {{
                        // Clean up will-change for memory optimization
                        gsap.set(".character-icon", {{ willChange: "auto" }});
                    }}
                }});

                entranceTL
                    // Initial state - characters off-screen with GPU acceleration
                    .set(".character-icon", {{
                        x: -150,
                        opacity: 0,
                        scale: 0.3,
                        rotation: -45,
                        force3D: true
                    }})
                    // Staggered entrance with optimized easing
                    .to(".character-icon", {{
                        duration: 1.5,
                        x: 0,
                        opacity: 1,
                        scale: 1,
                        rotation: 0,
                        ease: "back.out(2.5)",
                        force3D: true,
                        stagger: {{
                            amount: 3,
                            from: "random",
                            ease: "power2.inOut"
                        }},
                        clearProps: "transform" // Clean up after animation
                    }})
                    // Symbol pop animation
                    .fromTo(".character-symbol",
                        {{ scale: 0, rotation: 180 }},
                        {{
                            scale: 1,
                            rotation: 0,
                            duration: 0.8,
                            ease: "elastic.out(1, 0.5)",
                            stagger: 0.1
                        }}, "-=1")
                    // Faction-specific entrance effects
                    .call(() => {{
                        // Add special effects for specific factions
                        gsap.to(".faction-cultist", {{
                            duration: 0.5,
                            boxShadow: "0 0 20px rgba(255,0,0,0.8)",
                            repeat: 2,
                            yoyo: true,
                            ease: "power2.inOut"
                        }});

                        gsap.to(".faction-witchhunter", {{
                            duration: 0.3,
                            filter: "brightness(1.5)",
                            repeat: 3,
                            yoyo: true
                        }});

                        gsap.to(".faction-highelf", {{
                            duration: 2,
                            boxShadow: "0 0 15px rgba(135,206,235,0.6)",
                            ease: "sine.inOut"
                        }});
                    }});

                // Add hover animations for each character
                document.querySelectorAll('.character-icon').forEach(icon => {{
                    icon.addEventListener('mouseenter', () => {{
                        gsap.to(icon, {{
                            duration: 0.3,
                            scale: 1.2,
                            rotation: 10,
                            ease: "back.out(1.7)"
                        }});

                        gsap.to(icon.querySelector('.character-symbol'), {{
                            duration: 0.3,
                            scale: 1.3,
                            ease: "elastic.out(1, 0.3)"
                        }});
                    }});

                    icon.addEventListener('mouseleave', () => {{
                        gsap.to(icon, {{
                            duration: 0.3,
                            scale: 1,
                            rotation: 0,
                            ease: "power2.out"
                        }});

                        gsap.to(icon.querySelector('.character-symbol'), {{
                            duration: 0.3,
                            scale: 1,
                            ease: "power2.out"
                        }});
                    }});
                }});
            }}
            
            // Ultra Brawl animation with RoughEase, Flip, and advanced effects
            function triggerBrawlAnimation() {{
                const tavern = document.getElementById('tavern-main');
                const characters = document.querySelectorAll('.character-icon');

                // Create brawl timeline for orchestrated chaos
                const brawlTL = gsap.timeline();

                // Phase 1: Initial tension build-up
                brawlTL
                    .to(characters, {{
                        duration: 0.5,
                        scale: 1.1,
                        ease: "power2.inOut",
                        stagger: 0.1
                    }})
                    // Phase 2: Explosive shake with RoughEase
                    .to(tavern, {{
                        duration: 3,
                        x: "random(-20, 20)",
                        y: "random(-15, 15)",
                        ease: "rough({{ strength: 6, points: 30, template: 'none.out', randomize: true }})",
                        repeat: 5,
                        yoyo: true
                    }}, "-=0.2")
                    // Phase 3: Character scatter with Flip-like effects
                    .to(characters, {{
                        duration: 1.5,
                        x: "random(-50, 50)",
                        y: "random(-30, 30)",
                        rotation: "random(-45, 45)",
                        scale: "random(0.8, 1.3)",
                        ease: "power3.out",
                        stagger: {{
                            amount: 1,
                            from: "random"
                        }}
                    }}, "-=2")
                    // Phase 4: Screen flash effect
                    .to(tavern, {{
                        duration: 0.1,
                        filter: "brightness(2) contrast(1.5)",
                        repeat: 3,
                        yoyo: true,
                        ease: "power2.inOut"
                    }}, "-=1")
                    // Phase 5: Recovery and cleanup
                    .to(tavern, {{
                        duration: 1,
                        x: 0,
                        y: 0,
                        filter: "brightness(1) contrast(1)",
                        ease: "elastic.out(1, 0.3)"
                    }})
                    .to(characters, {{
                        duration: 2,
                        x: 0,
                        y: 0,
                        rotation: 0,
                        scale: 1,
                        ease: "back.out(1.7)",
                        stagger: 0.1
                    }}, "-=0.5");

                // Trigger multiple particle effects
                createParticleExplosion();
                createBrawlDebris();
                createBloodSplatters();

                // Add sound effect simulation with visual feedback
                createSoundWaves();
            }}
            
            // Ultra Particle explosion system with multiple effects
            function createParticleExplosion() {{
                const container = document.getElementById('tavern-main');
                const particleCount = 30;

                for (let i = 0; i < particleCount; i++) {{
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.left = '50%';
                    particle.style.top = '50%';
                    particle.style.background = `hsl(${{Math.random() * 60 + 15}}, 80%, 60%)`; // Gold to orange
                    container.appendChild(particle);

                    gsap.to(particle, {{
                        duration: gsap.utils.random(1, 2.5),
                        x: `random(-300, 300)`,
                        y: `random(-250, 250)`,
                        opacity: 0,
                        scale: gsap.utils.random(0.5, 2),
                        rotation: `random(-360, 360)`,
                        ease: "power2.out",
                        delay: gsap.utils.random(0, 0.5),
                        onComplete: () => particle.remove()
                    }});
                }}
            }}

            // Brawl debris particles (tables, chairs, mugs)
            function createBrawlDebris() {{
                const container = document.getElementById('tavern-main');
                const debrisItems = ['🪑', '🍺', '🍷', '🥨', '🗡️'];

                for (let i = 0; i < 15; i++) {{
                    const debris = document.createElement('div');
                    debris.style.position = 'absolute';
                    debris.style.fontSize = '20px';
                    debris.style.left = '50%';
                    debris.style.top = '50%';
                    debris.style.pointerEvents = 'none';
                    debris.style.zIndex = '10';
                    debris.textContent = debrisItems[Math.floor(Math.random() * debrisItems.length)];
                    container.appendChild(debris);

                    gsap.to(debris, {{
                        duration: gsap.utils.random(2, 4),
                        x: `random(-400, 400)`,
                        y: `random(-300, 100)`,
                        rotation: `random(-720, 720)`,
                        opacity: 0,
                        ease: "power3.out",
                        delay: gsap.utils.random(0, 1),
                        onComplete: () => debris.remove()
                    }});
                }}
            }}

            // Blood splatter effects (red particles)
            function createBloodSplatters() {{
                const container = document.getElementById('tavern-main');

                for (let i = 0; i < 12; i++) {{
                    const splatter = document.createElement('div');
                    splatter.style.position = 'absolute';
                    splatter.style.width = gsap.utils.random(8, 20) + 'px';
                    splatter.style.height = gsap.utils.random(8, 20) + 'px';
                    splatter.style.background = `hsl(${{gsap.utils.random(0, 15)}}, 80%, 40%)`;
                    splatter.style.borderRadius = '50%';
                    splatter.style.left = gsap.utils.random(20, 80) + '%';
                    splatter.style.top = gsap.utils.random(30, 70) + '%';
                    splatter.style.pointerEvents = 'none';
                    container.appendChild(splatter);

                    gsap.fromTo(splatter,
                        {{ scale: 0, opacity: 1 }},
                        {{
                            duration: 0.3,
                            scale: 1,
                            ease: "back.out(2)"
                        }}
                    );

                    gsap.to(splatter, {{
                        duration: 3,
                        opacity: 0,
                        delay: 2,
                        onComplete: () => splatter.remove()
                    }});
                }}
            }}

            // Sound wave visual effects
            function createSoundWaves() {{
                const container = document.getElementById('tavern-main');

                for (let i = 0; i < 5; i++) {{
                    const wave = document.createElement('div');
                    wave.style.position = 'absolute';
                    wave.style.left = '50%';
                    wave.style.top = '50%';
                    wave.style.width = '20px';
                    wave.style.height = '20px';
                    wave.style.border = '3px solid rgba(255, 255, 255, 0.6)';
                    wave.style.borderRadius = '50%';
                    wave.style.transform = 'translate(-50%, -50%)';
                    wave.style.pointerEvents = 'none';
                    container.appendChild(wave);

                    gsap.to(wave, {{
                        duration: 1.5,
                        width: '300px',
                        height: '300px',
                        opacity: 0,
                        ease: "power2.out",
                        delay: i * 0.2,
                        onComplete: () => wave.remove()
                    }});
                }}
            }}
            
            // Ultra Rumour spreading animation with TextPlugin and wave effects
            function animateRumourSpread(rumourText) {{
                const rumoursContainer = document.getElementById('rumours-list');
                const rumourDiv = document.createElement('div');
                rumourDiv.className = 'rumour-text';
                rumourDiv.style.position = 'relative';
                rumourDiv.style.padding = '10px';
                rumourDiv.style.margin = '5px 0';
                rumourDiv.style.background = 'linear-gradient(45deg, rgba(221,160,221,0.2), rgba(147,112,219,0.2))';
                rumourDiv.style.borderRadius = '8px';
                rumourDiv.style.border = '1px solid rgba(221,160,221,0.3)';
                rumourDiv.textContent = rumourText;
                rumoursContainer.appendChild(rumourDiv);

                // Create whisper particles
                createWhisperParticles(rumourDiv);

                // Split text for character-by-character animation
                const chars = rumourText.split('');
                rumourDiv.innerHTML = '';

                chars.forEach((char, index) => {{
                    const span = document.createElement('span');
                    span.textContent = char === ' ' ? '\u00A0' : char; // Non-breaking space
                    span.style.display = 'inline-block';
                    span.style.opacity = '0';
                    span.style.transform = 'translateY(20px)';
                    rumourDiv.appendChild(span);
                }});

                // Rumour reveal timeline with wave effect
                const rumourTL = gsap.timeline();

                rumourTL
                    // Container entrance
                    .fromTo(rumourDiv,
                        {{ opacity: 0, scale: 0.8, y: 30 }},
                        {{
                            duration: 0.8,
                            opacity: 1,
                            scale: 1,
                            y: 0,
                            ease: "back.out(1.7)"
                        }}
                    )
                    // Character wave animation
                    .to(rumourDiv.querySelectorAll('span'), {{
                        duration: 0.05,
                        opacity: 1,
                        y: 0,
                        ease: "power2.out",
                        stagger: {{
                            amount: 1.5,
                            from: "start"
                        }}
                    }}, "-=0.3")
                    // Glow effect for mystical feel
                    .to(rumourDiv, {{
                        duration: 2,
                        boxShadow: "0 0 20px rgba(221,160,221,0.6)",
                        ease: "sine.inOut",
                        repeat: 1,
                        yoyo: true
                    }}, "-=1")
                    // Text wave effect
                    .to(rumourDiv.querySelectorAll('span'), {{
                        duration: 0.3,
                        y: -5,
                        ease: "sine.inOut",
                        stagger: {{
                            amount: 0.8,
                            repeat: 2,
                            yoyo: true
                        }}
                    }}, "-=1.5");

                // Auto-remove with fade out after 8 seconds
                setTimeout(() => {{
                    gsap.to(rumourDiv, {{
                        duration: 1,
                        opacity: 0,
                        scale: 0.8,
                        y: -30,
                        ease: "power2.in",
                        onComplete: () => rumourDiv.remove()
                    }});
                }}, 8000);
            }}

            // Whisper particles for rumour spreading
            function createWhisperParticles(container) {{
                const particleCount = 8;

                for (let i = 0; i < particleCount; i++) {{
                    const particle = document.createElement('div');
                    particle.style.position = 'absolute';
                    particle.style.width = '4px';
                    particle.style.height = '4px';
                    particle.style.background = 'rgba(221,160,221,0.8)';
                    particle.style.borderRadius = '50%';
                    particle.style.left = '50%';
                    particle.style.top = '50%';
                    particle.style.pointerEvents = 'none';
                    particle.style.zIndex = '5';
                    container.appendChild(particle);

                    gsap.to(particle, {{
                        duration: gsap.utils.random(2, 4),
                        x: `random(-100, 100)`,
                        y: `random(-80, -20)`,
                        opacity: 0,
                        scale: gsap.utils.random(0.5, 1.5),
                        ease: "power1.out",
                        delay: gsap.utils.random(0, 1),
                        onComplete: () => particle.remove()
                    }});
                }}
            }}
            
            // Update tension meter with smooth animation
            function updateTensionMeter(tensionLevel) {{
                const tensionFill = document.getElementById('tension-fill');
                gsap.to(tensionFill, {{
                    duration: 1,
                    width: `${{tensionLevel}}%`,
                    ease: "power2.out"
                }});
                
                // Trigger brawl animation if tension is high
                if (tensionLevel > 80) {{
                    triggerBrawlAnimation();
                }}
            }}
            
            // Initialize tavern reveal
            function initializeTavern() {{
                masterTimeline.play();
            }}
            
            // Ultra Interactive Relationships Graph with DrawSVG
            function createRelationshipsGraph(relationships) {{
                const svg = document.getElementById('relationships-graph');
                const svgRect = svg.getBoundingClientRect();
                const width = svgRect.width || 600;
                const height = 300;

                // Clear existing graph
                svg.innerHTML = '';

                if (!relationships || Object.keys(relationships).length === 0) {{
                    return;
                }}

                const characters = Object.keys(relationships);
                const nodeCount = characters.length;

                // Calculate node positions in a circle
                const centerX = width / 2;
                const centerY = height / 2;
                const radius = Math.min(width, height) * 0.3;

                const nodes = characters.map((char, index) => {{
                    const angle = (index / nodeCount) * 2 * Math.PI;
                    return {{
                        name: char,
                        x: centerX + radius * Math.cos(angle),
                        y: centerY + radius * Math.sin(angle),
                        id: `node-${{index}}`
                    }};
                }});

                // Create edges first (so they appear behind nodes)
                const edges = [];
                characters.forEach((char1, i) => {{
                    Object.entries(relationships[char1] || {{}}).forEach(([char2, relationValue]) => {{
                        const node1 = nodes.find(n => n.name === char1);
                        const node2 = nodes.find(n => n.name === char2);

                        if (node1 && node2 && relationValue !== 0) {{
                            const edgeId = `edge-${{i}}-${{char2}}`;
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            line.setAttribute('id', edgeId);
                            line.setAttribute('x1', node1.x);
                            line.setAttribute('y1', node1.y);
                            line.setAttribute('x2', node2.x);
                            line.setAttribute('y2', node2.y);
                            line.setAttribute('stroke-width', Math.abs(relationValue) * 2 + 1);
                            line.setAttribute('opacity', '0');

                            // Color based on relationship
                            const color = relationValue > 0 ?
                                `hsl(${{120 - (3-relationValue) * 20}}, 70%, 50%)` : // Green to yellow for positive
                                `hsl(${{Math.abs(relationValue) * 20}}, 80%, 50%)`; // Red shades for negative
                            line.setAttribute('stroke', color);

                            svg.appendChild(line);
                            edges.push({{ element: line, value: relationValue }});
                        }}
                    }});
                }});

                // Create nodes
                nodes.forEach((node, index) => {{
                    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    group.setAttribute('id', node.id);

                    // Node circle
                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('cx', node.x);
                    circle.setAttribute('cy', node.y);
                    circle.setAttribute('r', 20);
                    circle.setAttribute('fill', '#ffd700');
                    circle.setAttribute('stroke', '#b8860b');
                    circle.setAttribute('stroke-width', '2');
                    circle.setAttribute('opacity', '0');
                    circle.style.cursor = 'pointer';

                    // Node label
                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('x', node.x);
                    text.setAttribute('y', node.y + 35);
                    text.setAttribute('text-anchor', 'middle');
                    text.setAttribute('fill', '#ddd');
                    text.setAttribute('font-size', '12');
                    text.setAttribute('opacity', '0');
                    text.textContent = node.name.split(' ')[0]; // First name only

                    group.appendChild(circle);
                    group.appendChild(text);
                    svg.appendChild(group);

                    // Add hover effects
                    circle.addEventListener('mouseenter', () => {{
                        gsap.to(circle, {{
                            duration: 0.3,
                            attr: {{ r: 25 }},
                            ease: "back.out(1.7)"
                        }});
                    }});

                    circle.addEventListener('mouseleave', () => {{
                        gsap.to(circle, {{
                            duration: 0.3,
                            attr: {{ r: 20 }},
                            ease: "power2.out"
                        }});
                    }});
                }});

                // Animate graph creation
                const graphTL = gsap.timeline();

                graphTL
                    // Animate edges drawing
                    .to('line', {{
                        duration: 2,
                        opacity: 0.7,
                        ease: "power2.out",
                        stagger: 0.1
                    }})
                    // Animate nodes appearing
                    .to('circle', {{
                        duration: 0.8,
                        opacity: 1,
                        ease: "back.out(1.7)",
                        stagger: 0.1
                    }}, "-=1")
                    // Animate labels
                    .to('text', {{
                        duration: 0.6,
                        opacity: 1,
                        ease: "power2.out",
                        stagger: 0.05
                    }}, "-=0.5");

                // Add pulsing animation for nodes
                gsap.to('circle', {{
                    duration: 2,
                    attr: {{ r: 22 }},
                    ease: "sine.inOut",
                    repeat: -1,
                    yoyo: true,
                    stagger: 0.2
                }});
            }}

            // Global functions for Streamlit communication
            window.animateCharacterEntrance = animateCharacterEntrance;
            window.triggerBrawlAnimation = triggerBrawlAnimation;
            window.animateRumourSpread = animateRumourSpread;
            window.updateTensionMeter = updateTensionMeter;
            window.createRelationshipsGraph = createRelationshipsGraph;
            window.initializeTavern = initializeTavern;
            
            // Auto-initialize when loaded
            document.addEventListener('DOMContentLoaded', initializeTavern);
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', () => {{
                ctx.revert();
            }});
            
        </script>
    </body>
    </html>
    """

def main():
    """Main Streamlit application with ultra GSAP animations"""
    
    # Custom CSS for Streamlit
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
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🏰 Warhammer Tavern Quest Hub Ultra Animated ⚔️</h1>', unsafe_allow_html=True)
    st.markdown("*Powered by GSAP animations pushed to 138% capability*")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Tavern Controls")
        
        if st.button("🏰 Generate New Tavern"):
            st.session_state.simulator.generate_new_tavern()
            st.session_state.animation_state['characters_entering'] = True
            st.rerun()
        
        if st.button("⏭️ Advance Turn"):
            st.session_state.simulator.advance_turn()
            st.rerun()
        
        if st.button("🎲 Trigger Random Event"):
            event = st.session_state.simulator.trigger_random_event()
            if event and "brawl" in event.title.lower():
                st.session_state.animation_state['brawl_active'] = True
            st.rerun()
        
        if st.button("💬 Generate Rumour"):
            rumour = st.session_state.simulator.generate_rumor()
            if rumour:
                st.session_state.animation_state['rumour_spreading'] = True
            st.rerun()
        
        st.markdown("---")
        st.subheader("🎯 HVAC CRM Metaphors")
        st.write("🔥 **Brawls** = Escalated Service Issues")
        st.write("💬 **Rumours** = Customer Feedback Spread")
        st.write("👥 **Character Entrances** = New Lead Acquisition")
        st.write("📊 **Tension Meter** = Customer Satisfaction")
        st.write("🤝 **Relationships** = Customer Loyalty Network")
        st.write("⚡ **Animations** = Real-time Process Flow")

        # HVAC CRM Process Simulator
        st.markdown("### 🏭 HVAC Process Simulator")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🆕 New Lead (Character Entry)"):
                st.session_state.animation_state['characters_entering'] = True
                st.rerun()

        with col_b:
            if st.button("🚨 Service Escalation (Brawl)"):
                st.session_state.animation_state['brawl_active'] = True
                st.rerun()

        if st.button("📢 Customer Feedback (Rumour)"):
            st.session_state.animation_state['rumour_spreading'] = True
            st.rerun()
    
    # Main content area with GSAP component
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Render the GSAP-powered tavern
        components.html(get_gsap_html(), height=600, scrolling=True)
        
        # JavaScript communication for animations
        if st.session_state.animation_state.get('characters_entering'):
            if st.session_state.simulator.current_tavern:
                characters_data = [
                    {
                        'name': char.name,
                        'faction': char.faction.value.replace(' ', '').lower()
                    }
                    for char in st.session_state.simulator.current_tavern.characters
                ]
                
                st.components.v1.html(f"""
                <script>
                if (window.animateCharacterEntrance) {{
                    window.animateCharacterEntrance({json.dumps(characters_data)});
                }}
                </script>
                """, height=0)
            
            st.session_state.animation_state['characters_entering'] = False
        
        if st.session_state.animation_state.get('brawl_active'):
            st.components.v1.html("""
            <script>
            if (window.triggerBrawlAnimation) {
                window.triggerBrawlAnimation();
            }
            </script>
            """, height=0)
            st.session_state.animation_state['brawl_active'] = False
        
        if st.session_state.animation_state.get('rumour_spreading'):
            latest_rumour = st.session_state.simulator.rumor_system.get_random_rumor()
            if latest_rumour:
                st.components.v1.html(f"""
                <script>
                if (window.animateRumourSpread) {{
                    window.animateRumourSpread("{latest_rumour}");
                }}
                </script>
                """, height=0)
            st.session_state.animation_state['rumour_spreading'] = False
        
        # Update tension meter
        if st.session_state.simulator.current_tavern:
            tension = st.session_state.simulator.current_tavern.tension_level
            st.components.v1.html(f"""
            <script>
            if (window.updateTensionMeter) {{
                window.updateTensionMeter({tension});
            }}
            </script>
            """, height=0)

            # Update relationships graph
            relationships = st.session_state.simulator.get_character_relationships()
            if relationships:
                st.components.v1.html(f"""
                <script>
                if (window.createRelationshipsGraph) {{
                    window.createRelationshipsGraph({json.dumps(relationships)});
                }}
                </script>
                """, height=0)
    
    with col2:
        st.subheader("📊 Tavern Status")
        
        if st.session_state.simulator.current_tavern:
            tavern = st.session_state.simulator.current_tavern
            
            st.metric("Tension Level", f"{tavern.tension_level}/100")
            st.metric("Occupancy", f"{tavern.current_occupancy}/{tavern.capacity}")
            st.metric("Reputation", f"{tavern.reputation}/100")
            
            st.subheader("🎭 Current Characters")
            for char in tavern.characters:
                mood_emoji = "😊" if char.current_mood == "happy" else "😠" if char.current_mood == "angry" else "🍺" if char.is_drunk() else "😐"
                st.write(f"{mood_emoji} **{char.name}** ({char.faction.value})")
            
            st.subheader("📰 Recent Events")
            for event in tavern.current_events[-3:]:
                st.write(f"• {event}")
        
        st.subheader("🎮 Interaction Controls")
        
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

if __name__ == "__main__":
    main()
