/**
 * GSAP Master Controller - 200% Utilization for Warhammer Fantasy
 * Manages all animations with advanced GSAP features and custom easing
 */

export class GSAPMasterController {
    constructor() {
        this.masterTimeline = null;
        this.activeAnimations = new Map();
        this.customEases = new Map();
        this.isInitialized = false;
        
        // Animation queues by priority
        this.animationQueues = {
            critical: [],
            high: [],
            medium: [],
            low: []
        };
        
        // Performance settings
        this.performanceMode = 'ultra';
        this.maxConcurrentAnimations = 50;
        this.frameRate = 60;
    }
    
    /**
     * Initialize GSAP with all plugins and custom settings
     */
    async init() {
        try {
            // Register all GSAP plugins
            gsap.registerPlugin(
                ScrollTrigger,
                TextPlugin,
                MorphSVGPlugin,
                DrawSVGPlugin,
                PixiPlugin,
                Flip,
                CustomEase,
                Draggable,
                MotionPathPlugin
            );
            
            // Configure GSAP for maximum performance
            gsap.config({
                force3D: true,
                nullTargetWarn: false,
                trialWarn: false,
                autoSleep: 60
            });
            
            // Set global defaults
            gsap.defaults({
                duration: 0.6,
                ease: "power2.out"
            });
            
            // Set optimal frame rate
            gsap.ticker.fps(this.frameRate);
            
            // Create custom eases for Warhammer atmosphere
            this.createCustomEases();
            
            // Create master timeline
            this.masterTimeline = gsap.timeline({
                paused: true,
                onComplete: () => console.log('🎭 Master timeline completed')
            });
            
            // Start animation processing loop
            this.startAnimationLoop();
            
            this.isInitialized = true;
            console.log('✅ GSAP Master Controller initialized with 200% utilization');
            
        } catch (error) {
            console.error('❌ Failed to initialize GSAP Master Controller:', error);
            throw error;
        }
    }
    
    /**
     * Create custom easing functions for Warhammer Fantasy atmosphere
     */
    createCustomEases() {
        // Tavern atmosphere easing
        CustomEase.create("tavernEase", "M0,0 C0.25,0.46 0.45,0.94 1,1");
        this.customEases.set('tavern', 'tavernEase');
        
        // Chaos corruption easing
        CustomEase.create("chaosEase", "M0,0 C0.68,-0.55 0.265,1.55 1,1");
        this.customEases.set('chaos', 'chaosEase');
        
        // Imperial march easing
        CustomEase.create("imperialEase", "M0,0 C0.175,0.885 0.32,1.275 1,1");
        this.customEases.set('imperial', 'imperialEase');
        
        // Elven grace easing
        CustomEase.create("elvenEase", "M0,0 C0.4,0 0.6,1 1,1");
        this.customEases.set('elven', 'elvenEase');
        
        // Dwarven sturdy easing
        CustomEase.create("dwarvenEase", "M0,0 C0.1,0.9 0.2,1 1,1");
        this.customEases.set('dwarven', 'dwarvenEase');
        
        // Brawl impact easing
        CustomEase.create("brawlEase", "M0,0 C0.9,0.1 0.1,0.9 1,1");
        this.customEases.set('brawl', 'brawlEase');
        
        console.log('🎨 Custom Warhammer eases created');
    }
    
    /**
     * Start the animation processing loop
     */
    startAnimationLoop() {
        const processAnimations = () => {
            this.processAnimationQueues();
            requestAnimationFrame(processAnimations);
        };
        
        processAnimations();
    }
    
    /**
     * Process animation queues by priority
     */
    processAnimationQueues() {
        const priorities = ['critical', 'high', 'medium', 'low'];
        
        for (const priority of priorities) {
            const queue = this.animationQueues[priority];
            
            while (queue.length > 0 && this.activeAnimations.size < this.maxConcurrentAnimations) {
                const animation = queue.shift();
                this.executeAnimation(animation);
            }
        }
    }
    
    /**
     * Execute a single animation
     */
    executeAnimation(animationConfig) {
        const { id, target, properties, options = {} } = animationConfig;
        
        // Add to active animations
        const animation = gsap.to(target, {
            ...properties,
            ...options,
            onComplete: () => {
                this.activeAnimations.delete(id);
                if (options.onComplete) options.onComplete();
            }
        });
        
        this.activeAnimations.set(id, animation);
        return animation;
    }
    
    /**
     * Character entrance animation with faction-specific effects
     */
    animateCharacterEntrance(character, delay = 0) {
        const characterElement = document.querySelector(`[data-character="${character.id}"]`);
        if (!characterElement) return;
        
        const factionEase = this.customEases.get(character.faction) || 'power2.out';
        
        // Create entrance timeline
        const entranceTL = gsap.timeline({ delay });
        
        // Initial state
        gsap.set(characterElement, {
            x: -200,
            y: gsap.utils.random(-50, 50),
            opacity: 0,
            scale: 0.3,
            rotation: gsap.utils.random(-45, 45)
        });
        
        // Entrance animation
        entranceTL
            .to(characterElement, {
                duration: 1.5,
                x: 0,
                y: 0,
                opacity: 1,
                scale: 1,
                rotation: 0,
                ease: factionEase,
                force3D: true
            })
            .to(characterElement.querySelector('.character-symbol'), {
                duration: 0.8,
                scale: 1.2,
                rotation: 360,
                ease: "elastic.out(1, 0.5)",
                yoyo: true,
                repeat: 1
            }, "-=0.5");
        
        // Add faction-specific effects
        this.addFactionEffects(characterElement, character.faction);
        
        return entranceTL;
    }
    
    /**
     * Add faction-specific visual effects
     */
    addFactionEffects(element, faction) {
        switch (faction) {
            case 'chaos':
                this.addChaosEffects(element);
                break;
            case 'empire':
                this.addImperialEffects(element);
                break;
            case 'elf':
                this.addElvenEffects(element);
                break;
            case 'dwarf':
                this.addDwarvenEffects(element);
                break;
        }
    }
    
    /**
     * Chaos corruption effects
     */
    addChaosEffects(element) {
        // Pulsing red glow
        gsap.to(element, {
            duration: 2,
            boxShadow: "0 0 30px rgba(139, 0, 0, 0.8)",
            ease: "power2.inOut",
            repeat: -1,
            yoyo: true
        });
        
        // Subtle distortion
        gsap.to(element, {
            duration: 3,
            skewX: gsap.utils.random(-2, 2),
            skewY: gsap.utils.random(-1, 1),
            ease: "chaosEase",
            repeat: -1,
            yoyo: true
        });
    }
    
    /**
     * Imperial golden effects
     */
    addImperialEffects(element) {
        // Golden glow
        gsap.to(element, {
            duration: 3,
            boxShadow: "0 0 20px rgba(255, 215, 0, 0.6)",
            ease: "power2.inOut",
            repeat: -1,
            yoyo: true
        });
    }
    
    /**
     * Elven graceful effects
     */
    addElvenEffects(element) {
        // Gentle floating
        gsap.to(element, {
            duration: 4,
            y: -10,
            ease: "elvenEase",
            repeat: -1,
            yoyo: true
        });
        
        // Shimmer effect
        gsap.to(element, {
            duration: 2,
            filter: "brightness(1.2)",
            ease: "sine.inOut",
            repeat: -1,
            yoyo: true
        });
    }
    
    /**
     * Dwarven sturdy effects
     */
    addDwarvenEffects(element) {
        // Solid, grounded feel
        gsap.to(element, {
            duration: 5,
            scaleY: 1.02,
            ease: "dwarvenEase",
            repeat: -1,
            yoyo: true
        });
    }
    
    /**
     * Conversation bubble animation
     */
    animateConversationBubble(bubbleElement, content, options = {}) {
        const {
            typingSpeed = 50,
            showDuration = 4000,
            faction = 'neutral'
        } = options;
        
        // Initial state
        gsap.set(bubbleElement, {
            opacity: 0,
            scale: 0.5,
            y: 30
        });
        
        // Entrance animation
        const bubbleTL = gsap.timeline();
        
        bubbleTL
            .to(bubbleElement, {
                duration: 0.4,
                opacity: 1,
                scale: 1,
                y: 0,
                ease: "back.out(1.7)"
            })
            .call(() => {
                this.typeText(bubbleElement.querySelector('.bubble-content'), content, typingSpeed);
            })
            .to(bubbleElement, {
                duration: 0.3,
                opacity: 0,
                scale: 0.8,
                y: -20,
                ease: "power2.in",
                delay: showDuration / 1000
            });
        
        return bubbleTL;
    }
    
    /**
     * Typewriter text effect
     */
    typeText(element, text, speed = 50) {
        element.textContent = '';
        
        gsap.to(element, {
            duration: text.length / speed,
            text: {
                value: text,
                delimiter: ""
            },
            ease: "none"
        });
    }
    
    /**
     * Brawl animation sequence
     */
    triggerBrawlAnimation() {
        const tavernContainer = document.getElementById('app');
        const characters = document.querySelectorAll('.character-card');
        
        // Create brawl timeline
        const brawlTL = gsap.timeline();
        
        // Phase 1: Tension build-up
        brawlTL
            .to(characters, {
                duration: 0.5,
                scale: 1.1,
                ease: "power2.inOut",
                stagger: 0.1
            })
            // Phase 2: Explosive shake
            .to(tavernContainer, {
                duration: 3,
                x: "random(-20, 20)",
                y: "random(-15, 15)",
                ease: "brawlEase",
                repeat: 8,
                yoyo: true
            }, "-=0.2")
            // Phase 3: Character scatter
            .to(characters, {
                duration: 1.5,
                x: "random(-50, 50)",
                y: "random(-30, 30)",
                rotation: "random(-45, 45)",
                scale: "random(0.8, 1.3)",
                ease: "power3.out",
                stagger: {
                    amount: 1,
                    from: "random"
                }
            }, "-=2")
            // Phase 4: Screen flash
            .to(tavernContainer, {
                duration: 0.1,
                filter: "brightness(2) contrast(1.5)",
                repeat: 3,
                yoyo: true,
                ease: "power2.inOut"
            }, "-=1")
            // Phase 5: Recovery
            .to(tavernContainer, {
                duration: 1,
                x: 0,
                y: 0,
                filter: "brightness(1) contrast(1)",
                ease: "elastic.out(1, 0.3)"
            })
            .to(characters, {
                duration: 2,
                x: 0,
                y: 0,
                rotation: 0,
                scale: 1,
                ease: "back.out(1.7)",
                stagger: 0.1
            }, "-=0.5");
        
        // Add particle effects
        this.createBrawlParticles();
        
        return brawlTL;
    }
    
    /**
     * Create particle effects for brawl
     */
    createBrawlParticles() {
        const container = document.getElementById('app');
        const particleCount = 30;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'brawl-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: hsl(${gsap.utils.random(0, 60)}, 80%, 60%);
                border-radius: 50%;
                left: 50%;
                top: 50%;
                pointer-events: none;
                z-index: 1000;
            `;
            
            container.appendChild(particle);
            
            gsap.to(particle, {
                duration: gsap.utils.random(1, 2.5),
                x: gsap.utils.random(-300, 300),
                y: gsap.utils.random(-250, 250),
                opacity: 0,
                scale: gsap.utils.random(0.5, 2),
                rotation: gsap.utils.random(-360, 360),
                ease: "power2.out",
                delay: gsap.utils.random(0, 0.5),
                onComplete: () => particle.remove()
            });
        }
    }
    
    /**
     * Celebration animation
     */
    triggerCelebrationAnimation() {
        const characters = document.querySelectorAll('.character-card');
        
        // Celebration timeline
        const celebrationTL = gsap.timeline();
        
        celebrationTL
            .to(characters, {
                duration: 0.6,
                y: -20,
                ease: "power2.out",
                stagger: 0.1
            })
            .to(characters, {
                duration: 0.4,
                y: 0,
                ease: "bounce.out",
                stagger: 0.1
            }, "-=0.3");
        
        // Add celebration particles
        this.createCelebrationParticles();
        
        return celebrationTL;
    }
    
    /**
     * Create celebration particles
     */
    createCelebrationParticles() {
        const container = document.getElementById('app');
        const colors = ['#ffd700', '#ff6b35', '#4CAF50', '#2196F3'];
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                left: ${gsap.utils.random(20, 80)}%;
                top: 100%;
                pointer-events: none;
                z-index: 1000;
            `;
            
            container.appendChild(particle);
            
            gsap.to(particle, {
                duration: gsap.utils.random(2, 4),
                y: -window.innerHeight,
                x: gsap.utils.random(-100, 100),
                rotation: gsap.utils.random(-360, 360),
                opacity: 0,
                ease: "power2.out",
                delay: gsap.utils.random(0, 1),
                onComplete: () => particle.remove()
            });
        }
    }
    
    /**
     * Mysterious effects for special events
     */
    triggerMysteriousEffects() {
        const app = document.getElementById('app');
        
        // Dim the environment
        gsap.to(app, {
            duration: 2,
            filter: "brightness(0.7) contrast(1.2) saturate(0.8)",
            ease: "power2.inOut"
        });
        
        // Add mysterious fog particles
        this.createMysteriousFog();
        
        // Restore after 10 seconds
        gsap.to(app, {
            duration: 3,
            filter: "brightness(1) contrast(1) saturate(1)",
            ease: "power2.inOut",
            delay: 10
        });
    }
    
    /**
     * Create mysterious fog effect
     */
    createMysteriousFog() {
        const container = document.getElementById('app');
        
        for (let i = 0; i < 10; i++) {
            const fog = document.createElement('div');
            fog.style.cssText = `
                position: absolute;
                width: 100px;
                height: 100px;
                background: radial-gradient(circle, rgba(200,200,200,0.2) 0%, transparent 70%);
                border-radius: 50%;
                left: ${gsap.utils.random(0, 100)}%;
                top: ${gsap.utils.random(0, 100)}%;
                pointer-events: none;
                z-index: 5;
            `;
            
            container.appendChild(fog);
            
            gsap.fromTo(fog, {
                opacity: 0,
                scale: 0.5
            }, {
                duration: gsap.utils.random(3, 6),
                opacity: 0.6,
                scale: gsap.utils.random(1, 2),
                x: gsap.utils.random(-50, 50),
                y: gsap.utils.random(-30, 30),
                ease: "sine.inOut",
                repeat: -1,
                yoyo: true,
                onComplete: () => fog.remove()
            });
            
            // Remove after 15 seconds
            setTimeout(() => {
                gsap.to(fog, {
                    duration: 2,
                    opacity: 0,
                    onComplete: () => fog.remove()
                });
            }, 15000);
        }
    }
    
    /**
     * Animate stat bars
     */
    animateStatBar(element, percentage) {
        return gsap.to(element, {
            duration: 1,
            width: `${percentage}%`,
            ease: "power2.out"
        });
    }
    
    /**
     * Animate number counters
     */
    animateNumber(element, targetValue) {
        const currentValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
        
        return gsap.to({ value: currentValue }, {
            duration: 1,
            value: targetValue,
            ease: "power2.out",
            onUpdate: function() {
                element.textContent = Math.round(this.targets()[0].value).toLocaleString();
            }
        });
    }
    
    /**
     * Fade out animation
     */
    fadeOut(element, duration = 0.5) {
        return gsap.to(element, {
            duration,
            opacity: 0,
            ease: "power2.out"
        });
    }
    
    /**
     * Animate width
     */
    animateWidth(element, width) {
        return gsap.to(element, {
            duration: 0.8,
            width: width,
            ease: "power2.out"
        });
    }
    
    /**
     * Kill all animations
     */
    killAll() {
        gsap.killTweensOf("*");
        this.activeAnimations.clear();
        
        // Clear all queues
        Object.keys(this.animationQueues).forEach(key => {
            this.animationQueues[key] = [];
        });
    }
    
    /**
     * Set performance mode
     */
    setPerformanceMode(mode) {
        this.performanceMode = mode;
        
        switch (mode) {
            case 'ultra':
                this.maxConcurrentAnimations = 50;
                this.frameRate = 60;
                break;
            case 'high':
                this.maxConcurrentAnimations = 30;
                this.frameRate = 60;
                break;
            case 'medium':
                this.maxConcurrentAnimations = 20;
                this.frameRate = 30;
                break;
            case 'low':
                this.maxConcurrentAnimations = 10;
                this.frameRate = 30;
                break;
        }
        
        gsap.ticker.fps(this.frameRate);
    }
}