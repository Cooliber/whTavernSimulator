import axios from 'axios'

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching
    config.params = {
      ...config.params,
      _t: Date.now()
    }
    
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`, {
        params: config.params,
        data: config.data
      })
    }
    
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, {
        status: response.status,
        data: response.data
      })
    }
    
    return response
  },
  (error) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      console.error(`❌ API Error ${status}:`, data)
      
      // Handle specific status codes
      switch (status) {
        case 401:
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
          break
          
        case 403:
          // Forbidden
          console.error('Access forbidden')
          break
          
        case 404:
          // Not found
          console.error('Resource not found')
          break
          
        case 429:
          // Rate limited
          console.error('Rate limit exceeded')
          break
          
        case 500:
          // Server error
          console.error('Internal server error')
          break
          
        default:
          console.error('Unknown API error')
      }
      
      // Return formatted error
      return Promise.reject({
        status,
        message: data?.message || data?.error || 'API request failed',
        details: data
      })
      
    } else if (error.request) {
      // Network error
      console.error('❌ Network Error:', error.message)
      return Promise.reject({
        status: 0,
        message: 'Network error - please check your connection',
        details: error
      })
      
    } else {
      // Request setup error
      console.error('❌ Request Setup Error:', error.message)
      return Promise.reject({
        status: -1,
        message: 'Request configuration error',
        details: error
      })
    }
  }
)

// API helper functions
export const api = {
  // Health check
  health: () => apiClient.get('/health'),
  
  // Tavern endpoints
  tavern: {
    getState: () => apiClient.get('/api/tavern/state'),
    generate: () => apiClient.post('/api/tavern/generate'),
    updateState: (state) => apiClient.put('/api/tavern/state', state)
  },
  
  // Agent endpoints
  agents: {
    getAll: () => apiClient.get('/api/agents'),
    getById: (id) => apiClient.get(`/api/agents/${id}`),
    getFactions: () => apiClient.get('/api/agents/factions'),
    executeAction: (agentName, actionType, parameters) => 
      apiClient.post(`/api/agents/${agentName}/action`, {
        action_type: actionType,
        parameters
      }),
    getRelationships: () => apiClient.get('/api/agents/relationships')
  },
  
  // Conversation endpoints
  conversation: {
    start: (participants, topic) => 
      apiClient.post('/api/conversation/start', { participants, topic }),
    getHistory: () => apiClient.get('/api/conversation/history'),
    sendMessage: (message) => apiClient.post('/api/conversation/message', { message })
  },
  
  // Event endpoints
  events: {
    generate: () => apiClient.post('/api/events/generate'),
    getHistory: () => apiClient.get('/api/events/history'),
    getActive: () => apiClient.get('/api/events/active')
  },
  
  // Game Master tools
  gamemaster: {
    generateNPC: (options) => apiClient.post('/api/gamemaster/npc/generate', options),
    generateEncounter: (options) => apiClient.post('/api/gamemaster/encounter/generate', options),
    generateHook: (options) => apiClient.post('/api/gamemaster/hook/generate', options),
    rollTable: (tableName) => apiClient.post('/api/gamemaster/table/roll', { table: tableName })
  }
}

// Export default client for direct use
export { apiClient }
export default apiClient
