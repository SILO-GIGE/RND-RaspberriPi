from PIL import Image
import time

"""
list = []
for i in range(1):
    lll = []
    print(f"{i:05d}")
    img = Image.open(f"image_{i:05d}.jpg")
    img.show()
    lll.append(i)
    list.append(lll)
    
print(list)
"""

color_frame = []

im = Image.open(f"image_00001.jpg")

print(im.format, im.size, im.mode)
w = im.width
h = im.height
pix =im.load()

print("-"*16)

for y in range(h-1, -1, -1):
    if h%2 != y%2: 
        for x in range(w):
            #print(h,y)
            #print(pix[x,y])
            color_frame.append(pix[x,y])
    else:
        for x in range(w-1, -1, -1):
            #print(h,y)
            #print(pix[x, y])
            color_frame.append(pix[x,y])
    #print("\n")

print("-"*16)

print(color_frame)

