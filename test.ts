import { createClient } from "redis";

const redis = createClient({ url: "redis://localhost:6379" });
await redis.connect();

await redis.publish("car_data", JSON.stringify({ speed: 200, rpm: 14000, gear: 5 }));

console.log("✅ Mensaje enviado a Redis");
await redis.disconnect();
