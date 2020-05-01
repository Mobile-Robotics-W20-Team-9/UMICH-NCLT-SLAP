import PriorityQueue as pq
import numpy as np
import scipy.interpolate

class Astar :
  # This class implements A* search along a network defined by several points
  # Poses is an array of coordinates
  # k defines how many nearest neighbors to look at during A* search
  # The primary usage of this class is the find_path function:
  #   Required parameters:
  #     start_idx:  
  #     goal_idx    

  def __init__(self, poses, k=20) :
    self.poses = poses
    self.k = k

  def _extract_path(self, cur_node, parent_idx, start_idx):
    next_idx = cur_node
    path = [next_idx]

    while next_idx != start_idx:
      next_idx = parent_idx[next_idx]
      path.append(next_idx)

    return path[::-1]

  def find_path(self, start_idx, goal_idx):
    visit_queue = pq.PriorityQueue()
    visited_flag, queueed_flag = np.zeros(self.poses.shape[0]), np.zeros(self.poses.shape[0])
    g_score, h_score = np.full(self.poses.shape[0], np.inf), np.full(self.poses.shape[0], np.inf)
    parent_idx = np.zeros(self.poses.shape[0], dtype='int')

    test_tree = scipy.spatial.KDTree(self.poses)

    # initialize
    goal = self.poses[goal_idx]
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
      neighbors = test_tree.query(self.poses[cur_node], k=self.k)

      for nb_cur_dist, nb_idx in zip(neighbors[0][1:], neighbors[1][1:]):
        if visited_flag[nb_idx] == 1:
          continue

        temp_dist = g_score[cur_node] + np.linalg.norm(self.poses[cur_node] - self.poses[nb_idx])
        # temp_dist = g_score[cur_node] + nb_cur_dist     ## this not work
        if g_score[nb_idx] > temp_dist:
          g_score[nb_idx] = temp_dist
          parent_idx[nb_idx] = cur_node
          f_score = g_score[nb_idx] + np.linalg.norm(self.poses[nb_idx] - goal)
        
        # put into queen
        if queueed_flag[nb_idx] == 0:
          visit_queue.put(nb_idx, f_score)
          queueed_flag[nb_idx] = 1

    return self_.extract_path(cur_node, parent_idx, start_idx), optimal
