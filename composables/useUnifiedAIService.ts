/**
 * Unified AI Service for Warhammer Tavern v3
 * Supports multiple AI providers: Groq, Cerebras, and fallback systems
 */

export interface AIProvider {
  name: 'groq' | 'cerebras' | 'fallback'
  apiKey?: string
  baseUrl?: string
  model: string
  maxTokens?: number
  temperature?: number
  isAvailable: boolean
  rateLimitRemaining?: number
  rateLimitReset?: Date
}

export interface AIMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
  timestamp?: Date
}

export interface AIResponse {
  content: string
  provider: string
  model: string
  usage?: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
  finishReason?: string
  error?: string
}

export interface AIServiceConfig {
  providers: AIProvider[]
  fallbackOrder: string[]
  retryAttempts: number
  timeoutMs: number
  enableRateLimiting: boolean
  enableCaching: boolean
}

export const useUnifiedAIService = () => {
  // Reactive state
  const config = ref<AIServiceConfig>({
    providers: [
      {
        name: 'groq',
        apiKey: '',
        baseUrl: 'https://api.groq.com/openai/v1',
        model: 'llama-3.3-70b-versatile',
        maxTokens: 1024,
        temperature: 0.7,
        isAvailable: false
      },
      {
        name: 'cerebras',
        apiKey: '',
        baseUrl: 'https://api.cerebras.ai/v1',
        model: 'llama-4-scout-17b-16e-instruct',
        maxTokens: 1024,
        temperature: 0.7,
        isAvailable: false
      },
      {
        name: 'fallback',
        model: 'local-fallback',
        maxTokens: 512,
        temperature: 0.8,
        isAvailable: true
      }
    ],
    fallbackOrder: ['groq', 'cerebras', 'fallback'],
    retryAttempts: 3,
    timeoutMs: 30000,
    enableRateLimiting: true,
    enableCaching: true
  })

  const isInitialized = ref(false)
  const currentProvider = ref<AIProvider | null>(null)
  const responseCache = ref<Map<string, { response: AIResponse; timestamp: Date }>>(new Map())
  const rateLimitTracker = ref<Map<string, { count: number; resetTime: Date }>>(new Map())

  // Initialize AI service
  const initializeAIService = async () => {
    try {
      // Load API keys from environment or runtime config
      await loadAPIKeys()
      
      // Test provider availability
      await testProviderAvailability()
      
      isInitialized.value = true
      console.log('✅ Unified AI Service initialized successfully')
    } catch (error) {
      console.error('❌ Failed to initialize AI Service:', error)
      // Fallback to local system
      config.value.providers.find(p => p.name === 'fallback')!.isAvailable = true
      isInitialized.value = true
    }
  }

  // Load API keys from environment or configuration
  const loadAPIKeys = async () => {
    // In a real implementation, these would come from secure environment variables
    // For demo purposes, we'll use placeholder values
    const groqProvider = config.value.providers.find(p => p.name === 'groq')
    const cerebrasProvider = config.value.providers.find(p => p.name === 'cerebras')
    
    if (groqProvider) {
      groqProvider.apiKey = process.env.GROQ_API_KEY || ''
    }
    
    if (cerebrasProvider) {
      cerebrasProvider.apiKey = process.env.CEREBRAS_API_KEY || ''
    }
  }

  // Test availability of AI providers
  const testProviderAvailability = async () => {
    for (const provider of config.value.providers) {
      if (provider.name === 'fallback') continue
      
      try {
        const isAvailable = await testProvider(provider)
        provider.isAvailable = isAvailable
        
        if (isAvailable) {
          console.log(`✅ ${provider.name} provider is available`)
        } else {
          console.log(`⚠️ ${provider.name} provider is not available`)
        }
      } catch (error) {
        console.error(`❌ Error testing ${provider.name}:`, error)
        provider.isAvailable = false
      }
    }
  }

  // Test individual provider
  const testProvider = async (provider: AIProvider): Promise<boolean> => {
    if (!provider.apiKey) return false
    
    try {
      const testMessage: AIMessage[] = [
        { role: 'user', content: 'Test connection. Respond with "OK".' }
      ]
      
      const response = await callProvider(provider, testMessage)
      return response.content.toLowerCase().includes('ok')
    } catch (error) {
      return false
    }
  }

  // Main AI completion function
  const generateCompletion = async (
    messages: AIMessage[],
    options?: {
      preferredProvider?: string
      maxTokens?: number
      temperature?: number
      systemPrompt?: string
    }
  ): Promise<AIResponse> => {
    if (!isInitialized.value) {
      await initializeAIService()
    }

    // Add system prompt if provided
    if (options?.systemPrompt) {
      messages = [
        { role: 'system', content: options.systemPrompt },
        ...messages
      ]
    }

    // Check cache first
    if (config.value.enableCaching) {
      const cacheKey = generateCacheKey(messages, options)
      const cached = responseCache.value.get(cacheKey)
      
      if (cached && isValidCache(cached.timestamp)) {
        return { ...cached.response, content: cached.response.content + ' [cached]' }
      }
    }

    // Determine provider order
    const providerOrder = options?.preferredProvider 
      ? [options.preferredProvider, ...config.value.fallbackOrder.filter(p => p !== options.preferredProvider)]
      : config.value.fallbackOrder

    let lastError: Error | null = null

    // Try providers in order
    for (const providerName of providerOrder) {
      const provider = config.value.providers.find(p => p.name === providerName)
      
      if (!provider || !provider.isAvailable) continue

      // Check rate limits
      if (config.value.enableRateLimiting && isRateLimited(provider)) {
        console.log(`⏳ Rate limited for ${provider.name}, trying next provider`)
        continue
      }

      try {
        const response = await callProviderWithRetry(provider, messages, options)
        
        // Cache successful response
        if (config.value.enableCaching) {
          const cacheKey = generateCacheKey(messages, options)
          responseCache.value.set(cacheKey, {
            response,
            timestamp: new Date()
          })
        }

        // Update rate limit tracking
        updateRateLimitTracking(provider)
        
        currentProvider.value = provider
        return response
        
      } catch (error) {
        console.error(`❌ Error with ${provider.name}:`, error)
        lastError = error as Error
        
        // Mark provider as temporarily unavailable if it's a serious error
        if (isSeriousError(error)) {
          provider.isAvailable = false
          setTimeout(() => {
            provider.isAvailable = true
          }, 5 * 60 * 1000) // Re-enable after 5 minutes
        }
      }
    }

    // If all providers failed, use fallback
    return generateFallbackResponse(messages, lastError)
  }

  // Call provider with retry logic
  const callProviderWithRetry = async (
    provider: AIProvider,
    messages: AIMessage[],
    options?: any
  ): Promise<AIResponse> => {
    let lastError: Error | null = null
    
    for (let attempt = 1; attempt <= config.value.retryAttempts; attempt++) {
      try {
        return await callProvider(provider, messages, options)
      } catch (error) {
        lastError = error as Error
        
        if (attempt < config.value.retryAttempts) {
          const delay = Math.pow(2, attempt) * 1000 // Exponential backoff
          await new Promise(resolve => setTimeout(resolve, delay))
        }
      }
    }
    
    throw lastError
  }

  // Call specific AI provider
  const callProvider = async (
    provider: AIProvider,
    messages: AIMessage[],
    options?: any
  ): Promise<AIResponse> => {
    switch (provider.name) {
      case 'groq':
        return await callGroqAPI(provider, messages, options)
      case 'cerebras':
        return await callCerebrasAPI(provider, messages, options)
      case 'fallback':
        return await callFallbackSystem(provider, messages, options)
      default:
        throw new Error(`Unknown provider: ${provider.name}`)
    }
  }

  // Groq API implementation
  const callGroqAPI = async (
    provider: AIProvider,
    messages: AIMessage[],
    options?: any
  ): Promise<AIResponse> => {
    const response = await fetch(`${provider.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${provider.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: provider.model,
        messages: messages.map(m => ({ role: m.role, content: m.content })),
        max_tokens: options?.maxTokens || provider.maxTokens,
        temperature: options?.temperature || provider.temperature,
        stream: false
      })
    })

    if (!response.ok) {
      throw new Error(`Groq API error: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    
    return {
      content: data.choices[0].message.content,
      provider: 'groq',
      model: provider.model,
      usage: data.usage,
      finishReason: data.choices[0].finish_reason
    }
  }

  // Cerebras API implementation
  const callCerebrasAPI = async (
    provider: AIProvider,
    messages: AIMessage[],
    options?: any
  ): Promise<AIResponse> => {
    const response = await fetch(`${provider.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${provider.apiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': 'Warhammer-Tavern-v3/1.0'
      },
      body: JSON.stringify({
        model: provider.model,
        messages: messages.map(m => ({ role: m.role, content: m.content })),
        max_tokens: options?.maxTokens || provider.maxTokens,
        temperature: options?.temperature || provider.temperature,
        stream: false
      })
    })

    if (!response.ok) {
      throw new Error(`Cerebras API error: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    
    return {
      content: data.choices[0].message.content,
      provider: 'cerebras',
      model: provider.model,
      usage: data.usage,
      finishReason: data.choices[0].finish_reason
    }
  }

  // Fallback system implementation
  const callFallbackSystem = async (
    provider: AIProvider,
    messages: AIMessage[],
    options?: any
  ): Promise<AIResponse> => {
    // Simple rule-based fallback system
    const lastMessage = messages[messages.length - 1]
    const content = lastMessage.content.toLowerCase()
    
    let response = ''
    
    if (content.includes('hello') || content.includes('greetings')) {
      response = 'Greetings, traveler. Welcome to our humble establishment.'
    } else if (content.includes('weather')) {
      response = 'The weather has been fair, though I hear storms approach from the north.'
    } else if (content.includes('news') || content.includes('rumors')) {
      response = 'I\'ve heard whispers of strange happenings in the countryside. Best to stay close to town.'
    } else if (content.includes('drink') || content.includes('ale')) {
      response = 'Our ale is the finest in the region. Brewed with care and aged to perfection.'
    } else {
      response = 'Interesting. Tell me more about that, friend.'
    }
    
    return {
      content: response,
      provider: 'fallback',
      model: 'local-fallback'
    }
  }

  // Generate fallback response when all providers fail
  const generateFallbackResponse = (messages: AIMessage[], error: Error | null): AIResponse => {
    return {
      content: '*The character seems distracted and doesn\'t respond clearly*',
      provider: 'fallback',
      model: 'error-fallback',
      error: error?.message || 'All AI providers unavailable'
    }
  }

  // Utility functions
  const generateCacheKey = (messages: AIMessage[], options?: any): string => {
    const key = JSON.stringify({ messages, options })
    return btoa(key).slice(0, 32) // Simple hash
  }

  const isValidCache = (timestamp: Date): boolean => {
    const cacheMaxAge = 5 * 60 * 1000 // 5 minutes
    return Date.now() - timestamp.getTime() < cacheMaxAge
  }

  const isRateLimited = (provider: AIProvider): boolean => {
    const tracker = rateLimitTracker.value.get(provider.name)
    if (!tracker) return false
    
    if (Date.now() > tracker.resetTime.getTime()) {
      rateLimitTracker.value.delete(provider.name)
      return false
    }
    
    return tracker.count >= 100 // Simple rate limit
  }

  const updateRateLimitTracking = (provider: AIProvider) => {
    const now = new Date()
    const resetTime = new Date(now.getTime() + 60 * 1000) // Reset every minute
    
    const tracker = rateLimitTracker.value.get(provider.name) || { count: 0, resetTime }
    tracker.count++
    
    rateLimitTracker.value.set(provider.name, tracker)
  }

  const isSeriousError = (error: any): boolean => {
    const errorMessage = error?.message || ''
    return errorMessage.includes('401') || errorMessage.includes('403') || errorMessage.includes('500')
  }

  // Get provider status
  const getProviderStatus = () => {
    return config.value.providers.map(provider => ({
      name: provider.name,
      isAvailable: provider.isAvailable,
      model: provider.model,
      rateLimitRemaining: provider.rateLimitRemaining,
      isCurrent: currentProvider.value?.name === provider.name
    }))
  }

  // Clear cache
  const clearCache = () => {
    responseCache.value.clear()
  }

  // Update provider configuration
  const updateProviderConfig = (providerName: string, updates: Partial<AIProvider>) => {
    const provider = config.value.providers.find(p => p.name === providerName)
    if (provider) {
      Object.assign(provider, updates)
    }
  }

  return {
    // State
    config: readonly(config),
    isInitialized: readonly(isInitialized),
    currentProvider: readonly(currentProvider),
    
    // Methods
    initializeAIService,
    generateCompletion,
    getProviderStatus,
    clearCache,
    updateProviderConfig,
    testProviderAvailability
  }
}
