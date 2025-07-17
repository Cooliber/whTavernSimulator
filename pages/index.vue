<template>
  <div class="space-y-12">
    <!-- Hero Section with Enhanced Accessibility -->
    <section
      class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-amber-900/20 to-amber-800/20 p-8 md:p-12"
      role="banner"
      aria-labelledby="hero-title"
    >
      <!-- Background Effects -->
      <div
        class="absolute inset-0"
        :class="{ 'opacity-5': prefersReducedMotion }"
        role="presentation"
        aria-hidden="true"
      >
        <LiquidBackground
          :colors="['#8b4513', '#a0522d', '#cd853f']"
          :blob-count="prefersReducedMotion ? 1 : 3"
          class="opacity-20"
        />
      </div>

      <!-- Content -->
      <div class="relative z-10 text-center space-y-6">
        <div class="space-y-4">
          <SparklesText
            id="hero-title"
            :text="$t('hero.title')"
            class="text-4xl md:text-6xl font-medieval text-foreground"
            :sparkles-count="prefersReducedMotion ? 0 : 15"
            role="heading"
            aria-level="1"
          />
          <Text3D
            :text="$t('hero.subtitle')"
            class="text-2xl md:text-3xl font-fantasy text-primary"
            :depth="prefersReducedMotion ? 0 : 3"
            role="heading"
            aria-level="2"
          />
        </div>

        <p
          class="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed"
          role="text"
        >
          {{ $t('hero.description', {
            aiNpcs: `<span class="text-primary font-medieval">${$t('hero.aiNpcs')}</span>`,
            inspiraUi: `<span class="text-primary font-medieval">${$t('hero.inspiraUi')}</span>`
          }) }}
        </p>

        <div
          class="flex flex-col sm:flex-row gap-4 justify-center items-center"
          role="group"
          aria-label="Main navigation actions"
        >
          <RippleButton
            class="faction-empire px-8 py-3 text-lg font-medieval wh-focus-ring"
            ripple-color="rgb(255, 215, 0)"
            :aria-label="$t('hero.enterTavernAriaLabel')"
            @click="enterTavern"
          >
            <Icon name="door-open" class="w-5 h-5 mr-2" aria-hidden="true" />
            {{ $t('hero.enterTavern') }}
          </RippleButton>

          <RainbowButton
            :colors="['#228b22', '#32cd32', '#90ee90']"
            class="px-8 py-3 text-lg font-medieval wh-focus-ring"
            :aria-label="$t('hero.meetCharactersAriaLabel')"
            @click="viewCharacters"
          >
            <Icon name="users" class="w-5 h-5 mr-2" aria-hidden="true" />
            {{ $t('hero.meetCharacters') }}
          </RainbowButton>
        </div>
      </div>
    </section>

    <!-- Tavern Statistics -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card3D 
        v-for="stat in tavernStats" 
        :key="stat.id"
        class="inspira-card-tavern p-6"
        :rotation-intensity="10"
      >
        <div class="text-center space-y-4">
          <div class="w-16 h-16 mx-auto rounded-full bg-gradient-to-r from-primary/20 to-primary/10 flex items-center justify-center">
            <Icon :name="stat.icon" class="w-8 h-8 text-primary" />
          </div>
          <div>
            <NumberTicker 
              :value="stat.value"
              class="text-3xl font-medieval text-foreground"
            />
            <p class="text-sm text-muted-foreground font-medieval">{{ $t(`stats.${stat.key}`) }}</p>
          </div>
        </div>
      </Card3D>
    </section>

    <!-- Character Gallery -->
    <section class="space-y-6">
      <div class="text-center space-y-2">
        <HyperText
          :text="$t('characters.title')"
          class="text-3xl font-medieval text-foreground"
          :animation-duration="1500"
        />
        <p class="text-muted-foreground">{{ $t('characters.subtitle') }}</p>
      </div>
      
      <ExpandableGallery 
        :items="characters"
        class="character-gallery"
        :grid-cols="3"
        :gap="6"
      >
        <template #item="{ item, isExpanded }">
          <div 
            class="character-item relative overflow-hidden rounded-lg inspira-card-character transition-all duration-300"
            :class="{ 'scale-105': isExpanded }"
          >
            <DirectionAwareHover class="w-full h-full">
              <template #content>
                <div class="aspect-square bg-gradient-to-br from-amber-800 to-amber-900 flex items-center justify-center">
                  <Icon :name="item.icon" class="w-16 h-16 text-primary" />
                </div>
                <div class="p-4 space-y-2">
                  <h3 class="text-lg font-medieval text-foreground">{{ item.name }}</h3>
                  <p class="text-sm text-muted-foreground">{{ item.class }}</p>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="item.factionColor"></div>
                    <span class="text-xs text-muted-foreground">{{ item.faction }}</span>
                  </div>
                </div>
              </template>
              
              <template #hover>
                <div class="absolute inset-0 bg-black/80 flex items-center justify-center p-4">
                  <div class="text-center space-y-4">
                    <SparklesText 
                      :text="item.name"
                      class="text-xl font-medieval text-foreground"
                      :sparkles-count="8"
                    />
                    <p class="text-sm text-muted-foreground leading-relaxed">{{ item.description }}</p>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                      <div class="flex items-center justify-center space-x-1">
                        <Icon name="sword" class="w-3 h-3 text-red-400" />
                        <NumberTicker 
                          :value="item.stats.attack"
                          class="text-red-400 font-bold"
                        />
                      </div>
                      <div class="flex items-center justify-center space-x-1">
                        <Icon name="shield" class="w-3 h-3 text-blue-400" />
                        <NumberTicker 
                          :value="item.stats.defense"
                          class="text-blue-400 font-bold"
                        />
                      </div>
                    </div>
                    <ShimmerButton 
                      class="w-full text-xs font-medieval"
                      shimmer-color="rgb(255, 215, 0)"
                      @click="talkToCharacter(item)"
                    >
                      Start Conversation
                    </ShimmerButton>
                  </div>
                </div>
              </template>
            </DirectionAwareHover>
          </div>
        </template>
      </ExpandableGallery>
    </section>

    <!-- Recent Events Timeline -->
    <section class="space-y-6">
      <div class="text-center space-y-2">
        <HyperText 
          text="Recent Tavern Events"
          class="text-3xl font-medieval text-foreground"
          :animation-duration="1500"
        />
        <p class="text-muted-foreground">Stay updated with the latest happenings</p>
      </div>
      
      <Timeline :items="recentEvents">
        <template #item="{ item }">
          <div class="space-y-2">
            <div class="flex items-center space-x-2">
              <Icon :name="item.icon" class="w-4 h-4 text-primary" />
              <span class="text-sm font-medieval text-foreground">{{ item.title }}</span>
            </div>
            <p class="text-sm text-muted-foreground">{{ item.description }}</p>
            <span class="text-xs text-muted-foreground">{{ item.time }}</span>
          </div>
        </template>
      </Timeline>
    </section>

    <!-- Call to Action -->
    <section class="text-center space-y-6 py-12">
      <BorderBeam 
        class="max-w-2xl mx-auto p-8 bg-gradient-to-br from-primary/10 to-primary/5 rounded-2xl"
        :border-width="2"
        color-from="#ffd700"
        color-to="#b8860b"
      >
        <div class="space-y-4">
          <Text3D 
            text="Ready for Adventure?"
            class="text-2xl font-medieval text-foreground"
            :depth="2"
          />
          <p class="text-muted-foreground">
            Join the most immersive Warhammer Fantasy experience with AI-powered storytelling
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <RippleButton 
              class="faction-empire px-6 py-3 font-medieval"
              ripple-color="rgb(255, 215, 0)"
              @click="startAdventure"
            >
              Begin Your Journey
            </RippleButton>
            <ShimmerButton 
              class="px-6 py-3 font-medieval bg-secondary text-secondary-foreground"
              shimmer-color="rgb(139, 69, 19)"
              @click="learnMore"
            >
              Learn More
            </ShimmerButton>
          </div>
        </div>
      </BorderBeam>
    </section>
  </div>
</template><script setup lang="ts">
// Composables
const { t } = useI18n()

// Page metadata
useHead({
  title: () => `${t('hero.title')} - ${t('hero.subtitle')}`,
  meta: [
    { name: 'description', content: () => t('hero.description', { aiNpcs: t('hero.aiNpcs'), inspiraUi: t('hero.inspiraUi') }) }
  ]
})

// Accessibility preferences
const prefersReducedMotion = ref(false)

// Detect user preferences
onMounted(() => {
  if (typeof window !== 'undefined') {
    // Check for reduced motion preference
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches

    // Listen for changes
    mediaQuery.addEventListener('change', (e) => {
      prefersReducedMotion.value = e.matches
    })
  }

  // Add some entrance animations
  console.log('Warhammer Tavern v3 loaded with Inspira UI!')
})

// Tavern statistics
const tavernStats = ref([
  {
    id: 'reputation',
    key: 'tavernReputation',
    value: 87,
    icon: 'star'
  },
  {
    id: 'visitors',
    key: 'dailyVisitors',
    value: 156,
    icon: 'users'
  },
  {
    id: 'events',
    key: 'activeEvents',
    value: 12,
    icon: 'calendar'
  }
])

// Character data
const characters = ref([
  {
    id: 'marcus',
    name: 'Sir Marcus Brightblade',
    class: 'Empire Knight',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    icon: 'sword',
    description: 'A noble knight of the Empire, seeking glory and honor in service to Sigmar.',
    stats: {
      attack: 85,
      defense: 78
    }
  },
  {
    id: 'grimjaw',
    name: 'Grimjaw Ironbeard',
    class: 'Dwarf Slayer',
    faction: 'Dwarfs',
    factionColor: 'bg-faction-dwarfs-500',
    icon: 'hammer',
    description: 'A fierce dwarf warrior who has taken the Slayer Oath to redeem his honor.',
    stats: {
      attack: 92,
      defense: 65
    }
  },
  {
    id: 'elara',
    name: 'Elara Moonwhisper',
    class: 'High Elf Mage',
    faction: 'High Elves',
    factionColor: 'bg-faction-elves-500',
    icon: 'sparkles',
    description: 'An elegant elven sorceress mastering the winds of magic.',
    stats: {
      attack: 70,
      defense: 55
    }
  },
  {
    id: 'thorgrim',
    name: 'Thorgrim the Bold',
    class: 'Dwarf Ranger',
    faction: 'Dwarfs',
    factionColor: 'bg-faction-dwarfs-500',
    icon: 'bow',
    description: 'A seasoned ranger who knows every path through the mountains.',
    stats: {
      attack: 75,
      defense: 80
    }
  },
  {
    id: 'valdris',
    name: 'Valdris Shadowbane',
    class: 'Witch Hunter',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    icon: 'flame',
    description: 'A grim hunter of heretics and creatures of darkness.',
    stats: {
      attack: 88,
      defense: 70
    }
  },
  {
    id: 'lyralei',
    name: 'Lyralei Starweaver',
    class: 'Wood Elf Scout',
    faction: 'Wood Elves',
    factionColor: 'bg-faction-elves-500',
    icon: 'leaf',
    description: 'A swift scout from the forests of Athel Loren.',
    stats: {
      attack: 82,
      defense: 60
    }
  }
])

// Recent events
const recentEvents = ref([
  {
    id: 1,
    title: 'Merchant Caravan Arrives',
    description: 'A wealthy merchant caravan from Altdorf has arrived with exotic goods.',
    time: '2 hours ago',
    icon: 'truck'
  },
  {
    id: 2,
    title: 'Brawl in the Common Room',
    description: 'A heated argument between a dwarf and an elf escalated into a tavern brawl.',
    time: '4 hours ago',
    icon: 'swords'
  },
  {
    id: 3,
    title: 'Mysterious Stranger',
    description: 'A hooded figure entered the tavern asking about ancient artifacts.',
    time: '6 hours ago',
    icon: 'user-question'
  },
  {
    id: 4,
    title: 'Celebration Feast',
    description: 'The tavern hosted a celebration for a successful monster hunt.',
    time: '1 day ago',
    icon: 'party-popper'
  }
])

// Methods
const enterTavern = () => {
  navigateTo('/tavern')
}

const viewCharacters = () => {
  navigateTo('/characters')
}

const talkToCharacter = (character: any) => {
  navigateTo(`/conversations/${character.id}`)
}

const startAdventure = () => {
  navigateTo('/quests')
}

const learnMore = () => {
  navigateTo('/about')
}

// Additional lifecycle hooks can be added here if needed
</script>

<style scoped>
/* Component-specific styles with accessibility */
.character-gallery {
  perspective: 1000px;
}

.character-item {
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.character-item:hover:not(:focus) {
  transform: rotateY(5deg) rotateX(5deg);
}

.character-item:focus {
  outline: 2px solid var(--wh-focus-ring);
  outline-offset: 2px;
  transform: scale(1.02);
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .character-item {
    transition: none;
  }

  .character-item:hover:not(:focus) {
    transform: none;
  }

  .character-item:focus {
    transform: none;
  }
}

/* High contrast improvements */
@media (prefers-contrast: high) {
  .character-item {
    border: 2px solid currentColor;
  }
}

/* Responsive adjustments with accessibility */
@media (max-width: 768px) {
  .character-gallery {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .character-item {
    min-height: 120px;
  }
}

@media (max-width: 480px) {
  .character-gallery {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .character-item {
    min-height: 100px;
  }
}

/* Touch improvements */
@media (pointer: coarse) {
  .character-item {
    min-height: 120px;
    padding: 1rem;
  }
}

/* Print styles */
@media print {
  .character-gallery {
    display: block;
  }

  .character-item {
    break-inside: avoid;
    margin-bottom: 1rem;
    border: 1px solid #000;
    padding: 1rem;
  }
}
</style>