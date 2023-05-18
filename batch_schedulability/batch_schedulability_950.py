import time
import multiprocessing as mp
import pandas as pd

import generate_tasks as gt
import csv_helper as ch
import schedulability as s

def run_sched_test1_parallel(dataframe, task_sets, indices, num_procs = 1):
  start_time = time.time()
  with mp.Pool(processes = num_procs) as pool:
    sched_test_results = pool.map(s.schedulability_test_thm1, task_sets)
    for i, result in zip(indices, sched_test_results):
      dataframe.loc[i, "thm1"] = result
  end_time = time.time()
  print("Elapsed time {:.2f} s".format(end_time - start_time))

def run_sched_test1(dataframe, t_max_range = range(10), num_procs = 1):
  task_sets = [gt.Task_Set(ts_dict=row.to_dict()) for _, row in dataframe.iterrows() if row["t_max"] in t_max_range and row["thm1"] is None]
  indices = [index for index, row in dataframe.iterrows() if row["t_max"] in t_max_range and row["thm1"] is None]
  if len(task_sets) < 1: 
    print("All done for range {}".format(t_max_range))
    return
  run_sched_test1_parallel(dataframe, task_sets, indices, num_procs)

def run_sched_test23(dataframe, t_max_range = range(10)):
  for index, row in dataframe.iterrows():
    if row["t_max"] in t_max_range and row["thm2"] is None:
      task_set = gt.Task_Set(ts_dict=row.to_dict())
      dataframe.loc[index, "thm2"] = s.schedulability_test_thm2(task_set)
      dataframe.loc[index, "thm3"] = s.schedulability_test_thm3(task_set)

PROCESS_N = 10
TOTAL_COUNT = 10000
TARGET_U = 0.95
FILENAME = 'task_sets_{}_{}'.format(int(TARGET_U * 1000), TOTAL_COUNT)

df = ch.read_csv_to_dataframe(FILENAME).sort_values('t_max', ascending=True)

T_MAX_RANGES = [(int(df['t_max'].quantile(i/25)), int(df['t_max'].quantile((i+1)/25))) for i in range(0, 25)]

if __name__ == "__main__":
  print(df.describe())
  print(df['thm1'].isin([True]).sum(), df['thm1'].isin([False]).sum())
  print(df['thm2'].isin([True]).sum(), df['thm2'].isin([False]).sum())
  print(df['thm3'].isin([True]).sum(), df['thm3'].isin([False]).sum())
  print(T_MAX_RANGES)

  for i, j in T_MAX_RANGES:
    run_sched_test1(df, t_max_range = range(i, j), num_procs = PROCESS_N)
    run_sched_test23(df, t_max_range = range(i, j))
    version = int(time.time())
    updated_file = './{}/'.format(int(TARGET_U * 1000)) + FILENAME + '_v{}'.format(version)
    df.to_csv(updated_file + '.csv', index = False)