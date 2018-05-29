
import pickle
import os
import sys
import warnings
import numpy as np
import cv2
import time
from scipy.spatial import distance
from sklearn import cluster as skcluster
import numpy
import time
sys.setrecursionlimit(1500)
start_time = time.time()


def load_image(gambar):
    gb = cv2.imread('./img/'+gambar[0])
    height, width, channels = gb.shape
    img = np.zeros(shape=(len(gambar),height,width,channels))

    for i in range(0, len(gambar)):
        gb = cv2.imread('./img/'+gambar[i])
        img[i] = np.array(gb)

    #     print(img[0][0][0])
    # print(len(img))

    return img

def convert_index(gambar, img):
    i=0
    size_x, size_y, count_image = len(img[0]), len(img[0][0]), len(img)
    data = np.zeros(shape=(size_x * size_y, count_image+1))
    cluster = []

    for x in range(0,size_x) :
        for y in range(0,size_y) :
            px = []
            for z in range(0,count_image) :
                px.append(img[z][x][y][0])
            px.append(i)
            data[i] = px
            cluster.append([i])
            i+=1
    
    return data, cluster

def dist(data, cluster):
    n = len(cluster)
    dstn = np.zeros(shape=(n, n))
    
    for x in range(0,len(cluster)) :
        dd = np.zeros(shape=(n))
        for y in range(0,len(cluster)) :
            if(y>x):
                dd[y] = distance.euclidean(data[x],data[y])
            else:
                dd[y] = 0
        dstn[x] = dd
    return dstn

def clustering(cluster):
    timeA = int(round(time.time() * 1000))
    
    while len(cluster) > 5:
        n = len(cluster)
        smallest=99999
        farSrcIdx = 0
        farTrgIdx = 0
        for src in range(0,n):
            for trg in range(src+1,n):
                farest = 0
                # For cluster Source
                print(src, trg)
                for source in cluster[src]:
                    for target in cluster[trg]:
                        
                        # If found farther distance between 2 cluster
                        if(source>target): # 1,0 is not available
                            target,source = source,target
                        if(dstn[int(source)][int(target)]>farest):
                            farest = dstn[int(source)][int(target)]
                            farSrcIdx = src
                            farTrgIdx = trg
                # If farther distance between cluster is smallest between all cluster couple
                if(farest<smallest):
                    smallest = farest
                    smallestSrc = farSrcIdx
                    smallestTrg = farTrgIdx 
        cluster[smallestSrc] = cluster[smallestSrc] + cluster[smallestTrg]
        del cluster[smallestTrg]
        # np.delete(cluster, smallestTrg)
    print(cluster)
    return cluster

def clustering_lib(data, img, num_cluster):
    result = skcluster.AgglomerativeClustering(n_clusters=num_cluster,linkage='complete').fit_predict(data)

    newCluster = []
    for y in range(0,len(img[0])):
        for x in range(0,len(img[0][0])):
            index = x + (y*32)
            newCluster.append([x,y,result[index]])

    return newCluster

gambar = ['gb1.jpg','gb2.jpg','gb3.jpg','gb4.jpg','gb5.jpg','gb7.jpg']
# gambar = ['gb1.jpg']
img = load_image(gambar)
print("--- load : %s seconds ---" % (time.time() - start_time))
data, cluster = convert_index(gambar, img)
print("--- data, cluster : %s seconds ---" % (time.time() - start_time))
# dstn = dist(data, cluster)
# print("--- dstn : %s seconds ---" % (time.time() - start_time))
# cluster = clustering(cluster)
# print("--- clustering : %s seconds ---" % (time.time() - start_time))
cluster = clustering_lib(data, img, 5)
print("--- clustering : %s seconds ---" % (time.time() - start_time))

