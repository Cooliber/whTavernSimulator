<template>
  <button 
    class="shimmer-button relative overflow-hidden rounded-lg px-6 py-3 font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
    :class="className"
    @click="$emit('click', $event)"
  >
    <span class="relative z-10">
      <slot />
    </span>
    <div 
      class="shimmer-overlay absolute inset-0 -translate-x-full transition-transform duration-1000 ease-out"
      :style="{ background: `linear-gradient(90deg, transparent, ${shimmerColor}, transparent)` }"
    />
  </button>
</template>

<script setup lang="ts">
interface Props {
  shimmerColor?: string
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  shimmerColor: 'rgba(255, 255, 255, 0.3)',
  className: ''
})

defineEmits<{
  click: [event: MouseEvent]
}>()

const shimmerRef = ref<HTMLElement>()

const triggerShimmer = () => {
  const overlay = shimmerRef.value?.querySelector('.shimmer-overlay') as HTMLElement
  if (overlay) {
    overlay.style.transform = 'translateX(100%)'
    setTimeout(() => {
      overlay.style.transform = 'translateX(-100%)'
    }, 1000)
  }
}

onMounted(() => {
  // Trigger shimmer effect periodically
  setInterval(triggerShimmer, 3000)
})
</script>

<style scoped>
.shimmer-button:hover .shimmer-overlay {
  transform: translateX(100%);
}

.shimmer-overlay {
  opacity: 0.6;
  width: 100%;
  height: 100%;
}
</style>