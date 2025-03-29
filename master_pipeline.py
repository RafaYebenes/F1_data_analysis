import psycopg2
import redis
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


# Configuración de Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Configuración de PostgreSQL
postgres_conn = psycopg2.connect(
    dbname='f1_database',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)
postgres_conn.autocommit = True

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
    try:
        with postgres_conn.cursor() as cursor:
            query = '''
                INSERT INTO telemetry_data (speed_kmh, rpm, gear, fuel_consumption, engine_temperature, position_x, position_y, position_z)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (
                data['speed_kmh'], data['rpm'], data['gear'],
                data['fuel_consumption'], data['engine_temperature'],
                data['position'][0], data['position'][1], data['position'][2]
            ))
        print("✅ Datos guardados correctamente en PostgreSQL")
    except Exception as e:
        print(f"❌ Error al guardar datos en PostgreSQL: {e}")


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