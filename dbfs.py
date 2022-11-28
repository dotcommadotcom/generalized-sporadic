
from functools import reduce
import math as m
import generate_tasks as gt
import random as r

def calculate_utilization(task_set):
  return sum([task.C_LO / task.T for task in task_set])

# TODO is it ok to calculate U with CLo and not CHi? 

def lcm_T(task_set):
  return reduce(lambda x, y: (x * y)//m.gcd(x, y), [task.T for task in task_set])

def max_D(task_set):
  return max([task.D for task in task_set])

def max_TD(task_set):
  return max([task.T - task.D for task in task_set])

# TODO what does it mean if all D > T and max TD is negative?

def calculate_t_max(task_set):
  U = calculate_utilization(task_set)
  first = lcm_T(task_set) + max_D(task_set)
  second = U / (1 - U) * max_TD(task_set)

  return m.floor(min(first, second)) if second >= 0 else first

def max_requests(T, upper, lower):
  return max(0, m.floor((upper - lower)/T) + 1)

def demand_based_function(C, T, upper, lower):
  return  C * max_requests(T, upper, lower)

def demand_based_function_CO(task, t, ts):
  upper = min(ts, t - task.D - task.T * max_requests(task.T, t - ts, task.D))
  lower = max(0, ts - task.tight_D + 1, task.T * max_requests(task.T, ts, task.tight_D))

  return demand_based_function(task.C_HI, task.T, upper, lower)

def demand_based_function_UN(task, t, ts):
  upper = min(ts, t - task.tight_D)
  lower = max(0, ts - task.tight_D + 1, task.T * max_requests(task.T, ts, task.tight_D))
  k = max_requests(task.T, upper, lower)

  return min(task.C_LO, ts - lower - (k - 1) * task.T / 2) * k

def sum_dbf_HI(task_set, t, ts):
  return sum([demand_based_function(task.C_HI, task.T, t - ts, task.D) if task.L == gt.Level.HI else 0 for task in task_set])

def sum_dbf_LO(task_set, ts):
  return sum([demand_based_function(task.C_LO, task.T, ts, task.tight_D) for task in task_set])

def sum_dbf_CO(task_set, t, ts):
  return sum([demand_based_function_CO(task, t, ts) if task.L == gt.Level.HI else 0 for task in task_set])

def sum_dbf_UN(task_set, t, ts):
  return sum([demand_based_function_UN(task, t, ts) if task.L == gt.Level.LO else 0 for task in task_set])

def sum_dbf(task_set, t, ts):
  return sum_dbf_HI(task_set, t, ts) + sum_dbf_LO(task_set, ts) + sum_dbf_CO(task_set, t, ts) + sum_dbf_UN(task_set, t, ts)

def schedulability_test_thm1(task_set):
  t_max = calculate_t_max(task_set)

  for i in range(2, t_max + 1):
    for j in range(i-1, 0, -1):
      if sum_dbf(task_set, i, j) > i:
        return False
  return True

def schedulability_test_thm2(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(1, t_max + 1):
    if sum_dbf_LO(task_set, i) > i:
      return False
  return True

def schedulability_test_thm3(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(1, t_max + 1):
    if sum_dbf_HI(task_set, i, 0) > i:
      return False
  return True





# def calc_min_t(task_set, t_max):
#     min_D = min([task.tight_D for task in task_set])
#     min_T = min([task.T for task in task_set])
#     minimum_t = 0
#     for i in range(0, t_max + 1):
#       if max_requests(min_T, i, min_D) >= 1:
#         minimum_t = i
#         break

#     return minimum_t

# def print_task_set(task_set):
#   for t in task_set:
#     print("ID: {}, C_LO: {}, C_HI: {}, T: {}, D: {}, L: {}".format(t.ID, t.C_LO, t.C_HI, t.T, t.D, t.L))

# if __name__ == '__main__':
#   task_set = gt.generate_task_set(0.8, 0.02, 0.25)
#   t_max = calculate_t_max(task_set)
#   print_task_set(task_set)
#   print(calc_min_t(task_set, t_max))
