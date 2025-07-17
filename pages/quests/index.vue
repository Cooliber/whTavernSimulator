<template>
  <div class="quests-page relative min-h-screen overflow-hidden">
    <!-- Epic background effects -->
    <InteractiveGridPattern 
      :grid-size="80"
      grid-color="#8b4513"
      :stroke-width="2"
      :proximity-radius="120"
      proximity-color="#ffd700"
      class="absolute inset-0 opacity-15"
    />
    <Meteors :meteor-count="8" :meteor-speed="0.7" />
    <ParticlesBg 
      :particle-count="30"
      particle-color="#ffd700"
      :particle-size="1"
      :animation-speed="0.4"
      class="opacity-30"
    />
    
    <div class="relative z-10 space-y-12 p-8">
      <!-- Epic Header -->
      <section class="text-center space-y-8">
        <Spotlight 
          spotlight-color="rgba(255, 69, 0, 0.5)"
          :spotlight-size="500"
          class="inline-block"
        >
          <div class="space-y-6">
            <SparklesText 
              text="Quest Board of Legends"
              class="text-6xl md:text-8xl font-medieval text-foreground"
              :sparkles-count="30"
            />
            <Text3D 
              text="Forge Your Destiny in the Old World"
              class="text-2xl md:text-3xl font-fantasy text-primary"
              :depth="5"
            />
          </div>
        </Spotlight>
        
        <!-- Quest Statistics Dashboard -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
          <BorderBeam 
            v-for="stat in questStats" 
            :key="stat.id"
            class="quest-stat-card bg-card/80 backdrop-blur-md rounded-xl p-6"
            :border-width="3"
            :color-from="stat.color"
            :color-to="stat.color + '80'"
          >
            <Card3D 
              class="text-center space-y-3"
              :rotation-intensity="15"
            >
              <div class="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center">
                <Icon :name="stat.icon" class="w-8 h-8 text-primary" />
              </div>
              <NumberTicker 
                :value="stat.value"
                class="text-3xl font-medieval text-foreground"
              />
              <p class="text-sm text-muted-foreground font-medieval">{{ stat.label }}</p>
            </Card3D>
          </BorderBeam>
        </div>
      </section>

      <!-- Available Quests -->
      <section class="space-y-6">
        <HyperText 
          text="Available Quests"
          class="text-3xl font-medieval text-foreground"
          :animation-duration="1500"
        />
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="quest in availableQuests" 
            :key="quest.id"
            class="available-quest-card"
          >
            <BorderBeam 
              class="quest-card bg-card/70 backdrop-blur-md rounded-xl overflow-hidden hover:scale-105 transition-all duration-300 cursor-pointer"
              :border-width="2"
              :color-from="quest.difficulty.color"
              :color-to="quest.difficulty.color + '40'"
              @click="acceptQuest(quest)"
            >
              <Spotlight 
                :spotlight-color="quest.difficulty.color + '30'"
                :spotlight-size="150"
                class="quest-spotlight"
              >
                <div class="p-6 space-y-4">
                  <!-- Quest Header -->
                  <div class="space-y-2">
                    <div class="flex items-center justify-between">
                      <h3 class="text-lg font-medieval text-foreground">{{ quest.title }}</h3>
                      <div 
                        class="w-3 h-3 rounded-full"
                        :class="quest.difficulty.bgClass"
                      />
                    </div>
                    <p class="text-sm text-muted-foreground">{{ quest.giver }}</p>
                  </div>
                  
                  <!-- Quest Preview -->
                  <TextReveal 
                    :text="quest.shortDescription"
                    class="text-sm text-foreground leading-relaxed"
                    :reveal-speed="25"
                    trigger="visible"
                  />
                  
                  <!-- Quest Info -->
                  <div class="grid grid-cols-2 gap-4 text-xs">
                    <div class="space-y-1">
                      <p class="text-muted-foreground">Location:</p>
                      <p class="text-foreground font-medieval">{{ quest.location }}</p>
                    </div>
                    <div class="space-y-1">
                      <p class="text-muted-foreground">Reward:</p>
                      <div class="flex items-center space-x-1">
                        <Icon name="star" class="w-3 h-3 text-yellow-400" />
                        <span class="text-yellow-400 font-medieval">{{ quest.goldReward }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Accept Button -->
                  <RippleButton 
                    class="w-full text-sm font-medieval"
                    :class="quest.difficulty.buttonClass"
                    :ripple-color="quest.difficulty.rippleColor"
                  >
                    <Icon name="plus" class="w-4 h-4 mr-2" />
                    Accept Quest
                  </RippleButton>
                </div>
              </Spotlight>
            </BorderBeam>
          </div>
        </div>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'Quest Board - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Embark on epic quests in the Warhammer Fantasy world. Accept challenges, earn rewards, and forge your legend.' }
  ]
})

// Quest statistics
const questStats = ref([
  {
    id: 'completed',
    label: 'Completed',
    value: 47,
    icon: 'check',
    color: '#22c55e'
  },
  {
    id: 'active',
    label: 'Active',
    value: 3,
    icon: 'play',
    color: '#3b82f6'
  },
  {
    id: 'available',
    label: 'Available',
    value: 12,
    icon: 'scroll',
    color: '#f59e0b'
  },
  {
    id: 'reputation',
    label: 'Reputation',
    value: 2847,
    icon: 'crown',
    color: '#8b5cf6'
  }
])

// Available quests data
const availableQuests = ref([
  {
    id: 'rats-in-cellar',
    title: 'Rats in the Cellar',
    giver: 'Tavern Keeper Wilhelm',
    shortDescription: 'The tavern cellar has been overrun by giant rats. Clear them out before they spoil the ale stores.',
    location: 'Tavern Cellar',
    goldReward: '50 Gold',
    difficulty: {
      name: 'Easy',
      level: 1,
      color: '#22c55e',
      bgClass: 'bg-green-500',
      buttonClass: 'bg-green-600 text-white',
      rippleColor: 'rgba(34, 197, 94, 0.6)'
    },
    timeLimit: '2 hours',
    recommendedLevel: '1-3'
  },
  {
    id: 'missing-merchant',
    title: 'The Missing Merchant',
    giver: 'Captain Marcus Brightblade',
    shortDescription: 'A wealthy merchant has gone missing on the road to Altdorf. Find him and ensure his safe return.',
    location: 'Old Forest Road',
    goldReward: '200 Gold',
    difficulty: {
      name: 'Medium',
      level: 2,
      color: '#f59e0b',
      bgClass: 'bg-yellow-500',
      buttonClass: 'bg-yellow-600 text-white',
      rippleColor: 'rgba(245, 158, 11, 0.6)'
    },
    timeLimit: '1 day',
    recommendedLevel: '4-6'
  },
  {
    id: 'chaos-cultists',
    title: 'Chaos Cultists Discovered',
    giver: 'Witch Hunter Valdris',
    shortDescription: 'Reports of chaos cultist activity in the abandoned mill. Investigate and purge any heretical presence.',
    location: 'Abandoned Mill',
    goldReward: '500 Gold',
    difficulty: {
      name: 'Hard',
      level: 3,
      color: '#ef4444',
      bgClass: 'bg-red-500',
      buttonClass: 'bg-red-600 text-white',
      rippleColor: 'rgba(239, 68, 68, 0.6)'
    },
    timeLimit: '3 days',
    recommendedLevel: '7-10'
  },
  {
    id: 'ancient-artifact',
    title: 'The Ancient Artifact',
    giver: 'High Mage Elara',
    shortDescription: 'An ancient elven artifact has been detected in the ruins. Retrieve it before it falls into the wrong hands.',
    location: 'Elven Ruins',
    goldReward: '1000 Gold',
    difficulty: {
      name: 'Legendary',
      level: 4,
      color: '#8b5cf6',
      bgClass: 'bg-purple-500',
      buttonClass: 'bg-purple-600 text-white',
      rippleColor: 'rgba(139, 92, 246, 0.6)'
    },
    timeLimit: '1 week',
    recommendedLevel: '15+'
  },
  {
    id: 'orc-raiders',
    title: 'Orc Raiders',
    giver: 'Village Elder',
    shortDescription: 'Orc raiders have been attacking trade caravans. Drive them back to their mountain lairs.',
    location: 'Mountain Pass',
    goldReward: '300 Gold',
    difficulty: {
      name: 'Medium',
      level: 2,
      color: '#f59e0b',
      bgClass: 'bg-yellow-500',
      buttonClass: 'bg-yellow-600 text-white',
      rippleColor: 'rgba(245, 158, 11, 0.6)'
    },
    timeLimit: '2 days',
    recommendedLevel: '5-8'
  },
  {
    id: 'haunted-manor',
    title: 'The Haunted Manor',
    giver: 'Local Noble',
    shortDescription: 'Strange lights and sounds have been reported from the old manor. Investigate the supernatural disturbances.',
    location: 'Blackwood Manor',
    goldReward: '750 Gold',
    difficulty: {
      name: 'Hard',
      level: 3,
      color: '#ef4444',
      bgClass: 'bg-red-500',
      buttonClass: 'bg-red-600 text-white',
      rippleColor: 'rgba(239, 68, 68, 0.6)'
    },
    timeLimit: '5 days',
    recommendedLevel: '10-12'
  },
  {
    id: 'dragon-sighting',
    title: 'Dragon Sighting',
    giver: 'Imperial Commander',
    shortDescription: 'A dragon has been spotted in the northern mountains. Confirm the sighting and assess the threat level.',
    location: 'Dragon Peak',
    goldReward: '2000 Gold',
    difficulty: {
      name: 'Legendary',
      level: 4,
      color: '#8b5cf6',
      bgClass: 'bg-purple-500',
      buttonClass: 'bg-purple-600 text-white',
      rippleColor: 'rgba(139, 92, 246, 0.6)'
    },
    timeLimit: '2 weeks',
    recommendedLevel: '20+'
  },
  {
    id: 'herb-gathering',
    title: 'Rare Herb Collection',
    giver: 'Apothecary Helga',
    shortDescription: 'Collect rare healing herbs from the enchanted forest for important alchemical research.',
    location: 'Enchanted Forest',
    goldReward: '150 Gold',
    difficulty: {
      name: 'Easy',
      level: 1,
      color: '#22c55e',
      bgClass: 'bg-green-500',
      buttonClass: 'bg-green-600 text-white',
      rippleColor: 'rgba(34, 197, 94, 0.6)'
    },
    timeLimit: '4 hours',
    recommendedLevel: '2-4'
  },
  {
    id: 'bandit-leader',
    title: 'Bandit Leader Bounty',
    giver: 'Sheriff Gunther',
    shortDescription: 'The notorious bandit leader "Black Wolf" has a bounty on his head. Bring him to justice.',
    location: 'Bandit Hideout',
    goldReward: '800 Gold',
    difficulty: {
      name: 'Hard',
      level: 3,
      color: '#ef4444',
      bgClass: 'bg-red-500',
      buttonClass: 'bg-red-600 text-white',
      rippleColor: 'rgba(239, 68, 68, 0.6)'
    },
    timeLimit: '1 week',
    recommendedLevel: '8-12'
  }
])

// Methods
const acceptQuest = (quest: any) => {
  // Add quest acceptance logic
  console.log('Accepting quest:', quest.title)
  
  // Show acceptance notification
  // This would typically update the player's active quests
  alert(`Quest "${quest.title}" accepted! Check your quest log for details.`)
}

// Lifecycle
onMounted(() => {
  console.log('Quest Board loaded with', availableQuests.value.length, 'available quests')
})
</script>

<style scoped>
/* Quest page specific animations */
.quests-page {
  background-attachment: fixed;
}

.quest-stat-card {
  animation: stat-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.available-quest-card {
  animation: quest-entrance 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.quest-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.quest-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 215, 0, 0.2),
    0 0 30px rgba(255, 215, 0, 0.1);
}

/* Custom animations */
@keyframes stat-entrance {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes quest-entrance {
  0% {
    opacity: 0;
    transform: translateY(40px) rotateX(15deg);
  }
  100% {
    opacity: 1;
    transform: translateY(0) rotateX(0deg);
  }
}

/* Difficulty indicators */
.quest-card[data-difficulty="easy"] {
  border-left: 4px solid #22c55e;
}

.quest-card[data-difficulty="medium"] {
  border-left: 4px solid #f59e0b;
}

.quest-card[data-difficulty="hard"] {
  border-left: 4px solid #ef4444;
}

.quest-card[data-difficulty="legendary"] {
  border-left: 4px solid #8b5cf6;
}

/* Responsive design */
@media (max-width: 768px) {
  .quest-stat-card {
    animation-delay: 0s;
  }
  
  .available-quest-card {
    animation-delay: 0s;
  }
}

/* Performance optimizations */
.quest-card,
.quest-stat-card {
  will-change: transform;
}

/* Spotlight effects */
.quest-spotlight {
  transition: all 0.3s ease;
}

.quest-spotlight:hover {
  filter: brightness(1.1) saturate(1.2);
}
</style>