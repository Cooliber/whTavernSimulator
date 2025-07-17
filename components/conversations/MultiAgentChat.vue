<template>
  <div class="multi-agent-chat h-full flex flex-col bg-background/95 backdrop-blur">
    <!-- Chat Header -->
    <div class="chat-header border-b border-border/40 p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="relative">
            <Icon name="users" class="w-6 h-6 text-primary" />
            <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background animate-pulse"></div>
          </div>
          <div>
            <h2 class="text-lg font-medieval text-foreground">{{ $t('conversations.multiAgent.title') }}</h2>
            <p class="text-sm text-muted-foreground">
              {{ $t('conversations.multiAgent.participants') }}: {{ activeAgents.length }}
            </p>
          </div>
        </div>
        
        <!-- Agent Management -->
        <div class="flex items-center space-x-2">
          <button
            @click="showAgentSelector = true"
            class="px-3 py-2 text-sm font-medieval bg-primary/10 hover:bg-primary/20 text-primary rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            :aria-label="$t('conversations.multiAgent.addAgent')"
          >
            <Icon name="plus" class="w-4 h-4 mr-1" />
            {{ $t('conversations.multiAgent.addAgent') }}
          </button>
        </div>
      </div>

      <!-- Active Agents Display -->
      <div class="mt-4 flex flex-wrap gap-2">
        <div
          v-for="agent in activeAgents"
          :key="agent.id"
          class="agent-indicator flex items-center space-x-2 px-3 py-2 rounded-full text-sm font-medieval transition-all duration-200"
          :class="[
            `bg-${agent.color}-500/20 text-${agent.color}-700 border border-${agent.color}-500/30`,
            { 'ring-2 ring-primary ring-offset-2': agent.isTyping }
          ]"
        >
          <div 
            class="w-3 h-3 rounded-full"
            :class="`bg-${agent.color}-500`"
            :title="agent.faction"
          ></div>
          <span>{{ agent.name }}</span>
          <div v-if="agent.isTyping" class="typing-indicator">
            <div class="flex space-x-1">
              <div class="w-1 h-1 bg-current rounded-full animate-bounce"></div>
              <div class="w-1 h-1 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-1 h-1 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
          <button
            @click="removeAgent(agent.id)"
            class="ml-2 w-4 h-4 rounded-full bg-red-500/20 hover:bg-red-500/40 text-red-600 flex items-center justify-center transition-colors"
            :aria-label="$t('conversations.multiAgent.removeAgent')"
          >
            <Icon name="x" class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div 
      ref="messagesContainer"
      class="messages-area flex-1 overflow-y-auto p-4 space-y-4"
      role="log"
      aria-live="polite"
      aria-label="Conversation messages"
    >
      <div
        v-for="message in messages"
        :key="message.id"
        class="message-bubble flex items-start space-x-3 animate-fade-in"
        :class="{ 'flex-row-reverse space-x-reverse': message.isUser }"
      >
        <!-- Agent Avatar -->
        <div 
          v-if="!message.isUser"
          class="agent-avatar flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
          :class="`bg-${message.agent?.color}-500`"
          :title="message.agent?.name"
        >
          {{ message.agent?.name?.charAt(0) || 'A' }}
        </div>

        <!-- User Avatar -->
        <div 
          v-else
          class="user-avatar flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-sm"
        >
          {{ $t('common.you').charAt(0) }}
        </div>

        <!-- Message Content -->
        <div 
          class="message-content max-w-[70%] rounded-lg p-3 shadow-sm"
          :class="[
            message.isUser 
              ? 'bg-primary text-primary-foreground ml-auto' 
              : `bg-${message.agent?.color}-50 border border-${message.agent?.color}-200`
          ]"
        >
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-medieval opacity-75">
              {{ message.isUser ? $t('common.you') : message.agent?.name }}
            </span>
            <span class="text-xs opacity-50">
              {{ formatTime(message.timestamp) }}
            </span>
          </div>
          <p class="text-sm leading-relaxed">{{ message.content }}</p>
          
          <!-- Message Actions -->
          <div v-if="!message.isUser" class="mt-2 flex items-center space-x-2">
            <button
              @click="reactToMessage(message.id, '👍')"
              class="text-xs px-2 py-1 rounded bg-white/20 hover:bg-white/30 transition-colors"
            >
              👍
            </button>
            <button
              @click="reactToMessage(message.id, '❤️')"
              class="text-xs px-2 py-1 rounded bg-white/20 hover:bg-white/30 transition-colors"
            >
              ❤️
            </button>
          </div>
        </div>
      </div>

      <!-- Typing Indicators -->
      <div v-if="typingAgents.length > 0" class="typing-message flex items-center space-x-2 text-muted-foreground">
        <div class="typing-dots flex space-x-1">
          <div class="w-2 h-2 bg-current rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
        <span class="text-sm font-medieval">
          {{ typingAgents.map(a => a.name).join(', ') }} {{ $t('conversations.thinking') }}
        </span>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-area border-t border-border/40 p-4">
      <div class="flex items-end space-x-3">
        <div class="flex-1">
          <textarea
            v-model="newMessage"
            @keydown.enter.prevent="sendMessage"
            @input="handleTyping"
            :placeholder="$t('conversations.typeMessage')"
            class="w-full px-4 py-3 bg-background border border-border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent font-medieval"
            rows="2"
            :disabled="isLoading"
          ></textarea>
        </div>
        <button
          @click="sendMessage"
          :disabled="!newMessage.trim() || isLoading"
          class="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medieval transition-all duration-200 hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Icon name="send" class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Agent Selector Modal -->
    <Teleport to="body">
      <div
        v-if="showAgentSelector"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        @click.self="showAgentSelector = false"
      >
        <div class="bg-background border border-border rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
          <h3 class="text-lg font-medieval text-foreground mb-4">{{ $t('conversations.selectCharacter') }}</h3>
          <div class="space-y-3 max-h-60 overflow-y-auto">
            <button
              v-for="agent in availableAgents"
              :key="agent.id"
              @click="addAgent(agent)"
              class="w-full flex items-center space-x-3 p-3 rounded-lg border border-border hover:bg-accent transition-colors text-left"
            >
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm"
                :class="`bg-${agent.color}-500`"
              >
                {{ agent.name.charAt(0) }}
              </div>
              <div>
                <div class="font-medieval text-foreground">{{ agent.name }}</div>
                <div class="text-sm text-muted-foreground">{{ agent.class }}</div>
              </div>
            </button>
          </div>
          <div class="mt-4 flex justify-end">
            <button
              @click="showAgentSelector = false"
              class="px-4 py-2 text-sm font-medieval text-muted-foreground hover:text-foreground transition-colors"
            >
              {{ $t('common.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
interface Agent {
  id: string
  name: string
  class: string
  faction: string
  color: string
  isTyping: boolean
  personality: string
}

interface Message {
  id: string
  content: string
  timestamp: Date
  isUser: boolean
  agent?: Agent
}

// Composables
const { t } = useI18n()

// State
const messages = ref<Message[]>([])
const newMessage = ref('')
const isLoading = ref(false)
const showAgentSelector = ref(false)
const messagesContainer = ref<HTMLElement>()

// Active agents in conversation
const activeAgents = ref<Agent[]>([
  {
    id: 'marcus',
    name: 'Sir Marcus',
    class: 'Empire Knight',
    faction: 'Empire',
    color: 'blue',
    isTyping: false,
    personality: 'Noble and honorable knight'
  }
])

// Available agents to add
const availableAgents = ref<Agent[]>([
  {
    id: 'grimjaw',
    name: 'Grimjaw',
    class: 'Dwarf Slayer',
    faction: 'Dwarfs',
    color: 'orange',
    isTyping: false,
    personality: 'Fierce and determined'
  },
  {
    id: 'elara',
    name: 'Elara',
    class: 'High Elf Mage',
    faction: 'High Elves',
    color: 'purple',
    isTyping: false,
    personality: 'Wise and mystical'
  },
  {
    id: 'valdris',
    name: 'Valdris',
    class: 'Witch Hunter',
    faction: 'Empire',
    color: 'red',
    isTyping: false,
    personality: 'Grim and suspicious'
  }
])

// Computed
const typingAgents = computed(() => activeAgents.value.filter(agent => agent.isTyping))

// Methods
const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMessage: Message = {
    id: Date.now().toString(),
    content: newMessage.value.trim(),
    timestamp: new Date(),
    isUser: true
  }

  messages.value.push(userMessage)
  const messageContent = newMessage.value.trim()
  newMessage.value = ''

  // Scroll to bottom
  nextTick(() => {
    scrollToBottom()
  })

  // Simulate agent responses
  await simulateAgentResponses(messageContent)
}

const simulateAgentResponses = async (userMessage: string) => {
  isLoading.value = true
  
  // Randomly select 1-2 agents to respond
  const respondingAgents = activeAgents.value
    .sort(() => Math.random() - 0.5)
    .slice(0, Math.floor(Math.random() * 2) + 1)

  for (const agent of respondingAgents) {
    // Show typing indicator
    agent.isTyping = true
    
    // Wait for realistic typing time
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
    
    // Generate response based on agent personality
    const response = generateAgentResponse(agent, userMessage)
    
    const agentMessage: Message = {
      id: Date.now().toString() + agent.id,
      content: response,
      timestamp: new Date(),
      isUser: false,
      agent
    }

    agent.isTyping = false
    messages.value.push(agentMessage)
    
    // Scroll to bottom
    nextTick(() => {
      scrollToBottom()
    })

    // Small delay between agent responses
    if (respondingAgents.indexOf(agent) < respondingAgents.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 500))
    }
  }

  isLoading.value = false
}

const generateAgentResponse = (agent: Agent, userMessage: string): string => {
  // Simple response generation based on agent personality
  const responses = {
    marcus: [
      "By Sigmar's hammer, that's an interesting point!",
      "Honor demands that we consider this carefully.",
      "As a knight of the Empire, I must say...",
      "The code of chivalry guides my thoughts on this matter."
    ],
    grimjaw: [
      "Bah! That's dwarf nonsense if I ever heard it!",
      "My axe has seen worse than that, manling!",
      "The ancestors would be proud of such thinking.",
      "Grudges must be settled, that's the dwarf way!"
    ],
    elara: [
      "The winds of magic whisper of deeper truths...",
      "Ancient wisdom suggests a different path.",
      "Magic flows through all things, including this matter.",
      "The elven perspective offers clarity here."
    ],
    valdris: [
      "Heresy! I sense corruption in those words!",
      "The witch hunters have seen such things before.",
      "Vigilance is the price of purity.",
      "By Sigmar's will, we must remain watchful."
    ]
  }

  const agentResponses = responses[agent.id as keyof typeof responses] || [
    "Interesting perspective, friend.",
    "I see your point.",
    "That's worth considering."
  ]

  return agentResponses[Math.floor(Math.random() * agentResponses.length)]
}

const addAgent = (agent: Agent) => {
  if (!activeAgents.value.find(a => a.id === agent.id)) {
    activeAgents.value.push({ ...agent })
    
    // Add join message
    const joinMessage: Message = {
      id: Date.now().toString(),
      content: t('conversations.multiAgent.agentJoined', { name: agent.name }),
      timestamp: new Date(),
      isUser: false,
      agent
    }
    messages.value.push(joinMessage)
  }
  showAgentSelector.value = false
}

const removeAgent = (agentId: string) => {
  const agent = activeAgents.value.find(a => a.id === agentId)
  if (agent) {
    // Add leave message
    const leaveMessage: Message = {
      id: Date.now().toString(),
      content: t('conversations.multiAgent.agentLeft', { name: agent.name }),
      timestamp: new Date(),
      isUser: false,
      agent
    }
    messages.value.push(leaveMessage)
    
    activeAgents.value = activeAgents.value.filter(a => a.id !== agentId)
  }
}

const handleTyping = () => {
  // Could implement typing indicators for user
}

const reactToMessage = (messageId: string, reaction: string) => {
  // Could implement message reactions
  console.log(`Reacted to message ${messageId} with ${reaction}`)
}

const formatTime = (timestamp: Date): string => {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Lifecycle
onMounted(() => {
  // Add welcome message
  const welcomeMessage: Message = {
    id: 'welcome',
    content: "Welcome to the tavern! The conversation begins...",
    timestamp: new Date(),
    isUser: false,
    agent: activeAgents.value[0]
  }
  messages.value.push(welcomeMessage)
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.typing-indicator {
  display: inline-flex;
  align-items: center;
}

/* Scrollbar styling */
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-track {
  background: transparent;
}

.messages-area::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .animate-fade-in,
  .animate-bounce {
    animation: none !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .message-content {
    border-width: 2px;
  }
  
  .agent-indicator {
    border-width: 2px;
  }
}
</style>
