<template>
  <div 
    ref="cardRef"
    class="card-3d transition-all duration-300 ease-out"
    :class="className"
    :style="cardStyle"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  rotationIntensity?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  rotationIntensity: 15,
  className: ''
})

const cardRef = ref<HTMLElement>()
const rotateX = ref(0)
const rotateY = ref(0)

const cardStyle = computed(() => ({
  transform: `perspective(1000px) rotateX(${rotateX.value}deg) rotateY(${rotateY.value}deg)`,
  transformStyle: 'preserve-3d'
}))

const handleMouseMove = (event: MouseEvent) => {
  if (!cardRef.value) return
  
  const rect = cardRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  
  const mouseX = event.clientX - centerX
  const mouseY = event.clientY - centerY
  
  const rotateXValue = (mouseY / (rect.height / 2)) * props.rotationIntensity
  const rotateYValue = (mouseX / (rect.width / 2)) * props.rotationIntensity
  
  rotateX.value = -rotateXValue
  rotateY.value = rotateYValue
}

const handleMouseLeave = () => {
  rotateX.value = 0
  rotateY.value = 0
}
</script>

<style scoped>
.card-3d {
  cursor: pointer;
  will-change: transform;
}
</style>