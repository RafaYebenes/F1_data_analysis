from pyspark.sql.types import *

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
])

LapData_schema = StructType([
    StructField("lastLapTimeInMS", IntegerType()),
    StructField("currentLapTimeInMS", IntegerType()),
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
    StructField("timeTrialPBCarIdx", IntegerType()),
    StructField("timeTrialRivalCarIdx", IntegerType()),
])

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
    StructField("mfdPanelIndex", IntegerType()),
    StructField("mfdPanelIndexSecondaryPlayer", IntegerType()),
    StructField("suggestedGear", IntegerType()),
])

FastestLap_schema = StructType([
    StructField("vehicleIdx", IntegerType()),
    StructField("lapTime", FloatType()),
])

Penalty_schema = StructType([
    StructField("penaltyType", IntegerType()),
    StructField("infringementType", IntegerType()),
    StructField("vehicleIdx", IntegerType()),
    StructField("otherVehicleIdx", IntegerType()),
    StructField("time", IntegerType()),
    StructField("lapNum", IntegerType()),
    StructField("placesGained", IntegerType()),
])

PacketEventData_schema = StructType([
    StructField("eventStringCode", ArrayType(StringType(), containsNull=False)),
])

ParticipantData_schema = StructType([
    StructField("aiControlled", IntegerType()),
    StructField("driverId", IntegerType()),
    StructField("networkId", IntegerType()),
    StructField("teamId", IntegerType()),
    StructField("myTeam", IntegerType()),
    StructField("raceNumber", IntegerType()),
    StructField("nationality", IntegerType()),
    StructField("name", ArrayType(StringType(), containsNull=False)),
    StructField("yourTelemetry", IntegerType()),
])

PacketParticipantsData_schema = StructType([
    StructField("numActiveCars", IntegerType()),
])

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
    StructField("rearLeftTyrePressure", FloatType()),
    StructField("rearRightTyrePressure", FloatType()),
    StructField("frontLeftTyrePressure", FloatType()),
    StructField("frontRightTyrePressure", FloatType()),
    StructField("ballast", IntegerType()),
    StructField("fuelLoad", FloatType()),
])

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

FinalClassificationData_schema = StructType([
    StructField("position", IntegerType()),
    StructField("numLaps", IntegerType()),
    StructField("gridPosition", IntegerType()),
    StructField("points", IntegerType()),
    StructField("numPitStops", IntegerType()),
    StructField("resultStatus", IntegerType()),
    StructField("bestLapTimeInMS", IntegerType()),
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
])

LobbyInfoData_schema = StructType([
    StructField("aiControlled", IntegerType()),
    StructField("teamId", IntegerType()),
    StructField("nationality", IntegerType()),
    StructField("platform", IntegerType()),
    StructField("name", ArrayType(StringType(), containsNull=False)),
    StructField("carNumber", IntegerType()),
    StructField("readyStatus", IntegerType()),
])

PacketLobbyInfoData_schema = StructType([
    StructField("numPlayers", IntegerType()),
])

CarDamageData_schema = StructType([
    StructField("tyresWear", ArrayType(IntegerType(), containsNull=False)),
    StructField("tyresDamage", ArrayType(IntegerType(), containsNull=False)),
    StructField("brakesDamage", ArrayType(IntegerType(), containsNull=False)),
    StructField("frontLeftWingDamage", IntegerType()),
    StructField("frontRightWingDamage", IntegerType()),
    StructField("rearWingDamage", IntegerType()),
    StructField("floorDamage", IntegerType()),
    StructField("diffuserDamage", IntegerType()),
    StructField("sidepodDamage", IntegerType()),
    StructField("drsFault", IntegerType()),
    StructField("gearBoxDamage", IntegerType()),
    StructField("engineDamage", IntegerType()),
    StructField("engineMGUHWear", IntegerType()),
    StructField("engineESWear", IntegerType()),
    StructField("engineCEWear", IntegerType()),
    StructField("engineICEWear", IntegerType()),
    StructField("engineMGUKWear", IntegerType()),
    StructField("engineTCWear", IntegerType()),
])

LapHistoryData_schema = StructType([
    StructField("lapTimeInMS", IntegerType()),
    StructField("sector1TimeInMS", IntegerType()),
    StructField("sector2TimeInMS", IntegerType()),
    StructField("sector3TimeInMS", IntegerType()),
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
])

TyreSetData_schema = StructType([
    StructField("actualTyreCompound", IntegerType()),
    StructField("visualTyreCompound", IntegerType()),
    StructField("wear", IntegerType()),
    StructField("available", IntegerType()),
    StructField("recommendedSession", IntegerType()),
    StructField("lifeSpan", IntegerType()),
    StructField("usableLife", IntegerType()),
    StructField("lapDeltaTime", FloatType()),
    StructField("fitted", IntegerType()),
])

PacketTyreSetsData_schema = StructType([
    StructField("carIdx", IntegerType()),
])

GForceData_schema = StructType([
    StructField("gForceLateral", FloatType()),
    StructField("gForceLongitudinal", FloatType()),
    StructField("gForceVertical", FloatType()),
])

PacketTimeTrialData_schema = StructType([
    StructField("deltaTimeInMS", IntegerType()),
])
