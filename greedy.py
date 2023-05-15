import dbfs as dbf
from generate_tasks import Task, Task_Set
import generate_tasks as gt
import helper as h 
import schedulability as s
from functools import lru_cache
import matplotlib.pyplot as plt


def is_eligible(task_set: Task_Set):
  return not task_set.thm1 and task_set.thm2

def initialize_candidates(task_set: Task_Set):
  candidates = [False] * task_set.num_tasks

  for task in task_set.hi_tasks_list:
    candidates[task.ID] = True

  return candidates

def find_candidates_wcet(candidates, task_set: Task_Set):
  max_wcet_difference = 0
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible:
      wcet_difference = task_set.task_set[i].C_HI - task_set.task_set[i].C_LO
      if wcet_difference > max_wcet_difference:
        max_wcet_difference = wcet_difference
        best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def find_candidates_min_deadline(candidates, task_set: Task_Set):
  min_deadline = 401
  best_candidate_id = -1

  for i, eligible in enumerate(candidates):
    if eligible and task_set.task_set[i].D < min_deadline:
      min_deadline = task_set.task_set[i].D
      best_candidate_id = task_set.task_set[i].ID

  return best_candidate_id

def get_failure_time(task_set: Task_Set, start_i = 2, start_j = 1):
  clear_cache()
  for i in range(start_i, task_set.t_max + 1):
    for j in range(start_j, i):
      if dbf.sum_dbf(task_set, i, j) > i:
        return i, j
  
  return -1, -1

def clear_cache():
  return
  # dbf.max_requests.cache_clear()
  # dbf.lower.cache_clear()
  # dbf.upper_CO.cache_clear()
  # dbf.upper_UN.cache_clear()
  # dbf.demand_based_function.cache_clear()
  # dbf.demand_based_function_LO.cache_clear()
  # # dbf.demand_based_function_HI.cache_clear()
  # dbf.demand_based_function_CO.cache_clear()

def greedy(task_set: Task_Set):
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
    
    # best_candidate = find_candidates_wcet(candidates, task_set) 
    best_candidate = find_candidates_min_deadline(candidates, task_set) if candidates_count > 0 else -1
    if best_candidate < 0: return ("No more eligible candidates", task_set) 

    task_set.task_set[best_candidate].tight_D -= 1 

    if task_set.task_set[best_candidate].tight_D < task_set.task_set[best_candidate].C_LO:  
      task_set.task_set[best_candidate].tight_D += 1 
      candidates[best_candidate] = False
      candidates_count -= 1

  return ("No more eligible candidates", task_set) 
    
if __name__ == "__main__":
  task_set_dict = {'num_tasks': 4, 
                   't_max': 77, 
                   'utilization': 0.49624662388746893, 
                   'thm1': False, 
                   'thm2': True, 
                   'thm3': True, 
                   'lo_tasks_list': [Task(0, 142, 17, 17, 63, 63)],
                   'hi_tasks_list': [Task(1, 111, 19, 52, 58, 58), Task(2, 224, 14, 48, 284, 284), Task(3, 49, 7, 17, 162, 162)]
                   }
  
  candidate_id = 3
  task_set_eligible = Task_Set(ts_dict = task_set_dict)
  i, j = get_failure_time(task_set_eligible, 2, 1)
  before = dbf.sum_dbf(task_set_eligible, i, j)
  before_sums = [dbf.sum_dbf(task_set_eligible, i, y) for y in range(i)] 

  task_set_eligible.task_set[candidate_id].tight_D = task_set_eligible.task_set[candidate_id].C_LO
  after = dbf.sum_dbf(task_set_eligible, i, j)
  after_sums = [dbf.sum_dbf(task_set_eligible, i, y) for y in range(i)] 

  print(i, j)
  print(task_set_eligible)
  print("demand before", before)

  print("after")
  print(task_set_eligible)
  print("demand after", after)
  

  # hi = [dbf.sum_dbf_HI(task_set_eligible, i, y) for y in range(i)] 
  # plt.plot(hi, label = "hi before")


  # task_set_eligible.task_set[0].tight_D = task_set_eligible.task_set[0].C_LO
  # task_set_eligible.task_set[3].tight_D = task_set_eligible.task_set[3].C_LO

  # lo = [dbf.sum_dbf_LO(task_set_eligible, y) for y in range(i)] 
  # # hi = [dbf.sum_dbf_HI(task_set_eligible, i, y) for y in range(i)] 
  # co = [dbf.sum_dbf_CO(task_set_eligible, i, y) for y in range(i)] 
  # un = [dbf.sum_dbf_UN(task_set_eligible, i, y) for y in range(i)] 




  

  plt.plot(before_sums, label = "before")
  plt.plot(after_sums, label = "after")
  # plt.plot(lo, label = "lo")
  # # plt.plot(hi, label = "hi")
  # plt.plot(co, label = "co")
  # plt.plot(un, label = "un")
  # plt.plot(after_sums, label = "after")
  # plt.plot(after_sums, label = "after")

  plt.legend()

  plt.show()




# def greedy_algorithm(hi_tasks, lo_tasks, t_max):
#   post_algorithm_feasibility = False
#   task_set = {task.ID : task for task in hi_tasks + lo_tasks}


  
#     # while not post_algorithm_feasibility or all(marked):
#   for i in range(2, t_max + 1):
#     for j in range(1, i):
#       dbf_sum_before = dbf.sum_dbf(list(task_set.values()), i, j)
#       if dbf_sum_before > i and any(candidates):
#         print(i - dbf_sum_before)
#         print("test fails ({}, {}), dbf sum {}".format(i, j, dbf_sum_before))
#         for id in range(len(candidates)):
#           if candidates[id]: 
#             print("found candidate {}".format(id))
#             break
#         while task_set[id].tight_D > task_set[id].C_LO:
#           task_set[id].tight_D -= 1
#           dbf_sum_after = dbf.sum_dbf(list(task_set.values()), i, j)
#           if dbf_sum_after <= i:
#             print("test now succeeds ({}, {}), dbf sum {}".format(i, j, dbf_sum_after))
#             break
    
#         if task_set[id].tight_D <= task_set[id].C_LO:
#           print("removing candidate {}".format(id))
#           candidates[id] = False

#   print(candidates)
#   h.print_task_set(list(task_set.values()))
#   return list(task_set.values())

# def try_again(task_set, t_max):
#   for i in range(2, t_max + 1):
#     for j in range(1, i):
#       if dbf.sum_dbf(task_set, i, j) > i:
#         print(i, j)
#         return
      
#   print("success")
# def greedy(task_set):
#   '''
#   Inputs:   
#   task_set:       type: a list of task object. Indicates the input task set.
#   '''
#   # if dbf.schedulability_test_thm2(task_set) == False:
#   #   print("Not schedulable under low-criticality mode.")
#   #   return False
#   # if dbf.schedulability_test_thm1_faster(task_set) == False:
#   #   print("Not schedulable before greedy algorithm")

#   t_max = dbf.calculate_t_max(task_set)

#   before = dbf.sum_dbf(task_set, t_max, t_max//2)

#   changed = False
#   marked = [False] * len(task_set)
#   # while not changed:
#     # run schedulability tests from 0 to l for low and hi respectively
#   for i in range(2, t_max + 1):
#     gen = dbf.generator(i, task_set)
#     for j in gen:
#       if dbf.sum_dbf(task_set, i, j) > i:
#         # find the task that maximizes the dbf increase
#         max_diff = 0
#         target = -1
#         for k in range(len(task_set)):
#           if marked[k]:
#             continue
#           diff = dbf.sum_dbf(task_set, i, j) - dbf.sum_dbf(task_set, i-1, j)
#           if diff > max_diff:
#             max_diff = diff
#             target = k
#         # print("Found target:{}".format(target))
#         if target == -1:
#           continue
#           # return False
#         task_set[target].tight_D -= 1
#         if task_set[target].tight_D == task_set[target].C_LO:
#           marked[target] = True
#           # changed = True

#   after = dbf.sum_dbf(task_set, t_max, t_max//2)
#   return (before, after, after-before)
#   # return dbf.schedulability_test_thm1_faster(task_set)
#   # return True

# MIN_U = 0.02
# MAX_U = 0.25




# # def is_best_candidate():

# def greed_v2(task_set):
#   if is_schedulable(task_set): 
#     print("Already schedulable")
#     return True
#   hi_tasks = [ts for ts in task_set if ts.L == gt.Level.HI]
#   lo_tasks = [ts for ts in task_set if ts.L == gt.Level.LO]
#   modified_ts = greedy_algorithm(hi_tasks, lo_tasks, t_max)
#   try_again(modified_ts, t_max)

