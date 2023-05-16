import sys

import dbfs as dbf
import schedulability as s

def is_eligible(task_set):
  return not task_set.thm1 and task_set.thm2

def initialize_candidates(task_set):
  candidates = [False] * task_set.num_tasks

  for task in task_set.hi_tasks_list:
    candidates[task.ID] = True

  return candidates

def find_candidate(candidates, task_set, heuristic):
  return heuristic(candidates, task_set)

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
      if dbf.sum_dbf(task_set, i, j) > i:
        return i, j
  
  return -1, -1


def greedy(task_set, heuristic):
  if not is_eligible(task_set):
    return ("Not eligible for deadline-tightening", task_set)
  
  candidates = initialize_candidates(task_set)
  best_candidate = -1
  candidates_count = len(task_set.hi_tasks_list)
  i, j = 2, 1

  while candidates_count > 0: 
    if best_candidate >= 0 and not s.schedulability_test_thm2(task_set):
      task_set.task_set[best_candidate].tight_D += 1
      candidates[best_candidate] = False
      candidates_count -= 1

    i, j = get_failure_time(task_set, i, j)
    if (i, j) == (-1, -1): 
      return (True, task_set) # sched 1 test is true now
    
    best_candidate = find_candidate(candidates, task_set, heuristic) if candidates_count > 0 else -1
    if best_candidate < 0: return ("No more eligible candidates", task_set) 

    task_set.task_set[best_candidate].tight_D -= 1 

    if task_set.task_set[best_candidate].tight_D < task_set.task_set[best_candidate].C_LO:  
      task_set.task_set[best_candidate].tight_D += 1 
      candidates[best_candidate] = False
      candidates_count -= 1

  return ("No more eligible candidates", task_set) 
    
# if __name__ == "__main__":
#   task_set_dict = {'num_tasks': 3, 
#                    't_max': 61, 
#                    'utilization': 0.5900067674261222, 
#                    'thm1': False, 
#                    'thm2': True, 
#                    'thm3': True, 
#                    'lo_tasks_list': [Task(2, 62, 11, 11, 19, 19)],
#                    'hi_tasks_list': [Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)]
#                    }
  
#   i = 1
#   task_set = Task_Set(ts_dict = task_set_dict)
#   t, ts = get_failure_time(task_set)

#   before = dbf.sum_dbf(task_set, t, ts)
#   before_sums = [dbf.sum_dbf(task_set, t, y) for y in range(t)] 

#   _, post_greedy_task_set = greedy(task_set, earliest_deadline)

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


