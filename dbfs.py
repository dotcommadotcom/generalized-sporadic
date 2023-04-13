
from functools import reduce, lru_cache
import math as m
import generate_tasks as gt

@lru_cache(maxsize=None)
def max_requests(T, upper, lower):
  return max(0, m.floor((upper - lower)/T) + 1)

@lru_cache(maxsize=None)
def demand_based_function(C, T, upper, lower):
  return  C * max_requests(T, upper, lower)

@lru_cache(maxsize=None)
def demand_based_function_LO(task, ts):
  return demand_based_function(task.C_LO, task.T, ts, task.tight_D)

def demand_based_function_HI(task, t, ts):
  return demand_based_function(task.C_HI, task.T, t - ts, task.D)

@lru_cache(maxsize=None)
def lower(task, ts):
  return task.T * max_requests(task.T, ts, task.tight_D) 

@lru_cache(maxsize=None)
def upper_CO(task, t, ts):
  return t - task.D - task.T * max_requests(task.T, t - ts, task.D)

@lru_cache(maxsize=None)
def upper_UN(task, t, ts):
  return min(ts, t - task.tight_D)

@lru_cache(maxsize=None)
def demand_based_function_CO(task, t, ts):
  return demand_based_function(task.C_HI, task.T, upper_CO(task, t, ts), lower(task, ts))

def demand_based_function_UN(task, t, ts):
  k = max_requests(task.T, upper_UN(task, t, ts), lower(task, ts))

  return int(min(task.C_LO, ts - lower(task, ts) - (k - 1) * task.T / 2) * k)

def sum_dbf_HI(task_set, t, ts):
  return sum([demand_based_function_HI(task, t, ts) for task in task_set if task.L == gt.Level.HI])

def sum_dbf_LO(task_set, ts):
  return sum([demand_based_function_LO(task, ts) for task in task_set])

def sum_dbf_CO(task_set, t, ts):
  return sum([demand_based_function_CO(task, t, ts) for task in task_set if task.L == gt.Level.HI])

def sum_dbf_UN(task_set, t, ts):
  return sum([demand_based_function_UN(task, t, ts) for task in task_set if task.L == gt.Level.LO])

def sum_dbf(task_set, t, ts):
  return sum_dbf_HI(task_set, t, ts) + sum_dbf_LO(task_set, ts) + sum_dbf_CO(task_set, t, ts) + sum_dbf_UN(task_set, t, ts)