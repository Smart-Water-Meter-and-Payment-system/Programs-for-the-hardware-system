import RPi.GPIO as GPIO
import time

channel = 40

# GPIO setup
GPIO.setmode(GPIO.BOARD) # sets numbering system to be used. Options are: BCM, BOARD
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

def motor_on(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor on 

def motor_off(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor off

while True:
    try:
        motor_on(channel)
        print("ON")
        time.sleep(5)
    
    except KeyboardInterrupt:
        GPIO.cleanup()

