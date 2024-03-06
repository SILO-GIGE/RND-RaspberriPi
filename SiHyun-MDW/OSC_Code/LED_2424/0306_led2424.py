'''
[03/04]
주석 달았음.
라즈베리파이 서버를 윈도우에서 테스트 하는중. 

24*24 pixels
_______________________
 front2|front3 |      | 
       |       |      | 
---------------|      |
               |      |
               |fornt4|
    front1     |      |
               |      |
               |      |
_______________|______|
               |   X  |
               |______|

[코드 실행 순서]
1. image_pixels_list 배열 생성. 
    - image_to_pixels함수 실행되어 이미지 각각 배열로 저장됨.
2. OSC신호 '1'을 수신하면.
3. show_image()함수 실행.
    - pixels[]마다 RGB 값이 하나씩 저장됨.
    - pixel.show()를 통해 한번에 출력.


    
'''
# -*- coding: utf-8 -*-g

import neopixel
from PIL import Image
from PIL import ImageEnhance
import time
import os
import threading
import sys
import board

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

Main_port_num=5557  # Window 포트번호
Server1_port_num=4207  #라즈베리파이 포트번호

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1728 + 192 #24*24 픽셀 3면, 8*8 픽셀 빈부분 3면 1920 pixels
ORDER = neopixel.GRB

# OSC 클라이언트 설정
client_ip = '192.168.50.191'  # Window IP 주소
client_port = Main_port_num
osc_client = udp_client.SimpleUDPClient(client_ip, client_port)

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 수신
port = Server1_port_num

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/SILOKSH":
        print(f"Received OSC message from {address}: {args}")#수신한 메세지를 출력. 
        #OSC신호 1을 수신하면 콘텐츠 재생
        if args[0]==1:
            start_time = time.time()
            for i in range(num_iterations):#출력할 이미지 개수
                index = i % len(image_pixels_list)  # 이미지 배열을 순환
                show_image(*image_pixels_list[index]) #이미지를 출력.
                #time.sleep(interval)
            end_time = time.time()
            execution_time = end_time - start_time
            print("코드 실행 시간:", execution_time, "초")
            pixels.fill((0, 0, 0))
            pixels.show()
            osc_client.send_message("/Rasp2", 4)
            print("Sent OSC message: /Rasp2 4")  # 전송한 메시지 출력
        #OSC신호 0을 수신하면 LED OFF
        elif args[0]==0:
            pixels.fill((0, 0, 0))
            pixels.show()
            
# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")

# LED 초기화 및 밝기 설정
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.7, auto_write=False, pixel_order=ORDER)

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/TEST1_LED3/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 이미지경로에 있는 png파일 가져오기
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # png 파일인 경우에만 처리
        image_paths.append(filename)

# 파일 이름들의 숫자 순서대로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# image_paths = ["image1.png", "image2.png", "image3.png"] 이런식으로 저장됨.

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
# 폴더의 경로가 아닌 각 이미지마다 자기 경로가 지정이됨. 
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]
# iamge_paths= ['/home/user/images/image1.png', '/home/user/images/image2.png', '/home/user/images/image3.png', ...]

def process_image(image_path):
    # 이미지를 불러와 RGB 색상 모드로 변환
    image = Image.open(image_path).convert("RGB")
    
    # 이미지의 채도를 강조
    enhancer = ImageEnhance.Contrast(image) 
    image = enhancer.enhance(3.0)
    
    # 이미지 영역을 자르고 상하 반전 수행
    cropped_images = []
    for box in [(0,16,16,32), (0,8,8,16), (8,8,16,16), (16,8,24,40), 
                (24,16,40,32), (24,8,32,16), (32,8,40,16), (40,8,48,40), 
                (48,16,64,32), (48,8,56,16), (56,8,64,16), (64,0,72,32)]:
        cropped_image = image.crop(box)
        cropped_image = cropped_image.transpose(Image.FLIP_TOP_BOTTOM)
        cropped_images.append(list(cropped_image.getdata()))
    
    return cropped_images

def show_image(*pixel_lists):
    combined_pixels = [pixel for sublist in pixel_lists for pixel in sublist]
    pixels[0:len(combined_pixels)] = combined_pixels
    pixels.show()

# 각 이미지를 픽셀 배열로 변환하여 배열에 저장
image_pixels_list = [process_image(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출e
interval = 1 / 30  # 1/30초 간격
total_time = 10 # 10초
num_iterations = int(total_time / interval) #이미지 출력 개수

#########################################################################
# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()

