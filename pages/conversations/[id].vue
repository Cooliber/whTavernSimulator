<template>
  <div class="space-y-8">
    <!-- Character Header -->
    <section v-if="character" class="text-center space-y-6">
      <div class="relative">
        <!-- Background Effects -->
        <div class="absolute inset-0 rounded-2xl overflow-hidden">
          <LiquidBackground 
            :colors="character.factionColors"
            :blob-count="2"
            class="opacity-20"
          />
        </div>
        
        <!-- Character Info -->
        <div class="relative z-10 p-8 rounded-2xl bg-gradient-to-br from-background/80 to-background/60 backdrop-blur">
          <div class="space-y-4">
            <div class="w-24 h-24 mx-auto rounded-full bg-gradient-to-r from-primary/30 to-primary/20 flex items-center justify-center">
              <Icon :name="character.icon" class="w-12 h-12 text-primary" />
            </div>
            
            <div>
              <SparklesText 
                :text="character.name"
                class="text-3xl font-medieval text-foreground"
                :sparkles-count="12"
              />
              <p class="text-lg text-primary font-medieval">{{ character.class }}</p>
              <div class="flex items-center justify-center space-x-2 mt-2">
                <div class="w-3 h-3 rounded-full" :class="character.factionColor"></div>
                <span class="text-sm text-muted-foreground">{{ character.faction }}</span>
              </div>
            </div>
            
            <p class="text-muted-foreground max-w-2xl mx-auto">{{ character.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Conversation Interface -->
    <section class="max-w-4xl mx-auto">
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="3">
        <div class="space-y-6">
          <!-- Conversation Header -->
          <div class="flex items-center justify-between border-b border-border/40 pb-4">
            <div class="flex items-center space-x-3">
              <Icon name="message-circle" class="w-6 h-6 text-primary" />
              <h3 class="text-xl font-medieval text-foreground">Conversation</h3>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span class="text-xs text-muted-foreground">{{ character?.name }} is listening</span>
            </div>
          </div>
          
          <!-- Messages Area -->
          <div 
            ref="messagesContainer"
            class="h-96 overflow-y-auto space-y-4 p-4 bg-gradient-to-br from-background/50 to-background/30 rounded-lg border border-border/30"
          >
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="flex"
              :class="message.sender === 'player' ? 'justify-end' : 'justify-start'"
            >
              <div 
                class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
                :class="message.sender === 'player' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'bg-secondary text-secondary-foreground'"
              >
                <p class="text-sm">{{ message.text }}</p>
                <span class="text-xs opacity-70">{{ formatTime(message.timestamp) }}</span>
              </div>
            </div>
            
            <!-- Typing Indicator -->
            <div v-if="isTyping" class="flex justify-start">
              <div class="bg-secondary text-secondary-foreground px-4 py-2 rounded-lg">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Input Area -->
          <div class="space-y-4">
            <!-- Quick Responses -->
            <div v-if="quickResponses.length > 0" class="space-y-2">
              <p class="text-sm text-muted-foreground font-medieval">Quick Responses:</p>
              <div class="flex flex-wrap gap-2">
                <ShimmerButton 
                  v-for="response in quickResponses"
                  :key="response.id"
                  class="text-xs font-medieval"
                  shimmer-color="rgb(255, 215, 0)"
                  @click="sendQuickResponse(response)"
                >
                  {{ response.text }}
                </ShimmerButton>
              </div>
            </div>
            
            <!-- Message Input -->
            <div class="flex space-x-3">
              <input 
                v-model="currentMessage"
                type="text" 
                placeholder="Type your message..."
                class="flex-1 p-3 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                @keypress.enter="sendMessage"
                :disabled="isTyping"
              />
              <RippleButton 
                class="faction-empire px-6 py-3 font-medieval"
                ripple-color="rgb(255, 215, 0)"
                @click="sendMessage"
                :disabled="isTyping || !currentMessage.trim()"
              >
                Send
              </RippleButton>
            </div>
          </div>
        </div>
      </Card3D>
    </section>

    <!-- Character Stats -->
    <section v-if="character" class="max-w-2xl mx-auto">
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="5">
        <div class="space-y-4">
          <h3 class="text-lg font-medieval text-foreground text-center">Character Stats</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center space-y-2">
              <div class="flex items-center justify-center space-x-2">
                <Icon name="sword" class="w-4 h-4 text-red-400" />
                <span class="text-sm text-muted-foreground">Attack</span>
              </div>
              <NumberTicker 
                :value="character.stats.attack"
                class="text-2xl font-medieval text-red-400"
              />
            </div>
            <div class="text-center space-y-2">
              <div class="flex items-center justify-center space-x-2">
                <Icon name="shield" class="w-4 h-4 text-blue-400" />
                <span class="text-sm text-muted-foreground">Defense</span>
              </div>
              <NumberTicker 
                :value="character.stats.defense"
                class="text-2xl font-medieval text-blue-400"
              />
            </div>
          </div>
        </div>
      </Card3D>
    </section>
  </div>
</template>

<script setup lang="ts">
// Get route parameter
const route = useRoute()
const characterId = route.params.id as string

// Page metadata
useHead({
  title: `Conversation - Warhammer Tavern Simulator v3`,
  meta: [
    { name: 'description', content: 'Engage in immersive conversations with AI-powered NPCs in the Warhammer Fantasy world.' }
  ]
})

// Character data (in a real app, this would come from an API)
const characters = {
  'marcus': {
    id: 'marcus',
    name: 'Sir Marcus Brightblade',
    class: 'Empire Knight',
    faction: 'Empire',
    factionColor: 'bg-yellow-600',
    factionColors: ['#ffd700', '#b8860b', '#daa520'],
    icon: 'sword',
    description: 'A noble knight of the Empire, seeking glory and honor in service to Sigmar.',
    stats: { attack: 85, defense: 78 }
  },
  'grimjaw': {
    id: 'grimjaw',
    name: 'Grimjaw Ironbeard',
    class: 'Dwarf Slayer',
    faction: 'Dwarfs',
    factionColor: 'bg-orange-600',
    factionColors: ['#cd853f', '#a0522d', '#8b4513'],
    icon: 'hammer',
    description: 'A fierce dwarf warrior who has taken the Slayer Oath to redeem his honor.',
    stats: { attack: 92, defense: 65 }
  },
  'elara': {
    id: 'elara',
    name: 'Elara Moonwhisper',
    class: 'High Elf Mage',
    faction: 'High Elves',
    factionColor: 'bg-blue-600',
    factionColors: ['#4169e1', '#6495ed', '#87ceeb'],
    icon: 'sparkles',
    description: 'An elegant elven sorceress mastering the winds of magic.',
    stats: { attack: 70, defense: 55 }
  }
}

// Reactive state
const character = ref(characters[characterId] || null)
const messages = ref([])
const currentMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref(null)

// Quick responses based on character
const quickResponses = computed(() => {
  if (!character.value) return []
  
  const responses = {
    'marcus': [
      { id: 1, text: 'Tell me about your service to the Empire' },
      { id: 2, text: 'Any threats in the area?' },
      { id: 3, text: 'What brings you to this tavern?' }
    ],
    'grimjaw': [
      { id: 1, text: 'What is the Slayer Oath?' },
      { id: 2, text: 'Tell me about dwarf craftsmanship' },
      { id: 3, text: 'Any good fights lately?' }
    ],
    'elara': [
      { id: 1, text: 'Teach me about magic' },
      { id: 2, text: 'What are the Winds of Magic?' },
      { id: 3, text: 'Tell me about the High Elves' }
    ]
  }
  
  return responses[character.value.id] || []
})

// Methods
const sendMessage = async () => {
  if (!currentMessage.value.trim() || isTyping.value) return
  
  // Add player message
  const playerMessage = {
    id: Date.now(),
    sender: 'player',
    text: currentMessage.value,
    timestamp: new Date()
  }
  
  messages.value.push(playerMessage)
  const messageText = currentMessage.value
  currentMessage.value = ''
  
  // Scroll to bottom
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
  
  // Simulate AI response
  isTyping.value = true
  
  setTimeout(() => {
    const aiResponse = generateAIResponse(messageText)
    messages.value.push({
      id: Date.now() + 1,
      sender: 'npc',
      text: aiResponse,
      timestamp: new Date()
    })
    
    isTyping.value = false
    
    // Scroll to bottom
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }, 1500 + Math.random() * 1000)
}

const sendQuickResponse = (response) => {
  currentMessage.value = response.text
  sendMessage()
}

const generateAIResponse = (playerMessage: string): string => {
  if (!character.value) return "I don't understand."
  
  const responses = {
    'marcus': [
      "By Sigmar's hammer, that's an interesting question! As a knight of the Empire, I've seen many battles.",
      "The Empire stands strong against all threats, friend. We protect the innocent and uphold justice.",
      "Honor and duty guide my every action. What brings you to speak with me this day?"
    ],
    'grimjaw': [
      "Bah! You want to know about the Slayer Oath? It's a sacred vow to seek a glorious death in battle!",
      "Dwarf craftsmanship is unmatched! These hands have forged weapons that could cleave mountains!",
      "A good fight? Every day I don't find my doom is a day wasted! But the ale here helps pass the time."
    ],
    'elara': [
      "The winds of magic flow through all things, mortal. To understand them is to touch the divine.",
      "Magic is both beautiful and dangerous. One must respect its power or face dire consequences.",
      "The High Elves have mastered the arcane arts for millennia. We are the guardians of ancient wisdom."
    ]
  }
  
  const characterResponses = responses[character.value.id] || ["I'm not sure how to respond to that."]
  return characterResponses[Math.floor(Math.random() * characterResponses.length)]
}

const formatTime = (timestamp: Date): string => {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Initialize conversation
onMounted(() => {
  if (!character.value) {
    // Redirect to characters page if character not found
    navigateTo('/characters')
    return
  }
  
  // Add initial greeting
  setTimeout(() => {
    messages.value.push({
      id: 1,
      sender: 'npc',
      text: `Greetings, traveler! I am ${character.value.name}. What brings you to speak with me?`,
      timestamp: new Date()
    })
  }, 500)
})
</script>

<style scoped>
/* Custom scrollbar for messages */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 215, 0, 0.3);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 215, 0, 0.5);
}

/* Animation for new messages */
.space-y-4 > div {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
