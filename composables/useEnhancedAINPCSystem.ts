/**
 * Enhanced AI NPC System for Warhammer Tavern v3
 * Integrates unified AI service with 17 distinct Warhammer agents
 * Supports inter-agent conversations and complex relationship dynamics
 */

import { useUnifiedAIService } from './useUnifiedAIService'
import { useWarhammerAgents } from './useWarhammerAgents'
import type { WarhammerAgent } from './useWarhammerAgents'
import type { AIMessage } from './useUnifiedAIService'

export interface AgentConversation {
  id: string
  participants: string[] // Agent IDs
  messages: ConversationMessage[]
  topic: string
  startTime: Date
  lastActivity: Date
  isActive: boolean
  context: Record<string, any>
}

export interface ConversationMessage {
  id: string
  agentId: string
  content: string
  timestamp: Date
  type: 'dialogue' | 'action' | 'thought' | 'system'
  metadata?: {
    emotion?: string
    intention?: string
    targetAgent?: string
    relationshipChange?: number
  }
}

export interface AgentInteraction {
  initiatorId: string
  targetId: string
  type: 'conversation' | 'trade' | 'conflict' | 'cooperation'
  outcome: 'positive' | 'negative' | 'neutral'
  relationshipChange: number
  timestamp: Date
}

export const useEnhancedAINPCSystem = () => {
  const { generateCompletion, isInitialized } = useUnifiedAIService()
  const { agents, getAgentById, getAgentRelationships, updateAgentRelationship } = useWarhammerAgents()

  // Reactive state
  const activeConversations = ref<Map<string, AgentConversation>>(new Map())
  const conversationHistory = ref<AgentConversation[]>([])
  const agentInteractions = ref<AgentInteraction[]>([])
  const currentPlayerConversation = ref<string | null>(null)

  // Initialize the enhanced system
  const initializeEnhancedSystem = async () => {
    console.log('🤖 Initializing Enhanced AI NPC System...')
    
    // Initialize base systems
    if (!isInitialized.value) {
      console.log('⏳ Waiting for AI service initialization...')
    }

    // Set up initial agent states
    initializeAgentStates()
    
    // Start background agent interactions
    startBackgroundInteractions()
    
    console.log('✅ Enhanced AI NPC System initialized with 17 agents')
  }

  // Initialize agent states and relationships
  const initializeAgentStates = () => {
    agents.value.forEach(agent => {
      // Initialize any missing relationships
      if (!agent.relationships.allies) agent.relationships.allies = []
      if (!agent.relationships.rivals) agent.relationships.rivals = []
      if (!agent.relationships.neutral) agent.relationships.neutral = []
    })
  }

  // Start a conversation with a specific agent
  const startPlayerConversation = async (
    agentId: string,
    initialMessage: string,
    context?: Record<string, any>
  ): Promise<string> => {
    const agent = getAgentById(agentId)
    if (!agent) throw new Error(`Agent ${agentId} not found`)

    const conversationId = `player_${agentId}_${Date.now()}`
    
    const conversation: AgentConversation = {
      id: conversationId,
      participants: ['player', agentId],
      messages: [
        {
          id: `msg_${Date.now()}`,
          agentId: 'player',
          content: initialMessage,
          timestamp: new Date(),
          type: 'dialogue'
        }
      ],
      topic: extractTopic(initialMessage),
      startTime: new Date(),
      lastActivity: new Date(),
      isActive: true,
      context: context || {}
    }

    activeConversations.value.set(conversationId, conversation)
    currentPlayerConversation.value = conversationId

    // Generate agent response
    const response = await generateAgentResponse(agent, conversation, context)
    
    // Add agent response to conversation
    conversation.messages.push({
      id: `msg_${Date.now() + 1}`,
      agentId: agentId,
      content: response,
      timestamp: new Date(),
      type: 'dialogue'
    })

    conversation.lastActivity = new Date()

    return response
  }

  // Continue an existing conversation
  const continuePlayerConversation = async (
    conversationId: string,
    message: string,
    context?: Record<string, any>
  ): Promise<string> => {
    const conversation = activeConversations.value.get(conversationId)
    if (!conversation) throw new Error(`Conversation ${conversationId} not found`)

    const agentId = conversation.participants.find(p => p !== 'player')
    if (!agentId) throw new Error('No agent found in conversation')

    const agent = getAgentById(agentId)
    if (!agent) throw new Error(`Agent ${agentId} not found`)

    // Add player message
    conversation.messages.push({
      id: `msg_${Date.now()}`,
      agentId: 'player',
      content: message,
      timestamp: new Date(),
      type: 'dialogue'
    })

    // Generate agent response
    const response = await generateAgentResponse(agent, conversation, context)
    
    // Add agent response
    conversation.messages.push({
      id: `msg_${Date.now() + 1}`,
      agentId: agentId,
      content: response,
      timestamp: new Date(),
      type: 'dialogue'
    })

    conversation.lastActivity = new Date()

    return response
  }

  // Generate agent response using AI service
  const generateAgentResponse = async (
    agent: WarhammerAgent,
    conversation: AgentConversation,
    context?: Record<string, any>
  ): Promise<string> => {
    // Build system prompt based on agent personality
    const systemPrompt = buildAgentSystemPrompt(agent, conversation, context)
    
    // Convert conversation to AI messages
    const messages: AIMessage[] = conversation.messages
      .slice(-10) // Keep last 10 messages for context
      .map(msg => ({
        role: msg.agentId === 'player' ? 'user' : 'assistant',
        content: msg.content,
        timestamp: msg.timestamp
      }))

    try {
      const response = await generateCompletion(messages, {
        systemPrompt,
        maxTokens: 150,
        temperature: 0.8,
        preferredProvider: 'groq' // Prefer Groq for faster responses
      })

      // Process response for agent-specific modifications
      return processAgentResponse(agent, response.content, conversation)
      
    } catch (error) {
      console.error('Error generating agent response:', error)
      
      // Fallback to agent's predefined responses
      return generateFallbackResponse(agent, conversation)
    }
  }

  // Build system prompt for specific agent
  const buildAgentSystemPrompt = (
    agent: WarhammerAgent,
    conversation: AgentConversation,
    context?: Record<string, any>
  ): string => {
    const relationships = getAgentRelationships(agent.id)
    
    return `You are ${agent.name}, a ${agent.species} ${agent.career} in the Warhammer Fantasy world.

PERSONALITY:
- Traits: ${agent.personality.traits.join(', ')}
- Conversation Style: ${agent.personality.conversationStyle}
- Current Mood: ${agent.personality.mood}
- Intelligence: ${agent.personality.intelligence}/10
- Charisma: ${agent.personality.charisma}/10

BACKGROUND:
- Origin: ${agent.background.origin}
- Motivation: ${agent.background.motivation}
- Fears: ${agent.background.fears.join(', ')}
- Goals: ${agent.background.goals.join(', ')}

KNOWLEDGE DOMAINS:
${agent.knowledge.domains.map(domain => `- ${domain}`).join('\n')}

SPEECH PATTERNS:
${agent.conversationPatterns.speechPatterns.map(pattern => `- ${pattern}`).join('\n')}

CATCHPHRASES:
${agent.conversationPatterns.catchphrases.map(phrase => `- "${phrase}"`).join('\n')}

CURRENT CONTEXT:
- Location: The Golden Griffin Tavern
- Time: Evening
- Atmosphere: ${context?.atmosphere || 'Busy tavern evening'}
- Topic: ${conversation.topic}

RELATIONSHIPS:
- Allies: ${relationships?.allies?.map(a => a.name).join(', ') || 'None'}
- Rivals: ${relationships?.rivals?.map(r => r.name).join(', ') || 'None'}

INSTRUCTIONS:
1. Stay in character at all times
2. Use your conversation style (${agent.personality.conversationStyle})
3. Reference your background and knowledge when relevant
4. Show your personality traits through dialogue
5. Keep responses under 100 words
6. Use appropriate Warhammer Fantasy terminology
7. React based on your current mood: ${agent.personality.mood}

Respond as ${agent.name} would, maintaining authenticity to the Warhammer Fantasy setting.`
  }

  // Process and modify agent response
  const processAgentResponse = (
    agent: WarhammerAgent,
    response: string,
    conversation: AgentConversation
  ): string => {
    let processedResponse = response

    // Add speech pattern modifications
    if (agent.personality.conversationStyle === 'terse') {
      processedResponse = processedResponse.split('.')[0] + '.'
    } else if (agent.personality.conversationStyle === 'verbose') {
      // Keep full response for verbose characters
    }

    // Add mood-based modifications
    if (agent.personality.mood === 'drunk') {
      processedResponse = processedResponse.replace(/\b(the|and|but)\b/g, '*hic* $1')
    }

    // Add species-specific speech patterns
    if (agent.species === 'dwarf') {
      processedResponse = processedResponse.replace(/\bby\b/gi, 'by my beard')
    }

    return processedResponse
  }

  // Generate fallback response when AI fails
  const generateFallbackResponse = (
    agent: WarhammerAgent,
    conversation: AgentConversation
  ): string => {
    const lastMessage = conversation.messages[conversation.messages.length - 1]
    const topic = conversation.topic.toLowerCase()

    // Check for topic-specific responses
    const topicResponses = agent.conversationPatterns.topics[topic]
    if (topicResponses && topicResponses.length > 0) {
      return topicResponses[Math.floor(Math.random() * topicResponses.length)]
    }

    // Use catchphrases
    if (agent.conversationPatterns.catchphrases.length > 0) {
      return agent.conversationPatterns.catchphrases[
        Math.floor(Math.random() * agent.conversationPatterns.catchphrases.length)
      ]
    }

    return "Interesting. Tell me more about that."
  }

  // Start inter-agent conversations
  const startAgentConversation = async (
    agentId1: string,
    agentId2: string,
    topic: string
  ): Promise<AgentConversation> => {
    const agent1 = getAgentById(agentId1)
    const agent2 = getAgentById(agentId2)
    
    if (!agent1 || !agent2) {
      throw new Error('One or both agents not found')
    }

    const conversationId = `agents_${agentId1}_${agentId2}_${Date.now()}`
    
    const conversation: AgentConversation = {
      id: conversationId,
      participants: [agentId1, agentId2],
      messages: [],
      topic,
      startTime: new Date(),
      lastActivity: new Date(),
      isActive: true,
      context: { type: 'inter-agent' }
    }

    // Generate initial exchange
    const greeting1 = generateAgentGreeting(agent1, agent2, topic)
    const greeting2 = generateAgentGreeting(agent2, agent1, topic)

    conversation.messages.push(
      {
        id: `msg_${Date.now()}`,
        agentId: agentId1,
        content: greeting1,
        timestamp: new Date(),
        type: 'dialogue'
      },
      {
        id: `msg_${Date.now() + 1}`,
        agentId: agentId2,
        content: greeting2,
        timestamp: new Date(),
        type: 'dialogue'
      }
    )

    activeConversations.value.set(conversationId, conversation)
    
    return conversation
  }

  // Generate greeting between agents
  const generateAgentGreeting = (
    speaker: WarhammerAgent,
    target: WarhammerAgent,
    topic: string
  ): string => {
    const relationship = getRelationshipType(speaker.id, target.id)
    
    if (relationship === 'allies') {
      return speaker.conversationPatterns.greetings[0] || `Greetings, ${target.name}!`
    } else if (relationship === 'rivals') {
      return `${target.name}... what brings you here?`
    } else {
      return speaker.conversationPatterns.greetings[0] || `Good evening, ${target.name}.`
    }
  }

  // Get relationship type between two agents
  const getRelationshipType = (agentId1: string, agentId2: string): 'allies' | 'rivals' | 'neutral' => {
    const agent1 = getAgentById(agentId1)
    if (!agent1) return 'neutral'

    if (agent1.relationships.allies.includes(agentId2)) return 'allies'
    if (agent1.relationships.rivals.includes(agentId2)) return 'rivals'
    return 'neutral'
  }

  // Start background agent interactions
  const startBackgroundInteractions = () => {
    // Simulate random agent interactions every few minutes
    setInterval(() => {
      if (Math.random() < 0.3) { // 30% chance every interval
        simulateRandomInteraction()
      }
    }, 2 * 60 * 1000) // Every 2 minutes
  }

  // Simulate random agent interaction
  const simulateRandomInteraction = async () => {
    const availableAgents = agents.value.filter(a => a.role !== 'player')
    if (availableAgents.length < 2) return

    const agent1 = availableAgents[Math.floor(Math.random() * availableAgents.length)]
    const agent2 = availableAgents[Math.floor(Math.random() * availableAgents.length)]
    
    if (agent1.id === agent2.id) return

    const topics = ['weather', 'business', 'rumors', 'politics', 'trade']
    const topic = topics[Math.floor(Math.random() * topics.length)]

    try {
      await startAgentConversation(agent1.id, agent2.id, topic)
      console.log(`🗣️ Background conversation started: ${agent1.name} and ${agent2.name} discussing ${topic}`)
    } catch (error) {
      console.error('Error in background interaction:', error)
    }
  }

  // Extract topic from message
  const extractTopic = (message: string): string => {
    const lowerMessage = message.toLowerCase()
    
    if (lowerMessage.includes('drink') || lowerMessage.includes('ale')) return 'drinks'
    if (lowerMessage.includes('news') || lowerMessage.includes('rumor')) return 'news'
    if (lowerMessage.includes('trade') || lowerMessage.includes('buy')) return 'trade'
    if (lowerMessage.includes('weather')) return 'weather'
    if (lowerMessage.includes('magic')) return 'magic'
    if (lowerMessage.includes('war') || lowerMessage.includes('battle')) return 'war'
    
    return 'general'
  }

  // End conversation
  const endConversation = (conversationId: string) => {
    const conversation = activeConversations.value.get(conversationId)
    if (conversation) {
      conversation.isActive = false
      conversationHistory.value.push(conversation)
      activeConversations.value.delete(conversationId)
      
      if (currentPlayerConversation.value === conversationId) {
        currentPlayerConversation.value = null
      }
    }
  }

  // Get conversation history for an agent
  const getAgentConversationHistory = (agentId: string): AgentConversation[] => {
    return conversationHistory.value.filter(conv => 
      conv.participants.includes(agentId)
    )
  }

  // Get active conversations
  const getActiveConversations = (): AgentConversation[] => {
    return Array.from(activeConversations.value.values())
  }

  return {
    // State
    activeConversations: readonly(activeConversations),
    conversationHistory: readonly(conversationHistory),
    currentPlayerConversation: readonly(currentPlayerConversation),
    
    // Methods
    initializeEnhancedSystem,
    startPlayerConversation,
    continuePlayerConversation,
    startAgentConversation,
    endConversation,
    getAgentConversationHistory,
    getActiveConversations,
    simulateRandomInteraction
  }
}
