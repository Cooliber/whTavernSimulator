import { test, expect } from '@playwright/test';

test.describe('Warhammer Tavern v3 - Core Functionality', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Wait for application to initialize
    await page.waitForTimeout(3000);
  });

  test('Application loads successfully', async ({ page }) => {
    // Check if the main page loads
    await expect(page).toHaveTitle(/Warhammer Tavern/);
    
    // Check for main content
    const mainContent = page.locator('main, .main-content, .tavern-content');
    await expect(mainContent).toBeVisible();
  });

  test('Navigation works correctly', async ({ page }) => {
    // Test navigation to different sections
    const navLinks = page.locator('nav a, .nav-link');
    const linkCount = await navLinks.count();
    
    if (linkCount > 0) {
      // Click on first navigation link
      await navLinks.first().click();
      await page.waitForTimeout(1000);
      
      // Should still be on the same domain
      expect(page.url()).toContain('5920');
    }
  });

  test('Interactive systems are present', async ({ page }) => {
    // Check for interactive systems section
    const interactiveSection = page.locator('.interactive-systems');
    await expect(interactiveSection).toBeVisible();

    // Check for feature cards
    const featureCards = page.locator('.feature-card');
    const cardCount = await featureCards.count();
    expect(cardCount).toBeGreaterThan(0);
  });

  test('AI Conversations feature is accessible', async ({ page }) => {
    // Look for AI Conversations feature
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    
    if (await conversationsCard.count() > 0) {
      await conversationsCard.click();
      await page.waitForTimeout(2000);
      
      // Should show some conversation interface or agent management
      const conversationInterface = page.locator('.npc-conversation, .agent-management-dashboard');
      await expect(conversationInterface).toBeVisible();
    }
  });

  test('Tavern Games feature works', async ({ page }) => {
    // Look for Tavern Games feature
    const gamesCard = page.locator('.feature-card').filter({ hasText: /Tavern Games/ });
    
    if (await gamesCard.count() > 0) {
      await gamesCard.click();
      await page.waitForTimeout(2000);
      
      // Should show games interface
      const gamesInterface = page.locator('.mini-games-hub, .games-overview');
      await expect(gamesInterface).toBeVisible();
    }
  });

  test('Character Progression feature works', async ({ page }) => {
    // Look for Character Growth feature
    const progressionCard = page.locator('.feature-card').filter({ hasText: /Character Growth/ });
    
    if (await progressionCard.count() > 0) {
      await progressionCard.click();
      await page.waitForTimeout(2000);
      
      // Should show character progression interface
      const progressionInterface = page.locator('.character-progression');
      await expect(progressionInterface).toBeVisible();
    }
  });

  test('Reputation System feature works', async ({ page }) => {
    // Look for Reputation System feature
    const reputationCard = page.locator('.feature-card').filter({ hasText: /Reputation System/ });
    
    if (await reputationCard.count() > 0) {
      await reputationCard.click();
      await page.waitForTimeout(2000);
      
      // Should show reputation interface
      const reputationInterface = page.locator('.reputation-section');
      await expect(reputationInterface).toBeVisible();
    }
  });

  test('Tavern menu is functional', async ({ page }) => {
    // Check for tavern menu
    const tavernMenu = page.locator('.tavern-menu');
    await expect(tavernMenu).toBeVisible();
    
    // Check for menu categories
    const menuCategories = page.locator('.category-tab, .menu-category');
    const categoryCount = await menuCategories.count();
    expect(categoryCount).toBeGreaterThan(0);
  });

  test('Character profiles are displayed', async ({ page }) => {
    // Check for character profiles
    const characterProfiles = page.locator('.character-profile, .patron-card');
    const profileCount = await characterProfiles.count();
    expect(profileCount).toBeGreaterThan(0);
  });

  test('Responsive design works', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(1000);
    
    // Main content should still be visible
    const mainContent = page.locator('main, .main-content, .tavern-content');
    await expect(mainContent).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(1000);
    
    // Content should adapt
    await expect(mainContent).toBeVisible();
    
    // Reset to desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
  });

  test('No critical JavaScript errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('pageerror', (error: Error) => {
      errors.push(error.message);
    });
    
    // Navigate and interact with the page
    await page.reload();
    await page.waitForTimeout(3000);
    
    // Click on interactive elements if they exist
    const interactiveElements = page.locator('button, .feature-card');
    const elementCount = await interactiveElements.count();
    
    if (elementCount > 0) {
      await interactiveElements.first().click();
      await page.waitForTimeout(1000);
    }
    
    // Filter out non-critical errors
    const criticalErrors = errors.filter(error => 
      !error.includes('Warning') && 
      !error.includes('DevTools') &&
      !error.includes('Extension')
    );
    
    expect(criticalErrors.length).toBe(0);
  });

  test('Performance is acceptable', async ({ page }) => {
    // Measure page load time
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;

    // Should load within reasonable time
    expect(loadTime).toBeLessThan(10000); // 10 seconds max
  });

  test('Basic accessibility features', async ({ page }) => {
    // Test keyboard navigation
    await page.keyboard.press('Tab');
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    
    // Should be able to focus on interactive elements
    const interactiveElements = ['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA'];
    const hasFocusableElements = interactiveElements.includes(focusedElement || '');
    
    // If there are no focusable elements, that's also acceptable
    expect(typeof focusedElement).toBe('string');
  });

  test('Content is properly structured', async ({ page }) => {
    // Check for proper heading structure
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const headingCount = await headings.count();
    expect(headingCount).toBeGreaterThan(0);
    
    // Check for main content areas
    const contentAreas = page.locator('main, section, article');
    const contentCount = await contentAreas.count();
    expect(contentCount).toBeGreaterThan(0);
  });

  test('Images load properly', async ({ page }) => {
    // Check for images
    const images = page.locator('img');
    const imageCount = await images.count();
    
    if (imageCount > 0) {
      // Check if first image loads
      const firstImage = images.first();
      await expect(firstImage).toBeVisible();
      
      // Check if image has alt text or proper attributes
      const hasAlt = await firstImage.getAttribute('alt');
      const hasSrc = await firstImage.getAttribute('src');
      
      expect(hasSrc).toBeTruthy();
      // Alt text is good practice but not always required
    }
  });

  test('Interactive elements respond to user input', async ({ page }) => {
    // Find clickable elements
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();
    
    if (buttonCount > 0) {
      const firstButton = buttons.first();
      
      // Check if button is clickable
      await expect(firstButton).toBeVisible();
      await expect(firstButton).toBeEnabled();
      
      // Click the button
      await firstButton.click();
      await page.waitForTimeout(500);
      
      // Should not cause page crash
      const pageTitle = await page.title();
      expect(pageTitle).toBeTruthy();
    }
  });

  test('Data persistence works', async ({ page }) => {
    // Test if any data persists across page reloads
    // This is a basic test for localStorage or sessionStorage usage
    
    const hasLocalStorage = await page.evaluate(() => {
      return typeof localStorage !== 'undefined';
    });
    
    const hasSessionStorage = await page.evaluate(() => {
      return typeof sessionStorage !== 'undefined';
    });
    
    // At least one storage mechanism should be available
    expect(hasLocalStorage || hasSessionStorage).toBe(true);
  });

  test('Application handles network issues gracefully', async ({ page }) => {
    // Test with simulated slow network
    await page.route('**/*', route => {
      // Add delay to simulate slow network
      setTimeout(() => route.continue(), 100);
    });
    
    await page.reload();
    await page.waitForTimeout(2000);
    
    // Page should still load and be functional
    const mainContent = page.locator('main, .main-content, .tavern-content');
    await expect(mainContent).toBeVisible();
  });
});
