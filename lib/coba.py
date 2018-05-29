from pyx import *
from PIL import Image

im = Image.open('../static/uploads/gb2.GIF')
pixels = list(im.getdata())
width, height = im.size

images = []
for i in range(height):
    for j in range(width):
        if(i%2==0):
            cluster = 1
            red = 255
            green = 0
            blue = 0
        else :
            cluster = 2
            red = 0
            green = 0
            blue = 255
        images.append([(i,j), cluster, (red, green, blue)])

im = Image.new("RGB", (width, height))
for i in range(len(images)):
    print(images[i])
    im.putpixel(images[i][0], images[i][2])

im.save('pil.png')

