# !/usr/bin/python
#
#   python point_cloud_vis.py \
#          /PATH/TO/ground_truth.csv \
#          /PATH/TO/velodyne_sync

import sys
import os
import struct
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class GTPose:
    def __init__(self, time, x, y, z, r, p, h):
        self.time = time
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.p = p
        self.h = h

class PointCloud:
    def __init__(self, time):
        self.time = time
        self.x_list = []
        self.y_list = []
        self.z_list = []
    
    def add_point(self, x, y, z):
        self.time += time
        self.x_list += x
        self.y_list += y
        self.z_list += z


def read_gt(file):
    gt = np.loadtxt(file, delimeter=",")
    
    time = gt[:, 0]
    x = gt[:, 1]
    y = gt[:, 2]
    z = gt[:, 3]
    r = gt[:, 4]
    p = gt[:, 5]
    h = gt[:, 6]

    return GTPose(time, x, y, z, r, p, h)


def convert(x_s, y_s, z_s):
    scaling = 0.005 # 5 mm
    offset = -100.0

    x = x_s * scaling + offset
    y = y_s * scaling + offset
    z = z_s * scaling + offset

    return x, y, z


def read_vel(file):
    time = os.path.splittext(os.path.basename(file))[0]
    pc = PointCloud(time)
    f_bin = open(file, "rb")
    
    while True:
        x_str = f_bin.read(2)

        if x_str == b'': # eof
            break
        
        x = struct.unpack('<H', x_str)[0]
        y = struct.unpack('<H', f_bin.read(2))[0]
        z = struct.unpack('<H', f_bin.read(2))[0]
        i = struct.unpack('B', f_bin.read(1))[0]
        l = struct.unpack('B', f_bin.read(1))[0]

        # TODO: Be careful about z being flipped when plotting the velodyne data
        x, y, z = convert(x, y, z)
        pc.add_point(x, y, -z)
    
    return pc


def r_to_g_frame(gt, pc):
    # TODO: Interpolate gt to find corresponding pose for pc

    # TODO: Transform pc from robot frame to global frame
    pass


def main(args):
    if len(sys.argv) != 2:
        print("Expecting 2 arguments: ground truth filepath and data folder")
        return 1
    
    ground_truth_file = sys.arv[1]
    data_path = sys.argv[2]

    x = []
    y = []
    z = []
    gt = read_gt(ground_truth_file)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for filename in os.listdir(data_path):
        pc = read_vel(ground_truth_file, data_path + '/' + filename)
        pc = r_to_g_frame(gt, pc)
        
        x += pc.x_list
        y += pc.y_list
        z += pc.z_list

    ax.scatter(x, y, z, c=z, s=5, linewidths=0)
    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
