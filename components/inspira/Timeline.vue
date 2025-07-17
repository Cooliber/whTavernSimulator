<template>
  <div class="timeline-container relative">
    <!-- Main timeline line -->
    <div class="timeline-line absolute left-6 top-0 w-0.5 h-full bg-gradient-to-b from-primary via-primary/50 to-transparent">
      <!-- Animated pulse -->
      <div class="timeline-pulse absolute top-0 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-primary rounded-full animate-pulse" />
      
      <!-- Flowing energy -->
      <div class="timeline-energy absolute top-0 left-1/2 transform -translate-x-1/2 w-1 h-8 bg-gradient-to-b from-primary to-transparent opacity-60">
        <div class="energy-flow w-full h-full bg-gradient-to-b from-primary to-transparent animate-flow" />
      </div>
    </div>
    
    <!-- Timeline items -->
    <div class="timeline-items space-y-8">
      <div 
        v-for="(item, index) in items" 
        :key="item.id || index"
        class="timeline-item relative pl-16 group"
        :class="{ 'animate-medieval-entrance': isVisible(index) }"
        :style="{ animationDelay: (index * 0.2) + 's' }"
      >
        <!-- Timeline node -->
        <div class="timeline-node absolute left-4 top-2 w-4 h-4 rounded-full border-2 border-primary bg-background z-10 transition-all duration-300 group-hover:scale-125 group-hover:bg-primary">
          <!-- Node glow effect -->
          <div class="node-glow absolute inset-0 rounded-full bg-primary opacity-0 group-hover:opacity-30 group-hover:scale-150 transition-all duration-300" />
          
          <!-- Ripple effect on hover -->
          <div class="node-ripple absolute inset-0 rounded-full border-2 border-primary opacity-0 group-hover:opacity-100 group-hover:scale-200 transition-all duration-500" />
        </div>
        
        <!-- Content card -->
        <div class="timeline-content bg-card border border-border rounded-lg p-4 shadow-lg hover:shadow-xl transition-all duration-300 group-hover:translate-x-2">
          <!-- Card glow effect -->
          <div class="card-glow absolute inset-0 rounded-lg bg-gradient-to-r from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          <!-- Content -->
          <div class="relative z-10">
            <slot name="item" :item="item" :index="index">
              <div class="space-y-2">
                <h3 class="font-medieval text-lg text-foreground">{{ item.title }}</h3>
                <p class="text-muted-foreground">{{ item.description }}</p>
                <span class="text-xs text-muted-foreground">{{ item.time }}</span>
              </div>
            </slot>
          </div>
          
          <!-- Decorative corner elements -->
          <div class="corner-decoration absolute top-2 right-2 w-2 h-2 border-t border-r border-primary/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          <div class="corner-decoration absolute bottom-2 left-2 w-2 h-2 border-b border-l border-primary/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        </div>
        
        <!-- Connecting line to next item -->
        <div 
          v-if="index < items.length - 1"
          class="connecting-line absolute left-6 top-8 w-0.5 h-8 bg-gradient-to-b from-primary/50 to-primary/20"
        />
      </div>
    </div>
    
    <!-- Timeline end marker -->
    <div class="timeline-end absolute left-4 bottom-0 w-4 h-4 rounded-full bg-gradient-to-br from-primary to-primary/50 shadow-lg">
      <div class="end-glow absolute inset-0 rounded-full bg-primary animate-ping opacity-30" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  items: any[]
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  className: ''
})

const visibleItems = ref(new Set<number>())

const isVisible = (index: number) => {
  return visibleItems.value.has(index)
}

const observeItems = () => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const index = parseInt(entry.target.getAttribute('data-index') || '0')
        if (entry.isIntersecting) {
          visibleItems.value.add(index)
        }
      })
    },
    { threshold: 0.1 }
  )
  
  // Observe timeline items
  nextTick(() => {
    const items = document.querySelectorAll('.timeline-item')
    items.forEach((item, index) => {
      item.setAttribute('data-index', index.toString())
      observer.observe(item)
    })
  })
}

onMounted(() => {
  observeItems()
  
  // Animate items in sequence
  props.items.forEach((_, index) => {
    setTimeout(() => {
      visibleItems.value.add(index)
    }, index * 200)
  })
})
</script>

<style scoped>
.timeline-container {
  padding: 2rem 0;
}

.energy-flow {
  animation: energy-flow 2s linear infinite;
}

.node-ripple {
  animation-delay: 0.2s;
}

@keyframes energy-flow {
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(400%);
    opacity: 0;
  }
}

@keyframes flow {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(100%);
  }
}

.timeline-item {
  opacity: 0;
  transform: translateX(-20px);
}

.timeline-item.animate-medieval-entrance {
  animation: medieval-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Responsive design */
@media (max-width: 768px) {
  .timeline-item {
    padding-left: 3rem;
  }
  
  .timeline-line {
    left: 1rem;
  }
  
  .timeline-node {
    left: 0.75rem;
  }
  
  .timeline-end {
    left: 0.75rem;
  }
}
</style>