import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
class TempSensor:
    def __init__(self):
        self.__BASE_DIR = '/sys/bus/w1/devices/'
        self.__DEVICE_FOLDER = glob.glob(self.__BASE_DIR + '28*')[0]
        self.__DEVICE_FILE = self.__DEVICE_FOLDER + '/w1_slave'
    
    def __read_temp_raw(self):
        f = open(self.__DEVICE_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def read_temp(self):
        lines = self.__read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = __read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_f
            
        
	