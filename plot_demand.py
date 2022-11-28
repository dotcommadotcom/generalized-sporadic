from cProfile import label
import generate_tasks as gt
import dbfs as dbf
import matplotlib.pyplot as plt
import random as r

def print_task_set(task_set):
  for t in task_set:
    print("ID: {}, C_LO: {}, C_HI: {}, T: {}, D: {}, L: {}".format(t.ID, t.C_LO, t.C_HI, t.T, t.D, t.L))

if __name__ == '__main__':
  # for u_sum in [0.5, 0.6, 0.7, 0.8, 0.9]:
  #   task_set = generate_task_set(u_sum, 0.02, 0.25)

  u_sum = r.choice([0.5, 0.6, 0.7, 0.8, 0.9])
  task_set = gt.generate_task_set(u_sum, 0.02, 0.25)
  print("------- Current utilization sum: {}---------".format(u_sum))
  print_task_set(task_set)
  print("Real utilization sum: {}".format(sum([task.C_LO / task.T for task in task_set])))
  print("t_max: {}".format(dbf.calculate_t_max(task_set)))

  t_maxes = []
  ts_low_demand = []
  ts_middle_demand = []
  ts_high_demand = []

  for i in range(1, dbf.calculate_t_max(task_set)):
    t_maxes.append(i)
    ts_low_demand.append(dbf.sum_dbf(task_set, i, 1))
    ts_middle_demand.append(dbf.sum_dbf(task_set, i, i//2))
    ts_high_demand.append(dbf.sum_dbf(task_set, i, i-1))
  plt.plot(t_maxes, ts_low_demand, label = "ts=1")
  plt.plot(t_maxes, ts_middle_demand, label = "ts=t//2")
  plt.plot(t_maxes, ts_high_demand, label = "ts=t-1")
  plt.plot(t_maxes, t_maxes)
  plt.legend()
  plt.show()

  
    