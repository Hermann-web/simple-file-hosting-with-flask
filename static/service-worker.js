importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

workbox.routing.registerRoute(
  '/',
  new workbox.strategies.NetworkFirst()
);

workbox.routing.registerRoute(
  '/login',
  new workbox.strategies.NetworkFirst()
);