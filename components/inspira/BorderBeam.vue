<template>
  <div 
    class="border-beam-container relative"
    :class="className"
  >
    <slot />
    
    <!-- Animated border beams -->
    <div 
      class="border-beam absolute inset-0 rounded-inherit pointer-events-none"
      :style="beamStyle"
    >
      <!-- Top beam -->
      <div 
        class="beam beam-top absolute top-0 left-0 h-px"
        :style="topBeamStyle"
      />
      
      <!-- Right beam -->
      <div 
        class="beam beam-right absolute top-0 right-0 w-px"
        :style="rightBeamStyle"
      />
      
      <!-- Bottom beam -->
      <div 
        class="beam beam-bottom absolute bottom-0 right-0 h-px"
        :style="bottomBeamStyle"
      />
      
      <!-- Left beam -->
      <div 
        class="beam beam-left absolute bottom-0 left-0 w-px"
        :style="leftBeamStyle"
      />
    </div>
    
    <!-- Corner sparkles -->
    <div 
      v-for="(sparkle, index) in cornerSparkles" 
      :key="index"
      class="corner-sparkle absolute pointer-events-none"
      :style="sparkle.style"
    >
      ✨
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  borderWidth?: number
  colorFrom?: string
  colorTo?: string
  duration?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  borderWidth: 2,
  colorFrom: '#ffd700',
  colorTo: '#b8860b',
  duration: 3000,
  className: ''
})

const beamStyle = computed(() => ({
  '--border-width': props.borderWidth + 'px',
  '--color-from': props.colorFrom,
  '--color-to': props.colorTo,
  '--duration': props.duration + 'ms'
}))

const topBeamStyle = computed(() => ({
  width: '100%',
  background: `linear-gradient(90deg, transparent, ${props.colorFrom}, ${props.colorTo}, transparent)`,
  animation: `beam-top ${props.duration}ms linear infinite`
}))

const rightBeamStyle = computed(() => ({
  height: '100%',
  background: `linear-gradient(180deg, transparent, ${props.colorFrom}, ${props.colorTo}, transparent)`,
  animation: `beam-right ${props.duration}ms linear infinite`,
  animationDelay: `${props.duration * 0.25}ms`
}))

const bottomBeamStyle = computed(() => ({
  width: '100%',
  background: `linear-gradient(270deg, transparent, ${props.colorFrom}, ${props.colorTo}, transparent)`,
  animation: `beam-bottom ${props.duration}ms linear infinite`,
  animationDelay: `${props.duration * 0.5}ms`
}))

const leftBeamStyle = computed(() => ({
  height: '100%',
  background: `linear-gradient(0deg, transparent, ${props.colorFrom}, ${props.colorTo}, transparent)`,
  animation: `beam-left ${props.duration}ms linear infinite`,
  animationDelay: `${props.duration * 0.75}ms`
}))

// Corner sparkles for extra magic
const cornerSparkles = ref([
  { style: { top: '-2px', left: '-2px', animationDelay: '0s' } },
  { style: { top: '-2px', right: '-2px', animationDelay: '0.75s' } },
  { style: { bottom: '-2px', right: '-2px', animationDelay: '1.5s' } },
  { style: { bottom: '-2px', left: '-2px', animationDelay: '2.25s' } }
])
</script>

<style scoped>
.border-beam-container {
  border: var(--border-width, 2px) solid transparent;
  background: linear-gradient(var(--bg-color, transparent), var(--bg-color, transparent)) padding-box,
              linear-gradient(45deg, var(--color-from, #ffd700), var(--color-to, #b8860b)) border-box;
}

.beam {
  opacity: 0;
}

.corner-sparkle {
  font-size: 0.5rem;
  animation: sparkle-corner 3s ease-in-out infinite;
  opacity: 0;
}

@keyframes beam-top {
  0% { opacity: 0; transform: translateX(-100%); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateX(100%); }
}

@keyframes beam-right {
  0% { opacity: 0; transform: translateY(-100%); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateY(100%); }
}

@keyframes beam-bottom {
  0% { opacity: 0; transform: translateX(100%); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateX(-100%); }
}

@keyframes beam-left {
  0% { opacity: 0; transform: translateY(100%); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateY(-100%); }
}

@keyframes sparkle-corner {
  0%, 90% { opacity: 0; transform: scale(0) rotate(0deg); }
  95% { opacity: 1; transform: scale(1) rotate(180deg); }
  100% { opacity: 0; transform: scale(0) rotate(360deg); }
}
</style>