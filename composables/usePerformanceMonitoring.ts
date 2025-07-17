/**
 * Performance Monitoring Composable
 * Warhammer Tavern v3
 * 
 * Provides utilities for monitoring application performance,
 * including image loading, component rendering, and user interactions
 */

export interface PerformanceMetrics {
  imageLoadTime: number
  componentRenderTime: number
  interactionResponseTime: number
  memoryUsage: number
  networkRequests: number
  errorCount: number
}

export interface PerformanceEntry {
  name: string
  startTime: number
  duration: number
  type: 'image' | 'component' | 'interaction' | 'network'
  metadata?: Record<string, any>
}

export const usePerformanceMonitoring = () => {
  // Performance entries storage
  const performanceEntries = ref<PerformanceEntry[]>([])
  const metrics = ref<PerformanceMetrics>({
    imageLoadTime: 0,
    componentRenderTime: 0,
    interactionResponseTime: 0,
    memoryUsage: 0,
    networkRequests: 0,
    errorCount: 0
  })

  // Performance observer
  let performanceObserver: PerformanceObserver | null = null

  // Initialize performance monitoring
  const initializeMonitoring = () => {
    if (process.client && 'PerformanceObserver' in window) {
      performanceObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries()
        
        entries.forEach((entry) => {
          // Process different types of performance entries
          if (entry.entryType === 'resource') {
            handleResourceEntry(entry as PerformanceResourceTiming)
          } else if (entry.entryType === 'measure') {
            handleMeasureEntry(entry as PerformanceMeasure)
          } else if (entry.entryType === 'navigation') {
            handleNavigationEntry(entry as PerformanceNavigationTiming)
          }
        })
      })

      // Observe different types of performance entries
      try {
        performanceObserver.observe({ 
          entryTypes: ['resource', 'measure', 'navigation'] 
        })
      } catch (error) {
        console.warn('Performance monitoring not fully supported:', error)
      }
    }
  }

  // Handle resource loading entries (images, scripts, etc.)
  const handleResourceEntry = (entry: PerformanceResourceTiming) => {
    const isImage = entry.name.match(/\.(jpg|jpeg|png|gif|webp|avif|svg)(\?.*)?$/i)
    
    if (isImage) {
      const imageEntry: PerformanceEntry = {
        name: entry.name,
        startTime: entry.startTime,
        duration: entry.duration,
        type: 'image',
        metadata: {
          transferSize: entry.transferSize,
          encodedBodySize: entry.encodedBodySize,
          decodedBodySize: entry.decodedBodySize
        }
      }
      
      performanceEntries.value.push(imageEntry)
      updateImageMetrics()
    } else {
      // Track network requests
      metrics.value.networkRequests++
    }
  }

  // Handle custom measure entries
  const handleMeasureEntry = (entry: PerformanceMeasure) => {
    const measureEntry: PerformanceEntry = {
      name: entry.name,
      startTime: entry.startTime,
      duration: entry.duration,
      type: entry.name.includes('component') ? 'component' : 'interaction'
    }
    
    performanceEntries.value.push(measureEntry)
    
    if (entry.name.includes('component')) {
      updateComponentMetrics()
    } else if (entry.name.includes('interaction')) {
      updateInteractionMetrics()
    }
  }

  // Handle navigation entries
  const handleNavigationEntry = (entry: PerformanceNavigationTiming) => {
    // Update overall page performance metrics
    const loadTime = entry.loadEventEnd - entry.navigationStart
    console.log(`Page load time: ${loadTime}ms`)
  }

  // Update image loading metrics
  const updateImageMetrics = () => {
    const imageEntries = performanceEntries.value.filter(e => e.type === 'image')
    if (imageEntries.length > 0) {
      const totalTime = imageEntries.reduce((sum, entry) => sum + entry.duration, 0)
      metrics.value.imageLoadTime = totalTime / imageEntries.length
    }
  }

  // Update component rendering metrics
  const updateComponentMetrics = () => {
    const componentEntries = performanceEntries.value.filter(e => e.type === 'component')
    if (componentEntries.length > 0) {
      const totalTime = componentEntries.reduce((sum, entry) => sum + entry.duration, 0)
      metrics.value.componentRenderTime = totalTime / componentEntries.length
    }
  }

  // Update interaction response metrics
  const updateInteractionMetrics = () => {
    const interactionEntries = performanceEntries.value.filter(e => e.type === 'interaction')
    if (interactionEntries.length > 0) {
      const totalTime = interactionEntries.reduce((sum, entry) => sum + entry.duration, 0)
      metrics.value.interactionResponseTime = totalTime / interactionEntries.length
    }
  }

  // Measure component rendering time
  const measureComponentRender = (componentName: string, renderFn: () => void) => {
    const measureName = `component-render-${componentName}`
    
    performance.mark(`${measureName}-start`)
    renderFn()
    performance.mark(`${measureName}-end`)
    
    performance.measure(measureName, `${measureName}-start`, `${measureName}-end`)
  }

  // Measure interaction response time
  const measureInteraction = async (interactionName: string, interactionFn: () => Promise<void>) => {
    const measureName = `interaction-${interactionName}`
    
    performance.mark(`${measureName}-start`)
    await interactionFn()
    performance.mark(`${measureName}-end`)
    
    performance.measure(measureName, `${measureName}-start`, `${measureName}-end`)
  }

  // Get memory usage (if available)
  const getMemoryUsage = () => {
    if (process.client && 'memory' in performance) {
      const memory = (performance as any).memory
      metrics.value.memoryUsage = memory.usedJSHeapSize / 1024 / 1024 // MB
      return {
        used: memory.usedJSHeapSize / 1024 / 1024,
        total: memory.totalJSHeapSize / 1024 / 1024,
        limit: memory.jsHeapSizeLimit / 1024 / 1024
      }
    }
    return null
  }

  // Track errors
  const trackError = (error: Error, context?: string) => {
    metrics.value.errorCount++
    
    // Log error for debugging
    console.error('Performance tracking error:', {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now()
    })
  }

  // Get performance summary
  const getPerformanceSummary = () => {
    return {
      metrics: { ...metrics.value },
      entries: performanceEntries.value.slice(-50), // Last 50 entries
      memoryUsage: getMemoryUsage(),
      timestamp: Date.now()
    }
  }

  // Clear performance data
  const clearPerformanceData = () => {
    performanceEntries.value = []
    metrics.value = {
      imageLoadTime: 0,
      componentRenderTime: 0,
      interactionResponseTime: 0,
      memoryUsage: 0,
      networkRequests: 0,
      errorCount: 0
    }
  }

  // Check if performance is degraded
  const isPerformanceDegraded = () => {
    const thresholds = {
      imageLoadTime: 2000, // 2 seconds
      componentRenderTime: 100, // 100ms
      interactionResponseTime: 200, // 200ms
      memoryUsage: 100 // 100MB
    }

    return (
      metrics.value.imageLoadTime > thresholds.imageLoadTime ||
      metrics.value.componentRenderTime > thresholds.componentRenderTime ||
      metrics.value.interactionResponseTime > thresholds.interactionResponseTime ||
      metrics.value.memoryUsage > thresholds.memoryUsage
    )
  }

  // Initialize monitoring on mount
  onMounted(() => {
    initializeMonitoring()
    
    // Update memory usage periodically
    const memoryInterval = setInterval(() => {
      getMemoryUsage()
    }, 5000)

    onUnmounted(() => {
      clearInterval(memoryInterval)
      performanceObserver?.disconnect()
    })
  })

  return {
    // State
    performanceEntries: readonly(performanceEntries),
    metrics: readonly(metrics),

    // Methods
    measureComponentRender,
    measureInteraction,
    getMemoryUsage,
    trackError,
    getPerformanceSummary,
    clearPerformanceData,
    isPerformanceDegraded,
    initializeMonitoring
  }
}
