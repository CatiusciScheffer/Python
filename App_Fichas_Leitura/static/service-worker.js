const CACHE_NAME = 'book-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js',
  '/static/images/icon-128x128.png',
  '/static/images/icon-512x512.png',
  '/static/manifest.json'
];

// Instalação do service worker e cache dos arquivos
self.addEventListener('install', event => {
  console.log('Service Worker: Install event in progress.');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching files');
        return cache.addAll(urlsToCache);
      })
  );
});

// Ativação do service worker e limpeza dos caches antigos
self.addEventListener('activate', event => {
  console.log('Service Worker: Activate event in progress.');
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Intercepção das requisições e resposta com cache
self.addEventListener('fetch', event => {
  console.log('Service Worker: Fetch event in progress.');
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          console.log('Service Worker: Found in cache:', event.request.url);
          return response;
        }
        console.log('Service Worker: Network request for:', event.request.url);
        return fetch(event.request);
      })
  );
});
