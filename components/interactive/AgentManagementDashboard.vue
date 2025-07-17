<template>
  <div class="agent-management-dashboard bg-card/95 backdrop-blur-sm border border-border rounded-lg p-6">
    <div class="dashboard-header mb-6">
      <h2 class="text-2xl font-bold text-foreground mb-2">
        🤖 AI Agent Management Dashboard
      </h2>
      <p class="text-muted-foreground">
        Monitor and manage the 17 Warhammer Fantasy AI agents
      </p>
    </div>

    <!-- AI Service Status -->
    <div class="ai-service-status mb-6">
      <h3 class="text-lg font-semibold mb-3">AI Service Status</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div 
          v-for="provider in providerStatus" 
          :key="provider.name"
          class="provider-card p-4 border rounded-lg"
          :class="{
            'border-green-500 bg-green-50': provider.isAvailable,
            'border-red-500 bg-red-50': !provider.isAvailable,
            'border-blue-500 bg-blue-50': provider.isCurrent
          }"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium capitalize">{{ provider.name }}</span>
            <div class="status-indicator">
              <div 
                class="w-3 h-3 rounded-full"
                :class="{
                  'bg-green-500': provider.isAvailable,
                  'bg-red-500': !provider.isAvailable
                }"
              ></div>
            </div>
          </div>
          <div class="text-sm text-muted-foreground">
            Model: {{ provider.model }}
          </div>
          <div v-if="provider.isCurrent" class="text-xs text-blue-600 mt-1">
            Currently Active
          </div>
        </div>
      </div>
    </div>

    <!-- Agent Overview -->
    <div class="agent-overview mb-6">
      <h3 class="text-lg font-semibold mb-3">Agent Overview</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div class="stat-card p-3 border rounded-lg text-center">
          <div class="text-2xl font-bold text-primary">{{ totalAgents }}</div>
          <div class="text-sm text-muted-foreground">Total Agents</div>
        </div>
        <div class="stat-card p-3 border rounded-lg text-center">
          <div class="text-2xl font-bold text-green-600">{{ activeConversations.length }}</div>
          <div class="text-sm text-muted-foreground">Active Conversations</div>
        </div>
        <div class="stat-card p-3 border rounded-lg text-center">
          <div class="text-2xl font-bold text-blue-600">{{ agentsByRole.bartender.length + agentsByRole.merchant.length }}</div>
          <div class="text-sm text-muted-foreground">Service Agents</div>
        </div>
        <div class="stat-card p-3 border rounded-lg text-center">
          <div class="text-2xl font-bold text-purple-600">{{ agentsByRole.scholar.length + agentsByRole.mystic.length }}</div>
          <div class="text-sm text-muted-foreground">Knowledge Agents</div>
        </div>
      </div>
    </div>

    <!-- Agent List -->
    <div class="agent-list mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">Agent Directory</h3>
        <div class="filters flex gap-2">
          <select 
            v-model="selectedRole" 
            class="px-3 py-1 border rounded text-sm"
          >
            <option value="">All Roles</option>
            <option value="bartender">Bartender</option>
            <option value="merchant">Merchant</option>
            <option value="guard">Guard</option>
            <option value="scholar">Scholar</option>
            <option value="entertainer">Entertainer</option>
            <option value="noble">Noble</option>
            <option value="warrior">Warrior</option>
            <option value="mystic">Mystic</option>
            <option value="artisan">Artisan</option>
            <option value="commoner">Commoner</option>
          </select>
          <select 
            v-model="selectedFaction" 
            class="px-3 py-1 border rounded text-sm"
          >
            <option value="">All Factions</option>
            <option value="empire">Empire</option>
            <option value="dwarfs">Dwarfs</option>
            <option value="elves">Elves</option>
            <option value="neutral">Neutral</option>
          </select>
        </div>
      </div>

      <div class="agents-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="agent in filteredAgents" 
          :key="agent.id"
          class="agent-card p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
          @click="selectAgent(agent)"
          :class="{ 'border-primary bg-primary/5': selectedAgent?.id === agent.id }"
        >
          <div class="agent-header flex items-center justify-between mb-2">
            <h4 class="font-semibold">{{ agent.name }}</h4>
            <div class="agent-status">
              <div 
                class="w-2 h-2 rounded-full"
                :class="{
                  'bg-green-500': isAgentActive(agent.id),
                  'bg-gray-400': !isAgentActive(agent.id)
                }"
              ></div>
            </div>
          </div>
          
          <div class="agent-info text-sm space-y-1">
            <div class="flex justify-between">
              <span class="text-muted-foreground">Species:</span>
              <span class="capitalize">{{ agent.species }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Career:</span>
              <span>{{ agent.career }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Role:</span>
              <span class="capitalize">{{ agent.role }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Faction:</span>
              <span class="capitalize">{{ agent.faction }}</span>
            </div>
          </div>

          <div class="agent-stats mt-3 grid grid-cols-2 gap-2 text-xs">
            <div class="stat">
              <span class="text-muted-foreground">Reputation:</span>
              <div class="w-full bg-gray-200 rounded-full h-1 mt-1">
                <div 
                  class="bg-blue-600 h-1 rounded-full" 
                  :style="{ width: `${agent.gameStats.reputation}%` }"
                ></div>
              </div>
            </div>
            <div class="stat">
              <span class="text-muted-foreground">Influence:</span>
              <div class="w-full bg-gray-200 rounded-full h-1 mt-1">
                <div 
                  class="bg-purple-600 h-1 rounded-full" 
                  :style="{ width: `${agent.gameStats.influence}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Agent Details -->
    <div v-if="selectedAgent" class="agent-details p-4 border rounded-lg bg-muted/50">
      <h3 class="text-lg font-semibold mb-3">{{ selectedAgent.name }} - Details</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="personality-section">
          <h4 class="font-medium mb-2">Personality</h4>
          <div class="space-y-2 text-sm">
            <div><strong>Traits:</strong> {{ selectedAgent.personality.traits.join(', ') }}</div>
            <div><strong>Style:</strong> {{ selectedAgent.personality.conversationStyle }}</div>
            <div><strong>Mood:</strong> {{ selectedAgent.personality.mood }}</div>
            <div><strong>Intelligence:</strong> {{ selectedAgent.personality.intelligence }}/10</div>
            <div><strong>Charisma:</strong> {{ selectedAgent.personality.charisma }}/10</div>
          </div>
        </div>

        <div class="knowledge-section">
          <h4 class="font-medium mb-2">Knowledge & Expertise</h4>
          <div class="space-y-2 text-sm">
            <div><strong>Domains:</strong> {{ selectedAgent.knowledge.domains.join(', ') }}</div>
            <div><strong>Specialties:</strong> {{ selectedAgent.knowledge.specialties.join(', ') }}</div>
          </div>
        </div>

        <div class="relationships-section">
          <h4 class="font-medium mb-2">Relationships</h4>
          <div class="space-y-2 text-sm">
            <div v-if="selectedAgent.relationships.allies.length">
              <strong>Allies:</strong> {{ getAllyNames(selectedAgent.relationships.allies).join(', ') }}
            </div>
            <div v-if="selectedAgent.relationships.rivals.length">
              <strong>Rivals:</strong> {{ getRivalNames(selectedAgent.relationships.rivals).join(', ') }}
            </div>
          </div>
        </div>

        <div class="background-section">
          <h4 class="font-medium mb-2">Background</h4>
          <div class="space-y-2 text-sm">
            <div><strong>Origin:</strong> {{ selectedAgent.background.origin }}</div>
            <div><strong>Motivation:</strong> {{ selectedAgent.background.motivation }}</div>
            <div><strong>Goals:</strong> {{ selectedAgent.background.goals.join(', ') }}</div>
          </div>
        </div>
      </div>

      <div class="agent-actions mt-4 flex gap-2">
        <button 
          @click="startConversationWithAgent(selectedAgent.id)"
          class="px-4 py-2 bg-primary text-primary-foreground rounded hover:bg-primary/90 transition-colors"
        >
          Start Conversation
        </button>
        <button 
          @click="simulateAgentInteraction(selectedAgent.id)"
          class="px-4 py-2 bg-secondary text-secondary-foreground rounded hover:bg-secondary/90 transition-colors"
        >
          Simulate Interaction
        </button>
      </div>
    </div>

    <!-- Active Conversations -->
    <div v-if="activeConversations.length > 0" class="active-conversations mt-6">
      <h3 class="text-lg font-semibold mb-3">Active Conversations</h3>
      <div class="conversations-list space-y-2">
        <div 
          v-for="conversation in activeConversations" 
          :key="conversation.id"
          class="conversation-item p-3 border rounded-lg bg-background"
        >
          <div class="flex items-center justify-between">
            <div>
              <span class="font-medium">{{ getConversationTitle(conversation) }}</span>
              <span class="text-sm text-muted-foreground ml-2">
                Topic: {{ conversation.topic }}
              </span>
            </div>
            <div class="text-xs text-muted-foreground">
              {{ formatTime(conversation.lastActivity) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUnifiedAIService } from '~/composables/useUnifiedAIService'
import { useWarhammerAgents } from '~/composables/useWarhammerAgents'
import { useEnhancedAINPCSystem } from '~/composables/useEnhancedAINPCSystem'
import type { WarhammerAgent } from '~/composables/useWarhammerAgents'

// Composables
const { getProviderStatus } = useUnifiedAIService()
const { agents, getAgentById, getAgentsByRole } = useWarhammerAgents()
const { 
  activeConversations, 
  initializeEnhancedSystem,
  startPlayerConversation,
  simulateRandomInteraction
} = useEnhancedAINPCSystem()

// Reactive state
const selectedAgent = ref<WarhammerAgent | null>(null)
const selectedRole = ref('')
const selectedFaction = ref('')

// Computed properties
const providerStatus = computed(() => getProviderStatus())
const totalAgents = computed(() => agents.value.length)
const agentsByRole = computed(() => getAgentsByRole)

const filteredAgents = computed(() => {
  return agents.value.filter(agent => {
    const roleMatch = !selectedRole.value || agent.role === selectedRole.value
    const factionMatch = !selectedFaction.value || agent.faction === selectedFaction.value
    return roleMatch && factionMatch
  })
})

// Methods
const selectAgent = (agent: WarhammerAgent) => {
  selectedAgent.value = agent
}

const isAgentActive = (agentId: string): boolean => {
  return activeConversations.value.some(conv => 
    conv.participants.includes(agentId) && conv.isActive
  )
}

const getAllyNames = (allyIds: string[]): string[] => {
  return allyIds.map(id => getAgentById(id)?.name || 'Unknown').filter(Boolean)
}

const getRivalNames = (rivalIds: string[]): string[] => {
  return rivalIds.map(id => getAgentById(id)?.name || 'Unknown').filter(Boolean)
}

const getConversationTitle = (conversation: any): string => {
  const participants = conversation.participants
    .filter((p: string) => p !== 'player')
    .map((id: string) => getAgentById(id)?.name || 'Unknown')
    .join(' & ')
  
  return participants || 'Unknown Conversation'
}

const formatTime = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date))
}

const startConversationWithAgent = async (agentId: string) => {
  try {
    const response = await startPlayerConversation(
      agentId, 
      'Hello, I\'d like to speak with you.',
      { source: 'dashboard' }
    )
    console.log('Conversation started:', response)
  } catch (error) {
    console.error('Failed to start conversation:', error)
  }
}

const simulateAgentInteraction = async (agentId: string) => {
  try {
    await simulateRandomInteraction()
    console.log('Agent interaction simulated')
  } catch (error) {
    console.error('Failed to simulate interaction:', error)
  }
}

// Lifecycle
onMounted(async () => {
  await initializeEnhancedSystem()
})
</script>

<style scoped>
.agent-management-dashboard {
  max-height: 80vh;
  overflow-y: auto;
}

.agent-card:hover {
  transform: translateY(-1px);
}

.stat-card {
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: scale(1.02);
}

.conversation-item {
  transition: all 0.2s ease;
}

.conversation-item:hover {
  background-color: var(--muted);
}
</style>
