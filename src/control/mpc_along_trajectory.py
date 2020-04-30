from mpc_func import *
from Astar import *

poses = load_poses('pose_gt.csv')
sparseness = 100
# print(poses.shape[0]/sparseness)
# plot_position(poses[1::sparseness])
sparse_poses = poses[1::sparseness, 1:3]

start_idx = np.random.randint(sparse_poses.shape[0])
goal_idx = np.random.randint(sparse_poses.shape[0])

# start_idx = 148
# goal_idx = 6976
# start_time = time.time()
cur_node, parent_idx = Astar(start_idx, goal_idx, sparse_poses, k=20)
path = find_path(cur_node, parent_idx, start_idx)
# print(time.time() - start_time)
#print(start_idx, goal_idx)
#print(path)
# print(len(path))
# print(total_dist(path))

plt.figure(figsize=(10,10))
plt.scatter(sparse_poses[:,0], sparse_poses[:,1], s=8)
plt.scatter(sparse_poses[path,0], sparse_poses[path,1], c='y', s=80)
plt.scatter(sparse_poses[start_idx,0], sparse_poses[start_idx,1], marker='o', c='g', s=200, label='start')
plt.scatter(sparse_poses[goal_idx,0], sparse_poses[goal_idx,1], marker='*', c='r', s=200, label='goal')
plt.legend()
plt.show()


# along trajectory
path_poses = sparse_poses[path, :]

dt = 1  # [s] discrete time
lr = 1.0  # [m]
T = 6  # number of horizon
max_speed = 5
min_speed = -5

speed_now = 1
theta = -1.5

for interval in range(len(path)//T):
  short_path_poses = path_poses[interval*T:(interval+1)*T,:]
  u, next_x, xstar, ustar = path_poses_to_input(path_poses, speed_now, theta,
                                                dt, lr, T, max_speed, min_speed)
  speed_now = xstar.value[2,-1]
  theta = xstar.value[3,-1]
  print(ustar.value)
