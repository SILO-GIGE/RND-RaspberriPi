# -*- coding: utf-8 -*-

import time
import os
import threading
import sys
import board
import digitalio
import busio
from PIL import Image
from PIL import ImageEnhance
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import BLACK
from adafruit_led_animation.led_strip import Adafruit_DotStar

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

Main_port_num = 5557  # Window 포트번호
Server1_port_num = 4206  # 라즈베리파이 포트번호

# LED 설정
num_pixels = 1280 + 512  # 256 픽셀 LED 5개
pixel_pin = board.D18  # GPIO 18에 연결된 LED

# Create DotStar LED object
pixels = Adafruit_DotStar(pixel_pin, num_pixels, auto_write=False)
pixels.fill(BLACK)  # Clear all pixel colors
pixels.show()  # Make sure to update the strip

# OSC 클라이언트 설정
client_ip = '192.168.50.191'  # Window IP 주소
client_port = Main_port_num
osc_client = udp_client.SimpleUDPClient(client_ip, client_port)

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 수신
port = Server1_port_num

# LED 초기화
pixels.fill(BLACK)  # Clear all pixel colors
pixels.show()  # Make sure to update the strip

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/0304TEST1/TEST1_LED1/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 이미지경로에 있는 png파일 가져오기
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # png 파일인 경우에만 처리
        image_paths.append(filename)

# 파일 이름들의 숫자 순서대로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
# 폴더의 경로가 아닌 각 이미지마다 자기 경로가 지정이됨.
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]


'''---------------------------------------------------------------------------'''

# 이미지각각 마다 이미지 영역을 자르고 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image = Image.open(image_path).convert("RGB")  # 이미지를 RGB색상모드로 변환
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)  # 이미지의 채도를 강하게.

    image1 = image.crop((0, 0, 16, 16))
    image2 = image.crop((16, 0, 32, 16))
    image3 = image.crop((32, 0, 48, 16))
    image4 = image.crop((48, 0, 64, 16))
    image5 = image.crop((64, 0, 80, 16))

    # 이미지를 상하로 반전
    image1 = image1.transpose(Image.FLIP_TOP_BOTTOM)
    image2 = image2.transpose(Image.FLIP_TOP_BOTTOM)
    image3 = image3.transpose(Image.FLIP_TOP_BOTTOM)
    image4 = image4.transpose(Image.FLIP_TOP_BOTTOM)
    image5 = image5.transpose(Image.FLIP_TOP_BOTTOM)

    # get Image pixel
    image1_pixels = list(image1.getdata())
    image2_pixels = list(image2.getdata())
    image3_pixels = list(image3.getdata())
    image4_pixels = list(image4.getdata())
    image5_pixels = list(image5.getdata())

    '''
    image1_pixels 형식
    [ (R,G,B), # 첫번째 픽셀의 색상
      (R,G,B), # 두번째 픽셀의 색상
      ...
    ]
    '''
    # 이미지들의 RGB색상들의 리스트가 배열로 저장됨.
    image_pixel_lists = [image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels]

    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for image_pixels in image_pixel_lists:
        for y in range(16):  # 0부터 15까지
            # 이미지는 x가 작은 순부터 읽기 때문에 네오픽셀 특성상
            # 홀수번째 행일때만 이미지를 반대로 뒤집음.
            if y % 2 == 1:
                start_index = y * 16
                end_index = (y + 1) * 16
                image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])

    return image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels


#########################################################################
# 이미지 출력 함수
def show_image(image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels):
    combined_pixels = image1_pixels + image2_pixels + image3_pixels + image4_pixels + image5_pixels

    # 네오픽셀에 한 번에 모든 픽셀 값을
