import random as r
import math
from enum import Enum 
from functools import reduce

class Level(Enum):
    HI = 1
    LO = 2

def generate_T():
  return r.randrange(5,101)

def generate_C_Lo(T):
  return math.ceil((T * r.randrange(2, 25))/100)

def generate_C_Hi(CLo):
  return CLo * r.randrange(2, 5)

def generate_D(CHi):
  return r.randrange(CHi, 101)

def generate_L():
  return r.choice([Level.HI, Level.LO])

def generate_utilization_bound():
  return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

def is_utilization_valid(Cs, Ts, u_bound):
  assert len(Cs) == len(Ts), "Input lists must be the same length."

  return calculate_utilization(Cs, Ts) <= u_bound

def calculate_utilization(Cs, Ts):
  return sum([Cs[i]/Ts[i] for i in range(0, len(Cs))])

def create_task_set():
  utilization_bound = generate_utilization_bound()
  CLos = []
  CHis = []
  Ds = []
  Ts = []
  Ls = []
  index = 0

  while is_utilization_valid(CHis, Ts, utilization_bound):
    Ts.append(generate_T())
    Ls.append(generate_L())
    CLos.append(generate_C_Lo(Ts[index]))
    CHis.append(CLos[index] if Ls[index] == Level.LO else generate_C_Hi(CLos[index]))
    Ds.append(generate_D(CHis[index]))
    index += 1

  length_task_set = len(Ts) if is_utilization_valid(CHis, Ts, 1) else len(Ts) - 1
  return [(CLos[i], CHis[i], Ds[i], Ds[i], Ts[i], Ls[i]) for i in range(length_task_set)]