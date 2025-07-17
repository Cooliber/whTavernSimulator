<template>
  <div class="tavern-atmosphere fixed inset-0 pointer-events-none z-0" :class="{ 'reduced-motion': prefersReducedMotion }">
    <!-- Base dark overlay -->
    <div class="absolute inset-0 bg-gradient-to-b from-atmosphere-shadow-deep/80 to-atmosphere-shadow-medium/90"></div>
    
    <!-- Flickering candle lights -->
    <div v-if="showCandleEffects" class="candle-lights">
      <div
        v-for="candle in candles"
        :key="candle.id"
        class="absolute rounded-full animate-candle-flicker"
        :style="{
          left: candle.x + '%',
          top: candle.y + '%',
          width: candle.size + 'px',
          height: candle.size + 'px',
          background: `radial-gradient(circle, ${candle.color} 0%, transparent 70%)`,
          filter: `blur(${candle.blur}px)`
        }"
      ></div>
    </div>
    
    <!-- Floating embers -->
    <div v-if="showEmberEffects" class="ember-particles">
      <div
        v-for="ember in embers"
        :key="ember.id"
        class="absolute w-1 h-1 bg-atmosphere-ember rounded-full animate-ember-rise"
        :style="{
          left: ember.x + '%',
          top: ember.y + '%',
          animationDelay: ember.delay + 's',
          animationDuration: ember.duration + 's'
        }"
      ></div>
    </div>
    
    <!-- Dancing shadows -->
    <div v-if="showShadowEffects" class="shadow-effects">
      <div
        v-for="shadow in shadows"
        :key="shadow.id"
        class="absolute bg-black/20 rounded-full animate-shadow-dance"
        :style="{
          left: shadow.x + '%',
          top: shadow.y + '%',
          width: shadow.width + 'px',
          height: shadow.height + 'px',
          animationDelay: shadow.delay + 's'
        }"
      ></div>
    </div>
    
    <!-- Atmospheric fog/smoke -->
    <div v-if="showFogEffects" class="fog-overlay">
      <div class="absolute inset-0 bg-gradient-to-t from-atmosphere-smoke/10 via-transparent to-transparent animate-pulse"></div>
    </div>
    
    <!-- Corner vignette -->
    <div class="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/30"></div>
    
    <!-- Fireplace glow (if enabled) -->
    <div v-if="showFireplaceGlow" class="fireplace-glow">
      <div 
        class="absolute bottom-0 left-1/4 w-1/2 h-1/3 bg-gradient-to-t from-atmosphere-fire-glow/20 to-transparent rounded-full animate-fire-flicker"
        style="filter: blur(20px)"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface AtmosphereProps {
  intensity?: 'low' | 'medium' | 'high'
  showCandleEffects?: boolean
  showEmberEffects?: boolean
  showShadowEffects?: boolean
  showFogEffects?: boolean
  showFireplaceGlow?: boolean
  candleCount?: number
  emberCount?: number
  shadowCount?: number
}

const props = withDefaults(defineProps<AtmosphereProps>(), {
  intensity: 'medium',
  showCandleEffects: true,
  showEmberEffects: true,
  showShadowEffects: true,
  showFogEffects: true,
  showFireplaceGlow: false,
  candleCount: 8,
  emberCount: 12,
  shadowCount: 6
})

// Accessibility
const prefersReducedMotion = ref(false)

onMounted(() => {
  if (typeof window !== 'undefined') {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches
    
    mediaQuery.addEventListener('change', (e) => {
      prefersReducedMotion.value = e.matches
    })
  }
})

// Generate candle light positions and properties
const candles = computed(() => {
  const candleArray = []
  for (let i = 0; i < props.candleCount; i++) {
    candleArray.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: 20 + Math.random() * 40,
      color: `rgba(255, ${179 + Math.random() * 76}, 71, ${0.1 + Math.random() * 0.2})`,
      blur: 8 + Math.random() * 12
    })
  }
  return candleArray
})

// Generate ember particles
const embers = computed(() => {
  const emberArray = []
  for (let i = 0; i < props.emberCount; i++) {
    emberArray.push({
      id: i,
      x: Math.random() * 100,
      y: 80 + Math.random() * 20, // Start from bottom
      delay: Math.random() * 4,
      duration: 3 + Math.random() * 2
    })
  }
  return emberArray
})

// Generate shadow effects
const shadows = computed(() => {
  const shadowArray = []
  for (let i = 0; i < props.shadowCount; i++) {
    shadowArray.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      width: 50 + Math.random() * 100,
      height: 30 + Math.random() * 60,
      delay: Math.random() * 6
    })
  }
  return shadowArray
})

// Intensity-based adjustments
const intensityMultiplier = computed(() => {
  switch (props.intensity) {
    case 'low': return 0.5
    case 'high': return 1.5
    default: return 1
  }
})
</script>

<style scoped>
.tavern-atmosphere {
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
}

/* Reduced motion support */
.reduced-motion .animate-candle-flicker,
.reduced-motion .animate-ember-rise,
.reduced-motion .animate-shadow-dance,
.reduced-motion .animate-fire-flicker,
.reduced-motion .animate-pulse {
  animation: none !important;
}

/* Custom radial gradient */
.bg-radial-gradient {
  background: radial-gradient(ellipse at center, var(--tw-gradient-stops));
}

/* Enhanced candle light effects */
.candle-lights > div {
  transition: opacity 0.3s ease-in-out;
}

.candle-lights > div:hover {
  opacity: 0.8;
}

/* Ember particle effects */
.ember-particles > div {
  box-shadow: 0 0 4px rgba(255, 69, 0, 0.6);
}

/* Shadow effects */
.shadow-effects > div {
  filter: blur(2px);
}

/* Fog overlay */
.fog-overlay {
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(105, 105, 105, 0.05) 25%,
    transparent 50%,
    rgba(105, 105, 105, 0.05) 75%,
    transparent 100%
  );
  background-size: 200% 200%;
  animation: fog-drift 20s ease-in-out infinite;
}

@keyframes fog-drift {
  0%, 100% {
    background-position: 0% 0%;
  }
  50% {
    background-position: 100% 100%;
  }
}

/* Fireplace glow */
.fireplace-glow > div {
  box-shadow: 
    0 0 50px rgba(255, 107, 53, 0.3),
    0 0 100px rgba(255, 107, 53, 0.2),
    0 0 150px rgba(255, 107, 53, 0.1);
}

/* Performance optimizations */
.tavern-atmosphere * {
  will-change: transform, opacity;
  backface-visibility: hidden;
  perspective: 1000px;
}

/* High contrast mode adjustments */
@media (prefers-contrast: high) {
  .tavern-atmosphere {
    filter: contrast(1.2);
  }
  
  .candle-lights > div,
  .ember-particles > div {
    opacity: 0.8;
  }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  .tavern-atmosphere {
    background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.5) 100%);
  }
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .candle-lights > div,
  .ember-particles > div,
  .shadow-effects > div {
    display: none;
  }
  
  .fog-overlay {
    opacity: 0.5;
  }
}

/* Print styles */
@media print {
  .tavern-atmosphere {
    display: none !important;
  }
}
</style>
