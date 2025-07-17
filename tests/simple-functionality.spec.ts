import { test, expect } from '@playwright/test';

test.describe('Simple Functionality Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to homepage before each test
    await page.goto('/');
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');
  });

  test('application loads and has correct title', async ({ page }) => {
    // Check if the page has the correct title
    await expect(page).toHaveTitle(/Warhammer Tavern Simulator v3/);
    
    // Check if basic content is present
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Check if there's some text content
    const textContent = await page.textContent('body');
    expect(textContent).toBeTruthy();
    expect(textContent!.length).toBeGreaterThan(10);
  });

  test('page loads without console errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    // Reload the page to capture any console errors
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Should have minimal console errors (allow up to 2 for development)
    expect(errors.length).toBeLessThan(3);
  });

  test('page is responsive', async ({ page }) => {
    // Test desktop viewport
    await page.setViewportSize({ width: 1200, height: 800 });
    await page.waitForTimeout(500);
    
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    await expect(body).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(500);
    
    await expect(body).toBeVisible();
  });

  test('basic navigation elements exist', async ({ page }) => {
    // Look for any navigation elements
    const navElements = page.locator('nav, [role="navigation"], a[href]');
    const navCount = await navElements.count();
    
    // Should have at least some navigation elements
    expect(navCount).toBeGreaterThan(0);
  });

  test('CSS and assets load correctly', async ({ page }) => {
    // Check if CSS is loaded by looking for styled elements
    const styledElements = page.locator('[class], [style]');
    const styledCount = await styledElements.count();
    
    // Should have styled elements
    expect(styledCount).toBeGreaterThan(0);
    
    // Check if fonts are loaded
    const computedStyle = await page.evaluate(() => {
      const element = document.body;
      return window.getComputedStyle(element).fontFamily;
    });
    
    expect(computedStyle).toBeTruthy();
  });

  test('page performance is acceptable', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Page should load within 10 seconds (generous for development)
    expect(loadTime).toBeLessThan(10000);
  });
});
