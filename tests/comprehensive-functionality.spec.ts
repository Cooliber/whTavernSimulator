import { test, expect } from '@playwright/test';

test.describe('Warhammer Tavern v3 - Comprehensive Functionality Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the homepage before each test
    await page.goto('/');
    // Wait for the page to load completely
    await page.waitForLoadState('networkidle');
  });

  test('Homepage loads and displays correctly', async ({ page }) => {
    // Check if the page title is correct
    await expect(page).toHaveTitle(/Warhammer Tavern Simulator v3/);
    
    // Check if main content is visible
    await expect(page.locator('body')).toBeVisible();
    
    // Check if the page has the enhanced background styling
    const body = page.locator('body');
    await expect(body).toHaveCSS('background-image', /linear-gradient/);
  });

  test('Navigation functionality', async ({ page }) => {
    // Test navigation links if they exist
    const navLinks = page.locator('nav a, [role="navigation"] a');
    const linkCount = await navLinks.count();
    
    if (linkCount > 0) {
      // Test first navigation link
      const firstLink = navLinks.first();
      await expect(firstLink).toBeVisible();
      
      // Check if link is clickable
      await expect(firstLink).toBeEnabled();
    }
  });

  test('Interactive elements functionality', async ({ page }) => {
    // Test buttons
    const buttons = page.locator('button, [role="button"]');
    const buttonCount = await buttons.count();
    
    if (buttonCount > 0) {
      for (let i = 0; i < Math.min(buttonCount, 3); i++) {
        const button = buttons.nth(i);
        await expect(button).toBeVisible();
        
        // Check if button is interactive
        if (await button.isEnabled()) {
          // Test hover effect
          await button.hover();
          await page.waitForTimeout(100);
        }
      }
    }
  });

  test('Character gallery functionality', async ({ page }) => {
    // Look for character-related elements
    const characterElements = page.locator('[data-testid*="character"], .character, [class*="character"]');
    const characterCount = await characterElements.count();
    
    if (characterCount > 0) {
      // Test first few character elements
      for (let i = 0; i < Math.min(characterCount, 3); i++) {
        const character = characterElements.nth(i);
        await expect(character).toBeVisible();
      }
    }
  });

  test('Responsive design - Mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if page is still functional on mobile
    await expect(page.locator('body')).toBeVisible();
    
    // Check if text is readable (minimum 16px font size)
    const textElements = page.locator('p, span, div').filter({ hasText: /\w+/ });
    const firstText = textElements.first();
    
    if (await firstText.isVisible()) {
      const fontSize = await firstText.evaluate(el => {
        return window.getComputedStyle(el).fontSize;
      });
      
      // Extract numeric value from fontSize (e.g., "16px" -> 16)
      const fontSizeValue = parseInt(fontSize.replace('px', ''));
      expect(fontSizeValue).toBeGreaterThanOrEqual(16);
    }
  });

  test('Responsive design - Tablet viewport', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if page adapts to tablet size
    await expect(page.locator('body')).toBeVisible();
  });

  test('Responsive design - Desktop viewport', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if page works on large screens
    await expect(page.locator('body')).toBeVisible();
  });

  test('Enhanced styling and visual effects', async ({ page }) => {
    // Check if enhanced CSS classes are applied
    const enhancedElements = page.locator('.card-enhanced, .btn-enhanced, .font-medieval');
    const enhancedCount = await enhancedElements.count();
    
    if (enhancedCount > 0) {
      const firstEnhanced = enhancedElements.first();
      await expect(firstEnhanced).toBeVisible();
    }
    
    // Check if faction styling is present
    const factionElements = page.locator('[class*="faction-"]');
    const factionCount = await factionElements.count();
    
    if (factionCount > 0) {
      const firstFaction = factionElements.first();
      await expect(firstFaction).toBeVisible();
    }
  });

  test('Accessibility features', async ({ page }) => {
    // Check for focus management
    await page.keyboard.press('Tab');
    const focusedElement = page.locator(':focus');
    
    if (await focusedElement.count() > 0) {
      await expect(focusedElement).toBeVisible();
    }
    
    // Check for proper heading structure
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const headingCount = await headings.count();
    
    if (headingCount > 0) {
      // Should have at least one main heading
      const h1 = page.locator('h1');
      if (await h1.count() > 0) {
        await expect(h1.first()).toBeVisible();
      }
    }
  });

  test('Performance and loading', async ({ page }) => {
    // Measure page load time
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    // Page should load within reasonable time (5 seconds)
    expect(loadTime).toBeLessThan(5000);
    
    // Check if images load properly
    const images = page.locator('img');
    const imageCount = await images.count();
    
    if (imageCount > 0) {
      for (let i = 0; i < Math.min(imageCount, 3); i++) {
        const img = images.nth(i);
        if (await img.isVisible()) {
          // Check if image has loaded
          const naturalWidth = await img.evaluate((el: HTMLImageElement) => el.naturalWidth);
          expect(naturalWidth).toBeGreaterThan(0);
        }
      }
    }
  });

  test('Error handling and edge cases', async ({ page }) => {
    // Test navigation to non-existent page
    const response = await page.goto('/non-existent-page');
    
    // Should handle 404 gracefully
    if (response) {
      expect([200, 404]).toContain(response.status());
    }
    
    // Navigate back to working page
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Component Test Page Verification', () => {
  test('Component test page functionality', async ({ page }) => {
    await page.goto('/test-components');
    await page.waitForLoadState('networkidle');
    
    // Check if test page loads
    await expect(page).toHaveTitle(/Component Test/);
    
    // Check if test content is visible
    const testHeading = page.locator('h1').filter({ hasText: /Component Test/ });
    await expect(testHeading).toBeVisible();
    
    // Check if welcome text is present
    const welcomeText = page.locator('text=Welcome to the Warhammer Tavern');
    await expect(welcomeText).toBeVisible();
  });
});
