from datetime import datetime
import psycopg2
import redis
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
from sql.queries import (
    query_motion,
    query_session,
    query_lap_data,
    query_event,
    query_car_telemetry
)

# Configuración de Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Configuración de PostgreSQL
conn = psycopg2.connect(
    dbname='f1_database',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)
conn.autocommit = True

cursor = conn.cursor()
# Configuración de Kafka
KAFKA_TOPIC = 'telemetry'
KAFKA_SERVER = 'localhost:9092'


# Consumidor de Kafka
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    group_id='f1_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def save_to_redis(data):
    try:
        for key, value in data.items():
            if isinstance(value, list):
                value = json.dumps(value)  # Convertimos listas a string JSON
            redis_client.set(key, value)
        print("✅ Datos guardados correctamente en Redis")
    except Exception as e:
        print(f"❌ Error al guardar datos en Redis: {e}")


def save_to_postgres(data):
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())
    session_uid = data.get('session_uid')
    car_index = data.get('car_index')
    session_type = data.get('session_type')

    # Filtramos por sesiones Time Trial únicamente
    if session_type != 3:
        return

    if 'motion' in data:
        motion = data['motion']
        cursor.execute(query_motion, (
            timestamp, session_uid, car_index,
            *motion['worldPosition'],
            *motion['velocity'],
            *motion['gForce'],
            *motion['rotation']
        ))

    elif 'session' in data:
        s = data['session']
        cursor.execute(query_session, (
            timestamp, session_uid, car_index,
            s['weather'], s['trackTemperature'], s['airTemperature'], s['totalLaps'], s['trackLength'],
            s['sessionType'], s['trackId'], s['formula'], s['sessionTimeLeft'], s['sessionDuration'],
            s['pitSpeedLimit'], s['gamePaused'], s['isSpectating'], s['spectatorCarIndex'],
            s['sliProNativeSupport'], s['numMarshalZones'], s['safetyCarStatus'], s['networkGame']
        ))

    elif 'lapData' in data:
        l = data['lapData']
        cursor.execute(query_lap_data, (
            timestamp, session_uid, car_index,
            l['lastLapTime'], l['currentLapTime'], l['sector1Time'], l['sector2Time'],
            l['lapDistance'], l['totalDistance'], l['safetyCarDelta'],
            l['carPosition'], l['currentLapNum']
        ))

    elif 'event' in data:
        e = data['event']
        cursor.execute(query_event, (timestamp, session_uid, car_index, e['eventStringCode']))

    elif 'carTelemetry' in data:
        t = data['carTelemetry']
        cursor.execute(query_car_telemetry, (
            timestamp, session_uid, car_index,
            t['speed'], t['throttle'], t['steer'], t['brake'], t['clutch'], t['gear'],
            t['engineRPM'], t['drs'], t['revLightsPercent'],
            t['brakesTemperature'], t['tyresSurfaceTemperature'], t['tyresInnerTemperature'],
            t['engineTemperature'], t['tyresPressure']
        ))
    
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    if 'motion' in data:
        motion = data['motion']
        cursor.execute(query_motion, (
            timestamp,
            *motion['worldPosition'],
            *motion['velocity'],
            *motion['gForce'],
            *motion['rotation']
        ))

    elif 'session' in data:
        s = data['session']
        cursor.execute(query_session, (
            timestamp,
            s['weather'], s['trackTemperature'], s['airTemperature'], s['totalLaps'], s['trackLength'],
            s['sessionType'], s['trackId'], s['formula'], s['sessionTimeLeft'], s['sessionDuration'],
            s['pitSpeedLimit'], s['gamePaused'], s['isSpectating'], s['spectatorCarIndex'],
            s['sliProNativeSupport'], s['numMarshalZones'], s['safetyCarStatus'], s['networkGame']
        ))

    elif 'lapData' in data:
        l = data['lapData']
        cursor.execute(query_lap_data, (
            timestamp,
            l['lastLapTime'], l['currentLapTime'], l['sector1Time'], l['sector2Time'],
            l['lapDistance'], l['totalDistance'], l['safetyCarDelta'],
            l['carPosition'], l['currentLapNum']
        ))

    elif 'event' in data:
        e = data['event']
        cursor.execute(query_event, (timestamp, e['eventStringCode']))

    elif 'carTelemetry' in data:
        t = data['carTelemetry']
        cursor.execute(query_car_telemetry, (
            timestamp,
            t['speed'], t['throttle'], t['steer'], t['brake'], t['clutch'], t['gear'],
            t['engineRPM'], t['drs'], t['revLightsPercent'],
            t['brakesTemperature'], t['tyresSurfaceTemperature'], t['tyresInnerTemperature'],
            t['engineTemperature'], t['tyresPressure']
        ))

    conn.commit()


def main():
    print("📥 Esperando mensajes desde Kafka...")
    for message in consumer:
        try:
            data = message.value  # Los datos que llegan de Kafka

            # Guardar datos en Redis y PostgreSQL
            save_to_redis(data)
            save_to_postgres(data)
        except Exception as e:
            print(f"❌ Error al procesar mensaje de Kafka: {e}")


if __name__ == "__main__":
    main()