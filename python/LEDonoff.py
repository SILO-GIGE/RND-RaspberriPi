#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LED two Seconds on/off

import RPi.GPIO as GPIO
import time

LED_pin=18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_pin,GPIO.OUT,initial=GPIO.LOW) 

while True:
    try:
        GPIO.output(LED_pin,False)#led off
        time.sleep(2)#2sec
        print("LED ON")
        GPIO.output(LED_pin,True)#led on
        time.sleep(2)
        print("LED OFF")

    except KeyboardInterrupt:
        pass
        print('Exit with ^C. Goodbye!')
        GPIO.cleanup() #pin reset
        exit() #code end

GPIO.cleanup() 
