<template>
  <div 
    ref="containerRef"
    class="direction-aware-hover relative overflow-hidden"
    :class="className"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <!-- Default content -->
    <div class="content-default transition-all duration-300" :class="{ 'opacity-100': !isHovered, 'opacity-0': isHovered }">
      <slot name="content" />
    </div>
    
    <!-- Hover content -->
    <div 
      class="content-hover absolute inset-0 transition-all duration-300"
      :class="{ 'opacity-0': !isHovered, 'opacity-100': isHovered }"
      :style="hoverStyle"
    >
      <slot name="hover" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  className: ''
})

const containerRef = ref<HTMLElement>()
const isHovered = ref(false)
const direction = ref('')

const hoverStyle = computed(() => {
  if (!isHovered.value) {
    // Position hover content off-screen based on direction
    switch (direction.value) {
      case 'top':
        return { transform: 'translateY(-100%)' }
      case 'bottom':
        return { transform: 'translateY(100%)' }
      case 'left':
        return { transform: 'translateX(-100%)' }
      case 'right':
        return { transform: 'translateX(100%)' }
      default:
        return { transform: 'scale(0.8)', opacity: '0' }
    }
  }
  return { transform: 'translate(0, 0)', opacity: '1' }
})

const getDirection = (event: MouseEvent) => {
  if (!containerRef.value) return 'center'
  
  const rect = containerRef.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  
  const deltaX = x - centerX
  const deltaY = y - centerY
  
  if (Math.abs(deltaX) > Math.abs(deltaY)) {
    return deltaX > 0 ? 'right' : 'left'
  } else {
    return deltaY > 0 ? 'bottom' : 'top'
  }
}

const handleMouseEnter = (event: MouseEvent) => {
  direction.value = getDirection(event)
  isHovered.value = true
}

const handleMouseLeave = () => {
  isHovered.value = false
}
</script>

<style scoped>
.direction-aware-hover {
  cursor: pointer;
}

.content-hover {
  will-change: transform, opacity;
}
</style>