/**
 * Warhammer Fantasy Tavern Simulator - Main Application Entry Point
 * Standalone Web Application with Three.js, GSAP, and Web Audio API
 */

// Import modules
import { TavernEnvironment3D } from './modules/TavernEnvironment3D.js';
import { GSAPMasterController } from './modules/GSAPMasterController.js';
import { SpatialAudioSystem } from './modules/SpatialAudioSystem.js';
import { Character3DSystem } from './modules/Character3DSystem.js';
import { RealTimeConversationEngine } from './modules/RealTimeConversationEngine.js';
import { WebSocketManager } from './modules/WebSocketManager.js';
import { PerformanceProfiler } from './modules/PerformanceProfiler.js';
import { ThemeEngine } from './modules/ThemeEngine.js';
import { UIController } from './modules/UIController.js';

/**
 * Main Application Class
 * Orchestrates all systems and manages the application lifecycle
 */
class WarhammerTavernApp {
    constructor() {
        this.isInitialized = false;
        this.isRunning = false;
        
        // Core systems
        this.tavernEnvironment = null;
        this.gsapController = null;
        this.audioSystem = null;
        this.characterSystem = null;
        this.conversationEngine = null;
        this.webSocketManager = null;
        this.performanceProfiler = null;
        this.themeEngine = null;
        this.uiController = null;
        
        // Application state
        this.appState = {
            currentTheme: 'dark-fantasy',
            isPaused: false,
            timeScale: 1.0,
            cameraMode: 'free',
            audioEnabled: true,
            performanceMode: 'auto'
        };
        
        // Configuration
        this.config = {
            webSocketUrl: this.getWebSocketUrl(),
            apiBaseUrl: this.getApiBaseUrl(),
            assetsPath: './assets/',
            enableDevTools: this.isDevelopment(),
            targetFPS: 60,
            maxParticles: 1000,
            audioSampleRate: 44100
        };
        
        // Bind methods
        this.handleResize = this.handleResize.bind(this);
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
        this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
        this.animate = this.animate.bind(this);
    }
    
    /**
     * Initialize the application
     */
    async init() {
        try {
            console.log('🏰 Initializing Warhammer Fantasy Tavern Simulator...');
            
            // Show loading screen
            this.showLoadingScreen();
            
            // Initialize core systems in order
            await this.initializeCoreSystems();
            await this.initializeAudioSystem();
            await this.initialize3DEnvironment();
            await this.initializeCharacterSystem();
            await this.initializeConversationEngine();
            await this.initializeNetworking();
            await this.initializeUI();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Load initial data
            await this.loadInitialData();
            
            // Start the application
            this.start();
            
            // Hide loading screen
            this.hideLoadingScreen();
            
            this.isInitialized = true;
            console.log('✅ Application initialized successfully!');
            
        } catch (error) {
            console.error('❌ Failed to initialize application:', error);
            this.showErrorScreen(error);
        }
    }
    
    /**
     * Initialize core systems (GSAP, Performance, Theme)
     */
    async initializeCoreSystems() {
        this.updateLoadingProgress(10, 'Initializing core systems...');
        
        // Initialize GSAP Master Controller
        this.gsapController = new GSAPMasterController();
        await this.gsapController.init();
        
        // Initialize Performance Profiler
        this.performanceProfiler = new PerformanceProfiler();
        this.performanceProfiler.init();
        
        // Initialize Theme Engine
        this.themeEngine = new ThemeEngine();
        await this.themeEngine.init();
        this.themeEngine.setTheme(this.appState.currentTheme);
        
        console.log('✅ Core systems initialized');
    }
    
    /**
     * Initialize Audio System
     */
    async initializeAudioSystem() {
        this.updateLoadingProgress(20, 'Loading audio system...');
        
        this.audioSystem = new SpatialAudioSystem();
        await this.audioSystem.init({
            sampleRate: this.config.audioSampleRate,
            enableSpatialAudio: true,
            masterVolume: 0.7
        });
        
        // Load initial audio assets
        await this.audioSystem.loadAudioAssets([
            'tavern-ambience.ogg',
            'medieval-music.ogg',
            'fire-crackling.ogg',
            'crowd-chatter.ogg'
        ]);
        
        console.log('✅ Audio system initialized');
    }
    
    /**
     * Initialize 3D Environment
     */
    async initialize3DEnvironment() {
        this.updateLoadingProgress(40, 'Creating 3D tavern environment...');
        
        const canvas = document.getElementById('webgl-canvas');
        this.tavernEnvironment = new TavernEnvironment3D(canvas);
        
        await this.tavernEnvironment.init({
            enableShadows: true,
            enablePostProcessing: true,
            antialias: true,
            pixelRatio: Math.min(window.devicePixelRatio, 2)
        });
        
        // Load 3D assets
        await this.tavernEnvironment.loadAssets([
            'tavern-interior.glb',
            'furniture-set.glb',
            'lighting-setup.json'
        ]);
        
        console.log('✅ 3D Environment initialized');
    }
    
    /**
     * Initialize Character System
     */
    async initializeCharacterSystem() {
        this.updateLoadingProgress(60, 'Loading characters...');
        
        this.characterSystem = new Character3DSystem(this.tavernEnvironment.scene);
        await this.characterSystem.init();
        
        // Load character models and animations
        await this.characterSystem.loadCharacterAssets([
            'empire-soldier.glb',
            'dwarf-warrior.glb',
            'elf-mage.glb',
            'chaos-cultist.glb',
            'tavern-keeper.glb'
        ]);
        
        console.log('✅ Character system initialized');
    }
    
    /**
     * Initialize Conversation Engine
     */
    async initializeConversationEngine() {
        this.updateLoadingProgress(70, 'Setting up conversation system...');
        
        this.conversationEngine = new RealTimeConversationEngine();
        await this.conversationEngine.init({
            webSocketManager: this.webSocketManager,
            gsapController: this.gsapController,
            maxConcurrentConversations: 3,
            typingSpeed: 50,
            bubbleLifetime: 5000
        });
        
        console.log('✅ Conversation engine initialized');
    }
    
    /**
     * Initialize Networking
     */
    async initializeNetworking() {
        this.updateLoadingProgress(80, 'Connecting to server...');
        
        this.webSocketManager = new WebSocketManager();
        await this.webSocketManager.connect(this.config.webSocketUrl);
        
        // Setup message handlers
        this.webSocketManager.on('character-update', this.handleCharacterUpdate.bind(this));
        this.webSocketManager.on('conversation-start', this.handleConversationStart.bind(this));
        this.webSocketManager.on('tavern-event', this.handleTavernEvent.bind(this));
        
        console.log('✅ Networking initialized');
    }
    
    /**
     * Initialize UI Controller
     */
    async initializeUI() {
        this.updateLoadingProgress(90, 'Setting up user interface...');
        
        this.uiController = new UIController();
        await this.uiController.init({
            gsapController: this.gsapController,
            audioSystem: this.audioSystem,
            themeEngine: this.themeEngine
        });
        
        // Setup UI event handlers
        this.uiController.on('settings-changed', this.handleSettingsChanged.bind(this));
        this.uiController.on('action-triggered', this.handleActionTriggered.bind(this));
        
        console.log('✅ UI initialized');
    }
    
    /**
     * Load initial data from server
     */
    async loadInitialData() {
        this.updateLoadingProgress(95, 'Loading tavern data...');
        
        try {
            // Request initial tavern state
            const tavernData = await this.webSocketManager.request('get-tavern-state');
            
            // Populate characters
            if (tavernData.characters) {
                await this.characterSystem.spawnCharacters(tavernData.characters);
            }
            
            // Set tavern properties
            if (tavernData.tavern) {
                this.updateTavernInfo(tavernData.tavern);
            }
            
        } catch (error) {
            console.warn('⚠️ Could not load initial data, using defaults:', error);
            await this.loadDefaultData();
        }
    }
    
    /**
     * Load default data when server is unavailable
     */
    async loadDefaultData() {
        const defaultCharacters = [
            { id: 'karczmarz', name: 'Karczmarz', faction: 'empire', role: 'Tavern Keeper' },
            { id: 'skrytobojca', name: 'Skrytobójca', faction: 'chaos', role: 'Shadow Agent' },
            { id: 'wiedzma', name: 'Wiedźma', faction: 'undead', role: 'Witch' },
            { id: 'zwiadowca', name: 'Zwiadowca', faction: 'elf', role: 'Scout' },
            { id: 'czempion', name: 'Czempion', faction: 'empire', role: 'Champion' }
        ];
        
        await this.characterSystem.spawnCharacters(defaultCharacters);
        
        this.updateTavernInfo({
            name: 'The Prancing Pony',
            reputation: 75,
            tension: 25,
            wealth: 1250
        });
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Window events
        window.addEventListener('resize', this.handleResize);
        window.addEventListener('beforeunload', this.handleBeforeUnload);
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
        
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Performance monitoring
        if (this.config.enableDevTools) {
            this.setupDevTools();
        }
    }
    
    /**
     * Start the application main loop
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        
        // Start audio ambience
        if (this.appState.audioEnabled) {
            this.audioSystem.playAmbience('tavern-ambience');
            this.audioSystem.playMusic('medieval-music', { loop: true, volume: 0.3 });
        }
        
        // Start animation loop
        this.animate();
        
        // Start conversation system
        this.conversationEngine.start();
        
        console.log('🚀 Application started!');
    }
    
    /**
     * Main animation loop
     */
    animate() {
        if (!this.isRunning) return;
        
        // Update performance profiler
        this.performanceProfiler.beginFrame();
        
        // Update systems
        if (!this.appState.isPaused) {
            const deltaTime = this.performanceProfiler.getDeltaTime() * this.appState.timeScale;
            
            this.tavernEnvironment.update(deltaTime);
            this.characterSystem.update(deltaTime);
            this.conversationEngine.update(deltaTime);
            this.audioSystem.update(deltaTime);
        }
        
        // Render
        this.tavernEnvironment.render();
        
        // Update UI
        this.uiController.update();
        
        // End performance measurement
        this.performanceProfiler.endFrame();
        
        // Continue loop
        requestAnimationFrame(this.animate);
    }
    
    /**
     * Event Handlers
     */
    
    handleResize() {
        if (this.tavernEnvironment) {
            this.tavernEnvironment.handleResize();
        }
        if (this.uiController) {
            this.uiController.handleResize();
        }
    }
    
    handleVisibilityChange() {
        if (document.hidden) {
            this.pause();
        } else {
            this.resume();
        }
    }
    
    handleBeforeUnload(event) {
        if (this.webSocketManager) {
            this.webSocketManager.disconnect();
        }
    }
    
    handleKeyDown(event) {
        // Keyboard shortcuts
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.togglePause();
                break;
            case 'KeyF':
                if (event.ctrlKey) {
                    event.preventDefault();
                    this.toggleFullscreen();
                }
                break;
            case 'KeyM':
                if (event.ctrlKey) {
                    event.preventDefault();
                    this.toggleAudio();
                }
                break;
            case 'F11':
                event.preventDefault();
                this.toggleFullscreen();
                break;
        }
    }
    
    handleCharacterUpdate(data) {
        if (this.characterSystem) {
            this.characterSystem.updateCharacter(data.characterId, data.updates);
        }
    }
    
    handleConversationStart(data) {
        if (this.conversationEngine) {
            this.conversationEngine.startConversation(data);
        }
    }
    
    handleTavernEvent(data) {
        console.log('🎭 Tavern event:', data);
        
        // Handle different event types
        switch (data.type) {
            case 'brawl':
                this.triggerBrawlEvent(data);
                break;
            case 'celebration':
                this.triggerCelebrationEvent(data);
                break;
            case 'mysterious_visitor':
                this.triggerMysteriousVisitor(data);
                break;
        }
    }
    
    handleSettingsChanged(settings) {
        // Apply settings changes
        if (settings.theme && settings.theme !== this.appState.currentTheme) {
            this.themeEngine.setTheme(settings.theme);
            this.appState.currentTheme = settings.theme;
        }
        
        if (settings.audioEnabled !== undefined) {
            this.appState.audioEnabled = settings.audioEnabled;
            if (settings.audioEnabled) {
                this.audioSystem.resume();
            } else {
                this.audioSystem.pause();
            }
        }
        
        if (settings.performanceMode) {
            this.setPerformanceMode(settings.performanceMode);
        }
    }
    
    handleActionTriggered(action) {
        switch (action.type) {
            case 'generate-event':
                this.generateRandomEvent();
                break;
            case 'trigger-conversation':
                this.triggerRandomConversation();
                break;
            case 'trigger-brawl':
                this.triggerBrawl();
                break;
            case 'reset-camera':
                this.tavernEnvironment.resetCamera();
                break;
        }
    }
    
    /**
     * Application Control Methods
     */
    
    pause() {
        this.appState.isPaused = true;
        this.audioSystem.pause();
        console.log('⏸️ Application paused');
    }
    
    resume() {
        this.appState.isPaused = false;
        if (this.appState.audioEnabled) {
            this.audioSystem.resume();
        }
        console.log('▶️ Application resumed');
    }
    
    togglePause() {
        if (this.appState.isPaused) {
            this.resume();
        } else {
            this.pause();
        }
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }
    
    toggleAudio() {
        this.appState.audioEnabled = !this.appState.audioEnabled;
        if (this.appState.audioEnabled) {
            this.audioSystem.resume();
        } else {
            this.audioSystem.pause();
        }
        this.uiController.updateAudioButton(this.appState.audioEnabled);
    }
    
    setTimeScale(scale) {
        this.appState.timeScale = Math.max(0.1, Math.min(5.0, scale));
        console.log(`⏩ Time scale set to ${this.appState.timeScale}x`);
    }
    
    setPerformanceMode(mode) {
        this.appState.performanceMode = mode;
        
        switch (mode) {
            case 'ultra':
                this.tavernEnvironment.setQuality('ultra');
                this.characterSystem.setLOD('high');
                break;
            case 'high':
                this.tavernEnvironment.setQuality('high');
                this.characterSystem.setLOD('medium');
                break;
            case 'medium':
                this.tavernEnvironment.setQuality('medium');
                this.characterSystem.setLOD('low');
                break;
            case 'low':
                this.tavernEnvironment.setQuality('low');
                this.characterSystem.setLOD('minimal');
                break;
        }
    }
    
    /**
     * Game Event Methods
     */
    
    async generateRandomEvent() {
        try {
            const event = await this.webSocketManager.request('generate-event');
            this.handleTavernEvent(event);
        } catch (error) {
            console.warn('Could not generate server event, using local event');
            this.generateLocalEvent();
        }
    }
    
    generateLocalEvent() {
        const events = [
            { type: 'celebration', description: 'A merchant announces successful trade!' },
            { type: 'mysterious_visitor', description: 'A hooded figure enters the tavern...' },
            { type: 'brawl', description: 'Tensions rise between patrons!' }
        ];
        
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        this.handleTavernEvent(randomEvent);
    }
    
    triggerRandomConversation() {
        const characters = this.characterSystem.getActiveCharacters();
        if (characters.length >= 2) {
            const speaker = characters[Math.floor(Math.random() * characters.length)];
            const listener = characters.filter(c => c.id !== speaker.id)[0];
            
            this.conversationEngine.startConversation({
                speaker: speaker.id,
                listener: listener.id,
                content: this.generateRandomDialogue(speaker, listener)
            });
        }
    }
    
    triggerBrawl() {
        console.log('⚔️ Triggering tavern brawl!');
        
        // Visual effects
        this.gsapController.triggerBrawlAnimation();
        
        // Audio effects
        this.audioSystem.playSound('brawl-start', { volume: 0.8 });
        
        // Character animations
        this.characterSystem.triggerBrawlAnimations();
        
        // Update tension
        this.updateTensionLevel(Math.min(100, this.getCurrentTension() + 30));
    }
    
    triggerBrawlEvent(data) {
        this.triggerBrawl();
    }
    
    triggerCelebrationEvent(data) {
        console.log('🎉 Celebration event!');
        
        // Celebration effects
        this.gsapController.triggerCelebrationAnimation();
        this.audioSystem.playSound('celebration', { volume: 0.6 });
        
        // Reduce tension
        this.updateTensionLevel(Math.max(0, this.getCurrentTension() - 20));
    }
    
    triggerMysteriousVisitor(data) {
        console.log('🕵️ Mysterious visitor arrives!');
        
        // Spawn mysterious character
        this.characterSystem.spawnTemporaryCharacter({
            id: 'mysterious_visitor',
            name: 'Hooded Stranger',
            faction: 'unknown',
            temporary: true
        });
        
        // Atmospheric effects
        this.gsapController.triggerMysteriousEffects();
        this.audioSystem.playSound('mysterious-entrance', { volume: 0.5 });
    }
    
    /**
     * UI Update Methods
     */
    
    updateTavernInfo(tavernData) {
        if (tavernData.name) {
            document.getElementById('tavern-name').textContent = tavernData.name;
        }
        
        if (tavernData.reputation !== undefined) {
            this.updateReputationLevel(tavernData.reputation);
        }
        
        if (tavernData.tension !== undefined) {
            this.updateTensionLevel(tavernData.tension);
        }
        
        if (tavernData.wealth !== undefined) {
            this.updateWealthLevel(tavernData.wealth);
        }
    }
    
    updateReputationLevel(level) {
        const fill = document.getElementById('reputation-fill');
        const value = document.getElementById('reputation-value');
        
        if (fill && value) {
            this.gsapController.animateStatBar(fill, level);
            value.textContent = Math.round(level);
        }
    }
    
    updateTensionLevel(level) {
        const fill = document.getElementById('tension-fill');
        const value = document.getElementById('tension-value');
        
        if (fill && value) {
            this.gsapController.animateStatBar(fill, level);
            value.textContent = Math.round(level);
        }
    }
    
    updateWealthLevel(amount) {
        const value = document.getElementById('wealth-value');
        if (value) {
            this.gsapController.animateNumber(value, amount);
        }
    }
    
    getCurrentTension() {
        const value = document.getElementById('tension-value');
        return value ? parseInt(value.textContent) : 0;
    }
    
    /**
     * Utility Methods
     */
    
    generateRandomDialogue(speaker, listener) {
        const dialogues = [
            `Greetings, ${listener.name}. How fares your journey?`,
            `The roads have been dangerous lately, ${listener.name}.`,
            `Have you heard the latest news from the capital?`,
            `This ale tastes better than usual tonight.`,
            `I've been hearing strange rumors about the forest...`
        ];
        
        return dialogues[Math.floor(Math.random() * dialogues.length)];
    }
    
    getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws`;
    }
    
    getApiBaseUrl() {
        return `${window.location.protocol}//${window.location.host}/api`;
    }
    
    isDevelopment() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.search.includes('debug=true');
    }
    
    /**
     * Loading Screen Methods
     */
    
    showLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.remove('hidden');
        }
    }
    
    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            this.gsapController.fadeOut(loadingScreen, 1.0).then(() => {
                loadingScreen.classList.add('hidden');
            });
        }
    }
    
    updateLoadingProgress(percentage, text) {
        const progressBar = document.getElementById('loading-progress');
        const loadingText = document.getElementById('loading-text');
        
        if (progressBar) {
            this.gsapController.animateWidth(progressBar, `${percentage}%`);
        }
        
        if (loadingText && text) {
            loadingText.textContent = text;
        }
    }
    
    showErrorScreen(error) {
        const loadingText = document.getElementById('loading-text');
        if (loadingText) {
            loadingText.textContent = `Error: ${error.message}`;
            loadingText.style.color = '#ff4444';
        }
    }
    
    /**
     * Development Tools
     */
    
    setupDevTools() {
        // Show performance monitor
        const perfMonitor = document.getElementById('performance-monitor');
        if (perfMonitor) {
            perfMonitor.classList.remove('hidden');
        }
        
        // Setup performance monitoring
        setInterval(() => {
            const fps = this.performanceProfiler.getFPS();
            const memory = this.performanceProfiler.getMemoryUsage();
            const triangles = this.tavernEnvironment.getTriangleCount();
            
            document.getElementById('fps-counter').textContent = Math.round(fps);
            document.getElementById('memory-counter').textContent = `${Math.round(memory)} MB`;
            document.getElementById('triangles-counter').textContent = triangles.toLocaleString();
        }, 1000);
        
        // Add to global scope for debugging
        window.tavernApp = this;
        
        console.log('🔧 Development tools enabled');
        console.log('Access app instance via window.tavernApp');
    }
}

/**
 * Application Entry Point
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🏰 Starting Warhammer Fantasy Tavern Simulator...');
    
    // Create and initialize application
    const app = new WarhammerTavernApp();
    await app.init();
    
    // Make app globally accessible
    window.app = app;
});

// Handle unhandled errors
window.addEventListener('error', (event) => {
    console.error('💥 Unhandled error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('💥 Unhandled promise rejection:', event.reason);
});

export default WarhammerTavernApp;