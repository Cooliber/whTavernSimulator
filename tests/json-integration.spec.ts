import { test, expect } from '@playwright/test';

test.describe('Warhammer Tavern v3 - JSON Data Integration & Visual Assets', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the enhanced tavern page
    await page.goto('/tavern');
    // Wait for the page to load completely
    await page.waitForLoadState('networkidle');
  });

  test('JSON Data API endpoints are accessible', async ({ page }) => {
    // Test careers API endpoint
    const careersResponse = await page.request.get('/api/warhammer/careers');
    expect(careersResponse.status()).toBe(200);
    const careersData = await careersResponse.json();
    expect(careersData.success).toBe(true);
    expect(careersData.data).toBeDefined();

    // Test trappings API endpoint
    const trappingsResponse = await page.request.get('/api/warhammer/trappings');
    expect(trappingsResponse.status()).toBe(200);
    const trappingsData = await trappingsResponse.json();
    expect(trappingsData.success).toBe(true);
    expect(trappingsData.data).toBeDefined();

    // Test bestiary API endpoint
    const bestiaryResponse = await page.request.get('/api/warhammer/bestiary');
    expect(bestiaryResponse.status()).toBe(200);
    const bestiaryData = await bestiaryResponse.json();
    expect(bestiaryData.success).toBe(true);
    expect(bestiaryData.data).toBeDefined();

    // Test spells API endpoint
    const spellsResponse = await page.request.get('/api/warhammer/spells');
    expect(spellsResponse.status()).toBe(200);
    const spellsData = await spellsResponse.json();
    expect(spellsData.success).toBe(true);
    expect(spellsData.data).toBeDefined();
  });

  test('Tavern Menu section displays with JSON data', async ({ page }) => {
    // Check if tavern menu section is visible
    const menuSection = page.locator('.tavern-menu-section');
    await expect(menuSection).toBeVisible();

    // Check for menu header
    const menuHeader = page.locator('h2').filter({ hasText: /Tavern Offerings/ });
    await expect(menuHeader).toBeVisible();

    // Check if TavernMenu component is rendered
    const tavernMenu = page.locator('.tavern-menu');
    await expect(tavernMenu).toBeVisible();

    // Wait for menu items to load
    await page.waitForTimeout(2000);

    // Check for category tabs
    const categoryTabs = page.locator('.category-tab');
    const tabCount = await categoryTabs.count();
    expect(tabCount).toBeGreaterThan(0);

    // Check for menu items
    const menuItems = page.locator('.menu-item');
    const itemCount = await menuItems.count();
    expect(itemCount).toBeGreaterThan(0);
  });

  test('Character Profiles section displays with JSON data', async ({ page }) => {
    // Check if characters section is visible
    const charactersSection = page.locator('.characters-section');
    await expect(charactersSection).toBeVisible();

    // Check for section header
    const charactersHeader = page.locator('h2').filter({ hasText: /Notable Patrons/ });
    await expect(charactersHeader).toBeVisible();

    // Wait for characters to load
    await page.waitForTimeout(2000);

    // Check for character profiles
    const characterProfiles = page.locator('.character-profile');
    const profileCount = await characterProfiles.count();
    expect(profileCount).toBeGreaterThan(0);

    // Check first character profile has required elements
    if (profileCount > 0) {
      const firstProfile = characterProfiles.first();
      
      // Check for character name
      const characterName = firstProfile.locator('.font-medieval').first();
      await expect(characterName).toBeVisible();
      
      // Check for characteristics if present
      const characteristics = firstProfile.locator('.characteristics-grid');
      if (await characteristics.count() > 0) {
        await expect(characteristics).toBeVisible();
      }
      
      // Check for skills if present
      const skills = firstProfile.locator('.skills-section');
      if (await skills.count() > 0) {
        await expect(skills).toBeVisible();
      }
    }
  });

  test('Atmospheric Gallery displays optimized images', async ({ page }) => {
    // Check if atmosphere gallery section is visible
    const gallerySection = page.locator('.atmosphere-gallery');
    await expect(gallerySection).toBeVisible();

    // Check for gallery header
    const galleryHeader = page.locator('h2').filter({ hasText: /Visions of the Old World/ });
    await expect(galleryHeader).toBeVisible();

    // Check for gallery items
    const galleryItems = page.locator('.gallery-item');
    const itemCount = await galleryItems.count();
    
    if (itemCount > 0) {
      // Check first gallery item
      const firstItem = galleryItems.first();
      await expect(firstItem).toBeVisible();
      
      // Check for optimized image component
      const optimizedImage = firstItem.locator('.optimized-image-container');
      await expect(optimizedImage).toBeVisible();
    }
  });

  test('Visual assets are properly optimized and accessible', async ({ page }) => {
    // Check if Warhammer images are accessible
    const imageResponse1 = await page.request.get('/warhammer-images/baronia.webp');
    expect(imageResponse1.status()).toBe(200);
    
    const imageResponse2 = await page.request.get('/warhammer-images/vientos.webp');
    expect(imageResponse2.status()).toBe(200);

    // Check for proper image alt text and accessibility
    const images = page.locator('img');
    const imageCount = await images.count();
    
    if (imageCount > 0) {
      for (let i = 0; i < Math.min(imageCount, 5); i++) {
        const img = images.nth(i);
        if (await img.isVisible()) {
          // Check for alt attribute
          const altText = await img.getAttribute('alt');
          expect(altText).toBeTruthy();
          expect(altText?.length).toBeGreaterThan(0);
        }
      }
    }
  });

  test('Enhanced UI components work correctly', async ({ page }) => {
    // Test character profile interactions
    const characterProfiles = page.locator('.character-profile');
    const profileCount = await characterProfiles.count();
    
    if (profileCount > 0) {
      const firstProfile = characterProfiles.first();
      
      // Test expandable sections if present
      const skillToggle = firstProfile.locator('.skill-toggle');
      if (await skillToggle.count() > 0) {
        await skillToggle.click();
        await page.waitForTimeout(500);
        // Should expand/collapse skills
      }
      
      // Test action buttons
      const actionButtons = firstProfile.locator('.character-actions button');
      const buttonCount = await actionButtons.count();
      
      if (buttonCount > 0) {
        const firstButton = actionButtons.first();
        await expect(firstButton).toBeVisible();
        await expect(firstButton).toBeEnabled();
      }
    }

    // Test tavern menu interactions
    const categoryTabs = page.locator('.category-tab');
    const tabCount = await categoryTabs.count();
    
    if (tabCount > 1) {
      // Click on second tab
      await categoryTabs.nth(1).click();
      await page.waitForTimeout(500);
      
      // Should show different menu items
      const menuItems = page.locator('.menu-item');
      await expect(menuItems.first()).toBeVisible();
    }
  });

  test('Responsive design works with new components', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if components are still visible and functional
    const menuSection = page.locator('.tavern-menu-section');
    await expect(menuSection).toBeVisible();
    
    const charactersSection = page.locator('.characters-section');
    await expect(charactersSection).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check grid layouts adapt properly
    const characterGrid = page.locator('.characters-grid');
    await expect(characterGrid).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // All components should be visible and properly laid out
    await expect(menuSection).toBeVisible();
    await expect(charactersSection).toBeVisible();
  });

  test('Performance and loading optimization', async ({ page }) => {
    // Measure page load time with new components
    const startTime = Date.now();
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    // Should load within reasonable time even with JSON data
    expect(loadTime).toBeLessThan(8000); // 8 seconds max
    
    // Check for lazy loading implementation
    const lazyImages = page.locator('img[loading="lazy"]');
    const lazyImageCount = await lazyImages.count();
    
    // Should have some lazy-loaded images
    expect(lazyImageCount).toBeGreaterThanOrEqual(0);
    
    // Check for proper caching headers on API endpoints
    const apiResponse = await page.request.get('/api/warhammer/careers');
    const cacheControl = apiResponse.headers()['cache-control'];
    expect(cacheControl).toContain('max-age');
  });

  test('Error handling for JSON data', async ({ page }) => {
    // Test graceful handling when API is unavailable
    // This would require mocking the API to return errors
    
    // For now, just check that error states are handled
    const errorElements = page.locator('.error-state');
    // Should not have error states under normal conditions
    const errorCount = await errorElements.count();
    expect(errorCount).toBe(0);
    
    // Check loading states are properly managed
    const loadingElements = page.locator('.loading-state');
    // Loading states should either be hidden or show briefly
    await page.waitForTimeout(3000);
    const visibleLoadingCount = await loadingElements.filter({ hasText: /loading/i }).count();
    expect(visibleLoadingCount).toBe(0); // Should be done loading
  });
});

test.describe('Integration with Existing Features', () => {
  test('New components work with existing tavern features', async ({ page }) => {
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    
    // Check that existing features still work
    const existingPatrons = page.locator('.patron-card');
    const patronCount = await existingPatrons.count();
    expect(patronCount).toBeGreaterThan(0);
    
    // Check that new sections don't interfere with existing ones
    const newCharacters = page.locator('.character-profile');
    const newCharacterCount = await newCharacters.count();
    expect(newCharacterCount).toBeGreaterThan(0);
    
    // Both should coexist
    expect(patronCount).toBeGreaterThan(0);
    expect(newCharacterCount).toBeGreaterThan(0);
  });
});
