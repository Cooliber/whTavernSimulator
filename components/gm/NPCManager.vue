<template>
  <div class="npc-manager wh-card wh-card-parchment p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h3 class="wh-title text-xl text-wh-dark-grey">NPC Management</h3>
      <div class="flex items-center space-x-2">
        <Icon name="users" class="w-5 h-5 text-wh-empire-gold" />
        <span class="text-sm text-wh-dark-grey">{{ activeNPCs.length }} Active</span>
      </div>
    </div>

    <!-- NPC Creation Panel -->
    <div class="creation-panel wh-ornate-border p-4 space-y-4">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey">Create New NPC</h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Basic Info -->
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Name</label>
            <input
              v-model="newNPC.name"
              type="text"
              class="wh-input w-full"
              placeholder="Enter NPC name..."
            />
          </div>
          
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Title/Occupation</label>
            <select v-model="newNPC.occupation" class="wh-input w-full">
              <option value="">Select occupation...</option>
              <option v-for="occupation in occupations" :key="occupation" :value="occupation">
                {{ occupation }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Faction</label>
            <select v-model="newNPC.faction" class="wh-input w-full">
              <option value="">Select faction...</option>
              <option v-for="faction in factions" :key="faction.id" :value="faction.id">
                {{ faction.name }}
              </option>
            </select>
          </div>
        </div>
        
        <!-- Appearance & Personality -->
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Race</label>
            <select v-model="newNPC.race" class="wh-input w-full">
              <option value="">Select race...</option>
              <option v-for="race in races" :key="race" :value="race">
                {{ race }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Gender</label>
            <select v-model="newNPC.gender" class="wh-input w-full">
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Age Category</label>
            <select v-model="newNPC.ageCategory" class="wh-input w-full">
              <option value="young">Young</option>
              <option value="adult">Adult</option>
              <option value="middle-aged">Middle-aged</option>
              <option value="elderly">Elderly</option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Personality Traits -->
      <div class="personality-section space-y-3">
        <h5 class="text-md font-medieval text-wh-dark-grey">Personality Traits</h5>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div v-for="trait in personalityTraits" :key="trait.id" class="trait-control">
            <label class="block text-xs text-wh-dark-grey mb-1">{{ trait.name }}</label>
            <input
              v-model="newNPC.personality[trait.id]"
              type="range"
              min="0"
              max="100"
              step="10"
              class="wh-slider w-full"
            />
            <span class="text-xs text-wh-empire-gold">{{ newNPC.personality[trait.id] }}%</span>
          </div>
        </div>
      </div>
      
      <!-- Quick Generation -->
      <div class="quick-gen flex space-x-2">
        <button
          class="wh-btn wh-btn-secondary flex-1 text-sm"
          @click="generateRandomNPC"
        >
          <Icon name="shuffle" class="w-4 h-4 mr-2" />
          Random Generate
        </button>
        
        <button
          class="wh-btn wh-btn-primary flex-1 text-sm"
          @click="createNPC"
          :disabled="!canCreateNPC"
        >
          <Icon name="user-plus" class="w-4 h-4 mr-2" />
          Create NPC
        </button>
      </div>
    </div>

    <!-- Active NPCs List -->
    <div class="active-npcs space-y-4">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey">Active NPCs</h4>
      
      <div class="npc-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="npc in activeNPCs"
          :key="npc.id"
          class="npc-card wh-card p-4 cursor-pointer transition-all duration-300 hover:scale-105"
          :class="selectedNPC?.id === npc.id ? 'wh-fire-glow' : ''"
          @click="selectNPC(npc)"
        >
          <!-- NPC Header -->
          <div class="npc-header flex items-center space-x-3 mb-3">
            <div class="npc-avatar w-12 h-12 rounded-full flex items-center justify-center"
                 :class="getFactionClass(npc.faction)">
              <Icon :name="getNPCIcon(npc)" class="w-6 h-6 text-white" />
            </div>
            <div class="flex-1">
              <h5 class="font-medieval text-wh-parchment">{{ npc.name }}</h5>
              <p class="text-xs text-wh-aged-paper">{{ npc.occupation }}</p>
            </div>
            <div class="npc-status">
              <div
                class="w-3 h-3 rounded-full"
                :class="npc.active ? 'bg-green-400' : 'bg-red-400'"
              />
            </div>
          </div>
          
          <!-- NPC Info -->
          <div class="npc-info space-y-2 text-xs">
            <div class="flex justify-between">
              <span class="text-wh-aged-paper">Race:</span>
              <span class="text-wh-parchment">{{ npc.race }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-wh-aged-paper">Faction:</span>
              <span class="text-wh-parchment">{{ getFactionName(npc.faction) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-wh-aged-paper">Mood:</span>
              <span class="text-wh-parchment">{{ npc.currentMood }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-wh-aged-paper">Activity:</span>
              <span class="text-wh-parchment">{{ npc.currentActivity }}</span>
            </div>
          </div>
          
          <!-- Quick Actions -->
          <div class="npc-actions flex space-x-2 mt-3">
            <button
              class="wh-btn wh-btn-secondary flex-1 py-1 text-xs"
              @click.stop="toggleNPCActive(npc)"
            >
              <Icon :name="npc.active ? 'pause' : 'play'" class="w-3 h-3 mr-1" />
              {{ npc.active ? 'Pause' : 'Activate' }}
            </button>
            
            <button
              class="wh-btn wh-btn-secondary py-1 px-2 text-xs"
              @click.stop="editNPC(npc)"
            >
              <Icon name="edit" class="w-3 h-3" />
            </button>
            
            <button
              class="wh-btn wh-btn-danger py-1 px-2 text-xs"
              @click.stop="removeNPC(npc)"
            >
              <Icon name="trash" class="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- NPC Detail Panel -->
    <div v-if="selectedNPC" class="npc-detail wh-ornate-border p-4 space-y-4">
      <div class="flex items-center justify-between">
        <h4 class="wh-subtitle text-lg text-wh-dark-grey">{{ selectedNPC.name }} Details</h4>
        <button
          class="wh-btn wh-btn-secondary text-xs"
          @click="selectedNPC = null"
        >
          <Icon name="x" class="w-3 h-3" />
        </button>
      </div>
      
      <!-- Detailed Stats -->
      <div class="stats-grid grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="trait in personalityTraits" :key="trait.id" class="stat-item">
          <label class="block text-xs text-wh-dark-grey mb-1">{{ trait.name }}</label>
          <div class="flex items-center space-x-2">
            <input
              v-model="selectedNPC.personality[trait.id]"
              type="range"
              min="0"
              max="100"
              step="5"
              class="wh-slider flex-1"
              @input="updateNPCPersonality"
            />
            <span class="text-xs text-wh-empire-gold w-8">{{ selectedNPC.personality[trait.id] }}%</span>
          </div>
        </div>
      </div>
      
      <!-- Dialogue Style -->
      <div class="dialogue-section space-y-2">
        <label class="block text-sm font-medieval text-wh-dark-grey">Dialogue Style</label>
        <textarea
          v-model="selectedNPC.dialogueStyle"
          class="wh-input w-full h-20 resize-none"
          placeholder="Describe how this NPC speaks and behaves..."
          @input="updateNPCDialogue"
        />
      </div>
      
      <!-- Current State -->
      <div class="current-state grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Current Mood</label>
          <select
            v-model="selectedNPC.currentMood"
            class="wh-input w-full"
            @change="updateNPCState"
          >
            <option v-for="mood in moods" :key="mood" :value="mood">{{ mood }}</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medieval text-wh-dark-grey mb-1">Current Activity</label>
          <select
            v-model="selectedNPC.currentActivity"
            class="wh-input w-full"
            @change="updateNPCState"
          >
            <option v-for="activity in activities" :key="activity" :value="activity">{{ activity }}</option>
          </select>
        </div>
      </div>
      
      <!-- Save Changes -->
      <button
        class="wh-btn wh-btn-primary w-full"
        @click="saveNPCChanges"
      >
        <Icon name="save" class="w-4 h-4 mr-2" />
        Save Changes
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface NPC {
  id: string
  name: string
  occupation: string
  race: string
  gender: string
  ageCategory: string
  faction: string
  active: boolean
  currentMood: string
  currentActivity: string
  dialogueStyle: string
  personality: Record<string, number>
  createdAt: Date
}

interface PersonalityTrait {
  id: string
  name: string
  description: string
}

interface Faction {
  id: string
  name: string
  color: string
}

// Reactive state
const selectedNPC = ref<NPC | null>(null)
const activeNPCs = ref<NPC[]>([])

// New NPC form
const newNPC = ref({
  name: '',
  occupation: '',
  race: '',
  gender: 'male',
  ageCategory: 'adult',
  faction: '',
  personality: {
    friendliness: 50,
    aggression: 30,
    intelligence: 60,
    curiosity: 70,
    trustworthiness: 80,
    greed: 25,
    courage: 65,
    humor: 55
  }
})

// Data arrays
const occupations = [
  'Barkeep', 'Cook', 'Serving Wench', 'Bard', 'Merchant', 'Soldier', 'Guard',
  'Priest', 'Scholar', 'Artisan', 'Noble', 'Peasant', 'Thief', 'Witch Hunter',
  'Rat Catcher', 'Scribe', 'Apothecary', 'Blacksmith', 'Stable Hand', 'Pilgrim'
]

const races = [
  'Human', 'Halfling', 'Dwarf', 'High Elf', 'Wood Elf', 'Dark Elf'
]

const factions: Faction[] = [
  { id: 'empire', name: 'The Empire', color: 'bg-red-600' },
  { id: 'bretonnia', name: 'Bretonnia', color: 'bg-blue-600' },
  { id: 'dwarfs', name: 'Dwarfs', color: 'bg-orange-600' },
  { id: 'high-elves', name: 'High Elves', color: 'bg-purple-600' },
  { id: 'wood-elves', name: 'Wood Elves', color: 'bg-green-600' },
  { id: 'chaos', name: 'Chaos', color: 'bg-black' },
  { id: 'neutral', name: 'Neutral', color: 'bg-gray-600' }
]

const personalityTraits: PersonalityTrait[] = [
  { id: 'friendliness', name: 'Friendliness', description: 'How friendly and approachable the NPC is' },
  { id: 'aggression', name: 'Aggression', description: 'How quick to anger or violence the NPC is' },
  { id: 'intelligence', name: 'Intelligence', description: 'How smart and knowledgeable the NPC is' },
  { id: 'curiosity', name: 'Curiosity', description: 'How interested in new things the NPC is' },
  { id: 'trustworthiness', name: 'Trustworthiness', description: 'How reliable and honest the NPC is' },
  { id: 'greed', name: 'Greed', description: 'How motivated by money and possessions the NPC is' },
  { id: 'courage', name: 'Courage', description: 'How brave and willing to take risks the NPC is' },
  { id: 'humor', name: 'Humor', description: 'How funny and lighthearted the NPC is' }
]

const moods = [
  'Happy', 'Sad', 'Angry', 'Fearful', 'Excited', 'Bored', 'Suspicious',
  'Friendly', 'Hostile', 'Nervous', 'Confident', 'Drunk', 'Tired', 'Alert'
]

const activities = [
  'Drinking', 'Eating', 'Talking', 'Working', 'Sleeping', 'Reading',
  'Gambling', 'Singing', 'Dancing', 'Arguing', 'Praying', 'Waiting',
  'Cleaning', 'Cooking', 'Serving', 'Watching', 'Thinking', 'Resting'
]

// Computed
const canCreateNPC = computed(() => {
  return newNPC.value.name.trim() && newNPC.value.occupation && newNPC.value.race && newNPC.value.faction
})

// Methods
const generateRandomNPC = () => {
  const randomName = generateRandomName()
  const randomOccupation = occupations[Math.floor(Math.random() * occupations.length)]
  const randomRace = races[Math.floor(Math.random() * races.length)]
  const randomFaction = factions[Math.floor(Math.random() * factions.length)]
  
  newNPC.value = {
    name: randomName,
    occupation: randomOccupation,
    race: randomRace,
    gender: Math.random() > 0.5 ? 'male' : 'female',
    ageCategory: ['young', 'adult', 'middle-aged', 'elderly'][Math.floor(Math.random() * 4)],
    faction: randomFaction.id,
    personality: {
      friendliness: Math.floor(Math.random() * 100),
      aggression: Math.floor(Math.random() * 100),
      intelligence: Math.floor(Math.random() * 100),
      curiosity: Math.floor(Math.random() * 100),
      trustworthiness: Math.floor(Math.random() * 100),
      greed: Math.floor(Math.random() * 100),
      courage: Math.floor(Math.random() * 100),
      humor: Math.floor(Math.random() * 100)
    }
  }
}

const generateRandomName = (): string => {
  const maleNames = ['Wilhelm', 'Heinrich', 'Klaus', 'Otto', 'Franz', 'Ludwig', 'Gunther', 'Siegfried']
  const femaleNames = ['Brunhilde', 'Gretchen', 'Ingrid', 'Helga', 'Ursula', 'Mathilde', 'Astrid', 'Elsa']
  const surnames = ['Schmidt', 'Mueller', 'Weber', 'Fischer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann']
  
  const firstNames = newNPC.value.gender === 'female' ? femaleNames : maleNames
  const firstName = firstNames[Math.floor(Math.random() * firstNames.length)]
  const surname = surnames[Math.floor(Math.random() * surnames.length)]
  
  return `${firstName} ${surname}`
}

const createNPC = () => {
  if (!canCreateNPC.value) return
  
  const npc: NPC = {
    id: `npc-${Date.now()}`,
    name: newNPC.value.name,
    occupation: newNPC.value.occupation,
    race: newNPC.value.race,
    gender: newNPC.value.gender,
    ageCategory: newNPC.value.ageCategory,
    faction: newNPC.value.faction,
    active: true,
    currentMood: moods[Math.floor(Math.random() * moods.length)],
    currentActivity: activities[Math.floor(Math.random() * activities.length)],
    dialogueStyle: generateDialogueStyle(newNPC.value),
    personality: { ...newNPC.value.personality },
    createdAt: new Date()
  }
  
  activeNPCs.value.push(npc)
  
  // Reset form
  newNPC.value = {
    name: '',
    occupation: '',
    race: '',
    gender: 'male',
    ageCategory: 'adult',
    faction: '',
    personality: {
      friendliness: 50,
      aggression: 30,
      intelligence: 60,
      curiosity: 70,
      trustworthiness: 80,
      greed: 25,
      courage: 65,
      humor: 55
    }
  }
  
  console.log('Created NPC:', npc.name)
}

const generateDialogueStyle = (npcData: any): string => {
  const styles = []
  
  if (npcData.personality.friendliness > 70) styles.push('friendly and welcoming')
  if (npcData.personality.aggression > 70) styles.push('quick to anger')
  if (npcData.personality.intelligence > 70) styles.push('speaks eloquently')
  if (npcData.personality.humor > 70) styles.push('often makes jokes')
  if (npcData.personality.greed > 70) styles.push('always mentions money')
  
  return styles.length > 0 ? styles.join(', ') : 'speaks in a typical manner'
}

const selectNPC = (npc: NPC) => {
  selectedNPC.value = npc
}

const editNPC = (npc: NPC) => {
  selectedNPC.value = npc
}

const toggleNPCActive = (npc: NPC) => {
  npc.active = !npc.active
  console.log(`${npc.name} is now ${npc.active ? 'active' : 'inactive'}`)
}

const removeNPC = (npc: NPC) => {
  if (confirm(`Remove ${npc.name} from the tavern?`)) {
    const index = activeNPCs.value.findIndex(n => n.id === npc.id)
    if (index > -1) {
      activeNPCs.value.splice(index, 1)
      if (selectedNPC.value?.id === npc.id) {
        selectedNPC.value = null
      }
    }
  }
}

const updateNPCPersonality = () => {
  if (selectedNPC.value) {
    console.log('Updated personality for:', selectedNPC.value.name)
  }
}

const updateNPCDialogue = () => {
  if (selectedNPC.value) {
    console.log('Updated dialogue style for:', selectedNPC.value.name)
  }
}

const updateNPCState = () => {
  if (selectedNPC.value) {
    console.log('Updated state for:', selectedNPC.value.name)
  }
}

const saveNPCChanges = () => {
  if (selectedNPC.value) {
    console.log('Saved changes for:', selectedNPC.value.name)
    // Here you would save to persistent storage
  }
}

const getFactionClass = (factionId: string): string => {
  const faction = factions.find(f => f.id === factionId)
  return faction ? faction.color : 'bg-gray-600'
}

const getFactionName = (factionId: string): string => {
  const faction = factions.find(f => f.id === factionId)
  return faction ? faction.name : 'Unknown'
}

const getNPCIcon = (npc: NPC): string => {
  const iconMap: Record<string, string> = {
    'Barkeep': 'cup',
    'Cook': 'utensils',
    'Bard': 'music',
    'Merchant': 'package',
    'Soldier': 'sword',
    'Guard': 'shield',
    'Priest': 'heart',
    'Scholar': 'book',
    'Noble': 'crown'
  }
  
  return iconMap[npc.occupation] || 'user'
}

// Initialize with some default NPCs
onMounted(() => {
  activeNPCs.value = [
    {
      id: 'npc-1',
      name: 'Wilhelm the Barkeep',
      occupation: 'Barkeep',
      race: 'Human',
      gender: 'male',
      ageCategory: 'middle-aged',
      faction: 'empire',
      active: true,
      currentMood: 'Friendly',
      currentActivity: 'Serving',
      dialogueStyle: 'Friendly and welcoming, speaks with authority about tavern matters',
      personality: {
        friendliness: 85,
        aggression: 20,
        intelligence: 70,
        curiosity: 60,
        trustworthiness: 90,
        greed: 30,
        courage: 65,
        humor: 75
      },
      createdAt: new Date()
    }
  ]
})
</script>

<style scoped>
.npc-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.npc-card:hover {
  transform: translateY(-4px);
}

.trait-control {
  transition: all 0.2s ease;
}

.stat-item {
  animation: slideInUp 0.5s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
