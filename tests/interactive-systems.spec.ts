import { test, expect } from '@playwright/test';

test.describe('Warhammer Tavern v3 - Interactive Systems', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    
    // Wait for interactive systems to initialize
    await page.waitForTimeout(3000);
  });

  test('Interactive features section displays correctly', async ({ page }) => {
    // Check if interactive systems section is visible
    const interactiveSection = page.locator('.interactive-systems');
    await expect(interactiveSection).toBeVisible();

    // Check for section header
    const sectionHeader = page.locator('h2').filter({ hasText: /Interactive Experiences/ });
    await expect(sectionHeader).toBeVisible();

    // Check for feature cards
    const featureCards = page.locator('.feature-card');
    const cardCount = await featureCards.count();
    expect(cardCount).toBe(4); // AI Conversations, Tavern Games, Character Growth, Reputation System

    // Verify each feature card has required elements
    for (let i = 0; i < cardCount; i++) {
      const card = featureCards.nth(i);
      await expect(card.locator('.feature-icon')).toBeVisible();
      await expect(card.locator('h3')).toBeVisible();
      await expect(card.locator('p')).toBeVisible();
      await expect(card.locator('.feature-stats')).toBeVisible();
    }
  });

  test('AI Conversations feature works correctly', async ({ page }) => {
    // Click on AI Conversations feature
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Check if NPC selection appears
    const npcSelection = page.locator('.npc-selection');
    await expect(npcSelection).toBeVisible();

    // Check for available NPCs
    const npcCards = page.locator('.npc-card');
    const npcCount = await npcCards.count();
    expect(npcCount).toBeGreaterThan(0);

    // Click on first NPC to start conversation
    if (npcCount > 0) {
      await npcCards.first().click();
      
      // Check if conversation interface appears
      const conversationInterface = page.locator('.npc-conversation');
      await expect(conversationInterface).toBeVisible();
      
      // Check for conversation elements
      await expect(page.locator('.conversation-header')).toBeVisible();
      await expect(page.locator('.conversation-history')).toBeVisible();
      await expect(page.locator('.conversation-input')).toBeVisible();
      
      // Check for initial greeting message
      const messages = page.locator('.message');
      const messageCount = await messages.count();
      expect(messageCount).toBeGreaterThan(0);
      
      // Test sending a message
      const textInput = page.locator('textarea[placeholder="Type your response..."]');
      await textInput.fill('Hello, how are you today?');
      
      const sendButton = page.locator('button').filter({ hasText: /send/i });
      await sendButton.click();
      
      // Wait for AI response
      await page.waitForTimeout(2000);
      
      // Check if message was added
      const newMessageCount = await page.locator('.message').count();
      expect(newMessageCount).toBeGreaterThan(messageCount);
    }
  });

  test('Mini Games feature works correctly', async ({ page }) => {
    // Click on Tavern Games feature
    const gamesCard = page.locator('.feature-card').filter({ hasText: /Tavern Games/ });
    await gamesCard.click();

    // Check if mini games interface appears
    const miniGamesHub = page.locator('.mini-games-hub');
    await expect(miniGamesHub).toBeVisible();

    // Check for games overview
    const gamesOverview = page.locator('.games-overview');
    await expect(gamesOverview).toBeVisible();

    // Check for available games
    const gameCards = page.locator('.game-card');
    const gameCount = await gameCards.count();
    expect(gameCount).toBeGreaterThan(0);

    // Test clicking on a game (if available and affordable)
    if (gameCount > 0) {
      const firstGame = gameCards.first();
      const isActive = await firstGame.locator('.status-badge').filter({ hasText: /Ready to Play/ }).count() > 0;
      
      if (isActive) {
        await firstGame.click();
        
        // Check if game interface appears
        const activeGame = page.locator('.active-game');
        await expect(activeGame).toBeVisible();
        
        // Check for game header
        await expect(page.locator('.game-header')).toBeVisible();
        
        // Check for game content
        await expect(page.locator('.game-content')).toBeVisible();
      }
    }
  });

  test('Character Progression feature works correctly', async ({ page }) => {
    // Click on Character Growth feature
    const progressionCard = page.locator('.feature-card').filter({ hasText: /Character Growth/ });
    await progressionCard.click();

    // Check if character progression interface appears
    const characterProgression = page.locator('.character-progression');
    await expect(characterProgression).toBeVisible();

    // Check for character overview
    const characterOverview = page.locator('.character-overview');
    await expect(characterOverview).toBeVisible();

    // Check for character info elements
    await expect(page.locator('.character-info')).toBeVisible();
    await expect(page.locator('.experience-progress')).toBeVisible();

    // Check for attributes section
    const attributesSection = page.locator('.attributes-section');
    await expect(attributesSection).toBeVisible();
    
    const attributeItems = page.locator('.attribute-item');
    const attributeCount = await attributeItems.count();
    expect(attributeCount).toBe(6); // 6 core attributes

    // Check for skills section
    const skillsSection = page.locator('.skills-section');
    await expect(skillsSection).toBeVisible();

    // Check for achievements section
    const achievementsSection = page.locator('.achievements-section');
    await expect(achievementsSection).toBeVisible();

    // Check for recent activity
    const recentActivity = page.locator('.recent-activity');
    await expect(recentActivity).toBeVisible();
  });

  test('Reputation System feature works correctly', async ({ page }) => {
    // Click on Reputation System feature
    const reputationCard = page.locator('.feature-card').filter({ hasText: /Reputation System/ });
    await reputationCard.click();

    // Check if reputation interface appears
    const reputationSection = page.locator('.reputation-section');
    await expect(reputationSection).toBeVisible();

    // Check for reputation dashboard
    const reputationDashboard = page.locator('.reputation-dashboard');
    await expect(reputationDashboard).toBeVisible();

    // Check for overall reputation card
    const overallReputationCard = page.locator('.reputation-card');
    await expect(overallReputationCard).toBeVisible();
    
    // Check for reputation meter
    await expect(page.locator('.reputation-meter')).toBeVisible();

    // Check for faction standings
    const factionStandings = page.locator('.faction-standings');
    await expect(factionStandings).toBeVisible();

    // Check for economy status
    const economyStatus = page.locator('.economy-status');
    await expect(economyStatus).toBeVisible();
    
    // Check for currency display
    const currencyDisplay = page.locator('.currency-display');
    await expect(currencyDisplay).toBeVisible();
    
    const currencyItems = page.locator('.currency-item');
    const currencyCount = await currencyItems.count();
    expect(currencyCount).toBe(3); // Gold, Silver, Brass
  });

  test('Feature navigation works correctly', async ({ page }) => {
    // Test opening and closing features
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Check if feature is open
    const activeFeature = page.locator('.active-feature-container');
    await expect(activeFeature).toBeVisible();

    // Check for close button
    const closeButton = page.locator('button').filter({ hasText: /Close/ });
    await expect(closeButton).toBeVisible();

    // Click close button
    await closeButton.click();

    // Check if feature is closed
    await expect(activeFeature).not.toBeVisible();

    // Test opening different feature
    const gamesCard = page.locator('.feature-card').filter({ hasText: /Tavern Games/ });
    await gamesCard.click();

    // Check if different feature content appears
    const miniGamesHub = page.locator('.mini-games-hub');
    await expect(miniGamesHub).toBeVisible();
  });

  test('Interactive systems integrate with existing features', async ({ page }) => {
    // Check that existing tavern features still work
    const existingPatrons = page.locator('.patron-card');
    const patronCount = await existingPatrons.count();
    expect(patronCount).toBeGreaterThan(0);

    // Check that new interactive features don't interfere
    const interactiveFeatures = page.locator('.feature-card');
    const featureCount = await interactiveFeatures.count();
    expect(featureCount).toBe(4);

    // Both should coexist
    expect(patronCount).toBeGreaterThan(0);
    expect(featureCount).toBe(4);

    // Check that tavern menu still works
    const tavernMenu = page.locator('.tavern-menu');
    await expect(tavernMenu).toBeVisible();

    // Check that character profiles still work
    const characterProfiles = page.locator('.character-profile');
    const profileCount = await characterProfiles.count();
    expect(profileCount).toBeGreaterThan(0);
  });

  test('Responsive design works with interactive features', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if interactive features are still accessible
    const interactiveSection = page.locator('.interactive-systems');
    await expect(interactiveSection).toBeVisible();
    
    const featureCards = page.locator('.feature-card');
    await expect(featureCards.first()).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check grid layouts adapt properly
    const featuresGrid = page.locator('.features-grid');
    await expect(featuresGrid).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // All features should be visible and properly laid out
    await expect(interactiveSection).toBeVisible();
    const featureCount = await featureCards.count();
    expect(featureCount).toBe(4);
  });

  test('Performance with interactive systems', async ({ page }) => {
    // Measure page load time with interactive systems
    const startTime = Date.now();
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    // Should load within reasonable time even with interactive systems
    expect(loadTime).toBeLessThan(10000); // 10 seconds max
    
    // Check that interactive features don't cause memory leaks
    // by opening and closing multiple features
    const features = ['conversations', 'games', 'progression', 'reputation'];
    
    for (const feature of features) {
      const featureCard = page.locator('.feature-card').nth(features.indexOf(feature));
      await featureCard.click();
      await page.waitForTimeout(1000);
      
      const closeButton = page.locator('button').filter({ hasText: /Close/ });
      if (await closeButton.count() > 0) {
        await closeButton.click();
        await page.waitForTimeout(500);
      }
    }
    
    // Page should still be responsive after multiple interactions
    const finalFeatureCard = page.locator('.feature-card').first();
    await expect(finalFeatureCard).toBeVisible();
  });

  test('Error handling in interactive systems', async ({ page }) => {
    // Test graceful handling when systems fail to initialize
    // This would require mocking failures, but for now check error states
    
    // Check that error states are handled gracefully
    const errorElements = page.locator('.error-state');
    const errorCount = await errorElements.count();
    
    // Should not have visible error states under normal conditions
    expect(errorCount).toBe(0);
    
    // Check that loading states are properly managed
    await page.waitForTimeout(5000);
    const loadingElements = page.locator('.loading-state');
    const visibleLoadingCount = await loadingElements.filter({ hasText: /loading/i }).count();
    
    // Loading states should be resolved
    expect(visibleLoadingCount).toBe(0);
  });
});
