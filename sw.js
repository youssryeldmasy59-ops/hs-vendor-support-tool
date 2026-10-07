const CACHE_NAME = 'hs-vendor-suite-v35-auto-purge';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          console.log('Purging old service worker cache:', key);
          return caches.delete(key);
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  const isHtml = event.request.mode === 'navigate' || event.request.headers.get('accept')?.includes('text/html');

  if (isHtml) {
    // Always fetch fresh HTML from network directly without cache
    event.respondWith(
      fetch(event.request, { cache: 'no-store' })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Network first for all scripts and styles
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        return networkResponse;
      })
      .catch(() => caches.match(event.request))
  );
});
