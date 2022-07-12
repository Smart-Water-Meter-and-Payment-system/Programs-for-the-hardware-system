import RPi.GPIO as g
import time

gpio_used=13

g.setmode(g.BOARD)

g.setup(gpio_used,g.IN, pull_up_down=g.PUD_UP)

counter = 1

try:
        while True:
                g.wait_for_edge(gpio_used, g.RISING)
                print("Pulse coming ! (%s)") % counter
                counter += 1
                

except KeyboardInterrupt:
        g.cleanup()

