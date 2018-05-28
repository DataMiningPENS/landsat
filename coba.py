import numpy as np
import cv2
import time
from scipy.spatial import distance

# Load an color image in grayscale
# 1. Ambil RGB
img = []
img.append(cv2.imread('img\gb1.jpg',0))
# img.append(cv2.imread('img\gb2.jpg',0))
# img.append(cv2.imread('img\gb3.jpg',0))
# img.append(cv2.imread('img\gb4.jpg',0))
# img.append(cv2.imread('img\gb5.jpg',0))
# img.append(cv2.imread('img\gb7.jpg',0))

gb = cv2.imread('img\gb1.jpg')
height, width, channels = gb.shape
# 2. Ubah gambar ke data pixel
data = []
cluster = []
ic=0
for x in range(0,25) :
    for y in range(0,25) :
        # untuk masing - masing gambar
        pxl = []
        for ig in img :
            pxl.append(ig[x][y])
        data.append(pxl)
        cluster.append([ic])
        ic=ic+1
# Collect Distance Data
dstn = []
for x in range(0,len(cluster)) :
    dd = []
    for y in range(0,len(cluster)) :
        if(y>x):
            d = distance.euclidean(data[x],data[y])
            dd.append(d)
        else:
            dd.append(0)
    dstn.append(dd)
# Clustering
timeA = int(round(time.time() * 1000))
while len(cluster) > 5:
    smallest=99999
    farSrcIdx = 0
    farTrgIdx = 0
    for src in range(0,len(cluster)):
        for trg in range(src+1,len(cluster)):
            farest = 0
            # For cluster Source
            for source in cluster[src]:
                for target in cluster[trg]:
                    # If found farther distance between 2 cluster
                    if(source>target): # 1,0 is not available
                        target,source = source,target
                    if(dstn[source][target]>farest):
                        farest = dstn[source][target]
                        farSrcIdx = src
                        farTrgIdx = trg
            # If farther distance between cluster is smallest between all cluster couple
            if(farest<smallest):
                smallest=farest
                smallestSrc = farSrcIdx
                smallestTrg = farTrgIdx
    cluster[smallestSrc]=cluster[smallestSrc]+cluster[smallestTrg]
    del cluster[smallestTrg]
print(cluster)
timeB = int(round(time.time() * 1000))
print("Time :",(timeB-timeA)*1000," ms")                        
                        

