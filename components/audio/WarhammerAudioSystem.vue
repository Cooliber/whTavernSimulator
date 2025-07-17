<template>
  <div class="warhammer-audio-system">
    <!-- Audio Controls Panel -->
    <div v-if="showControls" class="audio-controls wh-card p-4 space-y-4">
      <div class="flex items-center justify-between">
        <h4 class="wh-subtitle text-lg">Audio Atmosphere</h4>
        <button
          class="wh-btn wh-btn-secondary text-xs"
          @click="showControls = false"
        >
          <Icon name="x" class="w-3 h-3" />
        </button>
      </div>
      
      <!-- Master Controls -->
      <div class="master-controls space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm text-wh-parchment">Master Volume</span>
          <span class="text-sm text-wh-empire-gold">{{ Math.round(masterVolume * 100) }}%</span>
        </div>
        <input
          v-model="masterVolume"
          type="range"
          min="0"
          max="1"
          step="0.05"
          class="wh-slider w-full"
          @input="updateMasterVolume"
        />
      </div>
      
      <!-- Audio Layers -->
      <div class="audio-layers space-y-2">
        <div
          v-for="layer in audioLayers"
          :key="layer.id"
          class="audio-layer flex items-center justify-between p-2 rounded bg-wh-dark-grey/30"
        >
          <div class="flex items-center space-x-2">
            <button
              class="w-6 h-6 rounded-full flex items-center justify-center"
              :class="layer.playing ? 'bg-wh-empire-gold text-wh-black' : 'bg-wh-iron-grey text-wh-parchment'"
              @click="toggleLayer(layer.id)"
            >
              <Icon :name="layer.playing ? 'pause' : 'play'" class="w-3 h-3" />
            </button>
            <span class="text-sm text-wh-parchment">{{ layer.name }}</span>
          </div>
          
          <div class="flex items-center space-x-2">
            <input
              v-model="layer.volume"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="wh-slider w-16"
              :disabled="!layer.playing"
              @input="updateLayerVolume(layer.id)"
            />
            <span class="text-xs text-wh-aged-paper w-8">{{ Math.round(layer.volume * 100) }}%</span>
          </div>
        </div>
      </div>
      
      <!-- Atmosphere Presets -->
      <div class="presets space-y-2">
        <h5 class="text-sm font-medieval text-wh-parchment">Quick Presets</h5>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="preset in audioPresets"
            :key="preset.id"
            class="wh-btn wh-btn-secondary p-2 text-xs"
            @click="applyPreset(preset)"
          >
            {{ preset.name }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Floating Audio Toggle -->
    <button
      v-if="!showControls"
      class="audio-toggle fixed bottom-4 right-4 w-12 h-12 rounded-full wh-btn wh-btn-primary flex items-center justify-center z-50"
      @click="showControls = true"
    >
      <Icon name="volume-2" class="w-5 h-5" />
    </button>
    
    <!-- Hidden Audio Elements -->
    <div class="hidden">
      <audio
        v-for="layer in audioLayers"
        :key="layer.id"
        :ref="el => audioElements[layer.id] = el"
        :src="layer.src"
        :loop="layer.loop"
        preload="auto"
        @loadeddata="onAudioLoaded(layer.id)"
        @error="onAudioError(layer.id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
interface AudioLayer {
  id: string
  name: string
  src: string
  volume: number
  playing: boolean
  loop: boolean
  category: 'ambient' | 'music' | 'effects' | 'weather'
}

interface AudioPreset {
  id: string
  name: string
  layers: Record<string, { playing: boolean; volume: number }>
}

// Props
interface Props {
  autoPlay?: boolean
  defaultVolume?: number
  showControlsInitially?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoPlay: false,
  defaultVolume: 0.7,
  showControlsInitially: false
})

// Reactive state
const showControls = ref(props.showControlsInitially)
const masterVolume = ref(props.defaultVolume)
const audioElements = ref<Record<string, HTMLAudioElement>>({})
const loadedAudio = ref<Set<string>>(new Set())

// Audio layers with authentic Warhammer Fantasy sounds
const audioLayers = ref<AudioLayer[]>([
  {
    id: 'tavern-ambient',
    name: 'Tavern Ambience',
    src: '/audio/tavern-ambient.mp3',
    volume: 0.6,
    playing: false,
    loop: true,
    category: 'ambient'
  },
  {
    id: 'fireplace',
    name: 'Fireplace Crackling',
    src: '/audio/fireplace-crackling.mp3',
    volume: 0.4,
    playing: false,
    loop: true,
    category: 'ambient'
  },
  {
    id: 'crowd-chatter',
    name: 'Crowd Chatter',
    src: '/audio/crowd-chatter.mp3',
    volume: 0.5,
    playing: false,
    loop: true,
    category: 'ambient'
  },
  {
    id: 'medieval-music',
    name: 'Medieval Music',
    src: '/audio/medieval-music.mp3',
    volume: 0.3,
    playing: false,
    loop: true,
    category: 'music'
  },
  {
    id: 'rain-outside',
    name: 'Rain Outside',
    src: '/audio/rain-outside.mp3',
    volume: 0.7,
    playing: false,
    loop: true,
    category: 'weather'
  },
  {
    id: 'thunder',
    name: 'Thunder',
    src: '/audio/thunder.mp3',
    volume: 0.8,
    playing: false,
    loop: false,
    category: 'weather'
  },
  {
    id: 'wind-howling',
    name: 'Wind Howling',
    src: '/audio/wind-howling.mp3',
    volume: 0.6,
    playing: false,
    loop: true,
    category: 'weather'
  },
  {
    id: 'ale-pouring',
    name: 'Ale Pouring',
    src: '/audio/ale-pouring.mp3',
    volume: 0.5,
    playing: false,
    loop: false,
    category: 'effects'
  },
  {
    id: 'coins-clinking',
    name: 'Coins Clinking',
    src: '/audio/coins-clinking.mp3',
    volume: 0.4,
    playing: false,
    loop: false,
    category: 'effects'
  },
  {
    id: 'door-creak',
    name: 'Door Creaking',
    src: '/audio/door-creak.mp3',
    volume: 0.6,
    playing: false,
    loop: false,
    category: 'effects'
  }
])

// Audio presets for different tavern moods
const audioPresets: AudioPreset[] = [
  {
    id: 'cozy-evening',
    name: 'Cozy Evening',
    layers: {
      'tavern-ambient': { playing: true, volume: 0.6 },
      'fireplace': { playing: true, volume: 0.5 },
      'crowd-chatter': { playing: true, volume: 0.3 },
      'medieval-music': { playing: true, volume: 0.2 }
    }
  },
  {
    id: 'stormy-night',
    name: 'Stormy Night',
    layers: {
      'tavern-ambient': { playing: true, volume: 0.7 },
      'fireplace': { playing: true, volume: 0.6 },
      'rain-outside': { playing: true, volume: 0.8 },
      'wind-howling': { playing: true, volume: 0.4 },
      'crowd-chatter': { playing: true, volume: 0.5 }
    }
  },
  {
    id: 'busy-tavern',
    name: 'Busy Tavern',
    layers: {
      'tavern-ambient': { playing: true, volume: 0.8 },
      'crowd-chatter': { playing: true, volume: 0.7 },
      'medieval-music': { playing: true, volume: 0.4 },
      'ale-pouring': { playing: true, volume: 0.3 }
    }
  },
  {
    id: 'quiet-morning',
    name: 'Quiet Morning',
    layers: {
      'tavern-ambient': { playing: true, volume: 0.4 },
      'fireplace': { playing: true, volume: 0.3 },
      'crowd-chatter': { playing: true, volume: 0.2 }
    }
  }
]

// Emits
const emit = defineEmits<{
  layerToggled: [layerId: string, playing: boolean]
  volumeChanged: [layerId: string, volume: number]
  presetApplied: [presetId: string]
}>()

// Methods
const toggleLayer = async (layerId: string) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  const audio = audioElements.value[layerId]
  
  if (!layer || !audio) return
  
  try {
    if (layer.playing) {
      audio.pause()
      layer.playing = false
    } else {
      // Ensure audio is loaded
      if (!loadedAudio.value.has(layerId)) {
        await new Promise((resolve, reject) => {
          const timeout = setTimeout(() => reject(new Error('Audio load timeout')), 5000)
          audio.addEventListener('loadeddata', () => {
            clearTimeout(timeout)
            resolve(true)
          }, { once: true })
          audio.load()
        })
      }
      
      audio.volume = layer.volume * masterVolume.value
      await audio.play()
      layer.playing = true
    }
    
    emit('layerToggled', layerId, layer.playing)
  } catch (error) {
    console.warn(`Failed to toggle audio layer ${layerId}:`, error)
    // Fallback: create synthetic audio feedback
    createSyntheticAudio(layer.category)
  }
}

const updateLayerVolume = (layerId: string) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  const audio = audioElements.value[layerId]
  
  if (layer && audio) {
    audio.volume = layer.volume * masterVolume.value
    emit('volumeChanged', layerId, layer.volume)
  }
}

const updateMasterVolume = () => {
  // Update all playing audio elements
  audioLayers.value.forEach(layer => {
    if (layer.playing) {
      const audio = audioElements.value[layer.id]
      if (audio) {
        audio.volume = layer.volume * masterVolume.value
      }
    }
  })
}

const applyPreset = (preset: AudioPreset) => {
  // Stop all current audio
  audioLayers.value.forEach(layer => {
    if (layer.playing) {
      const audio = audioElements.value[layer.id]
      if (audio) {
        audio.pause()
        layer.playing = false
      }
    }
  })
  
  // Apply preset settings
  Object.entries(preset.layers).forEach(([layerId, settings]) => {
    const layer = audioLayers.value.find(l => l.id === layerId)
    if (layer) {
      layer.volume = settings.volume
      if (settings.playing) {
        toggleLayer(layerId)
      }
    }
  })
  
  emit('presetApplied', preset.id)
}

const onAudioLoaded = (layerId: string) => {
  loadedAudio.value.add(layerId)
  console.log(`Audio loaded: ${layerId}`)
}

const onAudioError = (layerId: string) => {
  console.warn(`Failed to load audio: ${layerId}`)
  // Remove from loaded set if it was there
  loadedAudio.value.delete(layerId)
}

// Synthetic audio fallback for when real audio files aren't available
const createSyntheticAudio = (category: string) => {
  if (typeof window === 'undefined' || !window.AudioContext) return
  
  try {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    // Different synthetic sounds for different categories
    switch (category) {
      case 'ambient':
        oscillator.frequency.setValueAtTime(200, audioContext.currentTime)
        oscillator.type = 'sine'
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime)
        break
      case 'weather':
        oscillator.frequency.setValueAtTime(100, audioContext.currentTime)
        oscillator.type = 'sawtooth'
        gainNode.gain.setValueAtTime(0.05, audioContext.currentTime)
        break
      case 'effects':
        oscillator.frequency.setValueAtTime(440, audioContext.currentTime)
        oscillator.type = 'square'
        gainNode.gain.setValueAtTime(0.03, audioContext.currentTime)
        break
      default:
        oscillator.frequency.setValueAtTime(300, audioContext.currentTime)
        oscillator.type = 'triangle'
        gainNode.gain.setValueAtTime(0.08, audioContext.currentTime)
    }
    
    oscillator.start()
    oscillator.stop(audioContext.currentTime + 0.5)
  } catch (error) {
    console.warn('Synthetic audio creation failed:', error)
  }
}

// Public methods for external control
const playLayer = (layerId: string) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  if (layer && !layer.playing) {
    toggleLayer(layerId)
  }
}

const stopLayer = (layerId: string) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  if (layer && layer.playing) {
    toggleLayer(layerId)
  }
}

const setLayerVolume = (layerId: string, volume: number) => {
  const layer = audioLayers.value.find(l => l.id === layerId)
  if (layer) {
    layer.volume = Math.max(0, Math.min(1, volume))
    updateLayerVolume(layerId)
  }
}

const stopAll = () => {
  audioLayers.value.forEach(layer => {
    if (layer.playing) {
      stopLayer(layer.id)
    }
  })
}

// Expose methods for parent components
defineExpose({
  playLayer,
  stopLayer,
  setLayerVolume,
  stopAll,
  applyPreset: (presetId: string) => {
    const preset = audioPresets.find(p => p.id === presetId)
    if (preset) applyPreset(preset)
  }
})

// Auto-play setup
onMounted(() => {
  if (props.autoPlay) {
    // Start with a gentle ambient preset
    setTimeout(() => {
      applyPreset(audioPresets[0])
    }, 1000)
  }
})

// Cleanup on unmount
onUnmounted(() => {
  stopAll()
})
</script>

<style scoped>
.audio-toggle {
  animation: pulse 2s infinite;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.audio-controls {
  position: fixed;
  bottom: 4rem;
  right: 1rem;
  width: 300px;
  max-height: 80vh;
  overflow-y: auto;
  z-index: 50;
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.audio-layer {
  transition: all 0.2s ease;
}

.audio-layer:hover {
  background: var(--wh-grey);
}

@media (max-width: 768px) {
  .audio-controls {
    width: calc(100vw - 2rem);
    right: 1rem;
    left: 1rem;
  }
}
</style>
