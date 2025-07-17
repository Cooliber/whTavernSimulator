<template>
  <div 
    class="dock-container flex items-center justify-center p-2 rounded-2xl backdrop-blur-md"
    :style="{ gap: gap + 'px' }"
  >
    <div 
      v-for="(item, index) in items" 
      :key="item.id || index"
      class="dock-item transition-all duration-300 ease-out cursor-pointer"
      :style="getDockItemStyle(index)"
      @mouseenter="handleMouseEnter(index)"
      @mouseleave="handleMouseLeave"
    >
      <slot name="item" :item="item" :index="index">
        <div 
          class="w-full h-full rounded-xl bg-primary/10 hover:bg-primary/20 flex items-center justify-center transition-colors"
        >
          {{ item.label || item.name }}
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  items: any[]
  dockSize?: number
  magnification?: number
  gap?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  dockSize: 60,
  magnification: 1.5,
  gap: 8,
  className: ''
})

const hoveredIndex = ref<number | null>(null)

const handleMouseEnter = (index: number) => {
  hoveredIndex.value = index
}

const handleMouseLeave = () => {
  hoveredIndex.value = null
}

const getDockItemStyle = (index: number) => {
  const baseSize = props.dockSize
  let scale = 1
  
  if (hoveredIndex.value !== null) {
    const distance = Math.abs(index - hoveredIndex.value)
    if (distance === 0) {
      scale = props.magnification
    } else if (distance === 1) {
      scale = 1 + (props.magnification - 1) * 0.5
    } else if (distance === 2) {
      scale = 1 + (props.magnification - 1) * 0.25
    }
  }
  
  return {
    width: baseSize + 'px',
    height: baseSize + 'px',
    transform: `scale(${scale})`,
    zIndex: hoveredIndex.value === index ? 10 : 1
  }
}
</script>

<style scoped>
.dock-container {
  user-select: none;
}

.dock-item {
  transform-origin: bottom center;
}
</style>