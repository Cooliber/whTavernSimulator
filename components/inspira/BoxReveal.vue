<template>
  <div 
    ref="containerRef"
    class="box-reveal-container relative overflow-hidden"
    :class="className"
  >
    <!-- Reveal Box Overlay -->
    <div 
      ref="revealBoxRef"
      class="reveal-box absolute inset-0 z-10 transition-all duration-500 ease-out"
      :class="revealBoxClasses"
      :style="revealBoxStyle"
    />
    
    <!-- Content -->
    <div 
      ref="contentRef"
      class="reveal-content relative z-0 transition-all duration-300"
      :class="{ 'opacity-0': !isRevealed }"
    >
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  revealDirection?: 'top' | 'bottom' | 'left' | 'right' | 'center'
  revealSpeed?: number
  triggerOnScroll?: boolean
  boxColor?: string
  revealDelay?: number
  className?: string
  faction?: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
}

const props = withDefaults(defineProps<Props>(), {
  revealDirection: 'bottom',
  revealSpeed: 800,
  triggerOnScroll: true,
  boxColor: '',
  revealDelay: 0,
  className: '',
  faction: 'empire'
})

const emit = defineEmits<{
  revealed: []
  revealStart: []
}>()

// Reactive state
const containerRef = ref<HTMLElement>()
const revealBoxRef = ref<HTMLElement>()
const contentRef = ref<HTMLElement>()
const isRevealed = ref(false)
const isRevealing = ref(false)

// Faction theming
const factionColors = computed(() => {
  const colors = {
    empire: '#ffd700',
    chaos: '#8b0000',
    elves: '#228b22',
    dwarfs: '#daa520',
    undead: '#800080',
    orcs: '#228b22'
  }
  return colors[props.faction]
})

// Computed styles
const revealBoxClasses = computed(() => {
  const baseClasses = 'reveal-box'
  const directionClasses = {
    top: 'origin-top',
    bottom: 'origin-bottom',
    left: 'origin-left',
    right: 'origin-right',
    center: 'origin-center'
  }
  
  return [
    baseClasses,
    directionClasses[props.revealDirection],
    { 'revealing': isRevealing.value }
  ]
})

const revealBoxStyle = computed(() => {
  const baseColor = props.boxColor || factionColors.value
  
  const style: Record<string, string> = {
    backgroundColor: baseColor,
    transitionDuration: `${props.revealSpeed}ms`,
    transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)'
  }
  
  // Apply transform based on reveal state and direction
  if (isRevealed.value) {
    switch (props.revealDirection) {
      case 'top':
        style.transform = 'scaleY(0)'
        break
      case 'bottom':
        style.transform = 'scaleY(0)'
        break
      case 'left':
        style.transform = 'scaleX(0)'
        break
      case 'right':
        style.transform = 'scaleX(0)'
        break
      case 'center':
        style.transform = 'scale(0)'
        break
    }
  } else {
    style.transform = 'scale(1)'
  }
  
  return style
})

// Methods
const startReveal = () => {
  if (isRevealing.value || isRevealed.value) return
  
  isRevealing.value = true
  emit('revealStart')
  
  // Apply delay if specified
  setTimeout(() => {
    isRevealed.value = true
    
    // Wait for animation to complete
    setTimeout(() => {
      isRevealing.value = false
      emit('revealed')
    }, props.revealSpeed)
  }, props.revealDelay)
}

const resetReveal = () => {
  isRevealed.value = false
  isRevealing.value = false
}

// Intersection Observer for scroll trigger
let observer: IntersectionObserver | null = null

const setupScrollTrigger = () => {
  if (!props.triggerOnScroll || !containerRef.value) return
  
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !isRevealed.value) {
          startReveal()
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    }
  )
  
  observer.observe(containerRef.value)
}

const cleanupScrollTrigger = () => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
}

// Lifecycle
onMounted(() => {
  nextTick(() => {
    if (props.triggerOnScroll) {
      setupScrollTrigger()
    }
  })
})

onUnmounted(() => {
  cleanupScrollTrigger()
})

// Watch for changes
watch(() => props.triggerOnScroll, (newValue) => {
  if (newValue) {
    setupScrollTrigger()
  } else {
    cleanupScrollTrigger()
  }
})

// Expose methods for external control
defineExpose({
  startReveal,
  resetReveal,
  isRevealed: readonly(isRevealed),
  isRevealing: readonly(isRevealing)
})
</script>

<style scoped>
.box-reveal-container {
  position: relative;
}

.reveal-box {
  will-change: transform;
  backface-visibility: hidden;
}

.reveal-content {
  will-change: opacity;
}

/* Direction-specific origins */
.origin-top {
  transform-origin: top;
}

.origin-bottom {
  transform-origin: bottom;
}

.origin-left {
  transform-origin: left;
}

.origin-right {
  transform-origin: right;
}

.origin-center {
  transform-origin: center;
}

/* Enhanced reveal effects */
.revealing .reveal-box {
  box-shadow: 
    0 0 20px rgba(255, 215, 0, 0.3),
    0 0 40px rgba(255, 215, 0, 0.1);
}

/* Faction-specific glow effects */
.box-reveal-container[data-faction="empire"] .revealing .reveal-box {
  box-shadow: 
    0 0 20px rgba(255, 215, 0, 0.4),
    0 0 40px rgba(255, 215, 0, 0.2);
}

.box-reveal-container[data-faction="chaos"] .revealing .reveal-box {
  box-shadow: 
    0 0 20px rgba(139, 0, 0, 0.4),
    0 0 40px rgba(139, 0, 0, 0.2);
}

.box-reveal-container[data-faction="elves"] .revealing .reveal-box {
  box-shadow: 
    0 0 20px rgba(34, 139, 34, 0.4),
    0 0 40px rgba(34, 139, 34, 0.2);
}

/* Performance optimizations */
.reveal-box,
.reveal-content {
  transform: translate3d(0, 0, 0);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .reveal-box {
    transition-duration: 600ms !important;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .reveal-box,
  .reveal-content {
    transition-duration: 0.1s !important;
  }
}
</style>
