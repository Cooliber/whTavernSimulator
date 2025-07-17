/**
 * AI-Powered NPC System for Warhammer Tavern v3
 * Provides intelligent NPCs with memory, personality, and dynamic conversations
 */

export interface NPCPersonality {
  id: string
  name: string
  species: 'human' | 'elf' | 'dwarf' | 'halfling' | 'ogre'
  faction: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs' | 'neutral'
  career: string
  traits: string[]
  mood: 'friendly' | 'neutral' | 'suspicious' | 'hostile' | 'drunk' | 'melancholy'
  interests: string[]
  secrets: string[]
  relationships: Record<string, number> // NPC ID -> relationship score (-100 to 100)
  memoryCapacity: number
  conversationStyle: 'verbose' | 'terse' | 'cryptic' | 'boastful' | 'scholarly'
}

export interface ConversationMemory {
  id: string
  npcId: string
  playerId: string
  timestamp: Date
  topic: string
  sentiment: 'positive' | 'neutral' | 'negative'
  content: string
  importance: number // 1-10
  tags: string[]
}

export interface DialogueOption {
  id: string
  text: string
  type: 'question' | 'statement' | 'threat' | 'bribe' | 'compliment'
  requirements?: {
    reputation?: number
    faction?: string
    items?: string[]
    skills?: string[]
  }
  consequences?: {
    reputation?: number
    relationship?: number
    mood?: NPCPersonality['mood']
    unlocks?: string[]
  }
}

export interface ConversationContext {
  npc: NPCPersonality
  player: {
    id: string
    name: string
    reputation: number
    faction?: string
    items: string[]
    skills: string[]
  }
  location: string
  timeOfDay: 'morning' | 'afternoon' | 'evening' | 'night'
  recentEvents: string[]
  conversationHistory: ConversationMemory[]
}

export const useAINPCSystem = () => {
  // Reactive state
  const npcs = ref<NPCPersonality[]>([])
  const conversationMemories = ref<ConversationMemory[]>([])
  const activeConversation = ref<ConversationContext | null>(null)
  const isGeneratingResponse = ref(false)
  const error = ref<string | null>(null)

  // NPC Templates based on Warhammer Fantasy careers
  const npcTemplates: Partial<NPCPersonality>[] = [
    {
      species: 'human',
      faction: 'empire',
      career: 'Soldier',
      traits: ['brave', 'disciplined', 'loyal'],
      interests: ['warfare', 'empire politics', 'training'],
      conversationStyle: 'terse'
    },
    {
      species: 'dwarf',
      faction: 'dwarfs',
      career: 'Artisan',
      traits: ['stubborn', 'skilled', 'proud'],
      interests: ['craftsmanship', 'grudges', 'ale'],
      conversationStyle: 'boastful'
    },
    {
      species: 'elf',
      faction: 'elves',
      career: 'Scholar',
      traits: ['intelligent', 'aloof', 'patient'],
      interests: ['magic', 'history', 'poetry'],
      conversationStyle: 'scholarly'
    },
    {
      species: 'human',
      faction: 'neutral',
      career: 'Merchant',
      traits: ['greedy', 'cunning', 'social'],
      interests: ['trade', 'gossip', 'profit'],
      conversationStyle: 'verbose'
    }
  ]

  // Generate NPC personality
  const generateNPC = (template?: Partial<NPCPersonality>): NPCPersonality => {
    const baseTemplate = template || npcTemplates[Math.floor(Math.random() * npcTemplates.length)]
    
    return {
      id: `npc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: generateNPCName(baseTemplate.species || 'human'),
      species: baseTemplate.species || 'human',
      faction: baseTemplate.faction || 'neutral',
      career: baseTemplate.career || 'Peasant',
      traits: baseTemplate.traits || ['common'],
      mood: 'neutral',
      interests: baseTemplate.interests || ['local news'],
      secrets: generateSecrets(),
      relationships: {},
      memoryCapacity: 10,
      conversationStyle: baseTemplate.conversationStyle || 'neutral'
    }
  }

  // Generate appropriate names based on species
  const generateNPCName = (species: string): string => {
    const nameDatabase = {
      human: {
        male: ['Magnus', 'Karl', 'Gunther', 'Wilhelm', 'Friedrich'],
        female: ['Katarina', 'Elsa', 'Greta', 'Brunhilde', 'Ingrid']
      },
      dwarf: {
        male: ['Thorek', 'Grimm', 'Borin', 'Kazrik', 'Dugan'],
        female: ['Valka', 'Nala', 'Dura', 'Mira', 'Kera']
      },
      elf: {
        male: ['Eltharion', 'Teclis', 'Alaric', 'Caelynn', 'Silvyr'],
        female: ['Ariel', 'Naestra', 'Elaria', 'Lyralei', 'Araloth']
      },
      halfling: {
        male: ['Bilbo', 'Samwise', 'Milo', 'Bingo', 'Drogo'],
        female: ['Rosie', 'Daisy', 'Poppy', 'Lily', 'Peony']
      }
    }

    const names = nameDatabase[species as keyof typeof nameDatabase] || nameDatabase.human
    const gender = Math.random() > 0.5 ? 'male' : 'female'
    const nameList = names[gender as keyof typeof names]
    
    return nameList[Math.floor(Math.random() * nameList.length)]
  }

  // Generate secrets for NPCs
  const generateSecrets = (): string[] => {
    const secretTemplates = [
      'owes money to a dangerous creditor',
      'witnessed a crime but hasn\'t reported it',
      'has a hidden magical talent',
      'is secretly working for another faction',
      'knows the location of hidden treasure',
      'has a forbidden romance',
      'is related to someone important',
      'committed a crime in the past'
    ]
    
    const numSecrets = Math.floor(Math.random() * 3) + 1
    return secretTemplates
      .sort(() => Math.random() - 0.5)
      .slice(0, numSecrets)
  }

  // AI Response Generation (simplified - would integrate with actual AI service)
  const generateAIResponse = async (context: ConversationContext, playerInput: string): Promise<string> => {
    isGeneratingResponse.value = true
    error.value = null

    try {
      // This would integrate with an actual AI service like OpenAI, Anthropic, etc.
      // For now, we'll use a rule-based system with some randomization
      
      const response = await generateContextualResponse(context, playerInput)
      
      // Store the conversation in memory
      await storeConversationMemory(context.npc.id, context.player.id, playerInput, response)
      
      return response
    } catch (err) {
      error.value = 'Failed to generate AI response'
      console.error('AI Response Error:', err)
      return generateFallbackResponse(context.npc)
    } finally {
      isGeneratingResponse.value = false
    }
  }

  // Generate contextual response based on NPC personality and conversation history
  const generateContextualResponse = async (context: ConversationContext, input: string): Promise<string> => {
    const { npc, player, conversationHistory } = context
    
    // Analyze input sentiment and topic
    const inputAnalysis = analyzeInput(input)
    
    // Get relevant memories
    const relevantMemories = getRelevantMemories(npc.id, player.id, inputAnalysis.topic)
    
    // Build response based on personality, mood, and context
    let response = ''
    
    // Greeting logic
    if (inputAnalysis.isGreeting) {
      response = generateGreeting(npc, player, relevantMemories.length > 0)
    }
    // Question about NPC
    else if (inputAnalysis.isPersonalQuestion) {
      response = generatePersonalResponse(npc, inputAnalysis.topic)
    }
    // Information request
    else if (inputAnalysis.isInformationRequest) {
      response = generateInformationResponse(npc, inputAnalysis.topic, context)
    }
    // Default conversation
    else {
      response = generateDefaultResponse(npc, inputAnalysis, context)
    }

    // Apply personality modifiers
    response = applyPersonalityStyle(response, npc.conversationStyle, npc.mood)
    
    return response
  }

  // Analyze player input to determine intent and topic
  const analyzeInput = (input: string) => {
    const lowerInput = input.toLowerCase()
    
    return {
      isGreeting: /^(hello|hi|greetings|good|hey)/.test(lowerInput),
      isPersonalQuestion: /\b(you|your|yourself)\b/.test(lowerInput),
      isInformationRequest: /\b(what|where|when|who|how|tell me|know about)\b/.test(lowerInput),
      topic: extractTopic(lowerInput),
      sentiment: analyzeSentiment(lowerInput)
    }
  }

  // Extract main topic from input
  const extractTopic = (input: string): string => {
    const topics = ['war', 'trade', 'magic', 'politics', 'weather', 'news', 'rumors', 'family', 'work']
    
    for (const topic of topics) {
      if (input.includes(topic)) {
        return topic
      }
    }
    
    return 'general'
  }

  // Simple sentiment analysis
  const analyzeSentiment = (input: string): 'positive' | 'neutral' | 'negative' => {
    const positiveWords = ['good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic']
    const negativeWords = ['bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate']
    
    const hasPositive = positiveWords.some(word => input.includes(word))
    const hasNegative = negativeWords.some(word => input.includes(word))
    
    if (hasPositive && !hasNegative) return 'positive'
    if (hasNegative && !hasPositive) return 'negative'
    return 'neutral'
  }

  // Generate greeting based on relationship and memory
  const generateGreeting = (npc: NPCPersonality, player: any, hasMetBefore: boolean): string => {
    const greetings = hasMetBefore 
      ? [`Ah, ${player.name}! Good to see you again.`, `Well met again, ${player.name}.`]
      : [`Greetings, stranger.`, `Welcome to our establishment.`, `Good day to you.`]
    
    let greeting = greetings[Math.floor(Math.random() * greetings.length)]
    
    // Add personality flavor
    if (npc.mood === 'drunk') {
      greeting += ' *hiccup*'
    } else if (npc.mood === 'suspicious') {
      greeting += ' What brings you here?'
    }
    
    return greeting
  }

  // Generate personal response about the NPC
  const generatePersonalResponse = (npc: NPCPersonality, topic: string): string => {
    const responses = {
      general: [
        `I'm ${npc.name}, a ${npc.career} by trade.`,
        `Just a simple ${npc.career}, trying to make an honest living.`
      ],
      work: [
        `I've been working as a ${npc.career} for many years now.`,
        `The life of a ${npc.career} isn't easy, but it's honest work.`
      ],
      family: [
        `My family? That's... personal.`,
        `I prefer not to discuss family matters with strangers.`
      ]
    }
    
    const responseList = responses[topic as keyof typeof responses] || responses.general
    return responseList[Math.floor(Math.random() * responseList.length)]
  }

  // Generate information response
  const generateInformationResponse = (npc: NPCPersonality, topic: string, context: ConversationContext): string => {
    // This would be much more sophisticated in a real implementation
    const responses = {
      news: [`I heard there's been trouble on the roads lately.`, `The merchants are talking about strange happenings.`],
      weather: [`The weather's been fair enough.`, `Could use some rain for the crops.`],
      politics: [`Politics? Above my station, I'm afraid.`, `Best not to speak of such things in public.`]
    }
    
    const responseList = responses[topic as keyof typeof responses] || [`I don't know much about that.`]
    return responseList[Math.floor(Math.random() * responseList.length)]
  }

  // Generate default response
  const generateDefaultResponse = (npc: NPCPersonality, analysis: any, context: ConversationContext): string => {
    const defaultResponses = [
      `Interesting point.`,
      `I see.`,
      `That's worth considering.`,
      `Hmm, perhaps.`
    ]
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)]
  }

  // Apply personality style to response
  const applyPersonalityStyle = (response: string, style: NPCPersonality['conversationStyle'], mood: NPCPersonality['mood']): string => {
    let styledResponse = response
    
    switch (style) {
      case 'verbose':
        styledResponse = `Well, you see, ${response.toLowerCase()} And I must say, it's quite fascinating when you think about it.`
        break
      case 'terse':
        styledResponse = response.split('.')[0] + '.'
        break
      case 'boastful':
        styledResponse = `${response} I should know - I'm quite experienced in these matters.`
        break
      case 'scholarly':
        styledResponse = `According to my understanding, ${response.toLowerCase()} This aligns with established knowledge on the subject.`
        break
      case 'cryptic':
        styledResponse = `${response} ...though perhaps there's more to it than meets the eye.`
        break
    }
    
    // Apply mood modifiers
    switch (mood) {
      case 'drunk':
        styledResponse += ' *sways slightly*'
        break
      case 'suspicious':
        styledResponse += ' *eyes you warily*'
        break
      case 'melancholy':
        styledResponse += ' *sighs*'
        break
    }
    
    return styledResponse
  }

  // Generate fallback response for errors
  const generateFallbackResponse = (npc: NPCPersonality): string => {
    const fallbacks = [
      `*${npc.name} seems distracted*`,
      `*${npc.name} mumbles something inaudible*`,
      `*${npc.name} takes a drink and doesn't respond*`
    ]
    
    return fallbacks[Math.floor(Math.random() * fallbacks.length)]
  }

  // Store conversation memory
  const storeConversationMemory = async (npcId: string, playerId: string, input: string, response: string) => {
    const memory: ConversationMemory = {
      id: `memory_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      npcId,
      playerId,
      timestamp: new Date(),
      topic: extractTopic(input.toLowerCase()),
      sentiment: analyzeSentiment(input.toLowerCase()),
      content: `Player: ${input} | NPC: ${response}`,
      importance: calculateImportance(input, response),
      tags: extractTags(input, response)
    }
    
    conversationMemories.value.push(memory)
    
    // Limit memory based on NPC capacity
    const npcMemories = conversationMemories.value.filter(m => m.npcId === npcId)
    const npc = npcs.value.find(n => n.id === npcId)
    
    if (npc && npcMemories.length > npc.memoryCapacity) {
      // Remove least important memories
      const sortedMemories = npcMemories.sort((a, b) => a.importance - b.importance)
      const toRemove = sortedMemories.slice(0, npcMemories.length - npc.memoryCapacity)
      
      conversationMemories.value = conversationMemories.value.filter(
        m => !toRemove.some(r => r.id === m.id)
      )
    }
  }

  // Calculate importance of a conversation
  const calculateImportance = (input: string, response: string): number => {
    let importance = 5 // Base importance
    
    // Increase importance for certain keywords
    const importantKeywords = ['secret', 'treasure', 'danger', 'war', 'magic', 'quest']
    const text = (input + ' ' + response).toLowerCase()
    
    for (const keyword of importantKeywords) {
      if (text.includes(keyword)) {
        importance += 2
      }
    }
    
    return Math.min(importance, 10)
  }

  // Extract tags from conversation
  const extractTags = (input: string, response: string): string[] => {
    const text = (input + ' ' + response).toLowerCase()
    const tags: string[] = []
    
    const tagKeywords = {
      'combat': ['fight', 'battle', 'war', 'weapon', 'armor'],
      'magic': ['spell', 'magic', 'wizard', 'enchant'],
      'trade': ['buy', 'sell', 'trade', 'merchant', 'gold'],
      'quest': ['quest', 'adventure', 'journey', 'mission'],
      'personal': ['family', 'friend', 'love', 'secret']
    }
    
    for (const [tag, keywords] of Object.entries(tagKeywords)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        tags.push(tag)
      }
    }
    
    return tags
  }

  // Get relevant memories for context
  const getRelevantMemories = (npcId: string, playerId: string, topic: string): ConversationMemory[] => {
    return conversationMemories.value
      .filter(m => m.npcId === npcId && m.playerId === playerId)
      .filter(m => m.topic === topic || m.tags.includes(topic))
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 3) // Get top 3 relevant memories
  }

  // Initialize NPCs
  const initializeNPCs = () => {
    const initialNPCs = npcTemplates.map(template => generateNPC(template))
    npcs.value = initialNPCs
  }

  // Start conversation with NPC
  const startConversation = (npcId: string, player: any, location: string = 'tavern'): ConversationContext | null => {
    const npc = npcs.value.find(n => n.id === npcId)
    if (!npc) return null
    
    const context: ConversationContext = {
      npc,
      player,
      location,
      timeOfDay: getCurrentTimeOfDay(),
      recentEvents: [], // Would be populated with recent tavern events
      conversationHistory: getRelevantMemories(npcId, player.id, 'general')
    }
    
    activeConversation.value = context
    return context
  }

  // Get current time of day
  const getCurrentTimeOfDay = (): ConversationContext['timeOfDay'] => {
    const hour = new Date().getHours()
    if (hour < 6) return 'night'
    if (hour < 12) return 'morning'
    if (hour < 18) return 'afternoon'
    if (hour < 22) return 'evening'
    return 'night'
  }

  // End conversation
  const endConversation = () => {
    activeConversation.value = null
  }

  return {
    // State
    npcs: readonly(npcs),
    conversationMemories: readonly(conversationMemories),
    activeConversation: readonly(activeConversation),
    isGeneratingResponse: readonly(isGeneratingResponse),
    error: readonly(error),
    
    // Methods
    generateNPC,
    generateAIResponse,
    startConversation,
    endConversation,
    initializeNPCs,
    storeConversationMemory,
    getRelevantMemories
  }
}
