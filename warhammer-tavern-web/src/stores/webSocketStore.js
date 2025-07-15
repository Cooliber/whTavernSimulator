import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'
import toast from 'react-hot-toast'

// Import the app store to update state
import { useAppStore } from './appStore'

const initialState = {
  socket: null,
  isConnected: false,
  connectionStatus: 'disconnected',
  reconnectAttempts: 0,
  maxReconnectAttempts: 5,
  subscriptions: new Set(),
  messageQueue: [],
  lastHeartbeat: null,
  clientId: null
}

export const useWebSocketStore = create()(
  devtools(
    immer((set, get) => ({
      ...initialState,
      
      // Connection management
      connect: async (url) => {
        const state = get()
        
        if (state.isConnected) {
          console.warn('WebSocket already connected')
          return
        }
        
        try {
          console.log(`🔌 Connecting to WebSocket: ${url}`)
          
          set((draft) => {
            draft.connectionStatus = 'connecting'
          })
          
          const socket = new WebSocket(url)
          
          // Set up event listeners
          socket.onopen = (event) => {
            console.log('✅ WebSocket connected')
            
            set((draft) => {
              draft.socket = socket
              draft.isConnected = true
              draft.connectionStatus = 'connected'
              draft.reconnectAttempts = 0
            })
            
            // Start heartbeat
            get().startHeartbeat()
            
            // Process queued messages
            get().processMessageQueue()
            
            toast.success('Connected to tavern server')
          }
          
          socket.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data)
              get().handleMessage(data)
            } catch (error) {
              console.error('Failed to parse WebSocket message:', error)
            }
          }
          
          socket.onclose = (event) => {
            console.log(`🔌 WebSocket closed: ${event.code} - ${event.reason}`)
            
            set((draft) => {
              draft.socket = null
              draft.isConnected = false
              draft.connectionStatus = 'disconnected'
            })
            
            get().stopHeartbeat()
            
            // Attempt reconnection if not intentional
            if (event.code !== 1000 && state.reconnectAttempts < state.maxReconnectAttempts) {
              get().attemptReconnection(url)
            } else {
              toast.error('Disconnected from tavern server')
            }
          }
          
          socket.onerror = (error) => {
            console.error('WebSocket error:', error)
            
            set((draft) => {
              draft.connectionStatus = 'error'
            })
            
            toast.error('Connection error')
          }
          
        } catch (error) {
          console.error('Failed to connect WebSocket:', error)
          
          set((draft) => {
            draft.connectionStatus = 'error'
          })
          
          throw error
        }
      },
      
      disconnect: () => {
        const state = get()
        
        if (state.socket) {
          console.log('🔌 Disconnecting WebSocket...')
          state.socket.close(1000, 'Client disconnect')
        }
        
        get().stopHeartbeat()
        
        set((draft) => {
          draft.socket = null
          draft.isConnected = false
          draft.connectionStatus = 'disconnected'
          draft.messageQueue = []
          draft.subscriptions.clear()
        })
      },
      
      // Message handling
      send: (message) => {
        const state = get()
        
        if (!state.isConnected || !state.socket) {
          // Queue message for later
          set((draft) => {
            draft.messageQueue.push(message)
          })
          return
        }
        
        try {
          state.socket.send(JSON.stringify(message))
        } catch (error) {
          console.error('Failed to send WebSocket message:', error)
        }
      },
      
      handleMessage: (data) => {
        const { type, data: payload, timestamp, client_id } = data
        
        // Update client ID if provided
        if (client_id) {
          set((draft) => {
            draft.clientId = client_id
          })
        }
        
        // Handle different message types
        switch (type) {
          case 'pong':
            set((draft) => {
              draft.lastHeartbeat = Date.now()
            })
            break
            
          case 'tavern_update':
            useAppStore.getState().updateTavernState(payload)
            break
            
          case 'conversation_start':
            toast.success(`Conversation started: ${payload.participants?.join(', ')}`)
            break
            
          case 'conversation_message':
            // Handle conversation message
            console.log('Conversation message:', payload)
            break
            
          case 'conversation_end':
            toast.info('Conversation ended')
            break
            
          case 'agent_action':
            toast.info(`${payload.agent_name} performed ${payload.action_type}`)
            break
            
          case 'tavern_event':
            toast.success(`Tavern Event: ${payload.description}`)
            break
            
          case 'economy_update':
            // Handle economy update
            console.log('Economy update:', payload)
            break
            
          case 'character_animation':
            // Handle character animation
            console.log('Character animation:', payload)
            break
            
          case 'system_status':
            // Handle system status
            console.log('System status:', payload)
            break
            
          case 'error':
            console.error('WebSocket error:', payload)
            toast.error(payload.error || 'Server error')
            break
            
          default:
            console.warn(`Unknown WebSocket message type: ${type}`)
        }
      },
      
      processMessageQueue: () => {
        const state = get()
        
        while (state.messageQueue.length > 0 && state.isConnected) {
          const message = state.messageQueue.shift()
          get().send(message)
        }
      },
      
      // Subscription management
      subscribe: (topic) => {
        const state = get()
        
        if (state.subscriptions.has(topic)) {
          return
        }
        
        set((draft) => {
          draft.subscriptions.add(topic)
        })
        
        get().send({
          type: 'subscribe',
          data: { topic }
        })
      },
      
      unsubscribe: (topic) => {
        const state = get()
        
        if (!state.subscriptions.has(topic)) {
          return
        }
        
        set((draft) => {
          draft.subscriptions.delete(topic)
        })
        
        get().send({
          type: 'unsubscribe',
          data: { topic }
        })
      },
      
      // Heartbeat management
      startHeartbeat: () => {
        const heartbeatInterval = setInterval(() => {
          const state = get()
          
          if (state.isConnected) {
            get().send({
              type: 'ping',
              data: { timestamp: Date.now() }
            })
            
            // Check for heartbeat timeout
            if (state.lastHeartbeat && Date.now() - state.lastHeartbeat > 60000) {
              console.warn('Heartbeat timeout')
              state.socket?.close()
            }
          }
        }, 30000) // 30 seconds
        
        set((draft) => {
          draft.heartbeatInterval = heartbeatInterval
        })
      },
      
      stopHeartbeat: () => {
        const state = get()
        
        if (state.heartbeatInterval) {
          clearInterval(state.heartbeatInterval)
          
          set((draft) => {
            draft.heartbeatInterval = null
          })
        }
      },
      
      // Reconnection logic
      attemptReconnection: (url) => {
        const state = get()
        
        set((draft) => {
          draft.reconnectAttempts += 1
        })
        
        const delay = Math.min(1000 * Math.pow(2, state.reconnectAttempts), 30000)
        
        console.log(`🔄 Attempting reconnection ${state.reconnectAttempts}/${state.maxReconnectAttempts} in ${delay}ms`)
        
        setTimeout(async () => {
          try {
            await get().connect(url)
          } catch (error) {
            console.error('Reconnection failed:', error)
            
            if (state.reconnectAttempts >= state.maxReconnectAttempts) {
              toast.error('Failed to reconnect to server')
            }
          }
        }, delay)
      },
      
      // Utility methods
      getConnectionStats: () => {
        const state = get()
        
        return {
          isConnected: state.isConnected,
          connectionStatus: state.connectionStatus,
          reconnectAttempts: state.reconnectAttempts,
          subscriptions: Array.from(state.subscriptions),
          queuedMessages: state.messageQueue.length,
          lastHeartbeat: state.lastHeartbeat,
          clientId: state.clientId
        }
      }
    })),
    {
      name: 'warhammer-tavern-websocket'
    }
  )
)
