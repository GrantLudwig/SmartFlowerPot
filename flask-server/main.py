from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
import json
import time
from sensorLoop import Sensors

WATERING_DURATION = 10 # seconds
PUMP_GPM = 1 # GPM
PUMP_GPS = PUMP_GPM / 60.0 # Gallons per second
lightNightOn = 0
lightNightOff = 0
lastLightTime = 0

app = Flask("__main__")
CORS(app)

# setup sensor measurements
sensors = Sensors()
sensors.start()

@app.route("/")
def my_index():
    return render_template("index.html", flask_token="Hello world")

@app.route("/back/moisture", methods=['GET'])
def moisture_level():
    global sensors

    level = sensors.getMoisture() # get moisture level
    response = json.dumps({"moisture": level})
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/light", methods=['GET'])
def light_level():
    global sensors

    level = sensors.getLight() # get light amount
    response = json.dumps({"light": level})
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/light24", methods=['GET'])
def light_on_24():
    global sensors

    lastLightTime = sensors.getLengthLighting()
    response = json.dumps({"time": lastLightTime}) # in min
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/water24", methods=['GET'])
def amount_water_24():
    global sensors

    waterAmount = sensors.getWaterLast24()
    response = json.dumps({"water": waterAmount}) # in gallons
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/waterLeft", methods=['GET'])
def water_left():
    global sensors

    waterAmount = sensors.getWaterLeft()
    response = json.dumps({"water": waterAmount}) # percentage
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/temp", methods=['GET'])
def temp():
    global sensors

    temperature = sensors.getTemp()
    response = json.dumps({"temp": temperature}) # in gallons
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/resetWater", methods=['PUT'])
def reset_water_level():
    global sensors

    sensors.resetWaterLevel()
    return Response(status=200, mimetype="application/json")

@app.route("/back/getName", methods=['GET'])
def plant_name():
    global sensors

    name = sensors.getPlantName()
    response = json.dumps({"name": name})  # in gallons
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/getType", methods=['GET'])
def plant_type():
    global sensors

    type = sensors.getPlantType()
    response = json.dumps({"type": type})  # in gallons
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/getPlantTime", methods=['GET'])
def plant_time():
    global sensors

    plantTime = sensors.getPlantTime()
    response = json.dumps({"time": plantTime})  # in gallons
    return Response(response=response, status=200, mimetype="application/json")

@app.route("/back/newPlant", methods=['POST'])
def new_plant():
    global sensors

    data = request.get_json(silent=True)
    newName = data.get('name')
    newType = data.get('type')

    sensors.newPlant(newName, newType)
    print("Done")
    return Response(status=200, mimetype="application/json")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', threaded = True)
        while True: # run so that when the program is interrupted, the sensors thread can be stopped
            None
    except KeyboardInterrupt:
        sensors.stop()
        sensors.join()
