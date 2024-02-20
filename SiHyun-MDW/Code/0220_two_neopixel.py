'''
[02/20]
 - 16 x 16 two LED pixel 300 image play
 - For 10 seconds 1/30 frame
 - Image crop
'''
# -*- coding: utf-8 -*-

import board
import neopixel
from PIL import Image
import time
import os

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 512  # 32x16 픽셀 LED
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
    image1 = image.crop((0, 0, 16, 16))  # Image crop (StartX, StartY, EndX, EndY)
    image2= image.crop((17,0,33,16))
    # 이미지를 상하로 반전
    image1 = image1.transpose(Image.FLIP_TOP_BOTTOM)
    image2 = image2.transpose(Image.FLIP_TOP_BOTTOM)

    #get Image pixel
    image1_pixels = list(image1.getdata())
    image2_pixels = list(image2.getdata())

    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image1_pixels[y * 16: (y + 1) * 16] = reversed(image1_pixels[y * 16: (y + 1) * 16])
    for y in range(16):
        if y % 2 == 1:  # 홀수 번째 행일 때
            image2_pixels[y * 16: (y + 1) * 16] = reversed(image2_pixels[y * 16: (y + 1) * 16])

    return image1_pixels,image2_pixels

# 이미지 출력 함수
def show_image(image1_pixels,image2_pixels):
    for i in range(256):
        pixels[i]=image1_pixels[i]
    for i in range(256,512):
        pixels[i]=image2_pixels[i-256]
        '''
    for i, pixel in enumerate(image_pixels):
        pixels[i] = pixel'''
    pixels.show()

# 각 이미지를 픽셀 배열로 변환하여 배열에 저장
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 10  # 10초
num_iterations = int(total_time / interval)

for i in range(num_iterations):
    index = i % len(image_pixels_list)  # 이미지 배열을 순환
    show_image(*image_pixels_list[index])
    time.sleep(interval)

# 모든 이미지 송출이 끝나면 LED를 끕니다.
pixels.fill((0, 0, 0))
pixels.show()
