/**
 * Warhammer Theme Composable
 * Provides faction colors, theme utilities, and atmospheric effects
 */

export interface FactionColors {
  primary: string
  secondary: string
  accent: string
  text: string
  background: string
}

export type FactionType = 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'

export function useWarhammerTheme() {
  // Faction color definitions
  const factionColors: Record<FactionType, FactionColors> = {
    empire: {
      primary: '#ffd700',
      secondary: '#b8860b',
      accent: '#daa520',
      text: '#2f1b14',
      background: 'rgba(255, 215, 0, 0.1)'
    },
    chaos: {
      primary: '#dc143c',
      secondary: '#8b0000',
      accent: '#ff4500',
      text: '#ffffff',
      background: 'rgba(220, 20, 60, 0.1)'
    },
    elves: {
      primary: '#32cd32',
      secondary: '#228b22',
      accent: '#90ee90',
      text: '#ffffff',
      background: 'rgba(50, 205, 50, 0.1)'
    },
    dwarfs: {
      primary: '#cd853f',
      secondary: '#a0522d',
      accent: '#deb887',
      text: '#2f1b14',
      background: 'rgba(205, 133, 63, 0.1)'
    },
    undead: {
      primary: '#9400d3',
      secondary: '#8b008b',
      accent: '#dda0dd',
      text: '#ffffff',
      background: 'rgba(148, 0, 211, 0.1)'
    },
    orcs: {
      primary: '#6b8e23',
      secondary: '#556b2f',
      accent: '#9acd32',
      text: '#ffffff',
      background: 'rgba(107, 142, 35, 0.1)'
    }
  }

  // Current theme state
  const currentFaction = ref<FactionType>('empire')
  const isDarkMode = ref(true)
  const atmosphereIntensity = ref(0.7)

  // Get faction colors
  const getFactionColors = (faction: FactionType): FactionColors => {
    return factionColors[faction] || factionColors.empire
  }

  // Get current faction colors
  const currentColors = computed(() => getFactionColors(currentFaction.value))

  // Apply faction theme as CSS custom properties
  const applyFactionTheme = (faction: FactionType) => {
    const colors = getFactionColors(faction)
    return {
      '--faction-primary': colors.primary,
      '--faction-secondary': colors.secondary,
      '--faction-accent': colors.accent,
      '--faction-text': colors.text,
      '--faction-background': colors.background
    }
  }

  // Generate faction-specific CSS classes
  const getFactionClasses = (faction: FactionType) => {
    return {
      [`faction-${faction}`]: true,
      'faction-theme': true
    }
  }

  // Atmospheric color schemes
  const atmosphericColors = {
    tavern: {
      warm: ['#8b4513', '#a0522d', '#cd853f', '#daa520'],
      cool: ['#2f4f4f', '#708090', '#778899', '#b0c4de'],
      mystical: ['#4b0082', '#8b008b', '#9400d3', '#dda0dd']
    },
    weather: {
      sunny: ['#ffd700', '#ffeb3b', '#fff176'],
      rainy: ['#607d8b', '#90a4ae', '#b0bec5'],
      stormy: ['#37474f', '#546e7a', '#78909c'],
      foggy: ['#eceff1', '#cfd8dc', '#b0bec5']
    }
  }

  // Get atmospheric colors based on conditions
  const getAtmosphericColors = (type: 'tavern' | 'weather', condition: string) => {
    return atmosphericColors[type]?.[condition] || atmosphericColors.tavern.warm
  }

  // Generate gradient backgrounds
  const createFactionGradient = (faction: FactionType, direction = 'to right') => {
    const colors = getFactionColors(faction)
    return `linear-gradient(${direction}, ${colors.primary}, ${colors.secondary})`
  }

  // Create atmospheric background
  const createAtmosphericBackground = (
    baseColors: string[],
    intensity: number = atmosphereIntensity.value
  ) => {
    const opacity = Math.max(0.1, Math.min(1, intensity))
    return {
      backgroundImage: `
        radial-gradient(circle at 20% 80%, ${baseColors[0]}${Math.round(opacity * 255).toString(16)} 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, ${baseColors[1]}${Math.round(opacity * 255).toString(16)} 0%, transparent 50%),
        linear-gradient(135deg, ${baseColors[2]}${Math.round(opacity * 0.8 * 255).toString(16)} 0%, ${baseColors[3]}${Math.round(opacity * 0.6 * 255).toString(16)} 100%)
      `
    }
  }

  // Theme transition utilities
  const transitionToFaction = (faction: FactionType, duration = 500) => {
    currentFaction.value = faction
    
    // Apply CSS custom properties with transition
    const root = document.documentElement
    const colors = getFactionColors(faction)
    
    root.style.setProperty('--transition-duration', `${duration}ms`)
    Object.entries(applyFactionTheme(faction)).forEach(([property, value]) => {
      root.style.setProperty(property, value)
    })
  }

  // Accessibility helpers
  const getContrastColor = (backgroundColor: string): string => {
    // Simple contrast calculation - in production, use a proper contrast library
    const hex = backgroundColor.replace('#', '')
    const r = parseInt(hex.substr(0, 2), 16)
    const g = parseInt(hex.substr(2, 2), 16)
    const b = parseInt(hex.substr(4, 2), 16)
    const brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness > 128 ? '#000000' : '#ffffff'
  }

  // High contrast mode support
  const isHighContrast = ref(false)
  
  const checkHighContrast = () => {
    if (typeof window !== 'undefined') {
      isHighContrast.value = window.matchMedia('(prefers-contrast: high)').matches
    }
  }

  // Reduced motion support
  const prefersReducedMotion = ref(false)
  
  const checkReducedMotion = () => {
    if (typeof window !== 'undefined') {
      prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    }
  }

  // Initialize accessibility preferences
  onMounted(() => {
    checkHighContrast()
    checkReducedMotion()
    
    // Listen for changes
    if (typeof window !== 'undefined') {
      window.matchMedia('(prefers-contrast: high)').addEventListener('change', checkHighContrast)
      window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', checkReducedMotion)
    }
  })

  onUnmounted(() => {
    if (typeof window !== 'undefined') {
      window.matchMedia('(prefers-contrast: high)').removeEventListener('change', checkHighContrast)
      window.matchMedia('(prefers-reduced-motion: reduce)').removeEventListener('change', checkReducedMotion)
    }
  })

  // Utility functions
  const hexToRgba = (hex: string, alpha: number = 1): string => {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
  }

  const lightenColor = (color: string, amount: number): string => {
    const num = parseInt(color.replace('#', ''), 16)
    const amt = Math.round(2.55 * amount)
    const R = (num >> 16) + amt
    const G = (num >> 8 & 0x00FF) + amt
    const B = (num & 0x0000FF) + amt
    return '#' + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
      (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
      (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)
  }

  const darkenColor = (color: string, amount: number): string => {
    return lightenColor(color, -amount)
  }

  return {
    // State
    currentFaction: readonly(currentFaction),
    currentColors,
    isDarkMode: readonly(isDarkMode),
    atmosphereIntensity: readonly(atmosphereIntensity),
    isHighContrast: readonly(isHighContrast),
    prefersReducedMotion: readonly(prefersReducedMotion),
    
    // Core functions
    getFactionColors,
    applyFactionTheme,
    getFactionClasses,
    getAtmosphericColors,
    createFactionGradient,
    createAtmosphericBackground,
    transitionToFaction,
    
    // Accessibility
    getContrastColor,
    
    // Utilities
    hexToRgba,
    lightenColor,
    darkenColor,
    
    // Constants
    factionColors,
    atmosphericColors
  }
}
