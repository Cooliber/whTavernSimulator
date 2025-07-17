<template>
  <button 
    ref="buttonRef"
    class="ripple-button relative overflow-hidden rounded-lg px-6 py-3 font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
    :class="className"
    @click="handleClick"
  >
    <span class="relative z-10">
      <slot />
    </span>
    <span 
      v-for="ripple in ripples" 
      :key="ripple.id"
      class="ripple absolute rounded-full pointer-events-none"
      :style="ripple.style"
    />
  </button>
</template>

<script setup lang="ts">
interface Props {
  rippleColor?: string
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  rippleColor: 'rgba(255, 255, 255, 0.6)',
  className: ''
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

interface Ripple {
  id: number
  style: Record<string, string>
}

const buttonRef = ref<HTMLElement>()
const ripples = ref<Ripple[]>([])
let rippleId = 0

const handleClick = (event: MouseEvent) => {
  createRipple(event)
  emit('click', event)
}

const createRipple = (event: MouseEvent) => {
  if (!buttonRef.value) return
  
  const button = buttonRef.value
  const rect = button.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  const x = event.clientX - rect.left - size / 2
  const y = event.clientY - rect.top - size / 2
  
  const newRipple: Ripple = {
    id: rippleId++,
    style: {
      width: size + 'px',
      height: size + 'px',
      left: x + 'px',
      top: y + 'px',
      backgroundColor: props.rippleColor,
      transform: 'scale(0)',
      animation: 'ripple-animation 0.6s ease-out forwards'
    }
  }
  
  ripples.value.push(newRipple)
  
  // Remove ripple after animation
  setTimeout(() => {
    ripples.value = ripples.value.filter(r => r.id !== newRipple.id)
  }, 600)
}
</script>

<style scoped>
.ripple-button {
  position: relative;
}

@keyframes ripple-animation {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}
</style>