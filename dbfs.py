
from functools import reduce
import math
import generate_tasks as gt
import random as r

def lcm(list):
  return reduce(lambda x, y: (x * y)//math.gcd(x, y), list)

def calculate_t_max(task_set):
  CHis = []
  Ds = []
  Ts = []

  for task in task_set:
    _, CHi, _, D, T, _ = task
    CHis.append(CHi)
    Ds.append(D)
    Ts.append(T)

  U = gt.calculate_utilization(CHis, Ts)
  
  t_max = min(lcm(Ts) + max(Ds), U / (1 - U) * max([T - D for (T, D) in zip(Ts, Ds)]))

  return math.floor(t_max) if t_max > 0 else lcm(Ts) + max(Ds)

def demand_based_function(t, C, D, T):
  return C * max(0, math.floor((t - D)/T) + 1)

def max_num_requests(t, ts, D, T):
  return math.floor((min(ts, t-D)-ts+D-1)/T) + 1 if t-D >= 0 else 0

def demand_based_function_CO(t, ts, CLo, CHi, D_tight, T):
  return CHi * max_num_requests(t, ts, D_tight, T)

def demand_based_function_UN(t, ts, CLo, D_tight, T):
  k = max_num_requests(t, ts, D_tight, T)
  return min(CLo, D_tight-1-(k-1)*T/2) * k

def total_dbf_HI(t, ts, task_set):
  return sum([demand_based_function(t-ts, CHi, D, T) if L == gt.Level.HI else 0 for (_, CHi, _, D, T, L) in task_set])

def total_dbf_LO(ts, task_set):
  return sum([demand_based_function(ts, CLo, D_tight, T) for (CLo, _, D_tight, _, T, _) in task_set])

def total_dbf_CO(t, ts, task_set):
  return sum([demand_based_function_CO(t, ts, CLo, CHi, D_tight, T) if L == gt.Level.HI else 0 for (CLo, CHi, D_tight, _, T, L) in task_set])

def total_dbf_UN(t, ts, task_set):
  return sum([demand_based_function_UN(t, ts, CLo, D_tight, T) if L == gt.Level.LO else 0 for (CLo, _, D_tight, _, T, L) in task_set])

def calculate_dbf(t, ts, task_set):
  return total_dbf_HI(t, ts, task_set) + total_dbf_LO(ts, task_set) + total_dbf_CO(t, ts, task_set) + total_dbf_UN(t, ts, task_set)

def schedulability_test(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(2, t_max + 1):
    for j in range(i-1, 0, -1):
      if calculate_dbf(i, j, task_set) > i:
        return False
  return True

