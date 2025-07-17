<template>
  <span 
    class="text-3d"
    :class="className"
    :style="textStyle"
  >
    {{ text }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  text: string
  depth?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  depth: 2,
  className: ''
})

const textStyle = computed(() => {
  const shadows = []
  for (let i = 1; i <= props.depth; i++) {
    shadows.push(`${i}px ${i}px 0 rgba(0, 0, 0, 0.3)`)
  }
  
  return {
    textShadow: shadows.join(', ')
  }
})
</script>

<style scoped>
.text-3d {
  display: inline-block;
  font-weight: bold;
  transform: perspective(500px) rotateX(15deg);
}
</style>