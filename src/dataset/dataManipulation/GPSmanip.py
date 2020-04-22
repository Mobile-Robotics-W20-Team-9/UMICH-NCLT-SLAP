import sys
import numpy as np


def gpstoLocalFrame(lat, lng, alt):
    lat0 = 0.7381566413
    lng0 = -1.4610097151
    alt0 = 265.8

    print(np.deg2rad(lng))
    dLat = np.deg2rad(lat) - lat0
    print(dLat)
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
