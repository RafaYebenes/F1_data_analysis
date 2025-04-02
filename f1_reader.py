import socket
import ctypes
import json
from datetime import datetime

class PacketHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("packetFormat", ctypes.c_uint16),
        ("gameYear", ctypes.c_uint8),
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

class F123FullParser:
    def __init__(self, ip='0.0.0.0', port=20778):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(0.1)

    def read_packet(self):
        try:
            data, _ = self.sock.recvfrom(2048)
            return self.route_packet(data)
        except socket.timeout:
            return None
        except Exception as e:
            print(f"❌ Error leyendo paquete: {e}")
            return None

    def route_packet(self, data):
        if len(data) < ctypes.sizeof(PacketHeader):
            print(f"❗ Paquete demasiado pequeño: {len(data)} bytes")
            return None

        try:
            header = PacketHeader.from_buffer_copy(data)
            packet_id = header.packetId
            print(f"📦 packet_id detectado: {packet_id} (tam: {len(data)} bytes)")
        except Exception as e:
            print("❌ Error leyendo el header con ctypes:", e)
            return None

        packet_map = {
            0: self.parse_motion,
            1: self.parse_session,
            2: self.parse_lap_data,
            3: self.parse_event,
            4: self.parse_participants,
            5: self.parse_car_setups,
            6: self.parse_car_telemetry,
            7: self.parse_car_status,
            8: self.parse_final_classification
        }

        parser = packet_map.get(packet_id)
        if parser:
            try:
                parsed = parser(data)
            except Exception as e:
                return {'packet_id': packet_id, 'error': str(e), 'timestamp': datetime.now().isoformat()}

            parsed['timestamp'] = datetime.now().isoformat()
            parsed['packet_id'] = packet_id
            return parsed
        else:
            return {'packet_id': packet_id, 'raw_data': data.hex(), 'timestamp': datetime.now().isoformat()}

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
        motion_data = MotionData.from_buffer_copy(data[offset:offset + ctypes.sizeof(MotionData)])

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
        session_data = SessionData.from_buffer_copy(data[offset:offset + ctypes.sizeof(SessionData)])

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
        lap_data = LapData.from_buffer_copy(data[offset:offset + ctypes.sizeof(LapData)])

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

    def parse_participants(self, data):
        return {'participants': {'status': 'ok'}}

    def parse_car_setups(self, data):
        return {'carSetups': {'status': 'ok'}}

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
        telemetry = TelemetryData.from_buffer_copy(data[offset:offset + ctypes.sizeof(TelemetryData)])

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

    def parse_car_status(self, data):
        return {'carStatus': {'status': 'ok'}}

    def parse_final_classification(self, data):
        return {'finalClassification': {'status': 'ok'}}

if __name__ == '__main__':
    parser = F123FullParser()
    while True:
        packet = parser.read_packet()
        if packet:
            print(json.dumps(packet, indent=2))