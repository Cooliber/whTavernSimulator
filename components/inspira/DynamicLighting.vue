<template>
  <div class="dynamic-lighting fixed inset-0 pointer-events-none z-10">
    <!-- Time of Day Overlay -->
    <div 
      class="time-overlay absolute inset-0 transition-all duration-1000"
      :style="timeOverlayStyle"
    />
    
    <!-- Light Sources -->
    <div class="light-sources absolute inset-0">
      <!-- Fireplace Light -->
      <div 
        v-if="lightSources.fireplace.active"
        class="fireplace-light absolute"
        :style="fireplaceStyle"
      >
        <div class="light-glow fireplace-glow" />
        <div class="light-flicker" />
      </div>
      
      <!-- Candle Lights -->
      <div 
        v-for="candle in activeCandleLights" 
        :key="candle.id"
        class="candle-light absolute"
        :style="candle.style"
      >
        <div class="light-glow candle-glow" />
        <div class="candle-flame" />
      </div>
      
      <!-- Magical Lights -->
      <div 
        v-for="magic in activeMagicLights" 
        :key="magic.id"
        class="magic-light absolute"
        :style="magic.style"
      >
        <div class="light-glow magic-glow" :style="{ backgroundColor: magic.color }" />
        <div class="magic-sparkles">
          <div 
            v-for="sparkle in magic.sparkles" 
            :key="sparkle.id"
            class="magic-sparkle"
            :style="sparkle.style"
          />
        </div>
      </div>
      
      <!-- Window Light (Daylight) -->
      <div 
        v-if="lightSources.daylight.active"
        class="window-light absolute"
        :style="windowLightStyle"
      >
        <div class="light-glow daylight-glow" />
        <div class="dust-particles">
          <div 
            v-for="dust in dustParticles" 
            :key="dust.id"
            class="dust-particle"
            :style="dust.style"
          />
        </div>
      </div>
    </div>
    
    <!-- Shadow Overlays -->
    <div class="shadows absolute inset-0">
      <div 
        v-for="shadow in dynamicShadows" 
        :key="shadow.id"
        class="dynamic-shadow absolute"
        :style="shadow.style"
      />
    </div>
    
    <!-- Ambient Light Control -->
    <div 
      class="ambient-control absolute inset-0 transition-opacity duration-2000"
      :style="ambientStyle"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  timeOfDay?: 'dawn' | 'morning' | 'noon' | 'afternoon' | 'dusk' | 'night' | 'midnight'
  fireplaceActive?: boolean
  candleCount?: number
  magicLightIntensity?: number
  ambientBrightness?: number
}

const props = withDefaults(defineProps<Props>(), {
  timeOfDay: 'night',
  fireplaceActive: true,
  candleCount: 6,
  magicLightIntensity: 0.5,
  ambientBrightness: 0.7
})

interface LightSource {
  id: number
  type: string
  x: number
  y: number
  intensity: number
  color: string
  radius: number
  active: boolean
}

interface Particle {
  id: number
  style: Record<string, string>
}

const currentTime = ref('evening')
const lightSources = ref({
  fireplace: { active: true, intensity: 0.8, x: 20, y: 60 },
  daylight: { active: false, intensity: 0.6, x: 80, y: 20 },
  ambient: { intensity: 0.7 }
})

const candleLights = ref<LightSource[]>([])
const magicLights = ref<LightSource[]>([])
const dustParticles = ref<Particle[]>([])
const dynamicShadows = ref<Particle[]>([])

let particleId = 0
let lightingInterval: NodeJS.Timeout | null = null

// Time of day configurations
const timeConfigs = {
  dawn: {
    overlay: 'linear-gradient(to bottom, rgba(255, 183, 77, 0.2), rgba(255, 154, 0, 0.1))',
    ambientLight: 0.4,
    daylightActive: true,
    shadowIntensity: 0.6
  },
  morning: {
    overlay: 'linear-gradient(to bottom, rgba(255, 235, 59, 0.15), rgba(255, 193, 7, 0.05))',
    ambientLight: 0.7,
    daylightActive: true,
    shadowIntensity: 0.4
  },
  noon: {
    overlay: 'linear-gradient(to bottom, rgba(255, 255, 255, 0.1), transparent)',
    ambientLight: 1.0,
    daylightActive: true,
    shadowIntensity: 0.2
  },
  afternoon: {
    overlay: 'linear-gradient(to bottom, rgba(255, 193, 7, 0.1), rgba(255, 152, 0, 0.05))',
    ambientLight: 0.8,
    daylightActive: true,
    shadowIntensity: 0.3
  },
  dusk: {
    overlay: 'linear-gradient(to bottom, rgba(255, 87, 34, 0.2), rgba(156, 39, 176, 0.1))',
    ambientLight: 0.5,
    daylightActive: false,
    shadowIntensity: 0.7
  },
  night: {
    overlay: 'linear-gradient(to bottom, rgba(63, 81, 181, 0.3), rgba(33, 150, 243, 0.2))',
    ambientLight: 0.3,
    daylightActive: false,
    shadowIntensity: 0.8
  },
  midnight: {
    overlay: 'linear-gradient(to bottom, rgba(26, 35, 126, 0.4), rgba(13, 71, 161, 0.3))',
    ambientLight: 0.2,
    daylightActive: false,
    shadowIntensity: 0.9
  }
}

// Computed styles
const timeOverlayStyle = computed(() => {
  const config = timeConfigs[currentTime.value] || timeConfigs.night
  return {
    background: config.overlay,
    opacity: '1'
  }
})

const fireplaceStyle = computed(() => ({
  left: lightSources.value.fireplace.x + '%',
  top: lightSources.value.fireplace.y + '%',
  width: '200px',
  height: '200px',
  transform: 'translate(-50%, -50%)',
  opacity: lightSources.value.fireplace.active ? lightSources.value.fireplace.intensity : '0'
}))

const windowLightStyle = computed(() => ({
  left: lightSources.value.daylight.x + '%',
  top: lightSources.value.daylight.y + '%',
  width: '300px',
  height: '400px',
  transform: 'translate(-50%, -50%)',
  opacity: lightSources.value.daylight.active ? lightSources.value.daylight.intensity : '0'
}))

const ambientStyle = computed(() => {
  const config = timeConfigs[currentTime.value] || timeConfigs.night
  const brightness = config.ambientLight * props.ambientBrightness
  return {
    backgroundColor: `rgba(0, 0, 0, ${1 - brightness})`,
    opacity: '1'
  }
})

const activeCandleLights = computed(() =>
  candleLights.value.filter(candle => candle.active).map(candle => ({
    ...candle,
    style: {
      left: candle.x + '%',
      top: candle.y + '%',
      width: '120px',
      height: '120px',
      transform: 'translate(-50%, -50%)',
      opacity: candle.intensity.toString()
    }
  }))
)

const activeMagicLights = computed(() =>
  magicLights.value.filter(magic => magic.active).map(magic => ({
    ...magic,
    style: {
      left: magic.x + '%',
      top: magic.y + '%',
      width: '150px',
      height: '150px',
      transform: 'translate(-50%, -50%)',
      opacity: magic.intensity.toString()
    }
  }))
)

// Light source management
const createCandleLight = (x: number, y: number): LightSource => ({
  id: particleId++,
  type: 'candle',
  x,
  y,
  intensity: 0.6 + Math.random() * 0.4,
  color: '#ffb74d',
  radius: 80 + Math.random() * 40,
  active: true
})

const createMagicLight = (x: number, y: number, color: string): LightSource & { sparkles: Particle[] } => ({
  id: particleId++,
  type: 'magic',
  x,
  y,
  intensity: 0.7 + Math.random() * 0.3,
  color,
  radius: 100 + Math.random() * 50,
  active: true,
  sparkles: Array.from({ length: 8 }, (_, i) => ({
    id: particleId++,
    style: {
      position: 'absolute',
      left: Math.random() * 100 + '%',
      top: Math.random() * 100 + '%',
      width: '2px',
      height: '2px',
      backgroundColor: color,
      borderRadius: '50%',
      animation: `sparkle-twinkle ${1 + Math.random()}s ease-in-out infinite`,
      animationDelay: Math.random() * 2 + 's'
    }
  }))
})

const createDustParticle = (): Particle => ({
  id: particleId++,
  style: {
    position: 'absolute',
    left: Math.random() * 100 + '%',
    top: Math.random() * 100 + '%',
    width: '1px',
    height: '1px',
    backgroundColor: 'rgba(255, 255, 255, 0.6)',
    borderRadius: '50%',
    animation: `dust-float ${3 + Math.random() * 4}s linear infinite`,
    animationDelay: Math.random() * 3 + 's'
  }
})

const createDynamicShadow = (x: number, y: number, size: number): Particle => ({
  id: particleId++,
  style: {
    left: x + '%',
    top: y + '%',
    width: size + 'px',
    height: size + 'px',
    background: 'radial-gradient(circle, rgba(0, 0, 0, 0.3) 0%, transparent 70%)',
    borderRadius: '50%',
    transform: 'translate(-50%, -50%)',
    animation: `shadow-sway ${4 + Math.random() * 2}s ease-in-out infinite`,
    animationDelay: Math.random() * 2 + 's'
  }
})

const initializeLights = () => {
  // Create candle lights
  candleLights.value = []
  for (let i = 0; i < props.candleCount; i++) {
    const x = 10 + Math.random() * 80
    const y = 30 + Math.random() * 60
    candleLights.value.push(createCandleLight(x, y))
  }
  
  // Create magic lights
  magicLights.value = []
  if (props.magicLightIntensity > 0) {
    const magicColors = ['#9c27b0', '#3f51b5', '#00bcd4', '#4caf50']
    for (let i = 0; i < Math.floor(props.magicLightIntensity * 4); i++) {
      const x = 20 + Math.random() * 60
      const y = 20 + Math.random() * 70
      const color = magicColors[Math.floor(Math.random() * magicColors.length)]
      magicLights.value.push(createMagicLight(x, y, color))
    }
  }
  
  // Create dust particles for daylight
  dustParticles.value = []
  if (lightSources.value.daylight.active) {
    for (let i = 0; i < 20; i++) {
      dustParticles.value.push(createDustParticle())
    }
  }
  
  // Create dynamic shadows
  dynamicShadows.value = []
  const config = timeConfigs[currentTime.value] || timeConfigs.night
  const shadowCount = Math.floor(config.shadowIntensity * 10)
  for (let i = 0; i < shadowCount; i++) {
    const x = Math.random() * 100
    const y = Math.random() * 100
    const size = 50 + Math.random() * 100
    dynamicShadows.value.push(createDynamicShadow(x, y, size))
  }
}

const updateTimeOfDay = (newTime: string) => {
  currentTime.value = newTime
  const config = timeConfigs[newTime] || timeConfigs.night
  
  // Update daylight
  lightSources.value.daylight.active = config.daylightActive
  lightSources.value.daylight.intensity = config.ambientLight
  
  // Update ambient lighting
  lightSources.value.ambient.intensity = config.ambientLight
  
  // Reinitialize lights for new time
  initializeLights()
}

const toggleFireplace = () => {
  lightSources.value.fireplace.active = !lightSources.value.fireplace.active
}

const addMagicLight = (x: number, y: number, color = '#9c27b0') => {
  magicLights.value.push(createMagicLight(x, y, color))
}

const removeMagicLight = (id: number) => {
  magicLights.value = magicLights.value.filter(light => light.id !== id)
}

const startLightingAnimation = () => {
  if (lightingInterval) clearInterval(lightingInterval)
  
  lightingInterval = setInterval(() => {
    // Flicker fireplace
    if (lightSources.value.fireplace.active) {
      lightSources.value.fireplace.intensity = 0.7 + Math.random() * 0.3
    }
    
    // Flicker candles
    candleLights.value.forEach(candle => {
      if (candle.active) {
        candle.intensity = 0.5 + Math.random() * 0.5
      }
    })
    
    // Update magic lights
    magicLights.value.forEach(magic => {
      if (magic.active) {
        magic.intensity = 0.6 + Math.random() * 0.4
      }
    })
  }, 100)
}

// Watch for prop changes
watch(() => props.timeOfDay, (newTime) => {
  updateTimeOfDay(newTime)
})

watch(() => props.fireplaceActive, (active) => {
  lightSources.value.fireplace.active = active
})

watch(() => props.candleCount, () => {
  initializeLights()
})

watch(() => props.magicLightIntensity, () => {
  initializeLights()
})

// Lifecycle
onMounted(() => {
  currentTime.value = props.timeOfDay
  lightSources.value.fireplace.active = props.fireplaceActive
  
  updateTimeOfDay(props.timeOfDay)
  startLightingAnimation()
})

onUnmounted(() => {
  if (lightingInterval) clearInterval(lightingInterval)
})

// Expose methods for external control
defineExpose({
  updateTimeOfDay,
  toggleFireplace,
  addMagicLight,
  removeMagicLight,
  getCurrentLighting: () => ({
    timeOfDay: currentTime.value,
    fireplace: lightSources.value.fireplace,
    candles: candleLights.value.length,
    magicLights: magicLights.value.length
  })
})
</script>

<style scoped>
.dynamic-lighting {
  mix-blend-mode: multiply;
}

.light-glow {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  filter: blur(20px);
}

.fireplace-glow {
  background: radial-gradient(circle, rgba(255, 87, 34, 0.8) 0%, rgba(255, 152, 0, 0.4) 50%, transparent 100%);
  animation: fireplace-flicker 2s ease-in-out infinite;
}

.candle-glow {
  background: radial-gradient(circle, rgba(255, 183, 77, 0.6) 0%, rgba(255, 152, 0, 0.3) 50%, transparent 100%);
  animation: candle-flicker 3s ease-in-out infinite;
}

.magic-glow {
  background: radial-gradient(circle, currentColor 0%, transparent 70%);
  animation: magic-pulse 2s ease-in-out infinite;
}

.daylight-glow {
  background: radial-gradient(ellipse, rgba(255, 255, 255, 0.4) 0%, rgba(255, 235, 59, 0.2) 50%, transparent 100%);
}

.light-flicker {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(255, 87, 34, 0.3) 0%, transparent 60%);
  animation: flicker-dance 0.5s ease-in-out infinite;
}

.candle-flame {
  position: absolute;
  top: 20%;
  left: 50%;
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff5722, #ff9800, #ffeb3b);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: translateX(-50%);
  animation: flame-dance 1s ease-in-out infinite;
}

.magic-sparkles {
  position: absolute;
  inset: 0;
}

.magic-sparkle {
  animation: sparkle-twinkle 2s ease-in-out infinite;
}

.dust-particles {
  position: absolute;
  inset: 0;
}

.dust-particle {
  animation: dust-float 6s linear infinite;
}

.dynamic-shadow {
  mix-blend-mode: multiply;
}

/* Animations */
@keyframes fireplace-flicker {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  25% { opacity: 0.9; transform: scale(1.05); }
  50% { opacity: 0.7; transform: scale(0.95); }
  75% { opacity: 0.85; transform: scale(1.02); }
}

@keyframes candle-flicker {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 0.8; }
}

@keyframes magic-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 0.9; transform: scale(1.1); }
}

@keyframes flicker-dance {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.4; }
}

@keyframes flame-dance {
  0%, 100% { transform: translateX(-50%) rotate(-2deg); }
  25% { transform: translateX(-50%) rotate(2deg) scaleY(1.1); }
  50% { transform: translateX(-50%) rotate(-1deg) scaleY(0.9); }
  75% { transform: translateX(-50%) rotate(1deg) scaleY(1.05); }
}

@keyframes sparkle-twinkle {
  0%, 100% { opacity: 0; transform: scale(0); }
  50% { opacity: 1; transform: scale(1); }
}

@keyframes dust-float {
  0% { transform: translateY(100vh) translateX(0); opacity: 0; }
  10% { opacity: 0.6; }
  90% { opacity: 0.6; }
  100% { transform: translateY(-20px) translateX(20px); opacity: 0; }
}

@keyframes shadow-sway {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-45%, -55%) scale(1.1); }
}

/* Performance optimizations */
.light-glow,
.light-flicker,
.candle-flame,
.magic-sparkle,
.dust-particle,
.dynamic-shadow {
  will-change: transform, opacity;
}
</style>