/**
 * Device Capabilities Composable
 * Detects device capabilities and optimizes performance accordingly
 */

export interface DeviceCapabilities {
  isMobile: boolean
  isTablet: boolean
  isDesktop: boolean
  supportsWebGL: boolean
  supportsWebGL2: boolean
  maxTextureSize: number
  hardwareConcurrency: number
  memoryGB: number
  connectionType: string
  pixelRatio: number
  screenSize: { width: number; height: number }
  orientation: 'portrait' | 'landscape'
  touchSupport: boolean
  prefersDarkMode: boolean
  prefersReducedMotion: boolean
  prefersHighContrast: boolean
}

export interface AdaptiveQualitySettings {
  particleCount: number
  animationQuality: 'low' | 'medium' | 'high' | 'ultra'
  textureQuality: 'low' | 'medium' | 'high'
  shadowQuality: 'off' | 'low' | 'medium' | 'high'
  postProcessing: boolean
  antiAliasing: boolean
  bloomEffect: boolean
  weatherEffects: boolean
  audioQuality: 'low' | 'medium' | 'high'
}

export function useDeviceCapabilities() {
  // Reactive device state
  const capabilities = ref<DeviceCapabilities>({
    isMobile: false,
    isTablet: false,
    isDesktop: false,
    supportsWebGL: false,
    supportsWebGL2: false,
    maxTextureSize: 0,
    hardwareConcurrency: 1,
    memoryGB: 0,
    connectionType: 'unknown',
    pixelRatio: 1,
    screenSize: { width: 0, height: 0 },
    orientation: 'landscape',
    touchSupport: false,
    prefersDarkMode: false,
    prefersReducedMotion: false,
    prefersHighContrast: false
  })

  const qualitySettings = ref<AdaptiveQualitySettings>({
    particleCount: 20,
    animationQuality: 'medium',
    textureQuality: 'medium',
    shadowQuality: 'medium',
    postProcessing: true,
    antiAliasing: true,
    bloomEffect: true,
    weatherEffects: true,
    audioQuality: 'medium'
  })

  // Device detection functions
  const detectScreenSize = () => {
    if (typeof window === 'undefined') return

    const width = window.innerWidth
    const height = window.innerHeight

    capabilities.value.screenSize = { width, height }
    capabilities.value.isMobile = width < 768
    capabilities.value.isTablet = width >= 768 && width < 1024
    capabilities.value.isDesktop = width >= 1024
    capabilities.value.orientation = width > height ? 'landscape' : 'portrait'
    capabilities.value.pixelRatio = window.devicePixelRatio || 1
  }

  const detectWebGLCapabilities = () => {
    if (typeof window === 'undefined') return

    const canvas = document.createElement('canvas')
    
    // WebGL 1.0 detection
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
    capabilities.value.supportsWebGL = !!gl

    // WebGL 2.0 detection
    const gl2 = canvas.getContext('webgl2')
    capabilities.value.supportsWebGL2 = !!gl2

    // Get max texture size
    if (gl) {
      capabilities.value.maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE)
    }
  }

  const detectHardwareCapabilities = () => {
    if (typeof navigator === 'undefined') return

    // CPU cores
    capabilities.value.hardwareConcurrency = navigator.hardwareConcurrency || 1

    // Memory (if available)
    if ('deviceMemory' in navigator) {
      capabilities.value.memoryGB = (navigator as any).deviceMemory || 0
    }

    // Connection type
    if ('connection' in navigator) {
      const connection = (navigator as any).connection
      capabilities.value.connectionType = connection?.effectiveType || 'unknown'
    }

    // Touch support
    capabilities.value.touchSupport = 'ontouchstart' in window || navigator.maxTouchPoints > 0
  }

  const detectUserPreferences = () => {
    if (typeof window === 'undefined') return

    // Dark mode preference
    capabilities.value.prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches

    // Reduced motion preference
    capabilities.value.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    // High contrast preference
    capabilities.value.prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches
  }

  // Quality optimization based on device capabilities
  const optimizeQualitySettings = () => {
    const caps = capabilities.value
    const settings = qualitySettings.value

    // Mobile optimizations
    if (caps.isMobile) {
      settings.particleCount = Math.min(10, settings.particleCount)
      settings.animationQuality = 'low'
      settings.textureQuality = 'low'
      settings.shadowQuality = 'off'
      settings.postProcessing = false
      settings.antiAliasing = false
      settings.bloomEffect = false
      settings.audioQuality = 'low'
    }
    // Tablet optimizations
    else if (caps.isTablet) {
      settings.particleCount = Math.min(15, settings.particleCount)
      settings.animationQuality = 'medium'
      settings.textureQuality = 'medium'
      settings.shadowQuality = 'low'
      settings.postProcessing = true
      settings.antiAliasing = false
      settings.bloomEffect = true
      settings.audioQuality = 'medium'
    }
    // Desktop optimizations
    else {
      // High-end desktop
      if (caps.hardwareConcurrency >= 8 && caps.memoryGB >= 8 && caps.supportsWebGL2) {
        settings.particleCount = 50
        settings.animationQuality = 'ultra'
        settings.textureQuality = 'high'
        settings.shadowQuality = 'high'
        settings.postProcessing = true
        settings.antiAliasing = true
        settings.bloomEffect = true
        settings.audioQuality = 'high'
      }
      // Mid-range desktop
      else if (caps.hardwareConcurrency >= 4 && caps.supportsWebGL) {
        settings.particleCount = 30
        settings.animationQuality = 'high'
        settings.textureQuality = 'medium'
        settings.shadowQuality = 'medium'
        settings.postProcessing = true
        settings.antiAliasing = true
        settings.bloomEffect = true
        settings.audioQuality = 'high'
      }
      // Low-end desktop
      else {
        settings.particleCount = 20
        settings.animationQuality = 'medium'
        settings.textureQuality = 'low'
        settings.shadowQuality = 'low'
        settings.postProcessing = false
        settings.antiAliasing = false
        settings.bloomEffect = false
        settings.audioQuality = 'medium'
      }
    }

    // Accessibility adjustments
    if (caps.prefersReducedMotion) {
      settings.particleCount = 0
      settings.animationQuality = 'low'
      settings.weatherEffects = false
    }

    // Connection-based adjustments
    if (caps.connectionType === 'slow-2g' || caps.connectionType === '2g') {
      settings.textureQuality = 'low'
      settings.audioQuality = 'low'
    }
  }

  // Performance monitoring
  const performanceMetrics = ref({
    fps: 60,
    frameTime: 16.67,
    memoryUsage: 0,
    gpuMemoryUsage: 0
  })

  const startPerformanceMonitoring = () => {
    let lastTime = performance.now()
    let frameCount = 0

    const monitor = () => {
      const currentTime = performance.now()
      const deltaTime = currentTime - lastTime
      frameCount++

      if (frameCount >= 60) {
        performanceMetrics.value.fps = Math.round(1000 / (deltaTime / frameCount))
        performanceMetrics.value.frameTime = deltaTime / frameCount
        frameCount = 0
        lastTime = currentTime

        // Auto-adjust quality based on performance
        if (performanceMetrics.value.fps < 30) {
          downgradeQuality()
        } else if (performanceMetrics.value.fps > 55) {
          upgradeQuality()
        }
      }

      requestAnimationFrame(monitor)
    }

    requestAnimationFrame(monitor)
  }

  const downgradeQuality = () => {
    const settings = qualitySettings.value

    if (settings.animationQuality === 'ultra') settings.animationQuality = 'high'
    else if (settings.animationQuality === 'high') settings.animationQuality = 'medium'
    else if (settings.animationQuality === 'medium') settings.animationQuality = 'low'

    if (settings.particleCount > 5) settings.particleCount = Math.max(5, settings.particleCount - 5)
    if (settings.shadowQuality !== 'off') {
      if (settings.shadowQuality === 'high') settings.shadowQuality = 'medium'
      else if (settings.shadowQuality === 'medium') settings.shadowQuality = 'low'
      else settings.shadowQuality = 'off'
    }
  }

  const upgradeQuality = () => {
    const settings = qualitySettings.value
    const caps = capabilities.value

    // Only upgrade if device supports it
    if (caps.isDesktop && caps.supportsWebGL2) {
      if (settings.animationQuality === 'low') settings.animationQuality = 'medium'
      else if (settings.animationQuality === 'medium') settings.animationQuality = 'high'
      else if (settings.animationQuality === 'high' && caps.hardwareConcurrency >= 8) {
        settings.animationQuality = 'ultra'
      }

      if (settings.particleCount < 30) settings.particleCount = Math.min(30, settings.particleCount + 5)
    }
  }

  // Utility functions
  const isLowEndDevice = computed(() => {
    const caps = capabilities.value
    return caps.isMobile || 
           caps.hardwareConcurrency <= 2 || 
           caps.memoryGB <= 2 || 
           !caps.supportsWebGL
  })

  const canHandleAdvancedEffects = computed(() => {
    const caps = capabilities.value
    return caps.isDesktop && 
           caps.supportsWebGL2 && 
           caps.hardwareConcurrency >= 4 && 
           !caps.prefersReducedMotion
  })

  const recommendedSettings = computed(() => qualitySettings.value)

  // Event listeners for dynamic updates
  const setupEventListeners = () => {
    if (typeof window === 'undefined') return

    window.addEventListener('resize', detectScreenSize)
    window.addEventListener('orientationchange', detectScreenSize)
    
    // Listen for preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', detectUserPreferences)
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', detectUserPreferences)
    window.matchMedia('(prefers-contrast: high)').addEventListener('change', detectUserPreferences)
  }

  const removeEventListeners = () => {
    if (typeof window === 'undefined') return

    window.removeEventListener('resize', detectScreenSize)
    window.removeEventListener('orientationchange', detectScreenSize)
    
    window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', detectUserPreferences)
    window.matchMedia('(prefers-reduced-motion: reduce)').removeEventListener('change', detectUserPreferences)
    window.matchMedia('(prefers-contrast: high)').removeEventListener('change', detectUserPreferences)
  }

  // Initialize everything
  const initialize = () => {
    detectScreenSize()
    detectWebGLCapabilities()
    detectHardwareCapabilities()
    detectUserPreferences()
    optimizeQualitySettings()
    setupEventListeners()
    startPerformanceMonitoring()
  }

  // Lifecycle
  onMounted(() => {
    initialize()
  })

  onUnmounted(() => {
    removeEventListeners()
  })

  return {
    // State
    capabilities: readonly(capabilities),
    qualitySettings: readonly(qualitySettings),
    performanceMetrics: readonly(performanceMetrics),
    
    // Computed
    isLowEndDevice,
    canHandleAdvancedEffects,
    recommendedSettings,
    
    // Methods
    optimizeQualitySettings,
    downgradeQuality,
    upgradeQuality,
    initialize
  }
}
