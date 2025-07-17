<template>
  <div 
    ref="containerRef"
    class="lens-container relative overflow-hidden cursor-none"
    :class="className"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    @mouseenter="handleMouseEnter"
  >
    <!-- Original content -->
    <div class="lens-content">
      <slot />
    </div>
    
    <!-- Lens effect -->
    <div 
      v-if="isActive"
      class="lens-effect absolute pointer-events-none z-20 rounded-full border-4 border-primary/50 shadow-2xl transition-all duration-200"
      :style="lensStyle"
    >
      <!-- Magnified content -->
      <div 
        class="lens-magnified absolute inset-0 rounded-full overflow-hidden"
        :style="magnifiedStyle"
      >
        <div 
          class="magnified-content"
          :style="contentStyle"
        >
          <slot name="magnified">
            <slot />
          </slot>
        </div>
      </div>
      
      <!-- Lens border glow -->
      <div class="lens-glow absolute inset-0 rounded-full border-2 border-primary/30 animate-pulse" />
      
      <!-- Lens reflection -->
      <div class="lens-reflection absolute top-2 left-2 w-4 h-4 bg-white/30 rounded-full blur-sm" />
      
      <!-- Crosshair -->
      <div class="lens-crosshair absolute inset-0 flex items-center justify-center">
        <div class="crosshair-h absolute w-full h-px bg-primary/40" />
        <div class="crosshair-v absolute h-full w-px bg-primary/40" />
      </div>
    </div>
    
    <!-- Lens cursor -->
    <div 
      v-if="isActive"
      class="lens-cursor absolute pointer-events-none z-30 w-2 h-2 bg-primary rounded-full shadow-lg"
      :style="cursorStyle"
    >
      <div class="cursor-glow absolute inset-0 bg-primary rounded-full animate-ping opacity-50" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  lensSize?: number
  magnification?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  lensSize: 150,
  magnification: 2,
  className: ''
})

const containerRef = ref<HTMLElement>()
const mouseX = ref(0)
const mouseY = ref(0)
const isActive = ref(false)

const lensStyle = computed(() => ({
  left: mouseX.value - props.lensSize / 2 + 'px',
  top: mouseY.value - props.lensSize / 2 + 'px',
  width: props.lensSize + 'px',
  height: props.lensSize + 'px',
  background: 'rgba(0, 0, 0, 0.1)',
  backdropFilter: 'blur(1px)'
}))

const magnifiedStyle = computed(() => ({
  transform: `scale(${props.magnification})`,
  transformOrigin: 'center center'
}))

const contentStyle = computed(() => {
  const offsetX = -(mouseX.value * props.magnification - props.lensSize / 2)
  const offsetY = -(mouseY.value * props.magnification - props.lensSize / 2)
  
  return {
    transform: `translate(${offsetX}px, ${offsetY}px)`,
    filter: 'brightness(1.2) contrast(1.1) saturate(1.2)'
  }
})

const cursorStyle = computed(() => ({
  left: mouseX.value - 4 + 'px',
  top: mouseY.value - 4 + 'px'
}))

const handleMouseMove = (event: MouseEvent) => {
  if (!containerRef.value) return
  
  const rect = containerRef.value.getBoundingClientRect()
  mouseX.value = event.clientX - rect.left
  mouseY.value = event.clientY - rect.top
}

const handleMouseEnter = () => {
  isActive.value = true
}

const handleMouseLeave = () => {
  isActive.value = false
}
</script>

<style scoped>
.lens-container {
  position: relative;
}

.lens-effect {
  background: 
    radial-gradient(circle at center, rgba(255, 215, 0, 0.1) 0%, transparent 70%),
    conic-gradient(from 0deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1), rgba(255, 215, 0, 0.1));
  box-shadow: 
    0 0 20px rgba(255, 215, 0, 0.3),
    0 0 40px rgba(255, 215, 0, 0.1),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
}

.lens-glow {
  animation: lens-pulse 2s ease-in-out infinite;
}

.lens-reflection {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, transparent 50%);
}

.crosshair-h,
.crosshair-v {
  opacity: 0.6;
}

.magnified-content {
  width: 100%;
  height: 100%;
  position: relative;
}

@keyframes lens-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.05);
  }
}

/* Disable text selection in lens area */
.lens-container {
  user-select: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .lens-effect {
    transform: scale(0.8);
  }
}
</style>