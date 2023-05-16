import sys

import dbfs as dbf
import schedulability as s
from generate_tasks import Task, Task_Set
from collections import deque

def is_eligible(task_set):
  return not task_set.thm1 and task_set.thm2

def initialize_candidates(task_set):
  candidates = [False] * task_set.num_tasks

  for task in task_set.hi_tasks_list:
    candidates[task.ID] = True

  return candidates

def find_candidate(candidates, task_set, heuristic):
  return heuristic(candidates, task_set)

def find_candidate_queue(candidates, task_set, heuristic):
  candidate_queue = deque()
  potential_candidates = deque([i for i, eligible in enumerate(candidates) if eligible])
  
  while len(potential_candidates) > 0:
    best_candidate_id = heuristic(potential_candidates, task_set)
    candidate_queue.append(best_candidate_id)
    potential_candidates.remove(best_candidate_id)

  return candidate_queue

def max_diff_wcet_queue(candidates, task_set):
  max_wcet_difference = 0
  best_candidate_id = -1

  for i in candidates:
    wcet_difference = task_set.task_set[i].C_HI - task_set.task_set[i].C_LO
    if wcet_difference > max_wcet_difference:
      max_wcet_difference = wcet_difference
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def max_diff_wcet(candidates, task_set):
  max_wcet_difference = 0
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible:
      wcet_difference = task_set.task_set[i].C_HI - task_set.task_set[i].C_LO
      if wcet_difference > max_wcet_difference:
        max_wcet_difference = wcet_difference
        best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def earliest_deadline(candidates, task_set):
  min_deadline = 401
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].D < min_deadline:
      min_deadline = task_set.task_set[i].D
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def smallest_sep_time(candidates, task_set):
  small_min_sep_time = sys.maxsize
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].T < small_min_sep_time:
      small_min_sep_time = task_set.task_set[i].T
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def shortest_wcet_lo(candidates, task_set):
  min_wcet_lo = 25
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].C_LO < min_wcet_lo:
      min_wcet_lo = task_set.task_set[i].C_LO
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def longest_wcet_hi(candidates, task_set):
  max_wcet_hi = 0
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].C_HI > max_wcet_hi:
      max_wcet_hi = task_set.task_set[i].C_HI
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def min_diff_wcet_hi_deadline(candidates, task_set):
  max_wcet_hi = 0
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].C_HI > max_wcet_hi:
      max_wcet_hi = task_set.task_set[i].C_HI
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def get_failure_time(task_set, start_i = 2, start_j = 1):
  for i in range(start_i, task_set.t_max + 1):
    for j in range(start_j, i):
      demand = dbf.sum_dbf(task_set, i, j)
      if demand > i:
        return i, j
  
  return -1, -1

def greedy_search(task_set, heuristic):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  candidates = initialize_candidates(task_set)
  best_candidate = -1
  candidates_count = len(task_set.hi_tasks_list)
  i, j = get_failure_time(task_set)
  # print("starting", candidates_count, i, j)

  while candidates_count > 0: 
    # find candidate
    best_candidate = find_candidate(candidates, task_set, heuristic) if candidates_count > 0 else -1
    # print("candidate info: best {}, candidate count {}, candidate boolean array {}".format(best_candidate, candidates_count, candidates))
    if best_candidate < 0: return ("No more eligible candidates", task_set) 
    
    # reduce tight_D
    previous_tight_D = task_set.task_set[best_candidate].tight_D
    task_set.task_set[best_candidate].tight_D = j if j > task_set.task_set[best_candidate].C_LO and previous_tight_D > j else task_set.task_set[best_candidate].C_LO
    # print(best_candidate, task_set.task_set[best_candidate].tight_D)
    # backtrack if reducing tight_D broke thm2
    if not s.schedulability_test_thm2(task_set):
      task_set.task_set[best_candidate].tight_D = previous_tight_D
      candidates[best_candidate] = False
      candidates_count -= 1
      continue
    
    # check if sched 1 test will now pass or if it fails at another time
    i, j = get_failure_time(task_set)
    if (i, j) == (-1, -1): 
      return (True, task_set) # sched 1 test is true now
    
    # remove candidate if tight_D reached limit
    if task_set.task_set[best_candidate].tight_D <= task_set.task_set[best_candidate].C_LO:
      candidates[best_candidate] = False
      candidates_count -= 1

  return ("No more eligible candidates", task_set) 

def greedy_search_bfs(task_set, heuristic):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  candidates = initialize_candidates(task_set)
  candidate_queue = find_candidate_queue(candidates, task_set, max_diff_wcet_queue)
  i, j = get_failure_time(task_set)
  # print("starting", candidate_queue, i, j)

  while len(candidate_queue) > 0: 
    # find candidate
    best_candidate = candidate_queue.popleft() if len(candidate_queue) > 0 else -1
    # print("candidate info: best {}, candidate count {}, candidate boolean array {}".format(best_candidate, len(candidate_queue), candidate_queue))
    if best_candidate < 0: return ("No more eligible candidates", task_set) 
    
    # reduce tight_D
    previous_tight_D = task_set.task_set[best_candidate].tight_D
    task_set.task_set[best_candidate].tight_D = j if j > task_set.task_set[best_candidate].C_LO and previous_tight_D > j else task_set.task_set[best_candidate].C_LO
    
    # backtrack if reducing tight_D broke thm2
    if not s.schedulability_test_thm2(task_set):
      task_set.task_set[best_candidate].tight_D = previous_tight_D
      continue
    
    # check if sched 1 test will now pass or if it fails at another time
    i, j = get_failure_time(task_set)
    if (i, j) == (-1, -1): 
      return (True, task_set) # sched 1 test is true now
    
    # queue candidate if tight_D has not reached limit
    if task_set.task_set[best_candidate].tight_D > task_set.task_set[best_candidate].C_LO:
      candidate_queue.append(best_candidate)

  return ("No more eligible candidates", task_set) 

if __name__ == "__main__":
  task_set_dict = {'num_tasks': 6, 
                   't_max': 501, 
                   'utilization': 0.5965283208825148, 
                   'thm1': False, 
                   'thm2': True, 
                   'thm3': True, 
                   'lo_tasks_list': [Task(1, 70, 15, 15, 44, 44), Task(2, 196, 12, 12, 153, 153), Task(3, 71, 9, 9, 154, 154), Task(4, 72, 6, 6, 154, 154)],
                   'hi_tasks_list': [Task(0, 479, 10, 32, 140, 140), Task(5, 211, 19, 69, 97, 97)]
  }  
  task_set = Task_Set(ts_dict = task_set_dict)

  print(task_set)
  # print(s.schedulability_test_thm1(task_set))
  # print(get_failure_time(task_set))

  # eligibility2, post_greedy1_task_set = greedy_search(task_set, max_diff_wcet)
  eligibility, post_greedy_task_set = greedy_search_bfs(task_set, max_diff_wcet)

  print("greedy result is", eligibility)
  print(post_greedy_task_set)
  # print(post_greedy1_task_set)
  print(s.schedulability_test_thm1(post_greedy_task_set))
  print(get_failure_time(post_greedy_task_set))
  
  # i, j = get_failure_time(task_set)
  # id = 1
  # print("before: sum {} co {} lo {} lower {} upper {}".format(dbf.sum_dbf(task_set, i, j), dbf.sum_dbf_CO(task_set, i, j), dbf.sum_dbf_LO(task_set, j), dbf.lower(task_set.task_set[id], j), dbf.upper_CO(task_set.task_set[id], i, j)))
  # task_set.task_set[id].tight_D = j
  # print("after: sum {} co {} lo {} lower {} upper {}".format(dbf.sum_dbf(task_set, i, j), dbf.sum_dbf_CO(task_set, i, j), dbf.sum_dbf_LO(task_set, j), dbf.lower(task_set.task_set[id], j), dbf.upper_CO(task_set.task_set[id], i, j)))

  # h.plot_greedy_search(task_set)
#   t, ts = get_failure_time(task_set)

#   before = dbf.sum_dbf(task_set, t, ts)
#   before_sums = [dbf.sum_dbf(task_set, t, y) for y in range(t)] 


#   after = dbf.sum_dbf(post_greedy_task_set, t, ts)
#   after_sums = [dbf.sum_dbf(post_greedy_task_set, t, y) for y in range(t)] 

#   print("Time of failure: {}, {}".format(t, ts))
#   print(task_set)
#   print("demand before", before)

#   print("demand after", after)
#   print("after")
#   print(post_greedy_task_set)
  
#   plt.plot(before_sums, label = "before")
#   plt.plot(after_sums, label = "after")

#   plt.legend()
#   plt.show()
  # hi = [dbf.sum_dbf_HI(task_set_eligible, i, y) for y in range(i)] 
  # plt.plot(hi, label = "hi before")


  # task_set_eligible.task_set[0].tight_D = task_set_eligible.task_set[0].C_LO
  # task_set_eligible.task_set[3].tight_D = task_set_eligible.task_set[3].C_LO

  # lo = [dbf.sum_dbf_LO(task_set_eligible, y) for y in range(i)] 
  # # hi = [dbf.sum_dbf_HI(task_set_eligible, i, y) for y in range(i)] 
  # co = [dbf.sum_dbf_CO(task_set_eligible, i, y) for y in range(i)] 
  # un = [dbf.sum_dbf_UN(task_set_eligible, i, y) for y in range(i)] 




  


  # # plt.plot(lo, label = "lo")
  # # # plt.plot(hi, label = "hi")
  # # plt.plot(co, label = "co")
  # # plt.plot(un, label = "un")
  # # plt.plot(after_sums, label = "after")
  # # plt.plot(after_sums, label = "after")


