import RPi.GPIO as GPIO
from SolenoidValve import *
from PumpMotor import *
import time
from amountToDatabase import *

global amountInserted
global count
global start_counter
count = 0
global totalVolumeL
global totalVolumeDispensed
global totalAmountPaid
global volume

def countPulse(channel):
	global count
	if start_counter == 1:
		count = count+1

#GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

def setup(flowSensorGPIO, pumpPin, s_Pin ):
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(flowSensorGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(s_Pin, GPIO.OUT)
	GPIO.setup(pumpPin, GPIO.OUT)
	GPIO.add_event_detect(flowSensorGPIO, GPIO.FALLING, callback=countPulse)


def getWaterChargeRate():
	lines = []
	with open('currentWaterChargeRate.txt') as c:
		lines = list(c)

	chargeAmount = int(lines[0])
	return chargeAmount

def getWaterChargeVolume():
	lines = []
	with open('currentWaterChargeRate.txt') as c:
		lines = list(c)

	volume = int(lines[1])
	return volume

def nonFirstTransaction(volume):
	waterCharge = getWaterChargeRate()
	volumeCharge = getWaterChargeVolume()
	amountCollected = (waterCharge/volumeCharge)*volume
	saveTransaction(volume, amountCollected)

def recordFetchingDetails():
	global totalVolumeL
	print("Total Volume left is:", totalVolumeL)
	currentWaterCharge = getWaterChargeRate()
	volumeBeingCharged = getWaterChargeVolume()
	amountLeft = (currentWaterCharge/volumeBeingCharged)*totalVolumeL
	roundedAmountLeft = round(amountLeft,2)
	print("Amount left remaining is", roundedAmountLeft)
	#phoneNumber = input("Enter your phone number:")
	updateCustomer(roundedAmountLeft)
	amountCollected = (totalVolumeDispensed * currentWaterCharge)/volumeBeingCharged
	saveTransaction(totalVolumeDispensed, amountCollected)

def convertCoinToVolume():
	global amountInserted
	global count
	global totalVolumeL
	global volume
	global totalVolumeDispensed
	totalVolumeDispensed = 0
	print("Amount inserted:", amountInserted)
	chargeAmount = getWaterChargeRate()
	volume = getWaterChargeVolume()*1000
	conversion = (amountInserted * volume)/chargeAmount
	totalVolumeL = conversion/1000
	totalVolumeL = round(totalVolumeL,2)
	print("You are getting ", totalVolumeL, " litres of water")
	totalVolumemL = totalVolumeL*1000
        #totalVolumeL = totalVolumeL -0.06 
	turnSolenoidOn()
	turnPumpOn()
	while totalVolumeL > 0:
		start_counter = 1
		time.sleep(1)
		start_counter = 0
		print("Count of the water flow sensor is :" , count)
		flow = (count /(45*10**4))
		print("The flow is %.5f liters/millisec" % (flow))
		count = 0
		time.sleep(1)
		volumeDispensed = flow
		totalVolumeDispensed = round((totalVolumeDispensed + volumeDispensed),5) 
               #volumeDispensed = volumeDispensed/1000
                #totalVolumeConversion = totalVolumemL - volumeDispensed
                #totalVolumemL = totalVolumeConversion
		totalVolumeL = totalVolumeL - volumeDispensed
		print("Volume left:",round(totalVolumeL,4))
		volume = round(totalVolumeL,4)
                #keyboard.on_press_key('x',here)
	turnSolenoidOff()
	turnPumpOff()

def getCoinAmount(amount):
        #print("Get coin amount:", amount)
	global amountInserted
	amountInserted = int(amount)
	if amountInserted == 0:
		turnSolenoidOff()
		turnPumpOff()
	else:
		convertCoinToVolume()

if __name__ == '__main__':
        #setup(33,16,37)
        while True:
                try:
                        start_counter=1
                        inputEntered = input("Enter a token:")
                        setup(33,16,37)
                        checkIfToken(inputEntered)


                except KeyboardInterrupt:
                        turnSolenoidOff()
                        turnPumpOff()
                        print("Going into fetching details")
                        recordFetchingDetails()
                        GPIO.cleanup()

