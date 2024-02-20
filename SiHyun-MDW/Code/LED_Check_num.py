# -*- coding: utf-8 -*-

import board
import neopixel
from PIL import Image
import time
import os

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 512  # 16x16 픽셀 LED
ORDER = neopixel.RGB

# LED 초기화
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)


# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/1616png/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 디렉토리 내 모든 파일에 대해 반복
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # jpg 파일인 경우에만 처리
        image_paths.append(filename)
        #print(filename)

# 파일 이름들을 숫자 부분을 기준으로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]

#print(image_paths)

# 이미지 파일들의 경로를 숫자 부분을 기준으로 정렬

# 이미지를 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((32, 16))  # 16x16 픽셀로 조정
    image_pixels = list(image.getdata())

    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image_pixels[y * 16 : (y + 1) * 16] = reversed(image_pixels[y * 16 : (y + 1) * 16])

    return image_pixels

# LED를 하나씩 켜는 함수
def show_image_led_by_led(image_pixels):
    for i in range(num_pixels):
        pixels.fill((0, 0, 0))  # 모든 LED를 끄고
        pixels[i] = image_pixels[i]  # 현재 LED에 대한 픽셀 데이터를 켜고
        pixels.show()  # LED 업데이트
        time.sleep(0.1)  # 0.1초 대기

# 각 이미지를 픽셀 배열로 변환하여 배열에 저장
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 하나씩 LED에 켜는 동안 기다림
for image_pixels in image_pixels_list:
    show_image_led_by_led(image_pixels)

# 마지막에 모든 LED를 끔
pixels.fill((0, 0, 0))
pixels.show()
