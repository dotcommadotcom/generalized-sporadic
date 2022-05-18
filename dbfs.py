
from functools import reduce
import math
import generate_tasks as gt
import random as r

def demand_based_function(t, C, D, T):
  return C * max(0, math.floor((t - D)/T) + 1)

def is_carry_over(ts, t, D, T):
  return D - ts % T > 0 and ts + D - ts % T <= t

def demand_based_function_CO(ts, CLo, CHi, T, L):
  return min(CLo, ts % T) if L == gt.Level.LO else CHi

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

def calculate_dbf(t, ts, task_set):
  demand = 0
  for task in task_set:
    CLo, CHi, D_tight, D, T, L = task
    demand += demand_based_function(ts, CLo, D_tight, T)
    if L == gt.Level.HI:
      demand += demand_based_function(t-ts-1, CHi, D, T)
    if is_carry_over(ts, t, D, T):
      demand += demand_based_function_CO(ts, CLo, CHi, T, L)
  return demand

def schedulability_test(task_set):
  t_max = calculate_t_max(task_set)
  for i in range(2, t_max + 1):
    for j in range(1, i):
      if calculate_dbf(i, j, task_set) > i:
        return False
  return True

