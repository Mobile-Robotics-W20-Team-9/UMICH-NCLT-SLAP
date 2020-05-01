from mpc_func import *
import sys

try:
    poses = load_poses(sys.argv[1])
except:
    print('Please use the right .csv file!')
sparseness = 100
sparse_poses = poses[1::sparseness, 1:3]

path = [148, 150, 151, 153, 154, 156, 158, 160, 162, 163]


dt = 1  # [s] discrete time
lr = 1.0  # [m]
T = 6  # number of horizon
max_speed = 5
min_speed = -5

speed_now = 1
theta = -1.5

path_poses = sparse_poses[path[:T+1], :]
u, next_x, xstar, ustar = path_poses_to_input(path_poses, speed_now, theta,
                                              dt, lr, T, max_speed, min_speed)


# plot the result
plt.figure(figsize=(10,10))
plt.subplot(3, 1, 1)
plt.plot(path_poses[0][0], path_poses[0][1], 'xb', label='current pose')
plt.plot(next_x[0], next_x[1], 'xr', label='next pose given current control output')
plt.plot(GetListFromMatrix(xstar.value[0, :]), GetListFromMatrix(
    xstar.value[1, :]), '-.', label='estimated trajectory given control outputs')
plt.plot(path_poses[:T,0], path_poses[:T,1], label='reference trajectory')
plt.axis("equal")
plt.xlabel("x[m]")
plt.ylabel("y[m]")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.cla()
plt.plot(GetListFromMatrix(xstar.value[2, :]), '-b',label='linear velocity')
plt.plot(GetListFromMatrix(xstar.value[3, :]), '-r',label='pose angle')
#plt.ylim([-1.0, 1.0])
plt.ylabel("velocity[m/s]")
plt.xlabel("horizon")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.cla()
plt.plot(GetListFromMatrix(ustar.value[0, :]), '-r', label="acceleration")
plt.plot(GetListFromMatrix(ustar.value[1, :]), '-b', label="beta")
#plt.ylim([-0.5, 0.5])
plt.legend()
plt.grid(True)
plt.show()
