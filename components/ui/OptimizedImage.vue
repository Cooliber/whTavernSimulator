<template>
  <div 
    :class="[
      'optimized-image-container',
      containerClass,
      { 'loading': isLoading, 'error': hasError }
    ]"
    :style="containerStyle"
  >
    <!-- Loading Placeholder -->
    <div 
      v-if="isLoading && showPlaceholder" 
      class="image-placeholder"
      :style="placeholderStyle"
    >
      <div class="placeholder-content">
        <div v-if="faction" class="faction-placeholder">
          <div class="faction-icon">{{ factionPlaceholder?.icon }}</div>
          <div class="faction-name font-medieval text-sm">{{ faction }}</div>
        </div>
        <div v-else class="loading-spinner">
          <div class="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full"></div>
        </div>
      </div>
    </div>

    <!-- Error Placeholder -->
    <div 
      v-else-if="hasError && showPlaceholder" 
      class="error-placeholder"
      :style="placeholderStyle"
    >
      <div class="error-content">
        <Icon name="image-off" class="w-8 h-8 text-muted-foreground mb-2" />
        <span class="text-xs text-muted-foreground font-medieval">Image unavailable</span>
      </div>
    </div>

    <!-- Actual Image -->
    <img
      v-show="!isLoading && !hasError"
      ref="imageRef"
      :src="optimizedSrc"
      :alt="alt"
      :title="title"
      :width="width"
      :height="height"
      :loading="loading"
      :srcset="srcset"
      :sizes="sizes"
      :decoding="decoding"
      :class="[
        'optimized-image',
        imageClass,
        { 'fade-in': fadeIn && imageLoaded }
      ]"
      :style="imageStyle"
      @load="handleImageLoad"
      @error="handleImageError"
    />

    <!-- Overlay Content -->
    <div v-if="$slots.overlay" class="image-overlay">
      <slot name="overlay" />
    </div>

    <!-- Caption -->
    <div v-if="caption" class="image-caption">
      <p class="text-xs text-muted-foreground font-sharp">{{ caption }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface OptimizedImageProps {
  src: string
  alt: string
  title?: string
  caption?: string
  width?: number
  height?: number
  loading?: 'lazy' | 'eager'
  srcset?: string
  sizes?: string
  decoding?: 'async' | 'sync' | 'auto'
  faction?: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
  category?: 'faction' | 'character' | 'atmosphere' | 'texture' | 'icon'
  containerClass?: string
  imageClass?: string
  showPlaceholder?: boolean
  fadeIn?: boolean
  aspectRatio?: string
  objectFit?: 'cover' | 'contain' | 'fill' | 'scale-down' | 'none'
  priority?: boolean
}

const props = withDefaults(defineProps<OptimizedImageProps>(), {
  loading: 'lazy',
  decoding: 'async',
  showPlaceholder: true,
  fadeIn: true,
  objectFit: 'cover',
  priority: false
})

const { createFactionPlaceholder } = useWarhammerImages()

// Reactive state
const imageRef = ref<HTMLImageElement>()
const isLoading = ref(true)
const hasError = ref(false)
const imageLoaded = ref(false)

// Computed properties
const optimizedSrc = computed(() => {
  // In a production app, you might transform the src for different CDNs or optimizations
  return props.src
})

const factionPlaceholder = computed(() => {
  return props.faction ? createFactionPlaceholder(props.faction, 'medium') : null
})

const containerStyle = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.aspectRatio) {
    styles.aspectRatio = props.aspectRatio
  } else if (props.width && props.height) {
    styles.aspectRatio = `${props.width} / ${props.height}`
  }
  
  return styles
})

const placeholderStyle = computed(() => {
  const styles: Record<string, string> = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '100%',
    minHeight: '120px'
  }
  
  if (factionPlaceholder.value) {
    styles.background = factionPlaceholder.value.background
    styles.color = factionPlaceholder.value.color
  } else {
    styles.background = 'rgb(var(--muted) / 0.1)'
  }
  
  return styles
})

const imageStyle = computed(() => {
  const styles: Record<string, string> = {
    width: '100%',
    height: '100%',
    objectFit: props.objectFit
  }
  
  return styles
})

// Event handlers
const handleImageLoad = () => {
  isLoading.value = false
  hasError.value = false
  imageLoaded.value = true
}

const handleImageError = () => {
  isLoading.value = false
  hasError.value = true
  imageLoaded.value = false
}

// Intersection Observer for lazy loading
const { observeImage } = useWarhammerImages().useImageLazyLoading()

onMounted(() => {
  if (imageRef.value && props.loading === 'lazy') {
    // Set up lazy loading
    imageRef.value.setAttribute('data-src', props.src)
    imageRef.value.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMSIgaGVpZ2h0PSIxIiB2aWV3Qm94PSIwIDAgMSAxIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9InRyYW5zcGFyZW50Ii8+PC9zdmc+'
    observeImage(imageRef.value)
  }
})

// Preload if priority
if (props.priority) {
  onMounted(async () => {
    try {
      const img = new Image()
      img.src = props.src
      await new Promise((resolve, reject) => {
        img.onload = resolve
        img.onerror = reject
      })
    } catch (error) {
      console.warn('Failed to preload priority image:', props.src)
    }
  })
}
</script>

<style scoped>
.optimized-image-container {
  @apply relative overflow-hidden rounded-lg;
  background-color: rgb(var(--muted) / 0.05);
}

.optimized-image {
  @apply transition-opacity duration-300;
  opacity: 0;
}

.optimized-image.fade-in {
  opacity: 1;
}

.image-placeholder,
.error-placeholder {
  @apply absolute inset-0 flex items-center justify-center;
  backdrop-filter: blur(2px);
}

.placeholder-content,
.error-content {
  @apply flex flex-col items-center justify-center text-center p-4;
}

.faction-placeholder {
  @apply flex flex-col items-center space-y-2;
}

.faction-icon {
  @apply text-2xl;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.faction-name {
  @apply capitalize;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.loading-spinner {
  @apply flex items-center justify-center;
}

.image-overlay {
  @apply absolute inset-0 flex items-center justify-center;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0, 0, 0, 0.1) 50%,
    rgba(0, 0, 0, 0.3) 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.optimized-image-container:hover .image-overlay {
  opacity: 1;
}

.image-caption {
  @apply absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/50 to-transparent;
}

/* Loading state animation */
.optimized-image-container.loading {
  @apply animate-pulse;
}

/* Error state styling */
.optimized-image-container.error {
  @apply border border-destructive/20;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .faction-icon {
    @apply text-xl;
  }
  
  .faction-name {
    @apply text-xs;
  }
  
  .image-caption {
    @apply p-1;
  }
  
  .image-caption p {
    @apply text-xs;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .optimized-image,
  .image-overlay,
  .optimized-image-container {
    @apply transition-none;
  }
  
  .optimized-image-container.loading {
    @apply animate-none;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .image-placeholder,
  .error-placeholder {
    @apply border border-foreground/20;
  }
  
  .image-caption {
    @apply bg-background/90 text-foreground;
  }
}
</style>
