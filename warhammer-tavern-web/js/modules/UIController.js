/**
 * UI Controller - Manages all user interface interactions and updates
 * Handles settings, controls, and UI state management
 */

export class UIController {
    constructor() {
        this.isInitialized = false;
        this.gsapController = null;
        this.audioSystem = null;
        this.themeEngine = null;
        
        // UI state
        this.uiState = {
            settingsPanelOpen: false,
            characterPanelCollapsed: false,
            fullscreen: false,
            audioEnabled: true,
            currentSpeed: 1.0
        };
        
        // Event listeners
        this.eventListeners = new Map();
        this.eventEmitter = new EventTarget();
        
        // UI elements cache
        this.elements = new Map();
    }
    
    /**
     * Initialize UI Controller
     */
    async init(dependencies = {}) {
        try {
            this.gsapController = dependencies.gsapController;
            this.audioSystem = dependencies.audioSystem;
            this.themeEngine = dependencies.themeEngine;
            
            // Cache UI elements
            this.cacheUIElements();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize UI state
            this.initializeUIState();
            
            // Setup keyboard shortcuts
            this.setupKeyboardShortcuts();
            
            this.isInitialized = true;
            console.log('✅ UI Controller initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize UI Controller:', error);
            throw error;
        }
    }
    
    /**
     * Cache frequently used UI elements
     */
    cacheUIElements() {
        const elementIds = [
            'settings-btn',
            'settings-panel',
            'settings-close',
            'fullscreen-btn',
            'audio-toggle',
            'character-panel',
            'character-panel-toggle',
            'generate-event',
            'trigger-conversation',
            'trigger-brawl',
            'pause-btn',
            'speed-btn',
            'camera-reset',
            'camera-follow',
            'theme-select',
            'quality-select',
            'master-volume',
            'music-volume',
            'sfx-volume',
            'camera-sensitivity'
        ];
        
        elementIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                this.elements.set(id, element);
            }
        });
        
        console.log(`📋 Cached ${this.elements.size} UI elements`);
    }
    
    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Settings panel
        this.addEventListenerSafe('settings-btn', 'click', () => this.toggleSettingsPanel());
        this.addEventListenerSafe('settings-close', 'click', () => this.closeSettingsPanel());
        
        // Top controls
        this.addEventListenerSafe('fullscreen-btn', 'click', () => this.toggleFullscreen());
        this.addEventListenerSafe('audio-toggle', 'click', () => this.toggleAudio());
        
        // Character panel
        this.addEventListenerSafe('character-panel-toggle', 'click', () => this.toggleCharacterPanel());
        
        // Action buttons
        this.addEventListenerSafe('generate-event', 'click', () => this.emitAction('generate-event'));
        this.addEventListenerSafe('trigger-conversation', 'click', () => this.emitAction('trigger-conversation'));
        this.addEventListenerSafe('trigger-brawl', 'click', () => this.emitAction('trigger-brawl'));
        
        // Time controls
        this.addEventListenerSafe('pause-btn', 'click', () => this.togglePause());
        this.addEventListenerSafe('speed-btn', 'click', () => this.cycleSpeed());
        
        // Camera controls
        this.addEventListenerSafe('camera-reset', 'click', () => this.emitAction('reset-camera'));
        this.addEventListenerSafe('camera-follow', 'click', () => this.toggleCameraFollow());
        
        // Settings controls
        this.setupSettingsListeners();
        
        // Window events
        window.addEventListener('resize', () => this.handleResize());
        document.addEventListener('fullscreenchange', () => this.handleFullscreenChange());
        
        console.log('🎮 Event listeners setup complete');
    }
    
    /**
     * Setup settings panel listeners
     */
    setupSettingsListeners() {
        // Theme selection
        this.addEventListenerSafe('theme-select', 'change', (e) => {
            this.emitSettingsChange({ theme: e.target.value });
        });
        
        // Quality selection
        this.addEventListenerSafe('quality-select', 'change', (e) => {
            this.emitSettingsChange({ performanceMode: e.target.value });
        });
        
        // Volume controls
        this.addEventListenerSafe('master-volume', 'input', (e) => {
            const volume = parseInt(e.target.value) / 100;
            this.updateVolumeDisplay(e.target, volume);
            this.emitSettingsChange({ masterVolume: volume });
        });
        
        this.addEventListenerSafe('music-volume', 'input', (e) => {
            const volume = parseInt(e.target.value) / 100;
            this.updateVolumeDisplay(e.target, volume);
            this.emitSettingsChange({ musicVolume: volume });
        });
        
        this.addEventListenerSafe('sfx-volume', 'input', (e) => {
            const volume = parseInt(e.target.value) / 100;
            this.updateVolumeDisplay(e.target, volume);
            this.emitSettingsChange({ sfxVolume: volume });
        });
        
        // Camera sensitivity
        this.addEventListenerSafe('camera-sensitivity', 'input', (e) => {
            const sensitivity = parseFloat(e.target.value);
            this.updateSensitivityDisplay(e.target, sensitivity);
            this.emitSettingsChange({ cameraSensitivity: sensitivity });
        });
        
        // Checkboxes
        const checkboxes = [
            'particles-toggle',
            'animations-toggle',
            'spatial-audio',
            'auto-camera',
            'reduced-motion'
        ];
        
        checkboxes.forEach(id => {
            this.addEventListenerSafe(id, 'change', (e) => {
                const setting = {};
                setting[this.camelCase(id.replace('-toggle', '').replace('-', '_'))] = e.target.checked;
                this.emitSettingsChange(setting);
            });
        });
        
        // Settings buttons
        this.addEventListenerSafe('settings-reset', 'click', () => this.resetSettings());
        this.addEventListenerSafe('settings-apply', 'click', () => this.applySettings());
    }
    
    /**
     * Add event listener with error handling
     */
    addEventListenerSafe(elementId, event, handler) {
        const element = this.elements.get(elementId);
        if (element) {
            element.addEventListener(event, handler);
            
            // Store for cleanup
            if (!this.eventListeners.has(elementId)) {
                this.eventListeners.set(elementId, []);
            }
            this.eventListeners.get(elementId).push({ event, handler });
        } else {
            console.warn(`⚠️ Element not found: ${elementId}`);
        }
    }
    
    /**
     * Initialize UI state
     */
    initializeUIState() {
        // Load saved settings from localStorage
        const savedSettings = this.loadSettings();
        
        // Apply saved settings to UI
        if (savedSettings.theme) {
            const themeSelect = this.elements.get('theme-select');
            if (themeSelect) themeSelect.value = savedSettings.theme;
        }
        
        if (savedSettings.quality) {
            const qualitySelect = this.elements.get('quality-select');
            if (qualitySelect) qualitySelect.value = savedSettings.quality;
        }
        
        // Set volume sliders
        this.setVolumeSlider('master-volume', savedSettings.masterVolume || 0.7);
        this.setVolumeSlider('music-volume', savedSettings.musicVolume || 0.5);
        this.setVolumeSlider('sfx-volume', savedSettings.sfxVolume || 0.8);
        
        // Set camera sensitivity
        this.setSensitivitySlider('camera-sensitivity', savedSettings.cameraSensitivity || 1.0);
        
        // Set checkboxes
        this.setCheckbox('particles-toggle', savedSettings.particlesEnabled !== false);
        this.setCheckbox('animations-toggle', savedSettings.animationsEnabled !== false);
        this.setCheckbox('spatial-audio', savedSettings.spatialAudio !== false);
        this.setCheckbox('auto-camera', savedSettings.autoCamera !== false);
        this.setCheckbox('reduced-motion', savedSettings.reducedMotion === true);
        
        console.log('🎛️ UI state initialized');
    }
    
    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Don't trigger shortcuts when typing in inputs
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            switch (e.code) {
                case 'Escape':
                    if (this.uiState.settingsPanelOpen) {
                        this.closeSettingsPanel();
                    }
                    break;
                    
                case 'KeyS':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        this.toggleSettingsPanel();
                    }
                    break;
                    
                case 'KeyC':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        this.toggleCharacterPanel();
                    }
                    break;
                    
                case 'KeyE':
                    e.preventDefault();
                    this.emitAction('generate-event');
                    break;
                    
                case 'KeyT':
                    e.preventDefault();
                    this.emitAction('trigger-conversation');
                    break;
                    
                case 'KeyB':
                    e.preventDefault();
                    this.emitAction('trigger-brawl');
                    break;
                    
                case 'KeyR':
                    e.preventDefault();
                    this.emitAction('reset-camera');
                    break;
                    
                case 'Digit1':
                case 'Digit2':
                case 'Digit3':
                case 'Digit4':
                case 'Digit5':
                    const speed = parseInt(e.code.slice(-1));
                    this.setSpeed(speed);
                    break;
            }
        });
        
        console.log('⌨️ Keyboard shortcuts setup');
    }
    
    /**
     * Toggle settings panel
     */
    toggleSettingsPanel() {
        const panel = this.elements.get('settings-panel');
        if (!panel) return;
        
        if (this.uiState.settingsPanelOpen) {
            this.closeSettingsPanel();
        } else {
            this.openSettingsPanel();
        }
    }
    
    /**
     * Open settings panel
     */
    openSettingsPanel() {
        const panel = this.elements.get('settings-panel');
        if (!panel) return;
        
        panel.classList.remove('hidden');
        this.uiState.settingsPanelOpen = true;
        
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: 'settings-panel-open',
                target: panel,
                properties: {
                    x: 0,
                    duration: 0.3,
                    ease: "power2.out"
                }
            });
        }
        
        // Focus first input
        const firstInput = panel.querySelector('select, input');
        if (firstInput) firstInput.focus();
    }
    
    /**
     * Close settings panel
     */
    closeSettingsPanel() {
        const panel = this.elements.get('settings-panel');
        if (!panel) return;
        
        this.uiState.settingsPanelOpen = false;
        
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: 'settings-panel-close',
                target: panel,
                properties: {
                    x: '100%',
                    duration: 0.3,
                    ease: "power2.in"
                },
                options: {
                    onComplete: () => panel.classList.add('hidden')
                }
            });
        } else {
            panel.classList.add('hidden');
        }
    }
    
    /**
     * Toggle character panel
     */
    toggleCharacterPanel() {
        const panel = this.elements.get('character-panel');
        if (!panel) return;
        
        this.uiState.characterPanelCollapsed = !this.uiState.characterPanelCollapsed;
        
        if (this.uiState.characterPanelCollapsed) {
            panel.classList.add('collapsed');
        } else {
            panel.classList.remove('collapsed');
        }
    }
    
    /**
     * Toggle fullscreen
     */
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }
    
    /**
     * Handle fullscreen change
     */
    handleFullscreenChange() {
        this.uiState.fullscreen = !!document.fullscreenElement;
        const btn = this.elements.get('fullscreen-btn');
        
        if (btn) {
            const icon = btn.querySelector('.btn-icon');
            if (icon) {
                icon.textContent = this.uiState.fullscreen ? '🔲' : '🔳';
            }
        }
    }
    
    /**
     * Toggle audio
     */
    toggleAudio() {
        this.uiState.audioEnabled = !this.uiState.audioEnabled;
        this.updateAudioButton(this.uiState.audioEnabled);
        this.emitSettingsChange({ audioEnabled: this.uiState.audioEnabled });
    }
    
    /**
     * Update audio button state
     */
    updateAudioButton(enabled) {
        const btn = this.elements.get('audio-toggle');
        if (!btn) return;
        
        const icon = btn.querySelector('.btn-icon');
        if (icon) {
            icon.textContent = enabled ? '🔊' : '🔇';
        }
        
        if (enabled) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
    
    /**
     * Toggle pause
     */
    togglePause() {
        // This will be handled by the main app
        this.emitAction('toggle-pause');
        
        const btn = this.elements.get('pause-btn');
        if (btn) {
            const icon = btn.querySelector('.btn-icon');
            if (icon) {
                // Toggle between pause and play icons
                icon.textContent = icon.textContent === '⏸️' ? '▶️' : '⏸️';
            }
        }
    }
    
    /**
     * Cycle through speed settings
     */
    cycleSpeed() {
        const speeds = [0.5, 1.0, 1.5, 2.0, 3.0];
        const currentIndex = speeds.indexOf(this.uiState.currentSpeed);
        const nextIndex = (currentIndex + 1) % speeds.length;
        
        this.setSpeed(speeds[nextIndex]);
    }
    
    /**
     * Set specific speed
     */
    setSpeed(speed) {
        this.uiState.currentSpeed = speed;
        
        const btn = this.elements.get('speed-btn');
        if (btn) {
            const indicator = btn.querySelector('.speed-indicator');
            if (indicator) {
                indicator.textContent = `${speed}x`;
            }
        }
        
        this.emitAction('set-speed', { speed });
    }
    
    /**
     * Toggle camera follow mode
     */
    toggleCameraFollow() {
        const btn = this.elements.get('camera-follow');
        if (btn) {
            btn.classList.toggle('active');
        }
        
        this.emitAction('toggle-camera-follow');
    }
    
    /**
     * Update volume display
     */
    updateVolumeDisplay(slider, volume) {
        const valueDisplay = slider.parentElement.querySelector('.volume-value');
        if (valueDisplay) {
            valueDisplay.textContent = `${Math.round(volume * 100)}%`;
        }
    }
    
    /**
     * Update sensitivity display
     */
    updateSensitivityDisplay(slider, sensitivity) {
        const valueDisplay = slider.parentElement.querySelector('.sensitivity-value');
        if (valueDisplay) {
            valueDisplay.textContent = `${sensitivity.toFixed(1)}x`;
        }
    }
    
    /**
     * Set volume slider value
     */
    setVolumeSlider(sliderId, volume) {
        const slider = this.elements.get(sliderId);
        if (slider) {
            slider.value = Math.round(volume * 100);
            this.updateVolumeDisplay(slider, volume);
        }
    }
    
    /**
     * Set sensitivity slider value
     */
    setSensitivitySlider(sliderId, sensitivity) {
        const slider = this.elements.get(sliderId);
        if (slider) {
            slider.value = sensitivity;
            this.updateSensitivityDisplay(slider, sensitivity);
        }
    }
    
    /**
     * Set checkbox value
     */
    setCheckbox(checkboxId, checked) {
        const checkbox = this.elements.get(checkboxId);
        if (checkbox) {
            checkbox.checked = checked;
        }
    }
    
    /**
     * Reset settings to defaults
     */
    resetSettings() {
        const defaults = {
            theme: 'dark-fantasy',
            quality: 'high',
            masterVolume: 0.7,
            musicVolume: 0.5,
            sfxVolume: 0.8,
            cameraSensitivity: 1.0,
            particlesEnabled: true,
            animationsEnabled: true,
            spatialAudio: true,
            autoCamera: true,
            reducedMotion: false
        };
        
        // Update UI
        Object.keys(defaults).forEach(key => {
            const value = defaults[key];
            
            if (key.includes('Volume')) {
                this.setVolumeSlider(this.kebabCase(key), value);
            } else if (key === 'cameraSensitivity') {
                this.setSensitivitySlider('camera-sensitivity', value);
            } else if (typeof value === 'boolean') {
                this.setCheckbox(this.kebabCase(key) + (key.includes('Enabled') ? '-toggle' : ''), value);
            } else {
                const element = this.elements.get(this.kebabCase(key) + '-select');
                if (element) element.value = value;
            }
        });
        
        // Emit changes
        this.emitSettingsChange(defaults);
        
        console.log('🔄 Settings reset to defaults');
    }
    
    /**
     * Apply settings
     */
    applySettings() {
        // Save current settings
        this.saveSettings();
        
        // Close settings panel
        this.closeSettingsPanel();
        
        // Show confirmation
        this.showNotification('Settings applied successfully!', 'success');
    }
    
    /**
     * Load settings from localStorage
     */
    loadSettings() {
        try {
            const saved = localStorage.getItem('warhammer-tavern-settings');
            return saved ? JSON.parse(saved) : {};
        } catch (error) {
            console.warn('Failed to load settings:', error);
            return {};
        }
    }
    
    /**
     * Save settings to localStorage
     */
    saveSettings() {
        try {
            const settings = this.getCurrentSettings();
            localStorage.setItem('warhammer-tavern-settings', JSON.stringify(settings));
            console.log('💾 Settings saved');
        } catch (error) {
            console.error('Failed to save settings:', error);
        }
    }
    
    /**
     * Get current settings from UI
     */
    getCurrentSettings() {
        const settings = {};
        
        // Get select values
        const selects = ['theme-select', 'quality-select'];
        selects.forEach(id => {
            const element = this.elements.get(id);
            if (element) {
                const key = this.camelCase(id.replace('-select', ''));
                settings[key] = element.value;
            }
        });
        
        // Get volume values
        const volumes = ['master-volume', 'music-volume', 'sfx-volume'];
        volumes.forEach(id => {
            const element = this.elements.get(id);
            if (element) {
                const key = this.camelCase(id);
                settings[key] = parseInt(element.value) / 100;
            }
        });
        
        // Get sensitivity
        const sensitivity = this.elements.get('camera-sensitivity');
        if (sensitivity) {
            settings.cameraSensitivity = parseFloat(sensitivity.value);
        }
        
        // Get checkboxes
        const checkboxes = [
            'particles-toggle',
            'animations-toggle',
            'spatial-audio',
            'auto-camera',
            'reduced-motion'
        ];
        
        checkboxes.forEach(id => {
            const element = this.elements.get(id);
            if (element) {
                const key = this.camelCase(id.replace('-toggle', '').replace('-', '_'));
                settings[key] = element.checked;
            }
        });
        
        return settings;
    }
    
    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(44, 24, 16, 0.95);
            color: #ffd700;
            padding: 15px 20px;
            border-radius: 8px;
            border: 2px solid #ffd700;
            z-index: 10000;
            backdrop-filter: blur(10px);
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: 'notification-in',
                target: notification,
                properties: {
                    x: 0,
                    opacity: 1,
                    duration: 0.3,
                    ease: "power2.out"
                }
            });
        }
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (this.gsapController) {
                this.gsapController.executeAnimation({
                    id: 'notification-out',
                    target: notification,
                    properties: {
                        x: 100,
                        opacity: 0,
                        duration: 0.3,
                        ease: "power2.in"
                    },
                    options: {
                        onComplete: () => notification.remove()
                    }
                });
            } else {
                notification.remove();
            }
        }, 3000);
    }
    
    /**
     * Handle window resize
     */
    handleResize() {
        // Update UI layout for new window size
        const isMobile = window.innerWidth < 768;
        
        if (isMobile && !this.uiState.characterPanelCollapsed) {
            this.toggleCharacterPanel();
        }
    }
    
    /**
     * Update method called from main loop
     */
    update() {
        // Update any dynamic UI elements here
        // This is called every frame from the main animation loop
    }
    
    /**
     * Emit action event
     */
    emitAction(type, data = {}) {
        this.eventEmitter.dispatchEvent(new CustomEvent('action-triggered', {
            detail: { type, ...data }
        }));
    }
    
    /**
     * Emit settings change event
     */
    emitSettingsChange(settings) {
        this.eventEmitter.dispatchEvent(new CustomEvent('settings-changed', {
            detail: settings
        }));
    }
    
    /**
     * Add event listener for UI events
     */
    on(event, handler) {
        this.eventEmitter.addEventListener(event, handler);
    }
    
    /**
     * Remove event listener
     */
    off(event, handler) {
        this.eventEmitter.removeEventListener(event, handler);
    }
    
    /**
     * Utility methods
     */
    camelCase(str) {
        return str.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
    }
    
    kebabCase(str) {
        return str.replace(/([A-Z])/g, '-$1').toLowerCase();
    }
    
    /**
     * Cleanup
     */
    destroy() {
        // Remove all event listeners
        this.eventListeners.forEach((listeners, elementId) => {
            const element = this.elements.get(elementId);
            if (element) {
                listeners.forEach(({ event, handler }) => {
                    element.removeEventListener(event, handler);
                });
            }
        });
        
        this.eventListeners.clear();
        this.elements.clear();
        
        console.log('🧹 UI Controller cleaned up');
    }
}