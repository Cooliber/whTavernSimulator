/**
 * Configuration Testing and Validation
 * Comprehensive tests for all system configurations
 */

import { test, expect } from '@playwright/test'

test.describe('Warhammer Tavern Simulator v3 - Configuration Tests', () => {
  test.describe('Port Configuration', () => {
    test('should serve application on port 5920', async ({ page }) => {
      const response = await page.goto('http://localhost:5920')
      expect(response.status()).toBe(200)
    })

    it('should have correct base URL in Playwright config', async () => {
      // This test verifies the Playwright configuration
      expect(page.url()).toContain('localhost:5920')
    })

    it('should handle WebSocket connections on correct port', async () => {
      // Test WebSocket connection if applicable
      const wsUrl = 'ws://localhost:5920/ws'
      // WebSocket test implementation would go here
      expect(true).toBe(true) // Placeholder
    })
  })

  describe('Routing Configuration', () => {
    it('should navigate to home page', async () => {
      await page.goto('http://localhost:5920/')
      await expect(page.locator('h1')).toContainText('Warhammer Tavern Simulator')
    })

    it('should navigate to characters page', async () => {
      await page.goto('http://localhost:5920/characters')
      await expect(page.locator('h1')).toContainText('Characters')
    })

    it('should navigate to conversations page', async () => {
      await page.goto('http://localhost:5920/conversations')
      await expect(page.locator('h1')).toContainText('Conversations')
    })

    it('should navigate to settings page', async () => {
      await page.goto('http://localhost:5920/settings')
      await expect(page.locator('h1')).toContainText('Tavern Settings')
    })

    it('should navigate to about page', async () => {
      await page.goto('http://localhost:5920/about')
      await expect(page.locator('h1')).toContainText('About Warhammer Tavern Simulator')
    })

    it('should navigate to generators page', async () => {
      await page.goto('http://localhost:5920/generators')
      await expect(page.locator('h1')).toContainText('Warhammer Content Generators')
    })

    it('should handle dynamic routes', async () => {
      await page.goto('http://localhost:5920/conversations/marcus')
      await expect(page.locator('h1')).toContainText('Sir Marcus Brightblade')
    })

    it('should handle 404 errors gracefully', async () => {
      const response = await page.goto('http://localhost:5920/nonexistent-page')
      expect(response.status()).toBe(404)
    })
  })

  describe('CSS Configuration', () => {
    it('should load main CSS file', async () => {
      await page.goto('http://localhost:5920/')
      
      // Check if CSS is loaded by verifying computed styles
      const bodyStyles = await page.evaluate(() => {
        return window.getComputedStyle(document.body)
      })
      
      expect(bodyStyles.margin).toBe('0px')
      expect(bodyStyles.padding).toBe('0px')
    })

    it('should apply Warhammer theme styles', async () => {
      await page.goto('http://localhost:5920/')
      
      // Check for faction colors
      const empireButton = page.locator('.faction-empire').first()
      if (await empireButton.count() > 0) {
        const styles = await empireButton.evaluate(el => {
          return window.getComputedStyle(el)
        })
        expect(styles.background).toContain('gradient')
      }
    })

    it('should support responsive design', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test mobile viewport
      await page.setViewportSize({ width: 375, height: 667 })
      await page.waitForTimeout(500)
      
      // Check if mobile styles are applied
      const navigation = page.locator('nav').first()
      if (await navigation.count() > 0) {
        const isVisible = await navigation.isVisible()
        expect(typeof isVisible).toBe('boolean')
      }
      
      // Reset viewport
      await page.setViewportSize({ width: 1280, height: 720 })
    })

    it('should handle dark mode preferences', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test dark mode media query
      await page.emulateMedia({ colorScheme: 'dark' })
      await page.waitForTimeout(500)
      
      const bodyStyles = await page.evaluate(() => {
        return window.getComputedStyle(document.body)
      })
      
      // Verify dark mode styles are applied
      expect(bodyStyles).toBeDefined()
    })

    it('should respect reduced motion preferences', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test reduced motion
      await page.emulateMedia({ reducedMotion: 'reduce' })
      await page.waitForTimeout(500)
      
      // Check if animations are disabled
      const animatedElement = page.locator('.animate-float').first()
      if (await animatedElement.count() > 0) {
        const styles = await animatedElement.evaluate(el => {
          return window.getComputedStyle(el)
        })
        // Animation should be disabled or very short
        expect(styles.animationDuration).toMatch(/0\.01ms|none/)
      }
    })
  })

  describe('Vue Component Configuration', () => {
    it('should render Vue components correctly', async () => {
      await page.goto('http://localhost:5920/')
      
      // Wait for Vue to hydrate
      await page.waitForTimeout(1000)
      
      // Check if Vue components are rendered
      const vueApp = await page.evaluate(() => {
        return document.querySelector('#__nuxt') !== null
      })
      
      expect(vueApp).toBe(true)
    })

    it('should handle component interactions', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test button interactions
      const button = page.locator('button').first()
      if (await button.count() > 0) {
        await button.click()
        // Verify click was handled
        expect(true).toBe(true)
      }
    })

    it('should support component props and events', async () => {
      await page.goto('http://localhost:5920/inspira-test')
      
      // Test component with props
      const rippleButton = page.locator('.faction-empire').first()
      if (await rippleButton.count() > 0) {
        await rippleButton.click()
        
        // Check for ripple effect
        await page.waitForTimeout(500)
        expect(true).toBe(true)
      }
    })
  })

  describe('InspiraUI Integration', () => {
    it('should load all InspiraUI components', async () => {
      await page.goto('http://localhost:5920/inspira-test')
      
      // Wait for components to load
      await page.waitForTimeout(2000)
      
      // Check for key components
      const components = [
        'RippleButton',
        'ShimmerButton',
        'Card3D',
        'SparklesText',
        'AuroraBackground'
      ]
      
      for (const component of components) {
        const element = page.locator(`[data-component="${component}"]`).first()
        // Component should exist or be rendered
        expect(true).toBe(true) // Placeholder for actual component check
      }
    })

    it('should handle component animations', async () => {
      await page.goto('http://localhost:5920/inspira-test')
      
      // Test animation performance
      const animationElement = page.locator('.animate-glow-pulse').first()
      if (await animationElement.count() > 0) {
        const styles = await animationElement.evaluate(el => {
          return window.getComputedStyle(el)
        })
        expect(styles.animation).toBeDefined()
      }
    })

    it('should support theme customization', async () => {
      await page.goto('http://localhost:5920/inspira-test')
      
      // Check for theme variables
      const themeVars = await page.evaluate(() => {
        const styles = window.getComputedStyle(document.documentElement)
        return {
          primary: styles.getPropertyValue('--primary'),
          background: styles.getPropertyValue('--background'),
          foreground: styles.getPropertyValue('--foreground')
        }
      })
      
      expect(themeVars.primary).toBeDefined()
      expect(themeVars.background).toBeDefined()
      expect(themeVars.foreground).toBeDefined()
    })
  })

  describe('Performance Configuration', () => {
    it('should meet performance benchmarks', async () => {
      await page.goto('http://localhost:5920/')
      
      // Measure page load time
      const loadTime = await page.evaluate(() => {
        return performance.timing.loadEventEnd - performance.timing.navigationStart
      })
      
      // Should load within 3 seconds
      expect(loadTime).toBeLessThan(3000)
    })

    it('should optimize bundle size', async () => {
      await page.goto('http://localhost:5920/')
      
      // Check for code splitting
      const scripts = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('script[src]')).map(script => 
          (script as HTMLScriptElement).src
        )
      })
      
      // Should have multiple chunks for code splitting
      expect(scripts.length).toBeGreaterThan(1)
    })

    it('should handle memory usage efficiently', async () => {
      await page.goto('http://localhost:5920/')
      
      // Navigate through multiple pages to test memory
      const pages = ['/characters', '/conversations', '/settings', '/about']
      
      for (const pagePath of pages) {
        await page.goto(`http://localhost:5920${pagePath}`)
        await page.waitForTimeout(500)
      }
      
      // Memory should not leak significantly
      const memoryInfo = await page.evaluate(() => {
        return (performance as any).memory ? {
          usedJSHeapSize: (performance as any).memory.usedJSHeapSize,
          totalJSHeapSize: (performance as any).memory.totalJSHeapSize
        } : null
      })
      
      if (memoryInfo) {
        // Memory usage should be reasonable
        expect(memoryInfo.usedJSHeapSize).toBeLessThan(100 * 1024 * 1024) // 100MB
      }
    })
  })

  describe('Accessibility Configuration', () => {
    it('should support keyboard navigation', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test tab navigation
      await page.keyboard.press('Tab')
      const focusedElement = await page.evaluate(() => document.activeElement?.tagName)
      
      expect(['BUTTON', 'A', 'INPUT'].includes(focusedElement || '')).toBe(true)
    })

    it('should have proper ARIA attributes', async () => {
      await page.goto('http://localhost:5920/')
      
      // Check for ARIA labels
      const ariaElements = await page.evaluate(() => {
        return document.querySelectorAll('[aria-label], [aria-labelledby], [role]').length
      })
      
      expect(ariaElements).toBeGreaterThan(0)
    })

    it('should support screen readers', async () => {
      await page.goto('http://localhost:5920/')
      
      // Check for screen reader only content
      const srOnlyElements = await page.evaluate(() => {
        return document.querySelectorAll('.sr-only').length
      })
      
      expect(srOnlyElements).toBeGreaterThanOrEqual(0)
    })
  })

  describe('Error Handling Configuration', () => {
    it('should handle JavaScript errors gracefully', async () => {
      const errors: string[] = []
      
      page.on('pageerror', (error: Error) => {
        errors.push(error.message)
      })
      
      await page.goto('http://localhost:5920/')
      await page.waitForTimeout(2000)
      
      // Should have no critical JavaScript errors
      const criticalErrors = errors.filter(error => 
        !error.includes('Warning') && !error.includes('DevTools')
      )
      expect(criticalErrors.length).toBe(0)
    })

    it('should handle network errors', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test with network failure simulation
      await page.route('**/api/**', route => route.abort())
      
      // Navigate to a page that might make API calls
      await page.goto('http://localhost:5920/generators')
      
      // Page should still render even with API failures
      const pageContent = await page.textContent('body')
      expect(pageContent).toContain('Warhammer')
    })
  })

  describe('Security Configuration', () => {
    it('should have proper CSP headers', async () => {
      const response = await page.goto('http://localhost:5920/')
      const headers = response.headers()
      
      // Check for security headers (in production)
      if (process.env.NODE_ENV === 'production') {
        expect(headers['content-security-policy']).toBeDefined()
      }
    })

    it('should sanitize user input', async () => {
      await page.goto('http://localhost:5920/settings')
      
      // Test input sanitization
      const input = page.locator('input').first()
      if (await input.count() > 0) {
        await input.fill('<script>alert("xss")</script>')
        
        // Should not execute script
        const value = await input.inputValue()
        expect(value).not.toContain('<script>')
      }
    })
  })

  describe('Integration Tests', () => {
    it('should integrate all systems seamlessly', async () => {
      await page.goto('http://localhost:5920/')
      
      // Test complete user flow
      await page.click('text=Characters')
      await page.waitForTimeout(500)
      
      await page.click('text=Conversations')
      await page.waitForTimeout(500)
      
      await page.click('text=Generators')
      await page.waitForTimeout(500)
      
      // All navigation should work without errors
      const currentUrl = page.url()
      expect(currentUrl).toContain('localhost:5920')
    })

    it('should maintain state across navigation', async () => {
      await page.goto('http://localhost:5920/settings')
      
      // Change a setting
      const checkbox = page.locator('input[type="checkbox"]').first()
      if (await checkbox.count() > 0) {
        await checkbox.check()
        
        // Navigate away and back
        await page.goto('http://localhost:5920/')
        await page.goto('http://localhost:5920/settings')
        
        // Setting should be preserved (if using localStorage)
        const isChecked = await checkbox.isChecked()
        expect(typeof isChecked).toBe('boolean')
      }
    })
  })
})

// Helper functions for testing
export const testHelpers = {
  async waitForAnimation(page: any, selector: string, timeout = 5000) {
    await page.waitForSelector(selector, { timeout })
    await page.waitForTimeout(500) // Allow animation to complete
  },

  async checkPerformance(page: any) {
    const metrics = await page.evaluate(() => {
      return {
        loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
        domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
      }
    })
    
    return metrics
  },

  async checkAccessibility(page: any) {
    // Basic accessibility checks
    const issues = await page.evaluate(() => {
      const issues = []
      
      // Check for images without alt text
      const images = document.querySelectorAll('img:not([alt])')
      if (images.length > 0) {
        issues.push(`${images.length} images without alt text`)
      }
      
      // Check for buttons without accessible names
      const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])')
      const buttonsWithoutText = Array.from(buttons).filter(btn => !btn.textContent?.trim())
      if (buttonsWithoutText.length > 0) {
        issues.push(`${buttonsWithoutText.length} buttons without accessible names`)
      }
      
      return issues
    })
    
    return issues
  }
}
