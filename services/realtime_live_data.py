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
    "invalid_lap": 0,
    "current_lap": 0,
    "sector": 1,
    "sector_1_time": 0.0,
    "sector_2_time": 0.0,
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
            car = packet["carTelemetry"][player_index]

            live_data.update({
                "rpm": car["engineRPM"],
                "gear": car["gear"],
                "speed_kph": car["speed"],
                "brake": round(car["brake"], 2),
                "throttle": round(car["throttle"], 2)
            })
        except Exception as e:
            print("Error en telemetry:", e)

    elif packet_id == 7:  # Car Status
        try:
            car = packet["carStatus"][player_index]  # 👈 corregido
            live_data["fuel"] = round(car["fuelInTank"], 2)
        except Exception as e:
            print("Error en fuel:", e)

    elif packet_id == 2:  # Lap Data
        try:
            car = packet["lapData"][player_index]
            live_data["lap_time_ms"] = car["currentLapTimeInMS"]
            live_data["invalid_lap"] = car["currentLapInvalid"]
            live_data["current_lap"] = car["currentLapNum"]
            live_data["sector"] = car["sector"]
            live_data["sector_1_time"] = car["sector1TimeMSPart"]
            live_data["sector_2_time"] = car["sector2TimeMSPart"]

            live_data["sector"] = car["sector"]
        except Exception as e:
            print("Error en lap_time:", e)

    elif packet_id == 1:  # Session
        try:
            live_data["track_id"] = packet["session"]["trackId"]
            live_data["timestamp"] = packet["header"]["sessionTime"]
        except Exception as e:
            print("Error en session:", e)

    if live_data["car_id"] is None:
        live_data["car_id"] = player_index

    
    try:
        return json.dumps(live_data)
    except Exception as e:
        print("Error publicando en Redis:", e)


def get_damage_info(packet):
    live_data = packet["carDamage"][player_index]
    try:
        return json.dumps(live_data)
    except Exception as e:
        print("Error publicando en Redis:", e)