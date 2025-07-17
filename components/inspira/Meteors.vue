<template>
  <div class="meteors-container fixed inset-0 pointer-events-none overflow-hidden">
    <!-- Canvas-based meteors for better performance -->
    <canvas
      ref="canvasRef"
      class="absolute inset-0 w-full h-full"
      :width="canvasSize.width"
      :height="canvasSize.height"
    />

    <!-- Fallback DOM meteors for older browsers -->
    <div v-if="!canvasSupported" class="dom-meteors">
      <div
        v-for="meteor in activeMeteors"
        :key="meteor.id"
        class="meteor absolute"
        :style="meteor.style"
      >
        <!-- Meteor head -->
        <div class="meteor-head w-2 h-2 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full shadow-lg">
          <!-- Core glow -->
          <div class="meteor-core absolute inset-0 bg-white rounded-full scale-50 opacity-80" />
        </div>

        <!-- Meteor tail -->
        <div class="meteor-tail absolute top-1/2 left-full transform -translate-y-1/2 h-0.5 bg-gradient-to-r from-yellow-400/80 via-orange-500/60 to-transparent"
             :style="{ width: meteor.tailLength + 'px' }" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  meteorCount?: number
  meteorSpeed?: number
  meteorSize?: number
  enableCanvas?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  meteorCount: 8,
  meteorSpeed: 1,
  meteorSize: 1,
  enableCanvas: true
})

interface Sparkle {
  x: number
  y: number
  opacity: number
  size: number
  life: number
}

interface Meteor {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  size: number
  tailLength: number
  opacity: number
  life: number
  maxLife: number
  sparkles: Sparkle[]
  style?: Record<string, string> // For DOM fallback
}

// Reactive state
const canvasRef = ref<HTMLCanvasElement>()
const canvasSupported = ref(true)
const canvasSize = ref({ width: 0, height: 0 })
const activeMeteors = ref<Meteor[]>([])
const meteorPool = ref<Meteor[]>([])
let meteorIdCounter = 0
let animationFrame: number | null = null
let ctx: CanvasRenderingContext2D | null = null

// Object pooling for performance
const createMeteor = (): Meteor => {
  const pooled = meteorPool.value.pop()
  if (pooled) {
    return resetMeteor(pooled)
  }
  return generateNewMeteor()
}

const generateNewMeteor = (): Meteor => {
  const size = props.meteorSize * (0.8 + Math.random() * 0.4)
  const startX = Math.random() * (canvasSize.value.width + 200) - 100
  const startY = -50
  const angle = -45 + Math.random() * 30
  const speed = (2 + Math.random() * 3) * props.meteorSpeed
  const vx = Math.cos(angle * Math.PI / 180) * speed
  const vy = Math.sin(angle * Math.PI / 180) * speed
  const maxLife = 120 + Math.random() * 60

  return {
    id: meteorIdCounter++,
    x: startX,
    y: startY,
    vx,
    vy,
    size,
    tailLength: 40 + Math.random() * 40,
    opacity: 0.8 + Math.random() * 0.2,
    life: 0,
    maxLife,
    sparkles: []
  }
}

const resetMeteor = (meteor: Meteor): Meteor => {
  const size = props.meteorSize * (0.8 + Math.random() * 0.4)
  const startX = Math.random() * (canvasSize.value.width + 200) - 100
  const angle = -45 + Math.random() * 30
  const speed = (2 + Math.random() * 3) * props.meteorSpeed

  meteor.x = startX
  meteor.y = -50
  meteor.vx = Math.cos(angle * Math.PI / 180) * speed
  meteor.vy = Math.sin(angle * Math.PI / 180) * speed
  meteor.size = size
  meteor.opacity = 0.8 + Math.random() * 0.2
  meteor.life = 0
  meteor.maxLife = 120 + Math.random() * 60
  meteor.sparkles = []

  return meteor
}

const recycleMeteor = (meteor: Meteor) => {
  const index = activeMeteors.value.indexOf(meteor)
  if (index > -1) {
    activeMeteors.value.splice(index, 1)
    meteorPool.value.push(meteor)
  }
}

// Canvas rendering
const initCanvas = () => {
  if (!canvasRef.value || !props.enableCanvas) {
    canvasSupported.value = false
    return
  }

  try {
    ctx = canvasRef.value.getContext('2d')
    if (!ctx) {
      canvasSupported.value = false
      return
    }

    updateCanvasSize()
    startAnimation()
  } catch (error) {
    console.warn('Canvas not supported, falling back to DOM meteors')
    canvasSupported.value = false
  }
}

const updateCanvasSize = () => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  canvasSize.value = {
    width: window.innerWidth,
    height: window.innerHeight
  }

  canvasRef.value.width = canvasSize.value.width
  canvasRef.value.height = canvasSize.value.height
}

const drawMeteor = (meteor: Meteor) => {
  if (!ctx) return

  const fadeOpacity = meteor.life < 20 ? meteor.life / 20 :
                     meteor.life > meteor.maxLife - 20 ? (meteor.maxLife - meteor.life) / 20 : 1

  ctx.save()
  ctx.globalAlpha = meteor.opacity * fadeOpacity

  // Draw meteor tail
  const gradient = ctx.createLinearGradient(
    meteor.x, meteor.y,
    meteor.x - meteor.vx * meteor.tailLength / 10, meteor.y - meteor.vy * meteor.tailLength / 10
  )
  gradient.addColorStop(0, '#ffd700')
  gradient.addColorStop(0.5, '#ff8c00')
  gradient.addColorStop(1, 'transparent')

  ctx.strokeStyle = gradient
  ctx.lineWidth = meteor.size * 2
  ctx.lineCap = 'round'
  ctx.beginPath()
  ctx.moveTo(meteor.x, meteor.y)
  ctx.lineTo(meteor.x - meteor.vx * meteor.tailLength / 10, meteor.y - meteor.vy * meteor.tailLength / 10)
  ctx.stroke()

  // Draw meteor head
  const headGradient = ctx.createRadialGradient(meteor.x, meteor.y, 0, meteor.x, meteor.y, meteor.size * 3)
  headGradient.addColorStop(0, '#ffffff')
  headGradient.addColorStop(0.3, '#ffd700')
  headGradient.addColorStop(0.7, '#ff8c00')
  headGradient.addColorStop(1, 'transparent')

  ctx.fillStyle = headGradient
  ctx.beginPath()
  ctx.arc(meteor.x, meteor.y, meteor.size * 3, 0, Math.PI * 2)
  ctx.fill()

  ctx.restore()
}

const updateMeteor = (meteor: Meteor) => {
  meteor.x += meteor.vx
  meteor.y += meteor.vy
  meteor.life++

  // Check if meteor is off screen or expired
  if (meteor.y > canvasSize.value.height + 50 ||
      meteor.x < -100 ||
      meteor.life >= meteor.maxLife) {
    recycleMeteor(meteor)
  }
}

const animate = () => {
  if (!ctx || !canvasSupported.value) return

  // Clear canvas
  ctx.clearRect(0, 0, canvasSize.value.width, canvasSize.value.height)

  // Add new meteors if needed
  while (activeMeteors.value.length < props.meteorCount) {
    activeMeteors.value.push(createMeteor())
  }

  // Update and draw meteors
  for (let i = activeMeteors.value.length - 1; i >= 0; i--) {
    const meteor = activeMeteors.value[i]
    updateMeteor(meteor)
    if (activeMeteors.value.includes(meteor)) {
      drawMeteor(meteor)
    }
  }

  animationFrame = requestAnimationFrame(animate)
}

const startAnimation = () => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
  animate()
}

const stopAnimation = () => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
    animationFrame = null
  }
}

// Fallback DOM meteor generation for older browsers
const generateDOMMeteors = () => {
  if (canvasSupported.value) return

  activeMeteors.value = Array.from({ length: props.meteorCount }, () => {
    const meteor = createMeteor()
    // Add DOM-specific style properties
    meteor.style = {
      left: meteor.x + 'px',
      top: meteor.y + 'px',
      transform: `rotate(${Math.atan2(meteor.vy, meteor.vx) * 180 / Math.PI}deg) scale(${meteor.size})`,
      animation: `meteor-fall ${meteor.maxLife / 60}s linear forwards`,
      animationDelay: Math.random() * 2 + 's'
    }
    return meteor
  })
}

// Lifecycle and event handlers
const handleResize = () => {
  updateCanvasSize()
}

onMounted(() => {
  nextTick(() => {
    initCanvas()
    if (!canvasSupported.value) {
      generateDOMMeteors()
    }
    window.addEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  stopAnimation()
  window.removeEventListener('resize', handleResize)
})

// Watch for prop changes
watch(() => props.meteorCount, () => {
  if (!canvasSupported.value) {
    generateDOMMeteors()
  }
})

watch(() => props.enableCanvas, (newValue) => {
  if (newValue && !canvasSupported.value) {
    initCanvas()
  } else if (!newValue) {
    stopAnimation()
    canvasSupported.value = false
    generateDOMMeteors()
  }
})

// Expose methods for external control
defineExpose({
  startAnimation,
  stopAnimation,
  addMeteor: () => {
    if (activeMeteors.value.length < props.meteorCount * 2) {
      activeMeteors.value.push(createMeteor())
    }
  },
  clearMeteors: () => {
    activeMeteors.value.forEach(meteor => recycleMeteor(meteor))
  },
  getPerformanceStats: () => ({
    activeMeteors: activeMeteors.value.length,
    pooledMeteors: meteorPool.value.length,
    canvasSupported: canvasSupported.value,
    animationRunning: animationFrame !== null
  })
})
</script>

<style scoped>
.meteors-container {
  z-index: 1;
  will-change: contents;
}

/* Canvas styles */
canvas {
  display: block;
  will-change: contents;
}

/* DOM fallback styles */
.dom-meteors {
  position: absolute;
  inset: 0;
}

.meteor {
  filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.8));
  will-change: transform;
  transform: translate3d(0, 0, 0); /* Force GPU layer */
}

.meteor-head {
  position: relative;
  box-shadow:
    0 0 10px rgba(255, 215, 0, 0.8),
    0 0 20px rgba(255, 165, 0, 0.6),
    0 0 30px rgba(255, 69, 0, 0.4);
}

.meteor-core {
  animation: core-pulse 0.5s ease-in-out infinite alternate;
}

.meteor-sparkle {
  animation: sparkle-twinkle 1s ease-in-out infinite;
}

@keyframes meteor-fall {
  0% {
    transform: translateX(0) translateY(0) rotate(45deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(-100vw) translateY(100vh) rotate(45deg);
    opacity: 0;
  }
}

@keyframes core-pulse {
  0% {
    transform: scale(0.3);
    opacity: 0.8;
  }
  100% {
    transform: scale(0.7);
    opacity: 1;
  }
}

@keyframes sparkle-twinkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .meteor {
    transform: scale(0.7) !important;
  }
}
</style>