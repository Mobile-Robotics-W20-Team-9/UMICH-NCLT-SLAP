import numpy as np

#SE(2) functions
def matrix_log_SO2(SO2_mat) :
  #ln(R) in SO(3) = theta
  return np.arctan2(SO2_mat[1,0], SO2_mat[0, 0])

def matrix_log_SE2(SE2_mat) :
  theta = matrix_log_SO2(SE2_mat[0:2, 0:2])
  if (theta < 1e-6) :
    A = 1
    B = 0
  else :
    A = np.sin(theta)/theta
    B = (1-np.cos(theta))/theta

  v_inv = 1/(A**2 + B**2) * np.array([[A, B], [-B, A]])
  mat_log = np.array(np.matmul(v_inv, SE2_mat[0:2, 2]))
  mat_log = np.append(mat_log, theta)

  return mat_log

def matrix_exp_so2(theta) :
  #reconstruct R.
  return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

def matrix_exp_se2(twist) :
  theta = twist[-1]
  R = matrix_exp_so2(theta)
  
  #V converges to I2
  if (theta < 1e-6) :
    V = np.eye(2)
  else:
    V = 1/theta * np.array([[np.sin(theta), -(1 - np.cos(theta))], [(1-np.cos(theta)), np.sin(theta)]])

  mat_exp = np.zeros((3,3))
  mat_exp[0:2, 0:2] = R
  mat_exp[0:2, 2] = np.matmul(V, twist[0:2])
  mat_exp[2, 2] = 1
  
  return mat_exp

def get_twist_SE2(Xstart, pos_end, pos_future=None) :
  
  Xend = np.zeros((3,3))
  
  Xend[-1,-1] = 1
  Xend[0:2, 2] = pos_end
  
  #compute end direction (face in direction of future step i.e. end+1)
  if not pos_future is None:
    next_displacement = pos_future - pos_end
    next_theta = np.arctan2(next_displacement[1], next_displacement[0])
    Xend[0:2, 0:2] = np.array([[np.cos(next_theta), -np.sin(next_theta)], [np.sin(next_theta), np.cos(next_theta)]])
  else :
    Xend[0:2, 0:2] = Xstart[0:2, 0:2]

  # set_trace()
  twist_SE2 = matrix_log_SE2(np.matmul(np.linalg.inv(Xstart), Xend))

  return twist_SE2, Xend

def twist_motion(Xstart, twist, s=1) :
  return np.matmul(Xstart, s * matrix_exp_se2(twist))