
from functools import reduce
import math
import generate_tasks as gt
import random as r

def demand_based_function(t, C, D, T):
  return C * max(0, math.floor((t - D)/T) + 1)

def is_carry_over(ts, D, T):
  return D - ts % T >= 0

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

  return t_max if t_max > 0 else lcm(Ts) + max(Ds)

def calculate_dbf(t, ts, task_set):
  demand = 0
  demand_CO = 0
  max_CHi = 0
  for task in task_set:
    CLo, CHi, DLo, D, T, L = task
    demand += demand_based_function(ts, CLo, DLo, T)
    if L == gt.Level.HI:
      if CHi > max_CHi:
        max_CHi = CHi
      demand += demand_based_function(t-ts-1, CHi, D, T)
    if is_carry_over(ts, D, T):
      demand_CO += demand_based_function_CO(ts, CLo, CHi, T, L)
  demand_CO = min(max_CHi, demand_CO)
  demand += demand_CO
  return demand

# def schedulability_test(task_set):
#   tmax = int(gt.calculate_t_max(task_set))
#   for t in range(tmax + 1):
#     for ts in range(gt):
#       if calculate_dbf(t, ts, task_set) > t:
#         return False
#   return True



