import ctypes
import socket
from datetime import datetime
from resources.utils import *
from interfaces.interfaces import *
import redis
from services.realtime_live_data import *

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


class F1Reader:

    def __init__(self, ip='0.0.0.0', port=20778):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_handlers = get_packet_handlers(self)
        self.sock.bind((ip, port))

    def start(self):
        print("🎮 Esperando paquetes UDP de F1 25...")

        while True:
            data, address = self.sock.recvfrom(65535)

            header = PacketHeader.from_buffer_copy(data[:ctypes.sizeof(PacketHeader)])
            packet_id = header.packetId

            header_dict = header_to_dict(header)
            ##createFile(header_dict, "header")

            parsed_data = self.route_packet(packet_id, data)
            parsed_data = parsed_data or {}

            parsed_data['packet_id'] = packet_id
            parsed_data['timestamp'] = datetime.utcnow().isoformat()
            parsed_data['session_uid'] = str(header.sessionUID)
            parsed_data['car_index'] = header.playerCarIndex
            ##createFile(parsed_data, "parsedData")

            updated_data = ""
            channel = ""
            if packet_id in {1, 2, 6, 7}:
                channel = "car_data"
                updated_data = update_live_data(parsed_data)

            if packet_id == 10:
                channel = "car_damage"
                updated_data = get_damage_info(parsed_data)

            self.save_to_redis(updated_data, channel)

            if packet_id in {0, 6}:
                trackHeatMap = get_track_heat_map(parsed_data)
                self.save_to_redis(trackHeatMap, "trackHeatMap")

            yield updated_data

    def route_packet(self, packet_id, data):
        handler = self.packet_handlers.get(packet_id)
        if handler:
            return handler(data)
        print(f"⚠️ Paquete con packet_id {packet_id} no procesado.")
        return {'error': f'packet_id {packet_id} no procesado'}

    # ------------------------------------------------------------------ #
    # ID 0 — Motion
    # ------------------------------------------------------------------ #
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
                'rotation': [car.yaw, car.pitch, car.roll],
            })
        return {'motion': motion_list}

    # ------------------------------------------------------------------ #
    # ID 1 — Session
    # ------------------------------------------------------------------ #
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
                'numWeatherForecastSamples': packet.numWeatherForecastSamples,
                'weatherForecastSamples': [
                    {
                        'sessionType': s.sessionType,
                        'timeOffset': s.timeOffset,
                        'weather': s.weather,
                        'trackTemperature': s.trackTemperature,
                        'trackTemperatureChange': s.trackTemperatureChange,
                        'airTemperature': s.airTemperature,
                        'airTemperatureChange': s.airTemperatureChange,
                        'rainPercentage': s.rainPercentage,
                    }
                    for s in packet.weatherForecastSamples[:packet.numWeatherForecastSamples]
                ],
                # F1 24/25 additions
                'forecastAccuracy': packet.forecastAccuracy,
                'aiDifficulty': packet.aiDifficulty,
                'pitStopWindowIdealLap': packet.pitStopWindowIdealLap,
                'pitStopWindowLatestLap': packet.pitStopWindowLatestLap,
                'pitStopRejoinPosition': packet.pitStopRejoinPosition,
                'gameMode': packet.gameMode,
                'ruleSet': packet.ruleSet,
                'timeOfDay': packet.timeOfDay,
                'sessionLength': packet.sessionLength,
                'numSafetyCarPeriods': packet.numSafetyCarPeriods,
                'numVirtualSafetyCarPeriods': packet.numVirtualSafetyCarPeriods,
                'numRedFlagPeriods': packet.numRedFlagPeriods,
                'sector2LapDistanceStart': packet.sector2LapDistanceStart,
                'sector3LapDistanceStart': packet.sector3LapDistanceStart,
            }
        }

    # ------------------------------------------------------------------ #
    # ID 2 — Lap Data
    # ------------------------------------------------------------------ #
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
                'speedTrapFastestLap': lap.speedTrapFastestLap,
            })
        return {
            'lapData': lap_list,
            'pbCarIdx': packet.timeTrialPBCarIdx,
            'rivalCarIdx': packet.timeTrialRivalCarIdx,
        }

    # ------------------------------------------------------------------ #
    # ID 3 — Event
    # ------------------------------------------------------------------ #
    def parse_event(self, data):
        packet = PacketEventData.from_buffer_copy(data)
        event_code = packet.eventStringCode.decode('utf-8').strip('\x00')
        event_data = {'eventStringCode': event_code}

        if event_code == "FTLP":
            event_data.update({
                'vehicleIdx': packet.eventDetails.fastestLap.vehicleIdx,
                'lapTime': packet.eventDetails.fastestLap.lapTime,
            })
        elif event_code == "RTMT":
            event_data.update({
                'vehicleIdx': packet.eventDetails.retirement.vehicleIdx,
                'reason': packet.eventDetails.retirement.reason,
            })
        elif event_code == "DRSD":
            event_data.update({'reason': packet.eventDetails.drsDisabled.reason})
        elif event_code == "TMPT":
            event_data.update({'vehicleIdx': packet.eventDetails.teamMateInPits.vehicleIdx})
        elif event_code == "RCWN":
            event_data.update({'vehicleIdx': packet.eventDetails.raceWinner.vehicleIdx})
        elif event_code == "PENA":
            ed = packet.eventDetails.penalty
            event_data.update({
                'penaltyType': ed.penaltyType,
                'infringementType': ed.infringementType,
                'vehicleIdx': ed.vehicleIdx,
                'otherVehicleIdx': ed.otherVehicleIdx,
                'time': ed.time,
                'lapNum': ed.lapNum,
                'placesGained': ed.placesGained,
            })
        elif event_code == "SPTP":
            ed = packet.eventDetails.speedTrap
            event_data.update({
                'vehicleIdx': ed.vehicleIdx,
                'speed': ed.speed,
                'isOverallFastestInSession': ed.isOverallFastestInSession,
                'isDriverFastestInSession': ed.isDriverFastestInSession,
                'fastestVehicleIdxInSession': ed.fastestVehicleIdxInSession,
                'fastestSpeedInSession': ed.fastestSpeedInSession,
            })
        elif event_code == "STLG":
            event_data.update({'numLights': packet.eventDetails.startLights.numLights})
        elif event_code == "DTSV":
            event_data.update({'vehicleIdx': packet.eventDetails.driveThroughPenaltyServed.vehicleIdx})
        elif event_code == "SGSV":
            ed = packet.eventDetails.stopGoPenaltyServed
            event_data.update({'vehicleIdx': ed.vehicleIdx, 'stopTime': ed.stopTime})
        elif event_code == "FLBK":
            ed = packet.eventDetails.flashback
            event_data.update({
                'flashbackFrameIdentifier': ed.flashbackFrameIdentifier,
                'flashbackSessionTime': ed.flashbackSessionTime,
            })
        elif event_code == "BUTN":
            event_data.update({'buttonStatus': packet.eventDetails.buttons.buttonStatus})
        elif event_code == "OVTK":
            ed = packet.eventDetails.overtake
            event_data.update({
                'overtakingVehicleIdx': ed.overtakingVehicleIdx,
                'beingOvertakenVehicleIdx': ed.beingOvertakenVehicleIdx,
            })
        elif event_code == "SCAR":
            ed = packet.eventDetails.safetyCar
            event_data.update({'safetyCarType': ed.safetyCarType, 'eventType': ed.eventType})
        elif event_code == "COLL":
            ed = packet.eventDetails.collision
            event_data.update({'vehicle1Idx': ed.vehicle1Idx, 'vehicle2Idx': ed.vehicle2Idx})
        # SSTA, SEND, DRSE, CHQF, LGOT, RDFL carry no extra data

        return {'event': event_data}

    # ------------------------------------------------------------------ #
    # ID 4 — Participants
    # ------------------------------------------------------------------ #
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
                'yourTelemetry': p.yourTelemetry,
                'showOnlineNames': p.showOnlineNames,
                'techLevel': p.techLevel,
                'platform': p.platform,
                'liveryColours': [
                    {'r': c.red, 'g': c.green, 'b': c.blue}
                    for c in p.liveryColours[:p.numColours]
                ],
            })
        return {'participants': participants, 'numActiveCars': packet.numActiveCars}

    # ------------------------------------------------------------------ #
    # ID 5 — Car Setups
    # ------------------------------------------------------------------ #
    def parse_car_setups(self, data):
        packet = PacketCarSetupData.from_buffer_copy(data)
        setups = []
        for s in packet.carSetups:
            setups.append({
                'frontWing': s.frontWing,
                'rearWing': s.rearWing,
                'onThrottle': s.onThrottle,
                'offThrottle': s.offThrottle,
                'frontCamber': s.frontCamber,
                'rearCamber': s.rearCamber,
                'frontToe': s.frontToe,
                'rearToe': s.rearToe,
                'frontSuspension': s.frontSuspension,
                'rearSuspension': s.rearSuspension,
                'frontAntiRollBar': s.frontAntiRollBar,
                'rearAntiRollBar': s.rearAntiRollBar,
                'frontSuspensionHeight': s.frontSuspensionHeight,
                'rearSuspensionHeight': s.rearSuspensionHeight,
                'brakePressure': s.brakePressure,
                'brakeBias': s.brakeBias,
                'engineBraking': s.engineBraking,
                'rearLeftTyrePressure': s.rearLeftTyrePressure,
                'rearRightTyrePressure': s.rearRightTyrePressure,
                'frontLeftTyrePressure': s.frontLeftTyrePressure,
                'frontRightTyrePressure': s.frontRightTyrePressure,
                'ballast': s.ballast,
                'fuelLoad': s.fuelLoad,
            })
        return {'carSetups': setups, 'nextFrontWingValue': packet.nextFrontWingValue}

    # ------------------------------------------------------------------ #
    # ID 6 — Car Telemetry
    # ------------------------------------------------------------------ #
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
                'surfaceType': list(car.surfaceType),
            })
        return {
            'carTelemetry': telemetry_list,
            'mfdPanelIndex': packet.mfdPanelIndex,
            'mfdPanelIndexSecondaryPlayer': packet.mfdPanelIndexSecondaryPlayer,
            'suggestedGear': packet.suggestedGear,
        }

    # ------------------------------------------------------------------ #
    # ID 7 — Car Status
    # ------------------------------------------------------------------ #
    def parse_car_status(self, data):
        packet = PacketCarStatusData.from_buffer_copy(data)
        status_list = []
        for s in packet.carStatusData:
            status_list.append({
                'tractionControl': s.tractionControl,
                'antiLockBrakes': s.antiLockBrakes,
                'fuelMix': s.fuelMix,
                'frontBrakeBias': s.frontBrakeBias,
                'pitLimiterStatus': s.pitLimiterStatus,
                'fuelInTank': s.fuelInTank,
                'fuelCapacity': s.fuelCapacity,
                'fuelRemainingLaps': s.fuelRemainingLaps,
                'maxRPM': s.maxRPM,
                'idleRPM': s.idleRPM,
                'maxGears': s.maxGears,
                'drsAllowed': s.drsAllowed,
                'drsActivationDistance': s.drsActivationDistance,
                'actualTyreCompound': s.actualTyreCompound,
                'visualTyreCompound': s.visualTyreCompound,
                'tyresAgeLaps': s.tyresAgeLaps,
                'vehicleFiaFlags': s.vehicleFiaFlags,
                'enginePowerICE': s.enginePowerICE,
                'enginePowerMGUK': s.enginePowerMGUK,
                'ersStoreEnergy': s.ersStoreEnergy,
                'ersDeployMode': s.ersDeployMode,
                'ersHarvestedThisLapMGUK': s.ersHarvestedThisLapMGUK,
                'ersHarvestedThisLapMGUH': s.ersHarvestedThisLapMGUH,
                'ersDeployedThisLap': s.ersDeployedThisLap,
                'networkPaused': s.networkPaused,
            })
        return {'carStatus': status_list}

    # ------------------------------------------------------------------ #
    # ID 8 — Final Classification
    # ------------------------------------------------------------------ #
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
                'resultReason': r.resultReason,
                'bestLapTimeInMS': r.bestLapTimeInMS,
                'totalRaceTime': r.totalRaceTime,
                'penaltiesTime': r.penaltiesTime,
                'numPenalties': r.numPenalties,
                'numTyreStints': r.numTyreStints,
                'tyreStintsActual': list(r.tyreStintsActual),
                'tyreStintsVisual': list(r.tyreStintsVisual),
                'tyreStintsEndLaps': list(r.tyreStintsEndLaps),
            })
        return {'finalClassification': results, 'numCars': packet.numCars}

    # ------------------------------------------------------------------ #
    # ID 9 — Lobby Info
    # ------------------------------------------------------------------ #
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
                'yourTelemetry': p.yourTelemetry,
                'showOnlineNames': p.showOnlineNames,
                'techLevel': p.techLevel,
                'readyStatus': p.readyStatus,
            })
        return {'lobbyPlayers': players, 'numPlayers': packet.numPlayers}

    # ------------------------------------------------------------------ #
    # ID 10 — Car Damage
    # ------------------------------------------------------------------ #
    def parse_car_damage(self, data):
        packet = PacketCarDamageData.from_buffer_copy(data)
        damages = []
        for d in packet.carDamageData:
            damages.append({
                'tyresWear': [round(w, 2) for w in d.tyresWear],   # float in F1 24/25
                'tyresDamage': list(d.tyresDamage),
                'brakesDamage': list(d.brakesDamage),
                'tyreBlisters': list(d.tyreBlisters),
                'frontLeftWingDamage': d.frontLeftWingDamage,
                'frontRightWingDamage': d.frontRightWingDamage,
                'rearWingDamage': d.rearWingDamage,
                'floorDamage': d.floorDamage,
                'diffuserDamage': d.diffuserDamage,
                'sidepodDamage': d.sidepodDamage,
                'drsFault': d.drsFault,
                'ersFault': d.ersFault,
                'gearBoxDamage': d.gearBoxDamage,
                'engineDamage': d.engineDamage,
                'engineMGUHWear': d.engineMGUHWear,
                'engineESWear': d.engineESWear,
                'engineCEWear': d.engineCEWear,
                'engineICEWear': d.engineICEWear,
                'engineMGUKWear': d.engineMGUKWear,
                'engineTCWear': d.engineTCWear,
                'engineBlown': d.engineBlown,
                'engineSeized': d.engineSeized,
            })
        return {'carDamage': damages}

    # ------------------------------------------------------------------ #
    # ID 11 — Session History
    # ------------------------------------------------------------------ #
    def parse_session_history(self, data):
        packet = PacketSessionHistoryData.from_buffer_copy(data)
        laps = []
        for lap in packet.lapHistoryData[:packet.numLaps]:
            laps.append({
                'lapTimeInMS': lap.lapTimeInMS,
                'sector1TimeMSPart': lap.sector1TimeMSPart,
                'sector1TimeMinutesPart': lap.sector1TimeMinutesPart,
                'sector2TimeMSPart': lap.sector2TimeMSPart,
                'sector2TimeMinutesPart': lap.sector2TimeMinutesPart,
                'sector3TimeMSPart': lap.sector3TimeMSPart,
                'sector3TimeMinutesPart': lap.sector3TimeMinutesPart,
                'lapValidBitFlags': lap.lapValidBitFlags,
            })
        stints = []
        for stint in packet.tyreStintsHistoryData[:packet.numTyreStints]:
            stints.append({
                'endLap': stint.endLap,
                'tyreActualCompound': stint.tyreActualCompound,
                'tyreVisualCompound': stint.tyreVisualCompound,
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
                'tyreStintsHistoryData': stints,
            }
        }

    # ------------------------------------------------------------------ #
    # ID 12 — Tyre Sets
    # ------------------------------------------------------------------ #
    def parse_tyre_sets(self, data):
        expected_size = ctypes.sizeof(PacketTyreSetsData)
        if len(data) < expected_size:
            return {'tyreSets': '', 'error': f"Paquete demasiado corto: {len(data)} < {expected_size}"}

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
                'lapDeltaTime': ts.lapDeltaTime,   # int16 ms (was float in F1 23)
                'fitted': ts.fitted,
            })
        return {
            'carIdx': packet.carIdx,
            'tyreSets': tyre_sets,
            'fittedIdx': packet.fittedIdx,
        }

    # ------------------------------------------------------------------ #
    # ID 13 — Motion Ex  (new in F1 24/25, player car only)
    # ------------------------------------------------------------------ #
    def parse_motion_ex(self, data):
        packet = PacketMotionExData.from_buffer_copy(data)
        return {
            'motionEx': {
                'suspensionPosition': list(packet.suspensionPosition),
                'suspensionVelocity': list(packet.suspensionVelocity),
                'suspensionAcceleration': list(packet.suspensionAcceleration),
                'wheelSpeed': list(packet.wheelSpeed),
                'wheelSlipRatio': list(packet.wheelSlipRatio),
                'wheelSlipAngle': list(packet.wheelSlipAngle),
                'wheelLatForce': list(packet.wheelLatForce),
                'wheelLongForce': list(packet.wheelLongForce),
                'heightOfCOGAboveGround': packet.heightOfCOGAboveGround,
                'localVelocity': [packet.localVelocityX, packet.localVelocityY, packet.localVelocityZ],
                'angularVelocity': [packet.angularVelocityX, packet.angularVelocityY, packet.angularVelocityZ],
                'angularAcceleration': [packet.angularAccelerationX, packet.angularAccelerationY, packet.angularAccelerationZ],
                'frontWheelsAngle': packet.frontWheelsAngle,
                'wheelVertForce': list(packet.wheelVertForce),
                'frontAeroHeight': packet.frontAeroHeight,
                'rearAeroHeight': packet.rearAeroHeight,
                'frontRollAngle': packet.frontRollAngle,
                'rearRollAngle': packet.rearRollAngle,
                'chassisYaw': packet.chassisYaw,
                'chassisPitch': packet.chassisPitch,
                'wheelCamber': list(packet.wheelCamber),
                'wheelCamberGain': list(packet.wheelCamberGain),
            }
        }

    # ------------------------------------------------------------------ #
    # ID 14 — Time Trial  (structure changed in F1 24/25)
    # ------------------------------------------------------------------ #
    def parse_time_trial(self, data):
        packet = PacketTimeTrialData.from_buffer_copy(data)

        def dataset_to_dict(ds):
            return {
                'carIdx': ds.carIdx,
                'teamId': ds.teamId,
                'lapTimeInMS': ds.lapTimeInMS,
                'sector1TimeInMS': ds.sector1TimeInMS,
                'sector2TimeInMS': ds.sector2TimeInMS,
                'sector3TimeInMS': ds.sector3TimeInMS,
                'tractionControl': ds.tractionControl,
                'gearboxAssist': ds.gearboxAssist,
                'antiLockBrakes': ds.antiLockBrakes,
                'equalCarPerformance': ds.equalCarPerformance,
                'customSetup': ds.customSetup,
                'valid': ds.valid,
            }

        return {
            'timeTrial': {
                'playerSessionBest': dataset_to_dict(packet.playerSessionBestDataSet),
                'personalBest': dataset_to_dict(packet.personalBestDataSet),
                'rival': dataset_to_dict(packet.rivalDataSet),
            }
        }

    # ------------------------------------------------------------------ #
    # ID 15 — Lap Positions  (new in F1 25)
    # ------------------------------------------------------------------ #
    def parse_lap_positions(self, data):
        expected_size = ctypes.sizeof(PacketLapPositionsData)
        if len(data) < expected_size:
            return {'lapPositions': '', 'error': f"Paquete demasiado corto: {len(data)} < {expected_size}"}

        packet = PacketLapPositionsData.from_buffer_copy(data)
        positions = []
        for lap_idx in range(packet.numLaps):
            positions.append(list(packet.positionForVehicleIdx[packet.lapStart + lap_idx]))
        return {
            'lapPositions': {
                'numLaps': packet.numLaps,
                'lapStart': packet.lapStart,
                'positions': positions,   # list[lap] → list[22 cars] of position (0 = no record)
            }
        }

    # ------------------------------------------------------------------ #
    # Redis
    # ------------------------------------------------------------------ #
    def save_to_redis(self, data, channel):
        if not data or not channel:
            return
        try:
            redis_client.publish(channel, data)
            print("✅ Datos guardados correctamente en Redis")
        except Exception as e:
            print(f"❌ Error al guardar datos en Redis: {e}")


if __name__ == '__main__':
    reader = F1Reader()
    for packet in reader.start():
        print(packet)
