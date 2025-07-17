<template>
  <div class="atmospheric-controls wh-card wh-card-tavern p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h3 class="wh-title text-xl">Atmospheric Controls</h3>
      <div class="flex items-center space-x-2">
        <Icon name="settings" class="w-5 h-5 text-wh-empire-gold" />
        <span class="text-sm text-wh-aged-paper">Master Controls</span>
      </div>
    </div>

    <!-- Weather Controls -->
    <div class="weather-section space-y-4">
      <h4 class="wh-subtitle text-lg flex items-center">
        <Icon name="cloud-rain" class="w-5 h-5 mr-2" />
        Weather System
      </h4>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-for="weather in weatherOptions"
          :key="weather.type"
          class="wh-btn weather-btn p-3 text-sm"
          :class="currentWeather === weather.type ? 'wh-btn-primary' : 'wh-btn-secondary'"
          @click="setWeather(weather.type)"
        >
          <Icon :name="weather.icon" class="w-4 h-4 mx-auto mb-1" />
          <span class="block">{{ weather.name }}</span>
        </button>
      </div>

      <!-- Weather Intensity -->
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-sm text-wh-parchment">Weather Intensity</span>
          <span class="text-sm text-wh-empire-gold">{{ weatherIntensity }}%</span>
        </div>
        <input
          v-model="weatherIntensity"
          type="range"
          min="0"
          max="100"
          step="10"
          class="wh-slider w-full"
          @input="updateWeatherIntensity"
        />
      </div>
    </div>

    <!-- Lighting Controls -->
    <div class="lighting-section space-y-4">
      <h4 class="wh-subtitle text-lg flex items-center">
        <Icon name="sun" class="w-5 h-5 mr-2" />
        Lighting & Time
      </h4>
      
      <div class="grid grid-cols-3 gap-3">
        <button
          v-for="time in timeOptions"
          :key="time.value"
          class="wh-btn time-btn p-3 text-sm"
          :class="currentTime === time.value ? 'wh-btn-primary' : 'wh-btn-secondary'"
          @click="setTimeOfDay(time.value)"
        >
          <Icon :name="time.icon" class="w-4 h-4 mx-auto mb-1" />
          <span class="block">{{ time.name }}</span>
        </button>
      </div>

      <!-- Fireplace Controls -->
      <div class="fireplace-controls space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm text-wh-parchment">Fireplace</span>
          <button
            class="wh-btn wh-btn-secondary px-3 py-1 text-xs"
            :class="fireplaceActive ? 'wh-fire-glow' : ''"
            @click="toggleFireplace"
          >
            <Icon name="fire" class="w-3 h-3 mr-1" />
            {{ fireplaceActive ? 'Burning' : 'Cold' }}
          </button>
        </div>
        
        <div v-if="fireplaceActive" class="space-y-2">
          <div class="flex justify-between">
            <span class="text-xs text-wh-aged-paper">Fire Intensity</span>
            <span class="text-xs text-wh-fire-orange">{{ fireIntensity }}%</span>
          </div>
          <input
            v-model="fireIntensity"
            type="range"
            min="10"
            max="100"
            step="5"
            class="wh-slider w-full"
            @input="updateFireIntensity"
          />
        </div>
      </div>

      <!-- Candle Controls -->
      <div class="candle-controls space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm text-wh-parchment">Candles</span>
          <span class="text-sm text-wh-candle-yellow">{{ candleCount }} lit</span>
        </div>
        
        <div class="flex space-x-2">
          <button
            class="wh-btn wh-btn-secondary flex-1 py-2 text-xs"
            @click="adjustCandles(-1)"
            :disabled="candleCount <= 0"
          >
            <Icon name="minus" class="w-3 h-3" />
          </button>
          <button
            class="wh-btn wh-btn-secondary flex-1 py-2 text-xs"
            @click="adjustCandles(1)"
            :disabled="candleCount >= 12"
          >
            <Icon name="plus" class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>

    <!-- Audio Controls -->
    <div class="audio-section space-y-4">
      <h4 class="wh-subtitle text-lg flex items-center">
        <Icon name="volume-2" class="w-5 h-5 mr-2" />
        Audio Atmosphere
      </h4>
      
      <!-- Master Volume -->
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-sm text-wh-parchment">Master Volume</span>
          <span class="text-sm text-wh-empire-gold">{{ masterVolume }}%</span>
        </div>
        <input
          v-model="masterVolume"
          type="range"
          min="0"
          max="100"
          step="5"
          class="wh-slider w-full"
          @input="updateMasterVolume"
        />
      </div>

      <!-- Audio Layers -->
      <div class="audio-layers space-y-3">
        <div
          v-for="layer in audioLayers"
          :key="layer.id"
          class="audio-layer flex items-center justify-between p-2 rounded bg-wh-dark-grey/50"
        >
          <div class="flex items-center space-x-2">
            <button
              class="w-6 h-6 rounded-full flex items-center justify-center"
              :class="layer.active ? 'bg-wh-empire-gold text-wh-black' : 'bg-wh-iron-grey text-wh-parchment'"
              @click="toggleAudioLayer(layer.id)"
            >
              <Icon :name="layer.active ? 'pause' : 'play'" class="w-3 h-3" />
            </button>
            <span class="text-sm text-wh-parchment">{{ layer.name }}</span>
          </div>
          
          <div class="flex items-center space-x-2">
            <input
              v-model="layer.volume"
              type="range"
              min="0"
              max="100"
              step="5"
              class="wh-slider w-16"
              :disabled="!layer.active"
              @input="updateLayerVolume(layer.id, layer.volume)"
            />
            <span class="text-xs text-wh-aged-paper w-8">{{ layer.volume }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Crowd Controls -->
    <div class="crowd-section space-y-4">
      <h4 class="wh-subtitle text-lg flex items-center">
        <Icon name="users" class="w-5 h-5 mr-2" />
        Tavern Crowd
      </h4>
      
      <div class="grid grid-cols-2 gap-3">
        <div class="crowd-control">
          <span class="text-sm text-wh-parchment block mb-2">Crowd Size</span>
          <select
            v-model="crowdSize"
            class="wh-input w-full text-sm"
            @change="updateCrowdSize"
          >
            <option value="empty">Empty</option>
            <option value="sparse">Sparse</option>
            <option value="moderate">Moderate</option>
            <option value="busy">Busy</option>
            <option value="packed">Packed</option>
          </select>
        </div>
        
        <div class="mood-control">
          <span class="text-sm text-wh-parchment block mb-2">Tavern Mood</span>
          <select
            v-model="tavernMood"
            class="wh-input w-full text-sm"
            @change="updateTavernMood"
          >
            <option value="peaceful">Peaceful</option>
            <option value="cheerful">Cheerful</option>
            <option value="tense">Tense</option>
            <option value="rowdy">Rowdy</option>
            <option value="mysterious">Mysterious</option>
            <option value="festive">Festive</option>
          </select>
        </div>
      </div>

      <!-- Crowd Noise Level -->
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-sm text-wh-parchment">Crowd Noise</span>
          <span class="text-sm text-wh-empire-gold">{{ crowdNoise }}%</span>
        </div>
        <input
          v-model="crowdNoise"
          type="range"
          min="0"
          max="100"
          step="5"
          class="wh-slider w-full"
          @input="updateCrowdNoise"
        />
      </div>
    </div>

    <!-- Quick Presets -->
    <div class="presets-section space-y-4">
      <h4 class="wh-subtitle text-lg flex items-center">
        <Icon name="bookmark" class="w-5 h-5 mr-2" />
        Atmosphere Presets
      </h4>
      
      <div class="grid grid-cols-2 gap-2">
        <button
          v-for="preset in atmospherePresets"
          :key="preset.id"
          class="wh-btn wh-btn-secondary p-2 text-xs"
          @click="applyPreset(preset)"
        >
          <Icon :name="preset.icon" class="w-3 h-3 mx-auto mb-1" />
          <span class="block">{{ preset.name }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface WeatherOption {
  type: string
  name: string
  icon: string
}

interface TimeOption {
  value: string
  name: string
  icon: string
}

interface AudioLayer {
  id: string
  name: string
  active: boolean
  volume: number
}

interface AtmospherePreset {
  id: string
  name: string
  icon: string
  settings: {
    weather: string
    weatherIntensity: number
    time: string
    fireplace: boolean
    fireIntensity: number
    candles: number
    crowdSize: string
    tavernMood: string
    crowdNoise: number
    audioLayers: Record<string, { active: boolean; volume: number }>
  }
}

// Reactive state
const currentWeather = ref('clear')
const weatherIntensity = ref(50)
const currentTime = ref('evening')
const fireplaceActive = ref(true)
const fireIntensity = ref(75)
const candleCount = ref(6)
const masterVolume = ref(70)
const crowdSize = ref('moderate')
const tavernMood = ref('cheerful')
const crowdNoise = ref(40)

// Weather options
const weatherOptions: WeatherOption[] = [
  { type: 'clear', name: 'Clear', icon: 'sun' },
  { type: 'cloudy', name: 'Cloudy', icon: 'cloud' },
  { type: 'rain', name: 'Rain', icon: 'cloud-rain' },
  { type: 'storm', name: 'Storm', icon: 'zap' },
  { type: 'snow', name: 'Snow', icon: 'snowflake' },
  { type: 'fog', name: 'Fog', icon: 'cloud' }
]

// Time options
const timeOptions: TimeOption[] = [
  { value: 'dawn', name: 'Dawn', icon: 'sunrise' },
  { value: 'day', name: 'Day', icon: 'sun' },
  { value: 'dusk', name: 'Dusk', icon: 'sunset' },
  { value: 'evening', name: 'Evening', icon: 'moon' },
  { value: 'night', name: 'Night', icon: 'moon' },
  { value: 'midnight', name: 'Midnight', icon: 'moon' }
]

// Audio layers
const audioLayers = ref<AudioLayer[]>([
  { id: 'ambient', name: 'Tavern Ambience', active: true, volume: 60 },
  { id: 'fire', name: 'Fireplace Crackling', active: true, volume: 40 },
  { id: 'crowd', name: 'Crowd Chatter', active: true, volume: 50 },
  { id: 'music', name: 'Background Music', active: false, volume: 30 },
  { id: 'weather', name: 'Weather Sounds', active: false, volume: 70 }
])

// Atmosphere presets
const atmospherePresets: AtmospherePreset[] = [
  {
    id: 'cozy-evening',
    name: 'Cozy Evening',
    icon: 'fire',
    settings: {
      weather: 'clear',
      weatherIntensity: 30,
      time: 'evening',
      fireplace: true,
      fireIntensity: 80,
      candles: 8,
      crowdSize: 'moderate',
      tavernMood: 'peaceful',
      crowdNoise: 30,
      audioLayers: {
        ambient: { active: true, volume: 70 },
        fire: { active: true, volume: 60 },
        crowd: { active: true, volume: 40 },
        music: { active: true, volume: 25 },
        weather: { active: false, volume: 0 }
      }
    }
  },
  {
    id: 'stormy-night',
    name: 'Stormy Night',
    icon: 'zap',
    settings: {
      weather: 'storm',
      weatherIntensity: 80,
      time: 'night',
      fireplace: true,
      fireIntensity: 90,
      candles: 12,
      crowdSize: 'busy',
      tavernMood: 'tense',
      crowdNoise: 60,
      audioLayers: {
        ambient: { active: true, volume: 80 },
        fire: { active: true, volume: 70 },
        crowd: { active: true, volume: 70 },
        music: { active: false, volume: 0 },
        weather: { active: true, volume: 85 }
      }
    }
  },
  {
    id: 'festival-celebration',
    name: 'Festival Night',
    icon: 'party-popper',
    settings: {
      weather: 'clear',
      weatherIntensity: 20,
      time: 'evening',
      fireplace: true,
      fireIntensity: 70,
      candles: 10,
      crowdSize: 'packed',
      tavernMood: 'festive',
      crowdNoise: 80,
      audioLayers: {
        ambient: { active: true, volume: 90 },
        fire: { active: true, volume: 50 },
        crowd: { active: true, volume: 85 },
        music: { active: true, volume: 70 },
        weather: { active: false, volume: 0 }
      }
    }
  },
  {
    id: 'quiet-morning',
    name: 'Quiet Morning',
    icon: 'sunrise',
    settings: {
      weather: 'clear',
      weatherIntensity: 40,
      time: 'dawn',
      fireplace: false,
      fireIntensity: 0,
      candles: 2,
      crowdSize: 'sparse',
      tavernMood: 'peaceful',
      crowdNoise: 15,
      audioLayers: {
        ambient: { active: true, volume: 40 },
        fire: { active: false, volume: 0 },
        crowd: { active: true, volume: 20 },
        music: { active: false, volume: 0 },
        weather: { active: false, volume: 0 }
      }
    }
  }
]

// Emits
const emit = defineEmits<{
  weatherChange: [weather: string, intensity: number]
  timeChange: [time: string]
  fireplaceChange: [active: boolean, intensity: number]
  candleChange: [count: number]
  audioChange: [layer: string, active: boolean, volume: number]
  crowdChange: [size: string, mood: string, noise: number]
  presetApplied: [preset: AtmospherePreset]
}>()

// Methods
const setWeather = (weather: string) => {
  currentWeather.value = weather
  emit('weatherChange', weather, weatherIntensity.value)
}

const updateWeatherIntensity = () => {
  emit('weatherChange', currentWeather.value, weatherIntensity.value)
}

const setTimeOfDay = (time: string) => {
  currentTime.value = time
  emit('timeChange', time)
}

const toggleFireplace = () => {
  fireplaceActive.value = !fireplaceActive.value
  emit('fireplaceChange', fireplaceActive.value, fireIntensity.value)
}

const updateFireIntensity = () => {
  emit('fireplaceChange', fireplaceActive.value, fireIntensity.value)
}

const adjustCandles = (delta: number) => {
  candleCount.value = Math.max(0, Math.min(12, candleCount.value + delta))
  emit('candleChange', candleCount.value)
}

const updateMasterVolume = () => {
  // Update all audio layers proportionally
  audioLayers.value.forEach(layer => {
    emit('audioChange', layer.id, layer.active, layer.volume)
  })
}

const toggleAudioLayer = (layerId: string) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  if (layer) {
    layer.active = !layer.active
    emit('audioChange', layerId, layer.active, layer.volume)
  }
}

const updateLayerVolume = (layerId: string, volume: number) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  if (layer) {
    emit('audioChange', layerId, layer.active, volume)
  }
}

const updateCrowdSize = () => {
  emit('crowdChange', crowdSize.value, tavernMood.value, crowdNoise.value)
}

const updateTavernMood = () => {
  emit('crowdChange', crowdSize.value, tavernMood.value, crowdNoise.value)
}

const updateCrowdNoise = () => {
  emit('crowdChange', crowdSize.value, tavernMood.value, crowdNoise.value)
}

const applyPreset = (preset: AtmospherePreset) => {
  // Apply all preset settings
  currentWeather.value = preset.settings.weather
  weatherIntensity.value = preset.settings.weatherIntensity
  currentTime.value = preset.settings.time
  fireplaceActive.value = preset.settings.fireplace
  fireIntensity.value = preset.settings.fireIntensity
  candleCount.value = preset.settings.candles
  crowdSize.value = preset.settings.crowdSize
  tavernMood.value = preset.settings.tavernMood
  crowdNoise.value = preset.settings.crowdNoise
  
  // Apply audio layer settings
  Object.entries(preset.settings.audioLayers).forEach(([layerId, settings]) => {
    const layer = audioLayers.value.find(l => l.id === layerId)
    if (layer) {
      layer.active = settings.active
      layer.volume = settings.volume
    }
  })
  
  emit('presetApplied', preset)
}
</script>

<style scoped>
.wh-slider {
  appearance: none;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(to right, var(--wh-empire-gold) 0%, var(--wh-empire-gold) var(--value, 0%), var(--wh-iron-grey) var(--value, 0%), var(--wh-iron-grey) 100%);
  outline: none;
  transition: all 0.2s ease;
}

.wh-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--wh-empire-gold);
  cursor: pointer;
  border: 2px solid var(--wh-brass);
  transition: all 0.2s ease;
}

.wh-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.audio-layer {
  transition: all 0.3s ease;
}

.audio-layer:hover {
  background: var(--wh-grey);
}

.weather-btn,
.time-btn {
  transition: all 0.3s ease;
}

.weather-btn:hover,
.time-btn:hover {
  transform: translateY(-2px);
}
</style>
