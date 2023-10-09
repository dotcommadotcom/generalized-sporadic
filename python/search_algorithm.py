from collections import deque

import dbfs as dbf
import schedulability as s

def is_eligible(task_set):
  return not task_set.thm1 and task_set.thm2 and task_set.thm3

def initialize_candidates(task_set):
  return deque([task.ID for task in sorted([task for task in task_set.hi_tasks_list], key = lambda task: task.C_HI - task.C_LO, reverse = True)])

def get_failure_time(task_set):
  for i in range(2, task_set.t_max + 1):
    for j in range(1, i):
      if dbf.sum_dbf(task_set, i, j) > i:
        return i, j
  
  return -1, -1

def is_demand_at_minimum(T, C_LO, D, ts):
  return ts < C_LO or ts - ((ts - 1)//T) * T > D

def find_optimal_tight_D(T, C_LO, previous_tight_D, ts):
  for n in range((ts - 1)//T + 1):
    if C_LO <= ts - n * T < previous_tight_D:
      return ts - n * T

  return previous_tight_D

def tighten_deadline(task_set):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  candidates = initialize_candidates(task_set)
  best_candidate = -1
  t, ts = get_failure_time(task_set)

  while len(candidates) > 0: 
    # Find best candidate with max(C_HI - C_LO) 
    best_candidate = candidates.popleft() if len(candidates) > 0 else -1
    if best_candidate < 0: return ("No more eligible candidates", task_set) 

    T, C_LO, D, previous_tight_D = task_set.task_set[best_candidate].T, task_set.task_set[best_candidate].C_LO, task_set.task_set[best_candidate].D, task_set.task_set[best_candidate].tight_D

    # Check if tightening best candidate deadline can reduce demand
    if is_demand_at_minimum(T, C_LO, D, ts):
      continue

    # Tighten best candidate deadline to ts - n * T 
    task_set.task_set[best_candidate].tight_D = find_optimal_tight_D(T, C_LO, previous_tight_D, ts)
    if task_set.task_set[best_candidate].tight_D == previous_tight_D:
      continue

    # Backtrack if tightening deadline causes theorem 2 or 3 to be false
    if not (s.schedulability_test_thm2(task_set) and s.schedulability_test_thm3(task_set)):
      task_set.task_set[best_candidate].tight_D = previous_tight_D
      continue
    
    # Check if theorem 1 is True with tightened deadline or if theorem 1 fails at another time
    t, ts = get_failure_time(task_set)
    if (t, ts) == (-1, -1): 
      return (True, task_set) # Task set is now schedulable with tightened deadline
    
    candidates.appendleft(best_candidate)

  return ("No more eligible candidates", task_set) 

def naive(task_set):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  # Get all HI tasks 
  candidates = deque([task.ID for task in task_set.hi_tasks_list])
  best_candidate = -1
  t, ts = get_failure_time(task_set)

  while len(candidates) > 0: 
    best_candidate = candidates.popleft() if len(candidates) > 0 else -1
    if best_candidate < 0: return ("No more eligible candidates", task_set) 

    C_LO, previous_tight_D = task_set.task_set[best_candidate].C_LO, task_set.task_set[best_candidate].tight_D

    # Decrement
    task_set.task_set[best_candidate].tight_D -= 1

    # Check if reached limit
    if task_set.task_set[best_candidate].tight_D < C_LO:
      continue

    # Backtrack if tightening deadline causes theorem 2 or 3 to be false
    if not (s.schedulability_test_thm2(task_set) and s.schedulability_test_thm3(task_set)):
      task_set.task_set[best_candidate].tight_D = previous_tight_D
      continue
    
    # Check if theorem 1 is True with tightened deadline or if theorem 1 fails at another time
    t, ts = get_failure_time(task_set)
    if (t, ts) == (-1, -1): 
      return (True, task_set) # Task set is now schedulable with tightened deadline
    
    candidates.appendleft(best_candidate)

  return ("No more eligible candidates", task_set) 