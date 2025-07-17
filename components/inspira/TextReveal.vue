<template>
  <span 
    ref="textRef"
    class="text-reveal"
    :class="className"
  >
    <span 
      v-for="(char, index) in characters" 
      :key="index"
      class="text-reveal-char"
      :style="char.style"
    >
      {{ char.char === ' ' ? '\u00A0' : char.char }}
    </span>
  </span>
</template>

<script setup lang="ts">
interface Props {
  text: string
  revealSpeed?: number
  className?: string
  trigger?: 'immediate' | 'hover' | 'visible'
}

const props = withDefaults(defineProps<Props>(), {
  revealSpeed: 50,
  className: '',
  trigger: 'immediate'
})

interface Character {
  char: string
  style: Record<string, string>
  revealed: boolean
}

const textRef = ref<HTMLElement>()
const characters = ref<Character[]>([])
const isRevealing = ref(false)

const initializeCharacters = () => {
  characters.value = props.text.split('').map((char, index) => ({
    char,
    revealed: false,
    style: {
      opacity: '0',
      transform: 'translateY(20px)',
      transition: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`,
      transitionDelay: '0s'
    }
  }))
}

const revealText = async () => {
  if (isRevealing.value) return
  
  isRevealing.value = true
  
  for (let i = 0; i < characters.value.length; i++) {
    const char = characters.value[i]
    
    char.style = {
      ...char.style,
      opacity: '1',
      transform: 'translateY(0)',
      transitionDelay: `${i * props.revealSpeed}ms`
    }
    
    char.revealed = true
    
    // Small delay between characters
    await new Promise(resolve => setTimeout(resolve, props.revealSpeed))
  }
  
  isRevealing.value = false
}

const resetText = () => {
  characters.value.forEach((char, index) => {
    char.style = {
      ...char.style,
      opacity: '0',
      transform: 'translateY(20px)',
      transitionDelay: '0s'
    }
    char.revealed = false
  })
}

const handleIntersection = (entries: IntersectionObserverEntry[]) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !isRevealing.value) {
      revealText()
    }
  })
}

onMounted(() => {
  initializeCharacters()
  
  if (props.trigger === 'immediate') {
    setTimeout(revealText, 100)
  } else if (props.trigger === 'visible' && textRef.value) {
    const observer = new IntersectionObserver(handleIntersection, {
      threshold: 0.1
    })
    observer.observe(textRef.value)
  }
})

watch(() => props.text, () => {
  initializeCharacters()
  if (props.trigger === 'immediate') {
    setTimeout(revealText, 100)
  }
})

// Expose methods for external control
defineExpose({
  reveal: revealText,
  reset: resetText
})
</script>

<style scoped>
.text-reveal {
  display: inline-block;
}

.text-reveal-char {
  display: inline-block;
  will-change: transform, opacity;
}
</style>