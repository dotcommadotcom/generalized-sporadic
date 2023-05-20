from enum import Enum 
from math import gcd, ceil, floor
from functools import reduce
import random as r

MIN_U = 0.02
MAX_U = 0.25

MIN_CLO = 5
MAX_CLO = 25

MIN_CHI = 2
MAX_CHI = 4

MAX_D = 400

class Level(Enum):
  HI = 1
  LO = 2

class Task:
  def __init__(self, ID, T, C_LO, C_HI, D, tight_D = -1, L = None):
    """
    Args:
      ID:         type: int. ID of task.
      T:          type: int. Minimum inter-arrival separation time of task.
      C_LO:       type: int. WCET in low-criticality mode.
      C_HI:       type: int. WCET in high-criticality mode. If L == LO, same as C_LO
      D:          type: int. Relative deadline of task.
      L:          type: Level. Criticality level of task. Either HI or LO.
      tight_D:    type: int. Tightened deadline of the task. If not assigned, the same as D.
    """
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
  
def generate_L():
  return r.choice([Level.HI, Level.LO])

def generate_C_LO():
  return r.randrange(MIN_CLO, MAX_CLO)

def generate_C_HI(C_LO, L):
  return C_LO if L == Level.LO else r.randrange(C_LO * MIN_CHI, C_LO * MAX_CHI + 1)

def generate_D(C_HI):
  return r.randrange(C_HI, MAX_D + 1)

def generate_T(C_LO, utilization):
  return ceil(C_LO / utilization) 

def generate_task(utilization, ID = -1):
  L = generate_L()
  C_LO = generate_C_LO()
  C_HI = generate_C_HI(C_LO, L)
  D = generate_D(C_HI)
  T = generate_T(C_LO, utilization)

  return Task(ID, T, C_LO, C_HI, D, -1, L)

class Task_Set:
  def __init__(self, target_u = None, task_set_dict = None):
    if target_u:
      self.task_set = self.initialize_task_set(target_u)
      self.num_tasks = len(self.task_set)
      self.utilization = self.calculate_utilization()
      self.t_max = self.calculate_t_max()
      self.thm1 = None
      self.thm2 = None
      self.thm3 = None
      self.lo_tasks_list = [task for task in self.task_set.values() if task.L == Level.LO]
      self.hi_tasks_list = [task for task in self.task_set.values() if task.L == Level.HI]
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
  
  def generate_kato_utilizations(self, target_u):
    utilizations = []
    total_u = 0

    while total_u < target_u:
      current_u = r.uniform(MIN_U, MAX_U)
      if current_u + total_u > target_u:
        current_u = target_u - total_u
      total_u += current_u
      utilizations.append(current_u)

    return utilizations

  def initialize_task_set(self, target_u):
    utilizations = self.generate_kato_utilizations(target_u)
    return {i: generate_task(u, i) for u, i in zip(utilizations, range(len(utilizations)))}
  
  def calculate_utilization(self):
    return sum([task.C_LO / task.T for task in self.task_set.values()])
  
  def lcmT_maxD(self):
    return reduce(lambda x, y: (x * y)//gcd(x, y), [task.T for task in self.task_set.values()]) + max([task.D for task in self.task_set.values()])

  def U_maxTD(self):
    return floor(self.utilization / (1 - self.utilization) * max([task.T - task.D for task in self.task_set.values()]))

  def calculate_t_max(self):
    return min(self.lcmT_maxD(), self.U_maxTD()) if self.U_maxTD() >= 0 else 0

  def set_thm1(self, test_result):
    self.thm1 = test_result

  def set_thm2(self, test_result):
    self.thm2 = test_result

  def set_thm3(self, test_result):
    self.thm3 = test_result

def generate_valid_task_set(target_u):
  while True:
    task_set = Task_Set(target_u)
    if task_set.t_max > 0:
      return task_set