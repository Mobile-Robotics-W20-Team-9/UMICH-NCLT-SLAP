import sys
import numpy as np
import pickle
import math  

def gpstoLocalFrame(lat, lng, alt):
    lat0 = 0.7381566413
    lng0 = -1.4610097151
    alt0 = 265.8

    dLat = np.deg2rad(lat) - lat0
    dLng = np.deg2rad(lng) - lng0
    dAlt = alt - alt0

    r = 6400000 # approx. radius of earth (m)
    y = r * np.cos(lat0) * np.sin(dLng)
    x = r * np.sin(dLat)
    z = dAlt

    return [x,y,z]
#Example
# x = gpstoLocalFrame(42.29360387311647,-83.71222615242006,272)
# print(x)

def buildingtoGPS(building):
    pickle_in = open('pickles/BuildingMappings.pkl',"rb")
    currDict = pickle.load(pickle_in)
    for place in currDict:
        if place == building:
            return currDict.get(building)
    return 0

def findClosestEntrance(building1, building2):
    gps1 = buildingtoGPS(building1)
    gps2 = buildingtoGPS(building2)

    x = [0,0,0,0]
    x[0] = calculateDistance(gps1[0][0],gps1[0][1],gps2[0][0],gps2[0][1])
    x[1] = calculateDistance(gps1[0][0],gps1[0][1],gps2[1][0],gps2[1][1])
    x[2] = calculateDistance(gps1[1][0],gps1[1][1],gps2[0][0],gps2[0][1])
    x[3] = calculateDistance(gps1[1][0],gps1[1][1],gps2[1][0],gps2[1][1])
    index = np.argmin(x)
    if index == 0:
        return [gps1[0],gps2[0]]
    elif index == 1:
        return [gps1[0],gps2[1]]
    elif index == 2:
        return [gps1[1],gps2[0]]
    else:
        return [gps1[1],gps2[1]]
# Example
# print(findClosestEntrance("BBB", "EECS"))

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

# Example usage of overall file
'''
GPScoords = findClosestEntrance("BBB", "EECS")
Building1 = gpstoLocalFrame(GPScoords[0][0], GPScoords[0][1], GPScoords[0][2])
Building2 = gpstoLocalFrame(GPScoords[1][0], GPScoords[1][1], GPScoords[1][2])
print(Building1)
print(Building2)
'''