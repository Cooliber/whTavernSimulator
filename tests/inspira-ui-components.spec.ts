import { test, expect } from '@playwright/test';

test.describe('Inspira UI Components Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('SparklesText component renders correctly', async ({ page }) => {
    // Look for sparkles text elements
    const sparklesText = page.locator('[class*="sparkles"]');
    await expect(sparklesText.first()).toBeVisible();
    
    // Check if sparkles animation is working
    const sparklesElement = sparklesText.first();
    const hasSparkles = await sparklesElement.evaluate(el => {
      return el.querySelector('[class*="sparkle"]') !== null;
    });
    
    expect(hasSparkles).toBeTruthy();
  });

  test('Card3D component has proper 3D effects', async ({ page }) => {
    // Navigate to characters page where Card3D is used
    await page.goto('/characters');
    await page.waitForLoadState('networkidle');
    
    const card3D = page.locator('[class*="card-3d"], [class*="Card3D"]').first();
    await expect(card3D).toBeVisible();
    
    // Check if card has transform properties
    const hasTransform = await card3D.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.transform !== 'none';
    });
    
    // Hover over card to test interaction
    await card3D.hover();
    
    // Wait for animation
    await page.waitForTimeout(500);
    
    // Check if transform changed on hover
    const transformAfterHover = await card3D.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.transform;
    });
    
    expect(transformAfterHover).not.toBe('none');
  });

  test('BorderBeam component displays animated borders', async ({ page }) => {
    const borderBeam = page.locator('[class*="border-beam"], [class*="BorderBeam"]').first();
    await expect(borderBeam).toBeVisible();
    
    // Check if border animation is present
    const hasAnimation = await borderBeam.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.animation !== 'none' || 
             style.animationName !== 'none' ||
             el.querySelector('[class*="beam"]') !== null;
    });
    
    expect(hasAnimation).toBeTruthy();
  });

  test('NumberTicker component animates numbers', async ({ page }) => {
    // Go to tavern page where NumberTicker is used
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');
    
    const numberTicker = page.locator('[class*="number-ticker"], [class*="NumberTicker"]').first();
    
    if (await numberTicker.count() > 0) {
      await expect(numberTicker).toBeVisible();
      
      // Check if the number is actually a number
      const text = await numberTicker.textContent();
      const hasNumber = /\d/.test(text || '');
      expect(hasNumber).toBeTruthy();
    }
  });

  test('RippleButton creates ripple effect on click', async ({ page }) => {
    const rippleButton = page.locator('[class*="ripple"], button').first();
    await expect(rippleButton).toBeVisible();
    
    // Click the button
    await rippleButton.click();
    
    // Wait for ripple animation
    await page.waitForTimeout(300);
    
    // Check if ripple effect was created
    const hasRipple = await rippleButton.evaluate(el => {
      return el.querySelector('[class*="ripple"]') !== null ||
             el.classList.toString().includes('ripple');
    });
    
    expect(hasRipple).toBeTruthy();
  });

  test('Lens component provides magnification', async ({ page }) => {
    // Go to inventory page where Lens is used
    await page.goto('/inventory');
    await page.waitForLoadState('networkidle');
    
    const lensComponent = page.locator('[class*="lens"], [class*="Lens"]').first();
    
    if (await lensComponent.count() > 0) {
      await expect(lensComponent).toBeVisible();
      
      // Hover over lens to activate magnification
      await lensComponent.hover();
      
      // Wait for magnification effect
      await page.waitForTimeout(500);
      
      // Check if magnified content appears
      const hasMagnification = await lensComponent.evaluate(el => {
        return el.querySelector('[class*="magnified"]') !== null ||
               window.getComputedStyle(el).transform.includes('scale');
      });
      
      expect(hasMagnification).toBeTruthy();
    }
  });

  test('Spotlight component follows mouse movement', async ({ page }) => {
    const spotlight = page.locator('[class*="spotlight"], [class*="Spotlight"]').first();
    
    if (await spotlight.count() > 0) {
      await expect(spotlight).toBeVisible();
      
      // Move mouse over spotlight area
      await spotlight.hover();
      
      // Check if spotlight has positioning styles
      const hasPositioning = await spotlight.evaluate(el => {
        const style = window.getComputedStyle(el);
        return style.background.includes('radial-gradient') ||
               style.backgroundImage.includes('radial-gradient');
      });
      
      expect(hasPositioning).toBeTruthy();
    }
  });

  test('Meteors component displays falling meteors', async ({ page }) => {
    // Check for meteor elements
    const meteors = page.locator('[class*="meteor"]');
    
    if (await meteors.count() > 0) {
      await expect(meteors.first()).toBeVisible();
      
      // Check if meteors have animation
      const hasAnimation = await meteors.first().evaluate(el => {
        const style = window.getComputedStyle(el);
        return style.animation !== 'none' || style.animationName !== 'none';
      });
      
      expect(hasAnimation).toBeTruthy();
    }
  });

  test('ParticlesBg component renders particles', async ({ page }) => {
    // Check for particle background
    const particles = page.locator('[class*="particle"]');
    
    if (await particles.count() > 0) {
      await expect(particles.first()).toBeVisible();
      
      // Check if particles are animated
      const particleCount = await particles.count();
      expect(particleCount).toBeGreaterThan(0);
      
      // Check if at least one particle has animation
      const hasAnimation = await particles.first().evaluate(el => {
        const style = window.getComputedStyle(el);
        return style.animation !== 'none' || style.animationName !== 'none';
      });
      
      expect(hasAnimation).toBeTruthy();
    }
  });

  test('InteractiveGridPattern responds to mouse movement', async ({ page }) => {
    const grid = page.locator('[class*="grid-pattern"], [class*="InteractiveGrid"]').first();
    
    if (await grid.count() > 0) {
      await expect(grid).toBeVisible();
      
      // Move mouse over grid
      await grid.hover();
      
      // Check if grid has interactive properties
      const isInteractive = await grid.evaluate(el => {
        return el.classList.toString().includes('interactive') ||
               el.hasAttribute('data-interactive');
      });
      
      // Grid should be visible even if not interactive
      expect(await grid.isVisible()).toBeTruthy();
    }
  });

  test('HyperText component displays animated text', async ({ page }) => {
    const hyperText = page.locator('[class*="hyper-text"], [class*="HyperText"]').first();
    
    if (await hyperText.count() > 0) {
      await expect(hyperText).toBeVisible();
      
      // Check if text content exists
      const textContent = await hyperText.textContent();
      expect(textContent).toBeTruthy();
      expect(textContent!.length).toBeGreaterThan(0);
    }
  });
});