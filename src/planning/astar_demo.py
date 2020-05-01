import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.interpolate
from Astar import Astar, total_dist_fun

#Loading poses from the ground truth file
def load_poses(pose_gt_file) :
    pose_gt = np.loadtxt(pose_gt_file, delimiter = ",")
    return pose_gt[1:, 1:3]

poses = load_poses('../dataset/ground_truth/groundtruth_2012-01-08.csv')

#construct A* instance
astar = Astar(poses)

#Test A*
start_idx = np.random.randint(poses.shape[0])
goal_idx = np.random.randint(poses.shape[0])

path, optimal = astar.find_path(start_idx, goal_idx, sparseness=10, k=50)

np.save('path.npy', path)

#Plot computed path
plt.figure(figsize=(16,9))
plt.scatter(poses[:,1], poses[:,0], s=1)
plt.scatter(poses[path,1], poses[path,0], c='y', s=20)
plt.scatter(poses[start_idx,1], poses[start_idx,0], marker='o', c='g', s=500, label='start')
plt.scatter(poses[goal_idx,1], poses[goal_idx,0], marker='*', c='r', s=750, label='goal')
plt.legend()
plt.title('Ground Truth Position of Nodes with Overlaid A* Path')
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.axis('equal')
plt.savefig('astar_path.png')


