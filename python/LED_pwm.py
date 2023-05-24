#밝기가 0에서 100 까지 0.1초 간격으로 바뀌는 코드

import RPi.GPIO as GPIO
import time

def led_pwm(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT,initial=GPIO.LOW)

    pwm = GPIO.PWM(pin, 100) # pwm 설정 (100Hz)
    pwm.start(0)
    
    # 밝기가 0에서 100 까지 0.1초 간격으로 바뀜
    for i in range(101):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.1)
    
    pwm.stop()
    GPIO.cleanup()

led_pwm(17)
GPIO.cleanup()
