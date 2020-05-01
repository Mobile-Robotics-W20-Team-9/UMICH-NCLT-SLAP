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
from scipy.spatial.transform import Rotation as R


class GTPoses:
    def __init__(self, time_list, x_list, y_list, z_list, r_list, p_list, h_list):
        self.time_list = time_list
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.r_list = r_list
        self.p_list = p_list
        self.h_list = h_list
        self.length = len(time_list)

class PointCloud:
    def __init__(self, time):
        self.time = time
        self.x_list = []
        self.y_list = []
        self.z_list = []
        self.length = 0
    
    def add_point(self, x, y, z):
        self.x_list += [x]
        self.y_list += [y]
        self.z_list += [z]
        self.length += 1


def read_gt(file):
    gt = np.loadtxt(file, delimiter=",")
    
    time_list = list(gt[:, 0])
    x_list = gt[:, 1]
    y_list = gt[:, 2]
    z_list = gt[:, 3]
    r_list = gt[:, 4]
    p_list = gt[:, 5]
    h_list = gt[:, 6]

    return GTPoses(time_list, x_list, y_list, z_list, r_list, p_list, h_list)


def convert(x_s, y_s, z_s):
    scaling = 0.005 # 5 mm
    offset = -100.0

    x = x_s * scaling + offset
    y = y_s * scaling + offset
    z = z_s * scaling + offset

    return x, y, z


def read_vel(file):
    time = os.path.splitext(os.path.basename(file))[0]
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
    
    f_bin.close()
    return pc


def r_to_g_frame(gt, pc):
    pc_global = PointCloud(pc.time)
    
    # Interpolate gt to find corresponding pose for pc
    t_x = np.interp(x=pc.time, xp=gt.time_list, fp=gt.x_list)
    t_y = np.interp(x=pc.time, xp=gt.time_list, fp=gt.y_list)
    t_z = np.interp(x=pc.time, xp=gt.time_list, fp=gt.z_list)
    R_r = np.interp(x=pc.time, xp=gt.time_list, fp=gt.r_list)
    R_p = np.interp(x=pc.time, xp=gt.time_list, fp=gt.p_list)
    R_h = np.interp(x=pc.time, xp=gt.time_list, fp=gt.h_list)

    # Transform pc from robot frame to global frame
    r = (R.from_euler('xyz', [R_r, R_p, R_h], degrees=False)).as_matrix()
    p = [t_x, t_y, t_z]
    n = [r[0,0], r[1,0], r[2,0]]
    o = [r[0,1], r[1,1], r[2,1]]
    a = [r[0,2], r[1,2], r[2,2]]

    T = np.matrix([[n[0], o[0], a[0], p[0]],
                   [n[1], o[1], a[1], p[1]],
                   [n[2], o[2], a[2], p[2]],
                   [0, 0, 0, 1]])
    # T = np.matrix([[n[0], n[1], n[2], -np.dot(p, n)],
    #                [o[0], o[1], o[2], -np.dot(p, o)],
    #                [a[0], a[1], a[2], -np.dot(p, a)],
    #                [0, 0, 0, 1]])
    
    for i in range(pc.length):
        point_local = np.matrix([[pc.x_list[i]],
                                 [pc.y_list[i]],
                                 [pc.z_list[i]],
                                 [1]])
        point_global = T * point_local
        pc_global.add_point(point_global[0], point_global[1], point_global[2])

    return pc_global


def main(args):
    if len(sys.argv) != 3:
        print("Expecting 3 arguments: python point_cloud_vis.py [ground truth filepath] [velodyne sync folder]")
        return 1
    
    ground_truth_file = sys.argv[1]
    data_path = sys.argv[2]

    x_list = []
    y_list = []
    z_list = []
    gt = read_gt(ground_truth_file)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    count = -1

    for filename in os.listdir(data_path):
        count += 1

        if count == 50:
            break
        elif count % 5 != 0:
            continue

        pc = read_vel(data_path + '/' + filename)
        pc = r_to_g_frame(gt, pc)
        
        x_list += pc.x_list
        y_list += pc.y_list
        z_list += pc.z_list

    ax.scatter(x_list, y_list, z_list, c=z_list, s=5, linewidths=0)
    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
