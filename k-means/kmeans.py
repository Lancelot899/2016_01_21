#!/usr/bin/python
#coding = utf-8

from numpy import *

def loadDataSet(fileName, splitSign):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curline = line.strip().split(splitSign)
        fltline = map(float, curline)
        dataMat.append(fltline)
    return mat(dataMat)

def distance(vecA, vecB, p = 2):
    dist = sum(power(vecA - vecB, p))
    dist **= 1 / float(p)
    return dist

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    for j in xrange(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
    return mat(centroids)


def kMeans(dataSet, k, dis_p = 2, createCent = randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in xrange(m):
            minDist = inf; minIndex = -1
            for j in xrange(k):
                disJI = distance(centroids[j, :], dataSet[i, :], dis_p)
                if disJI < minDist:
                    minDist = disJI; minIndex = j
            if clusterAssment[i, 0] != minIndex: clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        print centroids
        for cent in xrange(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = mean(ptsInClust, axis = 0)
    return centroids, clusterAssment

def biKmeans(dataSet, k, dis_p = 2):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroid0 = mean(dataSet, axis = 0).tolist()[0]
    centList = [centroid0]
    for j in xrange(m):
        clusterAssment[j, 1] = distance(mat(centroid0), dataSet[j, :], dis_p) ** 2
    while (len(centList) < k):
        lowestSSE = inf
        for i in xrange((len(centList))):
                ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0], :]
                centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2)
                sseSplit = sum(splitClustAss[:,1])
                sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0], 1])
                print "sseSplit: %f, sseNotSplit: %f"%(sseSplit, sseNotSplit)
                if (sseSplit + sseNotSplit) < lowestSSE:
                    bestCentToSplit = i
                    bestNewCents = centroidMat
                    bestClustAss = splitClustAss.copy()
                    lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        centList[bestCentToSplit] = bestNewCents[0,:]
        centList.append(bestNewCents[1,:])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0], :] = bestClustAss
    return centList, clusterAssment
