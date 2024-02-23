'''
[02/22]
 - 5면 LED pixel 10초 콘텐츠 재생.
 - 윈도우로부터 OSC신호로 1을 수신하면 콘텐츠10초 재생.
 - 콘텐츠 재생이 끝나면 윈도우로 OSC신호 3을 전송.
'''
# -*- coding: utf-8 -*-g

import board
import neopixel
from PIL import Image
import time
import os
import threading
import sys

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

#######################################################################
Main_port_num=5557  # Window 포트번호
Server1_port_num=4208  #라즈베리파이 포트번호

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1280 #256 픽셀 LED 5개
ORDER = neopixel.RGB

# OSC 클라이언트 설정
client_ip = '192.168.0.5'  # Window IP 주소
client_port = Main_port_num
osc_client = udp_client.SimpleUDPClient(client_ip, client_port)

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 수신
port = Server1_port_num
#######################################################################


# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/SILOKSH":
        print(f"Received OSC message from {address}: {args}")
        #OSC신호 1을 수신하면 콘텐츠 재생
        if args[0]==1:
            for i in range(num_iterations):
                index = i % len(image_pixels_list)  # 이미지 배열을 순환
                show_image(*image_pixels_list[index]) #이미지를 출력.
                time.sleep(interval)
            # 이미지가 모두 재생된 후 LED를 끄고 OSC 메시지 전송
            time.sleep(0.5)
            pixels.fill((0, 0, 0))
            pixels.show()
            osc_client.send_message("/Rasp", 3)
            print("Sent OSC message: /Rasp 3")  # 전송한 메시지 출력
        #OSC신호 0을 수신하면 콘텐츠 종료
        elif args[0]==0:
            pixels.fill((0, 0, 0))
            pixels.show()
            
# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")

# LED 초기화 및 설정
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/Contents/80x16png/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 이미지경로에 있는 png파일 가져오기
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # jpg 파일인 경우에만 처리
        image_paths.append(filename)

# 파일 이름들의 숫자 순서대로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]
 
 
#########################################################################
# 이미지를 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    # 이미지를 왼쪽부터 16x16 크기로 자르기
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
    
    #다듬어진 이미지를 배열에 저장. 
    image_pixel_lists = [image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels]
    
    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for image_pixels in image_pixel_lists:
        for y in range(16):
            if y % 2 == 1:  # 홀수 번째 행일 때
                start_index = y * 16
                end_index = (y + 1) * 16
                image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])
    return image1_pixels,image2_pixels,image3_pixels,image4_pixels,image5_pixels

#########################################################################
# 이미지 출력 함수
def show_image(image1_pixels,image2_pixels,image3_pixels,image4_pixels,image5_pixels):
    image_pixel_lists = [image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels]
    pixel_index = 0

    for image_pixels in image_pixel_lists:
        for pixel_value in image_pixels:
            pixels[pixel_index] = pixel_value
            pixel_index += 1
    pixels.show() #LED ON

# 각 이미지를 픽셀 배열로 변환하여 배열에 저장
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 10  # 10초
num_iterations = int(total_time / interval)


#########################################################################
# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
    

# 모든 이미지 송출이 끝나면 LED를 종료.
pixels.fill((0, 0, 0))
pixels.show()
