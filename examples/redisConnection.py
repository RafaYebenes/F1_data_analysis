import redis


def connect_redis():
    try:
        client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        client.ping()  # Prueba de conexión
        print("✅ Conexión exitosa a Redis")
        return client
    except Exception as e:
        print(f"❌ Error al conectar a Redis: {e}")
        return None

def store_data(client, key, value):
    try:
        client.set(key, value)
        print(f"✅ Datos guardados correctamente en Redis: {key} -> {value}")
    except Exception as e:
        print(f"❌ Error al guardar datos en Redis: {e}")

def retrieve_data(client, key):
    try:
        value = client.get(key)
        print(f"✅ Datos recuperados de Redis: {key} -> {value}")
        return value
    except Exception as e:
        print(f"❌ Error al recuperar datos de Redis: {e}")


def main():
    client = connect_redis()
    if client:
        # Almacenar datos ficticios para prueba
        store_data(client, 'velocidad', '150.5')
        store_data(client, 'rpm', '9000')

        # Recuperar datos
        retrieve_data(client, 'velocidad')
        retrieve_data(client, 'rpm')

if __name__ == "__main__":
    main()
