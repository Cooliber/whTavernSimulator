import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

// API client
import { apiClient } from '@utils/apiClient'

const initialState = {
  // Application state
  isInitialized: false,
  isLoading: false,
  error: null,
  
  // Theme and UI
  theme: 'dark',
  sidebarOpen: true,
  settingsOpen: false,
  
  // Tavern state
  tavern: {
    name: '',
    reputation: 75,
    tension: 25,
    wealth: 1250,
    activeCharacters: [],
    currentEvents: [],
    conversationHistory: []
  },
  
  // Agents state
  agents: [],
  factions: {},
  agentRelationships: {},
  
  // Performance settings
  performance: {
    quality: 'high',
    particlesEnabled: true,
    animationsEnabled: true,
    audioEnabled: true,
    spatialAudio: true
  },
  
  // User preferences
  preferences: {
    autoCamera: true,
    reducedMotion: false,
    masterVolume: 70,
    musicVolume: 50,
    sfxVolume: 80,
    cameraSensitivity: 1.0
  }
}

export const useAppStore = create()(
  devtools(
    persist(
      immer((set, get) => ({
        ...initialState,
        
        // Actions
        initialize: async () => {
          set((state) => {
            state.isLoading = true
            state.error = null
          })
          
          try {
            // Check API health
            const healthResponse = await apiClient.get('/health')
            
            if (healthResponse.data.status !== 'healthy') {
              throw new Error('Backend services not ready')
            }
            
            // Load initial tavern state
            const tavernResponse = await apiClient.get('/api/tavern/state')
            
            // Load agents
            const agentsResponse = await apiClient.get('/api/agents')
            
            // Load factions
            const factionsResponse = await apiClient.get('/api/agents/factions')
            
            set((state) => {
              state.tavern = tavernResponse.data
              state.agents = agentsResponse.data.agents
              state.factions = factionsResponse.data.factions
              state.isInitialized = true
              state.isLoading = false
            })
            
          } catch (error) {
            console.error('Initialization failed:', error)
            set((state) => {
              state.error = error
              state.isLoading = false
            })
          }
        },
        
        // Tavern actions
        updateTavernState: (newState) => {
          set((state) => {
            Object.assign(state.tavern, newState)
          })
        },
        
        generateNewTavern: async () => {
          try {
            await apiClient.post('/api/tavern/generate')
            // State will be updated via WebSocket
          } catch (error) {
            console.error('Failed to generate new tavern:', error)
          }
        },
        
        // Agent actions
        updateAgents: (agents) => {
          set((state) => {
            state.agents = agents
          })
        },
        
        updateAgentRelationships: (relationships) => {
          set((state) => {
            state.agentRelationships = relationships
          })
        },
        
        executeAgentAction: async (agentName, actionType, parameters = {}) => {
          try {
            await apiClient.post(`/api/agents/${agentName}/action`, {
              action_type: actionType,
              parameters
            })
          } catch (error) {
            console.error('Failed to execute agent action:', error)
          }
        },
        
        startConversation: async (participants, topic = 'general') => {
          try {
            await apiClient.post('/api/conversation/start', {
              participants,
              topic
            })
          } catch (error) {
            console.error('Failed to start conversation:', error)
          }
        },
        
        // Event actions
        generateEvent: async () => {
          try {
            await apiClient.post('/api/events/generate')
          } catch (error) {
            console.error('Failed to generate event:', error)
          }
        },
        
        // UI actions
        setTheme: (theme) => {
          set((state) => {
            state.theme = theme
          })
        },
        
        toggleSidebar: () => {
          set((state) => {
            state.sidebarOpen = !state.sidebarOpen
          })
        },
        
        openSettings: () => {
          set((state) => {
            state.settingsOpen = true
          })
        },
        
        closeSettings: () => {
          set((state) => {
            state.settingsOpen = false
          })
        },
        
        // Performance actions
        updatePerformance: (settings) => {
          set((state) => {
            Object.assign(state.performance, settings)
          })
        },
        
        // Preferences actions
        updatePreferences: (preferences) => {
          set((state) => {
            Object.assign(state.preferences, preferences)
          })
        },
        
        // Error handling
        setError: (error) => {
          set((state) => {
            state.error = error
          })
        },
        
        clearError: () => {
          set((state) => {
            state.error = null
          })
        },
        
        // Reset actions
        reset: () => {
          set((state) => {
            Object.assign(state, initialState)
          })
        },
        
        resetToDefaults: () => {
          set((state) => {
            state.performance = initialState.performance
            state.preferences = initialState.preferences
          })
        }
      })),
      {
        name: 'warhammer-tavern-app',
        partialize: (state) => ({
          theme: state.theme,
          performance: state.performance,
          preferences: state.preferences,
          sidebarOpen: state.sidebarOpen
        })
      }
    ),
    {
      name: 'warhammer-tavern-app'
    }
  )
)

// Selectors for better performance
export const useAppSelectors = {
  tavern: () => useAppStore((state) => state.tavern),
  agents: () => useAppStore((state) => state.agents),
  factions: () => useAppStore((state) => state.factions),
  theme: () => useAppStore((state) => state.theme),
  performance: () => useAppStore((state) => state.performance),
  preferences: () => useAppStore((state) => state.preferences),
  isLoading: () => useAppStore((state) => state.isLoading),
  error: () => useAppStore((state) => state.error)
}
