<template>
  <div class="npc-conversation card-enhanced max-w-4xl mx-auto">
    <!-- Conversation Header -->
    <div class="conversation-header flex items-center justify-between p-6 border-b border-border/30">
      <div class="npc-info flex items-center space-x-4">
        <div class="npc-avatar">
          <OptimizedImage
            :src="`/avatars/${npc.species}_${npc.faction}.webp`"
            :alt="`${npc.name} avatar`"
            :faction="npc.faction as any"
            container-class="w-16 h-16 rounded-full"
            :show-placeholder="true"
          />
        </div>
        <div>
          <h3 class="font-medieval text-xl text-foreground">{{ npc.name }}</h3>
          <p class="text-muted-foreground font-sharp">{{ npc.career }} • {{ npc.species }}</p>
          <div class="flex items-center space-x-2 mt-1">
            <span 
              :class="[
                'mood-indicator text-xs px-2 py-1 rounded-full font-sharp',
                getMoodClass(npc.mood)
              ]"
            >
              {{ npc.mood }}
            </span>
            <span 
              :class="[
                'faction-badge text-xs px-2 py-1 rounded-full font-sharp',
                getFactionClass(npc.faction)
              ]"
            >
              {{ npc.faction }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="conversation-controls">
        <button @click="endConversation" class="btn-enhanced text-sm">
          <Icon name="x" class="w-4 h-4 mr-2" />
          End Conversation
        </button>
      </div>
    </div>

    <!-- Conversation History -->
    <div class="conversation-history p-6 max-h-96 overflow-y-auto space-y-4">
      <div
        v-for="message in conversationHistory"
        :key="message.id"
        :class="[
          'message flex',
          message.speaker === 'player' ? 'justify-end' : 'justify-start'
        ]"
      >
        <div
          :class="[
            'message-bubble max-w-xs lg:max-w-md px-4 py-3 rounded-lg',
            message.speaker === 'player' 
              ? 'bg-primary text-primary-foreground ml-12' 
              : 'bg-card text-card-foreground mr-12'
          ]"
        >
          <div class="message-content font-sharp text-sm">
            {{ message.content }}
          </div>
          <div class="message-timestamp text-xs opacity-75 mt-1">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>
      </div>
      
      <!-- AI Response Loading -->
      <div v-if="isGeneratingResponse" class="message flex justify-start">
        <div class="message-bubble bg-card text-card-foreground mr-12 px-4 py-3 rounded-lg">
          <div class="flex items-center space-x-2">
            <div class="animate-spin w-4 h-4 border-2 border-primary border-t-transparent rounded-full"></div>
            <span class="font-sharp text-sm">{{ npc.name }} is thinking...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Conversation Input -->
    <div class="conversation-input p-6 border-t border-border/30">
      <!-- Quick Response Options -->
      <div v-if="quickResponses.length > 0" class="quick-responses mb-4">
        <h4 class="font-medieval text-sm text-muted-foreground mb-2">Quick Responses:</h4>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="response in quickResponses"
            :key="response.id"
            @click="sendQuickResponse(response)"
            :disabled="!canUseResponse(response)"
            :class="[
              'quick-response-btn px-3 py-2 rounded-lg text-sm font-sharp transition-all duration-200',
              canUseResponse(response)
                ? 'bg-secondary/20 text-secondary hover:bg-secondary/30'
                : 'bg-muted/10 text-muted-foreground cursor-not-allowed'
            ]"
          >
            {{ response.text }}
            <span v-if="response.requirements" class="ml-1 text-xs opacity-75">
              ({{ getRequirementText(response.requirements) }})
            </span>
          </button>
        </div>
      </div>

      <!-- Text Input -->
      <div class="input-area flex space-x-3">
        <div class="flex-1">
          <textarea
            v-model="playerInput"
            @keydown.enter.prevent="sendMessage"
            placeholder="Type your response..."
            :disabled="isGeneratingResponse"
            class="w-full px-4 py-3 bg-card border border-border rounded-lg resize-none font-sharp text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            rows="3"
          ></textarea>
        </div>
        <div class="flex flex-col space-y-2">
          <button
            @click="sendMessage"
            :disabled="!playerInput.trim() || isGeneratingResponse"
            class="btn-enhanced px-6 py-3"
          >
            <Icon name="send" class="w-4 h-4" />
          </button>
          <button
            @click="showConversationOptions = !showConversationOptions"
            class="btn-enhanced px-6 py-3 bg-secondary/90 hover:bg-secondary"
          >
            <Icon name="settings" class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Conversation Options -->
      <div v-if="showConversationOptions" class="conversation-options mt-4 p-4 bg-card/50 rounded-lg">
        <h4 class="font-medieval text-sm text-foreground mb-3">Conversation Style:</h4>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
          <button
            v-for="style in conversationStyles"
            :key="style.id"
            @click="setConversationStyle(style.id)"
            :class="[
              'style-btn px-3 py-2 rounded text-xs font-sharp transition-all duration-200',
              currentStyle === style.id
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted/20 text-muted-foreground hover:bg-muted/30'
            ]"
          >
            {{ style.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Relationship Status -->
    <div class="relationship-status p-4 bg-card/30 border-t border-border/30">
      <div class="flex items-center justify-between">
        <div class="relationship-info">
          <span class="font-medieval text-sm text-foreground">Relationship: </span>
          <span :class="getRelationshipClass(relationshipLevel)">
            {{ getRelationshipText(relationshipLevel) }}
          </span>
        </div>
        <div class="conversation-stats flex space-x-4 text-xs text-muted-foreground">
          <span>Conversations: {{ conversationCount }}</span>
          <span>Trust: {{ trustLevel }}/100</span>
          <span>Influence: {{ influenceLevel }}/100</span>
        </div>
      </div>
      
      <!-- Relationship Progress Bar -->
      <div class="relationship-progress mt-2">
        <div class="w-full bg-muted/20 rounded-full h-2">
          <div 
            class="bg-gradient-to-r from-primary to-accent h-2 rounded-full transition-all duration-500"
            :style="{ width: `${Math.max(0, (relationshipLevel + 100) / 2)}%` }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ConversationMessage {
  id: string
  speaker: 'player' | 'npc'
  content: string
  timestamp: Date
  style?: string
}

interface QuickResponse {
  id: string
  text: string
  type: 'question' | 'statement' | 'compliment' | 'threat' | 'bribe'
  requirements?: {
    reputation?: number
    faction?: string
    items?: string[]
    skills?: string[]
  }
}

interface ConversationProps {
  npc: any // NPCPersonality from the composable
  player: any
}

const props = defineProps<ConversationProps>()
const emit = defineEmits<{
  endConversation: []
  messagesSent: [count: number]
}>()

// Composables
const { generateAIResponse, isGeneratingResponse } = useAINPCSystem()
const { playerReputation } = useInteractiveTavernSystems()
const { strengthenConnection } = useEnhancedUserEngagement()
const {
  startPlayerConversation,
  continuePlayerConversation,
  currentPlayerConversation
} = useEnhancedAINPCSystem()
const { getAgentById } = useWarhammerAgents()

// Reactive state
const playerInput = ref('')
const conversationHistory = ref<ConversationMessage[]>([])
const showConversationOptions = ref(false)
const currentStyle = ref('friendly')
const relationshipLevel = ref(0)
const trustLevel = ref(50)
const influenceLevel = ref(25)
const conversationCount = ref(1)

// Conversation styles
const conversationStyles = [
  { id: 'friendly', name: 'Friendly' },
  { id: 'formal', name: 'Formal' },
  { id: 'casual', name: 'Casual' },
  { id: 'intimidating', name: 'Intimidating' }
]

// Quick responses based on NPC personality and context
const quickResponses = computed<QuickResponse[]>(() => {
  const responses: QuickResponse[] = [
    {
      id: 'greeting',
      text: 'How are you today?',
      type: 'question'
    },
    {
      id: 'compliment',
      text: 'You seem like an interesting person.',
      type: 'compliment'
    },
    {
      id: 'ask_news',
      text: 'Any interesting news lately?',
      type: 'question'
    },
    {
      id: 'ask_work',
      text: 'Tell me about your work.',
      type: 'question'
    }
  ]

  // Add faction-specific responses
  if (props.npc.faction === 'empire') {
    responses.push({
      id: 'empire_loyalty',
      text: 'For the Empire!',
      type: 'statement',
      requirements: { faction: 'empire' }
    })
  }

  // Add reputation-based responses
  if (playerReputation.value.overall >= 25) {
    responses.push({
      id: 'reputation_question',
      text: 'I hear you\'re well-regarded around here.',
      type: 'statement'
    })
  }

  return responses
})

// Methods
const sendMessage = async () => {
  if (!playerInput.value.trim() || isGeneratingResponse.value) return

  const message: ConversationMessage = {
    id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    speaker: 'player',
    content: playerInput.value.trim(),
    timestamp: new Date(),
    style: currentStyle.value
  }

  conversationHistory.value.push(message)
  const userMessage = playerInput.value.trim()
  playerInput.value = ''

  // Generate AI response
  try {
    const context = {
      npc: props.npc,
      player: props.player,
      location: 'tavern',
      timeOfDay: getCurrentTimeOfDay(),
      recentEvents: [],
      conversationHistory: []
    }

    const aiResponse = await generateAIResponse(context, userMessage)
    
    const aiMessage: ConversationMessage = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      speaker: 'npc',
      content: aiResponse,
      timestamp: new Date()
    }

    conversationHistory.value.push(aiMessage)
    
    // Update relationship based on conversation
    updateRelationship(userMessage, aiResponse)
    
  } catch (error) {
    console.error('Failed to generate AI response:', error)
    
    const errorMessage: ConversationMessage = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      speaker: 'npc',
      content: `*${props.npc.name} seems distracted and doesn't respond*`,
      timestamp: new Date()
    }
    
    conversationHistory.value.push(errorMessage)
  }

  // Scroll to bottom
  nextTick(() => {
    const historyElement = document.querySelector('.conversation-history')
    if (historyElement) {
      historyElement.scrollTop = historyElement.scrollHeight
    }
  })
}

const sendQuickResponse = (response: QuickResponse) => {
  playerInput.value = response.text
  sendMessage()
}

const canUseResponse = (response: QuickResponse): boolean => {
  if (!response.requirements) return true
  
  const req = response.requirements
  
  if (req.reputation && playerReputation.value.overall < req.reputation) return false
  if (req.faction && props.player.faction !== req.faction) return false
  
  return true
}

const getRequirementText = (requirements: QuickResponse['requirements']): string => {
  if (!requirements) return ''
  
  const parts = []
  if (requirements.reputation) parts.push(`Rep: ${requirements.reputation}`)
  if (requirements.faction) parts.push(requirements.faction)
  
  return parts.join(', ')
}

const setConversationStyle = (style: string) => {
  currentStyle.value = style
}

const updateRelationship = (playerMessage: string, npcResponse: string) => {
  // Simple relationship calculation based on message sentiment
  const positiveWords = ['thank', 'please', 'wonderful', 'great', 'excellent']
  const negativeWords = ['hate', 'terrible', 'awful', 'stupid', 'worthless']
  
  let change = 0
  
  positiveWords.forEach(word => {
    if (playerMessage.toLowerCase().includes(word)) change += 2
  })
  
  negativeWords.forEach(word => {
    if (playerMessage.toLowerCase().includes(word)) change -= 3
  })
  
  relationshipLevel.value = Math.max(-100, Math.min(100, relationshipLevel.value + change))
  trustLevel.value = Math.max(0, Math.min(100, trustLevel.value + Math.floor(change / 2)))
  
  if (change > 0) {
    influenceLevel.value = Math.min(100, influenceLevel.value + 1)
    strengthenConnection(props.npc.id, 1)
  }
}

const endConversation = () => {
  emit('endConversation')
}

const getCurrentTimeOfDay = () => {
  const hour = new Date().getHours()
  if (hour < 6) return 'night'
  if (hour < 12) return 'morning'
  if (hour < 18) return 'afternoon'
  if (hour < 22) return 'evening'
  return 'night'
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getMoodClass = (mood: string): string => {
  const moodClasses = {
    friendly: 'bg-green-500/20 text-green-400',
    neutral: 'bg-gray-500/20 text-gray-400',
    suspicious: 'bg-yellow-500/20 text-yellow-400',
    hostile: 'bg-red-500/20 text-red-400',
    drunk: 'bg-purple-500/20 text-purple-400',
    melancholy: 'bg-blue-500/20 text-blue-400'
  }
  
  return moodClasses[mood as keyof typeof moodClasses] || moodClasses.neutral
}

const getFactionClass = (faction: string): string => {
  const factionClasses = {
    empire: 'bg-yellow-500/20 text-yellow-400',
    chaos: 'bg-red-500/20 text-red-400',
    elves: 'bg-green-500/20 text-green-400',
    dwarfs: 'bg-orange-500/20 text-orange-400',
    undead: 'bg-purple-500/20 text-purple-400',
    orcs: 'bg-lime-500/20 text-lime-400',
    neutral: 'bg-gray-500/20 text-gray-400'
  }
  
  return factionClasses[faction as keyof typeof factionClasses] || factionClasses.neutral
}

const getRelationshipClass = (level: number): string => {
  if (level >= 50) return 'text-green-400'
  if (level >= 25) return 'text-blue-400'
  if (level >= 0) return 'text-yellow-400'
  if (level >= -25) return 'text-orange-400'
  return 'text-red-400'
}

const getRelationshipText = (level: number): string => {
  if (level >= 75) return 'Trusted Friend'
  if (level >= 50) return 'Good Friend'
  if (level >= 25) return 'Friendly'
  if (level >= 0) return 'Neutral'
  if (level >= -25) return 'Distrustful'
  if (level >= -50) return 'Hostile'
  return 'Enemy'
}

// Initialize conversation with greeting
onMounted(() => {
  const greeting: ConversationMessage = {
    id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    speaker: 'npc',
    content: `Greetings, ${props.player.name}. What brings you to speak with me?`,
    timestamp: new Date()
  }
  
  conversationHistory.value.push(greeting)
})
</script>

<style scoped>
.conversation-history {
  scrollbar-width: thin;
  scrollbar-color: rgb(var(--muted)) transparent;
}

.conversation-history::-webkit-scrollbar {
  width: 6px;
}

.conversation-history::-webkit-scrollbar-track {
  background: transparent;
}

.conversation-history::-webkit-scrollbar-thumb {
  background-color: rgb(var(--muted));
  border-radius: 3px;
}

.message-bubble {
  @apply shadow-lg;
  animation: fadeInUp 0.3s ease-out;
}

.quick-response-btn:hover:not(:disabled) {
  @apply transform -translate-y-px;
}

.relationship-progress {
  @apply relative;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .conversation-header {
    @apply flex-col space-y-4;
  }
  
  .npc-info {
    @apply w-full;
  }
  
  .conversation-controls {
    @apply w-full justify-center;
  }
  
  .quick-responses {
    @apply grid grid-cols-1 gap-2;
  }
  
  .input-area {
    @apply flex-col space-x-0 space-y-3;
  }
}
</style>
