import { test, expect, type Page } from '@playwright/test'

test.describe('Warhammer Tavern Experience', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test.describe('Polish Localization', () => {
    test('should display Polish text by default', async ({ page }) => {
      // Check main title is in Polish
      await expect(page.locator('h1')).toContainText('Witaj w Karczmie Warhammer')
      
      // Check navigation items are in Polish
      await expect(page.locator('nav')).toContainText('Karczma')
      await expect(page.locator('nav')).toContainText('Postacie')
      await expect(page.locator('nav')).toContainText('Rozmowy')
    })

    test('should switch to English when language is changed', async ({ page }) => {
      // Open language selector
      await page.click('[aria-label*="język"]')
      
      // Select English
      await page.click('text=English')
      
      // Verify English content
      await expect(page.locator('h1')).toContainText('Welcome to the Warhammer Tavern')
      await expect(page.locator('nav')).toContainText('Tavern')
      await expect(page.locator('nav')).toContainText('Characters')
    })

    test('should persist language preference', async ({ page, context }) => {
      // Switch to English
      await page.click('[aria-label*="język"]')
      await page.click('text=English')
      
      // Create new page in same context
      const newPage = await context.newPage()
      await newPage.goto('/')
      
      // Should remember English preference
      await expect(newPage.locator('h1')).toContainText('Welcome to the Warhammer Tavern')
    })
  })

  test.describe('Multi-Agent Conversation System', () => {
    test('should navigate to conversations page', async ({ page }) => {
      await page.click('text=Rozmowy')
      await expect(page).toHaveURL(/.*conversations/)
      await expect(page.locator('h1')).toContainText('Rozmowy')
    })

    test('should display conversation interface', async ({ page }) => {
      await page.goto('/conversations')
      
      // Check main elements are present
      await expect(page.locator('.multi-agent-chat')).toBeVisible()
      await expect(page.locator('.chat-header')).toBeVisible()
      await expect(page.locator('.messages-area')).toBeVisible()
      await expect(page.locator('.input-area')).toBeVisible()
    })

    test('should show active agents', async ({ page }) => {
      await page.goto('/conversations')
      
      // Should show at least one agent by default
      await expect(page.locator('.agent-indicator')).toBeVisible()
      await expect(page.locator('text=Sir Marcus')).toBeVisible()
    })

    test('should send messages', async ({ page }) => {
      await page.goto('/conversations')
      
      const messageInput = page.locator('textarea[placeholder*="wiadomość"]')
      const sendButton = page.locator('button:has-text("Wyślij")')
      
      // Type and send message
      await messageInput.fill('Witaj w karczmie!')
      await sendButton.click()
      
      // Message should appear in chat
      await expect(page.locator('.message-content')).toContainText('Witaj w karczmie!')
    })

    test('should add new agents to conversation', async ({ page }) => {
      await page.goto('/conversations')
      
      // Click add agent button
      await page.click('text=Dodaj Agenta')
      
      // Agent selector should appear
      await expect(page.locator('text=Wybierz Postać')).toBeVisible()
      
      // Select an agent
      await page.click('text=Grimjaw')
      
      // Agent should be added to conversation
      await expect(page.locator('text=Grimjaw')).toBeVisible()
    })

    test('should remove agents from conversation', async ({ page }) => {
      await page.goto('/conversations')
      
      // Add an agent first
      await page.click('text=Dodaj Agenta')
      await page.click('text=Grimjaw')
      
      // Remove the agent
      await page.click('.agent-indicator:has-text("Grimjaw") button[aria-label*="Usuń"]')
      
      // Agent should be removed
      await expect(page.locator('.agent-indicator:has-text("Grimjaw")')).not.toBeVisible()
    })

    test('should show typing indicators', async ({ page }) => {
      await page.goto('/conversations')
      
      // Send a message to trigger agent response
      await page.fill('textarea', 'Hello agents!')
      await page.click('button:has-text("Wyślij")')
      
      // Should show typing indicator
      await expect(page.locator('.typing-indicator')).toBeVisible({ timeout: 5000 })
    })
  })

  test.describe('Dark Tavern Atmosphere', () => {
    test('should display atmospheric effects', async ({ page }) => {
      // Check for atmosphere component
      await expect(page.locator('.tavern-atmosphere')).toBeVisible()
      
      // Check for candle effects (if not reduced motion)
      const prefersReducedMotion = await page.evaluate(() => 
        window.matchMedia('(prefers-reduced-motion: reduce)').matches
      )
      
      if (!prefersReducedMotion) {
        await expect(page.locator('.candle-lights')).toBeVisible()
        await expect(page.locator('.ember-particles')).toBeVisible()
      }
    })

    test('should respect reduced motion preferences', async ({ page }) => {
      // Simulate reduced motion preference
      await page.emulateMedia({ reducedMotion: 'reduce' })
      await page.reload()
      
      // Atmospheric effects should be reduced or disabled
      const atmosphereElement = page.locator('.tavern-atmosphere')
      await expect(atmosphereElement).toHaveClass(/reduced-motion/)
    })

    test('should have proper contrast ratios', async ({ page }) => {
      // Check text contrast against background
      const textElements = page.locator('h1, h2, h3, p, button')
      const count = await textElements.count()
      
      for (let i = 0; i < Math.min(count, 10); i++) {
        const element = textElements.nth(i)
        const isVisible = await element.isVisible()
        
        if (isVisible) {
          // Element should be readable (this is a basic check)
          await expect(element).toBeVisible()
          
          const color = await element.evaluate(el => 
            window.getComputedStyle(el).color
          )
          
          // Should not be completely transparent
          expect(color).not.toBe('rgba(0, 0, 0, 0)')
        }
      }
    })
  })

  test.describe('Enhanced Visual Assets', () => {
    test('should display Warhammer icons correctly', async ({ page }) => {
      await page.goto('/characters')
      
      // Check for faction icons
      await expect(page.locator('[class*="faction-"]')).toBeVisible()
      
      // Check for character class icons
      const characterCards = page.locator('.character-card')
      const count = await characterCards.count()
      
      for (let i = 0; i < count; i++) {
        const card = characterCards.nth(i)
        await expect(card.locator('svg, .icon')).toBeVisible()
      }
    })

    test('should show appropriate icons for different contexts', async ({ page }) => {
      // Navigation should have appropriate icons
      await expect(page.locator('nav svg')).toBeVisible()
      
      // Buttons should have icons where appropriate
      const buttonsWithIcons = page.locator('button:has(svg)')
      const count = await buttonsWithIcons.count()
      expect(count).toBeGreaterThan(0)
    })
  })

  test.describe('Responsive Design', () => {
    test('should work on mobile devices', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 })
      
      // Main content should be visible
      await expect(page.locator('h1')).toBeVisible()
      
      // Navigation should adapt to mobile
      const mobileMenu = page.locator('[aria-label*="menu"]')
      if (await mobileMenu.isVisible()) {
        await mobileMenu.click()
        await expect(page.locator('nav')).toBeVisible()
      }
    })

    test('should work on tablet devices', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 })
      
      // Layout should adapt appropriately
      await expect(page.locator('h1')).toBeVisible()
      await expect(page.locator('nav')).toBeVisible()
    })

    test('should work on desktop', async ({ page }) => {
      await page.setViewportSize({ width: 1920, height: 1080 })
      
      // Full layout should be visible
      await expect(page.locator('h1')).toBeVisible()
      await expect(page.locator('nav')).toBeVisible()
      
      // Desktop-specific elements should be present
      await expect(page.locator('.dock-navigation')).toBeVisible()
    })
  })

  test.describe('Accessibility', () => {
    test('should have proper heading hierarchy', async ({ page }) => {
      const headings = page.locator('h1, h2, h3, h4, h5, h6')
      const count = await headings.count()
      
      // Should have at least one h1
      await expect(page.locator('h1')).toBeVisible()
      
      // Check heading order (basic check)
      for (let i = 0; i < count; i++) {
        const heading = headings.nth(i)
        await expect(heading).toBeVisible()
      }
    })

    test('should have proper ARIA labels', async ({ page }) => {
      // Check for ARIA labels on interactive elements
      const interactiveElements = page.locator('button, a, input, textarea')
      const count = await interactiveElements.count()
      
      let labeledCount = 0
      for (let i = 0; i < Math.min(count, 20); i++) {
        const element = interactiveElements.nth(i)
        const ariaLabel = await element.getAttribute('aria-label')
        const ariaLabelledBy = await element.getAttribute('aria-labelledby')
        const textContent = await element.textContent()
        
        if (ariaLabel || ariaLabelledBy || (textContent && textContent.trim())) {
          labeledCount++
        }
      }
      
      // Most interactive elements should have labels
      expect(labeledCount).toBeGreaterThan(count * 0.7)
    })

    test('should be keyboard navigable', async ({ page }) => {
      // Tab through interactive elements
      await page.keyboard.press('Tab')
      
      // Should have visible focus indicators
      const focusedElement = page.locator(':focus')
      await expect(focusedElement).toBeVisible()
      
      // Continue tabbing
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')
      
      // Should still have focus somewhere
      await expect(page.locator(':focus')).toBeVisible()
    })

    test('should support screen readers', async ({ page }) => {
      // Check for skip links
      await expect(page.locator('text=Przejdź do treści')).toBeVisible()
      
      // Check for proper landmarks
      await expect(page.locator('main')).toBeVisible()
      await expect(page.locator('nav')).toBeVisible()
    })
  })

  test.describe('Performance', () => {
    test('should load quickly', async ({ page }) => {
      const startTime = Date.now()
      await page.goto('/')
      await page.waitForLoadState('networkidle')
      const loadTime = Date.now() - startTime
      
      // Should load within reasonable time (adjust as needed)
      expect(loadTime).toBeLessThan(5000)
    })

    test('should handle animations smoothly', async ({ page }) => {
      // Check that animations don't cause layout shifts
      await page.goto('/')
      
      // Wait for animations to settle
      await page.waitForTimeout(2000)
      
      // Page should be stable
      await expect(page.locator('h1')).toBeVisible()
      await expect(page.locator('h1')).toBeStable()
    })
  })
})
