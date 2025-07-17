<template>
  <div class="audio-atmosphere">
    <!-- Audio Control Panel -->
    <div v-if="showControls" class="audio-controls fixed bottom-4 right-4 z-50">
      <BorderBeam 
        class="bg-card/90 backdrop-blur-md rounded-xl p-4"
        :border-width="2"
        color-from="#ffd700"
        color-to="#b8860b"
      >
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <HyperText 
              text="Audio Controls"
              class="text-lg font-medieval text-foreground"
              :animation-duration="1000"
            />
            
            <RippleButton 
              class="w-8 h-8 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center"
              ripple-color="rgba(139, 69, 19, 0.5)"
              @click="toggleControls"
            >
              <Icon name="x" class="w-4 h-4" />
            </RippleButton>
          </div>
          
          <!-- Master Volume -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Master Volume</span>
              <span class="text-xs text-muted-foreground">{{ Math.round(masterVolume * 100) }}%</span>
            </div>
            <input 
              v-model="masterVolume"
              type="range"
              min="0"
              max="1"
              step="0.1"
              class="audio-slider w-full"
              @input="updateMasterVolume"
            />
          </div>
          
          <!-- Ambient Sounds -->
          <div class="space-y-3">
            <h4 class="text-sm font-medieval text-foreground">Ambient Sounds</h4>
            <div class="grid grid-cols-2 gap-2">
              <RippleButton 
                v-for="ambient in ambientSounds" 
                :key="ambient.id"
                class="text-xs font-medieval p-2"
                :class="ambient.active ? 'faction-empire' : 'bg-secondary text-secondary-foreground'"
                :ripple-color="ambient.active ? 'rgb(255, 215, 0)' : 'rgba(139, 69, 19, 0.5)'"
                @click="toggleAmbient(ambient.id)"
              >
                <Icon :name="ambient.icon" class="w-3 h-3 mr-1" />
                {{ ambient.name }}
              </RippleButton>
            </div>
          </div>
          
          <!-- Music Controls -->
          <div class="space-y-3">
            <h4 class="text-sm font-medieval text-foreground">Music</h4>
            <div class="flex items-center space-x-2">
              <RippleButton 
                class="flex-1 text-xs font-medieval"
                :class="musicPlaying ? 'bg-red-600 text-white' : 'faction-empire'"
                :ripple-color="musicPlaying ? 'rgba(220, 38, 38, 0.6)' : 'rgb(255, 215, 0)'"
                @click="toggleMusic"
              >
                <Icon :name="musicPlaying ? 'pause' : 'play'" class="w-3 h-3 mr-1" />
                {{ musicPlaying ? 'Pause' : 'Play' }}
              </RippleButton>
              
              <RippleButton 
                class="px-3 py-2 text-xs font-medieval bg-secondary text-secondary-foreground"
                ripple-color="rgba(139, 69, 19, 0.5)"
                @click="nextTrack"
              >
                <Icon name="skip-forward" class="w-3 h-3" />
              </RippleButton>
            </div>
            
            <!-- Music Volume -->
            <div class="space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-xs text-muted-foreground">Music Volume</span>
                <span class="text-xs text-muted-foreground">{{ Math.round(musicVolume * 100) }}%</span>
              </div>
              <input 
                v-model="musicVolume"
                type="range"
                min="0"
                max="1"
                step="0.1"
                class="audio-slider w-full"
                @input="updateMusicVolume"
              />
            </div>
          </div>
          
          <!-- Current Track Info -->
          <div v-if="currentTrack" class="current-track bg-background/30 rounded-lg p-3">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded bg-primary/20 flex items-center justify-center">
                <Icon name="music" class="w-4 h-4 text-primary" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medieval text-foreground truncate">{{ currentTrack.name }}</p>
                <p class="text-xs text-muted-foreground">{{ currentTrack.artist }}</p>
              </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="mt-2 space-y-1">
              <div class="w-full h-1 bg-muted rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-primary to-primary/60 transition-all duration-1000"
                  :style="{ width: trackProgress + '%' }"
                />
              </div>
              <div class="flex justify-between text-xs text-muted-foreground">
                <span>{{ formatTime(currentTime) }}</span>
                <span>{{ formatTime(currentTrack.duration) }}</span>
              </div>
            </div>
          </div>
        </div>
      </BorderBeam>
    </div>
    
    <!-- Audio Toggle Button -->
    <div v-else class="audio-toggle fixed bottom-4 right-4 z-50">
      <RippleButton 
        class="w-12 h-12 rounded-full faction-empire flex items-center justify-center"
        ripple-color="rgb(255, 215, 0)"
        @click="toggleControls"
      >
        <Icon name="volume-2" class="w-6 h-6" />
      </RippleButton>
    </div>
    
    <!-- Audio Elements (Hidden) -->
    <div class="hidden">
      <!-- Background Music -->
      <audio 
        ref="musicPlayer"
        :volume="musicVolume * masterVolume"
        loop
        @timeupdate="updateProgress"
        @ended="nextTrack"
      />
      
      <!-- Ambient Sound Players -->
      <audio 
        v-for="ambient in ambientSounds" 
        :key="ambient.id"
        :ref="el => setAmbientRef(el, ambient.id)"
        :volume="ambient.volume * masterVolume"
        loop
      />
      
      <!-- Sound Effect Players -->
      <audio 
        v-for="effect in soundEffects" 
        :key="effect.id"
        :ref="el => setEffectRef(el, effect.id)"
        :volume="effect.volume * masterVolume"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
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

interface AudioTrack {
  id: string
  name: string
  artist: string
  url: string
  duration: number
  genre: string
}

interface AmbientSound {
  id: string
  name: string
  icon: string
  url: string
  volume: number
  active: boolean
}

interface SoundEffect {
  id: string
  name: string
  url: string
  volume: number
}

const showControls = ref(props.showControlsInitially)
const masterVolume = ref(props.defaultVolume)
const musicVolume = ref(0.8)
const musicPlaying = ref(false)
const currentTrackIndex = ref(0)
const currentTime = ref(0)
const trackProgress = ref(0)

const musicPlayer = ref<HTMLAudioElement>()
const ambientRefs = ref<Record<string, HTMLAudioElement>>({})
const effectRefs = ref<Record<string, HTMLAudioElement>>({})

// Music tracks
const musicTracks = ref<AudioTrack[]>([
  {
    id: 'tavern-theme',
    name: 'The Golden Griffin',
    artist: 'Medieval Minstrels',
    url: '/audio/music/tavern-theme.mp3',
    duration: 240,
    genre: 'Medieval'
  },
  {
    id: 'battle-march',
    name: 'March of the Empire',
    artist: 'Imperial Orchestra',
    url: '/audio/music/battle-march.mp3',
    duration: 180,
    genre: 'Epic'
  },
  {
    id: 'mystical-forest',
    name: 'Whispers of Athel Loren',
    artist: 'Elven Choir',
    url: '/audio/music/mystical-forest.mp3',
    duration: 300,
    genre: 'Ambient'
  },
  {
    id: 'dwarf-halls',
    name: 'Halls of the Mountain King',
    artist: 'Dwarf Miners',
    url: '/audio/music/dwarf-halls.mp3',
    duration: 220,
    genre: 'Folk'
  }
])

// Ambient sounds
const ambientSounds = ref<AmbientSound[]>([
  {
    id: 'fireplace',
    name: 'Fireplace',
    icon: 'flame',
    url: '/audio/ambient/fireplace.mp3',
    volume: 0.6,
    active: true
  },
  {
    id: 'rain',
    name: 'Rain',
    icon: 'cloud-rain',
    url: '/audio/ambient/rain.mp3',
    volume: 0.4,
    active: false
  },
  {
    id: 'wind',
    name: 'Wind',
    icon: 'wind',
    url: '/audio/ambient/wind.mp3',
    volume: 0.3,
    active: false
  },
  {
    id: 'crowd',
    name: 'Crowd',
    icon: 'users',
    url: '/audio/ambient/tavern-crowd.mp3',
    volume: 0.5,
    active: true
  },
  {
    id: 'kitchen',
    name: 'Kitchen',
    icon: 'utensils',
    url: '/audio/ambient/kitchen.mp3',
    volume: 0.4,
    active: false
  },
  {
    id: 'horses',
    name: 'Stables',
    icon: 'horse',
    url: '/audio/ambient/horses.mp3',
    volume: 0.3,
    active: false
  }
])

// Sound effects
const soundEffects = ref<SoundEffect[]>([
  {
    id: 'coin-drop',
    name: 'Coin Drop',
    url: '/audio/effects/coin-drop.mp3',
    volume: 0.8
  },
  {
    id: 'door-open',
    name: 'Door Open',
    url: '/audio/effects/door-open.mp3',
    volume: 0.6
  },
  {
    id: 'sword-clash',
    name: 'Sword Clash',
    url: '/audio/effects/sword-clash.mp3',
    volume: 0.7
  },
  {
    id: 'magic-cast',
    name: 'Magic Cast',
    url: '/audio/effects/magic-cast.mp3',
    volume: 0.5
  },
  {
    id: 'ale-pour',
    name: 'Ale Pour',
    url: '/audio/effects/ale-pour.mp3',
    volume: 0.6
  }
])

// Computed properties
const currentTrack = computed(() => {
  return musicTracks.value[currentTrackIndex.value] || null
})

// Audio management methods
const setAmbientRef = (el: HTMLAudioElement | null, id: string) => {
  if (el) {
    ambientRefs.value[id] = el
  }
}

const setEffectRef = (el: HTMLAudioElement | null, id: string) => {
  if (el) {
    effectRefs.value[id] = el
  }
}

const toggleControls = () => {
  showControls.value = !showControls.value
}

const updateMasterVolume = () => {
  // Update all audio elements
  if (musicPlayer.value) {
    musicPlayer.value.volume = musicVolume.value * masterVolume.value
  }
  
  Object.values(ambientRefs.value).forEach(audio => {
    const ambient = ambientSounds.value.find(a => ambientRefs.value[a.id] === audio)
    if (ambient) {
      audio.volume = ambient.volume * masterVolume.value
    }
  })
}

const updateMusicVolume = () => {
  if (musicPlayer.value) {
    musicPlayer.value.volume = musicVolume.value * masterVolume.value
  }
}

const toggleMusic = async () => {
  if (!musicPlayer.value || !currentTrack.value) {
    console.warn('Music player or track not available')
    return
  }

  try {
    if (musicPlaying.value) {
      musicPlayer.value.pause()
      musicPlaying.value = false
    } else {
      // Load track if not loaded
      if (musicPlayer.value.src !== currentTrack.value.url) {
        musicPlayer.value.src = currentTrack.value.url
        // Wait for the audio to be ready
        await new Promise((resolve, reject) => {
          const onCanPlay = () => {
            musicPlayer.value?.removeEventListener('canplay', onCanPlay)
            musicPlayer.value?.removeEventListener('error', onError)
            resolve(true)
          }
          const onError = (e: Event) => {
            musicPlayer.value?.removeEventListener('canplay', onCanPlay)
            musicPlayer.value?.removeEventListener('error', onError)
            reject(e)
          }
          musicPlayer.value?.addEventListener('canplay', onCanPlay)
          musicPlayer.value?.addEventListener('error', onError)
        })
      }

      await musicPlayer.value.play()
      musicPlaying.value = true
    }
  } catch (error) {
    console.warn('Audio playback failed:', error)
    // Fallback to silent mode
    musicPlaying.value = false
  }
}

const nextTrack = () => {
  currentTrackIndex.value = (currentTrackIndex.value + 1) % musicTracks.value.length
  
  if (musicPlaying.value && musicPlayer.value && currentTrack.value) {
    musicPlayer.value.src = currentTrack.value.url
    musicPlayer.value.play().catch(console.warn)
  }
}

const toggleAmbient = async (ambientId: string) => {
  const ambient = ambientSounds.value.find(a => a.id === ambientId)
  const audioElement = ambientRefs.value[ambientId]

  if (!ambient) {
    console.warn(`Ambient sound ${ambientId} not found`)
    return
  }

  if (!audioElement) {
    console.warn(`Audio element for ${ambientId} not found`)
    return
  }

  try {
    if (ambient.active) {
      audioElement.pause()
      ambient.active = false
    } else {
      if (audioElement.src !== ambient.url) {
        audioElement.src = ambient.url
        // Wait for audio to be ready
        await new Promise((resolve, reject) => {
          const onCanPlay = () => {
            audioElement.removeEventListener('canplay', onCanPlay)
            audioElement.removeEventListener('error', onError)
            resolve(true)
          }
          const onError = (e: Event) => {
            audioElement.removeEventListener('canplay', onCanPlay)
            audioElement.removeEventListener('error', onError)
            reject(e)
          }
          audioElement.addEventListener('canplay', onCanPlay)
          audioElement.addEventListener('error', onError)
        })
      }

      audioElement.volume = ambient.volume * masterVolume.value
      await audioElement.play()
      ambient.active = true
    }
  } catch (error) {
    console.warn(`Ambient audio ${ambientId} failed:`, error)
    ambient.active = false
  }
}

const playEffect = async (effectId: string) => {
  const effect = soundEffects.value.find(e => e.id === effectId)
  const audioElement = effectRefs.value[effectId]
  
  if (!effect || !audioElement) return
  
  try {
    if (audioElement.src !== effect.url) {
      audioElement.src = effect.url
    }
    
    audioElement.volume = effect.volume * masterVolume.value
    audioElement.currentTime = 0
    await audioElement.play()
  } catch (error) {
    console.warn('Sound effect failed:', error)
  }
}

const updateProgress = () => {
  if (musicPlayer.value && currentTrack.value) {
    currentTime.value = musicPlayer.value.currentTime
    trackProgress.value = (currentTime.value / currentTrack.value.duration) * 100
  }
}

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const setWeatherAmbient = (weather: string) => {
  // Automatically adjust ambient sounds based on weather
  const weatherMappings = {
    rain: ['rain', 'wind'],
    storm: ['rain', 'wind'],
    snow: ['wind'],
    fog: ['wind'],
    clear: ['fireplace', 'crowd']
  }
  
  const targetAmbients = weatherMappings[weather] || ['fireplace', 'crowd']
  
  ambientSounds.value.forEach(ambient => {
    const shouldBeActive = targetAmbients.includes(ambient.id)
    if (ambient.active !== shouldBeActive) {
      toggleAmbient(ambient.id)
    }
  })
}

const setTimeOfDayMusic = (timeOfDay: string) => {
  // Change music based on time of day
  const timeMappings = {
    dawn: 0,
    morning: 0,
    noon: 1,
    afternoon: 1,
    dusk: 2,
    night: 2,
    midnight: 3
  }
  
  const targetIndex = timeMappings[timeOfDay] || 0
  if (currentTrackIndex.value !== targetIndex) {
    currentTrackIndex.value = targetIndex
    if (musicPlaying.value) {
      nextTrack()
    }
  }
}

// Initialize audio system
const initializeAudio = () => {
  try {
    // Set up music player
    if (musicPlayer.value && currentTrack.value) {
      musicPlayer.value.volume = musicVolume.value * masterVolume.value

      if (props.autoPlay) {
        // Try to autoplay (may be blocked by browser)
        toggleMusic().catch(() => {
          console.log('Autoplay blocked - user interaction required')
        })
      }
    }

    // Initialize active ambient sounds
    ambientSounds.value.forEach(ambient => {
      if (ambient.active) {
        toggleAmbient(ambient.id).catch(error => {
          console.warn(`Failed to initialize ambient sound ${ambient.id}:`, error)
        })
      }
    })
  } catch (error) {
    console.warn('Audio system initialization failed:', error)
  }
}

// Lifecycle
onMounted(() => {
  // Delay initialization to ensure DOM is ready
  nextTick(() => {
    initializeAudio()
  })
})

onUnmounted(() => {
  // Clean up audio
  if (musicPlayer.value) {
    musicPlayer.value.pause()
  }
  
  Object.values(ambientRefs.value).forEach(audio => {
    audio.pause()
  })
})

// Expose methods for external control
defineExpose({
  playEffect,
  setWeatherAmbient,
  setTimeOfDayMusic,
  toggleMusic,
  toggleAmbient,
  setMasterVolume: (volume: number) => {
    masterVolume.value = volume
    updateMasterVolume()
  },
  getCurrentState: () => ({
    musicPlaying: musicPlaying.value,
    currentTrack: currentTrack.value,
    activeAmbients: ambientSounds.value.filter(a => a.active).map(a => a.id),
    masterVolume: masterVolume.value
  })
})
</script>

<style scoped>
.audio-controls {
  min-width: 280px;
  max-width: 320px;
}

.audio-slider {
  appearance: none;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(to right, #ffd700 0%, #ffd700 var(--value, 0%), #374151 var(--value, 0%), #374151 100%);
  outline: none;
  transition: all 0.2s ease;
}

.audio-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #b8860b;
  transition: all 0.2s ease;
}

.audio-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.audio-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #b8860b;
  transition: all 0.2s ease;
}

.current-track {
  animation: track-slide-in 0.3s ease-out;
}

@keyframes track-slide-in {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.audio-toggle {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .audio-controls {
    min-width: 260px;
    max-width: 280px;
  }
}
</style>