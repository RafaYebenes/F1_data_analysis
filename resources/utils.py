import json, os
import ctypes

class PacketHeader(ctypes.LittleEndianStructure):
    _fields_ = [
        ("packetFormat", ctypes.c_uint16),            # uint16
        ("gameYear", ctypes.c_uint8),                 # uint8 (añadido)
        ("gameMajorVersion", ctypes.c_uint8),         # uint8
        ("gameMinorVersion", ctypes.c_uint8),         # uint8
        ("packetVersion", ctypes.c_uint8),            # uint8
        ("packetId", ctypes.c_uint8),                 # uint8
        ("sessionUID", ctypes.c_uint64),              # uint64
        ("sessionTime", ctypes.c_float),              # float
        ("frameIdentifier", ctypes.c_uint32),         # uint32
        ("overallFrameIdentifier", ctypes.c_uint32),  # uint32
        ("playerCarIndex", ctypes.c_uint8),           # uint8
        ("secondaryPlayerCarIndex", ctypes.c_uint8)   # uint8
    ]


class MotionData(ctypes.LittleEndianStructure):
            _pack_ = 1
            _fields_ = [
                ("worldPositionX", ctypes.c_float),
                ("worldPositionY", ctypes.c_float),
                ("worldPositionZ", ctypes.c_float),
                ("worldVelocityX", ctypes.c_float),
                ("worldVelocityY", ctypes.c_float),
                ("worldVelocityZ", ctypes.c_float),
                ("worldForwardDirX", ctypes.c_int16),
                ("worldForwardDirY", ctypes.c_int16),
                ("worldForwardDirZ", ctypes.c_int16),
                ("worldRightDirX", ctypes.c_int16),
                ("worldRightDirY", ctypes.c_int16),
                ("worldRightDirZ", ctypes.c_int16),
                ("gForceLateral", ctypes.c_float),
                ("gForceLongitudinal", ctypes.c_float),
                ("gForceVertical", ctypes.c_float),
                ("yaw", ctypes.c_float),
                ("pitch", ctypes.c_float),
                ("roll", ctypes.c_float)
            ]

class SessionData(ctypes.LittleEndianStructure):
            _pack_ = 1
            _fields_ = [
                ("weather", ctypes.c_uint8),
                ("trackTemperature", ctypes.c_int8),
                ("airTemperature", ctypes.c_int8),
                ("totalLaps", ctypes.c_uint8),
                ("trackLength", ctypes.c_uint16),
                ("sessionType", ctypes.c_uint8),
                ("trackId", ctypes.c_int8),
                ("formula", ctypes.c_uint8),
                ("sessionTimeLeft", ctypes.c_uint16),
                ("sessionDuration", ctypes.c_uint16),
                ("pitSpeedLimit", ctypes.c_uint8),
                ("gamePaused", ctypes.c_uint8),
                ("isSpectating", ctypes.c_uint8),
                ("spectatorCarIndex", ctypes.c_uint8),
                ("sliProNativeSupport", ctypes.c_uint8),
                ("numMarshalZones", ctypes.c_uint8),
                ("safetyCarStatus", ctypes.c_uint8),
                ("networkGame", ctypes.c_uint8)
            ]

class LapData(ctypes.LittleEndianStructure):
            _pack_ = 1
            _fields_ = [
                ("lastLapTime", ctypes.c_float),
                ("currentLapTime", ctypes.c_float),
                ("sector1Time", ctypes.c_uint16),
                ("sector2Time", ctypes.c_uint16),
                ("lapDistance", ctypes.c_float),
                ("totalDistance", ctypes.c_float),
                ("safetyCarDelta", ctypes.c_float),
                ("carPosition", ctypes.c_uint8),
                ("currentLapNum", ctypes.c_uint8)
            ]


class TelemetryData(ctypes.LittleEndianStructure):
            _pack_ = 1
            _fields_ = [
                ("speed", ctypes.c_uint16),
                ("throttle", ctypes.c_float),
                ("steer", ctypes.c_float),
                ("brake", ctypes.c_float),
                ("clutch", ctypes.c_uint8),
                ("gear", ctypes.c_int8),
                ("engineRPM", ctypes.c_uint16),
                ("drs", ctypes.c_uint8),
                ("revLightsPercent", ctypes.c_uint8),
                ("brakesTemperature", ctypes.c_uint16 * 4),
                ("tyresSurfaceTemperature", ctypes.c_uint8 * 4),
                ("tyresInnerTemperature", ctypes.c_uint8 * 4),
                ("engineTemperature", ctypes.c_uint16),
                ("tyresPressure", ctypes.c_float * 4)
            ]

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

