import RPi.GPIO as GPIO
import time

OUTLETS = [23, 24, 12, 16]

class GPIOcontrol:
    def __init__(self):
        GPIO.setmode(GPIO.BCM) #set numbering scheme to GPIO numbers
        GPIO.setup(OUTLETS[0], GPIO.OUT) #set GPIO on pi to outputs
        GPIO.setup(OUTLETS[1], GPIO.OUT)
        GPIO.setup(OUTLETS[2], GPIO.OUT)
        GPIO.setup(OUTLETS[3], GPIO.OUT)

        GPIO.output(OUTLETS[0], True) #when initialized, set high so power is not applied
        GPIO.output(OUTLETS[1], True)
        GPIO.output(OUTLETS[2], True)
        GPIO.output(OUTLETS[3], True)
        
    def control(self, outlet, on):
        if outlet <= len(OUTLETS):
            GPIO.output(OUTLETS[outlet - 1], not on)