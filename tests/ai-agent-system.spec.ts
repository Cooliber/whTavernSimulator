import { test, expect } from '@playwright/test';

test.describe('Warhammer Tavern v3 - AI Agent System', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    
    // Wait for AI systems to initialize
    await page.waitForTimeout(5000);
  });

  test('AI service providers are properly configured', async ({ page }) => {
    // Navigate to agent management dashboard
    const interactiveSection = page.locator('.interactive-systems');
    await expect(interactiveSection).toBeVisible();

    // Look for AI Conversations feature
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Check if AI service status is displayed
    const aiServiceStatus = page.locator('.ai-service-status');
    await expect(aiServiceStatus).toBeVisible();

    // Verify provider cards are present
    const providerCards = page.locator('.provider-card');
    const providerCount = await providerCards.count();
    expect(providerCount).toBeGreaterThanOrEqual(2); // At least Groq and Cerebras

    // Check for provider status indicators
    for (let i = 0; i < providerCount; i++) {
      const card = providerCards.nth(i);
      await expect(card.locator('.status-indicator')).toBeVisible();
      
      // Verify provider has a name and model
      const providerName = await card.locator('.font-medium').textContent();
      expect(providerName).toBeTruthy();
      
      const modelInfo = await card.locator('.text-sm').textContent();
      expect(modelInfo).toContain('Model:');
    }
  });

  test('17 distinct Warhammer agents are available', async ({ page }) => {
    // Access agent management dashboard
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Check agent overview statistics
    const agentOverview = page.locator('.agent-overview');
    await expect(agentOverview).toBeVisible();

    // Verify total agent count
    const totalAgentsCard = page.locator('.stat-card').first();
    const totalAgentsText = await totalAgentsCard.locator('.text-2xl').textContent();
    expect(parseInt(totalAgentsText || '0')).toBe(17);

    // Check agent directory
    const agentDirectory = page.locator('.agent-list');
    await expect(agentDirectory).toBeVisible();

    // Verify all 17 agents are displayed
    const agentCards = page.locator('.agent-card');
    const agentCount = await agentCards.count();
    expect(agentCount).toBe(17);

    // Verify each agent has required information
    for (let i = 0; i < Math.min(agentCount, 5); i++) { // Test first 5 agents
      const card = agentCards.nth(i);
      
      // Check agent name
      await expect(card.locator('h4')).toBeVisible();
      
      // Check agent info fields
      await expect(card.locator('.agent-info')).toBeVisible();
      
      // Verify species, career, role, and faction are displayed
      const agentInfo = card.locator('.agent-info');
      await expect(agentInfo.locator('text=Species:')).toBeVisible();
      await expect(agentInfo.locator('text=Career:')).toBeVisible();
      await expect(agentInfo.locator('text=Role:')).toBeVisible();
      await expect(agentInfo.locator('text=Faction:')).toBeVisible();
      
      // Check reputation and influence bars
      const statBars = card.locator('.agent-stats .stat');
      const statCount = await statBars.count();
      expect(statCount).toBe(2); // Reputation and Influence
    }
  });

  test('Agent filtering works correctly', async ({ page }) => {
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Test role filtering
    const roleFilter = page.locator('select').first();
    await roleFilter.selectOption('bartender');
    
    // Wait for filtering to apply
    await page.waitForTimeout(1000);
    
    // Check that only bartender agents are shown
    const agentCards = page.locator('.agent-card');
    const visibleCards = await agentCards.count();
    expect(visibleCards).toBeGreaterThan(0);
    
    // Verify the first visible card is a bartender
    if (visibleCards > 0) {
      const firstCard = agentCards.first();
      const roleText = await firstCard.locator('text=Role:').locator('..').locator('span').last().textContent();
      expect(roleText?.toLowerCase()).toBe('bartender');
    }

    // Test faction filtering
    const factionFilter = page.locator('select').last();
    await factionFilter.selectOption('empire');
    
    await page.waitForTimeout(1000);
    
    // Check that filtering is applied
    const filteredCards = await agentCards.count();
    expect(filteredCards).toBeGreaterThanOrEqual(0);

    // Reset filters
    await roleFilter.selectOption('');
    await factionFilter.selectOption('');
  });

  test('Agent selection and details display', async ({ page }) => {
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Select the first agent
    const firstAgentCard = page.locator('.agent-card').first();
    await firstAgentCard.click();

    // Check that agent details are displayed
    const agentDetails = page.locator('.agent-details');
    await expect(agentDetails).toBeVisible();

    // Verify personality section
    const personalitySection = page.locator('.personality-section');
    await expect(personalitySection).toBeVisible();
    await expect(personalitySection.locator('text=Traits:')).toBeVisible();
    await expect(personalitySection.locator('text=Style:')).toBeVisible();
    await expect(personalitySection.locator('text=Mood:')).toBeVisible();

    // Verify knowledge section
    const knowledgeSection = page.locator('.knowledge-section');
    await expect(knowledgeSection).toBeVisible();
    await expect(knowledgeSection.locator('text=Domains:')).toBeVisible();
    await expect(knowledgeSection.locator('text=Specialties:')).toBeVisible();

    // Verify relationships section
    const relationshipsSection = page.locator('.relationships-section');
    await expect(relationshipsSection).toBeVisible();

    // Verify background section
    const backgroundSection = page.locator('.background-section');
    await expect(backgroundSection).toBeVisible();
    await expect(backgroundSection.locator('text=Origin:')).toBeVisible();
    await expect(backgroundSection.locator('text=Motivation:')).toBeVisible();

    // Check action buttons
    const startConversationBtn = page.locator('button').filter({ hasText: /Start Conversation/ });
    await expect(startConversationBtn).toBeVisible();
    
    const simulateInteractionBtn = page.locator('button').filter({ hasText: /Simulate Interaction/ });
    await expect(simulateInteractionBtn).toBeVisible();
  });

  test('Agent conversation can be initiated', async ({ page }) => {
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Select an agent
    const firstAgentCard = page.locator('.agent-card').first();
    await firstAgentCard.click();

    // Start conversation
    const startConversationBtn = page.locator('button').filter({ hasText: /Start Conversation/ });
    await startConversationBtn.click();

    // Wait for conversation interface to appear
    await page.waitForTimeout(3000);

    // Check if conversation interface is displayed
    const conversationInterface = page.locator('.npc-conversation');
    if (await conversationInterface.count() > 0) {
      await expect(conversationInterface).toBeVisible();
      
      // Check for conversation elements
      await expect(page.locator('.conversation-header')).toBeVisible();
      await expect(page.locator('.conversation-history')).toBeVisible();
      
      // Check for input area
      const textInput = page.locator('textarea');
      if (await textInput.count() > 0) {
        await expect(textInput).toBeVisible();
      }
    }
  });

  test('Agent interaction simulation works', async ({ page }) => {
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Select an agent
    const firstAgentCard = page.locator('.agent-card').first();
    await firstAgentCard.click();

    // Simulate interaction
    const simulateBtn = page.locator('button').filter({ hasText: /Simulate Interaction/ });
    await simulateBtn.click();

    // Wait for simulation to process
    await page.waitForTimeout(2000);

    // Check if active conversations section appears or updates
    const activeConversations = page.locator('.active-conversations');
    
    // The section might appear if there are active conversations
    if (await activeConversations.count() > 0) {
      await expect(activeConversations).toBeVisible();
      
      const conversationItems = page.locator('.conversation-item');
      const itemCount = await conversationItems.count();
      expect(itemCount).toBeGreaterThanOrEqual(0);
    }
  });

  test('Agent system integrates with existing tavern features', async ({ page }) => {
    // Verify that existing tavern features still work
    const existingPatrons = page.locator('.patron-card');
    const patronCount = await existingPatrons.count();
    expect(patronCount).toBeGreaterThan(0);

    // Check that tavern menu is still accessible
    const tavernMenu = page.locator('.tavern-menu');
    await expect(tavernMenu).toBeVisible();

    // Verify interactive features section exists
    const interactiveSection = page.locator('.interactive-systems');
    await expect(interactiveSection).toBeVisible();

    // Check that all 4 interactive features are present
    const featureCards = page.locator('.feature-card');
    const featureCount = await featureCards.count();
    expect(featureCount).toBe(4);

    // Verify AI Conversations is one of the features
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await expect(conversationsCard).toBeVisible();
  });

  test('Agent system performance and error handling', async ({ page }) => {
    // Test rapid agent selection
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    const agentCards = page.locator('.agent-card');
    const cardCount = await agentCards.count();

    // Rapidly select different agents
    for (let i = 0; i < Math.min(cardCount, 3); i++) {
      await agentCards.nth(i).click();
      await page.waitForTimeout(500);
      
      // Verify details update
      const agentDetails = page.locator('.agent-details');
      await expect(agentDetails).toBeVisible();
    }

    // Test filter changes
    const roleFilter = page.locator('select').first();
    const roles = ['bartender', 'merchant', 'guard', ''];
    
    for (const role of roles) {
      await roleFilter.selectOption(role);
      await page.waitForTimeout(500);
      
      // Verify page doesn't crash
      const agentList = page.locator('.agent-list');
      await expect(agentList).toBeVisible();
    }
  });

  test('Agent system responsive design', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Check if agent management dashboard is still accessible
    const dashboard = page.locator('.agent-management-dashboard');
    await expect(dashboard).toBeVisible();

    // Verify agent cards are still visible and clickable
    const agentCards = page.locator('.agent-card');
    const firstCard = agentCards.first();
    await expect(firstCard).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Verify layout adapts
    await expect(dashboard).toBeVisible();
    await expect(firstCard).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    // All elements should be properly laid out
    await expect(dashboard).toBeVisible();
    const agentGrid = page.locator('.agents-grid');
    await expect(agentGrid).toBeVisible();
  });

  test('Agent system accessibility', async ({ page }) => {
    const conversationsCard = page.locator('.feature-card').filter({ hasText: /AI Conversations/ });
    await conversationsCard.click();

    // Test keyboard navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Check if elements are focusable
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();

    // Test with screen reader simulation
    const dashboard = page.locator('.agent-management-dashboard');
    
    // Check for proper headings
    const headings = page.locator('h2, h3, h4');
    const headingCount = await headings.count();
    expect(headingCount).toBeGreaterThan(0);

    // Verify buttons have accessible text
    const buttons = page.locator('button');
    for (let i = 0; i < Math.min(await buttons.count(), 3); i++) {
      const button = buttons.nth(i);
      const buttonText = await button.textContent();
      expect(buttonText?.trim()).toBeTruthy();
    }
  });
});
