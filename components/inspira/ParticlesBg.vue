<template>
  <div class="particles-container">
    <div 
      v-for="particle in particles" 
      :key="particle.id"
      class="particle"
      :style="particle.style"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  particleCount?: number
  particleColor?: string
  particleSize?: number
  animationSpeed?: number
}

const props = withDefaults(defineProps<Props>(), {
  particleCount: 50,
  particleColor: '#ffd700',
  particleSize: 2,
  animationSpeed: 0.5
})

interface Particle {
  id: number
  style: Record<string, string>
}

const particles = ref<Particle[]>([])

const generateParticles = () => {
  particles.value = Array.from({ length: props.particleCount }, (_, i) => ({
    id: i,
    style: {
      left: Math.random() * 100 + '%',
      top: Math.random() * 100 + '%',
      width: props.particleSize + 'px',
      height: props.particleSize + 'px',
      backgroundColor: props.particleColor,
      animationDelay: Math.random() * 4 + 's',
      animationDuration: (2 + Math.random() * 3) / props.animationSpeed + 's'
    }
  }))
}

onMounted(() => {
  generateParticles()
})

watch(() => props.particleCount, generateParticles)
watch(() => props.particleColor, generateParticles)
watch(() => props.particleSize, generateParticles)
</script>

<style scoped>
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.7;
  animation: float-particle linear infinite;
}

@keyframes float-particle {
  0% {
    transform: translateY(100vh) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.7;
  }
  90% {
    opacity: 0.7;
  }
  100% {
    transform: translateY(-10vh) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}
</style>