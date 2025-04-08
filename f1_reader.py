import ctypes
import socket
from datetime import datetime
from resources.utils import *
from interfaces.interfaces import *


class F1Reader:

    
    def __init__(self, ip='0.0.0.0', port=20778):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_handlers = get_packet_handlers(self)
        self.sock.bind((ip, port))

    
    def start(self):
        print("🎮 Esperando paquetes UDP de F1 23...")

        while True:

            data, address = self.sock.recvfrom(65535)
            
            header = PacketHeader.from_buffer_copy(data[:ctypes.sizeof(PacketHeader)])
            packet_id = header.packetId
            
            print(f"Paquete recibido con ID: {packet_id}\n")
            createFile(f"Paquete recibido con ID: {packet_id}\n", "header_struct")
            header_dict = header_to_dict(header)
            createFile(header_dict, "header")
            
            parsed_data = self.route_packet(packet_id, data)
            parsed_data = parsed_data or {}

            parsed_data['packet_id'] = packet_id
            parsed_data['timestamp'] = datetime.utcnow().isoformat()
            parsed_data['session_uid'] = str(header.sessionUID)
            parsed_data['car_index'] = header.playerCarIndex
            createFile(parsed_data, "parsedData")

            yield parsed_data
    
    

    def route_packet(self, packet_id, data):

        handler = self.packet_handlers.get(packet_id)
        if handler:
            return handler(data)
        print(f"⚠️ Paquete con packet_id {packet_id} no procesado.")
        return {'error': f'packet_id {packet_id} no procesado'}

    def parse_motion(self, data):
        packet = PacketMotionData.from_buffer_copy(data)
        motion_list = []

        for car in packet.carMotionData:
            motion_list.append({
                'position': [car.worldPositionX, car.worldPositionY, car.worldPositionZ],
                'velocity': [car.worldVelocityX, car.worldVelocityY, car.worldVelocityZ],
                'forwardDir': [car.worldForwardDirX, car.worldForwardDirY, car.worldForwardDirZ],
                'rightDir': [car.worldRightDirX, car.worldRightDirY, car.worldRightDirZ],
                'gForce': [car.gForceLateral, car.gForceLongitudinal, car.gForceVertical],
                'rotation': [car.yaw, car.pitch, car.roll]
            })
        createFile({ 'motion': motion_list }, 'motion')

        return {
            'motion': motion_list
        }

    def parse_session(self, data):
        packet = PacketSessionData.from_buffer_copy(data)

        return {
            'session': {
                'weather': packet.weather,
                'trackTemperature': packet.trackTemperature,
                'airTemperature': packet.airTemperature,
                'totalLaps': packet.totalLaps,
                'trackLength': packet.trackLength,
                'sessionType': packet.sessionType,
                'trackId': packet.trackId,
                'formula': packet.formula,
                'sessionTimeLeft': packet.sessionTimeLeft,
                'sessionDuration': packet.sessionDuration,
                'pitSpeedLimit': packet.pitSpeedLimit,
                'gamePaused': packet.gamePaused,
                'isSpectating': packet.isSpectating,
                'spectatorCarIndex': packet.spectatorCarIndex,
                'sliProNativeSupport': packet.sliProNativeSupport,
                'numMarshalZones': packet.numMarshalZones,
                'safetyCarStatus': packet.safetyCarStatus,
                'networkGame': packet.networkGame,
                'weatherForecastSamples': [
                    {
                        'sessionType': sample.sessionType,
                        'timeOffset': sample.timeOffset,
                        'weather': sample.weather,
                        'trackTemperature': sample.trackTemperature,
                        'trackTemperatureChange': sample.trackTemperatureChange,
                        'airTemperature': sample.airTemperature,
                        'airTemperatureChange': sample.airTemperatureChange,
                        'rainPercentage': sample.rainPercentage
                    }
                    for sample in packet.weatherForecastSamples[:packet.numWeatherForecastSamples]
                ]
            }
        }
  
    def parse_lap_data(self, data):
        packet = PacketLapData.from_buffer_copy(data)

        lap_list = []
        for lap in packet.lapData:
            lap_list.append({
                'lastLapTimeInMS': lap.lastLapTimeInMS,
                'currentLapTimeInMS': lap.currentLapTimeInMS,
                'sector1TimeMSPart': lap.sector1TimeMSPart,
                'sector1TimeMinutesPart': lap.sector1TimeMinutesPart,
                'sector2TimeMSPart': lap.sector2TimeMSPart,
                'sector2TimeMinutesPart': lap.sector2TimeMinutesPart,
                'deltaToCarInFrontMSPart': lap.deltaToCarInFrontMSPart,
                'deltaToCarInFrontMinutesPart': lap.deltaToCarInFrontMinutesPart,
                'deltaToRaceLeaderMSPart': lap.deltaToRaceLeaderMSPart,
                'deltaToRaceLeaderMinutesPart': lap.deltaToRaceLeaderMinutesPart,
                'lapDistance': lap.lapDistance,
                'totalDistance': lap.totalDistance,
                'safetyCarDelta': lap.safetyCarDelta,
                'carPosition': lap.carPosition,
                'currentLapNum': lap.currentLapNum,
                'pitStatus': lap.pitStatus,
                'numPitStops': lap.numPitStops,
                'sector': lap.sector,
                'currentLapInvalid': lap.currentLapInvalid,
                'penalties': lap.penalties,
                'totalWarnings': lap.totalWarnings,
                'cornerCuttingWarnings': lap.cornerCuttingWarnings,
                'numUnservedDriveThroughPens': lap.numUnservedDriveThroughPens,
                'numUnservedStopGoPens': lap.numUnservedStopGoPens,
                'gridPosition': lap.gridPosition,
                'driverStatus': lap.driverStatus,
                'resultStatus': lap.resultStatus,
                'pitLaneTimerActive': lap.pitLaneTimerActive,
                'pitLaneTimeInLaneInMS': lap.pitLaneTimeInLaneInMS,
                'pitStopTimerInMS': lap.pitStopTimerInMS,
                'pitStopShouldServePen': lap.pitStopShouldServePen,
                'speedTrapFastestSpeed': lap.speedTrapFastestSpeed,
                'speedTrapFastestLap': lap.speedTrapFastestLap
            })

        return {
            'lapData': lap_list,
            'pbCarIdx': packet.timeTrialPBCarIdx,
            'rivalCarIdx': packet.timeTrialRivalCarIdx
        }

    def parse_event(self, data):
        packet = PacketEventData.from_buffer_copy(data)
        event_code = packet.eventStringCode.decode('utf-8').strip('\x00')

        event_data = {'eventStringCode': event_code}

        if event_code == "FTLP":
            event_data.update({
                'vehicleIdx': packet.eventDetails.fastestLap.vehicleIdx,
                'lapTime': packet.eventDetails.fastestLap.lapTime
            })
        elif event_code == "RTMT":
            event_data.update({
                'vehicleIdx': packet.eventDetails.retirement.vehicleIdx
            })
        elif event_code == "TMPT":
            event_data.update({
                'vehicleIdx': packet.eventDetails.teamMateInPits.vehicleIdx
            })
        elif event_code == "RCWN":
            event_data.update({
                'vehicleIdx': packet.eventDetails.raceWinner.vehicleIdx
            })
        elif event_code == "PENA":
            ed = packet.eventDetails.penalty
            event_data.update({
                'penaltyType': ed.penaltyType,
                'infringementType': ed.infringementType,
                'vehicleIdx': ed.vehicleIdx,
                'otherVehicleIdx': ed.otherVehicleIdx,
                'time': ed.time,
                'lapNum': ed.lapNum,
                'placesGained': ed.placesGained
            })
        elif event_code == "SPTP":
            ed = packet.eventDetails.speedTrap
            event_data.update({
                'vehicleIdx': ed.vehicleIdx,
                'speed': ed.speed,
                'isOverallFastestInSession': ed.isOverallFastestInSession,
                'isDriverFastestInSession': ed.isDriverFastestInSession,
                'fastestVehicleIdxInSession': ed.fastestVehicleIdxInSession,
                'fastestSpeedInSession': ed.fastestSpeedInSession
            })

        return {'event': event_data}

    def parse_car_telemetry(self, data):
        packet = PacketCarTelemetryData.from_buffer_copy(data)

        telemetry_list = []
        for car in packet.carTelemetryData:
            telemetry_list.append({
                'speed': car.speed,
                'throttle': car.throttle,
                'steer': car.steer,
                'brake': car.brake,
                'clutch': car.clutch,
                'gear': car.gear,
                'engineRPM': car.engineRPM,
                'drs': car.drs,
                'revLightsPercent': car.revLightsPercent,
                'revLightsBitValue': car.revLightsBitValue,
                'brakesTemperature': list(car.brakesTemperature),
                'tyresSurfaceTemperature': list(car.tyresSurfaceTemperature),
                'tyresInnerTemperature': list(car.tyresInnerTemperature),
                'engineTemperature': car.engineTemperature,
                'tyresPressure': list(car.tyresPressure),
                'surfaceType': list(car.surfaceType)
            })

        return {
            'carTelemetry': telemetry_list,
            'mfdPanelIndex': packet.mfdPanelIndex,
            'mfdPanelIndexSecondaryPlayer': packet.mfdPanelIndexSecondaryPlayer,
            'suggestedGear': packet.suggestedGear
        }

    def parse_participants(self, data):
        packet = PacketParticipantsData.from_buffer_copy(data)

        participants = []
        for p in packet.participants:
            participants.append({
                'aiControlled': p.aiControlled,
                'driverId': p.driverId,
                'networkId': p.networkId,
                'teamId': p.teamId,
                'myTeam': p.myTeam,
                'raceNumber': p.raceNumber,
                'nationality': p.nationality,
                'name': p.name.decode('utf-8', errors='ignore').rstrip('\x00'),
                'yourTelemetry': p.yourTelemetry
            })

        return {
            'participants': participants,
            'numActiveCars': packet.numActiveCars
    }

    def parse_car_setups(self, data):
        packet = PacketCarSetupData.from_buffer_copy(data)

        setups = []
        for setup in packet.carSetups:
            setups.append({
                'frontWing': setup.frontWing,
                'rearWing': setup.rearWing,
                'onThrottle': setup.onThrottle,
                'offThrottle': setup.offThrottle,
                'frontCamber': setup.frontCamber,
                'rearCamber': setup.rearCamber,
                'frontToe': setup.frontToe,
                'rearToe': setup.rearToe,
                'frontSuspension': setup.frontSuspension,
                'rearSuspension': setup.rearSuspension,
                'frontAntiRollBar': setup.frontAntiRollBar,
                'rearAntiRollBar': setup.rearAntiRollBar,
                'frontSuspensionHeight': setup.frontSuspensionHeight,
                'rearSuspensionHeight': setup.rearSuspensionHeight,
                'brakePressure': setup.brakePressure,
                'brakeBias': setup.brakeBias,
                'rearLeftTyrePressure': setup.rearLeftTyrePressure,
                'rearRightTyrePressure': setup.rearRightTyrePressure,
                'frontLeftTyrePressure': setup.frontLeftTyrePressure,
                'frontRightTyrePressure': setup.frontRightTyrePressure,
                'ballast': setup.ballast,
                'fuelLoad': setup.fuelLoad
            })

        return {
            'carSetups': setups
        }

    def parse_car_status(self, data):
        packet = PacketCarStatusData.from_buffer_copy(data)

        status_list = []
        for status in packet.carStatusData:
            status_list.append({
                'tractionControl': status.tractionControl,
                'antiLockBrakes': status.antiLockBrakes,
                'fuelMix': status.fuelMix,
                'frontBrakeBias': status.frontBrakeBias,
                'pitLimiterStatus': status.pitLimiterStatus,
                'fuelInTank': status.fuelInTank,
                'fuelCapacity': status.fuelCapacity,
                'fuelRemainingLaps': status.fuelRemainingLaps,
                'maxRPM': status.maxRPM,
                'idleRPM': status.idleRPM,
                'maxGears': status.maxGears,
                'drsAllowed': status.drsAllowed,
                'drsActivationDistance': status.drsActivationDistance,
                'actualTyreCompound': status.actualTyreCompound,
                'visualTyreCompound': status.visualTyreCompound,
                'tyresAgeLaps': status.tyresAgeLaps,
                'vehicleFiaFlags': status.vehicleFiaFlags,
                'enginePowerICE': status.enginePowerICE,
                'enginePowerMGUK': status.enginePowerMGUK,
                'ersStoreEnergy': status.ersStoreEnergy,
                'ersDeployMode': status.ersDeployMode,
                'ersHarvestedThisLapMGUK': status.ersHarvestedThisLapMGUK,
                'ersHarvestedThisLapMGUH': status.ersHarvestedThisLapMGUH,
                'ersDeployedThisLap': status.ersDeployedThisLap,
                'networkPaused': status.networkPaused
            })

        return {
            'carStatus': status_list
        }

    def parse_final_classification(self, data):
        packet = PacketFinalClassificationData.from_buffer_copy(data)

        results = []
        for r in packet.classificationData:
            results.append({
                'position': r.position,
                'numLaps': r.numLaps,
                'gridPosition': r.gridPosition,
                'points': r.points,
                'numPitStops': r.numPitStops,
                'resultStatus': r.resultStatus,
                'bestLapTimeInMS': r.bestLapTimeInMS,
                'totalRaceTime': r.totalRaceTime,
                'penaltiesTime': r.penaltiesTime,
                'numPenalties': r.numPenalties,
                'numTyreStints': r.numTyreStints,
                'tyreStintsActual': list(r.tyreStintsActual),
                'tyreStintsVisual': list(r.tyreStintsVisual),
                'tyreStintsEndLaps': list(r.tyreStintsEndLaps)
            })

        return {
            'finalClassification': results,
            'numCars': packet.numCars
        }

    def parse_car_damage(self, data):
        packet = PacketCarDamageData.from_buffer_copy(data)

        damages = []
        for d in packet.carDamageData:
            damages.append({
                'tyresWear': list(d.tyresWear),
                'tyresDamage': list(d.tyresDamage),
                'brakesDamage': list(d.brakesDamage),
                'frontLeftWingDamage': d.frontLeftWingDamage,
                'frontRightWingDamage': d.frontRightWingDamage,
                'rearWingDamage': d.rearWingDamage,
                'floorDamage': d.floorDamage,
                'diffuserDamage': d.diffuserDamage,
                'sidepodDamage': d.sidepodDamage,
                'drsFault': d.drsFault,
                'gearBoxDamage': d.gearBoxDamage,
                'engineDamage': d.engineDamage,
                'engineMGUHWear': d.engineMGUHWear,
                'engineESWear': d.engineESWear,
                'engineCEWear': d.engineCEWear,
                'engineICEWear': d.engineICEWear,
                'engineMGUKWear': d.engineMGUKWear,
                'engineTCWear': d.engineTCWear
            })

        return {
            'carDamage': damages
        }

    def parse_session_history(self, data):
        packet = PacketSessionHistoryData.from_buffer_copy(data)

        laps = []
        for lap in packet.lapHistoryData[:packet.numLaps]:
            laps.append({
                'lapTimeInMS': lap.lapTimeInMS,
                'sector1TimeInMS': lap.sector1TimeInMS,
                'sector2TimeInMS': lap.sector2TimeInMS,
                'sector3TimeInMS': lap.sector3TimeInMS,
                'lapValidBitFlags': lap.lapValidBitFlags
            })

        stints = []
        for stint in packet.tyreStintsHistoryData[:packet.numTyreStints]:
            stints.append({
                'endLap': stint.endLap,
                'tyreActualCompound': stint.tyreActualCompound,
                'tyreVisualCompound': stint.tyreVisualCompound
            })

        return {
            'sessionHistory': {
                'carIdx': packet.carIdx,
                'numLaps': packet.numLaps,
                'numTyreStints': packet.numTyreStints,
                'bestLapTimeLapNum': packet.bestLapTimeLapNum,
                'bestSector1LapNum': packet.bestSector1LapNum,
                'bestSector2LapNum': packet.bestSector2LapNum,
                'bestSector3LapNum': packet.bestSector3LapNum,
                'lapHistoryData': laps,
                'tyreStintsHistoryData': stints
            }
        }

    def parse_tyre_sets(self, data):
        
        expected_size = ctypes.sizeof(PacketTyreSetsData)
        
        if len(data) < expected_size:
            return {
                'tyreSets': '',
                'error': f"Paquete demasiado corto: {len(data)} < {expected_size}"
            }
        
        packet = PacketTyreSetsData.from_buffer_copy(data)
        
        tyre_sets = []
        for ts in packet.tyreSetData:
            tyre_sets.append({
                'actualTyreCompound': ts.actualTyreCompound,
                'visualTyreCompound': ts.visualTyreCompound,
                'wear': ts.wear,
                'available': ts.available,
                'recommendedSession': ts.recommendedSession,
                'lifeSpan': ts.lifeSpan,
                'usableLife': ts.usableLife,
                'lapDeltaTime': ts.lapDeltaTime,
                'fitted': ts.fitted
            })

        return {
            'carIdx': packet.carIdx,
            'tyreSets': tyre_sets
        }

    def parse_time_trial(self, data):
        packet = PacketTimeTrialData.from_buffer_copy(data)

        return {
            'timeTrial': {
                'deltaTimeInMS': packet.deltaTimeInMS
            }
        }

    def parse_lobby_info(self, data):
        packet = PacketLobbyInfoData.from_buffer_copy(data)

        players = []
        for p in packet.lobbyPlayers:
            players.append({
                'aiControlled': p.aiControlled,
                'teamId': p.teamId,
                'nationality': p.nationality,
                'platform': p.platform,
                'name': p.name.decode('utf-8', errors='ignore').rstrip('\x00'),
                'carNumber': p.carNumber,
                'readyStatus': p.readyStatus
            })

        return {
            'lobbyPlayers': players,
            'numPlayers': packet.numPlayers
        }


if __name__ == '__main__':
    reader = F1Reader()
    for packet in reader.start():
        print(packet)
