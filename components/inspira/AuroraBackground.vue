<template>
  <div 
    class="aurora-background"
    :style="{ 
      '--aurora-width': auroraWidth + 'px',
      '--aurora-height': auroraHeight + 'px'
    }"
  >
    <div 
      v-for="(color, index) in colors" 
      :key="index"
      class="aurora-layer"
      :style="{ 
        '--color': color,
        '--delay': index * 0.5 + 's',
        '--duration': (8 + index * 2) + 's'
      }"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  colors?: string[]
  auroraWidth?: number
  auroraHeight?: number
}

const props = withDefaults(defineProps<Props>(), {
  colors: () => ['#8b4513', '#a0522d', '#cd853f', '#daa520'],
  auroraWidth: 400,
  auroraHeight: 300
})
</script>

<style scoped>
.aurora-background {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.aurora-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    ellipse var(--aurora-width) var(--aurora-height) at 50% 50%,
    var(--color) 0%,
    transparent 70%
  );
  opacity: 0.3;
  animation: aurora-move var(--duration) ease-in-out infinite var(--delay);
  mix-blend-mode: screen;
}

@keyframes aurora-move {
  0%, 100% {
    transform: translateX(-20%) translateY(-10%) rotate(0deg);
  }
  25% {
    transform: translateX(20%) translateY(-20%) rotate(90deg);
  }
  50% {
    transform: translateX(10%) translateY(10%) rotate(180deg);
  }
  75% {
    transform: translateX(-10%) translateY(20%) rotate(270deg);
  }
}
</style>