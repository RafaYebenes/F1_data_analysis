import redis
import json

# Configura tu conexión a Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Diccionario con los datos más recientes
live_data = {
    "username": "Rafa",
    "car_id": None,
    "track_id": None,
    "timestamp": 0.0,
    "rpm": 0,
    "gear": 0,
    "speed_kph": 0.0,
    "brake": 0.0,
    "throttle": 0.0,
    "fuel": 0.0,
    "lap_time_ms": 0
}

# Índice del jugador controlado
player_index = 0  # Puedes actualizarlo dinámicamente si quieres

def update_live_data(packet):
    packet_id = packet.get("packet_id")
    
    if packet_id == 6:  # Car Telemetry
        try:
            car = packet["m_carTelemetryData"][player_index]
            live_data.update({
                "rpm": car["m_engineRPM"],
                "gear": car["m_gear"],
                "speed_kph": car["m_speed"],
                "brake": round(car["m_brake"], 2),
                "throttle": round(car["m_throttle"], 2)
            })
        except Exception as e:
            print("Error en telemetry:", e)

    elif packet_id == 7:  # Car Status
        try:
            car = packet["m_carStatusData"][player_index]
            live_data["fuel"] = round(car["m_fuelInTank"], 2)
        except Exception as e:
            print("Error en fuel:", e)

    elif packet_id == 2:  # Lap Data
        try:
            car = packet["m_lapData"][player_index]
            live_data["lap_time_ms"] = car["m_currentLapTimeInMS"]
        except Exception as e:
            print("Error en lap_time:", e)

    elif packet_id == 1:  # Session
        try:
            live_data["track_id"] = packet["m_trackId"]
            live_data["timestamp"] = packet["m_header"]["m_sessionTime"]
        except Exception as e:
            print("Error en session:", e)

    if live_data["car_id"] is None:
        live_data["car_id"] = player_index

    # Publicar en Redis
    try:
        redis_client.publish("live_dashboard", json.dumps(live_data))
    except Exception as e:
        print("Error publicando en Redis:", e)
