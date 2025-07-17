<template>
  <div 
    ref="containerRef"
    class="interactive-grid-pattern relative overflow-hidden"
    :class="className"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Grid SVG -->
    <svg 
      class="absolute inset-0 w-full h-full pointer-events-none"
      :viewBox="`0 0 ${width} ${height}`"
    >
      <defs>
        <!-- Grid pattern definition -->
        <pattern 
          id="grid-pattern"
          :width="gridSize"
          :height="gridSize"
          patternUnits="userSpaceOnUse"
        >
          <path 
            :d="`M ${gridSize} 0 L 0 0 0 ${gridSize}`"
            fill="none"
            :stroke="gridColor"
            :stroke-width="strokeWidth"
            opacity="0.3"
          />
        </pattern>
        
        <!-- Glow filter -->
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Background grid -->
      <rect 
        width="100%" 
        height="100%" 
        fill="url(#grid-pattern)"
      />
      
      <!-- Interactive grid lines -->
      <g class="interactive-lines">
        <!-- Horizontal lines -->
        <line 
          v-for="(line, index) in horizontalLines" 
          :key="`h-${index}`"
          :x1="0"
          :y1="line.y"
          :x2="width"
          :y2="line.y"
          :stroke="line.color"
          :stroke-width="line.width"
          :opacity="line.opacity"
          filter="url(#glow)"
          class="grid-line"
          :style="{ 
            transition: 'all 0.3s ease',
            animationDelay: index * 0.1 + 's'
          }"
        />
        
        <!-- Vertical lines -->
        <line 
          v-for="(line, index) in verticalLines" 
          :key="`v-${index}`"
          :x1="line.x"
          :y1="0"
          :x2="line.x"
          :y2="height"
          :stroke="line.color"
          :stroke-width="line.width"
          :opacity="line.opacity"
          filter="url(#glow)"
          class="grid-line"
          :style="{ 
            transition: 'all 0.3s ease',
            animationDelay: index * 0.1 + 's'
          }"
        />
      </g>
      
      <!-- Intersection points -->
      <g class="intersection-points">
        <circle 
          v-for="(point, index) in intersectionPoints" 
          :key="`point-${index}`"
          :cx="point.x"
          :cy="point.y"
          :r="point.radius"
          :fill="point.color"
          :opacity="point.opacity"
          filter="url(#glow)"
          class="intersection-point"
          :style="{ 
            animation: `point-pulse ${2 + Math.random()}s ease-in-out infinite`,
            animationDelay: Math.random() * 2 + 's'
          }"
        />
      </g>
      
      <!-- Mouse proximity effect -->
      <circle 
        v-if="mousePosition.x > 0"
        :cx="mousePosition.x"
        :cy="mousePosition.y"
        :r="proximityRadius"
        fill="none"
        :stroke="proximityColor"
        :stroke-width="2"
        opacity="0.6"
        filter="url(#glow)"
        class="proximity-circle"
      />
      
      <!-- Energy waves -->
      <g class="energy-waves">
        <circle 
          v-for="wave in energyWaves" 
          :key="wave.id"
          :cx="wave.x"
          :cy="wave.y"
          :r="wave.radius"
          fill="none"
          :stroke="wave.color"
          :stroke-width="wave.width"
          :opacity="wave.opacity"
          class="energy-wave"
        />
      </g>
    </svg>
    
    <!-- Content overlay -->
    <div class="relative z-10">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  gridSize?: number
  gridColor?: string
  strokeWidth?: number
  proximityRadius?: number
  proximityColor?: string
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  gridSize: 40,
  gridColor: '#ffd700',
  strokeWidth: 1,
  proximityRadius: 60,
  proximityColor: '#ffd700',
  className: ''
})

interface GridLine {
  x?: number
  y?: number
  color: string
  width: number
  opacity: number
}

interface IntersectionPoint {
  x: number
  y: number
  radius: number
  color: string
  opacity: number
}

interface EnergyWave {
  id: number
  x: number
  y: number
  radius: number
  color: string
  width: number
  opacity: number
}

const containerRef = ref<HTMLElement>()
const mousePosition = ref({ x: 0, y: 0 })
const width = ref(800)
const height = ref(600)
const horizontalLines = ref<GridLine[]>([])
const verticalLines = ref<GridLine[]>([])
const intersectionPoints = ref<IntersectionPoint[]>([])
const energyWaves = ref<EnergyWave[]>([])
let waveId = 0

const updateDimensions = () => {
  if (!containerRef.value) return
  
  const rect = containerRef.value.getBoundingClientRect()
  width.value = rect.width
  height.value = rect.height
  
  generateGrid()
}

const generateGrid = () => {
  // Generate horizontal lines
  horizontalLines.value = []
  for (let y = 0; y <= height.value; y += props.gridSize) {
    horizontalLines.value.push({
      y,
      color: props.gridColor,
      width: props.strokeWidth,
      opacity: 0.3 + Math.random() * 0.4
    })
  }
  
  // Generate vertical lines
  verticalLines.value = []
  for (let x = 0; x <= width.value; x += props.gridSize) {
    verticalLines.value.push({
      x,
      color: props.gridColor,
      width: props.strokeWidth,
      opacity: 0.3 + Math.random() * 0.4
    })
  }
  
  // Generate intersection points
  intersectionPoints.value = []
  for (let x = 0; x <= width.value; x += props.gridSize) {
    for (let y = 0; y <= height.value; y += props.gridSize) {
      if (Math.random() < 0.1) { // Only show some intersection points
        intersectionPoints.value.push({
          x,
          y,
          radius: 1 + Math.random() * 2,
          color: props.gridColor,
          opacity: 0.5 + Math.random() * 0.5
        })
      }
    }
  }
}

const handleMouseMove = (event: MouseEvent) => {
  if (!containerRef.value) return
  
  const rect = containerRef.value.getBoundingClientRect()
  mousePosition.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }
  
  // Create energy wave occasionally
  if (Math.random() < 0.05) {
    createEnergyWave(mousePosition.value.x, mousePosition.value.y)
  }
  
  // Update grid lines based on mouse proximity
  updateGridProximity()
}

const handleMouseLeave = () => {
  mousePosition.value = { x: 0, y: 0 }
  resetGridLines()
}

const updateGridProximity = () => {
  const mouseX = mousePosition.value.x
  const mouseY = mousePosition.value.y
  
  // Update horizontal lines
  horizontalLines.value.forEach(line => {
    const distance = Math.abs(line.y! - mouseY)
    const proximity = Math.max(0, 1 - distance / props.proximityRadius)
    line.opacity = 0.3 + proximity * 0.7
    line.width = props.strokeWidth + proximity * 2
  })
  
  // Update vertical lines
  verticalLines.value.forEach(line => {
    const distance = Math.abs(line.x! - mouseX)
    const proximity = Math.max(0, 1 - distance / props.proximityRadius)
    line.opacity = 0.3 + proximity * 0.7
    line.width = props.strokeWidth + proximity * 2
  })
  
  // Update intersection points
  intersectionPoints.value.forEach(point => {
    const distance = Math.sqrt(
      Math.pow(point.x - mouseX, 2) + Math.pow(point.y - mouseY, 2)
    )
    const proximity = Math.max(0, 1 - distance / props.proximityRadius)
    point.opacity = 0.5 + proximity * 0.5
    point.radius = 1 + proximity * 3
  })
}

const resetGridLines = () => {
  horizontalLines.value.forEach(line => {
    line.opacity = 0.3 + Math.random() * 0.4
    line.width = props.strokeWidth
  })
  
  verticalLines.value.forEach(line => {
    line.opacity = 0.3 + Math.random() * 0.4
    line.width = props.strokeWidth
  })
  
  intersectionPoints.value.forEach(point => {
    point.opacity = 0.5 + Math.random() * 0.5
    point.radius = 1 + Math.random() * 2
  })
}

const createEnergyWave = (x: number, y: number) => {
  const wave: EnergyWave = {
    id: waveId++,
    x,
    y,
    radius: 0,
    color: props.proximityColor,
    width: 2,
    opacity: 0.8
  }
  
  energyWaves.value.push(wave)
  
  // Animate wave expansion
  const animate = () => {
    wave.radius += 2
    wave.opacity -= 0.02
    wave.width -= 0.02
    
    if (wave.opacity > 0 && wave.radius < 100) {
      requestAnimationFrame(animate)
    } else {
      energyWaves.value = energyWaves.value.filter(w => w.id !== wave.id)
    }
  }
  
  animate()
}

onMounted(() => {
  updateDimensions()
  window.addEventListener('resize', updateDimensions)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateDimensions)
})
</script>

<style scoped>
.interactive-grid-pattern {
  min-height: 400px;
}

.grid-line {
  transition: all 0.3s ease;
}

.intersection-point {
  transition: all 0.3s ease;
}

.proximity-circle {
  animation: proximity-pulse 2s ease-in-out infinite;
}

.energy-wave {
  animation: wave-expand 2s ease-out forwards;
}

@keyframes point-pulse {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.5);
  }
}

@keyframes proximity-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

@keyframes wave-expand {
  0% {
    opacity: 0.8;
    transform: scale(0);
  }
  100% {
    opacity: 0;
    transform: scale(1);
  }
}
</style>