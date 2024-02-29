'''
[02/20]
 - 16 x 16 Five LED pixel 300 image play
 - For 10 seconds 1/30 frame
 - Image crop
 - Receive OSC signal 
'''
# -*- coding: utf-8 -*-

import board
import neopixel
from PIL import Image
import time
import os

from pythonosc import dispatcher
from pythonosc import osc_server
#from pythonosc import udp_client

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/button1":
        print(f"Received OSC message from {address}: {args}")
        if args[0]==1:
                        
            for i in range(num_iterations):
                index = i % len(image_pixels_list)  # 이미지 배열을 순환
                show_image(*image_pixels_list[index])
                time.sleep(interval)
        elif args[0]==0:
            # 모든 이미지 송출이 끝나면 LED를 끕니다.
            pixels.fill((0, 0, 0))
            pixels.show()
            
            
# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 들으려면 '0.0.0.0'을 사용합니다.
port = 3999 # TouchDesigner에서 설정한 포트 번호로 변경해야 합니다.

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)  # 모든 메시지를 동일한 핸들러로 전달합니다.

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")


# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1280 # 32x16 픽셀 LED
ORDER = neopixel.RGB

# LED 초기화
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/Contents/80x16png/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 디렉토리 내 모든 파일에 대해 반복
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # jpg 파일인 경우에만 처리
        image_paths.append(filename)

# 파일 이름들을 숫자 부분을 기준으로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]
 
# 이미지 파일들의 경로를 숫자 부분을 기준으로 정렬


# 이미지를 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    # 이미지를 32x16 크기로 자르기
    image1 = image.crop((0, 0, 16, 16))   # 첫 번째 영역: (0, 0)에서 (16, 16)까지
    image2 = image.crop((16, 0, 32, 16))  # 두 번째 영역: (16, 0)에서 (32, 16)까지
    image3 = image.crop((32, 0, 48, 16))  # 세 번째 영역: (32, 0)에서 (48, 16)까지
    image4 = image.crop((48, 0, 64, 16))  # 네 번째 영역: (48, 0)에서 (64, 16)까지
    image5 = image.crop((64, 0, 80, 16))  # 다섯 번째 영역: (64, 0)에서 (80, 16)까지

    
    # 이미지를 상하로 반전
    image1 = image1.transpose(Image.FLIP_TOP_BOTTOM)
    image2 = image2.transpose(Image.FLIP_TOP_BOTTOM)
    image3 = image3.transpose(Image.FLIP_TOP_BOTTOM)
    image4 = image4.transpose(Image.FLIP_TOP_BOTTOM)
    image5 = image5.transpose(Image.FLIP_TOP_BOTTOM)


    #get Image pixel
    image1_pixels = list(image1.getdata())
    image2_pixels = list(image2.getdata())
    image3_pixels = list(image3.getdata())
    image4_pixels = list(image4.getdata())
    image5_pixels = list(image5.getdata())

    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image1_pixels[y * 16: (y + 1) * 16] = reversed(image1_pixels[y * 16: (y + 1) * 16])
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image2_pixels[y * 16: (y + 1) * 16] = reversed(image2_pixels[y * 16: (y + 1) * 16])
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image3_pixels[y * 16: (y + 1) * 16] = reversed(image3_pixels[y * 16: (y + 1) * 16])
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image4_pixels[y * 16: (y + 1) * 16] = reversed(image4_pixels[y * 16: (y + 1) * 16])
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image5_pixels[y * 16: (y + 1) * 16] = reversed(image5_pixels[y * 16: (y + 1) * 16])

    return image1_pixels,image2_pixels,image3_pixels,image4_pixels,image5_pixels


# 이미지 출력 함수
def show_image(image1_pixels,image2_pixels,image3_pixels,image4_pixels,image5_pixels):
    
    for i in range(256):
        pixels[i]=image1_pixels[i]
    for i in range(256,512):
        pixels[i]=image2_pixels[i-256]
    for i in range(512,768):
        pixels[i]=image3_pixels[i-512]
    for i in range(768,1024):
        pixels[i]=image4_pixels[i-768]
    for i in range(1024,1280):
        pixels[i]=image5_pixels[i-1024]
    
    pixels.show()

# 각 이미지를 픽셀 배열로 변환하여 배열에 저장
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 10  # 10초
num_iterations = int(total_time / interval)

# OSC 메시지 수신 대기

try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
    
# 모든 이미지 송출이 끝나면 LED를 끕니다.
pixels.fill((0, 0, 0))
pixels.show()
