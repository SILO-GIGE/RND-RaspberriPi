#LED two Seconds on/off 

import RPi.GPIO as GPIO
import time

LED=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT,initial=GPIO.LOW) 


try:
    while 1:
        GPIO.output(17,False)#led off
        time.sleep(2)#2sec
        print("LED ON")
        GPIO.output(17,True)#led on
        time.sleep(2)
        print("LED OFF")
except KeyvoardInterrupt:
    pass

GPIO.cleanup() #
