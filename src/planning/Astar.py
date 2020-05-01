import heapq #https://docs.python.org/3/library/heapq.html
import scipy.interpolate
import numpy as np


#Astar and path functions
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Astar :
  # This class implements A* search along a network defined by several points
  # Poses is an array of coordinates
  # k defines how many nearest neighbors to look at during A* search
  # The primary usage of this class is the find_path function:
  #   Required parameters:
  #     start_idx:  
  #     goal_idx    

  def __init__(self, poses) :
    self.poses = poses
    self.full_tree = scipy.spatial.KDTree(self.poses)

  def _extract_path(self, cur_node, parent_idx, start_idx, sparse_poses):
    next_idx = cur_node
    path = [self.full_tree.query(sparse_poses[next_idx])[1]]

    while next_idx != start_idx:
      next_idx = parent_idx[next_idx]
      path.append(self.full_tree.query(sparse_poses[next_idx])[1])
    
    return path[::-1]

  def find_path(self, full_start_idx, full_goal_idx, sparseness=1, k=5):
    sparse_poses = self.poses[0::sparseness, :]
    
    visit_queue = PriorityQueue()
    visited_flag, queueed_flag = np.zeros(sparse_poses.shape[0]), np.zeros(sparse_poses.shape[0])
    g_score, h_score = np.full(sparse_poses.shape[0], np.inf), np.full(sparse_poses.shape[0], np.inf)
    parent_idx = np.zeros(sparse_poses.shape[0], dtype='int')

    sparse_tree = scipy.spatial.KDTree(sparse_poses)

    start_idx = sparse_tree.query(self.poses[full_start_idx])[1]
    goal_idx = sparse_tree.query(self.poses[full_goal_idx])[1]
   
    # initialize
    goal = sparse_poses[goal_idx]

    g_score[start_idx] = 0
    visit_queue.put(start_idx, np.inf)
    queueed_flag[start_idx] = 1
    optimal = False

    while not visit_queue.empty():
      cur_node = visit_queue.get()
      visited_flag[cur_node] = 1

      if cur_node == goal_idx:
        optimal = True
        break

      # find neighbours
      neighbors = sparse_tree.query(sparse_poses[cur_node], k=k)

      for nb_cur_dist, nb_idx in zip(neighbors[0][1:], neighbors[1][1:]):
        if visited_flag[nb_idx] == 1:
          continue

        temp_dist = g_score[cur_node] + np.linalg.norm(sparse_poses[cur_node] - sparse_poses[nb_idx])
        # temp_dist = g_score[cur_node] + nb_cur_dist     ## this not work
        if g_score[nb_idx] > temp_dist:
          g_score[nb_idx] = temp_dist
          parent_idx[nb_idx] = cur_node
          f_score = g_score[nb_idx] + np.linalg.norm(sparse_poses[nb_idx] - goal)
        
        # put into queen
        if queueed_flag[nb_idx] == 0:
          visit_queue.put(nb_idx, f_score)
          queueed_flag[nb_idx] = 1

    path = self._extract_path(cur_node, parent_idx, start_idx, sparse_poses)    
    path[0] = full_start_idx
    path[-1] = full_goal_idx

    return path, optimal
  
  def find_local_path(self, start_pose, path, steps=5) :
    set_trace()

    path_tree = scipy.spatial.KDTree(self.poses[path])
    path_idx = path_tree.query(start_pose)[1]
    start_idx = self.full_tree.query(self.poses[path[path_idx]])[1]

    if path_idx + 5 < len(path) :
      goal_idx =self.full_tree.query(self.poses[path[path_idx + steps]])[1]
    else :
      goal_idx =self.full_tree.query(self.poses[path[-1]])[1]

    local_path, _ = self.find_path(start_idx, goal_idx)

    return local_path

def total_dist_fun(poses) :
  total_dist = 0
  curr_point = poses[0]

  for idx in range(1, poses.shape[0]) :
    total_dist += np.linalg.norm(curr_point - poses[idx])
    curr_point = poses[idx]
  
  return total_dist 
