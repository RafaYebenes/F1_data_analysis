import ctypes
import socket
from datetime import datetime

class PacketHeader(ctypes.LittleEndianStructure):
    _fields_ = [
        ("packetFormat", ctypes.c_uint16),
        ("gameMajorVersion", ctypes.c_uint8),
        ("gameMinorVersion", ctypes.c_uint8),
        ("packetVersion", ctypes.c_uint8),
        ("packetId", ctypes.c_uint8),
        ("sessionUID", ctypes.c_uint64),
        ("sessionTime", ctypes.c_float),
        ("frameIdentifier", ctypes.c_uint32),
        ("overallFrameIdentifier", ctypes.c_uint32),
        ("playerCarIndex", ctypes.c_uint8),
        ("secondaryPlayerCarIndex", ctypes.c_uint8)
    ]

class F1Reader:
    def __init__(self, ip='0.0.0.0', port=20778):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def start(self):
        print("🎮 Esperando paquetes UDP de F1 23...")
        while True:
            data, _ = self.sock.recvfrom(4096)
            header = PacketHeader.from_buffer_copy(data[:ctypes.sizeof(PacketHeader)])
            packet_id = header.packetId

            parsed_data = self.route_packet(packet_id, data)
            parsed_data = parsed_data or {}

            parsed_data['packet_id'] = packet_id
            parsed_data['timestamp'] = datetime.utcnow().isoformat()
            parsed_data['session_uid'] = str(header.sessionUID)
            parsed_data['car_index'] = header.playerCarIndex

            yield parsed_data

    def route_packet(self, packet_id, data):
        if packet_id == 0:
            return self.parse_motion(data)
        elif packet_id == 1:
            return self.parse_session(data)
        elif packet_id == 2:
            return self.parse_lap_data(data)
        elif packet_id == 3:
            return self.parse_event(data)
        elif packet_id == 6:
            return self.parse_car_telemetry(data)

        print(f"⚠️ Paquete con packet_id {packet_id} no procesado.")
        return {'error': f'packet_id {packet_id} no procesado'}

    def parse_motion(self, data):
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

        offset = ctypes.sizeof(PacketHeader)
        motion_bytes = data[offset:offset + ctypes.sizeof(MotionData)]
        if len(motion_bytes) < ctypes.sizeof(MotionData):
            return {'motion': '', 'error': "Paquete MotionData demasiado corto"}

        motion_data = MotionData.from_buffer_copy(motion_bytes)

        return {
            'motion': {
                'worldPosition': [motion_data.worldPositionX, motion_data.worldPositionY, motion_data.worldPositionZ],
                'velocity': [motion_data.worldVelocityX, motion_data.worldVelocityY, motion_data.worldVelocityZ],
                'gForce': [motion_data.gForceLateral, motion_data.gForceLongitudinal, motion_data.gForceVertical],
                'rotation': [motion_data.yaw, motion_data.pitch, motion_data.roll]
            }
        }

    def parse_session(self, data):
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

        offset = ctypes.sizeof(PacketHeader)
        session_bytes = data[offset:offset + ctypes.sizeof(SessionData)]
        if len(session_bytes) < ctypes.sizeof(SessionData):
            return {'session': '', 'error': "Paquete session demasiado corto"}

        session_data = SessionData.from_buffer_copy(session_bytes)

        return {
            'session': {
                'weather': session_data.weather,
                'trackTemperature': session_data.trackTemperature,
                'airTemperature': session_data.airTemperature,
                'totalLaps': session_data.totalLaps,
                'trackLength': session_data.trackLength,
                'sessionType': session_data.sessionType,
                'trackId': session_data.trackId,
                'formula': session_data.formula,
                'sessionTimeLeft': session_data.sessionTimeLeft,
                'sessionDuration': session_data.sessionDuration,
                'pitSpeedLimit': session_data.pitSpeedLimit,
                'gamePaused': session_data.gamePaused,
                'isSpectating': session_data.isSpectating,
                'spectatorCarIndex': session_data.spectatorCarIndex,
                'sliProNativeSupport': session_data.sliProNativeSupport,
                'numMarshalZones': session_data.numMarshalZones,
                'safetyCarStatus': session_data.safetyCarStatus,
                'networkGame': session_data.networkGame
            }
        }

    def parse_lap_data(self, data):
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

        offset = ctypes.sizeof(PacketHeader)
        lap_bytes = data[offset:offset + ctypes.sizeof(LapData)]
        if len(lap_bytes) < ctypes.sizeof(LapData):
            return {'lapData': '', 'error': "Paquete lap_data demasiado corto"}

        lap_data = LapData.from_buffer_copy(lap_bytes)

        return {
            'lapData': {
                'lastLapTime': lap_data.lastLapTime,
                'currentLapTime': lap_data.currentLapTime,
                'sector1Time': lap_data.sector1Time,
                'sector2Time': lap_data.sector2Time,
                'lapDistance': lap_data.lapDistance,
                'totalDistance': lap_data.totalDistance,
                'safetyCarDelta': lap_data.safetyCarDelta,
                'carPosition': lap_data.carPosition,
                'currentLapNum': lap_data.currentLapNum
            }
        }

    def parse_event(self, data):
        class EventDataDetails(ctypes.LittleEndianStructure):
            _pack_ = 1
            _fields_ = [("eventStringCode", ctypes.c_char * 4)]

        offset = ctypes.sizeof(PacketHeader)
        event = EventDataDetails.from_buffer_copy(data[offset:offset + ctypes.sizeof(EventDataDetails)])
        event_code = event.eventStringCode.decode('utf-8').strip('\x00')

        return {'event': {'eventStringCode': event_code}}

    def parse_car_telemetry(self, data):
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

        offset = ctypes.sizeof(PacketHeader)
        telemetry_bytes = data[offset:offset + ctypes.sizeof(TelemetryData)]
        if len(telemetry_bytes) < ctypes.sizeof(TelemetryData):
            return {'carTelemetry': '', 'error': "Paquete carTelemetry demasiado corto"}

        telemetry = TelemetryData.from_buffer_copy(telemetry_bytes)

        return {
            'carTelemetry': {
                'speed': telemetry.speed,
                'throttle': telemetry.throttle,
                'steer': telemetry.steer,
                'brake': telemetry.brake,
                'clutch': telemetry.clutch,
                'gear': telemetry.gear,
                'engineRPM': telemetry.engineRPM,
                'drs': telemetry.drs,
                'revLightsPercent': telemetry.revLightsPercent,
                'brakesTemperature': list(telemetry.brakesTemperature),
                'tyresSurfaceTemperature': list(telemetry.tyresSurfaceTemperature),
                'tyresInnerTemperature': list(telemetry.tyresInnerTemperature),
                'engineTemperature': telemetry.engineTemperature,
                'tyresPressure': list(telemetry.tyresPressure)
            }
        }

if __name__ == '__main__':
    reader = F1Reader()
    for packet in reader.start():
        print(packet)
