from PIL import Image
import numpy as np
import cv2
from scipy.spatial import distance
from sklearn import cluster as skcluster
import random, string

class ImageProcess  :
    def get_num_pixels(filepath):
        width, height = Image.open(open(filepath)).size
        return width*height

    def load_image(gambar):
        gb = Image.open('./static/uploads/'+gambar[0])
        height, width = gb.size
        img = np.zeros(shape=(len(gambar),height,width))

        for i in range(0, len(gambar)):
            gb = Image.open('./static/uploads/'+gambar[i])
            # pixels = list(gb.getdata())
            # img[i] = [pixels[i:i+width] for i  in range(0, len(pixels), width)]

            pix = gb.load()
            for j in range(height):
                for k in range(width):
                    img[i][j][k] = pix[j,k]

        #     print(img[0][0][0])
        # print(len(img))

        return img

    def convert_index(gambar, img):
        i=0
        size_x, size_y, count_image = len(img[0]), len(img[0][0]), len(img)
        data = np.zeros(shape=(size_x * size_y, count_image))
        cluster = []

        for x in range(0,size_x) :
            for y in range(0,size_y) :
                px = []
                for z in range(0,count_image) :
                    px.append(img[z][y][x])
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
        return cluster
        
    def clustering_lib(data, img, num_cluster):
        result = skcluster.AgglomerativeClustering(n_clusters=num_cluster,linkage='complete').fit_predict(data)

        newCluster = []
        for y in range(0,len(img[0])):
            for x in range(0,len(img[0][0])):
                index = x + (y*32)
                newCluster.append([x,y,result[index]])

        return newCluster

    def random_color():
        rgbl=[255,0,0]
        random.shuffle(rgbl)
        return tuple(rgbl)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def generate_image(cluster, img, num_cluster):
        color = []
        for i in range(0, num_cluster):
            temp = tuple(list(np.random.choice(range(256), size=3)))
            color.append(temp)

        im = Image.new("RGB", (len(img[0][0]), len(img[0])))
        for i in range(len(cluster)):
            print(cluster[i])
            im.putpixel((cluster[i][0],cluster[i][1]), color[cluster[i][2]])

        chars=string.ascii_uppercase + string.digits
        id = ''.join(random.choice(chars) for _ in range(10))
        im.save('./static/result/'+id+'.png')

        return id

    def coba():
        # print get_num_pixels("/path/to/my/file.jpg")
        print("Hello")