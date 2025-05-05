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


function broadcast(type: string, message: string) {
  const payload = JSON.stringify({ type, payload: JSON.parse(message) });
  for (const client of clients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(payload);
    }
  }
}

subscriber.subscribe("car_data", (msg) => broadcast("car_data", msg));
subscriber.subscribe("car_damage", (msg) => broadcast("car_damage", msg));
subscriber.subscribe("trackHeatMap", (msg) => broadcast("trackHeatMap", msg));
