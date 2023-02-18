from functools import reduce
import itertools
import math as m
import generate_tasks as gt
from dbfs import *

def calculate_utilization(task_set):
  return sum([(task.C_LO + task.C_HI) // 2 / task.T for task in task_set])

def lcmT_maxD(task_set):
  return reduce(lambda x, y: (x * y)//m.gcd(x, y), [task.T for task in task_set]) + max([task.D for task in task_set])

def U_maxTD(task_set):
  return int(m.floor(calculate_utilization(task_set) / (1 - calculate_utilization(task_set)) * max([task.T - task.D for task in task_set])))

def calculate_t_max(task_set):
  return min(lcmT_maxD(task_set), U_maxTD(task_set)) if U_maxTD(task_set) >= 0 else 0

def n(t, D, T):
  return m.floor((t - D)/T)

def ts_LO(task, t):
  return {task.tight_D + i * task.T for i in range(n(t, task.tight_D, task.T) + 1)}

def ts_HI(task, t):
  return {t - task.D - i * task.T for i in range(n(t, task.D, task.T), -1, -1) if task.L == gt.Level.HI}

def ts_CO(task, t):
  return ts_LO(task, t) | {ts + 1 for ts in ts_HI(task, t)} if task.L == gt.Level.HI else set()

# def ts_UN(task, t):
#   return {ts for ts in range(task.C_LO + 1)} | ts_LO(task, t) if task.L == gt.Level.LO else set()



# def ts(task_set, t):
#   ts_values = set()

#   for task in task_set:
#     ts_values.update(ts_LO(task, t) | ts_HI(task, t) | ts_CO(task, t) | ts_UN(task, t))

#   return ts_values

# def schedulability_test_thm1(task_set):
#   t_max = calculate_t_max(task_set)

#   return next((False for i in range(2, t_max + 1) for j in range(i - 1, 0, -1) if sum_dbf(task_set, i, j) > i), True)

# def schedulability_test_thm1_set(task_set):
#   t_max = calculate_t_max(task_set)

#   return next((False for i in range(2, t_max + 1) for j in ts(task_set, i) if sum_dbf(task_set, i, j) > i), True)





# def rule(task, t, ts):
#   if task.L == gt.Level.HI: 
#     return t >= task.D and upper(task, t, ts) >= lower(task, ts) and max_requests(task.T, upper(task, t, ts), lower(task, ts)) != max_requests(task.T, upper(task, t, ts - 1), lower(task, ts - 1))
#   return t >= task.tight_D and upper(task, t, ts) >= lower(task, ts) and max_requests(task.T, upper(task, t, ts), lower(task, ts)) != max_requests(task.T, upper(task, t, ts - 1), lower(task, ts - 1))

# def ts_list(t, task_set):
#   return {ts for ts in range(1, t) for task in task_set if rule_LO(ts, task.T, task.tight_D) or rule_HI(t, ts, task.T, task.D) or rule(t, ts, task)}



# def schedulability_test_thm2(task_set):
#   t_max = calculate_t_max(task_set)

#   return next((False for i in range(1, t_max + 1) if sum_dbf_LO(task_set, i) > i), True)

# def schedulability_test_thm3(task_set):
#   t_max = calculate_t_max(task_set)

#   return next((False for i in range(1, t_max + 1) if sum_dbf_HI(task_set, i, 0) > i), True)
