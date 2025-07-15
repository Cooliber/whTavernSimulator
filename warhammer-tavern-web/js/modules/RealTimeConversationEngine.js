/**
 * Real-Time Conversation Engine for CrewAI Agents
 * Handles live conversations, agent interactions, and dynamic dialogue
 */

export class RealTimeConversationEngine {
    constructor() {
        this.isInitialized = false;
        this.webSocketManager = null;
        this.gsapController = null;
        
        // Conversation state
        this.activeConversations = new Map();
        this.conversationQueue = [];
        this.agentStates = new Map();
        
        // Configuration
        this.config = {
            maxConcurrentConversations: 3,
            typingSpeed: 50, // characters per second
            bubbleLifetime: 5000, // milliseconds
            maxBubbleLength: 200,
            conversationCooldown: 2000
        };
        
        // Agent personalities and dialogue styles
        this.agentPersonalities = new Map();
        this.dialogueTemplates = new Map();
        
        // Event emitter for conversation events
        this.eventEmitter = new EventTarget();
        
        // Performance tracking
        this.metrics = {
            totalConversations: 0,
            activeAgents: 0,
            averageResponseTime: 0
        };
    }
    
    /**
     * Initialize the conversation engine
     */
    async init(dependencies = {}) {
        try {
            this.webSocketManager = dependencies.webSocketManager;
            this.gsapController = dependencies.gsapController;
            
            // Initialize agent personalities
            this.initializeAgentPersonalities();
            
            // Setup dialogue templates
            this.setupDialogueTemplates();
            
            // Setup WebSocket handlers for CrewAI integration
            this.setupWebSocketHandlers();
            
            // Initialize conversation display
            this.initializeConversationDisplay();
            
            this.isInitialized = true;
            console.log('💬 Real-Time Conversation Engine initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize Conversation Engine:', error);
            throw error;
        }
    } 
   
    /**
     * Initialize agent personalities based on CrewAI agents
     */
    initializeAgentPersonalities() {
        const personalities = {
            'karczmarz': {
                name: 'Karczmarz',
                role: 'Tavern Keeper',
                faction: 'empire',
                personality: 'wise, observant, protective',
                speechPattern: 'formal, measured',
                emoji: '🍺',
                responseStyle: 'thoughtful',
                commonPhrases: [
                    'Welcome to my establishment...',
                    'I\'ve seen many travelers pass through these doors...',
                    'The ale flows freely, but trouble is not welcome here.',
                    'What news do you bring from the roads?'
                ]
            },
            'skrytobojca': {
                name: 'Skrytobójca',
                role: 'Shadow Agent',
                faction: 'chaos',
                personality: 'mysterious, calculating, dangerous',
                speechPattern: 'cryptic, whispered',
                emoji: '🗡️',
                responseStyle: 'cryptic',
                commonPhrases: [
                    'The shadows whisper of interesting developments...',
                    'Not all who enter here leave unchanged...',
                    'Information has its price, as does silence.',
                    'The darkness sees all, remembers all.'
                ]
            },
            'wiedzma': {
                name: 'Wiedźma',
                role: 'Mystic Oracle',
                faction: 'undead',
                personality: 'mystical, prophetic, otherworldly',
                speechPattern: 'ethereal, riddling',
                emoji: '🔮',
                responseStyle: 'mystical',
                commonPhrases: [
                    'The spirits speak of change on the wind...',
                    'I see threads of fate intertwining...',
                    'The veil between worlds grows thin tonight.',
                    'Ancient powers stir in the darkness.'
                ]
            },
            'zwiadowca': {
                name: 'Zwiadowca',
                role: 'Scout',
                faction: 'elf',
                personality: 'alert, curious, well-traveled',
                speechPattern: 'direct, informative',
                emoji: '🏹',
                responseStyle: 'direct',
                commonPhrases: [
                    'The roads tell many tales to those who listen...',
                    'I bring word from distant lands...',
                    'Danger lurks in unexpected places.',
                    'The forest speaks to those who understand.'
                ]
            },
            'czempion': {
                name: 'Czempion',
                role: 'Chaos Champion',
                faction: 'chaos',
                personality: 'aggressive, unpredictable, corrupted',
                speechPattern: 'harsh, commanding',
                emoji: '⚔️',
                responseStyle: 'menacing',
                commonPhrases: [
                    'The weak shall serve the strong...',
                    'Chaos brings opportunity to those bold enough to seize it.',
                    'Order is an illusion, chaos is truth.',
                    'Power flows to those who dare to take it.'
                ]
            }
        };
        
        Object.entries(personalities).forEach(([id, personality]) => {
            this.agentPersonalities.set(id, personality);
        });
        
        console.log(`👥 Loaded ${this.agentPersonalities.size} agent personalities`);
    }    

    /**
     * Setup dialogue templates for different interaction types
     */
    setupDialogueTemplates() {
        const templates = {
            greeting: {
                empire: ['Greetings, {target}. How fares your journey?', 'Well met, {target}.'],
                chaos: ['So, {target}... we meet again.', 'Interesting to see you here, {target}.'],
                elf: ['Salutations, {target}. The day brings unexpected encounters.'],
                undead: ['The spirits whisper your name, {target}...'],
                dwarf: ['Hail and well met, {target}!']
            },
            rumor: {
                empire: ['Have you heard the news from {location}?', 'Word travels fast in these parts...'],
                chaos: ['Whispers speak of... opportunities in {location}.', 'The shadows carry interesting tales.'],
                elf: ['The wind brings strange tidings from afar.', 'Ancient signs point to change.'],
                undead: ['The dead speak of disturbances in {location}.', 'Omens gather like storm clouds.'],
                dwarf: ['The mountain folk speak of troubles brewing.']
            },
            trade: {
                empire: ['I have goods that might interest you.', 'Fair trade makes for good relations.'],
                chaos: ['Everything has a price... what do you offer?', 'I deal in more than mere coin.'],
                elf: ['These items carry the blessing of the forest.', 'Quality over quantity, always.'],
                undead: ['These artifacts hold... special properties.', 'Some things are worth more than gold.'],
                dwarf: ['Finest craftsmanship, guaranteed!', 'You won\'t find better quality anywhere.']
            },
            threat: {
                empire: ['I suggest you reconsider your words.', 'Peace is preferable, but I am prepared.'],
                chaos: ['You dare challenge me?', 'Your insolence will be... corrected.'],
                elf: ['Your hostility is noted and will be remembered.', 'Violence is crude, but sometimes necessary.'],
                undead: ['The dead have little patience for the living\'s threats.', 'You meddle with forces beyond your understanding.'],
                dwarf: ['Them\'s fighting words!', 'I\'ve faced worse than you!']
            },
            philosophical: {
                empire: ['Order brings prosperity to all.', 'Unity in purpose, strength in numbers.'],
                chaos: ['Change is the only constant in this world.', 'From destruction comes opportunity.'],
                elf: ['Balance must be maintained in all things.', 'Wisdom comes from understanding nature\'s ways.'],
                undead: ['Death is but another beginning.', 'The living fear what they do not understand.'],
                dwarf: ['Tradition and honor guide our path.', 'What\'s built to last, lasts.']
            }
        };
        
        Object.entries(templates).forEach(([type, factionTemplates]) => {
            this.dialogueTemplates.set(type, factionTemplates);
        });
        
        console.log(`📝 Loaded ${this.dialogueTemplates.size} dialogue template categories`);
    } 
   
    /**
     * Setup WebSocket handlers for CrewAI integration
     */
    setupWebSocketHandlers() {
        if (!this.webSocketManager) {
            console.warn('⚠️ WebSocket manager not available, using mock data');
            this.setupMockConversations();
            return;
        }
        
        // Handle agent thinking process
        this.webSocketManager.on('agent-thinking', (data) => {
            this.handleAgentThinking(data);
        });
        
        // Handle agent responses
        this.webSocketManager.on('agent-response', (data) => {
            this.handleAgentResponse(data);
        });
        
        // Handle conversation initiation
        this.webSocketManager.on('conversation-start', (data) => {
            this.startConversation(data);
        });
        
        // Handle conversation updates
        this.webSocketManager.on('conversation-update', (data) => {
            this.updateConversation(data);
        });
        
        // Handle agent state changes
        this.webSocketManager.on('agent-state-change', (data) => {
            this.updateAgentState(data);
        });
        
        console.log('🔌 WebSocket handlers setup for CrewAI integration');
    }
    
    /**
     * Setup mock conversations for development/demo
     */
    setupMockConversations() {
        // Start mock conversation cycle
        setInterval(() => {
            if (this.activeConversations.size < this.config.maxConcurrentConversations) {
                this.generateMockConversation();
            }
        }, 8000); // New conversation every 8 seconds
        
        // Start first conversation after 2 seconds
        setTimeout(() => this.generateMockConversation(), 2000);
        
        console.log('🎭 Mock conversation system activated');
    }
    
    /**
     * Generate mock conversation for demo purposes
     */
    generateMockConversation() {
        const agents = Array.from(this.agentPersonalities.keys());
        const speaker = agents[Math.floor(Math.random() * agents.length)];
        const listener = agents.filter(a => a !== speaker)[Math.floor(Math.random() * (agents.length - 1))];
        
        const conversationTypes = ['greeting', 'rumor', 'trade', 'philosophical'];
        const type = conversationTypes[Math.floor(Math.random() * conversationTypes.length)];
        
        this.startConversation({
            id: `mock-${Date.now()}`,
            speaker: speaker,
            listener: listener,
            type: type,
            content: this.generateDialogue(speaker, listener, type)
        });
    }    
    
/**
     * Generate dialogue based on agent personalities and context
     */
    generateDialogue(speakerId, listenerId, type = 'greeting', context = {}) {
        const speaker = this.agentPersonalities.get(speakerId);
        const listener = this.agentPersonalities.get(listenerId);
        
        if (!speaker || !listener) {
            return 'The tavern grows quiet...';
        }
        
        const templates = this.dialogueTemplates.get(type);
        if (!templates) {
            return speaker.commonPhrases[Math.floor(Math.random() * speaker.commonPhrases.length)];
        }
        
        const factionTemplates = templates[speaker.faction] || templates['empire'];
        let dialogue = factionTemplates[Math.floor(Math.random() * factionTemplates.length)];
        
        // Replace placeholders
        dialogue = dialogue.replace('{target}', listener.name);
        dialogue = dialogue.replace('{location}', context.location || 'the capital');
        dialogue = dialogue.replace('{item}', context.item || 'rare artifacts');
        
        return dialogue;
    }
    
    /**
     * Initialize conversation display elements
     */
    initializeConversationDisplay() {
        const conversationDisplay = document.getElementById('conversation-display');
        if (!conversationDisplay) {
            console.warn('⚠️ Conversation display element not found');
            return;
        }
        
        // Ensure conversation bubbles container exists
        let bubblesContainer = document.getElementById('conversation-bubbles');
        if (!bubblesContainer) {
            bubblesContainer = document.createElement('div');
            bubblesContainer.id = 'conversation-bubbles';
            bubblesContainer.className = 'conversation-bubbles';
            conversationDisplay.appendChild(bubblesContainer);
        }
        
        console.log('💬 Conversation display initialized');
    }
    
    /**
     * Start a new conversation
     */
    startConversation(conversationData) {
        const { id, speaker, listener, type, content } = conversationData;
        
        // Check if we can start a new conversation
        if (this.activeConversations.size >= this.config.maxConcurrentConversations) {
            this.conversationQueue.push(conversationData);
            return;
        }
        
        // Create conversation object
        const conversation = {
            id: id || `conv-${Date.now()}`,
            speaker,
            listener,
            type: type || 'general',
            content,
            startTime: Date.now(),
            bubbleElement: null,
            isActive: true
        };
        
        // Add to active conversations
        this.activeConversations.set(conversation.id, conversation);
        
        // Update agent states
        this.updateAgentState({ agentId: speaker, state: 'speaking' });
        this.updateAgentState({ agentId: listener, state: 'listening' });
        
        // Create and animate conversation bubble
        this.createConversationBubble(conversation);
        
        // Emit conversation start event
        this.emitEvent('conversation-started', conversation);
        
        // Update metrics
        this.metrics.totalConversations++;
        
        console.log(`💬 Started conversation: ${speaker} -> ${listener}`);
    }  
  
    /**
     * Create and animate conversation bubble
     */
    createConversationBubble(conversation) {
        const bubblesContainer = document.getElementById('conversation-bubbles');
        if (!bubblesContainer) return;
        
        const speaker = this.agentPersonalities.get(conversation.speaker);
        if (!speaker) return;
        
        // Create bubble element
        const bubble = document.createElement('div');
        bubble.className = 'conversation-bubble';
        bubble.id = `bubble-${conversation.id}`;
        
        // Determine bubble position (left/right alternating)
        const isLeft = this.activeConversations.size % 2 === 1;
        bubble.classList.add(isLeft ? 'left' : 'right');
        
        // Create bubble content
        bubble.innerHTML = `
            <div class="bubble-header">
                <div class="bubble-avatar faction-${speaker.faction}">
                    ${speaker.emoji}
                </div>
                <div class="bubble-name">${speaker.name}</div>
                <div class="bubble-faction">${speaker.faction}</div>
            </div>
            <div class="bubble-content">
                <div class="bubble-typing">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        // Add to container
        bubblesContainer.appendChild(bubble);
        conversation.bubbleElement = bubble;
        
        // Animate bubble entrance
        if (this.gsapController) {
            this.gsapController.animateConversationBubble(bubble, conversation.content, {
                typingSpeed: this.config.typingSpeed,
                showDuration: this.config.bubbleLifetime,
                faction: speaker.faction
            });
        } else {
            // Fallback animation
            this.animateBubbleFallback(bubble, conversation.content);
        }
        
        // Schedule bubble removal
        setTimeout(() => {
            this.endConversation(conversation.id);
        }, this.config.bubbleLifetime);
    }
    
    /**
     * Fallback bubble animation without GSAP
     */
    animateBubbleFallback(bubble, content) {
        // Show bubble
        bubble.classList.add('show');
        
        // Start typing animation
        setTimeout(() => {
            const contentElement = bubble.querySelector('.bubble-content');
            const typingElement = bubble.querySelector('.bubble-typing');
            
            if (typingElement) typingElement.style.display = 'none';
            
            // Type text character by character
            let currentText = '';
            let charIndex = 0;
            
            const typeInterval = setInterval(() => {
                if (charIndex < content.length) {
                    currentText += content[charIndex];
                    contentElement.textContent = currentText;
                    charIndex++;
                } else {
                    clearInterval(typeInterval);
                }
            }, 1000 / this.config.typingSpeed);
        }, 500);
    }   
 
    /**
     * End a conversation
     */
    endConversation(conversationId) {
        const conversation = this.activeConversations.get(conversationId);
        if (!conversation) return;
        
        // Remove bubble element
        if (conversation.bubbleElement) {
            if (this.gsapController) {
                this.gsapController.fadeOut(conversation.bubbleElement, 0.3).then(() => {
                    conversation.bubbleElement.remove();
                });
            } else {
                conversation.bubbleElement.classList.remove('show');
                setTimeout(() => conversation.bubbleElement.remove(), 300);
            }
        }
        
        // Update agent states back to idle
        this.updateAgentState({ agentId: conversation.speaker, state: 'idle' });
        this.updateAgentState({ agentId: conversation.listener, state: 'idle' });
        
        // Remove from active conversations
        this.activeConversations.delete(conversationId);
        
        // Process queued conversations
        if (this.conversationQueue.length > 0) {
            const nextConversation = this.conversationQueue.shift();
            setTimeout(() => this.startConversation(nextConversation), this.config.conversationCooldown);
        }
        
        // Emit conversation end event
        this.emitEvent('conversation-ended', { id: conversationId });
        
        console.log(`💬 Ended conversation: ${conversationId}`);
    }
    
    /**
     * Handle agent thinking process from CrewAI
     */
    handleAgentThinking(data) {
        const { agentId, reasoning, confidence } = data;
        
        // Update agent state
        this.updateAgentState({ 
            agentId, 
            state: 'thinking', 
            reasoning,
            confidence 
        });
        
        // Show thinking indicator on character card
        this.showThinkingIndicator(agentId, reasoning);
        
        console.log(`🤔 ${agentId} is thinking: ${reasoning}`);
    }
    
    /**
     * Handle agent response from CrewAI
     */
    handleAgentResponse(data) {
        const { agentId, response, emotion, confidence } = data;
        
        // Find if agent is in active conversation
        let targetConversation = null;
        for (const conversation of this.activeConversations.values()) {
            if (conversation.speaker === agentId || conversation.listener === agentId) {
                targetConversation = conversation;
                break;
            }
        }
        
        if (targetConversation) {
            // Update existing conversation
            this.updateConversationContent(targetConversation.id, response);
        } else {
            // Start new conversation
            this.startConversation({
                speaker: agentId,
                listener: this.selectRandomListener(agentId),
                content: response,
                emotion,
                confidence
            });
        }
    }
    
    /**
     * Update agent state and visual indicators
     */
    updateAgentState(data) {
        const { agentId, state, reasoning, confidence, emotion } = data;
        
        // Update internal state
        this.agentStates.set(agentId, {
            state,
            reasoning,
            confidence,
            emotion,
            lastUpdate: Date.now()
        });
        
        // Update character card visual state
        this.updateCharacterCardState(agentId, state, { reasoning, confidence, emotion });
        
        // Update metrics
        this.updateMetrics();
    } 
   
    /**
     * Update character card visual state
     */
    updateCharacterCardState(agentId, state, metadata = {}) {
        const characterCard = document.querySelector(`[data-character="${agentId}"]`);
        if (!characterCard) return;
        
        // Update status indicator
        const statusIndicator = characterCard.querySelector('.character-status');
        if (statusIndicator) {
            statusIndicator.className = `character-status ${state}`;
        }
        
        // Update character card class
        characterCard.className = characterCard.className.replace(/\bstate-\w+/g, '');
        characterCard.classList.add(`state-${state}`);
        
        // Show reasoning trace if available
        if (metadata.reasoning) {
            this.showReasoningTrace(characterCard, metadata.reasoning);
        }
        
        // Update confidence indicator
        if (metadata.confidence !== undefined) {
            this.updateConfidenceIndicator(characterCard, metadata.confidence);
        }
        
        // Add emotion effects
        if (metadata.emotion) {
            this.addEmotionEffects(characterCard, metadata.emotion);
        }
    }
    
    /**
     * Show thinking indicator
     */
    showThinkingIndicator(agentId, reasoning) {
        const characterCard = document.querySelector(`[data-character="${agentId}"]`);
        if (!characterCard) return;
        
        // Add thinking animation class
        characterCard.classList.add('thinking');
        
        // Create or update thinking bubble
        let thinkingBubble = characterCard.querySelector('.thinking-bubble');
        if (!thinkingBubble) {
            thinkingBubble = document.createElement('div');
            thinkingBubble.className = 'thinking-bubble';
            characterCard.appendChild(thinkingBubble);
        }
        
        thinkingBubble.innerHTML = `
            <div class="thinking-content">
                <div class="thinking-dots">
                    <span></span><span></span><span></span>
                </div>
                <div class="thinking-text">${reasoning}</div>
            </div>
        `;
        
        // Animate thinking bubble
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `thinking-${agentId}`,
                target: thinkingBubble,
                properties: {
                    opacity: 1,
                    scale: 1,
                    duration: 0.3,
                    ease: "back.out(1.7)"
                }
            });
        }
        
        // Remove thinking indicator after delay
        setTimeout(() => {
            characterCard.classList.remove('thinking');
            if (thinkingBubble) {
                if (this.gsapController) {
                    this.gsapController.fadeOut(thinkingBubble, 0.3).then(() => {
                        thinkingBubble.remove();
                    });
                } else {
                    thinkingBubble.remove();
                }
            }
        }, 3000);
    }
    
    /**
     * Show reasoning trace
     */
    showReasoningTrace(characterCard, reasoning) {
        let reasoningTrace = characterCard.querySelector('.reasoning-trace');
        if (!reasoningTrace) {
            reasoningTrace = document.createElement('div');
            reasoningTrace.className = 'reasoning-trace';
            characterCard.appendChild(reasoningTrace);
        }
        
        reasoningTrace.textContent = reasoning;
        
        // Animate trace update
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `reasoning-${characterCard.dataset.character}`,
                target: reasoningTrace,
                properties: {
                    opacity: 0.8,
                    duration: 0.2,
                    ease: "power2.out"
                }
            });
        }
    }    
 
   /**
     * Update confidence indicator
     */
    updateConfidenceIndicator(characterCard, confidence) {
        let confidenceBar = characterCard.querySelector('.confidence-bar');
        if (!confidenceBar) {
            confidenceBar = document.createElement('div');
            confidenceBar.className = 'confidence-bar';
            confidenceBar.innerHTML = '<div class="confidence-fill"></div>';
            characterCard.appendChild(confidenceBar);
        }
        
        const fill = confidenceBar.querySelector('.confidence-fill');
        if (fill && this.gsapController) {
            this.gsapController.animateStatBar(fill, confidence * 100);
        }
    }
    
    /**
     * Add emotion effects to character card
     */
    addEmotionEffects(characterCard, emotion) {
        // Remove existing emotion classes
        characterCard.className = characterCard.className.replace(/\bemotion-\w+/g, '');
        
        // Add new emotion class
        characterCard.classList.add(`emotion-${emotion}`);
        
        // Add emotion-specific visual effects
        switch (emotion) {
            case 'angry':
                this.addAngryEffects(characterCard);
                break;
            case 'happy':
                this.addHappyEffects(characterCard);
                break;
            case 'mysterious':
                this.addMysteriousEffects(characterCard);
                break;
            case 'worried':
                this.addWorriedEffects(characterCard);
                break;
        }
    }
    
    /**
     * Add angry emotion effects
     */
    addAngryEffects(element) {
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `angry-${element.dataset.character}`,
                target: element,
                properties: {
                    boxShadow: "0 0 20px rgba(255, 0, 0, 0.6)",
                    duration: 0.5,
                    ease: "power2.inOut",
                    repeat: 3,
                    yoyo: true
                }
            });
        }
    }
    
    /**
     * Add happy emotion effects
     */
    addHappyEffects(element) {
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `happy-${element.dataset.character}`,
                target: element,
                properties: {
                    boxShadow: "0 0 15px rgba(255, 215, 0, 0.8)",
                    duration: 1,
                    ease: "sine.inOut",
                    repeat: 2,
                    yoyo: true
                }
            });
        }
    }
    
    /**
     * Add mysterious emotion effects
     */
    addMysteriousEffects(element) {
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `mysterious-${element.dataset.character}`,
                target: element,
                properties: {
                    filter: "brightness(0.8) contrast(1.2)",
                    duration: 2,
                    ease: "power2.inOut",
                    repeat: -1,
                    yoyo: true
                }
            });
        }
    }
    
    /**
     * Add worried emotion effects
     */
    addWorriedEffects(element) {
        if (this.gsapController) {
            this.gsapController.executeAnimation({
                id: `worried-${element.dataset.character}`,
                target: element,
                properties: {
                    x: 2,
                    duration: 0.1,
                    ease: "power2.inOut",
                    repeat: 10,
                    yoyo: true
                }
            });
        }
    }    

    /**
     * Select random listener for conversation
     */
    selectRandomListener(speakerId) {
        const availableAgents = Array.from(this.agentPersonalities.keys())
            .filter(id => id !== speakerId);
        
        if (availableAgents.length === 0) return null;
        
        return availableAgents[Math.floor(Math.random() * availableAgents.length)];
    }
    
    /**
     * Update conversation content
     */
    updateConversationContent(conversationId, newContent) {
        const conversation = this.activeConversations.get(conversationId);
        if (!conversation || !conversation.bubbleElement) return;
        
        const contentElement = conversation.bubbleElement.querySelector('.bubble-content');
        if (contentElement) {
            // Update content with typing animation
            if (this.gsapController) {
                this.gsapController.typeText(contentElement, newContent, this.config.typingSpeed);
            } else {
                contentElement.textContent = newContent;
            }
        }
        
        conversation.content = newContent;
    }
    
    /**
     * Update metrics
     */
    updateMetrics() {
        this.metrics.activeAgents = this.agentStates.size;
        
        // Calculate average response time
        const responseTimes = Array.from(this.agentStates.values())
            .map(state => Date.now() - state.lastUpdate)
            .filter(time => time < 10000); // Only recent responses
        
        if (responseTimes.length > 0) {
            this.metrics.averageResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
        }
    }
    
    /**
     * Get conversation metrics
     */
    getMetrics() {
        return {
            ...this.metrics,
            activeConversations: this.activeConversations.size,
            queuedConversations: this.conversationQueue.length
        };
    }
    
    /**
     * Emit event
     */
    emitEvent(eventType, data) {
        this.eventEmitter.dispatchEvent(new CustomEvent(eventType, { detail: data }));
    }
    
    /**
     * Add event listener
     */
    on(eventType, handler) {
        this.eventEmitter.addEventListener(eventType, handler);
    }
    
    /**
     * Remove event listener
     */
    off(eventType, handler) {
        this.eventEmitter.removeEventListener(eventType, handler);
    }
    
    /**
     * Start the conversation engine
     */
    start() {
        if (!this.isInitialized) {
            console.error('❌ Conversation engine not initialized');
            return;
        }
        
        console.log('🚀 Real-Time Conversation Engine started');
        
        // Start processing conversation queue
        this.processConversationQueue();
    }
    
    /**
     * Process conversation queue
     */
    processConversationQueue() {
        setInterval(() => {
            if (this.conversationQueue.length > 0 && 
                this.activeConversations.size < this.config.maxConcurrentConversations) {
                const nextConversation = this.conversationQueue.shift();
                this.startConversation(nextConversation);
            }
        }, 1000);
    }
    
    /**
     * Stop the conversation engine
     */
    stop() {
        // End all active conversations
        for (const conversationId of this.activeConversations.keys()) {
            this.endConversation(conversationId);
        }
        
        // Clear queue
        this.conversationQueue = [];
        
        // Reset agent states
        this.agentStates.clear();
        
        console.log('⏹️ Real-Time Conversation Engine stopped');
    }
    
    /**
     * Update method called from main loop
     */
    update(deltaTime) {
        // Update conversation timers and cleanup
        const now = Date.now();
        
        for (const [id, conversation] of this.activeConversations.entries()) {
            if (now - conversation.startTime > this.config.bubbleLifetime) {
                this.endConversation(id);
            }
        }
        
        // Update metrics
        this.updateMetrics();
    }
}