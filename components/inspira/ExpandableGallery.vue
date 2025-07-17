<template>
  <div 
    class="expandable-gallery grid transition-all duration-500"
    :style="gridStyle"
  >
    <div 
      v-for="(item, index) in items" 
      :key="item.id || index"
      class="gallery-item cursor-pointer transition-all duration-300"
      :class="{ 'expanded': expandedIndex === index }"
      @click="toggleExpand(index)"
    >
      <slot 
        name="item" 
        :item="item" 
        :index="index" 
        :isExpanded="expandedIndex === index"
      >
        <div class="w-full h-48 bg-muted rounded-lg flex items-center justify-center">
          {{ item.name || item.title || 'Item' }}
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  items: any[]
  gridCols?: number
  gap?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  gridCols: 3,
  gap: 4,
  className: ''
})

const expandedIndex = ref<number | null>(null)

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${props.gridCols}, 1fr)`,
  gap: `${props.gap * 0.25}rem`
}))

const toggleExpand = (index: number) => {
  expandedIndex.value = expandedIndex.value === index ? null : index
}
</script>

<style scoped>
.gallery-item.expanded {
  transform: scale(1.05);
  z-index: 10;
}

@media (max-width: 768px) {
  .expandable-gallery {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 480px) {
  .expandable-gallery {
    grid-template-columns: 1fr !important;
  }
}
</style>