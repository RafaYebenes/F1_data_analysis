import json, os

def header_to_dict(header):
    return {
        "packetFormat": header.packetFormat,
        "gameMajorVersion": header.gameMajorVersion,
        "gameMinorVersion": header.gameMinorVersion,
        "packetVersion": header.packetVersion,
        "packetId": header.packetId,
        "sessionUID": header.sessionUID,
        "sessionTime": header.sessionTime,
        "frameIdentifier": header.frameIdentifier,
        "overallFrameIdentifier": header.overallFrameIdentifier,
        "playerCarIndex": header.playerCarIndex,
        "secondaryPlayerCarIndex": header.secondaryPlayerCarIndex,
    }

def createFile(entry, filename):
    path = f"logs/{filename}.json"
    
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Archivo {path} corrupto o mal formado. Se reiniciará.")
            data = []
    else:
        data = []

    data.append(entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def get_packet_handlers(instance):
    return {
        0: instance.parse_motion,
        1: instance.parse_session,
        2: instance.parse_lap_data,
        3: instance.parse_event,
        4: instance.parse_participants,
        5: instance.parse_car_setups,
        6: instance.parse_car_telemetry,
        7: instance.parse_car_status,
        8: instance.parse_final_classification,
        9: instance.parse_lobby_info,
        10: instance.parse_car_damage,
        11: instance.parse_session_history,
        12: instance.parse_tyre_sets,
        14: instance.parse_time_trial
    }

