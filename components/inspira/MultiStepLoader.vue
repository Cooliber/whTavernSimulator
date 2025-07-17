<template>
  <div class="multi-step-loader fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-md">
    <!-- Background Effects -->
    <AuroraBackground 
      class="absolute inset-0 opacity-30"
      :colors="factionColors"
    />
    
    <!-- Main Loader Container -->
    <BorderBeam 
      class="relative bg-card/90 backdrop-blur-md rounded-2xl p-8 max-w-md w-full mx-4"
      :border-width="3"
      :color-from="factionTheme.primary"
      :color-to="factionTheme.secondary"
    >
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
          <Icon 
            :name="currentStepData?.icon || 'loader'" 
            class="w-8 h-8 text-primary animate-spin"
          />
        </div>
        
        <HyperText 
          text="Tavern Loading"
          class="text-2xl font-medieval text-foreground mb-2"
          :animation-duration="1000"
        />
        
        <p class="text-sm text-muted-foreground">
          Preparing your Warhammer experience...
        </p>
      </div>
      
      <!-- Progress Bar -->
      <div class="mb-6">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medieval text-foreground">Progress</span>
          <span class="text-sm text-muted-foreground">{{ currentStep + 1 }}/{{ steps.length }}</span>
        </div>
        
        <div class="w-full h-3 bg-muted rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r transition-all duration-500 ease-out"
            :class="factionGradient"
            :style="{ width: progressPercentage + '%' }"
          >
            <!-- Progress shimmer effect -->
            <div class="w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
          </div>
        </div>
      </div>
      
      <!-- Current Step Display -->
      <div v-if="currentStepData" class="text-center mb-6">
        <div class="mb-4">
          <SparklesText 
            :text="currentStepData.title"
            class="text-lg font-medieval text-foreground"
            :sparkles-count="8"
          />
        </div>
        
        <TextReveal 
          :text="currentStepData.description"
          class="text-sm text-muted-foreground"
          :reveal-speed="50"
          trigger="immediate"
        />
      </div>
      
      <!-- Step Indicators -->
      <div class="flex justify-center space-x-2 mb-6">
        <div 
          v-for="(step, index) in steps" 
          :key="step.id"
          class="w-3 h-3 rounded-full transition-all duration-300"
          :class="{
            'bg-primary scale-110': index === currentStep,
            'bg-primary/50': index < currentStep,
            'bg-muted': index > currentStep
          }"
        />
      </div>
      
      <!-- Loading Animation -->
      <div class="flex justify-center">
        <div class="relative">
          <!-- Spinning runes -->
          <div class="w-12 h-12 relative">
            <div 
              v-for="i in 6" 
              :key="i"
              class="absolute w-2 h-2 bg-primary rounded-full"
              :style="{
                transform: `rotate(${i * 60}deg) translateY(-20px)`,
                animationDelay: `${i * 0.1}s`
              }"
              :class="'animate-pulse'"
            />
          </div>
          
          <!-- Center glow -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-4 h-4 bg-primary rounded-full animate-ping opacity-60" />
          </div>
        </div>
      </div>
      
      <!-- Skip Button (if enabled) -->
      <div v-if="allowSkip" class="mt-6 text-center">
        <RippleButton 
          class="text-sm text-muted-foreground hover:text-foreground transition-colors"
          :ripple-color="factionTheme.primary"
          @click="skipLoading"
        >
          Skip Loading
        </RippleButton>
      </div>
    </BorderBeam>
    
    <!-- Audio feedback -->
    <audio 
      v-if="enableAudio"
      ref="audioRef"
      :volume="0.3"
      preload="auto"
    />
  </div>
</template>

<script setup lang="ts">
interface LoadingStep {
  id: string
  title: string
  description: string
  icon: string
  duration: number
  faction?: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
  audioSrc?: string
}

interface Props {
  steps: LoadingStep[]
  autoProgress?: boolean
  allowSkip?: boolean
  enableAudio?: boolean
  onComplete?: () => void
  onStepChange?: (step: LoadingStep, index: number) => void
}

const props = withDefaults(defineProps<Props>(), {
  autoProgress: true,
  allowSkip: false,
  enableAudio: true
})

const emit = defineEmits<{
  complete: []
  stepChange: [step: LoadingStep, index: number]
  skip: []
}>()

// Reactive state
const currentStep = ref(0)
const isLoading = ref(true)
const audioRef = ref<HTMLAudioElement>()

// Computed properties
const currentStepData = computed(() => props.steps[currentStep.value])
const progressPercentage = computed(() => ((currentStep.value + 1) / props.steps.length) * 100)

// Faction theming
const factionTheme = computed(() => {
  const faction = currentStepData.value?.faction || 'empire'
  const themes = {
    empire: { primary: '#ffd700', secondary: '#b8860b' },
    chaos: { primary: '#8b0000', secondary: '#dc143c' },
    elves: { primary: '#228b22', secondary: '#32cd32' },
    dwarfs: { primary: '#daa520', secondary: '#b8860b' },
    undead: { primary: '#800080', secondary: '#4b0082' },
    orcs: { primary: '#228b22', secondary: '#006400' }
  }
  return themes[faction]
})

const factionColors = computed(() => [
  factionTheme.value.primary,
  factionTheme.value.secondary,
  '#2c1810'
])

const factionGradient = computed(() => {
  const faction = currentStepData.value?.faction || 'empire'
  return `from-${faction === 'empire' ? 'yellow' : faction === 'chaos' ? 'red' : 'green'}-600 to-${faction === 'empire' ? 'yellow' : faction === 'chaos' ? 'red' : 'green'}-400`
})

// Methods
const nextStep = () => {
  if (currentStep.value < props.steps.length - 1) {
    currentStep.value++
    emit('stepChange', currentStepData.value, currentStep.value)
    props.onStepChange?.(currentStepData.value, currentStep.value)
    
    if (props.enableAudio && currentStepData.value.audioSrc && audioRef.value) {
      audioRef.value.src = currentStepData.value.audioSrc
      audioRef.value.play().catch(() => {
        // Handle audio play failure silently
      })
    }
  } else {
    completeLoading()
  }
}

const completeLoading = () => {
  isLoading.value = false
  emit('complete')
  props.onComplete?.()
}

const skipLoading = () => {
  emit('skip')
  completeLoading()
}

// Auto-progress logic
let progressTimer: NodeJS.Timeout | null = null

const startAutoProgress = () => {
  if (!props.autoProgress || !currentStepData.value) return
  
  progressTimer = setTimeout(() => {
    nextStep()
    if (currentStep.value < props.steps.length) {
      startAutoProgress()
    }
  }, currentStepData.value.duration)
}

// Lifecycle
onMounted(() => {
  if (props.steps.length > 0) {
    emit('stepChange', currentStepData.value, currentStep.value)
    props.onStepChange?.(currentStepData.value, currentStep.value)
    startAutoProgress()
  }
})

onUnmounted(() => {
  if (progressTimer) {
    clearTimeout(progressTimer)
  }
  if (audioRef.value) {
    audioRef.value.pause()
  }
})

// Expose methods for external control
defineExpose({
  nextStep,
  skipLoading,
  currentStep: readonly(currentStep),
  isLoading: readonly(isLoading)
})
</script>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .multi-step-loader .max-w-md {
    max-width: 90vw;
  }
}
</style>
