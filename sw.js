const CACHE_NAME = 'genealogia-biblica-v3';
const ASSETS = [
    './',
    './index.html',
    './visor_genealogia.html',
    './arbol_genealogico.html',
    './grafo_relaciones.html',
    './mapa_geografico.html',
    './linea_temporal.html',
    './estadisticas.html',
    './genealogia_data.js',
    './manifest.json',
    './adam_portrait.png'
];

// Install Event
self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('SW: Cacheando recursos locales...');
            return cache.addAll(ASSETS);
        }).then(() => self.skipWaiting())
    );
});

// Activate Event
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        console.log('SW: Borrando caché antigua:', key);
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event (Cache-first with Network Fallback)
self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(cachedResponse => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(e.request).then(networkResponse => {
                // Dynamically cache external fonts/scripts if fetched
                if (e.request.url.includes('fonts.googleapis.com') || e.request.url.includes('fonts.gstatic.com') || e.request.url.includes('cdnjs.cloudflare.com') || e.request.url.includes('unpkg.com') || e.request.url.includes('cdn.jsdelivr.net')) {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(e.request, networkResponse.clone());
                        return networkResponse;
                    });
                }
                return networkResponse;
            }).catch(() => {
                // Fallback offline behaviors if needed
            });
        })
    );
});
