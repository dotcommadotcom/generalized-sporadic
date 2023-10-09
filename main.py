
from generate_tasks import Task, Task_Set, generate_task
import dbfs as dbf
import random as r
import schedulability as s
import cProfile
import multiprocessing as mp
from multiprocessing import Queue
import time
import matplotlib.pyplot as plt
import copy
import search_algorithm as alg

# # import search_algorithm as alg
# # TASK_SET_N = 30
# # PROCESS_N =  mp.cpu_count() - 1
# # MIN_U = 0.02
# # MAX_U = 0.25

# # MIN_CLO = 5
# # MAX_CLO = 25

# # MIN_CHI = 2
# # MAX_CHI = 4

# # MAX_D = 500

# # FILENAME = 'database_0.8_110'
# # import copy
# # def dec_d(task, change = None):
# #   copied = copy.deepcopy(task)
# #   if change:
# #     copied.tight_D = change
# #   else:
# #     copied.tight_D -= 1
# #   return copied

if __name__ == "__main__":
  while True:
    task_set = Task_Set(0.4)
    id = alg.initialize_candidates(task_set)[0]
    t, ts = 100, 50
    previous_un_demand = dbf.sum_dbf_UN(task_set, t, ts)
    previous_k = dbf.max_requests(task_set.task_set[id].T, dbf.upper_UN(task_set.task_set[id], t, ts), dbf.lower(task_set.task_set[id], ts))
    tight_task_set = copy.deepcopy(task_set)
    tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO
    post_k = dbf.max_requests(tight_task_set.task_set[id].T, dbf.upper_UN(tight_task_set.task_set[id], t, ts), dbf.lower(tight_task_set.task_set[id], ts))

    if previous_k != post_k:
      break
  print(repr(task_set))
  print(id)
  # print(tight_task_set)
  print("sum demand", dbf.sum_dbf(task_set, t, ts), dbf.sum_dbf(tight_task_set, t, ts))
  print("un demand", previous_un_demand, dbf.sum_dbf_UN(tight_task_set, t, ts))
  print("lower", previous_k, post_k)



#   # lo_u = sum([task.C_LO / task.T for task in task_set.lo_tasks_list])
#   # hi_u = sum([task.C_HI / task.T for task in task_set.hi_tasks_list])

#   # u = r.uniform(0.01, 0.1)
#   # task = generate_task(u)
#   # print(task)
#   task_set = [generate_task(r.uniform(0.01, 0.1)) for _ in range(3)]
#   print(task_set)
#   lo_u = sum([task.C_LO / task.T for task in task_set])
#   print(lo_u)
#   sum([demand_based_function_LO(task, ts) for task in task_set.task_set.values()])




  