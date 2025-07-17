import { ref, reactive, onMounted, onUnmounted } from 'vue'

interface GMAction {
  id: string
  type: 'npc_update' | 'event_trigger' | 'atmosphere_change' | 'session_pause' | 'focus_mode'
  payload: any
  timestamp: number
  gmId: string
  gmName: string
}

interface TavernState {
  npcs: any[]
  events: any[]
  atmosphere: any
  economy: any
  sessionPaused: boolean
  focusMode: boolean
}

interface ConnectedGM {
  id: string
  name: string
  role: 'primary' | 'assistant' | 'observer'
  lastSeen: number
  isActive: boolean
}

export const useGMCollaboration = () => {
  // Connection state
  const isConnected = ref(false)
  const connectionStatus = ref<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected')
  const socket = ref<WebSocket | null>(null)
  
  // Collaboration state
  const connectedGMs = ref<ConnectedGM[]>([])
  const currentGM = reactive({
    id: '',
    name: 'Game Master',
    role: 'primary' as 'primary' | 'assistant' | 'observer'
  })
  
  // Action history
  const actionHistory = ref<GMAction[]>([])
  const pendingActions = ref<GMAction[]>([])
  
  // Conflict resolution
  const conflictResolution = ref<'last_write_wins' | 'merge' | 'manual'>('last_write_wins')
  
  // Initialize WebSocket connection
  const connect = (sessionId: string, gmName: string = 'Game Master') => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      console.log('Already connected to GM collaboration session')
      return
    }
    
    connectionStatus.value = 'connecting'
    currentGM.name = gmName
    currentGM.id = generateGMId()
    
    // In a real implementation, this would connect to your WebSocket server
    const wsUrl = `ws://localhost:3001/gm-session/${sessionId}`
    
    try {
      socket.value = new WebSocket(wsUrl)
      
      socket.value.onopen = () => {
        console.log('Connected to GM collaboration session')
        connectionStatus.value = 'connected'
        isConnected.value = true
        
        // Send initial GM registration
        sendAction({
          type: 'gm_join',
          payload: {
            gmId: currentGM.id,
            gmName: currentGM.name,
            role: currentGM.role
          }
        })
      }
      
      socket.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleIncomingMessage(data)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }
      
      socket.value.onclose = () => {
        console.log('Disconnected from GM collaboration session')
        connectionStatus.value = 'disconnected'
        isConnected.value = false
        
        // Attempt to reconnect after 3 seconds
        setTimeout(() => {
          if (connectionStatus.value === 'disconnected') {
            connect(sessionId, gmName)
          }
        }, 3000)
      }
      
      socket.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        connectionStatus.value = 'error'
        isConnected.value = false
      }
      
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      connectionStatus.value = 'error'
    }
  }
  
  // Disconnect from session
  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }
    connectionStatus.value = 'disconnected'
    isConnected.value = false
    connectedGMs.value = []
  }
  
  // Send action to other GMs
  const broadcastAction = (actionType: GMAction['type'], payload: any) => {
    const action: GMAction = {
      id: generateActionId(),
      type: actionType,
      payload,
      timestamp: Date.now(),
      gmId: currentGM.id,
      gmName: currentGM.name
    }
    
    sendAction(action)
    addToHistory(action)
  }
  
  // Send raw action
  const sendAction = (action: any) => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(action))
    } else {
      // Queue action for when connection is restored
      pendingActions.value.push(action)
    }
  }
  
  // Handle incoming messages
  const handleIncomingMessage = (data: any) => {
    switch (data.type) {
      case 'gm_join':
        handleGMJoin(data.payload)
        break
      case 'gm_leave':
        handleGMLeave(data.payload)
        break
      case 'gm_list':
        connectedGMs.value = data.payload.gms
        break
      case 'action_broadcast':
        handleActionBroadcast(data.payload)
        break
      case 'state_sync':
        handleStateSync(data.payload)
        break
      case 'conflict_detected':
        handleConflict(data.payload)
        break
      default:
        console.log('Unknown message type:', data.type)
    }
  }
  
  // Handle GM joining
  const handleGMJoin = (payload: any) => {
    const existingGM = connectedGMs.value.find(gm => gm.id === payload.gmId)
    if (!existingGM) {
      connectedGMs.value.push({
        id: payload.gmId,
        name: payload.gmName,
        role: payload.role,
        lastSeen: Date.now(),
        isActive: true
      })
      console.log(`GM ${payload.gmName} joined the session`)
    }
  }
  
  // Handle GM leaving
  const handleGMLeave = (payload: any) => {
    const index = connectedGMs.value.findIndex(gm => gm.id === payload.gmId)
    if (index > -1) {
      const gm = connectedGMs.value[index]
      console.log(`GM ${gm.name} left the session`)
      connectedGMs.value.splice(index, 1)
    }
  }
  
  // Handle action broadcast from other GMs
  const handleActionBroadcast = (action: GMAction) => {
    // Don't process our own actions
    if (action.gmId === currentGM.id) return
    
    console.log(`Received action from ${action.gmName}:`, action.type)
    addToHistory(action)
    
    // Apply the action based on conflict resolution strategy
    applyRemoteAction(action)
  }
  
  // Handle state synchronization
  const handleStateSync = (state: TavernState) => {
    console.log('Received state sync from server')
    // This would update the local state to match the server state
    // Implementation depends on your state management system
  }
  
  // Handle conflicts
  const handleConflict = (payload: any) => {
    console.warn('Conflict detected:', payload)
    // Implement conflict resolution based on strategy
    switch (conflictResolution.value) {
      case 'last_write_wins':
        // Accept the latest change
        applyRemoteAction(payload.latestAction)
        break
      case 'merge':
        // Attempt to merge changes
        attemptMerge(payload.conflictingActions)
        break
      case 'manual':
        // Present conflict to user for manual resolution
        presentConflictDialog(payload)
        break
    }
  }
  
  // Apply remote action to local state
  const applyRemoteAction = (action: GMAction) => {
    // This would integrate with your state management
    // For now, just emit events that components can listen to
    const event = new CustomEvent('gm-action-received', {
      detail: action
    })
    window.dispatchEvent(event)
  }
  
  // Attempt to merge conflicting changes
  const attemptMerge = (actions: GMAction[]) => {
    // Simple merge strategy - apply all non-conflicting changes
    actions.forEach(action => {
      if (!hasConflict(action)) {
        applyRemoteAction(action)
      }
    })
  }
  
  // Check if action conflicts with recent local changes
  const hasConflict = (action: GMAction): boolean => {
    // Simple conflict detection based on timing and target
    const recentActions = actionHistory.value.filter(
      a => a.gmId === currentGM.id && 
           Math.abs(a.timestamp - action.timestamp) < 5000 && // Within 5 seconds
           a.type === action.type
    )
    return recentActions.length > 0
  }
  
  // Present conflict dialog to user
  const presentConflictDialog = (payload: any) => {
    // This would show a UI dialog for manual conflict resolution
    console.log('Manual conflict resolution required:', payload)
  }
  
  // Add action to history
  const addToHistory = (action: GMAction) => {
    actionHistory.value.push(action)
    
    // Keep only last 100 actions
    if (actionHistory.value.length > 100) {
      actionHistory.value = actionHistory.value.slice(-100)
    }
  }
  
  // Sync current state with other GMs
  const syncState = (state: TavernState) => {
    sendAction({
      type: 'state_sync',
      payload: state,
      timestamp: Date.now(),
      gmId: currentGM.id
    })
  }
  
  // Utility functions
  const generateGMId = (): string => {
    return `gm_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
  
  const generateActionId = (): string => {
    return `action_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
  
  // Send pending actions when connection is restored
  const sendPendingActions = () => {
    if (socket.value?.readyState === WebSocket.OPEN && pendingActions.value.length > 0) {
      pendingActions.value.forEach(action => {
        socket.value!.send(JSON.stringify(action))
      })
      pendingActions.value = []
    }
  }
  
  // Watch for connection restoration
  watch(isConnected, (connected) => {
    if (connected) {
      sendPendingActions()
    }
  })
  
  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })
  
  return {
    // Connection state
    isConnected: readonly(isConnected),
    connectionStatus: readonly(connectionStatus),
    
    // Collaboration state
    connectedGMs: readonly(connectedGMs),
    currentGM: readonly(currentGM),
    actionHistory: readonly(actionHistory),
    
    // Methods
    connect,
    disconnect,
    broadcastAction,
    syncState,
    
    // Configuration
    conflictResolution
  }
}
