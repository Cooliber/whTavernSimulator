/**
 * EmotionSystem3D - State-of-the-Art GSAP Emotion Engine
 * Advanced 3D emotion visualization with particle systems, facial animations, and atmospheric effects
 */

export class EmotionSystem3D {
    constructor() {
        this.isInitialized = false;
        this.gsapController = null;
        this.particleEngine = null;
        
        // Emotion state tracking
        this.activeEmotions = new Map();
        this.emotionHistory = new Map();
        this.emotionIntensity = new Map();
        
        // 3D emotion configurations
        this.emotionConfigs = new Map();
        this.particleConfigs = new Map();
        this.audioConfigs = new Map();
        
        // Performance tracking
        this.maxActiveEmotions = 15;
        this.particlePool = [];
        this.animationPool = [];
        
        // Emotion blending system
        this.emotionBlends = new Map();
        this.transitionTimelines = new Map();
        
        // Advanced lighting system
        this.emotionLights = new Map();
        this.ambientController = null;
        
        console.log('🎭 EmotionSystem3D initialized');
    }
    
    /**
     * Initialize the 3D emotion system
     */
    async init(dependencies = {}) {
        try {
            this.gsapController = dependencies.gsapController;
            this.particleEngine = dependencies.particleEngine;
            this.ambientController = dependencies.ambientController;
            
            // Initialize emotion configurations
            this.initializeEmotionConfigs();
            
            // Setup particle configurations
            this.setupParticleConfigs();
            
            // Initialize audio configurations
            this.initializeAudioConfigs();
            
            // Setup emotion blending system
            this.setupEmotionBlending();
            
            // Initialize lighting system
            this.initializeLightingSystem();
            
            // Create particle pools for performance
            this.createParticlePools();
            
            this.isInitialized = true;
            console.log('✅ EmotionSystem3D fully initialized with SOTA GSAP features');
            
        } catch (error) {
            console.error('❌ Failed to initialize EmotionSystem3D:', error);
            throw error;
        }
    }    
  
  /**
     * Initialize comprehensive emotion configurations
     */
    initializeEmotionConfigs() {
        const configs = {
            // Positive emotions
            joy: {
                color: { primary: '#FFD700', secondary: '#FFA500', accent: '#FFFF00' },
                intensity: { min: 0.3, max: 1.0, default: 0.7 },
                duration: { min: 2, max: 8, default: 4 },
                particles: {
                    type: 'sparkles',
                    count: { min: 15, max: 40 },
                    size: { min: 2, max: 8 },
                    velocity: { min: 50, max: 150 },
                    gravity: -0.2,
                    life: { min: 1, max: 3 }
                },
                animation: {
                    scale: { from: 1, to: 1.15, ease: 'elastic.out(1, 0.3)' },
                    glow: { intensity: 0.8, radius: 25, pulsate: true },
                    bounce: { amplitude: 10, frequency: 2 },
                    shimmer: { opacity: { min: 0.8, max: 1.2 }, speed: 1.5 }
                },
                facial: {
                    eyeScale: 1.1,
                    mouthCurve: 15,
                    cheekRaise: 0.3,
                    browLift: 0.2
                },
                audio: {
                    frequency: 440,
                    harmonics: [880, 1320],
                    volume: 0.3,
                    reverb: 0.2
                }
            },
            
            anger: {
                color: { primary: '#8B0000', secondary: '#FF4500', accent: '#DC143C' },
                intensity: { min: 0.4, max: 1.0, default: 0.8 },
                duration: { min: 1, max: 6, default: 3 },
                particles: {
                    type: 'flames',
                    count: { min: 20, max: 60 },
                    size: { min: 3, max: 12 },
                    velocity: { min: 80, max: 200 },
                    gravity: -0.1,
                    life: { min: 0.5, max: 2 },
                    turbulence: 0.8
                },
                animation: {
                    shake: { amplitude: 8, frequency: 15, decay: 0.9 },
                    glow: { intensity: 1.0, radius: 35, color: '#FF0000' },
                    distortion: { skewX: 3, skewY: 1, frequency: 8 },
                    pulsate: { scale: { min: 0.95, max: 1.1 }, speed: 3 }
                },
                facial: {
                    eyeScale: 0.8,
                    browFurrow: 0.8,
                    mouthTension: 0.6,
                    jawClench: 0.4
                },
                audio: {
                    frequency: 220,
                    harmonics: [110, 330],
                    volume: 0.4,
                    distortion: 0.3
                }
            },
            
            fear: {
                color: { primary: '#4B0082', secondary: '#8A2BE2', accent: '#9370DB' },
                intensity: { min: 0.2, max: 0.9, default: 0.6 },
                duration: { min: 3, max: 10, default: 6 },
                particles: {
                    type: 'wisps',
                    count: { min: 10, max: 30 },
                    size: { min: 1, max: 6 },
                    velocity: { min: 20, max: 80 },
                    gravity: 0.05,
                    life: { min: 2, max: 5 },
                    opacity: { min: 0.3, max: 0.7 }
                },
                animation: {
                    tremble: { amplitude: 3, frequency: 25, randomness: 0.8 },
                    shrink: { scale: { from: 1, to: 0.9 }, ease: 'power2.inOut' },
                    fade: { opacity: { min: 0.7, max: 1.0 }, speed: 2 },
                    recoil: { x: -15, duration: 0.3, ease: 'back.out(1.7)' }
                },
                facial: {
                    eyeWiden: 0.7,
                    browRaise: 0.6,
                    mouthOpen: 0.3,
                    nostrilFlare: 0.2
                },
                audio: {
                    frequency: 150,
                    harmonics: [75, 225],
                    volume: 0.2,
                    tremolo: 0.4
                }
            },
            
            // Warhammer-specific emotions
            corruption: {
                color: { primary: '#800080', secondary: '#4B0082', accent: '#8B008B' },
                intensity: { min: 0.5, max: 1.0, default: 0.8 },
                duration: { min: 5, max: 15, default: 10 },
                particles: {
                    type: 'chaos',
                    count: { min: 15, max: 40 },
                    size: { min: 2, max: 8 },
                    velocity: { min: 30, max: 120 },
                    gravity: 0,
                    life: { min: 2, max: 6 },
                    chaos: true
                },
                animation: {
                    distort: { skewX: 5, skewY: 2, frequency: 3 },
                    corrupt: { filter: 'hue-rotate(270deg) saturate(1.5)' },
                    writhe: { morphPath: 'chaotic', frequency: 2 },
                    pulse: { scale: { min: 0.9, max: 1.2 }, speed: 1.5 }
                },
                facial: {
                    eyeGlow: 0.9,
                    skinPallor: 0.7,
                    veinShow: 0.5,
                    shadowDeepen: 0.8
                },
                audio: {
                    frequency: 66.6,
                    harmonics: [133.2, 199.8],
                    volume: 0.4,
                    chaos: 0.7
                }
            },
            
            divine: {
                color: { primary: '#FFD700', secondary: '#FFFFFF', accent: '#F0E68C' },
                intensity: { min: 0.6, max: 1.0, default: 0.9 },
                duration: { min: 3, max: 10, default: 6 },
                particles: {
                    type: 'divine',
                    count: { min: 20, max: 60 },
                    size: { min: 1, max: 6 },
                    velocity: { min: 40, max: 100 },
                    gravity: -0.3,
                    life: { min: 2, max: 5 },
                    holy: true
                },
                animation: {
                    ascend: { y: -15, ease: 'power2.out' },
                    illuminate: { filter: 'brightness(1.4) contrast(1.1)' },
                    sanctify: { boxShadow: '0 0 40px rgba(255,215,0,0.8)' },
                    levitate: { y: -5, frequency: 1, ease: 'sine.inOut' }
                },
                facial: {
                    eyeShine: 1.0,
                    skinGlow: 0.8,
                    serenity: 0.9,
                    halo: 0.6
                },
                audio: {
                    frequency: 528,
                    harmonics: [1056, 1584],
                    volume: 0.35,
                    reverb: 0.8
                }
            }
        };
        
        Object.entries(configs).forEach(([emotion, config]) => {
            this.emotionConfigs.set(emotion, config);
        });
        
        console.log(`🎭 Loaded ${this.emotionConfigs.size} emotion configurations`);
    }    

    /**
     * Setup particle system configurations
     */
    setupParticleConfigs() {
        const particleTypes = {
            sparkles: {
                shape: 'star',
                material: 'luminous',
                physics: 'light',
                behavior: 'twinkle'
            },
            flames: {
                shape: 'flame',
                material: 'fire',
                physics: 'heat',
                behavior: 'flicker'
            },
            wisps: {
                shape: 'wisp',
                material: 'ethereal',
                physics: 'float',
                behavior: 'drift'
            },
            chaos: {
                shape: 'irregular',
                material: 'void',
                physics: 'chaotic',
                behavior: 'corrupt'
            },
            divine: {
                shape: 'cross',
                material: 'light',
                physics: 'blessed',
                behavior: 'ascend'
            }
        };
        
        Object.entries(particleTypes).forEach(([type, config]) => {
            this.particleConfigs.set(type, config);
        });
        
        console.log(`✨ Loaded ${this.particleConfigs.size} particle configurations`);
    }
    
    /**
     * Initialize audio configurations for emotions
     */
    initializeAudioConfigs() {
        const audioTypes = {
            harmonic: {
                waveform: 'sine',
                envelope: { attack: 0.1, decay: 0.3, sustain: 0.7, release: 0.5 },
                effects: ['reverb', 'chorus']
            },
            percussive: {
                waveform: 'sawtooth',
                envelope: { attack: 0.01, decay: 0.2, sustain: 0.3, release: 0.3 },
                effects: ['distortion', 'delay']
            },
            chaotic: {
                waveform: 'noise',
                envelope: { attack: 0.0, decay: 0.1, sustain: 0.5, release: 0.8 },
                effects: ['bitcrush', 'chaos']
            }
        };
        
        Object.entries(audioTypes).forEach(([type, config]) => {
            this.audioConfigs.set(type, config);
        });
        
        console.log(`🔊 Loaded ${this.audioConfigs.size} audio configurations`);
    }
    
    /**
     * Setup emotion blending system for complex emotional states
     */
    setupEmotionBlending() {
        const blendRules = {
            'joy+anger': 'excitement',
            'anger+fear': 'rage',
            'fear+corruption': 'terror',
            'joy+divine': 'bliss',
            'corruption+anger': 'wrath'
        };
        
        Object.entries(blendRules).forEach(([combination, result]) => {
            this.emotionBlends.set(combination, result);
        });
        
        console.log(`🎨 Loaded ${this.emotionBlends.size} emotion blend rules`);
    }
    
    /**
     * Initialize advanced lighting system for emotional atmosphere
     */
    initializeLightingSystem() {
        const lightingConfigs = {
            joy: {
                ambient: { color: '#FFD700', intensity: 0.8 },
                point: { color: '#FFFF00', intensity: 0.4, radius: 100 }
            },
            anger: {
                ambient: { color: '#8B0000', intensity: 0.9 },
                point: { color: '#DC143C', intensity: 0.7, radius: 80 }
            },
            fear: {
                ambient: { color: '#4B0082', intensity: 0.3 },
                point: { color: '#9370DB', intensity: 0.2, radius: 120 }
            },
            corruption: {
                ambient: { color: '#800080', intensity: 0.7 },
                point: { color: '#8B008B', intensity: 0.8, radius: 150 }
            },
            divine: {
                ambient: { color: '#FFFFFF', intensity: 1.0 },
                point: { color: '#F0E68C', intensity: 0.6, radius: 200 }
            }
        };
        
        Object.entries(lightingConfigs).forEach(([emotion, config]) => {
            this.emotionLights.set(emotion, config);
        });
        
        console.log(`💡 Loaded ${this.emotionLights.size} lighting configurations`);
    }
    
    /**
     * Create particle pools for optimal performance
     */
    createParticlePools() {
        const poolSizes = {
            sparkles: 100,
            flames: 80,
            wisps: 60,
            chaos: 90,
            divine: 70
        };
        
        Object.entries(poolSizes).forEach(([type, size]) => {
            this.particlePool[type] = [];
            
            for (let i = 0; i < size; i++) {
                const particle = this.createParticleElement(type);
                particle.style.display = 'none';
                this.particlePool[type].push(particle);
            }
        });
        
        console.log(`🏊 Created particle pools with ${Object.values(poolSizes).reduce((a, b) => a + b, 0)} particles`);
    }    

    /**
     * Create a particle element
     */
    createParticleElement(type) {
        const particle = document.createElement('div');
        particle.className = `emotion-particle particle-${type}`;
        
        const config = this.particleConfigs.get(type);
        if (config) {
            particle.dataset.shape = config.shape;
            particle.dataset.material = config.material;
            particle.dataset.physics = config.physics;
            particle.dataset.behavior = config.behavior;
        }
        
        return particle;
    }
    
    /**
     * Trigger emotion with full GSAP animation suite
     */
    triggerEmotion(characterId, emotion, intensity = null, duration = null, options = {}) {
        if (!this.isInitialized) {
            console.warn('⚠️ EmotionSystem3D not initialized');
            return;
        }
        
        const config = this.emotionConfigs.get(emotion);
        if (!config) {
            console.warn(`⚠️ Unknown emotion: ${emotion}`);
            return;
        }
        
        // Calculate final parameters
        const finalIntensity = intensity || config.intensity.default;
        const finalDuration = duration || config.duration.default;
        
        // Get character element
        const characterElement = document.querySelector(`[data-character="${characterId}"]`);
        if (!characterElement) {
            console.warn(`⚠️ Character element not found: ${characterId}`);
            return;
        }
        
        // Create emotion instance
        const emotionInstance = {
            id: `${characterId}-${emotion}-${Date.now()}`,
            characterId,
            emotion,
            intensity: finalIntensity,
            duration: finalDuration,
            startTime: Date.now(),
            config,
            element: characterElement,
            particles: [],
            animations: [],
            audio: null
        };
        
        // Store active emotion
        this.activeEmotions.set(emotionInstance.id, emotionInstance);
        
        // Execute emotion sequence
        this.executeEmotionSequence(emotionInstance, options);
        
        // Schedule cleanup
        setTimeout(() => {
            this.endEmotion(emotionInstance.id);
        }, finalDuration * 1000);
        
        console.log(`🎭 Triggered emotion: ${emotion} for ${characterId} (intensity: ${finalIntensity}, duration: ${finalDuration}s)`);
        
        return emotionInstance.id;
    }
    
    /**
     * Execute complete emotion sequence with GSAP
     */
    executeEmotionSequence(emotionInstance, options = {}) {
        const { config, element, intensity, duration } = emotionInstance;
        
        // Create master timeline for this emotion
        const masterTL = gsap.timeline({
            onComplete: () => {
                console.log(`🎭 Emotion sequence completed: ${emotionInstance.emotion}`);
            }
        });
        
        // Phase 1: Facial animation
        const facialTL = this.createFacialAnimations(element, config.facial, intensity);
        masterTL.add(facialTL, 0);
        
        // Phase 2: Body animation
        const bodyTL = this.createBodyAnimations(element, config.animation, intensity, duration);
        masterTL.add(bodyTL, 0.1);
        
        // Phase 3: Particle effects
        const particleTL = this.createParticleEffects(emotionInstance);
        masterTL.add(particleTL, 0.2);
        
        // Phase 4: Lighting effects
        const lightingTL = this.createLightingEffects(emotionInstance);
        masterTL.add(lightingTL, 0.3);
        
        // Phase 5: Audio effects
        if (options.enableAudio !== false) {
            this.createAudioEffects(emotionInstance);
        }
        
        // Store timeline for potential interruption
        emotionInstance.masterTimeline = masterTL;
        
        return masterTL;
    }    
  
  /**
     * Create facial animations using GSAP morphing
     */
    createFacialAnimations(element, facialConfig, intensity) {
        const facialTL = gsap.timeline();
        
        // Get facial elements
        const face = element.querySelector('.character-face') || element;
        const eyes = element.querySelector('.character-eyes');
        const mouth = element.querySelector('.character-mouth');
        const brows = element.querySelector('.character-brows');
        
        // Apply facial transformations based on emotion
        Object.entries(facialConfig).forEach(([feature, value]) => {
            const adjustedValue = value * intensity;
            
            switch (feature) {
                case 'eyeScale':
                    if (eyes) {
                        facialTL.to(eyes, {
                            duration: 0.3,
                            scale: adjustedValue,
                            ease: 'power2.out'
                        }, 0);
                    }
                    break;
                    
                case 'eyeWiden':
                    if (eyes) {
                        facialTL.to(eyes, {
                            duration: 0.2,
                            scaleY: 1 + adjustedValue,
                            ease: 'back.out(1.7)'
                        }, 0);
                    }
                    break;
                    
                case 'mouthCurve':
                    if (mouth) {
                        facialTL.to(mouth, {
                            duration: 0.4,
                            rotation: adjustedValue,
                            transformOrigin: 'center center',
                            ease: 'elastic.out(1, 0.3)'
                        }, 0.1);
                    }
                    break;
                    
                case 'browFurrow':
                    if (brows) {
                        facialTL.to(brows, {
                            duration: 0.3,
                            scaleY: 1 - adjustedValue * 0.3,
                            y: adjustedValue * 5,
                            ease: 'power2.inOut'
                        }, 0);
                    }
                    break;
                    
                case 'browRaise':
                    if (brows) {
                        facialTL.to(brows, {
                            duration: 0.25,
                            y: -adjustedValue * 8,
                            ease: 'power2.out'
                        }, 0);
                    }
                    break;
            }
        });
        
        return facialTL;
    }
    
    /**
     * Create body animations with advanced GSAP features
     */
    createBodyAnimations(element, animationConfig, intensity, duration) {
        const bodyTL = gsap.timeline();
        
        Object.entries(animationConfig).forEach(([animType, config]) => {
            const adjustedConfig = this.adjustConfigForIntensity(config, intensity);
            
            switch (animType) {
                case 'shake':
                    bodyTL.to(element, {
                        duration: duration * 0.8,
                        x: `random(-${adjustedConfig.amplitude}, ${adjustedConfig.amplitude})`,
                        y: `random(-${adjustedConfig.amplitude * 0.5}, ${adjustedConfig.amplitude * 0.5})`,
                        ease: 'none',
                        repeat: adjustedConfig.frequency,
                        yoyo: true
                    }, 0);
                    break;
                    
                case 'glow':
                    bodyTL.to(element, {
                        duration: duration,
                        boxShadow: `0 0 ${adjustedConfig.radius}px ${adjustedConfig.color || adjustedConfig.intensity}`,
                        ease: 'power2.inOut',
                        repeat: adjustedConfig.pulsate ? -1 : 0,
                        yoyo: adjustedConfig.pulsate
                    }, 0);
                    break;
                    
                case 'scale':
                    bodyTL.fromTo(element, {
                        scale: adjustedConfig.from
                    }, {
                        duration: duration * 0.3,
                        scale: adjustedConfig.to,
                        ease: adjustedConfig.ease || 'power2.out'
                    }, 0);
                    break;
                    
                case 'bounce':
                    bodyTL.to(element, {
                        duration: duration / adjustedConfig.frequency,
                        y: -adjustedConfig.amplitude,
                        ease: 'power2.out',
                        repeat: adjustedConfig.frequency,
                        yoyo: true
                    }, 0);
                    break;
                    
                case 'distortion':
                    bodyTL.to(element, {
                        duration: duration / adjustedConfig.frequency,
                        skewX: adjustedConfig.skewX,
                        skewY: adjustedConfig.skewY,
                        ease: 'sine.inOut',
                        repeat: adjustedConfig.frequency,
                        yoyo: true
                    }, 0);
                    break;
                    
                case 'tremble':
                    bodyTL.to(element, {
                        duration: 0.05,
                        x: `random(-${adjustedConfig.amplitude}, ${adjustedConfig.amplitude})`,
                        y: `random(-${adjustedConfig.amplitude}, ${adjustedConfig.amplitude})`,
                        ease: 'none',
                        repeat: duration * adjustedConfig.frequency,
                        repeatRefresh: true
                    }, 0);
                    break;
            }
        });
        
        return bodyTL;
    }