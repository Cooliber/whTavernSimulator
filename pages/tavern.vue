<template>
  <div class="tavern-page relative min-h-screen overflow-hidden">
    <!-- Advanced Weather System -->
    <WeatherSystem
      :weather="currentWeather.type"
      :intensity="currentWeather.intensity"
      :wind-speed="currentWeather.windSpeed"
      :temperature="currentWeather.temperature"
    />

    <!-- Dynamic Lighting System -->
    <DynamicLighting
      :time-of-day="timeOfDay"
      :fireplace-active="fireplaceActive"
      :candle-count="candleCount"
      :magic-light-intensity="magicLightIntensity"
      :ambient-brightness="ambientBrightness"
    />

    <!-- Audio Atmosphere -->
    <AudioAtmosphere
      ref="audioSystem"
      :auto-play="false"
      :default-volume="0.7"
      :show-controls-initially="false"
    />

    <!-- Interactive grid background -->
    <InteractiveGridPattern
      :grid-size="60"
      grid-color="#ffd700"
      :stroke-width="1"
      :proximity-radius="80"
      proximity-color="#ffd700"
      class="absolute inset-0 opacity-20"
    />

    <!-- Meteors for atmosphere -->
    <Meteors :meteor-count="4" :meteor-speed="0.6" />
    
    <!-- Main tavern content -->
    <div class="relative z-10 space-y-12 p-8">
      <!-- Tavern header -->
      <section class="text-center space-y-6">
        <Spotlight 
          spotlight-color="rgba(255, 69, 0, 0.4)"
          :spotlight-size="400"
          class="inline-block"
        >
          <div class="space-y-4">
            <SparklesText 
              text="The Golden Griffin Tavern"
              class="text-6xl md:text-8xl font-medieval text-foreground"
              :sparkles-count="25"
            />
            <Text3D 
              text="Where Legends Gather"
              class="text-2xl md:text-3xl font-fantasy text-primary"
              :depth="4"
            />
          </div>
        </Spotlight>
        
        <!-- Enhanced Tavern atmosphere controls -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          <RippleButton
            class="faction-empire px-4 py-3 font-medieval"
            ripple-color="rgb(255, 215, 0)"
            @click="toggleFireplace"
          >
            <Icon name="flame" class="w-5 h-5 mr-2" />
            {{ fireplaceActive ? 'Dim Fireplace' : 'Light Fireplace' }}
          </RippleButton>

          <ShimmerButton
            class="bg-secondary text-secondary-foreground px-4 py-3 font-medieval"
            shimmer-color="rgba(139, 69, 19, 0.5)"
            @click="toggleMusic"
          >
            <Icon name="music" class="w-5 h-5 mr-2" />
            {{ musicPlaying ? 'Stop Music' : 'Play Music' }}
          </ShimmerButton>

          <RippleButton
            class="bg-blue-600 text-white px-4 py-3 font-medieval"
            ripple-color="rgba(37, 99, 235, 0.6)"
            @click="changeWeather"
          >
            <Icon :name="currentWeather.icon" class="w-5 h-5 mr-2" />
            {{ currentWeather.name }}
          </RippleButton>

          <RainbowButton
            :colors="['#f59e0b', '#eab308', '#facc15']"
            class="px-4 py-3 font-medieval"
            @click="changeTimeOfDay"
          >
            <Icon :name="timeOfDayIcon" class="w-5 h-5 mr-2" />
            {{ timeOfDay }}
          </RainbowButton>
        </div>

        <!-- Advanced Atmosphere Panel -->
        <BorderBeam
          class="atmosphere-panel bg-card/60 backdrop-blur-md rounded-xl p-6 max-w-6xl mx-auto"
          :border-width="2"
          color-from="#8b4513"
          color-to="#a0522d"
        >
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Weather Controls -->
            <div class="space-y-4">
              <h3 class="text-lg font-medieval text-foreground">Weather Control</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Intensity</span>
                  <span class="text-sm text-foreground">{{ Math.round(currentWeather.intensity * 100) }}%</span>
                </div>
                <input
                  v-model="currentWeather.intensity"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  class="atmosphere-slider w-full"
                  @input="updateWeatherIntensity"
                />

                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Wind Speed</span>
                  <span class="text-sm text-foreground">{{ Math.round(currentWeather.windSpeed * 100) }}%</span>
                </div>
                <input
                  v-model="currentWeather.windSpeed"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  class="atmosphere-slider w-full"
                  @input="updateWeatherWind"
                />
              </div>
            </div>

            <!-- Lighting Controls -->
            <div class="space-y-4">
              <h3 class="text-lg font-medieval text-foreground">Lighting Control</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Candles</span>
                  <span class="text-sm text-foreground">{{ candleCount }}</span>
                </div>
                <input
                  v-model="candleCount"
                  type="range"
                  min="0"
                  max="12"
                  step="1"
                  class="atmosphere-slider w-full"
                />

                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Magic Light</span>
                  <span class="text-sm text-foreground">{{ Math.round(magicLightIntensity * 100) }}%</span>
                </div>
                <input
                  v-model="magicLightIntensity"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  class="atmosphere-slider w-full"
                />
              </div>
            </div>

            <!-- Reputation System -->
            <div class="space-y-4">
              <h3 class="text-lg font-medieval text-foreground">Tavern Reputation</h3>
              <div class="space-y-3">
                <div class="reputation-meter">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm text-muted-foreground">Overall Rating</span>
                    <div class="flex items-center space-x-1">
                      <Icon
                        v-for="i in 5"
                        :key="i"
                        name="star"
                        class="w-4 h-4"
                        :class="i <= tavernReputation.rating ? 'text-yellow-400' : 'text-muted'"
                      />
                    </div>
                  </div>
                  <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      class="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 transition-all duration-1000"
                      :style="{ width: (tavernReputation.score / 100 * 100) + '%' }"
                    />
                  </div>
                  <p class="text-xs text-muted-foreground mt-1">{{ tavernReputation.score }}/100 points</p>
                </div>

                <div class="reputation-factors space-y-2">
                  <div
                    v-for="factor in tavernReputation.factors"
                    :key="factor.name"
                    class="flex items-center justify-between text-sm"
                  >
                    <span class="text-muted-foreground">{{ factor.name }}</span>
                    <span class="text-foreground">{{ factor.value }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </BorderBeam>
      </section>

      <!-- Tavern layout grid -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main hall area -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Active characters in tavern -->
          <BorderBeam 
            class="tavern-section bg-card/50 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#ffd700"
            color-to="#b8860b"
          >
            <div class="space-y-6">
              <div class="flex items-center justify-between">
                <HyperText 
                  text="Tavern Patrons"
                  class="text-2xl font-medieval text-foreground"
                  :animation-duration="1500"
                />
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full bg-green-400 animate-pulse" />
                  <span class="text-sm text-muted-foreground">{{ activePatrons.length }} Active</span>
                </div>
              </div>
              
              <!-- Character cards in tavern -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="patron in activePatrons" 
                  :key="patron.id"
                  class="patron-card"
                >
                  <Lens 
                    :lens-size="120"
                    :magnification="1.3"
                  >
                    <Card3D 
                      class="patron-card-inner bg-gradient-to-br from-amber-900/80 to-amber-800/80 backdrop-blur-sm p-4 rounded-lg border border-amber-700/30"
                      :rotation-intensity="10"
                    >
                      <div class="flex items-center space-x-4">
                        <!-- Character avatar -->
                        <div class="relative">
                          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-amber-700 to-amber-800 flex items-center justify-center">
                            <Icon :name="patron.icon" class="w-6 h-6 text-primary" />
                          </div>
                          <!-- Activity indicator -->
                          <div class="absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-background flex items-center justify-center"
                               :class="patron.activity.color">
                            <div class="w-2 h-2 rounded-full bg-current animate-pulse" />
                          </div>
                        </div>
                        
                        <!-- Character info -->
                        <div class="flex-1 min-w-0">
                          <h3 class="font-medieval text-sm text-foreground truncate">{{ patron.name }}</h3>
                          <p class="text-xs text-muted-foreground">{{ patron.location }}</p>
                          <p class="text-xs text-primary">{{ patron.activity.text }}</p>
                        </div>
                        
                        <!-- Interaction button -->
                        <RippleButton 
                          class="w-8 h-8 rounded-full bg-primary/20 hover:bg-primary/30 flex items-center justify-center"
                          ripple-color="rgba(255, 215, 0, 0.5)"
                          @click="interactWithPatron(patron)"
                        >
                          <Icon name="message-circle" class="w-4 h-4 text-primary" />
                        </RippleButton>
                      </div>
                    </Card3D>
                    
                    <!-- Lens magnified content -->
                    <template #magnified>
                      <div class="patron-details bg-black/90 text-white p-3 rounded-lg">
                        <h4 class="font-medieval text-sm mb-1">{{ patron.name }}</h4>
                        <p class="text-xs mb-2">{{ patron.title }}</p>
                        <div class="space-y-1 text-xs">
                          <p><strong>Mood:</strong> {{ patron.mood }}</p>
                          <p><strong>Drink:</strong> {{ patron.currentDrink }}</p>
                          <p><strong>Topic:</strong> {{ patron.conversationTopic }}</p>
                        </div>
                      </div>
                    </template>
                  </Lens>
                </div>
              </div>
            </div>
          </BorderBeam>
          
          <!-- Tavern events feed -->
          <BorderBeam 
            class="tavern-section bg-card/50 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#ff4500"
            color-to="#ffd700"
          >
            <div class="space-y-4">
              <HyperText 
                text="Live Tavern Events"
                class="text-xl font-medieval text-foreground"
                :animation-duration="1200"
              />
              
              <!-- Events timeline -->
              <div class="space-y-3 max-h-64 overflow-y-auto">
                <div 
                  v-for="event in recentEvents" 
                  :key="event.id"
                  class="event-item flex items-start space-x-3 p-3 rounded-lg bg-background/30 hover:bg-background/50 transition-colors"
                >
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center flex-shrink-0">
                    <Icon :name="event.icon" class="w-4 h-4 text-primary" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm text-foreground">{{ event.description }}</p>
                    <p class="text-xs text-muted-foreground">{{ event.timeAgo }}</p>
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
        
        <!-- Sidebar with tavern info -->
        <div class="space-y-8">
          <!-- Tavern stats -->
          <BorderBeam 
            class="tavern-stats bg-card/50 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#32cd32"
            color-to="#228b22"
          >
            <div class="space-y-6">
              <HyperText 
                text="Tavern Status"
                class="text-xl font-medieval text-foreground"
                :animation-duration="1000"
              />
              
              <!-- Stats grid -->
              <div class="space-y-4">
                <div 
                  v-for="stat in tavernStats" 
                  :key="stat.id"
                  class="stat-item"
                >
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <Icon :name="stat.icon" class="w-4 h-4 text-primary" />
                      <span class="text-sm font-medieval text-foreground">{{ stat.label }}</span>
                    </div>
                    <NumberTicker 
                      :value="stat.value"
                      class="text-lg font-bold text-primary"
                    />
                  </div>
                  
                  <!-- Progress bar -->
                  <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-gradient-to-r from-primary to-primary/60 transition-all duration-1000"
                      :style="{ width: (stat.value / stat.max * 100) + '%' }"
                    />
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
          
          <!-- Weather and atmosphere -->
          <BorderBeam 
            class="atmosphere-panel bg-card/50 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#4b0082"
            color-to="#9400d3"
          >
            <div class="space-y-4">
              <HyperText 
                text="Atmosphere"
                class="text-xl font-medieval text-foreground"
                :animation-duration="1000"
              />
              
              <!-- Weather info -->
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Weather</span>
                  <div class="flex items-center space-x-2">
                    <Icon :name="currentWeather.icon" class="w-4 h-4 text-primary" />
                    <span class="text-sm text-foreground">{{ currentWeather.condition }}</span>
                  </div>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Temperature</span>
                  <span class="text-sm text-foreground">{{ currentWeather.temperature }}</span>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Ambiance</span>
                  <div class="flex items-center space-x-1">
                    <div 
                      v-for="i in 5" 
                      :key="i"
                      class="w-2 h-2 rounded-full"
                      :class="i <= ambianceLevel ? 'bg-primary' : 'bg-muted'"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Fireplace status -->
              <div 
                class="fireplace-status p-3 rounded-lg transition-all duration-500"
                :class="fireplaceActive ? 'bg-orange-500/20 border border-orange-500/30' : 'bg-muted/20'"
              >
                <div class="flex items-center space-x-3">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center transition-all duration-500"
                    :class="fireplaceActive ? 'bg-orange-500/30 fire-glow' : 'bg-muted/30'"
                  >
                    <Icon name="flame" class="w-4 h-4" :class="fireplaceActive ? 'text-orange-300' : 'text-muted-foreground'" />
                  </div>
                  <div>
                    <p class="text-sm font-medieval" :class="fireplaceActive ? 'text-orange-200' : 'text-muted-foreground'">
                      Fireplace
                    </p>
                    <p class="text-xs" :class="fireplaceActive ? 'text-orange-300' : 'text-muted-foreground'">
                      {{ fireplaceActive ? 'Crackling warmly' : 'Cold and dark' }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
          
          <!-- Quick actions -->
          <BorderBeam 
            class="quick-actions bg-card/50 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#ffd700"
            color-to="#ff4500"
          >
            <div class="space-y-4">
              <HyperText 
                text="Quick Actions"
                class="text-xl font-medieval text-foreground"
                :animation-duration="1000"
              />
              
              <div class="space-y-3">
                <RippleButton 
                  class="w-full faction-empire font-medieval"
                  ripple-color="rgb(255, 215, 0)"
                  @click="orderDrink"
                >
                  <Icon name="cup" class="w-4 h-4 mr-2" />
                  Order a Drink
                </RippleButton>
                
                <ShimmerButton 
                  class="w-full bg-secondary text-secondary-foreground font-medieval"
                  shimmer-color="rgba(139, 69, 19, 0.5)"
                  @click="callBard"
                >
                  <Icon name="music" class="w-4 h-4 mr-2" />
                  Call the Bard
                </ShimmerButton>
                
                <RainbowButton 
                  :colors="['#228b22', '#32cd32', '#90ee90']"
                  class="w-full font-medieval"
                  @click="startQuest"
                >
                  <Icon name="scroll" class="w-4 h-4 mr-2" />
                  Start New Quest
                </RainbowButton>
              </div>
            </div>
          </BorderBeam>
        </div>
      </section>
    </div>
    
    <!-- Floating particles when fireplace is active -->
    <div v-if="fireplaceActive" class="fixed inset-0 pointer-events-none z-5">
      <ParticlesBg 
        :particle-count="20"
        particle-color="#ff4500"
        :particle-size="1"
        :animation-speed="0.3"
        class="opacity-60"
      />
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'The Golden Griffin Tavern - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Experience the immersive atmosphere of The Golden Griffin Tavern with AI-powered NPCs and dynamic events.' }
  ]
})

// Reactive state
const fireplaceActive = ref(true)
const musicPlaying = ref(false)
const ambianceLevel = ref(4)

// Enhanced atmosphere state
const timeOfDay = ref('evening')
const candleCount = ref(6)
const magicLightIntensity = ref(0.5)
const ambientBrightness = ref(0.7)

// Audio system reference
const audioSystem = ref(null)

// Weather system
const currentWeather = ref({
  type: 'clear',
  name: 'Clear Night',
  icon: 'moon',
  intensity: 0.3,
  windSpeed: 0.2,
  temperature: 15
})

const weatherTypes = [
  { type: 'clear', name: 'Clear Night', icon: 'moon' },
  { type: 'rain', name: 'Rainy', icon: 'cloud-rain' },
  { type: 'storm', name: 'Storm', icon: 'zap' },
  { type: 'snow', name: 'Snowy', icon: 'snowflake' },
  { type: 'fog', name: 'Foggy', icon: 'cloud' }
]

const timeOfDayOptions = ['dawn', 'morning', 'noon', 'afternoon', 'dusk', 'evening', 'night', 'midnight']

// Tavern reputation system
const tavernReputation = ref({
  score: 87,
  rating: 4,
  factors: [
    { name: 'Cleanliness', value: 92 },
    { name: 'Service', value: 88 },
    { name: 'Atmosphere', value: 95 },
    { name: 'Food Quality', value: 85 },
    { name: 'Safety', value: 90 }
  ]
})

// Computed properties
const timeOfDayIcon = computed(() => {
  const icons = {
    dawn: 'sunrise',
    morning: 'sun',
    noon: 'sun',
    afternoon: 'sun',
    dusk: 'sunset',
    evening: 'moon',
    night: 'moon',
    midnight: 'moon'
  }
  return icons[timeOfDay.value] || 'moon'
})

// Active patrons in the tavern
const activePatrons = ref([
  {
    id: 'marcus',
    name: 'Sir Marcus',
    title: 'Empire Knight',
    icon: 'sword',
    location: 'Main Hall',
    mood: 'Confident',
    currentDrink: 'Ale',
    conversationTopic: 'Recent battles',
    activity: {
      text: 'Telling war stories',
      color: 'bg-blue-500'
    }
  },
  {
    id: 'grimjaw',
    name: 'Grimjaw',
    title: 'Dwarf Slayer',
    icon: 'hammer',
    location: 'Bar Counter',
    mood: 'Brooding',
    currentDrink: 'Strong Ale',
    conversationTopic: 'Honor and death',
    activity: {
      text: 'Drinking heavily',
      color: 'bg-red-500'
    }
  },
  {
    id: 'elara',
    name: 'Elara',
    title: 'High Elf Mage',
    icon: 'sparkles',
    location: 'Quiet Corner',
    mood: 'Contemplative',
    currentDrink: 'Elven Wine',
    conversationTopic: 'Ancient magic',
    activity: {
      text: 'Reading scrolls',
      color: 'bg-purple-500'
    }
  },
  {
    id: 'thorgrim',
    name: 'Thorgrim',
    title: 'Dwarf Ranger',
    icon: 'bow',
    location: 'Window Seat',
    mood: 'Alert',
    currentDrink: 'Mead',
    conversationTopic: 'Mountain paths',
    activity: {
      text: 'Watching the storm',
      color: 'bg-green-500'
    }
  },
  {
    id: 'valdris',
    name: 'Valdris',
    title: 'Witch Hunter',
    icon: 'flame',
    location: 'Dark Corner',
    mood: 'Vigilant',
    currentDrink: 'Black Coffee',
    conversationTopic: 'Heretic hunting',
    activity: {
      text: 'Observing patrons',
      color: 'bg-yellow-500'
    }
  },
  {
    id: 'stranger',
    name: 'Hooded Stranger',
    title: 'Unknown',
    icon: 'user-question',
    location: 'Back Booth',
    mood: 'Mysterious',
    currentDrink: 'Unknown',
    conversationTopic: 'Secrets',
    activity: {
      text: 'Sitting silently',
      color: 'bg-gray-500'
    }
  }
])

// Tavern statistics
const tavernStats = ref([
  {
    id: 'reputation',
    label: 'Reputation',
    value: 87,
    max: 100,
    icon: 'star'
  },
  {
    id: 'warmth',
    label: 'Warmth',
    value: fireplaceActive.value ? 85 : 45,
    max: 100,
    icon: 'flame'
  },
  {
    id: 'noise',
    label: 'Noise Level',
    value: 65,
    max: 100,
    icon: 'volume-2'
  },
  {
    id: 'safety',
    label: 'Safety',
    value: 92,
    max: 100,
    icon: 'shield'
  },
  {
    id: 'supplies',
    label: 'Supplies',
    value: 78,
    max: 100,
    icon: 'package'
  }
])

// Recent events in the tavern
const recentEvents = ref([
  {
    id: 1,
    description: 'A merchant caravan arrived seeking shelter from the storm',
    timeAgo: '5 minutes ago',
    icon: 'truck'
  },
  {
    id: 2,
    description: 'Grimjaw challenged a patron to an arm wrestling match',
    timeAgo: '12 minutes ago',
    icon: 'zap'
  },
  {
    id: 3,
    description: 'Elara cast a warming spell near the fireplace',
    timeAgo: '18 minutes ago',
    icon: 'sparkles'
  },
  {
    id: 4,
    description: 'A bard finished playing a haunting melody',
    timeAgo: '25 minutes ago',
    icon: 'music'
  },
  {
    id: 5,
    description: 'The tavern keeper served fresh bread and stew',
    timeAgo: '32 minutes ago',
    icon: 'utensils'
  },
  {
    id: 6,
    description: 'Lightning illuminated the tavern windows',
    timeAgo: '38 minutes ago',
    icon: 'zap'
  }
])

// Methods
const toggleFireplace = () => {
  fireplaceActive.value = !fireplaceActive.value
  
  // Update warmth stat
  const warmthStat = tavernStats.value.find(s => s.id === 'warmth')
  if (warmthStat) {
    warmthStat.value = fireplaceActive.value ? 85 : 45
  }
  
  // Add event
  addEvent({
    description: fireplaceActive.value 
      ? 'The fireplace was lit, warming the tavern' 
      : 'The fireplace was extinguished',
    icon: 'flame'
  })
}

const toggleMusic = () => {
  musicPlaying.value = !musicPlaying.value

  // Control audio system
  if (audioSystem.value) {
    audioSystem.value.toggleMusic()
  }

  // Update noise level
  const noiseStat = tavernStats.value.find(s => s.id === 'noise')
  if (noiseStat) {
    noiseStat.value = musicPlaying.value ? 75 : 65
  }

  // Add event
  addEvent({
    description: musicPlaying.value
      ? 'A bard began playing cheerful music'
      : 'The music stopped, leaving only conversation',
    icon: 'music'
  })
}

const changeWeather = () => {
  const currentIndex = weatherTypes.findIndex(w => w.type === currentWeather.value.type)
  const nextIndex = (currentIndex + 1) % weatherTypes.length
  const newWeather = weatherTypes[nextIndex]

  currentWeather.value = {
    ...currentWeather.value,
    type: newWeather.type,
    name: newWeather.name,
    icon: newWeather.icon
  }

  // Update audio ambients based on weather
  if (audioSystem.value) {
    audioSystem.value.setWeatherAmbient(newWeather.type)
  }

  // Add event
  addEvent({
    description: `The weather changed to ${newWeather.name.toLowerCase()}`,
    icon: newWeather.icon
  })

  // Update reputation based on weather management
  updateReputationFactor('Atmosphere', 2)
}

const changeTimeOfDay = () => {
  const currentIndex = timeOfDayOptions.indexOf(timeOfDay.value)
  const nextIndex = (currentIndex + 1) % timeOfDayOptions.length
  timeOfDay.value = timeOfDayOptions[nextIndex]

  // Update audio based on time
  if (audioSystem.value) {
    audioSystem.value.setTimeOfDayMusic(timeOfDay.value)
  }

  // Add event
  addEvent({
    description: `Time of day changed to ${timeOfDay.value}`,
    icon: timeOfDayIcon.value
  })

  // Update ambient brightness based on time
  const timeConfig = {
    dawn: 0.4, morning: 0.7, noon: 1.0, afternoon: 0.8,
    dusk: 0.5, evening: 0.6, night: 0.3, midnight: 0.2
  }
  ambientBrightness.value = timeConfig[timeOfDay.value] || 0.6
}

const updateWeatherIntensity = () => {
  // Weather intensity affects reputation
  if (currentWeather.value.intensity > 0.8) {
    updateReputationFactor('Atmosphere', -1)
  } else if (currentWeather.value.intensity < 0.3) {
    updateReputationFactor('Atmosphere', 1)
  }
}

const updateWeatherWind = () => {
  // Wind affects comfort
  if (currentWeather.value.windSpeed > 0.7) {
    updateReputationFactor('Atmosphere', -1)
  }
}

const updateReputationFactor = (factorName: string, change: number) => {
  const factor = tavernReputation.value.factors.find(f => f.name === factorName)
  if (factor) {
    factor.value = Math.max(0, Math.min(100, factor.value + change))

    // Recalculate overall score
    const average = tavernReputation.value.factors.reduce((sum, f) => sum + f.value, 0) / tavernReputation.value.factors.length
    tavernReputation.value.score = Math.round(average)
    tavernReputation.value.rating = Math.ceil(average / 20)
  }
}

const interactWithPatron = (patron: any) => {
  // Navigate to conversation with this patron
  navigateTo(`/conversations/${patron.id}`)
}

const orderDrink = () => {
  addEvent({
    description: 'You ordered a drink from the tavern keeper',
    icon: 'cup'
  })
}

const callBard = () => {
  if (!musicPlaying.value) {
    toggleMusic()
  }
  addEvent({
    description: 'You called for the bard to play a song',
    icon: 'music'
  })
}

const startQuest = () => {
  navigateTo('/quests')
}

const addEvent = (event: { description: string; icon: string }) => {
  const newEvent = {
    id: Date.now(),
    description: event.description,
    timeAgo: 'Just now',
    icon: event.icon
  }
  
  recentEvents.value.unshift(newEvent)
  
  // Keep only last 10 events
  if (recentEvents.value.length > 10) {
    recentEvents.value = recentEvents.value.slice(0, 10)
  }
}

// Simulate dynamic events
const simulateEvents = () => {
  const eventTemplates = [
    { description: 'A patron ordered another round of drinks', icon: 'cup' },
    { description: 'Someone threw another log on the fire', icon: 'flame' },
    { description: 'A group of travelers entered the tavern', icon: 'users' },
    { description: 'The wind howled outside the windows', icon: 'wind' },
    { description: 'A patron shared news from distant lands', icon: 'map' },
    { description: 'The tavern cat jumped onto a table', icon: 'cat' },
    { description: 'Someone started a friendly dice game', icon: 'dice' }
  ]
  
  setInterval(() => {
    if (Math.random() < 0.3) { // 30% chance every interval
      const template = eventTemplates[Math.floor(Math.random() * eventTemplates.length)]
      addEvent(template)
    }
  }, 30000) // Every 30 seconds
}

// Update time stamps
const updateTimeStamps = () => {
  recentEvents.value.forEach(event => {
    if (event.timeAgo === 'Just now') {
      event.timeAgo = '1 minute ago'
    } else if (event.timeAgo.includes('minute')) {
      const minutes = parseInt(event.timeAgo) + 1
      event.timeAgo = `${minutes} minutes ago`
    }
  })
}

// Lifecycle
onMounted(() => {
  console.log('Golden Griffin Tavern loaded with', activePatrons.value.length, 'patrons')
  
  // Start event simulation
  simulateEvents()
  
  // Update timestamps every minute
  setInterval(updateTimeStamps, 60000)
  
  // Simulate patron activity changes
  setInterval(() => {
    activePatrons.value.forEach(patron => {
      if (Math.random() < 0.2) { // 20% chance to change activity
        const activities = [
          { text: 'Drinking quietly', color: 'bg-blue-500' },
          { text: 'Talking with others', color: 'bg-green-500' },
          { text: 'Looking around', color: 'bg-yellow-500' },
          { text: 'Reading something', color: 'bg-purple-500' },
          { text: 'Eating food', color: 'bg-orange-500' }
        ]
        patron.activity = activities[Math.floor(Math.random() * activities.length)]
      }
    })
  }, 45000) // Every 45 seconds
})
</script>

<style scoped>
/* Tavern-specific animations */
.tavern-page {
  background-attachment: fixed;
}

.patron-card {
  animation: patron-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.patron-card-inner {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.patron-card-inner:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 
    0 10px 25px -5px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 215, 0, 0.2);
}

.event-item {
  animation: event-slide-in 0.4s ease-out forwards;
}

.stat-item {
  animation: stat-fade-in 0.6s ease-out forwards;
}

.fireplace-status {
  animation: fireplace-glow 2s ease-in-out infinite alternate;
}

/* Custom animations */
@keyframes patron-entrance {
  0% {
    opacity: 0;
    transform: translateX(-20px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes event-slide-in {
  0% {
    opacity: 0;
    transform: translateX(-10px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes stat-fade-in {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fireplace-glow {
  0% {
    box-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.5);
  }
}

/* Responsive design */
@media (max-width: 1024px) {
  .tavern-page {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .patron-card {
    animation-delay: 0s;
  }
}

/* Atmosphere controls styling */
.atmosphere-slider {
  appearance: none;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(to right, #ffd700 0%, #ffd700 var(--value, 0%), #374151 var(--value, 0%), #374151 100%);
  outline: none;
  transition: all 0.2s ease;
}

.atmosphere-slider::-webkit-slider-thumb {
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #b8860b;
  transition: all 0.2s ease;
}

.atmosphere-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
}

.atmosphere-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #b8860b;
  transition: all 0.2s ease;
}

.reputation-meter {
  animation: reputation-update 0.6s ease-out;
}

.reputation-factors {
  animation: factors-slide-in 0.8s ease-out;
}

@keyframes reputation-update {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes factors-slide-in {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.atmosphere-panel {
  animation: panel-expand 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes panel-expand {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Performance optimizations */
.patron-card-inner,
.event-item,
.stat-item,
.atmosphere-slider,
.reputation-meter {
  will-change: transform;
}
</style>