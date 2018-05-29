# import cv2
from PIL import Image

im = Image.open('./static/uploads/gb2.GIF')
im_rgb = im.convert('RGB')
print(im_rgb.getpixel((0,0))[0])
# pix = im.load()
height, width = im.size
img = []
for i in range(height):
    img.append([])
    for j in range(width):
        img[i].append(im_rgb.getpixel((i,j))[0])
        # print(pix[i,j])

print(img)

# gb = cv2.imread('./static/uploads/gb2.jpg')
# height, width, channels = gb.shape
# img = np.zeros(shape=(len(gambar),height,width,channels))

# for i in range(0, len(gambar)):
#     gb = cv2.imread('./img/'+gambar[i])
#     img[i] = np.array(gb)