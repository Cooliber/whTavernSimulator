/**
 * Screen Reader Composable
 * Provides accessibility utilities for screen reader support
 */

export interface AnnouncementOptions {
  priority?: 'polite' | 'assertive'
  atomic?: boolean
  delay?: number
  clear?: boolean
}

export interface NavigationContext {
  currentPage: string
  currentSection: string
  totalItems?: number
  currentItem?: number
  hasNext?: boolean
  hasPrevious?: boolean
}

export function useScreenReader() {
  // State
  const isScreenReaderActive = ref(false)
  const currentContext = ref<NavigationContext>({
    currentPage: '',
    currentSection: ''
  })
  const announcementQueue = ref<string[]>([])
  const isAnnouncing = ref(false)

  // Screen reader detection
  const detectScreenReader = () => {
    if (typeof window === 'undefined') return false

    // Check for common screen reader indicators
    const indicators = [
      // NVDA
      () => 'speechSynthesis' in window && navigator.userAgent.includes('NVDA'),
      // JAWS
      () => 'speechSynthesis' in window && navigator.userAgent.includes('JAWS'),
      // VoiceOver (macOS/iOS)
      () => 'speechSynthesis' in window && /Mac|iPhone|iPad/.test(navigator.userAgent),
      // Windows Narrator
      () => 'speechSynthesis' in window && navigator.userAgent.includes('Windows NT'),
      // General accessibility preference
      () => window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      // High contrast mode (often used with screen readers)
      () => window.matchMedia('(prefers-contrast: high)').matches
    ]

    isScreenReaderActive.value = indicators.some(check => check())
    return isScreenReaderActive.value
  }

  // Core announcement function
  const announceToScreenReader = (
    message: string, 
    options: AnnouncementOptions = {}
  ) => {
    if (!message.trim()) return

    const {
      priority = 'polite',
      atomic = true,
      delay = 0,
      clear = false
    } = options

    // Clear previous announcements if requested
    if (clear) {
      clearAnnouncements()
    }

    const announce = () => {
      const announcement = document.createElement('div')
      announcement.setAttribute('aria-live', priority)
      announcement.setAttribute('aria-atomic', atomic.toString())
      announcement.className = 'sr-only'
      announcement.textContent = message

      // Add to DOM
      document.body.appendChild(announcement)

      // Remove after announcement
      setTimeout(() => {
        if (announcement.parentNode) {
          document.body.removeChild(announcement)
        }
      }, 1000)
    }

    if (delay > 0) {
      setTimeout(announce, delay)
    } else {
      announce()
    }
  }

  // Queue management for multiple announcements
  const queueAnnouncement = (message: string, options: AnnouncementOptions = {}) => {
    announcementQueue.value.push(message)
    processAnnouncementQueue(options)
  }

  const processAnnouncementQueue = async (options: AnnouncementOptions = {}) => {
    if (isAnnouncing.value || announcementQueue.value.length === 0) return

    isAnnouncing.value = true

    while (announcementQueue.value.length > 0) {
      const message = announcementQueue.value.shift()
      if (message) {
        announceToScreenReader(message, options)
        // Wait between announcements
        await new Promise(resolve => setTimeout(resolve, 500))
      }
    }

    isAnnouncing.value = false
  }

  const clearAnnouncements = () => {
    announcementQueue.value = []
    isAnnouncing.value = false
    
    // Remove existing announcement elements
    const existingAnnouncements = document.querySelectorAll('[aria-live]')
    existingAnnouncements.forEach(el => {
      if (el.parentNode) {
        el.parentNode.removeChild(el)
      }
    })
  }

  // Context-aware announcements
  const announcePageChange = (pageName: string, description?: string) => {
    currentContext.value.currentPage = pageName
    const message = description 
      ? `Navigated to ${pageName}. ${description}`
      : `Navigated to ${pageName}`
    
    announceToScreenReader(message, { priority: 'assertive', clear: true })
  }

  const announceSectionChange = (sectionName: string, description?: string) => {
    currentContext.value.currentSection = sectionName
    const message = description
      ? `Entered ${sectionName} section. ${description}`
      : `Entered ${sectionName} section`
    
    announceToScreenReader(message, { priority: 'polite' })
  }

  const announceListNavigation = (
    currentItem: number,
    totalItems: number,
    itemDescription?: string
  ) => {
    currentContext.value.currentItem = currentItem
    currentContext.value.totalItems = totalItems
    currentContext.value.hasNext = currentItem < totalItems
    currentContext.value.hasPrevious = currentItem > 1

    const message = itemDescription
      ? `Item ${currentItem} of ${totalItems}: ${itemDescription}`
      : `Item ${currentItem} of ${totalItems}`
    
    announceToScreenReader(message, { priority: 'polite' })
  }

  // Warhammer-specific announcements
  const announceCharacterDetails = (character: any) => {
    const message = `Character: ${character.name}, ${character.class} from ${character.faction}. 
                    Attack: ${character.stats?.attack || 'unknown'}, 
                    Defense: ${character.stats?.defense || 'unknown'}`
    
    announceToScreenReader(message, { priority: 'polite' })
  }

  const announceWeatherChange = (weather: string, intensity?: number) => {
    const intensityText = intensity ? `, intensity ${Math.round(intensity * 100)}%` : ''
    const message = `Weather changed to ${weather}${intensityText}`
    
    announceToScreenReader(message, { priority: 'polite' })
  }

  const announceQuestUpdate = (questTitle: string, status: string) => {
    const message = `Quest update: ${questTitle} is now ${status}`
    announceToScreenReader(message, { priority: 'assertive' })
  }

  const announceInventoryChange = (action: string, itemName: string, quantity?: number) => {
    const quantityText = quantity ? ` ${quantity}` : ''
    const message = `${action}${quantityText} ${itemName} ${action === 'Added' ? 'to' : 'from'} inventory`
    
    announceToScreenReader(message, { priority: 'polite' })
  }

  const announceCombatAction = (attacker: string, target: string, damage?: number) => {
    const damageText = damage ? ` for ${damage} damage` : ''
    const message = `${attacker} attacks ${target}${damageText}`
    
    announceToScreenReader(message, { priority: 'assertive' })
  }

  // Keyboard navigation helpers
  const announceKeyboardShortcuts = () => {
    const shortcuts = [
      'Tab to navigate between elements',
      'Enter or Space to activate buttons',
      'Arrow keys to navigate lists',
      'Escape to close dialogs',
      'H to jump between headings'
    ]
    
    const message = `Keyboard shortcuts available: ${shortcuts.join(', ')}`
    announceToScreenReader(message, { priority: 'polite' })
  }

  const announceFormValidation = (errors: string[]) => {
    if (errors.length === 0) {
      announceToScreenReader('Form is valid', { priority: 'polite' })
    } else {
      const message = `Form has ${errors.length} error${errors.length > 1 ? 's' : ''}: ${errors.join(', ')}`
      announceToScreenReader(message, { priority: 'assertive' })
    }
  }

  // Loading and progress announcements
  const announceLoading = (description: string) => {
    announceToScreenReader(`Loading ${description}`, { priority: 'polite' })
  }

  const announceLoadingComplete = (description: string) => {
    announceToScreenReader(`${description} loaded`, { priority: 'polite' })
  }

  const announceProgress = (percentage: number, description?: string) => {
    const desc = description ? ` ${description}` : ''
    const message = `Progress:${desc} ${percentage}% complete`
    announceToScreenReader(message, { priority: 'polite' })
  }

  // Error and success announcements
  const announceError = (error: string) => {
    announceToScreenReader(`Error: ${error}`, { priority: 'assertive', clear: true })
  }

  const announceSuccess = (message: string) => {
    announceToScreenReader(`Success: ${message}`, { priority: 'polite' })
  }

  const announceWarning = (warning: string) => {
    announceToScreenReader(`Warning: ${warning}`, { priority: 'assertive' })
  }

  // Utility functions
  const createAriaLabel = (base: string, context?: string) => {
    return context ? `${base}, ${context}` : base
  }

  const createAriaDescription = (items: string[]) => {
    return items.filter(Boolean).join(', ')
  }

  const formatForScreenReader = (text: string) => {
    return text
      .replace(/([A-Z])/g, ' $1') // Add spaces before capital letters
      .replace(/\s+/g, ' ') // Normalize whitespace
      .trim()
  }

  // Focus management
  const manageFocus = (element: HTMLElement, announce = true) => {
    if (!element) return

    element.focus()
    
    if (announce) {
      const label = element.getAttribute('aria-label') || 
                   element.getAttribute('title') || 
                   element.textContent || 
                   'Element'
      
      announceToScreenReader(`Focused on ${formatForScreenReader(label)}`, { 
        priority: 'polite',
        delay: 100 
      })
    }
  }

  const trapFocus = (container: HTMLElement) => {
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    
    const firstElement = focusableElements[0] as HTMLElement
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus()
          e.preventDefault()
        }
      }
    }

    container.addEventListener('keydown', handleTabKey)
    
    return () => {
      container.removeEventListener('keydown', handleTabKey)
    }
  }

  // Initialize
  onMounted(() => {
    detectScreenReader()
    
    // Announce page load
    if (isScreenReaderActive.value) {
      announceToScreenReader('Warhammer Tavern Simulator loaded', { 
        priority: 'polite',
        delay: 1000 
      })
    }
  })

  return {
    // State
    isScreenReaderActive: readonly(isScreenReaderActive),
    currentContext: readonly(currentContext),
    
    // Core functions
    announceToScreenReader,
    queueAnnouncement,
    clearAnnouncements,
    
    // Context announcements
    announcePageChange,
    announceSectionChange,
    announceListNavigation,
    
    // Warhammer-specific
    announceCharacterDetails,
    announceWeatherChange,
    announceQuestUpdate,
    announceInventoryChange,
    announceCombatAction,
    
    // UI helpers
    announceKeyboardShortcuts,
    announceFormValidation,
    announceLoading,
    announceLoadingComplete,
    announceProgress,
    announceError,
    announceSuccess,
    announceWarning,
    
    // Utilities
    createAriaLabel,
    createAriaDescription,
    formatForScreenReader,
    manageFocus,
    trapFocus,
    
    // Detection
    detectScreenReader
  }
}
