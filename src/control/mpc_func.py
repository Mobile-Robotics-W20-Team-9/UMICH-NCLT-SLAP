import cvxpy
import numpy as np
from cvxpy import *
import matplotlib.pyplot as plt
from math import *
import time


def LinearizeCarModel(xb, u, dt, lr):
    x = xb[0]
    y = xb[1]
    v = xb[2]
    theta = xb[3]

    a = u[0]
    beta = u[1]

    t1 = -dt * v * sin(theta + beta)
    t2 = dt * v * cos(theta + beta)

    A = np.eye(xb.shape[0])
    A[0, 2] = dt * cos(theta + beta)
    A[1, 2] = dt * sin(theta + beta)
    A[3, 2] = dt * sin(beta) / lr
    #A[0, 3] = t1
    #A[1, 3] = t2

    B = np.zeros((xb.shape[0], u.shape[0]))
    B[2, 0] = dt
    B[0, 1] = t1
    B[1, 1] = t2
    B[3, 1] = dt * v * cos(beta) / lr

    tm = np.zeros((4, 1))
    tm[0, 0] = v * cos(theta + beta) * dt
    tm[1, 0] = v * sin(theta + beta) * dt
    tm[2, 0] = a * dt
    tm[3, 0] = v / lr * sin(beta) * dt
    C = xb + tm
    C = C - A @ xb - B @ u

    # print(A, B, C)

    return A, B, C


def NonlinearModel(x, u, dt, lr):
    print(x.value)
    x[0] = x[0] + x[2] * cos(x[3] + u[1]) * dt
    x[1] = x[1] + x[2] * sin(x[3] + u[1]) * dt
    x[2] = x[2] + u[0] * dt
    x[3] = x[3] + x[2] / lr * sin(u[1]) * dt

    return x


def CalcInput(A, B, C, x, u, T, max_speed, min_speed, path_poses):

    x_0 = x[:]
    x = Variable((x.shape[0], T + 1))
    u = Variable((u.shape[0], T))

    # MPC controller
    states = []
    constr = [x[:, 0] == (x_0.T)[0]]#, x[2, T] == 0.0]
    for t in range(1,T):
        #pdb.set_trace()
        
        constr += [x[:, t + 1] == A * x[:, t] + B * u[:, t] +(C.T)[0]]
        constr += [abs(u[:, t]) <= 5]
        constr += [x[2, t + 1] <= max_speed]
        constr += [x[2, t + 1] >= min_speed]
        #  cost = sum_squares(u[:,t])
        cost = sum_squares(abs(x[0, t] - path_poses[t][0])) * 1 * (10-2*t)
        cost += sum_squares(abs(x[1, t] - path_poses[t][1])) * 1 * (10-2*t)
        cost += sum_squares(abs(u[1, t])) * 10 * (t+1)
        if t == T - 1:
            cost += (x[0, t + 1] - path_poses[t][0]) ** 2 * 100.0
            cost += (x[1, t + 1] - path_poses[t][1]) ** 2 * 100.0

        states.append(Problem(Minimize(cost), constr))

    prob = sum(states)
    #pdb.set_trace()
    #prob.constraints += [x[:, 0] == (x_0.T)[0]]#, x[2, T] == 0.0]

    start = time.time()
    #  result=prob.solve(verbose=True)
    result = prob.solve()
    elapsed_time = time.time() - start
    # print("calc time:{0}".format(elapsed_time) + "[sec]")
    # print(prob.value)

    if prob.status != OPTIMAL:
        print("Cannot calc opt")

    #  print(prob.status)
    return u, x, prob.value


def GetListFromMatrix(x):
    return np.array(x).flatten().tolist()


def path_poses_to_input(path_poses, speed_now, theta, dt, lr, T, max_speed, min_speed):
    x0 = np.array([[path_poses[0][0], path_poses[0][1], speed_now, theta]]).T  # [x,y,v theta]
    u = np.array([[0.0, 0.0]]).T  # [a,beta]

    x = x0

    A, B, C = LinearizeCarModel(x, u, dt, lr)
    ustar, xstar, cost = CalcInput(A, B, C, x, u, T, max_speed, min_speed, path_poses)

    u[0, 0] = GetListFromMatrix(ustar.value[0, :])[0]
    u[1, 0] = float(ustar[1, 0].value)

    x = A @ x + B @ u

    return u, x, xstar, ustar


def load_poses(pose_gt_file) :
    pose_gt = np.loadtxt(pose_gt_file, delimiter = ",")

    return pose_gt

