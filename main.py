import math
import random
import matplotlib.pyplot as plt


def readfile(filename:str)->dict:
    testset = {}
    file = open(filename)
    for line in file.readlines():
        splited = line.split(',')
        values = []
        for i in range(len(splited)-1):
            values.append(float(splited[i]))
        testset[tuple(values)] = splited[len(splited)-1]
    return testset

def getlen(point1:tuple, point2:tuple) -> float:
    x = 0
    for i in range(len(point1)):
        x += math.pow(point1[i]-point2[i],2)
    return math.sqrt(x)

def assignToCentroid(points:list, centroids:list)->dict:
    pointsToCentroids = {}
    for i in centroids:
        for j in points:
            pointLen = getlen(tuple(i), tuple(j))
            if j in list(pointsToCentroids.keys()):
                if pointLen < getlen(pointsToCentroids[j], i):
                    pointsToCentroids[j] = i
            else:
                pointsToCentroids[j] = i
    return pointsToCentroids


def calcCentroid(centroidMapping:dict, centroids:list):
    newCentroids = []
    for i in centroids:
        mappinglist = []
        newCentroid = [0 for x in range(len(i))]
        for j in centroidMapping.keys():
            if centroidMapping[j] == i:
                mappinglist.append(j)
        for k in mappinglist:
            for m in range(len(k)):
                newCentroid[m] += k[m]
        finalCentroid = []
        for l in newCentroid:
            finalCentroid.append(l/len(mappinglist))
        newCentroids.append(finalCentroid)

    return newCentroids
            


def trainForEpoch(trainset:dict, centroids):
    points = assignToCentroid(trainset.keys(),centroids)
    newCentroids = calcCentroid(points,centroids)
    return newCentroids
            

def getLoss(trainset:dict, centroids:list):
    len_sum = 0
    mapping = assignToCentroid(trainset.keys(), centroids)
    for i in list(mapping.keys()):
        len_sum += getlen(i,mapping[i])
    return len_sum


def main():
    k = 3
    trainset = readfile('iris.data')
    centroids = []
    for i in range(k):
        centroids.append(random.choice(list(trainset.keys())))
    print(centroids)
    print('loss ',getLoss(trainset,centroids))
    centroids = trainForEpoch(trainset,centroids)
    print(centroids)
    print('loss ',getLoss(trainset,centroids))
    finds = 1
    while(finds!=0):
        new_centroids = trainForEpoch(trainset,centroids)
        print('centroids', centroids)
        print('new nentroids ',new_centroids)
        print('loss ',getLoss(trainset,new_centroids))
        is_equal = False
        for i,j in zip(new_centroids,centroids):
            if i == j:
                is_equal = True
            else:
                is_equal = False
        if is_equal:
            finds -= 1
        centroids = new_centroids
    mapping = assignToCentroid(trainset.keys(),centroids)

    print('final groups \n', mapping)


if __name__ == '__main__':
    main()