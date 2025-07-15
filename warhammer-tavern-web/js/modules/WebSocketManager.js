/**
 * WebSocket Manager for CrewAI Integration
 * Handles real-time communication with the backend CrewAI system
 */

export class WebSocketManager {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // Event handling
        this.eventHandlers = new Map();
        this.messageQueue = [];
        this.pendingRequests = new Map();
        
        // Configuration
        this.config = {
            heartbeatInterval: 30000, // 30 seconds
            messageTimeout: 10000,    // 10 seconds
            maxQueueSize: 100
        };
        
        // State tracking
        this.connectionState = 'disconnected';
        this.lastHeartbeat = null;
        this.heartbeatTimer = null;
        
        // Bind methods
        this.handleOpen = this.handleOpen.bind(this);
        this.handleMessage = this.handleMessage.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleError = this.handleError.bind(this);
    }
    
    /**
     * Connect to WebSocket server
     */
    async connect(url) {
        if (this.isConnected) {
            console.warn('⚠️ Already connected to WebSocket');
            return;
        }
        
        try {
            console.log(`🔌 Connecting to WebSocket: ${url}`);
            this.connectionState = 'connecting';
            
            this.socket = new WebSocket(url);
            
            // Setup event listeners
            this.socket.addEventListener('open', this.handleOpen);
            this.socket.addEventListener('message', this.handleMessage);
            this.socket.addEventListener('close', this.handleClose);
            this.socket.addEventListener('error', this.handleError);
            
            // Wait for connection
            await this.waitForConnection();
            
        } catch (error) {
            console.error('❌ Failed to connect to WebSocket:', error);
            this.connectionState = 'error';
            throw error;
        }
    }    

    /**
     * Wait for WebSocket connection
     */
    waitForConnection() {
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error('Connection timeout'));
            }, 10000);
            
            const checkConnection = () => {
                if (this.isConnected) {
                    clearTimeout(timeout);
                    resolve();
                } else if (this.connectionState === 'error') {
                    clearTimeout(timeout);
                    reject(new Error('Connection failed'));
                } else {
                    setTimeout(checkConnection, 100);
                }
            };
            
            checkConnection();
        });
    }
    
    /**
     * Handle WebSocket open event
     */
    handleOpen(event) {
        console.log('✅ WebSocket connected successfully');
        this.isConnected = true;
        this.connectionState = 'connected';
        this.reconnectAttempts = 0;
        
        // Start heartbeat
        this.startHeartbeat();
        
        // Send queued messages
        this.processMessageQueue();
        
        // Emit connection event
        this.emit('connected', { timestamp: Date.now() });
        
        // Send initial handshake
        this.send({
            type: 'handshake',
            clientType: 'warhammer-tavern-web',
            version: '1.0.0',
            capabilities: ['conversations', 'agent-monitoring', 'real-time-updates']
        });
    }
    
    /**
     * Handle WebSocket message
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            this.processMessage(data);
        } catch (error) {
            console.error('❌ Failed to parse WebSocket message:', error);
        }
    }
    
    /**
     * Process incoming message
     */
    processMessage(data) {
        const { type, id, payload, error } = data;
        
        // Handle heartbeat response
        if (type === 'heartbeat') {
            this.lastHeartbeat = Date.now();
            return;
        }
        
        // Handle request responses
        if (id && this.pendingRequests.has(id)) {
            const { resolve, reject } = this.pendingRequests.get(id);
            this.pendingRequests.delete(id);
            
            if (error) {
                reject(new Error(error));
            } else {
                resolve(payload);
            }
            return;
        }
        
        // Handle different message types
        switch (type) {
            case 'agent-thinking':
                this.emit('agent-thinking', payload);
                break;
                
            case 'agent-response':
                this.emit('agent-response', payload);
                break;
                
            case 'conversation-start':
                this.emit('conversation-start', payload);
                break;
                
            case 'conversation-update':
                this.emit('conversation-update', payload);
                break;
                
            case 'agent-state-change':
                this.emit('agent-state-change', payload);
                break;
                
            case 'tavern-event':
                this.emit('tavern-event', payload);
                break;
                
            case 'system-status':
                this.emit('system-status', payload);
                break;
                
            default:
                console.warn(`⚠️ Unknown message type: ${type}`);
        }
    }    
  
  /**
     * Handle WebSocket close event
     */
    handleClose(event) {
        console.log(`🔌 WebSocket connection closed: ${event.code} - ${event.reason}`);
        this.isConnected = false;
        this.connectionState = 'disconnected';
        
        // Stop heartbeat
        this.stopHeartbeat();
        
        // Emit disconnection event
        this.emit('disconnected', { 
            code: event.code, 
            reason: event.reason,
            timestamp: Date.now()
        });
        
        // Attempt reconnection if not intentional
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.attemptReconnection();
        }
    }
    
    /**
     * Handle WebSocket error event
     */
    handleError(event) {
        console.error('❌ WebSocket error:', event);
        this.connectionState = 'error';
        
        // Emit error event
        this.emit('error', { 
            error: event,
            timestamp: Date.now()
        });
    }
    
    /**
     * Attempt to reconnect
     */
    attemptReconnection() {
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`🔄 Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);
        
        setTimeout(async () => {
            try {
                // Get the original URL from the socket
                const url = this.socket?.url || this.getDefaultWebSocketUrl();
                await this.connect(url);
            } catch (error) {
                console.error('❌ Reconnection failed:', error);
                
                if (this.reconnectAttempts >= this.maxReconnectAttempts) {
                    console.error('❌ Max reconnection attempts reached');
                    this.emit('reconnection-failed', { attempts: this.reconnectAttempts });
                }
            }
        }, delay);
    }
    
    /**
     * Get default WebSocket URL
     */
    getDefaultWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws/tavern`;
    }
    
    /**
     * Send message to server
     */
    send(message) {
        if (!this.isConnected) {
            // Queue message for later
            if (this.messageQueue.length < this.config.maxQueueSize) {
                this.messageQueue.push(message);
                console.log('📤 Message queued (not connected)');
            } else {
                console.warn('⚠️ Message queue full, dropping message');
            }
            return;
        }
        
        try {
            const messageString = JSON.stringify(message);
            this.socket.send(messageString);
            console.log('📤 Message sent:', message.type);
        } catch (error) {
            console.error('❌ Failed to send message:', error);
        }
    }
    
    /**
     * Send request and wait for response
     */
    request(type, payload = {}, timeout = this.config.messageTimeout) {
        return new Promise((resolve, reject) => {
            const id = this.generateRequestId();
            
            // Store request for response handling
            this.pendingRequests.set(id, { resolve, reject });
            
            // Set timeout
            setTimeout(() => {
                if (this.pendingRequests.has(id)) {
                    this.pendingRequests.delete(id);
                    reject(new Error(`Request timeout: ${type}`));
                }
            }, timeout);
            
            // Send request
            this.send({
                type,
                id,
                payload
            });
        });
    }    

    /**
     * Process message queue
     */
    processMessageQueue() {
        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            this.send(message);
        }
    }
    
    /**
     * Start heartbeat mechanism
     */
    startHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            if (this.isConnected) {
                this.send({ type: 'heartbeat', timestamp: Date.now() });
                
                // Check if we received a heartbeat response recently
                if (this.lastHeartbeat && Date.now() - this.lastHeartbeat > this.config.heartbeatInterval * 2) {
                    console.warn('⚠️ Heartbeat timeout, connection may be lost');
                    this.socket?.close();
                }
            }
        }, this.config.heartbeatInterval);
    }
    
    /**
     * Stop heartbeat mechanism
     */
    stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }
    
    /**
     * Generate unique request ID
     */
    generateRequestId() {
        return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    /**
     * Add event listener
     */
    on(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        this.eventHandlers.get(eventType).push(handler);
    }
    
    /**
     * Remove event listener
     */
    off(eventType, handler) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }
    
    /**
     * Emit event to handlers
     */
    emit(eventType, data) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            handlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`❌ Error in event handler for ${eventType}:`, error);
                }
            });
        }
    }
    
    /**
     * CrewAI specific methods
     */
    
    /**
     * Request agent to think about something
     */
    async requestAgentThinking(agentId, context) {
        return this.request('request-agent-thinking', {
            agentId,
            context,
            timestamp: Date.now()
        });
    }
    
    /**
     * Trigger conversation between agents
     */
    async triggerConversation(speakerId, listenerId, topic = null) {
        return this.request('trigger-conversation', {
            speakerId,
            listenerId,
            topic,
            timestamp: Date.now()
        });
    }
    
    /**
     * Request tavern event generation
     */
    async generateTavernEvent(eventType = 'random') {
        return this.request('generate-tavern-event', {
            eventType,
            timestamp: Date.now()
        });
    }
    
    /**
     * Get current tavern state
     */
    async getTavernState() {
        return this.request('get-tavern-state');
    }
    
    /**
     * Update tavern settings
     */
    async updateTavernSettings(settings) {
        return this.request('update-tavern-settings', settings);
    }
    
    /**
     * Get agent status
     */
    async getAgentStatus(agentId = null) {
        return this.request('get-agent-status', { agentId });
    }
    
    /**
     * Send user action to CrewAI system
     */
    async sendUserAction(action, data = {}) {
        return this.request('user-action', {
            action,
            data,
            timestamp: Date.now()
        });
    }
    
    /**
     * Get connection status
     */
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            connectionState: this.connectionState,
            reconnectAttempts: this.reconnectAttempts,
            lastHeartbeat: this.lastHeartbeat,
            queuedMessages: this.messageQueue.length,
            pendingRequests: this.pendingRequests.size
        };
    }
    
    /**
     * Disconnect from WebSocket
     */
    disconnect() {
        if (this.socket) {
            console.log('🔌 Disconnecting WebSocket...');
            this.socket.close(1000, 'Client disconnect');
            this.socket = null;
        }
        
        this.isConnected = false;
        this.connectionState = 'disconnected';
        this.stopHeartbeat();
        
        // Clear pending requests
        this.pendingRequests.forEach(({ reject }) => {
            reject(new Error('Connection closed'));
        });
        this.pendingRequests.clear();
        
        // Clear message queue
        this.messageQueue = [];
    }
    
    /**
     * Cleanup resources
     */
    destroy() {
        this.disconnect();
        this.eventHandlers.clear();
        console.log('🧹 WebSocket Manager destroyed');
    }
}