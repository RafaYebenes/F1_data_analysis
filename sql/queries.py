query_motion = """
INSERT INTO motion_data (
    timestamp, world_position_x, world_position_y, world_position_z,
    velocity_x, velocity_y, velocity_z,
    g_force_lateral, g_force_longitudinal, g_force_vertical,
    yaw, pitch, roll
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

query_session = """
INSERT INTO session_data (
    timestamp, weather, track_temperature, air_temperature,
    total_laps, track_length, session_type, track_id,
    formula, session_time_left, session_duration, pit_speed_limit,
    game_paused, is_spectating, spectator_car_index,
    sli_pro_native_support, num_marshal_zones,
    safety_car_status, network_game
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

query_lap_data = """
INSERT INTO lap_data (
    timestamp, last_lap_time, current_lap_time, sector1_time, sector2_time,
    lap_distance, total_distance, safety_car_delta,
    car_position, current_lap_num
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

query_event = """
INSERT INTO event_data (
    timestamp, event_string_code
) VALUES (%s, %s)
"""

query_car_telemetry = """
INSERT INTO car_telemetry (
    timestamp, speed, throttle, steer, brake, clutch, gear, engine_rpm,
    drs, rev_lights_percent, brakes_temperature, tyres_surface_temperature,
    tyres_inner_temperature, engine_temperature, tyres_pressure
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
