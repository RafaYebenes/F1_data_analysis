import redis
import json
from kafka import KafkaProducer
from concurrent.futures import ThreadPoolExecutor
import queue
from f1_reader import F1Reader

##DEPRECATED NOW WE USE JUST F1_READER.PY

# Configuración de servicios
REDIS_HOST = "localhost"
KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "telemetry_enriched"

# Inicializar servicios
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Colas para procesamiento asincrónico
redis_queue = queue.Queue()
kafka_queue = queue.Queue()

# Worker para enviar a Redis
def redis_worker():
    while True:
        packet = redis_queue.get()
        try:
            # Construcción mínima del snapshot solo si hay datos útiles
            telemetry = packet.get("m_carTelemetryData", [{}])[0]
            status = packet.get("m_carStatusData", [{}])[0]
            lap = packet.get("m_lapData", [{}])[0]

            snapshot = {
                "timestamp": packet.get("m_header", {}).get("m_sessionTime"),
                "car_id": packet.get("m_header", {}).get("m_playerCarIndex"),
                "rpm": telemetry.get("m_engineRPM"),
                "gear": telemetry.get("m_gear"),
                "speed_kph": telemetry.get("m_speed"),
                "brake": telemetry.get("m_brake"),
                "throttle": telemetry.get("m_throttle"),
                "fuel": status.get("m_fuelInTank"),
                "lap_time_ms": lap.get("m_currentLapTimeInMS")
            }

            if snapshot["rpm"] is not None:
                redis_client.publish("live_dashboard", json.dumps(snapshot))
        except Exception as e:
            print("[Redis Worker] Error:", e)

# Worker para enviar a Kafka
def kafka_worker():
    while True:
        packet = kafka_queue.get()
        try:
            producer.send(KAFKA_TOPIC, packet)
        except Exception as e:
            print("[Kafka Worker] Error:", e)

# Procesamiento de cada paquete recibido desde f1_reader
def process_packet(packet):
    kafka_queue.put(packet)  # Siempre se envía a Kafka

    # Solo intentamos mandar a Redis si hay algo útil
    if packet.get("packet_id") in [2, 6, 7]:  # LapData, CarTelemetry, CarStatus
        redis_queue.put(packet)

# Lanzador principal
def main():
    reader = F1Reader()

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(redis_worker)
        executor.submit(kafka_worker)
        reader.start(callback=process_packet)

if __name__ == "__main__":
    main()
