<template>
  <div 
    class="warhammer-icon inline-flex items-center justify-center"
    :class="[
      sizeClasses,
      colorClasses,
      {
        'animate-pulse': pulsing,
        'animate-spin': spinning,
        'animate-bounce': bouncing,
        'cursor-pointer': clickable,
        'hover:scale-110 transition-transform duration-200': hoverable && !prefersReducedMotion
      }
    ]"
    :style="customStyles"
    :title="tooltip"
    :aria-label="ariaLabel || tooltip"
    @click="handleClick"
  >
    <!-- Main Icon -->
    <Icon 
      :name="iconName" 
      :class="iconClasses"
      :aria-hidden="!ariaLabel"
    />
    
    <!-- Badge/Overlay -->
    <div 
      v-if="badge"
      class="absolute -top-1 -right-1 min-w-[1.25rem] h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center px-1"
      :class="badgeClasses"
    >
      {{ badge }}
    </div>
    
    <!-- Status Indicator -->
    <div 
      v-if="status"
      class="absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-background"
      :class="statusClasses"
    ></div>
    
    <!-- Glow Effect -->
    <div 
      v-if="glowing"
      class="absolute inset-0 rounded-full opacity-50 animate-ping"
      :class="glowClasses"
    ></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  // Core props
  concept?: string
  name?: string
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  color?: string
  
  // Warhammer-specific
  faction?: string
  rarity?: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary' | 'artifact'
  difficulty?: 'easy' | 'medium' | 'hard' | 'legendary' | 'nightmare'
  
  // Visual effects
  pulsing?: boolean
  spinning?: boolean
  bouncing?: boolean
  glowing?: boolean
  hoverable?: boolean
  
  // Interactive
  clickable?: boolean
  tooltip?: string
  ariaLabel?: string
  
  // Overlays
  badge?: string | number
  badgeColor?: string
  status?: 'online' | 'offline' | 'busy' | 'away'
  
  // Custom styling
  customColor?: string
  customSize?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  hoverable: true,
  clickable: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Composables
const { getIcon, getIconWithColor, getFactionColor, getRarityColor, getDifficultyColor } = useWarhammerIcons()

// Check for reduced motion preference
const prefersReducedMotion = ref(false)

onMounted(() => {
  if (typeof window !== 'undefined') {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches
    
    mediaQuery.addEventListener('change', (e) => {
      prefersReducedMotion.value = e.matches
    })
  }
})

// Computed properties
const iconName = computed(() => {
  if (props.name) return props.name
  if (props.concept) return getIcon(props.concept)
  return 'circle'
})

const iconColor = computed(() => {
  if (props.customColor) return props.customColor
  if (props.color) return props.color
  if (props.faction) return getFactionColor(props.faction)
  if (props.rarity) return getRarityColor(props.rarity)
  if (props.difficulty) return getDifficultyColor(props.difficulty)
  return 'current'
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-8 h-8',
    '2xl': 'w-10 h-10'
  }
  return `relative ${sizes[props.size]}`
})

const iconClasses = computed(() => {
  return `w-full h-full text-${iconColor.value}-500`
})

const colorClasses = computed(() => {
  if (props.customColor) return ''
  return `text-${iconColor.value}-500`
})

const badgeClasses = computed(() => {
  if (props.badgeColor) {
    return `bg-${props.badgeColor}-500`
  }
  return 'bg-red-500'
})

const statusClasses = computed(() => {
  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-gray-500',
    busy: 'bg-red-500',
    away: 'bg-yellow-500'
  }
  return statusColors[props.status || 'offline']
})

const glowClasses = computed(() => {
  return `bg-${iconColor.value}-500`
})

const customStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.customSize) {
    styles.width = props.customSize
    styles.height = props.customSize
  }
  
  if (props.customColor) {
    styles.color = props.customColor
  }
  
  return styles
})

// Methods
const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.warhammer-icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .animate-pulse,
  .animate-spin,
  .animate-bounce,
  .animate-ping,
  .transition-transform {
    animation: none !important;
    transition: none !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .warhammer-icon {
    filter: contrast(1.5);
  }
}

/* Focus improvements */
.warhammer-icon:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 0.25rem;
}

/* Hover effects */
.warhammer-icon.cursor-pointer:hover {
  filter: brightness(1.1);
}

/* Custom glow animation for magical effects */
@keyframes magical-glow {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

.warhammer-icon.magical {
  animation: magical-glow 2s ease-in-out infinite;
}

/* Faction-specific styling */
.warhammer-icon.faction-empire {
  filter: drop-shadow(0 0 4px rgba(59, 130, 246, 0.5));
}

.warhammer-icon.faction-dwarfs {
  filter: drop-shadow(0 0 4px rgba(249, 115, 22, 0.5));
}

.warhammer-icon.faction-elves {
  filter: drop-shadow(0 0 4px rgba(34, 197, 94, 0.5));
}

.warhammer-icon.faction-chaos {
  filter: drop-shadow(0 0 4px rgba(239, 68, 68, 0.5));
}

/* Rarity-specific styling */
.warhammer-icon.rarity-legendary {
  animation: legendary-shimmer 3s ease-in-out infinite;
}

@keyframes legendary-shimmer {
  0%, 100% {
    filter: drop-shadow(0 0 6px rgba(249, 115, 22, 0.6));
  }
  50% {
    filter: drop-shadow(0 0 12px rgba(249, 115, 22, 0.9));
  }
}

.warhammer-icon.rarity-artifact {
  animation: artifact-pulse 2s ease-in-out infinite;
}

@keyframes artifact-pulse {
  0%, 100% {
    filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.7));
    transform: scale(1);
  }
  50% {
    filter: drop-shadow(0 0 16px rgba(239, 68, 68, 1));
    transform: scale(1.05);
  }
}

/* Status indicator animations */
.status-online {
  animation: online-pulse 2s ease-in-out infinite;
}

@keyframes online-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

/* Tooltip styling */
.warhammer-icon[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  white-space: nowrap;
  z-index: 50;
  pointer-events: none;
}
</style>
