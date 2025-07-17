<template>
  <span 
    ref="textRef"
    class="hyper-text"
    :class="className"
  >
    {{ displayText }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  text: string
  animationDuration?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  animationDuration: 2000,
  className: ''
})

const textRef = ref<HTMLElement>()
const displayText = ref('')
const isAnimating = ref(false)

const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'

const animateText = () => {
  if (isAnimating.value) return
  
  isAnimating.value = true
  const targetText = props.text
  const duration = props.animationDuration
  const steps = 20
  const stepDuration = duration / steps
  
  let currentStep = 0
  
  const animate = () => {
    if (currentStep >= steps) {
      displayText.value = targetText
      isAnimating.value = false
      return
    }
    
    const progress = currentStep / steps
    const revealedLength = Math.floor(targetText.length * progress)
    
    let result = targetText.slice(0, revealedLength)
    
    // Add random characters for unrevealed part
    for (let i = revealedLength; i < targetText.length; i++) {
      if (targetText[i] === ' ') {
        result += ' '
      } else {
        result += characters[Math.floor(Math.random() * characters.length)]
      }
    }
    
    displayText.value = result
    currentStep++
    
    setTimeout(animate, stepDuration)
  }
  
  animate()
}

onMounted(() => {
  // Start animation after a short delay
  setTimeout(animateText, 100)
})

watch(() => props.text, () => {
  animateText()
})
</script>

<style scoped>
.hyper-text {
  font-family: 'Courier New', monospace;
  letter-spacing: 0.1em;
}
</style>