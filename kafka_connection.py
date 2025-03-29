from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import time


KAFKA_TOPIC = 'telemetry'
KAFKA_SERVER = 'localhost:9092'


def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset='earliest',
        group_id='f1_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def send_message(producer, message):
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"✅ Mensaje enviado a Kafka: {message}")
    except KafkaError as e:
        print(f"❌ Error al enviar mensaje: {e}")

def consume_messages(consumer):
    print("📥 Esperando mensajes de Kafka...")
    for message in consumer:
        print(f"✅ Mensaje recibido: {message.value}")

def main():
    # Crear productor y consumidor
    producer = create_producer()
    consumer = create_consumer()

    # Enviar un mensaje de prueba
    test_message = {
        'speed_kmh': 150.5,
        'rpm': 9000,
        'gear': 3,
        'fuel_consumption': 0.05,
        'engine_temperature': 95.0,
        'position': [100.0, 200.0, 0.0]
    }
    send_message(producer, test_message)

    # Consumir mensajes
    consume_messages(consumer)


if __name__ == "__main__":
    main()
