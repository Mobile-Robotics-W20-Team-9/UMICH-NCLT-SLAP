import sys
import numpy as np
import pickle
import math  

# Example usage of overall file to find xyz coordinates of two buildings given name as string
'''
GPScoords = findClosestEntrance("BBB", "EECS")
Building1 = gpstoLocalFrame(GPScoords[0][0], GPScoords[0][1], GPScoords[0][2])
Building2 = gpstoLocalFrame(GPScoords[1][0], GPScoords[1][1], GPScoords[1][2])
print(Building1)
print(Building2)
'''

# Usage: finds building coordinates in lat, long, and alt in degrees
#           This takes in two building names as strings and returns 
#           closest two entrances 
# Example: GPScoords = findClosestEntrance("BBB", "EECS")
#           print(GPScoords[0][0]) #returns latitutde of first building
# Returns: 2x2 array of two GPS coordinates in lat, long, and alt in degrees
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

# Usage: finds building coordinates in lat, long, and alt in degrees
#           This takes in a building name and looks up coordinates in pickle file
# Example: buildingsGPScoords = buildingtoGPS(building1)
#           print(buildingGPScoords[0]) #returns latitutde of the building
# Returns: array of GPS coordinates (lat, long, and alt) in degrees
def buildingtoGPS(building):
    pickle_in = open('pickles/BuildingMappings.pkl',"rb")
    currDict = pickle.load(pickle_in)
    for place in currDict:
        if place == building:
            return currDict.get(building)
    return 0

# Usage: changes lat, long, alt into xyz local frame
#           This takes in lat, long, and alt and calculates xyz
# Example: print(gpstoLocalFrame(42.29360387311647,-83.71222615242006,272))
# Returns: array of XYZ coordinates in radians
def gpstoLocalFrame(lat, lng, alt):
    lat0 = 0.7381566413
    lng0 = -1.4610097151
    alt0 = 265.8

    dLat = np.deg2rad(lat) - lat0
    dLng = np.deg2rad(lng) - lng0
    dAlt = alt - alt0

    r = 6400000 # approx. radius of earth (m)
    # WARNING: x and y may need to be flipped. Paper and example files from NCLT have contradictory usages
    y = r * np.cos(lat0) * np.sin(dLng) 
    x = r * np.sin(dLat)
    z = dAlt

    return [x,y,z]

# Usage: Euclidean distance calculator - helper function
def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

     