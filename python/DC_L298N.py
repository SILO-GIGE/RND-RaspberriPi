
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
IN1 = 17
IN2 = 18
ENA = 27
                                                
# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 출력 핀으로 설정
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# PWM 객체 생성
pwm = GPIO.PWM(ENA, 100)  # 주파수 설정 (100Hz)

# DC 모터 제어 함수
def set_motor_speed(speed):
    if speed > 100:
        speed = 100
    elif speed < -100:
        speed = -100
    
    if speed >= 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    pwm.start(abs(speed))

# DC 모터 정지
def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.stop()

# DC 모터 제어 예시
try:
    while True:
        print('hi')
        set_motor_speed(30)  # 모터 속도 설정 (양수: 정방향, 음수: 역방향)
        time.sleep(2)
        stop_motor()#모터 정지
        time.sleep(2)
        set_motor_speed(-30)
        time.sleep(5)
        stop_motor()#모터 정지
        time.sleep(2)

except KeyboardInterrupt:
    stop_motor()
    GPIO.cleanup()
