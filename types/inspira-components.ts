// Enhanced TypeScript definitions for Inspira UI Components - Warhammer Tavern v3

// Base types
export type FactionVariant = 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs'
export type SizeVariant = 'sm' | 'md' | 'lg' | 'xl'
export type AnimationEasing = 'linear' | 'ease' | 'ease-in' | 'ease-out' | 'ease-in-out' | 'cubic-bezier'

// Animation configuration
export interface AnimationConfig {
  duration: number
  easing: AnimationEasing | string
  delay?: number
  repeat?: number | 'infinite'
  direction?: 'normal' | 'reverse' | 'alternate' | 'alternate-reverse'
}

// Faction color scheme
export interface FactionColors {
  primary: string
  secondary: string
  accent: string
  background: string
  foreground: string
}

export type FactionColorMap = Record<FactionVariant, FactionColors>

// Base component props
export interface BaseInspiraProps {
  className?: string
  faction?: FactionVariant
  size?: SizeVariant
  disabled?: boolean
}

// Utility types for component composition
export type WithFaction<T> = T & { faction?: FactionVariant }
export type WithAnimation<T> = T & { animation?: Partial<AnimationConfig> }
export type WithResponsive<T> = T & { 
  responsive?: {
    mobile?: Partial<T>
    tablet?: Partial<T>
    desktop?: Partial<T>
  }
}

// Combined utility type
export type InspiraProps<T> = WithFaction<WithAnimation<WithResponsive<T>>>

// MultiStepLoader types
export interface LoadingStep {
  id: string
  title: string
  description: string
  icon: string
  duration: number
  faction?: FactionVariant
  audioSrc?: string
}

export interface MultiStepLoaderProps extends BaseInspiraProps {
  steps: LoadingStep[]
  autoProgress?: boolean
  allowSkip?: boolean
  enableAudio?: boolean
  onComplete?: () => void
  onStepChange?: (step: LoadingStep, index: number) => void
}

export interface MultiStepLoaderExposed {
  nextStep: () => void
  skipLoading: () => void
  currentStep: Readonly<Ref<number>>
  isLoading: Readonly<Ref<boolean>>
}

// BoxReveal types
export type RevealDirection = 'top' | 'bottom' | 'left' | 'right' | 'center'

export interface BoxRevealProps extends BaseInspiraProps {
  revealDirection?: RevealDirection
  revealSpeed?: number
  triggerOnScroll?: boolean
  boxColor?: string
  revealDelay?: number
}

export interface BoxRevealExposed {
  startReveal: () => void
  resetReveal: () => void
  isRevealed: Readonly<Ref<boolean>>
  isRevealing: Readonly<Ref<boolean>>
}

// FocusCards types
export interface CharacterCard {
  id: string
  name: string
  faction: FactionVariant
  avatar?: string
  title?: string
  description: string
  stats?: Record<string, number>
}

export type FocusMode = 'hover' | 'click' | 'auto'

export interface FocusCardsProps extends BaseInspiraProps {
  cards: CharacterCard[]
  focusMode?: FocusMode
  blurIntensity?: number
  scaleIntensity?: number
  gridCols?: 1 | 2 | 3 | 4
}

export interface FocusCardsExposed {
  focusCard: (index: number) => void
  blurAll: () => void
  focusedCard: Readonly<Ref<number | null>>
}

// GlareCard types
export interface GlareCardProps extends BaseInspiraProps {
  glareColor?: string
  glareIntensity?: number
  rotationIntensity?: number
  enableGlare?: boolean
}

// MorphingTabs types
export interface Tab {
  id: string
  label: string
  icon?: string
  disabled?: boolean
  faction?: FactionVariant
}

export type IndicatorStyle = 'underline' | 'background' | 'border'

export interface MorphingTabsProps extends BaseInspiraProps {
  tabs: Tab[]
  activeTab?: string
  morphingSpeed?: number
  indicatorStyle?: IndicatorStyle
}

// Meteors types (optimized)
export interface Sparkle {
  x: number
  y: number
  opacity: number
  size: number
  life: number
}

export interface Meteor {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  size: number
  tailLength: number
  opacity: number
  life: number
  maxLife: number
  sparkles: Sparkle[]
  style?: Record<string, string> // For DOM fallback
}

export interface MeteorsProps extends BaseInspiraProps {
  meteorCount?: number
  meteorSpeed?: number
  meteorSize?: number
  enableCanvas?: boolean
}

export interface MeteorsExposed {
  startAnimation: () => void
  stopAnimation: () => void
  addMeteor: () => void
  clearMeteors: () => void
  getPerformanceStats: () => {
    activeMeteors: number
    pooledMeteors: number
    canvasSupported: boolean
    animationRunning: boolean
  }
}

// Performance monitoring types
export interface PerformanceMetrics {
  fps: number
  frameTime: number
  memoryUsage: number
  activeAnimations: number
  canvasSupported: boolean
}

export interface AdaptiveQualitySettings {
  particleCount: number
  animationQuality: 'low' | 'medium' | 'high'
  enableAdvancedEffects: boolean
  targetFPS: number
}

// Device capability detection
export interface DeviceCapabilities {
  isMobile: boolean
  isLowEnd: boolean
  hasGoodConnection: boolean
  supportsWebGL: boolean
  supportsCanvas: boolean
  hardwareConcurrency: number
}

// Composable return types
export interface UseAdaptivePerformanceReturn {
  deviceCapabilities: ComputedRef<DeviceCapabilities>
  qualitySettings: ComputedRef<AdaptiveQualitySettings>
  performanceMetrics: Ref<PerformanceMetrics>
}

export interface UseTouchOptimizationReturn {
  handleTouchStart: (event: TouchEvent) => void
  handleTouchEnd: (event: TouchEvent, callback: () => void) => void
  isTouchDevice: ComputedRef<boolean>
}

export interface UseAnimationCleanupReturn {
  registerAnimation: (id: string, cleanup: () => void) => void
  unregisterAnimation: (id: string) => void
  cleanupAll: () => void
}

// Event types
export interface InspiraComponentEvents {
  // MultiStepLoader events
  'step-change': [step: LoadingStep, index: number]
  'loading-complete': []
  'loading-skip': []
  
  // BoxReveal events
  'reveal-start': []
  'revealed': []
  
  // FocusCards events
  'card-focus': [card: CharacterCard, index: number]
  'card-blur': []
  'card-click': [card: CharacterCard, index: number]
  
  // Performance events
  'performance-warning': [metric: string, value: number]
  'quality-adjusted': [newQuality: AdaptiveQualitySettings]
}

// Error types
export class InspiraComponentError extends Error {
  constructor(
    message: string,
    public component: string,
    public code?: string
  ) {
    super(message)
    this.name = 'InspiraComponentError'
  }
}

// Validation schemas (for runtime type checking)
export interface ComponentValidationSchema {
  props: Record<string, {
    type: string
    required?: boolean
    default?: any
    validator?: (value: any) => boolean
  }>
}

// Global configuration
export interface InspiraUIConfig {
  defaultFaction: FactionVariant
  enablePerformanceMonitoring: boolean
  adaptiveQuality: boolean
  mobileOptimizations: boolean
  debugMode: boolean
}

// Module augmentation for Vue
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $inspira: {
      config: InspiraUIConfig
      performance: PerformanceMetrics
      utils: {
        getFactionColors: (faction: FactionVariant) => FactionColors
        detectDevice: () => DeviceCapabilities
        optimizeForDevice: (device: DeviceCapabilities) => AdaptiveQualitySettings
      }
    }
  }
}
