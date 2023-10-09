import dbfs as dbf

def demand_based_function_LO_ek(task, ts):
  return dbf.demand_based_function_LO(task, ts)

def demand_based_function_full(task, t, ts):
  return dbf.demand_based_function(task.C_HI, task.T, upper = t - ts, lower = task.D - task.tight_D)

def demand_based_function_done(task, t, ts):
  n = (t - ts) % task.T

  if task.D - task.tight_D <= n < task.D:
    return max(0, task.C_LO - n + task.D - task.tight_D)
  return 0

def demand_based_function_HI_ek(task, t, ts):
  return demand_based_function_full(task, t, ts) - demand_based_function_done(task, t, ts)

def sum_dbf_ek(task_set, t, ts):
  demand_sum = 0
  for task in task_set.task_set.values():
    if task.C_LO < task.C_HI:
      demand_sum += demand_based_function_HI_ek(task, t, ts)
    demand_sum += demand_based_function_LO_ek(task, ts) 

  return demand_sum

import matplotlib.pyplot as plt
from generate_tasks import Task

if __name__ == "__main__":
  task = Task(-1, 6, 2, 4, 6, 6)
  task2 = Task(-1, 6, 2, 4, 6, 4)

  dbf_hi_six = [demand_based_function_HI_ek(task, t, 0) for t in range(31)]
  dbf_lo_six = [demand_based_function_LO_ek(task, ts) for ts in range(31)]
  dbf_hi_four = [demand_based_function_HI_ek(task2, t, 0) for t in range(31)]
  dbf_lo_four = [demand_based_function_LO_ek(task2, ts) for ts in range(31)]
  t = [t for t in range(31)]
  plt.plot(dbf_hi_six)
  plt.plot(dbf_lo_six)
  plt.plot(dbf_hi_four)
  plt.plot(dbf_lo_four)
  plt.plot(t)
  plt.show()