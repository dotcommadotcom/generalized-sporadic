import csv
import multiprocessing as mp
import time
import pandas as pd

import generate_tasks as gt

def process_task_sets(task_sets):
  return [{
            'num_tasks':      ts.num_tasks,
            't_max':          ts.t_max,
            'utilization':    ts.utilization,
            'thm1':           ts.thm1,
            'thm2':           ts.thm2,
            'thm3':           ts.thm3,
            'lo_tasks_list':  ts.lo_tasks_list,
            'hi_tasks_list':  ts.hi_tasks_list,
            } for ts in task_sets]

def write_header(filename, header):
  with open(filename + '.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()

def write_task_sets(filename, task_sets, header):
  with open(filename + '.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)

    for ts in task_sets:
      writer.writerow(ts)

def write_df(batch_size, total_count, filename, header, num_procs = 1, target_u_sums = [0.5], header_exists = False):
  if not header_exists: write_header(filename, header)
  current_length = 0
  total_elapsed_time = 0

  for u_sum in target_u_sums:
    for _ in range(total_count//batch_size):
      task_sets = [gt.generate_valid_task_set(u_sum) for _ in range(batch_size)]
      start_time = time.time()

      for ts in task_sets:
        ts.sched_test_thm1(num_procs)
        ts.sched_test_thm2(num_procs)
        ts.sched_test_thm3(num_procs)
      end_time = time.time()
      total_elapsed_time += end_time - start_time
      current_length += batch_size
      print("Elapsed time: total {:.2f}, current {:.2f} s, current length: {}".format(total_elapsed_time, end_time - start_time, current_length))
      
      task_sets_dict = process_task_sets(task_sets)
      write_task_sets(filename, task_sets_dict, header)
        
def parse_tasks(task_set_str):
  task_list = []
  for task_str in task_set_str.strip('[]').split('), '):
    task_attrs = [int(attr_str) for attr_str in task_str.strip('Task()').split(',')]
    task = gt.Task(*task_attrs)
    task_list.append(task)
  return task_list

def parse_row(row):
  return {
          'num_tasks':      int(row["num_tasks"]),
          't_max':          int(row["t_max"]),
          'utilization':    float(row["utilization"]),
          'thm1':           bool(row["thm1"]),
          'thm2':           bool(row["thm2"]),
          'thm3':           bool(row["thm3"]),
          'lo_tasks_list':  parse_tasks(row["lo_tasks_list"]),
          'hi_tasks_list':  parse_tasks(row["hi_tasks_list"])
          } 

def read_task_sets(filename, header):
  task_sets_db = []
  task_sets_df = pd.DataFrame(columns=header)
  with open(filename + '.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
      task_set_dict = parse_row(row)

      task_sets_db.append(gt.Task_Set(ts_dict=task_set_dict))
      task_sets_df = task_sets_df.append(task_set_dict, ignore_index=True)
  
  print("--------------------DB LENGTH {}---------------------".format(len(task_sets_db)))
  for tsdb in task_sets_db:
    print(tsdb)

  return task_sets_db, task_sets_df

PROCESS_N = mp.cpu_count()
COUNT_PER_USUM = 10000
HEADER = ['num_tasks', 't_max', 'utilization', 'thm1', 'thm2', 'thm3', 'lo_tasks_list', 'hi_tasks_list']
UTARGETS = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975]
FILENAME = 'database_{}'.format(COUNT_PER_USUM * len(UTARGETS))

if __name__ == "__main__":
  print("running..........")
  write_df(batch_size = 1, 
           total_count =   COUNT_PER_USUM, 
           filename =      FILENAME,
           header =        HEADER, 
           num_procs =     PROCESS_N, 
           target_u_sums = UTARGETS,
           header_exists = False)

  # task_sets_db, task_sets_df = read_task_sets(FILENAME, HEADER)

  # print(task_sets_df)

