/**
 * Animation Composable
 * Provides reusable animation utilities for Warhammer Tavern components
 */

export interface AnimationOptions {
  duration?: number
  easing?: string
  delay?: number
  iterations?: number | 'infinite'
  direction?: 'normal' | 'reverse' | 'alternate' | 'alternate-reverse'
  fillMode?: 'none' | 'forwards' | 'backwards' | 'both'
}

export interface ParticleOptions {
  count?: number
  color?: string
  size?: number
  speed?: number
  direction?: 'up' | 'down' | 'left' | 'right' | 'random'
  lifetime?: number
}

export function useAnimation() {
  // Animation state
  const isAnimating = ref(false)
  const animationFrame = ref<number>()
  const activeAnimations = ref<Set<Animation>>(new Set())
  const performanceMode = ref<'low' | 'medium' | 'high'>('medium')

  // Performance monitoring
  const frameRate = ref(60)
  const lastFrameTime = ref(0)

  // Core animation functions
  const startAnimation = (callback: () => void) => {
    if (isAnimating.value) return
    
    isAnimating.value = true
    lastFrameTime.value = performance.now()
    
    const animate = (currentTime: number) => {
      const deltaTime = currentTime - lastFrameTime.value
      frameRate.value = Math.round(1000 / deltaTime)
      lastFrameTime.value = currentTime
      
      callback()
      
      if (isAnimating.value) {
        animationFrame.value = requestAnimationFrame(animate)
      }
    }
    
    animationFrame.value = requestAnimationFrame(animate)
  }

  const stopAnimation = () => {
    isAnimating.value = false
    if (animationFrame.value) {
      cancelAnimationFrame(animationFrame.value)
      animationFrame.value = undefined
    }
  }

  // CSS Animation utilities
  const createCSSAnimation = (
    element: HTMLElement,
    keyframes: Keyframe[],
    options: AnimationOptions = {}
  ): Animation => {
    const defaultOptions: KeyframeAnimationOptions = {
      duration: options.duration || 1000,
      easing: options.easing || 'ease-in-out',
      delay: options.delay || 0,
      iterations: options.iterations || 1,
      direction: options.direction || 'normal',
      fill: options.fillMode || 'forwards'
    }

    const animation = element.animate(keyframes, defaultOptions)
    activeAnimations.value.add(animation)
    
    animation.addEventListener('finish', () => {
      activeAnimations.value.delete(animation)
    })
    
    return animation
  }

  // Warhammer-specific animations
  const medievalEntrance = (element: HTMLElement, options: AnimationOptions = {}) => {
    const keyframes: Keyframe[] = [
      {
        opacity: 0,
        transform: 'translateY(30px) scale(0.9)',
        filter: 'blur(2px)'
      },
      {
        opacity: 1,
        transform: 'translateY(0px) scale(1)',
        filter: 'blur(0px)'
      }
    ]
    
    return createCSSAnimation(element, keyframes, {
      duration: 600,
      easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
      ...options
    })
  }

  const glowPulse = (element: HTMLElement, color = '#ffd700', options: AnimationOptions = {}) => {
    const keyframes: Keyframe[] = [
      {
        textShadow: `0 0 5px ${color}50`,
        boxShadow: `0 0 10px ${color}30`
      },
      {
        textShadow: `0 0 20px ${color}80, 0 0 30px ${color}60`,
        boxShadow: `0 0 30px ${color}50, 0 0 50px ${color}30`
      },
      {
        textShadow: `0 0 5px ${color}50`,
        boxShadow: `0 0 10px ${color}30`
      }
    ]
    
    return createCSSAnimation(element, keyframes, {
      duration: 3000,
      iterations: 'infinite',
      easing: 'ease-in-out',
      ...options
    })
  }

  const fireFlicker = (element: HTMLElement, options: AnimationOptions = {}) => {
    const keyframes: Keyframe[] = [
      {
        boxShadow: '0 0 20px rgba(255, 69, 0, 0.4), 0 0 40px rgba(255, 69, 0, 0.2)',
        filter: 'brightness(1) hue-rotate(0deg)'
      },
      {
        boxShadow: '0 0 30px rgba(255, 69, 0, 0.6), 0 0 50px rgba(255, 69, 0, 0.3)',
        filter: 'brightness(1.1) hue-rotate(5deg)'
      },
      {
        boxShadow: '0 0 25px rgba(255, 69, 0, 0.5), 0 0 45px rgba(255, 69, 0, 0.25)',
        filter: 'brightness(0.95) hue-rotate(-3deg)'
      }
    ]
    
    return createCSSAnimation(element, keyframes, {
      duration: 2000,
      iterations: 'infinite',
      direction: 'alternate',
      easing: 'ease-in-out',
      ...options
    })
  }

  const floatAnimation = (element: HTMLElement, distance = 10, options: AnimationOptions = {}) => {
    const keyframes: Keyframe[] = [
      { transform: 'translateY(0px)' },
      { transform: `translateY(-${distance}px)` },
      { transform: 'translateY(0px)' }
    ]
    
    return createCSSAnimation(element, keyframes, {
      duration: 6000,
      iterations: 'infinite',
      easing: 'ease-in-out',
      ...options
    })
  }

  // Particle system
  const createParticles = (
    container: HTMLElement,
    options: ParticleOptions = {}
  ) => {
    const {
      count = 20,
      color = '#ffd700',
      size = 2,
      speed = 1,
      direction = 'up',
      lifetime = 3000
    } = options

    const particles: HTMLElement[] = []

    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div')
      particle.className = 'warhammer-particle'
      particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: ${color};
        border-radius: 50%;
        pointer-events: none;
        z-index: 1000;
      `

      // Random starting position
      const startX = Math.random() * container.offsetWidth
      const startY = container.offsetHeight
      particle.style.left = `${startX}px`
      particle.style.top = `${startY}px`

      container.appendChild(particle)
      particles.push(particle)

      // Animate particle
      const endY = direction === 'up' ? -50 : container.offsetHeight + 50
      const endX = startX + (Math.random() - 0.5) * 100 // Add some horizontal drift

      const animation = particle.animate([
        {
          transform: `translate(0, 0)`,
          opacity: 1
        },
        {
          transform: `translate(${endX - startX}px, ${endY - startY}px)`,
          opacity: 0
        }
      ], {
        duration: lifetime / speed,
        easing: 'linear',
        fill: 'forwards'
      })

      animation.addEventListener('finish', () => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle)
        }
      })
    }

    return particles
  }

  // Performance optimization
  const optimizeForDevice = () => {
    // Detect device capabilities
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl')
    const hasWebGL = !!gl
    
    const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    const isLowEnd = navigator.hardwareConcurrency <= 2
    
    if (isMobile || isLowEnd || !hasWebGL) {
      performanceMode.value = 'low'
    } else if (frameRate.value < 30) {
      performanceMode.value = 'medium'
    } else {
      performanceMode.value = 'high'
    }
  }

  // Reduced motion support
  const respectsReducedMotion = ref(false)
  
  const checkReducedMotion = () => {
    if (typeof window !== 'undefined') {
      respectsReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    }
  }

  // Animation cleanup
  const cleanupAnimations = () => {
    stopAnimation()
    activeAnimations.value.forEach(animation => {
      animation.cancel()
    })
    activeAnimations.value.clear()
  }

  // Lifecycle management
  onMounted(() => {
    optimizeForDevice()
    checkReducedMotion()
    
    if (typeof window !== 'undefined') {
      window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', checkReducedMotion)
    }
  })

  onUnmounted(() => {
    cleanupAnimations()
    
    if (typeof window !== 'undefined') {
      window.matchMedia('(prefers-reduced-motion: reduce)').removeEventListener('change', checkReducedMotion)
    }
  })

  // Conditional animation wrapper
  const animateIf = (
    condition: boolean,
    animationFn: () => Animation | void,
    fallbackFn?: () => void
  ) => {
    if (condition && !respectsReducedMotion.value) {
      return animationFn()
    } else if (fallbackFn) {
      fallbackFn()
    }
  }

  return {
    // State
    isAnimating: readonly(isAnimating),
    frameRate: readonly(frameRate),
    performanceMode: readonly(performanceMode),
    respectsReducedMotion: readonly(respectsReducedMotion),
    
    // Core functions
    startAnimation,
    stopAnimation,
    createCSSAnimation,
    
    // Warhammer animations
    medievalEntrance,
    glowPulse,
    fireFlicker,
    floatAnimation,
    
    // Particle system
    createParticles,
    
    // Utilities
    optimizeForDevice,
    cleanupAnimations,
    animateIf
  }
}
