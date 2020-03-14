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

    PUMP_RUN_TIME = 2  # seconds
    PUMP_GPM = 0.5  # GPM
    PUMP_GPS = PUMP_GPM / 60.0  # Gallons per second
    FULL_WATER_BIN = 1 # 1 gallon

    LIGHTING_TIME = 18  # in hours
    DAYLIGHT = 7  # hours

    def __init__(self):
        threading.Thread.__init__(self)
        self.__firstMoistureFail = False
        self.__lastMoistureMeasure = 0.0
        self.__waterTimes = []
        self.__waterLeft = None

        self.__nightLightOn = False
        self.__lastLightMeasure = 0
        self.__aggregateLightTime = 0
        self.__nightTime = 0
        self.__prevNightTime = 0

        self.__lastTempMeasure = 0 # degrees celsius

        self.__plantJson = None
        self.__plantTypeJson = None
        self.__plantName = None
        self.__plantTime = None
        self.SOIL_MOISTURE_LEVEL = None
        self.ENOUGH_LIGHT_TIME = None
        self.ENOUGH_LIGHT = None

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
        self.ENOUGH_LIGHT_TIME = self.__plantTypeJson["LightTime"]
        self.ENOUGH_LIGHT = self.__plantTypeJson["LightAmount"]

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
        return self.__lastLightMeasure

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
        print("Light:", self.__lastLightMeasure)
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
            if self.__firstMoistureFail:
                self.__watering()
                self.__firstMoistureFail = False
            else:
                self.__firstMoistureFail = True
        else:
            self.__firstMoistureFail = False

        # ---- Lighting ---- FIXME
        currentDT = datetime.datetime.now()
        full, ir = self.__light.get_full_luminosity()
        self.__lastLightMeasure = full # ====light====
        if currentDT.hour >= self.DAYLIGHT and currentDT.hour < self.LIGHTING_TIME:
            if not self.__nightLightOn: # check if light was still on
                self.__nightLightOn = False
                self.__aggregateLightTime = 0
            if self.__lastLightMeasure > self.ENOUGH_LIGHT:
                self.__aggregateLightTime += self.SENSOR_MEASURE_INTERVAL / 60 # to min
        elif self.__aggregateLightTime < self.ENOUGH_LIGHT_TIME:
            if not self.__nightLightOn:
                self.__nightLightOn = True
                self.__prevNightTime = self.__nightTime
                self.__nightTime = self.ENOUGH_LIGHT_TIME - self.__aggregateLightTime
            else:
                self.__aggregateLightTime += self.SENSOR_MEASURE_INTERVAL / 60  # to min
        else:
            self.__nightLightOn = False
            self.__aggregateLightTime = 0

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