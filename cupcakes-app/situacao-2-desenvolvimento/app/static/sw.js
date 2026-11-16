// Service worker mínimo: guarda os arquivos estáticos para abrir mais rápido no celular.
const CACHE = "glace-v1";
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(["/static/style.css", "/static/icone.svg"])));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method === "GET" && new URL(e.request.url).pathname.startsWith("/static/")) {
    e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
  }
});
