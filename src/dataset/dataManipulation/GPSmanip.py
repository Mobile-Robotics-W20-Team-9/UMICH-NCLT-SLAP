import sys
import numpy as np

# Usage: changes lat, long, alt into xyz local frame
#           This takes in lat, long, and alt and calculates xyz
# Example: print(gpstoLocalFrame(42.29360387311647,-83.71222615242006,272))
# Returns: array of XYZ coordinates in radians
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
    # WARNING: x and y may need to be flipped. Paper and example files from NCLT have contradictory usages
    y = r * np.cos(lat0) * np.sin(dLng)
    x = r * np.sin(dLat)
    z = dAlt

    return [x,y,z]
