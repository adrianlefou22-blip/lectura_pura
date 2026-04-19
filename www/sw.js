// sw.js — Service Worker de Lectura Pura
// Este archivo es necesario para que Chrome y Brave
// habiliten el botón "Instalar aplicación".

const CACHE = 'lectura-pura-v1';

self.addEventListener('install', function(e) {
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(self.clients.claim());
});

// Estrategia: network first, sin caché forzado
// (el contenido del libro vive en localStorage del navegador)
self.addEventListener('fetch', function(e) {
  e.respondWith(
    fetch(e.request).catch(function() {
      return new Response('Sin conexión', { status: 503 });
    })
  );
});
