import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
 
class MoistSensor:

    def __init__(self):
        #create the spi bus
        self.__spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) 
        # create the cs (chip select)
        self.__cs = digitalio.DigitalInOut(board.CE0)
        # create the mcp object
        self.__mcp = MCP.MCP3008(self.__spi, self.__cs)
        # create an analog input channel on pin 0
        self.__chan = AnalogIn(self.__mcp, MCP.P0)
 
    def get_moisture(self):
        #min - wet - 32128
        #max - dry - 56384
        #math: make dry 0, make wet -24256
            #56384 - value / 24256
        value = (56384 - self.__chan.value)/24256
        return value