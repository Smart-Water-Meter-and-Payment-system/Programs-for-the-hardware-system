import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

gpio_used=10

GPIO.setup(gpio_used,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

count = 1
counter = 1

try:
        while True:
                GPIO.wait_for_edge(gpio_used, GPIO.RISING)
                print("Pulse incoming... (%s)") % counter
                counter += 1

except KeyboardInterrupt:
        GPIO.cleanup()
