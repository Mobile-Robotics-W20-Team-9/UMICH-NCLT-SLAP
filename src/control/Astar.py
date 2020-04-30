import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import math
import random
import time
import heapq  # https://docs.python.org/3/library/heapq.html


def load_poses(pose_gt_file) :
    pose_gt = np.loadtxt(pose_gt_file, delimiter = ",")

    return pose_gt


def plot_position(pose_gt):
    # NED (North, East, Down)
    x = pose_gt[:, 1]
    y = pose_gt[:, 2]
    z = pose_gt[:, 3]

    plt.figure()
    plt.scatter(y, x, 1, c=-z, linewidth=2)  # Note Z points down
    plt.axis('equal')
    plt.title('Ground Truth Position of Nodes in SLAM Graph')
    plt.xlabel('East (m)')
    plt.ylabel('North (m)')
    plt.colorbar()

    plt.show()

    return


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def find_path(cur_node, parent_idx, start_idx):
    next_idx = cur_node
    path = [next_idx]

    while next_idx != start_idx:
        next_idx = parent_idx[next_idx]
        path.append(next_idx)

    return path[::-1]


def Astar(start_idx, goal_idx, poses, k=20):
    visit_queue = PriorityQueue()
    visited_flag, queueed_flag = np.zeros(poses.shape[0]), np.zeros(poses.shape[0])
    g_score, h_score = np.full(poses.shape[0], np.inf), np.full(poses.shape[0], np.inf)
    parent_idx = np.zeros(poses.shape[0], dtype='int')

    test_tree = scipy.spatial.KDTree(poses)

    # initialize
    goal = poses[goal_idx]
    g_score[start_idx] = 0
    visit_queue.put(start_idx, np.inf)
    queueed_flag[start_idx] = 1

    while not visit_queue.empty():
        cur_node = visit_queue.get()
        visited_flag[cur_node] = 1

        if cur_node == goal_idx:
            print('find optimal path from {} to {}'.format(start_idx, goal_idx))
            break

        # find neighbours
        neighbors = test_tree.query(poses[cur_node], k=k)

        for nb_cur_dist, nb_idx in zip(neighbors[0][1:], neighbors[1][1:]):
            if visited_flag[nb_idx] == 1:
                continue

            temp_dist = g_score[cur_node] + np.linalg.norm(poses[cur_node] - poses[nb_idx])
            # temp_dist = g_score[cur_node] + nb_cur_dist     ## this not work
            if g_score[nb_idx] > temp_dist:
                g_score[nb_idx] = temp_dist
                parent_idx[nb_idx] = cur_node
                f_score = g_score[nb_idx] + np.linalg.norm(poses[nb_idx] - goal)

            # put into queen
            if queueed_flag[nb_idx] == 0:
                visit_queue.put(nb_idx, f_score)
                queueed_flag[nb_idx] = 1

    if cur_node != goal_idx:
        print('find closest path from {} to {}'.format(start_idx, cur_node))
    return cur_node, parent_idx