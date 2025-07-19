/**
 * Enochian Cyphers - Service Worker
 * PWA offline functionality with sacred caching strategies
 * Zero external dependencies - Pure JavaScript implementation
 */

const CACHE_NAME = 'enochian-cyphers-v4.0.0';
const SACRED_CACHE_NAME = 'enochian-sacred-data-v1';

// Core files that must be cached for offline functionality
const CORE_FILES = [
    '/',
    '/index.html',
    '/manifest.json',
    '/styles/main.css',
    '/styles/sacred-ui.css',
    '/js/wasm-loader.js',
    '/js/sacred-core.js',
    '/js/lighthouse-ui.js',
    '/js/governors-ui.js',
    '/js/quests-ui.js',
    '/js/divination-ui.js',
    '/js/bitcoin-ui.js',
    '/js/app.js'
];

// Sacred data files for offline access
const SACRED_DATA_FILES = [
    '/lighthouse/traditions/enochian_magic.json',
    '/lighthouse/traditions/hermetic_qabalah.json',
    '/lighthouse/traditions/thelema.json',
    '/lighthouse/traditions/golden_dawn.json',
    '/lighthouse/traditions/chaos_magic.json',
    '/lighthouse/traditions/alchemy.json',
    '/lighthouse/traditions/celtic_druidic.json',
    '/lighthouse/traditions/taoism.json',
    '/lighthouse/traditions/sufism.json',
    '/lighthouse/traditions/gnosticism.json',
    '/lighthouse/traditions/traditional_kabbalah.json',
    '/lighthouse/traditions/tarot.json',
    '/lighthouse/traditions/i_ching.json',
    '/lighthouse/traditions/astrology.json',
    '/lighthouse/traditions/numerology.json',
    '/lighthouse/traditions/norse_traditions.json',
    '/lighthouse/traditions/shamanism.json',
    '/lighthouse/traditions/quantum_physics.json',
    '/lighthouse/traditions/sacred_geometry.json',
    '/lighthouse/traditions/digital_physics.json',
    '/lighthouse/traditions/m_theory.json',
    '/lighthouse/traditions/egyptian_magic.json',
    '/lighthouse/traditions/greek_mythology.json',
    '/lighthouse/traditions/kuji_kiri.json',
    '/lighthouse/traditions/greek_philosophy.json',
    '/lighthouse/traditions/natal_astrology.json',
    '/lighthouse/traditions/lighthouse_master_index.json'
];

// Assets that can be cached opportunistically
const ASSET_PATTERNS = [
    /\/assets\/.+\.(png|jpg|jpeg|gif|svg|ico)$/,
    /\/wasm\/.+\.wasm$/,
    /\/fonts\/.+\.(woff|woff2|ttf|eot)$/
];

console.log('🔮 Enochian Cyphers Service Worker initializing...');

/**
 * Service Worker Installation
 * Cache core files for offline functionality
 */
self.addEventListener('install', event => {
    console.log('🔮 Service Worker installing...');
    
    event.waitUntil(
        Promise.all([
            // Cache core application files
            caches.open(CACHE_NAME).then(cache => {
                console.log('📦 Caching core files...');
                return cache.addAll(CORE_FILES.map(url => new Request(url, { cache: 'reload' })));
            }),
            
            // Cache sacred data files
            caches.open(SACRED_CACHE_NAME).then(cache => {
                console.log('📦 Caching sacred data...');
                return cache.addAll(SACRED_DATA_FILES.map(url => new Request(url, { cache: 'reload' })));
            })
        ]).then(() => {
            console.log('✅ Service Worker installation complete');
            // Force activation of new service worker
            return self.skipWaiting();
        }).catch(error => {
            console.error('❌ Service Worker installation failed:', error);
        })
    );
});

/**
 * Service Worker Activation
 * Clean up old caches
 */
self.addEventListener('activate', event => {
    console.log('🔮 Service Worker activating...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    // Delete old caches
                    if (cacheName !== CACHE_NAME && cacheName !== SACRED_CACHE_NAME) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('✅ Service Worker activation complete');
            // Take control of all clients immediately
            return self.clients.claim();
        })
    );
});

/**
 * Fetch Event Handler
 * Implement sacred caching strategies
 */
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Only handle GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip non-HTTP requests
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    event.respondWith(handleFetch(request));
});

/**
 * Handle fetch requests with sacred caching strategies
 */
async function handleFetch(request) {
    const url = new URL(request.url);
    const pathname = url.pathname;
    
    try {
        // Strategy 1: Core files - Cache First (for app shell)
        if (CORE_FILES.includes(pathname) || pathname === '/') {
            return await cacheFirst(request, CACHE_NAME);
        }
        
        // Strategy 2: Sacred data - Stale While Revalidate
        if (SACRED_DATA_FILES.some(file => pathname.includes(file.replace('/', '')))) {
            return await staleWhileRevalidate(request, SACRED_CACHE_NAME);
        }
        
        // Strategy 3: Assets - Cache First with fallback
        if (ASSET_PATTERNS.some(pattern => pattern.test(pathname))) {
            return await cacheFirstWithFallback(request, CACHE_NAME);
        }
        
        // Strategy 4: API calls - Network First
        if (pathname.includes('/api/') || pathname.includes('/rpc/')) {
            return await networkFirst(request, CACHE_NAME);
        }
        
        // Strategy 5: Everything else - Network with cache fallback
        return await networkWithCacheFallback(request, CACHE_NAME);
        
    } catch (error) {
        console.error('🔮 Fetch error:', error);
        return await getOfflineFallback(request);
    }
}

/**
 * Cache First Strategy
 * Check cache first, fallback to network
 */
async function cacheFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
        console.log('📦 Cache hit:', request.url);
        return cachedResponse;
    }
    
    console.log('🌐 Cache miss, fetching:', request.url);
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
        cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
}

/**
 * Stale While Revalidate Strategy
 * Return cached version immediately, update cache in background
 */
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    // Fetch fresh version in background
    const fetchPromise = fetch(request).then(networkResponse => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(error => {
        console.warn('🔮 Background fetch failed:', error);
    });
    
    // Return cached version immediately if available
    if (cachedResponse) {
        console.log('📦 Stale cache hit:', request.url);
        fetchPromise; // Don't await, let it run in background
        return cachedResponse;
    }
    
    // If no cache, wait for network
    console.log('🌐 No cache, waiting for network:', request.url);
    return await fetchPromise;
}

/**
 * Cache First with Fallback
 * For assets that might not be critical
 */
async function cacheFirstWithFallback(request, cacheName) {
    try {
        return await cacheFirst(request, cacheName);
    } catch (error) {
        console.warn('🔮 Asset fetch failed:', request.url);
        // Return a placeholder or skip
        return new Response('', { status: 404 });
    }
}

/**
 * Network First Strategy
 * Try network first, fallback to cache
 */
async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.warn('🔮 Network failed, trying cache:', request.url);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        throw error;
    }
}

/**
 * Network with Cache Fallback
 * Default strategy for unknown requests
 */
async function networkWithCacheFallback(request, cacheName) {
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.warn('🔮 Network failed, trying cache fallback:', request.url);
        const cache = await caches.open(cacheName);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        return await getOfflineFallback(request);
    }
}

/**
 * Get offline fallback response
 */
async function getOfflineFallback(request) {
    const url = new URL(request.url);
    
    // For HTML requests, return the main app
    if (request.headers.get('accept')?.includes('text/html')) {
        const cache = await caches.open(CACHE_NAME);
        const fallback = await cache.match('/index.html');
        if (fallback) {
            return fallback;
        }
    }
    
    // For API requests, return offline message
    if (url.pathname.includes('/api/')) {
        return new Response(
            JSON.stringify({
                error: 'Offline',
                message: 'Sacred connection temporarily unavailable',
                offline: true
            }),
            {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
    
    // Default offline response
    return new Response('Sacred content temporarily unavailable', {
        status: 503,
        headers: { 'Content-Type': 'text/plain' }
    });
}

/**
 * Handle background sync for quest generation
 */
self.addEventListener('sync', event => {
    console.log('🔮 Background sync:', event.tag);
    
    if (event.tag === 'sacred-quest-sync') {
        event.waitUntil(syncSacredQuests());
    }
    
    if (event.tag === 'bitcoin-inscription-sync') {
        event.waitUntil(syncBitcoinInscriptions());
    }
});

/**
 * Sync sacred quests in background
 */
async function syncSacredQuests() {
    try {
        console.log('🔮 Syncing sacred quests...');
        
        // Get pending quests from IndexedDB
        const pendingQuests = await getPendingQuests();
        
        for (const quest of pendingQuests) {
            try {
                // Attempt to sync quest
                await syncQuest(quest);
                await markQuestSynced(quest.id);
            } catch (error) {
                console.warn('🔮 Quest sync failed:', quest.id, error);
            }
        }
        
        console.log('✅ Sacred quest sync complete');
    } catch (error) {
        console.error('❌ Sacred quest sync failed:', error);
    }
}

/**
 * Sync Bitcoin inscriptions in background
 */
async function syncBitcoinInscriptions() {
    try {
        console.log('🔮 Syncing Bitcoin inscriptions...');
        
        // Get pending inscriptions from IndexedDB
        const pendingInscriptions = await getPendingInscriptions();
        
        for (const inscription of pendingInscriptions) {
            try {
                // Attempt to sync inscription
                await syncInscription(inscription);
                await markInscriptionSynced(inscription.id);
            } catch (error) {
                console.warn('🔮 Inscription sync failed:', inscription.id, error);
            }
        }
        
        console.log('✅ Bitcoin inscription sync complete');
    } catch (error) {
        console.error('❌ Bitcoin inscription sync failed:', error);
    }
}

/**
 * Handle push notifications for sacred events
 */
self.addEventListener('push', event => {
    console.log('🔮 Push notification received');
    
    const options = {
        body: 'A sacred event awaits your attention',
        icon: '/assets/icon-192x192.png',
        badge: '/assets/badge-72x72.png',
        tag: 'sacred-notification',
        requireInteraction: true,
        actions: [
            {
                action: 'view',
                title: 'View Sacred Event',
                icon: '/assets/view-icon.png'
            },
            {
                action: 'dismiss',
                title: 'Dismiss',
                icon: '/assets/dismiss-icon.png'
            }
        ]
    };
    
    if (event.data) {
        try {
            const data = event.data.json();
            options.body = data.message || options.body;
            options.tag = data.tag || options.tag;
        } catch (error) {
            console.warn('🔮 Invalid push data:', error);
        }
    }
    
    event.waitUntil(
        self.registration.showNotification('Enochian Cyphers', options)
    );
});

/**
 * Handle notification clicks
 */
self.addEventListener('notificationclick', event => {
    console.log('🔮 Notification clicked:', event.action);
    
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow('/?notification=true')
        );
    }
});

// Placeholder functions for IndexedDB operations
// These would be implemented with actual IndexedDB in production
async function getPendingQuests() { return []; }
async function syncQuest(quest) { return true; }
async function markQuestSynced(id) { return true; }
async function getPendingInscriptions() { return []; }
async function syncInscription(inscription) { return true; }
async function markInscriptionSynced(id) { return true; }

console.log('✅ Enochian Cyphers Service Worker loaded');
