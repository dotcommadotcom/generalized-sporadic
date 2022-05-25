from cProfile import label
from generate_tasks import task, task_generation
import dbfs as dbf
import matplotlib.pyplot as plt

if __name__ == '__main__':
  G = task_generation()
  t_maxes = []
  ts_low_demand = []
  ts_middle_demand = []
  ts_high_demand = []
  task_set_ex = G.create_task_set(0.5, 0.02, 0.25)
  for i in range(1, dbf.calculate_t_max(task_set_ex)):
    t_maxes.append(i)
    ts_low_demand.append(dbf.calculate_dbf(i, 1, task_set_ex))
    ts_middle_demand.append(dbf.calculate_dbf(i, i//2, task_set_ex))
    ts_high_demand.append(dbf.calculate_dbf(i, i-1, task_set_ex))
  plt.plot(t_maxes, ts_low_demand, label = "ts=1")
  plt.plot(t_maxes, ts_middle_demand, label = "ts=t//2")
  plt.plot(t_maxes, ts_high_demand, label = "ts=t-1")
  plt.plot(t_maxes, t_maxes)
  plt.legend()
  plt.show()