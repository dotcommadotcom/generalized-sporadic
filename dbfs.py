
from functools import reduce
import math
import generate_tasks as gt
import random as r

def lcm(list):
  return reduce(lambda x, y: (x * y)//math.gcd(x, y), list)

def calculate_utilization(Cs, Ts):
  return sum([Cs[i]/Ts[i] for i in range(0, len(Cs))])

def calculate_t_max(task_set):
  CLos = []
  Ds = []
  Ts = []

  for task in task_set:
    CLo, D, T = task.WCET_LO, task.D, task.T
    CLos.append(CLo)
    Ds.append(D)
    Ts.append(T)

  U = calculate_utilization(CLos, Ts)
  
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
  return sum([demand_based_function(t-ts, task.WCET_HI, task.D, task.T) if task.L == gt.Level.HI else 0 for task in task_set])

def total_dbf_LO(ts, task_set):
  return sum([demand_based_function(ts, task.WCET_LO, task.tight_D, task.T) for task in task_set])

def total_dbf_CO(t, ts, task_set):
  return sum([demand_based_function_CO(t, ts, task.WCET_LO, task.WCET_HI, task.tight_D, task.T) if task.L == gt.Level.HI else 0 for task in task_set])

def total_dbf_UN(t, ts, task_set):
  return sum([demand_based_function_UN(t, ts, task.WCET_LO, task.tight_D, task.T) if task.L == gt.Level.LO else 0 for task in task_set])

def calculate_dbf(t, ts, task_set):
  return total_dbf_HI(t, ts, task_set) + total_dbf_LO(ts, task_set) + total_dbf_CO(t, ts, task_set) + total_dbf_UN(t, ts, task_set)

def schedulability_test_thm1(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(2, t_max + 1):
    for j in range(i-1, 0, -1):
      if calculate_dbf(i, j, task_set) > i:
        return False
  return True

def schedulability_test_thm2(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(1, t_max+1):
    if total_dbf_LO(i, task_set) > i:
      return False
  return True

def schedulability_test_thm3(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(1, t_max+1):
    if total_dbf_HI(i, 0, task_set) > i:
      return False
  return True

