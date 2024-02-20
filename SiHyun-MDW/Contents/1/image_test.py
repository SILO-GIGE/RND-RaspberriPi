from PIL import Image

color_list = []

im = Image.open("/home/silolab_ksh/Desktop/RND-MDW/Contents/1/image.jpg")

print(im.format, im.size, im.mode)
w = im.width
h = im.height
pix =im.load()

print("-"*16)

for y in range(h-1, -1, -1):
    if h%2 != y%2: 
        for x in range(w):
            print(h,y)
            print(pix[x,y])
            color_list.append(pix[x,y])
    else:
        for x in range(w-1, -1, -1):
            print(h,y)
            print(pix[x, y])
            color_list.append(pix[x,y])
    print("\n")

print("-"*16)
