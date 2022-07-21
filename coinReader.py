import RPi.GPIO as g
import time
from threading import Thread

gpio_used=10

g.setmode(g.BOARD)

g.setup(gpio_used,g.IN, pull_up_down=g.PUD_UP)
        
global count
global counting

counting = 0

def firstFunction():
	global counter
	global ts
	global counting
	count = 1
	counter = 0
	ts = time.time()
	while True:
		if (count == 1):
			g.wait_for_edge(gpio_used, g.RISING)
			counting = 1
			counter += 1
			print("Pulse incoming ...(%s)") % counter
			ts = time.time()


def secondFunction():
	global count
	global counting
	global counter
	while True:
		cts = ts + 2
                if (cts < time.time()):
                        print("Counting finished with %s pulses") % counter
			count = 0
			counting = 0
			print("Processing payment now !")

			if (counter == 1):
                                print("100 Ugandan shillings received")
                        if (counter == 2):
                               print("200 Ugx received")
                        if (counter == 3):
                               print("500 Ugx received")
                        if (counter == 4):
                               print("1000 Ugx received")

			counter = 0
			count = 1
			print("Ready to process the next payment !")
		time.sleep(1)


def thirdFunction():
	while True:
		if (counting == 0):
			global ts
			ts = time.time()
			time.sleep(1)

try:
	t1 = Thread(target = firstFunction)
	t2 = Thread(target = secondFunction)
	t3 = Thread(target = thirdFunction)

	t1.start()
	t2.start()
	t3.start()

except KeyboardInterrupt:
	t1.stop()
	t2.stop()
	t3.stop()
	g.cleanup()

