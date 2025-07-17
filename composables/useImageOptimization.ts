/**
 * Image Optimization Composable
 * Warhammer Tavern v3
 * 
 * Provides utilities for optimizing image loading and display
 */

export interface ImageOptimizationOptions {
  lazy?: boolean
  progressive?: boolean
  responsive?: boolean
  quality?: number
  format?: 'webp' | 'avif' | 'jpg' | 'png'
  sizes?: string[]
  aspectRatio?: number
  placeholder?: string
}

export interface OptimizedImage {
  src: string
  srcSet?: string
  placeholder?: string
  loaded: Ref<boolean>
  error: Ref<boolean>
  loading: Ref<boolean>
}

export const useImageOptimization = () => {
  // Image format support detection
  const supportsWebP = ref<boolean | null>(null)
  const supportsAVIF = ref<boolean | null>(null)

  // Check format support
  const checkFormatSupport = async () => {
    if (process.client) {
      // Check WebP support
      const webpCanvas = document.createElement('canvas')
      webpCanvas.width = 1
      webpCanvas.height = 1
      const webpDataUrl = webpCanvas.toDataURL('image/webp')
      supportsWebP.value = webpDataUrl.indexOf('data:image/webp') === 0

      // Check AVIF support
      try {
        const avifImage = new Image()
        const avifPromise = new Promise((resolve) => {
          avifImage.onload = () => resolve(true)
          avifImage.onerror = () => resolve(false)
        })
        avifImage.src = 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAB0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIAAYAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACVtZGF0EgAKCBgABogQEAwgMg8f8D///8WfhwB8+ErK42A='
        supportsAVIF.value = await avifPromise as boolean
      } catch {
        supportsAVIF.value = false
      }
    }
  }

  // Initialize format support check
  onMounted(() => {
    checkFormatSupport()
  })

  // Generate optimized image URL
  const getOptimizedImageUrl = (
    originalUrl: string,
    options: ImageOptimizationOptions = {}
  ): string => {
    const {
      quality = 85,
      format,
      responsive = false
    } = options

    // If it's already an optimized URL or external URL, return as-is
    if (originalUrl.includes('?') || originalUrl.startsWith('http')) {
      return originalUrl
    }

    // Determine best format
    let targetFormat = format
    if (!targetFormat) {
      if (supportsAVIF.value) {
        targetFormat = 'avif'
      } else if (supportsWebP.value) {
        targetFormat = 'webp'
      } else {
        targetFormat = 'jpg'
      }
    }

    // Build optimization parameters
    const params = new URLSearchParams()
    params.set('q', quality.toString())
    params.set('f', targetFormat)

    if (responsive) {
      params.set('responsive', 'true')
    }

    return `${originalUrl}?${params.toString()}`
  }

  // Generate responsive srcSet
  const generateSrcSet = (
    originalUrl: string,
    sizes: number[] = [320, 640, 1024, 1280, 1920],
    options: ImageOptimizationOptions = {}
  ): string => {
    return sizes
      .map(size => {
        const optimizedUrl = getOptimizedImageUrl(originalUrl, {
          ...options,
          responsive: true
        })
        return `${optimizedUrl}&w=${size} ${size}w`
      })
      .join(', ')
  }

  // Create optimized image object
  const createOptimizedImage = (
    src: string,
    options: ImageOptimizationOptions = {}
  ): OptimizedImage => {
    const loaded = ref(false)
    const error = ref(false)
    const loading = ref(true)

    const optimizedSrc = getOptimizedImageUrl(src, options)
    const srcSet = options.responsive 
      ? generateSrcSet(src, options.sizes?.map(s => parseInt(s)) || undefined, options)
      : undefined

    // Generate placeholder
    let placeholder = options.placeholder
    if (!placeholder && options.progressive) {
      // Create a low-quality placeholder
      placeholder = getOptimizedImageUrl(src, {
        ...options,
        quality: 10,
        responsive: false
      })
    }

    return {
      src: optimizedSrc,
      srcSet,
      placeholder,
      loaded,
      error,
      loading
    }
  }

  // Lazy loading utility
  const useLazyImage = (
    src: string,
    options: ImageOptimizationOptions = {}
  ) => {
    const imageRef = ref<HTMLImageElement>()
    const optimizedImage = createOptimizedImage(src, options)

    const observer = ref<IntersectionObserver>()

    const startLoading = () => {
      if (optimizedImage.loading.value && !optimizedImage.loaded.value) {
        const img = new Image()
        
        img.onload = () => {
          optimizedImage.loaded.value = true
          optimizedImage.loading.value = false
          optimizedImage.error.value = false
        }
        
        img.onerror = () => {
          optimizedImage.error.value = true
          optimizedImage.loading.value = false
        }

        img.src = optimizedImage.src
        if (optimizedImage.srcSet) {
          img.srcset = optimizedImage.srcSet
        }
      }
    }

    onMounted(() => {
      if (process.client && options.lazy && imageRef.value) {
        observer.value = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                startLoading()
                observer.value?.unobserve(entry.target)
              }
            })
          },
          { threshold: 0.1 }
        )

        observer.value.observe(imageRef.value)
      } else {
        // Load immediately if not lazy
        startLoading()
      }
    })

    onUnmounted(() => {
      observer.value?.disconnect()
    })

    return {
      imageRef,
      ...optimizedImage
    }
  }

  // Preload critical images
  const preloadImage = (src: string, options: ImageOptimizationOptions = {}) => {
    if (process.client) {
      const link = document.createElement('link')
      link.rel = 'preload'
      link.as = 'image'
      link.href = getOptimizedImageUrl(src, options)
      
      if (options.responsive) {
        link.setAttribute('imagesrcset', generateSrcSet(src, undefined, options))
      }
      
      document.head.appendChild(link)
    }
  }

  // Background image optimization
  const useOptimizedBackground = (
    src: string,
    options: ImageOptimizationOptions = {}
  ) => {
    const backgroundStyle = computed(() => {
      const optimizedUrl = getOptimizedImageUrl(src, options)
      return {
        backgroundImage: `url(${optimizedUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }
    })

    return { backgroundStyle }
  }

  // Image compression utility
  const compressImage = async (
    file: File,
    maxWidth: number = 1920,
    maxHeight: number = 1080,
    quality: number = 0.8
  ): Promise<Blob> => {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')!
      const img = new Image()

      img.onload = () => {
        // Calculate new dimensions
        let { width, height } = img

        if (width > maxWidth) {
          height = (height * maxWidth) / width
          width = maxWidth
        }

        if (height > maxHeight) {
          width = (width * maxHeight) / height
          height = maxHeight
        }

        canvas.width = width
        canvas.height = height

        // Draw and compress
        ctx.drawImage(img, 0, 0, width, height)
        canvas.toBlob(resolve, 'image/jpeg', quality)
      }

      img.src = URL.createObjectURL(file)
    })
  }

  return {
    // State
    supportsWebP: readonly(supportsWebP),
    supportsAVIF: readonly(supportsAVIF),

    // Methods
    getOptimizedImageUrl,
    generateSrcSet,
    createOptimizedImage,
    useLazyImage,
    preloadImage,
    useOptimizedBackground,
    compressImage,
    checkFormatSupport
  }
}
