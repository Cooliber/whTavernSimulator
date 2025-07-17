<template>
  <div class="characters-page space-y-8">
    <!-- Meteors background effect -->
    <Meteors :meteor-count="6" :meteor-speed="0.8" />
    
    <!-- Page header with advanced effects -->
    <section class="relative">
      <div class="text-center space-y-6">
        <Spotlight 
          spotlight-color="rgba(255, 215, 0, 0.4)"
          :spotlight-size="300"
          class="inline-block"
        >
          <SparklesText 
            text="Legendary Characters"
            class="text-5xl md:text-7xl font-medieval text-foreground"
            :sparkles-count="20"
          />
        </Spotlight>
        
        <Text3D 
          text="Meet the Heroes & Villains of the Warhammer World"
          class="text-xl md:text-2xl font-fantasy text-primary"
          :depth="3"
        />
        
        <!-- Faction filter with morphing tabs -->
        <div class="flex justify-center">
          <div class="inspira-tabs-morphing flex space-x-2 p-2">
            <div class="tab-indicator" :style="tabIndicatorStyle" />
            <button 
              v-for="faction in factions" 
              :key="faction.id"
              class="relative z-10 px-6 py-3 rounded-lg font-medieval text-sm transition-colors"
              :class="{ 
                'text-foreground': selectedFaction === faction.id,
                'text-muted-foreground hover:text-foreground': selectedFaction !== faction.id 
              }"
              @click="selectFaction(faction.id)"
            >
              <Icon :name="faction.icon" class="w-4 h-4 mr-2 inline" />
              {{ faction.name }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Character gallery with advanced interactions -->
    <section class="space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="character in filteredCharacters" 
          :key="character.id"
          class="character-card-wrapper"
        >
          <!-- Character card with lens effect -->
          <Lens 
            :lens-size="200"
            :magnification="1.5"
            class="character-lens"
          >
            <Card3D 
              class="character-card inspira-card-character h-full"
              :rotation-intensity="20"
            >
              <div class="relative overflow-hidden">
                <!-- Character portrait with spotlight -->
                <Spotlight 
                  :spotlight-color="character.factionColor + '40'"
                  :spotlight-size="150"
                  class="character-portrait aspect-square bg-gradient-to-br from-amber-800 to-amber-900 flex items-center justify-center relative"
                >
                  <!-- Character icon -->
                  <Icon 
                    :name="character.icon" 
                    class="w-20 h-20 text-primary drop-shadow-lg"
                  />
                  
                  <!-- Faction emblem -->
                  <div class="absolute top-2 right-2 w-8 h-8 rounded-full flex items-center justify-center"
                       :class="character.factionBg">
                    <Icon :name="character.factionIcon" class="w-4 h-4 text-white" />
                  </div>
                  
                  <!-- Status indicator -->
                  <div class="absolute bottom-2 left-2 flex items-center space-x-1">
                    <div class="w-2 h-2 rounded-full animate-pulse"
                         :class="character.isOnline ? 'bg-green-400' : 'bg-gray-400'" />
                    <span class="text-xs text-white/80">
                      {{ character.isOnline ? 'Online' : 'Offline' }}
                    </span>
                  </div>
                </Spotlight>
                
                <!-- Character info -->
                <div class="p-6 space-y-4">
                  <!-- Name and title -->
                  <div class="space-y-2">
                    <HyperText 
                      :text="character.name"
                      class="text-xl font-medieval text-foreground"
                      :animation-duration="1500"
                    />
                    <p class="text-sm text-muted-foreground">{{ character.title }}</p>
                    <div class="flex items-center space-x-2">
                      <div class="w-3 h-3 rounded-full" :class="character.factionColor" />
                      <span class="text-xs font-medieval text-muted-foreground">{{ character.faction }}</span>
                    </div>
                  </div>
                  
                  <!-- Stats with number tickers -->
                  <div class="grid grid-cols-3 gap-4 text-center">
                    <div class="space-y-1">
                      <Icon name="sword" class="w-4 h-4 text-red-400 mx-auto" />
                      <NumberTicker 
                        :value="character.stats.attack"
                        class="text-lg font-bold text-red-400"
                      />
                      <p class="text-xs text-muted-foreground">Attack</p>
                    </div>
                    <div class="space-y-1">
                      <Icon name="shield" class="w-4 h-4 text-blue-400 mx-auto" />
                      <NumberTicker 
                        :value="character.stats.defense"
                        class="text-lg font-bold text-blue-400"
                      />
                      <p class="text-xs text-muted-foreground">Defense</p>
                    </div>
                    <div class="space-y-1">
                      <Icon name="sparkles" class="w-4 h-4 text-purple-400 mx-auto" />
                      <NumberTicker 
                        :value="character.stats.magic"
                        class="text-lg font-bold text-purple-400"
                      />
                      <p class="text-xs text-muted-foreground">Magic</p>
                    </div>
                  </div>
                  
                  <!-- Character description -->
                  <p class="text-sm text-muted-foreground leading-relaxed">
                    {{ character.description }}
                  </p>
                  
                  <!-- Action buttons -->
                  <div class="flex space-x-2">
                    <RippleButton 
                      class="flex-1 text-sm font-medieval"
                      :class="character.factionBg"
                      :ripple-color="character.factionColor"
                      @click="startConversation(character)"
                    >
                      <Icon name="message-circle" class="w-4 h-4 mr-2" />
                      Talk
                    </RippleButton>
                    
                    <ShimmerButton 
                      class="flex-1 text-sm font-medieval bg-secondary text-secondary-foreground"
                      shimmer-color="rgba(139, 69, 19, 0.5)"
                      @click="viewDetails(character)"
                    >
                      <Icon name="user" class="w-4 h-4 mr-2" />
                      Details
                    </ShimmerButton>
                  </div>
                </div>
              </div>
            </Card3D>
            
            <!-- Lens magnified content -->
            <template #magnified>
              <div class="character-magnified p-4 bg-black/80 text-white rounded-lg">
                <h3 class="font-medieval text-lg mb-2">{{ character.name }}</h3>
                <p class="text-sm mb-2">{{ character.title }}</p>
                <div class="space-y-1 text-xs">
                  <p><strong>Faction:</strong> {{ character.faction }}</p>
                  <p><strong>Location:</strong> {{ character.location }}</p>
                  <p><strong>Mood:</strong> {{ character.mood }}</p>
                </div>
              </div>
            </template>
          </Lens>
        </div>
      </div>
    </section>

    <!-- Character interaction modal -->
    <div 
      v-if="selectedCharacter"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click="closeModal"
    >
      <BorderBeam 
        class="character-modal bg-background border border-border rounded-2xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
        :border-width="3"
        :color-from="selectedCharacter.factionColor"
        :color-to="selectedCharacter.factionColor + '80'"
        @click.stop
      >
        <div class="space-y-6">
          <!-- Modal header -->
          <div class="text-center space-y-4">
            <div class="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-amber-800 to-amber-900 flex items-center justify-center">
              <Icon :name="selectedCharacter.icon" class="w-12 h-12 text-primary" />
            </div>
            
            <div>
              <SparklesText 
                :text="selectedCharacter.name"
                class="text-3xl font-medieval text-foreground"
                :sparkles-count="15"
              />
              <p class="text-lg text-muted-foreground">{{ selectedCharacter.title }}</p>
            </div>
          </div>
          
          <!-- Character details -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <h3 class="text-lg font-medieval text-foreground">Character Info</h3>
              <div class="space-y-2 text-sm">
                <p><strong>Faction:</strong> {{ selectedCharacter.faction }}</p>
                <p><strong>Location:</strong> {{ selectedCharacter.location }}</p>
                <p><strong>Mood:</strong> {{ selectedCharacter.mood }}</p>
                <p><strong>Status:</strong> 
                  <span :class="selectedCharacter.isOnline ? 'text-green-400' : 'text-gray-400'">
                    {{ selectedCharacter.isOnline ? 'Available' : 'Busy' }}
                  </span>
                </p>
              </div>
            </div>
            
            <div class="space-y-4">
              <h3 class="text-lg font-medieval text-foreground">Abilities</h3>
              <div class="space-y-3">
                <div 
                  v-for="ability in selectedCharacter.abilities" 
                  :key="ability.name"
                  class="flex items-center justify-between"
                >
                  <span class="text-sm">{{ ability.name }}</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-16 h-2 bg-muted rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-gradient-to-r from-primary to-primary/60 transition-all duration-1000"
                        :style="{ width: ability.level + '%' }"
                      />
                    </div>
                    <span class="text-xs text-muted-foreground">{{ ability.level }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Action buttons -->
          <div class="flex space-x-4 justify-center">
            <RippleButton 
              class="px-8 py-3 font-medieval"
              :class="selectedCharacter.factionBg"
              :ripple-color="selectedCharacter.factionColor"
              @click="startConversation(selectedCharacter)"
            >
              <Icon name="message-circle" class="w-5 h-5 mr-2" />
              Start Conversation
            </RippleButton>
            
            <ShimmerButton 
              class="px-8 py-3 font-medieval bg-secondary text-secondary-foreground"
              shimmer-color="rgba(139, 69, 19, 0.5)"
              @click="closeModal"
            >
              Close
            </ShimmerButton>
          </div>
        </div>
      </BorderBeam>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'Characters - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Meet the legendary characters of the Warhammer Fantasy world in our immersive tavern simulator.' }
  ]
})

// Faction data
const factions = ref([
  { id: 'all', name: 'All Factions', icon: 'users' },
  { id: 'empire', name: 'Empire', icon: 'crown' },
  { id: 'chaos', name: 'Chaos', icon: 'flame' },
  { id: 'elves', name: 'Elves', icon: 'leaf' },
  { id: 'dwarfs', name: 'Dwarfs', icon: 'hammer' },
  { id: 'undead', name: 'Undead', icon: 'skull' }
])

const selectedFaction = ref('all')
const selectedCharacter = ref(null)

// Character data with enhanced details
const characters = ref([
  {
    id: 'marcus',
    name: 'Sir Marcus Brightblade',
    title: 'Knight of the Blazing Sun',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    factionBg: 'bg-faction-empire-600',
    factionIcon: 'crown',
    icon: 'sword',
    description: 'A noble knight of the Empire, seeking glory and honor in service to Sigmar. His blade has never known defeat.',
    location: 'Main Hall',
    mood: 'Confident',
    isOnline: true,
    stats: {
      attack: 85,
      defense: 78,
      magic: 45
    },
    abilities: [
      { name: 'Swordsmanship', level: 95 },
      { name: 'Leadership', level: 88 },
      { name: 'Tactics', level: 82 },
      { name: 'Divine Magic', level: 60 }
    ]
  },
  {
    id: 'grimjaw',
    name: 'Grimjaw Ironbeard',
    title: 'Slayer of the Broken Chain',
    faction: 'Dwarfs',
    factionColor: 'bg-faction-dwarfs-500',
    factionBg: 'bg-faction-dwarfs-600',
    factionIcon: 'hammer',
    icon: 'hammer',
    description: 'A fierce dwarf warrior who has taken the Slayer Oath to redeem his honor. Death before dishonor!',
    location: 'Ale Corner',
    mood: 'Brooding',
    isOnline: true,
    stats: {
      attack: 92,
      defense: 65,
      magic: 20
    },
    abilities: [
      { name: 'Berserker Rage', level: 98 },
      { name: 'Axe Mastery', level: 95 },
      { name: 'Endurance', level: 90 },
      { name: 'Intimidation', level: 85 }
    ]
  },
  {
    id: 'elara',
    name: 'Elara Moonwhisper',
    title: 'High Mage of Hoeth',
    faction: 'Elves',
    factionColor: 'bg-faction-elves-500',
    factionBg: 'bg-faction-elves-600',
    factionIcon: 'leaf',
    icon: 'sparkles',
    description: 'An elegant elven sorceress mastering the winds of magic. Her knowledge spans centuries.',
    location: 'Quiet Alcove',
    mood: 'Contemplative',
    isOnline: false,
    stats: {
      attack: 70,
      defense: 55,
      magic: 98
    },
    abilities: [
      { name: 'High Magic', level: 98 },
      { name: 'Lore of Light', level: 92 },
      { name: 'Enchantment', level: 88 },
      { name: 'Meditation', level: 95 }
    ]
  },
  {
    id: 'thorgrim',
    name: 'Thorgrim the Bold',
    title: 'Ranger of the Grey Mountains',
    faction: 'Dwarfs',
    factionColor: 'bg-faction-dwarfs-500',
    factionBg: 'bg-faction-dwarfs-600',
    factionIcon: 'hammer',
    icon: 'bow',
    description: 'A seasoned ranger who knows every path through the mountains. His aim never misses.',
    location: 'By the Window',
    mood: 'Alert',
    isOnline: true,
    stats: {
      attack: 75,
      defense: 80,
      magic: 30
    },
    abilities: [
      { name: 'Marksmanship', level: 96 },
      { name: 'Tracking', level: 92 },
      { name: 'Survival', level: 90 },
      { name: 'Stealth', level: 78 }
    ]
  },
  {
    id: 'valdris',
    name: 'Valdris Shadowbane',
    title: 'Witch Hunter Captain',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    factionBg: 'bg-faction-empire-600',
    factionIcon: 'crown',
    icon: 'flame',
    description: 'A grim hunter of heretics and creatures of darkness. His faith is his shield.',
    location: 'Dark Corner',
    mood: 'Vigilant',
    isOnline: true,
    stats: {
      attack: 88,
      defense: 70,
      magic: 65
    },
    abilities: [
      { name: 'Heretic Detection', level: 95 },
      { name: 'Pistol Mastery', level: 90 },
      { name: 'Divine Protection', level: 85 },
      { name: 'Interrogation', level: 88 }
    ]
  },
  {
    id: 'lyralei',
    name: 'Lyralei Starweaver',
    title: 'Scout of Athel Loren',
    faction: 'Elves',
    factionColor: 'bg-faction-elves-500',
    factionBg: 'bg-faction-elves-600',
    factionIcon: 'leaf',
    icon: 'leaf',
    description: 'A swift scout from the forests of Athel Loren. She moves like the wind through trees.',
    location: 'Garden Entrance',
    mood: 'Curious',
    isOnline: false,
    stats: {
      attack: 82,
      defense: 60,
      magic: 75
    },
    abilities: [
      { name: 'Forest Lore', level: 95 },
      { name: 'Archery', level: 90 },
      { name: 'Nature Magic', level: 85 },
      { name: 'Camouflage', level: 92 }
    ]
  },
  {
    id: 'malachar',
    name: 'Malachar the Damned',
    title: 'Chaos Sorcerer',
    faction: 'Chaos',
    factionColor: 'bg-faction-chaos-500',
    factionBg: 'bg-faction-chaos-600',
    factionIcon: 'flame',
    icon: 'flame',
    description: 'A fallen wizard who has embraced the dark powers of Chaos. His presence chills the air.',
    location: 'Shadowed Booth',
    mood: 'Malevolent',
    isOnline: true,
    stats: {
      attack: 65,
      defense: 50,
      magic: 95
    },
    abilities: [
      { name: 'Chaos Magic', level: 98 },
      { name: 'Corruption', level: 90 },
      { name: 'Dark Rituals', level: 95 },
      { name: 'Fear Aura', level: 85 }
    ]
  },
  {
    id: 'necromancer',
    name: 'Heinrich von Carstein',
    title: 'Vampire Lord',
    faction: 'Undead',
    factionColor: 'bg-faction-undead-500',
    factionBg: 'bg-faction-undead-600',
    factionIcon: 'skull',
    icon: 'skull',
    description: 'An ancient vampire lord with centuries of dark knowledge. Death is but a doorway for him.',
    location: 'Crypt Entrance',
    mood: 'Ancient',
    isOnline: false,
    stats: {
      attack: 90,
      defense: 85,
      magic: 88
    },
    abilities: [
      { name: 'Necromancy', level: 95 },
      { name: 'Vampiric Powers', level: 98 },
      { name: 'Undead Command', level: 92 },
      { name: 'Ancient Wisdom', level: 90 }
    ]
  }
])

// Computed properties
const filteredCharacters = computed(() => {
  if (selectedFaction.value === 'all') {
    return characters.value
  }
  return characters.value.filter(char => 
    char.faction.toLowerCase() === selectedFaction.value.toLowerCase()
  )
})

const tabIndicatorStyle = computed(() => {
  const index = factions.value.findIndex(f => f.id === selectedFaction.value)
  return {
    left: `${index * 120}px`, // Approximate width per tab
    width: '120px'
  }
})

// Methods
const selectFaction = (factionId: string) => {
  selectedFaction.value = factionId
}

const startConversation = (character: any) => {
  // Navigate to conversation page
  navigateTo(`/conversations/${character.id}`)
}

const viewDetails = (character: any) => {
  selectedCharacter.value = character
}

const closeModal = () => {
  selectedCharacter.value = null
}

// Lifecycle
onMounted(() => {
  console.log('Characters page loaded with', characters.value.length, 'characters')
})
</script>

<style scoped>
/* Character card animations */
.character-card-wrapper {
  animation: medieval-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.character-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.character-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 215, 0, 0.2),
    0 0 20px rgba(255, 215, 0, 0.1);
}

/* Faction tabs styling */
.inspira-tabs-morphing {
  position: relative;
  background: rgba(139, 69, 19, 0.2);
  border-radius: 12px;
  padding: 4px;
}

.tab-indicator {
  position: absolute;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.9), rgba(184, 134, 11, 0.9));
  border-radius: 8px;
  height: calc(100% - 8px);
  top: 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

/* Character modal animations */
.character-modal {
  animation: modal-entrance 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes modal-entrance {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Lens effect enhancements */
.character-lens {
  transition: all 0.3s ease;
}

.character-lens:hover {
  z-index: 10;
}

/* Responsive design */
@media (max-width: 768px) {
  .character-card-wrapper {
    animation-delay: 0s;
  }
  
  .tab-indicator {
    width: 100px !important;
    left: calc(var(--index, 0) * 100px) !important;
  }
}

/* Performance optimizations */
.character-card,
.character-lens,
.character-modal {
  will-change: transform;
}
</style>