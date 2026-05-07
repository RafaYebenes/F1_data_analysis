-- F1 25 schema
-- Run once: psql -h localhost -U user -d f1_database -f sql/intial.sql

CREATE TABLE IF NOT EXISTS motion_data (
    id                      SERIAL PRIMARY KEY,
    timestamp               TIMESTAMPTZ,
    session_uid             TEXT,
    car_index               INT,
    world_position_x        REAL,
    world_position_y        REAL,
    world_position_z        REAL,
    velocity_x              REAL,
    velocity_y              REAL,
    velocity_z              REAL,
    g_force_lateral         REAL,
    g_force_longitudinal    REAL,
    g_force_vertical        REAL,
    yaw                     REAL,
    pitch                   REAL,
    roll                    REAL
);

CREATE TABLE IF NOT EXISTS session_data (
    id                              SERIAL PRIMARY KEY,
    timestamp                       TIMESTAMPTZ,
    session_uid                     TEXT,
    weather                         SMALLINT,
    track_temperature               SMALLINT,
    air_temperature                 SMALLINT,
    total_laps                      SMALLINT,
    track_length                    INT,
    session_type                    SMALLINT,
    track_id                        SMALLINT,
    formula                         SMALLINT,
    session_time_left               INT,
    session_duration                INT,
    pit_speed_limit                 SMALLINT,
    game_paused                     BOOLEAN,
    is_spectating                   BOOLEAN,
    spectator_car_index             SMALLINT,
    safety_car_status               SMALLINT,
    network_game                    BOOLEAN,
    -- F1 24/25 additions
    forecast_accuracy               SMALLINT,
    ai_difficulty                   SMALLINT,
    game_mode                       SMALLINT,
    rule_set                        SMALLINT,
    time_of_day                     INT,
    session_length                  SMALLINT,
    num_safety_car_periods          SMALLINT,
    num_virtual_safety_car_periods  SMALLINT,
    num_red_flag_periods            SMALLINT,
    pit_stop_window_ideal_lap       SMALLINT,
    pit_stop_window_latest_lap      SMALLINT,
    sector2_lap_distance_start      REAL,
    sector3_lap_distance_start      REAL
);

CREATE TABLE IF NOT EXISTS lap_data (
    id                      SERIAL PRIMARY KEY,
    timestamp               TIMESTAMPTZ,
    session_uid             TEXT,
    car_index               INT,
    last_lap_time_ms        INT,
    current_lap_time_ms     INT,
    -- F1 24/25: sector times split into ms + minutes parts
    sector1_time_ms_part    INT,
    sector1_time_min_part   SMALLINT,
    sector2_time_ms_part    INT,
    sector2_time_min_part   SMALLINT,
    lap_distance            REAL,
    total_distance          REAL,
    safety_car_delta        REAL,
    car_position            SMALLINT,
    current_lap_num         SMALLINT,
    pit_status              SMALLINT,
    num_pit_stops           SMALLINT,
    sector                  SMALLINT,
    current_lap_invalid     BOOLEAN,
    penalties               SMALLINT,
    grid_position           SMALLINT,
    driver_status           SMALLINT,
    result_status           SMALLINT,
    speed_trap_fastest_speed REAL,
    speed_trap_fastest_lap  SMALLINT
);

CREATE TABLE IF NOT EXISTS event_data (
    id                      SERIAL PRIMARY KEY,
    timestamp               TIMESTAMPTZ,
    session_uid             TEXT,
    event_string_code       CHAR(4),
    vehicle_idx             SMALLINT,
    other_vehicle_idx       SMALLINT,
    lap_time                REAL,
    speed                   REAL,
    penalty_type            SMALLINT,
    infringement_type       SMALLINT,
    places_gained           SMALLINT,
    lap_num                 SMALLINT,
    reason                  SMALLINT,
    button_status           BIGINT,
    safety_car_type         SMALLINT,
    event_type              SMALLINT
);

CREATE TABLE IF NOT EXISTS car_telemetry (
    id                          SERIAL PRIMARY KEY,
    timestamp                   TIMESTAMPTZ,
    session_uid                 TEXT,
    car_index                   INT,
    speed                       INT,
    throttle                    REAL,
    steer                       REAL,
    brake                       REAL,
    clutch                      SMALLINT,
    gear                        SMALLINT,
    engine_rpm                  INT,
    drs                         BOOLEAN,
    rev_lights_percent          SMALLINT,
    brakes_temperature          INT[],
    tyres_surface_temperature   INT[],
    tyres_inner_temperature     INT[],
    engine_temperature          INT,
    tyres_pressure              REAL[],
    surface_type                SMALLINT[]
);

CREATE TABLE IF NOT EXISTS car_damage (
    id                      SERIAL PRIMARY KEY,
    timestamp               TIMESTAMPTZ,
    session_uid             TEXT,
    car_index               INT,
    -- F1 24/25: tyres_wear is now a float percentage
    tyres_wear              REAL[],
    tyres_damage            SMALLINT[],
    brakes_damage           SMALLINT[],
    tyre_blisters           SMALLINT[],    -- F1 25
    front_left_wing_damage  SMALLINT,
    front_right_wing_damage SMALLINT,
    rear_wing_damage        SMALLINT,
    floor_damage            SMALLINT,
    diffuser_damage         SMALLINT,
    sidepod_damage          SMALLINT,
    drs_fault               BOOLEAN,
    ers_fault               BOOLEAN,       -- F1 24/25
    gear_box_damage         SMALLINT,
    engine_damage           SMALLINT,
    engine_mguh_wear        SMALLINT,
    engine_es_wear          SMALLINT,
    engine_ce_wear          SMALLINT,
    engine_ice_wear         SMALLINT,
    engine_mguk_wear        SMALLINT,
    engine_tc_wear          SMALLINT,
    engine_blown            BOOLEAN,       -- F1 24/25
    engine_seized           BOOLEAN        -- F1 24/25
);

CREATE TABLE IF NOT EXISTS final_classification (
    id                      SERIAL PRIMARY KEY,
    timestamp               TIMESTAMPTZ,
    session_uid             TEXT,
    position                SMALLINT,
    num_laps                SMALLINT,
    grid_position           SMALLINT,
    points                  SMALLINT,
    num_pit_stops           SMALLINT,
    result_status           SMALLINT,
    result_reason           SMALLINT,      -- F1 25
    best_lap_time_ms        INT,
    total_race_time         DOUBLE PRECISION,
    penalties_time          SMALLINT,
    num_penalties           SMALLINT,
    num_tyre_stints         SMALLINT,
    tyre_stints_actual      SMALLINT[],
    tyre_stints_visual      SMALLINT[],
    tyre_stints_end_laps    SMALLINT[]
);

CREATE TABLE IF NOT EXISTS motion_ex (
    id                          SERIAL PRIMARY KEY,
    timestamp                   TIMESTAMPTZ,
    session_uid                 TEXT,
    -- wheel arrays: RL, RR, FL, FR
    suspension_position         REAL[],
    suspension_velocity         REAL[],
    suspension_acceleration     REAL[],
    wheel_speed                 REAL[],
    wheel_slip_ratio            REAL[],
    wheel_slip_angle            REAL[],
    wheel_lat_force             REAL[],
    wheel_long_force            REAL[],
    height_of_cog_above_ground  REAL,
    local_velocity_x            REAL,
    local_velocity_y            REAL,
    local_velocity_z            REAL,
    angular_velocity_x          REAL,
    angular_velocity_y          REAL,
    angular_velocity_z          REAL,
    angular_acceleration_x      REAL,
    angular_acceleration_y      REAL,
    angular_acceleration_z      REAL,
    front_wheels_angle          REAL,
    wheel_vert_force            REAL[],
    front_aero_height           REAL,
    rear_aero_height            REAL,
    front_roll_angle            REAL,
    rear_roll_angle             REAL,
    chassis_yaw                 REAL,
    chassis_pitch               REAL,      -- F1 25
    wheel_camber                REAL[],    -- F1 25
    wheel_camber_gain           REAL[]     -- F1 25
);
