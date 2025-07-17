<template>
  <div class="smart-atmosphere-control wh-card wh-card-parchment p-6 space-y-6">
    <!-- Atmosphere Presets -->
    <div class="atmosphere-presets-section">
      <h3 class="wh-title text-xl text-wh-dark-grey mb-4">Atmosphere Presets</h3>
      <div class="presets-grid grid grid-cols-2 md:grid-cols-4 gap-3">
        <div 
          v-for="preset in atmospherePresets" 
          :key="preset.id"
          class="preset-card wh-ornate-border p-3 text-center cursor-pointer transition-all duration-300"
          :class="{ 'bg-wh-empire-gold text-wh-dark-grey': currentPreset === preset.id }"
          @click="applyPreset(preset)"
        >
          <div class="preset-icon w-12 h-12 mx-auto mb-2 rounded-full flex items-center justify-center"
               :style="{ backgroundColor: preset.color + '20', color: preset.color }">
            <Icon :name="preset.icon" class="w-6 h-6" />
          </div>
          <h4 class="font-medieval text-sm">{{ preset.name }}</h4>
          <p class="text-xs text-wh-muted mt-1">{{ preset.description }}</p>
        </div>
      </div>
    </div>

    <!-- Real-time Atmosphere Controls -->
    <div class="atmosphere-controls-section">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey mb-4">Live Controls</h4>
      
      <!-- Lighting Controls -->
      <div class="control-group mb-6">
        <h5 class="font-medieval text-md text-wh-dark-grey mb-3">Lighting & Ambiance</h5>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Overall Brightness</label>
            <div class="flex items-center space-x-3">
              <Icon name="sun" class="w-4 h-4 text-wh-empire-gold" />
              <input 
                v-model="atmosphereSettings.brightness" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateAtmosphere"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.brightness }}%</span>
            </div>
          </div>
          
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Warmth</label>
            <div class="flex items-center space-x-3">
              <Icon name="flame" class="w-4 h-4 text-wh-chaos-red" />
              <input 
                v-model="atmosphereSettings.warmth" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateAtmosphere"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.warmth }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Weather & Environment -->
      <div class="control-group mb-6">
        <h5 class="font-medieval text-md text-wh-dark-grey mb-3">Weather & Environment</h5>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Rain Intensity</label>
            <div class="flex items-center space-x-3">
              <Icon name="cloud-rain" class="w-4 h-4 text-wh-blue" />
              <input 
                v-model="atmosphereSettings.rain" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateWeather"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.rain }}%</span>
            </div>
          </div>
          
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Wind Strength</label>
            <div class="flex items-center space-x-3">
              <Icon name="wind" class="w-4 h-4 text-wh-grey" />
              <input 
                v-model="atmosphereSettings.wind" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateWeather"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.wind }}%</span>
            </div>
          </div>
          
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Fog Density</label>
            <div class="flex items-center space-x-3">
              <Icon name="cloud" class="w-4 h-4 text-wh-muted" />
              <input 
                v-model="atmosphereSettings.fog" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateWeather"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.fog }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Audio & Sound -->
      <div class="control-group mb-6">
        <h5 class="font-medieval text-md text-wh-dark-grey mb-3">Audio Atmosphere</h5>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Crowd Noise</label>
            <div class="flex items-center space-x-3">
              <Icon name="users" class="w-4 h-4 text-wh-empire-gold" />
              <input 
                v-model="atmosphereSettings.crowdNoise" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateAudio"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.crowdNoise }}%</span>
            </div>
          </div>
          
          <div class="control-item">
            <label class="block text-sm text-wh-dark-grey mb-2">Ambient Music</label>
            <div class="flex items-center space-x-3">
              <Icon name="music" class="w-4 h-4 text-wh-empire-gold" />
              <input 
                v-model="atmosphereSettings.music" 
                type="range" 
                min="0" 
                max="100" 
                class="wh-slider flex-1"
                @input="updateAudio"
              />
              <span class="text-sm text-wh-empire-gold w-12">{{ atmosphereSettings.music }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Action Buttons -->
    <div class="quick-actions-section">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey mb-3">Quick Actions</h4>
      <div class="actions-grid grid grid-cols-2 md:grid-cols-4 gap-3">
        <RippleButton 
          class="bg-wh-chaos-red text-white p-3 text-center"
          @click="triggerDramaticMoment"
        >
          <Icon name="zap" class="w-5 h-5 mx-auto mb-1" />
          <span class="text-xs">Dramatic Moment</span>
        </RippleButton>
        
        <ShimmerButton 
          class="bg-wh-empire-gold text-wh-dark-grey p-3 text-center"
          @click="createTension"
        >
          <Icon name="eye" class="w-5 h-5 mx-auto mb-1" />
          <span class="text-xs">Build Tension</span>
        </ShimmerButton>
        
        <RippleButton 
          class="bg-wh-green text-white p-3 text-center"
          @click="restorePeace"
        >
          <Icon name="heart" class="w-5 h-5 mx-auto mb-1" />
          <span class="text-xs">Restore Peace</span>
        </RippleButton>
        
        <ShimmerButton 
          class="bg-wh-purple text-white p-3 text-center"
          @click="addMystery"
        >
          <Icon name="question" class="w-5 h-5 mx-auto mb-1" />
          <span class="text-xs">Add Mystery</span>
        </ShimmerButton>
      </div>
    </div>

    <!-- Atmosphere Timeline -->
    <div class="atmosphere-timeline-section">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey mb-3">Atmosphere Timeline</h4>
      <div class="timeline-container bg-wh-parchment-light p-4 rounded-lg">
        <div class="timeline-track relative h-8 bg-wh-muted rounded-full overflow-hidden">
          <div 
            v-for="(segment, index) in atmosphereTimeline" 
            :key="index"
            class="timeline-segment absolute top-0 h-full transition-all duration-500"
            :style="{ 
              left: segment.start + '%', 
              width: (segment.end - segment.start) + '%',
              backgroundColor: segment.color 
            }"
          >
            <Tooltip :content="segment.name" />
          </div>
          <div 
            class="timeline-cursor absolute top-0 w-1 h-full bg-wh-chaos-red"
            :style="{ left: currentTimePosition + '%' }"
          />
        </div>
        <div class="timeline-controls flex items-center justify-between mt-3">
          <button 
            class="text-sm text-wh-empire-gold hover:text-wh-empire-gold-dark"
            @click="saveCurrentAtmosphere"
          >
            Save Current State
          </button>
          <div class="flex items-center space-x-2">
            <button 
              class="text-sm text-wh-empire-gold hover:text-wh-empire-gold-dark"
              @click="playAtmosphereSequence"
            >
              <Icon name="play" class="w-4 h-4" />
            </button>
            <button 
              class="text-sm text-wh-empire-gold hover:text-wh-empire-gold-dark"
              @click="pauseAtmosphereSequence"
            >
              <Icon name="pause" class="w-4 h-4" />
            </button>
            <button 
              class="text-sm text-wh-empire-gold hover:text-wh-empire-gold-dark"
              @click="resetAtmosphere"
            >
              <Icon name="refresh" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface AtmospherePreset {
  id: string
  name: string
  description: string
  icon: string
  color: string
  settings: AtmosphereSettings
}

interface AtmosphereSettings {
  brightness: number
  warmth: number
  rain: number
  wind: number
  fog: number
  crowdNoise: number
  music: number
}

interface TimelineSegment {
  start: number
  end: number
  name: string
  color: string
}

// Reactive data
const currentPreset = ref<string>('')
const currentTimePosition = ref(25)

const atmosphereSettings = ref<AtmosphereSettings>({
  brightness: 70,
  warmth: 60,
  rain: 0,
  wind: 20,
  fog: 10,
  crowdNoise: 50,
  music: 40
})

const atmospherePresets = ref<AtmospherePreset[]>([
  {
    id: 'cozy',
    name: 'Cozy Evening',
    description: 'Warm, inviting atmosphere',
    icon: 'home',
    color: '#D4AF37',
    settings: { brightness: 60, warmth: 80, rain: 0, wind: 10, fog: 5, crowdNoise: 40, music: 60 }
  },
  {
    id: 'stormy',
    name: 'Stormy Night',
    description: 'Dark and dramatic',
    icon: 'cloud-lightning',
    color: '#4A5568',
    settings: { brightness: 30, warmth: 40, rain: 80, wind: 70, fog: 30, crowdNoise: 30, music: 20 }
  },
  {
    id: 'festive',
    name: 'Festival',
    description: 'Bright and celebratory',
    icon: 'calendar',
    color: '#E53E3E',
    settings: { brightness: 90, warmth: 70, rain: 0, wind: 5, fog: 0, crowdNoise: 80, music: 90 }
  },
  {
    id: 'mysterious',
    name: 'Mysterious',
    description: 'Foggy and enigmatic',
    icon: 'eye',
    color: '#805AD5',
    settings: { brightness: 40, warmth: 30, rain: 20, wind: 30, fog: 70, crowdNoise: 20, music: 30 }
  },
  {
    id: 'tense',
    name: 'Tense Moment',
    description: 'High tension atmosphere',
    icon: 'zap',
    color: '#E53E3E',
    settings: { brightness: 50, warmth: 20, rain: 10, wind: 40, fog: 20, crowdNoise: 10, music: 10 }
  },
  {
    id: 'peaceful',
    name: 'Peaceful',
    description: 'Calm and serene',
    icon: 'heart',
    color: '#38A169',
    settings: { brightness: 80, warmth: 60, rain: 0, wind: 5, fog: 0, crowdNoise: 20, music: 70 }
  },
  {
    id: 'combat',
    name: 'Combat Ready',
    description: 'High energy, focused',
    icon: 'sword',
    color: '#E53E3E',
    settings: { brightness: 70, warmth: 50, rain: 0, wind: 20, fog: 0, crowdNoise: 60, music: 30 }
  },
  {
    id: 'magical',
    name: 'Magical',
    description: 'Mystical and otherworldly',
    icon: 'sparkles',
    color: '#805AD5',
    settings: { brightness: 60, warmth: 40, rain: 0, wind: 15, fog: 40, crowdNoise: 30, music: 80 }
  }
])

const atmosphereTimeline = ref<TimelineSegment[]>([
  { start: 0, end: 20, name: 'Peaceful Start', color: '#38A169' },
  { start: 20, end: 40, name: 'Building Tension', color: '#E53E3E' },
  { start: 40, end: 60, name: 'Dramatic Peak', color: '#E53E3E' },
  { start: 60, end: 80, name: 'Resolution', color: '#805AD5' },
  { start: 80, end: 100, name: 'Calm Return', color: '#38A169' }
])

// Methods
const applyPreset = (preset: AtmospherePreset) => {
  currentPreset.value = preset.id
  atmosphereSettings.value = { ...preset.settings }
  updateAtmosphere()
  updateWeather()
  updateAudio()
}

const updateAtmosphere = () => {
  // Emit atmosphere changes to parent components
  console.log('Updating atmosphere:', atmosphereSettings.value)
}

const updateWeather = () => {
  // Update weather effects
  console.log('Updating weather effects')
}

const updateAudio = () => {
  // Update audio settings
  console.log('Updating audio settings')
}

const triggerDramaticMoment = () => {
  // Temporarily apply dramatic lighting and effects
  console.log('Triggering dramatic moment')
}

const createTension = () => {
  // Gradually build tension through atmosphere
  console.log('Building tension')
}

const restorePeace = () => {
  // Return to peaceful atmosphere
  console.log('Restoring peaceful atmosphere')
}

const addMystery = () => {
  // Add mysterious elements
  console.log('Adding mysterious atmosphere')
}

const saveCurrentAtmosphere = () => {
  // Save current settings as custom preset
  console.log('Saving current atmosphere state')
}

const playAtmosphereSequence = () => {
  // Play predefined atmosphere sequence
  console.log('Playing atmosphere sequence')
}

const pauseAtmosphereSequence = () => {
  // Pause sequence playback
  console.log('Pausing atmosphere sequence')
}

const resetAtmosphere = () => {
  // Reset to default settings
  applyPreset(atmospherePresets.value[0])
}
</script>

<style scoped>
.preset-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.timeline-segment {
  opacity: 0.7;
}

.timeline-segment:hover {
  opacity: 1;
}

.timeline-cursor {
  z-index: 10;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
}

.wh-slider {
  appearance: none;
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  outline: none;
}

.wh-slider::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #D4AF37;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.wh-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #D4AF37;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
