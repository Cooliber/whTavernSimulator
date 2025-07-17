import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import pl from '../locales/pl.json'
import en from '../locales/en.json'

// Mock component for testing translations
const TestComponent = {
  template: `
    <div>
      <h1>{{ $t('hero.title') }}</h1>
      <p>{{ $t('hero.description', { aiNpcs: $t('hero.aiNpcs'), inspiraUi: $t('hero.inspiraUi') }) }}</p>
      <button>{{ $t('hero.enterTavern') }}</button>
    </div>
  `
}

describe('Polish Localization', () => {
  let i18n: any

  beforeEach(() => {
    i18n = createI18n({
      locale: 'pl',
      fallbackLocale: 'en',
      messages: {
        pl,
        en
      }
    })
  })

  it('should load Polish translations correctly', () => {
    expect(pl.hero.title).toBe('Witaj w Karczmie Warhammer')
    expect(pl.navigation.tavern).toBe('Karczma')
    expect(pl.characters.title).toBe('Poznaj Mieszkańców Karczmy')
  })

  it('should have all required translation keys', () => {
    const requiredKeys = [
      'navigation.home',
      'navigation.tavern',
      'navigation.characters',
      'navigation.conversations',
      'navigation.quests',
      'navigation.inventory',
      'hero.title',
      'hero.subtitle',
      'hero.description',
      'hero.enterTavern',
      'characters.title',
      'characters.subtitle',
      'conversations.title',
      'conversations.multiAgent.title',
      'common.loading',
      'common.error',
      'accessibility.skipToContent'
    ]

    requiredKeys.forEach(key => {
      const keys = key.split('.')
      let current = pl
      for (const k of keys) {
        expect(current).toHaveProperty(k)
        current = current[k]
      }
      expect(typeof current).toBe('string')
      expect(current.length).toBeGreaterThan(0)
    })
  })

  it('should render Polish text in components', () => {
    const wrapper = mount(TestComponent, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.find('h1').text()).toBe('Witaj w Karczmie Warhammer')
    expect(wrapper.find('button').text()).toBe('Wejdź do Karczmy')
  })

  it('should handle interpolation correctly', () => {
    const wrapper = mount(TestComponent, {
      global: {
        plugins: [i18n]
      }
    })

    const description = wrapper.find('p').text()
    expect(description).toContain('NPC sterowane przez AI')
    expect(description).toContain('Inspira UI')
  })

  it('should fallback to English when Polish translation is missing', () => {
    // Create i18n with incomplete Polish translations
    const incompleteI18n = createI18n({
      locale: 'pl',
      fallbackLocale: 'en',
      messages: {
        pl: {
          hero: {
            title: 'Witaj w Karczmie Warhammer'
            // Missing other keys
          }
        },
        en
      }
    })

    const wrapper = mount({
      template: '<div>{{ $t("hero.subtitle") }}</div>'
    }, {
      global: {
        plugins: [incompleteI18n]
      }
    })

    expect(wrapper.text()).toBe('Simulator v3') // Should fallback to English
  })

  it('should handle pluralization correctly', () => {
    const testI18n = createI18n({
      locale: 'pl',
      fallbackLocale: 'en',
      messages: {
        pl: {
          events: {
            timeAgo: {
              hours: '{count} godzin temu',
              hour: 'godzinę temu'
            }
          }
        },
        en
      }
    })

    const wrapper = mount({
      template: '<div>{{ $t("events.timeAgo.hours", { count: 5 }) }}</div>'
    }, {
      global: {
        plugins: [testI18n]
      }
    })

    expect(wrapper.text()).toBe('5 godzin temu')
  })

  it('should maintain consistent translation structure between languages', () => {
    // Check that Polish and English have the same structure
    const checkStructure = (obj1: any, obj2: any, path = '') => {
      for (const key in obj1) {
        const currentPath = path ? `${path}.${key}` : key
        
        if (typeof obj1[key] === 'object' && obj1[key] !== null) {
          expect(obj2).toHaveProperty(key, `Missing key in English: ${currentPath}`)
          checkStructure(obj1[key], obj2[key], currentPath)
        } else {
          expect(obj2).toHaveProperty(key, `Missing translation key: ${currentPath}`)
          expect(typeof obj2[key]).toBe('string', `Type mismatch for key: ${currentPath}`)
        }
      }
    }

    checkStructure(pl, en)
    checkStructure(en, pl)
  })

  it('should handle special Polish characters correctly', () => {
    const polishChars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
    const hasPolishChars = JSON.stringify(pl).split('').some(char => 
      polishChars.includes(char.toLowerCase())
    )
    
    expect(hasPolishChars).toBe(true)
  })

  it('should have appropriate text length for UI elements', () => {
    // Check that translations are not too long for UI elements
    const shortTextKeys = [
      'navigation.home',
      'navigation.tavern',
      'common.save',
      'common.cancel',
      'common.close'
    ]

    shortTextKeys.forEach(key => {
      const keys = key.split('.')
      let current = pl
      for (const k of keys) {
        current = current[k]
      }
      expect(current.length).toBeLessThan(20) // UI buttons should be short
    })
  })

  it('should handle accessibility labels correctly', () => {
    const accessibilityKeys = Object.keys(pl.accessibility)
    
    accessibilityKeys.forEach(key => {
      const text = pl.accessibility[key]
      expect(text).toBeTruthy()
      expect(text.length).toBeGreaterThan(5) // Accessibility labels should be descriptive
    })
  })
})

describe('Language Switching', () => {
  it('should switch between Polish and English', () => {
    const i18n = createI18n({
      locale: 'pl',
      fallbackLocale: 'en',
      messages: { pl, en }
    })

    expect(i18n.global.t('hero.title')).toBe('Witaj w Karczmie Warhammer')
    
    i18n.global.locale = 'en'
    expect(i18n.global.t('hero.title')).toBe('Welcome to the Warhammer Tavern')
  })

  it('should persist language preference', () => {
    // Mock localStorage
    const localStorageMock = {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn(),
      clear: vi.fn()
    }
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock
    })

    const i18n = createI18n({
      locale: 'pl',
      fallbackLocale: 'en',
      messages: { pl, en }
    })

    // Simulate language change
    i18n.global.locale = 'en'
    
    // Should save to localStorage
    expect(localStorageMock.setItem).toHaveBeenCalledWith('i18n_locale', 'en')
  })
})

describe('Translation Quality', () => {
  it('should have contextually appropriate translations', () => {
    // Check that faction names are appropriately translated
    expect(pl.characters.factions.empire).toBe('Imperium')
    expect(pl.characters.factions.dwarfs).toBe('Krasnoludy')
    expect(pl.characters.factions.highElves).toBe('Wysokie Elfy')
    
    // Check that character classes maintain fantasy context
    expect(pl.characters.classes.empireKnight).toBe('Rycerz Imperium')
    expect(pl.characters.classes.dwarfSlayer).toBe('Krasnoludzki Pogromca')
  })

  it('should maintain consistent terminology', () => {
    // Check that the same concepts use the same translations throughout
    const tavernReferences = [
      pl.navigation.tavern,
      pl.hero.title.includes('Karczm'),
      pl.tavern.title.includes('Karczm')
    ]
    
    // All should reference "Karczma" consistently
    expect(tavernReferences.every(ref => 
      typeof ref === 'string' ? ref.includes('Karczm') : ref
    )).toBe(true)
  })

  it('should use appropriate formality level', () => {
    // Polish translations should use appropriate formality
    // Check for consistent use of formal/informal address
    const formalityIndicators = [
      pl.hero.description,
      pl.characters.subtitle,
      pl.conversations.welcomeDesc
    ]
    
    formalityIndicators.forEach(text => {
      expect(text).toBeTruthy()
      expect(text.length).toBeGreaterThan(10)
      // Should not contain overly informal language
      expect(text).not.toMatch(/\b(hej|cześć|siema)\b/i)
    })
  })
})
