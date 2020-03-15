import time
import datetime
import threading
import json
from lux_sensor import Tsl2591 as LightSensor
from moisture_sensor import MoistSensor as MoistureSensor
from relay_control import GPIOcontrol as RelayControl
import RPi.GPIO as GPIO
from temp_sensor import TempSensor

class Sensors(threading.Thread):
    PUMP_OUTLET = 1
    LIGHT_OUTLET = 2

    SENSOR_MEASURE_INTERVAL = 600 # seconds, 10 min

    PUMP_RUN_TIME = 10  # seconds
    PUMP_GPS = 0.0125 # Gallons per second
    FULL_WATER_BIN = 1.5 # 1 gallon

    LIGHTING_TIME = 19  # in hours
    DAYLIGHT = 1  # hours
    HOURS_OF_LIGHT_ON = (24 - LIGHTING_TIME) + DAYLIGHT

    def __init__(self):
        threading.Thread.__init__(self)
        self.__firstMoistureFail = False
        self.__wateredLastRound = False
        self.__lastMoistureMeasure = 0.0
        self.__waterTimes = []
        self.__waterLeft = None

        self.__nightLightOn = False
        self.__lastSpectrumMeasure = 0
        self.__lastIrMeasure = 0
        self.__aggregateSpectrum = 0
        self.__aggregateIr = 0
        self.__lightOnTime = 0
        self.__nightTime = 0
        self.__prevNightTime = 0

        self.__lastTempMeasure = 0 # degrees celsius

        self.__plantJson = None
        self.__plantTypeJson = None
        self.__plantName = None
        self.__plantTime = None
        self.SOIL_MOISTURE_LEVEL = None
        self.ENOUGH_SPECTRUM = None
        self.ENOUGH_IR = None

        self.__readJson()

        self.__lastLoopTime = 0
        self.__running = True

        GPIO.setwarnings(False)
        self.__light = LightSensor()
        self.__moisture = MoistureSensor()
        self.__relayControl = RelayControl()
        self.__temp = TempSensor()

    def __readJson(self):
        with open("files/plantInfo.json", "r") as json_data:
            self.__plantJson = json.load(json_data)
        plantFile = "files/plants/" + self.__plantJson["Type"] + ".json"
        self.__readPlantType(plantFile)

        self.__plantName = self.__plantJson["Name"]
        self.__waterLeft = self.__plantJson["CurrWater"]
        self.__plantTime = self.__plantJson["PlantTime"]

    def __readPlantType(self, file):
        with open(file, "r") as json_data:
            self.__plantTypeJson = json.load(json_data)

        self.SOIL_MOISTURE_LEVEL = self.__plantTypeJson["Moisture"]
        self.ENOUGH_SPECTRUM = self.__plantTypeJson["SpectrumAmount"]
        self.ENOUGH_IR = self.__plantTypeJson["IRAmount"]

    def __writeJson(self):
        with open("files/plantInfo.json", 'w') as outfile:
            json.dump(self.__plantJson, outfile)

    def resetWaterLevel(self):
        self.__waterLeft = self.FULL_WATER_BIN
        self.__plantJson["CurrWater"] = self.__waterLeft
        self.__writeJson()

    def getMoisture(self):
        return round(self.__lastMoistureMeasure * 100, 2)

    def getLight(self):
        return round(self.__light.calculate_lux(self.__lastSpectrumMeasure, self.__lastIrMeasure), 2)

    def getLengthLighting(self):
        if self.__nightLightOn:
            return self.__prevNightTime
        else:
            return self.__nightTime

    def getTemp(self):
        return round(self.__lastTempMeasure, 2)

    def getWaterLast24(self):
        elementsToRemove = []
        waterAmount = 0
        for waterTime in self.__waterTimes:
            if waterTime > time.time() - (24 * 60 * 60):
                waterAmount += self.PUMP_RUN_TIME * self.PUMP_GPS
            else:
                elementsToRemove.append(waterTime)
        for self.__waterTimes in elementsToRemove:
            self.__waterTimes.remove(waterTime)
        return waterAmount

    def getWaterLeft(self):
        return round((self.__waterLeft / self.FULL_WATER_BIN) * 100, 2)

    def getPlantName(self):
        return self.__plantJson["Name"]

    def getPlantType(self):
        return self.__plantJson["Type"]

    def newPlant(self, newName, newType):
        self.__plantJson["Name"] = newName
        self.__plantJson["Type"] = newType
        self.__plantJson["PlantTime"] = time.time() - 2 # for easy display purposes
        self.__writeJson()
        plantFile = "files/plants/" + self.__plantJson["Type"] + ".json"
        self.__readPlantType(plantFile)

    def getPlantTime(self):
        return self.__plantJson["PlantTime"]

    def stop(self):
        self.__running = False
        self.__relayControl.control(self.PUMP_OUTLET, False)  # Turn off pump
        self.__relayControl.control(self.LIGHT_OUTLET, False)  # Turn off pump

    def __watering(self):
        self.__relayControl.control(self.PUMP_OUTLET, True) # Turn on pump
        self.__waterTimes.append(time.time())
        time.sleep(self.PUMP_RUN_TIME)
        self.__relayControl.control(self.PUMP_OUTLET, False) # Turn off pump

        self.__waterLeft -= self.PUMP_RUN_TIME * self.PUMP_GPS
        self.__plantJson["CurrWater"] = self.__waterLeft
        self.__writeJson()

        elementsToRemove = []
        for waterTime in self.__waterTimes:
            if waterTime <= time.time() - (24 * 60 * 60):
                elementsToRemove.append(waterTime)
        for self.__waterTimes in elementsToRemove:
            self.__waterTimes.remove(waterTime)

    def __printSensorMeasures(self):
        print("Moisture:", self.getMoisture())
        print("Light:", self.getLight())
        print("Full Spectrum:", self.__lastSpectrumMeasure)
        print("IR:", self.__lastIrMeasure)
        print("Temp:", self.__lastTempMeasure)
        print("Water24:", self.getWaterLast24())
        print("Water Left:", self.getWaterLeft())

    def __sensorMeasurements(self):
        print("Sensors Being Measured")

        # ---- Temperature ----
        self.__lastTempMeasure = self.__temp.read_temp()

        # ---- Moisture ----
        self.__lastMoistureMeasure = self.__moisture.get_moisture()
        if self.__lastMoistureMeasure <= self.SOIL_MOISTURE_LEVEL:
            if self.__firstMoistureFail and not self.__wateredLastRound:
                self.__watering()
                self.__firstMoistureFail = False
                self.__wateredLastRound = True
            else:
                self.__firstMoistureFail = True
                self.__wateredLastRound = False
        else:
            self.__wateredLastRound = False
            self.__firstMoistureFail = False

        # ---- Lighting ---- FIXME

        currentDT = datetime.datetime.now()
        self.__lastSpectrumMeasure, self.__lastIrMeasure = self.__light.get_full_luminosity()
        if currentDT.hour >= self.DAYLIGHT and currentDT.hour < self.LIGHTING_TIME:
            if not self.__nightLightOn: # check if light was still on
                self.__nightLightOn = False
                self.__aggregateSpectrum = 0
                self.__aggregateIr = 0
                self.__nightTime = self.HOURS_OF_LIGHT_ON * 60 # hours to min
            self.__aggregateSpectrum += self.__lastSpectrumMeasure
            self.__aggregateIr += self.__lastIrMeasure
        elif self.__aggregateSpectrum < self.ENOUGH_SPECTRUM or self.__aggregateIr < self.ENOUGH_IR:
            self.__aggregateSpectrum += self.__lastSpectrumMeasure
            self.__aggregateIr += self.__lastIrMeasure

            if not self.__nightLightOn:
                self.__nightLightOn = True
                self.__prevNightTime = self.__nightTime
                self.__lightOnTime = time.time()

            if self.__aggregateSpectrum >= self.ENOUGH_SPECTRUM and self.__aggregateIr >= self.ENOUGH_IR:
                self.__nightLightOn = False

        else:
            self.__nightLightOn = False
            self.__aggregateSpectrum = 0
            self.__aggregateIr = 0
            self.__nightTime = time.time() - self.__lightOnTime / 60  # seconds to min

        # turn on and off light
        if self.__nightLightOn:
            self.__relayControl.control(self.LIGHT_OUTLET, True)
        else:
            self.__relayControl.control(self.LIGHT_OUTLET, False)

        self.__printSensorMeasures()

    def run(self):
        while self.__running:
            if self.__lastLoopTime + self.SENSOR_MEASURE_INTERVAL <= time.time():
                self.__sensorMeasurements()
                self.__lastLoopTime = time.time()
            time.sleep(5)