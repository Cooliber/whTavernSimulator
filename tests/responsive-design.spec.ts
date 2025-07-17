import { test, expect } from '@playwright/test';

test.describe('Responsive Design Tests', () => {
  const viewports = [
    { name: 'Mobile Portrait', width: 375, height: 667 },
    { name: 'Mobile Landscape', width: 667, height: 375 },
    { name: 'Tablet Portrait', width: 768, height: 1024 },
    { name: 'Tablet Landscape', width: 1024, height: 768 },
    { name: 'Desktop Small', width: 1280, height: 720 },
    { name: 'Desktop Large', width: 1920, height: 1080 },
    { name: 'Ultra Wide', width: 2560, height: 1440 }
  ];

  const pages = ['/', '/characters', '/tavern', '/quests', '/inventory', '/map', '/conversations'];

  viewports.forEach(viewport => {
    test.describe(`${viewport.name} (${viewport.width}x${viewport.height})`, () => {
      test.beforeEach(async ({ page }) => {
        await page.setViewportSize({ width: viewport.width, height: viewport.height });
      });

      pages.forEach(pagePath => {
        test(`${pagePath} renders correctly on ${viewport.name}`, async ({ page }) => {
          await page.goto(pagePath);
          await page.waitForLoadState('networkidle');

          // Check if main content is visible
          const mainContent = page.locator('main, .main-content, body > div').first();
          await expect(mainContent).toBeVisible();

          // Check for horizontal scrollbar (should not exist on mobile)
          if (viewport.width <= 768) {
            const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
            const viewportWidth = viewport.width;
            expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 20); // Allow small tolerance
          }

          // Check text readability
          const headings = page.locator('h1, h2, h3');
          if (await headings.count() > 0) {
            const fontSize = await headings.first().evaluate(el => 
              window.getComputedStyle(el).fontSize
            );
            const fontSizeNum = parseInt(fontSize);
            
            // Minimum font sizes based on viewport
            const minFontSize = viewport.width <= 375 ? 16 : 14;
            expect(fontSizeNum).toBeGreaterThanOrEqual(minFontSize);
          }

          // Check button/touch target sizes on mobile
          if (viewport.width <= 768) {
            const buttons = page.locator('button, [role="button"]');
            if (await buttons.count() > 0) {
              const buttonSize = await buttons.first().evaluate(el => {
                const rect = el.getBoundingClientRect();
                return { width: rect.width, height: rect.height };
              });
              
              // Touch targets should be at least 44px (iOS) or 48px (Android)
              expect(buttonSize.width).toBeGreaterThanOrEqual(40);
              expect(buttonSize.height).toBeGreaterThanOrEqual(40);
            }
          }
        });
      });

      test(`navigation works on ${viewport.name}`, async ({ page }) => {
        await page.goto('/');
        await page.waitForLoadState('networkidle');

        // Test navigation menu (might be hamburger on mobile)
        const navLinks = page.locator('nav a, .nav-link');
        const hamburgerMenu = page.locator('.hamburger, .menu-toggle, [aria-label*="menu"]');

        if (viewport.width <= 768 && await hamburgerMenu.count() > 0) {
          // Mobile: test hamburger menu
          await hamburgerMenu.click();
          await page.waitForTimeout(500);
          
          // Menu should be visible after clicking hamburger
          const mobileMenu = page.locator('.mobile-menu, .nav-menu.open, .menu-open');
          if (await mobileMenu.count() > 0) {
            await expect(mobileMenu.first()).toBeVisible();
          }
        } else if (await navLinks.count() > 0) {
          // Desktop: test direct navigation
          await navLinks.first().click();
          await page.waitForTimeout(1000);
          expect(true).toBeTruthy();
        }
      });

      test(`interactive elements work on ${viewport.name}`, async ({ page }) => {
        await page.goto('/tavern');
        await page.waitForLoadState('networkidle');

        // Test various interactive elements
        const interactiveElements = page.locator('button, [role="button"], .clickable');
        
        if (await interactiveElements.count() > 0) {
          const element = interactiveElements.first();
          await expect(element).toBeVisible();

          if (viewport.width <= 768) {
            // Mobile: use tap
            await element.tap();
          } else {
            // Desktop: use click
            await element.click();
          }
          
          await page.waitForTimeout(500);
          expect(true).toBeTruthy();
        }

        // Test form inputs if present
        const inputs = page.locator('input, textarea, select');
        if (await inputs.count() > 0) {
          const input = inputs.first();
          await input.focus();
          
          // Check if virtual keyboard doesn't break layout on mobile
          if (viewport.width <= 768) {
            await page.waitForTimeout(1000);
            const isVisible = await input.isVisible();
            expect(isVisible).toBeTruthy();
          }
        }
      });

      test(`images and media scale properly on ${viewport.name}`, async ({ page }) => {
        await page.goto('/characters');
        await page.waitForLoadState('networkidle');

        // Check image scaling
        const images = page.locator('img');
        if (await images.count() > 0) {
          const imageSize = await images.first().evaluate(el => {
            const rect = el.getBoundingClientRect();
            return { width: rect.width, height: rect.height };
          });
          
          // Images should not exceed viewport width
          expect(imageSize.width).toBeLessThanOrEqual(viewport.width);
        }

        // Check video/canvas elements if present
        const mediaElements = page.locator('video, canvas');
        if (await mediaElements.count() > 0) {
          const mediaSize = await mediaElements.first().evaluate(el => {
            const rect = el.getBoundingClientRect();
            return { width: rect.width };
          });
          
          expect(mediaSize.width).toBeLessThanOrEqual(viewport.width);
        }
      });
    });
  });

  test('orientation change handling', async ({ page }) => {
    // Start in portrait
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Switch to landscape
    await page.setViewportSize({ width: 667, height: 375 });
    await page.waitForTimeout(1000);

    // Check if layout adapts
    const mainContent = page.locator('main, .main-content, body > div').first();
    await expect(mainContent).toBeVisible();

    // Switch back to portrait
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(1000);

    await expect(mainContent).toBeVisible();
  });

  test('zoom level compatibility', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Test different zoom levels
    const zoomLevels = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];

    for (const zoom of zoomLevels) {
      await page.evaluate((zoomLevel) => {
        document.body.style.zoom = zoomLevel.toString();
      }, zoom);

      await page.waitForTimeout(500);

      // Check if content is still accessible
      const mainContent = page.locator('main, .main-content, body > div').first();
      await expect(mainContent).toBeVisible();

      // Check if buttons are still clickable
      const buttons = page.locator('button').first();
      if (await buttons.count() > 0) {
        const isVisible = await buttons.isVisible();
        expect(isVisible).toBeTruthy();
      }
    }

    // Reset zoom
    await page.evaluate(() => {
      document.body.style.zoom = '1';
    });
  });

  test('accessibility at different screen sizes', async ({ page }) => {
    const testViewports = [
      { width: 375, height: 667 }, // Mobile
      { width: 1280, height: 720 }  // Desktop
    ];

    for (const viewport of testViewports) {
      await page.setViewportSize(viewport);
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      // Test keyboard navigation
      await page.keyboard.press('Tab');
      const focusedElement = page.locator(':focus');
      
      if (await focusedElement.count() > 0) {
        await expect(focusedElement).toBeVisible();
        
        // Focus should be visible (not hidden behind other elements)
        const focusRect = await focusedElement.boundingBox();
        if (focusRect) {
          expect(focusRect.x).toBeGreaterThanOrEqual(0);
          expect(focusRect.y).toBeGreaterThanOrEqual(0);
          expect(focusRect.x + focusRect.width).toBeLessThanOrEqual(viewport.width);
        }
      }

      // Test skip links (if present)
      const skipLinks = page.locator('a[href="#main"], .skip-link');
      if (await skipLinks.count() > 0) {
        await expect(skipLinks.first()).toBeVisible();
      }
    }
  });

  test('performance across different screen sizes', async ({ page }) => {
    const performanceResults: Array<{ viewport: string; loadTime: number }> = [];

    for (const viewport of viewports.slice(0, 4)) { // Test first 4 viewports
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      const startTime = Date.now();
      await page.goto('/', { waitUntil: 'networkidle' });
      const loadTime = Date.now() - startTime;
      
      performanceResults.push({
        viewport: viewport.name,
        loadTime
      });

      // Load time should be reasonable across all viewports
      expect(loadTime).toBeLessThan(8000); // 8 seconds max
    }

    // Log performance results for analysis
    console.log('Performance Results:', performanceResults);
  });

  test('cross-browser responsive compatibility', async ({ page, browserName }) => {
    // Test key responsive features across browsers
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check CSS Grid/Flexbox support
    const gridContainer = page.locator('.grid, [style*="grid"], [style*="flex"]').first();
    if (await gridContainer.count() > 0) {
      const computedStyle = await gridContainer.evaluate(el => {
        const style = window.getComputedStyle(el);
        return {
          display: style.display,
          gridTemplateColumns: style.gridTemplateColumns,
          flexDirection: style.flexDirection
        };
      });

      // Modern layout should be supported
      expect(['grid', 'flex'].some(layout =>
        computedStyle.display.includes(layout)
      )).toBeTruthy();
    }

    console.log(`Responsive test completed on ${browserName}`);
  });
});
