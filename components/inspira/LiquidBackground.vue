<template>
  <div class="liquid-background">
    <svg 
      class="w-full h-full" 
      viewBox="0 0 400 400" 
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <filter id="goo">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
          <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
          <feBlend in="SourceGraphic" in2="goo" />
        </filter>
      </defs>
      
      <g filter="url(#goo)">
        <circle 
          v-for="(blob, index) in blobs" 
          :key="index"
          :cx="blob.x"
          :cy="blob.y"
          :r="blob.radius"
          :fill="blob.color"
          class="blob"
          :style="{ 
            animationDelay: blob.delay + 's',
            animationDuration: blob.duration + 's'
          }"
        />
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
interface Props {
  colors?: string[]
  blobCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  colors: () => ['#8b4513', '#a0522d', '#cd853f'],
  blobCount: 3
})

interface Blob {
  x: number
  y: number
  radius: number
  color: string
  delay: number
  duration: number
}

const blobs = ref<Blob[]>([])

const generateBlobs = () => {
  blobs.value = Array.from({ length: props.blobCount }, (_, i) => ({
    x: Math.random() * 400,
    y: Math.random() * 400,
    radius: 40 + Math.random() * 60,
    color: props.colors[i % props.colors.length],
    delay: Math.random() * 2,
    duration: 8 + Math.random() * 4
  }))
}

onMounted(() => {
  generateBlobs()
})

watch(() => props.colors, generateBlobs)
watch(() => props.blobCount, generateBlobs)
</script>

<style scoped>
.liquid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.blob {
  animation: float-blob linear infinite;
}

@keyframes float-blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -20px) scale(1.1);
  }
  50% {
    transform: translate(-20px, 30px) scale(0.9);
  }
  75% {
    transform: translate(20px, 20px) scale(1.05);
  }
}
</style>