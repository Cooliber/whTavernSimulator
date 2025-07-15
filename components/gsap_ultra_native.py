"""
Ultra-Native JavaScript GSAP Renderer for Warhammer Tavern Simulator
Provides comprehensive JavaScript environment with advanced GSAP features
"""

import json
from typing import Dict, List, Optional, Any
from config import ui_config, GSAP_CDN_BASE, REQUIRED_GSAP_PLUGINS

class UltraNativeGSAPRenderer:
    """Ultra-native JavaScript GSAP renderer with comprehensive client-side features"""
    
    def __init__(self):
        self.animation_queue = []
        self.active_animations = {}
        self.particle_systems = {}
        self.interactive_elements = {}
        self.sound_effects = {}
        self.physics_engine = {}
        self.data_visualizations = {}
        
    def get_ultra_native_cdn_links(self) -> str:
        """Generate comprehensive CDN links for ultra-native JavaScript environment"""
        # Core GSAP with all professional plugins
        gsap_plugins = [
            "gsap.min.js",
            "ScrollTrigger.min.js", 
            "TextPlugin.min.js",
            "MorphSVGPlugin.min.js",
            "DrawSVGPlugin.min.js",
            "PixiPlugin.min.js",
            "Flip.min.js",
            "CustomEase.min.js",
            "MotionPathPlugin.min.js",
            "Physics2DPlugin.min.js",
            "ThrowPropsPlugin.min.js",
            "Draggable.min.js",
            "InertiaPlugin.min.js",
            "SplitText.min.js",
            "ScrambleTextPlugin.min.js"
        ]
        
        scripts = []
        for plugin in gsap_plugins:
            scripts.append(f'<script src="{GSAP_CDN_BASE}/{plugin}"></script>')
        
        # Additional JavaScript libraries for ultra-native environment
        additional_libs = [
            # Audio
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>',
            
            # 3D and Graphics
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/pixi.js/7.2.4/pixi.min.js"></script>',
            
            # Physics and Math
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.18.0/matter.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>',
            
            # Utilities
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js"></script>',
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js"></script>',
            
            # Performance monitoring
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r17/Stats.min.js"></script>'
        ]
        
        scripts.extend(additional_libs)
        return '\n        '.join(scripts)
    
    def get_ultra_native_html(self, tavern_name: str = "Ultra Native Tavern") -> str:
        """Generate ultra-native JavaScript GSAP environment"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{tavern_name} - Ultra Native GSAP Environment</title>
            {self.get_ultra_native_cdn_links()}
            <style>
                {self._get_ultra_native_css()}
            </style>
        </head>
        <body>
            <div id="ultra-tavern-container">
                {self._get_ultra_native_html_structure()}
            </div>
            
            <!-- Performance Monitor -->
            <div id="performance-monitor"></div>
            
            <!-- Audio Controls -->
            <div id="audio-controls"></div>
            
            <!-- Animation Controls -->
            <div id="animation-controls"></div>
            
            <script>
                {self._get_ultra_native_javascript()}
            </script>
        </body>
        </html>
        """
    
    def _get_ultra_native_css(self) -> str:
        """Ultra-native CSS with advanced styling"""
        return """
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Cinzel', serif;
                background: radial-gradient(ellipse at center, #2c1810 0%, #1a0f08 100%);
                color: #ffd700;
                overflow-x: hidden;
                min-height: 100vh;
            }
            
            #ultra-tavern-container {
                position: relative;
                width: 100%;
                height: 100vh;
                perspective: 1000px;
                transform-style: preserve-3d;
            }
            
            .ultra-character {
                position: absolute;
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: linear-gradient(45deg, #ffd700, #b8860b);
                border: 3px solid #8b0000;
                cursor: pointer;
                transition: all 0.3s ease;
                transform-style: preserve-3d;
                will-change: transform;
            }
            
            .ultra-particle {
                position: absolute;
                pointer-events: none;
                border-radius: 50%;
                will-change: transform, opacity;
            }
            
            .ultra-canvas {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
            }
            
            #performance-monitor {
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 1000;
                background: rgba(0,0,0,0.8);
                padding: 10px;
                border-radius: 5px;
                color: #00ff00;
                font-family: monospace;
                font-size: 12px;
            }
            
            #audio-controls {
                position: fixed;
                bottom: 10px;
                left: 10px;
                z-index: 1000;
                display: flex;
                gap: 10px;
            }
            
            #animation-controls {
                position: fixed;
                bottom: 10px;
                right: 10px;
                z-index: 1000;
                display: flex;
                gap: 10px;
            }
            
            .control-btn {
                padding: 8px 16px;
                background: linear-gradient(45deg, #8b0000, #4a0000);
                color: #ffd700;
                border: 1px solid #ffd700;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-family: inherit;
            }
            
            .control-btn:hover {
                background: linear-gradient(45deg, #b30000, #660000);
                box-shadow: 0 0 10px #ffd700;
                transform: translateY(-2px);
            }
            
            .physics-object {
                position: absolute;
                will-change: transform;
                transform-style: preserve-3d;
            }
            
            .morph-svg {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
                pointer-events: none;
            }
            
            .data-viz-container {
                position: absolute;
                top: 50px;
                left: 50px;
                width: 300px;
                height: 200px;
                background: rgba(0,0,0,0.7);
                border: 1px solid #ffd700;
                border-radius: 10px;
                padding: 10px;
            }
            
            .scroll-trigger-section {
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }
            
            .interactive-zone {
                position: absolute;
                border: 2px dashed #ffd700;
                border-radius: 10px;
                background: rgba(255, 215, 0, 0.1);
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .interactive-zone:hover {
                background: rgba(255, 215, 0, 0.2);
                border-color: #fff;
                box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            }
        """
    
    def _get_ultra_native_html_structure(self) -> str:
        """Generate ultra-native HTML structure"""
        return """
            <!-- Main Tavern Scene -->
            <div id="tavern-scene" class="scroll-trigger-section">
                <canvas id="pixi-canvas" class="ultra-canvas"></canvas>
                <canvas id="three-canvas" class="ultra-canvas"></canvas>
                <svg id="morph-svg" class="morph-svg">
                    <defs>
                        <filter id="glow">
                            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                            <feMerge> 
                                <feMergeNode in="coloredBlur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                    </defs>
                </svg>
                
                <!-- Interactive Zones -->
                <div class="interactive-zone" id="bar-zone" style="top: 20%; left: 10%; width: 200px; height: 100px;">
                    Bar Area
                </div>
                <div class="interactive-zone" id="fireplace-zone" style="top: 60%; left: 70%; width: 150px; height: 150px;">
                    Fireplace
                </div>
                <div class="interactive-zone" id="stage-zone" style="top: 30%; left: 40%; width: 180px; height: 120px;">
                    Stage
                </div>
                
                <!-- Data Visualization -->
                <div class="data-viz-container" id="real-time-data">
                    <h3>Real-time Metrics</h3>
                    <div id="fps-chart"></div>
                    <div id="interaction-graph"></div>
                </div>
            </div>
            
            <!-- Character Container -->
            <div id="characters-container"></div>
            
            <!-- Particle Systems Container -->
            <div id="particles-container"></div>
            
            <!-- Physics World -->
            <div id="physics-world"></div>
        """

    def _get_ultra_native_javascript(self) -> str:
        """Generate comprehensive ultra-native JavaScript environment"""
        return f"""
            // Ultra-Native GSAP Environment Initialization
            console.log('🚀 Initializing Ultra-Native GSAP Environment...');

            // Global Configuration
            const ULTRA_CONFIG = {{
                fps: 60,
                particleCount: 500,
                physicsEnabled: true,
                soundEnabled: true,
                performanceMonitoring: true,
                debugMode: false
            }};

            // Performance Monitoring
            let stats, frameCount = 0, lastTime = performance.now();
            let performanceData = {{
                fps: 0,
                frameTime: 0,
                memoryUsage: 0,
                animationCount: 0
            }};

            // Initialize Performance Monitor
            function initPerformanceMonitor() {{
                if (typeof Stats !== 'undefined') {{
                    stats = new Stats();
                    stats.showPanel(0); // 0: fps, 1: ms, 2: mb, 3+: custom
                    document.getElementById('performance-monitor').appendChild(stats.dom);
                }}

                // Custom performance tracking
                setInterval(updatePerformanceMetrics, 1000);
            }}

            function updatePerformanceMetrics() {{
                const now = performance.now();
                const deltaTime = now - lastTime;
                performanceData.fps = Math.round(1000 / (deltaTime / frameCount));
                performanceData.frameTime = deltaTime / frameCount;

                if (performance.memory) {{
                    performanceData.memoryUsage = Math.round(performance.memory.usedJSHeapSize / 1048576);
                }}

                frameCount = 0;
                lastTime = now;

                updatePerformanceDisplay();
            }}

            function updatePerformanceDisplay() {{
                const monitor = document.getElementById('performance-monitor');
                if (monitor && !stats) {{
                    monitor.innerHTML = `
                        <div>FPS: ${{performanceData.fps}}</div>
                        <div>Frame Time: ${{performanceData.frameTime.toFixed(2)}}ms</div>
                        <div>Memory: ${{performanceData.memoryUsage}}MB</div>
                        <div>Animations: ${{performanceData.animationCount}}</div>
                    `;
                }}
            }}

            // GSAP Ultra Configuration
            function initUltraGSAP() {{
                // Register all plugins
                gsap.registerPlugin(
                    ScrollTrigger, TextPlugin, MorphSVGPlugin, DrawSVGPlugin,
                    PixiPlugin, Flip, CustomEase, MotionPathPlugin, Physics2DPlugin,
                    ThrowPropsPlugin, Draggable, InertiaPlugin, SplitText, ScrambleTextPlugin
                );

                // Ultra-performance configuration
                gsap.config({{
                    force3D: true,
                    nullTargetWarn: false,
                    trialWarn: false,
                    autoSleep: 60,
                    units: {{left: "px", top: "px", rotation: "deg"}}
                }});

                // Set global performance optimizations
                gsap.set("*", {{
                    force3D: true,
                    transformPerspective: 1000,
                    backfaceVisibility: "hidden"
                }});

                // Configure ticker for 60+ FPS
                gsap.ticker.fps(ULTRA_CONFIG.fps);
                gsap.ticker.lagSmoothing(500, 33);

                // Custom ultra easing functions
                CustomEase.create("ultraBounce", "M0,0 C0.14,0 0.242,0.438 0.272,0.561 0.313,0.728 0.354,0.963 0.362,1 0.37,0.985 0.414,0.881 0.455,0.676 0.51,0.400 0.57,0.035 0.636,0.002 0.696,-0.027 0.771,0.227 0.82,0.514 0.87,0.804 0.906,1.003 1,1");
                CustomEase.create("ultraElastic", "M0,0 C0.29,0 0.474,0.334 0.61,0.6 0.75,0.9 0.818,1.001 1,1");
                CustomEase.create("ultraMagic", "M0,0 C0.175,0.885 0.32,1.275 0.5,1 0.68,0.725 0.825,0.115 1,1");
                CustomEase.create("ultraPhysics", "M0,0 C0.445,0.05 0.55,0.95 0.7,0.8 0.85,0.65 0.9,1.2 1,1");

                console.log('✅ Ultra GSAP Configuration Complete');
            }}

            {self._get_particle_system_js()}
            {self._get_morph_system_js()}
            {self._get_audio_system_js()}
            {self._get_physics_system_js()}
            {self._get_data_visualization_js()}
            {self._get_interaction_system_js()}
            {self._get_scroll_trigger_js()}
            {self._get_initialization_js()}
        """

    def _get_particle_system_js(self) -> str:
        """Advanced particle system JavaScript"""
        return """
            // Advanced Particle System with GSAP + Physics
            class UltraParticleSystem {
                constructor(container, options = {}) {
                    this.container = container;
                    this.particles = [];
                    this.options = {
                        count: options.count || 100,
                        type: options.type || 'spark',
                        physics: options.physics || true,
                        lifespan: options.lifespan || 3000,
                        ...options
                    };
                    this.timeline = gsap.timeline();
                }

                createParticle(x, y, type = 'spark') {
                    const particle = document.createElement('div');
                    particle.className = `ultra-particle ${type}-particle`;

                    // Particle styling based on type
                    const styles = this.getParticleStyles(type);
                    Object.assign(particle.style, styles);

                    particle.style.left = x + 'px';
                    particle.style.top = y + 'px';

                    this.container.appendChild(particle);

                    // GSAP animation with physics
                    const animation = this.animateParticle(particle, type);

                    this.particles.push({
                        element: particle,
                        animation: animation,
                        createdAt: Date.now()
                    });

                    return particle;
                }

                getParticleStyles(type) {
                    const styles = {
                        spark: {
                            width: '4px',
                            height: '4px',
                            background: 'radial-gradient(circle, #ffd700 0%, #ff6b00 100%)',
                            boxShadow: '0 0 6px #ffd700'
                        },
                        magic: {
                            width: '6px',
                            height: '6px',
                            background: 'radial-gradient(circle, #9370db 0%, #4b0082 100%)',
                            boxShadow: '0 0 8px #9370db'
                        },
                        fire: {
                            width: '8px',
                            height: '8px',
                            background: 'radial-gradient(circle, #ff4500 0%, #8b0000 100%)',
                            boxShadow: '0 0 10px #ff4500'
                        },
                        ice: {
                            width: '5px',
                            height: '5px',
                            background: 'radial-gradient(circle, #87ceeb 0%, #4682b4 100%)',
                            boxShadow: '0 0 7px #87ceeb'
                        }
                    };

                    return styles[type] || styles.spark;
                }

                animateParticle(particle, type) {
                    const tl = gsap.timeline();

                    // Initial state
                    gsap.set(particle, {
                        opacity: 0,
                        scale: 0,
                        rotation: 0
                    });

                    // Entrance animation
                    tl.to(particle, {
                        opacity: 1,
                        scale: "random(0.5, 1.5)",
                        duration: 0.1,
                        ease: "power2.out"
                    });

                    // Movement based on type
                    switch(type) {
                        case 'spark':
                            tl.to(particle, {
                                x: "random(-100, 100)",
                                y: "random(-80, -20)",
                                rotation: "random(0, 360)",
                                duration: "random(1, 2)",
                                ease: "ultraPhysics"
                            }, 0.1);
                            break;

                        case 'magic':
                            tl.to(particle, {
                                motionPath: {
                                    path: `M0,0 Q${Math.random() * 100 - 50},${Math.random() * -100} ${Math.random() * 200 - 100},${Math.random() * -150}`,
                                    autoRotate: true
                                },
                                duration: "random(2, 4)",
                                ease: "ultraMagic"
                            }, 0.1);
                            break;

                        case 'fire':
                            tl.to(particle, {
                                y: "random(-120, -60)",
                                x: "random(-30, 30)",
                                scale: "random(1.5, 2.5)",
                                duration: "random(1.5, 2.5)",
                                ease: "power1.out"
                            }, 0.1);
                            break;

                        case 'ice':
                            tl.to(particle, {
                                y: "random(50, 150)",
                                x: "random(-50, 50)",
                                rotation: "random(0, 720)",
                                duration: "random(2, 3)",
                                ease: "bounce.out"
                            }, 0.1);
                            break;
                    }

                    // Exit animation
                    tl.to(particle, {
                        opacity: 0,
                        scale: 0,
                        duration: 0.5,
                        ease: "power2.in",
                        onComplete: () => {
                            particle.remove();
                            this.removeParticle(particle);
                        }
                    }, "-=0.5");

                    return tl;
                }

                burst(x, y, count = 20, type = 'spark') {
                    for (let i = 0; i < count; i++) {
                        setTimeout(() => {
                            this.createParticle(x, y, type);
                        }, i * 10);
                    }
                }

                removeParticle(particleElement) {
                    this.particles = this.particles.filter(p => p.element !== particleElement);
                }

                cleanup() {
                    this.particles.forEach(p => {
                        p.animation.kill();
                        p.element.remove();
                    });
                    this.particles = [];
                    this.timeline.kill();
                }
            }

            // Global particle system instance
            let globalParticleSystem;
        """

    def _get_morph_system_js(self) -> str:
        """Advanced morphing system JavaScript"""
        return """
            // Advanced Morphing System using MorphSVG
            class UltraMorphSystem {
                constructor() {
                    this.morphTargets = new Map();
                    this.activeMorphs = new Map();
                }

                createMorphTarget(id, pathData, style = {}) {
                    const svg = document.getElementById('morph-svg');
                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

                    path.setAttribute('id', id);
                    path.setAttribute('d', pathData);
                    path.setAttribute('fill', style.fill || '#ffd700');
                    path.setAttribute('stroke', style.stroke || '#8b0000');
                    path.setAttribute('stroke-width', style.strokeWidth || '2');
                    path.setAttribute('filter', 'url(#glow)');

                    svg.appendChild(path);
                    this.morphTargets.set(id, path);

                    return path;
                }

                morphBetween(fromId, toId, duration = 2, ease = "ultraMagic") {
                    const fromPath = this.morphTargets.get(fromId);
                    const toPath = this.morphTargets.get(toId);

                    if (!fromPath || !toPath) {
                        console.warn('Morph targets not found:', fromId, toId);
                        return;
                    }

                    const tl = gsap.timeline();

                    // Morph the path
                    tl.to(fromPath, {
                        morphSVG: toPath,
                        duration: duration,
                        ease: ease,
                        onUpdate: () => {
                            this.onMorphUpdate(fromId, toId);
                        }
                    });

                    // Add visual effects
                    tl.to(fromPath, {
                        fill: '#ff6b00',
                        duration: duration / 2,
                        yoyo: true,
                        repeat: 1
                    }, 0);

                    this.activeMorphs.set(`${fromId}-${toId}`, tl);
                    return tl;
                }

                onMorphUpdate(fromId, toId) {
                    // Trigger particle effects during morph
                    if (Math.random() < 0.1) {
                        const rect = this.morphTargets.get(fromId).getBoundingClientRect();
                        globalParticleSystem.createParticle(
                            rect.left + Math.random() * rect.width,
                            rect.top + Math.random() * rect.height,
                            'magic'
                        );
                    }
                }

                createDynamicShape(points, style = {}) {
                    const pathData = this.pointsToPath(points);
                    const id = 'dynamic-' + Date.now();
                    return this.createMorphTarget(id, pathData, style);
                }

                pointsToPath(points) {
                    if (points.length < 2) return '';

                    let path = `M${points[0].x},${points[0].y}`;
                    for (let i = 1; i < points.length; i++) {
                        path += ` L${points[i].x},${points[i].y}`;
                    }
                    path += ' Z';

                    return path;
                }
            }

            // Global morph system instance
            let globalMorphSystem;
        """

    def _get_audio_system_js(self) -> str:
        """Advanced audio system with Tone.js and Howler.js"""
        return """
            // Ultra Audio System with Tone.js and Howler.js
            class UltraAudioSystem {
                constructor() {
                    this.sounds = new Map();
                    this.synth = null;
                    this.masterVolume = 0.7;
                    this.initialized = false;
                }

                async init() {
                    if (this.initialized) return;

                    try {
                        // Initialize Tone.js
                        if (typeof Tone !== 'undefined') {
                            await Tone.start();
                            this.synth = new Tone.Synth().toDestination();
                            console.log('✅ Tone.js initialized');
                        }

                        // Initialize sound effects
                        this.loadSoundEffects();
                        this.initialized = true;

                    } catch (error) {
                        console.warn('Audio initialization failed:', error);
                    }
                }

                loadSoundEffects() {
                    const soundData = {
                        click: { frequency: 800, duration: 0.1 },
                        hover: { frequency: 600, duration: 0.05 },
                        success: { frequency: 1200, duration: 0.2 },
                        error: { frequency: 200, duration: 0.3 },
                        magic: { frequency: 1000, duration: 0.5 },
                        combat: { frequency: 150, duration: 0.8 }
                    };

                    Object.entries(soundData).forEach(([name, config]) => {
                        this.sounds.set(name, config);
                    });
                }

                playTone(frequency, duration = 0.1, volume = 0.5) {
                    if (!this.synth) return;

                    this.synth.volume.value = Tone.gainToDb(volume * this.masterVolume);
                    this.synth.triggerAttackRelease(frequency, duration);
                }

                playSound(soundName) {
                    const sound = this.sounds.get(soundName);
                    if (!sound) return;

                    this.playTone(sound.frequency, sound.duration);
                }

                playSequence(notes, timing = 0.2) {
                    if (!this.synth) return;

                    const seq = new Tone.Sequence((time, note) => {
                        this.synth.triggerAttackRelease(note, timing, time);
                    }, notes, timing);

                    seq.start();
                    Tone.Transport.start();

                    setTimeout(() => {
                        seq.stop();
                        Tone.Transport.stop();
                    }, notes.length * timing * 1000 + 1000);
                }

                setMasterVolume(volume) {
                    this.masterVolume = Math.max(0, Math.min(1, volume));
                }
            }

            // Global audio system
            let globalAudioSystem;
        """

    def _get_physics_system_js(self) -> str:
        """Physics system with Matter.js integration"""
        return """
            // Ultra Physics System with Matter.js
            class UltraPhysicsSystem {
                constructor() {
                    this.engine = null;
                    this.world = null;
                    this.render = null;
                    this.bodies = new Map();
                    this.constraints = new Map();
                }

                init(container) {
                    if (typeof Matter === 'undefined') {
                        console.warn('Matter.js not loaded, physics disabled');
                        return;
                    }

                    // Create engine
                    this.engine = Matter.Engine.create();
                    this.world = this.engine.world;

                    // Configure physics
                    this.engine.world.gravity.y = 0.8;
                    this.engine.world.gravity.x = 0;

                    // Create renderer
                    this.render = Matter.Render.create({
                        element: container,
                        engine: this.engine,
                        options: {
                            width: container.clientWidth,
                            height: container.clientHeight,
                            wireframes: false,
                            background: 'transparent',
                            showAngleIndicator: false,
                            showVelocity: false
                        }
                    });

                    // Start the engine and renderer
                    Matter.Engine.run(this.engine);
                    Matter.Render.run(this.render);

                    console.log('✅ Physics system initialized');
                }

                createBody(x, y, width, height, options = {}) {
                    const body = Matter.Bodies.rectangle(x, y, width, height, {
                        restitution: options.restitution || 0.8,
                        friction: options.friction || 0.1,
                        frictionAir: options.frictionAir || 0.01,
                        density: options.density || 0.001,
                        ...options
                    });

                    Matter.World.add(this.world, body);

                    const id = 'body-' + Date.now() + '-' + Math.random();
                    this.bodies.set(id, body);

                    return { id, body };
                }

                createCircle(x, y, radius, options = {}) {
                    const body = Matter.Bodies.circle(x, y, radius, {
                        restitution: options.restitution || 0.9,
                        friction: options.friction || 0.1,
                        frictionAir: options.frictionAir || 0.01,
                        density: options.density || 0.001,
                        ...options
                    });

                    Matter.World.add(this.world, body);

                    const id = 'circle-' + Date.now() + '-' + Math.random();
                    this.bodies.set(id, body);

                    return { id, body };
                }

                applyForce(bodyId, force) {
                    const body = this.bodies.get(bodyId);
                    if (body) {
                        Matter.Body.applyForce(body, body.position, force);
                    }
                }

                syncWithGSAP(bodyId, element) {
                    const body = this.bodies.get(bodyId);
                    if (!body || !element) return;

                    // Sync physics body position with GSAP element
                    const updatePosition = () => {
                        gsap.set(element, {
                            x: body.position.x,
                            y: body.position.y,
                            rotation: body.angle * 180 / Math.PI
                        });

                        requestAnimationFrame(updatePosition);
                    };

                    updatePosition();
                }

                removeBody(bodyId) {
                    const body = this.bodies.get(bodyId);
                    if (body) {
                        Matter.World.remove(this.world, body);
                        this.bodies.delete(bodyId);
                    }
                }
            }

            // Global physics system
            let globalPhysicsSystem;
        """

    def _get_data_visualization_js(self) -> str:
        """Real-time data visualization with D3.js and GSAP"""
        return """
            // Ultra Data Visualization System
            class UltraDataViz {
                constructor() {
                    this.charts = new Map();
                    this.realTimeData = {
                        fps: [],
                        interactions: [],
                        performance: []
                    };
                }

                createFPSChart(container) {
                    if (typeof d3 === 'undefined') return;

                    const width = 280;
                    const height = 80;
                    const margin = { top: 10, right: 10, bottom: 20, left: 30 };

                    const svg = d3.select(container)
                        .append('svg')
                        .attr('width', width)
                        .attr('height', height);

                    const xScale = d3.scaleLinear()
                        .domain([0, 60])
                        .range([margin.left, width - margin.right]);

                    const yScale = d3.scaleLinear()
                        .domain([0, 120])
                        .range([height - margin.bottom, margin.top]);

                    const line = d3.line()
                        .x((d, i) => xScale(i))
                        .y(d => yScale(d))
                        .curve(d3.curveMonotoneX);

                    const path = svg.append('path')
                        .attr('fill', 'none')
                        .attr('stroke', '#ffd700')
                        .attr('stroke-width', 2);

                    this.charts.set('fps', { svg, path, line, xScale, yScale });
                }

                updateFPSChart(fps) {
                    this.realTimeData.fps.push(fps);
                    if (this.realTimeData.fps.length > 60) {
                        this.realTimeData.fps.shift();
                    }

                    const chart = this.charts.get('fps');
                    if (chart) {
                        chart.path
                            .datum(this.realTimeData.fps)
                            .attr('d', chart.line);

                        // Animate the line drawing
                        const pathLength = chart.path.node().getTotalLength();
                        gsap.fromTo(chart.path.node(),
                            { strokeDasharray: pathLength, strokeDashoffset: pathLength },
                            { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }
                        );
                    }
                }

                createInteractionGraph(container) {
                    // Create a simple interaction counter visualization
                    const div = d3.select(container)
                        .append('div')
                        .style('color', '#ffd700')
                        .style('font-size', '12px');

                    this.charts.set('interactions', { div });
                }

                updateInteractionGraph(interactionType) {
                    this.realTimeData.interactions.push({
                        type: interactionType,
                        timestamp: Date.now()
                    });

                    // Keep only last 10 interactions
                    if (this.realTimeData.interactions.length > 10) {
                        this.realTimeData.interactions.shift();
                    }

                    const chart = this.charts.get('interactions');
                    if (chart) {
                        const recent = this.realTimeData.interactions.slice(-5);
                        chart.div.html(
                            'Recent: ' + recent.map(i => i.type).join(', ')
                        );
                    }
                }
            }

            // Global data visualization
            let globalDataViz;
        """

    def _get_interaction_system_js(self) -> str:
        """Advanced interaction system with drag-and-drop"""
        return """
            // Ultra Interaction System
            class UltraInteractionSystem {
                constructor() {
                    this.draggables = new Map();
                    this.dropZones = new Map();
                    this.interactions = [];
                }

                makeDraggable(element, options = {}) {
                    const draggable = Draggable.create(element, {
                        type: "x,y",
                        edgeResistance: 0.65,
                        bounds: options.bounds || document.body,
                        inertia: true,
                        autoScroll: 1,
                        onDragStart: (e) => {
                            // Visual feedback
                            gsap.to(element, {
                                scale: 1.1,
                                rotation: "random(-5, 5)",
                                duration: 0.2,
                                ease: "back.out(1.7)"
                            });

                            // Particle effect
                            const rect = element.getBoundingClientRect();
                            globalParticleSystem.burst(
                                rect.left + rect.width/2,
                                rect.top + rect.height/2,
                                10, 'spark'
                            );

                            // Sound effect
                            globalAudioSystem.playSound('click');

                            // Log interaction
                            this.logInteraction('drag_start', element);
                        },
                        onDrag: (e) => {
                            // Check for drop zone collisions
                            this.checkDropZoneCollisions(element);
                        },
                        onDragEnd: (e) => {
                            // Reset visual state
                            gsap.to(element, {
                                scale: 1,
                                rotation: 0,
                                duration: 0.3,
                                ease: "elastic.out(1, 0.3)"
                            });

                            // Check final drop
                            this.handleDrop(element);

                            // Log interaction
                            this.logInteraction('drag_end', element);
                        }
                    });

                    const id = 'draggable-' + Date.now();
                    this.draggables.set(id, draggable[0]);

                    return id;
                }

                createDropZone(element, onDrop) {
                    const id = 'dropzone-' + Date.now();

                    this.dropZones.set(id, {
                        element: element,
                        onDrop: onDrop,
                        active: false
                    });

                    // Visual styling for drop zone
                    gsap.set(element, {
                        borderStyle: 'dashed',
                        borderWidth: '2px',
                        borderColor: '#ffd700'
                    });

                    return id;
                }

                checkDropZoneCollisions(dragElement) {
                    const dragRect = dragElement.getBoundingClientRect();

                    this.dropZones.forEach((zone, id) => {
                        const zoneRect = zone.element.getBoundingClientRect();
                        const isColliding = this.isColliding(dragRect, zoneRect);

                        if (isColliding && !zone.active) {
                            // Activate drop zone
                            zone.active = true;
                            gsap.to(zone.element, {
                                backgroundColor: 'rgba(255, 215, 0, 0.2)',
                                scale: 1.05,
                                duration: 0.2
                            });
                            globalAudioSystem.playSound('hover');

                        } else if (!isColliding && zone.active) {
                            // Deactivate drop zone
                            zone.active = false;
                            gsap.to(zone.element, {
                                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                                scale: 1,
                                duration: 0.2
                            });
                        }
                    });
                }

                isColliding(rect1, rect2) {
                    return !(rect1.right < rect2.left ||
                            rect1.left > rect2.right ||
                            rect1.bottom < rect2.top ||
                            rect1.top > rect2.bottom);
                }

                handleDrop(dragElement) {
                    const dragRect = dragElement.getBoundingClientRect();

                    this.dropZones.forEach((zone, id) => {
                        if (zone.active) {
                            // Execute drop callback
                            if (zone.onDrop) {
                                zone.onDrop(dragElement, zone.element);
                            }

                            // Visual feedback
                            globalParticleSystem.burst(
                                zone.element.getBoundingClientRect().left + zone.element.offsetWidth/2,
                                zone.element.getBoundingClientRect().top + zone.element.offsetHeight/2,
                                15, 'magic'
                            );

                            globalAudioSystem.playSound('success');

                            // Reset zone
                            zone.active = false;
                            gsap.to(zone.element, {
                                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                                scale: 1,
                                duration: 0.3
                            });
                        }
                    });
                }

                logInteraction(type, element) {
                    const interaction = {
                        type: type,
                        element: element.id || element.className,
                        timestamp: Date.now()
                    };

                    this.interactions.push(interaction);
                    globalDataViz.updateInteractionGraph(type);

                    // Keep only last 100 interactions
                    if (this.interactions.length > 100) {
                        this.interactions.shift();
                    }
                }
            }

            // Global interaction system
            let globalInteractionSystem;
        """

    def _get_scroll_trigger_js(self) -> str:
        """ScrollTrigger animations and effects"""
        return """
            // Ultra ScrollTrigger System
            function initScrollTriggerAnimations() {
                // Parallax background elements
                gsap.to('.tavern-scene', {
                    yPercent: -50,
                    ease: "none",
                    scrollTrigger: {
                        trigger: '.tavern-scene',
                        start: "top bottom",
                        end: "bottom top",
                        scrub: true
                    }
                });

                // Character entrance on scroll
                gsap.utils.toArray('.ultra-character').forEach((char, i) => {
                    gsap.fromTo(char,
                        {
                            y: 100,
                            opacity: 0,
                            scale: 0.5,
                            rotation: -180
                        },
                        {
                            y: 0,
                            opacity: 1,
                            scale: 1,
                            rotation: 0,
                            duration: 1,
                            ease: "back.out(1.7)",
                            scrollTrigger: {
                                trigger: char,
                                start: "top 80%",
                                end: "bottom 20%",
                                toggleActions: "play none none reverse",
                                onEnter: () => {
                                    globalParticleSystem.burst(
                                        char.offsetLeft + char.offsetWidth/2,
                                        char.offsetTop + char.offsetHeight/2,
                                        20, 'magic'
                                    );
                                    globalAudioSystem.playSound('magic');
                                }
                            }
                        }
                    );
                });

                // Interactive zones reveal
                gsap.utils.toArray('.interactive-zone').forEach((zone, i) => {
                    gsap.fromTo(zone,
                        {
                            scale: 0,
                            opacity: 0
                        },
                        {
                            scale: 1,
                            opacity: 1,
                            duration: 0.8,
                            ease: "elastic.out(1, 0.3)",
                            delay: i * 0.2,
                            scrollTrigger: {
                                trigger: zone,
                                start: "top 90%",
                                toggleActions: "play none none reverse"
                            }
                        }
                    );
                });

                // Data visualization reveal
                gsap.fromTo('#real-time-data',
                    {
                        x: -300,
                        opacity: 0
                    },
                    {
                        x: 0,
                        opacity: 1,
                        duration: 1,
                        ease: "power3.out",
                        scrollTrigger: {
                            trigger: '#real-time-data',
                            start: "top 80%",
                            toggleActions: "play none none reverse"
                        }
                    }
                );
            }
        """

    def _get_initialization_js(self) -> str:
        """Complete initialization system"""
        return """
            // Ultra Initialization System
            async function initializeUltraNativeEnvironment() {
                console.log('🚀 Starting Ultra-Native GSAP Environment...');

                try {
                    // Initialize performance monitoring
                    initPerformanceMonitor();

                    // Initialize GSAP
                    initUltraGSAP();

                    // Initialize all systems
                    globalParticleSystem = new UltraParticleSystem(
                        document.getElementById('particles-container')
                    );

                    globalMorphSystem = new UltraMorphSystem();

                    globalAudioSystem = new UltraAudioSystem();
                    await globalAudioSystem.init();

                    globalPhysicsSystem = new UltraPhysicsSystem();
                    globalPhysicsSystem.init(document.getElementById('physics-world'));

                    globalDataViz = new UltraDataViz();
                    globalDataViz.createFPSChart(document.getElementById('fps-chart'));
                    globalDataViz.createInteractionGraph(document.getElementById('interaction-graph'));

                    globalInteractionSystem = new UltraInteractionSystem();

                    // Initialize ScrollTrigger animations
                    initScrollTriggerAnimations();

                    // Create initial content
                    createInitialContent();

                    // Setup controls
                    setupControls();

                    // Start animation loop
                    startAnimationLoop();

                    console.log('✅ Ultra-Native Environment Fully Initialized!');

                } catch (error) {
                    console.error('❌ Initialization failed:', error);
                }
            }

            function createInitialContent() {
                // Create some initial characters
                for (let i = 0; i < 5; i++) {
                    createCharacter(
                        Math.random() * window.innerWidth,
                        Math.random() * window.innerHeight,
                        `Character ${i + 1}`
                    );
                }

                // Create initial morph shapes
                const shapes = [
                    { id: 'circle', path: 'M50,50 m-40,0 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0' },
                    { id: 'square', path: 'M10,10 L90,10 L90,90 L10,90 Z' },
                    { id: 'triangle', path: 'M50,10 L90,90 L10,90 Z' },
                    { id: 'star', path: 'M50,5 L61,35 L95,35 L68,57 L79,91 L50,70 L21,91 L32,57 L5,35 L39,35 Z' }
                ];

                shapes.forEach(shape => {
                    globalMorphSystem.createMorphTarget(shape.id, shape.path);
                });

                // Start morphing sequence
                setTimeout(() => {
                    globalMorphSystem.morphBetween('circle', 'square', 2);
                    setTimeout(() => {
                        globalMorphSystem.morphBetween('square', 'triangle', 2);
                        setTimeout(() => {
                            globalMorphSystem.morphBetween('triangle', 'star', 2);
                        }, 2500);
                    }, 2500);
                }, 1000);
            }

            function createCharacter(x, y, name) {
                const character = document.createElement('div');
                character.className = 'ultra-character';
                character.textContent = name.charAt(0);
                character.title = name;
                character.style.left = x + 'px';
                character.style.top = y + 'px';

                document.getElementById('characters-container').appendChild(character);

                // Make draggable
                globalInteractionSystem.makeDraggable(character);

                // Add physics body
                const physicsBody = globalPhysicsSystem.createCircle(x, y, 40);
                globalPhysicsSystem.syncWithGSAP(physicsBody.id, character);

                // Add hover effects
                character.addEventListener('mouseenter', () => {
                    gsap.to(character, {
                        scale: 1.2,
                        rotation: "random(-10, 10)",
                        duration: 0.3,
                        ease: "back.out(1.7)"
                    });
                    globalAudioSystem.playSound('hover');
                });

                character.addEventListener('mouseleave', () => {
                    gsap.to(character, {
                        scale: 1,
                        rotation: 0,
                        duration: 0.3,
                        ease: "elastic.out(1, 0.3)"
                    });
                });

                // Add click effects
                character.addEventListener('click', () => {
                    globalParticleSystem.burst(x, y, 15, 'magic');
                    globalAudioSystem.playSound('click');
                    globalInteractionSystem.logInteraction('character_click', character);
                });

                return character;
            }

            function setupControls() {
                // Audio controls
                const audioControls = document.getElementById('audio-controls');
                audioControls.innerHTML = `
                    <button class="control-btn" onclick="globalAudioSystem.playSequence(['C4', 'E4', 'G4', 'C5'])">🎵 Play Melody</button>
                    <button class="control-btn" onclick="toggleMasterVolume()">🔊 Volume</button>
                `;

                // Animation controls
                const animControls = document.getElementById('animation-controls');
                animControls.innerHTML = `
                    <button class="control-btn" onclick="triggerParticleBurst()">✨ Particles</button>
                    <button class="control-btn" onclick="triggerMorphSequence()">🔄 Morph</button>
                    <button class="control-btn" onclick="resetScene()">🔄 Reset</button>
                `;
            }

            function startAnimationLoop() {
                function animate() {
                    if (stats) stats.begin();

                    // Update performance data
                    frameCount++;
                    performanceData.animationCount = gsap.globalTimeline.getChildren().length;

                    // Update data visualizations
                    if (frameCount % 60 === 0) { // Update every second
                        globalDataViz.updateFPSChart(performanceData.fps);
                    }

                    if (stats) stats.end();
                    requestAnimationFrame(animate);
                }

                animate();
            }

            // Utility functions for controls
            function triggerParticleBurst() {
                const centerX = window.innerWidth / 2;
                const centerY = window.innerHeight / 2;
                globalParticleSystem.burst(centerX, centerY, 50, 'magic');
                globalAudioSystem.playSound('magic');
            }

            function triggerMorphSequence() {
                globalMorphSystem.morphBetween('circle', 'star', 1.5);
                globalAudioSystem.playSound('magic');
            }

            function resetScene() {
                // Reset all animations
                gsap.globalTimeline.clear();

                // Clear particles
                globalParticleSystem.cleanup();

                // Recreate content
                document.getElementById('characters-container').innerHTML = '';
                createInitialContent();

                globalAudioSystem.playSound('success');
            }

            function toggleMasterVolume() {
                const currentVolume = globalAudioSystem.masterVolume;
                const newVolume = currentVolume > 0 ? 0 : 0.7;
                globalAudioSystem.setMasterVolume(newVolume);
                globalAudioSystem.playSound('click');
            }

            // Initialize everything when DOM is ready
            document.addEventListener('DOMContentLoaded', initializeUltraNativeEnvironment);

            // Handle window resize
            window.addEventListener('resize', () => {
                if (globalPhysicsSystem.render) {
                    globalPhysicsSystem.render.canvas.width = window.innerWidth;
                    globalPhysicsSystem.render.canvas.height = window.innerHeight;
                }
            });
        """
