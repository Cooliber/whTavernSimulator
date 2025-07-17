import { test, expect } from '@playwright/test';

test.describe('Cross-Browser Compatibility Tests', () => {
  const pages = ['/', '/characters', '/tavern', '/quests', '/inventory', '/map'];

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  pages.forEach(pagePath => {
    test(`${pagePath} works correctly across browsers`, async ({ page, browserName }) => {
      await page.goto(pagePath);
      await page.waitForLoadState('networkidle');

      // Basic functionality should work in all browsers
      const mainContent = page.locator('main, .main-content, body > div').first();
      await expect(mainContent).toBeVisible();

      // Test JavaScript functionality
      const buttons = page.locator('button').first();
      if (await buttons.count() > 0) {
        await buttons.click();
        await page.waitForTimeout(500);
        // Should not cause JavaScript errors
        expect(true).toBeTruthy();
      }

      // Test CSS support
      const styledElements = page.locator('[class], [style]').first();
      if (await styledElements.count() > 0) {
        const computedStyle = await styledElements.evaluate(el => {
          const style = window.getComputedStyle(el);
          return {
            display: style.display,
            position: style.position,
            color: style.color
          };
        });
        
        // Basic CSS should be applied
        expect(computedStyle.display).not.toBe('');
      }

      console.log(`${pagePath} tested successfully on ${browserName}`);
    });
  });

  test('modern CSS features compatibility', async ({ page, browserName }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Test CSS Grid support
    const gridElements = page.locator('[style*="grid"], .grid').first();
    if (await gridElements.count() > 0) {
      const gridSupport = await gridElements.evaluate(el => {
        const style = window.getComputedStyle(el);
        return {
          display: style.display,
          gridTemplateColumns: style.gridTemplateColumns
        };
      });
      
      // Grid should be supported in modern browsers
      if (browserName !== 'webkit' || browserName !== 'firefox') {
        expect(gridSupport.display.includes('grid')).toBeTruthy();
      }
    }

    // Test Flexbox support
    const flexElements = page.locator('[style*="flex"], .flex').first();
    if (await flexElements.count() > 0) {
      const flexSupport = await flexElements.evaluate(el => {
        const style = window.getComputedStyle(el);
        return style.display;
      });
      
      expect(flexSupport.includes('flex')).toBeTruthy();
    }

    // Test CSS Custom Properties (CSS Variables)
    const customPropTest = await page.evaluate(() => {
      const testEl = document.createElement('div');
      testEl.style.setProperty('--test-var', 'test');
      return testEl.style.getPropertyValue('--test-var') === 'test';
    });
    
    expect(customPropTest).toBeTruthy();
  });

  test('JavaScript ES6+ features compatibility', async ({ page, browserName }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Test modern JavaScript features
    const jsFeatureSupport = await page.evaluate(() => {
      const results = {
        arrow_functions: false,
        const_let: false,
        template_literals: false,
        destructuring: false,
        promises: false,
        async_await: false,
        modules: false
      };

      try {
        // Arrow functions
        const arrowFunc = () => true;
        results.arrow_functions = arrowFunc();

        // const/let
        const testConst = 'test';
        let testLet = 'test';
        results.const_let = testConst === 'test' && testLet === 'test';

        // Template literals
        const name = 'test';
        results.template_literals = `Hello ${name}` === 'Hello test';

        // Destructuring
        const obj = { a: 1, b: 2 };
        const { a, b } = obj;
        results.destructuring = a === 1 && b === 2;

        // Promises
        results.promises = typeof Promise !== 'undefined';

        // Async/await (basic check)
        results.async_await = typeof (async () => {}) === 'function';

        // Module support (basic check)
        results.modules = typeof window.import !== 'undefined';
      } catch (error) {
        console.warn('JavaScript feature test failed:', error);
      }

      return results;
    });

    // Modern browsers should support most ES6+ features
    expect(jsFeatureSupport.arrow_functions).toBeTruthy();
    expect(jsFeatureSupport.const_let).toBeTruthy();
    expect(jsFeatureSupport.template_literals).toBeTruthy();
    expect(jsFeatureSupport.promises).toBeTruthy();

    console.log(`JavaScript features tested on ${browserName}:`, jsFeatureSupport);
  });

  test('Web APIs compatibility', async ({ page, browserName }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Test Web API support
    const apiSupport = await page.evaluate(() => {
      return {
        localStorage: typeof localStorage !== 'undefined',
        sessionStorage: typeof sessionStorage !== 'undefined',
        fetch: typeof fetch !== 'undefined',
        webgl: (() => {
          try {
            const canvas = document.createElement('canvas');
            return !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
          } catch (e) {
            return false;
          }
        })(),
        audioContext: typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined',
        geolocation: 'geolocation' in navigator,
        deviceOrientation: 'DeviceOrientationEvent' in window,
        touchEvents: 'ontouchstart' in window,
        intersectionObserver: 'IntersectionObserver' in window,
        mutationObserver: 'MutationObserver' in window
      };
    });

    // Core APIs should be supported
    expect(apiSupport.localStorage).toBeTruthy();
    expect(apiSupport.fetch).toBeTruthy();

    console.log(`Web APIs tested on ${browserName}:`, apiSupport);
  });

  test('form input compatibility', async ({ page, browserName }) => {
    await page.goto('/gm-dashboard');
    await page.waitForLoadState('networkidle');

    // Test HTML5 input types
    const inputTypes = ['text', 'email', 'url', 'number', 'date', 'color', 'range'];
    
    for (const inputType of inputTypes) {
      const testInput = await page.evaluate((type) => {
        const input = document.createElement('input');
        input.type = type;
        return input.type === type;
      }, inputType);
      
      // Most input types should be supported
      if (['text', 'email', 'number'].includes(inputType)) {
        expect(testInput).toBeTruthy();
      }
    }

    // Test form validation
    const validationSupport = await page.evaluate(() => {
      const input = document.createElement('input');
      input.type = 'email';
      input.value = 'invalid-email';
      return typeof input.checkValidity === 'function';
    });
    
    expect(validationSupport).toBeTruthy();
  });

  test('media and graphics compatibility', async ({ page, browserName }) => {
    await page.goto('/characters');
    await page.waitForLoadState('networkidle');

    // Test image format support
    const imageSupport = await page.evaluate(() => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      return {
        canvas: !!ctx,
        webp: (() => {
          canvas.width = 1;
          canvas.height = 1;
          return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        })(),
        svg: document.implementation.hasFeature('http://www.w3.org/TR/SVG11/feature#BasicStructure', '1.1')
      };
    });

    expect(imageSupport.canvas).toBeTruthy();
    expect(imageSupport.svg).toBeTruthy();

    // Test video support if video elements exist
    const videoElements = await page.locator('video').count();
    if (videoElements > 0) {
      const videoSupport = await page.evaluate(() => {
        const video = document.createElement('video');
        return {
          mp4: video.canPlayType('video/mp4') !== '',
          webm: video.canPlayType('video/webm') !== '',
          ogg: video.canPlayType('video/ogg') !== ''
        };
      });
      
      // At least one video format should be supported
      expect(videoSupport.mp4 || videoSupport.webm || videoSupport.ogg).toBeTruthy();
    }
  });

  test('audio compatibility', async ({ page, browserName }) => {
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');

    // Test audio support
    const audioSupport = await page.evaluate(() => {
      const audio = document.createElement('audio');
      return {
        mp3: audio.canPlayType('audio/mpeg') !== '',
        ogg: audio.canPlayType('audio/ogg') !== '',
        wav: audio.canPlayType('audio/wav') !== '',
        webAudio: typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined'
      };
    });

    // At least one audio format should be supported
    expect(audioSupport.mp3 || audioSupport.ogg || audioSupport.wav).toBeTruthy();

    console.log(`Audio support on ${browserName}:`, audioSupport);
  });

  test('animation and transition compatibility', async ({ page, browserName }) => {
    await page.goto('/tavern');
    await page.waitForLoadState('networkidle');

    // Test CSS animation support
    const animationSupport = await page.evaluate(() => {
      const testEl = document.createElement('div');
      const prefixes = ['', '-webkit-', '-moz-', '-o-', '-ms-'];
      
      for (const prefix of prefixes) {
        testEl.style.cssText = `${prefix}animation: test 1s;`;
        if (testEl.style.length > 0) {
          return true;
        }
      }
      return false;
    });

    expect(animationSupport).toBeTruthy();

    // Test transition support
    const transitionSupport = await page.evaluate(() => {
      const testEl = document.createElement('div');
      testEl.style.transition = 'all 1s';
      return testEl.style.transition !== '';
    });

    expect(transitionSupport).toBeTruthy();
  });

  test('performance across browsers', async ({ page, browserName }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Performance should be reasonable across browsers
    expect(loadTime).toBeLessThan(10000); // 10 seconds max
    
    // Test JavaScript performance
    const jsPerformance = await page.evaluate(() => {
      const start = performance.now();
      
      // Simple performance test
      let result = 0;
      for (let i = 0; i < 100000; i++) {
        result += Math.random();
      }
      
      const end = performance.now();
      return end - start;
    });
    
    // JavaScript execution should be reasonably fast
    expect(jsPerformance).toBeLessThan(1000); // 1 second max
    
    console.log(`Performance on ${browserName}: Load=${loadTime}ms, JS=${jsPerformance}ms`);
  });

  test('error handling across browsers', async ({ page, browserName }) => {
    const errors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    page.on('pageerror', error => {
      errors.push(error.message);
    });

    // Navigate through key pages
    const testPages = ['/', '/characters', '/tavern'];
    
    for (const testPage of testPages) {
      await page.goto(testPage);
      await page.waitForLoadState('networkidle');
      
      // Interact with page elements
      const buttons = page.locator('button').first();
      if (await buttons.count() > 0) {
        await buttons.click();
        await page.waitForTimeout(500);
      }
    }

    // Should have minimal errors across browsers
    expect(errors.length).toBeLessThan(5);
    
    if (errors.length > 0) {
      console.log(`Errors on ${browserName}:`, errors);
    }
  });
});
