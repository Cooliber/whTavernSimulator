<template>
  <button 
    class="rainbow-button relative overflow-hidden rounded-lg px-6 py-3 font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
    :class="className"
    :style="buttonStyle"
    @click="$emit('click', $event)"
  >
    <span class="relative z-10">
      <slot />
    </span>
    <div class="rainbow-overlay absolute inset-0 opacity-80" />
  </button>
</template>

<script setup lang="ts">
interface Props {
  colors?: string[]
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  colors: () => ['#ff0000', '#ff7f00', '#ffff00', '#00ff00', '#0000ff', '#4b0082', '#9400d3'],
  className: ''
})

defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonStyle = computed(() => {
  const gradient = `linear-gradient(45deg, ${props.colors.join(', ')})`
  return {
    background: gradient,
    backgroundSize: '200% 200%',
    animation: 'rainbow-shift 3s ease infinite'
  }
})
</script>

<style scoped>
.rainbow-button {
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.rainbow-overlay {
  background: inherit;
  animation: inherit;
}

@keyframes rainbow-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>