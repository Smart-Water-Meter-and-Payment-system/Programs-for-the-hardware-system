import os
import math
import random
import smtplib

digits = "0123456789"

def createToken():
    token = ""
    for i in range (5):
        token += digits[math.floor(random.random()*10)]
    return token