import RPi.GPIO as GPIO
import time

def red():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(17,GPIO.OUT)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(17,GPIO.HIGH)
    
    
def green():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(17,GPIO.LOW)
    GPIO.output(18,GPIO.HIGH)
    
    

#17 = red
#18 = green
