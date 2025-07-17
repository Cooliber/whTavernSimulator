<template>
  <div class="weather-system fixed inset-0 pointer-events-none z-5">
    <!-- Rain Effect -->
    <div v-if="currentWeather.type === 'rain'" class="rain-container absolute inset-0">
      <div 
        v-for="drop in rainDrops" 
        :key="drop.id"
        class="rain-drop absolute"
        :style="drop.style"
      />
      
      <!-- Rain overlay -->
      <div class="absolute inset-0 bg-blue-900/10 backdrop-blur-[0.5px]" />
      
      <!-- Lightning flashes -->
      <div 
        v-if="lightningActive"
        class="lightning-flash absolute inset-0 bg-white/20 animate-pulse"
        :style="{ animationDuration: '0.1s', animationIterationCount: '3' }"
      />
    </div>
    
    <!-- Snow Effect -->
    <div v-if="currentWeather.type === 'snow'" class="snow-container absolute inset-0">
      <div 
        v-for="flake in snowFlakes" 
        :key="flake.id"
        class="snow-flake absolute text-white"
        :style="flake.style"
      >
        ❄
      </div>
      
      <!-- Snow overlay -->
      <div class="absolute inset-0 bg-blue-100/5" />
    </div>
    
    <!-- Fog Effect -->
    <div v-if="currentWeather.type === 'fog'" class="fog-container absolute inset-0">
      <div 
        v-for="cloud in fogClouds" 
        :key="cloud.id"
        class="fog-cloud absolute rounded-full"
        :style="cloud.style"
      />
      
      <!-- Fog overlay -->
      <div class="absolute inset-0 bg-gray-500/20 backdrop-blur-sm" />
    </div>
    
    <!-- Wind Effect -->
    <div v-if="currentWeather.windStrength > 0" class="wind-container absolute inset-0">
      <div 
        v-for="particle in windParticles" 
        :key="particle.id"
        class="wind-particle absolute"
        :style="particle.style"
      >
        •
      </div>
    </div>
    
    <!-- Weather Transition Overlay -->
    <div 
      v-if="isTransitioning"
      class="weather-transition absolute inset-0 transition-opacity duration-2000"
      :class="{ 'opacity-100': isTransitioning, 'opacity-0': !isTransitioning }"
      :style="{ backgroundColor: transitionColor }"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  weather?: string
  intensity?: number
  windSpeed?: number
  temperature?: number
}

const props = withDefaults(defineProps<Props>(), {
  weather: 'clear',
  intensity: 0.5,
  windSpeed: 0.3,
  temperature: 15
})

interface WeatherParticle {
  id: number
  style: Record<string, string>
}

const currentWeather = ref({
  type: 'clear',
  intensity: 0.5,
  windStrength: 0.3,
  temperature: 15
})

const rainDrops = ref<WeatherParticle[]>([])
const snowFlakes = ref<WeatherParticle[]>([])
const fogClouds = ref<WeatherParticle[]>([])
const windParticles = ref<WeatherParticle[]>([])

const lightningActive = ref(false)
const isTransitioning = ref(false)
const transitionColor = ref('rgba(0, 0, 0, 0.1)')

let particleId = 0
let weatherInterval: NodeJS.Timeout | null = null
let lightningInterval: NodeJS.Timeout | null = null

// Weather patterns
const weatherPatterns = {
  clear: {
    particles: 0,
    overlay: 'transparent',
    duration: 0
  },
  rain: {
    particles: 150,
    overlay: 'rgba(59, 130, 246, 0.1)',
    duration: 800
  },
  snow: {
    particles: 80,
    overlay: 'rgba(219, 234, 254, 0.1)',
    duration: 3000
  },
  fog: {
    particles: 20,
    overlay: 'rgba(107, 114, 128, 0.2)',
    duration: 5000
  },
  storm: {
    particles: 200,
    overlay: 'rgba(17, 24, 39, 0.3)',
    duration: 600
  }
}

const createRainDrop = (): WeatherParticle => {
  const x = Math.random() * 100
  const speed = 0.5 + Math.random() * 1.5
  const size = 1 + Math.random() * 2
  
  return {
    id: particleId++,
    style: {
      left: x + '%',
      top: '-5px',
      width: size + 'px',
      height: (size * 10) + 'px',
      background: 'linear-gradient(to bottom, rgba(59, 130, 246, 0.6), rgba(59, 130, 246, 0.2))',
      borderRadius: '50%',
      animation: `rain-fall ${speed}s linear infinite`,
      animationDelay: Math.random() * 2 + 's'
    }
  }
}

const createSnowFlake = (): WeatherParticle => {
  const x = Math.random() * 100
  const speed = 2 + Math.random() * 4
  const size = 0.5 + Math.random() * 1
  const drift = Math.random() * 40 - 20
  
  return {
    id: particleId++,
    style: {
      left: x + '%',
      top: '-20px',
      fontSize: size + 'rem',
      opacity: '0.7',
      animation: `snow-fall ${speed}s linear infinite, snow-drift ${speed * 0.5}s ease-in-out infinite`,
      animationDelay: Math.random() * 3 + 's',
      transform: `translateX(${drift}px)`
    }
  }
}

const createFogCloud = (): WeatherParticle => {
  const x = Math.random() * 120 - 10
  const y = Math.random() * 120 - 10
  const size = 100 + Math.random() * 200
  const speed = 10 + Math.random() * 20
  
  return {
    id: particleId++,
    style: {
      left: x + '%',
      top: y + '%',
      width: size + 'px',
      height: size + 'px',
      background: 'radial-gradient(circle, rgba(156, 163, 175, 0.3) 0%, transparent 70%)',
      animation: `fog-drift ${speed}s linear infinite`,
      animationDelay: Math.random() * 5 + 's'
    }
  }
}

const createWindParticle = (): WeatherParticle => {
  const y = Math.random() * 100
  const speed = 1 + Math.random() * 2
  const size = 1 + Math.random()
  
  return {
    id: particleId++,
    style: {
      left: '-5px',
      top: y + '%',
      fontSize: size + 'rem',
      color: 'rgba(156, 163, 175, 0.4)',
      animation: `wind-blow ${speed}s linear infinite`,
      animationDelay: Math.random() * 1 + 's'
    }
  }
}

const generateWeatherParticles = () => {
  const pattern = weatherPatterns[currentWeather.value.type] || weatherPatterns.clear

  // Clear existing particles
  rainDrops.value = []
  snowFlakes.value = []
  fogClouds.value = []
  windParticles.value = []

  // Generate new particles based on weather type
  const particleCount = Math.min(Math.floor(pattern.particles * currentWeather.value.intensity), 200) // Limit max particles

  switch (currentWeather.value.type) {
    case 'rain':
    case 'storm':
      rainDrops.value = Array.from({ length: particleCount }, () => createRainDrop())

      // Lightning for storms
      if (currentWeather.value.type === 'storm') {
        startLightning()
      } else {
        stopLightning()
      }
      break

    case 'snow':
      snowFlakes.value = Array.from({ length: particleCount }, () => createSnowFlake())
      break

    case 'fog':
      fogClouds.value = Array.from({ length: particleCount }, () => createFogCloud())
      break

    default:
      stopLightning()
      break
  }

  // Wind particles
  if (currentWeather.value.windStrength > 0.2) {
    const windCount = Math.min(Math.floor(30 * currentWeather.value.windStrength), 50) // Limit wind particles
    windParticles.value = Array.from({ length: windCount }, () => createWindParticle())
  }
}

const startLightning = () => {
  if (lightningInterval) clearInterval(lightningInterval)
  
  lightningInterval = setInterval(() => {
    if (Math.random() < 0.1) { // 10% chance per interval
      lightningActive.value = true
      setTimeout(() => {
        lightningActive.value = false
      }, 300)
    }
  }, 2000)
}

const stopLightning = () => {
  if (lightningInterval) {
    clearInterval(lightningInterval)
    lightningInterval = null
  }
  lightningActive.value = false
}

const changeWeather = (newWeather: string, intensity = 0.5, windSpeed = 0.3, temperature = 15) => {
  isTransitioning.value = true
  transitionColor.value = weatherPatterns[newWeather]?.overlay || 'transparent'
  
  setTimeout(() => {
    currentWeather.value = {
      type: newWeather,
      intensity,
      windStrength: windSpeed,
      temperature
    }
    
    generateWeatherParticles()
    
    setTimeout(() => {
      isTransitioning.value = false
    }, 1000)
  }, 500)
}

const startWeatherCycle = () => {
  if (weatherInterval) clearInterval(weatherInterval)
  
  weatherInterval = setInterval(() => {
    generateWeatherParticles()
  }, 5000)
}

// Watch for prop changes
watch(() => props.weather, (newWeather) => {
  if (newWeather && typeof newWeather === 'string') {
    changeWeather(newWeather, props.intensity, props.windSpeed, props.temperature)
  }
}, { immediate: false })

watch(() => props.intensity, (newIntensity) => {
  if (typeof newIntensity === 'number' && newIntensity >= 0 && newIntensity <= 1) {
    currentWeather.value.intensity = newIntensity
    generateWeatherParticles()
  }
}, { immediate: false })

// Lifecycle
onMounted(() => {
  try {
    currentWeather.value = {
      type: props.weather || 'clear',
      intensity: Math.max(0, Math.min(1, props.intensity)),
      windStrength: Math.max(0, Math.min(1, props.windSpeed)),
      temperature: props.temperature
    }

    generateWeatherParticles()
    startWeatherCycle()
  } catch (error) {
    console.warn('WeatherSystem initialization failed:', error)
    // Fallback to clear weather
    currentWeather.value = {
      type: 'clear',
      intensity: 0.5,
      windStrength: 0.3,
      temperature: 15
    }
  }
})

onUnmounted(() => {
  try {
    if (weatherInterval) {
      clearInterval(weatherInterval)
      weatherInterval = null
    }
    stopLightning()
  } catch (error) {
    console.warn('WeatherSystem cleanup failed:', error)
  }
})

// Expose methods for external control
defineExpose({
  changeWeather,
  getCurrentWeather: () => currentWeather.value
})
</script>

<style scoped>
.weather-system {
  overflow: hidden;
}

.rain-drop {
  border-radius: 0 0 50% 50%;
}

.snow-flake {
  user-select: none;
  pointer-events: none;
}

.fog-cloud {
  filter: blur(2px);
}

.wind-particle {
  user-select: none;
  pointer-events: none;
}

/* Weather animations */
@keyframes rain-fall {
  0% {
    transform: translateY(-100vh) rotate(10deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(10deg);
    opacity: 0;
  }
}

@keyframes snow-fall {
  0% {
    transform: translateY(-100vh);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(100vh);
    opacity: 0;
  }
}

@keyframes snow-drift {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(20px);
  }
}

@keyframes fog-drift {
  0% {
    transform: translateX(-50px);
    opacity: 0;
  }
  25% {
    opacity: 0.6;
  }
  75% {
    opacity: 0.6;
  }
  100% {
    transform: translateX(calc(100vw + 50px));
    opacity: 0;
  }
}

@keyframes wind-blow {
  0% {
    transform: translateX(-20px);
    opacity: 0;
  }
  25% {
    opacity: 0.6;
  }
  75% {
    opacity: 0.6;
  }
  100% {
    transform: translateX(100vw);
    opacity: 0;
  }
}

.lightning-flash {
  animation: lightning-flash 0.1s ease-in-out;
}

@keyframes lightning-flash {
  0%, 100% {
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
}

/* Performance optimizations */
.rain-drop,
.snow-flake,
.fog-cloud,
.wind-particle {
  will-change: transform, opacity;
}
</style>