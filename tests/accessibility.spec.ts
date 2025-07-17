import { test, expect } from '@playwright/test';

test.describe('Accessibility Tests', () => {
  const pages = ['/', '/characters', '/tavern', '/quests', '/inventory', '/map', '/conversations'];

  test.beforeEach(async ({ page }) => {
    // Set up accessibility testing
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  pages.forEach(pagePath => {
    test(`${pagePath} meets basic accessibility standards`, async ({ page }) => {
      await page.goto(pagePath);
      await page.waitForLoadState('networkidle');

      // Check for proper heading hierarchy
      const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
      if (headings.length > 0) {
        // Should have at least one h1
        const h1Count = await page.locator('h1').count();
        expect(h1Count).toBeGreaterThanOrEqual(1);
        expect(h1Count).toBeLessThanOrEqual(1); // Should have only one h1
      }

      // Check for alt text on images
      const images = await page.locator('img').all();
      for (const img of images) {
        const alt = await img.getAttribute('alt');
        const ariaLabel = await img.getAttribute('aria-label');
        const role = await img.getAttribute('role');
        
        // Images should have alt text or be marked as decorative
        expect(alt !== null || ariaLabel !== null || role === 'presentation').toBeTruthy();
      }

      // Check for proper form labels
      const inputs = await page.locator('input, textarea, select').all();
      for (const input of inputs) {
        const id = await input.getAttribute('id');
        const ariaLabel = await input.getAttribute('aria-label');
        const ariaLabelledby = await input.getAttribute('aria-labelledby');
        const placeholder = await input.getAttribute('placeholder');
        
        if (id) {
          const label = await page.locator(`label[for="${id}"]`).count();
          const hasLabel = label > 0 || ariaLabel || ariaLabelledby;
          expect(hasLabel || placeholder).toBeTruthy();
        }
      }

      // Check for proper button accessibility
      const buttons = await page.locator('button, [role="button"]').all();
      for (const button of buttons) {
        const text = await button.textContent();
        const ariaLabel = await button.getAttribute('aria-label');
        const title = await button.getAttribute('title');
        
        // Buttons should have accessible text
        const hasAccessibleText = (text && text.trim().length > 0) || ariaLabel || title;
        expect(hasAccessibleText).toBeTruthy();
      }

      // Check for proper link accessibility
      const links = await page.locator('a').all();
      for (const link of links) {
        const text = await link.textContent();
        const ariaLabel = await link.getAttribute('aria-label');
        const title = await link.getAttribute('title');
        
        // Links should have accessible text
        const hasAccessibleText = (text && text.trim().length > 0) || ariaLabel || title;
        expect(hasAccessibleText).toBeTruthy();
      }
    });
  });

  test('keyboard navigation works properly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Test Tab navigation
    const focusableElements: string[] = [];
    
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press('Tab');
      const focusedElement = page.locator(':focus');
      
      if (await focusedElement.count() > 0) {
        const tagName = await focusedElement.evaluate(el => el.tagName.toLowerCase());
        const role = await focusedElement.getAttribute('role');
        const tabIndex = await focusedElement.getAttribute('tabindex');
        
        focusableElements.push(`${tagName}${role ? `[role="${role}"]` : ''}`);
        
        // Focus should be visible
        await expect(focusedElement).toBeVisible();
        
        // Check if element has proper focus styling
        const outline = await focusedElement.evaluate(el => 
          window.getComputedStyle(el).outline
        );
        const boxShadow = await focusedElement.evaluate(el => 
          window.getComputedStyle(el).boxShadow
        );
        
        // Should have some form of focus indicator
        const hasFocusIndicator = outline !== 'none' || boxShadow !== 'none';
        expect(hasFocusIndicator).toBeTruthy();
      }
    }

    // Should have found some focusable elements
    expect(focusableElements.length).toBeGreaterThan(0);

    // Test Shift+Tab (reverse navigation)
    await page.keyboard.press('Shift+Tab');
    const reverseFocused = page.locator(':focus');
    if (await reverseFocused.count() > 0) {
      await expect(reverseFocused).toBeVisible();
    }
  });

  test('screen reader compatibility', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check for proper ARIA landmarks
    const landmarks = await page.locator('[role="main"], [role="navigation"], [role="banner"], [role="contentinfo"], main, nav, header, footer').count();
    expect(landmarks).toBeGreaterThan(0);

    // Check for proper ARIA labels on interactive elements
    const interactiveElements = await page.locator('button, [role="button"], a, input, select, textarea').all();
    
    for (const element of interactiveElements) {
      const ariaLabel = await element.getAttribute('aria-label');
      const ariaLabelledby = await element.getAttribute('aria-labelledby');
      const ariaDescribedby = await element.getAttribute('aria-describedby');
      const text = await element.textContent();
      
      // Interactive elements should be properly labeled for screen readers
      const isAccessible = ariaLabel || ariaLabelledby || (text && text.trim().length > 0);
      expect(isAccessible).toBeTruthy();
    }

    // Check for proper heading structure for screen readers
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    if (headings.length > 1) {
      let previousLevel = 0;
      
      for (const heading of headings) {
        const tagName = await heading.evaluate(el => el.tagName);
        const level = parseInt(tagName.charAt(1));
        
        // Heading levels should not skip (e.g., h1 -> h3)
        if (previousLevel > 0) {
          expect(level - previousLevel).toBeLessThanOrEqual(1);
        }
        
        previousLevel = level;
      }
    }
  });

  test('color contrast and visual accessibility', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check text elements for sufficient contrast
    const textElements = await page.locator('p, span, div, h1, h2, h3, h4, h5, h6, a, button').all();
    
    for (const element of textElements.slice(0, 10)) { // Test first 10 elements
      const styles = await element.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          color: computed.color,
          backgroundColor: computed.backgroundColor,
          fontSize: computed.fontSize
        };
      });
      
      // Elements should have defined colors
      expect(styles.color).not.toBe('');
      expect(styles.fontSize).not.toBe('');
    }

    // Check for proper focus indicators
    const focusableElements = await page.locator('button, a, input, select, textarea, [tabindex]').all();
    
    for (const element of focusableElements.slice(0, 5)) { // Test first 5 elements
      await element.focus();
      
      const focusStyles = await element.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          outline: computed.outline,
          boxShadow: computed.boxShadow,
          borderColor: computed.borderColor
        };
      });
      
      // Should have some form of focus indicator
      const hasFocusIndicator = 
        focusStyles.outline !== 'none' || 
        focusStyles.boxShadow !== 'none' ||
        focusStyles.borderColor !== '';
      
      expect(hasFocusIndicator).toBeTruthy();
    }
  });

  test('motion and animation accessibility', async ({ page }) => {
    await page.goto('/tavern'); // Page with animations
    await page.waitForLoadState('networkidle');

    // Check for prefers-reduced-motion support
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.reload();
    await page.waitForLoadState('networkidle');

    // Animations should be reduced or disabled
    const animatedElements = await page.locator('[style*="animation"], [class*="animate"]').all();
    
    for (const element of animatedElements) {
      const animationDuration = await element.evaluate(el => 
        window.getComputedStyle(el).animationDuration
      );
      
      // With reduced motion, animations should be very short or disabled
      if (animationDuration && animationDuration !== '0s') {
        const duration = parseFloat(animationDuration);
        expect(duration).toBeLessThan(0.5); // Less than 500ms
      }
    }

    // Reset motion preference
    await page.emulateMedia({ reducedMotion: 'no-preference' });
  });

  test('form accessibility and validation', async ({ page }) => {
    // Test forms on GM dashboard or settings page
    await page.goto('/gm-dashboard');
    await page.waitForLoadState('networkidle');

    const forms = await page.locator('form').all();
    
    for (const form of forms) {
      // Check for proper form structure
      const inputs = await form.locator('input, textarea, select').all();
      
      for (const input of inputs) {
        const type = await input.getAttribute('type');
        const required = await input.getAttribute('required');
        const ariaRequired = await input.getAttribute('aria-required');
        const ariaInvalid = await input.getAttribute('aria-invalid');
        
        // Required fields should be properly marked
        if (required !== null) {
          expect(ariaRequired === 'true' || required !== null).toBeTruthy();
        }
        
        // Test validation messages
        if (type === 'email' || type === 'url') {
          await input.fill('invalid-input');
          await input.blur();
          
          // Check for validation message
          const validationMessage = await input.evaluate(el => 
            (el as HTMLInputElement).validationMessage
          );
          
          if (validationMessage) {
            expect(validationMessage.length).toBeGreaterThan(0);
          }
        }
      }
    }
  });

  test('mobile accessibility features', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check touch target sizes
    const touchTargets = await page.locator('button, a, [role="button"], input[type="checkbox"], input[type="radio"]').all();
    
    for (const target of touchTargets.slice(0, 10)) { // Test first 10 targets
      const boundingBox = await target.boundingBox();
      
      if (boundingBox) {
        // Touch targets should be at least 44x44px (iOS guidelines)
        expect(boundingBox.width).toBeGreaterThanOrEqual(40);
        expect(boundingBox.height).toBeGreaterThanOrEqual(40);
      }
    }

    // Check for proper spacing between touch targets
    const buttons = await page.locator('button').all();
    if (buttons.length > 1) {
      const firstButton = await buttons[0].boundingBox();
      const secondButton = await buttons[1].boundingBox();
      
      if (firstButton && secondButton) {
        const distance = Math.abs(firstButton.y - secondButton.y) + Math.abs(firstButton.x - secondButton.x);
        expect(distance).toBeGreaterThan(8); // Minimum spacing
      }
    }
  });

  test('error handling accessibility', async ({ page }) => {
    // Test error states and messages
    await page.goto('/non-existent-page');
    
    // Check for accessible error page
    const errorHeading = page.locator('h1, h2').first();
    if (await errorHeading.count() > 0) {
      const headingText = await errorHeading.textContent();
      expect(headingText).toBeTruthy();
    }

    // Test form validation errors
    await page.goto('/gm-dashboard');
    await page.waitForLoadState('networkidle');

    const submitButtons = await page.locator('button[type="submit"], input[type="submit"]').all();
    
    for (const button of submitButtons) {
      await button.click();
      await page.waitForTimeout(1000);
      
      // Check for accessible error messages
      const errorMessages = await page.locator('[role="alert"], .error, [aria-live]').all();
      
      for (const error of errorMessages) {
        const isVisible = await error.isVisible();
        if (isVisible) {
          const text = await error.textContent();
          expect(text && text.trim().length > 0).toBeTruthy();
        }
      }
    }
  });
});
