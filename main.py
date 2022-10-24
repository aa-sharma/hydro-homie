import time
import RPi.GPIO as GPIO

from daq.moisture import Moisture
from daq.temp import Temperature
from daq.ldr import LDR
from filter.kalman import KalmanFilter

RELAY_PIN = 21

# Threshold values
ideal_temp = 25
ideal_moisture = 50
ideal_light = 5

error_margin = 0.5


def turnOnPump():
    """
    Method to turn on pump
    Args: None
    Returns: None
    """
    GPIO.output(RELAY_PIN, GPIO.HIGH)

def turnOffPump():
    """
    Method to turn off pump
    Args: None
    Returns: None
    """
    GPIO.output(RELAY_PIN, GPIO.LOW)

if __name__ == '__main__':
    while True:
        time.sleep(2)
        # Data collection from all three
        current_moisture = Moisture.collect_data()
        current_temp = Temperature.read_temp()
        current_light = LDR.collect_data()

        # Filtering
        current_temp = KalmanFilter.kalman(current_temp)

        # actuate pump based on Temperature readings
        if (int(current_temp) + error_margin) < ideal_temp:
            turnOnPump()
        else:
            turnOffPump()