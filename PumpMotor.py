import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BOARD)
# GPIO setup

pump_pin = 16
#GPIO.setup(pump_pin, GPIO.OUT)


def turnPumpOn():
	GPIO.output(pump_pin,0)

def turnPumpOff():
	GPIO.output(pump_pin,1)


