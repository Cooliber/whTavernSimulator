/**
 * Warhammer Images Management Composable
 * Handles image optimization, lazy loading, and accessibility for Warhammer Fantasy assets
 */

export interface WarhammerImage {
  src: string
  alt: string
  title?: string
  width?: number
  height?: number
  category: 'faction' | 'character' | 'atmosphere' | 'texture' | 'icon'
  faction?: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
  lazy?: boolean
}

export interface ImageSizes {
  thumbnail: string
  small: string
  medium: string
  large: string
  original: string
}

export const useWarhammerImages = () => {
  // Available Warhammer images
  const availableImages = ref<WarhammerImage[]>([
    {
      src: '/warhammer-images/baronia.webp',
      alt: 'Baronia - Warhammer Fantasy map and heraldic design',
      title: 'The lands of Baronia in the Old World',
      category: 'atmosphere',
      width: 800,
      height: 600,
      lazy: true
    },
    {
      src: '/warhammer-images/vientos.webp',
      alt: 'Vientos - Warhammer Fantasy atmospheric artwork',
      title: 'The winds of magic in the Old World',
      category: 'atmosphere',
      width: 800,
      height: 600,
      lazy: true
    }
  ])

  // Faction-specific placeholder images (using CSS gradients as fallbacks)
  const factionPlaceholders = {
    empire: {
      background: 'linear-gradient(135deg, #FFD700 0%, #B8860B 100%)',
      icon: '⚔️',
      color: '#FFD700'
    },
    chaos: {
      background: 'linear-gradient(135deg, #B71C1C 0%, #8B0000 100%)',
      icon: '☠️',
      color: '#B71C1C'
    },
    elves: {
      background: 'linear-gradient(135deg, #2E8B57 0%, #228B22 100%)',
      icon: '🏹',
      color: '#2E8B57'
    },
    dwarfs: {
      background: 'linear-gradient(135deg, #CD853F 0%, #A0522D 100%)',
      icon: '⚒️',
      color: '#CD853F'
    },
    undead: {
      background: 'linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%)',
      icon: '💀',
      color: '#8A2BE2'
    },
    orcs: {
      background: 'linear-gradient(135deg, #6B8E23 0%, #556B2F 100%)',
      icon: '⚔️',
      color: '#6B8E23'
    }
  }

  // Generate responsive image sizes
  const generateImageSizes = (baseSrc: string): ImageSizes => {
    // For now, we'll use the same image for all sizes
    // In a production app, you'd have different sized versions
    return {
      thumbnail: baseSrc,
      small: baseSrc,
      medium: baseSrc,
      large: baseSrc,
      original: baseSrc
    }
  }

  // Get image by category
  const getImagesByCategory = (category: WarhammerImage['category']) => {
    return availableImages.value.filter(img => img.category === category)
  }

  // Get faction-specific images
  const getFactionImages = (faction: WarhammerImage['faction']) => {
    return availableImages.value.filter(img => img.faction === faction)
  }

  // Get random atmospheric image
  const getRandomAtmosphericImage = () => {
    const atmosphericImages = getImagesByCategory('atmosphere')
    if (atmosphericImages.length === 0) return null
    
    const randomIndex = Math.floor(Math.random() * atmosphericImages.length)
    return atmosphericImages[randomIndex]
  }

  // Create faction placeholder
  const createFactionPlaceholder = (
    faction: keyof typeof factionPlaceholders,
    size: 'small' | 'medium' | 'large' = 'medium'
  ) => {
    const placeholder = factionPlaceholders[faction]
    const dimensions = {
      small: { width: 64, height: 64 },
      medium: { width: 128, height: 128 },
      large: { width: 256, height: 256 }
    }
    
    return {
      background: placeholder.background,
      icon: placeholder.icon,
      color: placeholder.color,
      ...dimensions[size]
    }
  }

  // Optimize image loading with intersection observer
  const useImageLazyLoading = () => {
    const imageRefs = ref<HTMLImageElement[]>([])
    const observer = ref<IntersectionObserver | null>(null)

    const observeImage = (img: HTMLImageElement) => {
      if (!observer.value) {
        observer.value = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                const img = entry.target as HTMLImageElement
                const dataSrc = img.getAttribute('data-src')
                
                if (dataSrc) {
                  img.src = dataSrc
                  img.removeAttribute('data-src')
                  observer.value?.unobserve(img)
                }
              }
            })
          },
          {
            rootMargin: '50px 0px',
            threshold: 0.1
          }
        )
      }

      observer.value.observe(img)
      imageRefs.value.push(img)
    }

    const cleanup = () => {
      if (observer.value) {
        imageRefs.value.forEach(img => observer.value?.unobserve(img))
        observer.value.disconnect()
      }
    }

    onUnmounted(cleanup)

    return { observeImage, cleanup }
  }

  // Generate srcset for responsive images
  const generateSrcSet = (image: WarhammerImage) => {
    const sizes = generateImageSizes(image.src)
    return `${sizes.small} 400w, ${sizes.medium} 800w, ${sizes.large} 1200w`
  }

  // Generate sizes attribute for responsive images
  const generateSizesAttribute = (breakpoints?: string) => {
    return breakpoints || '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw'
  }

  // Preload critical images
  const preloadImage = (src: string) => {
    return new Promise<void>((resolve, reject) => {
      const img = new Image()
      img.onload = () => resolve()
      img.onerror = () => reject(new Error(`Failed to load image: ${src}`))
      img.src = src
    })
  }

  // Preload all atmospheric images for better UX
  const preloadAtmosphericImages = async () => {
    const atmosphericImages = getImagesByCategory('atmosphere')
    const preloadPromises = atmosphericImages.map(img => preloadImage(img.src))
    
    try {
      await Promise.all(preloadPromises)
      console.log('✅ Atmospheric images preloaded successfully')
    } catch (error) {
      console.warn('⚠️ Some atmospheric images failed to preload:', error)
    }
  }

  // Get optimized image props for components
  const getOptimizedImageProps = (
    image: WarhammerImage,
    options?: {
      sizes?: string
      loading?: 'lazy' | 'eager'
      priority?: boolean
    }
  ) => {
    const { sizes, loading = 'lazy', priority = false } = options || {}

    return {
      src: image.src,
      alt: image.alt,
      title: image.title,
      width: image.width,
      height: image.height,
      loading: priority ? 'eager' : loading,
      srcset: generateSrcSet(image),
      sizes: sizes || generateSizesAttribute(),
      decoding: 'async' as const,
      'data-category': image.category,
      'data-faction': image.faction
    }
  }

  // Create CSS background image with optimization
  const createBackgroundImage = (
    image: WarhammerImage,
    options?: {
      size?: 'cover' | 'contain' | 'auto'
      position?: string
      repeat?: 'no-repeat' | 'repeat' | 'repeat-x' | 'repeat-y'
      opacity?: number
    }
  ) => {
    const { size = 'cover', position = 'center', repeat = 'no-repeat', opacity = 1 } = options || {}

    return {
      backgroundImage: `url(${image.src})`,
      backgroundSize: size,
      backgroundPosition: position,
      backgroundRepeat: repeat,
      opacity
    }
  }

  // Add new image to collection
  const addImage = (image: WarhammerImage) => {
    availableImages.value.push(image)
  }

  // Remove image from collection
  const removeImage = (src: string) => {
    const index = availableImages.value.findIndex(img => img.src === src)
    if (index > -1) {
      availableImages.value.splice(index, 1)
    }
  }

  return {
    // Data
    availableImages: readonly(availableImages),
    factionPlaceholders,

    // Methods
    generateImageSizes,
    getImagesByCategory,
    getFactionImages,
    getRandomAtmosphericImage,
    createFactionPlaceholder,
    useImageLazyLoading,
    generateSrcSet,
    generateSizesAttribute,
    preloadImage,
    preloadAtmosphericImages,
    getOptimizedImageProps,
    createBackgroundImage,
    addImage,
    removeImage
  }
}
