import psycopg2
import redis
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import socket
import mmap
import struct
from datetime import datetime
from f1_reader import F123FullParser


# Configuración del sistema principal
REDIS_HOST = '192.168.1.181'  # Cambia esto por la IP de tu PC principal
POSTGRES_HOST = '192.168.1.181'
KAFKA_SERVER = '192.168.1.181:9092'

f1_parser = F123FullParser()

# Configuración de Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Configuración de PostgreSQL
postgres_conn = psycopg2.connect(
    dbname='f1_database',
    user='user',
    password='password',
    host=POSTGRES_HOST,
    port='5432'
)
postgres_conn.autocommit = True

# Configuración de Kafka
KAFKA_TOPIC = 'telemetry'
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)




# Assetto Corsa - Estructura de Datos
physics_layout = 'ifffiiffffffff 4f fffffffffffffffffffffffffffffffffffffffffffiifffiffffffffffffiiiiifiifffffffffffffffffiffffffffffffffffffffffffffffffffffffffffiifffffffffffffffffffffiifffffffffffffiiffffffff'
fields = 'packetId throttle brake fuel_consumption gear rpm steerAngle speed position_x position_y position_z accGX accGY accGZ wheelSlipFL wheelSlipFR wheelSlipRL wheelSlipRR'.split(' ')

def read_assetto_corsa_data():
    try:
        # Intentar abrir la memoria compartida
        mmap_file = mmap.mmap(-1, struct.calcsize(physics_layout), "Local\\acpmf_physics", access=mmap.ACCESS_READ)
        mmap_file.seek(0)
        raw_data = mmap_file.read(struct.calcsize(physics_layout))

        if not raw_data:
            print("❌ No se pudo leer ningún dato de la memoria compartida.")
            return None

        data_values = struct.unpack(physics_layout, raw_data)
        data = {fields[i]: data_values[i] for i in range(len(fields))}

        # Añadir la marca de tiempo actual
        data['timestamp'] = datetime.now().isoformat()

        mmap_file.close()
        return data

    except Exception as e:
        print(f"❌ Error al leer datos de Assetto Corsa usando mmap: {e}")
        return None



def send_to_redis(data):
    try:
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            redis_client.set(key, value)
    except Exception as e:
        print(f"❌ Error al enviar datos a Redis: {e}")


def send_to_postgres(data):
    try:
        with postgres_conn.cursor() as cursor:
            # Insertar datos en la tabla existente
            query = '''
                INSERT INTO telemetry_data (timestamp, speed_kmh, rpm, gear, fuel_consumption, engine_temperature, position_x, position_y, position_z)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (
                data.get('timestamp'),
                data.get('speed', 0),
                data.get('rpm', 0),
                data.get('gear', 0),
                data.get('fuel_consumption', 0),
                data.get('engine_temperature', 0),
                data.get('position_x', 0),
                data.get('position_y', 0),
                data.get('position_z', 0)
            ))
    except Exception as e:
        print(f"❌ Error al enviar datos a PostgreSQL: {e}")


def send_to_kafka(data):
    try:
        producer.send(KAFKA_TOPIC, data)
        producer.flush()
    except KafkaError as e:
        print(f"❌ Error al enviar datos a Kafka: {e}")


def main():
    while True:
        

        f1_data = f1_parser.read_packet()
        if f1_data:
            print("data to send")
            print(f1_data)
            send_to_redis(f1_data)
            send_to_kafka(f1_data)


        time.sleep(0.1)


if __name__ == "__main__":
    main()
