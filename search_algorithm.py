import dbfs as dbf
import schedulability as s
from generate_tasks import Task, Task_Set
from collections import deque

def is_eligible(task_set):
  return not task_set.thm1 and task_set.thm2 and task_set.thm3

def find_max_wcet_difference(task_set):
  max_wcet_difference = 0
  best_candidate_id = -1

  for task in task_set.hi_tasks_list:
    wcet_difference = task_set.task_set[task.ID].C_HI - task_set.task_set[task.ID].C_LO
    if wcet_difference > max_wcet_difference:
      max_wcet_difference = wcet_difference
      best_candidate_id = task.ID

  return best_candidate_id

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

def find_optimal_tight_D(T, C_LO, prev_tight_D, ts):
  for n in range((ts - 1)//T + 1):
    if C_LO <= ts - n * T < prev_tight_D:
      return ts - n * T

  return prev_tight_D

def greedy_search(task_set):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  candidates = initialize_candidates(task_set)
  best_candidate = -1
  t, ts = get_failure_time(task_set)

  while len(candidates) > 0: 
    # find candidate
    best_candidate = candidates.popleft() if len(candidates) > 0 else -1
    if best_candidate < 0: return ("No more eligible candidates", task_set) 

    # check if demand can be reduced by best candidate    
    T, C_LO, D, previous_tight_D = task_set.task_set[best_candidate].T, task_set.task_set[best_candidate].C_LO, task_set.task_set[best_candidate].D, task_set.task_set[best_candidate].tight_D
    if is_demand_at_minimum(T, C_LO, D, ts):
      continue

    # find optimal decreased tight_D
    task_set.task_set[best_candidate].tight_D = find_optimal_tight_D(T, C_LO, previous_tight_D, ts)

    # if no more changes possible to tight_D, continue
    if task_set.task_set[best_candidate].tight_D == previous_tight_D:
      continue

    # backtrack if reducing tight_D broke thm2
    if not s.schedulability_test_thm2(task_set) or not s.schedulability_test_thm3(task_set):
      task_set.task_set[best_candidate].tight_D = previous_tight_D
      continue
    
    # check if sched 1 test will now pass or if it fails at another time
    t, ts = get_failure_time(task_set)
    if (t, ts) == (-1, -1): 
      return (True, task_set) # sched 1 test is true now
    
    candidates.appendleft(best_candidate)

  return ("No more eligible candidates", task_set) 
