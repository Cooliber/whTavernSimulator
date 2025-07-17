import { test, expect } from '@playwright/test';

test.describe('Basic Functionality Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to homepage before each test
    await page.goto('/');
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');
  });

  test('homepage loads correctly', async ({ page }) => {
    // Check if the main title is visible
    await expect(page.locator('text=Welcome to the Warhammer Tavern')).toBeVisible();

    // Check if the page has the correct title
    await expect(page).toHaveTitle(/Warhammer Tavern Simulator v3/);

    // Verify that key elements are present
    await expect(page.locator('.character-gallery, [class*="character"]')).toBeVisible();
  });

  test('navigation works correctly', async ({ page }) => {
    // Test navigation to Characters page
    await page.click('text=Characters');
    await page.waitForURL('**/characters');
    await expect(page.locator('text=Character Profiles')).toBeVisible();
    
    // Test navigation to Tavern page
    await page.click('text=Tavern');
    await page.waitForURL('**/tavern');
    await expect(page.locator('text=The Golden Griffin Tavern')).toBeVisible();
    
    // Test navigation to Quests page
    await page.click('text=Quests');
    await page.waitForURL('**/quests');
    await expect(page.locator('text=Quest Board of Legends')).toBeVisible();
    
    // Test navigation to Inventory page
    await page.click('text=Inventory');
    await page.waitForURL('**/inventory');
    await expect(page.locator('text=Character Inventory')).toBeVisible();
    
    // Test navigation to Map page
    await page.click('text=Map');
    await page.waitForURL('**/map');
    await expect(page.locator('text=World Map of the Old World')).toBeVisible();
    
    // Test navigation to Conversations page
    await page.click('text=Conversations');
    await page.waitForURL('**/conversations');
    await expect(page.locator('text=Tavern Conversations')).toBeVisible();
  });

  test('responsive design works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Verify content is properly responsive
    const mainContent = page.locator('div, section, main');
    await expect(mainContent.first()).toBeVisible();
    
    // Check if text is readable (not too small)
    const headings = page.locator('h1, h2, h3');
    const headingCount = await headings.count();
    
    if (headingCount > 0) {
      const fontSize = await headings.first().evaluate(el => 
        window.getComputedStyle(el).fontSize
      );
      
      // Font size should be at least 16px on mobile
      const fontSizeNum = parseInt(fontSize);
      expect(fontSizeNum).toBeGreaterThanOrEqual(16);
    }
  });

  test('page performance is acceptable', async ({ page }) => {
    // Start performance measurement
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Page should load within 5 seconds
    expect(loadTime).toBeLessThan(5000);
    
    // Check for console errors
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    // Navigate through a few pages to check for errors
    await page.click('text=Characters');
    await page.waitForLoadState('networkidle');
    
    await page.click('text=Tavern');
    await page.waitForLoadState('networkidle');
    
    // Should have minimal console errors
    expect(errors.length).toBeLessThan(5);
  });
});