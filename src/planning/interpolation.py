import numpy as np
from Astar import total_dist_fun
import matplotlib.pyplot as plt

#Loading poses from the ground truth file
def load_poses(pose_gt_file) :
    pose_gt = np.loadtxt(pose_gt_file, delimiter = ",")
    return pose_gt[1:, 1:3]


if __name__ == "__main__" : 
  poses = load_poses('../dataset/ground_truth/groundtruth_2012-01-08.csv')
  path = np.load('path.npy')

  #Cubic interpolation of poses.

  poss = np.array(poses[path])
  velocities = np.zeros(poss.shape) 
  T = np.zeros(poss.shape[0])

  total_time = 100
  total_dist = total_dist_fun(poss)
  cum_dist = 0

  velocities[0] = 0

  for i in range(1, poss.shape[0] - 1) :
    seg_dist = np.linalg.norm(poss[i+1] - poss[i])
    velocities[i] = (((poss[i+1] - poss[i]) / seg_dist) + velocities[i-1])/2
    T[i] = total_time * cum_dist/total_dist
    cum_dist += seg_dist
    
  T[-1] = total_time
  velocities[-1] = 0

  a = np.zeros((poss.shape[0], 4, poss.shape[1]))

  for j in range(0, poss.shape[0]-1) :
    del_Tj = T[j+1] - T[j]
    a[j, 0] = poss[j]
    a[j, 1] = velocities[j]
    a[j, 2] = (3 * poss[j+1] - 3 * poss[j] - 2 * velocities[j] * del_Tj - velocities[j+1] * del_Tj)/ (del_Tj**2)
    a[j, 3] = (2 * poss[j] + (velocities[j] + velocities[j+1]) * del_Tj - 2 * poss[j + 1]) / (del_Tj**3)

  del_t = 0.005
  pos_x = [a[0,0][0]]
  pos_y = [a[0,0][1]]
  vel_x = [0]
  vel_y = [0]

  total_trial = 100

  for t in np.arange(del_t, total_trial, del_t) :
    j = np.argmax(T > t)-1
    delta_t = t - T[j]
    pos_t = a[j, 0] + a[j, 1]* delta_t + a[j, 2] * (delta_t**2) + a[j, 3] * (delta_t**3)
    pos_x.append(pos_t[0])
    pos_y.append(pos_t[1])
    vel_x.append((pos_x[-1] - pos_x[-2])/del_t)
    vel_y.append((pos_y[-1] - pos_y[-2])/del_t)

  t = np.arange(0, total_trial, del_t)

  plt.figure(figsize=(16,9))
  plt.plot(t[1:405], pos_x[1:405], linestyle='-', c='r', label='interpolated x position')
  # plt.scatter(t[0:400], pos_y[0:400], label='y position')

  plt.scatter(T[1:14], poss[1:14,0], c='b')
  plt.plot(T[1:14], poss[1:14,0], linestyle='-', c='g', label='no interpolation')
  # plt.scatter(T[0:10], poss[0:10,1], label='y no interp')

  plt.legend()
  plt.title('position with cubic interpolation of via points')
  plt.xlabel('Time (s)')
  plt.ylabel('Position (m)')
  plt.savefig('position.png')

  plt.figure()
  plt.scatter(t[2:500], vel_x[2:500])
  plt.scatter(t[2:500], vel_y[2:500])
  plt.savefig('velocity.png')
