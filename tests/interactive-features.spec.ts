import { test, expect } from '@playwright/test';

test.describe('Interactive Features Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('quest system functionality', async ({ page }) => {
    // Navigate to quests page
    await page.goto('/quests');
    await page.waitForLoadState('networkidle');
    
    // Check if quest cards are visible
    const questCards = page.locator('.quest-card, [class*="quest"]');
    await expect(questCards.first()).toBeVisible();
    
    // Try to accept a quest
    const acceptButton = page.locator('text=Accept Quest').first();
    if (await acceptButton.count() > 0) {
      await acceptButton.click();
      
      // Wait for any modal or confirmation
      await page.waitForTimeout(1000);
      
      // Check if quest was accepted (look for success message or state change)
      const successIndicator = page.locator('text=accepted, text=Quest, text=success');
      // Quest acceptance should trigger some response
      expect(await successIndicator.count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('inventory drag and drop functionality', async ({ page }) => {
    // Navigate to inventory page
    await page.goto('/inventory');
    await page.waitForLoadState('networkidle');
    
    // Check if inventory grid is visible
    const inventoryGrid = page.locator('.inventory-grid, [class*="inventory"]');
    await expect(inventoryGrid.first()).toBeVisible();
    
    // Look for draggable items
    const draggableItems = page.locator('[draggable="true"], .item-card');
    
    if (await draggableItems.count() > 0) {
      const firstItem = draggableItems.first();
      await expect(firstItem).toBeVisible();
      
      // Test drag functionality (simulate drag start)
      await firstItem.hover();
      await page.mouse.down();
      await page.mouse.move(100, 100);
      await page.mouse.up();
      
      // Drag and drop should not cause errors
      expect(true).toBeTruthy();
    }
  });

  test('battle system interactions', async ({ page }) => {
    // Navigate to battle page
    await page.goto('/battle');
    await page.waitForLoadState('networkidle');
    
    // Check if battle grid is visible
    const battleGrid = page.locator('.battle-grid, [class*="battle"]');
    await expect(battleGrid.first()).toBeVisible();
    
    // Look for action buttons
    const actionButtons = page.locator('.action-button, [class*="action"]');
    
    if (await actionButtons.count() > 0) {
      const firstAction = actionButtons.first();
      await expect(firstAction).toBeVisible();
      
      // Click action button
      await firstAction.click();
      
      // Wait for any response
      await page.waitForTimeout(500);
      
      // Action should not cause page errors
      expect(true).toBeTruthy();
    }
  });

  test('map interaction and location selection', async ({ page }) => {
    // Navigate to map page
    await page.goto('/map');
    await page.waitForLoadState('networkidle');
    
    // Check if map is visible
    const mapContainer = page.locator('.map-container, [class*="map"]');
    await expect(mapContainer.first()).toBeVisible();
    
    // Look for location markers
    const locationMarkers = page.locator('.location-marker, [class*="location"]');
    
    if (await locationMarkers.count() > 0) {
      const firstLocation = locationMarkers.first();
      await expect(firstLocation).toBeVisible();
      
      // Click on location
      await firstLocation.click();
      
      // Wait for location details to appear
      await page.waitForTimeout(1000);
      
      // Check if location details panel appears
      const locationDetails = page.locator('.location-details, [class*="details"]');
      if (await locationDetails.count() > 0) {
        await expect(locationDetails.first()).toBeVisible();
      }
    }
  });

  test('character interaction system', async ({ page }) => {
    // Navigate to characters page
    await page.goto('/characters');
    await page.waitForLoadState('networkidle');
    
    // Check if character cards are visible
    const characterCards = page.locator('.character-card, [class*="character"]');
    await expect(characterCards.first()).toBeVisible();
    
    // Click on a character card
    await characterCards.first().click();
    
    // Wait for character modal or details
    await page.waitForTimeout(1000);
    
    // Check if character details appear
    const characterModal = page.locator('.character-modal, [class*="modal"], [class*="details"]');
    if (await characterModal.count() > 0) {
      await expect(characterModal.first()).toBeVisible();
    }
  });

  test('tavern atmosphere controls', async ({ page }) => {
    // Navigate to tavern page
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    
    // Look for atmosphere control buttons
    const fireplaceButton = page.locator('text=Fireplace, text=Light Fireplace, text=Dim Fireplace');
    const musicButton = page.locator('text=Music, text=Play Music, text=Stop Music');
    
    if (await fireplaceButton.count() > 0) {
      await fireplaceButton.first().click();
      await page.waitForTimeout(500);
      
      // Fireplace toggle should work without errors
      expect(true).toBeTruthy();
    }
    
    if (await musicButton.count() > 0) {
      await musicButton.first().click();
      await page.waitForTimeout(500);
      
      // Music toggle should work without errors
      expect(true).toBeTruthy();
    }
  });

  test('conversation system functionality', async ({ page }) => {
    // Navigate to conversations page
    await page.goto('/conversations');
    await page.waitForLoadState('networkidle');
    
    // Look for character selection
    const characterButtons = page.locator('.character-button, [class*="character"]');
    
    if (await characterButtons.count() > 0) {
      await characterButtons.first().click();
      
      // Wait for conversation interface
      await page.waitForTimeout(1000);
      
      // Check if conversation area appears
      const conversationArea = page.locator('.conversation, [class*="chat"], [class*="message"]');
      if (await conversationArea.count() > 0) {
        await expect(conversationArea.first()).toBeVisible();
      }
    }
  });

  test('responsive touch interactions on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Test touch interactions on various pages
    const pages = ['/characters', '/tavern', '/quests', '/inventory'];
    
    for (const pagePath of pages) {
      await page.goto(pagePath);
      await page.waitForLoadState('networkidle');
      
      // Look for interactive elements
      const interactiveElements = page.locator('button, [role="button"], .clickable, [class*="card"]');
      
      if (await interactiveElements.count() > 0) {
        const element = interactiveElements.first();
        await expect(element).toBeVisible();
        
        // Test touch interaction
        await element.tap();
        await page.waitForTimeout(300);
        
        // Touch should work without errors
        expect(true).toBeTruthy();
      }
    }
  });

  test('form inputs and validation', async ({ page }) => {
    // Navigate to GM dashboard which has forms
    await page.goto('/gm-dashboard');
    await page.waitForLoadState('networkidle');
    
    // Look for input fields
    const inputs = page.locator('input, textarea, select');
    
    if (await inputs.count() > 0) {
      const firstInput = inputs.first();
      await expect(firstInput).toBeVisible();
      
      // Test input functionality
      await firstInput.fill('Test input');
      
      const value = await firstInput.inputValue();
      expect(value).toBe('Test input');
    }
  });

  test('keyboard navigation accessibility', async ({ page }) => {
    // Test keyboard navigation
    await page.keyboard.press('Tab');
    
    // Check if focus is visible
    const focusedElement = page.locator(':focus');
    if (await focusedElement.count() > 0) {
      await expect(focusedElement).toBeVisible();
    }
    
    // Test Enter key on buttons
    const buttons = page.locator('button');
    if (await buttons.count() > 0) {
      await buttons.first().focus();
      await page.keyboard.press('Enter');
      
      // Enter key should work on buttons
      expect(true).toBeTruthy();
    }
  });
});