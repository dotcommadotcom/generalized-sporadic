from enum import Enum 
from math import gcd, floor
from functools import reduce
import random as r

MIN_CLO = 5
MAX_CLO = 25

MAX_D = 500
MAX_T = 500

TARGET_U = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

class Level(Enum):
  LO = 0
  HI = 1
  
class Task:
  def __init__(self, ID, T, C_LO, C_HI, D, tight_D = -1, L = None):
    self.ID = ID
    self.T = T
    self.C_LO = C_LO
    self.C_HI = C_HI
    self.D = D
    self.tight_D = D if tight_D == -1 else tight_D
    self.L = L if L else (Level.LO if C_LO == C_HI else Level.HI)
  
  def __str__(self):
    return "ID: {}, T: {}, C_LO: {}, C_HI: {}, D: {}, D': {}, L: {}".format(self.ID, self.T, self.C_LO, self.C_HI, self.D, self.tight_D, self.L)

  def __repr__(self):
    return "Task({}, {}, {}, {}, {}, {})".format(self.ID, self.T, self.C_LO, self.C_HI, self.D, self.tight_D)

def generate_L(hi_probability = 0.5):
  return r.choices([Level.HI, Level.LO], weights = [hi_probability, 1 - hi_probability], k = 1)[0]

def generate_C_LO():
  return r.randrange(MIN_CLO, MAX_CLO)

def generate_C_HI(C_LO, L, wcet_ratio = 4):
  return C_LO if L == Level.LO else r.randrange(C_LO * 2, C_LO * wcet_ratio + 1)

def generate_D(C_HI):
  return r.randrange(C_HI, MAX_D + 1)

def generate_T(C_HI):
  return r.randrange(C_HI, MAX_T + 1)

def generate_task(ID = -1, hi_probability = 0.5, wcet_ratio = 4):
  L = generate_L(hi_probability)
  C_LO = generate_C_LO()
  C_HI = generate_C_HI(C_LO, L, wcet_ratio)
  D = generate_D(C_HI)
  T = generate_T(C_HI)

  return Task(ID, T, C_LO, C_HI, D, -1, L)

class Task_Set:
  def __init__(self, target_u = None, task_set_dict = None, hi_probability = 0.5, wcet_ratio = 4):
    if target_u:
      self.task_set = {}
      self.num_tasks = 0
      self.lo_tasks_list = []
      self.hi_tasks_list = []

      while True:
        task = generate_task(self.num_tasks, hi_probability, wcet_ratio)

        self.task_set[self.num_tasks] = task
        self.num_tasks = len(self.task_set)
        self.utilization = self.calculate_utilization()

        if task.L == Level.LO: self.lo_tasks_list.append(task)
        if task.L == Level.HI: self.hi_tasks_list.append(task)
        
        if target_u - 0.005 <= self.utilization <= target_u + 0.005 \
          and len(self.lo_tasks_list) > 0 and len(self.hi_tasks_list) > 0 and self.calculate_t_max() > 0:
          break

        elif self.utilization > target_u + 0.005:
          self.task_set = {}
          self.num_tasks = len(self.task_set)
          self.lo_tasks_list = []
          self.hi_tasks_list = []

      self.t_max = self.calculate_t_max()
      self.thm1 = None
      self.thm2 = None
      self.thm3 = None

    else:
      self.num_tasks = task_set_dict["num_tasks"]
      self.t_max = task_set_dict["t_max"]
      self.utilization = task_set_dict["utilization"]
      self.thm1 = task_set_dict["thm1"]
      self.thm2 = task_set_dict["thm2"]
      self.thm3 = task_set_dict["thm3"]
      self.lo_tasks_list = task_set_dict["lo_tasks_list"]
      self.hi_tasks_list = task_set_dict["hi_tasks_list"]
      self.task_set = {task.ID : task for task in self.lo_tasks_list + self.hi_tasks_list}
  
  def __str__(self):
    task_set_string = "Task set: {} tasks, t_max = {}, utilization = {} \n".format(self.num_tasks, self.t_max, self.utilization)
    if self.thm1 is not None: task_set_string += "Thm 1 -- {}\n".format(self.thm1)
    if self.thm2 is not None: task_set_string += "Thm 2 -- {}\n".format(self.thm2)
    if self.thm3 is not None: task_set_string += "Thm 3 -- {}\n".format(self.thm3)
    for task in self.task_set.values():
      task_set_string += str(task) + "\n"
    return task_set_string

  def __repr__(self):
    lo_tasks = str([repr(task) for task in self.lo_tasks_list])
    hi_tasks = str([repr(task) for task in self.hi_tasks_list])

    return """
          'num_tasks': {}, 
          't_max': {}, 
          'utilization': {}, 
          'thm1': {}, 
          'thm2': {}, 
          'thm3': {},
          'lo_tasks_list': {},
          'hi_tasks_list': {}
          """.format(self.num_tasks, self.t_max, self.utilization, self.thm1, self.thm2, self.thm3,
                      lo_tasks.replace("'", ""), hi_tasks.replace("'", ""))
  
  def lcmT_maxD(self):
    return reduce(lambda x, y: (x * y)//gcd(x, y), [task.T for task in self.task_set.values()]) + max([task.D for task in self.task_set.values()])

  def U_maxTD(self):
    return floor(self.utilization / (1 - self.utilization) * max([task.T - task.D for task in self.task_set.values()]))

  def calculate_t_max(self):
    return min(self.lcmT_maxD(), self.U_maxTD()) if self.U_maxTD() >= 0 else 0

  def calculate_utilization(self):
    lo_utilization = sum([task.C_LO / task.T for task in self.task_set.values() if task.L == Level.LO])
    hi_utilization = sum([task.C_HI / task.T for task in self.task_set.values() if task.L == Level.HI])

    return (lo_utilization + hi_utilization)/2