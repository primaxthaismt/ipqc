const CACHE_NAME = 'ipqc-v2-dev-v5';
const STATIC_ASSETS = ['/', '/css/styles.css', '/js/app.js', '/js/checklist_data.js', '/js/translations.js'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(STATIC_ASSETS)).catch(()=>{})); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))); });
self.addEventListener('fetch', e => { if (e.request.url.includes('/api/')) return; e.respondWith(fetch(e.request).catch(() => caches.match(e.request))); });
