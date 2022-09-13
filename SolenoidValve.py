#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep
#GPIO.setmode(GPIO.BOARD)


#If code is stopped while the solenoid is active it stays active
#This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
#from previous time the code was run. This line ensures that warning is given
GPIO.setwarnings(True)

pin=37
#GPIO.setup(pin, GPIO.OUT)

def turnSolenoidOn():
	GPIO.output(pin,0)

def turnSolenoidOff():
	GPIO.output(pin,1)

