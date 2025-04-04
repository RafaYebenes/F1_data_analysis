import psycopg2
from psycopg2 import sql

def connect_postgres():
    try:
        conn = psycopg2.connect(
            dbname='f1_database',
            user='user',
            password='password',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        print("✅ Conexión exitosa a PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        return None

def insert_telemetry_data(conn, speed_kmh, rpm, gear, fuel_consumption, engine_temperature, position):
    try:
        with conn.cursor() as cursor:
            insert_query = sql.SQL('''
                INSERT INTO telemetry_data (speed_kmh, rpm, gear, fuel_consumption, engine_temperature, position_x, position_y, position_z)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''')
            cursor.execute(insert_query, (speed_kmh, rpm, gear, fuel_consumption, engine_temperature, *position))
            print("✅ Datos insertados correctamente en la tabla telemetry_data")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

def main():
    conn = connect_postgres()
    if conn:
        # Datos ficticios para prueba
        insert_telemetry_data(conn, speed_kmh=150.5, rpm=9000, gear=3, 
                              fuel_consumption=0.05, engine_temperature=95.0,
                              position=(100.0, 200.0, 0.0))
        conn.close()

if __name__ == "__main__":
    main()
