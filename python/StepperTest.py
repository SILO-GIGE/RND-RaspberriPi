from flask import Flask, render_template_string, request  
import RPi.GPIO as GPIO    
from time import sleep
from RpiMotorLib import RpiMotorLib
GPIO_pins = (14, 15, 18)
direction = 20      
step = 21

slider = request.form["slider"]
print(int(slider))
if (int(slider)>10):
       mymotortest.motor_go(True, "Full" , 600,int(slider)*.0004, False, .05)
       print("Rotating Clockwise")
#Repeat the same procedure for the slider values less than 10.
if (int(slider)<10):
     mymotortest.motor_go(False, "Full" , 600,int(slider)*.001, False, .05)
     print("Rotating Anti-Clockwise")
