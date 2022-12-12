
from functools import reduce
import math as m
import generate_tasks as gt

def max_requests(T, upper, lower):
  return max(0, m.floor((upper - lower)/T) + 1)

def demand_based_function(C, T, upper, lower):
  return  C * max_requests(T, upper, lower)

def demand_based_function_LO(task, ts):
  return demand_based_function(task.C_LO, task.T, ts, task.tight_D)

def demand_based_function_HI(task, t, ts):
  return demand_based_function(task.C_HI, task.T, t - ts, task.D) if task.L == gt.Level.HI else 0

def lower(task, ts):
  return task.T * max_requests(task.T, ts, task.tight_D) 

def upper(task, t, ts):
  return min(ts, t - task.tight_D) if task.L == gt.Level.LO else min(ts, t - task.D - task.T * max_requests(task.T, t - ts, task.D)) 

def demand_based_function_CO(task, t, ts):
  return demand_based_function(task.C_HI, task.T, upper(task, t, ts), lower(task, ts)) if task.L == gt.Level.HI else 0

def demand_based_function_UN(task, t, ts):
  k = max_requests(task.T, upper(task, t, ts), lower(task, ts))

  return int(min(task.C_LO, ts - lower(task, ts) - (k - 1) * task.T / 2) * k) if task.L == gt.Level.LO else 0

def sum_dbf_HI(task_set, t, ts):
  return sum([demand_based_function_HI(task, t, ts) for task in task_set])

def sum_dbf_LO(task_set, ts):
  return sum([demand_based_function_LO(task, ts) for task in task_set])

def sum_dbf_CO(task_set, t, ts):
  return sum([demand_based_function_CO(task, t, ts) for task in task_set])

def sum_dbf_UN(task_set, t, ts):
  return sum([demand_based_function_UN(task, t, ts) for task in task_set])

def sum_dbf(task_set, t, ts):
  return sum_dbf_HI(task_set, t, ts) + sum_dbf_LO(task_set, ts) + sum_dbf_CO(task_set, t, ts) + sum_dbf_UN(task_set, t, ts)