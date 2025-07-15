/**
 * Service Worker for Warhammer Fantasy Tavern Simulator
 * Provides offline capabilities and caching strategies
 */

const CACHE_NAME = 'warhammer-tavern-v1.0.0';
const STATIC_CACHE = 'warhammer-static-v1';
const DYNAMIC_CACHE = 'warhammer-dynamic-v1';

// Files to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/styles/main.css',
  '/styles/themes.css',
  '/styles/responsive.css',
  '/js/main.js',
  
  // External CDN resources (fallbacks)
  '/assets/fallbacks/three.min.js',
  '/assets/fallbacks/gsap.min.js',
  '/assets/fallbacks/howler.min.js',
  
  // Essential assets
  '/assets/icons/icon-192x192.png',
  '/assets/icons/icon-512x512.png',
  '/assets/audio/tavern-ambience.ogg',
  '/assets/models/tavern-basic.glb'
];

// CDN resources to cache dynamically
const CDN_RESOURCES = [
  'https://cdnjs.cloudflare.com/ajax/libs/three.js/',
  'https://cdnjs.cloudflare.com/ajax/libs/gsap/',
  'https://cdnjs.cloudflare.com/ajax/libs/howler/',
  'https://fonts.googleapis.com/',
  'https://fonts.gstatic.com/'
];

/**
 * Install Event - Cache static assets
 */
self.addEventListener('install', event => {
  console.log('🔧 Service Worker installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('📦 Caching static assets...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Static assets cached successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('❌ Failed to cache static assets:', error);
      })
  );
});

/**
 * Activate Event - Clean up old caches
 */
self.addEventListener('activate', event => {
  console.log('🚀 Service Worker activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ Service Worker activated');
        return self.clients.claim();
      })
  );
});

/**
 * Fetch Event - Handle network requests with caching strategies
 */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip WebSocket and EventSource requests
  if (request.headers.get('upgrade') === 'websocket' || 
      request.headers.get('accept') === 'text/event-stream') {
    return;
  }
  
  // Handle different types of requests
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
  } else if (isCDNResource(request)) {
    event.respondWith(handleCDNResource(request));
  } else if (isAPIRequest(request)) {
    event.respondWith(handleAPIRequest(request));
  } else {
    event.respondWith(handleDynamicRequest(request));
  }
});

/**
 * Handle static assets (Cache First strategy)
 */
async function handleStaticAsset(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('Failed to fetch static asset:', error);
    
    // Return offline fallback for critical assets
    if (request.url.includes('.html')) {
      return caches.match('/offline.html');
    }
    
    throw error;
  }
}

/**
 * Handle CDN resources (Stale While Revalidate strategy)
 */
async function handleCDNResource(request) {
  try {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then(networkResponse => {
      if (networkResponse.ok) {
        cache.put(request, networkResponse.clone());
      }
      return networkResponse;
    });
    
    return cachedResponse || await fetchPromise;
  } catch (error) {
    console.error('Failed to fetch CDN resource:', error);
    
    // Try to return cached version
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    throw error;
  }
}

/**
 * Handle API requests (Network First strategy)
 */
async function handleAPIRequest(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('API request failed, trying cache:', error);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response for API requests
    return new Response(
      JSON.stringify({
        error: 'Offline',
        message: 'This feature requires an internet connection'
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

/**
 * Handle dynamic requests (Network First with fallback)
 */
async function handleDynamicRequest(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    throw error;
  }
}

/**
 * Utility functions
 */
function isStaticAsset(request) {
  const url = new URL(request.url);
  return STATIC_ASSETS.some(asset => url.pathname === asset) ||
         url.pathname.startsWith('/assets/') ||
         url.pathname.startsWith('/styles/') ||
         url.pathname.startsWith('/js/');
}

function isCDNResource(request) {
  return CDN_RESOURCES.some(cdn => request.url.startsWith(cdn));
}

function isAPIRequest(request) {
  const url = new URL(request.url);
  return url.pathname.startsWith('/api/') || 
         url.pathname.startsWith('/ws/');
}

/**
 * Background Sync for offline actions
 */
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Sync any pending actions when back online
    const pendingActions = await getStoredActions();
    
    for (const action of pendingActions) {
      try {
        await fetch('/api/sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(action)
        });
        
        await removeStoredAction(action.id);
      } catch (error) {
        console.error('Failed to sync action:', error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

/**
 * Push notifications
 */
self.addEventListener('push', event => {
  if (!event.data) return;
  
  try {
    const data = event.data.json();
    
    const options = {
      body: data.body || 'Something happened in your tavern!',
      icon: '/assets/icons/icon-192x192.png',
      badge: '/assets/icons/badge-72x72.png',
      tag: data.tag || 'tavern-notification',
      data: data.data || {},
      actions: [
        {
          action: 'view',
          title: 'View Tavern',
          icon: '/assets/icons/action-view.png'
        },
        {
          action: 'dismiss',
          title: 'Dismiss',
          icon: '/assets/icons/action-dismiss.png'
        }
      ],
      requireInteraction: data.urgent || false,
      silent: false,
      vibrate: [200, 100, 200]
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title || '🏰 Tavern Update', options)
    );
  } catch (error) {
    console.error('Failed to show notification:', error);
  }
});

/**
 * Notification click handling
 */
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'dismiss') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then(clientList => {
        for (const client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});

/**
 * Storage utilities for offline actions
 */
async function getStoredActions() {
  try {
    const cache = await caches.open('offline-actions');
    const request = new Request('/offline-actions');
    const response = await cache.match(request);
    
    if (response) {
      return await response.json();
    }
    
    return [];
  } catch (error) {
    console.error('Failed to get stored actions:', error);
    return [];
  }
}

async function removeStoredAction(actionId) {
  try {
    const actions = await getStoredActions();
    const filteredActions = actions.filter(action => action.id !== actionId);
    
    const cache = await caches.open('offline-actions');
    const request = new Request('/offline-actions');
    const response = new Response(JSON.stringify(filteredActions));
    
    await cache.put(request, response);
  } catch (error) {
    console.error('Failed to remove stored action:', error);
  }
}

/**
 * Message handling from main thread
 */
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

console.log('🏰 Warhammer Tavern Service Worker loaded successfully');