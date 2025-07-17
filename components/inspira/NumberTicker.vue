<template>
  <span 
    class="number-ticker"
    :class="className"
  >
    {{ displayValue }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  value: number
  duration?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  duration: 2000,
  className: ''
})

const displayValue = ref(0)

const animateToValue = (targetValue: number) => {
  const startValue = displayValue.value
  const difference = targetValue - startValue
  const startTime = Date.now()
  
  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / props.duration, 1)
    
    // Easing function (ease-out)
    const easeOut = 1 - Math.pow(1 - progress, 3)
    
    displayValue.value = Math.round(startValue + difference * easeOut)
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  
  animate()
}

onMounted(() => {
  animateToValue(props.value)
})

watch(() => props.value, (newValue) => {
  animateToValue(newValue)
})
</script>

<style scoped>
.number-ticker {
  font-variant-numeric: tabular-nums;
}
</style>