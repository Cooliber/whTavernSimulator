<template>
  <div class="animated-testimonials relative" :class="className">
    <!-- Testimonial container -->
    <div class="testimonial-container relative overflow-hidden rounded-2xl">
      <!-- Background effects -->
      <div class="absolute inset-0 bg-gradient-to-br from-background/80 to-background/60 backdrop-blur-sm" />
      
      <!-- Current testimonial -->
      <div 
        v-if="currentTestimonial"
        class="testimonial-content relative z-10 p-8 transition-all duration-500"
        :key="currentIndex"
      >
        <slot 
          name="testimonial" 
          :testimonial="currentTestimonial" 
          :index="currentIndex"
        >
          <!-- Default testimonial layout -->
          <div class="space-y-6">
            <!-- Avatar and info -->
            <div class="flex items-center space-x-4">
              <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-primary/30">
                <img 
                  v-if="currentTestimonial.avatar"
                  :src="currentTestimonial.avatar" 
                  :alt="currentTestimonial.name"
                  class="w-full h-full object-cover"
                />
                <div 
                  v-else
                  class="w-full h-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center"
                >
                  <Icon name="user" class="w-8 h-8 text-primary" />
                </div>
              </div>
              
              <div>
                <HyperText 
                  :text="currentTestimonial.name"
                  class="text-xl font-medieval text-foreground"
                  :animation-duration="1000"
                />
                <p class="text-sm text-muted-foreground">{{ currentTestimonial.title }}</p>
              </div>
            </div>
            
            <!-- Testimonial text -->
            <div class="testimonial-text">
              <TextReveal 
                :text="currentTestimonial.content"
                class="text-lg text-foreground leading-relaxed"
                :reveal-speed="30"
                trigger="immediate"
              />
            </div>
            
            <!-- Rating if available -->
            <div v-if="currentTestimonial.rating" class="flex items-center space-x-1">
              <Icon 
                v-for="i in 5" 
                :key="i"
                name="star"
                class="w-4 h-4"
                :class="i <= currentTestimonial.rating ? 'text-yellow-400' : 'text-muted'"
              />
            </div>
          </div>
        </slot>
      </div>
      
      <!-- Navigation dots -->
      <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        <button 
          v-for="(testimonial, index) in testimonials" 
          :key="index"
          class="w-3 h-3 rounded-full transition-all duration-300"
          :class="index === currentIndex ? 'bg-primary scale-125' : 'bg-muted hover:bg-primary/50'"
          @click="goToTestimonial(index)"
        />
      </div>
      
      <!-- Navigation arrows -->
      <button 
        class="absolute left-4 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm border border-border hover:bg-background transition-all duration-300 flex items-center justify-center"
        @click="previousTestimonial"
      >
        <Icon name="chevron-left" class="w-5 h-5 text-foreground" />
      </button>
      
      <button 
        class="absolute right-4 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm border border-border hover:bg-background transition-all duration-300 flex items-center justify-center"
        @click="nextTestimonial"
      >
        <Icon name="chevron-right" class="w-5 h-5 text-foreground" />
      </button>
    </div>
    
    <!-- Progress bar -->
    <div v-if="autoPlay" class="mt-4 w-full h-1 bg-muted rounded-full overflow-hidden">
      <div 
        class="h-full bg-gradient-to-r from-primary to-primary/60 transition-all duration-100 ease-linear"
        :style="{ width: progressPercentage + '%' }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  testimonials: any[]
  autoPlay?: boolean
  autoPlayInterval?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  autoPlay: true,
  autoPlayInterval: 5000,
  className: ''
})

const currentIndex = ref(0)
const progressPercentage = ref(0)
let autoPlayTimer: NodeJS.Timeout | null = null
let progressTimer: NodeJS.Timeout | null = null

const currentTestimonial = computed(() => {
  return props.testimonials[currentIndex.value] || null
})

const goToTestimonial = (index: number) => {
  if (index >= 0 && index < props.testimonials.length) {
    currentIndex.value = index
    resetProgress()
  }
}

const nextTestimonial = () => {
  const nextIndex = (currentIndex.value + 1) % props.testimonials.length
  goToTestimonial(nextIndex)
}

const previousTestimonial = () => {
  const prevIndex = currentIndex.value === 0 
    ? props.testimonials.length - 1 
    : currentIndex.value - 1
  goToTestimonial(prevIndex)
}

const startAutoPlay = () => {
  if (!props.autoPlay || props.testimonials.length <= 1) return
  
  autoPlayTimer = setInterval(() => {
    nextTestimonial()
  }, props.autoPlayInterval)
}

const stopAutoPlay = () => {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
    autoPlayTimer = null
  }
}

const startProgress = () => {
  if (!props.autoPlay) return
  
  progressPercentage.value = 0
  const interval = 100 // Update every 100ms
  const increment = (interval / props.autoPlayInterval) * 100
  
  progressTimer = setInterval(() => {
    progressPercentage.value += increment
    if (progressPercentage.value >= 100) {
      progressPercentage.value = 100
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
    }
  }, interval)
}

const resetProgress = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
  progressPercentage.value = 0
  startProgress()
}

// Keyboard navigation
const handleKeydown = (event: KeyboardEvent) => {
  switch (event.key) {
    case 'ArrowLeft':
      previousTestimonial()
      break
    case 'ArrowRight':
      nextTestimonial()
      break
    case ' ':
      event.preventDefault()
      if (autoPlayTimer) {
        stopAutoPlay()
      } else {
        startAutoPlay()
      }
      break
  }
}

onMounted(() => {
  if (props.testimonials.length > 0) {
    startAutoPlay()
    startProgress()
  }
  
  // Add keyboard navigation
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  stopAutoPlay()
  if (progressTimer) {
    clearInterval(progressTimer)
  }
  window.removeEventListener('keydown', handleKeydown)
})

watch(() => props.testimonials, () => {
  currentIndex.value = 0
  resetProgress()
  stopAutoPlay()
  startAutoPlay()
})

// Pause on hover
const handleMouseEnter = () => {
  stopAutoPlay()
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const handleMouseLeave = () => {
  startAutoPlay()
  startProgress()
}
</script>

<style scoped>
.animated-testimonials {
  max-width: 800px;
}

.testimonial-container {
  min-height: 300px;
  position: relative;
}

.testimonial-content {
  animation: testimonial-fade-in 0.5s ease-out forwards;
}

@keyframes testimonial-fade-in {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hover effects */
.animated-testimonials:hover .testimonial-container {
  transform: scale(1.02);
  transition: transform 0.3s ease;
}

/* Responsive design */
@media (max-width: 768px) {
  .testimonial-content {
    padding: 1.5rem;
  }
  
  .testimonial-container {
    min-height: 250px;
  }
}
</style>