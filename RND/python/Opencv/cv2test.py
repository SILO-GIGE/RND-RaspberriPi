import cv2

# 이미지 파일 읽기
image = cv2.imread('/home/silolab_ksh/Desktop/RND-RaspberryPi/cvtest.jpg')

# 이미지 크기 확인
height, width, channels = image.shape
print(f"Image height: {height}, width: {width}, channels: {channels}")

# 이미지 보기
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
