import numpy as np
from SE2_utils import matrix_log_SE2, matrix_exp_se2, get_twist_SE2, twist_motion

#Loading poses from the ground truth file
def load_poses(pose_gt_file) :
    pose_gt = np.loadtxt(pose_gt_file, delimiter = ",")
    return pose_gt[1:, 1:3]

if __name__ == "__main__" : 
  poses = load_poses('../dataset/ground_truth/groundtruth_2012-01-08.csv')
  path = np.load('path.npy')
  
  print('testing exponential map for SE2')
  thetas = [0, 1e-4, np.pi/2, np.pi, 15*np.pi/8, 4.5 * np.pi]

  for theta in thetas :
    test_SE2 = np.array([[np.cos(theta), -np.sin(theta), 1.5], [np.sin(theta), np.cos(theta), 2], [0, 0, 1]])
    
    twist = matrix_log_SE2(test_SE2)
    SE2_res = matrix_exp_se2(twist)
    
    assert(np.sum(test_SE2 - SE2_res) < 1e-6)
    print('passed theta = ', theta)

  #Generation of twists and executing path
  print('testing motion twist generation')
  twists = []

  Xstart = np.eye(3)
  Xstart[0:2, 2] = poses[path[0]]

  poses = np.array(poses)

  for pose_idx, path_idx in enumerate(path[1:-1]) :
    twist, Xstart = get_twist_SE2(Xstart, poses[pose_idx], poses[path_idx + 1])
    twists.append(twist)
    #print(twist)

  twist, Xend = get_twist_SE2(Xstart, poses[-1])
  twists.append(twist)


  Xk = np.eye(3)
  Xk[0:2, 2] = poses[path[0]]

  for twist in twists :
    Xk = twist_motion(Xk, twist)

  assert(np.sum(Xk - Xend) < 1e-6)
  print('passed')