import RPi.GPIO as GPIO
import os
import glob
import time

"""
Temperature Sensor Data Collection
DS18B20 
"""

base_dir = '/sys/bus/w1/devices/'

# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Mount device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class Temperature():
    def __init__(self):
        pass

    def read_rom(self):
        name_file=device_folder+'/name'
        f = open(name_file,'r')
        return f.readline()

    def read_temp_raw(self):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        """
        Reads and returns temperature values from sensor
        GPIO pin:
        """
        lines = self.read_temp_raw()
        # Analyze if the last 3 characters are 'YES'.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        # Find the index of 't=' in a string.
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c

# FOR DEBUGGING PURPOSES
# print(' rom: '+ Temperature.read_rom())
# while True:
#     print(' Celsius=%3.3f'% Temperature.read_temp())
#     time.sleep(1)