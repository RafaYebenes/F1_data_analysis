// live_dashboard_server.ts
import { createClient } from "redis";

// Cliente Redis principal
const redis = createClient({ url: "redis://localhost:6379" });
await redis.connect();

// Cliente dedicado a suscripciones
const subscriber = redis.duplicate();
await subscriber.connect();

// Set de clientes WebSocket conectados
const clients = new Set<WebSocket>();

const HEARTBEAT_INTERVAL = 30000; // 30 segundos

Bun.serve({
  port: 3000,
  hostname: "0.0.0.0",

  fetch(req, server) {
    if (server.upgrade(req)) {
      return;
    }
    return new Response("Upgrade failed", { status: 500 });
  },

  websocket: {
    open(ws) {
      clients.add(ws);
      console.log("👤 Cliente conectado. Total:", clients.size);

      const interval = setInterval(() => {
        if (ws.readyState === ws.OPEN) {
          ws.ping();
        } else {
          clearInterval(interval);
        }
      }, HEARTBEAT_INTERVAL);

      (ws as any).pingInterval = interval;
    },

    close(ws) {
      clients.delete(ws);
      clearInterval((ws as any).pingInterval);
      console.log("❌ Cliente desconectado. Total:", clients.size);
    },

    message(ws, message) {
      console.log("💬 Mensaje recibido del cliente:", message);
      // Aquí podrías gestionar comandos en el futuro
    },

    drain(ws) {
      console.log("🧹 Socket listo para recibir más datos");
    }
  }
});

// Suscribirse correctamente a Redis (sin bloquear)
subscriber.subscribe("car_data", (message) => {
  if (!message) return;

  console.log("📩 Nuevo mensaje desde Redis:", message);

  console.log("👥 Número de clientes activos:", clients.size);

  for (const client of clients) {
    console.log("🔎 Estado del cliente:", client.readyState);
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
      console.log("➡️ Enviado a cliente");
    } else {
      console.warn("⚠️ Cliente no está OPEN, no se envía");
    }
  }
});

console.log("🚀 WebSocket server listening on ws://localhost:3000");
