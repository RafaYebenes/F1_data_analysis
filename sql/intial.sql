CREATE TABLE IF NOT EXISTS motion_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    world_position_x REAL,
    world_position_y REAL,
    world_position_z REAL,
    velocity_x REAL,
    velocity_y REAL,
    velocity_z REAL,
    g_force_lateral REAL,
    g_force_longitudinal REAL,
    g_force_vertical REAL,
    yaw REAL,
    pitch REAL,
    roll REAL
);

CREATE TABLE IF NOT EXISTS session_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    weather INT,
    track_temperature INT,
    air_temperature INT,
    total_laps INT,
    track_length INT,
    session_type INT,
    track_id INT,
    formula INT,
    session_time_left INT,
    session_duration INT,
    pit_speed_limit INT,
    game_paused INT,
    is_spectating INT,
    spectator_car_index INT,
    sli_pro_native_support INT,
    num_marshal_zones INT,
    safety_car_status INT,
    network_game INT
);

CREATE TABLE IF NOT EXISTS lap_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    last_lap_time REAL,
    current_lap_time REAL,
    sector1_time INT,
    sector2_time INT,
    lap_distance REAL,
    total_distance REAL,
    safety_car_delta REAL,
    car_position INT,
    current_lap_num INT
);

CREATE TABLE IF NOT EXISTS event_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    event_string_code TEXT
);

CREATE TABLE IF NOT EXISTS car_telemetry (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    speed INT,
    throttle REAL,
    steer REAL,
    brake REAL,
    clutch INT,
    gear INT,
    engine_rpm INT,
    drs INT,
    rev_lights_percent INT,
    brakes_temperature INT[],
    tyres_surface_temperature INT[],
    tyres_inner_temperature INT[],
    engine_temperature INT,
    tyres_pressure REAL[]
);
