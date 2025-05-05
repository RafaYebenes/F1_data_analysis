# --- SQL Creation Script (PostgreSQL) ---

import psycopg2

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS lap_data (
    id SERIAL PRIMARY KEY,
    session_uid BIGINT,
    driver_name TEXT,
    lap_number INT,
    sector1_time_ms INT,
    sector2_time_ms INT,
    sector3_time_ms INT,
    total_lap_time_ms INT,
    is_valid_lap BOOLEAN,
    speed_at_sector1 FLOAT,
    speed_at_sector2 FLOAT,
    speed_at_finish_line FLOAT,
    track_id INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

def init_postgres_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_QUERY)
    conn.commit()


def insert_lap_data(conn, lap_data):
    print("entramos en insert_lap_data")

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO lap_data (
                session_uid, driver_name, lap_number,
                sector1_time_ms, sector2_time_ms, sector3_time_ms,
                total_lap_time_ms, is_valid_lap,
                speed_at_sector1, speed_at_sector2, speed_at_finish_line,
                track_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lap_data['session_uid'],
            lap_data['driver_name'],
            lap_data['lap_number'],
            lap_data['sector1_time_ms'],
            lap_data['sector2_time_ms'],
            lap_data['sector3_time_ms'],
            lap_data['total_lap_time_ms'],
            lap_data['is_valid_lap'],
            lap_data['speed_at_sector1'],
            lap_data['speed_at_sector2'],
            lap_data['speed_at_finish_line'],
            lap_data['track_id']
        ))

    print("insert_lap_data terminado")

    conn.commit()
