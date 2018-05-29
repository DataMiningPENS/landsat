import matplotlib.pyplot as plt
import numpy as np
import json
import cv2
import time
from scipy.spatial import distance
from sklearn import cluster

class Dot:
    x = 0
    y = 0
    cluster = 0
    def __init__(self,x,y,cluster):
        self.x = x
        self.y = y
        self.cluster = cluster

# 1. Ambil RGB
img = []
img.append(cv2.imread('img\gb1.jpg',0))
img.append(cv2.imread('img\gb2.jpg',0))
img.append(cv2.imread('img\gb3.jpg',0))
img.append(cv2.imread('img\gb4.jpg',0))
img.append(cv2.imread('img\gb5.jpg',0))
img.append(cv2.imread('img\gb7.jpg',0))

gb = cv2.imread('img\gb1.jpg')
height, width, channels = gb.shape
# 2. Ubah gambar ke data pixel
data = []
for x in range(0,width) :
    for y in range(0,height) :
        # untuk masing - masing gambar
        pxl = []
        for ig in img :
            pxl.append(ig[x][y])
        data.append(pxl)

timeA = int(round(time.time() * 1000))
result = cluster.AgglomerativeClustering(n_clusters=5,linkage='complete').fit_predict(data)

newCluster = []
for y in range(0,height):
    for x in range(0,width):
        index = x + (y*32)
        newCluster.append(Dot(x,y,result[index]))
        
cc = 0
for cc in newCluster:
    print(cc.x,cc.y,cc.cluster)
timeB = int(round(time.time() * 1000))
print("Time :",(timeB-timeA)*1000," ms")