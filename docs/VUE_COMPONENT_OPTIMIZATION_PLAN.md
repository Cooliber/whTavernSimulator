# Vue Component Structure Optimization Plan

## Executive Summary

This document outlines the optimization plan for Vue.js components in the Warhammer Tavern Simulator v3, ensuring adherence to Nuxt.js conventions, modern Vue 3 Composition API patterns, and best practices for performance and maintainability.

## Current Component Analysis

### ✅ **Strengths Identified**

1. **Modern Composition API Usage**
   - Proper use of `defineProps()` with TypeScript interfaces
   - Correct implementation of `defineEmits()` for event handling
   - Appropriate use of `ref()`, `reactive()`, and `computed()`
   - Good lifecycle hook usage (`onMounted()`, `onUnmounted()`)

2. **TypeScript Integration**
   - Well-defined interfaces for component props
   - Type-safe event emissions
   - Proper generic type usage in complex components

3. **Component Organization**
   - Clear separation between UI components (`/components/ui/`) and feature components (`/components/inspira/`)
   - Consistent naming conventions following Vue.js standards
   - Proper use of slots for content projection

### ⚠️ **Areas for Improvement**

1. **Performance Optimizations**
   - Some components could benefit from `shallowRef()` for large objects
   - Animation cleanup could be more robust
   - Memory management in complex components needs enhancement

2. **Composable Extraction**
   - Shared logic should be extracted to composables
   - Animation logic is repeated across components
   - State management patterns could be centralized

3. **Accessibility Enhancements**
   - ARIA attributes need to be added to interactive components
   - Keyboard navigation support is incomplete
   - Screen reader support could be improved

## Optimization Strategy

### Phase 1: Performance Enhancements

#### 1.1 Memory Management Improvements
```typescript
// Before: Regular ref for large objects
const characters = ref<Character[]>([])

// After: Shallow ref for better performance
const characters = shallowRef<Character[]>([])

// Proper cleanup in components
onUnmounted(() => {
  // Clean up animations, event listeners, etc.
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value)
  }
})
```

#### 1.2 Lazy Loading and Code Splitting
```typescript
// Implement lazy loading for heavy components
const WeatherSystem = defineAsyncComponent(() => import('./WeatherSystem.vue'))
const ParticlesBg = defineAsyncComponent(() => import('./ParticlesBg.vue'))
```

#### 1.3 Virtual Scrolling for Large Lists
```typescript
// For character lists and inventory items
import { VirtualList } from '@tanstack/vue-virtual'
```

### Phase 2: Composable Extraction

#### 2.1 Animation Composables
```typescript
// composables/useAnimation.ts
export function useAnimation() {
  const isAnimating = ref(false)
  const animationFrame = ref<number>()
  
  const startAnimation = (callback: () => void) => {
    if (isAnimating.value) return
    isAnimating.value = true
    
    const animate = () => {
      callback()
      if (isAnimating.value) {
        animationFrame.value = requestAnimationFrame(animate)
      }
    }
    animate()
  }
  
  const stopAnimation = () => {
    isAnimating.value = false
    if (animationFrame.value) {
      cancelAnimationFrame(animationFrame.value)
    }
  }
  
  onUnmounted(() => {
    stopAnimation()
  })
  
  return {
    isAnimating: readonly(isAnimating),
    startAnimation,
    stopAnimation
  }
}
```

#### 2.2 Warhammer Theme Composables
```typescript
// composables/useWarhammerTheme.ts
export function useWarhammerTheme() {
  const factionColors = {
    empire: ['#ffd700', '#b8860b', '#daa520'],
    chaos: ['#8b0000', '#dc143c', '#ff4500'],
    elves: ['#228b22', '#32cd32', '#90ee90'],
    dwarfs: ['#cd853f', '#a0522d', '#8b4513'],
    undead: ['#9400d3', '#8b008b', '#dda0dd'],
    orcs: ['#556b2f', '#6b8e23', '#9acd32']
  }
  
  const getFactionColors = (faction: string) => {
    return factionColors[faction] || factionColors.empire
  }
  
  const applyFactionTheme = (faction: string) => {
    const colors = getFactionColors(faction)
    return {
      '--faction-primary': colors[0],
      '--faction-secondary': colors[1],
      '--faction-accent': colors[2]
    }
  }
  
  return {
    factionColors,
    getFactionColors,
    applyFactionTheme
  }
}
```

#### 2.3 Device Detection Composables
```typescript
// composables/useDeviceCapabilities.ts
export function useDeviceCapabilities() {
  const isMobile = ref(false)
  const isTablet = ref(false)
  const isDesktop = ref(false)
  const supportsWebGL = ref(false)
  const preferredQuality = ref<'low' | 'medium' | 'high'>('medium')
  
  const detectDevice = () => {
    const width = window.innerWidth
    isMobile.value = width < 768
    isTablet.value = width >= 768 && width < 1024
    isDesktop.value = width >= 1024
    
    // WebGL detection
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
    supportsWebGL.value = !!gl
    
    // Quality based on device capabilities
    if (isMobile.value) {
      preferredQuality.value = 'low'
    } else if (isTablet.value) {
      preferredQuality.value = 'medium'
    } else {
      preferredQuality.value = 'high'
    }
  }
  
  onMounted(() => {
    detectDevice()
    window.addEventListener('resize', detectDevice)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', detectDevice)
  })
  
  return {
    isMobile: readonly(isMobile),
    isTablet: readonly(isTablet),
    isDesktop: readonly(isDesktop),
    supportsWebGL: readonly(supportsWebGL),
    preferredQuality: readonly(preferredQuality)
  }
}
```

### Phase 3: Accessibility Improvements

#### 3.1 ARIA Attributes and Keyboard Navigation
```typescript
// Enhanced component with accessibility
<template>
  <button
    :aria-label="ariaLabel"
    :aria-pressed="isPressed"
    :aria-disabled="disabled"
    @click="handleClick"
    @keydown.enter="handleClick"
    @keydown.space.prevent="handleClick"
    class="warhammer-button"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  ariaLabel?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  ariaLabel: '',
  disabled: false
})

const isPressed = ref(false)

const handleClick = () => {
  if (props.disabled) return
  isPressed.value = !isPressed.value
  emit('click')
}
</script>
```

#### 3.2 Screen Reader Support
```typescript
// composables/useScreenReader.ts
export function useScreenReader() {
  const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div')
    announcement.setAttribute('aria-live', 'polite')
    announcement.setAttribute('aria-atomic', 'true')
    announcement.className = 'sr-only'
    announcement.textContent = message
    
    document.body.appendChild(announcement)
    
    setTimeout(() => {
      document.body.removeChild(announcement)
    }, 1000)
  }
  
  return {
    announceToScreenReader
  }
}
```

### Phase 4: Component Architecture Improvements

#### 4.1 Enhanced Error Boundaries
```typescript
// components/ErrorBoundary.vue
<template>
  <div v-if="hasError" class="error-boundary">
    <h2>Something went wrong in the tavern!</h2>
    <p>{{ errorMessage }}</p>
    <button @click="retry">Try Again</button>
  </div>
  <slot v-else />
</template>

<script setup lang="ts">
const hasError = ref(false)
const errorMessage = ref('')

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
}

onErrorCaptured((error) => {
  hasError.value = true
  errorMessage.value = error.message
  console.error('Component error:', error)
  return false
})
</script>
```

#### 4.2 Improved State Management
```typescript
// stores/tavern.ts
export const useTavernStore = defineStore('tavern', () => {
  const characters = shallowRef<Character[]>([])
  const currentWeather = ref<WeatherState>('clear')
  const ambientSounds = ref<boolean>(true)
  
  const addCharacter = (character: Character) => {
    characters.value = [...characters.value, character]
  }
  
  const removeCharacter = (id: string) => {
    characters.value = characters.value.filter(c => c.id !== id)
  }
  
  const updateWeather = (weather: WeatherState) => {
    currentWeather.value = weather
  }
  
  return {
    characters: readonly(characters),
    currentWeather: readonly(currentWeather),
    ambientSounds: readonly(ambientSounds),
    addCharacter,
    removeCharacter,
    updateWeather
  }
})
```

## Implementation Timeline

### Week 1: Performance Optimizations
- [ ] Implement `shallowRef()` for large data structures
- [ ] Add proper cleanup in all components
- [ ] Implement lazy loading for heavy components
- [ ] Add virtual scrolling for lists

### Week 2: Composable Extraction
- [ ] Create animation composables
- [ ] Extract Warhammer theme logic
- [ ] Implement device detection composables
- [ ] Create shared utility composables

### Week 3: Accessibility Enhancements
- [ ] Add ARIA attributes to all interactive components
- [ ] Implement keyboard navigation
- [ ] Add screen reader support
- [ ] Test with accessibility tools

### Week 4: Architecture Improvements
- [ ] Implement error boundaries
- [ ] Enhance state management
- [ ] Add component testing
- [ ] Performance monitoring

## Testing Strategy

### Unit Testing
```typescript
// tests/components/Card3D.test.ts
import { mount } from '@vue/test-utils'
import Card3D from '@/components/inspira/Card3D.vue'

describe('Card3D', () => {
  it('applies correct rotation on mouse move', async () => {
    const wrapper = mount(Card3D, {
      props: { rotationIntensity: 15 }
    })
    
    await wrapper.trigger('mousemove', {
      clientX: 100,
      clientY: 100
    })
    
    expect(wrapper.vm.rotateX).toBeGreaterThan(0)
    expect(wrapper.vm.rotateY).toBeGreaterThan(0)
  })
})
```

### Integration Testing
```typescript
// tests/integration/tavern-flow.test.ts
describe('Tavern Flow', () => {
  it('should navigate between characters and conversations', async () => {
    // Test complete user flow
  })
})
```

## Performance Monitoring

### Metrics to Track
- Component render time
- Memory usage
- Animation frame rate
- Bundle size impact
- Time to interactive

### Tools
- Vue DevTools
- Lighthouse
- Bundle Analyzer
- Performance Observer API

## Conclusion

This optimization plan ensures that the Vue components in Warhammer Tavern Simulator v3 follow modern best practices while maintaining the immersive fantasy experience. The phased approach allows for systematic improvements without disrupting the existing functionality.

Key benefits:
- Improved performance and memory management
- Better code reusability through composables
- Enhanced accessibility for all users
- Maintainable and scalable architecture
- Comprehensive testing coverage

The implementation will result in a more robust, performant, and accessible application that provides an exceptional experience for Warhammer Fantasy players.
