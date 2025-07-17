import { test, expect } from '@playwright/test'

// Test data
const mockLoadingSteps = [
  {
    id: 'step1',
    title: 'Initializing Tavern',
    description: 'Setting up the medieval atmosphere...',
    icon: 'home',
    duration: 1000,
    faction: 'empire' as const
  },
  {
    id: 'step2',
    title: 'Loading Characters',
    description: 'Summoning NPCs and patrons...',
    icon: 'users',
    duration: 1500,
    faction: 'empire' as const
  },
  {
    id: 'step3',
    title: 'Preparing Audio',
    description: 'Tuning medieval instruments...',
    icon: 'music',
    duration: 800,
    faction: 'empire' as const
  }
]

const mockCharacterCards = [
  {
    id: 'char1',
    name: 'Sir Marcus',
    faction: 'empire' as const,
    description: 'A noble knight of the Empire',
    stats: { strength: 8, wisdom: 6, charisma: 7 }
  },
  {
    id: 'char2',
    name: 'Grimjaw',
    faction: 'orcs' as const,
    description: 'A fierce orc warrior',
    stats: { strength: 9, wisdom: 3, charisma: 4 }
  },
  {
    id: 'char3',
    name: 'Elaria',
    faction: 'elves' as const,
    description: 'An elegant elven mage',
    stats: { strength: 4, wisdom: 9, charisma: 8 }
  }
]

test.describe('Inspira UI Components - Warhammer Tavern v3', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to test page
    await page.goto('/test-components')
    
    // Wait for components to load
    await page.waitForLoadState('networkidle')
  })

  test.describe('MultiStepLoader Component', () => {
    test('should display loading steps correctly', async ({ page }) => {
      // Mount component with test data
      await page.evaluate((steps) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <MultiStepLoader 
              :steps="${JSON.stringify(steps)}"
              :auto-progress="false"
              :allow-skip="true"
            />
          `
        }
      }, mockLoadingSteps)

      // Check if loader is visible
      await expect(page.locator('.multi-step-loader')).toBeVisible()
      
      // Check step indicators
      const stepIndicators = page.locator('.multi-step-loader .step-indicator')
      await expect(stepIndicators).toHaveCount(3)
      
      // Check current step display
      await expect(page.locator('.current-step-title')).toContainText('Initializing Tavern')
      await expect(page.locator('.current-step-description')).toContainText('Setting up the medieval atmosphere')
    })

    test('should progress through steps automatically', async ({ page }) => {
      await page.evaluate((steps) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <MultiStepLoader 
              :steps="${JSON.stringify(steps)}"
              :auto-progress="true"
            />
          `
        }
      }, mockLoadingSteps)

      // Wait for first step
      await expect(page.locator('.current-step-title')).toContainText('Initializing Tavern')
      
      // Wait for second step (after 1000ms)
      await page.waitForTimeout(1200)
      await expect(page.locator('.current-step-title')).toContainText('Loading Characters')
      
      // Check progress bar
      const progressBar = page.locator('.progress-bar')
      await expect(progressBar).toHaveCSS('width', /[4-7][0-9]%/) // Should be around 66%
    })

    test('should handle skip functionality', async ({ page }) => {
      await page.evaluate((steps) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <MultiStepLoader 
              :steps="${JSON.stringify(steps)}"
              :auto-progress="false"
              :allow-skip="true"
            />
          `
        }
      }, mockLoadingSteps)

      // Click skip button
      await page.click('.skip-button')
      
      // Should emit skip event and complete loading
      await expect(page.locator('.multi-step-loader')).not.toBeVisible()
    })

    test('should be responsive on mobile', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 })
      
      await page.evaluate((steps) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <MultiStepLoader 
              :steps="${JSON.stringify(steps)}"
            />
          `
        }
      }, mockLoadingSteps)

      const loader = page.locator('.multi-step-loader')
      await expect(loader).toBeVisible()
      
      // Check mobile-specific styling
      await expect(loader).toHaveCSS('max-width', '90vw')
    })
  })

  test.describe('BoxReveal Component', () => {
    test('should reveal content on scroll', async ({ page }) => {
      await page.setContent(`
        <div style="height: 200vh;">
          <div style="height: 100vh;"></div>
          <BoxReveal trigger-on-scroll>
            <div class="reveal-content">Hidden Content</div>
          </BoxReveal>
        </div>
      `)

      const revealBox = page.locator('.reveal-box')
      const content = page.locator('.reveal-content')
      
      // Initially hidden
      await expect(content).toHaveCSS('opacity', '0')
      
      // Scroll to trigger reveal
      await page.evaluate(() => window.scrollTo(0, window.innerHeight))
      
      // Wait for reveal animation
      await page.waitForTimeout(1000)
      
      // Content should be revealed
      await expect(content).toHaveCSS('opacity', '1')
    })

    test('should support different reveal directions', async ({ page }) => {
      const directions = ['top', 'bottom', 'left', 'right', 'center']
      
      for (const direction of directions) {
        await page.setContent(`
          <BoxReveal reveal-direction="${direction}" :trigger-on-scroll="false">
            <div class="test-content">Test Content</div>
          </BoxReveal>
        `)

        const revealBox = page.locator('.reveal-box')
        
        // Check origin class
        await expect(revealBox).toHaveClass(new RegExp(`origin-${direction}`))
        
        // Trigger reveal manually
        await page.evaluate(() => {
          const component = document.querySelector('BoxReveal')
          if (component && component.startReveal) {
            component.startReveal()
          }
        })
        
        await page.waitForTimeout(500)
      }
    })
  })

  test.describe('FocusCards Component', () => {
    test('should display character cards correctly', async ({ page }) => {
      await page.evaluate((cards) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <FocusCards 
              :cards="${JSON.stringify(cards)}"
              focus-mode="hover"
            />
          `
        }
      }, mockCharacterCards)

      // Check if all cards are displayed
      const cards = page.locator('.focus-card')
      await expect(cards).toHaveCount(3)
      
      // Check character names
      await expect(page.locator('.character-name').first()).toContainText('Sir Marcus')
      await expect(page.locator('.character-name').nth(1)).toContainText('Grimjaw')
      await expect(page.locator('.character-name').nth(2)).toContainText('Elaria')
    })

    test('should handle hover focus mode', async ({ page }) => {
      await page.evaluate((cards) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <FocusCards 
              :cards="${JSON.stringify(cards)}"
              focus-mode="hover"
            />
          `
        }
      }, mockCharacterCards)

      const firstCard = page.locator('.focus-card').first()
      const secondCard = page.locator('.focus-card').nth(1)
      
      // Hover over first card
      await firstCard.hover()
      
      // First card should be focused (scaled up)
      await expect(firstCard).toHaveClass(/scale-105/)
      
      // Other cards should be blurred
      await expect(secondCard).toHaveClass(/opacity-50/)
    })

    test('should display faction-specific styling', async ({ page }) => {
      await page.evaluate((cards) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <FocusCards 
              :cards="${JSON.stringify(cards)}"
            />
          `
        }
      }, mockCharacterCards)

      // Check faction backgrounds
      const empireCard = page.locator('.focus-card').first()
      const orcCard = page.locator('.focus-card').nth(1)
      const elfCard = page.locator('.focus-card').nth(2)
      
      await expect(empireCard.locator('.card-background')).toHaveClass(/from-yellow-900/)
      await expect(orcCard.locator('.card-background')).toHaveClass(/from-green-800/)
      await expect(elfCard.locator('.card-background')).toHaveClass(/from-green-900/)
    })

    test('should be responsive on different screen sizes', async ({ page }) => {
      // Test mobile layout
      await page.setViewportSize({ width: 375, height: 667 })
      
      await page.evaluate((cards) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <FocusCards 
              :cards="${JSON.stringify(cards)}"
              :grid-cols="3"
            />
          `
        }
      }, mockCharacterCards)

      const grid = page.locator('.cards-grid')
      
      // Should use single column on mobile
      await expect(grid).toHaveClass(/grid-cols-1/)
      
      // Test tablet layout
      await page.setViewportSize({ width: 768, height: 1024 })
      await expect(grid).toHaveClass(/md:grid-cols-2/)
      
      // Test desktop layout
      await page.setViewportSize({ width: 1024, height: 768 })
      await expect(grid).toHaveClass(/lg:grid-cols-3/)
    })
  })

  test.describe('Meteors Component (Performance)', () => {
    test('should render meteors with canvas when supported', async ({ page }) => {
      await page.setContent(`
        <Meteors 
          :meteor-count="5"
          :enable-canvas="true"
        />
      `)

      const canvas = page.locator('canvas')
      await expect(canvas).toBeVisible()
      
      // Check canvas dimensions
      const canvasSize = await canvas.boundingBox()
      expect(canvasSize?.width).toBeGreaterThan(0)
      expect(canvasSize?.height).toBeGreaterThan(0)
    })

    test('should fallback to DOM meteors when canvas is disabled', async ({ page }) => {
      await page.setContent(`
        <Meteors 
          :meteor-count="3"
          :enable-canvas="false"
        />
      `)

      const domMeteors = page.locator('.dom-meteors')
      await expect(domMeteors).toBeVisible()
      
      const meteors = page.locator('.meteor')
      await expect(meteors).toHaveCount(3)
    })

    test('should maintain good performance with many meteors', async ({ page }) => {
      // Start performance monitoring
      await page.evaluate(() => {
        window.performanceStart = performance.now()
        window.frameCount = 0
        
        const measureFPS = () => {
          window.frameCount++
          requestAnimationFrame(measureFPS)
        }
        measureFPS()
      })

      await page.setContent(`
        <Meteors 
          :meteor-count="20"
          :enable-canvas="true"
        />
      `)

      // Wait for animation to run
      await page.waitForTimeout(2000)
      
      // Check performance
      const fps = await page.evaluate(() => {
        const elapsed = performance.now() - window.performanceStart
        return (window.frameCount / elapsed) * 1000
      })
      
      // Should maintain at least 30 FPS
      expect(fps).toBeGreaterThan(30)
    })
  })

  test.describe('Accessibility', () => {
    test('should support keyboard navigation', async ({ page }) => {
      await page.evaluate((cards) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <FocusCards 
              :cards="${JSON.stringify(cards)}"
              focus-mode="click"
            />
          `
        }
      }, mockCharacterCards)

      // Tab through cards
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')
      
      // Press Enter to focus
      await page.keyboard.press('Enter')
      
      // Check if card is focused
      const focusedCard = page.locator('.focus-card:focus')
      await expect(focusedCard).toBeVisible()
    })

    test('should respect reduced motion preferences', async ({ page }) => {
      // Set reduced motion preference
      await page.emulateMedia({ reducedMotion: 'reduce' })
      
      await page.setContent(`
        <BoxReveal>
          <div>Test Content</div>
        </BoxReveal>
      `)

      const revealBox = page.locator('.reveal-box')
      
      // Animation duration should be very short
      await expect(revealBox).toHaveCSS('transition-duration', '0.1s')
    })

    test('should have proper ARIA labels and roles', async ({ page }) => {
      await page.evaluate((steps) => {
        const app = document.querySelector('#app')
        if (app) {
          app.innerHTML = `
            <MultiStepLoader 
              :steps="${JSON.stringify(steps)}"
            />
          `
        }
      }, mockLoadingSteps)

      // Check ARIA attributes
      const loader = page.locator('.multi-step-loader')
      await expect(loader).toHaveAttribute('role', 'progressbar')
      await expect(loader).toHaveAttribute('aria-label', /loading/i)
    })
  })
})
