

import RPi.GPIO as g
import time
from threading import Thread
#from coinToVolume import getTempCoinAmount
#from SolenoidValve import *
#from PumpMotor import *

g.setmode(g.BOARD)

gpio_used=11

g.setup(gpio_used,g.IN, pull_up_down=g.PUD_UP)

global count
global counting
counting = 0


def firstFunction():
	global counter
	global ts
	count = 1
	counter = 0
	ts = time.time()
	while True:
		if (count == 1):
			#print("=============COUNT RIGHT BEFORE PULSE:", count)
			g.wait_for_edge(gpio_used, g.RISING)
			counting = 1
			counter += 1
			print("Pulse incoming ...(", counter,")")
			ts = time.time()


def secondFunction():
	global count
	global counter
	global pulse
	while True:
		cts = ts + 2
		if (cts < time.time()):
			print("Counting finished with", counter ,"pulses") 
			count = 0
			counting = 0
			#print("===========COUNT BEFORE PAYMENT PROCESSING:", count)
			print("Processing payment now !")

			if (counter == 1):
				print("100 Ugandan shillings received")
				money = 100
			if (counter == 2):
				print("200 Ugx received")
				money = 200
			if (counter == 3):
				print("500 Ugx received")
				money = 500
			if (counter == 4):
				print("1000 Ugx received")
				money = 1000
			counter = 0
			print("Ready to process the next payment !")
			#print("==============COUNT BEFORE PASSING MONEY:", count)
			#getCoinAmount(money)
			#print("==============COUNT AFTER PASSING MONEY:", count)
			#count=1
			time.sleep(1)


def thirdFunction():
	while True:
		if (counting == 0):
			global ts
			ts = time.time()
			time.sleep(1)

#def fourthDunction():
#	global pulse
#	pulse = input("Enter a number")

try:
	t1 = Thread(target = firstFunction)
	t2 = Thread(target = secondFunction)
	t3 = Thread(target = thirdFunction)
#	t4 = Thread(target = fourthDunction)

#	t1.daemon = True
#	t2.daemon = True
#	t3.daemon = True

	t1.start()
	t2.start()
	t3.start()
#	t4.start()

except KeyboardInterrupt:
	t1.stop()
	t2.stop()
	t3.stop()
	#turnSolenoidOff()
	#turnPumpOff()
	g.cleanup()

