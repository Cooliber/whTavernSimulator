<template>
  <span 
    ref="textRef"
    class="sparkles-text relative inline-block"
    :class="className"
  >
    {{ text }}
    <span 
      v-for="sparkle in sparkles" 
      :key="sparkle.id"
      class="sparkle absolute pointer-events-none"
      :style="sparkle.style"
    >
      ✨
    </span>
  </span>
</template>

<script setup lang="ts">
interface Props {
  text: string
  sparklesCount?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  sparklesCount: 10,
  className: ''
})

interface Sparkle {
  id: number
  style: Record<string, string>
}

const textRef = ref<HTMLElement>()
const sparkles = ref<Sparkle[]>([])
let sparkleId = 0

const generateSparkles = () => {
  if (!textRef.value) return
  
  const rect = textRef.value.getBoundingClientRect()
  
  sparkles.value = Array.from({ length: props.sparklesCount }, () => ({
    id: sparkleId++,
    style: {
      left: Math.random() * 100 + '%',
      top: Math.random() * 100 + '%',
      fontSize: (0.5 + Math.random() * 0.5) + 'em',
      animationDelay: Math.random() * 2 + 's',
      animationDuration: (1 + Math.random() * 2) + 's'
    }
  }))
}

const regenerateSparkles = () => {
  generateSparkles()
  setTimeout(regenerateSparkles, 3000 + Math.random() * 2000)
}

onMounted(() => {
  generateSparkles()
  regenerateSparkles()
})

watch(() => props.text, generateSparkles)
watch(() => props.sparklesCount, generateSparkles)
</script>

<style scoped>
.sparkles-text {
  position: relative;
}

.sparkle {
  animation: sparkle-twinkle linear infinite;
  opacity: 0;
}

@keyframes sparkle-twinkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0) rotate(0deg);
  }
  50% {
    opacity: 1;
    transform: scale(1) rotate(180deg);
  }
}
</style>