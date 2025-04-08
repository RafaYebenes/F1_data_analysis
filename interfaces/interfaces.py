import ctypes

# ================================ HEADER ================================
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


class CarMotionData(ctypes.LittleEndianStructure):
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
class PacketMotionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carMotionData", CarMotionData * 22)
    ]

# ================================ SESSION ================================
class MarshalZone(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("zoneStart", ctypes.c_float), ("zoneFlag", ctypes.c_int8)]

class WeatherForecastSample(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("sessionType", ctypes.c_uint8),
        ("timeOffset", ctypes.c_uint8),
        ("weather", ctypes.c_uint8),
        ("trackTemperature", ctypes.c_int8),
        ("trackTemperatureChange", ctypes.c_int8),
        ("airTemperature", ctypes.c_int8),
        ("airTemperatureChange", ctypes.c_int8),
        ("rainPercentage", ctypes.c_uint8)
    ]

class PacketSessionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
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
        ("marshalZones", MarshalZone * 21),
        ("safetyCarStatus", ctypes.c_uint8),
        ("networkGame", ctypes.c_uint8),
        ("numWeatherForecastSamples", ctypes.c_uint8),
        ("weatherForecastSamples", WeatherForecastSample * 64)
    ]

# =============================== LAP DATA ================================
class LapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("lastLapTimeInMS", ctypes.c_uint32),
        ("currentLapTimeInMS", ctypes.c_uint32),
        ("sector1TimeMSPart", ctypes.c_uint16),
        ("sector1TimeMinutesPart", ctypes.c_uint8),
        ("sector2TimeMSPart", ctypes.c_uint16),
        ("sector2TimeMinutesPart", ctypes.c_uint8),
        ("deltaToCarInFrontMSPart", ctypes.c_uint16),
        ("deltaToCarInFrontMinutesPart", ctypes.c_uint8),
        ("deltaToRaceLeaderMSPart", ctypes.c_uint16),
        ("deltaToRaceLeaderMinutesPart", ctypes.c_uint8),
        ("lapDistance", ctypes.c_float),
        ("totalDistance", ctypes.c_float),
        ("safetyCarDelta", ctypes.c_float),
        ("carPosition", ctypes.c_uint8),
        ("currentLapNum", ctypes.c_uint8),
        ("pitStatus", ctypes.c_uint8),
        ("numPitStops", ctypes.c_uint8),
        ("sector", ctypes.c_uint8),
        ("currentLapInvalid", ctypes.c_uint8),
        ("penalties", ctypes.c_uint8),
        ("totalWarnings", ctypes.c_uint8),
        ("cornerCuttingWarnings", ctypes.c_uint8),
        ("numUnservedDriveThroughPens", ctypes.c_uint8),
        ("numUnservedStopGoPens", ctypes.c_uint8),
        ("gridPosition", ctypes.c_uint8),
        ("driverStatus", ctypes.c_uint8),
        ("resultStatus", ctypes.c_uint8),
        ("pitLaneTimerActive", ctypes.c_uint8),
        ("pitLaneTimeInLaneInMS", ctypes.c_uint16),
        ("pitStopTimerInMS", ctypes.c_uint16),
        ("pitStopShouldServePen", ctypes.c_uint8),
        ("speedTrapFastestSpeed", ctypes.c_float),
        ("speedTrapFastestLap", ctypes.c_uint8)
    ]

class PacketLapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("lapData", LapData * 22),
        ("timeTrialPBCarIdx", ctypes.c_uint8),
        ("timeTrialRivalCarIdx", ctypes.c_uint8)
    ]


class CarTelemetryData(ctypes.LittleEndianStructure):
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
        ("revLightsBitValue", ctypes.c_uint16),
        ("brakesTemperature", ctypes.c_uint16 * 4),
        ("tyresSurfaceTemperature", ctypes.c_uint8 * 4),
        ("tyresInnerTemperature", ctypes.c_uint8 * 4),
        ("engineTemperature", ctypes.c_uint16),
        ("tyresPressure", ctypes.c_float * 4),
        ("surfaceType", ctypes.c_uint8 * 4)
    ]

class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carTelemetryData", CarTelemetryData * 22),
        ("mfdPanelIndex", ctypes.c_uint8),
        ("mfdPanelIndexSecondaryPlayer", ctypes.c_uint8),
        ("suggestedGear", ctypes.c_int8)
    ]


# =============================== EVENT DATA ===============================
class FastestLap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
        ("lapTime", ctypes.c_float)
    ]

class Retirement(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]

class TeamMateInPits(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]

class RaceWinner(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]

class Penalty(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("penaltyType", ctypes.c_uint8),
        ("infringementType", ctypes.c_uint8),
        ("vehicleIdx", ctypes.c_uint8),
        ("otherVehicleIdx", ctypes.c_uint8),
        ("time", ctypes.c_uint8),
        ("lapNum", ctypes.c_uint8),
        ("placesGained", ctypes.c_uint8)
    ]

class SpeedTrap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
        ("speed", ctypes.c_float),
        ("isOverallFastestInSession", ctypes.c_uint8),
        ("isDriverFastestInSession", ctypes.c_uint8),
        ("fastestVehicleIdxInSession", ctypes.c_uint8),
        ("fastestSpeedInSession", ctypes.c_float)
    ]

class EventDataDetails(ctypes.Union):
    _fields_ = [
        ("fastestLap", FastestLap),
        ("retirement", Retirement),
        ("teamMateInPits", TeamMateInPits),
        ("raceWinner", RaceWinner),
        ("penalty", Penalty),
        ("speedTrap", SpeedTrap)
    ]

class PacketEventData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("eventStringCode", ctypes.c_char * 4),
        ("eventDetails", EventDataDetails)
    ]

# ============================== PARTICIPANTS ==============================
class ParticipantData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("aiControlled", ctypes.c_uint8),
        ("driverId", ctypes.c_uint8),
        ("networkId", ctypes.c_uint8),
        ("teamId", ctypes.c_uint8),
        ("myTeam", ctypes.c_uint8),
        ("raceNumber", ctypes.c_uint8),
        ("nationality", ctypes.c_uint8),
        ("name", ctypes.c_char * 48),
        ("yourTelemetry", ctypes.c_uint8)
    ]

class PacketParticipantsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("numActiveCars", ctypes.c_uint8),
        ("participants", ParticipantData * 22)
    ]

class CarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("frontWing", ctypes.c_uint8),
        ("rearWing", ctypes.c_uint8),
        ("onThrottle", ctypes.c_uint8),
        ("offThrottle", ctypes.c_uint8),
        ("frontCamber", ctypes.c_float),
        ("rearCamber", ctypes.c_float),
        ("frontToe", ctypes.c_float),
        ("rearToe", ctypes.c_float),
        ("frontSuspension", ctypes.c_uint8),
        ("rearSuspension", ctypes.c_uint8),
        ("frontAntiRollBar", ctypes.c_uint8),
        ("rearAntiRollBar", ctypes.c_uint8),
        ("frontSuspensionHeight", ctypes.c_uint8),
        ("rearSuspensionHeight", ctypes.c_uint8),
        ("brakePressure", ctypes.c_uint8),
        ("brakeBias", ctypes.c_uint8),
        ("rearLeftTyrePressure", ctypes.c_float),
        ("rearRightTyrePressure", ctypes.c_float),
        ("frontLeftTyrePressure", ctypes.c_float),
        ("frontRightTyrePressure", ctypes.c_float),
        ("ballast", ctypes.c_uint8),
        ("fuelLoad", ctypes.c_float)
    ]

class PacketCarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carSetups", CarSetupData * 22)
    ]

class CarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("tractionControl", ctypes.c_uint8),
        ("antiLockBrakes", ctypes.c_uint8),
        ("fuelMix", ctypes.c_uint8),
        ("frontBrakeBias", ctypes.c_uint8),
        ("pitLimiterStatus", ctypes.c_uint8),
        ("fuelInTank", ctypes.c_float),
        ("fuelCapacity", ctypes.c_float),
        ("fuelRemainingLaps", ctypes.c_float),
        ("maxRPM", ctypes.c_uint16),
        ("idleRPM", ctypes.c_uint16),
        ("maxGears", ctypes.c_uint8),
        ("drsAllowed", ctypes.c_uint8),
        ("drsActivationDistance", ctypes.c_uint16),
        ("actualTyreCompound", ctypes.c_uint8),
        ("visualTyreCompound", ctypes.c_uint8),
        ("tyresAgeLaps", ctypes.c_uint8),
        ("vehicleFiaFlags", ctypes.c_int8),
        ("enginePowerICE", ctypes.c_float),
        ("enginePowerMGUK", ctypes.c_float),
        ("ersStoreEnergy", ctypes.c_float),
        ("ersDeployMode", ctypes.c_uint8),
        ("ersHarvestedThisLapMGUK", ctypes.c_float),
        ("ersHarvestedThisLapMGUH", ctypes.c_float),
        ("ersDeployedThisLap", ctypes.c_float),
        ("networkPaused", ctypes.c_uint8)
    ]

class PacketCarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carStatusData", CarStatusData * 22)
    ]


class FinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("position", ctypes.c_uint8),
        ("numLaps", ctypes.c_uint8),
        ("gridPosition", ctypes.c_uint8),
        ("points", ctypes.c_uint8),
        ("numPitStops", ctypes.c_uint8),
        ("resultStatus", ctypes.c_uint8),
        ("bestLapTimeInMS", ctypes.c_uint32),
        ("totalRaceTime", ctypes.c_double),
        ("penaltiesTime", ctypes.c_uint8),
        ("numPenalties", ctypes.c_uint8),
        ("numTyreStints", ctypes.c_uint8),
        ("tyreStintsActual", ctypes.c_uint8 * 8),
        ("tyreStintsVisual", ctypes.c_uint8 * 8),
        ("tyreStintsEndLaps", ctypes.c_uint8 * 8)
    ]

class PacketFinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("numCars", ctypes.c_uint8),
        ("classificationData", FinalClassificationData * 22)
    ]


class LobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("aiControlled", ctypes.c_uint8),
        ("teamId", ctypes.c_uint8),
        ("nationality", ctypes.c_uint8),
        ("platform", ctypes.c_uint8),
        ("name", ctypes.c_char * 48),
        ("carNumber", ctypes.c_uint8),
        ("readyStatus", ctypes.c_uint8)
    ]


class PacketLobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("numPlayers", ctypes.c_uint8),
        ("lobbyPlayers", LobbyInfoData * 22)
    ]


class CarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("tyresWear", ctypes.c_uint8 * 4),
        ("tyresDamage", ctypes.c_uint8 * 4),
        ("brakesDamage", ctypes.c_uint8 * 4),
        ("frontLeftWingDamage", ctypes.c_uint8),
        ("frontRightWingDamage", ctypes.c_uint8),
        ("rearWingDamage", ctypes.c_uint8),
        ("floorDamage", ctypes.c_uint8),
        ("diffuserDamage", ctypes.c_uint8),
        ("sidepodDamage", ctypes.c_uint8),
        ("drsFault", ctypes.c_uint8),
        ("gearBoxDamage", ctypes.c_uint8),
        ("engineDamage", ctypes.c_uint8),
        ("engineMGUHWear", ctypes.c_uint8),
        ("engineESWear", ctypes.c_uint8),
        ("engineCEWear", ctypes.c_uint8),
        ("engineICEWear", ctypes.c_uint8),
        ("engineMGUKWear", ctypes.c_uint8),
        ("engineTCWear", ctypes.c_uint8)
    ]


class PacketCarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carDamageData", CarDamageData * 22)
    ]


class LapHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("lapTimeInMS", ctypes.c_uint32),
        ("sector1TimeInMS", ctypes.c_uint16),
        ("sector2TimeInMS", ctypes.c_uint16),
        ("sector3TimeInMS", ctypes.c_uint16),
        ("lapValidBitFlags", ctypes.c_uint8)
    ]


class TyreStintHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("endLap", ctypes.c_uint8),
        ("tyreActualCompound", ctypes.c_uint8),
        ("tyreVisualCompound", ctypes.c_uint8)
    ]


class PacketSessionHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carIdx", ctypes.c_uint8),
        ("numLaps", ctypes.c_uint8),
        ("numTyreStints", ctypes.c_uint8),
        ("bestLapTimeLapNum", ctypes.c_uint8),
        ("bestSector1LapNum", ctypes.c_uint8),
        ("bestSector2LapNum", ctypes.c_uint8),
        ("bestSector3LapNum", ctypes.c_uint8),
        ("lapHistoryData", LapHistoryData * 100),
        ("tyreStintsHistoryData", TyreStintHistoryData * 8)
    ]


class TyreSetData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("actualTyreCompound", ctypes.c_uint8),
        ("visualTyreCompound", ctypes.c_uint8),
        ("wear", ctypes.c_uint8),
        ("available", ctypes.c_uint8),
        ("recommendedSession", ctypes.c_uint8),
        ("lifeSpan", ctypes.c_uint8),
        ("usableLife", ctypes.c_uint8),
        ("lapDeltaTime", ctypes.c_float),
        ("fitted", ctypes.c_uint8)
    ]


class PacketTyreSetsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("carIdx", ctypes.c_uint8),
        ("tyreSetData", TyreSetData * 20)
    ]


class GForceData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("gForceLateral", ctypes.c_float),
        ("gForceLongitudinal", ctypes.c_float),
        ("gForceVertical", ctypes.c_float)
    ]


class PacketTimeTrialData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", PacketHeader),
        ("deltaTimeInMS", ctypes.c_int32)
    ]




