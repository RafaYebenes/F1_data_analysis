"""
PySpark schema definitions for F1 25 UDP packets.
Used for batch analytics pipelines; not part of the live telemetry flow.
Array fields use order: RL, RR, FL, FR (wheels) unless otherwise noted.
"""

from pyspark.sql.types import (
    ArrayType, BinaryType, BooleanType, DoubleType, FloatType,
    IntegerType, LongType, ShortType, StringType, StructField, StructType,
)

# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

PacketHeader_schema = StructType([
    StructField("packetFormat", IntegerType()),
    StructField("gameYear", IntegerType()),
    StructField("gameMajorVersion", IntegerType()),
    StructField("gameMinorVersion", IntegerType()),
    StructField("packetVersion", IntegerType()),
    StructField("packetId", IntegerType()),
    StructField("sessionUID", LongType()),
    StructField("sessionTime", FloatType()),
    StructField("frameIdentifier", IntegerType()),
    StructField("overallFrameIdentifier", IntegerType()),
    StructField("playerCarIndex", IntegerType()),
    StructField("secondaryPlayerCarIndex", IntegerType()),
])

# ---------------------------------------------------------------------------
# ID 0 — Motion
# ---------------------------------------------------------------------------

CarMotionData_schema = StructType([
    StructField("worldPositionX", FloatType()),
    StructField("worldPositionY", FloatType()),
    StructField("worldPositionZ", FloatType()),
    StructField("worldVelocityX", FloatType()),
    StructField("worldVelocityY", FloatType()),
    StructField("worldVelocityZ", FloatType()),
    StructField("worldForwardDirX", IntegerType()),
    StructField("worldForwardDirY", IntegerType()),
    StructField("worldForwardDirZ", IntegerType()),
    StructField("worldRightDirX", IntegerType()),
    StructField("worldRightDirY", IntegerType()),
    StructField("worldRightDirZ", IntegerType()),
    StructField("gForceLateral", FloatType()),
    StructField("gForceLongitudinal", FloatType()),
    StructField("gForceVertical", FloatType()),
    StructField("yaw", FloatType()),
    StructField("pitch", FloatType()),
    StructField("roll", FloatType()),
])

PacketMotionData_schema = StructType([
    StructField("motion", ArrayType(CarMotionData_schema)),
])

# ---------------------------------------------------------------------------
# ID 1 — Session
# ---------------------------------------------------------------------------

WeatherForecastSample_schema = StructType([
    StructField("sessionType", IntegerType()),
    StructField("timeOffset", IntegerType()),
    StructField("weather", IntegerType()),
    StructField("trackTemperature", IntegerType()),
    StructField("trackTemperatureChange", IntegerType()),
    StructField("airTemperature", IntegerType()),
    StructField("airTemperatureChange", IntegerType()),
    StructField("rainPercentage", IntegerType()),
])

PacketSessionData_schema = StructType([
    StructField("weather", IntegerType()),
    StructField("trackTemperature", IntegerType()),
    StructField("airTemperature", IntegerType()),
    StructField("totalLaps", IntegerType()),
    StructField("trackLength", IntegerType()),
    StructField("sessionType", IntegerType()),
    StructField("trackId", IntegerType()),
    StructField("formula", IntegerType()),
    StructField("sessionTimeLeft", IntegerType()),
    StructField("sessionDuration", IntegerType()),
    StructField("pitSpeedLimit", IntegerType()),
    StructField("gamePaused", IntegerType()),
    StructField("isSpectating", IntegerType()),
    StructField("spectatorCarIndex", IntegerType()),
    StructField("sliProNativeSupport", IntegerType()),
    StructField("numMarshalZones", IntegerType()),
    StructField("safetyCarStatus", IntegerType()),
    StructField("networkGame", IntegerType()),
    StructField("numWeatherForecastSamples", IntegerType()),
    StructField("weatherForecastSamples", ArrayType(WeatherForecastSample_schema)),
    # F1 24/25 additions
    StructField("forecastAccuracy", IntegerType()),
    StructField("aiDifficulty", IntegerType()),
    StructField("seasonLinkIdentifier", LongType()),
    StructField("weekendLinkIdentifier", LongType()),
    StructField("sessionLinkIdentifier", LongType()),
    StructField("pitStopWindowIdealLap", IntegerType()),
    StructField("pitStopWindowLatestLap", IntegerType()),
    StructField("pitStopRejoinPosition", IntegerType()),
    StructField("steeringAssist", IntegerType()),
    StructField("brakingAssist", IntegerType()),
    StructField("gearboxAssist", IntegerType()),
    StructField("pitAssist", IntegerType()),
    StructField("pitReleaseAssist", IntegerType()),
    StructField("ersAssist", IntegerType()),
    StructField("drsAssist", IntegerType()),
    StructField("dynamicRacingLine", IntegerType()),
    StructField("dynamicRacingLineType", IntegerType()),
    StructField("gameMode", IntegerType()),
    StructField("ruleSet", IntegerType()),
    StructField("timeOfDay", LongType()),
    StructField("sessionLength", IntegerType()),
    StructField("speedUnitsLeadPlayer", IntegerType()),
    StructField("temperatureUnitsLeadPlayer", IntegerType()),
    StructField("speedUnitsSecondaryPlayer", IntegerType()),
    StructField("temperatureUnitsSecondaryPlayer", IntegerType()),
    StructField("numSafetyCarPeriods", IntegerType()),
    StructField("numVirtualSafetyCarPeriods", IntegerType()),
    StructField("numRedFlagPeriods", IntegerType()),
    StructField("equalCarPerformance", IntegerType()),
    StructField("recoveryMode", IntegerType()),
    StructField("flashbackLimit", IntegerType()),
    StructField("surfaceType", IntegerType()),
    StructField("lowFuelMode", IntegerType()),
    StructField("raceStarts", IntegerType()),
    StructField("tyreTemperature", IntegerType()),
    StructField("pitLaneTyreSim", IntegerType()),
    StructField("carDamageSetting", IntegerType()),
    StructField("carDamageRate", IntegerType()),
    StructField("collisions", IntegerType()),
    StructField("collisionsOffForFirstLapOnly", IntegerType()),
    StructField("mpUnsafePitRelease", IntegerType()),
    StructField("mpOffForGriefing", IntegerType()),
    StructField("cornerCuttingStringency", IntegerType()),
    StructField("parcFermeRules", IntegerType()),
    StructField("pitStopExperience", IntegerType()),
    StructField("safetyCar", IntegerType()),
    StructField("safetyCarExperience", IntegerType()),
    StructField("formationLap", IntegerType()),
    StructField("formationLapExperience", IntegerType()),
    StructField("redFlags", IntegerType()),
    StructField("affectsLicenceLevelSolo", IntegerType()),
    StructField("affectsLicenceLevelMP", IntegerType()),
    StructField("numSessionsInWeekend", IntegerType()),
    StructField("weekendStructure", ArrayType(IntegerType())),
    StructField("sector2LapDistanceStart", FloatType()),
    StructField("sector3LapDistanceStart", FloatType()),
])

# ---------------------------------------------------------------------------
# ID 2 — Lap Data
# ---------------------------------------------------------------------------

LapData_schema = StructType([
    StructField("lastLapTimeInMS", LongType()),
    StructField("currentLapTimeInMS", LongType()),
    StructField("sector1TimeMSPart", IntegerType()),
    StructField("sector1TimeMinutesPart", IntegerType()),
    StructField("sector2TimeMSPart", IntegerType()),
    StructField("sector2TimeMinutesPart", IntegerType()),
    StructField("deltaToCarInFrontMSPart", IntegerType()),
    StructField("deltaToCarInFrontMinutesPart", IntegerType()),
    StructField("deltaToRaceLeaderMSPart", IntegerType()),
    StructField("deltaToRaceLeaderMinutesPart", IntegerType()),
    StructField("lapDistance", FloatType()),
    StructField("totalDistance", FloatType()),
    StructField("safetyCarDelta", FloatType()),
    StructField("carPosition", IntegerType()),
    StructField("currentLapNum", IntegerType()),
    StructField("pitStatus", IntegerType()),
    StructField("numPitStops", IntegerType()),
    StructField("sector", IntegerType()),
    StructField("currentLapInvalid", IntegerType()),
    StructField("penalties", IntegerType()),
    StructField("totalWarnings", IntegerType()),
    StructField("cornerCuttingWarnings", IntegerType()),
    StructField("numUnservedDriveThroughPens", IntegerType()),
    StructField("numUnservedStopGoPens", IntegerType()),
    StructField("gridPosition", IntegerType()),
    StructField("driverStatus", IntegerType()),
    StructField("resultStatus", IntegerType()),
    StructField("pitLaneTimerActive", IntegerType()),
    StructField("pitLaneTimeInLaneInMS", IntegerType()),
    StructField("pitStopTimerInMS", IntegerType()),
    StructField("pitStopShouldServePen", IntegerType()),
    StructField("speedTrapFastestSpeed", FloatType()),
    StructField("speedTrapFastestLap", IntegerType()),
])

PacketLapData_schema = StructType([
    StructField("lapData", ArrayType(LapData_schema)),
    StructField("pbCarIdx", IntegerType()),
    StructField("rivalCarIdx", IntegerType()),
])

# ---------------------------------------------------------------------------
# ID 3 — Event
# ---------------------------------------------------------------------------

PacketEventData_schema = StructType([
    StructField("eventStringCode", StringType()),
    StructField("vehicleIdx", IntegerType()),
    StructField("lapTime", FloatType()),
    StructField("speed", FloatType()),
    StructField("reason", IntegerType()),
    StructField("penaltyType", IntegerType()),
    StructField("infringementType", IntegerType()),
    StructField("otherVehicleIdx", IntegerType()),
    StructField("time", IntegerType()),
    StructField("lapNum", IntegerType()),
    StructField("placesGained", IntegerType()),
    StructField("isOverallFastestInSession", IntegerType()),
    StructField("isDriverFastestInSession", IntegerType()),
    StructField("fastestVehicleIdxInSession", IntegerType()),
    StructField("fastestSpeedInSession", FloatType()),
    StructField("numLights", IntegerType()),
    StructField("stopTime", FloatType()),
    StructField("flashbackFrameIdentifier", LongType()),
    StructField("flashbackSessionTime", FloatType()),
    StructField("buttonStatus", LongType()),
    StructField("overtakingVehicleIdx", IntegerType()),
    StructField("beingOvertakenVehicleIdx", IntegerType()),
    StructField("safetyCarType", IntegerType()),
    StructField("eventType", IntegerType()),
    StructField("vehicle1Idx", IntegerType()),
    StructField("vehicle2Idx", IntegerType()),
])

# ---------------------------------------------------------------------------
# ID 4 — Participants
# ---------------------------------------------------------------------------

LiveryColour_schema = StructType([
    StructField("r", IntegerType()),
    StructField("g", IntegerType()),
    StructField("b", IntegerType()),
])

ParticipantData_schema = StructType([
    StructField("aiControlled", IntegerType()),
    StructField("driverId", IntegerType()),
    StructField("networkId", IntegerType()),
    StructField("teamId", IntegerType()),
    StructField("myTeam", IntegerType()),
    StructField("raceNumber", IntegerType()),
    StructField("nationality", IntegerType()),
    StructField("name", StringType()),
    StructField("yourTelemetry", IntegerType()),
    StructField("showOnlineNames", IntegerType()),
    StructField("techLevel", IntegerType()),
    StructField("platform", IntegerType()),
    StructField("liveryColours", ArrayType(LiveryColour_schema)),
])

PacketParticipantsData_schema = StructType([
    StructField("numActiveCars", IntegerType()),
    StructField("participants", ArrayType(ParticipantData_schema)),
])

# ---------------------------------------------------------------------------
# ID 5 — Car Setups
# ---------------------------------------------------------------------------

CarSetupData_schema = StructType([
    StructField("frontWing", IntegerType()),
    StructField("rearWing", IntegerType()),
    StructField("onThrottle", IntegerType()),
    StructField("offThrottle", IntegerType()),
    StructField("frontCamber", FloatType()),
    StructField("rearCamber", FloatType()),
    StructField("frontToe", FloatType()),
    StructField("rearToe", FloatType()),
    StructField("frontSuspension", IntegerType()),
    StructField("rearSuspension", IntegerType()),
    StructField("frontAntiRollBar", IntegerType()),
    StructField("rearAntiRollBar", IntegerType()),
    StructField("frontSuspensionHeight", IntegerType()),
    StructField("rearSuspensionHeight", IntegerType()),
    StructField("brakePressure", IntegerType()),
    StructField("brakeBias", IntegerType()),
    StructField("engineBraking", IntegerType()),
    StructField("rearLeftTyrePressure", FloatType()),
    StructField("rearRightTyrePressure", FloatType()),
    StructField("frontLeftTyrePressure", FloatType()),
    StructField("frontRightTyrePressure", FloatType()),
    StructField("ballast", IntegerType()),
    StructField("fuelLoad", FloatType()),
])

PacketCarSetupData_schema = StructType([
    StructField("carSetups", ArrayType(CarSetupData_schema)),
    StructField("nextFrontWingValue", FloatType()),
])

# ---------------------------------------------------------------------------
# ID 6 — Car Telemetry
# ---------------------------------------------------------------------------

CarTelemetryData_schema = StructType([
    StructField("speed", IntegerType()),
    StructField("throttle", FloatType()),
    StructField("steer", FloatType()),
    StructField("brake", FloatType()),
    StructField("clutch", IntegerType()),
    StructField("gear", IntegerType()),
    StructField("engineRPM", IntegerType()),
    StructField("drs", IntegerType()),
    StructField("revLightsPercent", IntegerType()),
    StructField("revLightsBitValue", IntegerType()),
    StructField("brakesTemperature", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyresSurfaceTemperature", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyresInnerTemperature", ArrayType(IntegerType(), containsNull=False)),
    StructField("engineTemperature", IntegerType()),
    StructField("tyresPressure", ArrayType(FloatType(), containsNull=False)),
    StructField("surfaceType", ArrayType(IntegerType(), containsNull=False)),
])

PacketCarTelemetryData_schema = StructType([
    StructField("carTelemetry", ArrayType(CarTelemetryData_schema)),
    StructField("mfdPanelIndex", IntegerType()),
    StructField("mfdPanelIndexSecondaryPlayer", IntegerType()),
    StructField("suggestedGear", IntegerType()),
])

# ---------------------------------------------------------------------------
# ID 7 — Car Status
# ---------------------------------------------------------------------------

CarStatusData_schema = StructType([
    StructField("tractionControl", IntegerType()),
    StructField("antiLockBrakes", IntegerType()),
    StructField("fuelMix", IntegerType()),
    StructField("frontBrakeBias", IntegerType()),
    StructField("pitLimiterStatus", IntegerType()),
    StructField("fuelInTank", FloatType()),
    StructField("fuelCapacity", FloatType()),
    StructField("fuelRemainingLaps", FloatType()),
    StructField("maxRPM", IntegerType()),
    StructField("idleRPM", IntegerType()),
    StructField("maxGears", IntegerType()),
    StructField("drsAllowed", IntegerType()),
    StructField("drsActivationDistance", IntegerType()),
    StructField("actualTyreCompound", IntegerType()),
    StructField("visualTyreCompound", IntegerType()),
    StructField("tyresAgeLaps", IntegerType()),
    StructField("vehicleFiaFlags", IntegerType()),
    StructField("enginePowerICE", FloatType()),
    StructField("enginePowerMGUK", FloatType()),
    StructField("ersStoreEnergy", FloatType()),
    StructField("ersDeployMode", IntegerType()),
    StructField("ersHarvestedThisLapMGUK", FloatType()),
    StructField("ersHarvestedThisLapMGUH", FloatType()),
    StructField("ersDeployedThisLap", FloatType()),
    StructField("networkPaused", IntegerType()),
])

PacketCarStatusData_schema = StructType([
    StructField("carStatus", ArrayType(CarStatusData_schema)),
])

# ---------------------------------------------------------------------------
# ID 8 — Final Classification
# ---------------------------------------------------------------------------

FinalClassificationData_schema = StructType([
    StructField("position", IntegerType()),
    StructField("numLaps", IntegerType()),
    StructField("gridPosition", IntegerType()),
    StructField("points", IntegerType()),
    StructField("numPitStops", IntegerType()),
    StructField("resultStatus", IntegerType()),
    StructField("resultReason", IntegerType()),
    StructField("bestLapTimeInMS", LongType()),
    StructField("totalRaceTime", DoubleType()),
    StructField("penaltiesTime", IntegerType()),
    StructField("numPenalties", IntegerType()),
    StructField("numTyreStints", IntegerType()),
    StructField("tyreStintsActual", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyreStintsVisual", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyreStintsEndLaps", ArrayType(IntegerType(), containsNull=False)),
])

PacketFinalClassificationData_schema = StructType([
    StructField("numCars", IntegerType()),
    StructField("finalClassification", ArrayType(FinalClassificationData_schema)),
])

# ---------------------------------------------------------------------------
# ID 9 — Lobby Info
# ---------------------------------------------------------------------------

LobbyInfoData_schema = StructType([
    StructField("aiControlled", IntegerType()),
    StructField("teamId", IntegerType()),
    StructField("nationality", IntegerType()),
    StructField("platform", IntegerType()),
    StructField("name", StringType()),
    StructField("carNumber", IntegerType()),
    StructField("yourTelemetry", IntegerType()),
    StructField("showOnlineNames", IntegerType()),
    StructField("techLevel", IntegerType()),
    StructField("readyStatus", IntegerType()),
])

PacketLobbyInfoData_schema = StructType([
    StructField("numPlayers", IntegerType()),
    StructField("lobbyPlayers", ArrayType(LobbyInfoData_schema)),
])

# ---------------------------------------------------------------------------
# ID 10 — Car Damage
# ---------------------------------------------------------------------------

CarDamageData_schema = StructType([
    StructField("tyresWear", ArrayType(FloatType(), containsNull=False)),    # float in F1 24/25
    StructField("tyresDamage", ArrayType(IntegerType(), containsNull=False)),
    StructField("brakesDamage", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyreBlisters", ArrayType(IntegerType(), containsNull=False)),
    StructField("frontLeftWingDamage", IntegerType()),
    StructField("frontRightWingDamage", IntegerType()),
    StructField("rearWingDamage", IntegerType()),
    StructField("floorDamage", IntegerType()),
    StructField("diffuserDamage", IntegerType()),
    StructField("sidepodDamage", IntegerType()),
    StructField("drsFault", IntegerType()),
    StructField("ersFault", IntegerType()),
    StructField("gearBoxDamage", IntegerType()),
    StructField("engineDamage", IntegerType()),
    StructField("engineMGUHWear", IntegerType()),
    StructField("engineESWear", IntegerType()),
    StructField("engineCEWear", IntegerType()),
    StructField("engineICEWear", IntegerType()),
    StructField("engineMGUKWear", IntegerType()),
    StructField("engineTCWear", IntegerType()),
    StructField("engineBlown", IntegerType()),
    StructField("engineSeized", IntegerType()),
])

PacketCarDamageData_schema = StructType([
    StructField("carDamage", ArrayType(CarDamageData_schema)),
])

# ---------------------------------------------------------------------------
# ID 11 — Session History
# ---------------------------------------------------------------------------

LapHistoryData_schema = StructType([
    StructField("lapTimeInMS", LongType()),
    StructField("sector1TimeMSPart", IntegerType()),
    StructField("sector1TimeMinutesPart", IntegerType()),
    StructField("sector2TimeMSPart", IntegerType()),
    StructField("sector2TimeMinutesPart", IntegerType()),
    StructField("sector3TimeMSPart", IntegerType()),
    StructField("sector3TimeMinutesPart", IntegerType()),
    StructField("lapValidBitFlags", IntegerType()),
])

TyreStintHistoryData_schema = StructType([
    StructField("endLap", IntegerType()),
    StructField("tyreActualCompound", IntegerType()),
    StructField("tyreVisualCompound", IntegerType()),
])

PacketSessionHistoryData_schema = StructType([
    StructField("carIdx", IntegerType()),
    StructField("numLaps", IntegerType()),
    StructField("numTyreStints", IntegerType()),
    StructField("bestLapTimeLapNum", IntegerType()),
    StructField("bestSector1LapNum", IntegerType()),
    StructField("bestSector2LapNum", IntegerType()),
    StructField("bestSector3LapNum", IntegerType()),
    StructField("lapHistoryData", ArrayType(LapHistoryData_schema)),
    StructField("tyreStintsHistoryData", ArrayType(TyreStintHistoryData_schema)),
])

# ---------------------------------------------------------------------------
# ID 12 — Tyre Sets
# ---------------------------------------------------------------------------

TyreSetData_schema = StructType([
    StructField("actualTyreCompound", IntegerType()),
    StructField("visualTyreCompound", IntegerType()),
    StructField("wear", IntegerType()),
    StructField("available", IntegerType()),
    StructField("recommendedSession", IntegerType()),
    StructField("lifeSpan", IntegerType()),
    StructField("usableLife", IntegerType()),
    StructField("lapDeltaTime", ShortType()),    # int16 ms in F1 24/25
    StructField("fitted", IntegerType()),
])

PacketTyreSetsData_schema = StructType([
    StructField("carIdx", IntegerType()),
    StructField("tyreSets", ArrayType(TyreSetData_schema)),
    StructField("fittedIdx", IntegerType()),
])

# ---------------------------------------------------------------------------
# ID 13 — Motion Ex  (new in F1 24/25, player car only)
# ---------------------------------------------------------------------------

PacketMotionExData_schema = StructType([
    StructField("suspensionPosition", ArrayType(FloatType(), containsNull=False)),
    StructField("suspensionVelocity", ArrayType(FloatType(), containsNull=False)),
    StructField("suspensionAcceleration", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelSpeed", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelSlipRatio", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelSlipAngle", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelLatForce", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelLongForce", ArrayType(FloatType(), containsNull=False)),
    StructField("heightOfCOGAboveGround", FloatType()),
    StructField("localVelocity", ArrayType(FloatType(), containsNull=False)),
    StructField("angularVelocity", ArrayType(FloatType(), containsNull=False)),
    StructField("angularAcceleration", ArrayType(FloatType(), containsNull=False)),
    StructField("frontWheelsAngle", FloatType()),
    StructField("wheelVertForce", ArrayType(FloatType(), containsNull=False)),
    StructField("frontAeroHeight", FloatType()),
    StructField("rearAeroHeight", FloatType()),
    StructField("frontRollAngle", FloatType()),
    StructField("rearRollAngle", FloatType()),
    StructField("chassisYaw", FloatType()),
    StructField("chassisPitch", FloatType()),
    StructField("wheelCamber", ArrayType(FloatType(), containsNull=False)),
    StructField("wheelCamberGain", ArrayType(FloatType(), containsNull=False)),
])

# ---------------------------------------------------------------------------
# ID 14 — Time Trial
# ---------------------------------------------------------------------------

TimeTrialDataSet_schema = StructType([
    StructField("carIdx", IntegerType()),
    StructField("teamId", IntegerType()),
    StructField("lapTimeInMS", LongType()),
    StructField("sector1TimeInMS", LongType()),
    StructField("sector2TimeInMS", LongType()),
    StructField("sector3TimeInMS", LongType()),
    StructField("tractionControl", IntegerType()),
    StructField("gearboxAssist", IntegerType()),
    StructField("antiLockBrakes", IntegerType()),
    StructField("equalCarPerformance", IntegerType()),
    StructField("customSetup", IntegerType()),
    StructField("valid", IntegerType()),
])

PacketTimeTrialData_schema = StructType([
    StructField("playerSessionBest", TimeTrialDataSet_schema),
    StructField("personalBest", TimeTrialDataSet_schema),
    StructField("rival", TimeTrialDataSet_schema),
])

# ---------------------------------------------------------------------------
# ID 15 — Lap Positions  (new in F1 25)
# ---------------------------------------------------------------------------

PacketLapPositionsData_schema = StructType([
    StructField("numLaps", IntegerType()),
    StructField("lapStart", IntegerType()),
    # positions[lap_idx] → list of 22 car positions (0 = no record)
    StructField("positions", ArrayType(ArrayType(IntegerType(), containsNull=False))),
])
