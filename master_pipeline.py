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
from resources.utils import *

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
           if isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value)  # Transforma dicts o listas en JSON string
                redis.set(key, value)
        print("✅ Datos guardados correctamente en Redis")
    except Exception as e:
        print(f"❌ Error al guardar datos en Redis: {e}")


def save_to_postgres(data):
    print("📥 Entrando en PostgreSQL:", data)
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())
    session_uid = data.get('session_uid')
    car_index = data.get('car_index')

    try:
        if 'motion' in data:
            createFile(data, "motion")
            motion = data['motion']
            cursor.execute(query_motion, (
                timestamp, session_uid, car_index,
                data['motion']['worldPosition'][0],
                data['motion']['worldPosition'][1],
                data['motion']['worldPosition'][2],
                data['motion']['velocity'][0],
                data['motion']['velocity'][1],
                data['motion']['velocity'][2],
                data['motion']['gForce'][0],
                data['motion']['gForce'][1],
                data['motion']['gForce'][2],
                data['motion']['rotation'][0],
                data['motion']['rotation'][1],
                data['motion']['rotation'][2]
            ))


        elif 'session' in data:
            s = data['session']
            createFile(s, "session")
            cursor.execute(query_session, (
                timestamp, session_uid, car_index,
                s['weather'], s['trackTemperature'], s['airTemperature'], s['totalLaps'], s['trackLength'],
                s['sessionType'], s['trackId'], s['formula'], s['sessionTimeLeft'], s['sessionDuration'],
                s['pitSpeedLimit'], s['gamePaused'], s['isSpectating'], s['spectatorCarIndex'],
                s['sliProNativeSupport'], s['numMarshalZones'], s['safetyCarStatus'], s['networkGame']
            ))

        elif 'lapData' in data:
            l = data['lapData']
            createFile(l, "lapData")
            cursor.execute(query_lap_data, (
                timestamp, session_uid, car_index,
                l['lastLapTime'], l['currentLapTime'], l['sector1Time'], l['sector2Time'],
                l['lapDistance'], l['totalDistance'], l['safetyCarDelta'],
                l['carPosition'], l['currentLapNum']
            ))

        elif 'event' in data:
            e = data['event']
            createFile(e, "events")
            cursor.execute(query_event, (timestamp, session_uid, car_index, e['eventStringCode']))

        elif 'carTelemetry' in data:
            t = data['carTelemetry']
            createFile(t, "telemetry")
            cursor.execute(query_car_telemetry, (
                timestamp, session_uid, car_index,
                t['speed'], t['throttle'], t['steer'], t['brake'], t['clutch'], t['gear'],
                t['engineRPM'], t['drs'], t['revLightsPercent'],
                json.dumps(t['brakesTemperature']),
                json.dumps(t['tyresSurfaceTemperature']),
                json.dumps(t['tyresInnerTemperature']),
                t['engineTemperature'],
                json.dumps(t['tyresPressure'])
            ))

        conn.commit()
        print("✅ Datos guardados correctamente en PostgreSQL")

    except Exception as e:
        print(f"❌ Error al guardar datos en PostgreSQL: {e}")


def main():
    print("📥 Esperando mensajes desde Kafka...")
    for message in consumer:
        try:
            data = message.value  # Los datos que llegan de Kafka
            # Guardar datos en Redis y PostgreSQL
            save_to_postgres(data)
            save_to_redis(data)
        except Exception as e:
            print(f"❌ Error al procesar mensaje de Kafka: {e}")


if __name__ == "__main__":
    main()