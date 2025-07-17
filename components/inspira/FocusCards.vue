<template>
  <div 
    class="focus-cards-container relative"
    :class="className"
  >
    <div 
      class="cards-grid grid gap-6 transition-all duration-500"
      :class="gridClasses"
    >
      <div 
        v-for="(card, index) in cards" 
        :key="card.id"
        ref="cardRefs"
        class="focus-card relative cursor-pointer transition-all duration-500 ease-out"
        :class="getCardClasses(index)"
        :style="getCardStyle(index)"
        @mouseenter="handleCardHover(index)"
        @mouseleave="handleCardLeave"
        @click="handleCardClick(index)"
        @touchstart="handleTouchStart(index)"
        @touchend="handleTouchEnd"
      >
        <!-- Card Background with Faction Theme -->
        <div 
          class="card-background absolute inset-0 rounded-xl transition-all duration-500"
          :class="getFactionBackground(card.faction)"
        />
        
        <!-- Card Content -->
        <div class="card-content relative z-10 p-6 h-full flex flex-col">
          <!-- Character Avatar -->
          <div class="avatar-container mb-4 flex justify-center">
            <div 
              class="avatar relative w-20 h-20 rounded-full overflow-hidden border-3 transition-all duration-300"
              :class="getFactionBorder(card.faction)"
            >
              <img 
                v-if="card.avatar"
                :src="card.avatar" 
                :alt="card.name"
                class="w-full h-full object-cover"
              />
              <div 
                v-else
                class="w-full h-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center"
              >
                <Icon name="user" class="w-10 h-10 text-primary" />
              </div>
              
              <!-- Avatar glow effect -->
              <div 
                class="avatar-glow absolute inset-0 rounded-full opacity-0 transition-opacity duration-300"
                :class="getFactionGlow(card.faction)"
              />
            </div>
          </div>
          
          <!-- Character Name -->
          <div class="text-center mb-3">
            <HyperText 
              :text="card.name"
              class="text-xl font-medieval text-foreground"
              :animation-duration="800"
            />
            <p class="text-sm text-muted-foreground mt-1">{{ card.title || getFactionTitle(card.faction) }}</p>
          </div>
          
          <!-- Character Description -->
          <div class="description flex-1 mb-4">
            <p class="text-sm text-foreground/80 leading-relaxed line-clamp-3">
              {{ card.description }}
            </p>
          </div>
          
          <!-- Character Stats (if available) -->
          <div v-if="card.stats" class="stats grid grid-cols-2 gap-2 text-xs">
            <div 
              v-for="(value, stat) in card.stats" 
              :key="stat"
              class="stat-item flex justify-between p-2 rounded bg-background/50"
            >
              <span class="stat-name capitalize text-muted-foreground">{{ stat }}</span>
              <span class="stat-value font-bold text-foreground">{{ value }}</span>
            </div>
          </div>
          
          <!-- Faction Badge -->
          <div class="faction-badge absolute top-3 right-3">
            <div 
              class="px-2 py-1 rounded-full text-xs font-medieval"
              :class="getFactionBadge(card.faction)"
            >
              {{ card.faction }}
            </div>
          </div>
        </div>
        
        <!-- Focus Overlay -->
        <div 
          class="focus-overlay absolute inset-0 rounded-xl pointer-events-none transition-all duration-500"
          :class="{ 'opacity-100': focusedCard === index, 'opacity-0': focusedCard !== index }"
          :style="getFocusOverlayStyle(card.faction)"
        />
      </div>
    </div>
    
    <!-- Blur Background -->
    <div 
      class="blur-background fixed inset-0 pointer-events-none transition-all duration-500 z-0"
      :class="{ 'backdrop-blur-md': focusedCard !== null }"
      :style="{ opacity: focusedCard !== null ? 0.8 : 0 }"
    />
  </div>
</template>

<script setup lang="ts">
interface CharacterCard {
  id: string
  name: string
  faction: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
  avatar?: string
  title?: string
  description: string
  stats?: Record<string, number>
}

interface Props {
  cards: CharacterCard[]
  focusMode?: 'hover' | 'click' | 'auto'
  blurIntensity?: number
  scaleIntensity?: number
  gridCols?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  focusMode: 'hover',
  blurIntensity: 8,
  scaleIntensity: 1.05,
  gridCols: 3,
  className: ''
})

const emit = defineEmits<{
  cardFocus: [card: CharacterCard, index: number]
  cardBlur: []
  cardClick: [card: CharacterCard, index: number]
}>()

// Reactive state
const cardRefs = ref<HTMLElement[]>([])
const focusedCard = ref<number | null>(null)
const touchStartTime = ref(0)

// Computed properties
const gridClasses = computed(() => {
  const colsMap = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  }
  return colsMap[props.gridCols as keyof typeof colsMap] || 'grid-cols-3'
})

// Methods
const getCardClasses = (index: number) => {
  const isFocused = focusedCard.value === index
  const isBlurred = focusedCard.value !== null && focusedCard.value !== index
  
  return {
    'scale-105 z-20': isFocused,
    'scale-95 opacity-50': isBlurred,
    'hover:scale-102': focusedCard.value === null
  }
}

const getCardStyle = (index: number) => {
  const isFocused = focusedCard.value === index
  return {
    transform: isFocused ? `scale(${props.scaleIntensity})` : 'scale(1)',
    zIndex: isFocused ? 20 : 1
  }
}

const getFactionBackground = (faction: string) => {
  const backgrounds = {
    empire: 'bg-gradient-to-br from-yellow-900/90 to-yellow-800/90',
    chaos: 'bg-gradient-to-br from-red-900/90 to-red-800/90',
    elves: 'bg-gradient-to-br from-green-900/90 to-green-800/90',
    dwarfs: 'bg-gradient-to-br from-amber-900/90 to-amber-800/90',
    undead: 'bg-gradient-to-br from-purple-900/90 to-purple-800/90',
    orcs: 'bg-gradient-to-br from-green-800/90 to-green-700/90'
  }
  return backgrounds[faction as keyof typeof backgrounds] || backgrounds.empire
}

const getFactionBorder = (faction: string) => {
  const borders = {
    empire: 'border-yellow-400',
    chaos: 'border-red-400',
    elves: 'border-green-400',
    dwarfs: 'border-amber-400',
    undead: 'border-purple-400',
    orcs: 'border-green-500'
  }
  return borders[faction as keyof typeof borders] || borders.empire
}

const getFactionGlow = (faction: string) => {
  const glows = {
    empire: 'bg-yellow-400/30',
    chaos: 'bg-red-400/30',
    elves: 'bg-green-400/30',
    dwarfs: 'bg-amber-400/30',
    undead: 'bg-purple-400/30',
    orcs: 'bg-green-500/30'
  }
  return glows[faction as keyof typeof glows] || glows.empire
}

const getFactionBadge = (faction: string) => {
  const badges = {
    empire: 'bg-yellow-600 text-yellow-100',
    chaos: 'bg-red-600 text-red-100',
    elves: 'bg-green-600 text-green-100',
    dwarfs: 'bg-amber-600 text-amber-100',
    undead: 'bg-purple-600 text-purple-100',
    orcs: 'bg-green-700 text-green-100'
  }
  return badges[faction as keyof typeof badges] || badges.empire
}

const getFactionTitle = (faction: string) => {
  const titles = {
    empire: 'Imperial Citizen',
    chaos: 'Chaos Warrior',
    elves: 'Elven Noble',
    dwarfs: 'Dwarf Craftsman',
    undead: 'Undead Minion',
    orcs: 'Orc Warrior'
  }
  return titles[faction as keyof typeof titles] || titles.empire
}

const getFocusOverlayStyle = (faction: string) => {
  const colors = {
    empire: 'rgba(255, 215, 0, 0.1)',
    chaos: 'rgba(139, 0, 0, 0.1)',
    elves: 'rgba(34, 139, 34, 0.1)',
    dwarfs: 'rgba(218, 165, 32, 0.1)',
    undead: 'rgba(128, 0, 128, 0.1)',
    orcs: 'rgba(34, 139, 34, 0.1)'
  }
  
  return {
    backgroundColor: colors[faction as keyof typeof colors] || colors.empire,
    boxShadow: `0 0 30px ${colors[faction as keyof typeof colors] || colors.empire}`
  }
}

// Event handlers
const handleCardHover = (index: number) => {
  if (props.focusMode === 'hover') {
    focusedCard.value = index
    emit('cardFocus', props.cards[index], index)
  }
}

const handleCardLeave = () => {
  if (props.focusMode === 'hover') {
    focusedCard.value = null
    emit('cardBlur')
  }
}

const handleCardClick = (index: number) => {
  if (props.focusMode === 'click') {
    focusedCard.value = focusedCard.value === index ? null : index
    if (focusedCard.value !== null) {
      emit('cardFocus', props.cards[index], index)
    } else {
      emit('cardBlur')
    }
  }
  emit('cardClick', props.cards[index], index)
}

const handleTouchStart = (index: number) => {
  touchStartTime.value = Date.now()
}

const handleTouchEnd = () => {
  const touchDuration = Date.now() - touchStartTime.value
  if (touchDuration < 200) { // Quick tap
    // Handle as click
  }
}

// Auto mode logic
let autoTimer: NodeJS.Timeout | null = null

const startAutoMode = () => {
  if (props.focusMode !== 'auto') return
  
  let currentIndex = 0
  autoTimer = setInterval(() => {
    focusedCard.value = currentIndex
    emit('cardFocus', props.cards[currentIndex], currentIndex)
    
    currentIndex = (currentIndex + 1) % props.cards.length
  }, 3000)
}

const stopAutoMode = () => {
  if (autoTimer) {
    clearInterval(autoTimer)
    autoTimer = null
  }
}

// Lifecycle
onMounted(() => {
  if (props.focusMode === 'auto') {
    startAutoMode()
  }
})

onUnmounted(() => {
  stopAutoMode()
})

// Watch for mode changes
watch(() => props.focusMode, (newMode) => {
  stopAutoMode()
  focusedCard.value = null
  
  if (newMode === 'auto') {
    startAutoMode()
  }
})

// Expose methods
defineExpose({
  focusCard: (index: number) => {
    focusedCard.value = index
    emit('cardFocus', props.cards[index], index)
  },
  blurAll: () => {
    focusedCard.value = null
    emit('cardBlur')
  },
  focusedCard: readonly(focusedCard)
})
</script>

<style scoped>
.focus-card {
  will-change: transform, opacity;
  transform: translate3d(0, 0, 0);
}

.card-background {
  backdrop-filter: blur(8px);
}

.avatar-glow {
  filter: blur(8px);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .focus-card {
    transform: none !important;
  }
  
  .cards-grid {
    gap: 1rem;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .focus-card,
  .card-background,
  .focus-overlay {
    transition-duration: 0.1s !important;
  }
}
</style>
