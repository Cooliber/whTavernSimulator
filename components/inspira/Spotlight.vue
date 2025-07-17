<template>
  <div 
    ref="containerRef"
    class="spotlight-container relative overflow-hidden"
    :class="className"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Content -->
    <div class="spotlight-content relative z-10">
      <slot />
    </div>
    
    <!-- Spotlight effect -->
    <div 
      class="spotlight-effect absolute inset-0 pointer-events-none transition-opacity duration-300"
      :style="spotlightStyle"
    >
      <!-- Main spotlight -->
      <div 
        class="spotlight-main absolute rounded-full transition-all duration-200 ease-out"
        :style="mainSpotlightStyle"
      />
      
      <!-- Secondary glow -->
      <div 
        class="spotlight-glow absolute rounded-full transition-all duration-300 ease-out"
        :style="glowStyle"
      />
      
      <!-- Particle effects -->
      <div 
        v-for="particle in particles" 
        :key="particle.id"
        class="spotlight-particle absolute rounded-full"
        :style="particle.style"
      />
    </div>
    
    <!-- Border highlight -->
    <div 
      class="spotlight-border absolute inset-0 rounded-inherit border-2 border-transparent transition-all duration-300"
      :class="{ 'border-primary/30': isHovered }"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  spotlightColor?: string
  spotlightSize?: number
  intensity?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  spotlightColor: 'rgba(255, 215, 0, 0.3)',
  spotlightSize: 200,
  intensity: 0.8,
  className: ''
})

interface Particle {
  id: number
  style: Record<string, string>
}

const containerRef = ref<HTMLElement>()
const mouseX = ref(0)
const mouseY = ref(0)
const isHovered = ref(false)
const particles = ref<Particle[]>([])
let particleId = 0

const spotlightStyle = computed(() => ({
  opacity: isHovered.value ? props.intensity : 0
}))

const mainSpotlightStyle = computed(() => ({
  left: mouseX.value - props.spotlightSize / 2 + 'px',
  top: mouseY.value - props.spotlightSize / 2 + 'px',
  width: props.spotlightSize + 'px',
  height: props.spotlightSize + 'px',
  background: `radial-gradient(circle, ${props.spotlightColor} 0%, transparent 70%)`,
  filter: 'blur(1px)'
}))

const glowStyle = computed(() => ({
  left: mouseX.value - props.spotlightSize + 'px',
  top: mouseY.value - props.spotlightSize + 'px',
  width: props.spotlightSize * 2 + 'px',
  height: props.spotlightSize * 2 + 'px',
  background: `radial-gradient(circle, ${props.spotlightColor.replace('0.3', '0.1')} 0%, transparent 80%)`,
  filter: 'blur(3px)'
}))

const handleMouseMove = (event: MouseEvent) => {
  if (!containerRef.value) return
  
  const rect = containerRef.value.getBoundingClientRect()
  mouseX.value = event.clientX - rect.left
  mouseY.value = event.clientY - rect.top
  isHovered.value = true
  
  // Create particles occasionally
  if (Math.random() < 0.1) {
    createParticle()
  }
}

const handleMouseLeave = () => {
  isHovered.value = false
  particles.value = []
}

const createParticle = () => {
  const particle: Particle = {
    id: particleId++,
    style: {
      left: mouseX.value + (Math.random() - 0.5) * 40 + 'px',
      top: mouseY.value + (Math.random() - 0.5) * 40 + 'px',
      width: (2 + Math.random() * 4) + 'px',
      height: (2 + Math.random() * 4) + 'px',
      background: props.spotlightColor.replace('0.3', '0.8'),
      animation: `particle-float ${1 + Math.random()}s ease-out forwards`,
      animationDelay: Math.random() * 0.2 + 's'
    }
  }
  
  particles.value.push(particle)
  
  // Remove particle after animation
  setTimeout(() => {
    particles.value = particles.value.filter(p => p.id !== particle.id)
  }, 1500)
}
</script>

<style scoped>
.spotlight-container {
  cursor: pointer;
}

.spotlight-effect {
  mix-blend-mode: screen;
}

@keyframes particle-float {
  0% {
    opacity: 0;
    transform: scale(0) translateY(0);
  }
  50% {
    opacity: 1;
    transform: scale(1) translateY(-10px);
  }
  100% {
    opacity: 0;
    transform: scale(0) translateY(-20px);
  }
}

/* Enhanced glow effect */
.spotlight-main {
  box-shadow: 
    0 0 20px rgba(255, 215, 0, 0.4),
    0 0 40px rgba(255, 215, 0, 0.2),
    inset 0 0 20px rgba(255, 215, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .spotlight-main,
  .spotlight-glow {
    transform: scale(0.7);
  }
}
</style>