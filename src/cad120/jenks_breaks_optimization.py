# from __future__ import print_function, division

import sys
import numpy as np
import cPickle as pickle
import timeit
import matplotlib.pyplot as plt

# code from http://danieljlewis.org/files/2010/06/Jenks.pdf
# described at http://danieljlewis.org/2010/06/07/jenks-natural-breaks-algorithm-in-python/

def getJenksBreaks( dataList, numClass ):
  dataList.sort()
  mat1 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat1.append(temp)
  mat2 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat2.append(temp)
  for i in range(1,numClass+1):
    mat1[1][i] = 1
    mat2[1][i] = 0
    for j in range(2,len(dataList)+1):
      mat2[j][i] = float('inf')
  v = 0.0
  for l in range(2,len(dataList)+1):
    s1 = 0.0
    s2 = 0.0
    w = 0.0
    for m in range(1,l+1):
      i3 = l - m + 1
      val = float(dataList[i3-1])
      s2 += val * val
      s1 += val
      w += 1
      v = s2 - (s1 * s1) / w
      i4 = i3 - 1
      if i4 != 0:
        for j in range(2,numClass+1):
          if mat2[l][j] >= (v + mat2[i4][j - 1]):
            mat1[l][j] = i3
            mat2[l][j] = v + mat2[i4][j - 1]
    mat1[l][1] = 1
    mat2[l][1] = v
  k = len(dataList)
  kclass = []
  for i in range(0,numClass+1):
    kclass.append(0)
  kclass[numClass] = float(dataList[len(dataList) - 1])
  countNum = numClass
  while countNum >= 2:#print "rank = " + str(mat1[k][countNum])
    id = int((mat1[k][countNum]) - 2)
    #print "val = " + str(dataList[id])
    kclass[countNum - 1] = dataList[id]
    k = int((mat1[k][countNum] - 1))
    countNum -= 1
  return kclass


def getGVF( dataList, numClass ):
  """
  The Goodness of Variance Fit (GVF) is found by taking the
  difference between the squared deviations
  from the array mean (SDAM) and the squared deviations from the
  class means (SDCM), and dividing by the SDAM
  """
  breaks = getJenksBreaks(dataList, numClass)
  dataList.sort()
  listMean = sum(dataList)/len(dataList)
  print listMean
  SDAM = 0.0
  for i in range(0,len(dataList)):
    sqDev = (dataList[i] - listMean)**2
    SDAM += sqDev
  SDCM = 0.0
  for i in range(0,numClass):
    if breaks[i] == 0:
      classStart = 0
    else:
      classStart = dataList.index(breaks[i])
      classStart += 1
    classEnd = dataList.index(breaks[i+1])
    classList = dataList[classStart:classEnd+1]
    classMean = sum(classList)/len(classList)
    print classMean
    preSDCM = 0.0
    for j in range(0,len(classList)):
      sqDev2 = (classList[j] - classMean)**2
      preSDCM += sqDev2
    SDCM += preSDCM
  return (SDAM - SDCM)/SDAM


# written by Drew
# used after running getJenksBreaks()
def classify(value, breaks):
  for i in range(1, len(breaks)):
    if value < breaks[i]:
      return i
  return len(breaks) - 1


def goodness_of_variance_fit(array, classes):
    # get the break points
    classes = getJenksBreaks(array, classes)

    # do the actual classification
    classified = np.array([classify(i, classes) for i in array])

    # max value of zones
    maxz = max(classified)

    # nested list of zone indices
    zone_indices = [[idx for idx, val in enumerate(classified) if zone + 1 == val] for zone in range(maxz)]

    # sum of squared deviations from array mean
    sdam = np.sum((array - array.mean()) ** 2)

    # sorted polygon stats
    array_sort = [np.array([array[index] for index in zone]) for zone in zone_indices]

    # sum of squared deviations of class means
    sdcm = sum([np.sum((classified - classified.mean()) ** 2) for classified in array_sort])

    # goodness of variance fit
    gvf = (sdam - sdcm) / sdam

    return gvf, classes


def jenks_break_optimization(data, gvf_thres=0.6, gvf=0.0, nclasses=1):
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    while gvf < gvf_thres and nclasses <= len(data):
        # print "computing gvf classes"
        gvf, classes = goodness_of_variance_fit(data, nclasses)
        # print nclasses, gvf, classes
        nclasses += 1
    return nclasses, gvf, classes

if __name__ == '__main__':
    data = [81.394102980498531, 60.745370193949761, 48.703182647543684, 46.518813398452032, 43.289721643826724, 41.048751503547585, 36.0, 29.614185789921695, 28.635642126552707, 27.0, 24.698178070456937, 24.0, 20.591260281974002, 17.029386365926403, 16.643316977093239, 16.15549442140351, 16.0, 15.132745950421556, 13.45362404707371, 13.152946437965905, 12.0, 12.0, 11.313708498984761, 10.04987562112089, 10.0, 10.0, 9.4339811320566032, 9.2195444572928871, 9.2195444572928871, 9.2195444572928871, 9.0553851381374173, 9.0, 8.6023252670426267, 8.6023252670426267, 8.5440037453175304, 8.0622577482985491, 8.0, 8.0, 8.0, 7.810249675906654, 7.6157731058639087, 7.6157731058639087, 7.6157731058639087, 7.2801098892805181, 7.2801098892805181, 7.2801098892805181, 7.2801098892805181, 7.2111025509279782, 7.0710678118654755, 7.0710678118654755, 7.0710678118654755, 7.0710678118654755, 7.0710678118654755, 7.0710678118654755, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.7082039324993694, 6.7082039324993694, 6.7082039324993694, 6.4031242374328485, 6.4031242374328485, 6.324555320336759, 6.324555320336759, 6.324555320336759, 6.0827625302982193, 6.0827625302982193, 6.0827625302982193, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.8309518948453007, 5.8309518948453007, 5.6568542494923806, 5.6568542494923806, 5.6568542494923806, 5.6568542494923806, 5.3851648071345037, 5.3851648071345037, 5.3851648071345037, 5.3851648071345037, 5.3851648071345037, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0990195135927845, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.4721359549995796, 4.2426406871192848, 4.2426406871192848, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.1231056256176606, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.6055512754639891, 3.6055512754639891, 3.6055512754639891, 3.6055512754639891, 3.6055512754639891, 3.6055512754639891, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.1622776601683795, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.8284271247461903, 2.8284271247461903, 2.8284271247461903, 2.8284271247461903, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.2360679774997898, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    print jenks_break_optimization(data)

    # jenks = getJenksBreaks(data, 1)
    # print jenks
    # print classify(80, jenks)
    # plt.scatter(range(len(data)), data)
    # plt.show()
